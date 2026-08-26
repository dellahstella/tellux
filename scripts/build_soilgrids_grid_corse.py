#!/usr/bin/env python3
"""
Build a static soil-texture grid over Corsica (sand %, clay %, bulk density
g/cm3) from SoilGrids v2.0 (ISRIC), for offline lookup by
calcSoilConductivityEffective() (app.html, ITU-R P.527-6 eq. 67-70).

Brief "implementation 3 chantiers orphelins" (2026-08-26), chantier D.

Requires:
    pip install rasterio requests

Output:
    public/data/soilgrids_grid_corse.json

--- Choix d'architecture (ecart signale, pas improvise) -------------------
Le brief proposait d'interroger l'API REST point-par-point de SoilGrids
(rest.isric.org/soilgrids/v2.0/properties/query) sur une grille, en arbitrant
la resolution (250m natif vs ~1km sous-echantillonne) pour un probleme de
POIDS DE FICHIER. En testant, la vraie contrainte bloquante n'est PAS le
poids du fichier de sortie (deja petit a n'importe quelle resolution
raisonnable) mais la politique "fair use" de cette API REST : **5 requetes
par MINUTE** (confirme via la doc ISRIC) — meme a 1km, une grille Corse
aurait demande des dizaines d'heures de requetes sequentielles.

Solution : le service WCS (Web Coverage Service) de SoilGrids
(maps.isric.org/mapserv) n'est PAS soumis a cette limite — il sert des
GeoTIFF bruts a resolution NATIVE (250m) pour une bbox donnee, en UNE
requete par variable (3 requetes au total ici, pas des milliers). On
telecharge le raster complet sur la Corse (3 fichiers, quelques centaines
de Ko chacun) puis on echantillonne LOCALEMENT (gratuit, instantane) sur
la grille de sortie — aucun compromis necessaire sur la resolution de la
grille de sortie elle-meme.

Grille de sortie : IDENTIQUE a public/data/wmm_2025_grid_corse.json
(lat 41.3-43.1 pas 0.05°, lon 8.5-9.6 pas 0.05°, ~5.5km) — reprise telle
quelle plutot que d'introduire une 3e convention de grille differente dans
public/data/ pour la meme zone Corse. Nettement plus grossier que le "~1km"
propose dans le brief, mais deux raisons : (1) coherence avec une grille
deja etablie dans ce repo pour la meme region ; (2) la texture du sol varie
a l'echelle de zones pedologiques larges, pas a l'echelle de la centaine de
metres — un maillage plus fin donnerait une precision illusoire au vu de
l'incertitude deja documentee du modele SoilGrids lui-meme (cf. couche
"uncertainty" disponible mais non recuperee ici, hors scope minimal).
----------------------------------------------------------------------------

Variables (§5.2 P.527-6, eq. 69-70) :
    sand (%), clay (%), bdod (bulk density, g/cm3 = kg/dm3)
    — PAS silt (absent des eq. 69-70, cf. commentaire calcSoilConductivityEffective).
Profondeur : 0-5cm (couche de surface, la plus documentee/stable du produit
SoilGrids ; les couches plus profondes existent mais ne sont pas necessaires
pour ce modele de conductivite effective RF, hors scope ici).

Unites SoilGrids (facteurs de conversion documentes par l'API, verifies en
requete REST ponctuelle avant ce script) :
    sand, clay : valeur brute / 10 -> %  (mapped "g/kg" -> target "%")
    bdod       : valeur brute / 100 -> g/cm3 (mapped "cg/cm3" -> target "kg/dm3")

Exclusion mer/hors-domaine : SoilGrids ne fournit AUCUN nodata/masque
explicite sur ce GeoTIFF (verifie : mask_flag_enums=all_valid, pixels de mer
a 0 comme n'importe quelle donnee) — un point est exclu de la grille de
sortie si sand=clay=bdod=0 simultanement (les 3 a exactement zero en meme
temps n'arrive jamais sur un sol reel ; c'est un proxy pragmatique pour "hors
domaine terrestre du produit", pas une detection cotiere precise).

Licence : SoilGrids v2.0, ISRIC — World Soil Information, CC-BY 4.0. Citation
requise : Poggio et al. (2021), SOIL 7, 217-240,
https://doi.org/10.5194/soil-7-217-2021.

Usage :
    python3 scripts/build_soilgrids_grid_corse.py

Regeneration : jamais necessaire en routine (la texture du sol est stable
dans le temps, contrairement aux donnees geomagnetiques INTERMAGNET) — a
relancer seulement si ISRIC publie une nouvelle version majeure de SoilGrids.
"""

import json
from datetime import date
from io import BytesIO
from pathlib import Path

import requests
import rasterio

WCS_BASE = "https://maps.isric.org/mapserv"
# Bbox de telechargement legerement plus large que la grille de sortie pour
# eviter tout effet de bord a l'echantillonnage (nearest-neighbor pres des limites).
FETCH_BBOX = {"lon_min": 8.4, "lon_max": 9.7, "lat_min": 41.2, "lat_max": 43.2}

