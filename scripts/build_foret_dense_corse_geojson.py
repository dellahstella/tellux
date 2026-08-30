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
prefixe FF (Foret Fermee, couvert arbore >40%) ou FO (Foret Ouverte, couvert
10-40%), plus LA (Lande/formation herbacee).

--- REVISION 2026-08-30 : "option C", liste blanche d'essences hautes --------
Le filtre "tous les FF*" (2026-08-26 -> 2026-08-30) donnait ~5 100 km2, soit
~59% de la Corse (donnee source, PAS une inflation du pipeline — verifie en
mesurant les shapefiles bruts). Cause : le seuil BD Foret V2 "foret fermee"
= couvert arbore >=40% SANS critere de hauteur ; en Corse il range en "foret
fermee" une grande part du maquis haut arbore (2-5 m), non pertinent pour
ITU-R P.833-6 (le modele suppose la traversee d'un couvert haut a hauteur
d'antenne). La classe FF1-00-00 "melange de feuillus" pesait 1 850 km2 a elle
seule (diagnostic : _drafts/DIAGNOSTIC_FORET_DENSE_2026-08-30.md).

RETENU  : tous les FF* SAUF la liste FF_EXCLUDE ci-dessous. Ce qui reste =
          formations a essence dominante identifiee et haute (hetre FF1-09,
          chataignier FF1-10, chenes decidus FF1G01, chene vert FF1G06) OU
          a composante resineuse (pin laricio/noir FF2G53, pin maritime
          FF2-51, sapin/epicea FF2G61, autres pins et coniferes FF2*,
          melanges feuillus/coniferes FF31/FF32). ~2 475 km2 = ~28,5% de la
          Corse (16 850 polygones sources).
EXCLU   : FF_EXCLUDE = ["FF0", "FF1-00", "FF1-00-00", "FF1-49-49"] —
          - FF0  "foret fermee SANS couvert arbore" : artefact de la base.
          - FF1-00, FF1-00-00 "feuillus (en ilots / en melange indifferencie)"
            + FF1-49-49 "autre feuillu pur" : classes de feuillus non
            differencies qui, en Corse, recouvrent la mosaique maquis-foret
            (chene vert bas, arbousier, bruyere arborescente) plutot qu'une
            futaie continue.
          - "FO*" (foret ouverte 10-40%), "LA*" (lande/herbace) : deja hors
            du prefixe FF, jamais inclus.
DETTE   : distinction fine foret-haute / maquis-foret (ex. Copernicus Tree
          Cover Density raster 10 m, ou donnee de hauteur de canopee) — cf.
          DETTES_TECHNIQUES. Le present filtre est une approximation par
          classe, pas une mesure de hauteur.
          Ajuster = editer FF_EXCLUDE ci-dessous, re-executer, pas de nouvelle
          extraction.

--- Traitement geometrique ---------------------------------------------------
mapshaper (via npx, invoque en sous-processus) : fusion des 2 departements,
filtre CODE_TFV (option C), reprojection Lambert-93 (EPSG:2154, CRS natif BD
Foret) vers WGS84, dissolution, simplification Visvalingam 0.6% (keep-shapes)
+ filtre des ilots <5ha, -clean. Post-traitement Shapely : buffer(0) sur les
auto-intersections residuelles.

Note sur la simplification : le filtre "tous les FF*" imposait 0.15% (tres
agressif) pour tenir la taille de fichier. L'option C reduit la donnee source
a ~2 475 km2 (16 850 polygones) — a couverture moindre on peut se permettre
0.6% (meilleure fidelite de contour) tout en restant compact. Le cout client
du test point-in-polygon est deja borne par le prefiltre bbox par partie
(isPointInForest() dans app.html), pas par le nombre total de sommets.

Taille obtenue (option C, 0.6%) : ~1,7 Mo bruts.

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


# Classes FF* EXCLUES (option C, 2026-08-30) — cf. docstring section "Classes retenues".
# On garde tous les FF* SAUF les classes de feuillus indifferencies (qui, en Corse,
# correspondent largement a la mosaique maquis-foret) et l'artefact FF0.
FF_EXCLUDE = ["FF0", "FF1-00", "FF1-00-00", "FF1-49-49"]


def run_mapshaper(shp_a, shp_b, out_path):
    ff_filter = (
        'CODE_TFV && CODE_TFV.substr(0,2) == "FF" && '
        + repr(FF_EXCLUDE).replace("'", '"')
        + ".indexOf(CODE_TFV) == -1"
    )
    cmd = [
        "npx", "--yes", "mapshaper",
        "-i", str(shp_a), str(shp_b), "combine-files", "encoding=latin1", "name=foret",
        "-merge-layers",
        "-filter", ff_filter,
        "-proj", "wgs84",
        "-dissolve",
        "-simplify", "0.6%", "keep-shapes",
        "-filter-islands", "min-area=50000sqm", "remove-empty",
        "-clean",
        "-o", "format=geojson", "precision=0.0001", str(out_path),
    ]
    print("Execution mapshaper (fusion + filtre FF* option C + reprojection + simplification)...", flush=True)
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
            "model": "BD Forêt V2 (IGN) — forêt fermée à essence haute (option C)",
            "source": "IGN, BD Forêt V2, départements 2A + 2B",
            "millesime": "D02A: 2017-05-10, D02B: 2016-02-16",
            "licence": "Etalab Open License 2.0",
            "classes_retenues": (
                "CODE_TFV préfixe FF* (Forêt fermée, couvert arboré ≥40%) SAUF "
                + ", ".join(FF_EXCLUDE)
                + " (feuillus indifférenciés = mosaïque maquis-forêt en Corse ; FF0 = artefact). "
                "Reste : hêtre, châtaignier, chênes décidus/verts, pins (laricio/noir, maritime, "
                "Alep…), sapin/épicéa, douglas, autres conifères, mélanges feuillus/conifères. "
                "≈ 2 475 km² ≈ 28,5 % de la Corse. Dette : distinction fine forêt-haute/maquis "
                "(Copernicus Tree Cover Density ou hauteur de canopée)."
            ),
            "date_pretraitement": date.today().isoformat(),
            "traitement": "mapshaper (fusion 2A+2B, filtre CODE_TFV option C, reprojection Lambert-93→WGS84, dissolution, simplification Visvalingam 0.6% + filtre îlots <5ha) + Shapely (buffer(0) validité).",
        },
        "features": [{
            "type": "Feature",
            "properties": {"classe": "foret_fermee_essence_haute"},
            "geometry": mapping(geom),
        }],
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False), encoding="utf-8")
    size_mb = OUT_PATH.stat().st_size / 1024 / 1024
    print(f"Ecrit {OUT_PATH} ({size_mb:.1f} Mo bruts)", flush=True)


if __name__ == "__main__":
    main()
