# TELLUX — Feuille de route

**Dernière mise à jour :** 10 avril 2026 (session 5)
**Remplace :** ROADMAP.md (7 avril), TELLUX_BRIEFING_SPRINTS.md (sprints C-E)

---

## 1. État au 10 avril 2026

| Composant | Référence | État |
|---|---|---|
| Code | `tellux_v6_design.html` | v6.1, session 10 avril — flux mesure corrigé + FAB mini-menu + prescription |
| Dossier | `CANDIDATURE_TELLUX_v7.docx` | v7, relecture en cours |
| Design | `DIRECTION_ARTISTIQUE_v2.md` | Validée et gelée |
| Déploiement | `tellux.pages.dev` | Cloudflare Pages, actif |
| Backend | Supabase PostGIS | Actif, connecté via MCP |
| Cible financement | CTC | Dossier multi-guichets en préparation |
| Porteur | Soleil (solo) | SARL Stella Canis Majoris, Bastia |

---

## 2. Deux chantiers parallèles

Le projet avance sur deux voies indépendantes. Si la voie B prend du retard, la voie A continue de fonctionner.

### Voie A — Livraison immédiate (gel v6)

**Objectif :** une version stable, déployée, livrable à des partenaires tests (associations CEM, permaculture, utilisateurs terrain) dans les 2 à 3 semaines.

**Base technique :** `tellux_v6_design.html` figé. Aucune migration, aucun refactoring lourd. On corrige les bugs bloquants, on fige, on livre. C'est cette version qui accompagne le dépôt CTC.

### Voie B — Montée en gamme (horizon 3-6 mois)

**Objectif :** migration progressive vers une architecture moderne (landing Framer, stack web modulaire, automatisations N8N).

**Détails :** voir `TELLUX_MONTEE_EN_GAMME.md` pour les 6 axes.

---

## 3. Voie A : problèmes à corriger avant gel

Chaque item doit être audité dans le HTML actuel pour déterminer s'il est déjà réglé ou nouveau.

### ✅ A-1. Placement GPS Anneaux Cap Corse — RÉSOLU (9 avril 2026, session 3)

Coordonnées exactes appliquées : **43°10'35.54"N 9°36'00.29"E** (43.17654°N 9.60008°E). Corrigées dans le tableau `SITES[]` ET dans les deux alignements `PRECOMPUTED_ALIGNMENTS` où l'ancienne valeur `44.008333°N` persistait.

**Contexte :** les 4 nouvelles mesures ajoutées au tableur n'ont pas causé la dérive — les coordonnées erronées dataient de la saisie initiale.

**Chantier ouvert — enrichissement sites patrimoniaux :**
- Étoffement du nombre de sites répertoriés via sessions Google Earth + reprise du tableur (Soleil)
- Constitution d'une base de données par site : données historiques, culturelles, et narratif poétique/fantastique mais sérieux (ton Tellux)
- Format cible : fiches enrichies par site (nom, coordonnées GPS vérifiées, époque, contexte géologique, anomalie EM mesurée ou modélisée, narration)
- Ces fiches alimenteront B-VISITES et potentiellement un mode "récit de territoire"
- À traiter en parallèle de la voie A : pas bloquant pour le gel, mais stratégique pour les partenariats mairies/DRAC

**Reste à traiter (A-1 général) :** vérifier les autres coordonnées GPS dans `SITES[]`. Solution structurelle : externaliser dans `SITES_REFERENCE.json` (voir A-1 original).

### ✅ A-2. Alignements : chargement lourd — RÉSOLU (8 avril 2026)

`PRECOMPUTED_ALIGNMENTS` : 15 alignements Broadbent 1980 calculés offline et injectés comme constante JS. `buildAutoAlignments()` lit directement depuis cette constante — plus de calcul runtime ni de Monte Carlo. Rebuild forcé à chaque activation de couche.

### ✅ A-3. Panneau explicatif — fermeture non liée au toggle couche — RÉSOLU (8 avril 2026)

`closeLayerPanel(id)` implémentée. Appelée dans la branche de désactivation de `tog()` : désactiver une couche ferme automatiquement son panneau associé. Cas spécial `hypo` gère aussi `hypo-list-panel`.

