# Plan d'extraction du moteur de calcul Tellux

**Date :** 2026-04-26
**Auteur :** Cowork (analyse statique)
**Statut :** note de cadrage en lecture seule, à valider par Soleil avant ouverture du sprint Claude Code phase 0
**Source primaire :** `app.html` du repo `dellahstella/tellux`, révision locale du 2026-04-26 (7441 lignes, 441 KB)

## Objet

Cette note prépare l'extraction du moteur de calcul de `app.html` vers un module Node.js réutilisable. Elle ne propose aucune modification du code et ne contient aucun prototype. Elle décrit ce qui existe, identifie ce qui posera problème lors de l'extraction, et propose un découpage logique adossé aux regroupements observés dans le fichier source.

Toutes les références de ligne renvoient à la révision actuelle de `app.html`. Si le fichier est modifié entre la production de cette note et le sprint d'extraction, les numéros de ligne seront à reconfirmer par grep avant action.

## 1. Inventaire exhaustif des fonctions de calcul

### 1.1 Fonctions `calc*` du moteur

| Nom | Ligne | Signature | Description | Domaine |
|-----|------:|-----------|-------------|---------|
| `calcLCS1` | 2582 | `(lat, lon) → number` (nT) | Anomalie magnétique crustale, EMAG2v3 si chargé sinon repli LCS1 | M_static |
| `calcMagneticWMM` | 2746 | `(lat, lon) → {F, I, D} \| null` | Champ géomagnétique WMM 2025 par bilinéaire sur grille pré-calculée | M_static |
| `calcSq` | 2776 | `(lat) → number` (nT) | Variation diurne Sq paramétrique (Campbell 1989) | M_static |
| `calcExternalCorr` | 2813 | `() → number` (nT) | Correction externe AQU INTERMAGNET ou Kp fallback | M_static |
| `calcMagneticStatic` | 2855 | `(lat, lon) → object` | Orchestrateur composante statique : IGRF + LCS1 + Sq + correction externe | M_static |
| `calcBiotSavartSegment` | 3089 | `(segLat1, segLon1, segLat2, segLon2, obsLat, obsLon, currentA) → number` (nT) | Segment fini Biot-Savart scalaire avec correction triphasée | M_elf |
| `calcBiotSavartSegmentVec` | 3129 | idem → `{bx, by}` (nT) | Variante vectorielle 2D, dette ELF-VECTOR-001 | M_elf |
| `calcMagneticELF_v1` | 3174 | `(lat, lon, chargeFactor) → object` | Champ basse fréquence v1 sur 8 axes hardcodés (legacy, conservée pour rollback) | M_elf |
| `calcMagneticELF_v2` | 3291 | `(lat, lon, chargeFactor) → object` | Champ basse fréquence v2 : sommation vectorielle sur segments HTA réels + BT proxy + postes sources + éoliennes | M_elf |
| `calcRF` | 3602 | `(lat, lon) → object` | Densité de puissance RF µW/m² : FH + TDF broadcast + fond départemental | RF |
| `calcHuman` | 3678 | `(lat, lon) → number` | Marqué DEPRECATED v2 phase 1 (2026-04-19), conservé jusqu'à migration `calcAll` complète | transverse legacy |
| `calcWater` | 3748 | `(lat, lon) → number` | Proxy de conductivité hydrique locale | transverse |
| `calcAll_v2` | 3760 | `(lat, lon, options) → object` | Orchestrateur principal v2 multi-domaines | racine |
| `calcAll` | 3845 | `(lat, lng, options) → object` | Wrapper de compatibilité legacy, dérive `human/water/geo/score` depuis `calcAll_v2` | racine |
| `computeExpertComposite` | 3868 | `(v2, weights, bounds) → object` | Indice composite mode Expertise (gelé, GELE-001) | transverse |
| `calcGeoSusc` | 3923 | `(lat, lon) → number` (nT) | Susceptibilité magnétique géologique par IDW sur `GEO_SUSC_GRID` | transverse |
| `calcSubstrateContext` | 3933 | `(lat, lon) → object` | Contexte géologique : lithologie, susceptibilité, radon class, distances faille/eau | transverse |
| `calcRadonPotential` | 4097 | `(lat, lon, options) → object` | Potentiel radon : classe IRSN 2018 + boost décret 2018-434 + plages Bq/m³ | I |
| `calcGammaAmbient` | 4150 | `(lat, lon, altitude_m) → object` | Rayonnement gamma : cosmique paramétrique + boost points chauds (terrestre GELÉ NCRP-001) | I |
| `calcSkinDepth` | 4238 | `(lat, lon) → object` | Épaisseur de peau Cagniard 1953 par lithologie | transverse |
| `calcTelluricSecondary` | 4262 | `(lat, lon) → object` | Champ tellurique secondaire Wait 1954 paramétrique | transverse |
| `calcFaultProximity` | 4339 | `(lat, lon) → number` | Indicateur de proximité faille tectonique | transverse |
| `calcDecomposition` | 4358 | `(lat, lon) → object` | Décomposition diagnostique multi-sources | transverse |
| `calcN_RF_loo` | 5096 | `(lat, lon, others) → number` | Calibration RF leave-one-out | RF (calibration) |
| `calcRFcorrFactor` | 5109 | `(lat, lon) → number` | Facteur de correction RF par interpolation | RF (calibration) |
| `calcN_RF_calib` | 5121 | `(lat, lon) → number` | Application du facteur de correction au calcul RF | RF (calibration) |
| `calcDeltaRF` | 5126 | `(lat, lon) → number` | Écart RF entre observation et modèle | RF (calibration) |
| `calcN_RF` | 5692 | `(lat, lon) → number` | Norme RF de simulation (couplée au mode simulation) | RF (simulation) |
| `calcSimDelta` | 5706 | `(lat, lon) → number` | Delta de simulation appliqué au calcul `calcAll` legacy | transverse |

