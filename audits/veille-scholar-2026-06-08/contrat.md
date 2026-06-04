# CONTRAT D'ITÉRATION — Veille Scholar Phase 1

> À lire avec `PROTOCOLE_AUTO_ITERATION.md` à la racine du repo et `INVENTAIRE_VEILLE.md` du même dossier.
> Brief d'origine : « BRIEF CODE — Veille Scholar (réalisation autonome) » du 2026-06-04.
> Arbitrages Soleil 2026-06-04 (post-inventaire) :
> - **Q1** : « n8n sur Railway » du brief = legacy à corriger. Pipeline reste sur GitHub Actions.
> - **Q3** : format digest = statu quo markdown. Améliorations Phase 1 en interne, pas dans le format de sortie.
> - **Q4** : `verify_citation.py` câblé en pré-qualification dès Phase 1.

```
CHANTIER  : Veille Scholar Phase 1 — durcissement amont (dédup + verify_citation)
AXE       : app (pipeline backend)
GÉNÉRATEUR: Code
ÉVALUATEUR: Code (session fraîche, fixture corpus_test/)
DATE      : 2026-06-04
ÉCHÉANCE  : pas d'urgence avant lundi 8 juin (le cron tournera sur le code actuel,
            stable. La Phase 1 entre en prod via merge après feu vert évaluateur).
```

## OBJECTIF (1 phrase)

Ajouter à `.github/scripts/veille_scholar.py` (a) une **dédup intra-run** par hash `(titre normalisé + premier auteur)` et (b) une **pré-qualification verify_citation** sur les DOI/URL extraits des bodies email Scholar, **sans toucher au format markdown de sortie** ni au prompt v2 (côté Cowork).

## DANS LE PÉRIMÈTRE

- Modifier `.github/scripts/veille_scholar.py` (fichier unique côté Code).
- Ajouter un parser basique des bodies emails Scholar pour extraire `(titre, premier auteur, doi_ou_url_si_présent)` par référence.
- Implémenter une dédup **intra-run** (même papier dans 2 alertes du même cycle hebdo → traité 1 fois).
- Importer `scripts/verify_citation.py` (le repo entier est checkouté par le workflow, donc accessible).
- Pour chaque référence avec DOI/URL : appel `verify_citation` côté Python (Crossref + fallbacks), annotation `verified: true/false` + quadruplet ou motif d'échec.
- Le résultat de la pré-qualif est **passé à Claude dans le contexte** pour qu'il puisse choisir d'en faire mention dans la synthèse markdown.
- Logging structuré : `[dedup] N total → M après dédup`, `[verify] X DOI/URL trouvés, Y verified, Z failed`.
- Aucune modification du format markdown de sortie (Q3 statu quo).
- Aucune modification du prompt `prompt_veille_tellux_v2.md` (côté Cowork uniquement).

## HORS PÉRIMÈTRE

- **Dédup inter-run** (papier déjà traité au run N-1) → différé Phase 2. Nécessite un index persistant côté repo privé.
- **Tag par axe machine-readable** (YAML frontmatter, JSON) → Q3 statu quo l'exclut.
- **Format JSON structuré** → Q3 statu quo l'exclut.
- **Modification du prompt v2** → côté Cowork, Soleil arbitre.
- **Modification du workflow YAML** → restera intact tant que le script Python est suffisant.
- **Migration vers n8n / Railway** → Q1 legacy, hors scope définitivement (sauf décision future).

## CRITÈRES D'ACCEPTATION

