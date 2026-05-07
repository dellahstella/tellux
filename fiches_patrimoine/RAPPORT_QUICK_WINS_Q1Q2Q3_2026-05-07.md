# Rapport Quick Wins Q1+Q2+Q3 - 2026-05-07

Date : 2026-05-07
Initie par : Soleil ("attaquons les problemes que tu as listes")
Trois quick wins post-Brief 39nonies en reponse aux recommandations Code (recap shipped 28-39octies).

## Synthese

| Quick win | Effort | Statut |
|---|---|---|
| Q1 - .gitignore __pycache__ | 5 min | DONE |
| Q2 - scripts/corpus_health_check.py | 1h | DONE |
| Q3 - manifest auto dans brief_pipeline.py | 30 min | DONE |
| Bonus - cleanup _orphan_brief35 + sync cross-app aleria_antique | 10 min | DONE |

## Q1 - .gitignore __pycache__

Ajout en fin de `.gitignore` :

```
# Python
__pycache__/
*.pyc
*.pyo
.pytest_cache/
```

Resout le warning Code C8. `git status` ne polluera plus avec `scripts/__pycache__/`.

## Q2 - scripts/corpus_health_check.py

Nouveau script (450 lignes) : validateur invariants corpus a lancer apres chaque PR.

### 11 invariants verifies

1. **JSON validity** : sites_patrimoine.json + sites_em.json + sites_corse.json + polygones
2. **Slugs uniques** par fichier
3. **Coords presentes** (lat/lon non-null)
4. **Coords precision** (<3 decimales = WARN approximation grossiere)
5. **Coords bbox Corse** (41.0-43.5 lat, 8.0-10.0 lon)
6. **Champs essentiels** axe_corpus + categorie remplis
7. **Sites locked par doyenne** (table compteurs)
8. **_orphan_brief35 residuels** (Brief 36 R5 partiel)
9. **Cross-app divergences** EM ↔ Patrimoine (14 doublons legitimes a verifier)
10. **Reverse-geo coherence** (echantillon 50 locked, doyenne declaree vs polygone)
11. **Sources_originales presentes**

### Usage

```
python scripts/corpus_health_check.py                         # stdout markdown
python scripts/corpus_health_check.py --output _drafts/health.md
python scripts/corpus_health_check.py --json                  # JSON pour CI
python scripts/corpus_health_check.py --quiet                 # exit code only
```

Exit codes : 0=OK, 1=warnings, 2=erreurs critiques.

### Premier run baseline

```json
{
  "errors": [],
  "warnings": [
    "coords imprecises : 217",
    "orphans residuels : 7"
  ],
  "n_sites_patrimoine": 449,
  "n_sites_em": 48,
  "n_locked": 76,
  "exit_code": 1
}
```

7 orphans residuels Brief 36 R5 (cf C6 dette technique - audit terrain Soleil).
217 coords imprecises (<3 decimales) - majoritairement sites EM ou megalithes legacy. A traiter par doyenne en futurs briefs audit.

## Q3 - manifest auto dans brief_pipeline.py

Ajout fonction `generate_manifest(brief_id, input, files_modified, today)` qui genere `_drafts/cowork_manifest_brief_<id>.txt` en mode `--apply`. Format :

```
# Manifest Cowork - Brief <id> - 2026-05-07
# Code: differ-check chaque path existe avant commit.

# Input brief
_drafts/brief_<id>_input.md

# Data modifiee
docs/data/sites_patrimoine.json

# Backup pipeline auto
_drafts/sites_patrimoine.backup_brief_<id>_2026-05-07.json

# Rapport
fiches_patrimoine/RAPPORT_SESSION_BRIEF_<id>.md

# Manifest (ce fichier)
_drafts/cowork_manifest_brief_<id>.txt
```

`generate_git_command()` ajoute le manifest a la liste `git add`. Code peut maintenant differ-checker la presence de tous les fichiers attendus avant commit.

Resout le warning Code A1 (promesses Cowork non livrees).

## Bonus - 2 nettoyages declenches par health check

Le premier run du health check a expose 2 quick wins immediats :

1. **9 sites _orphan_brief35** dont 2 maintenant gps_locked (menhir_sermano + santa_maria_della_neve_grosseto_prugna_basse, traites en Brief 39nonies). Le flag _orphan_brief35 est devenu obsolete pour ces 2. Cleanup applique. Restent 7 vrais orphans.

2. **1 cross-app divergence** : aleria_antique avait coords differentes entre patrimoine (42.1142, 9.5131 = Brief 39octies locked) et em (42.105, 9.513 = ancien). Sync : em.json aligne sur patrimoine. 0 cross-app divergence apres.

## Garde-fous Brief 39nonies inchanges

- Tous les sites locked Briefs 38-39nonies preserves
- Backup snapshot pre-Q1Q2Q3 : `_drafts/sites_patrimoine.brief39nonies_post_2026-05-07.json`

## Fichiers livres

- `.gitignore` (Q1 patch)
- `scripts/corpus_health_check.py` (Q2 nouveau)
- `scripts/brief_pipeline.py` (Q3 patch + reecrit complet apres troncature linter)
- `_drafts/health_check_2026-05-07.md` (premier baseline)
- `docs/data/sites_patrimoine.json` (worktree distracted-cohen, cleanup orphan flags)
- `docs/data/sites_em.json` (worktree distracted-cohen, sync aleria_antique)

## Recommandations pour la suite

1. **Lancer corpus_health_check.py avant chaque brief Cowork** pour avoir un baseline.
2. **CI optionnelle** : ajouter step "python scripts/corpus_health_check.py --quiet" dans workflow GitHub. Exit code 2 = bloque PR ; exit code 1 = comment warning.
3. **Briefs futurs** : reduire les 217 coords imprecises par doyenne (Sagone, Ajaccio, Aleria, Prunelli encore non audites).

## Critères d'acceptation

| Critere | Statut |
|---|---|
| Q1 .gitignore patche | OUI |
| Q2 script fonctionne (exit code coherent) | OUI (1 = warnings non bloquants) |
| Q3 pipeline genere manifest en mode --apply | OUI |
| Aucune regression sites_patrimoine.json | OUI (449 sites, 76 locked, 0 erreurs) |
| Backup conserve | OUI |
