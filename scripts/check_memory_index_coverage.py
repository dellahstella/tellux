#!/usr/bin/env python3
"""
Recense les fichiers d'un dossier de mémoire Claude Code (un .md = un fait, cf.
la convention mémoire du projet) qui ne sont atteignables PAR AUCUN CHEMIN depuis
son fichier d'index (MEMORY.md) — un fichier "orphelin" existe sur disque mais
n'est jamais relu depuis l'index, donc cesse d'exister en pratique pour une
session qui ne lit que l'index.

Contexte (brief, 2026-09-06/07) : la compaction de MEMORY.md du 2026-09-06 a
fait perdre 2 pointeurs réels et datés, restaurés après audit manuel. Le même
audit a remonté une liste de 127 orphelins antérieurs à cette session. Motif
nommé par Soleil : le contenu existe, le chemin pour l'atteindre ne tient pas
— même diagnostic que le corpus scientifique le même jour. Ce script rend cet
audit reproductible et pose un plancher de couverture.

Méthode — ATTEIGNABILITÉ MULTI-SAUTS, pas une simple sous-chaîne :
    "Atteignable" = le fichier est référencé (par [[nom]] ou (nom.md)) soit
    directement dans la PARTIE CHARGÉE de MEMORY.md (voir loaded_index : Claude Code
    ne lit que 200 lignes ou 25 000 caractères comptés ; corrigé le 2026-09-24, le script
    lisait jusque-là le fichier entier et ne voyait pas une troncature), soit dans un
    fichier lui-même atteignable
    depuis MEMORY.md — parcours en largeur, profondeur non plafonnée (les
    chaînes réelles observées dans ce dossier ne dépassent pas 2-3 sauts,
    ex. MEMORY.md → fichier d'agrégation de période → fichier individuel).
    C'est délibéré : le principe posé par Soleil est qu'un CHEMIN doit exister,
    pas que le lien soit direct — un fichier d'agrégation par période
    (cf. le patron déjà utilisé dans ce dossier : project_cloture_session_*.md)
    est un chemin valide, pas un contournement.

Two modes:
    --report   : imprime l'inventaire complet (orphelins avec date/sujet
                 extraits du frontmatter YAML), ne touche à rien.
    --check     : compare l'ensemble des orphelins actuel à celui d'un
                 passage précédent (fichier d'état local, jamais commité,
                 propre à ce dossier de mémoire) ; sort en erreur (exit 1)
                 si de nouveaux orphelins sont apparus depuis. Sur succès,
                 avance le plancher (ratchet, jamais un relâchement
                 silencieux).

Ce script NE SUPPRIME ET NE MODIFIE AUCUN fichier mémoire. --check ne fait
que lire et, sur succès, mettre à jour son propre fichier d'état interne.

Usage:
    python3 check_memory_index_coverage.py --memory-dir "<chemin>" --report
    python3 check_memory_index_coverage.py --memory-dir "<chemin>" --check
"""
import argparse
import json
import os
import re
import sys

LINK_PATTERN = re.compile(r"\[\[([^\]|]+)\]\]|\(([A-Za-z0-9_.\-]+\.md)\)")

# Limites de lecture de l'index par Claude Code (2.1.280, fonction de troncature de l'index) :
# le texte est lu BRUT (retours chariot compris), débarrassé de ses blancs de bord par trim(), puis
# réduit aux 200 premières lignes, puis coupé à la dernière fin de ligne située au plus à 25 000 en
# longueur de chaîne JavaScript (unités UTF-16). Au-delà, les sessions ne voient pas la fin de l'index :
# les liens qui s'y trouvent ne rendent rien atteignable (2026-09-24 : le 20/09, deux lignes coupées ont
# rendu 4 fichiers inatteignables, alors que ce script, qui lisait le fichier entier, répondait « aucun
# orphelin »).
INDEX_MAX_LINES = 200
INDEX_MAX_UNITS = 25000
# Blancs retirés par String.prototype.trim() (WhiteSpace + LineTerminator, BOM compris ; pas U+0085).
JS_TRIM_CHARS = (
    "\t\n\x0b\x0c\r            "
    "      　﻿"
)


def loaded_index(raw_text):
    """Partie de l'index réellement chargée par Claude Code, et ses mesures.

    `raw_text` doit être lu sans conversion des fins de ligne (open(..., newline="")) :
    les retours chariot comptent dans la limite.
    """
    text = raw_text.strip(JS_TRIM_CHARS)
    lines = text.split("\n")
    n_lines = len(lines)
    units = text.encode("utf-16-le", "surrogatepass")
    n_units = len(units) // 2
    truncated = n_lines > INDEX_MAX_LINES or n_units > INDEX_MAX_UNITS
    if truncated:
        if n_lines > INDEX_MAX_LINES:
            text = "\n".join(lines[:INDEX_MAX_LINES])
            units = text.encode("utf-16-le", "surrogatepass")
        if len(units) // 2 > INDEX_MAX_UNITS:
            cut = -1
            for i in range(INDEX_MAX_UNITS, -1, -1):  # comme lastIndexOf("\n", 25000)
                if units[2 * i:2 * i + 2] == b"\n\x00":
                    cut = i
                    break
            end = cut if cut > 0 else INDEX_MAX_UNITS
            text = units[:2 * end].decode("utf-16-le", "surrogatepass")
    return text, {"lines": n_lines, "units": n_units, "truncated": truncated}


