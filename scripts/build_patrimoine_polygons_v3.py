#!/usr/bin/env python3
"""
Tellux Patrimoine sub-passe 3 : polygones rigoureux Convex Hull effectif.

Lit MAPPING_HIERARCHIE.csv (173 communes) + communes_corse.json (INSEE).
Geocodage centroides via geo.api.gouv.fr (cache local).
Calcule Convex Hulls (>=3 communes) + cercles fallback (1-2 communes) +
dioceses agreges (Convex Hull global communes du diocese).
Genere COMMUNES_GEOCODEES.json + PATRIMOINE_V0_POLYGONES_DEBUG_v3.json.
Replace bloc PATRIMOINE_POLYGONS dans patrimoine.html (ligne 162).

Usage: python scripts/build_patrimoine_polygons_v3.py
"""
import csv
import json
import math
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path

from scipy.spatial import ConvexHull

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "docs" / "_drafts"
MAPPING_CSV = DRAFTS / "MAPPING_HIERARCHIE.csv"
COMMUNES_INSEE_JSON = ROOT / "public" / "data" / "communes_corse.json"
COMMUNES_GEOCODEES_JSON = DRAFTS / "COMMUNES_GEOCODEES.json"
POLYGONES_DEBUG_V3_JSON = DRAFTS / "PATRIMOINE_V0_POLYGONES_DEBUG_v3.json"
PATRIMOINE_HTML = ROOT / "patrimoine.html"
SITES_MANIFEST_JSON = DRAFTS / "PATRIMOINE_V0_MANIFEST.json"
SPOT_OVERRIDES_JSON = DRAFTS / "SPOT_PIEVE_OVERRIDES.json"

LAT_MIN, LAT_MAX = 41.30, 43.10
LON_MIN, LON_MAX = 8.50, 9.65
MARGIN_DEG = 0.03
EXCLAVE_FACTOR = 2.0

ACCIA_PIEVES = {"bozio", "vallerustie", "rostino"}


def normalize_name(s: str) -> str:
    s = (s or "").strip().lower()
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    s = s.replace("'", "").replace("-", " ").replace(".", "")
    return " ".join(s.split())


