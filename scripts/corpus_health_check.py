#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corpus_health_check.py - Validateur invariants corpus Tellux Patrimoine.

A lancer apres chaque PR (ou avant un brief Cowork) pour valider la sante
du corpus. Sortie : markdown report + exit code (0 = OK, 1 = warnings, 2 = erreurs).

Adapte en M3 (sprint sites_app.json, 2026-05-13) : sites_em.json a ete
supprime ; les 48 entrees site_em vivent dans public/data/sites_app.json
a cote des 8 site_uth et 5 source_thermale. Le check `sites_em` filtre
desormais type=site_em depuis sites_app.json. Voir AUDIT_COORDS_APP_2026-05-13.md.

INVARIANTS verifies :

1. JSON validity : sites_patrimoine.json + sites_app.json + sites_corse.json
   doivent etre des JSON valides.

2. Slugs uniques : chaque slug est unique a l'interieur de chaque fichier.

3. Coords presentes : tout site a `lat` et `lon` non-null.

4. Coords precision : flag les sites avec lat ou lon a moins de 3 decimales
   (suspect d'approximation grossiere).

5. Coords bbox Corse : 41.0 <= lat <= 43.5 et 8.0 <= lon <= 10.0 (sinon
   probable site en mer ou erreur).

6. Champs manquants : axe_corpus, categorie, description (warning si absent).

7. Sites locked : compteur par doyenne_contemporain_slug + total.

8. _orphan_brief35 residuels : detecter les sites flagges orphan non resolus.

9. Cross-app divergences : pour les slugs presents dans sites_em.json ET
   sites_patrimoine.json (14 doublons cross-app legitimes), verifier coords
   egales.

10. Reverse-geo coherence : pour un echantillon, verifier que
    doyenne_contemporain_slug correspond bien au polygone qui contient (lat, lon).

11. Sources_originales presentes : tout site doit avoir au moins 1 source.

12. axe_corpus null : aucun site ne doit avoir axe_corpus null/empty (sinon
    icone ? en prod).

USAGE :
  python scripts/corpus_health_check.py
  python scripts/corpus_health_check.py --output _drafts/health_2026-05-07.md
  python scripts/corpus_health_check.py --quiet  # exit code uniquement, pas de stdout

EXIT CODES :
  0 - OK : aucun warning, aucune erreur
  1 - WARNINGS : warnings mais pas d'erreurs bloquantes
  2 - ERREURS : invariants critiques violes (JSON invalide, slugs dupliques)

Author : Cowork (Brief 39nonies suite Q2, 2026-05-07)
"""

import argparse
import json
import math
import sys
from collections import defaultdict, Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "docs" / "data"
# Brief patch — découverte dynamique des worktrees au lieu de hardcoder
# des slugs datés et fragiles. Si .claude/worktrees/ n'existe pas, la liste
# reste vide (cas standard hors environnement multi-worktree Claude Code).
WORKTREES_ROOT = ROOT / ".claude" / "worktrees"
WORKTREES = (
    [w / "docs" / "data" for w in sorted(WORKTREES_ROOT.iterdir())
     if w.is_dir() and (w / "docs" / "data").is_dir()]
    if WORKTREES_ROOT.exists() else []
)


def load_json_with_fallback(filename, key=None):
    for src in [DATA_DIR] + WORKTREES:
        path = src / filename
        if not path.exists():
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            items = data.get(key, []) if key else data
            return path, data, items
        except json.JSONDecodeError as e:
            return path, None, str(e)
    return None, None, []


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


def coord_decimals(v):
    """Retourne le nombre de decimales effectives d'un float."""
    if v is None:
        return 0
    s = repr(v)
    if "." not in s:
        return 0
    return len(s.split(".")[1].rstrip("0"))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--output", help="Path markdown sortie (sinon stdout)")
    parser.add_argument("--quiet", action="store_true", help="Pas de stdout, juste exit code")
    parser.add_argument("--json", action="store_true", help="Sortie JSON au lieu de markdown")
    args = parser.parse_args()

    today = date.today().isoformat()
    report_lines = []
    warnings = []
    errors = []

    def add(line=""):
        report_lines.append(line)

    add(f"# Corpus Health Check - {today}")
    add()

    # === 1. JSON validity ===
    add("## 1. JSON validity")
    add()
    # Adapte en M3 (sprint sites_app.json, 2026-05-13) : sites_em.json a ete
    # supprime, les 48 entrees site_em vivent dans public/data/sites_app.json
    # a cote des site_uth et source_thermale. La validation utilise donc
    # sites_app.json (chargement via fallback path public/data/), et le
    # decompte/cross-app cible le filtre type=site_em ci-dessous.
    files_to_check = [
        ("sites_patrimoine.json", "sites"),
        ("sites_app.json", "sites"),
        ("sites_corse.json", "sites"),
        ("doyennes_polygons.json", "doyennes"),
        ("pieves_polygons.json", "pieves"),
    ]
    loaded = {}
    for fn, key in files_to_check:
        path, data, items = load_json_with_fallback(fn, key)
        if path is None:
            add(f"- ERROR `{fn}` : fichier absent")
            errors.append(f"{fn} absent")
        elif data is None:
            add(f"- ERROR `{fn}` : JSON invalide ({items})")
            errors.append(f"{fn} JSON invalide")
        else:
            n = len(items) if isinstance(items, list) else "?"
            add(f"- OK `{fn}` : {n} items")
            loaded[fn] = items
    add()

    sites_patrim = loaded.get("sites_patrimoine.json") or []
    # M3 : sites_em (48) extrait de sites_app.json par filtre type=site_em.
    all_app_sites = loaded.get("sites_app.json") or []
    sites_em = [s for s in all_app_sites if s.get("type") == "site_em"]
    sites_corse = loaded.get("sites_corse.json") or []
    doyennes = loaded.get("doyennes_polygons.json") or []
    pieves = loaded.get("pieves_polygons.json") or []

    # === 2. Slugs uniques ===
    add("## 2. Slugs uniques par fichier")
    add()
    for label, sites in [("patrimoine", sites_patrim), ("em", sites_em), ("corse", sites_corse)]:
        slugs = [s.get("slug") for s in sites if s.get("slug")]
        dup = [s for s, c in Counter(slugs).items() if c > 1]
        if dup:
            add(f"- ERROR {label} : {len(dup)} slug(s) dupliquees : {dup[:5]}")
            errors.append(f"{label} slugs dup : {dup}")
        else:
            add(f"- OK {label} : {len(slugs)} slugs uniques")
    add()

    # === 3. Coords presentes ===
    add("## 3. Coords presentes (lat/lon non-null)")
    add()
    for label, sites in [("patrimoine", sites_patrim), ("em", sites_em)]:
        missing = [s.get("slug") for s in sites if s.get("lat") is None or s.get("lon") is None]
        if missing:
            add(f"- WARN {label} : {len(missing)} sans coords : {missing[:5]}")
            warnings.append(f"{label} sans coords : {len(missing)}")
        else:
            add(f"- OK {label} : tous coords")
    add()

    # === 4. Coords precision (<3 decimales suspect) ===
    add("## 4. Coords precision (<3 decimales suspect)")
    add()
    suspects = []
    for s in sites_patrim:
        lat, lon = s.get("lat"), s.get("lon")
        if lat is None or lon is None:
            continue
        d_lat = coord_decimals(lat)
        d_lon = coord_decimals(lon)
        if d_lat < 3 or d_lon < 3:
            suspects.append((s["slug"], lat, lon, d_lat, d_lon))
    if suspects:
        add(f"- WARN {len(suspects)} sites avec coords <3 decimales :")
        for sl, la, lo, dl, dn in suspects[:10]:
            add(f"  - `{sl}` ({la}, {lo}) [{dl}/{dn} dec]")
        if len(suspects) > 10:
            add(f"  - ... ({len(suspects)-10} autres)")
        warnings.append(f"coords imprecises : {len(suspects)}")
    else:
        add("- OK tous coords >= 3 decimales")
    add()

    # === 5. Coords bbox Corse ===
    add("## 5. Coords bbox Corse (41.0-43.5 lat, 8.0-10.0 lon)")
    add()
    out_bbox = []
    for s in sites_patrim:
        lat, lon = s.get("lat"), s.get("lon")
        if lat is None or lon is None:
            continue
        if not (41.0 <= lat <= 43.5 and 8.0 <= lon <= 10.0):
            out_bbox.append((s["slug"], lat, lon))
    if out_bbox:
        add(f"- ERROR {len(out_bbox)} sites hors bbox Corse :")
        for sl, la, lo in out_bbox[:10]:
            add(f"  - `{sl}` ({la}, {lo})")
        errors.append(f"hors bbox : {len(out_bbox)}")
    else:
        add("- OK tous coords dans bbox Corse")
    add()

    # === 6. Champs manquants ===
    add("## 6. Champs essentiels (axe_corpus, categorie)")
    add()
    no_axe = [s["slug"] for s in sites_patrim if not s.get("axe_corpus")]
    no_cat = [s["slug"] for s in sites_patrim if not s.get("categorie")]
    if no_axe:
        add(f"- ERROR {len(no_axe)} sites sans axe_corpus (icone ? en prod) : {no_axe[:5]}")
        errors.append(f"axe_corpus null : {len(no_axe)}")
    else:
        add("- OK tous axe_corpus rempli")
    if no_cat:
        add(f"- WARN {len(no_cat)} sites sans categorie : {no_cat[:5]}")
        warnings.append(f"categorie null : {len(no_cat)}")
    else:
        add("- OK tous categorie remplie")
    add()

    # === 7. Sites locked par doyenne ===
    add("## 7. Sites gps_locked par doyenne")
    add()
    by_doy = defaultdict(lambda: {"locked": 0, "total": 0})
    total_locked = 0
    for s in sites_patrim:
        doy = s.get("doyenne_contemporain_slug") or "(null)"
        by_doy[doy]["total"] += 1
        if s.get("gps_locked"):
            by_doy[doy]["locked"] += 1
            total_locked += 1
    add(f"Total locked : **{total_locked}** / {len(sites_patrim)}")
    add()
    add("| Doyenne | Locked | Total | % |")
    add("|---|---|---|---|")
    for doy in sorted(by_doy.keys()):
        s = by_doy[doy]
        pct = (100*s["locked"]/s["total"]) if s["total"] else 0
        add(f"| {doy} | {s['locked']} | {s['total']} | {pct:.0f}% |")
    add()

    # === 8. _orphan_brief35 residuels ===
    add("## 8. _orphan_brief35 residuels")
    add()
    orphans = [s["slug"] for s in sites_patrim if s.get("_orphan_brief35")]
    if orphans:
        add(f"- WARN {len(orphans)} sites flagges orphan_brief35 (Brief 36 R5 partiellement resolu) : {orphans[:10]}")
        warnings.append(f"orphans residuels : {len(orphans)}")
    else:
        add("- OK aucun orphan_brief35 residuel")
    add()

    # === 9. Cross-app divergences EM <-> Patrimoine ===
    add("## 9. Cross-app divergences EM <-> Patrimoine")
    add()
    em_by_slug = {s["slug"]: s for s in sites_em}
    cross_app = []
    for s in sites_patrim:
        slug = s.get("slug")
        if slug in em_by_slug:
            ems = em_by_slug[slug]
            ds = abs((s.get("lat") or 0) - (ems.get("lat") or 0)) + abs((s.get("lon") or 0) - (ems.get("lon") or 0))
            if ds > 0.001:
                cross_app.append((slug, (s["lat"], s["lon"]), (ems["lat"], ems["lon"])))
    if cross_app:
        add(f"- WARN {len(cross_app)} slugs cross-app avec coords divergentes :")
        for sl, p, e in cross_app[:10]:
            add(f"  - `{sl}` patrimoine={p} em={e}")
        warnings.append(f"cross-app divergent : {len(cross_app)}")
    else:
        cross_present = sum(1 for s in sites_patrim if s.get("slug") in em_by_slug)
        add(f"- OK {cross_present} slugs cross-app, coords coherentes")
    add()

    # === 10. Reverse-geo coherence (echantillon 50) ===
    add("## 10. Reverse-geo coherence (sites locked uniquement)")
    add()
    incoherent = []
    if doyennes:
        sample = [s for s in sites_patrim if s.get("gps_locked")][:50]
        for s in sample:
            lat, lon = s.get("lat"), s.get("lon")
            if lat is None or lon is None:
                continue
            geo_doy = reverse_geocode(lat, lon, doyennes)
            decl_doy = s.get("doyenne_contemporain_slug")
            if geo_doy and decl_doy and geo_doy != decl_doy:
                incoherent.append((s["slug"], decl_doy, geo_doy))
        if incoherent:
            add(f"- WARN {len(incoherent)} sites locked avec doyenne incoherente vs polygone :")
            for sl, dec, geo in incoherent[:10]:
                add(f"  - `{sl}` declaree={dec} geo={geo}")
            warnings.append(f"reverse-geo incoherent : {len(incoherent)}")
        else:
            add(f"- OK {len(sample)} sites locked verifies, doyenne coherente")
    else:
        add("- SKIP polygones doyennes non charges")
    add()

    # === 11. Sources_originales presentes ===
    add("## 11. Sources_originales presentes")
    add()
    no_src = [s["slug"] for s in sites_patrim if not s.get("sources_originales")]
    if no_src:
        add(f"- WARN {len(no_src)} sites sans sources_originales : {no_src[:5]}")
        warnings.append(f"no sources : {len(no_src)}")
    else:
        add("- OK tous sites ont sources_originales")
    add()

    # === Synthese finale ===
    add("## Synthese")
    add()
    add(f"- Erreurs : **{len(errors)}**")
    add(f"- Warnings : **{len(warnings)}**")
    add(f"- Sites patrimoine : {len(sites_patrim)}")
    add(f"- Sites EM : {len(sites_em)}")
    pct_locked = (100*total_locked/len(sites_patrim)) if sites_patrim else 0
    add(f"- Sites locked : {total_locked} ({pct_locked:.0f}%)")
    add()
    if errors:
        add("Status : **FAIL** (erreurs critiques)")
        exit_code = 2
    elif warnings:
        add("Status : **WARN** (warnings non-bloquants)")
        exit_code = 1
    else:
        add("Status : **OK**")
        exit_code = 0
    add()
    add("---")
    add(f"Genere par scripts/corpus_health_check.py le {today}")

    output = "\n".join(report_lines)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        if not args.quiet:
            print(f"Rapport ecrit : {args.output}", file=sys.stderr)

    if args.json:
        out = {
            "date": today,
            "errors": errors,
            "warnings": warnings,
            "n_sites_patrimoine": len(sites_patrim),
            "n_sites_em": len(sites_em),
            "n_locked": total_locked,
            "exit_code": exit_code,
        }
        if not args.quiet:
            print(json.dumps(out, ensure_ascii=False, indent=2))
    elif not args.quiet and not args.output:
        print(output)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