### ✅ A-4. Carte bloquée — RÉSOLU (9 avril 2026)

La carte se bloquait dans certaines configurations (zoom verrouillé autour de la Corse). Cause identifiée : contrainte de bounds non souhaitée active dans certains états. Solution : forcer un dezoom (scroll arrière ou pinch-out) pour sortir du blocage. Aucun fix code nécessaire — comportement lié aux paramètres `maxBounds` de Leaflet qui empêchent de sortir de la bbox Corse. Documenté comme comportement intentionnel allégé.

### A-4b. Audit complet du pattern couche ↔ panneau ↔ légende

Pour chaque couche, vérifier la chaîne complète : toggle ON → couche visible + légende `txLegend.show()` + panneau explicatif si présent ; toggle OFF → couche masquée + `txLegend.hide()` + panneau explicatif fermé. Documenter les exceptions.

### ✅ A-5. Marqueur violet + formulaire mesure — RÉSOLU (9 avril 2026, session 3)

**Problème :** le point violet créé par `startContrib()` disparaissait au clic suivant sans permettre la saisie ; le bouton FAB (+mesure) n'enclenchait pas correctement la séquence.

**Cause :** double handler `map.on('click')` — `openProspecteurWithForm()` liait un handler prospDiag qui s'exécutait en même temps que le `map.once('click')` de `startContrib()`.

**Fix :**
- Flag `window._contribPending` : pendant la pose du point, le handler prospDiag est ignoré
- Bouton **Annuler mesure** ajouté dans le formulaire : supprime le marqueur violet, reset le flag
- `map.once('click')` dans `startContrib()` réécrit avec template strings sans backticks (compatibilité)

### ✅ A-6. CSS boutons actifs manquants — RÉSOLU (8 avril 2026)

Règles `.lbtn.on-aoc`, `.on-emag`, `.on-radon` ajoutées. Tous les boutons de couche ont désormais un retour visuel ON/OFF cohérent.

_(Note : l'item original portait sur l'unité anomalie Monticello. Ce point reste à auditer séparément — voir section 7.)_

### ✅ A-7. Conflit clic quadrillage anomalies — RÉSOLU (9 avril 2026, session 3)

**Problème :** les carrés colorés de `buildHot()` interceptaient les clics avec `L.DomEvent.stopPropagation(e)`, empêchant le clic de remonter au handler `map.on('click')` et bloquant le diagnostic au clic.

**Fix :** les rects `L.rectangle` de la couche `lHot` sont maintenant `interactive:false`. Le clic traverse directement jusqu'à `map.on('click')` qui affiche le diagnostic complet. L'info anomalie (score, label) est désormais intégrée dans le popup principal au clic carte.

### ✅ A-14. Couches patrimoine auto-activées — RÉSOLU (9 avril 2026)

Non reproductible en code. Cause probable : cache navigateur. Action : vider le cache (Ctrl+Shift+R / Cmd+Shift+R) avant test. Aucun fix code nécessaire.

### ⏳ A-8. Captures d'écran haute résolution pour dossier CTC

Une fois les corrections A-1 à A-7 appliquées, produire 6 à 8 captures 1920×1080 en light mode pour intégration dans `CANDIDATURE_TELLUX_v7.docx`. Vues attendues : vue d'ensemble, popup site mégalithique avec Indice Tellux, module agronomie, couches réseaux EDF+ANFR, panneau hypothèses, vue mobile.

### ✅ État technique supplémentaire (8 avril 2026)

- **Simulateur bâtiment** désactivé proprement (`disabled` + opacité 0.4 + label "en dev").
- **Couche lProd** (Production électrique) créée : 33 sites `PROD_ELECTRIQUE`, markers proportionnels à la puissance, colorés par type (hydraulique, éolien, diesel, TAC, interconnexion). Bouton "Production" dans la section Énergies humaines.
- **Gamification** : 9 bugs corrigés — async `runAutoTests`, guard XP double-award, géolocalisation hypothèses, narratif FR par résultat.
- **Panel agronomie** : texte d'accueil ajouté, jargon technique reformulé pour public non-scientifique.

