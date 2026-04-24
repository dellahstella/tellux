#!/usr/bin/env python3
"""
build_antennes_par_commune_corse.py
====================================
Pre-calcul des antennes ANFR de Corse indexees par code INSEE commune.

Pipeline :
  1. Telechargement des 3000 antennes depuis la table Supabase antennas_corse
  2. Telechargement des 360 polygones de commune via geo.api.gouv.fr
  3. Test point-in-polygon (shapely) pour assigner chaque antenne a un code INSEE
  4. Deduplication par (lat, lon, operateur) en agregeant les generations par support
  5. Ecriture de public/data/antennes_par_commune_corse.json

Structure de sortie :
    {
      "_meta": { source, date_extraction, version, counts },
      "communes": {
        "2A004": {
          "nom": "Ajaccio",
          "departement": "2A",
          "n_supports": 48,
          "n_antennes": 243,
          "operateurs": ["Orange", "SFR", "Bouygues", "Free"],
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
    pip install shapely requests
    python scripts/build_antennes_par_commune_corse.py

Auteur  : Tellux (2026-04-24)
Sources : ANFR CartoRadio via table Supabase antennas_corse
          geo.api.gouv.fr (contours IGN AdminExpress)
Licence : donnees ANFR sous Licence Ouverte 2.0 (Etalab)
          contours IGN AdminExpress sous Licence Ouverte IGN
"""

import json
import sys
import time
import urllib.request
from pathlib import Path

try:
    from shapely.geometry import shape, Point
    from shapely.prepared import prep
except ImportError:
    sys.exit("ERREUR : shapely requis. Installer avec : pip install shapely")

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "public" / "data"
OUTPUT_FILE = OUTPUT_DIR / "antennes_par_commune_corse.json"

SB_URL = "https://knckulwghgfrxmbweada.supabase.co"
SB_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtu"
    "Y2t1bHdnaGdmcnhtYndlYWRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NTAxMzQsImV4cCI6"
    "MjA4OTIyNjEzNH0.Cu9dvxFyn-5pbOP65gowCEQvRti74CLnlNYf92jebis"
)

GEO_API = "https://geo.api.gouv.fr/communes"

# Generations ordonnees canoniquement
GEN_ORDER = ["2G", "3G", "4G", "5G"]


# ---------------------------------------------------------------------------
# FETCH
# ---------------------------------------------------------------------------

def fetch_antennas():
    """Telecharge les 3000 antennes depuis Supabase (pagination 1000)."""
    print("Telechargement antennas_corse depuis Supabase...")
    rows = []
    page = 0
    while True:
        url = (
            f"{SB_URL}/rest/v1/antennas_corse"
            f"?select=id,lat,lon,generation,commune,operateur,sup_id"
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


def fetch_polygons():
    """Telecharge les 360 polygones de commune corse via geo.api.gouv.fr."""
    print("Telechargement des polygones de commune (2A + 2B)...")
    features = []
    for dep in ("2A", "2B"):
        url = (
            f"{GEO_API}?codeDepartement={dep}"
            f"&fields=nom,code,contour&format=geojson&geometry=contour"
        )
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read())
        features.extend(data.get("features", []))
    print(f"  {len(features)} polygones recus")
    return features


# ---------------------------------------------------------------------------
# POINT-IN-POLYGON
# ---------------------------------------------------------------------------

def build_polygon_index(features):
    """Cree une liste (code_insee, nom, dep, prepared_polygon, bbox)."""
    index = []
    for feat in features:
        props = feat["properties"]
        code = props["code"]
        nom = props["nom"]
        dep = code[:2]
        geom = shape(feat["geometry"])
        bbox = geom.bounds  # (minx, miny, maxx, maxy)
        index.append(
            {
                "code": code,
                "nom": nom,
                "departement": dep,
                "geom": geom,
                "prepared": prep(geom),
                "bbox": bbox,
            }
        )
    return index


