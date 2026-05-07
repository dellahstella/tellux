#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_gps_sites_patrimoine.py — Brief 34 audit GPS sites patrimoine.

Croise 3 sources publiques (OSM Nominatim, Wikidata SPARQL, IGN/Etalab
api-adresse.data.gouv.fr) pour valider/corriger les coordonnées des sites
patrimoine d'une phase donnée. Scoring HAUTE/MOYENNE/FAIBLE/ABSENT selon
nombre de sources concordantes et distance inter-sources.

Usage :
  python scripts/audit_gps_sites_patrimoine.py --phase A --list-only
  python scripts/audit_gps_sites_patrimoine.py --phase A --limit 5 --dry-run
  python scripts/audit_gps_sites_patrimoine.py --phase A --dry-run --reverse-geocode
  python scripts/audit_gps_sites_patrimoine.py --phase A --apply --reverse-geocode

Phases :
  A : Cap + Cortenais          (~96 sites)
  B : Plaine Orientale + Ajaccio
  C : Golo + Balagne
  D : Extrême-Sud + Piana-Vico-Sari
  E : Prunelli-Taravo-Valinco
  F : sites avec doyenne_contemporain_slug = null

Garde-fous :
  - User-Agent conforme OSM Nominatim usage policy.
  - Throttle 1.1 s entre requêtes (sécurité ≤ 1 req/s OSM).
  - Backup auto avant tout --apply.
  - Pas d'application si distance new/old > 5000 m (flag DIST_OVER_5000m).
  - Coords originales conservées dans le champ notes.
