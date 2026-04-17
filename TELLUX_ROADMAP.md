# TELLUX — Feuille de route

**Dernière mise à jour :** 13 avril 2026 (session Sonnet — Patrimoine)
**Remplace :** version du 10 avril 2026 (session 5)

---

## 1. État au 13 avril 2026

| Composant | Référence | État |
|---|---|---|
| Code | `tellux_CORRECT.html` | Source de vérité. ~7 000 lignes. Module géométrie + orientations ajoutés |
| Code (dev) | `tellux_v6_design.html` | Branche de travail, contient les mêmes ajouts |
| Dossier | `CANDIDATURE_TELLUX_v7.docx` | v7, relecture en cours |
| Design | `DIRECTION_ARTISTIQUE_v2.md` | Validée et gelée |
| Déploiement | `tellux.pages.dev` | Cloudflare Pages, actif |
| Backend | Supabase PostGIS (`knckulwghgfrxmbweada`) | Actif, 3 migrations appliquées |
| Git | `main` + `dev` | Nettoyé le 13 avril, workflow dans `WORKFLOW_GIT.md` |
| Cible financement | CTC | Dossier multi-guichets en préparation |
| Porteur | Soleil (solo) | SARL Stella Canis Majoris, Bastia |

### Migrations Supabase appliquées

| # | Fichier | Objet |
|---|---|---|
| 001 | `001_contributions_contexte_batiment.sql` | 7 colonnes contexte bâtiment |
| 002 | `002_contributions_csv.sql` | Support import CSV Phyphox |
| 003 | `003_orientations.sql` | Table `orientations_contributions` (9 col, RLS anon) |

---

## 2. Deux chantiers parallèles

Le projet avance sur deux voies indépendantes. Si la voie B prend du retard, la voie A continue de fonctionner.

### Voie A — Livraison immédiate (gel v6)

**Objectif :** version stable, déployée, livrable à des partenaires tests (associations CEM, permaculture, utilisateurs terrain).

**Base technique :** `tellux_CORRECT.html` figé. Aucune migration, aucun refactoring lourd. On corrige les bugs bloquants, on fige, on livre. C'est cette version qui accompagne le dépôt CTC.

### Voie B — Montée en gamme (horizon 3-6 mois)

**Objectif :** migration progressive vers une architecture moderne (landing Framer, stack web modulaire, automatisations N8N).

**Détails :** voir `TELLUX_MONTEE_EN_GAMME.md` pour les 6 axes.

---

## 3. Voie A : état des corrections

### Bugs résolus — sessions 1 à 5 (8-10 avril 2026)

| ID | Problème | Résolution |
|---|---|---|
| A-1 | GPS Anneaux Cap Corse | Coordonnées 43.008°N 9.348°E appliquées (session 3) |
| A-2 | Alignements chargement lourd | `PRECOMPUTED_ALIGNMENTS` 15 alignements offline (session 2) |
| A-3 | Panneau explicatif fermeture | `closeLayerPanel(id)` (session 2) |
| A-4 | Carte bloquée | Comportement `maxBounds` Leaflet — documenté (session 3) |
| A-5 | Marqueur violet + formulaire mesure | Flag `_contribPending` + bouton Annuler (session 3) |
| A-6 | CSS boutons actifs | Règles `.lbtn.on-aoc`, `.on-emag`, `.on-radon` (session 2) |
| A-7 | Conflit clic quadrillage | `L.rectangle` avec `interactive:false` (session 3) |
| A-9 | Doublons lProd/HT | Supprimé de `loadReseau()` (session 2) |
| A-10 | Fusion formulaire diagnostic | Panel unique `#prosp-wrapper` (session 2) |
| A-11 | Conflit légendes multi-couches | Système FIFO max 4 couches (session 3) |
| A-12 | Score agronomie hors échelle | Borné `Math.min(10, ...)` (session 3) |
| A-13 | Anneaux coordonnées | Corrigé 43.008°N 9.348°E (session 3) |
| A-14 | Couches patrimoine auto-activées | Non reproductible — cache navigateur (session 3) |
| A-15 | Confetti intempestifs | Réservé au 1er test réussi (session 3) |

### Bugs résolus — session 5 (10 avril 2026)

