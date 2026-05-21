# ============================================================================
# ARCHIVE 2026-05-18 (Etape 5 PR B / D2) — script one-shot historique.
# NE PLUS EXECUTER EN PRODUCTION. Conserve pour tracabilite uniquement.
# Voir scripts/archive/phase_oneshots/README.md
# ============================================================================
"""
Phase D-3 refactor pieves : aligner doyennes_majoritaire_declared sur actual.

Source : doyenne_majoritaire_reclassed du JSON derive donne les 3 divergences
en cours (identiques au doc PIEVES_REFACTOR_PLAN §3.D-3) :
  pieve_bastia   declared=doyenne_de_bastia            actual=doyenne_du_cap
  pieve_verde    declared=doyenne_prunelli_taravo_..   actual=doyenne_extreme_sud
  pieve_vivario  declared=doyenne_ajaccio              actual=doyenne_cortenais

Actions :
1. Patcher _drafts/pieves_communes_mapping.json (mapping amont v1) :
   aligner doyenne_contemporain_majoritaire des 3 pieves sur l'actual.
2. Vider doyenne_majoritaire_reclassed du JSON derive (puisque alignes).

doyenne_de_bastia n'existe pas comme doyenne contemporain (fusionne dans
doyenne_du_cap, Brief 32 2026-05-06). Son retrait du mapping amont est
coherent avec l'etat du repo.
"""
import json

MAPPING_PATH = "_drafts/pieves_communes_mapping.json"
PIEVES_PATH = "docs/data/pieves_polygons.json"

REALIGNS = {
    "pieve_bastia":  "doyenne_du_cap",
    "pieve_verde":   "doyenne_extreme_sud",
    "pieve_vivario": "doyenne_cortenais",
}

# === 1. Mapping amont ===
with open(MAPPING_PATH, encoding="utf-8") as f:
    m = json.load(f)

for p in m["pieves"]:
    if p.get("slug") in REALIGNS:
        old = p.get("doyenne_contemporain_majoritaire")
        p["doyenne_contemporain_majoritaire"] = REALIGNS[p["slug"]]
        print(f"mapping amont: {p['slug']} {old} -> {REALIGNS[p['slug']]}")

# Re-write avec indentation preservee (le mapping amont est formate, pas minifie)
with open(MAPPING_PATH, "w", encoding="utf-8") as f:
    json.dump(m, f, ensure_ascii=False, indent=2)
print(f"{MAPPING_PATH}: re-ecrit")

# === 2. JSON derive ===
with open(PIEVES_PATH, encoding="utf-8") as f:
    pp = json.load(f)

old_reclassed = pp.get("doyenne_majoritaire_reclassed", [])
print(f"\ndoyenne_majoritaire_reclassed AVANT: {len(old_reclassed)} entrees")
for e in old_reclassed:
    print(f"  {e}")

# Vider (puisque les 3 entrees correspondent EXACTEMENT aux pieves alignees)
# Verification : toutes les entries actuelles doivent etre dans REALIGNS
for e in old_reclassed:
    assert e["pieve"] in REALIGNS, f"reclassed entry not in realigns: {e}"
    assert e["actual"] == REALIGNS[e["pieve"]], f"actual mismatch: {e}"

pp["doyenne_majoritaire_reclassed"] = []
print("\ndoyenne_majoritaire_reclassed APRES: [] (vide, 3 entrees alignees)")

with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pp, f, ensure_ascii=False, separators=(",", ":"))

import os
print(f"{PIEVES_PATH}: {os.path.getsize(PIEVES_PATH)} B")
print("\nValidation : doyenne_de_bastia residuel dans mapping amont ?")
with open(MAPPING_PATH, encoding="utf-8") as f:
    raw = f.read()
hits = raw.count("doyenne_de_bastia")
print(f"  Occurrences 'doyenne_de_bastia' dans {MAPPING_PATH}: {hits}")
if hits > 0:
    # Find context
    for i, line in enumerate(raw.split("\n"), 1):
        if "doyenne_de_bastia" in line:
            print(f"  ligne {i}: {line.strip()[:150]}")
