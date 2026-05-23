#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-audit pieve_rogna (Bustanico+Sermano transferes).

Verifie :
  1. Bustanico (2B045) pieve_rogna -> pieve_bozio
  2. Sermano (2B275) pieve_rogna -> pieve_talcini
  3. Tallone (2B320) reste pieve_rogna (1 commune unique)
  4. pieve_rogna n'a plus de fragments dropped (resorption MultiPolygon degenere)
  5. Cascade counts (pieve_bozio +1, pieve_talcini +1, pieve_rogna -2)
  6. Site sant_andria_sermano_haut realigne pieve_bozio -> pieve_talcini
  7. Total Corse 360 inchange
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
]


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

    # 1-3. Set diff communes
    print("=== Set diff communes ===")
    expected = {
        "2B045": ("Bustanico", "pieve_bozio", "pieve_rogna"),
        "2B275": ("Sermano", "pieve_talcini", "pieve_rogna"),
        "2B320": ("Tallone", "pieve_rogna", None),  # reste
    }
    for insee, (nom, expected_pieve, origin) in expected.items():
        actual = c2p.get(insee)
        if actual == expected_pieve:
            print(f"  [OK] {insee} {nom:14s} -> {actual}")
        else:
            failures.append(f"{insee} {nom} -> {actual} (attendu {expected_pieve})")
            print(f"  [FAIL] {insee} {nom} -> {actual} (attendu {expected_pieve})")
        if origin and actual == origin:
            failures.append(f"{insee} {nom} STILL in {origin}")
            print(f"  [FAIL] {insee} {nom} STILL in {origin}")

    # 4. pieve_rogna résorbée
    print("\n=== Résorption pieve_rogna (MultiPolygon dégénéré) ===")
    p_rogna = by_slug.get("pieve_rogna")
    if not p_rogna:
        failures.append("pieve_rogna ABSENT du JSON")
        print("  [FAIL] pieve_rogna ABSENT du JSON")
    else:
        if p_rogna["communes_count"] != 1:
            failures.append(f"pieve_rogna.communes_count={p_rogna['communes_count']} (attendu 1)")
            print(f"  [FAIL] pieve_rogna.communes_count={p_rogna['communes_count']}")
        else:
            print(f"  [OK] pieve_rogna.communes_count = 1 (Tallone seule)")
        dropped = p_rogna.get("multipolygon_dropped_areas_km2", [])
        if dropped:
            failures.append(f"pieve_rogna.multipolygon_dropped = {dropped} (attendu [])")
            print(f"  [FAIL] pieve_rogna.multipolygon_dropped = {dropped}")
        else:
            print(f"  [OK] pieve_rogna sans fragments dropped (MultiPolygon resorbe)")

    # 5. Cascade counts
    print("\n=== Cascade counts ===")
    expected_counts = {
        "pieve_rogna": 1,
        "pieve_bozio": 8,      # 7 + Bustanico
        "pieve_talcini": 9,    # 8 + Sermano
    }
    for slug, exp in expected_counts.items():
        p = by_slug.get(slug)
        if p:
            ok = "OK" if p["communes_count"] == exp else "FAIL"
            if p["communes_count"] != exp:
                failures.append(f"{slug}.communes_count={p['communes_count']} (attendu {exp})")
            print(f"  [{ok}] {slug}.communes_count = {p['communes_count']} (attendu {exp})")

    # 6. Migration site sant_andria_sermano_haut
    print("\n=== Migration site sant_andria_sermano_haut ===")
    with SITES_OUTPUT.open(encoding="utf-8") as f:
        sp = json.load(f)
    site = next((s for s in sp["sites"] if s.get("slug") == "sant_andria_sermano_haut"), None)
    if not site:
        failures.append("Site sant_andria_sermano_haut introuvable")
        print("  [FAIL] Site introuvable")
    else:
        if site.get("pieve_slug") == "pieve_talcini":
            print(f"  [OK] sant_andria_sermano_haut.pieve_slug = pieve_talcini")
        else:
            failures.append(f"sant_andria_sermano_haut.pieve_slug = {site.get('pieve_slug')}")
            print(f"  [FAIL] pieve_slug = {site.get('pieve_slug')}")

    # 7. Aucun site pointe vers pieve_rogna sauf ceux dans Tallone (2B320)
    # Exception : sites avec commune_insee=None = dette INSEE separee (a traiter
    # dans un brief dedie), pas une regression de cette PR.
    print("\n=== Sites pointant pieve_rogna ===")
    DEBT_NO_INSEE = {"san_quilicu_prunete_village"}  # dette pre-existante commune_insee=None
    bad_rogna = [s for s in sp["sites"]
                 if s.get("pieve_slug") == "pieve_rogna"
                 and s.get("commune_insee") != "2B320"
                 and s["slug"] not in DEBT_NO_INSEE]
    if bad_rogna:
        for s in bad_rogna:
            failures.append(f"site {s['slug']} pieve_rogna mais commune {s.get('commune_insee')} != Tallone")
            print(f"  [FAIL] {s['slug']} commune={s.get('commune_insee')}")
    else:
        print(f"  [OK] Tous les sites pieve_rogna sont dans Tallone (sauf dette DEBT_NO_INSEE)")
        for slug in DEBT_NO_INSEE:
            print(f"    DETTE : {slug} (commune_insee=None, brief INSEE separe a traiter)")

    # 8. Total Corse 360
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