"""

import argparse
import csv
import json
import math
import re
import sys
import time
from datetime import date
from pathlib import Path

import requests

USER_AGENT = "Tellux-Audit-GPS/1.0 (contact: stelladluca@proton.me)"
THROTTLE = 1.1
TIMEOUT = 12
TODAY = date.today().isoformat()

ROOT = Path(__file__).resolve().parent.parent
SITES_PATH = ROOT / "docs" / "data" / "sites_patrimoine.json"
PIEVES_PATH = ROOT / "docs" / "data" / "pieves_polygons.json"
DOYENNES_PATH = ROOT / "docs" / "data" / "doyennes_polygons.json"
DRAFTS_DIR = ROOT / "_drafts"

PHASE_FILTERS = {
    "A": ["doyenne_du_cap", "doyenne_cortenais"],
    "B": ["doyenne_plaine_orientale", "doyenne_ajaccio"],
    "C": ["doyenne_du_golo", "doyenne_balagne"],
    "D": ["doyenne_extreme_sud", "doyenne_piana_vico_sari"],
    "E": ["doyenne_prunelli_taravo_valinco"],
    "F": [None],
}

CSV_FIELDS = [
    "slug", "name", "commune_nom",
    "old_lat", "old_lon", "new_lat", "new_lon", "distance_m",
    "confiance", "n_sources", "sources_used", "inter_max_m",
    "osm_match", "wikidata_match", "ign_match", "applied",
    "pieve_declared", "pieve_geocoded", "pieve_concordant",
    "doyenne_declared", "doyenne_geocoded", "doyenne_concordant",
    "note",
]


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def point_in_polygon(lat, lon, polygon):
    """Ray casting. polygon = [[lat, lng], ...]."""
    inside = False
    n = len(polygon)
    if n < 3:
        return False
    j = n - 1
    for i in range(n):
        yi, xi = polygon[i][0], polygon[i][1]
        yj, xj = polygon[j][0], polygon[j][1]
        if (yi > lat) != (yj > lat):
            denom = (yj - yi) if (yj - yi) != 0 else 1e-12
            if lon < (xj - xi) * (lat - yi) / denom + xi:
                inside = not inside
        j = i
    return inside


def filter_phase_sites(sites, phase):
    targets = PHASE_FILTERS[phase]
    out = []
    for s in sites:
        d = s.get("doyenne_contemporain_slug")
        if None in targets and d is None:
            out.append(s)
        elif d in targets:
            out.append(s)
    # Skip already audited
    out = [
        s for s in out
        if not s.get("gps_audit")
        or s.get("gps_audit") in ("pending", "a_auditer")
    ]
    return out


def http_get_json(url, params, retries=2):
    headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
            if r.status_code == 200:
                try:
                    return r.json()
                except ValueError:
                    return None
            if r.status_code in (429, 503):
                time.sleep(THROTTLE * (attempt + 2))
                continue
            return None
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(THROTTLE)
    return None


def query_osm(name, commune):
    url = "https://nominatim.openstreetmap.org/search"
    queries = []
    if commune:
        queries.append(f"{name}, {commune}, Corse, France")
    queries.append(f"{name}, Corse, France")
    queries.append(f"{name}, France")
    for q in queries:
        time.sleep(THROTTLE)
        # Nominatim refuse 'q' + paramètres structurés (country) ensemble : HTTP 400.
        # Le pays est inclus dans la chaîne libre.
        data = http_get_json(url, {"q": q, "format": "json", "limit": 5})
        if not data:
            continue
        # Chercher le 1er résultat dans la bbox Corse (filtrage post-fetch).
        for r in data:
            try:
                lat = float(r["lat"])
                lon = float(r["lon"])
                if 41.3 <= lat <= 43.1 and 8.5 <= lon <= 9.6:
                    return (lat, lon, r.get("display_name", "")[:80])
            except (KeyError, ValueError):
                continue
    return None


def query_wikidata(name):
    """Wikidata via wbsearchentities (sub-second) puis wbgetclaims P625.

    Bien plus rapide que SPARQL FILTER CONTAINS (qui peut prendre 30-60 s
    par requête sur les labels génériques).
    """
    api = "https://www.wikidata.org/w/api.php"
    # Étape 1 : recherche par nom (rapide, indexé).
    time.sleep(THROTTLE)
    search = http_get_json(api, {
        "action": "wbsearchentities",
        "search": name,
        "language": "fr",
        "uselang": "fr",
        "format": "json",
        "limit": 3,
        "type": "item",
    })
    if not search or not search.get("search"):
        return None
    # Étape 2 : pour chaque candidat, récupérer P625 (coordinate location).
    for item in search["search"][:3]:
        qid = item.get("id")
        if not qid:
            continue
        time.sleep(THROTTLE)
        claims = http_get_json(api, {
            "action": "wbgetclaims",
            "entity": qid,
            "property": "P625",
            "format": "json",
        })
        if not claims:
            continue
        p625_list = claims.get("claims", {}).get("P625", [])
        for c in p625_list:
            try:
                val = c["mainsnak"]["datavalue"]["value"]
                lat = float(val["latitude"])
                lon = float(val["longitude"])
                if 41.3 <= lat <= 43.1 and 8.5 <= lon <= 9.6:
                    return (lat, lon, qid + " " + (item.get("label") or "")[:60])
            except (KeyError, TypeError, ValueError):
                continue
    return None


def query_ign(name, commune):
    url = "https://api-adresse.data.gouv.fr/search/"
    q = f"{name} {commune}".strip() if commune else name
    time.sleep(THROTTLE)
    data = http_get_json(url, {"q": q, "limit": 3})
    if not data:
        return None
    for feat in data.get("features", []):
        coords = feat.get("geometry", {}).get("coordinates")
        if coords and len(coords) >= 2:
            try:
                lon, lat = float(coords[0]), float(coords[1])
                if 41.3 <= lat <= 43.1 and 8.5 <= lon <= 9.6:
                    label = feat.get("properties", {}).get("label", "")
                    return (lat, lon, label[:80])
            except (ValueError, TypeError):
                continue
    return None


def best_cluster(coords_list, threshold_m):
    """Trouve le plus grand sous-ensemble dont toutes les paires sont à
    moins de `threshold_m`. Retourne la liste des indices.
    """
    if not coords_list:
        return []
    n = len(coords_list)
    best = [0]
    for i in range(n):
        cluster = [i]
        for j in range(n):
            if j == i:
                continue
            ok = True
            for k in cluster:
                d = haversine(coords_list[k][0], coords_list[k][1],
                              coords_list[j][0], coords_list[j][1])
                if d >= threshold_m:
                    ok = False
                    break
            if ok:
                cluster.append(j)
        if len(cluster) > len(best):
            best = cluster
    return best


def compute_confidence(coords_list):
    """Score basé sur cluster (et non inter_max global), tolère un outlier
    parmi 3 sources. inter_max retourné = diamètre du cluster retenu.
    """
    n = len(coords_list)
    if n == 0:
        return ("ABSENT", 0, 0.0, [])
    if n == 1:
        return ("FAIBLE", 1, 0.0, [0])
    # Tente d'abord cluster strict <100m (HAUTE).
    haute = best_cluster(coords_list, 100)
    if len(haute) >= 3:
        return ("HAUTE", 3, _diameter(coords_list, haute), haute)
    # Cluster <500m (MOYENNE), au moins 2 sources concordantes.
    moy = best_cluster(coords_list, 500)
    if len(moy) >= 2:
        # HAUTE si cluster moy >=3 même si pas <100m (souvent IGN+OSM+WD à <500m)
        if len(moy) >= 3:
            return ("HAUTE", 3, _diameter(coords_list, moy), moy)
        return ("MOYENNE", len(moy), _diameter(coords_list, moy), moy)
    # Aucune concordance : 1 source isolée → FAIBLE.
    return ("FAIBLE", n, _diameter(coords_list, list(range(n))), [])


def _diameter(coords_list, idxs):
    if len(idxs) < 2:
        return 0.0
    md = 0.0
    for i in idxs:
        for j in idxs:
            if i >= j:
                continue
            d = haversine(coords_list[i][0], coords_list[i][1],
                          coords_list[j][0], coords_list[j][1])
            if d > md:
                md = d
    return md


def median_coord(coords_list, idxs=None):
    """Médiane sur un sous-ensemble si `idxs` fourni, sinon sur tout."""
    pool = coords_list if not idxs else [coords_list[i] for i in idxs]
    if not pool:
        return (None, None)
    lats = sorted(c[0] for c in pool)
    lons = sorted(c[1] for c in pool)
    n = len(lats)
    if n % 2 == 1:
        return (lats[n // 2], lons[n // 2])
    return (
        (lats[n // 2 - 1] + lats[n // 2]) / 2,
        (lons[n // 2 - 1] + lons[n // 2]) / 2,
    )


def reverse_geocode(lat, lon, polys_dict):
    for slug, poly in polys_dict.items():
        try:
            if point_in_polygon(lat, lon, poly):
                return slug
        except Exception:
            continue
    return ""


def audit_one_site(site, reverse_geo, pieves_polys, doyennes_polys):
    name = site.get("name", "")
    commune = site.get("commune_nom") or ""
    old_lat = site.get("lat")
    old_lon = site.get("lon")

    coords = []
    sources = []
    osm_m = wd_m = ign_m = ""

    r_osm = query_osm(name, commune)
    if r_osm:
        coords.append((r_osm[0], r_osm[1]))
        sources.append("osm")
        osm_m = f"{r_osm[0]:.5f},{r_osm[1]:.5f}"

    r_wd = query_wikidata(name)
    if r_wd:
        coords.append((r_wd[0], r_wd[1]))
        sources.append("wikidata")
        wd_m = f"{r_wd[0]:.5f},{r_wd[1]:.5f}"

    r_ign = query_ign(name, commune)
    if r_ign:
        coords.append((r_ign[0], r_ign[1]))
        sources.append("ign")
        ign_m = f"{r_ign[0]:.5f},{r_ign[1]:.5f}"

    confidence, n_sources, inter_max, cluster_idx = compute_confidence(coords)
    # Médiane sur le cluster retenu si MOYENNE/HAUTE, sinon sur tout (FAIBLE).
    new_lat, new_lon = median_coord(coords, cluster_idx if cluster_idx else None)
    dist = None
    if new_lat is not None and old_lat is not None and old_lon is not None:
        dist = haversine(old_lat, old_lon, new_lat, new_lon)

    pieve_geo = doyenne_geo = ""
    pieve_concord = doyenne_concord = ""
    if reverse_geo and new_lat is not None:
        pieve_geo = reverse_geocode(new_lat, new_lon, pieves_polys)
        doyenne_geo = reverse_geocode(new_lat, new_lon, doyennes_polys)
        pieve_decl = site.get("pieve_slug") or ""
        doy_decl = site.get("doyenne_contemporain_slug") or ""
        if pieve_geo:
            pieve_concord = "True" if pieve_geo == pieve_decl else "False"
        else:
            pieve_concord = "?"
        if doyenne_geo:
            doyenne_concord = "True" if doyenne_geo == doy_decl else "False"
        else:
            doyenne_concord = "?"

    note = ""
    if dist is not None and dist > 5000:
        note = "DIST_OVER_5000m"

    return {
        "slug": site["slug"], "name": name, "commune_nom": commune,
        "old_lat": old_lat, "old_lon": old_lon,
        "new_lat": f"{new_lat:.5f}" if new_lat is not None else "",
        "new_lon": f"{new_lon:.5f}" if new_lon is not None else "",
        "distance_m": f"{dist:.1f}" if dist is not None else "",
        "confiance": confidence, "n_sources": n_sources,
        "sources_used": "+".join(sources), "inter_max_m": f"{inter_max:.1f}",
        "osm_match": osm_m, "wikidata_match": wd_m, "ign_match": ign_m,
        "applied": "",
        "pieve_declared": site.get("pieve_slug") or "",
        "pieve_geocoded": pieve_geo,
        "pieve_concordant": pieve_concord,
        "doyenne_declared": site.get("doyenne_contemporain_slug") or "",
        "doyenne_geocoded": doyenne_geo,
        "doyenne_concordant": doyenne_concord,
        "note": note,
    }


def write_csv(rows, csv_path):
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(rows)


def is_tier1_eligible(row):
    """Filtre élargi pour --apply (Brief 34 Phase A revue automatisée).

    Tier 1 = éligible apply automatique :
      - HAUTE/MOYENNE non flaggé DIST_OVER_5000m
      - FAIBLE 1 source IGN avec concord pieve+doyenné OK et dist<1km
      - FAIBLE 2+ sources avec concord OK et dist<2km
    """
    if "DIST_OVER_5000m" in (row.get("note") or ""):
        return False
    if not row.get("new_lat") or not row.get("new_lon"):
        return False
    conf = row.get("confiance")
    if conf in ("HAUTE", "MOYENNE"):
        return True
    if conf == "FAIBLE":
        try:
            dist = float(row.get("distance_m") or 1e9)
            n_src = int(row.get("n_sources") or 0)
        except ValueError:
            return False
        pieve_ok = row.get("pieve_concordant") == "True"
        doy_ok = row.get("doyenne_concordant") == "True"
        if not (pieve_ok and doy_ok):
            return False
        sources = row.get("sources_used") or ""
        # H1 : 1 source IGN, dist<1km
        if n_src == 1 and "ign" in sources and dist < 1000:
            return True
        # H2 : 2+ sources, dist<2km
        if n_src >= 2 and dist < 2000:
            return True
    return False


def apply_updates(rows, sites_data):
    """Met à jour sites_patrimoine.json en place. Retourne (applied, skipped_far)."""
    idx = {s["slug"]: s for s in sites_data["sites"]}
    applied = 0
    skipped_far = 0
    for row in rows:
        if row.get("note") == "DIST_OVER_5000m":
            skipped_far += 1
            continue
        if not is_tier1_eligible(row):
            continue
        site = idx.get(row["slug"])
        if not site:
            continue
        # Idempotency : si ce site a déjà été audité aujourd'hui avec les mêmes
        # coords, ne pas re-empiler une 2ème note ni re-écrire.
        if site.get("gps_audit") == TODAY:
            try:
                if abs(float(site.get("lat", 0)) - float(row["new_lat"])) < 1e-6 and \
                   abs(float(site.get("lon", 0)) - float(row["new_lon"])) < 1e-6:
                    row["applied"] = "AlreadyApplied"
                    continue
            except (ValueError, TypeError):
                pass
        orig_note = site.get("notes") or ""
        prefix = (orig_note + " | ") if orig_note else ""
        site["notes"] = (
            prefix + f"gps_audit_{TODAY[:7]}: orig=({row['old_lat']}, {row['old_lon']})"
        )
        site["lat"] = float(row["new_lat"])
        site["lon"] = float(row["new_lon"])
        site["gps_audit"] = TODAY
        site["gps_source"] = row["sources_used"]
        applied += 1
        row["applied"] = "True"
    return applied, skipped_far


def load_rows_from_csv(csv_path):
    """Charge les rows d'un CSV existant (mode --from-csv, skip réseau)."""
    with csv_path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rescue_orphans(sites_data, pieves_polys, doyennes_polys):
    """Brief 36 R6 — tente de rescue les sites _orphan_brief35: true.

    Pour chaque orphan : essaie nom original + 2-3 variantes via OSM, Wikidata,
    IGN. Garde la 1ère variante qui produit ≥1 source. Reverse-geocode pour
    déterminer pieve/doyenne. Considère SUCCESS si le nouveau point tombe dans
    une pieve Corse (point-in-polygon valide).

    Retourne (rows_csv, n_rescued).
    """
    orphans = [s for s in sites_data["sites"] if s.get("_orphan_brief35")]
    print(f"[rescue] {len(orphans)} sites _orphan_brief35 à rescue")
    rows = []
    n_rescued = 0
    for i, site in enumerate(orphans, 1):
        slug = site["slug"]
        name = site.get("name") or ""
        commune = site.get("commune_nom") or ""
        old_lat = site.get("lat")
        old_lon = site.get("lon")
        print(f"  [{i:>2}/{len(orphans)}] {slug:<48} | {name[:48]}")
        # Variantes : nom original + retours name_variants()
        all_variants = [name] + name_variants(name)
        # Dédoublonne en préservant l'ordre
        seen = set()
        all_variants = [v for v in all_variants if v and not (v in seen or seen.add(v))]

        coords = []
        sources = []
        osm_m = wd_m = ign_m = ""
        used_variant = ""
        for v in all_variants[:4]:  # max 4 variantes
            if not osm_m:
                r_osm = query_osm(v, commune)
                if r_osm:
                    coords.append((r_osm[0], r_osm[1])); sources.append("osm")
                    osm_m = f"{r_osm[0]:.5f},{r_osm[1]:.5f}"
                    used_variant = used_variant or v
            if not wd_m:
                r_wd = query_wikidata(v)
                if r_wd:
                    coords.append((r_wd[0], r_wd[1])); sources.append("wikidata")
                    wd_m = f"{r_wd[0]:.5f},{r_wd[1]:.5f}"
                    used_variant = used_variant or v
            if not ign_m:
                r_ign = query_ign(v, commune)
                if r_ign:
                    coords.append((r_ign[0], r_ign[1])); sources.append("ign")
                    ign_m = f"{r_ign[0]:.5f},{r_ign[1]:.5f}"
                    used_variant = used_variant or v
            if osm_m and wd_m and ign_m:
                break  # 3 sources OK, pas besoin de plus de variantes
            if osm_m or wd_m or ign_m:
                # Au moins 1 source : on tente quand même les autres variantes
                # mais sans abandonner.
                pass

        if not coords:
            rows.append({
                "slug": slug, "name": name, "commune_nom": commune,
                "old_lat": old_lat, "old_lon": old_lon,
                "new_lat": "", "new_lon": "", "distance_m": "",
                "confiance": "ABSENT", "n_sources": 0, "sources_used": "",
                "inter_max_m": "", "osm_match": "", "wikidata_match": "", "ign_match": "",
                "applied": "", "pieve_declared": site.get("pieve_slug") or "",
                "pieve_geocoded": "", "pieve_concordant": "?",
                "doyenne_declared": site.get("doyenne_contemporain_slug") or "",
                "doyenne_geocoded": "", "doyenne_concordant": "?",
                "note": "RESCUE_ABSENT",
            })
            continue

        confidence, n_sources, inter_max, cluster_idx = compute_confidence(coords)
        new_lat, new_lon = median_coord(coords, cluster_idx if cluster_idx else None)
        dist = ""
        if old_lat is not None and old_lon is not None:
            dist = haversine(old_lat, old_lon, new_lat, new_lon)

        # Reverse-geocode : pieve/doyenne contenant la nouvelle coord
        pieve_geo = reverse_geocode(new_lat, new_lon, pieves_polys)
        doyenne_geo = reverse_geocode(new_lat, new_lon, doyennes_polys)

        is_in_corsica = bool(pieve_geo or doyenne_geo)
        pieve_decl = site.get("pieve_slug") or ""
        homonym_risk = (
            pieve_decl and pieve_geo and pieve_decl != pieve_geo
            and dist != "" and dist > 5000
        )
        # Garde-fous Brief 36 R6 (renforcés post audit dry-run) :
        #  - Très proche (<1km) : accept même hors polygone (cas îlots/sites
        #    côtiers comme Giraglia, plage de l'extrême nord, etc.)
        #  - Sinon dans Corse + ≥2 sources concord (ou HAUTE/MOYENNE)
        #  - Reject si homonyme (pieve_geo ≠ pieve_decl ET dist >5km)
        success = False
        if dist != "" and dist < 1000:
            success = True  # très proche, peu importe le polygone
        elif homonym_risk:
            success = False
        elif is_in_corsica and confidence in ("HAUTE", "MOYENNE"):
            success = True
        elif is_in_corsica and confidence == "FAIBLE" and n_sources >= 2:
            success = True

        note = "RESCUE_OK" if success else "RESCUE_REJECTED"
        if not is_in_corsica and dist != "" and dist >= 1000:
            note += "_HORS_CORSE"
        if homonym_risk:
            note += f"_HOMONYM_pieve_decl={pieve_decl}_vs_geo={pieve_geo}"
        if used_variant != name:
            note += f" | VARIANT:{used_variant}"

        rows.append({
            "slug": slug, "name": name, "commune_nom": commune,
            "old_lat": f"{old_lat:.5f}" if old_lat else "",
            "old_lon": f"{old_lon:.5f}" if old_lon else "",
            "new_lat": f"{new_lat:.5f}", "new_lon": f"{new_lon:.5f}",
            "distance_m": f"{dist:.1f}" if dist else "",
            "confiance": confidence, "n_sources": n_sources,
            "sources_used": "+".join(sources), "inter_max_m": f"{inter_max:.1f}",
            "osm_match": osm_m, "wikidata_match": wd_m, "ign_match": ign_m,
            "applied": "",
            "pieve_declared": site.get("pieve_slug") or "",
            "pieve_geocoded": pieve_geo or "",
            "pieve_concordant": "True" if pieve_geo else "?",
            "doyenne_declared": site.get("doyenne_contemporain_slug") or "",
            "doyenne_geocoded": doyenne_geo or "",
            "doyenne_concordant": "True" if doyenne_geo else "?",
            "note": note,
        })
        if success:
            n_rescued += 1

    return rows, n_rescued


