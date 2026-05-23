#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-transfert Vezzani (avancee fine cortenais).

Verifie :
  1. Vezzani (2B347) cote pieves : pieve_venaco -> pieve_tavignano
  2. Vezzani cote doyennes : doyenne_cortenais -> doyenne_plaine_orientale
  3. Disparition de l'avancee fine : 0 sommet cortenais a lon > 9.35 (etait 11)
  4. Cascade counts : pieve_tavignano +1 (10), pieve_venaco -1 (7),
     doyenne_cortenais -1 (51), doyenne_plaine_orientale +1 (54)
  5. Total Corse 360 inchange
  6. Aucun site Tellux a migrer (verifie en pre-build, 0 site dans Vezzani)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIEVES_OUTPUT = ROOT / "docs" / "data" / "pieves_polygons.json"
DOYENNES_OUTPUT = ROOT / "docs" / "data" / "doyennes_polygons.json"
DOYENNES_MAPPING = ROOT / "_drafts" / "doyennes_communes_mapping.json"
PIEVES_MAPPINGS = [
    ROOT / "_drafts" / "pieves_communes_mapping.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v2_canonicite_casta.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v3_stratD_2026-05-17.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v4_cleanup_2026-05-18.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v5_vague_22052026.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v5_pr2_arbitrages.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v6_tavignano_2026-05-23.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v7_vezzani_2026-05-23.json",
]
INSEE = "2B347"
NOM = "Vezzani"


def build_commune_to_pieve():
    c2p = {}
    with PIEVES_MAPPINGS[0].open(encoding="utf-8") as f:
        data = json.load(f)
    for p in data["pieves"]:
        for insee in p["communes_insee"]:
            c2p[insee] = p["slug"]
    for mp in PIEVES_MAPPINGS[1:]:
        if not mp.exists():
            continue
        with mp.open(encoding="utf-8") as f:
            data = json.load(f)
        for p in data.get("pieves_added", []):
            for insee in p["communes_insee"]:
                c2p[insee] = p["slug"]
        for t in data.get("transferts", []):
            c2p[t["commune_insee"]] = t["vers_pieve"]
        for r in data.get("renames", []):
            for insee, slug in list(c2p.items()):
                if slug == r["from"]:
                    c2p[insee] = r["to"]
    return c2p


def main():
    failures = []

    # 1. Vezzani pieve
    print(f"=== Vezzani ({INSEE}) pieve ===")
    c2p = build_commune_to_pieve()
    actual_pieve = c2p.get(INSEE)
    if actual_pieve == "pieve_tavignano":
        print(f"  [OK] {INSEE} {NOM} -> pieve_tavignano")
    else:
        failures.append(f"{INSEE} {NOM} pieve={actual_pieve} (attendu pieve_tavignano)")
        print(f"  [FAIL] {INSEE} {NOM} pieve={actual_pieve}")

    # 2. Vezzani doyenne
    print(f"\n=== Vezzani ({INSEE}) doyenne ===")
    with DOYENNES_MAPPING.open(encoding="utf-8") as f:
        dm = json.load(f)
    aja = next(d for d in dm["doyennes"] if d["slug"] == "doyenne_plaine_orientale")
    cort = next(d for d in dm["doyennes"] if d["slug"] == "doyenne_cortenais")
    if INSEE in aja["communes_insee"]:
        print(f"  [OK] {INSEE} in doyenne_plaine_orientale ({len(aja['communes_insee'])} communes)")
    else:
        failures.append(f"{INSEE} NOT in doyenne_plaine_orientale")
        print(f"  [FAIL] {INSEE} NOT in doyenne_plaine_orientale")
    if INSEE not in cort["communes_insee"]:
        print(f"  [OK] {INSEE} not in doyenne_cortenais ({len(cort['communes_insee'])} communes)")
    else:
        failures.append(f"{INSEE} STILL in doyenne_cortenais")
        print(f"  [FAIL] {INSEE} STILL in doyenne_cortenais")

    # 3. Disparition avancee fine cortenais
    print(f"\n=== Disparition avancee fine cortenais (sommets lon > 9.35) ===")
    with DOYENNES_OUTPUT.open(encoding="utf-8") as f:
        dd = json.load(f)
    for d in dd["doyennes"]:
        if d["slug"] == "doyenne_cortenais":
            poly = d["polygon"]
            east = [p for p in poly if p[1] > 9.35]
            max_lon = max(p[1] for p in poly)
            if len(east) == 0:
                print(f"  [OK] Cortenais : 0 sommet lon > 9.35 (max_lon={max_lon:.5f})")
            else:
                failures.append(f"Cortenais : {len(east)} sommets lon > 9.35 (attendu 0)")
                print(f"  [FAIL] Cortenais : {len(east)} sommets lon > 9.35")

    # 4. Cascade counts
    print(f"\n=== Cascade counts ===")
    with PIEVES_OUTPUT.open(encoding="utf-8") as f:
        pp = json.load(f)
    by_slug = {p["slug"]: p for p in pp["pieves"]}
    expected = {
        "pieve_tavignano": 10,    # 9 + Vezzani
        "pieve_venaco": 7,        # 8 - Vezzani
    }
    for slug, exp in expected.items():
        p = by_slug.get(slug)
        if p:
            ok = "OK" if p["communes_count"] == exp else "FAIL"
            if p["communes_count"] != exp:
                failures.append(f"{slug}.communes_count={p['communes_count']} (attendu {exp})")
            print(f"  [{ok}] {slug}.communes_count = {p['communes_count']} (attendu {exp})")

    expected_doy = {
        "doyenne_cortenais": 51,         # 52 - Vezzani
        "doyenne_plaine_orientale": 54,  # 53 + Vezzani
    }
    for slug, exp in expected_doy.items():
        d = next(d for d in dd["doyennes"] if d["slug"] == slug)
        ok = "OK" if d["communes_count"] == exp else "FAIL"
        if d["communes_count"] != exp:
            failures.append(f"{slug}.communes_count={d['communes_count']} (attendu {exp})")
        print(f"  [{ok}] {slug}.communes_count = {d['communes_count']} (attendu {exp})")

    # 5. Total Corse 360
    total_pieves = sum(p["communes_count"] for p in pp["pieves"])
    total_doyennes = sum(d["communes_count"] for d in dd["doyennes"])
    print(f"\n=== Total Corse pieves: {total_pieves}, doyennes: {total_doyennes} (attendu 360) ===")
    if total_pieves != 360:
        failures.append(f"Total pieves={total_pieves}")
    if total_doyennes != 360:
        failures.append(f"Total doyennes={total_doyennes}")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURES ===")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("=== ALL ASSERTIONS PASSED ===")


if __name__ == "__main__":
    main()
