#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-creation pieve_tavignano (Brief BRIEF_CODE_CREATION_PIEVE_TAVIGNANO).

Verifie :
  1. Creation pieve_tavignano (9 communes, doyenne_plaine_orientale)
  2. Disparition pieve_ghisoni (1 commune unique transferee)
  3. Set diff : 9 communes deplacees, 3 exclues (Vezzani/Muracciole/Rospigliani restent)
  4. Migration 8 sites Tellux vers pieve_tavignano / doyenne_plaine_orientale
  5. Cascade pieves d'origine (decompte attendu)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PIEVES_OUTPUT = ROOT / "docs" / "data" / "pieves_polygons.json"
SITES_OUTPUT = ROOT / "docs" / "data" / "sites_patrimoine.json"
PIEVES_MAPPINGS = [
    ROOT / "_drafts" / "pieves_communes_mapping.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v2_canonicite_casta.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v3_stratD_2026-05-17.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v4_cleanup_2026-05-18.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v5_vague_22052026.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v5_pr2_arbitrages.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v6_tavignano_2026-05-23.json",
]

NEW_PIEVE_SLUG = "pieve_tavignano"
TAVIGNANO_COMMUNES = {
    "2B229": ("Pietroso", "pieve_venaco"),
    "2B016": ("Antisanti", "pieve_rogna"),
    "2B126": ("Giuncaggio", "pieve_rogna"),
    "2B201": ("Pancheraccia", "pieve_rogna"),
    "2B075": ("Casevecchie", "pieve_aleria"),
    "2B002": ("Aghione", "pieve_aleria"),
    "2B236": ("Poggio-di-Nazza", "pieve_fiumorbo"),
    "2B149": ("Lugo-di-Nazza", "pieve_fiumorbo"),
    "2B124": ("Ghisoni", "pieve_ghisoni"),
}
EXCLUS = {"2B347": "Vezzani", "2B171": "Muracciole", "2B263": "Rospigliani"}


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

    with PIEVES_OUTPUT.open(encoding="utf-8") as f:
        pp = json.load(f)
    by_slug = {p["slug"]: p for p in pp["pieves"]}

    # 1. Creation pieve_tavignano
    print(f"=== Creation {NEW_PIEVE_SLUG} ===")
    if NEW_PIEVE_SLUG not in by_slug:
        failures.append(f"{NEW_PIEVE_SLUG} ABSENT du JSON output")
        print(f"  [FAIL] {NEW_PIEVE_SLUG} ABSENT du JSON output")
    else:
        nt = by_slug[NEW_PIEVE_SLUG]
        print(f"  [OK] {NEW_PIEVE_SLUG} present (communes_count={nt['communes_count']})")
        doy = nt.get("doyenne_contemporain_override") or nt.get("doyenne_contemporain_majoritaire")
        if doy != "doyenne_plaine_orientale":
            failures.append(f"{NEW_PIEVE_SLUG}.doyenne={doy} (attendu doyenne_plaine_orientale)")
            print(f"  [FAIL] {NEW_PIEVE_SLUG}.doyenne={doy}")
        else:
            print(f"  [OK] {NEW_PIEVE_SLUG}.doyenne = doyenne_plaine_orientale")
        if nt["communes_count"] != 9:
            failures.append(f"{NEW_PIEVE_SLUG}.communes_count={nt['communes_count']} (attendu 9)")
            print(f"  [FAIL] {NEW_PIEVE_SLUG}.communes_count={nt['communes_count']}")
        else:
            print(f"  [OK] {NEW_PIEVE_SLUG}.communes_count = 9")
        if not nt.get("polygon") or len(nt["polygon"]) < 4:
            failures.append(f"{NEW_PIEVE_SLUG}.polygon degenere")
            print(f"  [FAIL] {NEW_PIEVE_SLUG}.polygon degenere")
        else:
            print(f"  [OK] {NEW_PIEVE_SLUG}.polygon = {len(nt['polygon'])} vertices")

    # 2. Disparition pieve_ghisoni
    print(f"\n=== Disparition pieve_ghisoni ===")
    if "pieve_ghisoni" in by_slug:
        failures.append(f"pieve_ghisoni ENCORE present (communes_count={by_slug['pieve_ghisoni']['communes_count']})")
        print(f"  [FAIL] pieve_ghisoni encore present")
    else:
        print(f"  [OK] pieve_ghisoni ABSENT du JSON output")

    # 3. Set diff communes Tavignano
    print(f"\n=== Set diff : 9 communes -> {NEW_PIEVE_SLUG} ===")
    for insee, (nom, origin) in TAVIGNANO_COMMUNES.items():
        actual = c2p.get(insee)
        if actual == NEW_PIEVE_SLUG:
            print(f"  [OK] {insee} {nom:20s} -> {actual}")
        else:
            failures.append(f"{insee} {nom} -> {actual} (attendu {NEW_PIEVE_SLUG})")
            print(f"  [FAIL] {insee} {nom} -> {actual}")
        # Verifier qu'elles ne sont plus dans leur pieve d'origine
        if actual == origin:
            failures.append(f"{insee} {nom} STILL in {origin}")
            print(f"  [FAIL] {insee} {nom} STILL in {origin}")

    # 4. Exclus restent dans pieve_venaco
    print(f"\n=== Exclus (3 communes) ===")
    for insee, nom in EXCLUS.items():
        actual = c2p.get(insee)
        if actual == "pieve_venaco":
            print(f"  [OK] {insee} {nom:14s} -> pieve_venaco (exclu OK)")
        else:
            failures.append(f"Exclu {insee} {nom} -> {actual} (attendu pieve_venaco)")
            print(f"  [FAIL] Exclu {insee} {nom} -> {actual}")

    # 5. Cascade counts
    print(f"\n=== Cascade pieves d'origine ===")
    expected_counts = {
        "pieve_tavignano": 9,
        "pieve_venaco": 8,     # 9 - 1 (Pietroso)
        "pieve_rogna": 3,      # 6 - 3 (Antisanti/Giuncaggio/Pancheraccia) — DEGENERE en MultiPolygon
        "pieve_aleria": 2,     # 4 - 2 (Casevecchie/Aghione)
        "pieve_fiumorbo": 8,   # 10 - 2 (Poggio-di-Nazza/Lugo-di-Nazza)
    }
    for slug, exp in expected_counts.items():
        p = by_slug.get(slug)
        if p:
            ok = "OK" if p["communes_count"] == exp else "FAIL"
            if p["communes_count"] != exp:
                failures.append(f"{slug}.communes_count={p['communes_count']} (attendu {exp})")
            print(f"  [{ok}] {slug}.communes_count = {p['communes_count']} (attendu {exp})")

    # 6. Total Corse 360 inchange
    total = sum(p["communes_count"] for p in pp["pieves"])
    print(f"\n=== Total Corse : {total} (attendu 360) ===")
    if total != 360:
        failures.append(f"Total Corse = {total} (attendu 360)")

    # 7. Migration sites Tellux : 8 sites doivent pointer vers pieve_tavignano + doyenne_PO
    print(f"\n=== Migration 8 sites Tellux ===")
    with SITES_OUTPUT.open(encoding="utf-8") as f:
        sp = json.load(f)
    migrated = []
    for s in sp["sites"]:
        if s.get("commune_insee") in TAVIGNANO_COMMUNES:
            migrated.append(s)
    print(f"  {len(migrated)} sites dans les 9 communes Tavignano")
    bad = []
    for s in migrated:
        if s.get("pieve_slug") != "pieve_tavignano":
            bad.append(f"{s['slug']} pieve={s.get('pieve_slug')}")
        if s.get("doyenne_contemporain_slug") != "doyenne_plaine_orientale":
            bad.append(f"{s['slug']} doy={s.get('doyenne_contemporain_slug')}")
    if bad:
        for b in bad:
            failures.append(f"site mal aligne : {b}")
            print(f"  [FAIL] {b}")
    else:
        print(f"  [OK] {len(migrated)} sites tous alignes sur pieve_tavignano + doyenne_plaine_orientale")

    # 8. Pas de site Tellux pointant vers pieve_ghisoni (qui disparait)
    orphans_ghisoni = [s for s in sp["sites"] if s.get("pieve_slug") == "pieve_ghisoni"]
    if orphans_ghisoni:
        for s in orphans_ghisoni:
            failures.append(f"site pointe vers pieve_ghisoni (disparait) : {s['slug']}")
            print(f"  [FAIL] site orphelin pieve_ghisoni : {s['slug']}")
    else:
        print(f"  [OK] 0 site pointe vers pieve_ghisoni (disparait propre)")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURES ===")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("=== ALL ASSERTIONS PASSED ===")


if __name__ == "__main__":
    main()
