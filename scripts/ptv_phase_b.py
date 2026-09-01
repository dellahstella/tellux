"""
PTV Phase B — Prunelli-Taravo-Valinco : 4 anomalies
A1 : retag santa_maria_della_neve → pieve_ajaccio + doyenne_ajaccio
A2 : extension polygon pieve_ornano NW (absorption zone limitrophe Ajaccio)
A3 : création pieve_talavo (polygon est + retag sites)
A4 : retag 5 sites orphelins pieve_sartene_prunelli_taravo_valinco → pieve_istria
     + extension polygon pieve_istria vers le sud
"""

import json
import copy
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import unary_union
from shapely.validation import make_valid

PIEVES_PATH = "docs/data/pieves_polygons.json"
SITES_PATH = "docs/data/sites_patrimoine.json"
DOYENNES_PATH = "docs/data/doyennes_polygons.json"
TOLERANCE = 0.0005

def from_shapely(poly, decimals=5):
    """Shapely (lon,lat) exterior → [[lat,lon]] list."""
    return [[round(lat, decimals), round(lon, decimals)]
            for lon, lat in poly.exterior.coords]

def largest_poly(geom):
    """Extract largest Polygon from any geometry."""
    if isinstance(geom, Polygon):
        return geom
    if isinstance(geom, MultiPolygon):
        return max(geom.geoms, key=lambda g: g.area)
    polys = [g for g in getattr(geom, 'geoms', []) if isinstance(g, Polygon)]
    if polys:
        return max(polys, key=lambda g: g.area)
    return None

def to_shapely(polygon_ll):
    """[[lat,lon]] → Shapely Polygon (lon,lat)."""
    return make_valid(Polygon([(lon, lat) for lat, lon in polygon_ll]))

# ── Load data ────────────────────────────────────────────────────────────────
with open(PIEVES_PATH, encoding="utf-8") as f:
    pieves_data = json.load(f)
pieves = pieves_data["pieves"]

with open(SITES_PATH, encoding="utf-8") as f:
    sites_data = json.load(f)
sites = sites_data["sites"]

with open(DOYENNES_PATH, encoding="utf-8") as f:
    doyennes_data = json.load(f)
doyennes = doyennes_data["doyennes"]

# Index pieves by slug
pieve_index = {p["slug"]: i for i, p in enumerate(pieves)}

def get_pieve(slug):
    return pieves[pieve_index[slug]]

# ── A1 : Retag santa_maria_della_neve ────────────────────────────────────────
print("=== A1 : Retag santa_maria_della_neve ===")
TARGET_SITE = "santa_maria_della_neve_grosseto_prugna_basse"
for s in sites:
    if s["slug"] == TARGET_SITE:
        old_pieve = s.get("pieve_slug")
        old_doyenne = s.get("doyenne_contemporain_slug")
        s["pieve_slug"] = "pieve_ajaccio"
        s["doyenne_contemporain_slug"] = "doyenne_ajaccio"
        print(f"  {TARGET_SITE}")
        print(f"    pieve_slug : {old_pieve} → pieve_ajaccio")
        print(f"    doyenne    : {old_doyenne} → doyenne_ajaccio")

# Update pieve_ajaccio doyennes_appartenance (add if not present)
p_ajaccio = get_pieve("pieve_ajaccio")
# Remove from pieve_ornano doyennes_appartenance if present with trivial ratio
# (santa_maria was in ornano; it was 1 of 21 ornano sites)
# pieve_ornano communes_count doesn't change (it was a single cross-doyenné site)

# ── A2 : Extension pieve_ornano NW ───────────────────────────────────────────
print("\n=== A2 : Extension pieve_ornano NW ===")
# The NW gap between ornano and Ajaccio pieves is geometrically tiny (<0.0001 area)
# pieve_ornano already covers the key NW sites (san_giovanni_bastelicaccia, tour_de_capitello)
# Action: absorb the doyenne_prunelli_taravo_valinco zone not yet covered by ornano or ajaccio
# Strategy: union pieve_ornano with the PTV doyenne NW strip
# (lat 41.85-41.96, lon 8.77-8.91) minus ajaccio pieves

ptv_doyenne = next(d for d in doyennes if d["slug"] == "doyenne_prunelli_taravo_valinco")
ptv_poly = to_shapely(ptv_doyenne["polygon"])

# Ajaccio doyenne
ajaccio_doyenne = next(d for d in doyennes if d["slug"] == "doyenne_ajaccio")
ajaccio_poly = to_shapely(ajaccio_doyenne["polygon"])

# pieve_ornano current polygon
p_ornano = get_pieve("pieve_ornano")
ornano_poly = to_shapely(p_ornano["polygon"])