def apply_rescue(rows, sites_data):
    """Apply rescue : pour les sites RESCUE_OK, met à jour lat/lon, pieve/doyenne,
    retire le flag _orphan_brief35. Retourne n_applied."""
    idx = {s["slug"]: s for s in sites_data["sites"]}
    n_applied = 0
    for row in rows:
        if not row.get("note", "").startswith("RESCUE_OK"):
            continue
        site = idx.get(row["slug"])
        if not site:
            continue
        try:
            new_lat = float(row["new_lat"]); new_lon = float(row["new_lon"])
        except (ValueError, TypeError):
            continue
        orig_note = site.get("notes") or ""
        prefix = (orig_note + " | ") if orig_note else ""
        site["notes"] = (
            prefix + f"gps_rescue_{TODAY[:7]}: orig=({row['old_lat']}, {row['old_lon']})"
        )
        site["lat"] = new_lat
        site["lon"] = new_lon
        site["gps_audit"] = TODAY
        site["gps_source"] = row["sources_used"] + "+rescue"
        # Mise à jour pieve/doyenne depuis reverse-geocode
        if row.get("pieve_geocoded"):
            site["pieve_slug"] = row["pieve_geocoded"]
        if row.get("doyenne_geocoded"):
            site["doyenne_contemporain_slug"] = row["doyenne_geocoded"]
        # Retrait du flag orphan
        site.pop("_orphan_brief35", None)
        row["applied"] = "True"
        n_applied += 1
    return n_applied


