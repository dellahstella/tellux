# B-ZONES — Audit inventaire des zones géographiques (Étape 4 pré-FEDER) — 2026-05-18

**Type :** Audit programmatique read-only — inventaire des sites Tellux qui sont des **zones étendues** (km²) actuellement affichés comme pins ponctuels, et plan d'exécution Code pour les transformer en polygones interactifs.
**Auteur :** Cowork (sandbox) — sous validation Soleil avant brief Code.
**Statut :** DRAFT, non commit.
**Référence amont :** sites_patrimoine.json (working tree, 541 sites). ADR-001 (navigation pédagogique). BP-FIX-RATTACHEMENT-COMPLET-001.

---

## 0. Note méthodologique

**Sandbox :** working tree principal (pré-Phase 1, 45 pieves) — la liste des sites zones n'est pas affectée par Phase 1/2 (le rattachement pieve_slug peut différer entre versions, mais les coords et l'identité des sites zones sont identiques).

**Méthode :** double scan de `sites_patrimoine.json` :
1. **Filtre par axe_corpus** : `patrimoine_naturel_sacre` (13 sites) + `remarquables_geologiques` (17 sites) = 30 sites candidats principaux
2. **Filtre par mot-clé dans le nom** : « réserve / désert / forêt / gorges / massif / calanques / lagune / étang / marais / vallée / défilé / presqu' » + noms emblématiques (Scandola, Agriates, Aïtone, Vizzavona, Bonifatu, Cinto, Bavella, Restonica, Spelunca, Rotondo, Renoso, d'Oro, Incudine, Petrone, Tartagine, Tova, Marmano, Pineta, Diane, Urbino, Biguglia, Capo Rosso, Capu Rossu, Anneaux) = 6 sites supplémentaires (3 chapelles « Vizzavona » + Tour de Turghiu + Menhirs Agriate + Défilé de Lancône)

**Sites zones retenus :** 31 candidats au total. Brief Soleil annonce « ~15-25 sites » — filtrage Cowork ci-dessous (§3) propose **15 Tier 1 (zones évidentes)** + **11 Tier 2 (ambigus, arbitrage Soleil)** + **5 Tier 3 (à laisser pins)**.

**Limites outillage :**
- WebFetch/WebSearch non utilisable (provenance set). Codes INPN précis non re-vérifiés en ligne pour cet audit. Cowork donne des références plausibles à confirmer.
- Pas de download géométries en Phase A (conforme brief : Phase A read-only inventaire).

---

## 1. Inventaire complet des candidats B-ZONES

### 1.1 Tableau principal (31 candidats)

Colonnes : `slug`, `name`, `lat/lon`, `commune`, `pieve`, `axe`, `surface estimée`, `tier proposé`, `source géom`.