Total : **27 fonctions `calc*`**.

### 1.2 Helpers internes consommés par les `calc*`

| Nom | Ligne | Rôle |
|-----|------:|------|
| `dist` | 2885 | Distance haversine en kilomètres (formule inline) |
| `haversine` | 4329 | Distance haversine en mètres (variante) |
| `interpIDW` | 2534 | Interpolation inverse distance pondérée sur grille `[lat, lon, val]` |
| `igrfFallback` | 2719 | Lookup IGRF sur `IGRF14_GRID` via `interpIDW` |
| `tileKey` | 2940 | Clé de tuile spatiale pour `SEGMENT_GRID` |
| `buildSegmentGrid` | 2944 | Pré-indexation spatiale des segments HTA |
| `getSegmentsNear` | 2985 | Lookup des segments HTA proches |
| `buildBTSegmentGrid` | 2991 | Idem pour segments BT |
| `getBTSegmentsNear` | 3029 | Lookup segments BT proches |
| `getGeoType` | 3975 | Lookup lithologie sur `GEO_SUSC_GRID` (plus proche voisin) |
| `normCommuneName` | 4055 | Normalisation nom commune pour comparaison |
| `isCommuneRadonL3` | 4082 | Test appartenance commune au décret 2018-434 |

Total : **12 helpers**, tous purs sauf `buildSegmentGrid` et `buildBTSegmentGrid` qui mutent les variables globales `SEGMENT_GRID` et `BT_SEGMENT_GRID` lors de la construction de l'index.

## 2. Constantes et données capturées par fermeture

### 2.1 Constantes physiques inline

