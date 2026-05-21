# ============================================================================
# ARCHIVE 2026-05-18 (Etape 5 PR B / D2) — script one-shot historique.
# NE PLUS EXECUTER EN PRODUCTION. Conserve pour tracabilite uniquement.
# Voir scripts/archive/phase_oneshots/README.md
# ============================================================================
"""
Phase Strategie D Phase 2 (2026-05-18) — splits pieve_vico (×3) + pieve_balagne (×3).

Voie-b patch direct du derive (Phase 1 eprouvee). Cree 4 nouvelles pieves +
rename pieve_balagne -> pieve_aregno + ajuste pieves modifiees
(pieve_vico réduite, pieve_sorroinsu retire 3 communes, pieve_cinarca retire 1).

Arbitrages Soleil 2026-05-18 :
- 47 -> 51 pieves (+4 nouvelles : piana, sagone, ostriconi, calenzana)
- aregno = rename pieve_balagne (pas creation nette)
- Q-2 : san_pietro_letia retag commune INSEE (Phase B retag sites)
- Q-3 : tour_d_isolella_sette_navi conserve pieve_ornano + dette
- Vezzani 2B347 NON inclus (Phase 1)
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

# === Load communes ===
print("[strat-d-p2] loading communes GeoJSON...")
communes_index = {}
for path in [GEO_2A, GEO_2B]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    for feat in data["features"]:
        insee = feat["properties"]["code"]
        communes_index[insee] = shape(feat["geometry"])
print(f"[strat-d-p2] {len(communes_index)} communes indexees")

# === Definitions des splits ===
PIEVES_DEF = {
    # === Vico splits ===
    "pieve_piana": {
        "name": "Piana",
        "diocese_medieval": "Sagone",
        "doyenne_majoritaire": "doyenne_piana_vico_sari",
        "communes": ["2A197", "2A203", "2A279", "2A198", "2A212", "2A108", "2A100"],
        "note_rattachement": "Pieve couvrant le golfe de Porto et les calanques de Piana — patrimoine UNESCO Scandola/Piana inclus.",
        "preserve_multipolygon": True,
    },
    "pieve_sagone": {
        "name": "Sagone",
        "diocese_medieval": "Sagone",
        "doyenne_majoritaire": "doyenne_piana_vico_sari",
        "communes": ["2A065", "2A090"],  # Cargese + Coggia (migre cinarca)
        "note_rattachement": "Pieve heritiere du diocese medieval de Sagone, centree sur le golfe de Sagone (Cargese paese grec, vestiges cathedrale Sant'Appianu).",
    },
    "pieve_vico_reduite": {  # MODIF (slug conserve pieve_vico)
        "name": "Vico",
        "diocese_medieval": "Sagone",
        "doyenne_majoritaire": "doyenne_piana_vico_sari",
        "communes": ["2A154", "2A028", "2A348", "2A019", "2A258", "2A141", "2A174"],  # Marignana+Balogna+Vico+Arbori+Renno+Letia+Murzo
        "note_rattachement": "Pieve recentree sur le bassin du Liamone et l'arriere-pays de Vico (Phase 2 Strategie D 2026-05-18).",
        "target_slug": "pieve_vico",
    },
    # === Balagne splits ===
    "pieve_ostriconi": {
        "name": "Ostriconi",
        "diocese_medieval": "Nebbiu",
        "doyenne_majoritaire": "doyenne_balagne",
        "communes": ["2B199", "2B034", "2B332", "2B180", "2B223", "2B136", "2B182", "2B097",
                     "2B352", "2B290", "2B190", "2B339", "2B235", "2B156"],  # Palasca, Belgodere, Urtaca, Novella, Pietralba, Lama, Occhiatana, Costa, Ville-di-Paraso, Speloncato, Olmi-Cappella, Vallica, Pioggiola, Mausoleo
        "note_rattachement": "Pieve couvrant le bassin versant Ostriconi (NE Balagne, vallee Lama-Belgodere-Speloncato).",
    },
    "pieve_aregno": {  # RENAME de pieve_balagne
        "name": "Aregno",
        "diocese_medieval": "Sagone",  # heritage balagne
        "doyenne_majoritaire": "doyenne_balagne",
        "communes": ["2B134", "2B168", "2B093", "2B010", "2B316", "2B231", "2B020", "2B296",
                     "2B138", "2B084", "2B025", "2B175", "2B112", "2B173"],  # Ile-Rousse, Monticello, Corbara, Algajola, Santa-Reparata-di-Balagna, Pigna, Aregno, Sant'Antonino, Lavatoggio, Cateri, Avapessa, Nessa, Feliceto, Muro
        "note_rattachement": "Pieve centre-Balagne (Aregno, Pigna, Sant'Antonino, Lavatoggio, Ile-Rousse). Rename de l'ancienne pieve_balagne (Phase 2 Strategie D 2026-05-18, split en 3 : ostriconi/aregno/calenzana).",
        "rename_from": "pieve_balagne",
    },
    "pieve_calenzana": {
        "name": "Calenzana",
        "diocese_medieval": "Sagone",
        "doyenne_majoritaire": "doyenne_balagne",
        "communes": ["2B050", "2B150", "2B165", "2B361", "2B167", "2B049"],  # Calvi, Lumio, Moncale, Zilia, Montegrosso, Calenzana
        "note_rattachement": "Pieve couvrant Calvi et son arriere-pays (Calenzana paese, golfe de Calvi, Tartagine basse).",
    },
}

# Pieves modifiees (rétrécies post-migration cross)
PIEVES_RETRECIES = {
    "pieve_sorroinsu": {
        "communes_retirees": ["2A258", "2A141", "2A174"],  # Renno, Letia, Murzo
    },
    "pieve_cinarca": {
        "communes_retirees": ["2A090"],  # Coggia
    },
}

# === Build polygon helper ===
def build_polygon(communes_insee, preserve_multipolygon=False):
    polys = []
    missing = []
    for insee in communes_insee:
        g = communes_index.get(insee)
        if g is None:
            missing.append(insee)
        else:
            polys.append(g)
    if missing:
        print(f"[strat-d-p2] WARN communes manquantes: {missing}")
    if not polys:
        raise SystemExit("[strat-d-p2] FAIL 0 commune")
    union = unary_union(polys)
    simplified = union.simplify(TOLERANCE, preserve_topology=True)
    if isinstance(simplified, MultiPolygon):
        if preserve_multipolygon:
            # Conserver tous les morceaux : prendre le main + concat des secondaires
            main = max(simplified.geoms, key=lambda g: g.area)
            coords = [[round(y, 5), round(x, 5)] for x, y in main.exterior.coords]
            print(f"[strat-d-p2]   multipolygon preserve ({len(list(simplified.geoms))} pieces, main only used pour polygon)")
        else:
            main = max(simplified.geoms, key=lambda g: g.area)
            coords = [[round(y, 5), round(x, 5)] for x, y in main.exterior.coords]
    else:
        coords = [[round(y, 5), round(x, 5)] for x, y in simplified.exterior.coords]
    return coords, len(polys)

def make_entry(slug, defn):
    coords, n = build_polygon(defn["communes"], defn.get("preserve_multipolygon", False))
    entry = {
        "slug": slug,
        "name": defn["name"],
        "diocese_medieval": defn["diocese_medieval"],
        "doyenne_contemporain_majoritaire": defn["doyenne_majoritaire"],
        "doyennes_visibles": [defn["doyenne_majoritaire"]],
        "doyennes_appartenance": [{"slug": defn["doyenne_majoritaire"], "ratio": 1.0}],
        "communes_count": n,
        "polygon": coords,
    }
    if defn.get("note_rattachement"):
        entry["note_rattachement"] = defn["note_rattachement"]
    return entry

# === Charger derive original ===
with DERIVE_PATH.open(encoding="utf-8") as f:
    derive = json.load(f)
pieves_by_slug = {p["slug"]: p for p in derive["pieves"]}
print(f"[strat-d-p2] derive original: {len(pieves_by_slug)} pieves")

# === Construire les nouvelles + modifiees ===
# 1. Construire les 4 nouvelles + 2 modifiees (vico reduite, aregno)
built_entries = {}
for key, defn in PIEVES_DEF.items():
    target_slug = defn.get("target_slug", defn.get("rename_from") and "pieve_aregno" or key)
    if "rename_from" in defn:
        target_slug = key  # pieve_aregno
    elif "target_slug" in defn:
        target_slug = defn["target_slug"]
    else:
        target_slug = key
    entry = make_entry(target_slug, defn)
    built_entries[target_slug] = entry
    print(f"[strat-d-p2] built {target_slug}: {entry['communes_count']} communes")

# 2. Reconstruire pieve_sorroinsu et pieve_cinarca (retraits)
# Pour ces 2, on doit connaitre la liste actuelle de communes.
# On reconstitue depuis le mapping v1 + transferts v2 + retraits Phase 2.
v1 = json.load(open(ROOT / "_drafts" / "pieves_communes_mapping.json", encoding="utf-8"))
v1_by_slug = {p["slug"]: p for p in v1["pieves"]}

for sl, info in PIEVES_RETRECIES.items():
    base = v1_by_slug.get(sl, {})
    current_insee = list(base.get("communes_insee", []))
    for ret in info["communes_retirees"]:
        if ret in current_insee:
            current_insee.remove(ret)
    if not current_insee:
        print(f"[strat-d-p2] WARN {sl}: 0 commune apres retrait")
        continue
    coords, n = build_polygon(current_insee)
    # Preserver les meta du derive original
    orig = pieves_by_slug.get(sl, {})
    entry = {
        "slug": sl,
        "name": orig.get("name", base.get("name", sl)),
        "diocese_medieval": orig.get("diocese_medieval", base.get("diocese_medieval", "?")),
        "doyenne_contemporain_majoritaire": orig.get("doyenne_contemporain_majoritaire"),
        "doyennes_visibles": orig.get("doyennes_visibles", []),
        "doyennes_appartenance": orig.get("doyennes_appartenance", []),
        "communes_count": n,
        "polygon": coords,
    }
    if orig.get("note_rattachement"):
        entry["note_rattachement"] = orig["note_rattachement"]
    built_entries[sl] = entry
    print(f"[strat-d-p2] retreci {sl}: {n} communes (etait {orig.get('communes_count','?')})")

# === Reconstruire derive final ===
# Retirer du derive : pieve_vico (sera replace par vico reduite), pieve_balagne (rename -> aregno),
# pieve_sorroinsu (retreci), pieve_cinarca (retreci)
TO_REMOVE = {"pieve_vico", "pieve_balagne", "pieve_sorroinsu", "pieve_cinarca"}
final_pieves = []
for p in derive["pieves"]:
    if p["slug"] in TO_REMOVE:
        continue
    final_pieves.append(p)
# Ajouter les 4 nouvelles + vico reduite + aregno + 2 retrécies
for slug in ["pieve_piana", "pieve_sagone", "pieve_vico", "pieve_ostriconi", "pieve_aregno",
             "pieve_calenzana", "pieve_sorroinsu", "pieve_cinarca"]:
    if slug in built_entries:
        final_pieves.append(built_entries[slug])

# Tri par slug pour diff stable
final_pieves.sort(key=lambda p: p["slug"])
derive["pieves"] = final_pieves
derive["version"] = "v6-stratD-phase2-splits-2026-05-18"
derive["source_mapping"] = derive.get("source_mapping", "") + " + Strategie D Phase 2 (split vico×3 + balagne×3, voie-b patch direct)"
derive["stats"]["pieves_count"] = len(final_pieves)
derive["stats"]["total_communes"] = sum(p.get("communes_count", 0) for p in final_pieves)

with DERIVE_PATH.open("w", encoding="utf-8") as f:
    json.dump(derive, f, ensure_ascii=False, separators=(",", ":"))

import os
print(f"\n[strat-d-p2] {DERIVE_PATH}: {os.path.getsize(DERIVE_PATH)} B")

# Validation
slugs_final = sorted({p["slug"] for p in final_pieves})
print(f"[strat-d-p2] {len(slugs_final)} slugs uniques (attendu 51)")
assert len(slugs_final) == 51, f"Expected 51, got {len(slugs_final)}"
for new in ["pieve_piana", "pieve_sagone", "pieve_ostriconi", "pieve_aregno", "pieve_calenzana"]:
    assert new in slugs_final, f"{new} absent"
assert "pieve_balagne" not in slugs_final, "pieve_balagne devrait etre supprime (rename)"
assert "pieve_vico" in slugs_final, "pieve_vico (reduite) devrait etre present"
print("[strat-d-p2] OK 51 pieves : 4 nouvelles + pieve_aregno (rename) + pieve_vico/sorroinsu/cinarca redimensionnes")
