# TELLUX — Audit A-4b : pattern couche ↔ panneau ↔ légende

**Date :** 14 avril 2026
**Fichier audité :** `tellux_CORRECT.html` (7 630 lignes)
**Modèle :** Sonnet

---

## 1. Inventaire des couches

| ID couche | Bouton HTML | Layer Leaflet | Panneau d'options | Légende (LEGEND_HTML) | Fonction build/load | ACTIVE init |
|---|---|---|---|---|---|---|
| `hot` | `b-hot` (L1190) | `lHot` (layerGroup, `.addTo(map)`) | — | ✅ `hot` | `buildHot()` | `true` |
| `con` | ❌ **ABSENT** (`b-con` jamais créé) | `lCon` (layerGroup) | `#contrib-panel` (L1913) | ❌ aucune | `loadDB()` (async, init+interval) | `false` |
| `sit` | `b-sit` (L1156) | `lSit` (layerGroup) | — | ✅ `sit` | `buildSiteMarkers()` via `loadSitesReference()` | `false` |
| `sit2` | `b-sit2` (L1162) | `lSit2` (layerGroup) | — | ✅ `sit2` | `buildSit2()` | `false` |
| `egl` | `b-egl` (L1157) | `lEgl` (layerGroup) | — | ✅ `egl` | `buildEglLayer()` (async) | `false` |
| `align` | `b-align` (L1158) | `lAlign` (layerGroup) | — | ✅ `align` | `buildAutoAlignments()` | `false` |
| `ant` | `b-ant` (L1204) | `lAnt` (layerGroup) | — | ✅ `ant` | `loadAnt()` (async) | `false` |
| `antOffshore` | ❌ **ABSENT** (pas de bouton UI) | `lAntOffshore` (layerGroup) | — | Partage `ant` | `loadAnt()` (async, aussi pour ant) | `false` |
| `res` | `b-res` (L1202) | `lRes` (layerGroup) | — | ✅ `res` | `loadReseau()` (async) | `false` |
| `bt` | `b-bt` (L1203) | `lBT` (layerGroup) | — | ✅ `bt` | `loadBT()` (async) | `false` |
| `geo` | `b-geo` (L1173) | `wmsGeo` (WMS) | `#geo-op-row` (slider opacité, L1225) | ✅ `geo` | — (WMS direct) | `false` |
| `hyd` | `b-hyd` (L1174) | `wmsHyd` (WMS) | `#hyd-op-row` (slider opacité, L1226) | ✅ `hyd` | — (WMS direct) | `false` |
| `emag` | `b-emag` (L1177) | `wmsEmag` (imageOverlay) | `#emag-op-row` (slider opacité, L1227) | ✅ `emag` | — (imageOverlay direct) | `false` |
| `cav` | `b-cav` (L1176) | `wmsCav` (WMS) | — | ✅ `cav` | — (WMS direct) | `false` |
| `radon` | `b-radon` (L1175) | `lRadon` (layerGroup) | — | ❌ **ABSENT** | `buildRadonLayer()` | `false` |
| `net` | `b-net` (L1179) | `lNet` (layerGroup) | — | ✅ `net` | `buildNets()` (init) | `false` |
| `aoc` | `b-aoc` (L1216) | `lAOC` (layerGroup) | — | ✅ `aoc` | `buildAOCLayer()` | `false` |
| `rpg` | ❌ **DISABLED** (L1218) | `wmsRPG` (WMS) + `lRPG` | — | ❌ aucune | — (WMS) | `false` |
| `foret` | ❌ **DISABLED** (L1217) | `wmsForet` (WMS) + `lForet` | — | ❌ aucune | — (WMS) | `false` |
| `cem` | ❌ **ABSENT** (pas de bouton toggle) | `lCem` (layerGroup) | `#cem-panel` (CartoRadio, L1741) | ❌ aucune | `loadCEMSample()` (init) | `false` |
| `intl` | `b-intl` (L1191) | `lIntl` (layerGroup) | — | ✅ `intl` | `buildIntlLayer()` | `false` (activé programmatiquement à L6688) |