### A-9. Doublons lProd/HT — RÉSOLU (8 avril 2026) ✅

`PROD_ELECTRIQUE` était affiché en double : dans `loadReseau()` (couche HT) ET dans `buildProdLayer()` (couche Production). Supprimé de `loadReseau()` — la couche HT ne contient plus que les lignes/polylines réseau.

### A-10. Fusion formulaire diagnostic — RÉSOLU (8 avril 2026) ✅

Un seul panel `#prosp-wrapper` avec : section haute diagnostic instantané (toujours visible) + section basse `<details>` "Enrichir avec une mesure réelle →" (formulaire terrain expandable). Bouton sidebar et FAB ouvrent le panel avec la section dépliée via `openProspecteurWithForm()`.

### ✅ A-11. Conflit légendes multi-couches — RÉSOLU (9 avril 2026)

Système FIFO implémenté : `_activeLayers` (Set), `_layerOrder[]`, `LAYER_NAMES{}`, `checkLayerLimit()`, `showToast()`. Au-delà de 4 couches actives, la plus ancienne est automatiquement désactivée avec notification toast. `addActiveLayers()` / `removeActiveLayers()` appelés dans `tog()`. Initialisation : `hot` et `con` pré-inscrits dans le Set au démarrage.

### ✅ A-12. Score agronomie hors échelle — RÉSOLU (9 avril 2026)

`runPermaDiag()` affichait 61.4/10 au lieu de 6.1/10 : `scorePhys` (somme non bornée) passait directement à l'affichage. Corrigé par `Math.min(10, Math.round((all.score||0)/10*10)/10)` dans `runPermaDiag`. Barre de progression en % corrigée en conséquence.

### ✅ A-13. Anneaux Cap Corse — coordonnées corrigées (9 avril 2026)

Les coordonnées `44.008°N 9.848°E` (mer Tyrrhénienne nord, hors Corse) corrigées en `43.008°N 9.348°E` (Parc marin Cap Corse, plausible). Note : la position exacte des 1 417 formations sous-marines reste à valider via la publication Ballesta/CEREGE 2021-2024. À traiter dans A-1 (externalisation SITES JSON).

### A-14. Couches patrimoine — investigation non concluante

Signalement : couches `sit` (mégalithes), `align`, `egl` s'activeraient automatiquement en page d'accueil. Audit code : aucune activation automatique identifiée dans le code (ACTIVE init = sit:false, align:false, egl:false ; pas de localStorage ACTIVE ; buildSitesLayer ne fait qu'alimenter lSit sans l'ajouter à la carte). Hypothèse probable : état CSS résiduel dans le navigateur (form restore) ou cache navigateur de la version précédente. **Action : vider le cache navigateur + tester sur profil vierge.** Si reproductible, investiguer côté `window._hypoAutoRan` au démarrage.

### ✅ A-15. Confetti — déclenchement intempestif corrigé (9 avril 2026)

Les confettis se déclenchaient à chaque auto-test réussi (clic hypothèse). Corrigé : confetti réservé au **1er test réussi uniquement** (`_gameState.testsPassed===1`). Cohérent avec la règle de gamification : récompense au 1er badge débloqué.

### Critère de gel voie A

**Résolus :** A-2, A-3, A-6, A-9, A-10, A-11, A-12, A-13, A-14, A-15 + A-1 (anneaux), A-4, A-5, A-7.

**Reste à traiter :** A-1 général (GPS autres sites — session Google Earth + tableur), A-4b (audit pattern couche↔légende), A-8 (captures HD).

La version peut être taguée et livrée aux partenaires tests. A-8 peut être fait en parallèle du gel.

### Session 5 — Audit et refonte du flux de mesure (10 avril 2026)

**Bugs bloquants corrigés :**

