"""
Phase Strategie D Phase 1 (2026-05-17) — retag 28 sites + revert valle_d_alesani.

Arbitrage Soleil :
- 28 retags selon brief Strat D (20 modifs effectives + 8 no-op = 28)
- Q3 option B : san_cervone_valle_d_alesani revert pieve_bozio/cortenais (PR #633
  interim) -> pieve_alesani/PO (cohérent commune INSEE 2B334)

Doctrine BP-FIX-RATTACHEMENT-COMPLET-001 : pieve_slug + doyenne_contemporain_slug
retag en coherence.
"""
import json
from collections import Counter

PATH = "docs/data/sites_patrimoine.json"

# 28 sites Strat D (brief §2.8)
RETAGS = {
    # === pieve_alesani -> pieve_bozio (no-op : déjà bozio/cortenais) ===
    "san_martinu_alando":           ("pieve_bozio", "doyenne_cortenais"),
    "san_pietro_favalello":         ("pieve_bozio", "doyenne_cortenais"),
    "santa_lucia_mazzola":          ("pieve_bozio", "doyenne_cortenais"),

    # === pieve_mariana -> pieve_biguglia ===
    "san_martinu_borgo":            ("pieve_biguglia", "doyenne_du_golo"),
    "tour_de_punta_d_arcu_borgo":   ("pieve_biguglia", "doyenne_du_golo"),
    "san_petru_canavaggia":         ("pieve_biguglia", "doyenne_du_golo"),
    "la_canonica":                  ("pieve_biguglia", "doyenne_du_golo"),
    "san_parteo_lucciana_mariana":  ("pieve_biguglia", "doyenne_du_golo"),
    "santa_maria_lucciana_interieur":("pieve_biguglia", "doyenne_du_golo"),
    "mariana_antique":              ("pieve_biguglia", "doyenne_du_golo"),

    # === pieve_mariana -> pieve_balagne ===
    "san_giovanni_novella":         ("pieve_balagne", "doyenne_balagne"),
    "santa_maria_novella_basse":    ("pieve_balagne", "doyenne_balagne"),

    # === pieve_nebbiu -> pieve_patrimonio ===
    "santa_reparata_barbaggio":     ("pieve_patrimonio", "doyenne_du_cap"),
    "mine_de_magnetite_de_farinole":("pieve_patrimonio", "doyenne_du_cap"),
    "santa_maria_farinole":         ("pieve_patrimonio", "doyenne_du_cap"),
    "tour_de_farinole":             ("pieve_patrimonio", "doyenne_du_cap"),
    "san_gavino_oletta":            ("pieve_patrimonio", "doyenne_du_cap"),
    "san_martino_de_patrimonio":    ("pieve_patrimonio", "doyenne_du_cap"),
    "santa_maria_poggio_d_oletta":  ("pieve_patrimonio", "doyenne_du_cap"),
    "casa_di_u_banditu":            ("pieve_patrimonio", "doyenne_du_cap"),
    "cathedrale_du_nebbio":         ("pieve_patrimonio", "doyenne_du_cap"),
    "menhirs_agriate":              ("pieve_patrimonio", "doyenne_du_cap"),
    "tour_de_fornali_saint_florent":("pieve_patrimonio", "doyenne_du_cap"),

    # === pieve_nebbiu -> pieve_balagne ===
    "san_quilicu_lama":             ("pieve_balagne", "doyenne_balagne"),
    "santa_maria_urtaca":           ("pieve_balagne", "doyenne_balagne"),

    # === pieve_rogna -> pieve_altiani ===
    "pont_genois_d_altiani":        ("pieve_altiani", "doyenne_cortenais"),
    "san_cervone_stazzona":         ("pieve_altiani", "doyenne_cortenais"),
    "san_quilicu_piedicorte_di_gaggio":("pieve_altiani", "doyenne_cortenais"),
}

# Q3 option B : revert valle_d_alesani vers pieve_alesani/PO (commune 2B334 hors migration)
SPECIAL_REVERT = {
    "san_cervone_valle_d_alesani":  ("pieve_alesani", "doyenne_plaine_orientale"),
}

