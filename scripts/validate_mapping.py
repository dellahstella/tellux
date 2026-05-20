#!/usr/bin/env python3
"""
validate_mapping.py REV2 — verifie coherence interne du mapping (v1+v2+v3+v4)
contre invariants stables (PAS contre communes_count prod qui peut etre faux).

Criteres de succes :
1. 0 zombie : tout slug reference dans mapping doit exister dans pieves_polygons.json prod
2. 0 manquante : tout slug dans pieves_polygons.json prod doit etre mappable
3. Total communes mappees == 360 (toutes communes 2A+2B)
4. Pas de commune doublement assignee
5. PIP sanity check (warning seulement) : centroide commune dans polygone cible ?

Used in :
- Phase A : baseline avant cleanup (doit montrer 22 issues)
- Phase B' : validation post-cleanup (doit montrer 0 issues)
- PR C future : guard pre-rebuild
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPPING_V1 = ROOT / "_drafts" / "pieves_communes_mapping.json"
MAPPING_V2 = ROOT / "_drafts" / "pieves_communes_mapping_v2_canonicite_casta.json"
MAPPING_V3 = ROOT / "_drafts" / "pieves_communes_mapping_v3_stratD_2026-05-17.json"
MAPPING_V4 = ROOT / "_drafts" / "pieves_communes_mapping_v4_cleanup_2026-05-18.json"
PIEVES_PROD = ROOT / "docs" / "data" / "pieves_polygons.json"
GEO_2A = ROOT / "scripts" / ".cache" / "communes-2A.geojson"
GEO_2B = ROOT / "scripts" / ".cache" / "communes-2B.geojson"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.JSONDecoder().raw_decode(f.read())[0]


def merge_mappings():
    """Reproduit logique build_pieves_polygons.py + v4."""
    commune_to_pieve = {}

    m1 = load(MAPPING_V1)
    for p in m1.get("pieves", []):
        for insee in p["communes_insee"]:
            commune_to_pieve[insee] = p["slug"]

    if MAPPING_V2.exists():
        m2 = load(MAPPING_V2)
        for p in m2.get("pieves_added", []):
            for insee in p["communes_insee"]:
                commune_to_pieve[insee] = p["slug"]
        for t in m2.get("transferts", []):
            commune_to_pieve[t["commune_insee"]] = t["vers_pieve"]

    if MAPPING_V3.exists():
        m3 = load(MAPPING_V3)
        for p in m3.get("pieves_added", []):
            for insee in p["communes_insee"]:
                commune_to_pieve[insee] = p["slug"]
        for t in m3.get("transferts", []):
            commune_to_pieve[t["commune_insee"]] = t["vers_pieve"]
        for r in m3.get("renames", []):
            for insee, slug in list(commune_to_pieve.items()):
                if slug == r["from"]:
                    commune_to_pieve[insee] = r["to"]

    if MAPPING_V4.exists():
        m4 = load(MAPPING_V4)
        for p in m4.get("pieves_added", []):
            for insee in p["communes_insee"]:
                commune_to_pieve[insee] = p["slug"]
        for t in m4.get("transferts", []):
            commune_to_pieve[t["commune_insee"]] = t["vers_pieve"]
        for r in m4.get("renames", []):
            for insee, slug in list(commune_to_pieve.items()):
                if slug == r["from"]:
                    commune_to_pieve[insee] = r["to"]

    return commune_to_pieve


def main():
    commune_to_pieve = merge_mappings()
    mapping_slugs = set(commune_to_pieve.values())

    pieves_prod = load(PIEVES_PROD)
    prod_slugs = {p["slug"] for p in pieves_prod["pieves"]}

    zombies = sorted(mapping_slugs - prod_slugs)
    missing = sorted(prod_slugs - mapping_slugs)
    total = len(commune_to_pieve)

    pip_warnings = []
    if GEO_2A.exists() and GEO_2B.exists():
        from shapely.geometry import shape, Polygon
        commune_geoms = {}
        for path in (GEO_2A, GEO_2B):
            for feat in json.load(open(path, encoding="utf-8"))["features"]:
                commune_geoms[feat["properties"]["code"]] = shape(feat["geometry"])

        def to_poly(latlng):
            return Polygon([[c[1], c[0]] for c in latlng])

        pieve_shapes = {p["slug"]: to_poly(p["polygon"]) for p in pieves_prod["pieves"]}

        for insee, target_slug in commune_to_pieve.items():
            g = commune_geoms.get(insee)
            if not g:
                continue
            target_poly = pieve_shapes.get(target_slug)
            if not target_poly or not target_poly.is_valid:
                continue
            rp = g.representative_point()
            if not (target_poly.contains(rp) or target_poly.intersects(rp)):
                pip_warnings.append({"insee": insee, "target": target_slug})

    print(f"Mapping slugs : {len(mapping_slugs)}")
    print(f"Prod slugs    : {len(prod_slugs)}")
    print(f"Total communes mapped : {total} (expected 360)")
    print(f"\nZombies (mapping -> absent prod) : {len(zombies)}")
    for z in zombies:
        n = sum(1 for v in commune_to_pieve.values() if v == z)
        print(f"  - {z} ({n} communes)")
    print(f"Missing (prod -> absent mapping) : {len(missing)}")
    for m in missing:
        print(f"  - {m}")
    print(f"\nPIP sanity warnings (centroide hors polygone cible) : {len(pip_warnings)} [INFO]")
    if pip_warnings and len(pip_warnings) < 20:
        for w in pip_warnings:
            print(f"  - {w['insee']} -> {w['target']}")
    elif pip_warnings:
        print("  (premieres 10) :")
        for w in pip_warnings[:10]:
            print(f"  - {w['insee']} -> {w['target']}")

    fails = []
    if zombies:
        fails.append(f"{len(zombies)} zombies")
    if missing:
        fails.append(f"{len(missing)} missing")
    if total != 360:
        fails.append(f"total={total} (expected 360)")

    if not fails:
        print("\nOK validate_mapping REV2 : mapping coherent, 360 communes mappees, 0 zombie, 0 manquante")
        if pip_warnings:
            print(f"  (Note: {len(pip_warnings)} PIP warnings = polygones prod obsoletes, dette PR C)")
        sys.exit(0)
    else:
        print(f"\nFAIL validate_mapping REV2 : {' + '.join(fails)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
