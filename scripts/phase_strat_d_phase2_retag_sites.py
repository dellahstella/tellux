"""
Phase 2 Strategie D retag sites.

Mapping INSEE -> sous-pieve pour sites avec commune_insee.
PIP fallback (lat/lon vs polygones nouveaux) pour sites sans commune_insee.

Doctrine BP-FIX-RATTACHEMENT-COMPLET-001 : pieve_slug + doyenne_contemporain_slug
retag en coherence.

Arbitrages Soleil 2026-05-18 :
- Q-2 : san_pietro_letia retag commune INSEE (sorroinsu->vico via commune Letia)
- Q-3 : tour_d_isolella_sette_navi conserve pieve_ornano (INSEE Renno mais
  geo cote sud Ajaccio, dette TOUR-ISOLELLA-INSEE-DISCORDANCE-001 commit suivant)
"""
import json
from shapely.geometry import Polygon, Point
from shapely.validation import make_valid

PATH_SITES = "docs/data/sites_patrimoine.json"
PATH_PIEVES = "docs/data/pieves_polygons.json"

# Mapping INSEE -> (pieve_slug, doyenne_slug)
INSEE_TO_TARGET = {}

# Vico splits
for insee in ["2A197","2A203","2A279","2A198","2A212","2A108","2A100"]:
    INSEE_TO_TARGET[insee] = ("pieve_piana", "doyenne_piana_vico_sari")
for insee in ["2A065","2A090"]:
    INSEE_TO_TARGET[insee] = ("pieve_sagone", "doyenne_piana_vico_sari")
for insee in ["2A154","2A028","2A348","2A019","2A258","2A141","2A174"]:
    INSEE_TO_TARGET[insee] = ("pieve_vico", "doyenne_piana_vico_sari")

# Balagne splits
for insee in ["2B199","2B034","2B332","2B180","2B223","2B136","2B182","2B097",
              "2B352","2B290","2B190","2B339","2B235","2B156"]:
    INSEE_TO_TARGET[insee] = ("pieve_ostriconi", "doyenne_balagne")
for insee in ["2B134","2B168","2B093","2B010","2B316","2B231","2B020","2B296",
              "2B138","2B084","2B025","2B175","2B112","2B173"]:
    INSEE_TO_TARGET[insee] = ("pieve_aregno", "doyenne_balagne")
for insee in ["2B050","2B150","2B165","2B361","2B167","2B049"]:
    INSEE_TO_TARGET[insee] = ("pieve_calenzana", "doyenne_balagne")

# Q-3 : sites a ne PAS retag par INSEE (anomalie INSEE vs geo)
SKIP_BY_INSEE = {"tour_d_isolella_sette_navi"}  # insee=2A258 Renno mais geo cote sud Ajaccio

# === Load ===
with open(PATH_SITES, encoding="utf-8") as f:
    d = json.load(f)
with open(PATH_PIEVES, encoding="utf-8") as f:
    pp = json.load(f)

# Polygones pour PIP fallback
def to_shp(poly_ll):
    return make_valid(Polygon([(lo, la) for la, lo in poly_ll]))
pv_polys = {p["slug"]: to_shp(p["polygon"]) for p in pp["pieves"] if p.get("polygon")}
pv_doy = {p["slug"]: p.get("doyenne_contemporain_majoritaire") for p in pp["pieves"]}

# Sites a retag (concernés par Phase 2)
# 1. Sites avec pieve_slug in (vico, balagne, sorroinsu, cinarca) actuels
# 2. Sites avec commune INSEE migrée (incluant celle taggée ailleurs comme san_pietro_letia)
OLD_PIEVES_SCOPE = {"pieve_vico", "pieve_balagne", "pieve_sorroinsu", "pieve_cinarca"}

modifs = 0
nops = 0
pip_fallback = 0
ghost_letia = 0
skipped = 0

