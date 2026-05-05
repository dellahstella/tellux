#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pieves_polygons.py — Pipeline build polygones pieves médiévales (Brief 9 Strat A).

Génère `docs/data/pieves_polygons.json` à partir de :
  - `_drafts/pieves_communes_mapping.json` (mapping commune INSEE -> pieve, livré Cowork)
  - `_drafts/PIEVE_OVERRIDES.json` (overrides manuels Soleil, appliqués AVANT l'union)
  - GeoJSON communes 2A + 2B (cache local, source : github.com/gregoiredavid/france-geojson)

Pour chaque pieve, fait l'union polygonale des communes via shapely.unary_union,
simplifie selon `--tolerance` (défaut 0.0005° ≈ 55m, plus fin que doyennés vu la
granularité ~5-15 communes par pieve), et écrit au format Brief 9 (slug, name,
diocese_medieval, doyenne_contemporain_majoritaire, polygon = liste de [lat, lng]).
Si l'union est un MultiPolygon, ne conserve que le plus grand sous-polygone (îles
satellites mineures loggées).

Usage :
  python scripts/build_pieves_polygons.py [--tolerance 0.0005]

Sortie : docs/data/pieves_polygons.json (overwrite)
"""

import argparse
import json
import sys
from pathlib import Path

from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
MAPPING_PATH = ROOT / "_drafts" / "pieves_communes_mapping.json"
OVERRIDES_PATH = ROOT / "_drafts" / "PIEVE_OVERRIDES.json"
PIEVE_DOY_OVERRIDES_PATH = ROOT / "_drafts" / "PIEVE_DOYENNES_OVERRIDES.json"
CACHE_DIR = ROOT / "scripts" / ".cache"
GEO_2A = CACHE_DIR / "communes-2A.geojson"
GEO_2B = CACHE_DIR / "communes-2B.geojson"
OUTPUT_PATH = ROOT / "docs" / "data" / "pieves_polygons.json"
# B10-UX-025 — input pour recalcul rigoureux du doyenne_contemporain_majoritaire
# par intersection polygonale (vs declaration Cowork qui peut etre incoherente
# pour les pieves a cheval sur deux doyennes).
DOYENNES_PATH = ROOT / "docs" / "data" / "doyennes_polygons.json"


def latlng_polygon_to_shapely(latlng):
    coords = [[c[1], c[0]] for c in latlng]
    return Polygon(coords)


def load_doyennes_shapes():
    """Charge les polygones doyennes (Strat A) en shapely pour intersection."""
    if not DOYENNES_PATH.exists():
        return None
    with DOYENNES_PATH.open(encoding="utf-8") as f:
        data = json.load(f)
    return {d["slug"]: latlng_polygon_to_shapely(d["polygon"]) for d in data["doyennes"]}


def compute_majoritaire_by_intersection(pieve_geom, doyennes_shapes):
    """Retourne le slug du doyenne avec le plus grand % d'intersection
    avec la geometrie pieve (recalcul rigoureux B10-UX-025)."""
    if not doyennes_shapes:
        return None
    best_slug = None
    best_pct = 0.0
    for doy_slug, doy_geom in doyennes_shapes.items():
        if not pieve_geom.intersects(doy_geom):
            continue
        inter = pieve_geom.intersection(doy_geom)
        pct = inter.area / pieve_geom.area
        if pct > best_pct:
            best_pct = pct
            best_slug = doy_slug
    return best_slug


def compute_doyennes_appartenance(pieve_geom, doyennes_shapes):
    """Brief 12 (B11-UX-028) — pour chaque doyenne, calcule le ratio
    intersection / aire_pieve. Retourne tous les doyennes avec ratio > 0,
    tries par ratio descendant. Le seuil de visibilite est applique cote
    runtime (constante SEUIL_PIEVE_DOYENNE dans patrimoine.html)."""
    if not doyennes_shapes:
        return []
    out = []
    for doy_slug, doy_geom in doyennes_shapes.items():
        if not pieve_geom.intersects(doy_geom):
            continue
        inter = pieve_geom.intersection(doy_geom)
        ratio = inter.area / pieve_geom.area
        if ratio > 0:
            out.append({"slug": doy_slug, "ratio": round(ratio, 4)})
    out.sort(key=lambda x: -x["ratio"])
    return out


def load_communes_index():
    index = {}
    for path in (GEO_2A, GEO_2B):
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
        for feat in data["features"]:
            insee = feat["properties"]["code"]
            geom = shape(feat["geometry"])
            index[insee] = geom
    return index


def coords_to_latlng(coords):
    return [[round(c[1], 5), round(c[0], 5)] for c in coords]


def geom_to_latlng_polygon(geom, slug):
    dropped = []
    if isinstance(geom, MultiPolygon):
        polys = sorted(geom.geoms, key=lambda p: p.area, reverse=True)
        main = polys[0]
        for sub in polys[1:]:
            dropped.append(round(sub.area * 9156, 2))
    elif isinstance(geom, Polygon):
        main = geom
    else:
        raise ValueError(f"[{slug}] géométrie inattendue: {type(geom).__name__}")
    return coords_to_latlng(list(main.exterior.coords)), dropped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tolerance", type=float, default=0.0005,
                        help="Tolérance simplification shapely (degrés, défaut 0.0005 ≈ 55m)")
    args = parser.parse_args()

    print(f"[build] mapping     : {MAPPING_PATH}")
    print(f"[build] overrides   : {OVERRIDES_PATH}")
    print(f"[build] geo 2A      : {GEO_2A}")
    print(f"[build] geo 2B      : {GEO_2B}")
    print(f"[build] output      : {OUTPUT_PATH}")
    print(f"[build] tolerance   : {args.tolerance}° (~{int(args.tolerance * 111000)}m)")

    with MAPPING_PATH.open(encoding="utf-8") as f:
        mapping_data = json.load(f)
    with OVERRIDES_PATH.open(encoding="utf-8") as f:
        overrides_data = json.load(f)
    overrides = overrides_data.get("overrides") or {}

    # Brief 10 — overrides "pieve -> [doyennes_visibles]" pour permettre a une
    # pieve d'apparaitre dans plusieurs doyennes a la fois (multi-affectation
    # arbitree manuellement par Soleil sans modifier les frontieres doyennes).
    pieve_doy_overrides = {}
    if PIEVE_DOY_OVERRIDES_PATH.exists():
        with PIEVE_DOY_OVERRIDES_PATH.open(encoding="utf-8") as f:
            pieve_doy_data = json.load(f)
        pieve_doy_overrides = pieve_doy_data.get("overrides") or {}
        print(f"[build] PIEVE_DOYENNES_OVERRIDES: {len(pieve_doy_overrides)} pieves multi-affectees")

    # Construire commune INSEE -> pieve_slug à partir du mapping Cowork
    commune_to_pieve = {}
    for p in mapping_data["pieves"]:
        for insee in p["communes_insee"]:
            commune_to_pieve[insee] = p["slug"]

    # Appliquer overrides (post-mapping Cowork)
    overrides_applied = []
    for insee, target_slug in overrides.items():
        previous = commune_to_pieve.get(insee)
        commune_to_pieve[insee] = target_slug
        overrides_applied.append({
            "insee": insee, "previous": previous, "new": target_slug,
        })
    print(f"[build] overrides applied: {len(overrides_applied)}")

    # Re-grouper communes par pieve (post-overrides)
    pieve_to_communes = {}
    for insee, slug in commune_to_pieve.items():
        pieve_to_communes.setdefault(slug, []).append(insee)

    communes_index = load_communes_index()
    print(f"[build] communes indexées: {len(communes_index)} (attendu 360)")

    # B10-UX-025 — chargement des polygones doyennes pour recalcul rigoureux
    # du doyenne_contemporain_majoritaire par intersection. Le mapping Cowork
    # reste intact, on derive juste le rattachement majoritaire de la geometrie
    # reelle (resout les pieves a cheval ou les declarations incoherentes).
    doyennes_shapes = load_doyennes_shapes()
    if doyennes_shapes:
        print(f"[build] doyennes shapes chargees pour recalcul majoritaire : {len(doyennes_shapes)}")
    else:
        print(f"[build] WARN doyennes_polygons.json absent, fallback declaration Cowork")

    # Métadonnées (name, diocese_medieval, doyenne_contemporain_majoritaire) du mapping
    meta_by_slug = {p["slug"]: p for p in mapping_data["pieves"]}

    out_pieves = []
    total_vertices_before = 0
    total_vertices_after = 0
    total_area_km2 = 0.0
    not_found = []
    surface_by_diocese = {}
    reclassed = []   # B10-UX-025 — log des reclasses (declared vs actual)

    for slug, insee_list in pieve_to_communes.items():
        meta = meta_by_slug.get(slug, {})
        polys = []
        missing = []
        for insee in insee_list:
            geom = communes_index.get(insee)
            if geom is None:
                missing.append(insee)
                continue
            polys.append(geom)
        if missing:
            not_found.append({"pieve": slug, "insee": missing})
        if not polys:
            print(f"[build] WARN {slug}: aucune commune trouvée, ignoré")
            continue

        union = unary_union(polys)
        before = sum(len(p.exterior.coords) for p in (
            union.geoms if isinstance(union, MultiPolygon) else [union]
        ))
        simplified = union.simplify(args.tolerance, preserve_topology=True)
        after = sum(len(p.exterior.coords) for p in (
            simplified.geoms if isinstance(simplified, MultiPolygon) else [simplified]
        ))
        total_vertices_before += before
        total_vertices_after += after

        latlng_polygon, dropped = geom_to_latlng_polygon(simplified, slug)
        area_km2 = simplified.area * 9156
        total_area_km2 += area_km2
        diocese = meta.get("diocese_medieval", "?")
        surface_by_diocese[diocese] = surface_by_diocese.get(diocese, 0) + area_km2

        # B10-UX-025 — recalcul rigoureux du doyenne majoritaire par intersection
        # polygonale shapely (sur le polygone simplifie pour coherence visuelle).
        declared_doy = meta.get("doyenne_contemporain_majoritaire")
        if doyennes_shapes:
            actual_doy = compute_majoritaire_by_intersection(simplified, doyennes_shapes)
            if actual_doy and actual_doy != declared_doy:
                reclassed.append({"pieve": slug, "declared": declared_doy, "actual": actual_doy})
            doyenne_final = actual_doy or declared_doy
        else:
            doyenne_final = declared_doy

        # Brief 10 (post-arbitrage Soleil) — doyennes_visibles : liste des doyennes
        # ou la pieve apparait au drill-down N2. Override manuel prioritaire sur
        # le majoritaire calcule. Permet la multi-affectation (ex: Caccia visible
        # au clic Balagne ET au clic Golo).
        doyennes_visibles = pieve_doy_overrides.get(slug) or [doyenne_final]

        # Brief 12 (B11-UX-028) — appartenance multi-doyennes pour le seuillage
        # cote runtime. Le runtime fait l'union de doyennes_visibles (override
        # manuel) et des doyennes ou ratio >= SEUIL_PIEVE_DOYENNE.
        doyennes_appartenance = compute_doyennes_appartenance(simplified, doyennes_shapes)

        entry = {
            "slug": slug,
            "name": meta.get("name", slug),
            "diocese_medieval": diocese,
            "doyenne_contemporain_majoritaire": doyenne_final,
            "doyennes_visibles": doyennes_visibles,
            "doyennes_appartenance": doyennes_appartenance,
            "communes_count": len(polys),
            "polygon": latlng_polygon,
        }
        if dropped:
            entry["multipolygon_dropped_areas_km2"] = dropped
        out_pieves.append(entry)

        print(f"[build] {slug:30s}: {len(polys):3d} communes, "
              f"{before}->{after} vertices, ~{area_km2:.0f} km²"
              + (f", dropped {len(dropped)}" if dropped else ""))

    output = {
        "version": "v1-stratA-from-communes",
        "generated_by": "scripts/build_pieves_polygons.py",
        "source_mapping": "_drafts/pieves_communes_mapping.json (Cowork)",
        "source_communes": "github.com/gregoiredavid/france-geojson (departements 2A + 2B)",
        "tolerance_degrees": args.tolerance,
        "overrides_applied": overrides_applied,
        "doyenne_majoritaire_recalc": "intersection_polygonale_shapely_vs_declaration_cowork",
        "doyenne_majoritaire_reclassed": reclassed,
        "stats": {
            "pieves_count": len(out_pieves),
            "total_communes": sum(p["communes_count"] for p in out_pieves),
            "vertices_before_simplify": total_vertices_before,
            "vertices_after_simplify": total_vertices_after,
            "approx_total_area_km2": round(total_area_km2, 1),
            "surface_by_diocese_km2": {k: round(v, 1) for k, v in surface_by_diocese.items()},
            "communes_not_found_in_geo": not_found,
            "doyenne_reclassed_count": len(reclassed),
        },
        "pieves": out_pieves,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[build] OK -> {OUTPUT_PATH}")
    print(f"[build] {len(out_pieves)} pieves | "
          f"{total_vertices_before}->{total_vertices_after} vertices | "
          f"~{total_area_km2:.0f} km² (Corse théorique ~8 680 km²)")
    print(f"[build] surface par diocèse médiéval :")
    for k, v in sorted(surface_by_diocese.items(), key=lambda x: -x[1]):
        print(f"  - {k:12s}: ~{v:.0f} km²")
    if not_found:
        print(f"[build] {len(not_found)} pieves avec INSEE manquants:")
        for nf in not_found:
            print(f"  - {nf['pieve']}: {nf['insee']}")
    if reclassed:
        print(f"[build] B10-UX-025 reclasses {len(reclassed)} pieves (declared Cowork -> majoritaire reel) :")
        for rc in reclassed:
            print(f"  - {rc['pieve']}: {rc['declared']} -> {rc['actual']}")


if __name__ == "__main__":
    main()