| slug | name | lat | lon | commune | pieve | axe | Surface ~ | Tier | Source |
|------|------|-----|-----|---------|-------|-----|------------|------|--------|
| **reserve_de_scandola** | Réserve de Scandola | 42.3589 | 8.5615 | Osani | pieve_vico | naturel_sacre | ~20 km² (terre + marin) | **T1** | INPN FR3600158 (Réserve naturelle nationale) + UNESCO Golfe de Porto |
| **desert_des_agriate** | Désert des Agriate | 42.6800 | 9.1000 | (multi-commune) | pieve_nebbiu | naturel_sacre | ~150 km² | **T1** | Conservatoire du Littoral (Site classé) |
| **calanques_de_piana** | Calanques de Piana | 42.2529 | 8.6575 | Piana | pieve_vico | naturel_sacre | ~17 km² | **T1** | UNESCO 2008 (Golfe de Porto) + INPN FR3600159 ou similaire |
| **aiguilles_de_bavella** | Aiguilles de Bavella | 41.7998 | 9.2148 | (multi-commune) | pieve_verde | naturel_sacre | ~10 km² (massif pics) | **T1** | OSM relation possible + INPN ZNIEFF |
| **vizzavona** | Forêt de Vizzavona | 42.1331 | 9.1283 | Vivario | pieve_vivario | naturel_sacre | ~16 km² (forêt domaniale) | **T1** | ONF (Forêt domaniale) + OSM tag |
| **foret_de_tartagine** | Forêt de Tartagine | 42.4750 | 8.9600 | Mausoléo | pieve_balagne | remarquables_geo | ~30 km² | **T1** | ONF (Forêt domaniale) |
| **foret_de_valdu_niellu** | Forêt de Valdu Niellu | 42.2820 | 8.9330 | Albertacce | pieve_niolu | remarquables_geo | ~46 km² (plus grande forêt Corse) | **T1** | ONF (Forêt domaniale) |
| **cirque_de_bonifato** | Cirque de Bonifato | 42.4700 | 8.8600 | Calenzana | pieve_balagne | remarquables_geo | ~5 km² | **T1** | OSM + ONF (englobe forêt domaniale) |
| **gorges_du_spelunca** | Gorges du Spelunca | 42.2470 | 8.7320 | None (cheval Ota/Évisa) | pieve_vico | naturel_sacre | ~3 km² (ligne 8 km × 200-400m) | **T1** | OSM relation + tracé manuel |
| **gorges_du_tavignano** | Gorges du Tavignano | 42.3010 | 9.1540 | Corte | pieve_talcini | naturel_sacre | ~5 km² (ligne 12 km) | **T1** | OSM relation + tracé manuel |
| **gorges_de_l_inzecca** | Gorges de l'Inzecca | 42.0978 | 9.2256 | Ghisoni | pieve_ghisoni | remarquables_geo | ~2 km² | **T1** | OSM + tracé manuel |
| **defile_de_lancone** | Défilé de Lancône | 42.5950 | 9.3950 | None | pieve_nebbiu | patrimoine_bati | ~3 km² (ligne) | **T1** | OSM + tracé manuel |
| **massif_du_haut_asco** | Massif du Haut-Asco | 42.4035 | 8.9223 | Asco | pieve_mariana | remarquables_geo | ~40 km² (vallée Asco amont) | **T1** | OSM + tracé manuel |
| **massif_de_l_ospedale** | Massif de l'Ospedale | 41.7000 | 9.2100 | Zonza | pieve_verde | remarquables_geo | ~30 km² | **T1** | ONF (forêt) + tracé manuel |
| **plateau_du_coscione** | Plateau du Coscione | 41.8300 | 9.1000 | None | pieve_tallano | remarquables_geo | ~20 km² | **T1** | OSM tag + tracé manuel |
| **monte_cinto** | Monte Cinto | 42.3797 | 8.9458 | Monte | pieve_mariana | naturel_sacre | ~25 km² (massif) ou point (sommet) | **T2** | OSM massif vs point |
| **monte_san_petrone** | Monte San Petrone | 42.3961 | 9.3269 | Monte | pieve_orezza | naturel_sacre | ~10 km² ou point | **T2** | OSM massif vs point |
| **monte_stello** | Monte Stello | 42.7886 | 9.4181 | Olcani | pieve_nonza | naturel_sacre | ~8 km² (crête Cap) ou point | **T2** | OSM vs point |
| **monte_d_oro** | Monte d'Oro | 42.1372 | 9.0986 | Monte | pieve_vivario | remarquables_geo | ~10 km² ou point | **T2** | OSM vs point |
| **monte_renoso** | Monte Renoso | 42.0594 | 9.1339 | Monte | pieve_ghisoni | remarquables_geo | ~12 km² ou point | **T2** | OSM vs point |
| **monte_genova** | Monte Genova | 42.6883 | 9.1957 | (secteur Agriate) | pieve_nebbiu | remarquables_geo | ~2 km² (sommet Agriates) | **T2** | Sous-zone Agriate ou point |
| **monte_revincu** | Monte-Revincu | 42.6690 | 9.2585 | Santo-Pietro-di-Tenda | pieve_nebbiu | remarquables_geo | ~2 km² | **T2** | Sous-zone Agriate ou point |
| **capu_rossu** | Capu Rossu | 42.2250 | 8.5730 | Piana | pieve_vico | remarquables_geo | ~5 km² (promontoire 331m) | **T2** | OSM tag + tracé manuel |
| **cap_corse_extreme_nord** | Capu Bianchi | 43.0050 | 9.3950 | None | None | naturel_sacre | ~3 km² (pointe Barcaggio) | **T2** | OSM tag + tracé manuel |
| **anneaux_du_cap_corse** | Anneaux du Cap Corse | 43.1765 | 9.6001 | Centuri | pieve_rogliano | remarquables_geo | sous-marin ~120m | **T2** | Cas spécial — zone marine non visible carte standard |
| **grotte_de_bonifacio** | Grotte de Bonifacio | 41.3884 | 9.1430 | Bonifacio | pieve_bonifacio | remarquables_geo | grotte = point | **T3** | Laisser pin (grotte ponctuelle, falaises voisines hors scope) |
| **piscia_di_gallo** | Piscia di Gallo | 41.6806 | 9.2160 | Zonza | pieve_carbini | remarquables_geo | cascade = ligne | **T3** | Laisser pin (cascade quasi-point) |
| **lac_de_creno** | Lac de Creno | 42.2048 | 8.9459 | Orto | pieve_sorroinsu | naturel_sacre | ~0.05 km² (petit lac) | **T3** | Laisser pin |
| **lac_de_nino** | Lac de Nino | 42.2556 | 8.9403 | Albertacce | pieve_talcini | naturel_sacre | ~0.4 km² (lac + pozzines) | **T2** | Polygone manuel petit (lac + pozzines sacrées autour) |
| **lac_de_tolla** | Lac de Tolla | 41.9683 | 8.9772 | Tolla | pieve_ornano | remarquables_geo | ~1 km² (retenue artificielle) | **T3** | Laisser pin (compact, peu d'intérêt zone) |
| **ile_rousse_pietra** | Île Rousse / Pietra | 42.6428 | 8.9362 | L'Île-Rousse | None | remarquables_geo | îlot ~0.1 km² | **T3** | Laisser pin |

**Total :** 15 T1 (zones évidentes) + 11 T2 (cas ambigus) + 5 T3 (à laisser pins).

### 1.2 Décompte par tier

- **Tier 1 — Zones évidentes (15 sites)** : à transformer en polygones systématiquement. Surface ≥ 2 km², caractère « étendu » clair.
- **Tier 2 — Cas ambigus (11 sites)** : à arbitrer par Soleil. Soit zone (avec polygone), soit point (laisser pin). Argumentaire au §3.
- **Tier 3 — À laisser pins (5 sites)** : objets ponctuels (grotte, cascade, îlot, petits lacs, retenue compacte).

---

## 2. Catégorisation par type

### 2.1 Réserves naturelles officielles (INPN dispo) — 3 sites

- `reserve_de_scandola` — **Réserve Naturelle Nationale créée 1975, UNESCO 1983.** Géométrie INPN officielle disponible (~20 km² terrestre + marin).
- `desert_des_agriate` — **Site classé Conservatoire du Littoral**, ~150 km². Périmètre officiel à confirmer (probablement parcelles foncières du Conservatoire).
- `calanques_de_piana` — **UNESCO 2008** (composante Golfe de Porto), Site classé Mérimée. ~17 km².

### 2.2 Forêts domaniales (ONF) — 4 sites

- `vizzavona` — Forêt domaniale ONF, ~16 km², pins laricio.
- `foret_de_tartagine` — Forêt domaniale ONF Balagne, ~30 km².
- `foret_de_valdu_niellu` — Forêt domaniale ONF Niolu, plus grande de Corse ~46 km².
- `cirque_de_bonifato` — Englobe forêt domaniale Calenzana, ~5 km².

### 2.3 Massifs montagneux — 7 sites (1 T1, 6 T2)

- `aiguilles_de_bavella` (T1, pics granitiques distinctifs)
- `monte_cinto` / `monte_san_petrone` / `monte_stello` / `monte_d_oro` / `monte_renoso` / `massif_du_haut_asco` / `massif_de_l_ospedale` (5 T2 + 2 T1)

### 2.4 Gorges / défilés — 4 sites

- `gorges_du_spelunca` (T1)
- `gorges_du_tavignano` (T1)
- `gorges_de_l_inzecca` (T1)
- `defile_de_lancone` (T1)

### 2.5 Zones côtières / promontoires — 4 sites

- `capu_rossu` (T2 — promontoire 331m)
- `cap_corse_extreme_nord` (T2 — pointe Barcaggio)
- `anneaux_du_cap_corse` (T2 — sous-marin)
- `grotte_de_bonifacio` (T3 — grotte point)
- `ile_rousse_pietra` (T3 — îlot petit)

### 2.6 Plateaux + lacs — 4 sites

- `plateau_du_coscione` (T1)
- `lac_de_creno` (T3 — petit lac)
- `lac_de_nino` (T2 — lac + pozzines)
- `lac_de_tolla` (T3 — retenue)

### 2.7 Cascades / curiosités ponctuelles — 1 site

- `piscia_di_gallo` (T3 — cascade 90m, point essentiel)

### 2.8 Sous-zones des Agriates — 2 sites

- `monte_genova` (T2 — sommet 421m dans Agriates)
- `monte_revincu` (T2 — sommet 359m dans Agriates)

⚠️ **Cas particulier :** ces 2 sommets sont **géographiquement dans** le polygone `desert_des_agriate`. Si Soleil active les polygones Agriates + monte_genova + monte_revincu en T1/T2, les 3 zones se superposeront. Décision UX : (a) garder les 3 polygones empilés (z-index hiérarchique), (b) ne polygoner que Agriates et garder les sommets en pins, (c) ne polygoner que les sommets et garder Agriates en pin.

---

## 3. Sources géométriques proposées par candidat

### 3.1 Sources INPN (3 sites)

| Site | Code INPN candidat | Confiance | Note |
|------|---------------------|-----------|------|
| reserve_de_scandola | FR3600158 (RNN Scandola) | Haute — réserve nationale officielle | À confirmer Code via API INPN ou geojson INPN |
| desert_des_agriate | Site classé Agriates / Conservatoire du Littoral | Moyenne | Géométrie via Conservatoire du Littoral, pas forcément INPN |
| calanques_de_piana | UNESCO Golfe de Porto + INPN ZNIEFF type II ou Site classé | Moyenne | À recouper avec UNESCO geojson (whc.unesco.org) |

### 3.2 Sources OSM relations (estimées)

| Site | Source OSM probable | Note |
|------|----------------------|------|
| vizzavona | `natural=wood` + `name=Forêt de Vizzavona` | OSM tag bbox |
| foret_de_tartagine | OSM relation forêt | À identifier ID |
| foret_de_valdu_niellu | OSM relation forêt + Parc Naturel Régional de Corse | Englobé dans PNRC |
| massif_du_haut_asco | OSM relation vallée Asco | À identifier |
| aiguilles_de_bavella | OSM tag `natural=peak` regroupés ou ZNIEFF | À tracer manuellement bbox des pics |
| gorges_du_spelunca | OSM `waterway` + vallée | Tracé manuel le long de l'axe |
| gorges_du_tavignano | OSM `waterway` Tavignano | Tracé manuel bbox |
| gorges_de_l_inzecca | OSM tag défilé | Tracé manuel |
| defile_de_lancone | OSM tag défilé | Tracé manuel |
| cirque_de_bonifato | OSM relation cirque ou forêt | OSM tag ou ONF |
| plateau_du_coscione | OSM relation plateau | OSM tag ou ZNIEFF |

### 3.3 Tracé manuel (polygones simplifiés 4-8 points)

Pour les sites sans source officielle ou OSM identifiable, **tracé manuel à partir de l'IGN topo / OSM visualisation** :

- Tous les sommets (T2) : si Soleil arbitre OUI massif, tracer un polygone autour de la crête principale (5-8 points selon orographie)
- `capu_rossu` : pointe ouest Piana, 4-5 points
- `cap_corse_extreme_nord` (Capu Bianchi) : pointe Barcaggio, 4-5 points
- `lac_de_nino` (T2) : bordure lac + pozzines, 6-8 points

### 3.4 Cas spéciaux

- `anneaux_du_cap_corse` : sous-marin ~120m profondeur. **Géométrie peu pertinente carte standard.** Recommandation Cowork : laisser pin avec popup explicatif (zone sous-marine non visible).
- Sites T3 : pas de géométrie. Restent pins.

---

## 4. Schéma de données proposé

### 4.1 Extension `sites_patrimoine.json` — proposition

Pour chaque site B-ZONE, ajouter un ou plusieurs des champs suivants :

```json
{
  "slug": "reserve_de_scandola",
  "name": "Réserve de Scandola",
  "lat": 42.3589,
  "lon": 8.5615,
  "...autres champs existants...": "...",
  
  "is_zone": true,
  "zone_geometry": {
    "type": "Polygon",
    "coordinates": [[
      [8.5500, 42.3500],
      [8.5700, 42.3500],
      [8.5700, 42.3700],
      [8.5500, 42.3700],
      [8.5500, 42.3500]
    ]]
  },
  "zone_source": "INPN FR3600158",
  "zone_simplification_pts": 4
}
```

Ou alternative avec ID INPN à résoudre côté front :

```json
{
  "is_zone": true,
  "inpn_id": "FR3600158",
  "zone_geometry_url": "https://inpn.mnhn.fr/api/.../FR3600158.geojson"
}
```

### 4.2 Recommandation Cowork — schéma combiné

**Pour les T1 INPN :** inclure `zone_geometry` inline (autonome, pas dépendant fetch externe), avec `zone_source` documentant la provenance (INPN code ou OSM relation).

**Pour les T1/T2 manuels :** inclure `zone_geometry` directement, `zone_source="manuel tellux 2026-05-18"`.

**Champ `is_zone: true`** : flag explicite pour distinguer dans le code de rendu. Permet le filtrage `sites_patrimoine.json` côté `patrimoine.html`.

**Conserver `lat`/`lon`** : centre du pin permanent. Pas changé.

**Convention coords :** `[lon, lat]` ordre GeoJSON standard (pas `[lat, lon]` comme les polygones pieves/doyennés du repo qui utilisent `[lat, lon]`). À aligner avec une convention claire dans le brief Code.

### 4.3 Validation schema

Préférer **vérification à l'import** : pour chaque `is_zone: true`, le polygone doit être présent et avoir ≥ 4 points (3 + closure). Sinon erreur de chargement claire dans la console.

---

## 5. Plan interaction patrimoine.html

### 5.1 Modèle d'interaction

**Pin permanent + polygone au hover** (brief Soleil Axe 2) :

```javascript
// Pseudocode Leaflet
const marker = L.marker([site.lat, site.lon], {...}); // pin permanent
let zonePolygon = null;

marker.on('mouseover', function() {
  if (!site.is_zone || !site.zone_geometry) return;
  if (zonePolygon) return; // déjà affiché
  
  const latLngs = site.zone_geometry.coordinates[0].map(c => [c[1], c[0]]);
  zonePolygon = L.polygon(latLngs, {
    color: '#C28533',          // ocre DA v2
    weight: 2,
    opacity: 0.8,
    fillColor: '#C28533',
    fillOpacity: 0.3,          // léger remplissage
    className: 'tlx-zone-hover',
    interactive: false         // pas de re-click sur polygone (le pin garde focus)
  }).addTo(map);
});

marker.on('mouseout', function() {
  if (zonePolygon) {
    map.removeLayer(zonePolygon);
    zonePolygon = null;
  }
});
```

### 5.2 Animation fade in/out

CSS :
```css
.leaflet-overlay-pane .tlx-zone-hover {
  transition: opacity 200ms ease-out;
}
```

### 5.3 Comportement N1 / N2 / N3

Le hover-polygone est **actif à tous les niveaux de zoom** (N1, N2, N3) car le pin permanent l'est aussi. Pas de filtre par niveau.

### 5.4 Précédence pin vs polygone

- Le pin **garde le clic** (ouvre le popup site comme aujourd'hui)
- Le polygone est `interactive: false` (Leaflet) → pas de capture clic, juste visuel
- Z-index : pin > polygone (pin reste cliquable même si polygone affiché)

### 5.5 Tap mobile

Sur mobile (pas de hover), le polygone s'affiche au **premier tap** (avant l'ouverture du popup). Le **second tap** sur le pin déclenche le popup.

Implémentation possible : sur `click` du pin, afficher le polygone pendant 1.5s avec fade-out, puis ouvrir le popup. À ajuster en preview.

### 5.6 Cas multi-zones empilées (Agriates + monte_genova + monte_revincu)

Si Soleil active polygones pour les 3, le hover sur le pin sommet (genova/revincu) affiche **uniquement le polygone du sommet** (pas Agriates). Pour Agriates → hover sur pin Agriates. Pas de propagation hiérarchique. Si une zone est entièrement contenue dans une autre, c'est visuellement OK (l'utilisateur voit "le sommet est dans le désert").

