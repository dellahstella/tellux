"""
Fix Cortenais: extend pieve_talcini, pieve_vallerustie, pieve_bozio
to absorb all uncovered gaps inside doyenne_cortenais.
Each gap component is assigned to its nearest neighbour pieve.
"""
import json
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.validation import make_valid
from shapely.ops import unary_union

PIEVES_PATH = "docs/data/pieves_polygons.json"
DOYENNES_PATH = "docs/data/doyennes_polygons.json"
TOLERANCE = 0.0002

def to_shapely(poly_ll):
    return make_valid(Polygon([(lo, la) for la, lo in poly_ll]))

def from_shapely(poly, decimals=5):
    return [[round(la, decimals), round(lo, decimals)] for lo, la in poly.exterior.coords]

def largest_poly(geom):
    if isinstance(geom, Polygon):
        return geom
    if isinstance(geom, MultiPolygon):
        return max(geom.geoms, key=lambda g: g.area)
    polys = [g for g in getattr(geom, 'geoms', []) if isinstance(g, Polygon)]
    return max(polys, key=lambda g: g.area) if polys else geom

with open(PIEVES_PATH, encoding="utf-8") as f:
    pieves_data = json.load(f)
pieves = pieves_data["pieves"]
pieve_index = {p["slug"]: i for i, p in enumerate(pieves)}

with open(DOYENNES_PATH, encoding="utf-8") as f:
    doyennes = json.load(f)["doyennes"]

# Cortenais doyenne boundary
d_cortenais = next(d for d in doyennes if d["slug"] == "doyenne_cortenais")
d_poly = to_shapely(d_cortenais["polygon"])

# All cortenais pieves
cortenais_slugs = [p["slug"] for p in pieves
                   if "cortenais" in p.get("doyenne_contemporain_majoritaire", "")
                   or "cortenais" in str(p.get("doyennes_visibles", ""))]

pieve_polys = {}
for slug in cortenais_slugs:
    p = pieves[pieve_index[slug]]
    if len(p.get("polygon", [])) >= 3:
        pieve_polys[slug] = to_shapely(p["polygon"])

covered = make_valid(unary_union(list(pieve_polys.values())))
gap_total = make_valid(d_poly.difference(covered))

# Candidate pieves to extend (as per user instruction)
CANDIDATES = ["pieve_talcini", "pieve_vallerustie", "pieve_bozio"]
candidate_polys = {s: pieve_polys[s] for s in CANDIDATES}

# For each gap component, assign to nearest candidate
gap_pieces = list(gap_total.geoms) if hasattr(gap_total, "geoms") else [gap_total]
assignment = {s: [] for s in CANDIDATES}

for i, piece in enumerate(gap_pieces):
    if piece.area < 1e-8:
        continue
    best, best_dist = None, float("inf")
    for slug, cpoly in candidate_polys.items():
        d = cpoly.distance(piece)
        if d < best_dist:
            best_dist = d
            best = slug
    if best:
        assignment[best].append(piece)
        b = piece.bounds
        print("Gap %d (area=%.5f lat %.3f-%.3f lon %.3f-%.3f) -> %s (dist=%.4f)" % (
            i, piece.area, b[1], b[3], b[0], b[2], best, best_dist))

# Apply extensions
print("\nApplying extensions:")
for slug in CANDIDATES:
    pieces = assignment[slug]
    if not pieces:
        print("  %s: no gap assigned" % slug)
        continue
    original = candidate_polys[slug]
    extended = make_valid(unary_union([original] + pieces))
    extended = largest_poly(extended.simplify(TOLERANCE))
    p = pieves[pieve_index[slug]]
    old_pts = len(p["polygon"])
    p["polygon"] = from_shapely(extended)
    print("  %s: %d pts -> %d pts (absorbed %d gap pieces, area delta +%.5f)" % (
        slug, old_pts, len(p["polygon"]), len(pieces),
        sum(g.area for g in pieces)))

# Verify
covered2 = make_valid(unary_union([to_shapely(pieves[pieve_index[s]]["polygon"]) for s in cortenais_slugs]))
gap2 = make_valid(d_poly.difference(covered2))
print("\nGap after fix: %.5f" % gap2.area)

# Write
pieves_data["pieves"] = pieves
with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pieves_data, f, ensure_ascii=False, separators=(",", ":"))
print("%s written (%d bytes)" % (PIEVES_PATH, len(open(PIEVES_PATH, "rb").read())))
print("Done.")
