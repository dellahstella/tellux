#!/usr/bin/env python3
"""
Build simplified GeoJSON layers for open forest ("foret ouverte") and
heathland/scrubland ("lande/maquis") over Corsica, from BD Foret V2 (IGN) —
contextual layers only, NOT consumed by any calculation (cf. app.html
calcVegetationAttenuation(), which reads only foret_dense_corse.geojson via
FORET_DENSE_PARTS).

Brief F "couches contextuelles foret ouverte et lande/maquis, hors calcul"
(2026-09-02). Sibling of scripts/build_foret_dense_corse_geojson.py — meme
source, meme chaine mapshaper et memes parametres, filtre CODE_TFV different.
Ne remplace ni ne regenere foret_dense_corse.geojson (regle non negociable
du brief F) ; les trois couches coexistent.

Requires (identique a build_foret_dense_corse_geojson.py):
    pip install py7zr shapely requests
    Node.js + npx (mapshaper est invoque en sous-processus)

Output:
    public/data/foret_ouverte_corse.geojson
    public/data/lande_maquis_corse.geojson

--- Source --------------------------------------------------------------
Identique a build_foret_dense_corse_geojson.py : BD Foret V2 (IGN),
departements 2A (Corse-du-Sud) et 2B (Haute-Corse), memes archives,
memes millesimes (D02A 2017-05-10, D02B 2016-02-16), licence Etalab
Open License 2.0. Verifie accessible (HTTP 200, tailles coherentes) le
2026-09-02.

--- Nomenclature CODE_TFV — source citee, pas deduite par analogie ------
IGN, "BD Foret(R) Version 2 -- Descriptif de contenu", Septembre 2014,
https://inventaire-forestier.ign.fr/IMG/pdf/DC_BDFORET_v2.pdf (verifie
accessible et lisible le 2026-09-02), section 4.1.2 "Description des
attributs" (tableau des 32 valeurs de CODE_TFV) + section 4.1.3
"Correspondance entre les attributs" (p.16-17). Nomenclature nationale
= 32 postes fixes, identiques quel que soit le departement.

Postes retenus pour "foret ouverte" (TFV_G11 "Foret ouverte feuillus" /
"Foret ouverte coniferes" / "Foret ouverte mixte") :
    FO1  Foret ouverte de feuillus purs             (couvert feuillus >=75%)
    FO2  Foret ouverte de coniferes purs            (couvert coniferes >=75%)
    FO3  Foret ouverte a melange feuillus/coniferes (feuillus>=25% ET coniferes>=25%)
Exclu : FO0 "Foret ouverte SANS couvert arbore" -- definition IGN :
"changement brutal de couverture du sol suite a une perturbation
anthropique (coupe rase) ou un incident (tempete, incendie...)". Texte
structurellement identique a celui de FF0 (deja exclu de la foret dense,
cf. build_foret_dense_corse_geojson.py) : artefact transitoire, pas une
vegetation de foret ouverte actuellement presente. Meme rationale
d'exclusion, appliquee au meme type de poste "X0" dans la branche
"ouverte" de la nomenclature.

Poste retenu pour "lande/maquis" :
    LA4  Lande -- definition IGN explicite : "vegetation spontanee qui
         comprend une proportion importante de plantes ligneuses
         (bruyeres, genets, ajoncs, epineux divers) et semi-ligneuses
         (fougeres, phragmites...) [...] Les landes, au sens usuel,
         regroupent notamment les landes alpines, les landes
         montagnardes, LES GARRIGUES OU MAQUIS NON BOISES, les terrains
         incultes ou en friches, les landes sur terrains sales, les
         landes a phragmite." -- correspond exactement au libelle du
         brief ("lande/maquis").

*** POINT A SIGNALER (etape 2 du brief, risque explicitement flagge) ***
LA6 "Formation herbacee" est un poste DISTINCT de LA4 dans la
nomenclature (TFV_G11 les separe explicitement : "Lande" vs "Formation
herbacee"), bien que les deux partagent le prefixe cartographique "LA".
Definition LA6 : "vegetation naturelle qui comprend une proportion
d'herbacee superieure ou egale a 75%, la vegetation ligneuse ne
presentant alors qu'un couvert vegetal inferieur a 25%. [...] pelouses
alpines, les pelouses montagnardes pastorales, les pelouses pastorales
des garrigues et maquis." -- ce sont des pelouses/paturages a dominante
herbacee, pas du maquis (vegetation a dominante ligneuse). LA6 n'est
PAS inclus ici : les inclure sous l'etiquette "lande/maquis" du brief
serait trompeur (deux formations vegetales ecologiquement distinctes
sous un seul nom). Le diagnostic prive du 30/08/2026
(_drafts/DIAGNOSTIC_FORET_DENSE_2026-08-30.md) avait mesure un total
agrege "LA*" (LA4+LA6, ~159 163 ha / ~18% de la Corse) sans operer
cette distinction -- ce script s'en ecarte deliberement, sur la base de
la nomenclature officielle plutot que de la mesure agregee. Si Soleil
souhaite LA6 en plus (couche "formations herbacees/pelouses" distincte,
ou fusionnee sous "lande/maquis"), c'est un ajustement d'une ligne
(LANDE_CODES ci-dessous) a rejouer -- pas une nouvelle extraction.

--- Traitement geometrique ------------------------------------------------
Identique a build_foret_dense_corse_geojson.py, aux memes parametres
(brief F, etape 3 : "coherence entre les trois couches compte plus que
l'optimisation de chacune") : mapshaper (fusion 2A+2B, filtre CODE_TFV,
reprojection Lambert-93->WGS84, dissolution, simplification Visvalingam
0.6% keep-shapes, filtre ilots <5ha, -clean) + Shapely buffer(0) sur les
auto-intersections residuelles.

Usage:
    python3 scripts/build_foret_ouverte_lande_corse_geojson.py
"""

