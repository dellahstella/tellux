# TELLUX — Plan de montée en gamme

**Dernière mise à jour :** 8 avril 2026
**Statut :** Voie B — horizon 3 à 6 mois, démarrage après gel de la voie A.

---

## Vue d'ensemble

Ce document détaille les 6 axes de la montée en gamme du projet Tellux. Chaque axe est actionnable : outils nommés, étapes ordonnées, dépendances explicites, estimé de complexité.

| Axe | Sujet | Complexité | Dépendance |
|---|---|---|---|
| 1 | Exploitation complète de l'écosystème Anthropic | 🟢-🟡 | Voie A livrée |
| 2 | Migration design : landing Framer ou Webflow | 🟡 | DA v2 gelée |
| 3 | Automatisation N8N | 🟡 | Backend Supabase stable |
| 4 | Migration technique du monofichier HTML | 🔴 | Voie A gelée + tests de non-régression |
| 5 | Gouvernance et structure juridique | 🟡 | Arbitrage Soleil |
| 6 | Stratégie de subventions et financement | 🟡 | Structure juridique choisie |

---

## Axe 1 — Exploitation complète de l'écosystème Anthropic

**Complexité :** 🟢 facile à 🟡 moyen selon la profondeur.

### Contexte

Le projet utilise déjà Claude (Cowork) pour le design, le code et la documentation. L'objectif est de systématiser et d'approfondir cette utilisation en exploitant les fonctionnalités avancées de l'écosystème Anthropic : instructions projet persistantes, MCP (Model Context Protocol), Claude Code, mémoire inter-sessions.

### Outils

- **Claude Code** — CLI pour tâches de développement agentic directement dans le terminal.
- **Cowork (Claude Desktop)** — Sessions interactives pour documentation, design, stratégie.
- **MCP Servers** — Connexions persistantes à Supabase, Cloudflare, GitHub, et potentiellement N8N.
- **Instructions projet** — Fichier CLAUDE.md à la racine du dépôt pour guider chaque session.
- **Mémoire auto** — Système de mémoire fichier pour conserver le contexte entre les sessions.

### Étapes

1. **Rédiger un fichier `CLAUDE.md`** à la racine du dépôt Tellux. Ce fichier contiendra : la description du projet, les conventions de code, les décisions gelées, les fichiers clés et leur rôle, les garde-fous (ex : ne jamais modifier les coordonnées GPS sans vérification manuelle). Chaque session Claude Code ou Cowork chargera ces instructions automatiquement.

2. **Configurer les MCP pertinents.** Les connecteurs déjà actifs (Supabase, Cloudflare) doivent être documentés. Ajouter si nécessaire : GitHub (pour les issues et PR), un serveur MCP pour N8N (axe 3), un serveur MCP pour les données brutes locales (dossier `DATA/`).

3. **Établir un workflow de session type.** Avant chaque session de travail, charger le briefing (`TELLUX_BRIEFING.md`), la roadmap (`TELLUX_ROADMAP.md`), et les fichiers pertinents. Utiliser la mémoire auto pour conserver les retours et préférences d'une session à l'autre.

4. **Exploiter Claude Code pour les tâches techniques répétitives.** Exemples : audit de régression GPS (A-1), vérification des patterns couche↔panneau (A-4), génération de captures d'écran, mise à jour du JSON de sites.

5. **Mettre en place des skills personnalisés.** Si des tâches reviennent souvent (ex : « auditer le HTML pour les conflits de z-index », « générer une capture Tellux en mode clair »), créer des skills Cowork dédiés pour les standardiser.

### Dépendances

