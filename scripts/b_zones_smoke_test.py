#!/usr/bin/env python3
"""Smoke test B-ZONES — verifie que chaque polygone zone_geometry est en Corse
(PIP bbox, hard fail) + containment doyenne (informationnel).

Convention coords : zone_geometry.coordinates est en GeoJSON [lon, lat].
A lancer avant chaque commit qui modifie is_zone / zone_geometry.

Usage : python scripts/b_zones_smoke_test.py
Exit 1 si un polygone tombe hors de la bbox Corse.
"""
import json
import sys
from shapely.geometry import shape, Polygon

CORSE_BBOX = (8.5, 41.3, 9.7, 43.2)  # lon_min, lat_min, lon_max, lat_max


def main():
    with open('docs/data/sites_patrimoine.json', encoding='utf-8') as f:
        sites = json.load(f)['sites']

    # doyennes pour containment ([lat,lon] -> [lon,lat])
    with open('docs/data/doyennes_polygons.json', encoding='utf-8') as f:
        doy_raw = json.load(f)['doyennes']
    doy = {}
    for d in doy_raw:
        p = d.get('polygon')
        if p and len(p) >= 4:
            try:
                doy[d['slug']] = Polygon([(c[1], c[0]) for c in p])
            except Exception:
                pass

    zones = [s for s in sites if s.get('is_zone')]
    print(f"B-ZONES a verifier : {len(zones)}")

    fails = []
    for s in zones:
        geom = shape(s['zone_geometry'])
        c = geom.centroid
        in_corse = (CORSE_BBOX[0] <= c.x <= CORSE_BBOX[2] and
                    CORSE_BBOX[1] <= c.y <= CORSE_BBOX[3])
        dslug = s.get('doyenne_contemporain_slug')
        dp = doy.get(dslug)
        if dp is not None and geom.area:
            ratio = geom.intersection(dp).area / geom.area
            cont = f"{dslug} {ratio*100:.0f}%"
            if ratio < 0.5:
                cont += " [<50% — verifier rattachement]"
        else:
            cont = f"{dslug} (pas de polygone doyenne)"
        if not in_corse:
            fails.append(s['slug'])
            print(f"FAIL {s['slug']}: centroide ({c.x:.4f},{c.y:.4f}) HORS CORSE")
        else:
            print(f"OK   {s['slug']:28} centroide ({c.x:.4f},{c.y:.4f})  {cont}")

    if fails:
        print(f"\n{len(fails)} polygone(s) HORS CORSE — STOP avant commit")
        sys.exit(1)
    print(f"\nTous les polygones B-ZONES ({len(zones)}) sont en Corse.")


if __name__ == '__main__':
    main()