def slug_pieve(name: str) -> str:
    return normalize_name(name).replace(" ", "_")


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    rlat1, rlat2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(rlat1) * math.cos(rlat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def point_in_polygon(lat, lon, poly):
    """Ray casting point-in-polygon. poly is list of [lat, lon] vertices."""
    n = len(poly)
    if n < 3:
        return False
    inside = False
    j = n - 1
    for i in range(n):
        lat_i, lon_i = poly[i][0], poly[i][1]
        lat_j, lon_j = poly[j][0], poly[j][1]
        if ((lon_i > lon) != (lon_j > lon)) and (
            lat < (lat_j - lat_i) * (lon - lon_i) / (lon_j - lon_i + 1e-15) + lat_i
        ):
            inside = not inside
        j = i
    return inside


def polygon_centroid(poly):
    """Approx centroid as mean of vertices. poly is list of [lat, lon]."""
    n = len(poly)
    if n == 0:
        return None
    return [sum(p[0] for p in poly) / n, sum(p[1] for p in poly) / n]


def bbox_ok(lat, lon):
    return LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX


def convex_hull_with_margin(points, margin=MARGIN_DEG):
    if len(points) < 3:
        return None
    pts_xy = [(p[1], p[0]) for p in points]
    try:
        hull = ConvexHull(pts_xy)
    except Exception as exc:
        print(f"    ! ConvexHull fail: {exc}")
        return None
    verts = [pts_xy[i] for i in hull.vertices]
    cx = sum(v[0] for v in verts) / len(verts)
    cy = sum(v[1] for v in verts) / len(verts)
    expanded = []
    for vx, vy in verts:
        dx, dy = vx - cx, vy - cy
        d = math.hypot(dx, dy)
        if d < 1e-9:
            expanded.append([round(vy, 5), round(vx, 5)])
            continue
        nx = vx + (dx / d) * margin
        ny = vy + (dy / d) * margin
        expanded.append([round(ny, 5), round(nx, 5)])
    return expanded


def circle_polygon(lat, lon, radius_km, n=24):
    R = 6371.0
    lat_rad = math.radians(lat)
    pts = []
    for i in range(n):
        theta = 2 * math.pi * i / n
        dlat = (radius_km / R) * math.cos(theta)
        dlon = (radius_km / (R * math.cos(lat_rad))) * math.sin(theta)
        pts.append([round(lat + math.degrees(dlat), 5), round(lon + math.degrees(dlon), 5)])
    return pts


def fetch_centre(insee_code: str):
    url = f"https://geo.api.gouv.fr/communes/{insee_code}?fields=centre,nom,code"
    req = urllib.request.Request(url, headers={"User-Agent": "Tellux-Patrimoine/sub-passe-3"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    # 1. Read mapping CSV
    mapping_all = []
    with open(MAPPING_CSV, encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            mapping_all.append(r)
    has_type_entite = "type_entite" in (mapping_all[0].keys() if mapping_all else [])
    print(f"[INFO] Loaded MAPPING_HIERARCHIE.csv: {len(mapping_all)} entries total")
    if not has_type_entite:
        print("[WARN] Column 'type_entite' missing — fallback to legacy behaviour (silent INSEE-match exclusion)")

    # 1b. Filter explicit by type_entite == 'commune_insee'
    if has_type_entite:
        mapping = [r for r in mapping_all if r.get("type_entite") == "commune_insee"]
        excluded_rows = [r for r in mapping_all if r.get("type_entite") != "commune_insee"]
    else:
        mapping = mapping_all
        excluded_rows = []

    excluded_by_type = defaultdict(list)
    for r in excluded_rows:
        t = r.get("type_entite") or "(empty)"
        excluded_by_type[t].append(r)

    if has_type_entite:
        print(f"[INFO] Filter by type_entite == 'commune_insee':")
        print(f"       - {len(mapping)} entries kept (commune_insee)")
        for t, rows in sorted(excluded_by_type.items()):
            names = ", ".join(r["commune_nom"] for r in rows)
            print(f"       - {len(rows)} entries excluded ({t}): {names}")
        print(f"[INFO] Polygon computation operates on {len(mapping)} commune_insee entries")
        # Editorial preservation log
        if excluded_rows:
            print("[INFO] Hameaux/lieux-dits preserved in CSV for editorial use:")
            for r in excluded_rows:
                print(f"       - {r['commune_nom']} -> pieve {r['pieve']} (type={r.get('type_entite')})")

    confidence_counts = defaultdict(int)
    for r in mapping:
        confidence_counts[r["confiance"]] += 1
    print(f"[1] Confiance (commune_insee only): {dict(confidence_counts)}")

    # 2. Read INSEE data
    with open(COMMUNES_INSEE_JSON, encoding="utf-8") as f:
        insee_data = json.load(f)
    insee_by_norm = {normalize_name(c["nom"]): c for c in insee_data["communes"]}
    print(f"[2] INSEE communes: {len(insee_by_norm)}")

    # 3. Match mapping -> INSEE
    matched_insee = {}
    unmatched = []
    for r in mapping:
        nom = r["commune_nom"]
        nom_clean = nom.split("(")[0].strip()
        key = normalize_name(nom_clean)
        if key in insee_by_norm:
            matched_insee[nom] = insee_by_norm[key]["code_insee"]
        else:
            unmatched.append(nom)
    print(f"[3] Matched INSEE: {len(matched_insee)}/{len(mapping)} (unmatched={len(unmatched)})")
    if unmatched:
        print(f"    Unmatched: {unmatched}")

    # 4. Load geocode cache
    geocodes = {}
    if COMMUNES_GEOCODEES_JSON.exists():
        with open(COMMUNES_GEOCODEES_JSON, encoding="utf-8") as f:
            geocodes = json.load(f)
        print(f"[4] Geocode cache: {len(geocodes)} entries")
    else:
        print("[4] No geocode cache yet")

    # 5. Geocode missing
    to_fetch = [(nom, code) for nom, code in matched_insee.items() if nom not in geocodes]
    print(f"[5] To fetch: {len(to_fetch)}")
    out_of_bbox = []
    fetch_fail = []
    for i, (nom, code) in enumerate(to_fetch, 1):
        try:
            d = fetch_centre(code)
            coords = d.get("centre", {}).get("coordinates", [])
            if not coords or len(coords) != 2:
                fetch_fail.append((nom, code, "no coordinates"))
                continue
            lon, lat = coords
            if not bbox_ok(lat, lon):
                out_of_bbox.append((nom, code, lat, lon))
                continue
            geocodes[nom] = {
                "lat": round(lat, 6),
                "lon": round(lon, 6),
                "insee": code,
                "source": "geo.api.gouv.fr",
            }
        except Exception as exc:
            fetch_fail.append((nom, code, str(exc)))
        if i % 20 == 0:
            print(f"    fetched {i}/{len(to_fetch)}")
        time.sleep(0.05)

    # 6. Save cache
    with open(COMMUNES_GEOCODEES_JSON, "w", encoding="utf-8") as f:
        json.dump(geocodes, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"[6] Saved {len(geocodes)} geocoded entries -> {COMMUNES_GEOCODEES_JSON.name}")
    if out_of_bbox:
        print(f"    out_of_bbox={out_of_bbox}")
    if fetch_fail:
        print(f"    fetch_fail={fetch_fail}")

    # 7. Group communes by pieve
    pieve_communes = defaultdict(list)
    pieve_diocese_csv = {}
    for r in mapping:
        nom, pieve, diocese, conf = r["commune_nom"], r["pieve"], r["diocese"], r["confiance"]
        if nom in geocodes and pieve:
            pieve_communes[pieve].append({
                "nom": nom,
                "lat": geocodes[nom]["lat"],
                "lon": geocodes[nom]["lon"],
                "confiance": conf,
            })
        if pieve and pieve not in pieve_diocese_csv:
            pieve_diocese_csv[pieve] = diocese
    print(f"[7] Pieves with >=1 geocoded commune: {len(pieve_communes)}")

    # Apply Accia bascule (Bozio/Vallerustie/Rostino -> Accia in pieve_diocese_csv)
    pieve_diocese = dict(pieve_diocese_csv)
    accia_bascule_log = []
    for slug in ACCIA_PIEVES:
        # Find pieve key by normalized slug match
        for p_csv, d_csv in pieve_diocese_csv.items():
            if slug_pieve(p_csv) == slug and d_csv != "Accia":
                pieve_diocese[p_csv] = "Accia"
                accia_bascule_log.append({"pieve": p_csv, "from": d_csv, "to": "Accia"})

    # 8. Compute pieve polygons
    pieves_out = {}
    exclaves_flagged = []
    for pieve, comms in pieve_communes.items():
        slug = slug_pieve(pieve)
        n = len(comms)
        diocese = pieve_diocese.get(pieve, "?")

        if n >= 3:
            points = [[c["lat"], c["lon"]] for c in comms]
            poly = convex_hull_with_margin(points)
            if poly is None:
                # Should not happen for n>=3 unique points, but guard
                clat = sum(c["lat"] for c in comms) / n
                clon = sum(c["lon"] for c in comms) / n
                poly = circle_polygon(clat, clon, 4.0)
                method = "circle_fallback_hull_failed"
            else:
                method = "convex_hull_effective"
                # Exclave detection
                clat = sum(c["lat"] for c in comms) / n
                clon = sum(c["lon"] for c in comms) / n
                dists = [(c, haversine_km(c["lat"], c["lon"], clat, clon)) for c in comms]
                mean_d = sum(d for _, d in dists) / n
                if mean_d > 0:
                    for c, d in dists:
                        if d > EXCLAVE_FACTOR * mean_d:
                            exclaves_flagged.append({
                                "pieve": pieve,
                                "commune": c["nom"],
                                "distance_km": round(d, 2),
                                "mean_distance_km": round(mean_d, 2),
                                "ratio": round(d / mean_d, 2),
                            })
            pieves_out[slug] = {
                "pieve": pieve,
                "diocese": diocese,
                "n_spots": 0,
                "n_communes": n,
                "communes": [c["nom"] for c in comms],
                "slugs": [],
                "method": method,
                "polygon": poly,
                "is_subpieve": False,
            }
        elif n == 2:
            lat = (comms[0]["lat"] + comms[1]["lat"]) / 2
            lon = (comms[0]["lon"] + comms[1]["lon"]) / 2
            d_km = haversine_km(comms[0]["lat"], comms[0]["lon"], comms[1]["lat"], comms[1]["lon"])
            r_km = d_km / 2 + 3.0
            poly = circle_polygon(lat, lon, r_km)
            pieves_out[slug] = {
                "pieve": pieve,
                "diocese": diocese,
                "n_spots": 0,
                "n_communes": n,
                "communes": [c["nom"] for c in comms],
                "slugs": [],
                "method": "circle_fallback_2communes",
                "centre": [round(lat, 5), round(lon, 5)],
                "rayon_km": round(r_km, 2),
                "polygon": poly,
                "is_subpieve": False,
            }
        elif n == 1:
            lat, lon = comms[0]["lat"], comms[0]["lon"]
            r_km = 5.0
            poly = circle_polygon(lat, lon, r_km)
            pieves_out[slug] = {
                "pieve": pieve,
                "diocese": diocese,
                "n_spots": 0,
                "n_communes": n,
                "communes": [c["nom"] for c in comms],
                "slugs": [],
                "method": "circle_fallback_1commune",
                "centre": [round(lat, 5), round(lon, 5)],
                "rayon_km": r_km,
                "polygon": poly,
                "is_subpieve": False,
            }

    # 9. Aggregate diocese polygons (Convex Hull on all communes of diocese)
    diocese_communes_by_d = defaultdict(list)
    diocese_pieves_by_d = defaultdict(set)
    for pieve, comms in pieve_communes.items():
        d = pieve_diocese.get(pieve)
        if d:
            diocese_communes_by_d[d].extend(comms)
            diocese_pieves_by_d[d].add(slug_pieve(pieve))

    dioceses_out = {}
    for d_name, comms in diocese_communes_by_d.items():
        if not comms:
            continue
        # Dedupe by commune name
        seen = set()
        uniq = []
        for c in comms:
            if c["nom"] not in seen:
                seen.add(c["nom"])
                uniq.append(c)
        n = len(uniq)
        n_pieves = len(diocese_pieves_by_d[d_name])
        if n >= 3:
            points = [[c["lat"], c["lon"]] for c in uniq]
            poly = convex_hull_with_margin(points, margin=MARGIN_DEG * 1.5)
            if poly is None:
                continue
            dioceses_out[d_name] = {
                "diocese": d_name,
                "n_pieves": n_pieves,
                "n_communes": n,
                "pieves": sorted(diocese_pieves_by_d[d_name]),
                "method": "convex_hull_aggregated_communes",
                "polygon": poly,
            }
        elif n >= 1:
            # Fallback circle
            clat = sum(c["lat"] for c in uniq) / n
            clon = sum(c["lon"] for c in uniq) / n
            dioceses_out[d_name] = {
                "diocese": d_name,
                "n_pieves": n_pieves,
                "n_communes": n,
                "pieves": sorted(diocese_pieves_by_d[d_name]),
                "method": "circle_fallback_diocese",
                "centre": [round(clat, 5), round(clon, 5)],
                "rayon_km": 8.0,
                "polygon": circle_polygon(clat, clon, 8.0),
            }

    # 9b. Post-filter pieve count validation
    pieve_count_validation = []
    for pieve, comms in pieve_communes.items():
        slug = slug_pieve(pieve)
        n_insee = len(comms)
        method = pieves_out.get(slug, {}).get("method", "n/a")
        viable = n_insee >= 3
        pieve_count_validation.append({
            "pieve": pieve,
            "n_communes_insee": n_insee,
            "method_applied": method,
            "convex_hull_viable": viable,
        })
    print(f"[9b] Pieve viability post-filter:")
    for v in sorted(pieve_count_validation, key=lambda x: (-x["n_communes_insee"], x["pieve"])):
        flag = "OK" if v["convex_hull_viable"] else "FALLBACK"
        print(f"     {v['pieve']:18s}  n_insee={v['n_communes_insee']:3d}  {v['method_applied']:30s}  {flag}")

    # 9c. Geographic spot <-> pieve attachment (UX-003 / UX-004)
    sites = []
    if SITES_MANIFEST_JSON.exists():
        with open(SITES_MANIFEST_JSON, encoding="utf-8") as f:
            sites = json.load(f)
        print(f"[9c] Loaded {len(sites)} sites from manifest")
    else:
        print(f"[9c] !! Sites manifest not found at {SITES_MANIFEST_JSON}, skipping spot attachment")

    overrides = {}
    if SPOT_OVERRIDES_JSON.exists():
        try:
            with open(SPOT_OVERRIDES_JSON, encoding="utf-8") as f:
                overrides_doc = json.load(f)
            overrides = overrides_doc.get("overrides", {}) if isinstance(overrides_doc, dict) else {}
            print(f"[9c] Loaded {len(overrides)} overrides from {SPOT_OVERRIDES_JSON.name}")
        except Exception as exc:
            print(f"[9c] !! overrides load failed: {exc}")

    # Pre-compute pieve centroids for tie-break on overlaps
    pieve_centroids = {}
    for slug, p in pieves_out.items():
        c = polygon_centroid(p.get("polygon", []))
        if c:
            pieve_centroids[slug] = c

    spot_to_pieve = {}        # spot_slug -> pieve_slug retained
    pieve_to_spots = defaultdict(list)
    spots_orphans = []
    spots_overlaps = []

    for site in sites:
        spot_slug = site.get("slug")
        lat = site.get("lat")
        lon = site.get("lon")
        if not spot_slug or lat is None or lon is None:
            continue
        # Override has highest priority
        if spot_slug in overrides:
            forced_slug = slug_pieve(overrides[spot_slug])
            if forced_slug in pieves_out:
                spot_to_pieve[spot_slug] = forced_slug
                pieve_to_spots[forced_slug].append(spot_slug)
                continue
        # Geometric containment in any pieve
        candidates = []
        for slug, p in pieves_out.items():
            poly = p.get("polygon", [])
            if poly and point_in_polygon(lat, lon, poly):
                candidates.append(slug)
        if not candidates:
            spots_orphans.append({"slug": spot_slug, "nom": site.get("nom"), "lat": lat, "lon": lon})
            continue
        if len(candidates) == 1:
            chosen = candidates[0]
        else:
            # Tie-break: nearest centroid
            best_slug, best_d = None, float("inf")
            for slug in candidates:
                c = pieve_centroids.get(slug)
                if c is None:
                    continue
                d = haversine_km(lat, lon, c[0], c[1])
                if d < best_d:
                    best_d, best_slug = d, slug
            chosen = best_slug or candidates[0]
            spots_overlaps.append({
                "slug": spot_slug, "nom": site.get("nom"),
                "candidates": sorted(candidates), "retained": chosen,
            })
        spot_to_pieve[spot_slug] = chosen
        pieve_to_spots[chosen].append(spot_slug)

    # Inject n_spots_geographic + spot_ids into pieves_out (alphabetical slug order)
    for slug, p in pieves_out.items():
        ids = sorted(pieve_to_spots.get(slug, []))
        p["n_spots_geographic"] = len(ids)
        p["spot_ids"] = ids
        # Keep legacy n_spots populated for retrocompat (= n_spots_geographic)
        p["n_spots"] = len(ids)

    # Aggregate diocese counts from child pieves (no double counting since spot_to_pieve assigns 1 pieve max)
    for d_name, d in dioceses_out.items():
        child_slugs = d.get("pieves", [])
        agg_ids = []
        for cs in child_slugs:
            agg_ids.extend(pieve_to_spots.get(cs, []))
        agg_ids = sorted(set(agg_ids))
        d["n_spots_geographic"] = len(agg_ids)
        d["spot_ids"] = agg_ids

    total_spots = len(sites)
    total_rattaches = len(spot_to_pieve)
    total_orphans = len(spots_orphans)
    print(f"[9c] Spots: total={total_spots}  rattaches={total_rattaches}  orphans={total_orphans}  overlaps={len(spots_overlaps)}")
    if total_rattaches + total_orphans != total_spots:
        print(f"[9c] !! coherence check FAIL: rattaches+orphans={total_rattaches+total_orphans} != total={total_spots}")
    # Filitosa sanity check (test ref UX-003)
    fil = spot_to_pieve.get("filitosa")
    if fil:
        print(f"[9c] Filitosa -> pieve {fil}  {'(OK Istria)' if fil == 'istria' else '(WARNING expected istria)'}")
    elif "filitosa" in {s.get('slug') for s in sites}:
        print(f"[9c] !! Filitosa is ORPHAN (expected in Istria hull)")

    # 10. Save debug JSON (v3.1 — adds excluded_entities + pieve_count_validation)
    methods_count = defaultdict(int)
    for v in pieves_out.values():
        methods_count[v["method"]] += 1

    excluded_entities = {}
    for t, rows in excluded_by_type.items():
        excluded_entities[t] = [
            {
                "commune_nom": r["commune_nom"],
                "pieve": r["pieve"],
                "diocese": r["diocese"],
                "note": r.get("note", ""),
            }
            for r in rows
        ]

    debug = {
        "version": "3.1",
        "date_generation": "2026-05-04",
        "mapping_source": f"MAPPING_HIERARCHIE.csv ({len(mapping_all)} lignes total)",
        "filter_applied": "type_entite == 'commune_insee'" if has_type_entite else "(legacy: silent INSEE-match exclusion)",
        "entries_total": len(mapping_all),
        "entries_kept": len(mapping),
        "entries_excluded": excluded_entities,
        "spots_attachment": {
            "total_spots": total_spots,
            "total_rattaches": total_rattaches,
            "total_orphans": total_orphans,
            "total_overlaps": len(spots_overlaps),
            "overrides_applied": len(overrides),
            "filitosa_pieve": spot_to_pieve.get("filitosa"),
        },
        "spots_orphans": spots_orphans,
        "spots_overlaps": spots_overlaps,
        "stats": {
            "total_communes_csv": len(mapping),
            "total_communes_geocoded": len(geocodes),
            "unmatched_insee": unmatched,
            "out_of_bbox": out_of_bbox,
            "fetch_failures": fetch_fail,
            "total_pieves_polygons": len(pieves_out),
            "total_dioceses_polygons": len(dioceses_out),
            "pieve_methods": dict(methods_count),
            "exclaves_count": len(exclaves_flagged),
            "accia_bascule": accia_bascule_log,
            "csv_confidence": dict(confidence_counts),
        },
        "pieve_count_validation": pieve_count_validation,
        "exclaves_flagged": exclaves_flagged,
        "polygones_dioceses": dioceses_out,
        "polygones_pieves": pieves_out,
    }
    with open(POLYGONES_DEBUG_V3_JSON, "w", encoding="utf-8") as f:
        json.dump(debug, f, ensure_ascii=False, indent=2)
    print(f"[10] Saved debug v3 -> {POLYGONES_DEBUG_V3_JSON.name}")

    # 11. Update patrimoine.html line 162 (PATRIMOINE_POLYGONS = ...)
    polygons_for_html = {
        "dioceses": {d: v for d, v in dioceses_out.items()},
        "pieves": {p: v for p, v in pieves_out.items()},
    }
    json_str = json.dumps(polygons_for_html, ensure_ascii=False, separators=(",", ":"))
    new_line = f"const PATRIMOINE_POLYGONS = {json_str};\n"

    with open(PATRIMOINE_HTML, encoding="utf-8") as f:
        lines = f.readlines()
    target_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().startswith("const PATRIMOINE_POLYGONS"):
            target_idx = i
            break
    if target_idx is None:
        print("!! could not find PATRIMOINE_POLYGONS line in patrimoine.html")
        return 1
    lines[target_idx] = new_line
    with open(PATRIMOINE_HTML, "w", encoding="utf-8", newline="") as f:
        f.writelines(lines)
    print(f"[11] Updated patrimoine.html line {target_idx + 1} (PATRIMOINE_POLYGONS)")

    # Summary
    print("\n=== SUMMARY ===")
    print(f"Geocoded: {len(geocodes)}/{len(mapping)} (unmatched_insee={len(unmatched)}, out_of_bbox={len(out_of_bbox)}, fetch_fail={len(fetch_fail)})")
    print(f"Pieves polygons: {len(pieves_out)}  methods={dict(methods_count)}")
    print(f"Dioceses polygons: {len(dioceses_out)}  ({list(dioceses_out.keys())})")
    print(f"Exclaves flagged: {len(exclaves_flagged)}")
    print(f"Accia bascule applied to: {[x['pieve'] for x in accia_bascule_log]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