- Voie A livrée (les instructions projet doivent refléter l'état gelé).
- Accès au dépôt GitHub à jour.

### Livrables

- `CLAUDE.md` à la racine du dépôt.
- Documentation des MCP actifs et de leur usage.
- Au moins 2 skills personnalisés opérationnels.

---

## Axe 2 — Migration design : landing Framer ou Webflow

**Complexité :** 🟡 moyen.

### Contexte

Le projet n'a pas de page d'accueil marketing distincte de l'application cartographique. L'objectif est de créer une landing page professionnelle qui présente Tellux, ses fonctionnalités, son positionnement scientifique, et redirige vers la carte interactive. Cette page servira aussi de vitrine pour les dossiers de financement.

### Outils

- **Framer** — Outil no-code/low-code pour sites marketing. Export statique possible. Bonne gestion des animations et du responsive.
- **Webflow** — Alternative plus mature, plus de contrôle sur le CSS, plan gratuit limité.
- **Figma** — En amont, pour maquetter la landing si nécessaire.
- **Cloudflare Pages** — Hébergement existant, peut servir la landing sur un sous-domaine ou un chemin dédié.

### Étapes

1. **Définir le contenu de la landing.** Pages envisagées : accueil (hero + tagline + CTA), fonctionnalités (couches EM, patrimoine, agronomie), méthodologie scientifique (corpus de 130 études, 80 hypothèses), à propos (porteur, SARL, territoire). Rédiger le copy en français.

2. **Maquetter dans Figma.** Appliquer la direction artistique v2 : palette Tellux, typographies Fraunces / IBM Plex Sans, logo V7. Respecter le positionnement : rigueur scientifique + sensibilité au territoire.

3. **Implémenter dans Framer (choix par défaut) ou Webflow.** Framer est recommandé pour sa rapidité de mise en ligne et ses animations fluides. Si Soleil préfère un contrôle plus fin sur le CSS, passer à Webflow.

4. **Configurer le domaine.** Deux options : (a) sous-domaine `www.tellux.pages.dev` pour la landing, `app.tellux.pages.dev` pour la carte ; (b) domaine personnalisé si budget disponible.

5. **Intégrer les liens croisés.** La landing renvoie vers la carte. La carte conserve un lien « En savoir plus » vers la landing.

6. **Optimiser SEO et accessibilité.** Balises meta, Open Graph, alt text sur les images, scores Lighthouse > 90.

### Dépendances

- DA v2 gelée (c'est le cas).
- Contenu rédactionnel validé par Soleil.
- Choix Framer vs Webflow (décision Soleil).

### Livrables

- Landing page en ligne.
- Maquette Figma archivée.
- Documentation du déploiement et des liens croisés.

---

## Axe 3 — Automatisation N8N

**Complexité :** 🟡 moyen.

### Contexte

Certaines tâches du projet sont répétitives et manuelles : mise à jour des données antennes ANFR, veille réglementaire, notifications de nouvelles mesures citoyennes, export de rapports. N8N est un outil d'automatisation open-source auto-hébergeable qui peut orchestrer ces workflows.

### Outils

- **N8N** — Plateforme d'automatisation de workflows (self-hosted ou cloud). Nœuds HTTP, Supabase, email, Telegram, Webhook.
- **Supabase** — Backend existant, requêtes SQL automatisables via API REST ou nœud Supabase natif N8N.
- **Cloudflare Workers** — Pour des triggers légers (cron) si N8N n'est pas auto-hébergé en permanence.

### Étapes

1. **Recenser les workflows candidats.** Priorité suggérée :
   - Import périodique des données ANFR (antennes relais) depuis l'open data.
   - Notification (email ou Telegram) quand une nouvelle mesure citoyenne est soumise via la carte.
   - Export hebdomadaire d'un résumé des nouvelles données en base (pour suivi projet).
   - Veille automatique sur les publications scientifiques liées aux champs EM et agronomie (via flux RSS ou API).

2. **Choisir le mode d'hébergement N8N.** Deux options : (a) N8N Cloud (plan gratuit limité, rapide à démarrer) ; (b) self-hosted sur un VPS (plus de contrôle, coût mensuel ~5-10 €). Recommandation : démarrer sur N8N Cloud pour le MVP, migrer en self-hosted si les volumes augmentent.

3. **Implémenter le premier workflow** (import ANFR). Ce workflow sert de preuve de concept : trigger cron → HTTP request vers l'API open data → transformation → upsert Supabase.

4. **Tester et monitorer.** Chaque workflow doit avoir un nœud d'erreur qui notifie Soleil (email ou Telegram) en cas d'échec.

5. **Documenter chaque workflow.** Nom, déclencheur, fréquence, données touchées, nœud de notification d'erreur.

### Dépendances

- Backend Supabase stable et API REST activée.
- Données ANFR accessibles en open data (vérifier les endpoints).
- Choix d'hébergement N8N (décision Soleil).

### Livrables

- Instance N8N opérationnelle.
- Au moins 2 workflows actifs (import ANFR + notification mesure citoyenne).
- Documentation des workflows dans un fichier dédié ou dans le README du dépôt.

---

## Axe 4 — Migration technique du monofichier HTML

**Complexité :** 🔴 difficile.

### Contexte

Le fichier `tellux_v6_design.html` fait environ 500 Ko et 6 500 lignes. Il contient tout : HTML, CSS, JavaScript, données JSON inline, configurations Leaflet, logique métier, UI. Cette architecture monolithique fonctionne mais pose des risques croissants : maintenance difficile, impossibilité de tests unitaires, plantage sur mobile ancien, conflits de merge, charge cognitive élevée.

### Outils

- **Vite** — Bundler moderne, rapide, support natif des modules ES, HMR (Hot Module Replacement).
- **Leaflet.js** — Déjà utilisé, reste la base cartographique.
- **Vitest** — Framework de test unitaire compatible Vite.
- **GitHub Actions** — CI/CD pour build automatique et déploiement sur Cloudflare Pages.
- **ESLint + Prettier** — Linting et formatage du code.

### Étapes

1. **Inventaire du monofichier.** Cartographier les blocs fonctionnels du HTML actuel : combien de fonctions JS, combien de styles CSS, combien de données inline, quelles dépendances externes (Mapbox GL ? Leaflet ? Turf.js ?). Produire un document d'inventaire.

2. **Définir l'architecture cible.** Structure proposée :
   ```
   src/
   ├── index.html
   ├── main.js              ← point d'entrée
   ├── styles/
   │   ├── base.css          ← variables, reset, typographie
   │   ├── map.css           ← styles carte
   │   ├── panels.css        ← panneaux latéraux
   │   └── layers.css        ← légendes et toggles
   ├── layers/
   │   ├── heritage.js       ← couche patrimoine mégalithique
   │   ├── antennes.js       ← couche antennes ANFR
   │   ├── anomalies.js      ← couche anomalies telluriques
   │   ├── alignements.js    ← couche alignements
   │   └── agronomie.js      ← couche agronomie
   ├── data/
   │   ├── sites.json        ← SITES_REFERENCE.json (source de vérité GPS)
   │   ├── hypotheses.json   ← 80 hypothèses
   │   └── ...
   ├── ui/
   │   ├── header.js         ← header + logo
   │   ├── panels.js         ← gestion panneaux explicatifs
   │   ├── legend.js         ← système txLegend
   │   └── search.js         ← barre de recherche
   ├── utils/
   │   ├── geo.js            ← calculs géographiques (Broadbent, etc.)
   │   └── telluric.js       ← indice Tellux, score vibratoire
   └── tests/
       ├── heritage.test.js
       ├── geo.test.js
       └── ...
   ```

3. **Extraire les données en premier.** Sortir les tableaux `SITES[]`, les hypothèses, et toute donnée JSON inline dans des fichiers `.json` séparés dans `data/`. C'est l'étape la moins risquée et elle résout directement le problème A-1 (régression GPS).

4. **Extraire le CSS.** Séparer les styles en fichiers thématiques. Conserver les variables CSS `:root` dans `base.css`.

5. **Extraire le JS couche par couche.** Commencer par la couche la plus indépendante (probablement `antennes.js`), tester, valider, puis passer à la suivante. Chaque extraction doit être suivie d'un test de non-régression visuel (comparaison de captures d'écran avant/après).

6. **Configurer Vite.** Créer `vite.config.js`, `package.json`, et la pipeline de build. Le build doit produire un seul bundle optimisé pour la production (pour que le déploiement Cloudflare Pages reste simple).

7. **Configurer les tests.** Écrire des tests unitaires pour les fonctions utilitaires (`geo.js`, `telluric.js`) et des tests d'intégration pour les couches (vérifier que chaque couche charge ses données et s'affiche correctement).