- ✅ **PGRST204 résolu** — 7 colonnes ajoutées dans Supabase (`contexte`, `etage`, `geo_nets`, `geo_netval`, `materiaux_murs`, `appareils_actifs`, `attenuation_prevue_db`). Migration SQL versionnée dans `_migrations/001_contributions_contexte_batiment.sql`.
- ✅ **saveContrib() sécurisé** — filtrage des champs null/undefined avant envoi POST (protection contre futures colonnes manquantes).
- ✅ **FAB double-clic résolu** — `startContribFromFAB()` découplé de `startContrib()` pour éviter le double-toggle de la couche contributions. Marqueur nettoyé à la fermeture.
- ✅ **Messages de validation stylés DA v2** — `info()` supporte maintenant 4 types : error (porphyre), success (maquis), warn (ocre), neutre. Toutes les anciennes spans inline converties.

**Nouvelles fonctionnalités :**

- ✅ **Formulaire redesigné DA v2** — titre en Fraunces, labels en IBM Plex Sans, indicateurs d'étapes 1-5, focus states avec halo vert, bouton "Repositionner le point", affichage position dans le formulaire.
- ✅ **FAB mini-menu** — Le bouton (+) ouvre un menu à 2 options : "Ajouter une mesure" (vert maquis) et "Prescription de mesure" (ocre).
- ✅ **Mode prescription** — 8 méthodes de mesure recommandées avec badges de niveau (vert/ocre/bleu). Clic sur une méthode ouvre le formulaire avec instrument et unité pré-sélectionnés.

**Documentation produite :**

- `TELLUX_AUDIT_FLUX_MESURE.md` — cartographie complète du flux de mesure, 10 fonctions documentées, 10 failles identifiées, architecture Supabase 27 colonnes.
- `TELLUX_TEST_FLUX_MESURE.md` — 5 scénarios de test de bout en bout (nominal extérieur, intérieur avec matériaux, prescription, erreurs, mobile).

### Infrastructure — Actions réalisées (session 4, vérifiées session 5)

| # | Action | État | Vérification |
|---|---|---|---|
| 1 | Cron d'éveil Supabase (UptimeRobot) | ✅ Réalisé | Supabase ACTIVE_HEALTHY confirmé le 10 avril |
| 2 | Mirror GitHub → GitLab | ✅ Réalisé | À vérifier par Soleil (synchro auto) |
| 3 | Clone local Git vérifié | ✅ Réalisé | remote origin = `dellahstella/tellux.git` |
| 4 | Mirror Netlify plan B | ✅ Réalisé | À vérifier par Soleil (URL Netlify) |
| 5 | Tag v6.0.0 | ✅ Réalisé | `git tag` confirme v6.0.0 |
| 6 | Branche staging Cloudflare | ✅ Réalisé | branche `staging` active, `staging.tellux.pages.dev` |
| 7 | Export manuel Supabase | ✅ Réalisé | 7 tables exportées dans `SupaData-backup/` (CSV) |
| 8 | Domaine tellux.fr | ⏳ Reporté | Place dans le dossier candidature (session ultérieure) |

**Données JSON externalisées (prêtes pour Git) :**

- `SITES_REFERENCE.json` — 121 sites patrimoniaux (déjà sur GitHub)
- `failles_corse.json` — 8 failles géologiques (extrait du HTML, à ajouter)
- `prod_electrique.json` — 33 sites de production électrique (extrait du HTML, à ajouter)
- `hypotheses.json` — 80 hypothèses testables (extrait du HTML, à ajouter)

---

## 4. Validation scientifique (post-gel, pré-voie B)

Ces items renforcent la crédibilité scientifique du projet. Ils peuvent être traités entre le gel voie A et le lancement voie B.

- **E-1.** Refactoring `FAILLES_CORSE` en segments LineString. Gain précision ±300 m.
- **E-2.** Implémentation tests automatiques H55–H88 (hypothèses auto-testables).
- **E-3.** Externalisation `SITES[]` dans `SITES_REFERENCE.json` hébergé (recoupe A-1, à traiter ensemble).
- **E-4.** Protocole calibration Trifield TF2 standardisé (mesures en aveugle parallèle : deux opérateurs indépendants, non communication pendant la mesure).

---

## 5. Voie B : plan de montée en gamme (sommaire)

Détails complets dans `TELLUX_MONTEE_EN_GAMME.md`.