import json
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

import requests

try:
    import py7zr
except ImportError:
    print("ERROR: pip install py7zr shapely requests", flush=True)
    raise SystemExit(1)

from shapely.geometry import shape, mapping

ARCHIVES = {
    "D02A": "https://data.geopf.fr/telechargement/download/BDFORET/BDFORET_2-0__SHP_LAMB93_D02A_2017-05-10/BDFORET_2-0__SHP_LAMB93_D02A_2017-05-10.7z",
    "D02B": "https://data.geopf.fr/telechargement/download/BDFORET/BDFORET_2-0__SHP_LAMB93_D02B_2016-02-16/BDFORET_2-0__SHP_LAMB93_D02B_2016-02-16.7z",
}

# Nomenclature nationale BD Foret V2 (IGN, DC_BDFORET_v2.pdf, section 4.1.2/4.1.3) --
# codes cites depuis la source officielle, cf. docstring ci-dessus.
FORET_OUVERTE_CODES = ["FO1", "FO2", "FO3"]  # FO0 exclu (artefact, cf. docstring)
LANDE_CODES = ["LA4"]  # LA6 "Formation herbacee" volontairement exclu, cf. docstring

LAYERS = {
    "foret_ouverte": {
        "codes": FORET_OUVERTE_CODES,
        "out_path": Path("public/data/foret_ouverte_corse.geojson"),
        "classe": "foret_ouverte",
        "model": "BD Forêt V2 (IGN) — forêt ouverte (couvert arboré 10-40 %)",
        "classes_retenues": (
            "CODE_TFV FO1 (feuillus purs, couvert feuillus ≥75 %), FO2 (conifères purs, "
            "couvert conifères ≥75 %), FO3 (mélange feuillus/conifères, chacun ≥25 %). "
            "Exclu : FO0 « forêt ouverte sans couvert arboré » (artefact transitoire — "
            "coupe rase/incident, même rationale que l'exclusion FF0 de la forêt dense). "
            "Source nomenclature : IGN, BD Forêt V2, Descriptif de contenu, Sept. 2014, "
            "§4.1.2/4.1.3 (32 postes de la nomenclature nationale)."
        ),
    },
    "lande_maquis": {
        "codes": LANDE_CODES,
        "out_path": Path("public/data/lande_maquis_corse.geojson"),
        "classe": "lande_maquis",
        "model": "BD Forêt V2 (IGN) — lande (maquis/garrigue non boisés)",
        "classes_retenues": (
            "CODE_TFV LA4 « Lande » — définition IGN : végétation spontanée à dominante "
            "ligneuse/semi-ligneuse (bruyères, genêts, ajoncs, épineux divers…), "
            "regroupant notamment landes alpines, landes montagnardes, garrigues ou "
            "maquis non boisés, terrains incultes/en friches, landes sur terrains "
            "salés. Exclu délibérément : LA6 « Formation herbacée » (pelouses "
            "alpines/montagnardes/pastorales — poste distinct de la nomenclature, "
            "végétation herbacée ≥75 %, pas du maquis). "
            "Source nomenclature : IGN, BD Forêt V2, Descriptif de contenu, Sept. 2014, "
            "§4.1.2/4.1.3 (32 postes de la nomenclature nationale)."
        ),
    },
}


