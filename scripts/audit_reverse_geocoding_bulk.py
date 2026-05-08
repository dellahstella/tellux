#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit_reverse_geocoding_bulk.py — Brief 35 Bonus Cat. 2.

Audit bulk : pour chaque site de sites_patrimoine.json, fait un point-in-polygon
de ses (lat, lon) contre :
  - doyennes_polygons.json (9 doyennés post-fusion)
  - pieves_polygons.json (47 pieves)

Compare le résultat géographique au champ déclaré (`doyenne_contemporain_slug`,
`pieve_slug`) et flag les mismatches.

Sortie : _drafts/audit_reverse_geocoding_{TODAY}.csv

Format CSV :
    slug, name, lat, lon,
    doyenne_declared, doyenne_real_geo, doyenne_mismatch,
    pieve_declared, pieve_real_geo, pieve_mismatch,
    in_corse, axe_corpus, note

Aucune modification du JSON. Pure analyse.

Usage :
    python scripts/audit_reverse_geocoding_bulk.py
    python scripts/audit_reverse_geocoding_bulk.py --filter doyenne_du_cap
    python scripts/audit_reverse_geocoding_bulk.py --only-mismatch

Author : Cowork (Brief 35 Bonus, 2026-05-06)
"""

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITES_JSON = ROOT / "docs" / "data" / "sites_patrimoine.json"
DOYENNES_JSON = ROOT / "docs" / "data" / "doyennes_polygons.json"
PIEVES_JSON = ROOT / "docs" / "data" / "pieves_polygons.json"
DRAFTS_DIR = ROOT / "_drafts"

CORSE_BBOX = {"lat_min": 41.30, "lat_max": 43.10, "lon_min": 8.50, "lon_max": 9.65}


def point_in_ring(lat, lon, ring):
    """Ray-casting point-in-polygon. ring = liste de [lat, lon]."""
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        yi, xi = ring[i][0], ring[i][1]
        yj, xj = ring[j][0], ring[j][1]
        denom = (yj - yi)
        if denom == 0:
            denom = 1e-12
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / denom + xi):
            inside = not inside
        j = i
    return inside


def reverse_geocode(lat, lon, polygons_data):
    """Trouve le slug de polygone qui contient (lat, lon). None si aucun match."""
    for entry in polygons_data:
        polygon = entry.get("polygon")
        if polygon and point_in_ring(lat, lon, polygon):
            return entry["slug"]
    return None


def in_corse(lat, lon):
    """Vérifie si le point est dans la bbox de la Corse."""
    return (CORSE_BBOX["lat_min"] <= lat <= CORSE_BBOX["lat_max"]
            and CORSE_BBOX["lon_min"] <= lon <= CORSE_BBOX["lon_max"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", help="Filtre par doyenne_contemporain_slug déclaré")
    parser.add_argument("--only-mismatch", action="store_true",
                        help="N'écrit dans le CSV que les sites avec mismatch")
    args = parser.parse_args()

    with open(SITES_JSON, encoding="utf-8") as f:
        sites = json.load(f)["sites"]
    with open(DOYENNES_JSON, encoding="utf-8") as f:
        doyennes = json.load(f)["doyennes"]
    with open(PIEVES_JSON, encoding="utf-8") as f:
        pieves = json.load(f)["pieves"]

    if args.filter:
        sites = [s for s in sites if s.get("doyenne_contemporain_slug") == args.filter]

    print(f"[reverse-geo] {len(sites)} sites à analyser")
    print(f"[reverse-geo] {len(doyennes)} doyennés, {len(pieves)} pieves chargés")

    today = date.today().isoformat()
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = DRAFTS_DIR / f"audit_reverse_geocoding_{today}.csv"

    n_total = 0
    n_doy_mismatch = 0
    n_piv_mismatch = 0
    n_in_mer = 0
    n_no_doy = 0
    n_no_piv = 0
    rows = []

    for s in sites:
        lat = s.get("lat")
        lon = s.get("lon")
        if lat is None or lon is None:
            continue

        in_c = in_corse(lat, lon)
        if not in_c:
            n_in_mer += 1

        doy_decl = s.get("doyenne_contemporain_slug")
        piv_decl = s.get("pieve_slug")
        doy_geo = reverse_geocode(lat, lon, doyennes)
        piv_geo = reverse_geocode(lat, lon, pieves)

        if doy_geo is None:
            n_no_doy += 1
        if piv_geo is None:
            n_no_piv += 1

        # Mismatch : declared non null + geo non null + différents
        doy_mismatch = (doy_decl is not None and doy_geo is not None and doy_decl != doy_geo)
        piv_mismatch = (piv_decl is not None and piv_geo is not None and piv_decl != piv_geo)

        if doy_mismatch:
            n_doy_mismatch += 1
        if piv_mismatch:
            n_piv_mismatch += 1

        notes = []
        if not in_c:
            notes.append("HORS_CORSE_BBOX")
        if doy_geo is None and doy_decl:
            notes.append("doyenne_geo_NONE")
        if piv_geo is None and piv_decl:
            notes.append("pieve_geo_NONE")

        if args.only_mismatch and not (doy_mismatch or piv_mismatch or not in_c):
            continue

        rows.append([
            s["slug"], s.get("name") or s.get("nom") or "",
            lat, lon,
            doy_decl or "", doy_geo or "", "TRUE" if doy_mismatch else "FALSE",
            piv_decl or "", piv_geo or "", "TRUE" if piv_mismatch else "FALSE",
            "TRUE" if in_c else "FALSE",
            s.get("axe_corpus") or "",
            "; ".join(notes),
        ])
        n_total += 1

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "slug", "name", "lat", "lon",
            "doyenne_declared", "doyenne_real_geo", "doyenne_mismatch",
            "pieve_declared", "pieve_real_geo", "pieve_mismatch",
            "in_corse_bbox", "axe_corpus", "note"
        ])
        writer.writerows(rows)

    print()
    print(f"[reverse-geo] CSV -> {csv_path}")
    print(f"[reverse-geo] sites analysés     : {len(sites)}")
    print(f"[reverse-geo] sites en CSV       : {n_total}")
    print(f"[reverse-geo] mismatch doyenné   : {n_doy_mismatch}")
    print(f"[reverse-geo] mismatch pieve     : {n_piv_mismatch}")
    print(f"[reverse-geo] hors bbox Corse    : {n_in_mer}")
    print(f"[reverse-geo] doyenné_geo NONE   : {n_no_doy} (sites hors polygones)")
    print(f"[reverse-geo] pieve_geo NONE     : {n_no_piv} (sites hors polygones)")


if __name__ == "__main__":
    main()
