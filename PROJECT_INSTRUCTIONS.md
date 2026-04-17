# TELLUX — Instructions projet pour les sessions Claude

**Mise à jour :** 14 avril 2026
**Usage :** Ce fichier est lu en début de chaque session Claude (claude.ai web, Cowork, Claude Code). Il contient les règles de conduite impératives. Il est divisé en deux parties : (A) règles communes à tous les environnements, (B) règles spécifiques par environnement.

---

# PARTIE A — Règles communes à toutes les sessions Claude

## A.1 Source unique du code

**Fichier canonique : `index.html` à la racine du repo `dellahstella/tellux` sur GitHub.**

C'est le fichier servi en production sur `tellux.pages.dev`. Aucun autre fichier HTML ne fait foi.
**Usage :** Ce fichier est lu en début de chaque session. Il contient les règles de conduite impératives. Ces règles s'appliquent à tous les modèles (Opus, Sonnet, Haiku).

---

## 1. Fichier HTML canonique — règle absolue

**Source unique : `index.html` à la racine du repo `dellahstella/tellux`.**

C'est le fichier servi par Cloudflare Pages sur `tellux.pages.dev`. Il n'existe plus de fichiers HTML parallèles (`tellux_CORRECT.html`, `tellux_v6_design.html`, `tellux.html` ont tous été supprimés le 14 avril 2026 pour éliminer les risques de divergence).

**Règles :**
- Ne jamais créer de fichier HTML alternatif "de travail" sur le repo. Si une expérimentation est nécessaire, elle se fait en branche dev ou en local, jamais comme second fichier sur main.
- Toujours lire la zone à modifier avant de toucher au code.
- Toujours vérifier que les fonctions voisines ne sont pas cassées après modification (grep des noms de fonction touchés).

Les fichiers HTML parallèles (`tellux_CORRECT.html`, `tellux_v6_design.html`, `tellux.html`, `TELLUX_LOGO_V7.html`) ont été supprimés du repo le 14 avril 2026 pour éliminer les risques de divergence. **Ils ne doivent pas être recréés.** Si une expérimentation est nécessaire, elle se fait en branche dédiée (`exp/...`, `wip/...`), jamais comme fichier parallèle sur `main` ou `dev`.

## A.2 Repo et branches

**Remote unique : GitHub.** Le repo officiel est `https://github.com/dellahstella/tellux`. Un ancien remote GitLab (`gitlab.com/dellahstella/tellux`) existe encore en ligne mais n'est plus utilisé depuis le 14 avril 2026. Ne pas le rebrancher comme remote sans décision explicite de Soleil.

**Branches actives :**
- `main` — production. Servie par Cloudflare Workers sur `tellux.pages.dev`. Ne reçoit que des merges de PR validées manuellement par Soleil.
- `dev` — branche de travail courante. Reçoit les fixes et features avant validation pour `main`.
- Branches éphémères `fix/...`, `chore/...`, `feat/...`, `exp/...`, `wip/...` — créées pour des PRs ciblées, mergées dans `dev`, supprimées après merge.
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

**Convention de commit (obligatoire) :**
- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `refactor:` réorganisation sans changement fonctionnel
- `data:` mise à jour de corpus, sites, hypothèses
- `docs:` documentation, README, fichiers `.md`
- `chore:` maintenance, suppression de fichiers obsolètes
- `wip:` work in progress (à éviter sur `dev` et `main`, accepté sur branches éphémères)

## A.3 Hébergement et déploiement

**Cloudflare Workers** sert `tellux.pages.dev`. Le projet est configuré comme **Worker static-assets** (pas Pages classique) via `wrangler.jsonc` à la racine du repo.

Contenu de référence de `wrangler.jsonc` :
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

    {
      "name": "tellux",
      "compatibility_date": "2026-04-14",
      "assets": {
        "directory": "."
      }
    }

Le Worker s'appelle `tellux` sur le compte Cloudflare de Soleil (`Stelladluca@proton.me`). Tout push sur GitHub déclenche un build automatique. Les builds sur les PRs créent des **preview deployments** accessibles via une URL distincte de `tellux.pages.dev`, utiles pour valider une PR avant merge.

**Ne jamais modifier `wrangler.jsonc` sans raison documentée.** Si une migration vers Cloudflare Pages classique ou un autre hébergement est envisagée, c'est une décision projet, pas une décision de session.

## A.4 Backend Supabase

Le backend du projet est **Supabase** (PostgreSQL + RLS). Les migrations SQL sont versionnées dans le dossier `_migrations/` du repo, numérotées (`001_...sql`, `002_...sql`, etc.). Toute modification de schéma doit produire un nouveau fichier migration, jamais modifier les anciennes.

