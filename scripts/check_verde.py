import json
from shapely.geometry import Polygon, Point
from shapely.validation import make_valid

with open('docs/data/pieves_polygons.json', encoding='utf-8') as f:
    pieves = json.load(f)['pieves']
with open('docs/data/sites_patrimoine.json', encoding='utf-8') as f:
    sites = json.load(f)['sites']

p_verde = next(p for p in pieves if p['slug'] == 'pieve_verde')
verde_poly = make_valid(Polygon([(lon, lat) for lat, lon in p_verde['polygon']]))
b = verde_poly.bounds
print('pieve_verde bounds: lat %.3f-%.3f, lon %.3f-%.3f' % (b[1], b[3], b[0], b[2]))

carbini_sites = [s for s in sites if s.get('pieve_slug') == 'pieve_carbini']
print('\nSites carbini dans pieve_verde polygon:')
in_verde = []
for s in carbini_sites:
    pt = Point(s['lon'], s['lat'])
    if verde_poly.contains(pt) or verde_poly.distance(pt) < 0.005:
        in_verde.append(s['slug'])
        print('  %s | lat=%s lon=%s' % (s['slug'], s['lat'], s['lon']))

print('\nTotal in verde polygon: %d' % len(in_verde))
print('Remaining in carbini: %d' % (len(carbini_sites) - len(in_verde)))
print('\nSites NOT in verde (stay carbini):')
for s in carbini_sites:
    if s['slug'] not in in_verde:
        print('  %s | lat=%s lon=%s' % (s['slug'], s['lat'], s['lon']))
