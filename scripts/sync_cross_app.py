#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_cross_app.py - Sync coords/locks cross-app EM <- Patrimoine.

Pour chaque slug present dans sites_patrimoine.json ET sites_em.json,
verifie que les champs canoniques sont identiques. Si divergence, propage
depuis Patrimoine (source canon) vers EM.

Champs synced (Patrimoine -> EM) :
  - lat, lon
  - gps_locked, gps_lock_reason, gps_audit, gps_source
  - commune_nom (si present cote em)
  - doyenne_contemporain_slug
  - pieve_slug

Champs NOT synced (propres a chaque fichier) :
  - axe_corpus / axe_em
  - categorie / categorie_em
  - description / description_em
  - sources_originales (peuvent diverger)
  - signal_em + autres champs EM-specifiques
  - phase_publication, couleur, priorite (Patrimoine-specifiques)
  - fiche_v3_slug

Usage :
  python scripts/sync_cross_app.py --dry-run
  python scripts/sync_cross_app.py --apply
  python scripts/sync_cross_app.py --apply --output _drafts/sync_log.md

EXIT CODES :
  0 - Aucune divergence (deja sync)
  1 - Divergences detectees (en dry-run) ou syncees (en apply)
  2 - Erreur (JSON invalide)

Author : Cowork (Brief 39decies suite, 2026-05-07)
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "docs" / "data"
WORKTREES = [
    ROOT / ".claude" / "worktrees" / "distracted-cohen-9850e9" / "docs" / "data",
    ROOT / ".claude" / "worktrees" / "inspiring-snyder-b363e6" / "docs" / "data",
]
DRAFTS = ROOT / "_drafts"

SYNCED_FIELDS = [
    "lat", "lon",
    "gps_locked", "gps_lock_reason", "gps_audit", "gps_source",
    "commune_nom",
    "doyenne_contemporain_slug", "pieve_slug",
]


def load_json_path(filename):
    """Charge un JSON et retourne (path, data) ou (None, None)."""
    for src in [DATA_DIR] + WORKTREES:
        path = src / filename
        if not path.exists():
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return path, data
        except json.JSONDecodeError as e:
            print(f"ERROR JSON invalide {path} : {e}", file=sys.stderr)
            return path, None
    return None, None


def coord_diff(a, b):
    if a is None or b is None:
        return float("inf") if (a is None) != (b is None) else 0
    return abs(a - b)


def detect_divergences(patrim_sites, em_sites):
    """Retourne liste de (slug, em_site, diffs:dict champs->(em_val, patrim_val))."""
    p_by_slug = {s["slug"]: s for s in patrim_sites}
    divergences = []
    for em in em_sites:
        slug = em.get("slug")
        if slug not in p_by_slug:
            continue
        p = p_by_slug[slug]
        diffs = {}
        for field in SYNCED_FIELDS:
            p_val = p.get(field)
            e_val = em.get(field)
            # Special case for lat/lon : tolerance numerique
            if field in ("lat", "lon"):
                if coord_diff(p_val, e_val) > 0.0001:
                    diffs[field] = (e_val, p_val)
            else:
                if p_val != e_val:
                    # Skip si patrim n'a pas la donnee mais em oui (em peut avoir des champs propres)
                    if p_val is None and e_val is not None:
                        continue
                    diffs[field] = (e_val, p_val)
        if diffs:
            divergences.append((slug, em, diffs))
    return divergences


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    parser.add_argument("--output", help="Path markdown log (sinon stdout)")
    args = parser.parse_args()

    # Charger les 2 JSON
    p_path, p_data = load_json_path("sites_patrimoine.json")
    e_path, e_data = load_json_path("sites_em.json")

    if not p_data or not e_data:
        print("ERROR : impossible de charger les JSON", file=sys.stderr)
        sys.exit(2)

    patrim_sites = p_data.get("sites", [])
    em_sites = e_data.get("sites", [])

    p_slugs = {s["slug"] for s in patrim_sites}
    e_slugs = {s["slug"] for s in em_sites}
    cross_app = sorted(p_slugs & e_slugs)

    divergences = detect_divergences(patrim_sites, em_sites)

    today = date.today().isoformat()
    lines = []
    lines.append(f"# Sync cross-app - {today}")
    lines.append("")
    lines.append(f"Mode : {'DRY-RUN' if args.dry_run else 'APPLY'}")
    lines.append("")
    lines.append("## Synthese")
    lines.append("")
    lines.append(f"- Sites Patrimoine : {len(patrim_sites)}")
    lines.append(f"- Sites EM : {len(em_sites)}")
    lines.append(f"- Cross-app : {len(cross_app)}")
    lines.append(f"- Divergences detectees : **{len(divergences)}**")
    lines.append("")

    if not divergences:
        lines.append("Status : OK (aucune divergence, tout sync)")
        output = "\n".join(lines)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
        else:
            print(output)
        sys.exit(0)

    lines.append("## Divergences")
    lines.append("")
    for slug, em, diffs in divergences:
        lines.append(f"### {slug}")
        lines.append("")
        for field, (e_val, p_val) in diffs.items():
            lines.append(f"  - `{field}` : em=`{e_val}` -> patrim=`{p_val}`")
        lines.append("")

    if args.apply:
        # Backup
        DRAFTS.mkdir(parents=True, exist_ok=True)
        backup_em = DRAFTS / f"sites_em.backup_sync_cross_app_{today}.json"
        with open(e_path, encoding="utf-8") as f:
            backup_em.write_text(f.read(), encoding="utf-8")

        em_by_slug = {s["slug"]: s for s in em_sites}
        p_by_slug = {s["slug"]: s for s in patrim_sites}
        n_synced = 0
        for slug, em, diffs in divergences:
            p = p_by_slug[slug]
            for field in diffs:
                em[field] = p.get(field)
            existing_notes = em.get("notes") or ""
            em["notes"] = (
                existing_notes + f" | sync_cross_app {today} : {len(diffs)} champ(s) sync depuis patrimoine."
            ).strip(" |")
            n_synced += 1

        with open(e_path, "w", encoding="utf-8") as f:
            json.dump(e_data, f, ensure_ascii=False, indent=2)

        lines.append(f"## Apply")
        lines.append("")
        lines.append(f"- Backup : `{backup_em.relative_to(ROOT)}`")
        lines.append(f"- Sites synces : {n_synced}")
        lines.append(f"- Patrimoine : non touche (canon source)")
        lines.append(f"- EM : ecrit sur `{e_path.relative_to(ROOT)}`")
        lines.append("")

    output = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Log : {args.output}", file=sys.stderr)
    else:
        print(output)

    sys.exit(1)  # divergences traitees ou detectees


if __name__ == "__main__":
    main()