| Bug | Fix |
|---|---|
| PGRST204 formulaire mesure | 7 colonnes ajoutées Supabase (migration 001) |
| FAB double-clic | `startContribFromFAB()` découplé |
| Messages validation non stylés | `info()` 4 types : error/success/warn/neutre |

### Bugs résolus — session 13 avril 2026

| Bug | Fix |
|---|---|
| Flux mesure 3 erreurs résiduelles | Corrigés par refonte design formulaire |
| CSV Phyphox import cassé | Corrigé par refonte du bouton — le bug n'existe plus dans le design actuel |

### Items restants voie A

| ID | Action | Priorité |
|---|---|---|
| A-1g | Vérification GPS autres sites (session Google Earth) | 🟡 Soleil |
| A-4b | Audit pattern couche ↔ panneau ↔ légende | 🟡 Cowork |
| A-8 | Captures d'écran HD pour dossier CTC | 🟡 Cowork |
| A-16 | Vocabulaire module prescription : retrait résidus UI radon + reformulation cage Faraday | ✅ Cowork — 17 avr 2026 |
| A-17 | Position épistémique : sections A7 (Kirschvink/Wang) + A8 (vocabulaire interdit) | ✅ Cowork — 17 avr 2026 |
| A-18 | Hypothèses H84-H88 : magnétoréception, troupeaux, balbuzard, Kp cardio, shinrin-yoku | ✅ Cowork — 17 avr 2026 |
| A-19 | Corpus scientifique v6 : 5 sections thématiques, ~50 études structurées | ✅ Cowork — 17 avr 2026 |

**Critère de gel :** A-1g + A-4b + A-8 + A-16 + A-17 + A-18 + A-19 → tag v6.1.0

---

## 3.0 Finitions pré-envoi associations EM

`[À COMPLÉTER SESSION 14 AVRIL]`

Ce bloc sera rempli lors de la prochaine session Opus. Il contiendra les retouches UX finales identifiées avant le premier envoi aux associations EM : relecture des textes d'interface, vérification des disclaimers, cohérence terminologique avec `TELLUX_POSITION_EPISTEMIQUE.md`.

---

## 3.5 Session 6 — Clarification épistémique (12 avril 2026)

**7 missions complétées :**

| Mission | Livrable | Objet |
|---|---|---|
| A | `TELLUX_POSITION_EPISTEMIQUE.md` | Document fondateur : ce que Tellux mesure, 3 erreurs à ne jamais commettre |
| B | `TELLUX_DOSSIER_ASSO_EM.md` | Réécrit — terminologie corrigée, hiérarchie contributions A/B/C/D |
| C | `TELLUX_DOSSIER_AGRO_BIO.md` | Réécrit — 1ère vague prudente, 2ème vague ambitieuse, corpus enrichi |
| D | `TELLUX_DOSSIER_MAIRIES_PATRIMOINE.md` | Réécrit — §Anneaux retiré, §géométrie ajouté, §orientation ajouté |
| E | `TELLUX_DOSSIER_SCIENTIFIQUES.md` | Pause sur profils A/B/C/E, profil D seul actif |
| F | `TELLUX_KIT_ENVOI_EM.md` | Terminologie alignée, posture retour critique |
| G | `TELLUX_SESSION6_SYNTHESE.md` | Rapport de session |

**3 erreurs éradiquées :** "deux réalités différentes", "les mesures ne s'additionnent pas", "naturel = bénin".

**Principe clé :** les contributions EM s'additionnent vectoriellement (superposition). Tellux mesure le résultat total et modélise les parts.

---

## 3.6 Session Sonnet — Patrimoine (13 avril 2026)

**5 missions complétées :**

| Mission | Objet |
|---|---|
| A — Audit corpus | 116 SITES confirmés, 314 CHURCHES confirmées, aucun doublon, GPS OK |
| B — Retrait focus Anneaux | H2 diversifiée (Cauria, Inzecca, Anneaux) |
| C — Module géométrie avancée | Panneau `#geom-panel`, 21 fonctions JS, ratios φ/√2/√3/Fibonacci, triangles, Broadbent, arcs |
| D — Orientation astrale | `SITES_ORIENTATION` (9 sites), popup enrichi, modal contribution, migration 003 |
| E — Validation | 21 nouvelles fonctions + 11 existantes vérifiées |

