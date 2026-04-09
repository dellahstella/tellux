# TELLUX — Feuille de route
**Dernière mise à jour :** 9 avril 2026 (session 4 — gel voie A)
**Remplace :** version session 3 (9 avril 2026)

---

## 1. État au 9 avril 2026 (post session 4)

| Composant | Référence | État |
|---|---|---|
| Code | `tellux_CORRECT.html` | **v7 — GELÉ pour envoi partenaires** |
| Dossier CTC | `CANDIDATURE_TELLUX_v7.docx` | v7, relecture Soleil en cours |
| Design | `DIRECTION_ARTISTIQUE_v2.md` | Validée et gelée |
| Guide fiches patrimoine | `TELLUX_GUIDE_FICHES_PATRIMOINE.md` | v2 — double fiche A/B + gamification |
| Déploiement | `tellux.pages.dev` | Cloudflare Pages, actif |
| Backend | Supabase PostGIS | Actif, connecté |
| Cible financement | CTC | Dossier multi-guichets en préparation |
| Porteur | Soleil (solo) | SARL Stella Canis Majoris, Bastia |

---

## 2. Statut bugs voie A — tous résolus

| Bug | Description | État |
|---|---|---|
| A-1 | Anneaux Cap Corse coordonnées erronées | ✅ `43.17654°N 9.60008°E` exact |
| A-2 | Alignements chargement lourd | ✅ PRECOMPUTED_ALIGNMENTS |
| A-3 | Panneau non lié au toggle couche | ✅ `closeLayerPanel()` |
| A-4 | Carte bloquée | ✅ Comportement intentionnel maxBounds |
| A-4b | Audit couche ↔ panneau ↔ légende | ✅ Résolu — pattern vérifié |
| A-5 | FAB mesure point violet disparaît | ✅ `_contribPending` flag |
| A-6 | CSS boutons actifs manquants | ✅ Classes `.on-*` ajoutées |
| A-7 | Popup bloqué par zones anomalies | ✅ `interactive:false` tous rectangles |
| A-8 | Captures HD dossier CTC | ⏳ Soleil — après vérifications terrain |
| A-9 | Doublons lProd/HT | ✅ |
| A-10 | Fusion formulaire diagnostic | ✅ |
| A-11 | FIFO 4 couches max | ✅ |
| A-12 | Score agronomie 61.4/10 | ✅ Normalisé 0-10 |
| A-13 | Anneaux Cap Corse approximatif | ✅ → A-1 exact |
| A-14 | Couches patrimoine auto-activées | ✅ Cache navigateur — pas de bug code |
| A-15 | Confetti intempestif | ✅ Réservé au 1er test |
| FAB double-clic | 1er clic inactif | ✅ `setTimeout(0)` map.once |

**La voie A est gelée. Le HTML ne doit plus être modifié sauf régression critique constatée.**

---

## 3. Prochaines actions côté Soleil (hors Cowork)

Ces tâches appartiennent à Soleil et ne nécessitent pas de code.

### 3.1 Envoi partenaires — préparation

- **Récupération contacts** : associations EM, mairies proches de sites, scientifiques identifiés
- **Vérification structure juridique** : arbitrage SARL / SASU / asso (voir S-1 ci-dessous)
- **Adaptation documentation par cible** : kit EM, dossier agronomie, dossier patrimoine — chaque cible ne reçoit pas le même angle

### 3.2 Captures d'écran A-8

Requis : servir le fichier via HTTP (pas `file://`). Options :
- `npx serve .` en local puis `http://localhost:3000`
- Déploiement Cloudflare Pages (`tellux.pages.dev`)

Vues attendues (1920×1080, light mode) :
1. Vue d'ensemble Corse + couche hotspots
2. Popup site mégalithique avec Indice Tellux complet
3. Module agronomie — tab Diagnostic + tab Design
4. Couches réseaux EDF+ANFR actives simultanément
5. Panneau hypothèses avec H-xx
6. Vue mobile (375px) bottom sheet

### 3.3 GPS audit sites

Session Google Earth pour vérifier les coordonnées des autres sites dans `SITES[]`. Priorité : Filitosa, Cauria, sites Cap Corse. Solution structurelle associée : externaliser dans `SITES_REFERENCE.json`.

---

## 4. Chantiers ouverts (pour session Opus dédiée)

Ces chantiers sont documentés, priorisés, mais ne nécessitent pas de code immédiat.

### 4.1 B-VISITES — Fiches patrimoine

**Guide de rédaction :** `TELLUX_GUIDE_FICHES_PATRIMOINE.md` v2

**Deux fiches par site :**
- **Fiche A — Territoire** : narration, mythologie, légende, histoire, terroir. Libre d'accès.
- **Fiche B — Tellux** : score EM, hypothèses H-xx, outils Tellux, préconisations. Débloquée par visite terrain (géoloc ±100m) OU résolution d'hypothèse associée.

**Gamification collection (style Pokémon Go) :**
- La beauté de la carte crée l'envie d'explorer
- Badges : 🗿 Mégalitheur, 🔬 Investigateur, 🌿 Permaculteur, 📡 Sentinelle, 🏆 Archiviste Corse
- Image générée par site (style gravure naturaliste sobre — palette Tellux)