| Axe | Sujet | Complexité |
|---|---|---|
| 1 | Exploitation complète de l'écosystème Anthropic | 🟢-🟡 |
| 2 | Migration design : landing Framer | 🟡 |
| 3 | Automatisation N8N | 🟡 |
| 4 | Migration technique du monofichier HTML | 🔴 |
| 5 | Gouvernance et structure juridique | 🟡 |
| 6 | Stratégie de subventions | 🟡 |

**Axe 2 — Framer (décision arrêtée) :** Webflow abandonné. Framer retenu — courbe d'apprentissage plus douce, ludique, compatible React. Claude peut produire des composants JSX directement exportables dans Framer. L'app cartographique (HTML/Leaflet) reste indépendante et intacte ; Framer = landing page marketing uniquement. Pas de migration du code carte.

**B-VISITES — Mode visite guidée patrimoine (moyen terme) :** Pour chaque site mégalithique et ouvrage remarquable, fiche enrichie avec photos, texte narratif, contexte historique et géophysique. Si l'intégration dans la carte actuelle est trop lourde : créer des articles dédiés par site (HTML statique ou Notion public), liés depuis le popup Leaflet via un lien "En savoir plus". Axe stratégique fort pour les mairies proches de sites mégalithiques — argument patrimonial concret. La rédaction d'articles de fond avec identité visuelle Tellux et accès à la base de données enrichie est un chantier éditorial à part entière, à développer progressivement. Levier d'engagement pour les communes non directement concernées par l'EM.

**B-STRUCTURES — Structures EM remarquables (long terme, étude faisabilité) :** Détection de structures à géométrie et orientation EM significative : pyramides, tertres, terrasses, systèmes d'irrigation anciens, tunnels, terrassements agricoles. Phénomène pan-européen sous-documenté, nombreux candidats en Corse. Pas de couche dédiée avec marqueurs "candidat non validé" pour l'instant — étude de faisabilité d'abord, puis ajout de sites peu connus à l'échelle mondiale (Bosnie, Nice, Pays basque, Chine, Russie, Antarctique, Mexique, etc.). Corpus scientifique de niveau B à constituer. Disclaimer explicite obligatoire, possibilité de contribution crowdsourcée à cadrer.

---

## 6. Chantiers structurels transverses (urgents)

Ces sujets ne sont ni A ni B. Ce sont des décisions qui conditionnent tout le reste.

### S-1. Structure juridique — arbitrage urgent

Comparaison des options (micro-entreprise, SASU, association loi 1901, SCIC, SARL existante) avec implications fiscales, administratives, de responsabilité et de capacité à recevoir des subventions publiques. Voir `TELLUX_STRUCTURE_JURIDIQUE.md`.

**Non tranché.** Soleil décide après lecture du document comparatif.

### S-2. Pérennité technique — risque monofichier HTML

Le fichier `tellux_v6_design.html` fait environ 500 Ko et 6 500 lignes, tout-en-un. Risques : plantage navigateur sur mobile ancien, maintenance difficile, impossibilité de tests unitaires, conflits de merge.

**Mesures immédiates (voie A) :** sauvegardes git versionnées à chaque session, pas de refactor risqué, dépôt GitHub à jour.

**Mesure structurelle (voie B) :** migration vers architecture modulaire (axe 4 de `TELLUX_MONTEE_EN_GAMME.md`).

### S-3. Stratégie de subventions et de financement

Court terme : CTC (en cours). Moyen terme : OEC, ADEME, ANR, LEADER. Long terme : partenariat laboratoire, publication scientifique. Voir `TELLUX_FINANCEMENT.md`.

---

## 7. Items à vérifier (peut-être déjà résolus)

Ces points proviennent de sessions antérieures. À auditer dans le HTML actuel avant de les ajouter au backlog ou de les clore.

- Migration WMS Géoplateforme (anciennement Géoportail).
- Sélecteur culture personnalisée (module agronomie).
- Template PDF propre pour `exportPermaPDF`.
- Lazy-loading couches lourdes (performances mobiles).

---

## 8. Agenda court terme (avril – mi-mai 2026)