**Livrables :** `TELLUX_AUDIT_CORPUS_SITES.md`, code dans `tellux_v6_design.html` (à reporter dans `tellux_CORRECT.html`).

**⚠️ Point d'attention :** le module géométrie et l'orientation astrale ont été développés dans `tellux_v6_design.html`. Il faut reporter ces ajouts dans `tellux_CORRECT.html` (source de vérité) lors de la prochaine session code.

---

## 4. Validation scientifique (post-gel, pré-voie B)

- **E-1.** Refactoring `FAILLES_CORSE` en segments LineString (gain précision ±300 m).
- **E-2.** Implémentation tests automatiques H55–H88.
- **E-3.** Externalisation `SITES[]` dans JSON hébergé.
- **E-4.** Protocole calibration Trifield TF2 standardisé (mesures en aveugle parallèle).
- ### 4.4 B-MESURES — Contribution utilisateurs + auto-correction du modèle

**Objectif de fond** : faire passer Tellux de *cartographie théorique* à *instrument scientifique vivant* où les mesures terrain corrigent et affinent le modèle de calcul. Brique pour l'un des objectifs fondateurs du projet.

**Principes :**
- Lecture de la carte reste 100% anonyme, aucune friction à l'entrée
- Contribution d'une mesure nécessite un compte (Supabase Auth magic link — pas de mot de passe à retenir)
- Une mesure contribuée est visible uniquement par son auteur, sauf activation d'une couche globale opt-in
- Qualification progressive des mesures : score de fiabilité basé sur protocole + placement, expiration automatique des low-score
- Claude reste hors de la boucle d'ingestion temps réel (coût + non-pertinent). Analyses offline / batch uniquement.

**Sous-tickets :**
- B-MESURES-1 : Schéma Supabase `mesures` + RLS (lecture perso / couche publique filtrée par score)
- B-MESURES-2 : Supabase Auth magic link, flow connexion/déconnexion, templates email customisés
- B-MESURES-3 : UI contribution — zoom minimum requis, placement par clic carte, formulaire (valeur, unité, protocole checkboxes, description lieu)
- B-MESURES-4 : UI affichage — mesure perso sur carte (auteur uniquement), bouton couche "toutes les mesures" avec cluster Leaflet
- B-MESURES-5 : Score de fiabilité serveur (fonction Edge ou trigger Postgres), règle d'expiration low-score
- B-MESURES-6 : Intégration dans `calcHuman()` — pondération locale par mesures validées (méthodologie à définir : gaussienne par distance, recalibration coefficient, etc.)
- B-MESURES-7 : Protocole de mesure documenté (page dédiée, validée vis-à-vis de la position épistémique)
- B-MESURES-8 : RGPD — CGU, politique de confidentialité, droits utilisateur, export/suppression compte

**Pré-requis de conception :**
- La méthodologie d'auto-correction du modèle est un **sujet scientifique**, pas une simple feature. À co-concevoir avec les associations EM partenaires et (idéalement) un relecteur scientifique.
- Protocole de mesure à stabiliser **avant** l'implémentation, sinon le scoring ne veut rien dire.

**Déclencheur** : après les premiers retours des associations EM sur v6, pour intégrer leurs attentes dans la conception.

**Estimation réaliste** : 3 à 6 semaines de travail concentré + phase de test terrain avant ouverture publique.

**Statut** : voie B, à ouvrir après livraison v6 aux associations et premiers retours.

---

### 4.5 B-PIEZO — Modélisation piézoélectricité substrat corse

**Objectif :** Aller au-delà de l'index binaire piézoélectrique actuel (granit oui/non) pour estimer un gradient de contrainte mécanique × propriétés diélectriques du substrat. Données BRGM (failles actives, géologie détaillée) + modèle Biot-Savart sous contrainte tectonique.

- **B-PIEZO-1 :** Caractérisation diélectrique granit/schiste corse dans le formalisme ITU-R P.2040-2 (hypothèse H91)
- **B-PIEZO-2 :** Interface cartographique gradients piézo (couche vectorielle couleur continue, non binaire)
- **B-PIEZO-3 :** Tests terrain mesures ELF sur failles actives identifiées (protocole triple aveugle, partenariat BRGM Corse)

