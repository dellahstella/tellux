#!/usr/bin/env python3
"""Recupere le polygone officiel du Conservatoire du Littoral pour le Desert
des Agriates et genere les livrables d'audit (_drafts/POLYGONE_AGRIATES_*.json).

Brief Cowork 2026-05-22 — remplacement du polygone approximatif de
desert_des_agriate dans docs/data/zone_geometries.json.

Source : couche WFS officielle CONSERVATOIRE_LITTORAL.PARCELLES:parcelles_protegees
de la Geoplateforme IGN (data.geopf.fr), ressource du jeu de donnees data.gouv.fr
"Espaces proteges du Conservatoire du littoral". Le jeu data.gouv.fr n'expose
aucun shapefile telechargeable directement (seulement un lien portail + services
OGC) ; le WFS donne acces aux memes donnees officielles CdL, par parcelle.

Le site Agriate = 871 parcelles (pera_nom='AGRIATE', pera_id=50, Haute-Corse)
qu'on fusionne (unary_union) pour obtenir la propriete CdL.

Dependances : requests, shapely, pyproj (pas de geopandas/fiona — sortie WFS
deja en GeoJSON, et geopandas indisponible sur Python 3.14).

Reproductible : python _scripts/fetch_agriate_polygon.py
"""
import json
import os
import datetime

import requests
from shapely.geometry import shape, mapping, MultiPolygon
from shapely.ops import unary_union, transform
from pyproj import Transformer

WFS_URL = "https://data.geopf.fr/wfs"
TYPENAME = "CONSERVATOIRE_LITTORAL.PARCELLES:parcelles_protegees"
CQL = "pera_nom = 'AGRIATE'"
PAGE = 2000
SIMPLIFY_M = 50.0
MIN_PART_HA = 10.0  # variante B elaguee : on ecarte les fragments <= 10 ha
SURFACE_OFFICIELLE_HA = 5532

RAW_DIR = "_data/raw_cdl"
DRAFTS_DIR = "_drafts"
DATASET_URL = "https://www.data.gouv.fr/datasets/espaces-proteges-du-conservatoire-du-littoral-1"

_to_2154 = Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True).transform
_to_4326 = Transformer.from_crs("EPSG:2154", "EPSG:4326", always_xy=True).transform


def fetch_parcelles():
    """Telecharge toutes les parcelles Agriate via WFS GetFeature (pagine)."""
    feats = []
    start = 0
    while True:
        params = {
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "REQUEST": "GetFeature",
            "TYPENAMES": TYPENAME,
            "OUTPUTFORMAT": "application/json",
            "SRSNAME": "EPSG:4326",
            "CQL_FILTER": CQL,
            "COUNT": PAGE,
            "STARTINDEX": start,
        }
        r = requests.get(WFS_URL, params=params, timeout=120)
        r.raise_for_status()
        doc = r.json()
        batch = doc.get("features", [])
        feats.extend(batch)
        matched = doc.get("numberMatched")
        print(f"  WFS page startindex={start} : {len(batch)} parcelles "
              f"(numberMatched={matched})")
        if len(batch) < PAGE:
            break
        start += PAGE
    return feats


def count_points(geom):
    """Nombre total de sommets d'un (Multi)Polygon."""
    total = 0
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    for p in polys:
        total += len(p.exterior.coords)
        for ring in p.interiors:
            total += len(ring.coords)
    return total


