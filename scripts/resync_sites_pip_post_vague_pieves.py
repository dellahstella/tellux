#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-derive doyenne_contemporain_slug + pieve_slug de chaque site
via PIP sur polygones actuels (post-Vague Pieves PR1+PR2 + cascades).

Arbitrage Soleil 2026-05-24 : Strategie B integrale.
- Re-derive TOUS les sites P1+P2+P3 dont GPS tombe dans un polygone different.
- Annule l'arbitrage editorial Patrimonio area (4 sites passeront Cap -> Golo).
- Preserve lat/lon/commune_insee/gps_locked/gps_source (jamais touches).
- Preserve sites dont PIP retourne None (bord cote, ilots, simplification).

Conformement au brief §6.
"""
import json
from pathlib import Path
from shapely.geometry import Polygon, Point

ROOT = Path(__file__).resolve().parent.parent

with (ROOT / 'docs/data/doyennes_polygons.json').open(encoding='utf-8') as f:
    pp_doy = json.load(f)
with (ROOT / 'docs/data/pieves_polygons.json').open(encoding='utf-8') as f:
    pp_pieves = json.load(f)
SITES_PATH = ROOT / 'docs/data/sites_patrimoine.json'
with SITES_PATH.open(encoding='utf-8') as f:
    sp = json.load(f)

doyennes_shapes = {d['slug']: Polygon([(p[1], p[0]) for p in d['polygon']])
                   for d in pp_doy['doyennes']}
pieves_shapes = {p['slug']: Polygon([(c[1], c[0]) for c in p['polygon']])
                 for p in pp_pieves['pieves']}

changes_doy = []
changes_pieve = []
preserved_pip_none = []

for s in sp['sites']:
    lat, lon = s.get('lat'), s.get('lon')
    if lat is None or lon is None:
        continue
    pt = Point(lon, lat)

    # Doyenne contemporain via PIP
    true_doy = next((slug for slug, shape in doyennes_shapes.items()
                     if shape.contains(pt)), None)
    cur_doy = s.get('doyenne_contemporain_slug')
    if true_doy and cur_doy != true_doy:
        changes_doy.append({
            'slug': s['slug'], 'phase': s.get('phase_publication'),
            'before': cur_doy, 'after': true_doy,
        })
        s['doyenne_contemporain_slug'] = true_doy
    elif true_doy is None and cur_doy:
        # PIP retourne None mais site a un doyenne assigne -> preserve
        preserved_pip_none.append({
            'slug': s['slug'], 'kept_doyenne': cur_doy,
        })

    # Pieve via PIP
    true_pieve = next((slug for slug, shape in pieves_shapes.items()
                       if shape.contains(pt)), None)
    cur_pieve = s.get('pieve_slug')
    if true_pieve and cur_pieve != true_pieve:
        changes_pieve.append({
            'slug': s['slug'], 'phase': s.get('phase_publication'),
            'before': cur_pieve, 'after': true_pieve,
        })
        s['pieve_slug'] = true_pieve

# Sauvegarder
with SITES_PATH.open('w', encoding='utf-8') as f:
    json.dump(sp, f, ensure_ascii=False, separators=(",", ":"))

print(f"=== Resync PIP termine ===")
print(f"doyenne_contemporain_slug modifies : {len(changes_doy)}")
print(f"pieve_slug modifies                 : {len(changes_pieve)}")
print(f"Sites preserves (PIP=None bord)    : {len(preserved_pip_none)}")

if changes_doy:
    print("\n--- Changements doyenne (top 30) ---")
    for c in changes_doy[:30]:
        print(f"  P{c['phase']} {c['slug']:48s} {str(c['before']):32s} -> {c['after']}")
if changes_pieve:
    print("\n--- Changements pieve (top 30) ---")
    for c in changes_pieve[:30]:
        print(f"  P{c['phase']} {c['slug']:48s} {str(c['before']):32s} -> {c['after']}")
