#!/usr/bin/env python3
"""
Fetch INTERMAGNET observatory data (BGS GIN, Edinburgh) for the Corse app's
external geomagnetic correction (niveau 1 de la hierarchie ELF, cf. app.html
calcExternalCorr()) and write a small static JSON consumed same-origin by the
client (no CORS: the real GIN endpoint sends no Access-Control-Allow-Origin
header, verified 2026-08-26 during PR #1033 — a browser fetch() is blocked
regardless of the station queried).

Architecture (brief "implementation 3 chantiers orphelins", 2026-08-26,
chantier A/E) : job batch planifie (GitHub Actions cron) plutot qu'un proxy
serveur — plus simple, plus robuste si BGS GIN est indisponible ponctuellement
(le dernier fichier reste utilisable au lieu de casser une requete live).

Stations (memes que le chantier SECS de la meme session, par distance Corse
croissante) : DUR (Duronia, Italie, 470km) > EBR (Ebro, Espagne, 733km) >
CLF (Chambon-la-Foret, France, 845km). AQU (L'Aquila) et CTS (Castello
Tesino) retires : confirmes morts / jamais reconnus par ce GIN (cf. PR #1033).

API reelle (verifiee en direct, pas l'ancien endpoint mort geomag.bgs.ac.uk) :
    https://imag-data.bgs.ac.uk/GIN_V1/GINServices
    ?Request=GetData&observatoryIagaCode=<code>&dataDuration=30
    &samplesPerDay=Minute&publicationState=reported&Format=json
Reponse en colonnes paralleles {datetime:[...], S:[...], D:[...], H:[...],
Z:[...]} — S = composante scalaire totale (orientation HDZS), equivalent du F
habituel (IAGA).

Sortie : public/data/intermagnet_latest.json
    {
      "generated_at": "2026-08-26T14:30:00+00:00",
      "station_used": "DUR" | null,
      "delta_nT": <float> | null,
      "baseline_30j_nT": <float> | null,
      "n_samples": <int> | null,
      "attempts": [{"code": "DUR", "status": "ok"|"no_data"|"error", "detail": "..."}]
    }

Usage :
    python3 scripts/fetch_intermagnet.py

Dependances runtime : stdlib Python uniquement (urllib.request, json,
datetime, statistics, pathlib) — pas de pip install (meme convention que
refresh-antennes.yml : stdlib prefere quand suffisant).
"""

import json
import math
import statistics
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path

GIN_BASE = "https://imag-data.bgs.ac.uk/GIN_V1/GINServices"
TIMEOUT_S = 15

# Dst horaire (Kyoto WDC redistribue par NOAA SWPC) — MEME endpoint que celui lu par
# loadDst() dans app.html, donc meme donnee que le niveau 2 de la cascade.
NOAA_DST_URL = "https://services.swpc.noaa.gov/products/kyoto-dst.json"

# Memes stations, meme ordre que INTERMAGNET_OBSERVATORIES dans app.html (PR #1033).
OBSERVATORIES = ["DUR", "EBR", "CLF"]

OUT_PATH = Path("public/data/intermagnet_latest.json")


