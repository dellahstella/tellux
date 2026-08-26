#!/usr/bin/env python3
"""
Build a simplified GeoJSON of dense forest cover (canopy closed, IGN
"foret fermee" classes) over Corsica, from BD Foret V2 (IGN), for offline
client-side path-intersection lookup by calcVegetationAttenuation() (ITU-R
P.833-6, app.html).

Brief "implementation 3 chantiers orphelins" (2026-08-26), chantier B.

Requires:
    pip install py7zr shapely requests
    Node.js + npx (mapshaper est invoque via npx, deja utilise ailleurs dans
    ce repo pour du traitement geospatial ad hoc — pas de nouvelle dependance
    d'environnement, juste un usage scripte plutot que manuel).

Output:
    public/data/foret_dense_corse.geojson

--- Source ------------------------------------------------------------------
BD Foret V2 (IGN), departements 2A (Corse-du-Sud) et 2B (Haute-Corse),
telecharges depuis data.geopf.fr (geoservices.ign.fr a ferme le 26/03/2026,
cartes.gouv.fr / data.geopf.fr sont la reference actuelle) :
    D02A : BDFORET_2-0__SHP_LAMB93_D02A_2017-05-10.7z (millesime 2017-05-10)
    D02B : BDFORET_2-0__SHP_LAMB93_D02B_2016-02-16.7z (millesime 2016-02-16)
Licence : Etalab Open License 2.0 — tous usages autorises, attribution requise.

--- Classes retenues (nomenclature TFV / CODE_TFV) --------------------------
BD Foret V2 classe chaque polygone par "Type de Formation Vegetale" (TFV),
prefixe FF (Foret Fermee, couvert arbore >40% — canopee dense) ou FO (Foret
Ouverte, couvert 10-40% — canopee clairsemee), plus LA (Lande/formation
herbacee, pas de foret).

RETENU  : tous les codes commencant par "FF" (19 classes rencontrees sur les
          2 departements — melanges feuillus/coniferes, essences pures :
          hetre, chataignier, chenes, pins (maritime, Alep, laricio/noir),
          sapin/epicea, douglas, etc.) — couvert arbore dense, seul niveau
          coherent avec l'hypothese du modele ITU-R P.833-6 (attenuation par
          propagation A TRAVERS de la vegetation continue).
EXCLU   : "FO*" (foret ouverte, couvert 10-40% — canopee trop clairsemee pour
          representer un milieu de propagation continu au sens du modele) ;
          "LA4" (Lande) et "LA6" (Formation herbacee) — pas de couvert arbore
          du tout, exclusion explicitement demandee au brief (garrigue/lande
          basse). Choix "FF-only" documente ici, pas tranche silencieusement :
          si une inclusion de FO s'avere pertinente plus tard (garrigue haute
          dense par exemple), le refaire est un simple changement du filtre
          ci-dessous, pas une nouvelle extraction.

--- Traitement geometrique ---------------------------------------------------
mapshaper (via npx, invoque en sous-processus) : fusion des 2 departements,
filtre sur CODE_TFV, reprojection Lambert-93 (EPSG:2154, CRS natif BD Foret)
vers WGS84, dissolution en un seul polygone (la distinction entre parcelles
individuelles n'a pas de valeur pour un test d'intersection de trajet RF),
simplification (Visvalingam, 0.15% + filtre des ilots <5ha) — reduit ~33 000
polygones sources a un fichier exploitable cote client sans shapefile brut
de plusieurs dizaines de Mo, cf. objectif du brief. Post-traitement Shapely :
la simplification laisse quelques auto-intersections mineures (mapshaper
-clean ne les repare pas toutes) — corrige par buffer(0), fix standard.

Un premier essai a 1% (moins agressif, sans filtre d'ilots) laissait ~178 000
sommets sur ~3 555 polygones — bien trop pour un test point-in-polygon naif
repete cote client (des dizaines d'antennes x potentiellement des milliers de
cellules de heatmap). Le filtrage des ilots (fragments <5ha, nombreux en
terrain morcele/montagneux corse) et une simplification plus agressive
reduisent a ~2 880 polygones / ~122 000 sommets — la simplification seule ne
descend plus beaucoup en dessous sans deformer visiblement les contours. La
vraie parade cote client n'est PAS plus de simplification mais un prefiltre
bbox par partie de polygone (cf. isPointInForest() dans app.html) — meme
principe que ANFR_GRID deja present dans ce fichier.

Taille obtenue : ~2 Mo bruts, ~500 Ko compresses gzip (Cloudflare Pages sert
les assets statiques compresses automatiquement — c'est le poids reseau reel).

Usage :
    python3 scripts/build_foret_dense_corse_geojson.py

Regeneration : seulement si IGN publie une nouvelle version majeure de BD
Foret (V3) ou une mise a jour de millesime pour la Corse — pas une donnee
appelee a changer souvent.
"""

