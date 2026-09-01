"""
Fusion pieve_caccia -> pieve_giovellina (Cortenais)
- Union des polygones
- Retag 11 sites caccia -> giovellina
- Suppression pieve_caccia
- Mise a jour doyennes_visibles/appartenance de giovellina
"""
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

p_caccia = next(p for p in pieves if p["slug"] == "pieve_caccia")
p_giovellina = next(p for p in pieves if p["slug"] == "pieve_giovellina")

caccia_poly = to_shapely(p_caccia["polygon"])
giovellina_poly = to_shapely(p_giovellina["polygon"])

# Union
merged = make_valid(unary_union([caccia_poly, giovellina_poly]))
merged = largest_poly(merged.simplify(TOLERANCE))
print("pieve_giovellina merged: %d pts -> %d pts" % (len(p_giovellina["polygon"]), len(from_shapely(merged))))

# Update giovellina polygon + doyenne config (union of both)
p_giovellina["polygon"] = from_shapely(merged)
p_giovellina["doyennes_visibles"] = ["doyenne_balagne", "doyenne_du_golo"]
# Recalculate doyennes_appartenance: weighted average by area
total_area = caccia_poly.area + giovellina_poly.area
doy_map = {}
for entry in p_caccia.get("doyennes_appartenance", []):
    doy_map[entry["slug"]] = doy_map.get(entry["slug"], 0) + entry["ratio"] * caccia_poly.area
for entry in p_giovellina.get("doyennes_appartenance", []):
    doy_map[entry["slug"]] = doy_map.get(entry["slug"], 0) + entry["ratio"] * giovellina_poly.area
appartenance = [{"slug": k, "ratio": round(v / total_area, 4)} for k, v in sorted(doy_map.items(), key=lambda x: -x[1])]
p_giovellina["doyennes_appartenance"] = appartenance
p_giovellina["doyenne_contemporain_majoritaire"] = appartenance[0]["slug"]
print("doyennes_appartenance:", appartenance)

# Retag caccia sites -> giovellina
print("\nRetag sites caccia -> pieve_giovellina:")
for s in sites:
    if s.get("pieve_slug") == "pieve_caccia":
        s["pieve_slug"] = "pieve_giovellina"
        print("  %s (doyenne=%s)" % (s["slug"], s.get("doyenne_contemporain_slug")))

# Remove pieve_caccia
pieves = [p for p in pieves if p["slug"] != "pieve_caccia"]
print("\npieve_caccia supprimee. Total pieves: %d" % len(pieves))

# Update communes_count
giovellina_sites = [s for s in sites if s.get("pieve_slug") == "pieve_giovellina"]
p_giovellina["communes_count"] = len(giovellina_sites)
print("pieve_giovellina: %d sites" % len(giovellina_sites))

# Sanity
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
