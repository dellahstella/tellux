# Corpus scientifique vivant — Tellux Corse

## Objet

Ce dossier `_corpus/` contient la matière scientifique qui fonde le projet Tellux : une cartographie progressive des études sur les champs électromagnétiques et leurs interactions avec les systèmes biologiques, les ressources naturelles, et les territoires. Ce n'est pas une archive passive, mais un corpus vivant qui s'enrichit au fil des itérations du projet et alimente directement les hypothèses de travail en phase 2 et 3.

## Organisation à trois niveaux

**1. Documentation scientifique par axe** (`axes/`)
- Fiches de recherche structurées par domaine (A : conscience EM, B : thérapeutiques, C : résonances, etc.)
- Chaque fiche est le résultat d'une session Cowork : question de recherche spécifiée, littérature peer-reviewed intégrée, contradictions identifiées
- Format : fiche autonome, ~1500-2500 lignes, consommable indépendamment
- Convention de nommage : `AXE_<LETTRE>_<SLUG>.md` (ex. `AXE_A_CONSCIENCE_EM.md`)

**2. Cartographie des tensions** (`tensions/`, `TENSIONS.md`)
- Identifie les contradictions et débats ouverts du corpus
- Croise les axes : quelle tension se retrouve dans A ET C ? Quels axes la résolvent ou l'aggravent ?
- Chaque tension a un statut épistémique (non résolue, en cours de résolution, structurelle, résolue)
- Implications explicitées pour l'architecture Tellux

**3. Hypothèses novatrices** (`hypotheses/`, `HYPOTHESES.md`)
- Énoncés générés ou affinés par Tellux à partir du corpus
- Distingue entre hypothèses formulées et hypothèses testables
- Traçabilité : d'où vient l'hypothèse, quelles données la testeraient, comment Tellux peut y répondre en phases 2-3

## Règles de mise à jour

1. **Nouvelle fiche d'axe** : placer dans `axes/` avec nommage `AXE_<LETTRE>_<SLUG>.md`, mettre à jour `INDEX.md`
2. **Nouvelle tension identifiée** : ajouter un résumé dans `TENSIONS.md` ; si complexe (>3 axes, analyse détaillée requise), créer `tensions/TENSION_<SLUG>.md`
3. **Nouvelle hypothèse** : ajouter dans `HYPOTHESES.md` ; si elle développe un protocole de test, créer `hypotheses/HYPOTHESE_<SLUG>.md`
4. **Mise à jour INDEX/TENSIONS/HYPOTHESES** : mettre à jour compteurs et dates de révision ; chaque révision est tracée dans ce corpus

## État actuel (2026-04-19)

- **Axes A-G** : briefs produits côté Soleil, à copier manière à être intégrés dans `axes/`
- **Axes H-I-J** : briefs prêts (H EM participative, I modèle de score, J autres), exécution Cowork à venir
- **Tensions** : 8 tensions pré-identifiées en structure (voir `TENSIONS.md`), détails à documenter au fur et à mesure
- **Hypothèses** : 3 hypothèses Tellux en structure (voir `HYPOTHESES.md`), testabilité à affiner

## Convention de nommage et langue

- **Langue** : français uniquement (titres, slugs, contenu)
- **Slugs** : minuscules, tirets (pas d'accents)
- **Dates** : ISO 8601 (YYYY-MM-DD)
- **Métadonnées** : chaque fiche inclut date, auteur corpus, statut de version

## Licence et diffusion

Ce corpus est usage interne au projet Tellux. Aucune diffusion, publication, ou utilisation externe sans accord explicite de Soleil Mazzucatto. Les fiches de recherche peuvent contenir des données préliminaires, des hypothèses non confirmées, et des débats ouverts qui ne reflètent pas nécessairement une position consolidée de Tellux.

---

**Infrastructure créée : 2026-04-19 | Dernière révision : 2026-04-19**