Rubrique §5.1 du protocole, adaptée au pipeline backend (pas d'UI à tester).

### Fonctionnalité (0.35)

**Dédup intra-run** :
- Sur le `corpus_test/` (10-15 mails, au moins 2 doublons artificiels), la dédup détecte et écarte les doublons (M < N).
- Log `[dedup] N → M` présent et cohérent.
- Aucune référence légitime perdue (false-positive < 5%).

**verify_citation câblé** :
- Sur le corpus de test, au moins une référence avec DOI/URL passe en `verified: true`.
- Au moins une référence sans DOI/URL passe en `verified: null` ou `verified: false` (motif `no_doi_or_url`).
- Aucune exception non-gérée du fait de `verify_citation` (failsafe).
- Le contexte injecté dans le prompt Claude contient les annotations (vérifiable dans `[anthropic] ... caractères en input`).

### Non-régression (0.30)

- Le pipeline en `dry_run=1` se termine **succès** sur le corpus de test.
- La synthèse markdown produite garde la structure habituelle (titre H1, header méta-données, contenu).
- Aucune erreur ni warning supplémentaire vs le pipeline actuel.
- Les 5 secrets restent les seuls requis (pas de nouveau secret introduit).

### Craft (0.20)

- Le code ajouté reste lisible (fonctions nommées, docstrings, type hints comme le reste du fichier).
- Pas de duplication majeure (parser email factorisé).
- Le diff reste localisé dans `.github/scripts/veille_scholar.py` (et éventuellement un fichier helper si justifié).

### Robustesse (0.15)

- Échec réseau lors d'un appel `verify_citation` → log warning, `verified: false` + raison, on continue. Le run ne tombe pas.
- Email Scholar mal-formé (parser ne trouve pas titre/auteur) → log debug, référence passée telle quelle à Claude, on continue.
- `verify_citation` raise une exception → catch, log, on continue.
- 0 erreur fatale sur le corpus de test.

## NOTE — Stratégie de test

L'évaluateur tourne **localement** (pas dans GitHub Actions) sur le `corpus_test/` :

```bash
# Cibler le script modifié avec une fixture fichier au lieu de Gmail API
python3 -m pytest audits/veille-scholar-2026-06-08/test_phase1.py
# OU exécution directe avec env CORPUS_FIXTURE=audits/veille-scholar-2026-06-08/corpus_test/
```

Pour cela, **modifier `veille_scholar.py` pour qu'il accepte une fixture fichier au lieu de Gmail API** si une env var `CORPUS_FIXTURE` est définie. C'est une porte de test, pas un changement du comportement prod.

Spécifications du `corpus_test/` :
- 10-15 fichiers `.eml` ou `.json` représentant des alertes Scholar récentes (snapshot Gmail).
- Au moins 2 doublons artificiels (même papier dans 2 mails de requêtes différentes — vérifier la dédup intra-run).
- Au moins 3 références avec DOI valide (vérifier `verify_citation` PASS).
- Au moins 1 référence sans DOI / DOI faux (vérifier failsafe).
- Aucun PII / credentials dans les fichiers (uniquement le payload public des alertes Scholar).

## PARAMÈTRES DE BOUCLE

```
SEUIL DE RÉUSSITE : 7.0 / 10 (pondéré)
MAX ITÉRATIONS    : 8
ESCALADE          : plateau (Δ < 0.3 sur 3 itérations) → stop + RAPPORT_FINAL.md
                    OU régression sur la synthèse markdown → stop + rollback
                    OU casse du run en prod → stop + revert immédiat
```

## STRATÉGIE DE DÉPLOIEMENT

```
1. Phase 1 développée sur branche feat/veille-scholar-2026-06-08 (déjà créée).
2. Tests locaux sur corpus_test/ — pas de touche au workflow tant que les tests
   ne passent pas.
3. Itération générateur ≠ évaluateur jusqu'à score ≥ 7.0.
4. Dry-run du workflow sur la feature branch via GitHub UI / gh CLI.
5. Soleil arbitre le merge (cf. mémoire feedback_merge_autonomy.md : merge possible
   par Code si PR solide, sinon demander).
6. Le run scheduled de lundi 8 juin 8h UTC tournera sur main — si la PR Phase 1
   n'est pas encore mergée, c'est le code stable actuel qui tourne (filet de
   sécurité, aucun risque pour le cron).
```

## NOTES TECHNIQUES PRÉLIMINAIRES

### Format des bodies Scholar Alerts

Le body texte des alertes Scholar suit une structure régulière (vue dans le snippet MCP) :

```
[HTML|PDF|TXT] Title of the paper
First-Initial. Last-Author, Other Authors - Journal name, Year ... snippet
```

Parser de référence pour Phase 1 :
- Découpage du body sur blocs de 2-3 lignes par référence (Scholar Alerts groupe 5-10 résultats par mail).
- Regex sur la ligne d'auteurs : `[A-Z]\. [A-Z][a-zàâäéèêëïîôöùûüç]+(?:, [A-Z]\. [A-Z]...)+ - (.+), (\d{4})` (approximatif).
- Premier auteur = premier match sur l'auteur initial.
- DOI : regex `10\.\d{4,9}/[^\s\"<>]+` (cf. verify_citation.py L52).
- URL Scholar : extraction de href dans le body HTML si dispo (sinon nada — Scholar Alerts ne pousse pas systématiquement de DOI).

Tolérance d'erreur acceptée : 10-15% de parsing imparfait. Une référence qui ne parse pas passe à Claude telle quelle (failsafe).

### Hash dédup

```python
import hashlib, re

def dedup_key(title: str, first_author: str) -> str:
    norm_title = re.sub(r"\s+", " ", title.lower().strip())
    norm_title = re.sub(r"[^\w\s]", "", norm_title)
    norm_author = first_author.lower().strip()
    return hashlib.sha1(f"{norm_title}|{norm_author}".encode()).hexdigest()
```

### Import verify_citation depuis veille_scholar.py

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import verify_citation  # importe le module du repo public
```

(Le `actions/checkout@v5` du workflow checkout `dellahstella/tellux` complet, donc `scripts/verify_citation.py` est accessible depuis `.github/scripts/`.)

## CONDITION D'ARRÊT EXPLICITE

L'évaluateur ne propose **jamais** de correctif (§2 du protocole). Si l'itération échoue 3 fois consécutives avec amélioration < 0.3, escalade Soleil + `RAPPORT_FINAL.md`. La Phase 1 reste sur la feature branch, pas de merge sur main avant feu vert.

---

*Contrat d'itération Phase 1 — autonome (Code arbitre seul tant que le scope du contrat est respecté). À publier dans le commit Phase 1 sur `feat/veille-scholar-2026-06-08`.*
