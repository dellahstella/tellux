"""
Phase Strategie D Phase 1 (2026-05-17) — patch direct du JSON derive.

Voie (b) du brief Cowork : patch direct du derive plutot que regeneration via
build_pieves_polygons.py (qui ferait reapparaitre 4 pieves zombies du mapping
v1 desynchronise — ampugnani, caccia, campoloro, giovellina).

Strategie :
1. Charger derive prod actuel (45 pieves)
2. Lancer build complet (49 pieves) pour obtenir les polygones recalcules
   correctement pour les 6 pieves modifiees + 2 nouvelles
3. Construire pieve_castagniccia manuellement (7 communes : Asco, Castifao,
   Castiglione, Moltifao, Piedigriggio, Popolasca, Prato-di-Giovellina) via
   unary_union shapely (le rename mariana via build est vide car v1 mariana
   n'avait pas ces 7 communes — elles etaient dans pieve_caccia + giovellina
   zombies, fusionnees dans mariana via scripts ad hoc historiques non
   synchronises avec le mapping amont)
4. Patcher derive : retirer ancien mariana, retirer 6 modifiees, ajouter
   versions build des 6 + 2 nouvelles + castagniccia construite manuellement
5. Conserver les 38 pieves stables intactes (y compris zicavo)
6. Preserver note_rattachement existantes (nebbiu, balagne, mariana→castagniccia)

Resultat attendu : 47 pieves (45 - 1 mariana + 2 nouvelles + 1 castagniccia + 0)
"""
import json
from pathlib import Path
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parent.parent
DERIVE_PATH = ROOT / "docs" / "data" / "pieves_polygons.json"
GEO_2A = ROOT / "scripts" / ".cache" / "communes-2A.geojson"
GEO_2B = ROOT / "scripts" / ".cache" / "communes-2B.geojson"
TOLERANCE = 0.0005

# === 1. Communes GeoJSON index ===
print("[strat-d] loading communes GeoJSON...")
communes_index = {}
for path in [GEO_2A, GEO_2B]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    for feat in data["features"]:
        insee = feat["properties"]["code"]
        communes_index[insee] = shape(feat["geometry"])
print(f"[strat-d] {len(communes_index)} communes indexees")

# === 2. Derive original ===
with DERIVE_PATH.open(encoding="utf-8") as f:
    derive = json.load(f)
pieves_orig = {p["slug"]: p for p in derive["pieves"]}
print(f"[strat-d] derive original: {len(pieves_orig)} pieves")

# === 3. Pieves modifiees (6) : reconstruire commune_list cible + polygone ===
# Pour chaque pieve modifiee, on a besoin de connaitre sa liste de communes
# DANS LE DERIVE PROD ACTUEL (incluant les fusions ad hoc historiques),
# puis appliquer les ajustements strat D.
#
# Comme le derive n'a pas la liste communes_insee, on doit la reconstituer
# en chargeant le mapping v1+v2+overrides + ajustements ad hoc.
#
# Approche pragmatique : on definit explicitement la liste communes_insee
# attendue pour chaque pieve modifiee post-strat-D (sourcee depuis le brief
# Cowork + audit prod).

# Listes attendues post-Strategie D (sourcees du brief §2 + cross-check)
PIEVES_TARGET_COMMUNES = {
    # === Nouvelles ===
    "pieve_biguglia": [
        "2B036", "2B037", "2B042", "2B055", "2B059", "2B120",
        "2B140", "2B148", "2B274", "2B350", "2B355"
    ],
    "pieve_altiani": [
        "2B012", "2B218", "2B226"
    ],
    # === Renommee (mariana -> castagniccia, 7 communes restantes) ===
    "pieve_castagniccia": [
        "2B023", "2B080", "2B081", "2B162", "2B220", "2B244", "2B248"
    ],
}

# === 4. Construire polygones ===
def build_pieve_entry(slug, communes_insee, meta):
    polys = []
    missing = []
    for insee in communes_insee:
        g = communes_index.get(insee)
        if g is None:
            missing.append(insee)
        else:
            polys.append(g)
    if missing:
        print(f"[strat-d] WARN {slug}: communes manquantes {missing}")
    if not polys:
        raise SystemExit(f"[strat-d] FAIL {slug}: 0 commune trouvee")
    union = unary_union(polys)
    simplified = union.simplify(TOLERANCE, preserve_topology=True)
    # Convert to [[lat,lng],...]
    if isinstance(simplified, MultiPolygon):
        main = max(simplified.geoms, key=lambda g: g.area)
    else:
        main = simplified
    coords = [[round(y, 5), round(x, 5)] for x, y in main.exterior.coords]
    entry = {
        "slug": slug,
        "name": meta["name"],
        "diocese_medieval": meta["diocese_medieval"],
        "doyenne_contemporain_majoritaire": meta["doyenne_majoritaire"],
        "doyennes_visibles": [meta["doyenne_majoritaire"]],
        "doyennes_appartenance": [{"slug": meta["doyenne_majoritaire"], "ratio": 1.0}],
        "communes_count": len(polys),
        "polygon": coords,
    }
    if meta.get("note_rattachement"):
        entry["note_rattachement"] = meta["note_rattachement"]
    return entry

