#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions set diff post-patch PR1 Vague Pieves 22/05/2026.

Doctrine : feedback_transferts_assert_set_diff.md — verifier l'identite des
communes transferees (pas seulement le compte) pour detecter substitution.

Verifie :
  - Modif 1a : Coggia (2A090) dans pieve_sagone, retiree de pieve_cinarca
  - Modif 1b : Osani (2A197) dans pieve_piana, retiree de pieve_vico
  - Modif 4  : 4 Solenzara dans pieve_fiumorbo, retirees de pieve_verde
  - Modif 2a : Bastelicaccia (2A032) dans doyenne_ajaccio, retiree de PTV

Source verite cote pieves : reconstruction du chaining v1+v2+v3+v4+v5
(car docs/data/pieves_polygons.json ne stocke pas communes_insee).
Source verite cote doyennes : _drafts/doyennes_communes_mapping.json.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOYENNES_MAPPING = ROOT / "_drafts" / "doyennes_communes_mapping.json"
PIEVES_MAPPINGS = [
    ROOT / "_drafts" / "pieves_communes_mapping.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v2_canonicite_casta.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v3_stratD_2026-05-17.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v4_cleanup_2026-05-18.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v5_vague_22052026.json",
]
PIEVES_OUTPUT = ROOT / "docs" / "data" / "pieves_polygons.json"


def build_commune_to_pieve():
    """Reconstitue commune_to_pieve final apres chaining v1->v5."""
    c2p = {}
    # v1 (base)
    with PIEVES_MAPPINGS[0].open(encoding="utf-8") as f:
        data = json.load(f)
    for p in data["pieves"]:
        for insee in p["communes_insee"]:
            c2p[insee] = p["slug"]
    # v2-v5
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

    print("=== Modif 1a - Coggia (2A090) ===")
    assert_pieve("2A090", "pieve_sagone", "Modif 1a")
    assert_not_pieve("2A090", "pieve_cinarca", "Modif 1a")

    print("=== Modif 1b - Osani (2A197) ===")
    assert_pieve("2A197", "pieve_piana", "Modif 1b")
    assert_not_pieve("2A197", "pieve_vico", "Modif 1b")

    print("=== Modif 4 - Solenzara (4 communes) ===")
    for c in ["2A269", "2B283", "2B366", "2B342"]:
        assert_pieve(c, "pieve_fiumorbo", "Modif 4")
        assert_not_pieve(c, "pieve_verde", "Modif 4")

    print("=== Modif 2a - Bastelicaccia (2A032) ===")
    assert_pieve("2A032", "pieve_gulfo_d_aiacciu", "Modif 2a pieves")
    # Cote doyennes (debordement traite via _drafts/doyennes_communes_mapping.json)
    with DOYENNES_MAPPING.open(encoding="utf-8") as f:
        dm = json.load(f)
    aja = next(d for d in dm["doyennes"] if d["slug"] == "doyenne_ajaccio")
    ptv = next(d for d in dm["doyennes"] if d["slug"] == "doyenne_prunelli_taravo_valinco")
    if "2A032" in aja["communes_insee"]:
        print(f"  [OK] Modif 2a doyennes: 2A032 in doyenne_ajaccio ({len(aja['communes_insee'])} communes)")
    else:
        failures.append("Modif 2a doyennes: 2A032 NOT in doyenne_ajaccio")
        print("  [FAIL] Modif 2a doyennes: 2A032 NOT in doyenne_ajaccio")
    if "2A032" not in ptv["communes_insee"]:
        print(f"  [OK] Modif 2a doyennes: 2A032 not in doyenne_PTV ({len(ptv['communes_insee'])} communes)")
    else:
        failures.append("Modif 2a doyennes: 2A032 STILL in doyenne_PTV")
        print("  [FAIL] Modif 2a doyennes: 2A032 STILL in doyenne_PTV")

    # Sanity check : total Corse inchange (360 communes)
    all_communes = set()
    for d in dm["doyennes"]:
        all_communes.update(d["communes_insee"])
    print(f"\n=== Total Corse: {len(all_communes)} (attendu 360) ===")
    if len(all_communes) != 360:
        failures.append(f"Total Corse: {len(all_communes)} (attendu 360)")

    # Sanity check : pieves_polygons.json regenere coherent
    with PIEVES_OUTPUT.open(encoding="utf-8") as f:
        pp = json.load(f)
    pieves_by_slug = {p["slug"]: p for p in pp["pieves"]}
    print(f"\n=== Sanity pieves_polygons.json ===")
    for slug, expected_count in [("pieve_fiumorbo", 10),  # 6 + 4 Solenzara
                                  ("pieve_verde", 4),      # 8 - 4 Solenzara
                                  ("pieve_sagone", 2),     # inchange
                                  ("pieve_piana", 7),      # inchange (v4 deja a 7)
                                  ("pieve_cinarca", 8),    # inchange (v1 avait deja 9 mais 2A090 deja deplace par v4 mapping)
                                  ("pieve_vico", 7)]:      # inchange
        p = pieves_by_slug.get(slug)
        if p:
            ok = "OK" if p["communes_count"] == expected_count else "INFO"
            print(f"  [{ok}] {slug}: communes_count={p['communes_count']} (attendu {expected_count})")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURES ===")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("=== ALL ASSERTIONS PASSED ===")


if __name__ == "__main__":
    main()
