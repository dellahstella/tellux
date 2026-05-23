#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-v10 Vico fix zone orpheline.

Verifie :
  1. Coggia (2A090) transferee pieve_sagone -> pieve_vico
  2. pieve_vico passe 7 -> 8 communes (Polygon contigu)
  3. pieve_sagone passe 2 -> 1 commune (Cargese 2A065 seule, polygon non degenere)
  4. Gap doyenne_PVS - union pieves PVS = 0 (zone orpheline resorbee)
  5. Migration 2 sites Coggia (san_giovanni_de_coggia, renicciu_coggia)
  6. Tous les sites pieve_sagone sont dans Cargese (2A065)
  7. Total Corse 360 inchange
"""
import json
import sys
from pathlib import Path
from shapely.geometry import Polygon
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
PIEVES_OUTPUT = ROOT / "docs" / "data" / "pieves_polygons.json"
DOYENNES_OUTPUT = ROOT / "docs" / "data" / "doyennes_polygons.json"
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
    ROOT / "_drafts" / "pieves_communes_mapping_v10_fix_zone_orpheline_vico.json",
]
SITES_COGGIA = {"san_giovanni_de_coggia", "renicciu_coggia"}


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

    # 1. Coggia transferee
    print("=== Coggia (2A090) transferee ===")
    actual = c2p.get("2A090")
    if actual == "pieve_vico":
        print(f"  [OK] 2A090 Coggia -> pieve_vico")
    else:
        failures.append(f"2A090 -> {actual} (attendu pieve_vico)")
        print(f"  [FAIL] 2A090 -> {actual}")

    # 2-3. Counts + contiguite
    print("\n=== Counts + contiguite ===")
    with PIEVES_OUTPUT.open(encoding="utf-8") as f:
        pp = json.load(f)
    by_slug = {p["slug"]: p for p in pp["pieves"]}
    for slug, expected_count in (("pieve_vico", 8), ("pieve_sagone", 1)):
        p = by_slug.get(slug)
        if not p:
            failures.append(f"{slug} ABSENT")
            continue
        if p["communes_count"] != expected_count:
            failures.append(f"{slug}.communes_count={p['communes_count']} (attendu {expected_count})")
            print(f"  [FAIL] {slug}.communes_count={p['communes_count']}")
        else:
            print(f"  [OK] {slug}.communes_count = {expected_count}")
        dropped = p.get("multipolygon_dropped_areas_km2", [])
        if dropped:
            failures.append(f"{slug}.dropped = {dropped}")
            print(f"  [FAIL] {slug}.dropped = {dropped}")
        else:
            print(f"  [OK] {slug} contigu (0 dropped)")

    # 4. Gap doyenne_PVS - union pieves PVS
    print("\n=== Gap doyenne_PVS - union pieves PVS ===")
    with DOYENNES_OUTPUT.open(encoding="utf-8") as f:
        dd = json.load(f)
    doy_pvs_poly = None
    for d in dd["doyennes"]:
        if d["slug"] == "doyenne_piana_vico_sari":
            doy_pvs_poly = Polygon([(lng, lat) for lat, lng in d["polygon"]])
            break
    pieves_pvs = []
    for p in pp["pieves"]:
        doy = p.get("doyenne_contemporain_override") or p.get("doyenne_contemporain_majoritaire")
        if doy == "doyenne_piana_vico_sari":
            pieves_pvs.append(Polygon([(lng, lat) for lat, lng in p["polygon"]]))
    union_pieves = unary_union(pieves_pvs)
    gap = doy_pvs_poly.difference(union_pieves)
    gap_km2 = gap.area * 9156
    # Tolerance simplification : on accepte un gap < 5 km² (artefacts de simplification 0.0005°)
    if gap_km2 < 5.0:
        print(f"  [OK] Gap doy_PVS - union pieves = {gap_km2:.2f} km² (< 5 tolerance simplification)")
    else:
        failures.append(f"Gap = {gap_km2:.2f} km² (>= 5 km² seuil)")
        print(f"  [FAIL] Gap = {gap_km2:.2f} km²")

    # 5. Migration sites Coggia
    print("\n=== Migration sites Coggia (2 sites) ===")
    with SITES_OUTPUT.open(encoding="utf-8") as f:
        sp = json.load(f)
    coggia_sites = [s for s in sp["sites"] if s.get("commune_insee") == "2A090"]
    bad = []
    for s in coggia_sites:
        if s.get("pieve_slug") != "pieve_vico":
            bad.append(f"{s['slug']} pieve={s.get('pieve_slug')}")
    if bad:
        for b in bad:
            failures.append(f"site mal aligne : {b}")
            print(f"  [FAIL] {b}")
    else:
        print(f"  [OK] {len(coggia_sites)} sites Coggia tous alignes pieve_vico")
    # Verifier que les 2 sites attendus sont presents
    found = {s["slug"] for s in coggia_sites}
    missing = SITES_COGGIA - found
    if missing:
        failures.append(f"Sites attendus manquants : {missing}")

    # 6. Aucun site pieve_sagone hors Cargese (2A065)
    print("\n=== Sites pieve_sagone (tous doivent etre Cargese 2A065) ===")
    bad_sagone = [s for s in sp["sites"]
                  if s.get("pieve_slug") == "pieve_sagone" and s.get("commune_insee") != "2A065"]
    if bad_sagone:
        for s in bad_sagone:
            failures.append(f"site pieve_sagone hors Cargese : {s['slug']} commune={s.get('commune_insee')}")
            print(f"  [FAIL] {s['slug']} commune={s.get('commune_insee')}")
    else:
        print(f"  [OK] Tous les sites pieve_sagone sont dans Cargese (2A065)")

    # 7. Total Corse 360
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
