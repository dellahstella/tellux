"""
Retag des sites cross-doyennes (cat 2 audit Phase B 2026-05-17).
Doctrine Soleil : geo prime, BP-FIX-RATTACHEMENT-COMPLET-001
(pieve + doyenne ensemble cohereents).

Exception Mariana : pieve_mariana est un mega-pieve heritage des
fusions caccia->giovellina->mariana. Le refactor doctrinal Mariana
passe par Cowork (ADR dedie). Pour cette PR : seuls les sites
pieve_mariana geometriquement HORS du polygone pieve_mariana sont
retag (4 sites). Les 10 autres restent en pieve_mariana en attendant
le refactor.

Cas suspendus (option D arbitrage Soleil) :
- tour_de_farinole : coord verifiee correcte (42.7333/9.3333 ouest Cap),
  point a ~700m frontiere pieve (mer probable). Suspends. Dette
  FARINOLE-COORD-DOUTE-001.
- casteddu_bastelica : nom suggere commune Bastelica (sud Ajaccio,
  PTV) mais geo dans pieve_rogna/Cortenais. Doute homonymie/coord.
  Suspends. Dette CASTEDDU-BASTELICA-COORD-DOUTE-001.

Cas A (Soleil arbitrage) : 4 sites - geo prime malgre incoherence
pieve.majoritaire vs doyenne geo.
"""
import json

SITES_PATH = "docs/data/sites_patrimoine.json"

RETAGS = {
    # --- Cat 2 non-mariana coherent (10 sites) ---
    "san_giovanni_antisanti":                       ("pieve_rogna",     "doyenne_plaine_orientale"),
    "san_pietro_poggio_mezzana":                    ("pieve_rogna",     "doyenne_plaine_orientale"),
    "san_pietro_santo_pietro_di_tenda":             ("pieve_balagne",   "doyenne_balagne"),
    "sant_andrea_belvedere_campomoro_haute":        ("pieve_istria",    "doyenne_prunelli_taravo_valinco"),
    "santa_maria_calacuccia_village":               ("pieve_balagne",   "doyenne_balagne"),
    "santa_maria_carpineto":                        ("pieve_talcini",   "doyenne_cortenais"),
    "santa_maria_della_neve_grosseto_prugna_basse": ("pieve_ajaccio",   "doyenne_ajaccio"),
    "santa_maria_farinole":                         ("pieve_canari",    "doyenne_du_cap"),
    "santa_restituda_meria_vico_interieur":         ("pieve_sorroinsu", "doyenne_piana_vico_sari"),
    "pont_genois_de_santa_maria_poggio":            ("pieve_moriani",   "doyenne_plaine_orientale"),

    # --- Cat 2 mariana in_pv=False (4 sites) ---
    "san_martinu_borgo":              ("pieve_casinca",   "doyenne_du_golo"),
    "santa_maria_lucciana_interieur": ("pieve_casacconi", "doyenne_du_golo"),
    "santa_maria_nessa":              ("pieve_balagne",   "doyenne_balagne"),
    "santa_maria_novella_basse":      ("pieve_balagne",   "doyenne_balagne"),

    # --- Cat 2 cas A : Option A Soleil arbitrage (4 sites) ---
    "san_quilicu_lama":           ("pieve_nebbiu", "doyenne_du_golo"),
    "santa_maria_urtaca":         ("pieve_nebbiu", "doyenne_du_golo"),
    "san_cervone_valle_d_alesani":("pieve_rogna",  "doyenne_plaine_orientale"),
    "pont_genois_d_altiani":      ("pieve_rogna",  "doyenne_plaine_orientale"),
}

# Sites suspendus (no edit)
SUSPENDED = {"tour_de_farinole", "casteddu_bastelica"}

with open(SITES_PATH, encoding="utf-8") as f:
    data = json.load(f)

count = 0
for s in data["sites"]:
    if s["slug"] in RETAGS:
        pv, doy = RETAGS[s["slug"]]
        old_pv = s.get("pieve_slug")
        old_doy = s.get("doyenne_contemporain_slug")
        s["pieve_slug"] = pv
        s["doyenne_contemporain_slug"] = doy
        change = "no-op" if (old_pv == pv and old_doy == doy) else f"{old_pv}/{old_doy} -> {pv}/{doy}"
        print(f"  {s['slug']:48s} {change}")
        count += 1

for slug in SUSPENDED:
    s = next((x for x in data["sites"] if x["slug"] == slug), None)
    if s:
        print(f"  SUSPENDED {slug:38s} (tag inchange: {s.get('pieve_slug')}/{s.get('doyenne_contemporain_slug')})")

print(f"\nRetag: {count}/{len(RETAGS)}")
print(f"Suspended: {len(SUSPENDED)}")

with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

import os
print(f"{SITES_PATH}: {os.path.getsize(SITES_PATH)} B")