def main():
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(DRAFTS_DIR, exist_ok=True)
    today = datetime.date.today().isoformat()

    print("[1/6] Telechargement WFS des parcelles Agriate...")
    feats = fetch_parcelles()
    print(f"  -> {len(feats)} parcelles recuperees.")
    with open(os.path.join(RAW_DIR, "agriate_parcelles.geojson"), "w",
              encoding="utf-8") as f:
        json.dump({"type": "FeatureCollection", "features": feats}, f)

    noms = sorted({ft["properties"].get("pera_nom") for ft in feats})
    pera_ids = sorted({str(ft["properties"].get("pera_id")) for ft in feats})
    print(f"  pera_nom distincts : {noms}")
    print(f"  pera_id distincts  : {pera_ids}")
    if not feats:
        raise SystemExit("ARRET : aucune parcelle Agriate trouvee dans le WFS.")

    print("[2/6] Construction + fusion des geometries (unary_union)...")
    geoms = [shape(ft["geometry"]) for ft in feats]
    union_4326 = unary_union(geoms)
    union_2154 = transform(_to_2154, union_4326)
    n_parts = (len(union_2154.geoms)
               if union_2154.geom_type == "MultiPolygon" else 1)
    print(f"  union : {union_4326.geom_type}, {n_parts} part(s)")

    print("[3/6] Surface de controle...")
    surface_ha = round(union_2154.area / 10000.0, 1)
    ecart = round(surface_ha - SURFACE_OFFICIELLE_HA, 1)
    print(f"  surface calculee  : {surface_ha} ha")
    print(f"  surface officielle: {SURFACE_OFFICIELLE_HA} ha  (ecart {ecart:+} ha)")
    if surface_ha < 4000 or surface_ha > 7000:
        raise SystemExit(f"ARRET : surface aberrante ({surface_ha} ha), "
                         "hors [4000, 7000]. Signaler a Soleil.")
    if abs(ecart) > 200:
        print(f"  /!\\ ALERTE : ecart {ecart:+} ha > 200 ha — a signaler a Soleil "
              "(dataset mis a jour ou perimetre 'propriete' different).")

    print("[4/6] Variante A — convex hull simplifie...")
    hull_2154 = union_2154.convex_hull.simplify(SIMPLIFY_M, preserve_topology=True)
    hull_4326 = transform(_to_4326, hull_2154)
    hull_pts = count_points(hull_4326)
    hull_ha = round(hull_2154.area / 10000.0, 1)
    print(f"  convex hull : {hull_pts} points, enveloppe {hull_ha} ha")
    with open(os.path.join(DRAFTS_DIR, "POLYGONE_AGRIATES_CONVEX_HULL.json"),
              "w", encoding="utf-8") as f:
        json.dump(mapping(hull_4326), f, indent=2)

    print(f"[5/6] Variante B — multipart simplifie, elague (parts > {MIN_PART_HA} ha)...")
    all_parts = (list(union_2154.geoms)
                 if union_2154.geom_type == "MultiPolygon" else [union_2154])
    kept = [p for p in all_parts if p.area / 10000.0 > MIN_PART_HA]
    dropped = len(all_parts) - len(kept)
    dropped_ha = round(sum(p.area for p in all_parts
                           if p.area / 10000.0 <= MIN_PART_HA) / 10000.0, 1)
    multi_2154 = MultiPolygon(kept).simplify(SIMPLIFY_M, preserve_topology=True)
    multi_4326 = transform(_to_4326, multi_2154)
    multi_pts = count_points(multi_4326)
    multi_parts = (len(multi_4326.geoms)
                   if multi_4326.geom_type == "MultiPolygon" else 1)
    multi_ha = round(multi_2154.area / 10000.0, 1)
    print(f"  multipart elague : {multi_parts} parts (> {MIN_PART_HA} ha), "
          f"{multi_pts} points, {multi_ha} ha")
    print(f"  {dropped} fragments <= {MIN_PART_HA} ha ecartes ({dropped_ha} ha)")
    with open(os.path.join(DRAFTS_DIR, "POLYGONE_AGRIATES_MULTIPART.json"),
              "w", encoding="utf-8") as f:
        json.dump(mapping(multi_4326), f, indent=2)

    print("[6/6] Centroide + metadonnees...")
    rep = union_4326.representative_point()
    centroid = {"lat": round(rep.y, 6), "lon": round(rep.x, 6),
                "source": "representative_point() de l'union des parcelles CdL"}
    with open(os.path.join(DRAFTS_DIR, "POLYGONE_AGRIATES_CENTROID.json"),
              "w", encoding="utf-8") as f:
        json.dump(centroid, f, indent=2)
    print(f"  centroide : lat={centroid['lat']} lon={centroid['lon']}")

    metadata = {
        "source": "Conservatoire du Littoral (CELRL) — couche WFS "
                   "CONSERVATOIRE_LITTORAL.PARCELLES:parcelles_protegees "
                   "de la Geoplateforme IGN (data.geopf.fr)",
        "dataset_url": DATASET_URL,
        "note_methode": "Le jeu data.gouv.fr n'expose pas de shapefile "
                        "telechargeable ; donnees recuperees via le service WFS "
                        "officiel (memes donnees CdL). Niveau parcelle : "
                        f"{len(feats)} parcelles fusionnees (unary_union).",
        "download_date": today,
        "dataset_version_or_date": "data.gouv.fr maj 2026-04-23",
        "wfs_typename": TYPENAME,
        "wfs_cql_filter": CQL,
        "code_site_cdl": "pera_id=" + ",".join(pera_ids),
        "noms_features_retenues": noms,
        "nb_parcelles": len(feats),
        "surface_officielle_publiee_ha": SURFACE_OFFICIELLE_HA,
        "surface_calculee_ha": surface_ha,
        "ecart_ha": ecart,
        "convex_hull_points": hull_pts,
        "convex_hull_surface_ha": hull_ha,
        "convex_hull_verdict": "non viable — englobe mer + interieur des terres "
                               "(propriete eclatee en 123 fragments)",
        "multipart_variante": "B elaguee — fragments > %s ha conserves" % MIN_PART_HA,
        "multipart_min_part_ha": MIN_PART_HA,
        "multipart_parts": multi_parts,
        "multipart_points_total": multi_pts,
        "multipart_surface_ha": multi_ha,
        "multipart_slivers_ecartes": dropped,
        "multipart_slivers_surface_ha": dropped_ha,
        "centroid": {"lat": centroid["lat"], "lon": centroid["lon"]},
        "simplification_tolerance_m": SIMPLIFY_M,
        "runtime_note": "Variante B = MultiPolygon : renderZonePolygon() de "
                        "patrimoine.html ne lit que coordinates[0]. Necessite un "
                        "brief separe d'adaptation runtime avant application a "
                        "zone_geometries.json.",
    }
    with open(os.path.join(DRAFTS_DIR, "POLYGONE_AGRIATES_METADATA.json"),
              "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print("\nTermine. Livrables dans _drafts/ :")
    print("  POLYGONE_AGRIATES_CONVEX_HULL.json  (variante A)")
    print("  POLYGONE_AGRIATES_MULTIPART.json    (variante B)")
    print("  POLYGONE_AGRIATES_CENTROID.json")
    print("  POLYGONE_AGRIATES_METADATA.json")


if __name__ == "__main__":
    main()