for s in d["sites"]:
    if s["slug"] in SKIP_BY_INSEE:
        skipped += 1
        print(f"  SKIP  {s['slug']:45s} (Q-3 INSEE anomalie, conserve {s.get('pieve_slug')}/{s.get('doyenne_contemporain_slug')})")
        continue

    insee = s.get("commune_insee")
    cur_pv = s.get("pieve_slug")

    # Cas 1 : INSEE dans mapping
    if insee in INSEE_TO_TARGET:
        new_pv, new_doy = INSEE_TO_TARGET[insee]
        old_doy = s.get("doyenne_contemporain_slug")
        if cur_pv == new_pv and old_doy == new_doy:
            nops += 1
        else:
            s["pieve_slug"] = new_pv
            s["doyenne_contemporain_slug"] = new_doy
            modifs += 1
            print(f"  RETAG {s['slug']:45s} insee={insee} {cur_pv}/{old_doy} -> {new_pv}/{new_doy}")
            if s["slug"] == "san_pietro_letia":
                ghost_letia += 1
        continue

    # Cas 2 : pas d'INSEE mappé mais pieve_slug dans scope -> PIP fallback
    if cur_pv in OLD_PIEVES_SCOPE:
        if cur_pv == "pieve_sorroinsu" or cur_pv == "pieve_cinarca":
            # Reste sur cette pieve si pas concerné par migration (INSEE non mappé)
            continue
        # Pour pieve_vico / pieve_balagne actuel : PIP fallback vers nouvelle pieve
        lat = s.get("lat"); lon = s.get("lon")
        if lat is None or lon is None:
            continue
        pt = Point(lon, lat)
        candidates = [k for k in ("pieve_piana", "pieve_sagone", "pieve_vico",
                                  "pieve_ostriconi", "pieve_aregno", "pieve_calenzana")
                      if pv_polys.get(k) and pv_polys[k].contains(pt)]
        if candidates:
            new_pv = candidates[0]
            new_doy = pv_doy.get(new_pv)
            old_doy = s.get("doyenne_contemporain_slug")
            if cur_pv != new_pv or old_doy != new_doy:
                s["pieve_slug"] = new_pv
                s["doyenne_contemporain_slug"] = new_doy
                modifs += 1
                pip_fallback += 1
                print(f"  PIP   {s['slug']:45s} ({lat},{lon}) {cur_pv}/{old_doy} -> {new_pv}/{new_doy}")
        else:
            # PIP echec : forcer un fallback selon ancien pieve (probablement orphan)
            if cur_pv == "pieve_vico":
                new_pv = "pieve_vico"  # garde
                new_doy = "doyenne_piana_vico_sari"
            elif cur_pv == "pieve_balagne":
                new_pv = "pieve_aregno"  # default rename
                new_doy = "doyenne_balagne"
            old_doy = s.get("doyenne_contemporain_slug")
            s["pieve_slug"] = new_pv
            s["doyenne_contemporain_slug"] = new_doy
            modifs += 1
            print(f"  FBCK  {s['slug']:45s} ({lat},{lon}) {cur_pv}/{old_doy} -> {new_pv}/{new_doy} (PIP fail, default fallback)")

print(f"\nTotal: {modifs} modifs + {nops} no-op + {pip_fallback} PIP + {skipped} skip")
print(f"san_pietro_letia retag confirme (Q-2): {ghost_letia}")

# === Save ===
with open(PATH_SITES, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
import os
print(f"{PATH_SITES}: {os.path.getsize(PATH_SITES)} B")

# === Anti-ghost validation ===
declared = {p["slug"] for p in pp["pieves"]}
ghosts = [s["slug"] for s in d["sites"] if s.get("pieve_slug") and s["pieve_slug"] not in declared]
assert not ghosts, f"GHOSTS: {ghosts}"
print("Ghosts: 0")

# Compteurs par pieve cible
from collections import Counter
c = Counter(s.get("pieve_slug") for s in d["sites"])
print("\nCompteurs sites par pieve cible :")
for sl in ("pieve_piana", "pieve_sagone", "pieve_vico", "pieve_ostriconi",
           "pieve_aregno", "pieve_calenzana", "pieve_sorroinsu", "pieve_cinarca",
           "pieve_balagne"):
    print(f"  {sl:25s}: {c.get(sl, 0)}")