**Système de légende :** `LEGEND_ACTIVE` (Set), `updateLegendPanel()` (L2179), `showLegend(id,bool)` (L2187).
**Ordre légende :** `['hot','res','bt','ant','geo','hyd','cav','emag','intl','align','egl','net','sit','sit2','aoc']` (L2182).
**Fonction tog :** L2188-2216. Gère activation/désactivation, panneaux d'opacité (geo/hyd/emag), légendes, builds lazy.

---

## 2. Incohérences détectées

### 🔴 INC-1 — `startContrib()` crash sur bouton `b-con` inexistant

**Couche :** `con`
**Type :** Activation
**Lignes :** L2993
**Description :** `startContrib()` appelle `tog('con','on-con',document.getElementById('b-con'))`. Or `b-con` n'existe pas dans le HTML — `getElementById` retourne `null`. Dans `tog` (L2196), `btn.classList.add(cls)` provoque un **TypeError: Cannot read properties of null**.
**Impact :** Crash silencieux quand l'utilisateur clique "Ajouter une mesure" depuis le sidebar (si le flow passe par `startContrib()` plutôt que `startContribFromFAB()`).
**Note :** `startContribFromFAB()` (L7020-7021) a un guard `if(btn&&!ACTIVE.con)` — correct. Mais `startContrib()` (L2993) n'a pas ce guard.
**Correction :** Ajouter le même guard dans `startContrib()` : `const btn=document.getElementById('b-con'); if(btn&&!ACTIVE.con){tog('con','on-con',btn);} else if(!ACTIVE.con){ACTIVE.con=true;map.addLayer(LAYERS.con);}`

### 🔴 INC-2 — `tog()` crash sur `btn` null pour couches sans bouton

**Couche :** `con`, `cem`, `antOffshore`
**Type :** Activation / Désactivation
**Lignes :** L2190, L2196
**Description :** Si `tog()` est appelé avec `btn=null` (ce qui arrive si `document.getElementById('b-xxx')` retourne null), les opérations `btn.className='lbtn'` (désactivation, L2190) ou `btn.classList.add(cls)` (activation, L2196) provoquent un TypeError.
**Impact :** Crash pour toute couche sans bouton HTML si `tog` est appelé programmatiquement.
**Correction :** Ajouter un guard dans `tog` : `if(btn)btn.className='lbtn'` et `if(btn)btn.classList.add(cls)`.

### 🟡 INC-3 — Couche `radon` sans légende

**Couche :** `radon`
**Type :** Activation
**Lignes :** LEGEND_HTML (L2030-2047), ordre légende (L2182)
**Description :** `radon` a un bouton (`b-radon`), un layer (`lRadon`), un build (`buildRadonLayer`) — mais pas d'entrée dans `LEGEND_HTML` et pas de place dans l'ordre de la légende. Quand on active le radon, `showLegend('radon',true)` ajoute `'radon'` au Set `LEGEND_ACTIVE` mais `updateLegendPanel` ne le rend pas car il n'est pas dans l'ordre `['hot','res',...]`.
**Impact :** Pas de légende affichée pour la couche radon. L'utilisateur voit des marqueurs sans explication.
**Correction :** Ajouter une entrée `radon` dans `LEGEND_HTML` et dans le tableau `order` de `updateLegendPanel`.

### 🟡 INC-4 — `rpg` et `foret` : logique toggle inversée (code mort)

**Couche :** `rpg`, `foret`
**Type :** Activation
**Lignes :** L2208-2209
**Description :** Dans la branche activation de `tog` (ACTIVE vient de passer à `true`), le code fait `wmsRPG[ACTIVE.rpg?'remove':'addTo'](map)`. Puisque `ACTIVE.rpg` est déjà `true`, cela appelle `wmsRPG.remove(map)` au lieu de `addTo`. Même chose pour `foret`.
**Impact :** Actuellement nul car les boutons sont `disabled`. Mais si les boutons sont réactivés, les couches ne s'afficheront pas.
**Gravité réduite :** Les boutons sont désactivés (`disabled` + `opacity:0.4`). Bug latent uniquement.
**Correction :** Retirer ces deux lignes ou les corriger : `wmsRPG.addTo(map)` dans la branche activation, `map.removeLayer(wmsRPG)` dans la branche désactivation.