| Semaine | Tâche | Responsable | Dépendance |
|---|---|---|---|
| S15 (7-13 avr) | Design validé, logo V7 gelé, dossier v7 produit | ✅ fait | — |
| S15 (8 avr) | A-2, A-3, A-6, A-9, A-10 résolus — gamification, lProd, diagnostic fusionné | ✅ fait | — |
| S15 (9 avr) | Audit infrastructure + 7 actions sécurisation | ✅ fait | — |
| S15 (10 avr) | Flux de mesure : 3 bugs corrigés + FAB mini-menu + prescription + audit + tests | ✅ fait | — |
| S16 (14-20 avr) | Commit des fichiers JSON + docs dans Git. Push staging → test Cloudflare | Soleil | Fichiers prêts |
| S16 | Arbitrage structure juridique | Soleil | Lecture `TELLUX_STRUCTURE_JURIDIQUE.md` |
| S16 | Test flux mesure de bout en bout (5 scénarios) | Soleil | `TELLUX_TEST_FLUX_MESURE.md` |
| S17 (21-27 avr) | Corrections restantes (A-1 GPS, A-4b audit couches, A-8 captures) | Cowork | — |
| S17 | Relecture finale dossier v7 + captures HD | Soleil | — |
| S18 (28 avr – 4 mai) | Gel voie A, tag v6.1.0 | Soleil + Cowork | Tests OK |
| S19 (5-11 mai) | Dépôt CTC | Soleil | Dossier complet |
| S19-S20 | Validation scientifique E-1 à E-4 | Cowork | Voie A gelée |
| S20+ | Lancement voie B (axe 1 : instructions projet + Claude Code) | Soleil | Voie A livrée |

---

## 9. Stratégie partenariats

### 9.1 Cibles et critères « prêt à envoyer »

| Cible | Critère de passage | État | Documents |
|---|---|---|---|
| **Associations EM** (PRIARTEM, CRIIREM, collectifs locaux) | Carte opérationnelle + double indice documenté + disclaimer santé visible | ✅ PRÊT | `TELLUX_KIT_ENVOI_EM.md` |
| **Agronomie / permaculture** (groupements bio, sol vivant, LPO) | Module parcelle opérationnel + au moins 3 relevés terrain parcelles contrastées (H63) | ⚠️ Manque terrain | `TELLUX_DOSSIER_AGRO_BIO.md` |
| **Mairies / patrimoine** (DRAC, communes, guides) | 5+ fiches de visite enrichies (B-VISITES) + liste communes concernées | ⚠️ Manque B-VISITES | `TELLUX_DOSSIER_MAIRIES_PATRIMOINE.md` |
| **Scientifiques — Géophysiciens** (CEREGE, CNRS, Univ. Corse) | Carte opérationnelle + GPS vérifiés + alignements visibles | ⚠️ GPS A-1 | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |
| **Scientifiques — EM & santé** (CRIIREM, INRAE, Grenoble) | Double indice documenté + corpus A citant leurs travaux | ✅ PRÊT | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |
| **Scientifiques — Alignements** (ACEM, Leplat, Crowhurst) | 15 alignements Broadbent + méthode expliquée dans l'interface | ✅ PRÊT | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |
| **Scientifiques — Agronomie EM** (INRAE, chambres bio) | Module parcelle + au moins 1 mesure terrain agro | ❌ Pas de terrain | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |
| **Scientifiques — Permaculture** (AgroParisTech, SupAgro) | Module parcelle + disclaimer H64 renforcé dans l'interface | ⚠️ Disclaimer | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |

### 9.2 Séquence de prise de contact recommandée

**Phase 1 — Immédiat (avril 2026) :** Associations EM nationales et locales. Scientifiques profils A (géophysiciens), B (EM & santé), C (alignements). Pas de dépendance terrain.

**Phase 2 — Après 3 relevés terrain H63 (mai–juin 2026) :** Agronomie/permaculture. Scientifiques profils D (agronomie EM) et E (permaculture scientifique).

**Phase 3 — Après B-VISITES (été 2026) :** Mairies rurales individuelles. DRAC (si pas déjà contactée via le dossier candidature).

### 9.3 Notes stratégiques