def assign_insee(lat, lon, polygons):
    """Retourne le code INSEE de la commune qui contient le point (lat, lon)."""
    pt = Point(lon, lat)
    for poly in polygons:
        minx, miny, maxx, maxy = poly["bbox"]
        if lon < minx or lon > maxx or lat < miny or lat > maxy:
            continue
        if poly["prepared"].contains(pt):
            return poly["code"], poly["nom"], poly["departement"]
    return None, None, None


# ---------------------------------------------------------------------------
# AGGREGATION
# ---------------------------------------------------------------------------

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


def aggregate(antennas, polygons):
    """Regroupe par commune INSEE puis par support (lat, lon, operateur)."""
    by_commune = {}
    unassigned = []
    t0 = time.time()

    for i, ant in enumerate(antennas):
        if i > 0 and i % 500 == 0:
            print(f"  {i}/{len(antennas)} antennes traitees ({time.time()-t0:.1f}s)")

        lat = ant.get("lat")
        lon = ant.get("lon")
        gen = ant.get("generation")
        op = ant.get("operateur")

        if lat is None or lon is None:
            unassigned.append({"reason": "no_coords", "antenna": ant})
            continue

        code, nom, dep = assign_insee(lat, lon, polygons)
        if code is None:
            unassigned.append(
                {
                    "reason": "not_in_corsica",
                    "lat": lat,
                    "lon": lon,
                    "operateur": op,
                    "generation": gen,
                }
            )
            continue

        bucket = by_commune.setdefault(
            code,
            {
                "code_insee": code,
                "nom": nom,
                "departement": dep,
                "supports_map": {},
            },
        )

        # Cle de support = (lat arrondi, lon arrondi, operateur)
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

    print(f"  Done in {time.time()-t0:.1f}s")
    return by_commune, unassigned


def finalize(by_commune):
    """Transforme la map interne en structure finale triee."""
    out = {}
    for code, bucket in by_commune.items():
        supports = list(bucket["supports_map"].values())
        # Tri canonique generations sur chaque support
        for s in supports:
            s["generations"] = sort_generations(s["generations"])
        # Tri supports : nb antennes desc, puis operateur
        supports.sort(key=lambda s: (-s["n_antennes"], s["operateur"] or ""))
        # Agregats commune
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
    features = fetch_polygons()
    polygons = build_polygon_index(features)

    print(f"Assignation INSEE de {len(antennas)} antennes sur {len(polygons)} polygones...")
    by_commune, unassigned = aggregate(antennas, polygons)
    final = finalize(by_commune)

    # Meta
    n_communes_with_antenna = len(final)
    n_supports_total = sum(c["n_supports"] for c in final.values())
    n_antennes_placed = sum(c["n_antennes"] for c in final.values())

    out = {
        "_meta": {
            "source": "ANFR CartoRadio via Supabase antennas_corse",
            "source_polygons": "geo.api.gouv.fr (IGN AdminExpress)",
            "date_extraction": "2026-04-24",
            "version": "1.0",
            "pipeline": "scripts/build_antennes_par_commune_corse.py",
            "n_antennes_source": len(antennas),
            "n_antennes_placees": n_antennes_placed,
            "n_antennes_non_placees": len(unassigned),
            "n_supports_total": n_supports_total,
            "n_communes_avec_antenne": n_communes_with_antenna,
            "note": (
                "Antennes indexees par code INSEE via test point-in-polygon "
                "sur contours IGN. Supports = groupes par (lat arrondi, lon arrondi, "
                "operateur). Le champ 'generations' liste les technologies 2G/3G/4G/5G "
                "presentes sur le support. Donnees ANFR sous Licence Ouverte 2.0."
            ),
        },
        "communes": final,
    }

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
        print(f"  Non placees : {len(unassigned)} (premieres 5) :")
        for u in unassigned[:5]:
            print(f"    - {u}")


if __name__ == "__main__":
    main()
