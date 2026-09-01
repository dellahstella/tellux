"""
PTV Restauration pieve_cauro (Variante B — maximaliste)
- Creation pieve_cauro : cluster nord (Bastelica/Tolla/Bastelicaccia) + cote ouest (Coti-Chiavari)
- Decoupage pieve_ornano : retrait zone cauro
- Retag 10 sites pieve_ornano + 1 site null -> pieve_cauro
- Fix san_pietro_tavaco : doyenne_contemporain_slug -> doyenne_ajaccio
"""

import json
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import unary_union
from shapely.validation import make_valid

PIEVES_PATH = "docs/data/pieves_polygons.json"
SITES_PATH = "docs/data/sites_patrimoine.json"
TOLERANCE = 0.0005

def from_shapely(poly, decimals=5):
    return [[round(lat, decimals), round(lon, decimals)]
            for lon, lat in poly.exterior.coords]

def to_shapely(polygon_ll):
    return make_valid(Polygon([(lon, lat) for lat, lon in polygon_ll]))

def largest_poly(geom):
    if isinstance(geom, Polygon):
        return geom
    polys = [g for g in geom.geoms if isinstance(g, Polygon)] if hasattr(geom, "geoms") else []
    return max(polys, key=lambda g: g.area) if polys else geom

# Load
with open(PIEVES_PATH, encoding="utf-8") as f:
    pieves_data = json.load(f)
pieves = pieves_data["pieves"]

with open(SITES_PATH, encoding="utf-8") as f:
    sites_data = json.load(f)
sites = sites_data["sites"]

pieve_index = {p["slug"]: i for i, p in enumerate(pieves)}

# Current ornano polygon
p_ornano = pieves[pieve_index["pieve_ornano"]]
ornano_poly = to_shapely(p_ornano["polygon"])
print(f"ornano original: {len(p_ornano['polygon'])} pts, area={ornano_poly.area:.4f}")

# Sites to move to cauro (known by slug)
cauro_candidates = [
    "bastelica_paese", "lac_de_tolla", "pont_de_zippitoli_disparu_2023",
    "tour_de_capitello_castelluccio", "san_giovanni_bastelicaccia",
    "tour_d_isolella_sette_navi", "san_nicolao_coti_chiavari",
    "tour_de_la_castagna_coti_chiavari", "tour_de_capo_di_muro",
    "tour_de_capu_neru_coti_chiavari",
    "castello_di_baricci",  # currently null, goes to cauro
]

# Load doyennes for clipping
with open("docs/data/doyennes_polygons.json", encoding="utf-8") as f:
    doyennes = json.load(f)["doyennes"]
ptv_poly = to_shapely(next(d for d in doyennes if d["slug"] == "doyenne_prunelli_taravo_valinco")["polygon"])
es_poly = to_shapely(next(d for d in doyennes if d["slug"] == "doyenne_extreme_sud")["polygon"])
allowed = make_valid(unary_union([ptv_poly, es_poly]))

# Build cauro polygon: buffer around all cauro sites, intersect with ornano + allowed zone
cauro_site_points = []
for s in sites:
    if s["slug"] in cauro_candidates:
        cauro_site_points.append(Point(s["lon"], s["lat"]))
print(f"Cauro sites found: {len(cauro_site_points)}")

buffers = [pt.buffer(0.06) for pt in cauro_site_points]  # ~6km radius each
cauro_union = make_valid(unary_union(buffers))
# Clip to ornano territory + allowed doyennes
cauro_poly_raw = ornano_poly.intersection(cauro_union)
cauro_poly_raw = make_valid(cauro_poly_raw.intersection(allowed))
cauro_poly = make_valid(cauro_poly_raw.simplify(TOLERANCE))
print(f"pieve_cauro polygon: {len(from_shapely(cauro_poly)) if isinstance(cauro_poly, Polygon) else 'MultiPolygon'} pts, area={cauro_poly.area:.4f}")
b = cauro_poly.bounds
print(f"  bounds: lat {b[1]:.3f}-{b[3]:.3f}, lon {b[0]:.3f}-{b[2]:.3f}")

# Ornano new = ornano - cauro
ornano_new_raw = ornano_poly.difference(cauro_poly)
ornano_new = make_valid(ornano_new_raw)
ornano_new = largest_poly(ornano_new.simplify(TOLERANCE))
print(f"pieve_ornano trimmed: {len(from_shapely(ornano_new))} pts, area={ornano_new.area:.4f}")
b2 = ornano_new.bounds
print(f"  bounds: lat {b2[1]:.3f}-{b2[3]:.3f}, lon {b2[0]:.3f}-{b2[2]:.3f}")

# Verify sites end up in correct polygon
print()
from shapely.geometry import Point
ornano_sites_check = [s for s in sites if s.get("pieve_slug") == "pieve_ornano"]
print("=== Verification site -> polygon assignment ===")
baricci = next((s for s in sites if s["slug"] == "castello_di_baricci"), None)
for s in ornano_sites_check + ([baricci] if baricci else []):
    if not s:
        continue
    pt = Point(s["lon"], s["lat"])
    in_cauro = cauro_poly.contains(pt) or cauro_poly.distance(pt) < 0.005
    in_ornano_new = ornano_new.contains(pt) or ornano_new.distance(pt) < 0.005
    expected = "cauro" if s["slug"] in cauro_candidates else "ornano"
    ok = (expected == "cauro" and in_cauro) or (expected == "ornano" and in_ornano_new)
    flag = "OK" if ok else "MISMATCH"
    print(f"  [{flag}] {s['slug']}: expected={expected}, in_cauro={in_cauro}, in_ornano={in_ornano_new}")

