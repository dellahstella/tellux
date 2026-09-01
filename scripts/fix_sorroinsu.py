import json
with open('docs/data/pieves_polygons.json', encoding='utf-8') as f:
    data = json.load(f)
pieves = data['pieves']
p = next(p for p in pieves if p['slug'] == 'pieve_sorroinsu')
print('old:', repr(p['name']))
# "Sorroins" (8 chars) + u-grave U+00F9
name = ''.join(['S','o','r','r','o','i','n','s', chr(0x00F9)])
p['name'] = name
print('new:', repr(p['name']), '| bytes:', p['name'].encode('utf-8').hex(), '| len:', len(p['name']))
with open('docs/data/pieves_polygons.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, separators=(',',':'))
print('done, size=%d' % len(open('docs/data/pieves_polygons.json', 'rb').read()))
