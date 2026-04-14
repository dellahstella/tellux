# TELLUX — Instructions projet pour les sessions Claude

**Mise à jour :** 14 avril 2026
**Usage :** Ce fichier est lu en début de chaque session. Il contient les règles de conduite impératives. Ces règles s'appliquent à tous les modèles (Opus, Sonnet, Haiku).

---

## 1. Fichier HTML canonique — règle absolue

**Source unique : `index.html` à la racine du repo `dellahstella/tellux`.**

C'est le fichier servi par Cloudflare Pages sur `tellux.pages.dev`. Il n'existe plus de fichiers HTML parallèles (`tellux_CORRECT.html`, `tellux_v6_design.html`, `tellux.html` ont tous été supprimés le 14 avril 2026 pour éliminer les risques de divergence).

**Règles :**
- Ne jamais créer de fichier HTML alternatif "de travail" sur le repo. Si une expérimentation est nécessaire, elle se fait en branche dev ou en local, jamais comme second fichier sur main.
- Toujours lire la zone à modifier avant de toucher au code.
- Toujours vérifier que les fonctions voisines ne sont pas cassées après modification (grep des noms de fonction touchés).

---

## 2. Workflow GitHub — qui fait quoi

Le repo est `dellahstella/tellux`, branche par défaut `main`. Cloudflare Pages déploie automatiquement à chaque push sur `main`. Le compte Soleil est sur le plan Claude max, donc le budget de contexte n'est plus un facteur limitant — Claude peut lire largement sans rationnement.

**Claude (via MCP GitHub) — autorisé à faire en autonomie :**
- Lecture de tous les fichiers du repo (`get_file_contents`)
- Lecture de l'historique (`list_commits`, `get_commit`)
- Audit, vérification d'état, comparaison de versions
- Lecture complète d'`index.html` quand un audit ou une modification le justifie

**Claude — limites actuelles :**
- Le PAT GitHub configuré est en lecture seule. Claude ne peut pas pousser de commits via le MCP. Toute écriture passe par Soleil via l'interface web GitHub.
- Si plus tard le PAT est régénéré en mode écriture, Claude pourra committer directement les petits fichiers (`.md`, `.json`, scripts).

**Soleil — workflow d'écriture :**
- Édition directe via l'interface web GitHub (icône crayon ✏️ sur le fichier)
- Pour les gros patches préparés par Claude : copier-coller dans l'éditeur web GitHub
- Suppressions / renommages : via l'interface web (icône poubelle 🗑️ ou édition du chemin du fichier)
- Éviter Git en ligne de commande / Bash sauf si le repo est cloné localement et le contexte connu

**Convention de commit :**
- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `refactor:` réorganisation sans changement fonctionnel
- `data:` mise à jour de corpus, sites, hypothèses
- `docs:` documentation, README, fichiers `.md`
- `chore:` maintenance, suppression de fichiers obsolètes

---

## 3. Audit d'état HTML obligatoire en début de session technique

Avant toute modification de `index.html`, Claude exécute un audit d'état :
1. `get_file_contents` sur `index.html` pour récupérer le SHA blob actuel
2. Comparer ce SHA et le contenu visible aux références mémoire (recovery, dernier état documenté)
3. Si écart inattendu : alerter Soleil avant toute modification, attendre confirmation

Aucune modification silencieuse sur un fichier dont l'état n'a pas été validé.

---

## 4. Workflow modification code (pattern éprouvé)

1. **Audit d'état** (voir §3)
2. **Lecture** de la zone à modifier — large si nécessaire, le contexte n'est pas rationné
3. **Patch préparé** : Python `str.replace(old, new, 1)` est plus fiable que les outils de remplacement automatique sur ce gros fichier (caractères spéciaux, multilignes, HTML entities)
4. **Validation JS** : extraire les blocs `<script>`, écrire dans `/tmp/test.js`, lancer `node --check`. **Obligatoire avant de rendre la main.**
5. **Livraison** : Claude prépare le contenu, Soleil le copie-colle dans l'éditeur web GitHub (tant que le PAT reste en lecture seule)
6. **Vérification post-déploiement** : Claude relit `index.html` après commit pour confirmer que le SHA correspond à ce qui était attendu

**Ne jamais reporter "c'est fait" sans `node --check` passé.**

Si erreur de parsing : diagnostiquer, ne pas livrer un fichier cassé.

---

## 5. Garde-fous domaine

### Ce que Tellux est
Un outil de cartographie et de visualisation des champs électromagnétiques en Corse, avec un module patrimoine (sites mégalithiques, églises romanes, alignements) et un module agronomie (diagnostic parcellaire).

### Ce que Tellux n'est pas
- Un outil de diagnostic médical
- Un substitut à des mesures professionnelles certifiées
- Un système de prédiction ou d'alerte EM
- Un outil de géobiologie ésotérique

### Position épistémique (obligatoire)
Lire `TELLUX_POSITION_EPISTEMIQUE.md` avant toute rédaction de contenu textuel.