def name_variants(name):
    """Génère 2-3 variantes orthographiques pour les sites ABSENT.

    Stratégie :
      1. Strip parenthèses désambiguïsantes : "San Giovanni (Bastia haute)" -> "San Giovanni"
      2. Strip suffixes locatifs : "Santa Maria (Bocognano haute)" -> "Santa Maria"
      3. Variante FR du préfixe corse : "San" -> "Saint", "Santa" -> "Sainte"
    Retourne max 3 variantes uniques, name original exclu (ce sont des retries).
    """
    out = []
    seen = {name}
    # Strip parens
    no_paren = re.sub(r"\s*\([^)]*\)", "", name).strip()
    no_paren = re.sub(r"\s+", " ", no_paren)
    if no_paren and no_paren not in seen:
        out.append(no_paren); seen.add(no_paren)
    # Strip suffixes locatifs même hors parens
    base = no_paren or name
    cleaned = re.sub(
        r"\b(haute|basse|village|ville|bas|haut|disparu|détruit|intérieur|versant|plage|station|littoral)\b",
        "", base, flags=re.IGNORECASE
    ).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    if cleaned and cleaned not in seen:
        out.append(cleaned); seen.add(cleaned)
    # San/Santa -> Saint/Sainte
    fr = base
    fr = re.sub(r"\bSantu\b", "Saint", fr)
    fr = re.sub(r"\bSan\b(?!\s*[A-Z][a-z]+ed)", "Saint", fr)  # naive but works
    fr = re.sub(r"\bSanta\b", "Sainte", fr)
    fr = re.sub(r"\bSant[''']", "Saint-", fr)
    fr = re.sub(r"\s+", " ", fr).strip()
    if fr and fr not in seen:
        out.append(fr); seen.add(fr)
    return out[:3]


