"""
Creation pieve_patrimonio (doyenne_du_cap) :
- Polygone = gap non couvert dans doyenne_du_cap
- Retag sites dans le gap -> pieve_patrimonio / doyenne_du_cap
- Insertion apres pieve_nonza alphabetiquement
"""
import json
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.validation import make_valid
from shapely.ops import unary_union

PIEVES_PATH = "docs/data/pieves_polygons.json"
SITES_PATH = "docs/data/sites_patrimoine.json"
TOLERANCE = 0.0002

def to_shapely(poly_ll):
    return make_valid(Polygon([(lo, la) for la, lo in poly_ll]))

def from_shapely(poly, decimals=5):
    return [[round(la, decimals), round(lo, decimals)] for lo, la in poly.exterior.coords]

def largest_poly(geom):
    if isinstance(geom, Polygon): return geom
    if isinstance(geom, MultiPolygon): return max(geom.geoms, key=lambda g: g.area)
    polys = [g for g in getattr(geom, 'geoms', []) if isinstance(g, Polygon)]
    return max(polys, key=lambda g: g.area) if polys else geom

with open(PIEVES_PATH, encoding="utf-8") as f:
    pieves_data = json.load(f)
pieves = pieves_data["pieves"]

with open(SITES_PATH, encoding="utf-8") as f:
    sites_data = json.load(f)
sites = sites_data["sites"]

with open("docs/data/doyennes_polygons.json", encoding="utf-8") as f:
    doyennes = json.load(f)["doyennes"]

d_poly = to_shapely(next(d for d in doyennes if d["slug"] == "doyenne_du_cap")["polygon"])

cap_pieves = [p for p in pieves if "cap" in p.get("doyenne_contemporain_majoritaire","") or "cap" in str(p.get("doyennes_visibles",""))]
covered = make_valid(unary_union([to_shapely(p["polygon"]) for p in cap_pieves if len(p.get("polygon",[])) >= 3]))
gap = make_valid(d_poly.difference(covered))

# Take the largest piece as the patrimonio polygon
gap_poly = largest_poly(gap.simplify(TOLERANCE))
coords = from_shapely(gap_poly)
b = gap_poly.bounds
print("pieve_patrimonio polygon: %d pts area=%.4f lat %.3f-%.3f lon %.3f-%.3f" % (
    len(coords), gap_poly.area, b[1],b[3],b[0],b[2]))

# Build pieve entry
pieve_patrimonio = {
    "slug": "pieve_patrimonio",
    "name": "Patrimonio",
    "doyenne_contemporain_majoritaire": "doyenne_du_cap",
    "doyennes_visibles": ["doyenne_du_cap"],
    "doyennes_appartenance": [{"slug": "doyenne_du_cap", "ratio": 1.0}],
    "communes_count": 0,
    "polygon": coords
}

# Retag sites in gap
print("\nRetag sites -> pieve_patrimonio:")
count = 0
for s in sites:
    pt = Point(s["lon"], s["lat"])
    if gap_poly.contains(pt) or gap_poly.distance(pt) < 0.005:
        old_pieve = s.get("pieve_slug") or "null"
        old_doy = s.get("doyenne_contemporain_slug") or "null"
        s["pieve_slug"] = "pieve_patrimonio"
        s["doyenne_contemporain_slug"] = "doyenne_du_cap"
        print("  %s : pieve %s->patrimonio | doyenne %s->cap" % (s["slug"], old_pieve, old_doy))
        count += 1

pieve_patrimonio["communes_count"] = count

# Insert after pieve_nonza
nonza_idx = next(i for i, p in enumerate(pieves) if p["slug"] == "pieve_nonza")
pieves.insert(nonza_idx + 1, pieve_patrimonio)
print("\nInserted pieve_patrimonio after pieve_nonza (idx %d). Total: %d pieves" % (nonza_idx+1, len(pieves)))

# Verify gap closed
pieve_index = {p["slug"]: i for i, p in enumerate(pieves)}
cap_pieves2 = [p for p in pieves if "cap" in p.get("doyenne_contemporain_majoritaire","") or "cap" in str(p.get("doyennes_visibles",""))]
covered2 = make_valid(unary_union([to_shapely(p["polygon"]) for p in cap_pieves2 if len(p.get("polygon",[])) >= 3]))
gap2 = make_valid(d_poly.difference(covered2))
print("Gap after: %.5f" % gap2.area)

pieve_slugs = {p["slug"] for p in pieves}
orphans = [s["slug"] for s in sites if s.get("pieve_slug") and s["pieve_slug"] not in pieve_slugs]
print("Orphans: %s" % orphans)

# Write
pieves_data["pieves"] = pieves
with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pieves_data, f, ensure_ascii=False, separators=(",", ":"))
print("%s: %d bytes" % (PIEVES_PATH, len(open(PIEVES_PATH, "rb").read())))

sites_data["sites"] = sites
with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(sites_data, f, ensure_ascii=False, separators=(",", ":"))
print("%s: %d bytes" % (SITES_PATH, len(open(SITES_PATH, "rb").read())))
print("Done.")
