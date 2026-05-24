#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-fix GPS Pont du Diable Castirla.

Verifie :
  1. GPS dans bbox Castirla (brief : 42.35 <= lat <= 42.40, 9.10 <= lon <= 9.15)
  2. gps_locked = True (arbitrage explicite Soleil contre re-derivation)
  3. Rattachements inchanges (commune_insee, pieve_slug, doyenne_contemporain_slug)
  4. gps_source documente la correction
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES = ROOT / "docs" / "data" / "sites_patrimoine.json"

with SITES.open(encoding="utf-8") as f:
    sp = json.load(f)
site = next((s for s in sp["sites"] if s.get("slug") == "pont_genois_castirla"), None)
assert site is not None, "FAIL : pont_genois_castirla introuvable"

failures = []

# 1. GPS dans bbox Castirla
print("=== GPS dans bbox commune Castirla ===")
lat, lon = site["lat"], site["lon"]
if not (42.35 <= lat <= 42.40):
    failures.append(f"lat={lat} hors bbox [42.35, 42.40]")
    print(f"  [FAIL] lat={lat}")
else:
    print(f"  [OK] lat={lat} dans [42.35, 42.40]")
if not (9.10 <= lon <= 9.15):
    failures.append(f"lon={lon} hors bbox [9.10, 9.15]")
    print(f"  [FAIL] lon={lon}")
else:
    print(f"  [OK] lon={lon} dans [9.10, 9.15]")

# 2. gps_locked
print("\n=== gps_locked ===")
if site.get("gps_locked") is not True:
    failures.append(f"gps_locked={site.get('gps_locked')} (attendu True)")
    print(f"  [FAIL] gps_locked={site.get('gps_locked')}")
else:
    print(f"  [OK] gps_locked = True")

# 3. Rattachements inchanges
print("\n=== Rattachements inchanges ===")
expected = {
    "commune_insee": "2B083",
    "commune_nom": "Castirla",
    "pieve_slug": "pieve_vallerustie",
    "doyenne_contemporain_slug": "doyenne_cortenais",
    "axe_corpus": "ponts_historiques",
    "phase_publication": 1,
}
for k, v in expected.items():
    actual = site.get(k)
    if actual != v:
        failures.append(f"{k}={actual} (attendu {v})")
        print(f"  [FAIL] {k}={actual} (attendu {v})")
    else:
        print(f"  [OK] {k}={actual}")

# 4. gps_source documente
print("\n=== gps_source documente ===")
src = site.get("gps_source", "")
if "Estimation centroide" in src or "centroïde" in src:
    failures.append("gps_source contient encore 'centroide' (ancienne valeur)")
    print(f"  [FAIL] gps_source = {src!r}")
elif not src or len(src) < 20:
    failures.append(f"gps_source trop court ou vide : {src!r}")
    print(f"  [FAIL] gps_source = {src!r}")
else:
    print(f"  [OK] gps_source = {src!r}")

print()
if failures:
    print(f"=== {len(failures)} FAILURES ===")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("=== ALL ASSERTIONS PASSED ===")
