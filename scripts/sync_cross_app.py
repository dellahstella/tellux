#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_cross_app.py - Sync coords/locks cross-app App (sites_app.json filter
type=site_em) <- Patrimoine (sites_patrimoine.json).

Adapte en M3 (sprint sites_app.json) : consomme desormais public/data/sites_app.json
(filter type=site_em) au lieu de l ancien docs/data/sites_em.json. Voir
docs/internal/AUDIT_COORDS_APP_2026-05-13.md pour le contexte de la migration.
Le fichier sites_em.json a ete supprime ; les 48 entrees site_em vivent dans
sites_app.json a cote des 8 site_uth et 5 source_thermale.

Pour chaque slug present dans sites_patrimoine.json ET sites_app.json (type=site_em),
verifie que les champs canoniques sont identiques. Si divergence, propage
depuis Patrimoine (source canon) vers les entrees site_em de sites_app.json.

Le champ `gps_cross_app_origin: "patrimoine"` est ajoute aux entrees synchronisees
(doctrine M3 : tracer la provenance de la coord pour audit ulterieur).

Champs synced (Patrimoine -> site_em dans sites_app.json) :
  - lat, lon
  - gps_locked, gps_lock_reason, gps_audit, gps_source
  - commune_nom (si present cote app)
  - cross_app.doyenne, cross_app.pieve (imbriques dans sites_app.json)

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
M3 update : Cowork (sprint sites_app.json, 2026-05-13)
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "docs" / "data"
PUBLIC_DATA_DIR = ROOT / "public" / "data"
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


def load_json_path(filename, dirs=None):
    """Charge un JSON et retourne (path, data) ou (None, None).

    M3 : `dirs` permet de specifier les emplacements candidates. Si None,
    defaut = [DATA_DIR] + WORKTREES (pour sites_patrimoine.json).
    Pour sites_app.json, passer dirs=[PUBLIC_DATA_DIR].
    """
    if dirs is None:
        dirs = [DATA_DIR] + WORKTREES
    for src in dirs:
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


def _get_app_field(em_entry, field):
    """M3 : recupere un champ d une entree site_em de sites_app.json.

    Les champs `doyenne_contemporain_slug` et `pieve_slug` cote patrimoine
    sont imbriques dans `cross_app.{doyenne, pieve}` cote sites_app.json.
    """
    if field == "doyenne_contemporain_slug":
        return (em_entry.get("cross_app") or {}).get("doyenne")
    if field == "pieve_slug":
        return (em_entry.get("cross_app") or {}).get("pieve")
    return em_entry.get(field)


def _set_app_field(em_entry, field, value):
    """M3 : ecrit un champ vers une entree site_em de sites_app.json.

    Mapping inverse de _get_app_field pour les champs cross_app.
    """
    if field == "doyenne_contemporain_slug":
        em_entry.setdefault("cross_app", {})
        em_entry["cross_app"]["doyenne"] = value
    elif field == "pieve_slug":
        em_entry.setdefault("cross_app", {})
        em_entry["cross_app"]["pieve"] = value
    else:
        em_entry[field] = value


def detect_divergences(patrim_sites, em_sites):
    """Retourne liste de (slug, em_site, diffs:dict champs->(em_val, patrim_val)).

    `em_sites` est ici la liste des entrees type=site_em filtree depuis
    sites_app.json.
    """
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
            e_val = _get_app_field(em, field)
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
    # M3 : sites_app.json remplace sites_em.json (public/data/, contient les 3
    # types fusionnes). On filtre type=site_em pour la sync cross-app.
    p_path, p_data = load_json_path("sites_patrimoine.json")
    e_path, e_data = load_json_path("sites_app.json", dirs=[PUBLIC_DATA_DIR])

    if not p_data or not e_data:
        print("ERROR : impossible de charger les JSON", file=sys.stderr)
        sys.exit(2)

    patrim_sites = p_data.get("sites", [])
    all_app_sites = e_data.get("sites", [])
    # M3 : ne syncer que les entrees site_em (les site_uth et source_thermale
    # n ont pas d homologue patrimoine).
    em_sites = [s for s in all_app_sites if s.get("type") == "site_em"]

    p_slugs = {s["slug"] for s in patrim_sites}
    e_slugs = {s["slug"] for s in em_sites}
    cross_app = sorted(p_slugs & e_slugs)

    divergences = detect_divergences(patrim_sites, em_sites)

    today = date.today().isoformat()
    lines = []
    lines.append("# Sync cross-app - " + today)
    lines.append("")
    lines.append("Mode : " + ("DRY-RUN" if args.dry_run else "APPLY"))
    lines.append("")
    lines.append("## Synthese")
    lines.append("")
    lines.append("- Sites Patrimoine : " + str(len(patrim_sites)))
    lines.append("- Sites site_em (depuis sites_app.json) : " + str(len(em_sites)))
    lines.append("- Cross-app : " + str(len(cross_app)))
    lines.append("- Divergences detectees : **" + str(len(divergences)) + "**")
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
        lines.append("### " + slug)
        lines.append("")
        for field, (e_val, p_val) in diffs.items():
            lines.append("  - `" + field + "` : app=`" + repr(e_val) + "` -> patrim=`" + repr(p_val) + "`")
        lines.append("")

    if args.apply:
        # Backup
        # M3 : nom de backup adapte pour refleter la cible sites_app.json.
        DRAFTS.mkdir(parents=True, exist_ok=True)
        backup_em = DRAFTS / ("sites_app.backup_sync_cross_app_" + today + ".json")
        with open(e_path, encoding="utf-8") as f:
            backup_em.write_text(f.read(), encoding="utf-8")

        p_by_slug = {s["slug"]: s for s in patrim_sites}
        n_synced = 0
        for slug, em, diffs in divergences:
            p = p_by_slug[slug]
            for field in diffs:
                _set_app_field(em, field, p.get(field))
            # M3 : tracer la provenance pour audit ulterieur.
            em["gps_cross_app_origin"] = "patrimoine"
            existing_notes = em.get("notes") or ""
            em["notes"] = (
                existing_notes + " | sync_cross_app " + today + " : " + str(len(diffs)) + " champ(s) sync depuis patrimoine."
            ).strip(" |")
            n_synced += 1

        # M3 : ecriture du sites_app.json complet (les site_em modifies sont
        # dans la meme liste racine que les site_uth et source_thermale qui
        # restent intacts).
        with open(e_path, "w", encoding="utf-8") as f:
            json.dump(e_data, f, ensure_ascii=False, indent=2)

        lines.append("## Apply")
        lines.append("")
        lines.append("- Backup : `" + str(backup_em.relative_to(ROOT)) + "`")
        lines.append("- Sites synces : " + str(n_synced) + " (type=site_em)")
        lines.append("- Patrimoine : non touche (canon source)")
        lines.append("- sites_app.json : ecrit sur `" + str(e_path.relative_to(ROOT)) + "`")
        lines.append("")

    output = "\n".join(lines)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print("Log : " + args.output, file=sys.stderr)
    else:
        print(output)

    sys.exit(1)  # divergences traitees ou detectees


if __name__ == "__main__":
    main()