8. **Configurer la CI/CD.** GitHub Actions : sur chaque push, lancer les tests, builder, et déployer sur Cloudflare Pages si la branche est `main`.

9. **Migration progressive.** Ne jamais réécrire tout d'un coup. Chaque étape produit une version fonctionnelle. L'ancienne version monofichier reste disponible en fallback pendant toute la migration.

### Dépendances

- Voie A gelée (on ne migre pas un fichier en cours de correction).
- Inventaire complet du monofichier (étape 1).
- Tests de non-régression définis avant toute extraction.

### Risques spécifiques

- Régressions visuelles ou fonctionnelles à chaque extraction.
- Dépendances implicites entre blocs JS (variables globales, event listeners partagés).
- Temps d'exécution estimé : 4 à 8 semaines selon la disponibilité.

### Livrables

- Dépôt structuré avec architecture modulaire.
- `SITES_REFERENCE.json` comme source de vérité GPS.
- Suite de tests couvrant au minimum les fonctions utilitaires et les couches principales.
- Pipeline CI/CD opérationnelle.
- Documentation technique de l'architecture.

---

## Axe 5 — Gouvernance et structure juridique

**Complexité :** 🟡 moyen.

### Contexte

Le projet est actuellement porté par Soleil via la SARL Stella Canis Majoris (Bastia). L'ouverture à des partenaires (associations CEM, permaculture, laboratoires), la réception de subventions publiques et la gouvernance d'un projet open-source nécessitent de clarifier la structure juridique et les règles de gouvernance.