| Nom | Ligne | Valeur ou nature |
|-----|------:|-------------------|
| `HTA_BASE_CURRENT_A` | 2923 | `225` (ampères, courant moyen ligne HTA) |
| `BT_BASE_CURRENT_A` | 2924 | `60` (ampères, courant moyen distribution BT) |
| `TILE_SIZE_DEG` | 2933 | `1 / 111.32` (degrés, taille tuile spatiale) |
| `WMM_STEP` | 2727 | `0.05` (degrés, pas grille WMM) |
| `MU0_OVER_2PI` | 3350 (inline) | `2e-7` (T·m/A, intra-fonction) |
| `METERS_PER_DEG_LAT` | 3090, 3130 (inline) | `111320` (intra-fonction Biot-Savart) |
| `METERS_PER_DEG_LON` | 3091, 3131 (inline) | `111320 × cos(42°)` (intra-fonction) |
| Coefficients NCRP 94 | 4143-4160 (commentaire) | Formule `13·U + 5.4·Th + 42·K`, **GELÉ NCRP-001** (placeholder dans `calcGammaAmbient`) |
| `SIGMA_ROCK` | 4218 | Conductivité par lithologie (S/m), Wait 1954 / Chave 2012 |
| `RADON_CLASS_BY_LITHOLOGY` | 3939, 4102 (intra-fonction, dupliqué) | Mapping lithologie → classe IRSN |
| `ACTIVITY_RANGES` | 4117 (intra-fonction) | Plages Bq/m³ par classe radon |

### 2.2 Datasets inline (capturés par fermeture, importables directement)

| Nom | Ligne | Taille approx. |
|-----|------:|----------------|
| `IGRF14_GRID` | 2497 | grille IGRF-14 pré-calculée pour la Corse |
| `LCS1_GRID` | 2514 | grille LCS-1 satellite (champ lithosphérique) |
| `CRUSTAL_REFS` | 2594 | 5 références mondiales (Bangui, Kursk, Vredefort, Ries, Chicxulub) |
| `CARTORADIO_STATS` | 2887 | stats agrégées 2A/2B antennes ANFR |
| `DENSITY` | 2894 | densité fond départemental RF |
| `FH_POINTS` | 2901 | faisceaux hertziens corses |
| `ELF_TEST_POINTS` | 3454 | 20 points de test régression |
| `EXPERT_WEIGHTS_DEFAULT` | 3864 | `{ M: 0.4, RF: 0.4, I: 0.2 }` **GELÉ GELE-001** |
| `EXPERT_BOUNDS_DEFAULT` | 3865 | `{ ELF_nT: [0,1000], RF_uW_m2: [0,1000], GAMMA_nSv_h: [50,250] }` **GELÉ GELE-001** |
| `EXPERT_EPISTEMIC_NOTE` | 3866 | chaîne note épistémique permanente **GELÉ GELE-001** |
| `GEO_SUSC_GRID` | 3893 | grille de susceptibilité géologique IDW |
| `FAILLES_CORSE` | 4276 | failles tectoniques BRGM + Ghilardi 2017 + D'Anna 2019 |
| `THERMAL_SOURCES_CORSE` | 4298 | sources thermales |
| `PROFIL_HORAIRE_CORSE` | 6790 | profil horaire de charge réseau (24 valeurs) |

### 2.3 Datasets chargés dynamiquement

| Nom | Mode de chargement | Ligne du loader |
|-----|--------------------|-----------------|
| Grille EMAG2v3 (raster NOAA) | `fetch` arcgis NCEI | 2546 (`fetchEMAG2`), 2561 (`preloadEMAG2`) |
| `WMM_GRID`, `WMM_INDEX` | `fetch` `public/data/wmm_2025_grid_corse.json` | 2728 (`loadWMMGrid`) |
| `EMAG2_CACHE` | mutable, alimenté par `fetchEMAG2` | 2544 (déclaration) |
| `TDF_EMITTERS` | `fetch` `public/data/tdf_emitters_corse.json` | 3517 (`loadTDFEmitters`) |
| `POSTES_SOURCES` | `fetch` `public/data/postes_sources_corse.json` | 3540 (`loadPostesSources`) |
| `EOLIENNES_DATA` | `fetch` `public/data/eoliennes_corse.json` | 3563 (`loadEoliennesData`) |
| `POINTS_CHAUDS_RADIO` | `fetch` `public/data/points_chauds_radio_corse.json` | 3585 (`loadPointsChaudsRadio`) |
| `HTA_SEGMENTS_DATA`, `SEGMENT_GRID` | construit depuis fetch Supabase `hta_lines` | dans `loadReseau` (5278) |
| `BT_SEGMENTS_DATA`, `BT_SEGMENT_GRID` | construit depuis fetch Supabase `bt_lines` | 3037 (`loadBTLinesAsync`) |
| `RADON_L3_INSEE_SET`, `RADON_L3_NAME_SET`, `RADON_L3_SOURCE` | mutables, alimentés par `loadRadonCommunesL3` | 4051-4061 |
| `PROD_ELECTRIQUE` | chargé par `loadProd` | 5206 |