### 🟡 INC-5 — `egl` : légende non retirée si désactivation pendant build async

**Couche :** `egl`
**Type :** Désactivation (cas limite)
**Lignes :** L2213
**Description :** `buildEglLayer().then(()=>{if(ACTIVE.egl)showLegend('egl',true);})` vérifie `ACTIVE.egl` dans le `.then()` — correct pour l'activation. Mais si l'utilisateur désactive `egl` immédiatement après activation (pendant le fetch), la désactivation passe par la branche standard (L2194) qui fait `showLegend('egl',false)`. Cependant, si le `.then()` s'exécute après, il fait `if(ACTIVE.egl)showLegend('egl',true)` — comme `ACTIVE.egl` est `false` à ce moment, la légende n'est pas re-ajoutée. **Pas de bug réel** — le guard fonctionne.
**Impact :** Aucun. Le pattern est correct. Résolu par le guard `if(ACTIVE.egl)`.
**Correction :** Aucune nécessaire.

### 🟡 INC-6 — `intl` activé programmatiquement au démarrage sans guard double-build

**Couche :** `intl`
**Type :** État initial
**Lignes :** L6687-6690
**Description :** `setTimeout(()=>{tog('intl','on-intl',bi)},600)` active `intl` 600ms après l'init. Si l'utilisateur clique sur le bouton `b-intl` dans les 600 premières ms, `tog` sera appelé deux fois. La première fois construit `lIntl` (guard `getLayers().length===0`), la deuxième fois la désactive. Le build ne sera pas dupliqué grâce au guard — pas de vrai bug.
**Impact :** Cosmétique. Si clic rapide, la couche est désactivée alors que l'utilisateur voulait l'activer. Comportement surprenant mais non bloquant.
**Correction :** Aucune correction urgente. Le guard `getLayers().length===0` protège contre le double-build.

### 🟡 INC-7 — `closePanel()` ne synchronise pas la couche

**Couche :** Toutes (panneau `mpanel`)
**Type :** Fermeture programmatique
**Lignes :** L6643-6646
**Description :** `closePanel()` ferme `#mpanel` (panneau de diagnostic/modèle au clic carte). Ce panneau n'est PAS un panneau de couche — c'est le panneau principal d'information. Sa fermeture n'a pas besoin de désactiver une couche. **Pas d'incohérence.**
**Correction :** Aucune.

### 🟡 INC-8 — `hypo-list-panel` : bouton ✕ ne désactive pas la couche hypothèses

**Couche :** Hypothèses (pas une couche au sens ACTIVE, mais un panneau)
**Type :** Fermeture programmatique
**Lignes :** L1728
**Description :** Le bouton ✕ du panneau `hypo-list-panel` fait `document.getElementById('hypo-list-panel').style.display='none'`. Le panneau hypothèses n'est pas lié à une couche toggleable dans ACTIVE — il a son propre système de navigation. **Pas d'incohérence avec le pattern couche↔légende.**
**Correction :** Aucune.

### 🟢 INC-9 — Couches `cem`, `con`, `antOffshore` sans bouton toggle UI

**Couche :** `cem`, `con`, `antOffshore`
**Type :** Design
**Description :**
- `cem` : pas de bouton toggle. Activé uniquement via `importCartoRadioCSV()`. Les données sont pré-chargées dans `lCem` par `loadCEMSample()` au init mais le layer n'est pas sur la carte. Pattern acceptable — les données CEM alimentent le modèle RF, pas l'affichage utilisateur.
- `con` : pas de bouton toggle. Activé programmatiquement via `startContrib()`/`startContribFromFAB()`. Le panneau `contrib-panel` s'affiche si des contributions existent. Pattern acceptable — la couche s'active automatiquement quand nécessaire.
- `antOffshore` : pas de bouton toggle. Chargé via `loadAnt()` dans le layer `lAntOffshore`. Partage la légende `ant`. Pattern acceptable — couche secondaire liée à `ant`.
**Impact :** Cosmétique. L'utilisateur ne peut pas toggler ces couches manuellement.
**Correction :** Reporté voie B. Si nécessaire, ajouter des boutons toggle.

