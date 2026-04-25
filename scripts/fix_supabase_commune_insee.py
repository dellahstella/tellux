#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_supabase_commune_insee.py
==============================
Fix ticket SUPABASE-COMMUNE-FIELD-001.

Calcule `code_insee_commune` pour chaque antenne de la table Supabase
`antennas_corse` via point-in-polygon contre les contours communaux
`geo.api.gouv.fr` (IGN AdminExpress), puis `UPDATE` la colonne
`code_insee_commune` preablement creee par la migration
`antennas_corse_add_code_insee_commune` (2026-04-24).

Le champ `commune` historique (pollue) est conserve pour tracabilite.
La colonne `code_insee_commune` devient la source de verite.

Prerequis :
  1. Colonne `code_insee_commune TEXT` existante sur `antennas_corse`.
  2. Variables d'environnement :
       - SUPABASE_URL            : URL du projet Supabase
       - SUPABASE_SERVICE_ROLE_KEY : cle service_role (non committee)
     Ou bien fichier `.env` local avec ces memes variables.

Usage :
    python scripts/fix_supabase_commune_insee.py --dry-run
    python scripts/fix_supabase_commune_insee.py --apply
    python scripts/fix_supabase_commune_insee.py --apply --batch 100

Sorties :
    stdout : logs de progression, resume par batch
    code retour : 0 si OK, 1 si point d'arret atteint

ALERTE : ce script modifie la table `antennas_corse` en production.
Toujours faire un dump prealable dans `_backups/` et executer avec
`--dry-run` avant le mode `--apply`.

Version : 1.0
Date    : 2026-04-24
Auteur  : session Claude Code fix SUPABASE-COMMUNE-FIELD-001
Licence donnees : Etalab 2.0 (contours IGN AdminExpress via geo.api.gouv.fr)
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
import urllib.request
from urllib.error import HTTPError

try:
    from shapely.geometry import shape, Point
    from shapely.prepared import prep
except ImportError:
    sys.exit("ERREUR : shapely requis. Installer avec : pip install shapely")


LOG = logging.getLogger("fix_supabase_commune_insee")

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

GEO_API = "https://geo.api.gouv.fr/communes"

# Clef anon publique (lecture seule, RLS) : permet les SELECT pour verification.
# Pour les UPDATE, SUPABASE_SERVICE_ROLE_KEY est requise.
SB_URL_PUBLIC = "https://knckulwghgfrxmbweada.supabase.co"
SB_KEY_ANON = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtu"
    "Y2t1bHdnaGdmcnhtYndlYWRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NTAxMzQsImV4cCI6"
    "MjA4OTIyNjEzNH0.Cu9dvxFyn-5pbOP65gowCEQvRti74CLnlNYf92jebis"
)


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _sb_url() -> str:
    return os.environ.get("SUPABASE_URL", SB_URL_PUBLIC).rstrip("/")


def _sb_anon_key() -> str:
    return os.environ.get("SUPABASE_ANON_KEY", SB_KEY_ANON)


def _sb_service_key() -> str:
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not key:
        sys.exit(
            "ERREUR : variable d'environnement SUPABASE_SERVICE_ROLE_KEY requise "
            "pour le mode --apply. La recuperer depuis le dashboard Supabase, "
            "rubrique Project Settings > API > service_role key. Ne pas "
            "committer cette cle."
        )
    return key


def http_json(url: str, method: str = "GET", headers: dict | None = None,
              body: dict | list | None = None, timeout: int = 30):
    req = urllib.request.Request(url, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        if "Content-Type" not in (headers or {}):
            req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, data=data, timeout=timeout) as r:
            raw = r.read()
            if not raw:
                return None
            return json.loads(raw)
    except HTTPError as e:
        body_err = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} sur {url} : {body_err}") from None


# ---------------------------------------------------------------------------
# Point-in-polygon (reutilise la logique de build_antennes_par_commune_corse.py)
# ---------------------------------------------------------------------------

def fetch_polygons() -> list[dict]:
    LOG.info("Telechargement des contours communaux Corse (2A + 2B)...")
    features = []
    for dep in ("2A", "2B"):
        url = (
            f"{GEO_API}?codeDepartement={dep}"
            f"&fields=nom,code,contour&format=geojson&geometry=contour"
        )
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read())
        features.extend(data.get("features", []))
    LOG.info("  %d polygones recus", len(features))
    polygons = []
    for feat in features:
        props = feat["properties"]
        geom = shape(feat["geometry"])
        polygons.append({
            "code": props["code"],
            "nom": props["nom"],
            "prepared": prep(geom),
            "bbox": geom.bounds,
        })
    return polygons


def assign_insee(lat: float, lon: float, polygons: list[dict]) -> str | None:
    pt = Point(lon, lat)
    for poly in polygons:
        minx, miny, maxx, maxy = poly["bbox"]
        if lon < minx or lon > maxx or lat < miny or lat > maxy:
            continue
        if poly["prepared"].contains(pt):
            return poly["code"]
    return None