**Statut :** Voie B, post v6.

---

### 4.6 B-CHRONO — Module chronobiologique

**Objectif :** Intégrer les fenêtres temporelles optimales pour la pratique en maquis corse dans le module prescription. Données : CAR matinal, concentration phytoncides après-midi, variabilité Kp géomagnétique.

- **B-CHRONO-1 :** Index de qualité chronobiologique par heure et saison (modèle NOAA Kp + données phénologiques maquis)
- **B-CHRONO-2 :** UI calendrier : « Fenêtres optimales de la semaine » dans le module prescription
- **B-CHRONO-3 :** Protocole de validation H88 (partenariat CHU Ajaccio, mesures cortisol salivaire)

**Statut :** Voie B, post v6. Hypothèses H87 + H88.

---

### 4.7 B-HABITAT — Module habitat vernaculaire corse

**Objectif :** Valoriser l'atténuation RF passive des matériaux de construction corses (granit, schiste, murs épais). Données ITU-R P.2040-2 + mesures terrain dans bâti vernaculaire.

- **B-HABITAT-1 :** Calcul d'atténuation estimée par type de bâti (granit 100 cm → 30-50 dB, selon ITU-R P.2040-2)
- **B-HABITAT-2 :** Couche cartographique bâti dense corse (BDTOPO IGN)
- **B-HABITAT-3 :** Fiche recommandation « Optimiser son habitat » (vocabulaire A8 obligatoire)

**Statut :** Voie B, post v6. Hypothèse H86 (atténuation passive).

---

### 4.8 B-FAUNE — Module faune sensible

**Objectif :** Croiser les données de distribution de la faune sensible aux CEM avec les scores EM Tellux pour identifier les zones de conflits potentiels.

- **B-FAUNE-1 :** Couche chiroptères (données PGHB Corse) × score EM → carte de pression
- **B-FAUNE-2 :** Interface LPO Corse : accès données nidification balbuzard Scandola (H86)
- **B-FAUNE-3 :** Protocole drone ovins/caprins corses (H85) — partenariat chambre d'agriculture

**Statut :** Voie B, post v6. Hypothèses H85 + H86.

---

### 4.9 B-ZONES — Zones à exposition réduite

**Objectif :** Générer automatiquement des zones de récupération (jamais « safe place » ou « sanctuaire EHS » — voir vocabulaire A8) basées sur le score EM combiné. Outil d'aide à la décision, pas un diagnostic.

- **B-ZONES-1 :** Algorithme de sélection zones (score EM ≤ 1/5, couverture végétale, altitude)
- **B-ZONES-2 :** UI couche « Zones à exposition réduite » avec densimètre et légende explicative
- **B-ZONES-3 :** Export PDF « Fiche lieu » pour usage terrain (mairies, associations)

**Statut :** Voie B, post v6. Dépend de B-CHRONO pour la dimension temporelle.

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
| 6 | Stratégie subventions | 🟡 |
| 7 | B-MESURES : contribution + auto-correction modèle | 🔴 |
| 8 | B-PIEZO : modélisation piézoélectricité substrat corse | 🔴 |
| 9 | B-CHRONO : module chronobiologique (CAR + phytoncides + maquis) | 🟡 |
| 10 | B-HABITAT : module habitat vernaculaire corse (atténuation RF passive) | 🟡 |
| 11 | B-FAUNE : module faune sensible (chiroptères, balbuzard, ovins/caprins) | 🟠 |
| 12 | B-ZONES : module zones à exposition réduite (recommandation espaces récupération) | 🟡 |

**Axe 2 — Framer :** Webflow abandonné. Framer retenu. L'app cartographique (HTML/Leaflet) reste indépendante ; Framer = landing page marketing.

**B-VISITES — Mode visite guidée patrimoine :** Fiches enrichies par site, liées depuis les popups Leaflet. Argument patrimonial pour mairies.

**B-STRUCTURES — Structures EM remarquables :** Étude de faisabilité long terme. Disclaimer obligatoire.

---

## 6. Chantiers structurels transverses

### S-1. Structure juridique — arbitrage urgent