---

## 6. Estimation effort Code Phase B

### 6.1 Création géométries

| Type | n sites | Effort par site | Sous-total |
|------|---------|-----------------|------------|
| **INPN** (Scandola, Agriates, Calanques) | 3 | 30-45 min (téléchargement geojson + simplification 4-8 points) | 1h30-2h15 |
| **OSM relation** (forêts, gorges, plateau) | 6-8 | 20-30 min (identifier relation, extraire bbox, simplifier) | 2h00-4h00 |
| **Manuel** (sommets si arbitrés, capes, défilés) | 4-15 | 10-15 min (tracé sur IGN/OSM, 4-8 points) | 1h00-3h45 |

**Sous-total géométries : 4h30-10h** selon scope final.

### 6.2 Intégration `sites_patrimoine.json`

| Tâche | Effort |
|-------|--------|
| Ajout champs `is_zone`, `zone_geometry`, `zone_source` aux ~15-25 sites | 30 min |
| Validation JSON + tests | 15 min |

### 6.3 Refactor `patrimoine.html`

| Tâche | Effort |
|-------|--------|
| Logique hover (mouseover/mouseout) + render Leaflet polygon | 30-45 min |
| CSS fade in/out | 15 min |
| Handler mobile tap (1.5s show + popup) | 30 min |
| Précédence z-index pin > polygone | 15 min |
| Tests preview Cloudflare | 30 min |