def download_and_extract(work_dir, code, url):
    archive_path = work_dir / f"{code}.7z"
    print(f"Telechargement {code}...", flush=True)
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    archive_path.write_bytes(r.content)
    print(f"  {len(r.content)/1024/1024:.1f} Mo", flush=True)

    extract_dir = work_dir / code
    with py7zr.SevenZipFile(archive_path, mode="r") as z:
        z.extractall(path=extract_dir)

    shp_files = list(extract_dir.rglob("FORMATION_VEGETALE.shp"))
    if not shp_files:
        raise RuntimeError(f"FORMATION_VEGETALE.shp introuvable dans l'archive {code}")
    return shp_files[0]


def run_mapshaper(shp_a, shp_b, codes, out_path):
    codes_js = repr(codes).replace("'", '"')
    tfv_filter = f'CODE_TFV && {codes_js}.indexOf(CODE_TFV) != -1'
    cmd = [
        "npx", "--yes", "mapshaper",
        "-i", str(shp_a), str(shp_b), "combine-files", "encoding=latin1", "name=veg",
        "-merge-layers",
        "-filter", tfv_filter,
        "-proj", "wgs84",
        "-dissolve",
        "-simplify", "0.6%", "keep-shapes",
        "-filter-islands", "min-area=50000sqm", "remove-empty",
        "-clean",
        "-o", "format=geojson", "precision=0.0001", str(out_path),
    ]
    print(f"Execution mapshaper (filtre CODE_TFV {codes})...", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform == "win32"))
    print(result.stdout, flush=True)
    if result.returncode != 0:
        print(result.stderr, flush=True)
        raise RuntimeError("mapshaper a echoue — cf. stderr ci-dessus")


def build_layer(shp_a, shp_b, work_dir, layer_key, layer_def):
    mapshaper_out = work_dir / f"{layer_key}_mapshaper_output.geojson"
    run_mapshaper(shp_a, shp_b, layer_def["codes"], mapshaper_out)

    raw = json.loads(mapshaper_out.read_text(encoding="utf-8"))
    # mapshaper produit un GeometryCollection (1 seule geometrie dissoute) --
    # converti en FeatureCollection standard avec metadonnees, meme format
    # que foret_dense_corse.geojson.
    geom_raw = raw["geometries"][0] if "geometries" in raw else raw["features"][0]["geometry"]
    geom = shape(geom_raw)
    if not geom.is_valid:
        geom = geom.buffer(0)
        print(f"  Geometrie corrigee (buffer(0)) — valide maintenant : {geom.is_valid}", flush=True)

    output = {
        "type": "FeatureCollection",
        "properties": {
            "model": layer_def["model"],
            "source": "IGN, BD Forêt V2, départements 2A + 2B",
            "millesime": "D02A: 2017-05-10, D02B: 2016-02-16",
            "licence": "Etalab Open License 2.0",
            "classes_retenues": layer_def["classes_retenues"],
            "date_pretraitement": date.today().isoformat(),
            "traitement": "mapshaper (fusion 2A+2B, filtre CODE_TFV, reprojection Lambert-93→WGS84, dissolution, simplification Visvalingam 0.6% + filtre îlots <5ha) + Shapely (buffer(0) validité).",
        },
        "features": [{
            "type": "Feature",
            "properties": {"classe": layer_def["classe"]},
            "geometry": mapping(geom),
        }],
    }

    out_path = layer_def["out_path"]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"Ecrit {out_path} ({size_mb:.1f} Mo bruts)", flush=True)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        shp_a = download_and_extract(work_dir, "D02A", ARCHIVES["D02A"])
        shp_b = download_and_extract(work_dir, "D02B", ARCHIVES["D02B"])

        for layer_key, layer_def in LAYERS.items():
            build_layer(shp_a, shp_b, work_dir, layer_key, layer_def)


if __name__ == "__main__":
    main()
