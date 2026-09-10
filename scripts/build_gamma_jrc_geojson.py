#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_gamma_jrc_geojson.py — Pipeline d'acquisition C3 (couche « fond gamma terrestre régional »).

Source : JRC European Atlas of Natural Radiation (EANR) — « 07. Terrestrial gamma dose »
         Dataset ID : jrc-eanr-07_terrestrial-gamma-dose · DOI : 10.2905/JRC.SBESAC0
         Fichier    : tgdrngyh.zip (ESRI ArcInfo Binary Grid, unité nGy/h)
         Grille     : 10 km × 10 km, GISCO/EEA reference grid, CRS natif EPSG:3035 (ETRS89-LAEA)
         Licence    : Creative Commons Attribution 4.0 International (CC BY 4.0)

Produit : public/data/gamma_jrc_corse.geojson — cellules 10 km de la fenêtre Corse,
          reprojetées en WGS84 (CRS84), valeur `tgdr_ngyh` par cellule + classe indicative.

GARDE-FOUS (NCRP-001 GELÉ, garde-fous A.4) :
  - Couche de CONTEXTE affichée uniquement — HORS de tout modèle de calibration/dose Tellux.
  - Grandeur = débit de dose absorbée dans l'air (nGy/h), 10 km : INDICATIF, NON métrologique,
    aucune lecture sanitaire. La classe est un repère de lecture, pas un seuil.
  - Ne fabrique aucune valeur : lit la donnée JRC telle quelle, filtre nodata, arrondit.

Exécution (aucune dépendance système ; GDAL embarqué dans la wheel rasterio) :
    uv run --with rasterio python scripts/build_gamma_jrc_geojson.py
