# ============================================================================
# ARCHIVE 2026-05-18 (Etape 5 PR B / D2) — script one-shot historique.
# NE PLUS EXECUTER EN PRODUCTION. Conserve pour tracabilite uniquement.
# Voir scripts/archive/phase_oneshots/README.md
# ============================================================================
"""
Phase QW refactor pieves (Soleil arbitrage 2026-05-17).
Patche directement les JSON dérivés (autorise par le doc QW).

QW-1 : stats.pieves_count + total_communes recalculés
QW-2 : SKIP (mojibake déjà résolu)
QW-3 : diocese_medieval ajouté pour mezzana(Ajaccio), patrimonio(Nebbiu),
       zicavo(Ajaccio), verde(Aleria)
QW-4 : ANNULE - pieve_verde conservée (option C). Retag 2 sites mistagged
       (capula_torre, pacciunituli) vers pieve_carbini. 2 sites cote est
       (pinarellu, fautea) gardes en pieve_verde (frontiere polygone),
       dette ouverte post-FEDER.
QW-5 : prefixe 'Pieve di/d'' retire des 7 names :
       celavo, tavagna, casacconi, filosorma, luri, talcini, aleria
"""
import json

PIEVES_PATH = "docs/data/pieves_polygons.json"
SITES_PATH = "docs/data/sites_patrimoine.json"

# QW-3 : diocese_medieval à ajouter
DIOCESES_TO_ADD = {
    "pieve_mezzana":    "Ajaccio",
    "pieve_patrimonio": "Nebbiu",
    "pieve_zicavo":     "Ajaccio",
    "pieve_verde":      "Aleria",
}

# QW-4 option C : retag mistagged in pieve_carbini
SITE_RETAGS = {
    "capula_torre":   ("pieve_carbini", "doyenne_extreme_sud"),
    "pacciunituli":   ("pieve_carbini", "doyenne_extreme_sud"),
}

# QW-5 : retirer prefixe "Pieve di" / "Pieve d'"
NAME_STRIPS = {
    "pieve_celavo":    "Celavo",
    "pieve_tavagna":   "Tavagna",
    "pieve_casacconi": "Casacconi",
    "pieve_filosorma": "Filosorma",
    "pieve_luri":      "Luri",
    "pieve_talcini":   "Talcini",
    "pieve_aleria":    "Aleria",
}

# === pieves_polygons.json ===
with open(PIEVES_PATH, encoding="utf-8") as f:
    pp = json.load(f)

# QW-1 stats
old_count = pp["stats"].get("pieves_count")
old_communes = pp["stats"].get("total_communes")
pp["stats"]["pieves_count"] = len(pp["pieves"])
pp["stats"]["total_communes"] = sum(p.get("communes_count", 0) for p in pp["pieves"])
print(f"QW-1 stats: pieves_count {old_count} -> {pp['stats']['pieves_count']}")
print(f"           total_communes {old_communes} -> {pp['stats']['total_communes']}")

# QW-3 dioceses + QW-5 names
for p in pp["pieves"]:
    if p["slug"] in DIOCESES_TO_ADD and not p.get("diocese_medieval"):
        p["diocese_medieval"] = DIOCESES_TO_ADD[p["slug"]]
        print(f"QW-3 diocese: {p['slug']} -> {p['diocese_medieval']}")
    if p["slug"] in NAME_STRIPS:
        old_name = p.get("name", "")
        p["name"] = NAME_STRIPS[p["slug"]]
        print(f"QW-5 name: {p['slug']} {old_name!r} -> {p['name']!r}")

# Verifier que toutes les pieves ont diocese_medieval
sans_doy = [p["slug"] for p in pp["pieves"] if not p.get("diocese_medieval")]
print(f"Pieves sans diocese_medieval restantes: {sans_doy}")

with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pp, f, ensure_ascii=False, separators=(",", ":"))
import os
print(f"{PIEVES_PATH}: {os.path.getsize(PIEVES_PATH)} B")

# === sites_patrimoine.json — QW-4 retags ===
with open(SITES_PATH, encoding="utf-8") as f:
    sd = json.load(f)
retag_count = 0
for s in sd["sites"]:
    if s["slug"] in SITE_RETAGS:
        new_pv, new_doy = SITE_RETAGS[s["slug"]]
        old_pv = s.get("pieve_slug")
        old_doy = s.get("doyenne_contemporain_slug")
        s["pieve_slug"] = new_pv
        s["doyenne_contemporain_slug"] = new_doy
        print(f"QW-4 retag: {s['slug']} {old_pv}/{old_doy} -> {new_pv}/{new_doy}")
        retag_count += 1
assert retag_count == len(SITE_RETAGS), f"missing retags: {retag_count}/{len(SITE_RETAGS)}"

with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(sd, f, ensure_ascii=False, separators=(",", ":"))
print(f"{SITES_PATH}: {os.path.getsize(SITES_PATH)} B")

# === Validation finale ===
declared = {p["slug"] for p in pp["pieves"]}
ghosts = [s["slug"] for s in sd["sites"] if s.get("pieve_slug") and s["pieve_slug"] not in declared]
print(f"Ghosts: {len(ghosts)}")
assert not ghosts, ghosts
print("OK no ghost pieve_slug")
