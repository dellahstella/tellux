#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_doyennes_polygons.py — Pipeline build polygones doyennés (Brief 8 Avenant Strat A).

Génère `docs/data/doyennes_polygons.json` à partir de :
  - `_drafts/doyennes_communes_mapping.json` (mapping commune INSEE -> doyenné, livré Cowork 2026-05-04)
  - GeoJSON communes 2A + 2B (cache local, source : github.com/gregoiredavid/france-geojson)

Pour chaque doyenné, fait l'union polygonale des communes via shapely.unary_union,
simplifie selon `--tolerance` (défaut 0.001° ≈ 100m), et écrit au format Brief 8
(slug, name, polygon = liste de [lat, lng]). Si l'union est un MultiPolygon, ne
conserve que le plus grand sous-polygone (les îles/enclaves mineures sont ignorées
et loggées).

Usage :
  python scripts/build_doyennes_polygons.py [--tolerance 0.001]

Sortie : docs/data/doyennes_polygons.json (overwrite)
"""

import argparse
import json
import re
import sys
from pathlib import Path

from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union

# B10-UX-026 — calcul display_name : retrait du préfixe "Doyenné [du|de l'|d'|de la|de]"
# au début du nom canonique. Ex: "Doyenné du Cap" -> "Cap", "Doyenné d'Ajaccio" -> "Ajaccio".
DOYENNE_PREFIX_RE = re.compile(r"^Doyenn[ée]\s+(?:du\s+|de\s+l'|d'|de\s+la\s+|de\s+)?", re.IGNORECASE)


def compute_display_name(name):
    return DOYENNE_PREFIX_RE.sub("", name).strip() or name

ROOT = Path(__file__).resolve().parent.parent
MAPPING_PATH = ROOT / "_drafts" / "doyennes_communes_mapping.json"
CACHE_DIR = ROOT / "scripts" / ".cache"
GEO_2A = CACHE_DIR / "communes-2A.geojson"
GEO_2B = CACHE_DIR / "communes-2B.geojson"
OUTPUT_PATH = ROOT / "docs" / "data" / "doyennes_polygons.json"

# Palette ABCD répartie post-fusion (10 doyennés).
TONE_BY_SLUG = {
    "doyenne_du_cap": "A",
    "doyenne_de_bastia": "B",
    "doyenne_du_golo": "C",
    "doyenne_balagne": "D",
    "doyenne_cortenais": "A",
    "doyenne_piana_vico_sari": "B",
    "doyenne_plaine_orientale": "D",
    "doyenne_ajaccio": "C",
    "doyenne_prunelli_taravo_valinco": "A",
    "doyenne_extreme_sud": "D",
}


def load_communes_index():
    """Indexe les 360 communes corses par INSEE -> shapely geometry."""
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
    """GeoJSON [lng, lat] -> Leaflet [lat, lng], arrondi 5 décimales (~1m)."""
    return [[round(c[1], 5), round(c[0], 5)] for c in coords]


def geom_to_latlng_polygon(geom, slug):
    """Extrait l'anneau extérieur du plus grand sous-polygone (drop multi mineurs)."""
    dropped = []
    if isinstance(geom, MultiPolygon):
        polys = sorted(geom.geoms, key=lambda p: p.area, reverse=True)
        main = polys[0]
        for sub in polys[1:]:
            dropped.append(round(sub.area * 12321, 2))  # area en ~km² (1° ≈ 111 km)
    elif isinstance(geom, Polygon):
        main = geom
    else:
        raise ValueError(f"[{slug}] géométrie inattendue: {type(geom).__name__}")
    return coords_to_latlng(list(main.exterior.coords)), dropped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tolerance", type=float, default=0.001,
                        help="Tolérance simplification shapely (degrés, défaut 0.001 ≈ 100m)")
    args = parser.parse_args()

    print(f"[build] mapping  : {MAPPING_PATH}")
    print(f"[build] geo 2A   : {GEO_2A}")
    print(f"[build] geo 2B   : {GEO_2B}")
    print(f"[build] output   : {OUTPUT_PATH}")
    print(f"[build] tolerance: {args.tolerance}° (~{int(args.tolerance * 111000)}m)")

    with MAPPING_PATH.open(encoding="utf-8") as f:
        mapping_data = json.load(f)
    communes_index = load_communes_index()
    print(f"[build] communes indexées: {len(communes_index)} (attendu 360)")

    out_doyennes = []
    total_vertices_before = 0
    total_vertices_after = 0
    total_area_km2 = 0.0
    not_found = []

    for d in mapping_data["doyennes"]:
        slug = d["slug"]
        polys = []
        missing = []
        for insee in d["communes_insee"]:
            geom = communes_index.get(insee)
            if geom is None:
                missing.append(insee)
                continue
            polys.append(geom)
        if missing:
            not_found.append({"doyenne": slug, "insee": missing})

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
        # Aire en km² (approximation projection plate à lat ~42°N : 1°² ≈ 12 321 * cos(42°) ≈ 9 156 km²)
        area_km2 = simplified.area * 9156
        total_area_km2 += area_km2

        display = compute_display_name(d["name"])
        entry = {
            "slug": slug,
            "name": d["name"],
            "display_name": display,
            "tone": TONE_BY_SLUG.get(slug, "A"),
            # Brief 14 — chemin speculatif vers la miniature illustration. Si le
            # fichier n'existe pas, le fallback typographique JS (initiale du
            # display_name) prend le relais via onerror du <img>. La bascule est
            # automatique au depot d'un fichier doyenne_<slug>_tellux_v2.png.
            "illustration_path": f"docs/assets/visuels/doyenne_{slug.replace('doyenne_', '')}_tellux_v2.png",
            "initiale": display[:1].upper() if display else "?",
            "communes_count": len(polys),
            "polygon": latlng_polygon,
        }
        if dropped:
            entry["multipolygon_dropped_areas_km2"] = dropped
        out_doyennes.append(entry)

        print(f"[build] {slug}: {len(polys)} communes, "
              f"{before}->{after} vertices, ~{area_km2:.0f} km²"
              + (f", dropped {len(dropped)} sub-polygons" if dropped else ""))

    output = {
        "version": "v2-stratA-from-communes",
        "generated_by": "scripts/build_doyennes_polygons.py",
        "source_mapping": "_drafts/doyennes_communes_mapping.json (Cowork 2026-05-04)",
        "source_communes": "github.com/gregoiredavid/france-geojson (departements 2A + 2B)",
        "tolerance_degrees": args.tolerance,
        "stats": {
            "doyennes_count": len(out_doyennes),
            "total_communes": sum(d["communes_count"] for d in out_doyennes),
            "vertices_before_simplify": total_vertices_before,
            "vertices_after_simplify": total_vertices_after,
            "approx_total_area_km2": round(total_area_km2, 1),
            "communes_not_found_in_geo": not_found,
        },
        "doyennes": out_doyennes,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[build] OK -> {OUTPUT_PATH}")
    print(f"[build] {len(out_doyennes)} doyennes | "
          f"{total_vertices_before}->{total_vertices_after} vertices | "
          f"~{total_area_km2:.0f} km² (Corse théorique ~8 680 km²)")
    if not_found:
        print(f"[build] {len(not_found)} doyennes avec INSEE manquants:")
        for nf in not_found:
            print(f"  - {nf['doyenne']}: {nf['insee']}")


if __name__ == "__main__":
    main()