### Outils

- **Comparatif juridique** — Voir `TELLUX_STRUCTURE_JURIDIQUE.md`.
- **Statuts types** — Modèles SCIC, association loi 1901, SASU disponibles en ligne.
- **CCI / CMA Corse** — Conseil juridique gratuit pour les porteurs de projet.
- **Expert-comptable** — Pour les implications fiscales et sociales.

### Étapes

1. **Compléter le comparatif juridique.** Le squelette est dans `TELLUX_STRUCTURE_JURIDIQUE.md`. Soleil doit arbitrer entre les options après lecture. Les critères clés : capacité à recevoir des subventions publiques, responsabilité limitée, souplesse de gouvernance, coût de création et de fonctionnement, compatibilité avec l'open-source.

2. **Consulter un expert.** Prendre RDV avec la CCI de Bastia ou un expert-comptable pour valider le choix. Coût estimé : 0 € (CCI) à 200 € (consultation comptable ponctuelle).

3. **Rédiger ou adapter les statuts.** Si la SARL Stella Canis Majoris est conservée, vérifier que l'objet social couvre les activités Tellux (recherche, cartographie, open data). Si une nouvelle structure est créée, rédiger les statuts.

4. **Définir la politique de contribution.** Pour un projet open-source : licence (déjà à choisir — recommandation : AGPL-3.0 ou GPL-3.0 pour garantir que les dérivés restent open-source), CLA (Contributor License Agreement) si des contributeurs externes rejoignent, code de conduite.

5. **Documenter la gouvernance.** Qui décide quoi, comment les partenaires sont intégrés, comment les décisions techniques sont prises. Un fichier `GOVERNANCE.md` dans le dépôt.

### Dépendances

- Arbitrage de Soleil sur la structure juridique.
- Résultat du comparatif dans `TELLUX_STRUCTURE_JURIDIQUE.md`.

### Livrables

- Structure juridique choisie et formalisée.
- Statuts à jour (existants ou nouveaux).
- `GOVERNANCE.md` dans le dépôt.
- Licence open-source choisie et appliquée.

---

## Axe 6 — Stratégie de subventions et financement

**Complexité :** 🟡 moyen.

### Contexte

Le projet vise plusieurs guichets de financement publics et semi-publics. La CTC est la cible prioritaire (dossier en cours). D'autres guichets sont envisagés à moyen et long terme. La stratégie doit être structurée pour maximiser les chances et minimiser la charge administrative.

### Outils