def parse_frontmatter(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    fm = {}
    if m:
        block = m.group(1)
        for line in block.split("\n"):
            stripped = line.strip()
            if stripped.startswith("type:"):
                fm["type"] = stripped.split(":", 1)[1].strip()
            elif stripped.startswith("modified:"):
                fm["modified"] = stripped.split(":", 1)[1].strip()
            elif line.startswith("name:"):
                fm["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("description:"):
                fm["description"] = line.split(":", 1)[1].strip().strip('"')
    return fm, text


def extract_links(text):
    """Renvoie l'ensemble des stems de fichiers référencés par [[nom]] ou (nom.md)."""
    stems = set()
    for m in LINK_PATTERN.finditer(text):
        wiki, md = m.group(1), m.group(2)
        if wiki:
            stems.add(wiki.strip())
        elif md:
            stems.add(md[:-3])
    return stems


def scan(memory_dir, index_filename="MEMORY.md"):
    index_path = os.path.join(memory_dir, index_filename)
    with open(index_path, encoding="utf-8", newline="") as f:
        index_text, index_stats = loaded_index(f.read())

    all_files = sorted(
        f for f in os.listdir(memory_dir)
        if f.endswith(".md") and f != index_filename
    )
    stem_to_file = {f[:-3]: f for f in all_files}

    # Parcours en largeur depuis MEMORY.md, en suivant les liens [[..]]/(..md)
    # trouvés dans chaque fichier déjà atteint, jusqu'à saturation.
    reachable_stems = set()
    frontier = extract_links(index_text) & set(stem_to_file)
    while frontier:
        reachable_stems |= frontier
        next_frontier = set()
        for stem in frontier:
            fpath = os.path.join(memory_dir, stem_to_file[stem])
            try:
                with open(fpath, encoding="utf-8") as f:
                    body = f.read()
            except OSError:
                continue
            linked = extract_links(body) & set(stem_to_file)
            next_frontier |= (linked - reachable_stems)
        frontier = next_frontier

    reachable = sorted(stem_to_file[s] for s in reachable_stems)
    orphans = sorted(f for f in all_files if f[:-3] not in reachable_stems)

    return {
        "total_files": len(all_files),
        "reachable": reachable,
        "orphans": orphans,
        "index": index_stats,
    }


def report(memory_dir):
    result = scan(memory_dir)
    idx = result["index"]
    print(f"Index chargé : {idx['units']} caractères comptés (limite {INDEX_MAX_UNITS}), "
          f"{idx['lines']} lignes (limite {INDEX_MAX_LINES}) — "
          f"{'TRONQUÉ : seule la partie chargée compte ci-dessous' if idx['truncated'] else 'chargé en entier'}")
    print(f"Fichiers .md (hors index) : {result['total_files']}")
    print(f"Atteignables depuis l'index (tous chemins confondus) : {len(result['reachable'])}")
    print(f"Orphelins (aucun chemin)  : {len(result['orphans'])}")
    print()
    if not result["orphans"]:
        print("Aucun orphelin.")
        return result
    print("--- Orphelins (fichier, date, type, description) ---")
    rows = []
    for fname in result["orphans"]:
        fm, _ = parse_frontmatter(os.path.join(memory_dir, fname))
        rows.append((
            fname,
            fm.get("modified", "?")[:10],
            fm.get("type", "?"),
            fm.get("description", "")[:200],
        ))
    rows.sort(key=lambda r: r[1])
    for fname, date, ftype, desc in rows:
        print(f"[{date}] ({ftype}) {fname}")
        print(f"    {desc}")
    return result


def check(memory_dir, state_filename="_coverage_baseline.json"):
    result = scan(memory_dir)
    orphan_set = set(result["orphans"])
    state_path = os.path.join(memory_dir, state_filename)

    if not os.path.exists(state_path):
        with open(state_path, "w", encoding="utf-8") as f:
            json.dump({
                "orphans": sorted(orphan_set),
                "reachable_count": len(result["reachable"]),
                "total_files": result["total_files"],
            }, f, ensure_ascii=False, indent=2)
        print(f"Plancher initial posé : {len(orphan_set)} orphelin(s) connu(s), "
              f"{len(result['reachable'])} fichier(s) atteignable(s).")
        return 0

    with open(state_path, encoding="utf-8") as f:
        baseline = json.load(f)
    baseline_orphans = set(baseline.get("orphans", []))

    new_orphans = orphan_set - baseline_orphans
    if new_orphans:
        print("ÉCHEC — nouveau(x) fichier(s) devenu(s) inatteignable(s) depuis le dernier passage :")
        for fname in sorted(new_orphans):
            print(f"  - {fname}")
        print()
        print("Rattacher ces fichiers depuis MEMORY.md (directement ou via un fichier "
              "d'agrégation déjà atteignable), ou les marquer explicitement comme périmés "
              "s'ils ne sont plus pertinents, puis relancer --check pour avancer le plancher.")
        return 1

    healed = baseline_orphans - orphan_set
    if healed:
        print(f"{len(healed)} orphelin(s) résorbé(s) depuis le dernier passage — plancher resserré.")

    with open(state_path, "w", encoding="utf-8") as f:
        json.dump({
            "orphans": sorted(orphan_set),
            "reachable_count": len(result["reachable"]),
            "total_files": result["total_files"],
        }, f, ensure_ascii=False, indent=2)
    print(f"OK — {len(orphan_set)} orphelin(s) connu(s) (plancher inchangé ou resserré), "
          f"{len(result['reachable'])} fichier(s) atteignable(s) sur {result['total_files']}.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--memory-dir", required=True, help="Chemin du dossier de mémoire Claude Code")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--report", action="store_true", help="Imprime l'inventaire complet, lecture seule")
    mode.add_argument("--check", action="store_true", help="Compare au plancher précédent, exit 1 si régression")
    args = ap.parse_args()

    if args.report:
        report(args.memory_dir)
        sys.exit(0)
    else:
        sys.exit(check(args.memory_dir))


if __name__ == "__main__":
    main()
