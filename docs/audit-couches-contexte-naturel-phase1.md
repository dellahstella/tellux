# Audit Phase 1 — Groupe 3 « Contexte naturel » du menu hamburger

**Branche** : `audit/groupe3-contexte-naturel`
**Date** : 2026-04-27
**Périmètre** : 11 couches listées dans le brief Soleil, plus 1 couche découverte hors brief (`b-radon`).
**Mode** : read-only intégral. Aucune modification de production.

---

## 0. Verdict synthétique (à lire en premier)

- **12 couches dans le menu Groupe 3** (lignes 1481-1492 de `app.html`), pas 11. Le brief omet `b-radon` (ligne 1484). À arbitrer en chat : est-ce un oubli ou un choix de scope (Radon a déjà son audit propre) ?
- **Classification proposée par Soleil partiellement corrigée par l'audit** :
  - `b-failles` doit basculer **B → A** (impact direct via `calcFaultProximity` + `calcSubstrateContext`)
  - `b-radon` (12e couche) appartient au **groupe A** (`calcRadonPotential` + `calcSubstrateContext`)
  - `b-hyd` reste en B mais avec une **nuance forte** : la couche WMS BRGM est purement visuelle, le calc `calcWater` utilise un dataset parallèle hardcodé (`RIVER_PTS`)
