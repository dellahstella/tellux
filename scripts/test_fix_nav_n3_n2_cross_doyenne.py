#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifie que le patch nav N3->N2 cross-doyenne a bien ete applique a
enterNiveau2View (cleanup symetrique exitNiveau3View)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "patrimoine.html"
content = HTML.read_text(encoding="utf-8")

# Localiser le corps de enterNiveau2View
idx_start = content.find("function enterNiveau2View")
idx_end = content.find("function enterNiveau3View")
assert idx_start > 0, "FAIL : enterNiveau2View introuvable"
assert idx_end > idx_start, "FAIL : enterNiveau3View introuvable"
fn_body = content[idx_start:idx_end]

assertions = [
    ("clusterGroupN3 && map.hasLayer(clusterGroupN3)", "cleanup clusterGroupN3 hasLayer manquant"),
    ("clusterGroupN3.clearLayers()", "cleanup clusterGroupN3.clearLayers manquant"),
    ("_pieveActivePolygonRef", "reset _pieveActivePolygonRef manquant"),
    ("classList.remove('active-niveau-3')", "cleanup classe active-niveau-3 manquant"),
    ("classList.remove('selected')", "cleanup classe 'selected' pieve shapes manquant"),
    ("Brief Nav N3->N2 cross-doyenne", "commentaire reference brief manquant"),
]
failures = []
for snippet, msg in assertions:
    if snippet in fn_body:
        print(f"  [OK] {msg.replace(' manquant', '')}")
    else:
        failures.append(msg)
        print(f"  [FAIL] {msg}")

# Verifier qu'on n'a PAS modifie exitNiveau3View, enterNiveau3View
# (cleanup symetrique, mais pas de modif des autres fonctions)
exit_n3 = content[content.find("function exitNiveau3View"):content.find("function exitNiveau3View")+2000]
# Doit toujours contenir les cleanups originaux
for must in ("clusterGroupN3 && map.hasLayer", "clusterGroupN3.clearLayers"):
    if must not in exit_n3:
        failures.append(f"exitNiveau3View modifie (manque '{must}')")
        print(f"  [FAIL] exitNiveau3View modifie : manque '{must}'")
    else:
        print(f"  [OK] exitNiveau3View intact : '{must}' present")

print()
if failures:
    print(f"=== {len(failures)} FAILURES ===")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("=== ALL ASSERTIONS PASSED ===")