def fetch_station(code, duration_days=30):
    """Retourne (delta_nT, baseline_nT, n_samples) ou (None, None, None) si indisponible."""
    # dataStartDate EXPLICITE obligatoire : par defaut (parametre omis) l'API prend
    # "hier" comme depart et dataDuration comme nombre de jours vers l'AVENIR, pas
    # vers le passe — bug trouve en testant ce script (verifie en direct : sans
    # dataStartDate, une requete dataDuration=30 a renvoye une fenetre 25/08→23/09,
    # majoritairement future et donc vide). Meme bug present dans PR #1033 (app.html),
    # corrige dans la meme PR que ce script puisqu'il la remplace de toute facon.
    start_date = (datetime.now(timezone.utc) - timedelta(days=duration_days)).strftime("%Y-%m-%d")
    url = (
        f"{GIN_BASE}?Request=GetData&observatoryIagaCode={code}"
        f"&dataStartDate={start_date}&dataDuration={duration_days}&samplesPerDay=Minute"
        f"&publicationState=reported&Format=json"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Tellux-fetch-intermagnet/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    times = data.get("datetime")
    scalar_f = data.get("S")
    if not times or not scalar_f or len(times) != len(scalar_f):
        return None, None, None, "reponse sans donnees exploitables (datetime/S absents ou desalignes)"

    # La fenetre demandee (dataDuration jours passes) inclut souvent des jours SANS
    # donnee (lag de publication, cf. commentaire module) : la reponse contient alors
    # des null en fin de serie pour les jours les plus recents. On ne peut donc pas
    # prendre bêtement scalar_f[-1] comme "dernier echantillon" — il faut le dernier
    # echantillon REELLEMENT valide (non-null), meme s'il date de plusieurs jours.
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=duration_days)
    recent = []
    last_valid = None
    for t_str, f_val in zip(times, scalar_f):
        try:
            t = datetime.fromisoformat(t_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        if f_val is None:
            continue
        try:
            f = float(f_val)
        except (ValueError, TypeError):
            continue
        if f != f:  # NaN
            continue
        if t >= cutoff:
            recent.append(f)
            last_valid = f

    if len(recent) < 24:
        return None, None, None, f"seulement {len(recent)} echantillons recents valides (<24 requis)"

    recent_sorted = sorted(recent)
    median = recent_sorted[len(recent_sorted) // 2]
    delta = round(last_valid - median, 1)
    return delta, round(median, 1), len(recent), "ok"


def fetch_dst():
    """Dernier Dst horaire publie. Retourne (dst_nT, time_tag, detail).

    POURQUOI CETTE FONCTION EXISTE — et pourquoi elle n'alimente AUCUN calcul.

    `calcExternalCorr()` (app.html) est une cascade a trois niveaux : INTERMAGNET,
    puis Dst, puis Kp. Quand le fichier ecrit ici depasse le seuil de peremption, le
    client descend au niveau 2. On sait donc, a posteriori, quelle valeur INTERMAGNET
    aurait donnee — elle est dans ce fichier — mais on ne sait PAS quelle valeur Dst
    la remplacait au meme instant : elle n'a jamais ete conservee nulle part.

    Consequence, etablie par le constat CM (2026-09-08) : l'ecart mesure entre les deux
    niveaux (21 nT a un instant) ne vaut que pour cet instant. En regime calme il reste
    tres sous l'incertitude declaree du champ statique (+/-100 nT) ; en tempete, les
    niveaux 2 et 3 ne sont pas bornes vers le haut et l'ecart pourrait la depasser. Les
    treize jours observes ne contiennent pas de tempete, donc ils ne tranchent pas ce
    cas — et sans serie appariee, aucune observation future ne le tranchera non plus.

    Enregistrer Dst A COTE de delta_nT, au meme instant, construit cette serie appariee.
    C'est tout ce que fait cette fonction : elle prepare une comparaison, elle n'en tire
    aucune conclusion et le client ne lit pas ce champ.

    AUCUNE EXCEPTION NE REMONTE. Ce terme est observationnel ; le fichier qu'il
    accompagne, lui, alimente un calcul public. Une panne NOAA ne doit jamais pouvoir
    empecher l'ecriture du delta INTERMAGNET — ce serait faire dependre le niveau 1
    d'une source du niveau 2, exactement l'inverse de la hierarchie.
    """
    try:
        req = urllib.request.Request(NOAA_DST_URL, headers={"User-Agent": "Tellux-fetch-intermagnet/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:  # noqa: BLE001 — voir docstring : aucune exception ne remonte
        return None, None, f"error: {type(e).__name__}: {e}"

    if not isinstance(data, list) or not data:
        return None, None, "reponse vide ou format inattendu"

    last = data[-1]
    # Deux formats supportes, comme loadDst() cote client : objets {dst, time_tag}
    # (format servi au 2026-09-08, verifie en direct) et tableaux [time_tag, dst]
    # avec en-tetes en ligne 0 (format historique NOAA). Meme tolerance des deux cotes.
    try:
        if isinstance(last, dict) and "dst" in last:
            return float(last["dst"]), last.get("time_tag") or last.get("time-tag"), "ok"
        if isinstance(last, list) and len(last) >= 2 and len(data) >= 2:
            return float(last[1]), last[0], "ok (format tableau historique)"
    except (TypeError, ValueError) as e:
        return None, None, f"valeur illisible: {e}"
    return None, None, "dernier element ni objet {dst} ni tableau [time_tag, dst]"


def main():
    attempts = []
    station_used = None
    delta_nT = None
    baseline_nT = None
    n_samples = None

    for code in OBSERVATORIES:
        try:
            delta, baseline, n, detail = fetch_station(code)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
            attempts.append({"code": code, "status": "error", "detail": str(e)})
            continue
        if delta is None:
            attempts.append({"code": code, "status": "no_data", "detail": detail})
            continue
        attempts.append({"code": code, "status": "ok", "detail": detail})
        station_used, delta_nT, baseline_nT, n_samples = code, delta, baseline, n
        break  # premiere station exploitable = succes, meme logique que loadINTERMAGNETObservatory()

    # Releve au meme instant que delta_nT, cf. docstring de fetch_dst(). Champs
    # OBSERVATIONNELS : aucune surface ne les lit, aucun calcul ne les consomme.
    dst_nT, dst_time_tag, dst_detail = fetch_dst()

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "station_used": station_used,
        "delta_nT": delta_nT,
        "baseline_30j_nT": baseline_nT,
        "n_samples": n_samples,
        "attempts": attempts,
        "source": "BGS GIN Edinburgh (imag-data.bgs.ac.uk/GIN_V1) — observatoires DUR/EBR/CLF",
        # ── Temoin apparie niveau 2, ajoute le 2026-09-08 (constat CM) ──────────────
        # NON LU PAR L'APPLICATION. Sert a constituer la serie qui permettra un jour de
        # comparer le niveau 1 (delta_nT ci-dessus) au niveau 2 qui le remplace quand il
        # perime — la comparaison qui manque pour trancher le cas tempete. `dst_corr_nT`
        # reproduit la formule du client (Math.round(curDst * 0.42), calcDstCorrection())
        # pour que la comparaison porte sur deux corrections et non sur une correction et
        # un indice brut ; elle est RECOPIEE ici, pas partagee : si la formule du client
        # change un jour, ce champ devient faux et doit etre reajuste a la main.
        #
        # math.floor(x + 0.5) et NON round(x) : `round` de Python arrondit au pair le plus
        # proche (round(10.5) == 10), `Math.round` de JS arrondit vers +inf (11). Dst etant
        # entier, le produit tombe sur un demi exact pour dst = 25, 75, -25… — rare, mais
        # une divergence d'1 nT dans le champ dont le SEUL role est de servir de terme de
        # comparaison viderait ce champ de son sens. floor(x + 0.5) reproduit Math.round
        # exactement, negatifs compris (floor(-10.5 + 0.5) == -10 == Math.round(-10.5)).
        "dst_nT": dst_nT,
        "dst_time_tag": dst_time_tag,
        "dst_status": dst_detail,
        "dst_corr_nT": None if dst_nT is None else math.floor(dst_nT * 0.42 + 0.5),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    if station_used:
        print(f"OK: station={station_used} delta={delta_nT}nT baseline={baseline_nT}nT n={n_samples}", flush=True)
    else:
        print("Aucune station INTERMAGNET exploitable ce cycle — fichier ecrit avec station_used=null "
              "(le client retombera sur Dst/Kp, comportement inchange).", flush=True)
        for a in attempts:
            print(f"  {a['code']}: {a['status']} — {a['detail']}", flush=True)


if __name__ == "__main__":
    main()