- **Aucune couche à RETIRER avec arbitrage historique formel.** Toutes les couches sont active depuis au moins une PR documentée.
- **3 couches `AMBIGU`** appellent un arbitrage Soleil :
  - `b-cav`, `b-therm`, `b-hyd` : indicateurs documentés (légende enrichie en PR #179) sans modulation calc, statut « contexte structurel pur »
  - `b-wdmam` : redondance fonctionnelle confirmée avec `b-emag` (même source NOAA EMAG2v3, bbox seule différence) — note recherche `EMAG2_WDMAM_NOTE_RECHERCHE.md` (2026-04-24) recommande explicitement d'arbitrer
  - `b-crustal` : module pédagogique opt-in INTL-CRUSTAL-001 — décision de conservation/retrait à arbitrer
- **Explication globale sur les couches d'impact indirect : NON UNIFIÉE.** Disséminée à 4 endroits :
  - `title` du bouton `b-foret` (ligne 1482) — seule couche concernée
  - Sous-titres `LEGEND_HTML` ajoutés en PR #179 (commit `5113b60`, 2026-04-26) pour `foret`, `cav`, `therm`
  - Panneau `#methodology-panel` ligne 1328 — seulement pour la proximité faille
  - Commentaires `// EPISTEMIC NOTE (v2)` dans le code (ligne 4326 et autres) — invisibles utilisateur
  - Pas dans `transparence.html`, `corpus.html`, `index.html`, ni dans aucun fichier `.md` public
- **Dette technique ouverte** : `WDMAM-NAMING-001` — le bouton « EMAG2 mondial » conserve l'ID `b-wdmam`, var `wmsWDMAM`, fonction `togWDMAM`, classe `on-wdmam` (PR #125 a renommé visuellement, PR #127 a documenté la dette de renommage technique).
- **Code mort résiduel signalé (non purgé)** : `lCem` est déclaré ligne 2055, présent dans `LAYERS` ligne 2061 et dans `ACTIVE` ligne 2063, mais **aucun bouton ne le toggle** et **aucun loader ne le remplit**. Variable orpheline.

---

## 1. Mapping technique des 12 couches du Groupe 3

### Légende du tableau

- **MOD-CALC** = la couche module-t-elle un calc EM ?
  - **OUI-direct** = la couche/dataset est lue par `calc*`
  - **OUI-parallèle** = un dataset distinct mais sémantiquement lié est lu par `calc*` (la couche elle-même n'est pas le canal)
  - **NON** = couche purement visuelle/contextuelle
- Numéros de ligne référencent `app.html` au commit `4add85c` (HEAD `main` au 2026-04-27).

### Tableau exhaustif

| # | Bouton | Ligne | Layer Leaflet | LAYERS/WMS | ACTIVE init | Source data | Loader | Render | MOD-CALC | Calc consumer |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **b-geo** Géologie BRGM | 1481 | (pas de layerGroup) | `WMS.geo = wmsGeo` | `false` | `wmsGeo` ligne 2034 — BRGM `https://geoservices.brgm.fr/geologie · GEOLOGIE` | aucun (WMS Leaflet) | natif Leaflet | **OUI-parallèle** | `calcGeoSusc` (3934) + `calcSubstrateContext` (3944) — via `GEO_SUSC_GRID` (dataset hardcodé inline ≠ WMS) |
| 2 | **b-foret** Forêts publiques | 1482 | (pas de layerGroup) | `WMS.foret = wmsForet` | `false` | `wmsForet` ligne 2041 — IGN `https://data.geopf.fr/wms-v/ows · FORETS.PUBLIQUES` | aucun (WMS Leaflet) | natif Leaflet | **NON** | aucun — confirmé par RECHERCHE_Zones7-8-9 (2026-04-19) verdict B |
| 3 | **b-failles** Failles tectoniques | 1483 | `lFailles` (ligne 2050) | **HORS LAYERS** | n/a | `failles-corse.json` + fallback `FAILLES_CORSE` inline (4287-4303, 8 entrées) | `loadFailles` (6362) | `renderFailles` (6368) | **OUI-direct** | `calcFaultProximity` (4350) + `calcSubstrateContext` (3944, lignes 3958-3963) consomment `FAILLES_CORSE` |
| 4 | **b-radon** *(hors brief)* | 1484 | `lRadon` (ligne 2057) | `LAYERS.radon` | `false` | `buildRadonLayer` (4036) + `loadRadonCommunesL3` (4072) — polygones GeoJSON ASNR/IRSN 253 communes | `loadRadonCommunesL3` | `buildRadonLayer` | **OUI-direct** | `calcRadonPotential` (4108) + `calcSubstrateContext.radon_potential_class` (3950-3956) via `RADON_CLASS_BY_LITHOLOGY` |
| 5 | **b-points-chauds** Sites U/Th | 1485 | `lPointsChaudsRadio` (ligne 2052) | **HORS LAYERS** | n/a | `public/data/points_chauds_radio.json` + `POINTS_CHAUDS_RADIO` (handler `togPointsChauds`) | `loadPointsChaudsRadio` (3596) | `_renderPointsChauds` (6451) | **NON** | aucun — catalogue affichage. Tooltip explicite : « doses non mesurées, sources documentaires BRGM » |
| 6 | **b-sites-remarq** Sites géophysiques remarquables | 1486 | `lSitesRemarq` (ligne 2055) | `LAYERS.sitesRemarq` | `false` | `public/data/sites_remarquables_corse.json` + `SITES_REMARQUABLES` | `loadSitesRemarquables` (6484) | `_renderSitesRemarquables` (6535) | **NON** | aucun — catalogue 10 sites (ophiolite, minier, surveillance_radio). Tooltip : « données documentaires, mesures in situ requises » |
| 7 | **b-hyd** Hydrographie | 1487 | (pas de layerGroup) | `WMS.hyd = wmsHyd` | `false` | `wmsHyd` ligne 2035 — BRGM `REMNAPPE_FR` | aucun (WMS Leaflet) | natif Leaflet | **OUI-parallèle (faible)** | `calcWater` (3759) consomme `RIVER_PTS` (8 points hardcodés inline ligne 3764) **DIFFÉRENT** du WMS BRGM. La couche WMS = visuel pur ; le calc utilise des points distincts. |
| 8 | **b-cav** Cavités | 1488 | (pas de layerGroup) | `WMS.cav = wmsCav` | `false` | `wmsCav` ligne 2036 — BRGM `risques · CAVITE_LOCALISEE` | aucun (WMS Leaflet) | natif Leaflet | **NON** | aucun — légende enrichie PR #179 « Anomalies magnétiques locales (discontinuité de susceptibilité) » mais cet effet n'est pas modélisé dans le code |
| 9 | **b-therm** Émergences thermales | 1489 | `lTherm` (ligne 2049) | `LAYERS.therm` | `false` | `THERMAL_SOURCES_CORSE` inline (4309-4316, 6 sites) | aucun (inline) | `buildThermLayer` (5436) | **NON** | aucun — légende PR #179 « Marqueurs de failles actives, courants telluriques » mais ces effets ne sont pas modélisés. Note ligne 5452 : « lien EM : failles actives → géothermie → émergence de surface » (intention, pas calc) |
| 10 | **b-emag** Crustale (EMAG2) | 1490 | (pas de layerGroup) | `WMS.emag = wmsEmag` | `false` | `wmsEmag` ligne 2043 — `L.imageOverlay` NOAA EMAG2v3 ImageServer **bbox Corse fixe** `[[41.3,8.5],[43.1,9.65]]` | aucun (imageOverlay) | natif Leaflet | **OUI-parallèle** | `calcMagneticStatic` (2866) → `calcLCS1` (2593) → `EMAG2_CACHE` (cache de fetchs ponctuels). Cache populé par `loadWMMGrid` (2739). Le visuel imageOverlay et le cache sont **deux mécanismes distincts** alimentés par la même source NOAA. |
| 11 | **b-wdmam** EMAG2 mondial *(ID `wdmam` historique, dette WDMAM-NAMING-001)* | 1491 | `wmsWDMAM` (var dynamique 6740) | **HORS LAYERS / WMS** | n/a | `togWDMAM` (6741) construit dynamiquement `L.imageOverlay` NOAA EMAG2v3 ImageServer **bbox viewport courant** | aucun | inline dans `togWDMAM` | **NON** | aucun — affichage seulement. **Source NOAA EMAG2v3 identique à `b-emag`**, seule la bbox diffère (Corse fixe vs viewport dynamique). |
| 12 | **b-crustal** Crustale mondiale | 1492 | `lCrustal` (ligne 2056) | `LAYERS.crustal` | `false` | `CRUSTAL_REFS` inline (2605-2621, 5 sites mondiaux : Bangui, Kursk, Vredefort, Ries, Chicxulub) | aucun (inline) | `buildCrustalLayer` (2624) | **NON** | aucun — module opt-in INTL-CRUSTAL-001. Panneau comparatif `showCrustalGauge` (gauge top-right) montre la valeur EMAG2v3 locale + 5 barres log(|nT|) des références. |

### Notes complémentaires sur le mapping

**Découplage WMS visuel vs dataset calc** — c'est le pattern dominant du Groupe 3 :
- `b-geo` (WMS BRGM) ≠ `GEO_SUSC_GRID` (grille hardcodée inline consommée par `calcGeoSusc`)
- `b-hyd` (WMS BRGM REMNAPPE_FR) ≠ `RIVER_PTS` (8 points hardcodés inline consommés par `calcWater`)
- `b-emag` (imageOverlay NOAA bbox Corse) ≠ `EMAG2_CACHE` (fetchs ponctuels NOAA via `fetchEMAG2`)

Conséquence : **cocher la couche n'active pas le calc** ; le calc est toujours actif si la fonction est appelée. La couche n'est qu'un overlay informatif. Le tooltip de `b-foret` (« couche visuelle niveau A — pas de modulation calcul ») dit cette vérité explicitement, mais elle n'est explicite que pour Forêts.

**Toggle générique vs handlers dédiés** :
- 7 couches passent par `tog(id, cls, btn)` (ligne 2408) : `geo`, `foret`, `radon`, `hyd`, `cav`, `therm`, `emag`, `crustal` — guard `if(!LAYERS[id]&&!WMS[id])return;` ligne 2411
- 4 couches ont un handler dédié : `togFailles` (6386), `togPointsChauds` (6468), `togSitesRemarquables` (6551), `togWDMAM` (6741) — parce qu'elles ne sont pas dans `LAYERS`/`WMS`

**Code mort résiduel** :
- `lCem` (ligne 2055) — `LAYERS.cem` (2061) et `ACTIVE.cem` (2063) — aucun bouton ne le toggle, aucun loader ne le remplit. Vestige de la couche « Cimenterie » purgée dans une session antérieure (à confirmer dans git log si Soleil le souhaite).

---

## 2. Statut épistémique de chaque couche

### Annotations dans le code par couche

| # | Bouton | Title HTML (ligne) | Légende (LEGEND_HTML) | EPISTEMIC NOTE (commentaire) | Visibilité utilisateur |
|---|---|---|---|---|---|
| 1 | b-geo | « Carte géologique BRGM — granite, schiste, calcaire » (1481) | `geo` (2072) — pas de subtitle, juste légende lithologique | aucun direct sur `wmsGeo`, mais `calcSubstrateContext` (3939-3943) commente sa zone GELÉE | titre + légende |
| 2 | b-foret | **« couche visuelle niveau A (pas de modulation calcul). BD Forêt V2 complète non disponible en WMS public. »** (1482) | `foret` (2075) — subtitle « Atténuation RF en zones boisées (modèle ITU-R P.833) » (PR #179) | commentaires lignes 2037-2040 « couche visuelle niveau A » | titre + légende complète |
| 3 | b-failles | « Failles tectoniques BRGM — 8 failles principales (actives + quaternaires) » (1483) | `failles` (2073) — pas de subtitle | **EPISTEMIC NOTE (v2) lignes 4326-4332** : « Indicateur de CONTEXTE STRUCTURAL — la proximité d'une faille tectonique est un facteur géologique documenté (potentiel sismique, perméabilité, radon), pas un amplificateur de signal EM mesurable. » | titre + EPISTEMIC NOTE invisible UI |
| 4 | b-radon | « Potentiel radon géologique — zones ASNR cat. 2/3 » (1484) | `radon` (2107) — subtitle « Exhalation du sous-sol, géologie granitique » | commentaires lignes 4001-4006 sur source ASNR/IRSN | titre + légende |
| 5 | b-points-chauds | « Sites U/Th à mesurer — catalogue de sites candidats à des mesures radiométriques (**doses non mesurées, sources documentaires BRGM ou analogies géologiques**) » (1485) | (pas dans LEGEND_HTML — tooltip de marker à la place via `_formatPcTooltip` 6434) | tooltip indique « Mesure in situ requise » et « Indice documenté (BRGM) » selon `pc.statut` | titre + tooltips marker |
| 6 | b-sites-remarq | « Sites géophysiques remarquables — 10 sites ponctuels à signature singulière. **Données documentaires, mesures in situ souvent requises.** » (1486) | `sitesRemarq` (2097) — subtitle « Géologie insolite et anciens sites miniers » + footer « 10 sites · données documentaires · mesures terrain requises » | tooltip de marker indique précision communale si présente | titre + légende + tooltip marker |
| 7 | b-hyd | « Nappes et cours d'eau souterrains (BRGM REMNAPPE) » (1487) | `hyd` (2074) — subtitle « Eau souterraine proche de la surface » (PR #125) | EPISTEMIC NOTE sur `calcWater` ligne 3752 « Cette valeur est un proxy grossier de la conductivité » (mais `calcWater` ≠ couche `b-hyd`) | titre + légende |
| 8 | b-cav | « Cavités souterraines — grottes, mines, karst (BRGM) » (1488) | `cav` (2076) — 2 subtitles : « Grottes, karst, mines souterraines » + « **Anomalies magnétiques locales (discontinuité de susceptibilité)** » (PR #179 ajout) | aucun | titre + légende enrichie |
| 9 | b-therm | « Émergences thermales — marqueurs de failles actives » (1489) | `therm` (2082) — subtitle « **Marqueurs de failles actives, courants telluriques** » (PR #179 extension) | commentaires lignes 5450-5452 « lien EM : failles actives → géothermie → émergence de surface » | titre + légende enrichie |
| 10 | b-emag | « Anomalie magnétique crustale NOAA EMAG2v3 — fond géologique régional » (1490) | `emag` (2079) — subtitle « Signature magnétique du socle profond » (PR #125) + 2 lignes de note « Fond régional profond (~50-100km) » + « Non lié à l'homme · EMAG2v3 NOAA » | commentaires `calcMagneticStatic` (2861-2864) « Leur combinaison éventuelle appartient à la zone GELÉE » | titre + légende complète |
| 11 | b-wdmam | « **Anomalie magnétique crustale mondiale — EMAG2v3, dynamique** » (1491) | `wdmam` (2078) — titre « EMAG2 mondial » + subtitle « Anomalies crustales mondiales dynamiques » (PR #125) | dette WDMAM-NAMING-001 documentée | titre + légende |
| 12 | b-crustal | « 5 anomalies magnétiques crustales mondiales de référence (cratères d'impact + BIF) — **opt-in, comparaison locale/mondiale** » (1492) | `crustal` (2080) — subtitle « Cinq références pédagogiques mondiales » + footer « Panneau comparatif en haut à droite quand couche active » | commentaires lignes 2601-2604 « Purement géologiques, aucun site humain » | titre + légende + panneau comparatif `showCrustalGauge` |

### Synthèse épistémique

**Les couches qui ont une note explicite « pas de modulation EM » dans le code** :
- `b-foret` : title (ligne 1482), commentaire (lignes 2037-2040)
- `b-failles` : EPISTEMIC NOTE complet (lignes 4326-4332) — mais la couche **module bel et bien** `calcFaultProximity` et `calcSubstrateContext`. La note clarifie qu'elle est **structurelle** (faille = facteur géologique), pas **EM amplificatrice**. Nuance importante.

**Les couches avec un statut implicite (légende suggérant un effet EM mais aucun calc) — ambigues** :
- `b-cav` : « Anomalies magnétiques locales (discontinuité de susceptibilité) » suggère un effet, mais aucun calc ne le modélise
- `b-therm` : « Marqueurs de failles actives, courants telluriques » suggère un effet, idem

**Les couches purement visuelles documentées** :
- `b-foret` (RECHERCHE_Zones7-8-9 verdict B confirmé)
- `b-points-chauds`, `b-sites-remarq` (catalogues documentaires explicites)
- `b-crustal` (module opt-in pédagogique)

**Les couches d'impact direct calculs** :
- `b-failles`, `b-radon`, `b-emag` (via cache parallèle), `b-geo` (via grille parallèle)

---

## 3. Localisation de l'explication globale (Bloc B du brief)

Soleil cherche une explication ajoutée à un moment donné sur les couches d'impact indirect. **Réponse : il n'existe pas une seule explication globale. Elle est disséminée à 5 endroits.**

### 3.1 Sur le bouton b-foret (title HTML)

**Ligne 1482** :
> *« Forêts publiques ONF via WMS IGN Géoplateforme — couche visuelle niveau A (pas de modulation calcul). BD Forêt V2 complète non disponible en WMS public. »*

C'est la **seule couche** qui porte cette annotation explicite dans son title.

### 3.2 Dans les sous-titres de légende `LEGEND_HTML` — PR #179 du 2026-04-26

Commit `5113b60` (refactor app: « add EM-context notes on 3 layers »). Lignes ajoutées :
- `LEGEND_HTML.foret` (ligne 2075) : *« Atténuation RF en zones boisées (modèle ITU-R P.833) »*
- `LEGEND_HTML.cav` (ligne 2076) : *« Anomalies magnétiques locales (discontinuité de susceptibilité) »* (2e subtitle ajouté)
- `LEGEND_HTML.therm` (ligne 2082) : *« Marqueurs de failles actives, courants telluriques »* (extension du subtitle existant)

Ces annotations apparaissent **uniquement quand la couche est activée** (panneau légende affiché par `showLegend()` / `updateLegendPanel()`).

### 3.3 Dans le panneau Méthodologie (`#methodology-panel`)

**Ligne 1328** d'`app.html` (panneau « 🔬 Méthodologie & Audit » accessible via `toggleMethodology()`) :
> *« **Contexte substrat géologique — proximité faille :** *[indicateur de contexte structural, pas d'indicateur EM]* »*

Cette mention couvre **uniquement** la proximité faille. Pas les autres couches structurelles.

### 3.4 Dans les commentaires `// EPISTEMIC NOTE (v2)` du code JS

**4 EPISTEMIC NOTE identifiées** :
- ligne 3752 : `calcWater` proxy de conductivité
- ligne 4240 : `calcSkinDepth` (hors Groupe 3)
- ligne 4264 : `calcGammaAmbient` (hors Groupe 3)
- **ligne 4326-4332** : `calcFaultProximity` — la note la plus complète sur le concept « contexte structural »

Texte clé (4326-4328) :
> *« Indicateur de CONTEXTE STRUCTURAL — la proximité d'une faille tectonique est un facteur géologique documenté (potentiel sismique, perméabilité, radon), **pas un amplificateur de signal EM mesurable**. »*

**Visibilité utilisateur : nulle** — c'est uniquement dans le source JS.

### 3.5 Dans `transparence.html`

Pas d'explication épistémique générique. Mention factuelle de chaque source bibliographique (EMAG2v3, WDMAM, IGN/ONF), mais pas de classification « impact direct vs indirect ».

### 3.6 Dans la documentation `.md`

- **`EMAG2_WDMAM_NOTE_RECHERCHE.md`** (2026-04-24) — note de recherche interne sur les 3 couches magnétiques. Recommandation explicite (§5) : si on simplifie, garder seul `b-emag` (EMAG2v3) ; supprimer `crustal` et `wdmam`. **À arbitrer.**
- **`_archive/recherche_axes/RECHERCHE_Zones7-8-9_CouchesNaturelles_2026-04-19.md`** — verdict B explicite pour Forêt (couche affichage) et Sources/Fontaines (idem).
- **`docs/data-sources/bd_foret_v2_corse_notes.md`** — notes sur la couche forêt (matchait sur grep niveau A).
- Aucune `.md` n'unifie l'explication dans une formulation centrale.

### 3.7 Conclusion

L'explication des couches d'impact indirect existe **partiellement et fragmentée** :
- Pleinement explicite uniquement pour `b-foret` (title + légende + commentaire code)
- Partielle pour `b-cav` et `b-therm` (légende suggérant un effet mais pas de calc, sans clarification du statut)
- Implicite pour `b-hyd` (légende + commentaire code sur calcWater)
- Cachée dans EPISTEMIC NOTE invisible UI pour `b-failles`

**Recommandation pour la phase 2** : centraliser une explication concise dans le header du Groupe 3 (avant les boutons) et/ou dans un sous-groupe « ℹ Comprendre les couches » accessible via un bouton info.

---

## 4. Historique d'arbitrage (Bloc C du brief)

### 4.1 Commits pertinents — chronologie inverse

Recherche effectuée via `git log --all --grep="EMAG\|crustal\|wdmam\|emag\|couche\|menu\|sources naturelles\|contexte naturel"`.

| Hash | Date | Message | Pertinence |
|---|---|---|---|
| `5113b60` | 2026-04-26 | refactor(app): remove visible version numbers and **add EM-context notes on 3 layers** (#179) | **CRITIQUE** — ajout PR #179 des subtitles « Atténuation RF... », « Anomalies magnétiques locales... », « courants telluriques » sur foret/cav/therm. C'est la PR à laquelle Soleil pense probablement quand il dit « j'ai ajouté l'explication mais je ne sais plus où ». |
| `1fde339` | 2026-04-24 | docs(debt): add **WDMAM-NAMING-001** (rename JS identifiers to match EMAG2 reality) (#127) | **DÉCISION ACTÉE — DETTE OUVERTE** : reconnaissance que `wdmam` est mal nommé techniquement, renommage différé. |
| `4882f00` | 2026-04-24 | fix(legends): add 9 subtitles + **rename wdmam → EMAG2 mondial** (honest citation NOAA Meyer 2017) (#125) | **DÉCISION ACTÉE** : libellé visible utilisateur corrigé. La couche n'est plus un faux-ami WDMAM côté UI. |
| `43f4f0d` | 2026-04-23 | feat(app): **world crustal anomalies comparison module (INTL-CRUSTAL-001)** (#103) | **DÉCISION ACTÉE** : ajout du module `b-crustal` avec 5 références mondiales hardcodées. Marqué comme **fermé** dans `DETTES_TECHNIQUES.md`. |
| `bf9e91a` | 2026-04-23 | docs: mark INTL-CRUSTAL-001 resolved (world crustal anomalies module implemented) | confirmation closure dette |
| `037e095` | 2026-04-23 | feat(app): add world crustal anomalies comparison module (INTL-CRUSTAL-001) | implémentation module crustal |
| `24fe274` | 2026-04-? (ancien) | feat(ui): regroupe les couches en 3 accordeons thematiques | structure menu hamburger 3 groupes (le contexte de cet audit) |
| `5dc194b`, `aee3bad`, `b693140`, `276741f`, `2557a4e`, `6057ef2` | 2026-04-25 → 2026-04-26 | série de PR a11y/refactor/cleanup (FAB onclick, ARIA, version numbers, social meta tags, semantic H1, purge patrimoine) | hors scope mais montre l'activité récente sur app.html |

### 4.2 Lecture des notes `.md` clés

**`EMAG2_WDMAM_NOTE_RECHERCHE.md`** (2026-04-24, 162 lignes, racine repo, gitignored) — note de recherche scientifique de référence sur les 3 couches magnétiques. Conclusion §5 (lignes 116-145) :

> *« Les trois couches du code actuel (`emag`, `crustal`, `wdmam`) représentent deux phénomènes distincts, pas trois : `emag` et `crustal` pointent tous deux vers des anomalies crustales — ils sont probablement redondants (même donnée source, ou deux produits issus du même dataset EMAG2). »*

**Note importante** : la note se trompe sur la couche redondante. **L'audit de cet audit** confirme que :
- `b-emag` et `b-wdmam` partagent **strictement la même source** NOAA EMAG2v3 ImageServer (lignes 2043-2044 et 6747-6749). La seule différence est la bbox (Corse fixe vs viewport dynamique).
- `b-crustal` est **distinct** : 5 sites ponctuels mondiaux hardcodés (Bangui, Kursk, Vredefort, Ries, Chicxulub).

La recommandation de la note s'applique donc à `emag` ↔ `wdmam`, pas à `emag` ↔ `crustal`. **Recommandation §5.1 corrigée par cet audit** : garder `b-emag` régional (bbox Corse), arbitrer `b-wdmam` (redondance fonctionnelle confirmée).

**`_archive/recherche_axes/RECHERCHE_Zones7-8-9_CouchesNaturelles_2026-04-19.md`** — verdicts explicites :
- Zone 7 (Forêt) : **affichage uniquement** ✓ (déjà appliqué via title + légende)
- Zone 8 (Sources et fontaines) : **proxy géologique déjà couvert par Zone 2** ; **pas de couche supplémentaire**. Note : ne traite pas explicitement les sources thermales ; il s'agit ici de sources d'eau et fontaines patrimoniales.
- Zone 9 (RF urbain) : **pas de couche supplémentaire** ; documenter le gap dans `calcAll`

**`NETTOYAGE_PROPOSE.md`** (2026-04-20) — concerne le rangement des fichiers, pas les couches du menu. Mention de `RECHERCHE_Zones7-8-9` à archiver (déjà fait : présent dans `_archive/recherche_axes/`).

**`RECAP_AUDIT_CONSOLIDATION_2026-04-27.md`** — audit du corpus scientifique (Kirschvink, Wang, Devlin, Koch). Hors scope couches.

### 4.3 Décisions actées vs en suspens

**Actées (mergées dans main)** :
- `b-foret` → couche d'affichage uniquement (verdict Zone 7, 2026-04-19) — appliqué via title `b-foret` + commentaires code 2037-2040
- `b-wdmam` → libellé UI corrigé en « EMAG2 mondial » (PR #125, 2026-04-24)
- `b-crustal` → module pédagogique opt-in implémenté (PR #103 INTL-CRUSTAL-001, 2026-04-23)
- Subtitles épistémiques sur `foret`, `cav`, `therm` ajoutés en légende (PR #179, 2026-04-26)

**Discussions en suspens (sans décision claire)** :
- `b-emag` vs `b-wdmam` : recommandation `EMAG2_WDMAM_NOTE_RECHERCHE.md` propose 2 scénarios (garder les deux différenciés ou simplifier à une seule). Pas de décision tranchée.
- `b-cav`, `b-therm`, `b-hyd` : statut « contexte structurel » documenté en légende mais aucun arbitrage explicite sur leur conservation/retrait/reclassification.

**Décisions non implémentées** :
- `WDMAM-NAMING-001` (PR #127) — renommage technique différé volontairement (priorité Faible). La dette reste ouverte.

---

## 5. Tableau de synthèse — Verdicts (Bloc D du brief)

| # | Bouton | Layer | MOD-CALC | Statut épistémique | Arbitrage historique | **VERDICT** | Justification |
|---|---|---|---|---|---|---|---|
| 1 | b-geo | wmsGeo | OUI-parallèle | Visuel BRGM, dataset GEO_SUSC_GRID parallèle | aucun arbitrage de retrait | **CONSERVER** | substrat magnétique structurant, parallèlement consommé par calcGeoSusc |
| 2 | b-foret | wmsForet | NON | « couche visuelle niveau A » explicite | Zone 7 (2026-04-19) verdict B confirmé | **CONSERVER** | référence comparative/visuelle confirmée |
| 3 | b-failles | lFailles | OUI-direct | EPISTEMIC NOTE « contexte structural » | aucun arbitrage de retrait | **CONSERVER** | impact direct calcFaultProximity + calcSubstrateContext, indispensable au calc EM |
| 4 | b-radon *(hors brief)* | lRadon | OUI-direct | Polygones ASNR/IRSN officiels | aucun arbitrage de retrait | **CONSERVER (à confirmer en chat)** | hors brief Soleil — à vérifier que c'est un oubli, pas un choix de scope |
| 5 | b-points-chauds | lPointsChaudsRadio | NON | catalogue documentaire explicite | aucun arbitrage de retrait | **CONSERVER** | catalogue de sites à mesurer, statut documentaire transparent |
| 6 | b-sites-remarq | lSitesRemarq | NON | catalogue documentaire explicite | aucun arbitrage de retrait | **CONSERVER** | catalogue de sites singuliers, statut documentaire transparent |
| 7 | b-hyd | wmsHyd | OUI-parallèle (faible) | légende enrichie, calcWater utilise dataset distinct | aucun arbitrage de retrait | **AMBIGU** — arbitrer en chat | **Question** : la couche WMS est purement visuelle (calcWater n'en dépend pas). Reclasser comme « contexte structurel pur » (groupe B) ou retirer pour cohérence du modèle ? |
| 8 | b-cav | wmsCav | NON | légende suggère anomalies magnétiques mais aucun calc | aucun arbitrage de retrait | **AMBIGU** — arbitrer en chat | **Question** : la mention « Anomalies magnétiques locales (discontinuité de susceptibilité) » de la légende suggère un effet EM. Le calc ne le modélise pas. Soit on documente explicitement « non calculé », soit on retire la mention, soit on retire la couche. |
| 9 | b-therm | lTherm | NON | légende « marqueurs de failles, courants telluriques » mais aucun calc | aucun arbitrage de retrait | **AMBIGU** — arbitrer en chat | **Question** : 6 sites thermaux hardcodés. Indicateur de failles actives (déjà couvert par `b-failles`). À conserver comme indicateur structurel distinct, ou intégrer comme métadonnée dans `b-failles` ? |
| 10 | b-emag | wmsEmag | OUI-parallèle | « fond géologique régional » explicite | EMAG2_WDMAM_NOTE recommande de le conserver | **CONSERVER** | source canonique EMAG2v3 régionale, parallèlement consommé par calcLCS1 |
| 11 | b-wdmam | wmsWDMAM | NON | « EMAG2 mondial » (renommé en PR #125) | EMAG2_WDMAM_NOTE recommande arbitrage ; dette WDMAM-NAMING-001 ouverte | **AMBIGU** — arbitrer en chat | **Question** : redondance fonctionnelle confirmée avec `b-emag` (même source NOAA, seule la bbox diffère). Justifie-t-on de conserver une vue mondiale dynamique distincte de la vue régionale, ou simplifier à `b-emag` seul ? |
| 12 | b-crustal | lCrustal | NON | « 5 références mondiales pédagogiques » | INTL-CRUSTAL-001 fermée 2026-04-23 | **AMBIGU** — arbitrer en chat | **Question** : module opt-in pédagogique introduit récemment. Conserver comme outil de mise en perspective (5 cratères/BIFs mondiaux) ou retirer pour simplifier le menu ? Pas d'usage détecté dans les calcs. |

### 5.1 Récapitulatif

- **CONSERVER** : 7 couches sur 12 (b-geo, b-foret, b-failles, b-radon, b-points-chauds, b-sites-remarq, b-emag)
- **RETIRER** : 0
- **AMBIGU — arbitrer en chat** : 4 couches (b-hyd, b-cav, b-therm, b-wdmam, b-crustal) → 5 si on inclut b-radon (hors brief)

### 5.2 Pour les verdicts AMBIGU — Chaînes de dépendance à supprimer (préparation phase 2)

*Note : aucun verdict RETIRER actuellement. Les chaînes ci-dessous sont fournies par anticipation au cas où Soleil tranche en AMBIGU vers RETIRER.*

#### Si retrait de `b-hyd` (Hydrographie WMS)

Suppressions à effectuer :
- HTML : `<button id="b-hyd">` ligne 1487
- CSS : `.on-hyd` (existe ?), à grepper
- JS — déclaration : `wmsHyd` ligne 2035
- JS — entrées : `WMS.hyd` (ligne 2062), `ACTIVE.hyd` (ligne 2063)
- JS — fragments toggle : `tog` ligne 2415 (`if(id==='hyd')…op-row`), ligne 2422 (idem)
- JS — légende : `LEGEND_HTML.hyd` ligne 2074
- HTML — op-row : `<div id="hyd-op-row">` à grepper
- **À conserver** : `RIVER_PTS` (ligne 3764) et `calcWater` (3759) — utilisés par `calcSubstrateContext`. Le retrait de la couche ne touche pas le calc parallèle.

#### Si retrait de `b-cav` (Cavités)

- HTML : ligne 1488
- JS — déclaration : `wmsCav` ligne 2036
- JS — entrées : `WMS.cav` (2062), `ACTIVE.cav` (2063)
- JS — légende : `LEGEND_HTML.cav` ligne 2076
- pas de fragment tog spécifique (passe par `tog` générique)
- pas de calc à supprimer
- **CSS à grepper** : `.on-cav`

#### Si retrait de `b-therm` (Émergences thermales)

- HTML : ligne 1489
- JS — déclaration : `lTherm` ligne 2049
- JS — entrées : `LAYERS.therm` (2061), `ACTIVE.therm` (2063)
- JS — fragment tog : `tog` ligne 2425 (`if(id==='therm')…buildThermLayer`)
- JS — fonction : `buildThermLayer` (5436-5449)
- JS — dataset : `THERMAL_SOURCES_CORSE` (4309-4316)
- JS — légende : `LEGEND_HTML.therm` ligne 2082
- CSS à grepper : `.on-therm`

#### Si retrait de `b-wdmam` (EMAG2 mondial dynamique)

- HTML : ligne 1491
- JS — variable : `wmsWDMAM` ligne 6740 (let)
- JS — fonction : `togWDMAM` (6741-6757)
- JS — légende : `LEGEND_HTML.wdmam` ligne 2078
- HORS LAYERS/WMS — pas de fragment dans `tog`
- CSS à grepper : `.on-wdmam`
- **Dette WDMAM-NAMING-001** se résoudrait automatiquement par retrait

#### Si retrait de `b-crustal` (Crustale mondiale 5 réf)

- HTML : ligne 1492
- JS — déclaration : `lCrustal` ligne 2056
- JS — entrées : `LAYERS.crustal` (2061), `ACTIVE.crustal` (2063)
- JS — fragments tog : `tog` ligne 2417 (`showCrustalGauge(false)`), 2426 (`buildCrustalLayer + showCrustalGauge(true)`)
- JS — dataset : `CRUSTAL_REFS` (2605-2621)
- JS — fonctions : `buildCrustalLayer` (2624) + `showCrustalGauge` (à grepper)
- JS — légende : `LEGEND_HTML.crustal` ligne 2080
- CSS à grepper : `.on-crustal`
- Réouverture éventuelle de la dette **INTL-CRUSTAL-001** (actuellement fermée)

---

## 6. Classification proposée — révision (Bloc E du brief)

### 6.1 Proposition initiale Soleil

> A. Substrat magnétique : Géologie BRGM, Crustale EMAG2
> B. Contexte structurel : Failles, Cavités, Sources thermales, Hydrographie
> C. Sites documentaires : Sites U/Th, Sites géophysiques remarquables
> D. Référence comparative : Forêts, WDMAM mondial, Crustale mondiale

### 6.2 Audit de la classification

L'audit confirme **partiellement** la proposition. **Trois corrections nécessaires** :

#### Correction 1 — `b-failles` doit basculer **B → A**

`calcFaultProximity` (4350) et `calcSubstrateContext` (3958-3963) consomment directement `FAILLES_CORSE`. C'est un **impact direct calcul EM**, pas seulement un contexte structurel. La couche est centrale au modèle.

#### Correction 2 — `b-radon` (12e couche, hors brief) doit être en **A**

`calcRadonPotential` (4108) et `calcSubstrateContext.radon_potential_class` (3950-3956) consomment directement les classes radon. La couche `lRadon` (polygones ASNR/IRSN) module donc le calcul. **Impact direct.**

#### Correction 3 — `b-hyd` reste en B mais avec une nuance forte

Le calc `calcWater` (3759) utilise des `RIVER_PTS` hardcodés inline, **pas** la donnée WMS BRGM REMNAPPE. La couche WMS est **visuellement utile** mais **fonctionnellement découplée** du calc. C'est un **contexte structurel pur visuel** — pas un indicateur documenté contribuant au calc.

### 6.3 Classification corrigée par l'audit

| Sous-groupe | Couches | Justification audit |
|---|---|---|
| **A. Substrat magnétique / impact direct calc** | `b-geo`, `b-failles`, `b-radon`, `b-emag` | `b-geo` via `GEO_SUSC_GRID`/`calcGeoSusc` ; `b-failles` via `calcFaultProximity` ; `b-radon` via `calcRadonPotential` ; `b-emag` via `calcLCS1`/`EMAG2_CACHE` |
| **B. Contexte structurel visuel (pas de calc)** | `b-cav`, `b-therm`, `b-hyd` | tous trois ont des subtitles épistémiques ajoutés en PR #179 mais **aucun calc ne consomme leur donnée**. Couches d'orientation/contexte. **À arbitrer** : conserver groupé ? |
| **C. Sites documentaires** | `b-points-chauds`, `b-sites-remarq` | catalogues de sites à mesurer ; tooltips explicites « doses non mesurées », « mesures in situ requises » |
| **D. Référence comparative mondiale/extérieure** | `b-foret`, `b-wdmam`, `b-crustal` | `b-foret` (RF only ITU-R P.833, hors modèle) ; `b-wdmam` (EMAG2v3 mondial dynamique) ; `b-crustal` (5 cratères/BIFs pédagogiques opt-in) |

**12 couches → 4 sous-groupes** (4 + 3 + 2 + 3).

### 6.4 Forêts — confirmation que c'est purement visuel

Confirmé par 4 sources convergentes :
- title bouton ligne 1482 (« couche visuelle niveau A — pas de modulation calcul »)
- commentaires code 2037-2040
- `RECHERCHE_Zones7-8-9_CouchesNaturelles_2026-04-19.md` (verdict B explicite)
- absence de référence à `wmsForet` ou `foret` dans toute fonction `calc*` (vérifié par grep)

Verdict CONSERVER en groupe **D**. Pas de réouverture de débat possible sans nouvelle preuve scientifique.

---

## 7. Questions à arbitrer en chat avec Soleil (pour la phase 2)

### Q1 — `b-radon` est-il un oubli du brief ou un choix de scope ?

Le brief liste 11 boutons mais le menu en contient **12**. `b-radon` (ligne 1484, entre `b-failles` et `b-points-chauds`) module `calcRadonPotential` (4108) et est piloté par les polygones officiels ASNR/IRSN (PR à grepper). À traiter en groupe A par défaut, mais à confirmer.

### Q2 — `b-hyd` Hydrographie : conserver, reclasser ou retirer ?

La couche WMS BRGM REMNAPPE est **purement visuelle** (le calc parallèle `calcWater` utilise des points hardcodés distincts). Trois options :
- (a) Conserver dans le groupe B comme contexte structurel visuel — message à l'utilisateur clarifié (« visuel uniquement, le calc utilise un dataset distinct »)
- (b) Retirer (cohérence avec `RECHERCHE_Zones7-8-9` qui dit « eau = proxy géologique déjà couvert ») et garder `RIVER_PTS` dans `calcSubstrateContext`
- (c) Conserver mais sans annonce épistémique (couche purement visuelle, sans prétention de modulation)

**Recommandation audit** : (a) pour la cohérence avec le pattern de Forêts (visuel niveau A annoncé).

### Q3 — `b-cav` Cavités : statut explicite à clarifier

La légende dit « Anomalies magnétiques locales (discontinuité de susceptibilité) » — vrai phénomène géophysique mais **non modélisé** dans le code Tellux. Trois options :
- (a) Conserver et **expliciter** dans la légende qu'il s'agit d'un phénomène documenté mais non calculé (« indicateur structurel non modélisé »)
- (b) Retirer la mention « Anomalies magnétiques » de la légende ; conserver la couche comme purement visuelle (cohérent avec la décision sur Forêts)
- (c) Retirer la couche

**Recommandation audit** : (b). La phrase actuelle suggère un effet calc qui n'existe pas — risque de désinformer l'utilisateur.

### Q4 — `b-therm` Émergences thermales : redondance avec `b-failles` ?

6 sites thermaux hardcodés, présentés comme « marqueurs de failles actives ». Or `b-failles` couvre déjà 8 failles. Trois options :
- (a) Conserver les deux : `b-failles` = trait géométrique faille, `b-therm` = manifestation hydrothermale ponctuelle observable
- (b) Intégrer les 6 sites thermaux comme métadonnée dans la couche `b-failles` (popup enrichi) et retirer le bouton dédié
- (c) Retirer la couche thermale (redondance fonctionnelle)

**Recommandation audit** : (a). Distinction sémantique légitime — la faille est une structure géologique, l'émergence thermale est une observation de surface.

### Q5 — `b-wdmam` vs `b-emag` : redondance de source NOAA EMAG2v3

Confirmé : **même source** (NOAA EMAG2v3 ImageServer), seule la bbox diffère (Corse fixe vs viewport dynamique). Recommandation `EMAG2_WDMAM_NOTE_RECHERCHE.md` (2026-04-24) :

> *« WDMAM apporte une valeur ajoutée de contexte mondial mais redondant à l'échelle de la Corse seule. La différence visuelle sera minime pour un public non expert sur une zone aussi petite. »*

Trois options :
- (a) Conserver les deux : `b-emag` = vue par défaut Corse, `b-wdmam` = « zoom-out mondial » à la demande
- (b) Fusionner : la couche `b-emag` se redessine selon la bbox courante (comme `wmsWDMAM`). Retirer `b-wdmam`. Renommer `b-emag` → « Anomalie magnétique crustale (EMAG2v3) ».
- (c) Retirer `b-wdmam`, conserver `b-emag` strict bbox Corse.

**Recommandation audit** : (b). Élimine la dette `WDMAM-NAMING-001` automatiquement. Évite la redondance utilisateur. Une seule couche, comportement bbox-dynamique de fait.

### Q6 — `b-crustal` Crustale mondiale 5 références : module pédagogique à conserver ?

Module opt-in, désactivé par défaut, pas de calc consumer. Introduit récemment (PR #103 INTL-CRUSTAL-001, 2026-04-23). Trois options :
- (a) Conserver dans le groupe D (référence comparative) — c'est sa place naturelle
- (b) Retirer (simplification du menu)
- (c) Le déplacer dans une section « Outils pédagogiques » distincte

**Recommandation audit** : (a). Module récent, résolu en dette fermée, opt-in (n'encombre pas par défaut), enrichit le contexte pour public expert/curieux.

### Q7 — Quelle stratégie pour l'explication globale (« couches d'impact indirect ») ?

L'explication actuelle est dispersée (5 endroits, dont 4 invisibles en lecture rapide). Trois options pour la phase 2 :
- (a) Centraliser dans le header du Groupe 3 (avant les boutons) un texte de 2-3 lignes
- (b) Ajouter un sous-bouton « ℹ Comprendre les couches » qui ouvre un modal détaillé
- (c) Maintenir le statu quo (subtitles dans LEGEND_HTML, visibles seulement après activation)

**Recommandation audit** : (a) pour la pédagogie immédiate, ou (b) si on veut un détail par couche. (c) déjà jugé insuffisant par Soleil puisqu'il a oublié où l'explication était.

### Q8 — Code mort `lCem` : purger en passant en phase 2 ?

`lCem` (ligne 2055), `LAYERS.cem` (2061), `ACTIVE.cem` (2063) — vestige sans bouton ni loader. Hors scope brief, **non purgé** dans cet audit (règle stricte). À arbitrer : intégrer la purge à la PR phase 2 du Groupe 3, ou ouvrir un ticket séparé ?

**Recommandation audit** : intégrer à la PR phase 2 (gain marginal, déjà en main sur la zone du fichier).

---

## 8. Annexes

### A — Fichiers consultés pour cet audit

- `app.html` (HEAD `main` `4add85c`) — lecture intégrale ciblée des zones : 1474-1494 (HTML menu), 2030-2110 (déclarations layers + WMS + LAYERS/ACTIVE/LEGEND_HTML), 2408-2447 (toggle générique), 2580-2900 (calc magnétiques), 3528-3611 (loaders dataset), 3759-3990 (calcWater + calcSubstrateContext + calcGeoSusc), 4036-4365 (radon + EPISTEMIC NOTES + failles dataset + calcFaultProximity), 5436-5450 (buildThermLayer), 6362-6760 (handlers tog dédiés + togWDMAM)
- `transparence.html` — recherche grep pas de mention couches d'impact indirect
- `EMAG2_WDMAM_NOTE_RECHERCHE.md` (2026-04-24, 162 lignes) — note de recherche sur les 3 couches magnétiques
- `_archive/recherche_axes/RECHERCHE_Zones7-8-9_CouchesNaturelles_2026-04-19.md` (406 lignes) — verdicts Zone 7/8/9
- `NETTOYAGE_PROPOSE.md` (2026-04-20) — pas pertinent direct
- `RECAP_AUDIT_CONSOLIDATION_2026-04-27.md` (2026-04-27) — pas pertinent direct (corpus scientifique)
- Git log via `git log --all --grep` sur EMAG/crustal/wdmam/couche/menu/contexte naturel

### B — Patterns recherchés et résultats

- `niveau A | couche visuelle | impact indirect | pas un amplificateur | contexte structur` → trouvé dans `app.html` (3 fois), `transparence.html` (0 fois), `_archive/exports_html/TELLUX_DOCUMENT_COMPLET_CONTACT.html` (mentions corpus scientifique différentes), `_archive/exports_html/TELLUX_CADRE_CONDENSE.html` (idem)
- `niveau A | couche visuelle | impact indirect | pas un amplificateur | contexte structur` (.md) → 9 fichiers dont 8 hors scope corpus, 1 pertinent (`docs/data-sources/bd_foret_v2_corse_notes.md` — non lu, à explorer si phase 2 a besoin)

### C — Code mort signalé pour la phase 2

- `lCem` ligne 2055, `LAYERS.cem` ligne 2061, `ACTIVE.cem` ligne 2063 — variable orpheline sans bouton ni loader.

### D — Dettes techniques actives sur le périmètre

- **WDMAM-NAMING-001** (2026-04-24) — renommage JS différé (`wmsWDMAM`, `togWDMAM`, `LEGEND_HTML.wdmam`, `#b-wdmam`, `.on-wdmam`). Priorité Faible. Se résoudrait par retrait de la couche (Q5 option (b) ou (c)).

### E — Avertissement sur l'audit Explore initial

Un agent Explore a été lancé en début d'audit pour mapper les 11 couches d'`app.html`. **Son output a été rejeté** : il a inventé des IDs de boutons (`b-geologie`, `b-hydrologie`, `b-radon`, `b-emag2`, etc.) qui ne correspondent pas aux IDs réels du fichier (`b-geo`, `b-hyd`, etc.). L'audit a été refait par lecture directe + grep ciblé sur les IDs canoniques du brief Soleil. Mention à conserver pour la rigueur méthodologique : tout futur audit similaire doit verrouiller la liste des IDs par grep direct avant de déléguer.
