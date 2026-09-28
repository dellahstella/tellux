#!/usr/bin/env python3
"""
build_antennes_par_commune_corse.py
====================================
Agregat des antennes ANFR de Corse indexees par code INSEE commune,
lu depuis la colonne code_insee_commune de la table Supabase antennas_corse.

Pipeline simplifie (ticket SUPABASE-COMMUNE-FIELD-001, Option 2) :
  1. Telechargement des antennes depuis antennas_corse avec code_insee_commune
  2. Resolution commune_nom via geo.api.gouv.fr (cache local dans le fichier)
  3. Deduplication par (lat, lon, operateur) en agregeant les generations par support
  4. Ecriture de public/data/antennes_par_commune_corse.json

Changement majeur vs version precedente (avant resolution du ticket) :
  - SUPPRESSION : telechargement des 360 polygones de commune via geo.api.gouv.fr
  - SUPPRESSION : dependance a shapely pour le point-in-polygon
  - SUPPRESSION : logique de calcul geometrique cote client
  - AJOUT : lecture directe de code_insee_commune, source de verite en base

Structure de sortie (inchangee) :
    {
      "_meta": { source, date_extraction, version, counts },
      "communes": {
        "2A004": {
          "nom": "Ajaccio",
          "departement": "2A",
          "n_supports": 98,
          "n_antennes": 327,
          "operateurs": ["Bouygues", "Free", "Orange", "SFR"],
          "technologies": ["2G", "3G", "4G", "5G"],
          "supports": [
            { "lat": 41.92, "lon": 8.73, "operateur": "Orange", "generations": ["4G", "5G"], "n_antennes": 2 },
            ...
          ]
        },
        ...
      }
    }

Usage :
    pip install requests
    python scripts/build_antennes_par_commune_corse.py

Auteur  : Tellux (2026-04-24)
Sources : ANFR CartoRadio via table Supabase antennas_corse
          code_insee_commune peuple par scripts/fix_supabase_commune_insee.py
Licence : donnees ANFR sous Licence Ouverte 2.0 (Etalab)
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "public" / "data"
OUTPUT_FILE = OUTPUT_DIR / "antennes_par_commune_corse.json"

# Credentials Supabase lus depuis les variables d'environnement avec fallback
# sur les valeurs publiques hardcodees (cle anon = lecture seule soumise a RLS,
# exposable sans risque). La lecture d'env vars sert la CI GitHub Actions
# (workflow .github/workflows/refresh-antennes.yml) ou les secrets sont
# definis dans Settings > Secrets and variables > Actions du repo.
_SB_URL_DEFAULT = "https://knckulwghgfrxmbweada.supabase.co"
_SB_KEY_DEFAULT = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtu"
    "Y2t1bHdnaGdmcnhtYndlYWRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NTAxMzQsImV4cCI6"
    "MjA4OTIyNjEzNH0.Cu9dvxFyn-5pbOP65gowCEQvRti74CLnlNYf92jebis"
)
# Utilisation de `or` (et non `get(..., default)`) pour traiter les env vars
# vides ("") comme absentes et basculer sur le fallback. Cas utile en CI si
# un secret n'est pas defini.
SB_URL = os.environ.get("SUPABASE_URL") or _SB_URL_DEFAULT
# Accepte SUPABASE_ANON_KEY (nom canonique) ou SUPABASE_KEY (alias court
# utilise dans certains workflows CI).
SB_KEY = (
    os.environ.get("SUPABASE_ANON_KEY")
    or os.environ.get("SUPABASE_KEY")
    or _SB_KEY_DEFAULT
)

GEO_API = "https://geo.api.gouv.fr/communes"

# Generations ordonnees canoniquement
GEN_ORDER = ["2G", "3G", "4G", "5G"]


# ---------------------------------------------------------------------------
# FETCH
# ---------------------------------------------------------------------------

def fetch_antennas():
    """Telecharge les antennes depuis Supabase avec code_insee_commune."""
    print("Telechargement antennas_corse depuis Supabase...")
    rows = []
    page = 0
    while True:
        url = (
            f"{SB_URL}/rest/v1/antennas_corse"
            f"?select=id,lat,lon,generation,commune,operateur,code_insee_commune"
            f"&order=id.asc&offset={page * 1000}&limit=1000"
        )
        req = urllib.request.Request(
            url,
            headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            batch = json.loads(r.read())
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < 1000:
            break
        page += 1
    print(f"  {len(rows)} antennes telechargees")
    return rows


def fetch_commune_names(codes_insee):
    """Telecharge le nom officiel des communes INSEE via geo.api.gouv.fr.

    Appel groupe (un par departement), beaucoup plus leger qu'en Passe 1
    puisqu'on n'a plus besoin des contours.
    """
    print("Resolution noms des communes Corse (2A + 2B)...")
    mapping = {}
    for dep in ("2A", "2B"):
        url = f"{GEO_API}?codeDepartement={dep}&fields=nom,code&format=json"
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read())
        for c in data:
            mapping[c["code"]] = c["nom"]
    print(f"  {len(mapping)} communes resolues")
    return mapping


# ---------------------------------------------------------------------------
# AGGREGATION
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# COMPLEMENT (2026-09-28) : supports mobiles ANFR absents de antennas_corse
# ---------------------------------------------------------------------------
# antennas_corse ne couvre qu'environ la moitie de la Haute-Corse (dette privee
# ANFR-DECOMPTES-NON-RAPPROCHES-LEGENDE-METHODE-MODELE-001). La carte EM lit
# depuis le 2026-09-28 un fichier statique des 656 supports mobiles ANFR (export
# du 31/05/2026, public/data/supports_mobiles_anfr_corse_*.json). Ce complement
# ajoute a la page Mairies chaque position de support mobile ANFR qui n'a aucune
# entree antennas_corse a moins d'environ 60 m. Le jeu ANFR des secteurs ne porte
# pas l'operateur : ces entrees ont "operateur": null et le marqueur
# "operateur_non_renseigne": true. Les entrees existantes ne sont pas modifiees.
# n_antennes d'une entree ajoutee = nombre de generations presentes, meme grain
# qu'une ligne antennas_corse (position x operateur x generation), l'operateur
# etant inconnu.

import glob

SEUIL_LAT = 0.0006   # ~67 m
SEUIL_LON = 0.0008   # ~66 m a 42 N


def fichier_supports():
    fichiers = sorted(glob.glob(str(OUTPUT_DIR / "supports_mobiles_anfr_corse_*.json")))
    return Path(fichiers[-1]) if fichiers else None


def completer_depuis_supports(final, commune_names=None):
    """Ajoute a `final` (structure de finalize) les positions de supports
    mobiles ANFR sans entree antennas_corse proche. Rend un dict de meta."""
    chemin = fichier_supports()
    if chemin is None:
        print("  (complement) aucun fichier supports_mobiles_anfr_corse_*.json : rien ajoute")
        return None
    with open(chemin, encoding="utf-8") as f:
        data = json.load(f)
    supports = data.get("supports") or []
    existants = [(s["lat"], s["lon"]) for c in final.values() for s in c["supports"]]
    ajouts = {}
    n_supports = 0
    for sp in supports:
        lat, lon = sp.get("lat"), sp.get("lon")
        if lat is None or lon is None:
            continue
        if any(abs(a - lat) < SEUIL_LAT and abs(b - lon) < SEUIL_LON for a, b in existants):
            continue
        n_supports += 1
        code = sp.get("code_insee")
        cle = (code, round_coord(lat), round_coord(lon))
        e = ajouts.setdefault(cle, {
            "lat": round_coord(lat), "lon": round_coord(lon), "operateur": None,
            "operateur_non_renseigne": True, "generations": [], "n_antennes": 0,
            "source": "supports ANFR " + (data.get("_meta", {}).get("export_anfr_mise_a_disposition") or ""),
        })
        for g in (sp.get("secteurs") or {}):
            if g not in e["generations"]:
                e["generations"].append(g)
        e["nom_commune"] = (commune_names or {}).get(code) or sp.get("commune") or code
    for (code, _, _), e in ajouts.items():
        e["generations"] = sort_generations(e["generations"])
        e["n_antennes"] = len(e["generations"])
        nom = e.pop("nom_commune")
        c = final.setdefault(code, {"nom": nom, "departement": code[:2], "n_supports": 0, "n_antennes": 0,
                                    "operateurs": [], "technologies": [], "supports": []})
        c["supports"].append(e)
        c["n_supports"] = len(c["supports"])
        c["n_antennes"] = sum(s["n_antennes"] for s in c["supports"])
        c["technologies"] = sort_generations(g for s in c["supports"] for g in s["generations"])
        c["n_positions_operateur_non_renseigne"] = sum(1 for s in c["supports"] if s.get("operateur_non_renseigne"))
    print(f"  (complement) {len(ajouts)} positions ajoutees ({n_supports} supports ANFR sans entree antennas_corse a ~60 m)")
    return {
        "fichier": chemin.name,
        "export_anfr_mise_a_disposition": data.get("_meta", {}).get("export_anfr_mise_a_disposition"),
        "date_complement": "2026-09-28",
        "n_supports_ajoutes": n_supports,
        "n_positions_ajoutees": len(ajouts),
        "note": ("Positions de supports mobiles ANFR absentes de antennas_corse (a ~60 m pres). Operateur non "
                 "renseigne : le jeu ANFR des secteurs ne le porte pas. n_antennes = nombre de generations."),
    }


def round_coord(v, digits=5):
    return round(float(v), digits)


def sort_generations(gens):
    """Tri canonique 2G < 3G < 4G < 5G < autres."""
    def key(g):
        try:
            return GEN_ORDER.index(g)
        except ValueError:
            return 99
    return sorted(set(gens), key=key)


def aggregate(antennas, commune_names):
    """Regroupe par commune INSEE puis par support (lat, lon, operateur)."""
    by_commune = {}
    unassigned = 0

    for ant in antennas:
        code = ant.get("code_insee_commune")
        if code is None:
            unassigned += 1
            continue

        lat = ant.get("lat")
        lon = ant.get("lon")
        gen = ant.get("generation")
        op = ant.get("operateur")
        if lat is None or lon is None:
            unassigned += 1
            continue

        bucket = by_commune.setdefault(
            code,
            {
                "code_insee": code,
                "nom": commune_names.get(code, code),
                "departement": code[:2],
                "supports_map": {},
            },
        )

        sup_key = (round_coord(lat), round_coord(lon), op)
        sup = bucket["supports_map"].setdefault(
            sup_key,
            {
                "lat": round_coord(lat),
                "lon": round_coord(lon),
                "operateur": op,
                "generations": [],
                "n_antennes": 0,
            },
        )
        if gen and gen not in sup["generations"]:
            sup["generations"].append(gen)
        sup["n_antennes"] += 1

    return by_commune, unassigned


def finalize(by_commune):
    """Transforme la map interne en structure finale triee."""
    out = {}
    for code, bucket in by_commune.items():
        supports = list(bucket["supports_map"].values())
        for s in supports:
            s["generations"] = sort_generations(s["generations"])
        supports.sort(key=lambda s: (-s["n_antennes"], s["operateur"] or ""))
        all_ops = sorted({s["operateur"] for s in supports if s["operateur"]})
        all_techs = sort_generations(
            g for s in supports for g in s["generations"]
        )
        n_ant = sum(s["n_antennes"] for s in supports)
        out[code] = {
            "nom": bucket["nom"],
            "departement": bucket["departement"],
            "n_supports": len(supports),
            "n_antennes": n_ant,
            "operateurs": all_ops,
            "technologies": all_techs,
            "supports": supports,
        }
    return out


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    antennas = fetch_antennas()
    commune_names = fetch_commune_names(
        {a["code_insee_commune"] for a in antennas if a.get("code_insee_commune")}
    )

    print(f"Agregation de {len(antennas)} antennes...")
    by_commune, unassigned = aggregate(antennas, commune_names)
    final = finalize(by_commune)
    complement = completer_depuis_supports(final, commune_names)

    n_communes_with_antenna = len(final)
    n_supports_total = sum(c["n_supports"] for c in final.values())
    n_antennes_placed = sum(c["n_antennes"] for c in final.values())

    out = {
        "_meta": {
            "source": "ANFR CartoRadio via Supabase antennas_corse.code_insee_commune",
            "source_note": (
                "Colonne code_insee_commune peuplee par "
                "scripts/fix_supabase_commune_insee.py (ticket "
                "SUPABASE-COMMUNE-FIELD-001, Option 2) le 2026-04-24. Source "
                "de verite en base, lecture directe, plus de point-in-polygon "
                "cote client."
            ),
            "date_extraction": "2026-04-24",
            "version": "2.0",
            "pipeline": "scripts/build_antennes_par_commune_corse.py",
            "n_antennes_source": len(antennas),
            "n_antennes_placees": n_antennes_placed,
            "n_antennes_non_placees": unassigned,
            "n_supports_total": n_supports_total,
            "n_communes_avec_antenne": n_communes_with_antenna,
            "note": (
                "Antennes indexees par code INSEE via la colonne "
                "code_insee_commune de la table antennas_corse. Supports = "
                "groupes par (lat arrondi 5 decimales, lon arrondi, operateur). "
                "Le champ 'generations' liste les technologies 2G/3G/4G/5G "
                "presentes sur le support. Donnees ANFR sous Licence "
                "Ouverte 2.0."
            ),
        },
        "communes": final,
    }
    if complement:
        out["_meta"]["complement_supports_anfr"] = complement
        out["_meta"]["n_supports_total"] = sum(c["n_supports"] for c in final.values())
        out["_meta"]["n_communes_avec_antenne"] = len(final)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))

    size = OUTPUT_FILE.stat().st_size
    print()
    print(f"OK : {OUTPUT_FILE.relative_to(REPO_ROOT)}")
    print(f"  Taille : {size} bytes ({size/1024:.1f} KB)")
    print(f"  Communes avec au moins une antenne : {n_communes_with_antenna}")
    print(f"  Antennes placees : {n_antennes_placed}/{len(antennas)}")
    print(f"  Supports distincts : {n_supports_total}")
    if unassigned:
        print(f"  Non placees (code_insee_commune NULL) : {unassigned}")


def completer_fichier_existant():
    """Mode --completer-seulement : applique le complement au JSON deja
    produit (sans reseau). Equivalent a un run complet tant que antennas_corse
    n'a pas change (derniere extraction : 2026-04-24)."""
    with open(OUTPUT_FILE, encoding="utf-8") as f:
        out = json.load(f)
    final = out["communes"]
    for c in final.values():
        c["supports"] = [s for s in c["supports"] if not s.get("operateur_non_renseigne")]
        c["n_supports"] = len(c["supports"])
        c["n_antennes"] = sum(s["n_antennes"] for s in c["supports"])
        c["technologies"] = sort_generations(g for s in c["supports"] for g in s["generations"])
        c.pop("n_positions_operateur_non_renseigne", None)
    for code in [k for k, c in final.items() if not c["supports"]]:
        del final[code]
    complement = completer_depuis_supports(final, {k: c["nom"] for k, c in final.items()})
    if complement:
        out["_meta"]["complement_supports_anfr"] = complement
        out["_meta"]["n_supports_total"] = sum(c["n_supports"] for c in final.values())
        out["_meta"]["n_communes_avec_antenne"] = len(final)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK (complement seul) : {OUTPUT_FILE.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    if "--completer-seulement" in sys.argv:
        sys.exit(completer_fichier_existant() or 0)
    sys.exit(main() or 0)