Options comparées dans `TELLUX_STRUCTURE_JURIDIQUE.md`. Non tranché. Soleil décide après lecture.

### S-2. Pérennité technique — risque monofichier HTML

`tellux_CORRECT.html` fait ~7 000 lignes. Mesures immédiates : git versionné. Mesure structurelle : migration modulaire (voie B axe 4).

### S-3. Stratégie subventions et financement

Court terme : CTC. Moyen terme : OEC, ADEME, ANR, LEADER. Voir `TELLUX_FINANCEMENT.md`.

---

## 7. Items à vérifier

- Migration WMS Géoplateforme (anciennement Géoportail).
- Sélecteur culture personnalisée (module agronomie).
- Template PDF propre pour `exportPermaPDF`.
- Lazy-loading couches lourdes (performances mobiles).

---

## 8. Agenda court terme (avril – mi-mai 2026)

| Semaine | Tâche | Responsable | État |
|---|---|---|---|
| S15 (7-13 avr) | Design validé, logo V7 gelé, dossier v7 produit | ✅ fait | — |
| S15 (8 avr) | Bugs A-2 à A-15 résolus, gamification, lProd, diagnostic fusionné | ✅ fait | — |
| S15 (9 avr) | Audit infrastructure + 7 actions sécurisation | ✅ fait | — |
| S15 (10 avr) | Flux mesure : 3 bugs + FAB + prescription + audit + tests | ✅ fait | — |
| S15 (12 avr) | Session 6 : clarification épistémique (7 missions) | ✅ fait | — |
| S15 (13 avr) | Sonnet Patrimoine : géométrie, orientation, audit corpus | ✅ fait | — |
| S15 (13 avr) | Mise à jour fichiers contexte (roadmap, recovery, instructions) | ✅ fait | — |
| **S16 (14 avr)** | **Session Opus : finitions pré-envoi EM** | **Cowork** | `[À COMPLÉTER]` |
| S16 (14-20 avr) | Reporter géométrie/orientation dans `tellux_CORRECT.html` | Cowork | — |
| S16 | Test flux mesure bout en bout (5 scénarios) | Soleil | — |
| S16 | Arbitrage structure juridique | Soleil | — |
| S17 (21-27 avr) | A-1g GPS, A-4b audit couches, A-8 captures HD | Cowork + Soleil | — |
| S18 (28 avr – 4 mai) | Gel voie A, tag v6.1.0 | Soleil + Cowork | Tests OK |
| S19 (5-11 mai) | Dépôt CTC | Soleil | Dossier complet |
| S19-S20 | Validation scientifique E-1 à E-4 | Cowork | Voie A gelée |

---

## 9. Stratégie partenariats

### 9.1 Cibles et critères « prêt à envoyer »

| Cible | Critère | État | Documents |
|---|---|---|---|
| Associations EM (PRIARTEM, CRIIREM, collectifs) | Carte + double indice + disclaimer santé | ✅ PRÊT | `TELLUX_KIT_ENVOI_EM.md` |
| Agronomie / permaculture | Module parcelle + 3 relevés terrain H63 | ⚠️ Manque terrain | `TELLUX_DOSSIER_AGRO_BIO.md` |
> **Note B-MESURES** : la co-conception du module contribution avec les associations EM partenaires (PRIARTEM/CRIIREM, LPO Corse, autres) devient un axe stratégique. Le module n'est pas livré dans v6 — il sera conçu avec les retours des premières associations contactées.
> data: ajout ticket B-MESURES voie B (contribution utilisateurs + auto-correction modèle)
| Mairies / patrimoine | 5+ fiches B-VISITES + module géométrie opérationnel | ⚠️ Fiches manquantes | `TELLUX_DOSSIER_MAIRIES_PATRIMOINE.md` |
| Scientifiques — Géophysiciens | Carte + GPS vérifiés + alignements | ⚠️ GPS A-1g | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |
| Scientifiques — EM & santé | Double indice + corpus A | ✅ PRÊT | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |
| Scientifiques — Alignements | 15 alignements Broadbent + géométrie avancée | ✅ PRÊT (nouveau) | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |
| Scientifiques — Agronomie EM | Module parcelle + 1 mesure terrain | ❌ Terrain | `TELLUX_DOSSIER_SCIENTIFIQUES.md` |

