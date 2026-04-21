# Changelog

Toutes les modifications notables de ce projet sont documentées dans ce fichier.

Format : [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/)
Versioning sémantique : [SemVer](https://semver.org/lang/fr/)

---

## [2.5.0] — 2026-04-21

### Modifié — Biot-Savart réel sur réseau HTA (PR `feat/biot-savart-reel-hta`)

- `calcMagneticELF` migré vers `calcMagneticELF_v2` : formule segment fini + correction triphasée sur 11 735 segments réels (expansion des 8386 polylines `hta_lines` Supabase) au lieu de 8 axes hardcodés
- Courant unique 225 A × `chargeFacteur` (Option B, dataset sans champ voltage — dette migration SQL)
- Champ RMS explicite (facteur 1/√2)
- Grille spatiale précalculée 1 km × 1.35 km au chargement `loadReseau` (10 704 tuiles)
- Calcul par clic : < 2 ms en moyenne (cible 50 ms largement battue)

### Ajouts

- Fonction `calcBiotSavartSegment()` — calcul unitaire par segment avec correction triphasée k=0.5 au-delà de 20 m
- Fonction `buildSegmentGrid()` + `getSegmentsNear()` — pré-indexation spatiale
- Fonction `runELFRegressionTest()` — validation sur 20 points témoins (5 urbains, 5 ruraux, 5 éloignés, 5 mégalithiques)
- Flag `USE_ELF_V2 = true` — bascule v1/v2 pour rollback d'urgence sans redéploiement

### Déprécié

- `calcMagneticELF_v1` conservée pour référence et rollback, sera supprimée en v3 après validation tiers
- 8 axes `HTA_SEGS` hardcodés : uniquement utilisés par v1, sortiront avec v1

### Documentation

- `docs/notes-tri/AUDIT_TELLUX_NIVEAU2_NOTE_EVOLUTION_BIOTSAVART_v1.md` — note scientifique complète avec tableau comparatif 20 points

---

## [2.4.0] — 2026-04-20

### Ajouts — Précision modèle (PR `feat/precision-radon-mnt-tdf`)

- Reverse geocoding commune via `api-adresse.data.gouv.fr` (`reverseGeocodeCommune`, cache `COMMUNE_CACHE`)
- Altimétrie réelle via IGN RGE Alti (`fetchAltitudeIGN`, cache `ALTITUDE_CACHE`)
- Correction rayonnement cosmique dans `calcGammaAmbient` : composante altitude ×4–5 selon z réel (vs 0 m fixe)
- Intégration 10 émetteurs TDF/radiodiffusion corse dans `calcRF` (modèle isotrope S = PAR/4πd², plafond 50 000 µW/m²)
- Jeu de données `public/data/radon_communes_level3_corse.json` — 28 communes niveau 3 décret 2018-434 (IRSN)
- Jeu de données `public/data/tdf_emitters_corse.json` — 10 émetteurs avec PAR estimées (ANFR/CSA)
- Notes méthodologie sources : `docs/data-sources/radon_communes_level3_corse_notes.md`, `docs/data-sources/tdf_emitters_corse_notes.md`
- Détection radon triple : règle département 2A entier + INSEE explicite + nom de commune normalisé
- Handler click carte rendu asynchrone avec `Promise.all([reverseGeocodeCommune, fetchAltitudeIGN])`

### Modifié — Précision modèle

- `calcGammaAmbient(lat, lon, altitude_m)` : accepte altitude réelle en 3ème paramètre
- `calcRadonPotential(lat, lon, options)` : accepte `commune_info`, retourne `class_source` et `official_classification`
- `calcAll_v2(lat, lon, options)` : passe `commune_info` et `altitude_m` aux fonctions calc sous-jacentes
- `calcRF` : blocs contributions structurés avec `source_type: 'broadcast_TDF'`
- `.gitignore` : `DATA/` → `/DATA/` (ancrage racine, corrige conflit Windows case-insensitive)
- Fond de carte : fond unique IGN Plan V2, suppression du switcher de fond, `maxZoom` 20 (`maxNativeZoom` 19)

### Ajouts — Interface (PR `feat/ui-menu-reorg`)

- 3 groupes accordéons thématiques dans la sidebar : « Modèle EM », « Sources anthropiques », « Contexte naturel »
- Panneau « Conditions actuelles » unifié : 3 sections repliables (géomagnétique, réseau électrique, météo/autre)
- Sparkline inline SVG (180×40 px) de la charge réseau Corse heure par heure (`PROFIL_HORAIRE_CORSE`)
- Marqueur rouge sur l'heure courante dans la sparkline
- Modal contribution restructuré en 3 onglets : Observation, Mesure terrain, Capteurs appareil (placeholder)

### Modifié — Interface

- Terminologie : « prédiction » → « champ composite estimé » dans toute l'interface (libellés, popups, titres)

---

## [2.3.0] — 2026-04-19

### Ajouts — Mode Expertise (PR `feat/v2-phase3-expertise`)

- Mode Expertise avec `EXPERT_WEIGHTS_DEFAULT` et `EXPERT_BOUNDS_DEFAULT` (GELÉS — GELÉ-001)
- Fonction `computeExpertComposite(lat, lon, weights)`
- Modal avertissement épistémique à l'activation du mode Expert
- Bandeau permanent rouge « MODE EXPERT ACTIF »
- Curseurs pondérations `w_M`, `w_RF`, `w_I` avec throttle 300 ms
- Export CSV enrichi UTF-8 BOM (`exportExpertCSV`)
- Partage URL hash `#/z=Z&c=LAT,LNG&m=DOM[&e=1]` (`shareURL`, `applyHashToMap`)
- Tests non-régression phase 3 (`tests/non-regression-v2-phase3.js`, catégories H–O, 7 invariants)

### Modifié

- Migration `calcPiezoScore` complète : retourne `susceptibility_nT`, plus d'appelant actif legacy

---

## [2.2.0] — 2026-04-19

### Ajouts — Modèle composite v2 phases 1 et 2

- `calcMagneticELF(lat, lon)` — champ basse fréquence (lignes HT, transformateurs)
- `calcRF(lat, lon)` — RF antennes ANFR
- `calcHeritageDensity(lat, lon)` — densité patrimoine (mégalithes + églises romanes)
- `calcAll_v2(lat, lon, options)` — orchestrateur multi-domaines
- Légende couleur Ocre (#C28533) / Porphyre (#8E2F1F) pour couches EM
- Popup v2 restructurée avec sections par domaine
- Section « À propos » réécrite (humilité épistémique, 3 formulations interdites)

### Corrigé

- Suppression de 10 occurrences « piézo » résiduelles (calcul et libellés)

---

## [2.1.0] — 2026-04-18

### Ajouts — Architecture en suite + mode Expertise phase 1–2

- DA v2 palette gelée : Ardoise, Pierre, Maquis, Ocre, Porphyre, Tyrrhénien
- Typographie Fraunces (titres) + IBM Plex Sans (corps)
- Sidebar desktop élargie à 420 px
- Aliasing typo corrigé (guillemets courbes → droits)

---

## [2.0.0] — 2026-04-14

### Architecture

- Pivot vers architecture en suite d'applications (`app.html`, `patrimoine.html`, `agronomie.html`)
- Suppression des fichiers historiques (`tellux_CORRECT.html`, `tellux_v6_design.html`, `TELLUX_LOGO_V7.html`)
- Remote GitLab désactivé, GitHub `dellahstella/tellux` devient remote unique
- Déploiement Cloudflare Workers via `wrangler.jsonc`