# ---------------------------------------------------------------------------
# Supabase IO
# ---------------------------------------------------------------------------

def fetch_antennas() -> list[dict]:
    """Charge id, lat, lon de toutes les antennes via cle anon."""
    LOG.info("Chargement des antennes depuis antennas_corse...")
    sb_url = _sb_url()
    key = _sb_anon_key()
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}
    rows = []
    page = 0
    while True:
        url = (
            f"{sb_url}/rest/v1/antennas_corse"
            f"?select=id,lat,lon,commune,code_insee_commune"
            f"&order=id.asc&offset={page*1000}&limit=1000"
        )
        batch = http_json(url, headers=headers, timeout=30)
        if not batch:
            break
        rows.extend(batch)
        if len(batch) < 1000:
            break
        page += 1
    LOG.info("  %d antennes chargees", len(rows))
    return rows


def update_batch(updates: list[dict], service_key: str) -> int:
    """UPDATE PostgREST bulk par id via upsert-on-conflict.

    updates : liste de dicts {id, code_insee_commune} (peut etre None).
    Retourne le nombre de lignes effectivement mises a jour.
    """
    sb_url = _sb_url()
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation,resolution=merge-duplicates",
    }
    url = f"{sb_url}/rest/v1/antennas_corse?on_conflict=id"
    result = http_json(url, method="POST", headers=headers, body=updates, timeout=60)
    return len(result) if isinstance(result, list) else 0


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def run(dry_run: bool, batch_size: int):
    polygons = fetch_polygons()
    rows = fetch_antennas()

    if len(rows) < 2900:
        LOG.error("Nombre d'antennes (%d) tres bas, probable probleme. ABORT.", len(rows))
        return 1

    # Calcul INSEE pour toutes les antennes
    LOG.info("Point-in-polygon sur %d antennes...", len(rows))
    t0 = time.time()
    computed = []
    n_null = 0
    for r in rows:
        code = assign_insee(r["lat"], r["lon"], polygons)
        computed.append({"id": r["id"], "code_insee_commune": code, "current": r.get("code_insee_commune")})
        if code is None:
            n_null += 1
    dt = time.time() - t0

    n_placed = len(computed) - n_null
    distinct = len({c["code_insee_commune"] for c in computed if c["code_insee_commune"]})
    LOG.info("  Termine en %.1fs : %d places, %d NULL, %d codes INSEE distincts",
             dt, n_placed, n_null, distinct)

    # Points d'arret de securite
    if n_null > 30:
        LOG.error("Trop de NULL (%d > 30), probable regression. ABORT.", n_null)
        return 1
    if distinct < 200:
        LOG.error("Trop peu de codes INSEE distincts (%d < 200), probable regression. ABORT.",
                  distinct)
        return 1

    # Top 5 communes de validation
    from collections import Counter
    top = Counter(c["code_insee_commune"] for c in computed if c["code_insee_commune"])
    LOG.info("Top 5 communes :")
    for code, n in top.most_common(5):
        LOG.info("  %s : %d antennes", code, n)

    if dry_run:
        LOG.info("=== DRY RUN : aucun UPDATE effectue ===")
        return 0

    # Batched UPDATE via PostgREST upsert
    service_key = _sb_service_key()
    LOG.info("UPDATE en cours par batches de %d...", batch_size)
    t0 = time.time()
    total_updated = 0
    for i in range(0, len(computed), batch_size):
        batch = [
            {"id": c["id"], "code_insee_commune": c["code_insee_commune"]}
            for c in computed[i:i+batch_size]
        ]
        try:
            n = update_batch(batch, service_key)
        except RuntimeError as exc:
            LOG.error("ECHEC batch %d (%d elements) : %s", i, len(batch), exc)
            LOG.error("Stop. %d lignes deja mises a jour. Rollback non auto (upsert).", total_updated)
            return 1
        total_updated += n
        if (i // batch_size) % 5 == 0:
            LOG.info("  Batch %d-%d : +%d (%.1fs cumule)",
                     i, i + batch_size, n, time.time() - t0)

    dt = time.time() - t0
    LOG.info("UPDATE termine : %d lignes en %.1fs", total_updated, dt)

    if total_updated != len(computed):
        LOG.warning("UPDATE incoherent : %d envoyes, %d retournes", len(computed), total_updated)

    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true",
                       help="Calcule mais n'UPDATE pas. Aucune modification en base.")
    group.add_argument("--apply", action="store_true",
                       help="UPDATE en base. Necessite SUPABASE_SERVICE_ROLE_KEY.")
    parser.add_argument("--batch", type=int, default=500,
                        help="Taille de batch pour les UPDATE (defaut : 500)")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )

    return run(dry_run=args.dry_run, batch_size=args.batch)


if __name__ == "__main__":
    sys.exit(main())