# Grille de sortie — identique a public/data/wmm_2025_grid_corse.json.
LAT_MIN, LAT_MAX, LAT_STEP = 41.3, 43.1, 0.05
LON_MIN, LON_MAX, LON_STEP = 8.5, 9.6, 0.05

VARIABLES = {
    # nom_sortie: (coverage_id, d_factor, mapfile)
    "sand": ("sand_0-5cm_mean", 10.0, "sand.map"),
    "clay": ("clay_0-5cm_mean", 10.0, "clay.map"),
    "bdod": ("bdod_0-5cm_mean", 100.0, "bdod.map"),
}


def fetch_coverage(coverage_id, mapfile):
    url = (
        f"{WCS_BASE}?map=/map/{mapfile}&SERVICE=WCS&VERSION=2.0.1"
        f"&REQUEST=GetCoverage&COVERAGEID={coverage_id}&FORMAT=image/tiff"
        f"&SUBSET=Long({FETCH_BBOX['lon_min']},{FETCH_BBOX['lon_max']})"
        f"&SUBSET=Lat({FETCH_BBOX['lat_min']},{FETCH_BBOX['lat_max']})"
        f"&SUBSETTINGCRS=http://www.opengis.net/def/crs/EPSG/0/4326"
        f"&OUTPUTCRS=http://www.opengis.net/def/crs/EPSG/0/4326"
    )
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    if r.headers.get("content-type", "").split(";")[0] != "image/tiff":
        raise RuntimeError(f"Reponse inattendue pour {coverage_id} (pas un GeoTIFF) : {r.text[:300]}")
    return r.content


def main():
    print("Telechargement des 3 couches SoilGrids (WCS, bbox Corse)...", flush=True)
    rasters = {}
    for name, (coverage_id, d_factor, mapfile) in VARIABLES.items():
        raw = fetch_coverage(coverage_id, mapfile)
        rasters[name] = (rasterio.open(BytesIO(raw)), d_factor)
        print(f"  {name} ({coverage_id}) : {len(raw)/1024:.0f} Ko", flush=True)

    n_lat = int(round((LAT_MAX - LAT_MIN) / LAT_STEP)) + 1
    n_lon = int(round((LON_MAX - LON_MIN) / LON_STEP)) + 1

    grid = []
    n_excluded = 0
    for i in range(n_lat):
        lat = round(LAT_MIN + i * LAT_STEP, 3)
        for j in range(n_lon):
            lon = round(LON_MIN + j * LON_STEP, 3)
            values = {}
            for name, (src, d_factor) in rasters.items():
                row, col = src.index(lon, lat)
                raw_val = src.read(1)[row, col]
                values[name] = round(float(raw_val) / d_factor, 3)

            if values["sand"] == 0 and values["clay"] == 0 and values["bdod"] == 0:
                n_excluded += 1
                continue  # hors domaine terrestre (mer), cf. note en tete de fichier

            grid.append({
                "lat": lat,
                "lon": lon,
                "P_sand": values["sand"],
                "P_clay": values["clay"],
                "rho_b_g_cm3": values["bdod"],
            })

    for src, _ in rasters.values():
        src.close()

    output = {
        "model": "SoilGrids v2.0 (ISRIC)",
        "source": "ISRIC World Soil Information, SoilGrids v2.0, https://www.isric.org/explore/soilgrids",
        "citation": "Poggio, L. et al. (2021). SoilGrids 2.0: producing soil information for the globe with quantified spatial uncertainty. SOIL, 7, 217-240. https://doi.org/10.5194/soil-7-217-2021",
        "licence": "CC-BY 4.0",
        "variables": "sand (%), clay (%) — profondeur 0-5cm ; bulk density rho_b (g/cm3) — profondeur 0-5cm. Silt absent (non requis par ITU-R P.527-6 eq. 69-70).",
        "date_extraction": date.today().isoformat(),
        "grid_spec": {
            "lat_min": LAT_MIN, "lat_max": LAT_MAX, "lat_step": LAT_STEP,
            "lon_min": LON_MIN, "lon_max": LON_MAX, "lon_step": LON_STEP,
            "note_resolution": "Grille alignee sur wmm_2025_grid_corse.json (~5.5km) — pas la resolution native SoilGrids (250m) ni le ~1km propose au brief, cf. note en tete de script.",
        },
        "n_points": len(grid),
        "n_excluded_hors_domaine": n_excluded,
        "grid": grid,
    }

    out_path = Path("public/data/soilgrids_grid_corse.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Genere {len(grid)} points ({n_excluded} exclus, hors domaine) -> {out_path}", flush=True)
    print(f"Taille fichier : {out_path.stat().st_size / 1024:.1f} Ko", flush=True)


if __name__ == "__main__":
    main()