Pour l'extraction, ces datasets devront soit être chargés en amont par le hôte (Worker, Edge Function, navigateur) et passés au moteur via injection, soit le moteur expose un loader Node.js dédié qui lit le fichier depuis disque (pour usage serveur) et un loader DOM-fetch (pour usage navigateur).

### 2.4 Variables globales mutables consommées par les `calc*`

| Nom | Ligne | Statut | Risque |
|-----|------:|--------|--------|
| `SEGMENT_GRID` | construite à `buildSegmentGrid` | mutable | `calcMagneticELF_v2` la lit ; doit être passée en paramètre ou injectée |
| `HTA_SEGMENTS_DATA` | id. | mutable | id. |
| `BT_SEGMENT_GRID`, `BT_SEGMENTS_DATA` | id. | mutable | id. |
| `chargeFacteur` | global mutable | dépend de `loadChargeReseau` | `calcMagneticELF_v2` lit fallback `chargeFacteur` si `chargeFactor` non fourni — couplage à découpler |
| `curKp` | global mutable | dépend de `loadNOAA` | `calcAll_v2` lit `curKp` pour le snapshot Kp |
| `USE_ELF_V2` | constante (`true`) ligne 3427 | flag | flag de bascule v1/v2 |
| `USE_BT_SEGMENTS` | constante (`false`) ligne 3446 | flag de hotfix | déclencheur du retour aux `BT_ZONES` proxy |
| `window._btDisabledWarned` | flag de log warning | mutable | ligne 3318, à retirer ou neutraliser |

Toutes ces variables doivent devenir des paramètres explicites du moteur ou être encapsulées dans un objet d'état injecté.

## 3. Dépendances entre fonctions

Représentation textuelle, fonctions racines en haut, feuilles en bas.

```
calcAll → calcAll_v2, calcSimDelta
calcAll_v2 → calcMagneticStatic, calcMagneticELF_v2 (ou v1), calcRF,
             calcGammaAmbient, calcRadonPotential, calcSubstrateContext,
             calcWater, calcFaultProximity, calcTelluricSecondary
calcMagneticStatic → igrfFallback, calcLCS1, calcSq, calcExternalCorr
calcLCS1 → interpIDW (sur LCS1_GRID ou EMAG2_CACHE)
igrfFallback → interpIDW (sur IGRF14_GRID)
calcMagneticWMM → lookups directs WMM_INDEX (bilinéaire) + nearest-neighbor fallback
calcMagneticELF_v2 → calcBiotSavartSegmentVec, getSegmentsNear, getBTSegmentsNear,
                     dist (pour POSTES_SOURCES, EOLIENNES_DATA, PROD_ELECTRIQUE)
calcMagneticELF_v1 → calcBiotSavartSegment, dist
calcRF → dist (sur FH_POINTS, TDF_EMITTERS), lookup DENSITY
calcGammaAmbient → dist (sur POINTS_CHAUDS_RADIO)
calcSubstrateContext → getGeoType, calcGeoSusc, dist (sur FAILLES_CORSE)
calcGeoSusc → interpIDW (sur GEO_SUSC_GRID)
calcRadonPotential → getGeoType, isCommuneRadonL3, normCommuneName
calcSkinDepth → getGeoType (lookup SIGMA_ROCK)
calcTelluricSecondary → calcSkinDepth, getGeoType
calcFaultProximity → dist (sur FAILLES_CORSE)
calcDecomposition → composition de plusieurs calc* précédents
computeExpertComposite → consomme un objet `v2` produit par calcAll_v2
                          + EXPERT_WEIGHTS_DEFAULT, EXPERT_BOUNDS_DEFAULT
calcN_RF_loo, calcRFcorrFactor, calcN_RF_calib, calcDeltaRF → suite calibration RF
calcN_RF, calcSimDelta → suite simulation
```