Les credentials Supabase ne doivent **jamais** être collés dans le chat, dans un fichier markdown, dans un commit, ou dans un prompt Claude Code. Elles vivent uniquement dans les variables d'environnement Cloudflare et le dashboard Supabase.

## A.5 Garde-fous domaine
## 5. Garde-fous domaine

### Ce que Tellux est
Un outil de cartographie et de visualisation des champs électromagnétiques en Corse, avec un module patrimoine (sites mégalithiques, églises romanes, alignements) et un module agronomie (diagnostic parcellaire).

### Ce que Tellux n'est pas
- Un outil de diagnostic médical
- Un substitut à des mesures professionnelles certifiées
- Un système de prédiction ou d'alerte EM
- Un outil de géobiologie ésotérique

### Position épistémique (obligatoire)
Lire `TELLUX_POSITION_EPISTEMIQUE.md` avant toute rédaction de contenu textuel destiné à un public extérieur (assos EM, mairies, scientifiques, dossier CTC).

**3 formulations interdites dans tout le projet :**
1. *"deux réalités différentes"* — le champ EM est un seul champ physique, pas deux mondes parallèles
2. *"les mesures ne s'additionnent pas"* — elles s'additionnent vectoriellement (principe de superposition)
3. *"naturel = bénin"* — les perturbations géologiques ne sont pas intrinsèquement inoffensives

### Géographie et corpus
- **Monte d'Oro** (~41.99N, 9.12E) = centre géométrique des mégalithes (pas Vizzavona)
- Ratio heritage/électrique dans `calcHuman()` : ~1:10 à 1:20. Ne pas double-compter entre `PROD_ELECTRIQUE` et `SITES` hydrauliques
- GPS : déférer à Soleil en cas de doute. **Ne jamais "corriger" des coordonnées sans source explicite.**
- Pas de figures humaines inventées (équipes, partenaires, individus) à moins que Soleil les ait nommées dans la conversation en cours

### Code
- Unicode : jamais de guillemets courbes (U+2018/U+2019) dans les string literals JS
- Pas de zèle : ne pas ajouter de features non demandées
- Pas de "nettoyage" de code que Soleil n'a pas demandé de toucher
- Pas de dépendances externes (CDN) sans validation explicite

## A.6 Voie A / Voie B

- **Voie A** = livraison immédiate, gel v6 (stable, déployée, envoi partenaires, dépôt CTC)
- **Voie B** = montée en gamme horizon 3-6 mois (landing Framer, n8n, migration modulaire, contributions utilisateurs, polygones zones, etc.)
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

**Ne jamais inverser.** En session voie A, ne pas embarquer de chantiers voie B sous prétexte que "ce serait plus propre".

## A.7 Candidature CTC

- Cible = **CTC (Collectivité de Corse)**. Pas OEC, pas ADEME, sauf mention explicite de Soleil
- Projet **solo** (Soleil). Pas d'embauche mentionnée
- Financement = logement + temps de travail + matériel de mesure + prestations extérieures pour mesures de validation indépendantes
- Les mesures pour crédibilité scientifique sont faites par des **tiers extérieurs** (association CEM, laboratoire). Ne jamais rédiger comme si Soleil faisait lui-même les mesures de validation
- Toute modification du projet doit rester cohérente avec les arguments du dossier `CANDIDATURE_TELLUX_v7.docx`
## 7. Voie A / Voie B

- **Voie A** = livraison immédiate, gel v6 (stable, déployée, envoi partenaires, dépôt CTC)
- **Voie B** = montée en gamme horizon 3-6 mois (landing Framer, N8N, migration modulaire, clustering contributions, polygones zones, etc.)

**Ne jamais inverser.** En session voie A, ne pas embarquer de chantiers voie B.

**Ticket B-ZONES (voie B)** : sites étendus (Scandola, Désert des Agriates, Anneaux du Cap Corse, forêts, gorges, massifs) actuellement représentés par un pin unique alors qu'ils couvrent des dizaines de km². À traiter en session dédiée : polygones Leaflet ou cercles d'extension + récupération géométries officielles (INPN pour réserves, OSM pour massifs). Flag `"zone": true` dans `SITES_REFERENCE.json` pour identification future.

## A.8 Position sur le contexte : fin de l'économie de tokens

**Le contexte n'est plus rationné.** Soleil est sur un compte Claude Max. Les anciennes instructions projet contenaient des consignes d'économie de tokens (lire le minimum, ne pas relire un fichier déjà ouvert, privilégier des modifications partielles). Ces consignes sont désormais **obsolètes et activement nuisibles** : elles ont conduit à des sessions qui modifient du code sans le lire en entier, à des assomptions non vérifiées, et à des bugs silencieux.

