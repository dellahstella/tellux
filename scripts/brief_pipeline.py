#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brief_pipeline.py - Pipeline d'automatisation des briefs corrections GPS.

Parse un brief Soleil (markdown), applique les corrections data,
genere rapport + manifest + commande git prete a coller pour Code.

Usage :
  python scripts/brief_pipeline.py --input _drafts/brief_NNN_input.md --brief-id NNN --dry-run
  python scripts/brief_pipeline.py --input _drafts/brief_NNN_input.md --brief-id NNN --apply

SORTIES en mode --apply :
  - JSON modifies dans worktree distracted-cohen ou DATA_DIR
  - _drafts/sites_*.backup_brief_<NNN>_<DATE>.json
  - fiches_patrimoine/RAPPORT_SESSION_BRIEF_<NNN>.md
  - _drafts/cowork_manifest_brief_<NNN>.txt (Q3 : manifest pour Code)
  - Commande git imprimee a coller a Code

Author : Cowork (Q3 patch 2026-05-07)
"""

import argparse
import json
import math
import re
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
RAPPORTS = ROOT / "fiches_patrimoine"

STOPWORDS = {
    "slug", "note", "coord", "coords", "lat", "lon", "valeur", "valeurs",
    "ecart", "remarque", "commune", "source", "sources", "axe", "auteur",
    "decision", "soleil", "brief", "sites", "patrimoine", "garder", "ecraser",
    "campile", "haute", "corse", "extreme", "decision", "garde",
}


def load_json_with_fallback(filename, key):
    for src in [DATA_DIR] + WORKTREES:
        path = src / filename
        if not path.exists():
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            return path, data, data.get(key, [])
        except json.JSONDecodeError:
            continue
    return None, None, []


def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def point_in_ring(lat, lon, ring):
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        yi, xi = ring[i][0], ring[i][1]
        yj, xj = ring[j][0], ring[j][1]
        denom = yj - yi
        if denom == 0:
            denom = 1e-12
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / denom + xi):
            inside = not inside
        j = i
    return inside


def reverse_geocode(lat, lon, polygons):
    for entry in polygons:
        polygon = entry.get("polygon")
        if polygon and point_in_ring(lat, lon, polygon):
            return entry["slug"]
    return None


def parse_brief_markdown(text):
    corrections = []
    lines = text.splitlines()
    row_pattern = re.compile(r"^\s*\|(.+)\|\s*$")
    slug_pattern = re.compile(r"[a-z][a-z0-9_]+")
    float_pattern = re.compile(r"[-+]?\d+\.\d+")

    for line in lines:
        m = row_pattern.match(line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if all(set(c) <= set("-: ") for c in cells):
            continue
        slug_match = None
        floats_in_cells = []
        note = ""
        for c in cells:
            sm = slug_pattern.findall(c.lower())
            for s in sm:
                if slug_match:
                    break
                if "_" in s and len(s) > 5:
                    slug_match = s
                elif len(s) >= 7 and s not in STOPWORDS and not float_pattern.match(s):
                    slug_match = s
            for f in float_pattern.findall(c):
                try:
                    floats_in_cells.append(float(f))
                except ValueError:
                    pass

        if slug_match and len(floats_in_cells) >= 2:
            lat, lon = floats_in_cells[0], floats_in_cells[1]
            if 41.0 <= lat <= 43.5 and 8.0 <= lon <= 10.0:
                for c in reversed(cells):
                    if not float_pattern.match(c.strip()) and slug_match not in c:
                        note = c
                        break
                corrections.append({"slug": slug_match, "lat": lat, "lon": lon, "note": note})
    return corrections


def find_site_in_jsons(slug, jsons):
    for filename, data, items in jsons:
        for item in items:
            if item.get("slug") == slug:
                return filename, item
    parts = slug.split("_")
    if len(parts) < 2:
        return None, None
    for filename, data, items in jsons:
        for item in items:
            real_slug = (item.get("slug") or "").lower()
            if all(p in real_slug for p in parts if len(p) > 2):
                return filename, item
    return None, None


def apply_corrections(corrections, brief_id, dry_run=True):
    today = date.today().isoformat()
    jsons = {}
    for fn in ["sites_patrimoine.json", "sites_em.json", "sites_corse.json"]:
        path, data, items = load_json_with_fallback(fn, "sites")
        if path:
            jsons[fn] = (path, data, items)
    jsons_for_search = [(fn, t[1], t[2]) for fn, t in jsons.items()]

    _, _, doyennes = load_json_with_fallback("doyennes_polygons.json", "doyennes")
    _, _, pieves = load_json_with_fallback("pieves_polygons.json", "pieves")

    log = []
    files_modified = set()
    n_applied = 0
    n_skipped_locked = 0
    n_not_found = 0

    for c in corrections:
        slug_brief = c["slug"]
        new_lat = c["lat"]
        new_lon = c["lon"]
        note = c["note"]

        filename, item = find_site_in_jsons(slug_brief, jsons_for_search)
        if not item:
            log.append({"slug": slug_brief, "status": "NOT_FOUND",
                        "lat": new_lat, "lon": new_lon, "note": note})
            n_not_found += 1
            continue

        slug_real = item["slug"]
        if item.get("gps_locked"):
            log.append({"slug": slug_real, "slug_brief": slug_brief,
                        "status": "LOCKED_SKIPPED",
                        "lock_reason": item.get("gps_lock_reason"),
                        "note": note})
            n_skipped_locked += 1
            continue

        old_lat = item["lat"]
        old_lon = item["lon"]
        dist_km = haversine_km(old_lat, old_lon, new_lat, new_lon) if old_lat else 0
        new_doy = reverse_geocode(new_lat, new_lon, doyennes) if doyennes else None
        new_piv = reverse_geocode(new_lat, new_lon, pieves) if pieves else None
        old_doy = item.get("doyenne_contemporain_slug")
        old_piv = item.get("pieve_slug")

        if not dry_run:
            existing_notes = item.get("notes") or ""
            item["lat"] = new_lat
            item["lon"] = new_lon
            item["gps_audit"] = today
            item["gps_source"] = f"Soleil manuel - audit terrain Brief {brief_id}"
            item["gps_locked"] = True
            item["gps_lock_reason"] = f"Brief {brief_id} audit Soleil - ne pas modifier automatiquement"
            item["notes"] = (
                f"{existing_notes} | GPS corrige Brief {brief_id} ({today}). "
                f"Coord originale: ({old_lat}, {old_lon}). Coord corrigee: ({new_lat}, {new_lon}). "
                f"{note}"
            ).strip(" |")
            if new_doy:
                item["doyenne_contemporain_slug"] = new_doy
            if new_piv:
                item["pieve_slug"] = new_piv
            files_modified.add(filename)

        log.append({
            "slug": slug_real,
            "slug_brief": slug_brief if slug_brief != slug_real else None,
            "status": "APPLIED" if not dry_run else "WOULD_APPLY",
            "old_lat": old_lat, "old_lon": old_lon,
            "new_lat": new_lat, "new_lon": new_lon,
            "dist_km": round(dist_km, 2),
            "old_doy": old_doy, "new_doy": new_doy,
            "old_piv": old_piv, "new_piv": new_piv,
            "doy_reassigned": old_doy != new_doy and new_doy is not None,
            "piv_reassigned": old_piv != new_piv and new_piv is not None,
            "note": note,
        })
        n_applied += 1

    if not dry_run:
        DRAFTS.mkdir(parents=True, exist_ok=True)
        for fn in files_modified:
            path, data, _ = jsons[fn]
            backup = DRAFTS / f"{fn.replace('.json', '')}.backup_brief_{brief_id}_{today}.json"
            with open(path, encoding="utf-8") as f:
                backup_content = f.read()
            with open(backup, "w", encoding="utf-8") as f:
                f.write(backup_content)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "log": log,
        "files_modified": list(files_modified),
        "n_applied": n_applied,
        "n_skipped_locked": n_skipped_locked,
        "n_not_found": n_not_found,
        "today": today,
    }


def generate_report(brief_id, result, dry_run):
    today = result["today"]
    lines = []
    lines.append(f"# Rapport de session - Brief {brief_id} (pipeline auto)")
    lines.append("")
    lines.append(f"Date : {today}")
    lines.append(f"Mode : {'DRY-RUN' if dry_run else 'APPLY'}")
    lines.append("")
    lines.append("## Synthese")
    lines.append("")
    lines.append(f"- Corrections appliquees   : {result['n_applied']}")
    lines.append(f"- Sites locked skippes     : {result['n_skipped_locked']}")
    lines.append(f"- Sites non trouves        : {result['n_not_found']}")
    lines.append(f"- Fichiers modifies        : {', '.join(result['files_modified']) or '-'}")
    lines.append("")
    lines.append("## Detail par site")
    lines.append("")
    for entry in result["log"]:
        slug = entry["slug"]
        status = entry["status"]
        lines.append(f"### {slug} ({status})")
        if entry.get("slug_brief"):
            lines.append(f"  - Slug brief Soleil : `{entry['slug_brief']}` -> slug reel : `{slug}`")
        if status in ("APPLIED", "WOULD_APPLY"):
            lines.append(f"  - Coords : ({entry['old_lat']}, {entry['old_lon']}) -> ({entry['new_lat']}, {entry['new_lon']}) (ecart {entry['dist_km']} km)")
            if entry["doy_reassigned"]:
                lines.append(f"  - Reassignation doyenne : {entry['old_doy']} -> {entry['new_doy']}")
            if entry["piv_reassigned"]:
                lines.append(f"  - Reassignation pieve : {entry['old_piv']} -> {entry['new_piv']}")
            if entry["note"]:
                lines.append(f"  - Note : {entry['note']}")
        elif status == "LOCKED_SKIPPED":
            lines.append(f"  - Lock : {entry.get('lock_reason')}")
        elif status == "NOT_FOUND":
            lines.append(f"  - Slug absent du corpus, action manuelle requise")
        lines.append("")
    return "\n".join(lines)


def generate_git_command(brief_id, files_modified):
    today = date.today().isoformat()
    if not files_modified:
        return "# Aucun fichier modifie - pas de commit necessaire"
    files_to_add = [f"docs/data/{f}" for f in files_modified]
    files_to_add.append(f"fiches_patrimoine/RAPPORT_SESSION_BRIEF_{brief_id}.md")
    files_to_add.append(f"_drafts/sites_*.backup_brief_{brief_id}_{today}.json")
    files_to_add.append(f"_drafts/cowork_manifest_brief_{brief_id}.txt")
    branch = f"feat/brief-{brief_id}-cowork-pipeline"
    cmd = (
        f"git checkout -b {branch} && "
        f"git add {' '.join(files_to_add)} && "
        f"git commit -m 'data(patrimoine): Brief {brief_id} - corrections via pipeline Cowork (gps_locked)' && "
        f"git push -u origin {branch}"
    )
    return cmd


def generate_manifest(brief_id, input_path, files_modified, today):
    """Manifest pour Code : fichiers attendus apres ce brief.
    Code peut differ-checker que tout existe avant commit.
    """
    files = []
    files.append(f"# Manifest Cowork - Brief {brief_id} - {today}")
    files.append(f"# Code: differ-check chaque path existe avant commit. Tout fichier absent = a flagger.")
    files.append("")
    files.append("# Input brief (Cowork-side)")
    inp = Path(input_path)
    if inp.is_absolute():
        try:
            files.append(str(inp.relative_to(ROOT)))
        except ValueError:
            files.append(str(inp))
    else:
        files.append(str(inp))
    files.append("")
    files.append("# Data modifiee")
    for fn in files_modified:
        files.append(f"docs/data/{fn}")
    files.append("")
    files.append("# Backup pipeline auto (preuve d'integrite)")
    for fn in files_modified:
        files.append(f"_drafts/{fn.replace('.json', '')}.backup_brief_{brief_id}_{today}.json")
    files.append("")
    files.append("# Rapport")
    files.append(f"fiches_patrimoine/RAPPORT_SESSION_BRIEF_{brief_id}.md")
    files.append("")
    files.append("# Manifest (ce fichier)")
    files.append(f"_drafts/cowork_manifest_brief_{brief_id}.txt")
    return "\n".join(files)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", required=True)
    parser.add_argument("--brief-id", required=True)
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    print(f"[pipeline] Brief {args.brief_id} - parsing {args.input}", file=sys.stderr)
    corrections = parse_brief_markdown(text)
    print(f"[pipeline] {len(corrections)} corrections detectees", file=sys.stderr)
    for c in corrections:
        print(f"  - {c['slug']:50s} ({c['lat']}, {c['lon']})", file=sys.stderr)
    print("", file=sys.stderr)

    if not corrections:
        print("[pipeline] Aucune correction parsee.", file=sys.stderr)
        sys.exit(1)

    result = apply_corrections(corrections, args.brief_id, dry_run=args.dry_run)
    report = generate_report(args.brief_id, result, args.dry_run)
    if not args.dry_run:
        RAPPORTS.mkdir(parents=True, exist_ok=True)
        rapport_path = RAPPORTS / f"RAPPORT_SESSION_BRIEF_{args.brief_id}.md"
        rapport_path.write_text(report, encoding="utf-8")
        print(f"[pipeline] Rapport : {rapport_path}", file=sys.stderr)

    print("\n=== RAPPORT ===\n")
    print(report)

    # Brief patch — manifest généré aussi en dry-run pour permettre à Code de
    # valider en avance. L'écriture du fichier _drafts/ ne se fait qu'avec
    # --apply (non destructif en dry-run, mais visibilité totale).
    manifest = generate_manifest(args.brief_id, args.input, result["files_modified"], result["today"])
    if args.apply:
        manifest_path = DRAFTS / f"cowork_manifest_brief_{args.brief_id}.txt"
        manifest_path.write_text(manifest, encoding="utf-8")
        print(f"[pipeline] Manifest : {manifest_path}", file=sys.stderr)
    else:
        print("[pipeline] Manifest généré (dry-run, non écrit)", file=sys.stderr)
    print("\n=== MANIFEST COWORK ===\n")
    print(manifest)
    print("\n=== COMMANDE GIT POUR CODE ===\n")
    print(generate_git_command(args.brief_id, result["files_modified"]))


if __name__ == "__main__":
    main()
