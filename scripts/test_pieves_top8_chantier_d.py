#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-refactor Chantier D global (Top 8 generalise toutes pieves > 8 sites).

Verifie :
  1. Map PIEVE_TOP8 declaree dans patrimoine.html
  2. Anciennes constantes PIEVE_ROGLIANO_TOP8 + PIEVE_NEBBIU_TOP8 supprimees (code)
  3. 15 pieves attendues dans la Map
  4. Chaque pieve contient exactement 8 slugs
  5. Tous les slugs existent dans sites_patrimoine.json
  6. spotVisibleAtNiveau2 utilise PIEVE_TOP8.get() (pas les anciennes constantes)
  7. Doctrine N2/N3 preservee : sitesPieve (N3) reste exhaustif
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "patrimoine.html"
SITES = ROOT / "docs" / "data" / "sites_patrimoine.json"

EXPECTED_PIEVES = {
    "pieve_rogliano", "pieve_nebbiu",  # preserves doctrine acquise
    "pieve_sartene", "pieve_carbini", "pieve_calenzana", "pieve_piana",
    "pieve_istria", "pieve_ornano", "pieve_bonifacio", "pieve_talcini",
    "pieve_aregno", "pieve_vico", "pieve_gulfo_d_aiacciu",
    "pieve_castagniccia", "pieve_niolu",
}


def main():
    failures = []
    content = HTML.read_text(encoding="utf-8")

    # 1. Map PIEVE_TOP8 declaree
    print("=== Map PIEVE_TOP8 declaration ===")
    if "const PIEVE_TOP8 = new Map(" not in content:
        failures.append("const PIEVE_TOP8 = new Map(...) absent")
        print("  [FAIL] PIEVE_TOP8 absent")
    else:
        print("  [OK] PIEVE_TOP8 Map declaration trouvee")

    # 2. Anciennes constantes JS supprimees (les refs en commentaire OK)
    print("\n=== Anciennes constantes JS supprimees ===")
    for old in ("const PIEVE_ROGLIANO_TOP8", "const PIEVE_NEBBIU_TOP8"):
        if old in content:
            failures.append(f"ancienne constante {old} encore presente")
            print(f"  [FAIL] {old} encore presente")
        else:
            print(f"  [OK] {old} supprimee")

    # 3-4. 15 pieves, chacune 8 slugs
    print(f"\n=== 15 pieves x 8 slugs ===")
    m = re.search(r"const PIEVE_TOP8 = new Map\(\[(.*?)\]\);", content, re.DOTALL)
    if not m:
        failures.append("Extraction Map echec")
        print("  [FAIL] Extraction Map echec")
    else:
        block = m.group(1)
        entries = re.findall(r"\['(pieve_\w+)',\s*new Set\(\[(.*?)\]\)\]", block, re.DOTALL)
        pieves_found = {p for p, _ in entries}
        missing = EXPECTED_PIEVES - pieves_found
        extra = pieves_found - EXPECTED_PIEVES
        if missing:
            failures.append(f"pieves manquantes dans Map : {missing}")
            print(f"  [FAIL] pieves manquantes : {missing}")
        if extra:
            failures.append(f"pieves inattendues dans Map : {extra}")
            print(f"  [FAIL] pieves inattendues : {extra}")
        if not missing and not extra:
            print(f"  [OK] 15 pieves attendues toutes presentes")

        # Verifier 8 slugs par pieve
        for pieve, set_content in entries:
            slugs = re.findall(r'"([a-z0-9_]+)"', set_content)
            if len(slugs) != 8:
                failures.append(f"{pieve} contient {len(slugs)} slugs (attendu 8)")
                print(f"  [FAIL] {pieve} : {len(slugs)} slugs")
            else:
                print(f"  [OK] {pieve} : 8 slugs")

    # 5. Tous slugs existent dans sites_patrimoine.json
    print(f"\n=== Slugs presents dans sites_patrimoine.json ===")
    with SITES.open(encoding="utf-8") as f:
        sp = json.load(f)
    all_slugs = {s["slug"] for s in sp["sites"]}
    if m:
        for pieve, set_content in entries:
            slugs = re.findall(r'"([a-z0-9_]+)"', set_content)
            missing_slugs = [s for s in slugs if s not in all_slugs]
            if missing_slugs:
                failures.append(f"{pieve} : slugs invalides {missing_slugs}")
                print(f"  [FAIL] {pieve} slugs invalides : {missing_slugs}")
        if not any(f.startswith("pieve_") and "slugs invalides" in f for f in failures):
            print(f"  [OK] Tous les slugs de la Map existent dans sites_patrimoine.json")

    # 6. spotVisibleAtNiveau2 utilise PIEVE_TOP8
    print(f"\n=== spotVisibleAtNiveau2 refactore ===")
    sv_m = re.search(r"function spotVisibleAtNiveau2\(site\)\s*\{(.*?)\n\}", content, re.DOTALL)
    if not sv_m:
        failures.append("spotVisibleAtNiveau2 introuvable")
        print("  [FAIL] spotVisibleAtNiveau2 introuvable")
    else:
        body = sv_m.group(1)
        if "PIEVE_TOP8.get(" not in body:
            failures.append("spotVisibleAtNiveau2 n'utilise pas PIEVE_TOP8.get()")
            print("  [FAIL] spotVisibleAtNiveau2 n'utilise pas PIEVE_TOP8.get()")
        else:
            print("  [OK] spotVisibleAtNiveau2 utilise PIEVE_TOP8.get(pv)")
        # Verifier que les anciennes references sont parties
        for old in ("PIEVE_ROGLIANO_TOP8.has", "PIEVE_NEBBIU_TOP8.has"):
            if old in body:
                failures.append(f"spotVisibleAtNiveau2 contient encore {old}")
                print(f"  [FAIL] {old} encore present")

    # 7. Doctrine N2/N3 preservee : sitesPieve (N3) exhaustif
    print(f"\n=== Doctrine N2/N3 (sitesPieve N3 exhaustif) ===")
    # On verifie qu'il n'y a PAS de "PIEVE_TOP8" dans le scope sitesPieve (entre const sitesPieve et la closure})
    sp_m = re.search(r"const sitesPieve = .*?\.filter\(function\(s\)\s*\{(.*?)\}\);", content, re.DOTALL)
    if sp_m:
        sp_body = sp_m.group(1)
        if "PIEVE_TOP8" in sp_body:
            failures.append("sitesPieve (N3) contient un filtre PIEVE_TOP8 — doctrine N3 exhaustive violee")
            print("  [FAIL] sitesPieve filtre par PIEVE_TOP8 (doctrine N3 exhaustive violee)")
        else:
            print("  [OK] sitesPieve (N3) reste exhaustif (pas de filtre PIEVE_TOP8)")

    print()
    if failures:
        print(f"=== {len(failures)} FAILURES ===")
        for f in failures:
            print("  - " + f)
        sys.exit(1)
    print("=== ALL ASSERTIONS PASSED ===")


if __name__ == "__main__":
    main()