**Règle nouvelle, qui prime sur tout le reste :**
- Lire largement avant de modifier. Lire le fichier entier si nécessaire.
- Vérifier la zone à modifier ET son contexte (au moins 50 lignes avant et après).
- Vérifier que les fonctions appelées existent et n'ont pas changé de signature.
- Ne jamais "deviner" la structure d'une fonction. La lire.
- Si une vérification semble redondante, la faire quand même. Le coût en tokens est nul. Le coût d'une erreur silencieuse est élevé.

## A.9 Refus et limites

Toute session Claude doit refuser de :

- Modifier le code sans avoir lu la zone concernée
- Rendre un fichier sans validation JS passée (sessions code uniquement)
- Ajouter des sites au corpus sans source vérifiable
- Rédiger du contenu qui contrevient à la position épistémique
- Promettre des capacités que Tellux n'a pas (diagnostic santé, prédiction)
- Ajouter des dépendances externes (CDN) sans validation explicite
- "Nettoyer" du code que Soleil n'a pas demandé de toucher
- Produire des fichiers livrables en doublon (si on produit un roadmap, on ne produit pas aussi un "plan d'action" séparé)
- Réécrire le HTML sans avoir lu la zone cible
- Coller des credentials (clés API, tokens, mots de passe) dans le chat ou dans un commit

## A.10 Patterns techniques à respecter

- **`L.rectangle`** : toujours `interactive: false` (sinon bloque les clics carte)
- **FAB mesure** : appeler `startContribFromFAB()`, avec `map.once('click')` dans `setTimeout(0)`
- **Palette DA v2** : Ardoise #1F2329, Pierre #F5F0E7, Maquis #3F5B3A, Ocre #C28533, Porphyre #8E2F1F, Tyrrhénien #1F3A5F
- **Typographie** : Fraunces (titres), IBM Plex Sans (corps)
- **DA v2 gelée** : ne pas revisiter en voie A

## A.11 Test local avant push de PR

Toute modification du HTML qui implique un fetch (JSON, données externes) ne peut PAS être testée en ouvrant index.html directement dans le navigateur via file://. Les navigateurs bloquent les requêtes fetch en protocole file pour raisons de sécurité. Le fetch échoue silencieusement et le code tombe en fallback (ou crashe).

**Workflow de test local obligatoire :**

1. Dans Git Bash, se placer dans le dossier du repo Tellux :

       cd /c/Users/lucas/Documents/Claude/Projects/Tellux

   Vérifier qu'on est au bon endroit avec `ls` — on doit voir index.html, _data/, _scripts/, wrangler.jsonc.

2. Lancer un serveur HTTP local :

       python -m http.server 8000

   (Si Python absent : `npx serve .` ou `php -S localhost:8000`)

3. Ouvrir http://localhost:8000/ dans le navigateur. Tellux doit s'afficher comme en production.

4. Tester la fonctionnalité modifiée. Ouvrir la console développeur (F12) et vérifier l'absence d'erreurs rouges. Pour les fetch, vérifier dans l'onglet Network le statut HTTP 200 et la taille du fichier reçu.

5. Une fois validé en local, push de la branche, création de la PR, vérification sur le preview Cloudflare (URL dans le commentaire automatique de la PR), puis merge.

**Règle :** ne JAMAIS merger une PR qui touche au comportement du HTML sans avoir validé soit en local (serveur HTTP), soit sur le preview Cloudflare. Le merge à l'aveugle dans dev est tolérable pour de la doc pure ; il est interdit pour du code.

**Optionnel — alias bash pour gagner du temps :**
Ajouter dans ~/.bashrc :

    alias tellux='cd /c/Users/lucas/Documents/Claude/Projects/Tellux'
    alias telluxserve='cd /c/Users/lucas/Documents/Claude/Projects/Tellux && python -m http.server 8000'

Puis `source ~/.bashrc`. Après ça, taper `telluxserve` lance le serveur en une commande.

---

# PARTIE B — Règles spécifiques par environnement

## B.1 Sessions claude.ai web (chat avec Soleil)

**Modèle typique :** Opus 4.6 (réflexion stratégique) ou Sonnet 4.6 (rédaction lourde).
**Outils disponibles :** lecture du repo via connecteur GitHub si actif, lecture des fichiers projet via `/mnt/project/`, web search, connecteurs MCP (Cloudflare, Supabase, n8n).
**Ce qui n'est PAS disponible :** modification directe du code (Claude ne peut pas committer/pousser depuis le chat), exécution de commandes shell, validation JS via `node --check`.

