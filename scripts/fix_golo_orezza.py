"""Extend pieve_orezza to absorb uncovered gap in doyenne_du_golo."""
import json
from shapely.geometry import Polygon, MultiPolygon
from shapely.validation import make_valid
from shapely.ops import unary_union

PIEVES_PATH = "docs/data/pieves_polygons.json"
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
pieve_index = {p["slug"]: i for i, p in enumerate(pieves)}

with open("docs/data/doyennes_polygons.json", encoding="utf-8") as f:
    doyennes = json.load(f)["doyennes"]

d_poly = to_shapely(next(d for d in doyennes if d["slug"] == "doyenne_du_golo")["polygon"])

golo_pieves = [p for p in pieves if "golo" in p.get("doyenne_contemporain_majoritaire","") or "golo" in str(p.get("doyennes_visibles",""))]
covered = make_valid(unary_union([to_shapely(p["polygon"]) for p in golo_pieves if len(p.get("polygon",[])) >= 3]))
gap = make_valid(d_poly.difference(covered))
print("Gap area before: %.5f" % gap.area)

p_orezza = pieves[pieve_index["pieve_orezza"]]
orezza_poly = to_shapely(p_orezza["polygon"])
extended = make_valid(unary_union([orezza_poly, gap]))
extended = largest_poly(extended.simplify(TOLERANCE))

old_pts = len(p_orezza["polygon"])
p_orezza["polygon"] = from_shapely(extended)
b = extended.bounds
print("pieve_orezza: %d pts -> %d pts | lat %.3f-%.3f lon %.3f-%.3f" % (
    old_pts, len(p_orezza["polygon"]), b[1],b[3],b[0],b[2]))

# Verify
covered2 = make_valid(unary_union([to_shapely(pieves[pieve_index[p["slug"]]]["polygon"]) for p in golo_pieves if len(p.get("polygon",[])) >= 3]))
gap2 = make_valid(d_poly.difference(covered2))
print("Gap area after: %.5f" % gap2.area)

pieves_data["pieves"] = pieves
with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pieves_data, f, ensure_ascii=False, separators=(",", ":"))
print("%s: %d bytes" % (PIEVES_PATH, len(open(PIEVES_PATH, "rb").read())))
print("Done.")
