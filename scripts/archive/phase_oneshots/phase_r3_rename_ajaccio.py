# ============================================================================
# ARCHIVE 2026-05-18 (Etape 5 PR B / D2) — script one-shot historique.
# NE PLUS EXECUTER EN PRODUCTION. Conserve pour tracabilite uniquement.
# Voir scripts/archive/phase_oneshots/README.md
# ============================================================================
"""
Phase R-3 : rename pieve_ajaccio -> pieve_gulfo_d_aiacciu.

Arbitrage Soleil 2026-05-17 (PIEVES_REFACTOR_PLAN_2026-05-17 §5 + §R-3).
Procedure generique R-X (PIEVES_REFACTOR_EXEC_CODE §3).

Slug : pieve_ajaccio -> pieve_gulfo_d_aiacciu
Name  : "Ajaccio" -> "Gulfo d'Aiacciu" (graphie corse coherente avec le slug)

Fichiers touches :
- _drafts/pieves_communes_mapping.json (mapping amont v1, slug)
- _drafts/pieves_communes_mapping_v2_canonicite_casta.json (transferts + stats)
- _drafts/PIEVE_DOYENNES_OVERRIDES.json (overrides)
- docs/data/pieves_polygons.json (derive, slug + name + transferts_v2_appliques)
- docs/data/sites_patrimoine.json (retag pieve_slug)
- docs/data/dioceses_polygons.json (dioceses[0].pieves[0])

SKIP :
- _drafts/PIEVE_OVERRIDES.json : pieve_ajaccio seulement dans usage_example
- docs/data/sites_corse.json : DEPRECATED
- _drafts/sites_patrimoine.backup_*.json : snapshots historiques (immuables)
- _drafts/brief_*.csv, audit_*.csv : logs historiques (immuables)
- docs/operations/PIEVES_*.md : docs originaux (acter R-3 ailleurs)
- DETTES_TECHNIQUES.md : references historiques
- scripts/retag_cross_doyennes.py : script archive
"""
import json
import os

OLD_SLUG = "pieve_ajaccio"
NEW_SLUG = "pieve_gulfo_d_aiacciu"
NEW_NAME = "Gulfo d'Aiacciu"

# === 1. Mapping amont v1 (formate, indent=2) ===
PATH_V1 = "_drafts/pieves_communes_mapping.json"
with open(PATH_V1, encoding="utf-8") as f:
    v1 = json.load(f)
renamed_v1 = 0
for p in v1["pieves"]:
    if p.get("slug") == OLD_SLUG:
        p["slug"] = NEW_SLUG
        renamed_v1 += 1
with open(PATH_V1, "w", encoding="utf-8") as f:
    json.dump(v1, f, ensure_ascii=False, indent=2)
print(f"v1 mapping: {renamed_v1} pieve(s) renamed in pieves[]")

# === 2. Mapping amont v2 (transferts + stats) ===
PATH_V2 = "_drafts/pieves_communes_mapping_v2_canonicite_casta.json"
with open(PATH_V2, encoding="utf-8") as f:
    raw = f.read()
old_count = raw.count(f'"{OLD_SLUG}"')
raw = raw.replace(f'"{OLD_SLUG}"', f'"{NEW_SLUG}"')
new_count = raw.count(f'"{NEW_SLUG}"')
# Verifier JSON valide
try:
    json.loads(raw)
except json.JSONDecodeError as e:
    print(f"ERROR JSON v2 invalide apres rename: {e}")
    raise
with open(PATH_V2, "w", encoding="utf-8") as f:
    f.write(raw)
print(f"v2 mapping: {old_count} occurrences {OLD_SLUG} -> {new_count} occurrences {NEW_SLUG}")

# === 3. PIEVE_DOYENNES_OVERRIDES.json ===
PATH_DOY_OV = "_drafts/PIEVE_DOYENNES_OVERRIDES.json"
with open(PATH_DOY_OV, encoding="utf-8") as f:
    od = json.load(f)
if OLD_SLUG in od.get("overrides", {}):
    od["overrides"][NEW_SLUG] = od["overrides"].pop(OLD_SLUG)
    print(f"PIEVE_DOYENNES_OVERRIDES: clef {OLD_SLUG} -> {NEW_SLUG}")