**Rôle des sessions web :**
- Réflexion stratégique, arbitrages roadmap, audits projet
- Rédaction de contenus textuels (emails, dossiers, kits assos, documentation)
- Préparation de prompts structurés pour Claude Code et Cowork
- Discussion des décisions de conception
- Visualisations, recherche web, audit des fichiers projet via /mnt/project/

**Ce que les sessions web ne doivent PAS faire :**
- Préparer des "patches HTML à coller dans GitHub" — c'est le rôle de Claude Code, qui le fera mieux en lisant le vrai fichier sur disque
- Promettre des modifications de code qu'elles ne peuvent pas exécuter elles-mêmes
- Tenter de deviner l'état du repo sans utiliser les connecteurs disponibles
- Sauter les vérifications "pour gagner du temps" sur des opérations destructrices

## B.1.bis Posture pédagogique des sessions claude.ai web

Soleil n'est pas développeur professionnel. Les sessions claude.ai web doivent adopter une posture pédagogique constante :

- **Donner les commandes complètes à chaque fois.** Ne jamais écrire "tu connais la procédure" ou "comme d'habitude". Recopier la commande, expliquer ce qu'elle fait, signaler les pièges connus.
- **Expliquer pourquoi avant de dire quoi faire.** Le contexte aide Soleil à comprendre ce qu'il fait, pas juste exécuter.
- **Anticiper les frictions.** Si une commande peut produire un message d'erreur courant (404 Cloudflare le temps de la propagation, file:// qui bloque les fetch, gh non installé), le mentionner avant que Soleil tombe dessus.
- **Ne jamais reprocher l'oubli d'une étape vue précédemment.** Si une étape manque, la rappeler simplement, sans formulation qui suggère que Soleil aurait dû s'en souvenir.
- **Distinguer ce qui est obligatoire de ce qui est optionnel.** Marquer clairement les étapes "obligatoires" et celles qui sont "pour gagner du temps plus tard".

Cette posture vaut aussi pour les sessions Cowork et Claude Code dans leurs rapports finaux à Soleil : un rapport doit dire ce qui a été fait, ce qui reste à faire côté Soleil, et comment exactement le faire (commandes, URL à cliquer, choix à valider).

## B.2 Sessions Cowork (Sonnet via interface dédiée)

**Modèle :** Sonnet 4.6 généralement, parfois Opus 4.6 pour gros refactors.
**Outils disponibles :** lecture/écriture de fichiers locaux dans le dossier de travail, exécution de code, accès navigateur.
**Spécificité :** Cowork travaille sur les fichiers **locaux** du dossier projet. Pas directement sur le repo git distant. Les modifications sont visibles dans Cowork et synchronisées avec le filesystem local, mais ne sont pas automatiquement committées ni poussées sur GitHub.

**Rôle des sessions Cowork :**
- Édition ciblée de fichiers locaux (HTML, JSON, scripts)
- Exécution et test de code dans un environnement contrôlé
- Génération d'artefacts locaux (rapports, audits, visuels)

**Workflow Cowork avec git :**
- Cowork modifie les fichiers locaux
- Soleil ou Claude Code prend ensuite le relais pour committer et pousser sur GitHub
- Cowork peut faire des commits simples (sauvegarde de travail), mais pas de push sur des branches partagées sans validation