### 🟢 INC-10 — `con` : `contrib-panel` visible/masqué indépendamment du toggle couche

**Couche :** `con`
**Type :** Synchronisation panneau
**Lignes :** L2978
**Description :** `loadDB()` (L2978) fait `contrib-panel.style.display=n>0?'block':'none'` — affiche le panneau si des contributions existent, indépendamment de `ACTIVE.con`. Le panneau est une section informative dans le sidebar, pas un overlay cartographique. **Pas d'incohérence fonctionnelle.**
**Correction :** Aucune.

### 🟢 INC-11 — Mobile : accordéon fermé après toggle — pattern correct

**Type :** Responsive
**Lignes :** L2189
**Description :** `tog` commence par fermer l'accordéon mobile si ouvert. Vérifié : le pattern est cohérent. Après toggle, l'accordéon se ferme pour laisser la carte visible. Correct.
**Correction :** Aucune.

---

## 3. Statistiques

| Métrique | Valeur |
|---|---|
| Couches inventoriées | 21 (dont 2 disabled, 3 sans bouton UI) |
| Incohérences détectées | 11 |
| 🔴 Bloquantes | 2 (INC-1, INC-2) |
| 🟡 Gênantes | 4 (INC-3, INC-4, INC-5[non-bug], INC-6[non-bug]) |
| 🟢 Cosmétiques | 3 (INC-9, INC-10, INC-11) |
| Non-bugs confirmés | 4 (INC-5, INC-6, INC-7, INC-8) |
| Couches avec légende | 16/21 |
| Couches avec panneau d'options | 3 (geo, hyd, emag) |

---

## 4. Corrections appliquées

### Fix INC-1 + INC-2 : guard `btn` null dans `tog()` et `startContrib()`

**tog() — L2190 et L2196 :**
```
Avant: btn.className='lbtn'
Après: if(btn)btn.className='lbtn'

Avant: btn.classList.add(cls)
Après: if(btn)btn.classList.add(cls)
```

**startContrib() — L2993 :**
```
Avant: if(!ACTIVE.con){tog('con','on-con',document.getElementById('b-con'));}
Après: const _bcon=document.getElementById('b-con');
       if(!ACTIVE.con){if(_bcon){tog('con','on-con',_bcon);}else{ACTIVE.con=true;map.addLayer(LAYERS.con);}}
```

### Fix INC-3 : légende radon ajoutée

Ajout dans `LEGEND_HTML` :
```
radon:'<div class="leg-block"><b class="leg-title">Radon (cat. 3)</b><div class="leg-row"><span style="display:inline-block;width:10px;height:8px;background:#ea580c;border-radius:2px"></span> Potentiel radon élevé</div><div class="leg-row"><span style="font-size:9px;color:var(--tx3)">Massifs granitiques</span></div><div class="leg-src">ASNR · Zones cat. 3</div></div>'
```

Ajout de `'radon'` dans le tableau `order` de `updateLegendPanel`.

### Fix INC-4 : logique rpg/foret corrigée

```
Avant (L2208): if(id==='rpg')wmsRPG[ACTIVE.rpg?'remove':'addTo'](map);
Après: if(id==='rpg')wmsRPG.addTo(map);

Avant (L2209): if(id==='foret')wmsForet[ACTIVE.foret?'remove':'addTo'](map);
Après: if(id==='foret')wmsForet.addTo(map);
```

Ajout dans la branche désactivation :
```
if(id==='rpg')map.removeLayer(wmsRPG);
if(id==='foret')map.removeLayer(wmsForet);
```

---

## 5. Items reportés voie B

- INC-9 : boutons toggle pour `cem`, `con`, `antOffshore`
- Légendes manquantes pour `cem`, `con`, `rpg`, `foret` (couches sans bouton ou disabled)
- Système FIFO de limitation de couches (existait dans `tellux_v6_design.html` mais absent dans `tellux_CORRECT.html`)
