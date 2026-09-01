"""
Fix ES doyenne:
1. Retag sites carbini -> pieve_verde (sites geometriquement dans le polygone verde)
2. Fix pieve_sartene.name double-encodage
"""
import json
from shapely.geometry import Polygon, Point
from shapely.validation import make_valid

PIEVES_PATH = "docs/data/pieves_polygons.json"
SITES_PATH = "docs/data/sites_patrimoine.json"

with open(PIEVES_PATH, encoding="utf-8") as f:
    pieves_data = json.load(f)
pieves = pieves_data["pieves"]

with open(SITES_PATH, encoding="utf-8") as f:
    sites_data = json.load(f)
sites = sites_data["sites"]

# --- Fix 1: pieve_sartene name ---
p_sartene = next(p for p in pieves if p["slug"] == "pieve_sartene")
old_name = p_sartene.get("name")
p_sartene["name"] = "Sartène"
print("pieve_sartene name: %r -> 'Sartène'" % old_name)

# --- Fix 2: retag carbini sites inside verde polygon ---
p_verde = next(p for p in pieves if p["slug"] == "pieve_verde")
verde_poly = make_valid(Polygon([(lon, lat) for lat, lon in p_verde["polygon"]]))

VERDE_RETAG = []
for s in sites:
    if s.get("pieve_slug") != "pieve_carbini":
        continue
    pt = Point(s["lon"], s["lat"])
    if verde_poly.contains(pt) or verde_poly.distance(pt) < 0.005:
        VERDE_RETAG.append(s["slug"])

print("\nRetag carbini -> pieve_verde (%d sites):" % len(VERDE_RETAG))
for s in sites:
    if s["slug"] in VERDE_RETAG:
        s["pieve_slug"] = "pieve_verde"
        print("  %s" % s["slug"])

# --- Fix 3: orphan pieve_slug (anciens slugs combines supprimes) ---
ORPHAN_ASSIGN = {
    "castidetta":                   ("pieve_sartene",  "doyenne_extreme_sud"),
    "san_giuseppu_arbellara_haute":  ("pieve_ornano",   "doyenne_prunelli_taravo_valinco"),
    "san_pietro_fozzano":            ("pieve_ornano",   "doyenne_prunelli_taravo_valinco"),
    "san_rocco_viggianello_bas":     ("pieve_istria",   "doyenne_prunelli_taravo_valinco"),
    "santa_maria_arbellara":         ("pieve_istria",   "doyenne_prunelli_taravo_valinco"),
    "santa_maria_propriano_baraci":  ("pieve_istria",   "doyenne_prunelli_taravo_valinco"),
}
print("\nFix orphans:")
for s in sites:
    if s["slug"] in ORPHAN_ASSIGN:
        pieve, doyenne = ORPHAN_ASSIGN[s["slug"]]
        print("  %s: %s -> %s | doyenne: %s -> %s" % (
            s["slug"], s.get("pieve_slug"), pieve, s.get("doyenne_contemporain_slug"), doyenne))
        s["pieve_slug"] = pieve
        s["doyenne_contemporain_slug"] = doyenne

# Verification
verde_after = [s for s in sites if s.get("pieve_slug") == "pieve_verde"]
carbini_after = [s for s in sites if s.get("pieve_slug") == "pieve_carbini"]
print("\npieve_verde: %d sites" % len(verde_after))
print("pieve_carbini: %d sites" % len(carbini_after))

# Write
pieves_data["pieves"] = pieves
with open(PIEVES_PATH, "w", encoding="utf-8") as f:
    json.dump(pieves_data, f, ensure_ascii=False, separators=(",", ":"))
print("\n%s written (%d bytes)" % (PIEVES_PATH, open(PIEVES_PATH, "rb").read().__len__()))

sites_data["sites"] = sites
with open(SITES_PATH, "w", encoding="utf-8") as f:
    json.dump(sites_data, f, ensure_ascii=False, separators=(",", ":"))
print("%s written (%d bytes)" % (SITES_PATH, open(SITES_PATH, "rb").read().__len__()))

# Sanity checks
pieve_slugs = {p["slug"] for p in pieves}
orphans = [s["slug"] for s in sites if s.get("pieve_slug") and s["pieve_slug"] not in pieve_slugs]
print("\nOrphans: %s" % orphans)
print("Done.")
