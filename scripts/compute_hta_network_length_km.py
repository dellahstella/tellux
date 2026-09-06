#!/usr/bin/env python3
"""
Compute the total length (km) of the Corsican HTA (medium-voltage, EDF SEI)
overhead line network actually ingested by Tellux — i.e. the live Supabase
`hta_lines` table that feeds calcMagneticELF_v2() (app.html), fetched exactly
as the app itself does (same endpoint, same public anon key already embedded
client-side — no secret involved).

Brief CH addendum (2026-09-06, revue Soleil PR #1290) : la landing page
(index.html, stat hero) affichait "8 000+ km lignes HTA/HTB" — l'unite
elle-meme etait fausse (8 387 est un compte de polylignes, pas des km) en plus
de l'inclusion erronee de HTB (non modelise, cf. brief CH). Ce script calcule
le chiffre en kilometres reellement defendable, pour remplacer le compte de
lignes par une grandeur qui communique quelque chose sur une landing, avec sa
methode consignee ici (doctrine anti-"dossier AD" : jamais de chiffre de mise
en avant sans provenance ecrite).

Method:
    Somme des distances Haversine entre points consecutifs de chaque
    polyligne du dataset. Rayon terrestre 6 371 000 m (sphere, pas
    l'ellipsoide WGS84 — a l'echelle de la Corse, l'ecart induit est trop
    petit pour affecter le chiffre affiche, deja arrondi a la centaine de km).

Requires:
    stdlib Python 3.10+ uniquement (json, math, urllib).

Source:
    Table Supabase `hta_lines` (endpoint public, cle anon deja exposee
    cote client dans app.html — SB_URL/SB_KEY, aucun secret). C'est le
    dataset REELLEMENT ingere par le calcul ELF, pas l'export brut EDF SEI
    d'origine (DATA/Tellux-Data/lignes-haute-tension-hta-aerien.csv,
    gitignore) : verifie a l'ecart entre les deux — l'export brut a une
    resolution de points superieure (27 488 pts, longueur brute 2 627,8 km)
    a celle du dataset importe en base (20 122 pts, 2 608,5 km) — la
    simplification a l'ingestion explique l'ecart (~0,75%). C'est le
    dataset ingere qui fait foi pour ce calcul, pas la source brute.

Result (recalcule en direct le 2026-09-06, cf. commit) :
    8 387 polylignes, 20 122 points, longueur totale = 2 608,5 km
    (moyenne 311.0 m/polyligne, mediane 172.1 m, max 4 737.6 m — aucune
    polyligne ne depasse 5 km, coherent avec un reseau de distribution HTA,
    pas des troncons de transport HTB longue distance)

Usage:
    python3 scripts/compute_hta_network_length_km.py
"""
import json
import math
import urllib.request

SB_URL = "https://knckulwghgfrxmbweada.supabase.co"
SB_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
    "ImtuY2t1bHdnaGdmcnhtYndlYWRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NTAxMzQs"
    "ImV4cCI6MjA4OTIyNjEzNH0.Cu9dvxFyn-5pbOP65gowCEQvRti74CLnlNYf92jebis"
)  # cle publique anon, deja exposee cote client dans app.html — pas un secret
EARTH_RADIUS_M = 6_371_000
PAGE = 1000


def fetch_all_rows():
    rows = []
    offset = 0
    while True:
        req = urllib.request.Request(
            SB_URL + "/rest/v1/hta_lines?select=pts&order=id",
            headers={
                "apikey": SB_KEY,
                "Authorization": "Bearer " + SB_KEY,
                "Range": f"{offset}-{offset + PAGE - 1}",
                "Range-Unit": "items",
                "Prefer": "count=exact",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            page = json.loads(resp.read())
        rows.extend(page)
        if len(page) < PAGE:
            break
        offset += PAGE
    return rows


def haversine_m(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(a))


def main():
    rows = fetch_all_rows()
    total_m = 0.0
    n_points = 0
    lengths_m = []
    for row in rows:
        pts = row["pts"]  # [[lat, lon], ...]
        n_points += len(pts)
        line_m = sum(
            haversine_m(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])
            for i in range(len(pts) - 1)
        )
        total_m += line_m
        lengths_m.append(line_m)

    lengths_m.sort()
    print(f"polylignes: {len(rows)}")
    print(f"points: {n_points}")
    print(f"longueur totale: {total_m / 1000:.1f} km")
    print(f"longueur moyenne: {total_m / len(rows):.1f} m")
    print(f"longueur mediane: {lengths_m[len(lengths_m) // 2]:.1f} m")
    print(f"longueur max: {lengths_m[-1]:.1f} m")


if __name__ == "__main__":
    main()
