# Prompt Claude Code — Audit et plan de découpe du monofichier HTML

**Usage :** Copier-coller ce prompt dans une session Claude Code (CLI) avec le dépôt Tellux ouvert.
**Objectif :** Produire un plan de découpe — pas d'exécution, pas de modification de fichier.

---

## Prompt

```
Tu es Claude Code. Tu travailles sur le projet Tellux Corse.

Le fichier `tellux_v6_design.html` à la racine du projet est un monofichier
HTML de ~500 Ko et ~6500 lignes qui contient tout : HTML, CSS, JavaScript,
données JSON en dur, configurations Leaflet, logique métier, UI, gamification.

Ta mission est de produire un PLAN DE DÉCOUPE — tu ne modifies RIEN.
Pas de fichier créé, pas de fichier modifié. Uniquement un document d'analyse.

## Étape 1 — Inventaire structurel

Lis le fichier en entier et produis un inventaire :

1. **Blocs de données en dur** : identifie chaque tableau ou objet JavaScript
   contenant des données qui devraient être externalisées. Cherche notamment :
   - SITES[] (sites mégalithiques)
   - CHURCHES[] (églises romanes)
   - FAILLES_CORSE[] (failles tectoniques)
   - PROD_ELECTRIQUE[] (sites de production électrique)
   - PRECOMPUTED_ALIGNMENTS[] (alignements Broadbent)
   - HYPOTHESES ou tableau d'hypothèses H1-H88
   - INTL_CALIB ou données de calibration
   - Tout autre tableau de données > 50 lignes

   Pour chaque bloc : nom, lignes de début-fin, nombre de lignes,
   taille estimée en Ko, type de données.

2. **Blocs JavaScript fonctionnels** : identifie les groupes de fonctions
   qui forment des modules logiques. Cherche notamment :
   - Fonctions de calcul (calcHuman, calcHeritagePiezo, calcPiezoScore)
   - Fonctions de couches cartographiques (buildXxxLayer pour chaque couche)
   - Fonctions de gamification (runAutoTests, renderHypo, _loadGameState)
   - Fonctions UI (tog, closeLayerPanel, txLegend)
   - Fonctions Supabase (fetch, insert, contributions)
   - Fonctions d'export (exportPermaPDF, etc.)
   - Fonctions popup (buildPopup, etc.)

   Pour chaque groupe : nom proposé du module, fonctions incluses,
   dépendances vers d'autres groupes (variables globales partagées,
   fonctions appelées dans d'autres modules).

3. **Blocs CSS** : identifie les sections de styles.
   Pour chaque section : thème (base/variables, carte, panneaux, légendes,
   mobile, gamification), lignes de début-fin, nombre de lignes.

## Étape 2 — Graphe de dépendances

Produis un graphe simplifié des dépendances entre les modules JS identifiés :
- Quelles variables globales sont partagées ?
- Quelles fonctions appellent des fonctions d'autres modules ?
- Quels modules accèdent au DOM ?
- Quels modules accèdent à la carte Leaflet (variable `map`) ?
- Quels modules accèdent à Supabase ?

Format : liste de dépendances, ex :
  layers/heritage.js → utils/geo.js (appelle calcHeritagePiezo)
  layers/heritage.js → ui/legend.js (appelle txLegend.show)
  layers/heritage.js → data/sites.json (lit SITES[])

## Étape 3 — Plan de découpe en étapes

Propose un plan de migration en étapes ordonnées. Chaque étape doit :
- Produire une version FONCTIONNELLE (pas de cassure intermédiaire)
- Être testable indépendamment
- Minimiser le risque de régression

Ordre recommandé :
1. Extraction des données en JSON (le plus sûr, résout A-1)
2. Extraction du CSS en fichiers séparés
3. Extraction des modules JS couche par couche (du plus indépendant au plus couplé)
4. Configuration Vite (bundler)
5. Tests unitaires sur les fonctions utilitaires

Pour chaque étape : fichier(s) créé(s), modifications dans le HTML,
test de non-régression proposé, estimation de complexité (🟢/🟡/🔴).

## Étape 4 — Données : que garder inline ?

Pour chaque bloc de données identifié en étape 1, recommande :
- EXTERNALISER en JSON/GeoJSON (chargé par fetch, avec fallback inline pour offline)
- GARDER EN DUR (constantes scientifiques, paramètres modèle, données < 1 Ko)
- MIGRER EN BACKEND (données dynamiques, contributions)

Justifie chaque choix en 1 phrase.

## Étape 5 — Risques et garde-fous

Liste les risques de la migration :
- Variables globales qui casseront si on les met dans un module
- Event listeners qui dépendent de l'ordre de chargement du DOM
- Fonctions appelées depuis le HTML (onclick="xxx()") qui ne seront plus
  accessibles dans un module ES
- Dépendances circulaires entre modules

Pour chaque risque : solution proposée.

## Format de sortie

Produis un seul fichier `AUDIT_DECOUPE_RESULTATS.md` dans le dossier
`_prompts_code_claude/` avec toutes les sections ci-dessus. Ne modifie
aucun autre fichier.

## Garde-fous

- NE MODIFIE AUCUN FICHIER existant
- NE CRÉE AUCUN FICHIER de code (.js, .css, .html)
- Produis UNIQUEMENT le document d'analyse
- Si tu n'es pas sûr d'une dépendance, le dire plutôt que de deviner
- Ne touche JAMAIS aux fonctions calcHuman(), calcHeritagePiezo(),
  runAutoTests(), runPermaDiag() — ce sont des zones protégées
- Ne touche JAMAIS aux données SITES[], CHURCHES[], FAILLES_CORSE[],
  PROD_ELECTRIQUE[] — analyse-les mais ne les modifie pas
```

---

## Notes pour Soleil

Ce prompt est conçu pour être utilisé dans Claude Code en CLI (`claude` dans le terminal, depuis la racine du dépôt Tellux). Il produit un document d'analyse sans toucher au code.

Une fois le document `AUDIT_DECOUPE_RESULTATS.md` produit, Soleil le relit et valide ou ajuste le plan. La découpe effective se fait ensuite en sessions séparées, étape par étape, avec tests de non-régression à chaque étape.

**Pré-requis :** Claude Code installé et configuré, dépôt Tellux cloné localement, `tellux_v6_design.html` à la racine.
