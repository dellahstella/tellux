#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assertions post-resync : 0 vraie desync entre sites et polygones.

Sont autorises (preserves par le script resync_sites_pip_post_vague_pieves) :
- Sites en bord cote/ilots ou PIP retourne None pour doyenne et/ou pieve
- Sites sans GPS (lat/lon = None)

NE doit PAS exister apres resync :
- Site dont GPS tombe dans un polygone different de doyenne_contemporain_slug assigne
- Site dont GPS tombe dans un polygone different de pieve_slug assigne
"""
import json
import sys
from pathlib import Path
from shapely.geometry import Polygon, Point

ROOT = Path(__file__).resolve().parent.parent

with (ROOT / 'docs/data/doyennes_polygons.json').open(encoding='utf-8') as f:
    pp_doy = json.load(f)
with (ROOT / 'docs/data/pieves_polygons.json').open(encoding='utf-8') as f:
    pp_pieves = json.load(f)
with (ROOT / 'docs/data/sites_patrimoine.json').open(encoding='utf-8') as f:
    sp = json.load(f)

doy_shapes = {d['slug']: Polygon([(p[1], p[0]) for p in d['polygon']])
              for d in pp_doy['doyennes']}
pieves_shapes = {p['slug']: Polygon([(c[1], c[0]) for c in p['polygon']])
                 for p in pp_pieves['pieves']}

failures_doy = []
failures_pieve = []
preserves_doy = []
preserves_pieve = []

for s in sp['sites']:
    if s.get('phase_publication') not in (1, 2):
        continue
    lat, lon = s.get('lat'), s.get('lon')
    if lat is None or lon is None:
        continue
    pt = Point(lon, lat)

    doy = s.get('doyenne_contemporain_slug')
    if doy and doy in doy_shapes and not doy_shapes[doy].contains(pt):
        true_doy = next((sl for sl, sh in doy_shapes.items() if sh.contains(pt)), None)
        if true_doy:
            failures_doy.append((s['slug'], doy, true_doy))
        else:
            preserves_doy.append(s['slug'])

    pieve = s.get('pieve_slug')
    if pieve and pieve in pieves_shapes and not pieves_shapes[pieve].contains(pt):
        true_pieve = next((sl for sl, sh in pieves_shapes.items() if sh.contains(pt)), None)
        if true_pieve:
            failures_pieve.append((s['slug'], pieve, true_pieve))
        else:
            preserves_pieve.append(s['slug'])

print(f"=== Resync assertions ===")
print(f"  Vraies desyncs doyenne_contemporain_slug : {len(failures_doy)} (attendu 0)")
print(f"  Vraies desyncs pieve_slug                 : {len(failures_pieve)} (attendu 0)")
print(f"  Sites preserves (PIP None doyenne)        : {len(preserves_doy)} (artefacts simplification, OK)")
print(f"  Sites preserves (PIP None pieve)          : {len(preserves_pieve)} (idem)")

if failures_doy:
    print(f"\n--- FAILURES doyenne ---")
    for slug, assigned, true in failures_doy[:10]:
        print(f"  {slug:48s} assigned={assigned:32s} true_pip={true}")
if failures_pieve:
    print(f"\n--- FAILURES pieve ---")
    for slug, assigned, true in failures_pieve[:10]:
        print(f"  {slug:48s} assigned={assigned:32s} true_pip={true}")

if failures_doy or failures_pieve:
    sys.exit(1)
print("\n=== ALL ASSERTIONS PASSED ===")
