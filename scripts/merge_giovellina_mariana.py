"""Fusion pieve_giovellina -> pieve_mariana (Golo)."""
import json
from shapely.geometry import Polygon, MultiPolygon
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

p_giov = next(p for p in pieves if p["slug"] == "pieve_giovellina")
p_mar  = next(p for p in pieves if p["slug"] == "pieve_mariana")

giov_poly = to_shapely(p_giov["polygon"])
mar_poly  = to_shapely(p_mar["polygon"])

# Union polygons
merged = make_valid(unary_union([giov_poly, mar_poly]))
merged = largest_poly(merged.simplify(TOLERANCE))
print("pieve_mariana merged: %d pts -> %d pts" % (len(p_mar["polygon"]), len(from_shapely(merged))))
b = merged.bounds
print("  bounds: lat %.3f-%.3f lon %.3f-%.3f" % (b[1],b[3],b[0],b[2]))

# Update mariana doyenne config (weighted average)
total_area = giov_poly.area + mar_poly.area
doy_map = {}
for e in p_giov.get("doyennes_appartenance", []):
    doy_map[e["slug"]] = doy_map.get(e["slug"], 0) + e["ratio"] * giov_poly.area
for e in p_mar.get("doyennes_appartenance", []):
    doy_map[e["slug"]] = doy_map.get(e["slug"], 0) + e["ratio"] * mar_poly.area
appartenance = [{"slug": k, "ratio": round(v / total_area, 4)}
                for k, v in sorted(doy_map.items(), key=lambda x: -x[1])]
p_mar["polygon"] = from_shapely(merged)
p_mar["doyenne_contemporain_majoritaire"] = appartenance[0]["slug"]
p_mar["doyennes_appartenance"] = appartenance
# visibles = all doyennes with ratio >= 0.25 or already in giovellina visibles
visibles_set = set(p_mar.get("doyennes_visibles", [])) | set(p_giov.get("doyennes_visibles", []))
p_mar["doyennes_visibles"] = sorted(visibles_set)
print("doyennes_appartenance:", appartenance)
print("doyennes_visibles:", p_mar["doyennes_visibles"])

# Retag giovellina sites -> mariana
print("\nRetag sites giovellina -> pieve_mariana:")
for s in sites:
    if s.get("pieve_slug") == "pieve_giovellina":
        s["pieve_slug"] = "pieve_mariana"
        print("  %s (doyenne=%s)" % (s["slug"], s.get("doyenne_contemporain_slug")))

# Remove pieve_giovellina
pieves = [p for p in pieves if p["slug"] != "pieve_giovellina"]
print("\npieve_giovellina supprimee. Total pieves: %d" % len(pieves))

mariana_sites = [s for s in sites if s.get("pieve_slug") == "pieve_mariana"]
p_mar["communes_count"] = len(mariana_sites)
print("pieve_mariana: %d sites" % len(mariana_sites))

pieve_slugs = {p["slug"] for p in pieves}
orphans = [s["slug"] for s in sites if s.get("pieve_slug") and s["pieve_slug"] not in pieve_slugs]
print("Orphans: %s" % orphans)

pieves_data["pieves"] = pieves
with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pieves_data, f, ensure_ascii=False, separators=(",", ":"))
print("\n%s: %d bytes" % (PIEVES_PATH, len(open(PIEVES_PATH, "rb").read())))

sites_data["sites"] = sites
with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(sites_data, f, ensure_ascii=False, separators=(",", ":"))
print("%s: %d bytes" % (SITES_PATH, len(open(SITES_PATH, "rb").read())))
print("Done.")