**Sous-total patrimoine.html : ~2h30.**

### 6.4 Documentation + commit

| Tâche | Effort |
|-------|--------|
| Suivi interne mis à jour | 15 min |
| `CHANGELOG.md` | 10 min |
| Commit(s) atomiques + push + PR | 15 min |

### 6.5 Total estimé Phase B Code

| Scope | Total |
|-------|-------|
| **Scope minimal (T1 seul = 15 sites)** | ~8-10h |
| **Scope étendu (T1 + T2 favorables = ~22 sites)** | ~12-15h |
| **Scope maximal (T1 + tous T2 = 26 sites)** | ~16-18h |

Probablement **2 jours de Code** pour le scope étendu.

---

## 7. Questions à arbitrer par Soleil

### 7.1 Scope final — Tier 2 cas ambigus

Pour chaque site T2, OUI/NON inclusion en polygone :

| Site | OUI polygone | NON pin garder |
|------|--------------|-----------------|
| monte_cinto | ? massif | ? pic |
| monte_san_petrone | ? massif | ? pic |
| monte_stello | ? crête | ? pic |
| monte_d_oro | ? massif | ? pic |
| monte_renoso | ? massif | ? pic |
| monte_genova | ? sous-zone Agriate | ? pin |
| monte_revincu | ? sous-zone Agriate | ? pin |
| capu_rossu | OUI promontoire (Cowork recommandé) | NON |
| cap_corse_extreme_nord | OUI pointe (Cowork recommandé) | NON |
| anneaux_du_cap_corse | NON (sous-marin) (Cowork recommandé) | OUI laisser pin |
| lac_de_nino | OUI lac + pozzines (Cowork recommandé) | NON |