# pieve_mezzana and pieve_ajaccio (Ajaccio pieves bordering PTV NW)
p_mezzana = get_pieve("pieve_mezzana")
mezzana_poly = to_shapely(p_mezzana["polygon"])
p_ajaccio_pieve = get_pieve("pieve_ajaccio")
ajaccio_pieve_poly = to_shapely(p_ajaccio_pieve["polygon"])

# NW strip: PTV intersection of area lat>41.85, lon<8.92 that is not covered
# by any ajaccio pieve — extend ornano to fill it
nw_strip_coords = [
    (8.77, 41.85), (8.92, 41.85), (8.92, 41.97), (8.77, 41.97), (8.77, 41.85)
]
nw_strip = Polygon(nw_strip_coords)
nw_in_ptv = nw_strip.intersection(ptv_poly)
nw_excl_ajaccio = nw_in_ptv.difference(ajaccio_pieve_poly).difference(mezzana_poly)

ornano_extended_nw = make_valid(unary_union([ornano_poly, nw_excl_ajaccio]))
ornano_extended_nw = largest_poly(ornano_extended_nw.simplify(TOLERANCE))
print(f"  ornano: {len(p_ornano['polygon'])} pts → {len(from_shapely(ornano_extended_nw))} pts")
print(f"  area delta NW: +{nw_excl_ajaccio.area:.5f}")

# ── A3 : Création pieve_talavo ────────────────────────────────────────────────
print("\n=== A3 : Création pieve_talavo ===")
# East gap: lat 41.837-42.031, lon 8.992-9.252 (area=0.0277)
# Compute: PTV doyenne MINUS all existing pieves

all_pieve_polys = []
for p in pieves:
    if len(p["polygon"]) >= 4:
        try:
            all_pieve_polys.append(to_shapely(p["polygon"]))
        except Exception:
            pass

all_union = make_valid(unary_union(all_pieve_polys))
gap_in_ptv = make_valid(ptv_poly.difference(all_union))

# Extract the east gap component (largest uncovered area)
if hasattr(gap_in_ptv, "geoms"):
    east_gap = max(gap_in_ptv.geoms, key=lambda g: g.area)
else:
    east_gap = gap_in_ptv

print(f"  East gap: area={east_gap.area:.4f}")
b = east_gap.bounds
print(f"  Bounds: lat {b[1]:.3f}-{b[3]:.3f}, lon {b[0]:.3f}-{b[2]:.3f}")

# pieve_talavo polygon = east gap (within PTV doyenne)
talavo_poly = make_valid(east_gap.simplify(TOLERANCE))
talavo_coords = from_shapely(talavo_poly)
print(f"  pieve_talavo: {len(talavo_coords)} polygon points")

# Sites to retag → pieve_talavo
# All sites currently in the east gap bounding box with no polygon coverage
talavo_pieve_polys = {p["slug"]: to_shapely(p["polygon"])
                     for p in pieves if len(p["polygon"]) >= 4}

RETAG_TALAVO = []
for s in sites:
    lat, lon = s.get("lat", 0), s.get("lon", 0)
    pt = Point(lon, lat)
    if east_gap.contains(pt) or east_gap.distance(pt) < 0.005:
        # Check it's not already well-covered by another pieve
        covered = any(poly.contains(pt) for slug, poly in talavo_pieve_polys.items())
        if not covered or s.get("pieve_slug") in ("pieve_verde_ajaccio", "pieve_sartene_prunelli_taravo_valinco"):
            RETAG_TALAVO.append(s["slug"])

print(f"  Sites to retag → pieve_talavo: {RETAG_TALAVO}")

for s in sites:
    if s["slug"] in RETAG_TALAVO:
        old = s.get("pieve_slug")
        s["pieve_slug"] = "pieve_talavo"
        s["doyenne_contemporain_slug"] = "doyenne_prunelli_taravo_valinco"
        print(f"    {s['slug']}: {old} → pieve_talavo")

# Build new pieve_talavo entry
pieve_talavo_entry = {
    "slug": "pieve_talavo",
    "name": "Talavo",
    "doyenne_contemporain_majoritaire": "doyenne_prunelli_taravo_valinco",
    "doyennes_visibles": ["doyenne_prunelli_taravo_valinco"],
    "doyennes_appartenance": [
        {"slug": "doyenne_prunelli_taravo_valinco", "ratio": 1.0}
    ],
    "communes_count": len(RETAG_TALAVO),
    "polygon": talavo_coords
}

# ── A4 : Retag orphelins → pieve_istria + extension polygon ──────────────────
print("\n=== A4 : Retag orphelins pieve_sartene_prunelli_taravo_valinco → pieve_istria ===")
ORPHAN_SLUG = "pieve_sartene_prunelli_taravo_valinco"
orphan_sites = [s["slug"] for s in sites if s.get("pieve_slug") == ORPHAN_SLUG]
print(f"  Orphan sites: {orphan_sites}")