with open(PATH_DOY_OV, "w", encoding="utf-8") as f:
    json.dump(od, f, ensure_ascii=False, indent=2)

# === 4. JSON derive pieves_polygons.json (minifie) ===
PATH_DER = "docs/data/pieves_polygons.json"
with open(PATH_DER, encoding="utf-8") as f:
    pp = json.load(f)
renamed_der = 0
old_name = None
for p in pp["pieves"]:
    if p.get("slug") == OLD_SLUG:
        p["slug"] = NEW_SLUG
        old_name = p.get("name")
        p["name"] = NEW_NAME
        renamed_der += 1
print(f"derive: {renamed_der} pieve(s) renamed | name {old_name!r} -> {NEW_NAME!r}")
# Aussi dans transferts_v2_appliques
tv2 = pp.get("transferts_v2_appliques", [])
tv2_count = 0
for t in tv2:
    for k in ("from", "to"):
        if t.get(k) == OLD_SLUG:
            t[k] = NEW_SLUG
            tv2_count += 1
print(f"derive transferts_v2: {tv2_count} occurrences {OLD_SLUG} -> {NEW_SLUG}")
with open(PATH_DER, "w", encoding="utf-8") as f:
    json.dump(pp, f, ensure_ascii=False, separators=(",", ":"))
print(f"{PATH_DER}: {os.path.getsize(PATH_DER)} B")

# === 5. sites_patrimoine.json (retag) ===
PATH_SITES = "docs/data/sites_patrimoine.json"
with open(PATH_SITES, encoding="utf-8") as f:
    sd = json.load(f)
retag = 0
for s in sd["sites"]:
    if s.get("pieve_slug") == OLD_SLUG:
        s["pieve_slug"] = NEW_SLUG
        retag += 1
print(f"sites_patrimoine: {retag} sites retag pieve_slug {OLD_SLUG} -> {NEW_SLUG}")
with open(PATH_SITES, "w", encoding="utf-8") as f:
    json.dump(sd, f, ensure_ascii=False, separators=(",", ":"))
print(f"{PATH_SITES}: {os.path.getsize(PATH_SITES)} B")

# === 6. dioceses_polygons.json (reference simple) ===
PATH_DIO = "docs/data/dioceses_polygons.json"
with open(PATH_DIO, encoding="utf-8") as f:
    dp = json.load(f)
dio_count = 0
for d in dp.get("dioceses", []):
    if OLD_SLUG in d.get("pieves", []):
        idx = d["pieves"].index(OLD_SLUG)
        d["pieves"][idx] = NEW_SLUG
        dio_count += 1
print(f"dioceses_polygons: {dio_count} reference(s) renamed")
with open(PATH_DIO, "w", encoding="utf-8") as f:
    json.dump(dp, f, ensure_ascii=False, separators=(",", ":"))

# === Validation finale ===
print("\n=== Validation ===")
# JSON valide
for p in [PATH_V1, PATH_V2, PATH_DOY_OV, PATH_DER, PATH_SITES, PATH_DIO]:
    json.load(open(p, encoding="utf-8"))
print("Tous JSON valides")

# Verifier: aucun OLD_SLUG residuel dans les fichiers touches
for p in [PATH_V1, PATH_V2, PATH_DOY_OV, PATH_DER, PATH_SITES, PATH_DIO]:
    raw = open(p, encoding="utf-8").read()
    cnt = raw.count(OLD_SLUG)
    print(f"  {p}: {cnt} occurrences {OLD_SLUG} restantes")

# Pieves dans le derive
declared = {p["slug"] for p in pp["pieves"]}
assert NEW_SLUG in declared, f"{NEW_SLUG} pas dans declared"
assert OLD_SLUG not in declared, f"{OLD_SLUG} encore dans declared"
print(f"declared: {NEW_SLUG} present, {OLD_SLUG} absent")

# Ghost slug check
ghosts = [s["slug"] for s in sd["sites"] if s.get("pieve_slug") and s["pieve_slug"] not in declared]
assert not ghosts, ghosts
print(f"Ghosts: 0")
print(f"\nSites tagues {NEW_SLUG}: {sum(1 for s in sd['sites'] if s.get('pieve_slug') == NEW_SLUG)}")