**A éviter en Cowork :**
- Modification de fichiers HTML canoniques sans vérification préalable de la version git actuelle (risque de partir d'un fichier obsolète)
- Création de fichiers parallèles "de travail" qui ne seront jamais nettoyés
- Exécution de scripts longs qui consomment du budget de session

## B.3 Sessions Claude Code (CLI local)

**Environnement :** terminal local de Soleil (Windows / Git Bash), installé via Anthropic CLI.
**Modèle :** dépend de la session, généralement Sonnet ou Opus selon la complexité.
**Outils disponibles :** filesystem complet, git, exécution de commandes shell, validation Node.js, accès Internet.
**Compte :** Claude Max — aucune contrainte de tokens. Lire largement, vérifier tout.

### Workflow standard

1. **Audit d'état au démarrage** (obligatoire pour toute session technique sur le code)
   - `git status` — working directory clean ?
   - `git branch --show-current` — sur quelle branche ?
   - `git fetch origin` — état du remote
   - `git log --oneline -5` — derniers commits
   - Si quelque chose semble inattendu, STOP et signaler à Soleil avant toute modification.

2. **Lecture avant modification** (obligatoire)
   - Lire le fichier cible en entier ou au minimum la zone large autour de la modification
   - Grep des fonctions et identifiants concernés pour vérifier qu'ils existent et n'ont pas bougé
   - Si le fichier dépasse la capacité d'une seule lecture, le découper proprement

3. **Plan d'édition explicite avant action pour les modifications substantielles**
   - Lister les modifications à apporter avec numéros de ligne et nature
   - Présenter ce plan à Soleil et attendre validation avant d'appliquer, pour les changements de logique métier
   - Pour les petits fix ciblés (typo, valeur numérique, constante), plan d'édition non requis, aller directement à la modification

4. **Modification ciblée**
   - Utiliser `str_replace` (ou équivalent) plutôt que réécriture complète du fichier
   - Une modification = un objectif clair
   - Pas de "nettoyage opportuniste" non demandé

5. **Validation JS obligatoire** pour toute modification du HTML canonique
   - Extraire les blocs `<script>` du HTML
   - Lancer `node --check` sur le résultat
   - Si erreur de parsing, STOP, ne pas livrer un fichier cassé

6. **Commit atomique et push direct sur branche éphémère**
   - Un commit = un objectif. Ne pas mélanger un fix et un refactor dans le même commit.
   - Message de commit suivant la convention (section A.2)
   - Vérifier `git status` avant commit pour s'assurer qu'aucun fichier non voulu n'est inclus
   - Push direct sans demander sur la branche éphémère de travail (`fix/...`, `chore/...`, `feat/...`, `exp/...`)
   - Pas besoin de validation Soleil pour un commit/push sur une branche de travail. C'est le mode normal.

7. **Workflow de merge selon la cible**

   **Pour merger une branche éphémère dans `dev`** : Claude Code peut le faire directement si la PR est triviale (chore, docs, fix mineur sans changement de comportement). Pour les PRs plus substantielles (feat, refactor, modification de logique métier), créer la PR et attendre validation Soleil avant de merger.

   **Pour merger `dev` dans `main`** : JAMAIS automatique. `main` = production, déployée par Cloudflare sur `tellux.pages.dev`. Toute PR `dev -> main` doit être créée puis mergée par Soleil uniquement. Claude Code ne merge jamais sur `main` lui-même.

   **Push direct sur `main`** : interdit dans tous les cas, même par Soleil. Toute modification de `main` passe par PR depuis `dev`. Une protection de branche GitHub doit être activée pour empêcher techniquement les push directs.

### Règles strictes pour Claude Code

- Pas de `git push --force` sans demande explicite, jamais sur `dev` ou `main`
- Pas de `git rebase` interactif sans validation, sauf sur les branches éphémères personnelles
- Pas de suppression de branche (`git branch -d` ou `-D`) sans audit préalable du contenu de la branche, même pour les éphémères
- Pas de modification de fichiers en dehors du périmètre demandé — si une modif "logique" semble nécessaire ailleurs, signaler et demander
- Pas d'auto-validation ("c'est fait") sans avoir effectivement vérifié dans un navigateur ou via tests
- Toujours signaler les fichiers untracked en fin de session plutôt que de les commiter automatiquement
- Jamais de merge ou push direct sur `main`, même avec autorisation de Soleil dans le chat

### Format des prompts Claude Code préparés en session web

Quand une session web prépare un prompt Claude Code, ce prompt doit contenir :

1. **OBJECTIF** — une phrase qui résume ce qu'on veut obtenir
2. **CONTEXTE** — pourquoi on fait ça, quels fichiers sont concernés
3. **MODE** — strictement read-only ou modification autorisée, et sur quoi
4. **ETAPES NUMEROTEES** — chaque action à faire, dans l'ordre
5. **REGLES STRICTES** — ce qui est interdit, en bullet points
6. **POINT DE VALIDATION** — où Claude Code doit s'arrêter pour attendre Soleil avant de continuer, s'il y en a un
7. **LIVRABLES ATTENDUS** — fichiers créés, commits, PRs, format de rapport final

Plus le prompt est précis, moins il y a de risque d'interprétation libre. Pour les opérations destructrices (suppression, force-push, rebase), expliciter toujours : *"NE FAIS QUE X. NE FAIS PAS Y. ATTENDS validation explicite avant Z."*

---

# Annexe — Fin de session

Produire un recovery `.md` uniquement si :
- plus de 5 modifications substantielles dans la session, OU
- Soleil le demande, OU
- un bug non résolu doit être transmis à la session suivante

Sinon : réponse courte de clôture, c'est tout.

Ne pas créer de fichiers markdown redondants — mettre à jour les existants quand c'est possible.

---

**Fin du fichier d'instructions projet Tellux. Toute session Claude qui démarre sur ce projet doit avoir lu ce fichier en entier avant la première action.**
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