**Fonctions feuilles** (n'appellent aucune autre fonction du moteur) : `dist`, `haversine`, `interpIDW`, `igrfFallback`, `calcSq`, `calcLCS1`, `calcExternalCorr`, `calcBiotSavartSegment`, `calcBiotSavartSegmentVec`, `calcGeoSusc`, `getGeoType`, `normCommuneName`, `isCommuneRadonL3`, `tileKey`.

**Fonctions racines** (appelées depuis le code de rendu de la carte ou les handlers UI) : `calcAll`, `calcAll_v2`, `computeExpertComposite`. Toute extraction qui préserve le comportement doit garantir que ces trois racines retournent strictement les mêmes objets pour les mêmes entrées.

## 4. Couplages avec le DOM, le navigateur ou des APIs externes

### 4.1 Fonctions `calc*` strictement pures

Les fonctions suivantes sont pures au sens de l'extraction : elles ne touchent ni au DOM, ni à `window`, ni à `localStorage`, ni à `fetch`, et leurs side effects se limitent à des `console.warn` ou `console.log` éventuels que l'extraction pourra optionnellement supprimer.

`calcMagneticStatic`, `calcLCS1`, `calcSq`, `calcExternalCorr`, `calcBiotSavartSegment`, `calcBiotSavartSegmentVec`, `calcRF`, `calcGammaAmbient`, `calcRadonPotential`, `calcSubstrateContext`, `calcGeoSusc`, `calcSkinDepth`, `calcTelluricSecondary`, `calcFaultProximity`, `calcWater`, `calcDecomposition`, `computeExpertComposite`, `igrfFallback`, `interpIDW`, `dist`, `haversine`, `getGeoType`, `tileKey`, `getSegmentsNear`, `getBTSegmentsNear`, `normCommuneName`, `isCommuneRadonL3`.

Soit **27 fonctions sur 39** strictement pures sous réserve que les datasets globaux qu'elles consomment soient injectés au lieu d'être lus depuis le scope global.

### 4.2 Fonctions `calc*` impures

| Fonction | Couplage | Recommandation |
|----------|----------|----------------|
| `calcMagneticELF_v2` | lit `chargeFacteur` global, `console.warn`, `window._btDisabledWarned` | Passer `chargeFactor` en paramètre obligatoire ; déplacer le warning dans le code appelant ; passer les datasets `SEGMENT_GRID`, `HTA_SEGMENTS_DATA`, `BT_SEGMENT_GRID`, `BT_SEGMENTS_DATA`, `POSTES_SOURCES`, `EOLIENNES_DATA`, `PROD_ELECTRIQUE` via un objet d'état injecté |
| `calcMagneticELF_v1` | id. (chargeFacteur global) | id. |
| `calcMagneticWMM` | lit `WMM_INDEX`, `WMM_GRID`, `WMM_STEP` globaux | Passer la grille en paramètre ou par closure de fabrique |
| `calcAll_v2` | lit `curKp` global pour `kp_snapshot.value`, lit `USE_ELF_V2` | Injecter `kp` et `useElfV2` via `options` |
| `calcAll` | id. via `calcAll_v2` + lit `v2.context.heritage._score_legacy` (champ disparu en v8) | Idem ; le bloc `heritage` ayant migré vers `patrimoine.html`, le fallback `?? 0` est défensif et restera correct |

### 4.3 Helpers impurs

| Helper | Couplage | Recommandation |
|--------|----------|----------------|
| `buildSegmentGrid` | mute `SEGMENT_GRID`, `HTA_SEGMENTS_DATA`, `console.log` | Pure fonction qui retourne `{grid, segments}` au lieu de muter un global |
| `buildBTSegmentGrid` | id. pour BT | id. |
| `loadBTLinesAsync` | `fetch` Supabase, `console.log/warn`, mute globals | Reste hors moteur ; le moteur consomme les segments déjà construits |
| `fetchEMAG2`, `preloadEMAG2`, `loadWMMGrid`, `loadTDFEmitters`, `loadPostesSources`, `loadEoliennesData`, `loadPointsChaudsRadio`, `loadRadonCommunesL3`, `loadProd`, `loadReseau`, `loadAQU`, `loadNOAA` | `fetch` réseau, mutent globals | Restent hors moteur — couche I/O à la charge du hôte |

## 5. Stratégie de découpage proposée

Découpage adossé aux regroupements observés dans `app.html` (sections de commentaires « DOMAINE M », « DOMAINE I », etc.) et au graphe d'appels du §3.

```
lib/tellux-engine/
  index.js                 // export public : calcAll_v2, calcAll, computeExpertComposite
  domains/
    magnetic-static.js     // calcMagneticStatic, calcLCS1, calcSq, calcExternalCorr,
                           //   calcMagneticWMM, igrfFallback
    magnetic-elf.js        // calcMagneticELF_v1, calcMagneticELF_v2,
                           //   calcBiotSavartSegment, calcBiotSavartSegmentVec
    radiofrequency.js      // calcRF, calcN_RF_loo, calcRFcorrFactor,
                           //   calcN_RF_calib, calcDeltaRF, calcN_RF
    ionizing.js            // calcGammaAmbient, calcRadonPotential
    context.js             // calcSubstrateContext, calcGeoSusc, calcSkinDepth,
                           //   calcTelluricSecondary, calcFaultProximity, calcWater,
                           //   calcDecomposition, getGeoType
    expertise.js           // computeExpertComposite + EXPERT_WEIGHTS_DEFAULT,
                           //   EXPERT_BOUNDS_DEFAULT, EXPERT_EPISTEMIC_NOTE (GELE-001)
  utils/
    geo.js                 // dist, haversine, interpIDW, tileKey
    spatial-grid.js        // buildSegmentGrid, getSegmentsNear,
                           //   buildBTSegmentGrid, getBTSegmentsNear
    commune.js             // normCommuneName, isCommuneRadonL3
  data/
    igrf14-grid.json       // export de IGRF14_GRID
    lcs1-grid.json         // export de LCS1_GRID
    crustal-refs.json      // export de CRUSTAL_REFS
    geo-susc-grid.json     // export de GEO_SUSC_GRID
    failles-corse.json     // export de FAILLES_CORSE
    sigma-rock.json        // export de SIGMA_ROCK
    fh-points.json         // export de FH_POINTS
    cartoradio-stats.json  // export de CARTORADIO_STATS, DENSITY
    profil-horaire.json    // export de PROFIL_HORAIRE_CORSE
    elf-test-points.json   // export de ELF_TEST_POINTS (utilisé en tests)
  loaders/
    node-loaders.js        // chargement depuis disque pour Node.js / Edge
    browser-loaders.js     // chargement depuis fetch HTTP pour le navigateur
```

Le fichier `index.js` exporte les trois racines (`calcAll_v2`, `calcAll`, `computeExpertComposite`) et accepte en option un objet `state` qui regroupe : `chargeFactor`, `curKp`, `useElfV2`, `useBtSegments`, `htaSegments`, `htaSegmentGrid`, `btSegments`, `btSegmentGrid`, `postesSources`, `eoliennes`, `prodElectrique`, `pointsChaudsRadio`, `tdfEmitters`, `emag2Cache`, `wmmGrid`, `radonL3InseeSet`, `radonL3NameSet`. Le hôte (navigateur ou Worker) construit ce `state` via les loaders appropriés et le passe au moteur à chaque appel.

L'organisation par domaine respecte la partition du `calcAll_v2` actuel (M_static, M_elf, RF, I_gamma, contexte). Les helpers transverses (`dist`, `haversine`, `interpIDW`, `tileKey`) vivent dans `utils/`. Les datasets sont sortis du JS et stockés en JSON, ce qui rend le code beaucoup plus lisible et facilite la maintenance ultérieure.

## 6. Difficultés anticipées

### 6.1 Couplage `chargeFacteur` / `curKp`

Ces deux variables globales mutables sont alimentées par des fetches asynchrones (`loadChargeReseau`, `loadNOAA`) et lues par le moteur sans appel explicite. L'extraction doit les transformer en paramètres explicites de `calcAll_v2`, ce qui change la signature publique du moteur. Soleil devra arbitrer si la signature reste `(lat, lon, options)` avec ces champs dans `options`, ou si un objet `state` distinct est introduit.

### 6.2 Construction d'index spatiaux côté serveur

`SEGMENT_GRID` et `BT_SEGMENT_GRID` sont aujourd'hui construits côté navigateur après un fetch Supabase de plusieurs milliers de polylines. Côté Edge Function ou Worker, deux options : construire l'index à chaud à chaque cold start (coûteux), ou pré-calculer l'index et le stocker en R2/Storage (à mettre à jour quand le dataset HTA évolue). Le sprint d'extraction ne tranche pas cette question, il l'expose.

### 6.3 Hotfix `USE_BT_SEGMENTS = false` et `BT_ZONES` proxy

La constante `USE_BT_SEGMENTS` (ligne 3446) est à `false` depuis le hotfix `BT-CALIBRATION-001` du 2026-04-22. La fonction `calcMagneticELF_v2` retombe sur le proxy `BT_ZONES` hardcodé inline (ligne 3367). Cet inline doit être extrait en constante exportée pour pouvoir être mocké en test. Lors du déblocage de la dette `BT-CALIBRATION-001`, l'extraction facilitera la bascule en réglant un paramètre du `state`.

### 6.4 Composante terrestre gamma gelée (NCRP-001)

La composante terrestre de `calcGammaAmbient` est un placeholder explicite (`terrestrial_nSv_h = null`, ligne 4161). La formule `13·U + 5.4·Th + 42·K` est commentée mais non implémentée, en attente de validation par le physicien tiers (cf. `DETTES_TECHNIQUES.md` `NCRP-001`). L'extraction doit conserver ce placeholder et exposer une signature qui permettra de brancher la formule sans casser les appelants.

### 6.5 Constantes Expert gelées (GELE-001)

`EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, `EXPERT_EPISTEMIC_NOTE` (lignes 3864-3866) sont identifiés comme gelés sous `GELE-001` (cf. commentaires inline). L'extraction doit reproduire le commentaire de gel dans `expertise.js` et idéalement encapsuler ces constantes dans un namespace clairement marqué (par exemple `EXPERT_DEFAULTS_FROZEN`) pour décourager toute modification non concertée.

### 6.6 Fonction `calcHuman` DEPRECATED

`calcHuman` (ligne 3678) est explicitement marquée DEPRECATED v2 phase 1 du 2026-04-19, conservée pour compatibilité avec `calcAll` legacy. Décision à prendre lors de l'extraction : garder dans `domains/legacy.js` avec un avertissement de dépréciation, ou supprimer si `calcAll` peut être ré-implémenté sans elle.

### 6.7 Doublonnage `RADON_CLASS_BY_LITHOLOGY`

Ce mapping est défini en deux endroits (lignes 3939 et 4102), une fois dans `calcSubstrateContext` et une fois dans `calcRadonPotential`. L'extraction doit le centraliser dans `data/radon-classification.js` ou similaire et l'importer dans les deux fonctions, pour éviter une dérive future entre les deux copies.

### 6.8 Helpers définis inline dans les fonctions

Plusieurs constantes sont définies inline dans le corps des fonctions (`MU0_OVER_2PI`, `METERS_PER_DEG_LAT`, `METERS_PER_DEG_LON`, `RIVER_PTS` dans `calcSubstrateContext`). Elles devront être hissées au niveau du module pour être testables et pour éviter leur recréation à chaque appel.

### 6.9 Logs `console.warn` / `console.log`

Plusieurs fonctions du moteur émettent des logs (`buildSegmentGrid` 2945, `loadBTLinesAsync`, `calcMagneticELF_v2` 3318-3321, `runELFRegressionTest` 3479, 3500). Décision : conserver tels quels (acceptables côté serveur), ou les remplacer par un logger injecté permettant de les rediriger ou de les couper en production.

### 6.10 Pas de stochastique ni de dépendance temporelle dans les `calc*`

Vérifié par lecture : aucun `Math.random` ni `Date.now()` dans les fonctions de calcul. La seule lecture temporelle est `new Date().toISOString()` dans `calcAll_v2` ligne 3814 pour le champ `timestamp` de retour. Le test de non-régression devra ignorer ce champ (sinon il échoue toujours).

## 7. Plan de test de non-régression

### 7.1 Capture des valeurs de référence (avant extraction)

Réutiliser les 20 points existants de `ELF_TEST_POINTS` (ligne 3454) qui couvrent 5 catégories : urbains, ruraux, éloignés, mégalithiques, et un dernier groupe non documenté à confirmer en lecture. Compléter par 5 points supplémentaires choisis pour couvrir des contextes non exploités par les tests existants : un point en mer (offshore), un sommet (Monte Cinto), un site thermal (Pietrapola), une commune radon classée niveau 3 du décret 2018-434 (par exemple Murato), et un point dans une zone à anomalie crustale forte (sud Sartenais). Total : 25 points.

Pour chacun de ces 25 points, exécuter dans la console du navigateur sur l'application actuelle :

```javascript
JSON.stringify(calcAll_v2(lat, lon, { altitude_m: alt, commune_info: ci }), null, 2)
```

et capturer le résultat. Sauvegarder le tout dans `tests/fixtures/known-values-pre-extraction.json` (hors moteur, en racine `tests/`).

### 7.2 Fixture format suggéré

```json
{
  "schema_version": "1.0",
  "captured_at": "2026-04-26T...",
  "captured_from": "app.html révision <git-sha>",
  "points": [
    {
      "id": "urbain-bastia-centre",
      "lat": 42.7028,
      "lon": 9.4503,
      "options": { "altitude_m": 5, "commune_info": null },
      "expected": { ... objet retourné par calcAll_v2 ... }
    },
    ...
  ]
}
```

### 7.3 Suite de tests post-extraction

Le sprint d'extraction écrit une suite de tests qui charge cette fixture, exécute le moteur extrait sur chaque point avec les mêmes options, et compare champ par champ avec un epsilon de `1e-9` pour les valeurs flottantes. Les champs `timestamp` et `kp_snapshot.timestamp` sont ignorés.

Le runner de test n'est pas tranché par cette note : node:test (zéro dépendance), vitest (rapide), ou jest (familier) sont des options à arbitrer en début de phase 0.

### 7.4 Tests complémentaires

En plus du test de non-régression sur les 25 points :

- Tests unitaires sur les helpers feuilles : `dist` et `haversine` doivent retourner exactement la même valeur sur 10 paires de points connus, `interpIDW` doit retomber sur la valeur exacte si la position cliquée est un nœud de la grille, `calcBiotSavartSegment` doit retourner zéro pour un segment dégénéré et un fil infini approximé pour un segment très long centré.
- Tests de bornes sur `computeExpertComposite` : entrées au-delà des bornes doivent être clippées à 1 ; entrées en deçà doivent être clippées à 0 ; valeur médiane doit retourner exactement le poids du domaine concerné.
- Test que le placeholder `terrestrial_nSv_h: null` reste en place (gel NCRP-001).
- Test que `EXPERT_WEIGHTS_DEFAULT` exporte exactement `{ M: 0.4, RF: 0.4, I: 0.2 }` (gel GELE-001).

### 7.5 Capture continue post-extraction

Une fois la suite passée verte, le repo Tellux devrait conserver le test de non-régression en CI. Toute évolution future du moteur qui ferait dériver une valeur de référence sera remontée comme une régression à expliciter (soit la dérive est volontaire et la fixture est mise à jour avec changelog, soit la dérive est un bug).

## Fin du document

Document produit en lecture seule. Aucune modification de `app.html` ni d'autre fichier du moteur. Toutes les références de ligne ont été vérifiées par grep direct sur la révision actuelle. Les zones gelées (`GELE-001` ligne 3864, `NCRP-001` ligne 4143) sont mentionnées avec leur identifiant exact tel que présent dans le code.
