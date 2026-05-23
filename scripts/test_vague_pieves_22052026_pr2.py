#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions set diff post-patch PR2 Vague Pieves 22/05/2026.

Verifie :
  - Modif 2b : 5 Valinco sud transferees pieve_sartene -> pieve_istria
  - Modif 3  : pieve_ampugnani creee (7 communes), retirees de pieve_bozio
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIEVES_OUTPUT = ROOT / "docs" / "data" / "pieves_polygons.json"
PIEVES_MAPPINGS = [
    ROOT / "_drafts" / "pieves_communes_mapping.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v2_canonicite_casta.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v3_stratD_2026-05-17.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v4_cleanup_2026-05-18.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v5_vague_22052026.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v5_pr2_arbitrages.json",
]

NEW_PIEVE_SLUG = "pieve_ampugnani"


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
    c2p = build_commune_to_pieve()

    def assert_pieve(commune, expected_pieve, label):
        actual = c2p.get(commune)
        if actual == expected_pieve:
            print(f"  [OK] {label}: {commune} -> {actual}")
        else:
            failures.append(f"{label}: {commune} -> {actual} (attendu {expected_pieve})")
            print(f"  [FAIL] {label}: {commune} -> {actual} (attendu {expected_pieve})")

    def assert_not_pieve(commune, bad_pieve, label):
        actual = c2p.get(commune)
        if actual != bad_pieve:
            print(f"  [OK] {label}: {commune} not in {bad_pieve}")
        else:
            failures.append(f"{label}: {commune} STILL in {bad_pieve}")
            print(f"  [FAIL] {label}: {commune} STILL in {bad_pieve}")

    print("=== Modif 2b - Valinco sud (5 communes) ===")
    for c in ["2A249", "2A349", "2A018", "2A118", "2A310"]:
        assert_pieve(c, "pieve_istria", "Modif 2b")
        assert_not_pieve(c, "pieve_sartene", "Modif 2b")

    print(f"=== Modif 3 - Creation {NEW_PIEVE_SLUG} (7 communes) ===")
    with PIEVES_OUTPUT.open(encoding="utf-8") as f:
        pp = json.load(f)
    pieves_by_slug = {p["slug"]: p for p in pp["pieves"]}
    if NEW_PIEVE_SLUG not in pieves_by_slug:
        failures.append(f"{NEW_PIEVE_SLUG} not present in pieves_polygons.json")
        print(f"  [FAIL] {NEW_PIEVE_SLUG} not present")
    else:
        new_pieve = pieves_by_slug[NEW_PIEVE_SLUG]
        print(f"  [OK] {NEW_PIEVE_SLUG} created (communes_count={new_pieve['communes_count']})")
        doy = new_pieve.get("doyenne_contemporain_override") or new_pieve.get("doyenne_contemporain_majoritaire")
        if doy != "doyenne_plaine_orientale":
            failures.append(f"{NEW_PIEVE_SLUG}.doyenne != doyenne_plaine_orientale (got {doy})")
            print(f"  [FAIL] {NEW_PIEVE_SLUG}.doyenne = {doy}")
        else:
            print(f"  [OK] {NEW_PIEVE_SLUG}.doyenne = doyenne_plaine_orientale")
        if not new_pieve.get("polygon") or len(new_pieve["polygon"]) < 4:
            failures.append(f"{NEW_PIEVE_SLUG}.polygon empty or degenerate")
            print(f"  [FAIL] {NEW_PIEVE_SLUG}.polygon degenerate")
        else:
            print(f"  [OK] {NEW_PIEVE_SLUG}.polygon contains {len(new_pieve['polygon'])} vertices")

    for c in ["2B015", "2B356", "2B364", "2B053", "2B155", "2B161", "2B213"]:
        assert_pieve(c, NEW_PIEVE_SLUG, "Modif 3")
        assert_not_pieve(c, "pieve_bozio", "Modif 3")

    # Sanity counts
    print("\n=== Sanity counts ===")
    expected = {
        "pieve_ampugnani": 7,
        "pieve_istria": 13,      # 8 + 5 Valinco
        "pieve_sartene": 7,      # 12 - 5
        "pieve_bozio": 7,        # 14 - 7
    }
    for slug, exp in expected.items():
        p = pieves_by_slug.get(slug)
        if p:
            ok = "OK" if p["communes_count"] == exp else "FAIL"
            if p["communes_count"] != exp:
                failures.append(f"{slug}.communes_count={p['communes_count']} (attendu {exp})")
            print(f"  [{ok}] {slug}.communes_count={p['communes_count']} (attendu {exp})")

    # Total Corse
    total = sum(p["communes_count"] for p in pp["pieves"])
    print(f"\n=== Total communes mappees : {total} (attendu 360) ===")
    if total != 360:
        failures.append(f"Total mappees = {total} (attendu 360)")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURES ===")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("=== ALL ASSERTIONS PASSED ===")


if __name__ == "__main__":
    main()
