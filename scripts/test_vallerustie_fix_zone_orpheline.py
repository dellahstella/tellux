#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-v9 Vallerustie fix zone orpheline.

Verifie :
  1. 7 transferts effectifs (5 brief + Sermano + Castellare cascade)
  2. pieve_vallerustie 7 -> 14 communes, contigu (dropped=[])
  3. pieve_talcini 9 -> 2 communes (Corte+Casanova), contigu (dropped=[])
  4. Migration 9 sites Tellux vers pieve_vallerustie
  5. Total Corse 360 inchange
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
    ROOT / "_drafts" / "pieves_communes_mapping_v7_vezzani_2026-05-23.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v8_rogna_audit_2026-05-23.json",
    ROOT / "_drafts" / "pieves_communes_mapping_v9_fix_zombies_orphelines_vallerustie.json",
]

VALLERUSTIE_TRANSFERS = {
    "2B193": "Omessa",
    "2B306": "Santa-Lucia-di-Mercurio",
    "2B289": "Soveria",
    "2B329": "Tralonca",
    "2B083": "Castirla",
    "2B275": "Sermano",                    # cascade niveau 1
    "2B078": "Castellare-di-Mercurio",     # cascade niveau 2
}

SITES_MIGRATED = {
    # Brief original
    "pont_genois_castirla", "san_martinu_omessa", "santa_maria_francardo_omessa",
    "santa_maria_tralonca", "santa_maria_castirla",
    # Cascade
    "menhir_sermano", "san_nicolao_sermano", "sant_andria_sermano_haut",
    "san_nicolao_castellare_di_mercurio",
}


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

    # 1. Transferts vers pieve_vallerustie
    print(f"=== Transferts vers pieve_vallerustie (7 communes) ===")
    for insee, nom in VALLERUSTIE_TRANSFERS.items():
        actual = c2p.get(insee)
        if actual == "pieve_vallerustie":
            print(f"  [OK] {insee} {nom:30s} -> pieve_vallerustie")
        else:
            failures.append(f"{insee} {nom} -> {actual} (attendu pieve_vallerustie)")
            print(f"  [FAIL] {insee} {nom} -> {actual}")

    # 2. pieve_vallerustie counts + contiguite
    print(f"\n=== Contiguite + counts ===")
    with PIEVES_OUTPUT.open(encoding="utf-8") as f:
        pp = json.load(f)
    by_slug = {p["slug"]: p for p in pp["pieves"]}
    for slug, expected_count in (("pieve_vallerustie", 14), ("pieve_talcini", 2)):
        p = by_slug.get(slug)
        if not p:
            failures.append(f"{slug} ABSENT")
            print(f"  [FAIL] {slug} ABSENT")
            continue
        if p["communes_count"] != expected_count:
            failures.append(f"{slug}.communes_count={p['communes_count']} (attendu {expected_count})")
            print(f"  [FAIL] {slug}.communes_count={p['communes_count']} (attendu {expected_count})")
        else:
            print(f"  [OK] {slug}.communes_count = {expected_count}")
        dropped = p.get("multipolygon_dropped_areas_km2", [])
        if dropped:
            failures.append(f"{slug}.multipolygon_dropped = {dropped} (attendu [])")
            print(f"  [FAIL] {slug}.dropped = {dropped}")
        else:
            print(f"  [OK] {slug} sans fragments dropped (contigu)")

    # 3. Migration sites
    print(f"\n=== Migration sites Tellux ({len(SITES_MIGRATED)} attendus) ===")
    with SITES_OUTPUT.open(encoding="utf-8") as f:
        sp = json.load(f)
    bad = []
    for s in sp["sites"]:
        if s.get("slug") in SITES_MIGRATED:
            if s.get("pieve_slug") != "pieve_vallerustie":
                bad.append(f"{s['slug']} pieve={s.get('pieve_slug')}")
            if s.get("doyenne_contemporain_slug") != "doyenne_cortenais":
                bad.append(f"{s['slug']} doy={s.get('doyenne_contemporain_slug')}")
    if bad:
        for b in bad:
            failures.append(f"site mal aligne : {b}")
            print(f"  [FAIL] {b}")
    else:
        print(f"  [OK] {len(SITES_MIGRATED)} sites tous alignes pieve_vallerustie/doyenne_cortenais")

    # 4. Total Corse 360
    total = sum(p["communes_count"] for p in pp["pieves"])
    print(f"\n=== Total Corse : {total} (attendu 360) ===")
    if total != 360:
        failures.append(f"Total = {total}")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURES ===")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("=== ALL ASSERTIONS PASSED ===")


if __name__ == "__main__":
    main()
