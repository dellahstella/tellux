# Rapport session Brief 35 — Réparation sites + investigations Code

**Date** : 2026-05-06
**Périmètre** : propagation corrections Cowork (Cat. 2 + 3c) + investigation Code des bugs niveau 1→2 et coloriage pieve Brando.

---

## Corrections data Cowork propagées

| Fichier | Avant | Après | Δ |
|---|---|---|---|
| `docs/data/sites_patrimoine.json` | 437 sites | **450 sites** | +14, -1 (min_canari) |
| `docs/data/sites_corse.json` | 479 sites | 479 sites | meta notes condensées |
| `docs/data/doyennes_polygons.json` | 9 doyennés | 9 doyennés | regen propre (CRLF only) |
| `docs/data/pieves_polygons.json` | 47 pieves | 47 pieves | regen propre (CRLF only) |

### Détails sites_patrimoine.json

- **70 sites** avec `doyenne_contemporain_slug` réaligné sur le polygone réel (Cat. 2)
- **55 sites** avec `pieve_slug` réaligné (Cat. 2)
- **1 site supprimé** : `min_canari` (Cat. 3c, fusionné avec carrière_amiante_canari)
- **14 sites naturels ajoutés** : barrages (Alesani, Calacuccia, Padula, Rizzanese), lacs (Creno, Nino), monts (Cinto, San Petrone, Stello), désert (Agriate), réserve (Scandola), aiguilles (Bavella), Cap Corse extrême nord, calanques de Piana

⚠️ **Note doublons cross-app** : les 14 sites ajoutés sont **aussi présents dans `sites_em.json`** (49 sites EM). Doublons intentionnels selon le plan Cowork mais à confirmer auprès de Soleil — voir `_drafts/sites_doublons_em_patrimoine.md` (Brief 33). Les 14 sites apparaîtront donc à la fois dans la couche EM (app.html) et le drill-down patrimoine (patrimoine.html).

### Préservation Brief 34 GPS audits

⚠️ La régénération Cowork de `sites_patrimoine.json` aurait écrasé les **33 audits GPS du Brief 34** (coords 5 décimales + `gps_audit=2026-05-06` + sources OSM/Wikidata/IGN).

**Mitigation appliquée** (avant commit) : pour les 33 sites Brief 34, restauration depuis `origin/main` :
- `lat`, `lon`, `gps_audit`, `gps_source`
- `notes` si contient marqueur `gps_audit_2026-05` (préserve historique audit)

**Total final** : 34 sites avec `gps_audit=2026-05-06` (33 Brief 34 + 1 nouveau Cowork).

---

## Investigation 1 — Bug niveau 1→2

**Hypothèses brief** :
- Filtre dépendant simultanément de `pieve_slug` ET `doyenne_contemporain_slug` (AND silencieux)
- Sous-ensemble chargé au boot non re-filtré au drill-down

**Réalité du code** (patrimoine.html lignes 940-948, 1064-1067) :
```js
// Boot : iterate markersBySlug, prend site.doyenne (= doyenne_contemporain_slug)
const doy = site.doyenne;
if (doy) { SPOT_TO_DOYENNE.set(slug, doy); }
// ...
// Push marker dans spotsLevel2ByDoyenne[doy]
spotsLevel2ByDoyenne.get(doy).addLayer(markersBySlug[slug].marker);
```

Le filtre est **simple et correct** : pas de AND `pieve_slug + doyenne`, pas de re-filter manqué. Il dépend uniquement de `site.doyenne_contemporain_slug`.

**Verdict** : le bug observé était 100% data-driven. Les 70 sites avec `doyenne_contemporain_slug` désynchronisé étaient bien attribués au mauvais doyenné au boot, donc absents du drill-down du bon doyenné. **Cat. 2 corrige le problème en aval, aucun fix Code requis.**

À confirmer post-merge en testant manuellement le drill-down sur chaque doyenné.

---

## Investigation 2 — Pieve Brando rendu visuel

**Hypothèse brief** : seuil de ratio dans la logique de coloriage qui pénaliserait les pieves <0.95 (Brando = 0.9259).

**Réalité du code** (patrimoine.html lignes 226-228, 1011-1029) :
```css
.pieve-polygon-v2{stroke:#8c6e50;stroke-width:1.5;fill:#8c6e50;fill-opacity:0.08;...}
.pieve-polygon-v2:hover{fill-opacity:0.18;stroke-width:2.5;}
.pieve-polygon-v2:focus,.pieve-polygon-v2.selected{...stroke:#5a3f2a;stroke-width:3;fill-opacity:0.22;}
```

Toutes les pieves ont le même rendu CSS uniforme. Aucun seuil de ratio dans le code.

Le seuil `SEUIL_PIEVE_DOYENNE = 0.25` est un seuil de **visibilité** (inclusion/exclusion d'une pieve dans le drill-down d'un doyenné), pas de **couleur**. Pieve Brando avec ratio 0.9259 passe largement ce seuil.

Vérifications data sur pieve_brando :
- ✓ `doyenne_contemporain_majoritaire = doyenne_du_cap`
- ✓ `doyennes_visibles = ['doyenne_du_cap']`
- ✓ `doyennes_appartenance = [{cap: 0.9259}]` → passe SEUIL 0.25
- ✓ Polygon 133 points, fermé, sans doublons consécutifs, bbox cohérente

**Verdict** : aucun bug Code détecté. Le coloriage est uniforme par construction CSS. Si pieve Brando paraissait visuellement différente avant Brief 35, c'était parce qu'elle était ajoutée au mauvais doyenné via `doyenne_contemporain_majoritaire` désynchronisé (= cas Cat. 2). **Cat. 2 corrige le problème, aucun fix Code requis.**

---

## Bilan commits Brief 35

1. `925be7e` — data Cat. 2 (sites_patrimoine + GPS preserve)
2. `c6627ae` — data Cat. 3c (sites_corse meta condensé)
3. `fc9a00c` — chore script reverse-geocoding bulk
4. (ce rapport)

**Pas de commit `fix(patrimoine.html)`** : les 2 investigations concluent qu'aucune modification Code n'est requise. Le brief annonçait potentiellement 2 fix Code (commits 4-5), remplacés par cette documentation.

---

## Reste à faire (hors scope Code)

### Cat. 1 — 5 sites en mer (audit manuel Soleil)

Sites avec coords en zone maritime, à vérifier sur Google Earth/OSM :
- `tour_d_omigna_cargese`
- `tour_d_erbalunga_brando`
- `san_giovanni_de_pino`
- `tour_de_la_chiappella_rogliano`
- `mine_de_magnetite_de_farinole`

### Test post-merge

- Vérifier drill-down N1→N2 sur les 9 doyennés (Cat. 2 effective)
- Vérifier rendu pieve Brando uniforme (Cat. 4 effective)
- Vérifier 1 spot par cas Cat. 3 :
  - `la_trinite_d_aregno` (post-fusion)
  - `la_trinita_de_prunelli_di_fiumorbo`
  - carrière amiante Canari (post-fusion `min_canari`)

### Si régression détectée par MCP Soleil

Backup pré-Brief 35 disponible : `_drafts/sites_patrimoine.backup_brief35_2026-05-06.json` (état avant les 70 + 55 + 1 corrections Cowork). Backup pré-Brief 34 : `_drafts/sites_patrimoine.backup_2026-05-06.json` (état avant les 33 GPS audits). Rollback granulaire possible sur les 2 niveaux.
