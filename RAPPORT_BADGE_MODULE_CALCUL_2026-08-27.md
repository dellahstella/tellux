# Audit badge "Module le calcul" — cohérence RF/Composite (2026-08-27)

Brief "Panneau '?' sélectif + cohérence badge 'Module le calcul'", partie B. **Recherche/audit
uniquement — rien n'a été implémenté**, conformément au gate ("pas de gate à ce stade, juste un
rapport"). Toutes les affirmations ci-dessous sont sourcées par citation exacte (fichier +
ligne), pas de supposition.

## Périmètre audité

Toutes les couches portant une classe `.layer-badge--calc` (couleur "calc-relevant") dans
`app.html`, tous domaines confondus (RF et Composite) :

| Bouton | Badge affiché | Domaine |
|---|---|---|
| `b-emag` (Fond magnétique régional) | "Module le calcul" | Composite (statique) |
| `b-foretdense` (Forêt dense) | "Module le calcul" | RF |
| `b-con` (Mesures EM) | "Calibration RF" (déjà distinct depuis #1060) | RF |

Grep exhaustif sur `layer-badge--calc` dans `app.html` : 3 occurrences boutons, aucune autre —
ce tableau est complet, pas un échantillon.

## Classification par couche

### 1. Fond magnétique régional (`b-emag`) — **entrée directe du calcul**, avec réserve importante

**Calc :** `calcMagneticStatic()` ([app.html:4538](app.html:4538)) calcule
`B_total_nT = B_principal_nT + B_anomaly_nT + Sq_correction_nT + external_correction_nT`
([app.html:4546](app.html:4546)), où `B_anomaly_nT = calcLCS1(lat_, lon_)`
([app.html:4543](app.html:4543)). Cet appel est **inconditionnel** — aucune garde sur
`ACTIVE.emag` ni sur l'état du bouton `b-emag` dans `calcMagneticStatic()`. Le terme
crustal est donc bien une entrée directe, sommée à chaque analyse de point.

**⚠️ Réserve majeure — le bouton `b-emag` ne pilote PAS cette entrée :**

- `calcLCS1(lat,lon)` ([app.html:3919](app.html:3919)) préfère `EMAG2_CACHE[key]` si
  disponible, sinon retombe sur la grille statique 24 points `LCS1_GRID`
  ([app.html:3837-3854](app.html:3837)) via interpolation IDW.
- `EMAG2_CACHE` n'est peuplée en bloc que par `preloadEMAG2()`
  ([app.html:3898](app.html:3898)) — **fonction jamais appelée nulle part dans le fichier**
  (grep exhaustif sur `preloadEMAG2` : une seule occurrence, sa propre déclaration). Code mort.
- Le seul autre point de peuplement de `EMAG2_CACHE` est `fetchEMAG2()`
  ([app.html:3879](app.html:3879)), appelée à un seul endroit :
  `updateCrustalGauge()` ([app.html:4087](app.html:4087)) — la jauge comparative du bouton
  **`b-crustal`** ("Anomalies de référence"), pas `b-emag`. Elle ne s'exécute que si
  `b-crustal` est actif (`map.on('moveend', updateCrustalGauge)` armé par
  `showCrustalGauge(true)`), et seulement pour le centre courant de la carte.
- **Conséquence** : dans l'immense majorité des usages réels, le terme crustal du calcul
  utilise la grille statique `LCS1_GRID`, **pas** les données EMAG2v3 en direct que le bouton
  `b-emag` affiche visuellement (couche WMS `wmsEmag`, cf. commentaire
  [app.html:3864-3866](app.html:3864)). Activer ou désactiver `b-emag` **ne change rien** au
  calcul — ni la présence du terme (toujours là), ni sa source de données (déterminée par un
  bouton différent, `b-crustal`, de façon incidente et localisée).

**Verdict précis** : entrée directe du calcul (toujours active), mais le toggle du bouton n'a
aucun effet sur elle — ni pour l'activer/désactiver, ni pour changer sa source de données.

### 2. Forêt dense (`b-foretdense`) — **entrée directe du calcul**, même réserve

**Calc :** `RF_field(lat, lon, applyVegetation)` ([app.html:5437](app.html:5437)) applique
l'atténuation végétation si `applyVegetation && FORET_DENSE_PARTS`
([app.html:5454](app.html:5454)), via `calcVegetationAttenuation()`
([app.html:5624](app.html:5624)). `FORET_DENSE_PARTS` est chargée au boot par
`loadForetDenseGrid()`, appelée inconditionnellement dans le `Promise.all` de démarrage —
indépendante de `ACTIVE.foretdense`.

Le paramètre `applyVegetation` est threadé `RF_field()` → `calcRF()`
([app.html:5752](app.html:5752)) → `calcAll()`. **Le seul point d'appel légitime qui le passe à
`true`** est [app.html:6578](app.html:6578) : `calcAll(lat,lng,{...,applyVegetation:true})`,
documenté comme "seul point d'entrée légitime pour ce coût (clic carte réel...)"
([app.html:6576](app.html:6576)) — cf. aussi le commentaire HOTFIX
[app.html:5742-5751](app.html:5742) (bug corrigé le 2026-08-26 : `applyVegetation` avait été
codé en dur à `true` partout, y compris pour des appels heatmap/survol, avant d'être restreint
au seul clic carte réel pour des raisons de performance — **pas** pour un contrôle utilisateur).

**⚠️ Même réserve que `b-emag`** : le déclenchement de l'atténuation végétation dépend
uniquement du **type d'appel** (clic carte réel vs heatmap/autre), jamais de
`ACTIVE.foretdense`/l'état du bouton `b-foretdense`. Sur un clic carte réel, l'atténuation
s'applique que le bouton soit activé ou non.

**Verdict précis** : entrée directe du calcul (active sur tout clic carte réel), toggle du
bouton sans effet sur le calcul — identique au cas `b-emag`.

### 3. Mesures EM / "Calibration RF" (`b-con`) — **calibration hors-ligne**, déjà correctement badgée

**Calc :** `calibrateRF()` ([app.html:5659](app.html:5659)) fetch
`public/data/cartoradio_certified_corse.json` — **même fichier** que celui chargé par
`loadMesuresCertifiees()`/`MESURES_CERTIFIEES` (affichage du bouton `b-con`,
[app.html:8899](app.html:8899), vérifié chemin identique) — et calcule `RF_CALIB_K`, une
constante appliquée ensuite dans `RF_field()`/`calcRF()`. `calibrateRF()` est appelée une seule
fois au boot, dans le même `Promise.all` que `loadForetDenseGrid()` — également indépendante de
`ACTIVE.con`.

**Différence structurelle réelle avec les 2 cas précédents** : ici il n'y a **pas de terme
recalculé à chaque point** — `RF_CALIB_K` est une constante figée une fois pour toutes au
démarrage, qui multiplie ensuite le champ RF prédit partout. Ce badge ("Calibration RF",
distinct de "Module le calcul" depuis #1060) est déjà correctement différencié.

**Verdict précis** : calibration hors-ligne, confirmé, badge déjà cohérent — rien à corriger
ici (déjà traité par #1060).

## Constat transversal (au-delà du cadre à 2 catégories du brief)

L'audit fait apparaître un troisième axe que la distinction "calibration hors-ligne / entrée
directe" ne capture pas : **pour les 2 couches "entrée directe" (`emag`, `foretdense`), le
bouton lui-même ne gate rien** — contrairement à ce que "Module le calcul" pourrait laisser
penser à un utilisateur (« si j'active ce bouton, le calcul se met à en tenir compte »). En
réalité :

- Le calcul intègre ces facteurs **de façon permanente**, sur tout point analysé au clic —
  que le bouton soit activé ou non.
- Le bouton contrôle uniquement l'**affichage visuel** de la géométrie/couche correspondante
  sur la carte (où se trouve la forêt dense, où se situe le fond magnétique).
- Pour `emag` spécifiquement, il y a une couche d'inexactitude supplémentaire : la donnée
  *affichée* par le bouton (EMAG2v3 en direct) n'est, dans la quasi-totalité des cas réels,
  **pas** la donnée *utilisée* par le calcul (grille statique `LCS1_GRID`) — deux choses
  visuellement associées au même bouton mais qui divergent silencieusement.

## Proposition de différenciation (non implémentée — décision Soleil)

Le cadre à 2 badges du brief capture bien la distinction calibration/entrée-directe, mais
l'audit suggère qu'un badge unique "Module le calcul" pour `emag`/`foretdense` resterait encore
trompeur sur un point différent (le lien toggle↔calcul). Deux pistes, à arbitrer :

1. **Minimal (fidèle au brief)** : 2 badges distincts — "Calibration RF" (déjà fait pour `con`)
   vs un nouveau libellé pour `emag`/`foretdense` explicitant "entrée permanente du calcul"
   plutôt que "Module le calcul" (qui suggère à tort un contrôle par le toggle).
2. **Plus complet** : ajouter une précision au `title=` de `b-emag`/`b-foretdense` du type
   "toujours pris en compte au clic carte, indépendamment de l'affichage de cette couche" — et,
   pour `b-emag` spécifiquement, corriger ou clarifier le fait que la donnée visuelle affichée
   (EMAG2v3 direct) diverge en pratique de la donnée réellement utilisée par le calcul (grille
   statique).

Aucune de ces pistes n'est implémentée. Décision et libellé exact reviennent à Soleil.

## Fichiers/lignes cités (pour vérification indépendante)

- `calcMagneticStatic()` : [app.html:4538](app.html:4538)
- `calcLCS1()` : [app.html:3919](app.html:3919)
- `LCS1_GRID` : [app.html:3837](app.html:3837)
- `preloadEMAG2()` (jamais appelée) : [app.html:3898](app.html:3898)
- `fetchEMAG2()` : [app.html:3879](app.html:3879)
- `updateCrustalGauge()` (seul appelant de `fetchEMAG2()`) : [app.html:4083](app.html:4083)
- `RF_field()` / garde `applyVegetation` : [app.html:5437](app.html:5437),
  [app.html:5454](app.html:5454)
- `calcVegetationAttenuation()` : [app.html:5624](app.html:5624)
- `loadForetDenseGrid()` : [app.html:5652](app.html:5652)
- HOTFIX `applyVegetation` (2026-08-26) : [app.html:5742](app.html:5742)
- Seul appel `applyVegetation:true` légitime : [app.html:6578](app.html:6578)
- `calibrateRF()` : [app.html:5659](app.html:5659)
- `loadMesuresCertifiees()` : [app.html:8899](app.html:8899)