"""
import json
import math
import os
import sys

import rasterio
from rasterio.crs import CRS
from rasterio.warp import transform as warp_transform, transform_bounds

HERE = os.path.dirname(os.path.abspath(__file__))
GRID = os.path.join(HERE, ".cache", "gamma_jrc", "tgdrngyh", "w001001.adf")
OUT = os.path.join(HERE, "..", "public", "data", "gamma_jrc_corse.geojson")

# Le fichier ADF ne porte pas son CRS ; l'aux.xml JRC le donne = LAEA ETRS89 custom
# (« ETRS_1989_LAEA_L48_M09 » : centre lat 48°N / lon 9°E, false E/N = 0, ellipsoïde GRS80).
# CE N'EST PAS EPSG:3035 (centre 52/10, FE 4321000) — utiliser le proj4 exact.
SRC_CRS = CRS.from_proj4("+proj=laea +lat_0=48 +lon_0=9 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs")
DST_CRS = CRS.from_epsg(4326)

# Fenêtre Corse (WGS84), marge large ; le filtrage nodata retire la mer/hors-socle.
CORSE_BBOX = {"lon_min": 8.40, "lon_max": 9.66, "lat_min": 41.30, "lat_max": 43.10}

# Repères de lecture (nGy/h), ancrés sur références reconnues — INDICATIF, non sanitaire :
#   ~59 nGy/h = moyenne mondiale pondérée population (UNSCEAR 2000/2008)
#   70–200 nGy/h = fourchette typique des terrains granitiques
# Bornes de classe purement visuelles (repère de lecture), jamais un seuil réglementaire.
CLASS_BREAKS = [50.0, 75.0, 120.0]  # -> classes 1..4


def classify(v):
    if v < CLASS_BREAKS[0]:
        return 1
    if v < CLASS_BREAKS[1]:
        return 2
    if v < CLASS_BREAKS[2]:
        return 3
    return 4


def main():
    if not os.path.exists(GRID):
        sys.exit("Grille introuvable : %s\nLancer d'abord le téléchargement (voir docs/data-sources/gamma_jrc_corse_notes.md)." % GRID)

    with rasterio.open(GRID) as ds:
        band = ds.read(1)
        T = ds.transform
        nodata = ds.nodata
        H, W = band.shape

        # Fenêtre Corse exprimée dans le CRS natif (EPSG:3035).
        x0, y0, x1, y1 = transform_bounds(
            DST_CRS, SRC_CRS,
            CORSE_BBOX["lon_min"], CORSE_BBOX["lat_min"],
            CORSE_BBOX["lon_max"], CORSE_BBOX["lat_max"],
        )

        features = []
        vals = []
        for row in range(H):
            for col in range(W):
                v = float(band[row, col])
                if nodata is not None and (v == nodata or math.isnan(v) or v < -1e30):
                    continue
                # Coins de la cellule (LAEA)
                cx0, cy0 = T * (col, row)          # coin haut-gauche
                cx1, cy1 = T * (col + 1, row + 1)  # coin bas-droit
                ccx, ccy = (cx0 + cx1) / 2.0, (cy0 + cy1) / 2.0
                # Filtre fenêtre Corse (centre de cellule dans la bbox LAEA)
                if not (x0 <= ccx <= x1 and y0 <= ccy <= y1):
                    continue
                # Reprojection des 4 coins -> WGS84
                xs = [cx0, cx1, cx1, cx0]
                ys = [cy0, cy0, cy1, cy1]
                lons, lats = warp_transform(SRC_CRS, DST_CRS, xs, ys)
                ring = [[round(lons[i], 5), round(lats[i], 5)] for i in range(4)]
                ring.append(ring[0])
                val = round(v, 1)
                vals.append(val)
                features.append({
                    "type": "Feature",
                    "properties": {
                        "tgdr_ngyh": val,
                        "classe_indicative": classify(val),
                    },
                    "geometry": {"type": "Polygon", "coordinates": [ring]},
                })

    if not vals:
        sys.exit("Aucune cellule valide dans la fenêtre Corse — vérifier la bbox / la grille.")

    vals_sorted = sorted(vals)
    fc = {
        "type": "FeatureCollection",
        "name": "gamma_jrc_corse",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "metadata": {
            "description": "Fond gamma terrestre régional (débit de dose absorbée air) — fenêtre Corse, maille 10 km",
            "grandeur": "Débit de dose gamma terrestre absorbée dans l'air (nGy/h). NB : Téléray/ASNR affiche du nSv/h (H*(10)) ; JRC/Euratom assimilent ≈ 1 mais la grandeur est explicitée ici.",
            "statut": "INDICATIF, NON métrologique, aucune lecture sanitaire — couche de contexte hors modèle Tellux (NCRP-001 gelé).",
            "source": "JRC European Atlas of Natural Radiation (EANR) — 07. Terrestrial gamma dose",
            "source_dataset_id": "jrc-eanr-07_terrestrial-gamma-dose",
            "source_doi": "10.2905/JRC.SBESAC0",
            "source_fichier": "tgdrngyh.zip (ESRI ArcInfo Grid, LAEA ETRS89 centre 48N/9E, 10 km) — reprojeté WGS84",
            "attribution": "© European Union, JRC — European Atlas of Natural Radiation (Tollefsen, De Cort, Cinelli, Gruber, Bossew). Licence CC BY 4.0.",
            "licence": "Creative Commons Attribution 4.0 International (CC BY 4.0)",
            "reference_methode": "Bossew et al. 2016, DOI 10.1016/j.jenvrad.2016.02.013",
            "reperes_lecture_ngyh": "~59 (moyenne mondiale UNSCEAR) · 70-200 (terrains granitiques) — repères, pas des seuils",
            "classe_indicative_bornes_ngyh": CLASS_BREAKS,
            "date_production": "2026-07-05",
            "features_total": len(features),
            "tgdr_ngyh_min": vals_sorted[0],
            "tgdr_ngyh_max": vals_sorted[-1],
            "tgdr_ngyh_median": vals_sorted[len(vals_sorted) // 2],
        },
        "features": features,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False, separators=(",", ":"))

    print("OK -> %s" % os.path.normpath(OUT))
    print("  cellules : %d" % len(features))
    print("  nGy/h    : min=%.1f  med=%.1f  max=%.1f" % (vals_sorted[0], fc["metadata"]["tgdr_ngyh_median"], vals_sorted[-1]))


if __name__ == "__main__":
    main()