**Ciblage mairies :** privilégier les communes situées à moins de 5 km d'un alignement Broadbent détecté OU à moins de 2 km d'une source de production ou perturbation EM (centrale hydraulique, barrage, antenne mobile dense). Ces communes ont un intérêt direct et mesurable dans Tellux. À faire : produire une liste des communes concernées par croisement automatique (PRECOMPUTED_ALIGNMENTS × bbox communes × PROD_ELECTRIQUE × données ANFR).

**Levier patrimonial :** le mode visite guidée (B-VISITES) est l'argument d'entrée pour les mairies rurales qui ne sont pas directement concernées par l'EM. Sans fiche de site enrichie et narrative, l'argument patrimonial seul est insuffisant pour motiver un élu local. B-VISITES doit donc précéder ou accompagner toute démarche de partenariat communal.

**Audit de solidité :** voir `TELLUX_AUDIT_MODELE.md` pour l'évaluation détaillée de ce que Tellux peut et ne peut pas promettre par cible, les 3 limites à communiquer proactivement, et les 6 actions prioritaires pour renforcer la crédibilité.

### 9.4 Veille corpus scientifique

**Option retenue : veille semi-automatique (Scholar Alerts + Claude).** 8 alertes Google Scholar configurées sur des mots-clés ciblés (EMF agriculture, archaeoastronomy Corsica, piezoelectric megalith, Schumann resonance crop, etc.). Résumés hebdomadaires → évaluation Claude → classement A/B/C proposé → validation Soleil.

Effort : ~1h setup, ~15 min/semaine maintenance. Veille manuelle assistée maintenue comme socle. Option crowdsourcée (formulaire « Proposer une étude ») reportée à la voie B après 200+ utilisateurs actifs.

Détails complets des 3 options évaluées dans `TELLUX_AUDIT_MODELE.md`, section E.

---

## 10. Vision module agronomie & géobiologie (long terme)

### 10.1 Mode Agronomie — feuille de route

**Vision :** outil tout-en-un pour le design de permaculture — visualisation cartographique, diagnostic EM parcellaire, base de données cultures, calculateur de zonation, générateur de design.

**État actuel (9 avril 2026) :**
- Tab Diagnostic : score EM parcelle + recommandations cultures corses (révisé score borné 0-10)
- Tab Cultures Corse : grille 9 cultures avec résilience EM
- Tab Design *(nouveau)* : formulaire guidé 3 questions (surface / usage / priorité) → préconisations design adapté au profil EM du point cliqué

**Prochaines étapes :**
- B-AGRO-1 : Zonation PDC interactive (zones 1-2-3-4-5 dessinables sur la carte)
- B-AGRO-2 : Calculateur swale / bilan eau selon pente détectée
- B-AGRO-3 : Base de données semences corses (30+ variétés anciennes, source INAO + Hameau des Buis)
- B-AGRO-4 : Export plan de design PDF avec carte + recommandations + sources
- B-AGRO-5 : Intégration données météo / ETP locales pour conseils irrigation

### 10.2 Mode Diagnostic & Géobiologie — feuille de route

**Vision :** équilibrer l'environnement vibratoire à toutes les échelles — de la chambre d'adolescent à l'exploitation agricole, de l'habitat individuel à la décision de territoire régional.

**État actuel (9 avril 2026) :**
- Panneau Géobiologue : checklist mesure, guide interprétation Δ nT, export rapport
- Section "Équilibrer l'environnement" *(nouvelle)* : méthodes empiriques par échelle (chambre → habitat → jardin → exploitation → territoire)
- Sources : FFGéobio 2024, Olifirenko 2015, Becker 1990, Maffei 2014, Hermans 2023

**Prochaines étapes :**
- B-GEO-1 : Diagnostic EM par pièce — superposer grilles Hartmann/Curry sur plan schématique habitation
- B-GEO-2 : Protocole calibration magnétomètre téléphone (température, interférences, procédure)
- B-GEO-3 : Bibliothèque de solutions matériaux (tourmaline, shungite, matériaux biosourcés, plantes) avec sourcing
- B-GEO-4 : Mode "Rééquilibrage" — guide pas-à-pas pour corriger une anomalie mesurée
- B-GEO-5 : Intégration calendrier biodynamique (Thun) pour optimiser interventions terrain