def retry_absent(rows, sites_data, pieves_polys, doyennes_polys):
    """Re-tente les sites ABSENT du CSV avec des variantes orthographiques.

    Modifie rows en place. Retourne (n_retried, n_recovered).
    """
    sites_by_slug = {s["slug"]: s for s in sites_data["sites"]}
    n_retried = 0
    n_recovered = 0
    for row in rows:
        if row.get("confiance") != "ABSENT":
            continue
        slug = row.get("slug")
        site = sites_by_slug.get(slug)
        if not site:
            continue
        variants = name_variants(site.get("name", ""))
        if not variants:
            continue
        n_retried += 1
        commune = site.get("commune_nom") or ""
        # Tente chaque variante jusqu'à trouver une source.
        coords = []
        sources = []
        osm_m = wd_m = ign_m = ""
        used_variant = ""
        for v in variants:
            r_osm = query_osm(v, commune)
            if r_osm and not osm_m:
                coords.append((r_osm[0], r_osm[1])); sources.append("osm")
                osm_m = f"{r_osm[0]:.5f},{r_osm[1]:.5f}"
                used_variant = v
            r_wd = query_wikidata(v)
            if r_wd and not wd_m:
                coords.append((r_wd[0], r_wd[1])); sources.append("wikidata")
                wd_m = f"{r_wd[0]:.5f},{r_wd[1]:.5f}"
                used_variant = v
            r_ign = query_ign(v, commune)
            if r_ign and not ign_m:
                coords.append((r_ign[0], r_ign[1])); sources.append("ign")
                ign_m = f"{r_ign[0]:.5f},{r_ign[1]:.5f}"
                used_variant = v
            if coords:
                break  # 1ère variante qui marche suffit
        if not coords:
            continue
        confidence, n_sources, inter_max, cluster_idx = compute_confidence(coords)
        new_lat, new_lon = median_coord(coords, cluster_idx if cluster_idx else None)
        old_lat = site.get("lat"); old_lon = site.get("lon")
        dist = None
        if new_lat is not None and old_lat is not None and old_lon is not None:
            dist = haversine(old_lat, old_lon, new_lat, new_lon)
        # Reverse geocode
        pieve_geo = doyenne_geo = ""
        pieve_concord = doyenne_concord = ""
        if new_lat is not None:
            pieve_geo = reverse_geocode(new_lat, new_lon, pieves_polys)
            doyenne_geo = reverse_geocode(new_lat, new_lon, doyennes_polys)
            pieve_decl = site.get("pieve_slug") or ""
            doy_decl = site.get("doyenne_contemporain_slug") or ""
            if pieve_geo:
                pieve_concord = "True" if pieve_geo == pieve_decl else "False"
            else:
                pieve_concord = "?"
            if doyenne_geo:
                doyenne_concord = "True" if doyenne_geo == doy_decl else "False"
            else:
                doyenne_concord = "?"
        note = "RETRY_VARIANT:" + used_variant
        if dist is not None and dist > 5000:
            note = "DIST_OVER_5000m | " + note
        # Update row in place
        row["new_lat"] = f"{new_lat:.5f}" if new_lat is not None else ""
        row["new_lon"] = f"{new_lon:.5f}" if new_lon is not None else ""
        row["distance_m"] = f"{dist:.1f}" if dist is not None else ""
        row["confiance"] = confidence
        row["n_sources"] = n_sources
        row["sources_used"] = "+".join(sources)
        row["inter_max_m"] = f"{inter_max:.1f}"
        row["osm_match"] = osm_m
        row["wikidata_match"] = wd_m
        row["ign_match"] = ign_m
        row["pieve_geocoded"] = pieve_geo
        row["pieve_concordant"] = pieve_concord
        row["doyenne_geocoded"] = doyenne_geo
        row["doyenne_concordant"] = doyenne_concord
        row["note"] = note
        n_recovered += 1
    return n_retried, n_recovered


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", required=False, default=None, choices=list(PHASE_FILTERS.keys()),
                        help="Phase A-F (requis sauf en mode --rescue-orphans).")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limite le nombre de sites traités (sanity check).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Génère le CSV sans modifier le JSON.")
    parser.add_argument("--apply", action="store_true",
                        help="Applique les MAJ HAUTE/MOYENNE au JSON (avec backup).")
    parser.add_argument("--reverse-geocode", action="store_true",
                        help="Vérifie pieve/doyenné via point-in-polygon.")
    parser.add_argument("--list-only", action="store_true",
                        help="Affiche les slugs cibles sans appel réseau.")
    parser.add_argument("--from-csv", type=Path, default=None,
                        help="Charge les rows d'un CSV existant (skip réseau, utile pour --apply après un --dry-run).")
    parser.add_argument("--retry-absent", type=Path, default=None,
                        help="CSV existant : retry les sites ABSENT avec variantes orthographiques (strip parens, San->Saint, etc.).")
    parser.add_argument("--rescue-orphans", action="store_true",
                        help="Brief 36 R6 : tente de rescue les sites avec _orphan_brief35=true via OSM/Wikidata/IGN + variantes ortho. Avec --apply, met à jour lat/lon, pieve/doyenne, retire le flag orphan.")
    args = parser.parse_args()

    if args.apply and args.dry_run:
        print("ERROR: --apply et --dry-run mutuellement exclusifs", file=sys.stderr)
        return 2

    with SITES_PATH.open(encoding="utf-8") as f:
        sites_data = json.load(f)

    if not args.rescue_orphans and not args.phase:
        print("ERROR: --phase est requis (sauf en mode --rescue-orphans)", file=sys.stderr)
        return 2

    targets = filter_phase_sites(sites_data["sites"], args.phase) if args.phase else []
    if args.limit:
        targets = targets[:args.limit]

    if args.list_only:
        print(f"[Phase {args.phase}] {len(targets)} sites cibles :")
        for s in targets:
            doy = s.get("doyenne_contemporain_slug") or "(null)"
            commune = s.get("commune_nom") or "-"
            name = (s.get("name") or "")[:40]
            print(f"  {s['slug']:<48} | {name:<40} | {commune:<22} | {doy}")
        return 0

    # Mode --retry-absent : recharge un CSV existant, re-tente les ABSENT
    # avec variantes orthographiques, ré-écrit le CSV. Implique reverse-geocode.
    if args.retry_absent:
        if not args.retry_absent.exists():
            print(f"ERROR: CSV {args.retry_absent} introuvable", file=sys.stderr)
            return 2
        rows = load_rows_from_csv(args.retry_absent)
        # Charge polygons reverse
        with PIEVES_PATH.open(encoding="utf-8") as f:
            pdata = json.load(f)
        pieves_polys = {p["slug"]: p["polygon"] for p in pdata.get("pieves", []) if p.get("polygon")}
        with DOYENNES_PATH.open(encoding="utf-8") as f:
            ddata = json.load(f)
        doyennes_polys = {d["slug"]: d["polygon"] for d in ddata.get("doyennes", []) if d.get("polygon")}
        absent_count = sum(1 for r in rows if r.get("confiance") == "ABSENT")
        print(f"[retry-absent] {absent_count} sites ABSENT à retry dans {args.retry_absent}")
        n_retried, n_recovered = retry_absent(rows, sites_data, pieves_polys, doyennes_polys)
        write_csv(rows, args.retry_absent)
        new_conf = {}
        for r in rows:
            new_conf[r.get("confiance", "ABSENT")] = new_conf.get(r.get("confiance", "ABSENT"), 0) + 1
        print(f"[retry-absent] {n_retried} retried, {n_recovered} recovered (au moins 1 source trouvée)")
        print(f"[Counts post-retry] HAUTE={new_conf.get('HAUTE',0)} | MOYENNE={new_conf.get('MOYENNE',0)} | FAIBLE={new_conf.get('FAIBLE',0)} | ABSENT={new_conf.get('ABSENT',0)}")
        if args.apply:
            backup_path = DRAFTS_DIR / f"sites_patrimoine.backup_{TODAY}.json"
            if not backup_path.exists():
                with backup_path.open("w", encoding="utf-8") as f:
                    json.dump(sites_data, f, ensure_ascii=False, indent=2)
                print(f"[Backup] {backup_path}")
            applied, skipped = apply_updates(rows, sites_data)
            with SITES_PATH.open("w", encoding="utf-8") as f:
                json.dump(sites_data, f, ensure_ascii=False, indent=2)
            write_csv(rows, args.retry_absent)
            print(f"[Apply] {applied} sites mis à jour | {skipped} skip (DIST_OVER_5000m)")
        return 0

    # Mode --rescue-orphans : Brief 36 R6, tente de récupérer les coords des
    # sites avec _orphan_brief35: true via OSM/Wikidata/IGN + variantes ortho.
    if args.rescue_orphans:
        with PIEVES_PATH.open(encoding="utf-8") as f:
            pdata = json.load(f)
        pieves_polys = {p["slug"]: p["polygon"] for p in pdata.get("pieves", []) if p.get("polygon")}
        with DOYENNES_PATH.open(encoding="utf-8") as f:
            ddata = json.load(f)
        doyennes_polys = {d["slug"]: d["polygon"] for d in ddata.get("doyennes", []) if d.get("polygon")}
        rows, n_rescued = rescue_orphans(sites_data, pieves_polys, doyennes_polys)
        out_csv = DRAFTS_DIR / f"audit_gps_rescue_{TODAY}.csv"
        write_csv(rows, out_csv)
        print(f"[rescue] CSV {out_csv}")
        ok = sum(1 for r in rows if r.get("note", "").startswith("RESCUE_OK"))
        rejected = sum(1 for r in rows if r.get("note", "").startswith("RESCUE_REJECTED"))
        absent = sum(1 for r in rows if r.get("note") == "RESCUE_ABSENT")
        print(f"[Counts] RESCUE_OK={ok} | RESCUE_REJECTED={rejected} | RESCUE_ABSENT={absent}")
        if args.apply:
            backup_path = DRAFTS_DIR / f"sites_patrimoine.backup_rescue_{TODAY}.json"
            if not backup_path.exists():
                with backup_path.open("w", encoding="utf-8") as f:
                    json.dump(sites_data, f, ensure_ascii=False, indent=2)
                print(f"[Backup] {backup_path}")
            n_applied = apply_rescue(rows, sites_data)
            with SITES_PATH.open("w", encoding="utf-8") as f:
                json.dump(sites_data, f, ensure_ascii=False, indent=2)
            write_csv(rows, out_csv)
            print(f"[Apply] {n_applied} sites rescued (lat/lon + pieve + doyenne MAJ, flag _orphan_brief35 retiré)")
        return 0

    # Mode --from-csv : skip réseau, charge les rows existants et applique direct.
    if args.from_csv:
        if not args.from_csv.exists():
            print(f"ERROR: CSV {args.from_csv} introuvable", file=sys.stderr)
            return 2
        rows = load_rows_from_csv(args.from_csv)
        print(f"[from-csv] {len(rows)} rows chargés depuis {args.from_csv}")
        counts = {"HAUTE": 0, "MOYENNE": 0, "FAIBLE": 0, "ABSENT": 0}
        for r in rows:
            counts[r.get("confiance", "ABSENT")] = counts.get(r.get("confiance", "ABSENT"), 0) + 1
        print(f"[Counts] HAUTE={counts['HAUTE']} | MOYENNE={counts['MOYENNE']} | FAIBLE={counts['FAIBLE']} | ABSENT={counts['ABSENT']}")
        if args.apply:
            backup_path = DRAFTS_DIR / f"sites_patrimoine.backup_{TODAY}.json"
            if not backup_path.exists():
                with backup_path.open("w", encoding="utf-8") as f:
                    json.dump(sites_data, f, ensure_ascii=False, indent=2)
                print(f"[Backup] {backup_path}")
            applied, skipped = apply_updates(rows, sites_data)
            with SITES_PATH.open("w", encoding="utf-8") as f:
                json.dump(sites_data, f, ensure_ascii=False, indent=2)
            # Re-write CSV avec applied flag
            write_csv(rows, args.from_csv)
            print(f"[Apply] {applied} sites mis à jour | {skipped} skip (DIST_OVER_5000m)")
            print(f"[Tier1] eligibles : HAUTE/MOYENNE non flag + FAIBLE concord IGN <1km + FAIBLE concord >=2src <2km")
        return 0

    pieves_polys = {}
    doyennes_polys = {}
    if args.reverse_geocode:
        with PIEVES_PATH.open(encoding="utf-8") as f:
            pdata = json.load(f)
        for p in pdata.get("pieves", []):
            if p.get("polygon"):
                pieves_polys[p["slug"]] = p["polygon"]
        with DOYENNES_PATH.open(encoding="utf-8") as f:
            ddata = json.load(f)
        for d in ddata.get("doyennes", []):
            if d.get("polygon"):
                doyennes_polys[d["slug"]] = d["polygon"]
        print(f"[reverse-geocode] {len(pieves_polys)} pieves + {len(doyennes_polys)} doyennes chargés")

    print(f"[Phase {args.phase}] Audit GPS sur {len(targets)} sites…")
    rows = []
    counts = {"HAUTE": 0, "MOYENNE": 0, "FAIBLE": 0, "ABSENT": 0}
    t0 = time.time()
    for i, site in enumerate(targets, 1):
        print(f"  [{i}/{len(targets)}] {site['slug']:<45} | {(site.get('name') or '')[:42]}", flush=True)
        row = audit_one_site(site, args.reverse_geocode, pieves_polys, doyennes_polys)
        counts[row["confiance"]] += 1
        rows.append(row)
        # Periodic CSV flush (résilience aux interruptions)
        if i % 10 == 0:
            csv_path = DRAFTS_DIR / f"audit_gps_phase{args.phase}_{TODAY}.csv"
            write_csv(rows, csv_path)

    csv_path = DRAFTS_DIR / f"audit_gps_phase{args.phase}_{TODAY}.csv"
    write_csv(rows, csv_path)
    elapsed = time.time() - t0
    print(f"\n[CSV]   {csv_path}")
    print(f"[Time]  {elapsed:.0f}s ({elapsed/max(len(targets),1):.1f}s/site)")
    print(f"[Counts] HAUTE={counts['HAUTE']} | MOYENNE={counts['MOYENNE']} | FAIBLE={counts['FAIBLE']} | ABSENT={counts['ABSENT']}")

    if args.apply:
        backup_path = DRAFTS_DIR / f"sites_patrimoine.backup_{TODAY}.json"
        if not backup_path.exists():
            with backup_path.open("w", encoding="utf-8") as f:
                json.dump(sites_data, f, ensure_ascii=False, indent=2)
            print(f"[Backup] {backup_path}")
        applied, skipped_far = apply_updates(rows, sites_data)
        with SITES_PATH.open("w", encoding="utf-8") as f:
            json.dump(sites_data, f, ensure_ascii=False, indent=2)
        write_csv(rows, csv_path)  # Re-write avec applied flag
        print(f"[Apply] {applied} sites mis à jour | {skipped_far} skip (DIST_OVER_5000m)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
