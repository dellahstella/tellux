#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_doyennes_polygons.py — Pipeline build polygones doyennés (Brief 8 Avenant Strat A).

Génère `docs/data/doyennes_polygons.json` à partir de :
  - `_drafts/doyennes_communes_mapping.json` (mapping commune INSEE -> doyenné, livré Cowork 2026-05-04)
  - GeoJSON communes 2A + 2B (cache local, source : github.com/gregoiredavid/france-geojson)

Pour chaque doyenné, fait l'union polygonale des communes via shapely.unary_union,
simplifie selon `--tolerance` (défaut 0.001° ≈ 100m), et écrit au format Brief 8
étendu (Op B audit géométrie 22-23/05/2026) :
  - polygon  : main exterior ring (compat ascendante)
  - polygons : NEW liste de tous les rings (main + îles whitelist)
  - islands  : NEW metadata par sous-polygone (commune_insee, area_km2, centroid)

Les sous-polygones doivent appartenir à une commune INSEE whitelistée
(ISLAND_WHITELIST). Tout sous-polygone non whitelist → log ERROR + exit 1
(pas de drop silencieux).

Usage :
  python scripts/build_doyennes_polygons.py [--tolerance 0.001]

Sortie : docs/data/doyennes_polygons.json (overwrite)
"""

import argparse
import json
import re
import sys
from pathlib import Path

from shapely.geometry import shape, mapping, Point, Polygon, MultiPolygon
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

# Palette ABCD répartie post-fusion Bastia->Cap 2026-05-06 (9 doyennés).
TONE_BY_SLUG = {
    "doyenne_du_cap": "A",
    "doyenne_du_golo": "C",
    "doyenne_balagne": "D",
    "doyenne_cortenais": "A",
    "doyenne_piana_vico_sari": "B",
    "doyenne_plaine_orientale": "D",
    "doyenne_ajaccio": "C",
    "doyenne_prunelli_taravo_valinco": "B",
    "doyenne_extreme_sud": "D",
}

# Op D — Whitelist îles INSEE légitimes par doyenné.
# Source : _drafts/doyennes_audit_full_2026-05-24.json + _drafts/doyennes_geometry_proposal.json
# (re-vérif 24/05, 12 sous-polygones identifiés, tous îles INSEE confirmées).
# Tout sous-polygone provenant d'une commune hors whitelist → ERROR + exit 1.
ISLAND_WHITELIST = {
    "doyenne_du_cap": {"2B107", "2B086"},            # Ersa (Giraglia), Centuri
    "doyenne_piana_vico_sari": {"2A197"},            # Osani (Gargalo/Scandola)
    "doyenne_ajaccio": {"2A004"},                    # Ajaccio (Sanguinaires)
    "doyenne_extreme_sud": {"2A041", "2A247", "2A362"},  # Bonifacio, Porto-Vecchio, Zonza
}

# Labels human-readable par commune INSEE pour le log (ordre par area décroissante).
ISLAND_LABELS = {
    "2B107": "Giraglia (Ersa)",
    "2B086": "Centuri",
    "2A197": "Gargalo/Scandola (Osani)",
    "2A004": "Sanguinaires (Ajaccio)",
    "2A041": "Lavezzi/Cavallo/Bouches Bonifacio",
    "2A247": "Cerbicales (Porto-Vecchio)",
    "2A362": "Pinarello/Zonza",
}

# Conversion area degrés² -> km² (projection plate à lat ~42°N).
DEG2_TO_KM2 = 9156


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


def _identify_commune_insee(sub_geom, candidate_insee_list, communes_index):
    """Renvoie l'INSEE de la commune dont la geom contient un point représentatif
    du sous-polygone. Recherche restreinte à la liste candidate (communes du doyenné).
    Retourne None si aucune commune ne contient le point (cas anormal)."""
    rp = sub_geom.representative_point()
    for insee in candidate_insee_list:
        cg = communes_index.get(insee)
        if cg is not None and cg.contains(rp):
            return insee
    # Fallback : intersection (cas bord après simplify).
    for insee in candidate_insee_list:
        cg = communes_index.get(insee)
        if cg is not None and cg.intersects(sub_geom):
            return insee
    return None


def geom_to_rings_and_islands(geom, slug, doyenne_communes_insee, communes_index):
    """Op B + Op D — extrait tous les rings du Polygon/MultiPolygon.

    Returns:
      main_ring        : [[lat,lng], ...] du plus grand sous-polygone (compat `polygon`)
      all_rings        : liste [[[lat,lng], ...], ...] ordonnée main puis îles (champ `polygons`)
      islands_metadata : liste [{commune_insee, area_km2, centroid: [lat,lng],
                                identification, polygon_index}] (champ `islands`)
      unexpected       : liste d'erreurs (commune INSEE non whitelist) — déclenche STOP appelant
    """
    if isinstance(geom, Polygon):
        sub_polys = [geom]
    elif isinstance(geom, MultiPolygon):
        sub_polys = sorted(geom.geoms, key=lambda p: p.area, reverse=True)
    else:
        raise ValueError(f"[{slug}] géométrie inattendue: {type(geom).__name__}")

    main_poly = sub_polys[0]
    main_ring = coords_to_latlng(list(main_poly.exterior.coords))

    all_rings = [main_ring]
    islands_metadata = []
    unexpected = []

    whitelist = ISLAND_WHITELIST.get(slug, set())

    for idx, sub in enumerate(sub_polys[1:], start=1):
        area_km2 = round(sub.area * DEG2_TO_KM2, 3)
        c = sub.representative_point()
        centroid_latlng = [round(c.y, 5), round(c.x, 5)]
        insee = _identify_commune_insee(sub, doyenne_communes_insee, communes_index)

        if insee is None:
            unexpected.append({
                "slug": slug,
                "polygon_index": idx,
                "area_km2": area_km2,
                "centroid": centroid_latlng,
                "reason": "commune INSEE non identifiable (PIP failed)",
            })
            continue

        if insee not in whitelist:
            unexpected.append({
                "slug": slug,
                "polygon_index": idx,
                "area_km2": area_km2,
                "centroid": centroid_latlng,
                "commune_insee": insee,
                "reason": f"commune INSEE {insee} absente whitelist {sorted(whitelist)}",
            })
            continue

        ring = coords_to_latlng(list(sub.exterior.coords))
        all_rings.append(ring)
        islands_metadata.append({
            "polygon_index": len(all_rings) - 1,
            "commune_insee": insee,
            "area_km2": area_km2,
            "centroid": centroid_latlng,
            "identification": ISLAND_LABELS.get(insee, insee),
        })

    return main_ring, all_rings, islands_metadata, unexpected


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
    total_islands = 0
    not_found = []
    unexpected_all = []

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

        main_ring, all_rings, islands_meta, unexpected = geom_to_rings_and_islands(
            simplified, slug, d["communes_insee"], communes_index
        )
        if unexpected:
            unexpected_all.extend(unexpected)

        # Aire totale = somme de tous les sous-polygones rendus (main + îles whitelist).
        sub_polys_all = simplified.geoms if isinstance(simplified, MultiPolygon) else [simplified]
        sub_polys_sorted = sorted(sub_polys_all, key=lambda p: p.area, reverse=True)
        kept_count = 1 + len(islands_meta)
        area_km2 = sum(p.area for p in sub_polys_sorted[:kept_count]) * DEG2_TO_KM2
        total_area_km2 += area_km2
        total_islands += len(islands_meta)

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
            # `polygon` : compat ascendante — main exterior ring (single).
            # Consommateurs actuels (patrimoine.html L.polygon + pointInPolygon) inchangés.
            "polygon": main_ring,
            # `polygons` : Op B audit 22-23/05/2026 — liste de tous les rings
            # (main + îles whitelist Op D). Format Leaflet-friendly :
            # `[[[lat,lng], ...], [[lat,lng], ...], ...]`. Consommateurs futurs
            # peuvent rendre toutes les parts via L.polygon(d.polygons).
            "polygons": all_rings,
        }
        if islands_meta:
            entry["islands"] = islands_meta
        out_doyennes.append(entry)

        islands_log = f", islands {len(islands_meta)}/{len(sub_polys_sorted) - 1}" if len(sub_polys_sorted) > 1 else ""
        print(f"[build] {slug}: {len(polys)} communes, "
              f"{before}->{after} vertices, ~{area_km2:.1f} km²"
              + islands_log)
        for isl in islands_meta:
            print(f"        + ile #{isl['polygon_index']}: {isl['identification']} "
                  f"INSEE={isl['commune_insee']} area={isl['area_km2']} km²")

    # Op D — STOP si sous-polygone hors whitelist (pas de drop silencieux).
    if unexpected_all:
        print(f"\n[build] ERROR : {len(unexpected_all)} sous-polygone(s) non whitelist détecté(s) :")
        for u in unexpected_all:
            print(f"  - {u['slug']} #{u['polygon_index']}: area={u['area_km2']} km² "
                  f"centroid={u['centroid']} | {u['reason']}")
        print("[build] ABORT — étendre ISLAND_WHITELIST ou investiguer mapping commune.")
        print("[build] JSON output NON écrit (préservation du fichier prod).")
        sys.exit(1)

    output = {
        "version": "v3-stratA-multipolygon-preserved",
        "generated_by": "scripts/build_doyennes_polygons.py",
        "source_mapping": "_drafts/doyennes_communes_mapping.json (Cowork 2026-05-04)",
        "source_communes": "github.com/gregoiredavid/france-geojson (departements 2A + 2B)",
        "tolerance_degrees": args.tolerance,
        "schema_note": (
            "Op B audit géométrie 22-23/05/2026 + re-vérif 24/05 : champ `polygon` "
            "(compat ascendante : main exterior ring) + champ `polygons` (NEW : liste "
            "de tous les rings, main + îles whitelist Op D) + champ `islands` (NEW : "
            "metadata par sous-polygone). Whitelist Op D : 12 sous-polygones légitimes "
            "via INSEE Ersa/Centuri/Osani/Ajaccio/Bonifacio/Porto-Vecchio/Zonza."
        ),
        "stats": {
            "doyennes_count": len(out_doyennes),
            "total_communes": sum(d["communes_count"] for d in out_doyennes),
            "vertices_before_simplify": total_vertices_before,
            "vertices_after_simplify": total_vertices_after,
            "approx_total_area_km2": round(total_area_km2, 1),
            "total_islands_kept": total_islands,
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
          f"~{total_area_km2:.1f} km² (Corse théorique ~8 680 km²) | "
          f"{total_islands} îles whitelist préservées")
    if not_found:
        print(f"[build] {len(not_found)} doyennes avec INSEE manquants:")
        for nf in not_found:
            print(f"  - {nf['doyenne']}: {nf['insee']}")


if __name__ == "__main__":
    main()