# For JSON polygon: convex hull of all cauro site points + buffer,
# clipped to allowed doyenne territory — single polygon covering both clusters visually
from shapely.geometry import MultiPoint
cauro_site_geom = MultiPoint([(s["lon"], s["lat"])
                               for s in sites if s["slug"] in cauro_candidates])
cauro_hull = cauro_site_geom.convex_hull.buffer(0.04)  # ~4km margin
cauro_poly_for_json = make_valid(cauro_hull.intersection(allowed)).simplify(TOLERANCE)
if isinstance(cauro_poly_for_json, MultiPolygon):
    cauro_poly_for_json = largest_poly(cauro_poly_for_json)
print(f"cauro_poly_for_json: {len(from_shapely(cauro_poly_for_json))} pts")
b3 = cauro_poly_for_json.bounds
print(f"  bounds: lat {b3[1]:.3f}-{b3[3]:.3f}, lon {b3[0]:.3f}-{b3[2]:.3f}")

print()

# Build pieve_cauro entry
cauro_entry = {
    "slug": "pieve_cauro",
    "name": "Cauro",
    "doyenne_contemporain_majoritaire": "doyenne_prunelli_taravo_valinco",
    "doyennes_visibles": ["doyenne_prunelli_taravo_valinco"],
    "doyennes_appartenance": [
        {"slug": "doyenne_prunelli_taravo_valinco", "ratio": 1.0}
    ],
    "communes_count": len(cauro_candidates),
    "polygon": from_shapely(cauro_poly_for_json)
}

# Update ornano polygon
p_ornano["polygon"] = from_shapely(ornano_new)
p_ornano["communes_count"] = len([s for s in sites
                                   if s.get("pieve_slug") == "pieve_ornano"
                                   and s["slug"] not in cauro_candidates])

# Insert cauro after ornano (alphabetically close)
ornano_idx = pieve_index["pieve_ornano"]
pieves.insert(ornano_idx, cauro_entry)
pieve_index = {p["slug"]: i for i, p in enumerate(pieves)}

# Site retags
print("=== Site retags ===")

# pieve_ornano -> pieve_cauro (10 sites) + castello_di_baricci (null -> pieve_cauro)
for s in sites:
    if s["slug"] in cauro_candidates:
        old_pieve = s.get("pieve_slug") or "null"
        s["pieve_slug"] = "pieve_cauro"
        if not s.get("doyenne_contemporain_slug"):
            s["doyenne_contemporain_slug"] = "doyenne_prunelli_taravo_valinco"
        print(f"  {s['slug']}: {old_pieve} -> pieve_cauro")

# san_pietro_tavaco: doyenne PTV -> doyenne_ajaccio
tavaco = next((s for s in sites if s["slug"] == "san_pietro_tavaco"), None)
if tavaco:
    old_d = tavaco.get("doyenne_contemporain_slug")
    tavaco["doyenne_contemporain_slug"] = "doyenne_ajaccio"
    print(f"  san_pietro_tavaco: doyenne {old_d} -> doyenne_ajaccio (pieve_ajaccio inchange)")

# Update communes_count for pieve_cauro and pieve_ornano
cauro_sites_count = len([s for s in sites if s.get("pieve_slug") == "pieve_cauro"])
ornano_sites_count = len([s for s in sites if s.get("pieve_slug") == "pieve_ornano"])
pieves[pieve_index["pieve_cauro"]]["communes_count"] = cauro_sites_count
pieves[pieve_index["pieve_ornano"]]["communes_count"] = ornano_sites_count
print(f"\npieve_cauro: {cauro_sites_count} sites")
print(f"pieve_ornano: {ornano_sites_count} sites")

# Write
pieves_data["pieves"] = pieves
with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pieves_data, f, ensure_ascii=False, indent=2)
print(f"\n{PIEVES_PATH}: {len(pieves)} pieves")

with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(sites_data, f, ensure_ascii=False, indent=2)
print(f"{SITES_PATH}: {len(sites)} sites")

# Final verification
print("\n=== Final verification ===")
pieve_slugs = {p["slug"] for p in pieves}
orphan = [s["slug"] for s in sites if s.get("pieve_slug") and s.get("pieve_slug") not in pieve_slugs]
print(f"Orphan pieve slugs in sites: {orphan}")
cauro_check = next(p for p in pieves if p["slug"] == "pieve_cauro")
ornano_check = next(p for p in pieves if p["slug"] == "pieve_ornano")
print(f"pieve_cauro: {len(cauro_check['polygon'])} pts, communes_count={cauro_check['communes_count']}")
print(f"pieve_ornano: {len(ornano_check['polygon'])} pts, communes_count={ornano_check['communes_count']}")
print("Done.")