### 9.2 Séquence de prise de contact

**Phase 1 — Immédiat (avril 2026) :** Associations EM. Scientifiques profils A, B, C. Pas de dépendance terrain.

**Phase 2 — Après relevés terrain (mai–juin 2026) :** Agronomie/permaculture. Scientifiques profils D, E.

**Phase 3 — Après B-VISITES (été 2026) :** Mairies rurales. DRAC.

### 9.3 Notes stratégiques

**Ciblage mairies :** communes < 5 km d'un alignement Broadbent OU < 2 km d'une source EM. Liste à produire par croisement automatique.

**Levier patrimonial :** B-VISITES est l'argument d'entrée pour mairies rurales non concernées par l'EM. Le module géométrie avancée (session 13 avril) renforce considérablement cet argument.

**Audit de solidité :** voir `TELLUX_AUDIT_MODELE.md`.

### 9.4 Veille corpus scientifique

Veille semi-automatique retenue (Scholar Alerts + Claude). 8 alertes configurées. ~15 min/semaine.

---

## 10. Vision modules (long terme)

### 10.1 Mode Agronomie

État : tab Diagnostic + tab Cultures Corse + tab Design. Prochaines étapes : zonation PDC interactive, calculateur swale, base semences corses, export PDF, données météo.

### 10.2 Mode Diagnostic & Géobiologie

État : panneau Géobiologue + section Équilibrer. Prochaines étapes : diagnostic par pièce, calibration magnétomètre, bibliothèque matériaux, mode Rééquilibrage, calendrier biodynamique.

### 10.3 Module Géométrie avancée (nouveau — 13 avril 2026)

État : panneau latéral `#geom-panel`, sélection 3-20 sites, calculs distances/ratios/triangles/alignements/arcs/orientations, visualisation carte, export JSON, modal bibliographie (Broadbent, Thom, Leplat, Crowhurst, Hoskin, Santucci).

Prochaines étapes : intégration données orientation crowdsourcées (table Supabase prête), enrichissement corpus SITES_ORIENTATION au-delà des 9 sites documentés.

### 10.4 Positionnement Tellux

Plateforme de décision environnementale : bien-être individuel, agriculture régénérative, gestion territoriale, recherche participative. Ancrage dans données institutionnelles vérifiables + corpus peer-reviewed à 3 niveaux.

---

## 11. Actions différées

| ID | Action | Priorité |
|---|---|---|
| F-1 | Sauvegarde brouillon formulaire (localStorage) | 🟡 |
| F-2 | Upload photo/pièce jointe contributions | 🟡 |
| F-5 | Formulaire bottom-sheet mobile | 🟠 |
| F-6 | Validation temps réel formulaire | 🟡 |
| F-9 | Mode hors-ligne (file localStorage → sync) | 🟠 |
| D-1 | Retirer bouton "Diagnostic terrain" du sidebar | 🟢 |
| D-2 | Badges validation par méthode prescription | 🟡 |
| D-3 | Historique mesures par session + export CSV | 🟡 |
| INF-8 | Achat domaine tellux.fr ou tellux.corsica | 🟡 |
| JSON-1 | Externaliser failles, prod, hypothèses en JSON | 🟡 |

---

## 12. Risques ouverts

- **Régression GPS** — coordonnées sites dérivent entre sessions. Solution : JSON externe (A-1g + E-3).
- **Dépendance fournisseur** — Supabase + Cloudflare. Faible à court terme.
- **Charge cognitive monofichier** — ~7 000 lignes. Git + tests manuels en attendant voie B axe 4.
- **Absence relecteur scientifique** — corpus 130 études + 88 hypothèses non relus par un pair.
- **Retard dépôt CTC** — mitigation : découpler captures du gel.
- **Dépôt nom « Tellux »** — à évaluer selon budget.
- **⚠️ Risque UX — premier envoi EM** — les textes d'interface doivent être relus pour cohérence avec la position épistémique avant tout envoi. Session 14 avril dédiée.
- **⚠️ Divergence fichiers HTML** — le module géométrie est dans `tellux_v6_design.html` mais pas encore dans `tellux_CORRECT.html`. À reporter S16.