import json
import shutil
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

OUT_PATH = Path("public/data/foret_dense_corse.geojson")


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


def run_mapshaper(shp_a, shp_b, out_path):
    cmd = [
        "npx", "--yes", "mapshaper",
        "-i", str(shp_a), str(shp_b), "combine-files", "encoding=latin1", "name=foret",
        "-merge-layers",
        "-filter", 'CODE_TFV.substr(0,2) == "FF"',
        "-proj", "wgs84",
        "-dissolve",
        "-simplify", "0.15%", "keep-shapes",
        "-filter-islands", "min-area=50000sqm", "remove-empty",
        "-clean",
        "-o", "format=geojson", "precision=0.0001", str(out_path),
    ]
    print("Execution mapshaper (fusion + filtre FF* + reprojection + simplification)...", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True, shell=(sys.platform == "win32"))
    print(result.stdout, flush=True)
    if result.returncode != 0:
        print(result.stderr, flush=True)
        raise RuntimeError("mapshaper a echoue — cf. stderr ci-dessus")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        shp_a = download_and_extract(work_dir, "D02A", ARCHIVES["D02A"])
        shp_b = download_and_extract(work_dir, "D02B", ARCHIVES["D02B"])

        mapshaper_out = work_dir / "mapshaper_output.geojson"
        run_mapshaper(shp_a, shp_b, mapshaper_out)

        raw = json.loads(mapshaper_out.read_text(encoding="utf-8"))
        # mapshaper produit un GeometryCollection (1 seule geometrie dissoute) —
        # on le convertit en FeatureCollection standard avec metadonnees, plus
        # utile/lisible cote client que le format brut de sortie mapshaper.
        geom_raw = raw["geometries"][0] if "geometries" in raw else raw["features"][0]["geometry"]
        geom = shape(geom_raw)
        if not geom.is_valid:
            # Fix standard pour les auto-intersections residuelles laissees par
            # la simplification (mapshaper -clean ne repare pas systematiquement
            # tout, cf. logs "intersections could not be repaired").
            geom = geom.buffer(0)
            print(f"Geometrie corrigee (buffer(0)) — valide maintenant : {geom.is_valid}", flush=True)

    output = {
        "type": "FeatureCollection",
        "properties": {
            "model": "BD Forêt V2 (IGN) — couvert arboré dense uniquement",
            "source": "IGN, BD Forêt V2, départements 2A + 2B",
            "millesime": "D02A: 2017-05-10, D02B: 2016-02-16",
            "licence": "Etalab Open License 2.0",
            "classes_retenues": "CODE_TFV préfixe FF* (Forêt fermée, couvert arboré >40%) — 19 classes rencontrées (mélanges feuillus/conifères, essences pures : hêtre, châtaignier, chênes, pins, sapin/épicéa, douglas...). Exclus : FO* (forêt ouverte, 10-40%), LA4 (Lande), LA6 (formation herbacée).",
            "date_pretraitement": date.today().isoformat(),
            "traitement": "mapshaper (fusion 2A+2B, filtre CODE_TFV, reprojection Lambert-93→WGS84, dissolution, simplification Visvalingam 1%) + Shapely (buffer(0) validité).",
        },
        "features": [{
            "type": "Feature",
            "properties": {"classe": "foret_fermee_dense"},
            "geometry": mapping(geom),
        }],
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")
    size_mb = OUT_PATH.stat().st_size / 1024 / 1024
    print(f"Ecrit {OUT_PATH} ({size_mb:.1f} Mo bruts)", flush=True)


if __name__ == "__main__":
    main()
