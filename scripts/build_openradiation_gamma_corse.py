#!/usr/bin/env python3
"""Construit public/data/openradiation_gamma_corse.geojson depuis le jeu OpenRadiation (ODbL).

Streame le tarball open data OpenRadiation, filtre la bbox Corse, emet un GeoJSON leger
des mesures citoyennes de DEBIT DE DOSE gamma/X ambiant (tubes Geiger). GAMMA/X seulement,
JAMAIS radon. Couche d'AFFICHAGE : non injectee dans aucun calcul Tellux, ne recale ni le
modele ni les bornes gamma (NCRP-001 / GELE-001b intacts).

Repro : python scripts/build_openradiation_gamma_corse.py
Source : OpenRadiation (science citoyenne, ASNR co-fondatrice) - https://request.openradiation.net/download.html
Licence : ODbL. Attribution : « OpenRadiation contributors - ODbL ».
"""
import urllib.request, tarfile, csv, json, io, os

URL = "https://request.openradiation.net/openradiation_dataset.tar.gz"
MEMBER = "measurements_withoutEnclosedObject.csv"  # variante SANS blobs photo (parsing propre)
LAT_MIN, LAT_MAX, LON_MIN, LON_MAX = 41.3, 43.1, 8.4, 9.7  # bbox Corse
OUT = "public/data/openradiation_gamma_corse.geojson"
BUILT = "2026-07-09"  # horodatage fixe (pas de date dynamique)

csv.field_size_limit(10 ** 7)
feats = []
req = urllib.request.Request(URL, headers={"User-Agent": "tellux-build/1.0"})
with urllib.request.urlopen(req, timeout=600) as resp:
    with tarfile.open(fileobj=resp, mode="r|gz") as tar:
        for m in tar:
            if not m.name.endswith(MEMBER):
                continue
            raw = tar.extractfile(m)  # binaire ; streaming r|gz -> pas de TextIOWrapper (seekable() KO)
            rdr = csv.reader((ln.decode("utf-8", "replace") for ln in raw), delimiter=";")
            hdr = next(rdr)
            ix = {name: i for i, name in enumerate(hdr)}
            LAT, LON, VAL, ST, SENS, DEV = ix["latitude"], ix["longitude"], ix["value"], ix["startTime"], ix["apparatusSensorType"], ix["deviceModel"]
            for row in rdr:
                try:
                    la, lo = float(row[LAT]), float(row[LON])
                except (ValueError, IndexError):
                    continue
                if not (LAT_MIN <= la <= LAT_MAX and LON_MIN <= lo <= LON_MAX):
                    continue
                try:
                    v = round(float(row[VAL]), 4)
                except (ValueError, IndexError):
                    v = None
                feats.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [round(lo, 5), round(la, 5)]},
                    "properties": {
                        "v": v,                                   # debit de dose (uSv/h)
                        "d": (row[ST][:10] if ST < len(row) else ""),  # date YYYY-MM-DD
                        "s": (row[SENS] if SENS < len(row) else ""),   # type capteur
                        "m": (row[DEV] if DEV < len(row) else ""),     # modele appareil
                    },
                })
            break  # seul ce membre est necessaire

fc = {
    "type": "FeatureCollection",
    "metadata": {
        "source": "OpenRadiation (science citoyenne, ASNR co-fondatrice)",
        "license": "ODbL",
        "attribution": "OpenRadiation contributors - ODbL",
        "quantity": "debit de dose gamma/X ambiant (Geiger), uSv/h - PAS radon",
        "bbox_corse": [LON_MIN, LAT_MIN, LON_MAX, LAT_MAX],
        "n": len(feats),
        "built": BUILT,
        "epistemic": "Mesures citoyennes indicatives, capteurs heterogenes, non certifiees. "
                     "Le jeu inclut des traces continues (une session de marche vaut plusieurs "
                     "centaines de points) : densite affichee != nombre de sites de mesure.",
    },
    "features": feats,
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(fc, f, ensure_ascii=False)
print(f"[openradiation] {len(feats)} features -> {OUT}")