**Sites prioritaires première vague :** Filitosa, Cauria (Stantari+Rinaghju+Palaggiu), Anneaux Cap Corse, San Michele de Murato, site choix terrain Soleil

**Langue :** français uniquement pour l'instant. Noms corses dans les titres dès maintenant. Traduction corse intégrale = levier financement régional (CTC, FEADER).

**Questions en attente de décision Soleil :**
- Longueur fiche légère (300 mots) vs fiche complète (600 mots) ?
- Style image : gravure naturaliste / vectoriel / photomontage sobre ?
- Déblocage Fiche B : géoloc ±100m stricte ou tolérance plus large ?

### 4.2 B-AGRO — Module permaculture complet

- B-AGRO-1 : Zonation PDC interactive (zones 1-5 dessinables)
- B-AGRO-2 : Calculateur swale / bilan eau
- B-AGRO-3 : Base semences corses (30+ variétés INAO)
- B-AGRO-4 : Export plan design PDF
- B-AGRO-5 : Météo/ETP locales intégrées

### 4.3 B-GEO — Mode diagnostic géobiologique

- B-GEO-1 : Diagnostic par pièce (grilles Hartmann/Curry sur plan schématique)
- B-GEO-2 : Protocole calibration magnétomètre téléphone
- B-GEO-3 : Bibliothèque matériaux/solutions
- B-GEO-4 : Mode "Rééquilibrage" guidé
- B-GEO-5 : Calendrier biodynamique intégré

---

## 5. Voie B — Montée en gamme (horizon 3-6 mois)

Détails complets dans `TELLUX_MONTEE_EN_GAMME.md`.

| Axe | Sujet | Complexité |
|---|---|---|
| 1 | Exploitation écosystème Anthropic | 🟢-🟡 |
| 2 | Landing Framer (décision arrêtée) | 🟡 |
| 3 | Automatisation N8N | 🟡 |
| 4 | Migration architecture modulaire | 🔴 |
| 5 | Gouvernance et structure juridique | 🟡 |
| 6 | Stratégie subventions | 🟡 |

---

## 6. Chantiers structurels

### S-1. Structure juridique — arbitrage Soleil
Options : micro-entreprise, SASU, asso 1901, SCIC, SARL existante (Stella Canis Majoris). Implications fiscales et capacité subventions. Voir `TELLUX_STRUCTURE_JURIDIQUE.md`. **Non tranché.**

### S-2. Pérennité technique
Monofichier ~540 Ko / 7 000 lignes. Sauvegardes git versionnées à chaque session. Migration modulaire en voie B (axe 4).

### S-3. Stratégie subventions
Court terme : CTC. Moyen terme : OEC, ADEME, ANR, LEADER. Long terme : partenariat laboratoire. Voir `TELLUX_FINANCEMENT.md`.

---

## 7. Validation scientifique (post-gel)

- E-1 : Refactoring `FAILLES_CORSE` en segments LineString
- E-2 : Implémentation tests automatiques H55–H88
- E-3 : Externalisation `SITES[]` → `SITES_REFERENCE.json`
- E-4 : Protocole calibration Trifield TF2 standardisé

---

## 8. Agenda (avril – mi-mai 2026)

| Semaine | Tâche | Responsable |
|---|---|---|
| S15 (7-13 avr) | Design, logo V7, dossier v7 | ✅ fait |
| S15 (8-9 avr) | Sessions code 1-4, tous A-xx résolus | ✅ fait |
| **S16 (14-20 avr)** | **Vérif juridique, récup contacts, adapt docs par cible** | **Soleil** |
| S16 | GPS audit sites (Google Earth) | Soleil |
| S17 (21-27 avr) | Captures A-8 (serveur HTTP) | Soleil |
| S17 | Envoi phase 1 : associations EM + scientifiques | Soleil |
| S18 (28 avr) | Session Opus : B-VISITES + fiches + gamification | Cowork |
| S19 (5-11 mai) | Dépôt CTC | Soleil |
| S20+ | Lancement voie B | Soleil + Cowork |

---

## 9. Partenariats — statut

| Cible | Prêt ? | Dépendance |
|---|---|---|
| Associations EM (PRIARTEM, CRIIREM) | ✅ | — |
| Scientifiques géophysiciens | ✅ | GPS audit A-1 |
| Scientifiques EM & santé | ✅ | — |
| Scientifiques alignements | ✅ | — |
| Mairies / patrimoine / DRAC | ⚠️ | B-VISITES 5 fiches |
| Agronomie / permaculture | ⚠️ | 3 relevés terrain H63 |

---

## 10. Risques ouverts

- **GPS régression** : coordonnées sites dérivent entre sessions. Solution : `SITES_REFERENCE.json` externe.
- **Monofichier** : 7 000 lignes, risque maintenance. Mitigation : git + tests manuels.
- **Absence second relecteur scientifique** : corpus 130 études non relu par pair. Chercher partenariat CEREGE/INRAE.
- **Retard dépôt CTC** : mitigation — découpler captures du gel si nécessaire.
- **Score agronomie** : correction appliquée mais calibration fine des plages 0-3/3-6/6-10 reste à faire.
- **Dépôt marque "Tellux"** : à évaluer selon budget.
