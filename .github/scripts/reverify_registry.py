#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tellux — R2 Re-vérification périodique des citations (registry).

Re-passe le résolveur anti-Frankenstein (scripts/verify_citation.py) sur CHAQUE
entrée du registry public scripts/citations_registry.json, pour détecter les
régressions silencieuses : DOI qui ne résout plus (UNRESOLVED) ou métadonnée qui
dérive (DRIFT sur l'année). DÉTECTE et SIGNALE uniquement — ne modifie NI le
registry NI aucune citation (Cran B/C selon le scope ; voir le workflow).

Scope : registry PUBLIC uniquement. Les refs espèces volet (b) (Phase 3) ne sont
pas registrées (comme voulu) → hors champ par construction.

« Affichée publiquement » : en CI, seul le contenu TRACKÉ est présent (les
chantiers recherche/ sont gitignored, donc absents du checkout). Un DOI qui
apparaît dans un fichier tracké (hors registry) est donc, de fait, public-facing
→ une régression dessus relève du Cran C (signale + parque, décision Soleil).

Sortie : JSON sur stdout { total, ok, regressions[] }. Exit 0 si aucune
régression, 2 sinon (cohérent avec le gate §10).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Importer le résolveur canonique (scripts/verify_citation.py) comme module.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from verify_citation import resolve, load_registry, REGISTRY_PATH  # noqa: E402


def _norm(s: object) -> str:
    return "".join(ch for ch in str(s or "").lower() if ch.isalnum())


def _tracked_public_files() -> list[Path]:
    """Fichiers texte trackés susceptibles d'afficher une citation (hors registry)."""
    out: list[Path] = []
    for pat in ("*.html", "*.md"):
        for p in REPO_ROOT.rglob(pat):
            sp = str(p)
            if ".git" in sp or "node_modules" in sp:
                continue
            if p.resolve() == REGISTRY_PATH.resolve():
                continue
            out.append(p)
    return out


def _is_public_facing(doi: str, corpus: list[tuple[str, str]]) -> list[str]:
    """Retourne la liste des fichiers trackés où le DOI apparaît (public-facing)."""
    needle = doi.lower()
    return [rel for rel, text in corpus if needle in text]


def main() -> int:
    reg = load_registry()
    if not reg:
        print(json.dumps({"error": "registry vide ou introuvable", "path": str(REGISTRY_PATH)}))
        return 2

    # Pré-charger le corpus public tracké une seule fois.
    corpus: list[tuple[str, str]] = []
    for p in _tracked_public_files():
        try:
            corpus.append((str(p.relative_to(REPO_ROOT)), p.read_text(encoding="utf-8", errors="ignore").lower()))
        except Exception:
            continue

    regressions = []
    skipped_non_doi = []
    ok = 0
    dois = sorted(reg.keys())
    for doi in dois:
        entry = reg[doi] or {}
        # Clés non-DOI (ex. PII Elsevier "PII:S...") : non résolvables par le
        # résolveur DOI → ce n'est pas une régression, on ne re-vérifie pas.
        # Signalé en info (data-quality du registry, à arbitrer Soleil).
        if not (doi.startswith("10.") and "/" in doi):
            skipped_non_doi.append({"key": doi, "titre": entry.get("titre")})
            continue
        fresh = None
        try:
            fresh = resolve(doi)
        except Exception as e:  # réseau / parsing — traité comme non concluant
            fresh = None
            err = str(e)[:160]
        else:
            err = None

        if not fresh:
            public_in = _is_public_facing(doi, corpus)
            regressions.append({
                "doi": doi,
                "type": "UNRESOLVED",
                "detail": err or "le résolveur n'a renvoyé aucune source",
                "public_facing": bool(public_in),
                "public_in": public_in,
                "registry_titre": entry.get("titre"),
            })
        else:
            # Dérive : comparer l'année (champ stable). Le titre varie en forme
            # selon l'API → comparé en info seulement, pas en régression dure.
            drift = []
            if entry.get("annee") and fresh.get("annee") and str(entry["annee"]) != str(fresh["annee"]):
                drift.append(f"année registry={entry['annee']} vs résolue={fresh['annee']}")
            title_changed = bool(entry.get("titre") and fresh.get("titre") and _norm(entry["titre"]) != _norm(fresh["titre"]))
            if drift:
                public_in = _is_public_facing(doi, corpus)
                regressions.append({
                    "doi": doi,
                    "type": "DRIFT",
                    "detail": "; ".join(drift),
                    "title_changed": title_changed,
                    "public_facing": bool(public_in),
                    "public_in": public_in,
                })
            else:
                ok += 1
        time.sleep(0.4)  # politesse réseau Crossref/DataCite

    public_regressions = [r for r in regressions if r.get("public_facing")]
    report = {
        "total": len(dois),
        "ok": ok,
        "regressions_count": len(regressions),
        "public_regressions_count": len(public_regressions),
        "skipped_non_doi_count": len(skipped_non_doi),
        "regressions": regressions,
        "skipped_non_doi": skipped_non_doi,
        "note": "Re-vérification lecture seule. Aucune écriture registry/citation. Clés non-DOI "
                "(PII…) ignorées (info, pas régression). Régression public-facing => Cran C "
                "(signale + parque, Soleil) ; interne => Cran B.",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not regressions else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