- **Tableau de suivi** — Voir `TELLUX_FINANCEMENT.md`.
- **Aides-territoires.beta.gouv.fr** — Moteur de recherche des aides publiques.
- **BPI France** — Subventions innovation, avances remboursables.
- **Europe** — LEADER (développement rural), Horizon Europe (recherche).
- **Fondations** — Fondation de France, Fondation pour la Nature et l'Homme, etc.

### Étapes

1. **Court terme (avril – juin 2026) : dépôt CTC.**
   - Finaliser `CANDIDATURE_TELLUX_v7.docx` avec captures d'écran post-corrections.
   - Préparer les annexes (CV porteur, budget prévisionnel, lettres de soutien si disponibles).
   - Identifier l'interlocuteur CTC (service innovation numérique ou patrimoine).
   - Déposer le dossier (S19, début mai 2026).

2. **Moyen terme (été – automne 2026) : diversification.**
   - **OEC (Office de l'Environnement de la Corse)** — Volet patrimoine naturel et paysager. Tellux touche aux mégalithes et à l'agronomie, deux thématiques OEC.
   - **ADEME** — Volet transition écologique. L'angle agronomie régénérative et données EM peut entrer dans les appels à projets ADEME « Recherche et Innovation ».
   - **ANR (Agence Nationale de la Recherche)** — Si partenariat avec un laboratoire (CEREGE, INRAE). Nécessite un porteur académique.
   - **LEADER** — Programme européen de développement rural. Les GAL (Groupes d'Action Locale) en Corse ont des enveloppes pour l'innovation territoriale.

3. **Long terme (2027+) : ancrage académique et institutionnel.**
   - **Partenariat laboratoire** — CEREGE (géosciences, Aix-Marseille), INRAE (agronomie), ou université de Corse. Objectif : co-publication scientifique sur les corrélations EM / agronomie, validation du corpus de 130 études.
   - **Publication scientifique** — Article dans une revue à comité de lecture. Augmente la crédibilité du projet et ouvre l'accès aux financements recherche.
   - **BPI France** — Si le projet génère un modèle économique (SaaS pour collectivités, API de données). Subvention ou avance remboursable.

4. **Préparer un budget prévisionnel.** Pour chaque guichet, les attentes sont différentes mais le socle est commun : coûts de développement (temps Soleil valorisé), hébergement (Cloudflare + Supabase), matériel de mesure (capteurs terrain si applicable), déplacements (sites mégalithiques), communication (landing page, documentation).

5. **Mettre en place une veille.** Surveiller les appels à projets via aides-territoires.beta.gouv.fr, les newsletters des GAL corses, les AAP ADEME et ANR. Fréquence : mensuelle.

### Dépendances

- Structure juridique choisie (axe 5) — certains guichets exigent une forme juridique spécifique.
- Voie A livrée — le dossier CTC s'appuie sur une version fonctionnelle de la carte.
- Partenariat labo — pour les guichets recherche (ANR, publications).

### Livrables

- Dossier CTC déposé (mai 2026).
- Tableau de suivi des guichets complété dans `TELLUX_FINANCEMENT.md`.
- Budget prévisionnel type (réutilisable pour plusieurs guichets).
- Au moins un contact laboratoire identifié.
- Veille mensuelle active sur les AAP.

---

## Calendrier synthétique

| Période | Axes actifs | Jalon |
|---|---|---|
| Avril 2026 | — | Gel voie A, dépôt CTC préparé |
| Mai 2026 | 1, 5 | Dépôt CTC, CLAUDE.md rédigé, arbitrage juridique |
| Juin 2026 | 1, 2, 3 | Landing page en ligne, premier workflow N8N actif |
| Juillet – Août 2026 | 3, 4, 6 | Début migration HTML, candidatures OEC/ADEME |
| Septembre – Octobre 2026 | 4, 6 | Migration HTML avancée, contact laboratoire |
| Novembre – Décembre 2026 | 4, 5, 6 | Architecture modulaire livrée, gouvernance formalisée |

---

## Notes

- Les axes sont indépendants sauf quand une dépendance est explicitement listée.
- L'ordre de priorité recommandé est : 1 → 5 → 6 → 2 → 3 → 4 (du plus rapide et impactant au plus lourd).
- Ce plan est vivant. Il sera mis à jour au fil des sessions et des décisions de Soleil.