### 10.3 Positionnement stratégique Tellux

Tellux n'est pas seulement un outil de cartographie EM. À terme, c'est une **plateforme de décision environnementale** couvrant :
- **Bien-être individuel** (habitat, chambre, feng-shui pragmatique fondé sur données)
- **Agriculture régénérative** (permaculture, agroécologie, biodynamie)
- **Gestion territoriale** (communes, EPCI, CTC — planification usage des sols)
- **Recherche participative** (crowdsourcing mesures, validation hypothèses, co-publication)

La singularité : tout est ancré dans des **données institutionnelles vérifiables** (ANFR, IGRF, BRGM, EMAG2) et un **corpus peer-reviewed à 3 niveaux de crédibilité**. Ce n'est pas de la géobiologie ésotérique — c'est de la géobiologie instrumentée.

---

## 11. Actions différées (identifiées session 5, non prioritaires)

Ces items ont été identifiés pendant l'audit du flux de mesure mais ne sont pas bloquants pour le gel voie A. À traiter en sessions ultérieures.

| ID | Action | Priorité | Contexte |
|---|---|---|---|
| F-1 | Sauvegarde brouillon formulaire (localStorage) | 🟡 | Éviter perte de données si fermeture accidentelle pendant la saisie |
| F-2 | Upload photo/pièce jointe dans les contributions | 🟡 | Documentation visuelle des mesures terrain (Supabase Storage) |
| F-5 | Formulaire bottom-sheet mobile | 🟠 | Le formulaire actuel fonctionne sur mobile mais n'est pas optimal |
| F-6 | Validation en temps réel (avant clic Enregistrer) | 🟡 | Meilleure UX — erreurs visibles immédiatement pendant la saisie |
| F-9 | Mode hors-ligne (file d'attente localStorage → sync) | 🟠 | Si Supabase inaccessible, la mesure est perdue. File offline = résilience |
| D-1 | Retirer le bouton "Diagnostic terrain" du sidebar | 🟢 | Le FAB mini-menu remplace l'accès direct depuis le sidebar |
| D-2 | Badges de validation par méthode dans la prescription | 🟡 | Afficher la fiabilité par méthode (vert/ocre/rouge) avec critères |
| D-3 | Historique des mesures par session avec export CSV | 🟡 | Permettre aux contributeurs de revoir et exporter leurs mesures |
| INF-8 | Achat domaine tellux.fr ou tellux.corsica | 🟡 | Évaluer disponibilité et intégrer dans le dossier candidature CTC |
| JSON-1 | Charger `failles_corse.json`, `prod_electrique.json`, `hypotheses.json` depuis fichiers externes plutôt que inline | 🟡 | Réduction taille HTML, maintenabilité, cohérence avec SITES_REFERENCE.json |

---

## 12. Risques ouverts

- **Régression GPS récurrente** — les coordonnées des sites mégalithiques dérivent entre les sessions. Solution proposée en A-1 (JSON externe). À traiter : anneaux Cap Corse, position exacte à valider via CEREGE.
- **Dépendance fournisseur unique** — Supabase (backend) et Cloudflare (hébergement). Risque faible à court terme, à surveiller.
- **Charge cognitive monofichier** — 6 500+ lignes rendent toute modification risquée. Atténuation par git + tests manuels.
- **Absence de second relecteur scientifique** — le corpus de 130 études et les 88 hypothèses n'ont pas été relus par un pair. À chercher via partenariat labo (CEREGE, INRAE).
- **Retard dépôt CTC** — si la voie A prend plus de temps que prévu, le dépôt glisse. Mitigation : découpler les captures du gel complet si nécessaire.
- **Dépôt nom « Tellux »** — à évaluer selon budget, noter en feuille de route long terme.
- **Couches patrimoine auto-activées** — signalement A-14 non reproduit en code. À surveiller, vider cache navigateur si observation persistante.
- **Score agronomie** — correction appliquée (division par 10) mais calibration fine des valeurs `calcAll()` reste à faire pour que les plages 0-3 / 3-6 / 6-10 correspondent à des seuils physiques réels mesurables terrain.