# Ghost rescue : 8 sites taggés pieve_mariana (rename castagniccia) en prod
# mais leur commune n'est pas dans les 11 biguglia/2 balagne/7 castagniccia.
# Cause : prod pieve_mariana = 24 communes (fusions ad hoc historiques caccia/
# giovellina), brief Strat D ne couvre que 20. Auto-retag selon PIP géographique
# (cf. doctrine geo prime, FB feedback_doctrine_geo_prime).
GHOST_RESCUE = {
    "monte_cinto":                       ("pieve_castagniccia", "doyenne_cortenais"),
    "san_giovanni_bastia_terra_vecchia": ("pieve_biguglia",     "doyenne_du_golo"),
    "san_martinu_casanova":              ("pieve_talcini",      "doyenne_cortenais"),
    "san_nicolao_castellare_di_mercurio":("pieve_talcini",      "doyenne_cortenais"),
    "san_petru_bisinchi":                ("pieve_biguglia",     "doyenne_du_golo"),
    "santa_maria_erbajolo":              ("pieve_venaco",       "doyenne_cortenais"),
    "tour_de_furiani":                   ("pieve_biguglia",     "doyenne_du_golo"),
    "pont_de_ponte_leccia_morosaglia":   ("pieve_balagne",      "doyenne_balagne"),
    # Asco/Popolasca/Castifao (communes castagniccia 2B023/2B244/2B080)
    "san_giovanni_castifao":             ("pieve_castagniccia", "doyenne_cortenais"),
    "san_giovanni_popolasca":            ("pieve_castagniccia", "doyenne_cortenais"),
    "san_pietro_asco":                   ("pieve_castagniccia", "doyenne_cortenais"),
    "massif_du_haut_asco":               ("pieve_castagniccia", "doyenne_cortenais"),
    "pont_genois_d_asco":                ("pieve_castagniccia", "doyenne_cortenais"),
}
RETAGS.update(GHOST_RESCUE)

with open(PATH, encoding="utf-8") as f:
    d = json.load(f)

c_before = Counter(s.get("pieve_slug") for s in d["sites"])

modifs = 0
nops = 0
for s in d["sites"]:
    target = None
    if s["slug"] in RETAGS:
        target = RETAGS[s["slug"]]
    elif s["slug"] in SPECIAL_REVERT:
        target = SPECIAL_REVERT[s["slug"]]
    if target:
        new_pv, new_doy = target
        old_pv = s.get("pieve_slug")
        old_doy = s.get("doyenne_contemporain_slug")
        if old_pv == new_pv and old_doy == new_doy:
            nops += 1
            print(f"  NO-OP {s['slug']:42s} (deja {new_pv}/{new_doy})")
        else:
            s["pieve_slug"] = new_pv
            s["doyenne_contemporain_slug"] = new_doy
            modifs += 1
            print(f"  RETAG {s['slug']:42s} {old_pv}/{old_doy} -> {new_pv}/{new_doy}")

print(f"\nTotal : {modifs} modifs + {nops} no-op = {modifs+nops}")
# RETAGS contient deja les ghost rescue (update au-dessus). +1 special revert.
assert modifs + nops == len(RETAGS) + len(SPECIAL_REVERT), f"compteur incoherent ({modifs+nops} vs {len(RETAGS)+len(SPECIAL_REVERT)})"

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, separators=(",", ":"))

import os
print(f"{PATH}: {os.path.getsize(PATH)} B")

# Validation ghost
pp = json.load(open("docs/data/pieves_polygons.json", encoding="utf-8"))
declared = {p["slug"] for p in pp["pieves"]}
ghosts = [s["slug"] for s in d["sites"] if s.get("pieve_slug") and s["pieve_slug"] not in declared]
assert not ghosts, f"GHOSTS: {ghosts}"
print(f"\nGhosts: 0")

c_after = Counter(s.get("pieve_slug") for s in d["sites"])
print("\nCompteurs sites par pieve (Δ vs avant) :")
for sl in sorted(set(list(c_before.keys()) + list(c_after.keys())), key=lambda x: str(x)):
    a = c_before.get(sl, 0); b = c_after.get(sl, 0); delta = b - a
    if delta != 0:
        print(f"  {str(sl):28s}: {a:>3} -> {b:>3} ({delta:+d})")