META = {
    "pieve_biguglia": {
        "name": "Biguglia",
        "diocese_medieval": "Mariana",
        "doyenne_majoritaire": "doyenne_du_golo",
    },
    "pieve_altiani": {
        "name": "Altiani",
        "diocese_medieval": "Aleria",
        "doyenne_majoritaire": "doyenne_cortenais",
    },
    "pieve_castagniccia": {
        "name": "Castagniccia",
        "diocese_medieval": "Mariana",
        "doyenne_majoritaire": "doyenne_cortenais",
        "note_rattachement": "Sous-ensemble nord-ouest du doyenne Cortenais : haute vallee d'Asco, Caccia, ouvertures vers le Niolu via le col de San-Colombano. Issue du split de l'ancienne pieve_mariana (Strategie D Phase 1, 2026-05-17).",
    },
}

# === 5. Recomputer polygones des 6 pieves modifiees ===
# Pour ces 6, on doit connaitre leur commune_list dans prod actuelle.
# Pas de source directe : on prend la liste depuis le mapping v1+v2 + ajustements ad hoc.
# Hack pragmatique : on lance le build et on extrait juste les 6 polygones cibles
# (le build calcule les polygones corrects pour ces 6, en ignorant les zombies pour le reste).
import subprocess, sys
print("[strat-d] running build_pieves_polygons.py pour extraire polygones 6 pieves modifiees...")
res = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_pieves_polygons.py")],
                     capture_output=True, text=True, cwd=str(ROOT))
if res.returncode != 0:
    print(res.stderr)
    sys.exit(1)

# Re-lire le build (qui a ecrase DERIVE_PATH)
with DERIVE_PATH.open(encoding="utf-8") as f:
    build = json.load(f)
build_by_slug = {p["slug"]: p for p in build["pieves"]}

# 6 pieves modifiees a extraire du build (leurs polygones sont corrects)
MODIFIEES = ["pieve_alesani", "pieve_nebbiu", "pieve_rogna",
             "pieve_bozio", "pieve_balagne", "pieve_patrimonio"]

extracted_modifiees = {}
for slug in MODIFIEES:
    if slug not in build_by_slug:
        raise SystemExit(f"[strat-d] FAIL {slug} absent du build")
    extracted_modifiees[slug] = build_by_slug[slug]
    print(f"[strat-d] extrait du build : {slug} ({build_by_slug[slug]['communes_count']} communes)")

# === 6. Construire les 2 nouvelles + castagniccia ===
new_entries = {}
for slug in ["pieve_biguglia", "pieve_altiani", "pieve_castagniccia"]:
    new_entries[slug] = build_pieve_entry(
        slug,
        PIEVES_TARGET_COMMUNES[slug],
        META[slug],
    )
    print(f"[strat-d] construit : {slug} ({new_entries[slug]['communes_count']} communes)")

# === 7. Reconstruire derive final ===
# Pieves a retirer du derive original : 6 modifiees + 1 mariana renommee
TO_REMOVE = set(MODIFIEES) | {"pieve_mariana"}
final_pieves = []
for p in derive["pieves"]:
    if p["slug"] in TO_REMOVE:
        continue
    final_pieves.append(p)
# Ajouter les 6 modifiees (extraites build) + 2 nouvelles + castagniccia
for slug in MODIFIEES:
    final_pieves.append(extracted_modifiees[slug])
for slug in ["pieve_biguglia", "pieve_altiani", "pieve_castagniccia"]:
    final_pieves.append(new_entries[slug])

print(f"\n[strat-d] derive final: {len(final_pieves)} pieves (attendu 47)")

# Tri par slug pour stabilite diff
final_pieves.sort(key=lambda p: p["slug"])
derive["pieves"] = final_pieves
derive["version"] = "v5-stratD-containment-2026-05-17-patch-direct"
derive["source_mapping"] = (
    derive.get("source_mapping", "") +
    " + _drafts/pieves_communes_mapping_v3_stratD_2026-05-17.json (Strategie D Phase 1, voie b patch direct du derive)"
)
derive["stats"]["pieves_count"] = len(final_pieves)
derive["stats"]["total_communes"] = sum(p.get("communes_count", 0) for p in final_pieves)

# Ecrire (minifie pour Cloudflare Workers Assets <512 KB)
with DERIVE_PATH.open("w", encoding="utf-8") as f:
    json.dump(derive, f, ensure_ascii=False, separators=(",", ":"))

import os
print(f"[strat-d] {DERIVE_PATH}: {os.path.getsize(DERIVE_PATH)} B")

# Validation
slugs_final = sorted({p["slug"] for p in final_pieves})
print(f"\n[strat-d] {len(slugs_final)} slugs uniques")
assert len(slugs_final) == 47, f"Expected 47 pieves, got {len(slugs_final)}"
for cible in ["pieve_biguglia", "pieve_altiani", "pieve_castagniccia"]:
    assert cible in slugs_final, f"{cible} absent du final"
for absent in ["pieve_mariana", "pieve_giovellina", "pieve_caccia", "pieve_ampugnani", "pieve_campoloro"]:
    assert absent not in slugs_final, f"{absent} ne devrait pas etre present"
assert "pieve_zicavo" in slugs_final, "pieve_zicavo perdue !"
print("[strat-d] OK 47 pieves, biguglia+altiani+castagniccia presents, zombies absents, zicavo preservee")