### 7.2 Schéma data

- `is_zone` + `zone_geometry` inline (Cowork recommandé) **VS** `inpn_id` + fetch dynamique externe ?
- Convention `[lon, lat]` (GeoJSON standard) ou `[lat, lon]` (cohérence pieves_polygons.json) ?

### 7.3 Interaction patrimoine.html

- Comportement mobile tap (1.5s show + popup, Cowork recommandé) — OUI/NON ?
- Couleur polygone : `--tx-ocre` `#C28533` (Cowork recommandé) ou autre couleur DA ?
- fillOpacity 0.3 (Cowork recommandé) — OK ou plus/moins ?

### 7.4 Sources géométriques

- Téléchargement INPN officiel (Scandola, Calanques) **VS** tracé manuel simplifié (cohérence avec autres) ?
- OSM relations utilisables (vérifier ID) **VS** tracé manuel partout ?

### 7.5 Cas multi-zones empilées (Agriates + sommets sous-zones)

- Polygones empilés (Cowork recommandé) **VS** choisir un seul niveau ?

### 7.6 Effort time-box

- 2 jours Code OK pour scope étendu, ou phaser en 2 PRs (T1 d'abord, T2 ensuite) ?

### 7.7 Sites manqués

- Cowork a inventorié 31 candidats sur la base axe_corpus + keywords. Y a-t-il des **zones absentes du scan** que Soleil veut inclure ? Exemples potentiels :
  - **Étang de Diane** (lagune Plaine Orientale, ~600 ha) — n'apparaît pas dans sites_patrimoine.json (à vérifier)
  - **Étang d'Urbino** (lagune Plaine Orientale) — idem
  - **Étang de Biguglia** (réserve naturelle régionale) — idem
  - **Parc Naturel Régional de Corse** (couvre ~40 % de l'île) — sans doute trop large
  - **Sentier littoral du Cap Corse** — ligne, pas zone

⚠️ Si Soleil veut inclure étangs, Cowork peut faire un second scan sur mots-clés « étang / lagune / marais ». Aucun match dans le scan initial — ces entités ne sont probablement pas dans le corpus actuel, à confirmer.

---

## 8. Risques / dettes identifiés

| Risque | Sévérité | Mitigation |
|--------|----------|------------|
| Sandbox stale (sites_patrimoine.json mtime 2026-05-15) | Faible | Les sites zones n'ont pas évolué Phase 1/2. Audit valide. |
| Géométries INPN non vérifiées en temps réel (provenance restriction WebFetch) | Moyenne | Code à confirmer en Phase A — ouvrir les URLs INPN candidates |
| Performance Leaflet avec 15-25 polygones hover (au pire 25 layers actifs) | Faible | `interactive: false` + add/remove on demand. ~25 polygones de 4-8 points = ~200 vertices total max = negligible |
| Conflit visuel polygones empilés (Agriates + sommets) | Faible | Z-index ordering + opacity faible. Acceptable visuel |
| Z-index pin vs polygone vs pieves vs doyennés | Moyenne | À tester en preview. Convention Leaflet : `pane` séparé `tlx-zone-hover` < `markerPane` |
| Cassure UX mobile (pas de hover) | Moyenne | Tap-first behavior à valider preview |
| Sites zones avec `pieve_slug=None` (cap_corse_extreme_nord, plateau_du_coscione, etc.) | Faible | Hors scope B-ZONES — c'est une dette `PATRIMOINE-ORPHANS-INVISIBLES-001` distincte |
| Lacs lac_de_creno / lac_de_tolla / petits étangs : doivent-ils basculer en T2 ? | Faible | Arbitrage Soleil §7.1 |
| Convention coords `[lat,lon]` (pieves) vs `[lon,lat]` (GeoJSON standard B-ZONES) — risque erreur Code | Élevée | À documenter explicitement dans le brief Code. Sinon Code peut intervertir et tracer en mer Tyrrhénienne |

---

## 9. Synthèse Cowork

**Inventoriés : 31 sites candidats B-ZONES.**

**Recommandé Cowork :**
- **15 T1 sites zones évidents** (forêts, gorges, désert, Scandola, Calanques, Bavella, Spelunca, Coscione, etc.) → polygones obligatoires.
- **11 T2 cas ambigus** → arbitrage Soleil §7.1.
- **5 T3 sites ponctuels** (grotte Bonifacio, lac_de_creno/tolla, piscia_di_gallo, ile_rousse_pietra) → laisser pins.

**Scope final probable :** **15-22 polygones** (T1 + T2 favorables), cohérent avec brief Soleil « ~15-25 sites ».

**Effort Code estimé :** 8-15h selon scope, 1-2 jours.

**Risque principal à surveiller :** convention coords [lat,lon] vs [lon,lat] (différence avec pieves_polygons.json) → bien documenter dans le brief Code.

---

## 10. Annexes — données extraites (sandbox)

Dans `/sessions/.../outputs/audit_zones/` (à créer si exploitation aval) :
- inventory complet 31 sites avec axe / cat / desc / lat / lon — déjà extrait dans cette session

---

_Généré le 2026-05-18 par Cowork, sandbox. Audit read-only conforme aux règles strictes du brief. À transmettre à Soleil pour arbitrage des questions §7, puis rédaction du brief Code pour Phase B exécution._