**3 formulations interdites :**
1. "deux réalités différentes" (le champ EM est un seul champ physique)
2. "les mesures ne s'additionnent pas" (elles s'additionnent vectoriellement — superposition)
3. "naturel = bénin" (les perturbations géologiques ne sont pas intrinsèquement inoffensives)

### Géographie & corpus
- **Monte d'Oro** (~41.99°N, 9.12°E) = centre géométrique des mégalithes (pas Vizzavona)
- Ratio heritage/électrique dans `calcHuman()` : ~1:10 à 1:20. Ne pas double-compter entre `PROD_ELECTRIQUE` et `SITES` hydrauliques
- GPS : déférer à Soleil en cas de doute. Ne jamais "corriger" des coordonnées sans source explicite
- Pas de figures humaines inventées (équipes, partenaires, individus) à moins que Soleil les ait nommées dans la conversation en cours

### Code
- Unicode : jamais de guillemets courbes (U+2018/U+2019) dans les string literals JS
- Pas de zèle : ne pas ajouter de features non demandées
- Pas de "nettoyage" de code que Soleil n'a pas demandé de toucher
- Pas de dépendances externes (CDN) sans demander

---

## 6. Choix de modèle (pour Soleil)

| Tâche | Modèle optimal |
|---|---|
| Refactors gros HTML, patches complexes, debug JS | **Sonnet 4.6** |
| Patches courts ciblés, corrections GPS, ajouts simples | **Haiku 4.5** |
| Réflexion stratégique, architecture, rédaction dossier | **Opus 4.6** |
| Revue candidature, direction artistique, long terme | **Opus 4.6** |

**Ne pas paralléliser Haiku et Sonnet sur le même fichier** — cause de conflits déjà vécus.

---

## 7. Voie A / Voie B

- **Voie A** = livraison immédiate, gel v6 (stable, déployée, envoi partenaires, dépôt CTC)
- **Voie B** = montée en gamme horizon 3-6 mois (landing Framer, N8N, migration modulaire, clustering contributions, polygones zones, etc.)

**Ne jamais inverser.** En session voie A, ne pas embarquer de chantiers voie B.

**Ticket B-ZONES (voie B)** : sites étendus (Scandola, Désert des Agriates, Anneaux du Cap Corse, forêts, gorges, massifs) actuellement représentés par un pin unique alors qu'ils couvrent des dizaines de km². À traiter en session dédiée : polygones Leaflet ou cercles d'extension + récupération géométries officielles (INPN pour réserves, OSM pour massifs). Flag `"zone": true` dans `SITES_REFERENCE.json` pour identification future.

---

## 8. Candidature CTC

- Cible = CTC (Collectivité de Corse). Pas OEC, pas ADEME, sauf mention explicite
- Projet **solo** (Soleil). Pas d'embauche mentionnée
- Financement = logement + temps de travail + matériel de mesure + prestations extérieures pour mesures de validation indépendantes
- Les mesures pour crédibilité scientifique sont faites par des **tiers extérieurs** (association CEM, laboratoire). Ne jamais rédiger comme si Soleil faisait lui-même les mesures de validation
- Toute modification du projet doit rester cohérente avec les arguments du dossier `CANDIDATURE_TELLUX_v7.docx`

---

## 9. Refus et limites

Claude doit refuser de :

- Modifier le code sans avoir lu la zone concernée
- Rendre un fichier sans `node --check` passé
- Ajouter des sites au corpus sans source vérifiable
- Rédiger du contenu qui contrevient à la position épistémique
- Promettre des capacités que Tellux n'a pas (diagnostic santé, prédiction)
- Ajouter des dépendances externes (CDN) sans demander
- "Nettoyer" du code que Soleil n'a pas demandé de toucher
- Produire des fichiers livrables en doublon (si on produit un roadmap, on ne produit pas aussi un "plan d'action" séparé)
- Réécrire le HTML sans avoir lu la zone cible

---

## 10. Patterns techniques à respecter

- **`L.rectangle`** : toujours `interactive: false` (sinon bloque les clics carte)
- **FAB mesure** : appeler `startContribFromFAB()`, avec `map.once('click')` dans `setTimeout(0)`
- **Palette DA v2** : Ardoise #1F2329, Pierre #F5F0E7, Maquis #3F5B3A, Ocre #C28533, Porphyre #8E2F1F, Tyrrhénien #1F3A5F
- **Typographie** : Fraunces (titres), IBM Plex Sans (corps)
- **Hébergement** : Cloudflare Pages (`tellux.pages.dev`), repo `dellahstella/tellux`. Backup GitLab. Pas Netlify
- **Backend** : Supabase. Migrations versionnées dans `_migrations/`
- **DA v2 gelée** : ne pas revisiter en voie A

---

## 11. Fin de session

Produire un recovery `.md` **uniquement si** :
- plus de 5 modifications substantielles dans la session, OU
- Soleil le demande, OU
- un bug non résolu doit être transmis à la session suivante

Sinon : réponse courte de clôture, c'est tout.

Ne pas créer de fichiers markdown redondants — mettre à jour les existants quand c'est possible.