for s in sites:
    if s.get("pieve_slug") == ORPHAN_SLUG:
        s["pieve_slug"] = "pieve_istria"
        print(f"    {s['slug']}: {ORPHAN_SLUG} → pieve_istria")

# Extend pieve_istria to cover the south gap (absorb orphan sites area)
p_istria = get_pieve("pieve_istria")
istria_poly = to_shapely(p_istria["polygon"])

# South gap sites to absorb: those in PTV doyenné with pieve_istria tag but outside polygon
# Build bounding box of all istria sites (including freshly retagged orphans)
istria_sites = [s for s in sites if s.get("pieve_slug") == "pieve_istria"
                and s.get("doyenne_contemporain_slug") == "doyenne_prunelli_taravo_valinco"]
print(f"  pieve_istria PTV sites: {len(istria_sites)}")

# Extend polygon to include all PTV istria sites (add small buffer around each outlier)
outlier_polys = []
for s in istria_sites:
    pt = Point(s["lon"], s["lat"])
    if not istria_poly.contains(pt):
        # Add a small buffer polygon around this point
        outlier_polys.append(pt.buffer(0.04))  # ~4km radius buffer
        print(f"    outlier absorbed: {s['slug']} (lat={s['lat']}, lon={s['lon']})")

if outlier_polys:
    istria_extended = make_valid(unary_union([istria_poly] + outlier_polys))
    # Clip to PTV + ES doyennes only (avoid bleeding into other areas)
    es_doyenne = next(d for d in doyennes if d["slug"] == "doyenne_extreme_sud")
    es_poly = to_shapely(es_doyenne["polygon"])
    allowed = make_valid(unary_union([ptv_poly, es_poly]))
    istria_extended = make_valid(istria_extended.intersection(allowed))
    istria_final = largest_poly(istria_extended.simplify(TOLERANCE))
    print(f"  istria: {len(p_istria['polygon'])} pts → {len(from_shapely(istria_final))} pts")
else:
    istria_final = istria_poly.simplify(TOLERANCE)
    print("  No outliers — istria polygon unchanged")

# ── Apply polygon changes ────────────────────────────────────────────────────
print("\n=== Applying polygon changes ===")

# A2: update ornano
pieves[pieve_index["pieve_ornano"]]["polygon"] = from_shapely(ornano_extended_nw)

# A3: insert pieve_talavo (after pieve_ornano alphabetically within PTV)
ornano_idx = pieve_index["pieve_ornano"]
pieves.insert(ornano_idx + 1, pieve_talavo_entry)
# Rebuild index
pieve_index = {p["slug"]: i for i, p in enumerate(pieves)}

# A4: update istria
pieves[pieve_index["pieve_istria"]]["polygon"] = from_shapely(istria_final)

pieves_data["pieves"] = pieves

# ── Write outputs ─────────────────────────────────────────────────────────────
print("\n=== Writing files ===")
with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pieves_data, f, ensure_ascii=False, indent=2)
print(f"  {PIEVES_PATH} → {len(pieves)} pieves")

with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(sites_data, f, ensure_ascii=False, indent=2)
print(f"  {SITES_PATH} → {len(sites)} sites")

# ── Verification ──────────────────────────────────────────────────────────────
print("\n=== Verification ===")
# Check pieve_talavo exists
talavo = next((p for p in pieves if p["slug"] == "pieve_talavo"), None)
print(f"  pieve_talavo: {'OK' if talavo else 'MISSING'} — {len(talavo['polygon']) if talavo else 0} pts")

# Check no orphan slugs remain
orphan_slugs = {"pieve_verde_ajaccio", "pieve_sartene_prunelli_taravo_valinco", "pieve_sartene_plaine_orientale"}
pieve_slugs_in_json = {p["slug"] for p in pieves}
remaining_orphans = [s["slug"] for s in sites if s.get("pieve_slug") in orphan_slugs]
print(f"  Remaining orphan-slug sites: {remaining_orphans}")

# Check A1 site
a1 = next((s for s in sites if s["slug"] == TARGET_SITE), None)
print(f"  {TARGET_SITE}: pieve={a1['pieve_slug']}, doyenne={a1['doyenne_contemporain_slug']}")

# Count talavo sites
talavo_sites = [s["slug"] for s in sites if s.get("pieve_slug") == "pieve_talavo"]
print(f"  pieve_talavo sites: {len(talavo_sites)} — {talavo_sites}")
istria_ptv_sites = [s["slug"] for s in sites if s.get("pieve_slug") == "pieve_istria"
                    and s.get("doyenne_contemporain_slug") == "doyenne_prunelli_taravo_valinco"]
print(f"  pieve_istria PTV sites: {len(istria_ptv_sites)}")

print("\nDone.")
