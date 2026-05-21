# ============================================================================
# ARCHIVE 2026-05-18 (Etape 5 PR B / D2) — script one-shot historique.
# NE PLUS EXECUTER EN PRODUCTION. Conserve pour tracabilite uniquement.
# Voir scripts/archive/phase_oneshots/README.md
# ============================================================================
"""
Phase Strategie D Etape 3 (2026-05-18) — fusion pieve_bastia + pieve_brando
-> pieve_lota.

SCRIPT RECONSTITUE RETROACTIVEMENT le 2026-05-18 (Etape 5 PR B / D2).
La fusion reelle a ete executee par la PR #648 (refonte pieve_lota, Option A
audit Cowork, validee Soleil) directement sur le derive prod, sans script
trace. Ce fichier documente la logique a posteriori pour tracabilite.

Effet (deja applique en prod) :
- Suppression de pieve_bastia (1 commune) et pieve_brando (cote sud Cap, 6 des
  9 communes v1 ; les 3 autres — Cagnano, Luri, Meria — etaient deja parties
  vers d'autres pieves du Cap via les transferts v2/v3).
- Creation de pieve_lota : 7 communes cote est du Cap Corse sud
  (Bastia + Brando + Pietracorbara + Sisco + San-Martino-di-Lota +
  Santa-Maria-di-Lota + Ville-di-Pietrabugno), diocese Mariana, doyenne_du_cap.
- 2 anomalies sites double-retag (doctrine BP-FIX-RATTACHEMENT-COMPLET-001) :
  oratoire_santa_croce_bastia_haute_bastia_citadelle (ex pieve_nebbiu/doy_golo)
  et san_giovanni_bastia_terra_vecchia (ex pieve_biguglia/doy_golo)
  -> pieve_lota / doyenne_du_cap.

IDEMPOTENT : si pieve_lota existe deja dans le derive (etat prod normal), le
script est un no-op pour la partie pieve. Les retags sites ne s'appliquent que
si le site est encore mal tague. Peut etre lance a blanc sans risque.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DERIVE_PATH = ROOT / "docs" / "data" / "pieves_polygons.json"
SITES_PATH = ROOT / "docs" / "data" / "sites_patrimoine.json"
GEO_2A = ROOT / "scripts" / ".cache" / "communes-2A.geojson"
GEO_2B = ROOT / "scripts" / ".cache" / "communes-2B.geojson"
TOLERANCE = 0.0005

# Composition pieve_lota (cf. _drafts/pieves_communes_mapping_v4_cleanup_2026-05-18.json)
LOTA_COMMUNES = ["2B033", "2B043", "2B224", "2B281", "2B305", "2B309", "2B353"]
LOTA_META = {
    "slug": "pieve_lota",
    "name": "Lota",
    "diocese_medieval": "Mariana",
    "doyenne_contemporain_majoritaire": "doyenne_du_cap",
}
ZOMBIES_FUSIONNES = ["pieve_bastia", "pieve_brando"]

# Anomalies sites — double-retag pieve_slug + doyenne_contemporain_slug
SITE_RETAGS = {
    "oratoire_santa_croce_bastia_haute_bastia_citadelle": ("pieve_lota", "doyenne_du_cap"),
    "san_giovanni_bastia_terra_vecchia": ("pieve_lota", "doyenne_du_cap"),
}


def main():
    derive = json.loads(DERIVE_PATH.read_text(encoding="utf-8"))
    slugs = {p["slug"] for p in derive["pieves"]}

    if "pieve_lota" in slugs:
        print("[etape3-lota] pieve_lota deja present — fusion deja appliquee (no-op).")
    else:
        # Reconstruction (non executee en pratique : prod a deja lota).
        from shapely.geometry import shape, MultiPolygon
        from shapely.ops import unary_union
        communes_index = {}
        for path in (GEO_2A, GEO_2B):
            for feat in json.loads(path.read_text(encoding="utf-8"))["features"]:
                communes_index[feat["properties"]["code"]] = shape(feat["geometry"])
        polys = [communes_index[i] for i in LOTA_COMMUNES if i in communes_index]
        union = unary_union(polys).simplify(TOLERANCE, preserve_topology=True)
        main_geom = max(union.geoms, key=lambda g: g.area) if isinstance(union, MultiPolygon) else union
        coords = [[round(y, 5), round(x, 5)] for x, y in main_geom.exterior.coords]
        entry = dict(LOTA_META)
        entry.update({
            "doyennes_visibles": ["doyenne_du_cap"],
            "doyennes_appartenance": [{"slug": "doyenne_du_cap", "ratio": 1.0}],
            "communes_count": len(polys),
            "polygon": coords,
        })
        derive["pieves"] = [p for p in derive["pieves"] if p["slug"] not in ZOMBIES_FUSIONNES]
        derive["pieves"].append(entry)
        derive["pieves"].sort(key=lambda p: p["slug"])
        DERIVE_PATH.write_text(
            json.dumps(derive, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"[etape3-lota] pieve_lota cree ({len(polys)} communes), "
              f"{ZOMBIES_FUSIONNES} supprimes.")

    # Retags sites (idempotent : ne touche que si encore mal tague)
    sites = json.loads(SITES_PATH.read_text(encoding="utf-8"))
    changed = 0
    for s in sites["sites"]:
        tgt = SITE_RETAGS.get(s.get("slug"))
        if tgt and (s.get("pieve_slug"), s.get("doyenne_contemporain_slug")) != tgt:
            s["pieve_slug"], s["doyenne_contemporain_slug"] = tgt
            changed += 1
    if changed:
        SITES_PATH.write_text(
            json.dumps(sites, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"[etape3-lota] {changed} site(s) retague(s).")
    else:
        print("[etape3-lota] sites deja tagues correctement (no-op).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
