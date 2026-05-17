"""
Retag des 17 sites orphelins (doyenne_contemporain_slug = null) selon
geo reelle, doctrine BP-FIX-RATTACHEMENT-COMPLET-001 (pieve + doyenne
ensemble). Soleil arbitrage 2026-05-17 : geo prime sur orthodoxie
historique.
"""
import json

SITES_PATH = "docs/data/sites_patrimoine.json"

# 17 retags (cap_corse_extreme_nord reste orphan transcommunal Cap)
RETAGS = {
    "san_cipriano_sagone_basse":              ("pieve_vico",       "doyenne_piana_vico_sari"),
    "san_giovanni_serrabone":                 ("pieve_orezza",     "doyenne_du_golo"),
    "san_giovanni_vizzavona_bas":             ("pieve_talcini",    "doyenne_cortenais"),
    "san_giovanni_vizzavona_village":         ("pieve_talcini",    "doyenne_cortenais"),
    "san_giovanni_zeloso":                    ("pieve_alesani",    "doyenne_plaine_orientale"),
    "san_giuliano_cuttoli_haute":             ("pieve_cinarca",    "doyenne_piana_vico_sari"),
    "san_petru_vallerustie_village":          ("pieve_rostino",    "doyenne_cortenais"),
    "san_pietro_lozari":                      ("pieve_balagne",    "doyenne_balagne"),
    "san_quilicu_castagniccia_opino":         ("pieve_orezza",     "doyenne_du_golo"),
    "san_quilicu_prunete_village":            ("pieve_rogna",      "doyenne_plaine_orientale"),
    "sant_appiano_fils_vico_golfe":           ("pieve_vico",       "doyenne_piana_vico_sari"),
    "santa_maria_di_e_grazie_sagone_littoral":("pieve_vico",       "doyenne_piana_vico_sari"),
    "santa_maria_favone":                     ("pieve_fiumorbo",   "doyenne_plaine_orientale"),
    "santa_maria_folelli":                    ("pieve_casinca",    "doyenne_du_golo"),
    "santa_maria_moriani_plage_haute":        ("pieve_moriani",    "doyenne_plaine_orientale"),
    "santa_maria_pietrapola":                 ("pieve_fiumorbo",   "doyenne_plaine_orientale"),
    "santa_maria_vizzavona":                  ("pieve_talcini",    "doyenne_cortenais"),
}

with open(SITES_PATH, encoding="utf-8") as f:
    data = json.load(f)

count = 0
not_found = []
for s in data["sites"]:
    if s["slug"] in RETAGS:
        pv, doy = RETAGS[s["slug"]]
        assert not s.get("pieve_slug"), f"{s['slug']} a deja un pieve_slug"
        assert not s.get("doyenne_contemporain_slug"), f"{s['slug']} a deja un doyenne_slug"
        s["pieve_slug"] = pv
        s["doyenne_contemporain_slug"] = doy
        print(f"  {s['slug']:48s} -> {pv} / {doy}")
        count += 1

for slug in RETAGS:
    if not any(s["slug"] == slug for s in data["sites"]):
        not_found.append(slug)

print(f"\nRetag: {count}/{len(RETAGS)}")
if not_found:
    print(f"NON TROUVES: {not_found}")

# Reecrit minifie (contrainte Cloudflare Workers Assets 512 KB)
with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

import os
print(f"{SITES_PATH}: {os.path.getsize(SITES_PATH)} B")
