# BRIEF CODE — B-ZONES Étape 4 sprint pré-FEDER (PR A + PR B)

**Type :** Brief autonome pour exécution Claude Code (transformation de 23 sites Tellux en zones polygonales interactives avec hover, en 2 PRs phasées séquentielles).
**Date :** 2026-05-18.
**Référence amont :** `docs/operations/B_ZONES_AUDIT_2026-05-18.md` (audit programmatique 31 candidats → 23 retenus).
**Branches cibles :**
- PR A : `feat/b-zones-tier1-15-sites`
- PR B : `feat/b-zones-tier2-8-sites` (après merge PR A en main + validation preview)

---

## 0. Arbitrages Soleil intégrés (2026-05-18)

| Q | Décision |
|---|----------|
| Tier 2 inclusion | 5 monts (Cinto/San Petrone/Stello/d'Oro/Renoso) en ZONE + Capu Rossu/Bianchi en ZONE + Lac de Nino en ZONE = **8 sites T2 favorables**. Monte Genova/Revincu en PIN (sous-zones Agriates redondantes), Anneaux Cap en PIN (sous-marin). |
| Schéma data | **Tout inline** dans `zone_geometry`. Pas de fetch externe runtime. INPN/UNESCO téléchargés une fois, simplifiés, inline. |
| Convention coords | **GeoJSON standard `[lon, lat]`** pour `zone_geometry.coordinates` — **à documenter en gras dans le JSON et dans tous les commentaires Code**. |
| Mobile tap | 1.5 s polygone show puis ouverture popup. |
| Couleur | Ocre `#C28533` (`--tx-ocre`), `fillOpacity: 0.3`, `stroke opacity: 0.8`. |
| INPN | Téléchargement officiel, simplification ~50-100 points, inline. Source documentée dans `zone_source`. |
| Multi-zones | Pas d'empilement : hover sur pin affiche le polygone du **site survolé uniquement**. |
| PR phasing | **2 PRs séquentielles strictes** : PR A merge dev → preview validée Soleil → merge main → PUIS PR B démarre. |
| Tracé manuel | **Overpass API first** (récupérer relations OSM existantes), fallback geojson.io tracé manuel uniquement si pas de relation OSM exploitable. |
| Étangs Diane/Urbino/Biguglia | Vérification Phase A — si présents dans `sites_patrimoine.json`, inclure en T1. Si absents, note pour Phase 2 corpus, hors scope ce brief. |

---

## 1. Compteurs avant / après

| Indicateur | Avant | Après PR A | Après PR B (final) |
|------------|-------|-------------|----------------------|
| Sites avec `is_zone: true` | 0 | 15 (T1) | **23** (T1 + T2 favorables) |
| Sites avec `zone_geometry` | 0 | 15 | 23 |
| Sites restant en pins seuls | 541 | 526 | 518 (+5 T3 + 3 T2 défavorables = 528 inchangés UI) |
| Aliases | 3 ou 5 selon Phase 2 état | inchangé | inchangé |
| Polygones Leaflet rendus | 0 | 15 (au hover) | 23 |
| Volume `sites_patrimoine.json` | ~550 KB | +5-10 KB | +5-10 KB (total ~560-570 KB) |

---

## 2. Plan de scope — détail site par site

### 2.1 Tier 1 — 15 sites (PR A)

| slug | name | Source géom prio 1 | Source fallback |
|------|------|---------------------|------------------|
| `reserve_de_scandola` | Réserve de Scandola | INPN RNN (code à confirmer `FR3600158` ou via API) | UNESCO Golfe de Porto |
| `desert_des_agriate` | Désert des Agriate | Conservatoire du Littoral (geojson OpenData) | OSM `natural=heath` + `name=*Agriate*` |
| `calanques_de_piana` | Calanques de Piana | UNESCO Golfe de Porto (whc.unesco.org) | INPN ZNIEFF |
| `aiguilles_de_bavella` | Aiguilles de Bavella | Overpass `natural=ridge` ou `natural=peak` cluster | Tracé manuel 6-8 points bbox des pics |
| `vizzavona` | Forêt de Vizzavona | Overpass `name=Forêt domaniale de Vizzavona` `landuse=forest` | OSM tag bbox |
| `foret_de_tartagine` | Forêt de Tartagine | Overpass `name=Forêt domaniale de Tartagine` | OSM tag bbox |
| `foret_de_valdu_niellu` | Forêt de Valdu Niellu | Overpass `name=*Valdu*Niellu*` | ONF Niolu / OSM |
| `cirque_de_bonifato` | Cirque de Bonifato | Overpass `natural=cirque` ou `name=Bonifato` | OSM tag bbox |
| `gorges_du_spelunca` | Gorges du Spelunca | Overpass `name=Spelunca` `natural=gorge` | Tracé manuel le long Porto entre Ota-Évisa |
| `gorges_du_tavignano` | Gorges du Tavignano | Overpass `name=*Tavignano*` `natural=gorge` | Tracé manuel depuis Corte 12 km amont |
| `gorges_de_l_inzecca` | Gorges de l'Inzecca | Overpass `name=Inzecca` | Tracé manuel défilé Fium'Orbu |
| `defile_de_lancone` | Défilé de Lancône | Overpass `name=Lancône` ou `name=Lancone` | Tracé manuel 4-5 points |
| `massif_du_haut_asco` | Massif du Haut-Asco | Overpass relation `name=Asco` `boundary=*` | Tracé manuel vallée Asco amont |
| `massif_de_l_ospedale` | Massif de l'Ospedale | Overpass `name=Ospedale` `landuse=forest` ou ZNIEFF | Tracé manuel bbox |
| `plateau_du_coscione` | Plateau du Coscione | Overpass `name=Coscione` `natural=plateau` ou ZNIEFF | Tracé manuel bbox |

### 2.2 Tier 2 favorables — 8 sites (PR B)

| slug | name | Source géom prio 1 | Source fallback |
|------|------|---------------------|------------------|
| `monte_cinto` | Monte Cinto | Overpass `natural=peak` + tracé manuel rayon ~3 km autour sommet | Tracé manuel 5-6 points |
| `monte_san_petrone` | Monte San Petrone | Overpass `natural=peak` + tracé manuel rayon ~2 km | Tracé manuel 5-6 points |
| `monte_stello` | Monte Stello | Overpass + tracé manuel crête Cap Corse | Tracé manuel 5-6 points |
| `monte_d_oro` | Monte d'Oro | Overpass + tracé manuel rayon ~2 km | Tracé manuel 5-6 points |
| `monte_renoso` | Monte Renoso | Overpass + tracé manuel rayon ~2 km | Tracé manuel 5-6 points |
| `capu_rossu` | Capu Rossu | Overpass `natural=cape` ou `natural=peninsula` | Tracé manuel 4-5 points pointe |
| `cap_corse_extreme_nord` | Capu Bianchi | Overpass + tracé manuel pointe Barcaggio | Tracé manuel 4-5 points |
| `lac_de_nino` | Lac de Nino | Overpass `natural=water` Nino + extension pozzines | Tracé manuel 6-8 points lac + pozzines |

### 2.3 Tier 2 défavorables — 3 sites (PINS, hors scope)

- `monte_genova` (sommet 421m Agriates — pin dedans le polygone Agriates)
- `monte_revincu` (sommet 359m Agriates — idem)
- `anneaux_du_cap_corse` (sous-marin, non représentable carte standard)

**Aucune modification** sur ces 3 sites — restent pins avec popup actuel. Pas de `is_zone: true`.

### 2.4 Tier 3 — 5 sites (PINS, hors scope)

`grotte_de_bonifacio`, `piscia_di_gallo`, `lac_de_creno`, `lac_de_tolla`, `ile_rousse_pietra`. **Aucune modification.**

---

## 3. Phase A — Read-only Code (~45 min)

### 3.1 État repo

```bash
cd <tellux>
git fetch && git status                         # working tree clean attendu
git checkout dev && git pull
git checkout -b feat/b-zones-tier1-15-sites
```

### 3.2 Vérifs préalables (read-only)

#### 3.2.1 Vérifier présence des 23 sites + lecture états actuels

Script Python à run :

```python
import json
with open('docs/data/sites_patrimoine.json') as f:
    data = f.read()
sites = json.JSONDecoder().raw_decode(data)[0]['sites']

T1 = ['reserve_de_scandola','desert_des_agriate','calanques_de_piana','aiguilles_de_bavella',
      'vizzavona','foret_de_tartagine','foret_de_valdu_niellu','cirque_de_bonifato',
      'gorges_du_spelunca','gorges_du_tavignano','gorges_de_l_inzecca','defile_de_lancone',
      'massif_du_haut_asco','massif_de_l_ospedale','plateau_du_coscione']

T2_fav = ['monte_cinto','monte_san_petrone','monte_stello','monte_d_oro','monte_renoso',
          'capu_rossu','cap_corse_extreme_nord','lac_de_nino']

for slug in T1 + T2_fav:
    site = next((s for s in sites if s['slug'] == slug), None)
    if site is None:
        print(f"❌ MISSING: {slug}")
    else:
        has_zone = 'is_zone' in site
        print(f"✓ {slug:32} lat={site.get('lat'):.4f} lon={site.get('lon'):.4f} has_zone={has_zone}")
```

Attendu : **23 sites présents**, aucun `is_zone` déjà défini. Si un site manque, STOP et remonter à Soleil.

#### 3.2.2 Vérifier étangs Diane / Urbino / Biguglia

```python
for kw in ['Diane', 'Urbino', 'Biguglia', 'étang', 'lagune', 'marais']:
    matches = [s for s in sites if kw.lower() in (s.get('name') or '').lower()]
    if matches:
        for s in matches:
            print(f"  {kw}: {s['slug']} → {s['name']} (axe={s.get('axe_corpus')})")
    else:
        print(f"  {kw}: 0 match")
```

**Si étangs trouvés (Diane/Urbino/Biguglia comme entités étendues, pas comme communes) :** ajouter en T1 avec source INPN potentielle (RNR Étang de Biguglia). Sinon : note pour Phase 2 corpus, hors scope.

**Décision Code :** si ≤2 étangs trouvés, les ajouter en T1 (scope deviendrait 17 + 8 = 25). Si ≥3, remonter à Soleil pour arbitrage.

#### 3.2.3 Vérifier intégrité JSON

```bash
python -c "import json; json.load(open('docs/data/sites_patrimoine.json'))"
```

⚠️ **Si le fichier est tronqué/corrompu** (pattern `OPS-COWORK-SANDBOX-GIT-DRIFT-001` ou file truncation), STOP et remonter avant de modifier.

#### 3.2.4 Vérifier `patrimoine.html` état actuel

```bash
grep -n "L.polygon\|markerPane\|tlx-zone" patrimoine.html | head -30
grep -n "ficheType === 'pieves'" patrimoine.html        # U1 actif ?
```

Attendu :
- U1 actif (cf. brief précédent FICHES_PIEVES) — `if (ficheType === 'pieves') return;` doit être présent dans `openFichePopup`.
- Pas de classe CSS `tlx-zone-hover` déjà définie (sera ajoutée Phase B).

#### 3.2.5 Identifier sources Overpass + URLs INPN candidates

**À faire avant Phase B** : pour chaque site T1 + T2, **lancer une requête Overpass test** pour confirmer disponibilité de la géométrie :

```bash
# Exemple pour Forêt de Vizzavona
curl -s "https://overpass-api.de/api/interpreter" -d 'data=[out:json];relation["name"~"Vizzavona"][type="multipolygon"](around:5000,42.13,9.13);out body;>;out skel;'

# Exemple pour Réserve de Scandola
curl -s "https://overpass-api.de/api/interpreter" -d 'data=[out:json];relation["name"~"Scandola"](around:5000,42.36,8.56);out body;>;out skel;'

# Réserves INPN — recherche par nom
curl -s "https://inpn.mnhn.fr/site/inpn/api/...recherche..." # À identifier l'API exacte
```

**Documenter dans un fichier `_drafts/B_ZONES_SOURCES_2026-05-18.json` à scratch (NON commit pour Phase A) :**

```json
{
  "reserve_de_scandola": {
    "primary_source": "INPN",
    "url": "https://inpn.mnhn.fr/.../FR3600158.geojson",
    "status": "to_download_phase_B",
    "expected_points": "~50-100 simplified",
    "fallback": "manual_5pts"
  },
  "vizzavona": {
    "primary_source": "Overpass",
    "relation_id": "1234567",
    "status": "confirmed",
    "expected_points": "~30 simplified",
    "fallback": "manual_8pts"
  },
  ...
}
```

### 3.3 POINT DE VALIDATION SOLEIL avant Phase B PR A

Remonter à Soleil dans le chat :

1. Confirmation des **15 sites T1 présents** dans `sites_patrimoine.json` (et 8 T2 si arbitré inclure PR B).
2. **Étangs Diane/Urbino/Biguglia** : présents oui/non/combien → décision inclure en T1 ou laisser hors scope.
3. **Sources Overpass / INPN identifiées** pour les 15 sites T1 : combien `confirmed`, combien `fallback_manual` ?
4. Confirmation `patrimoine.html` n'a pas déjà du code `is_zone` (sinon conflit potentiel).
5. **Code INPN exact** pour Scandola (`FR3600158` à confirmer) — si introuvable, fallback OSM ou manuel.

**Attendre confirmation explicite Soleil dans le chat avant Phase B.**

---

## 4. Phase B — Édition Code

### 4.1 PR A — Tier 1 (15 sites) — Effort estimé 8-10h

#### Commit 1 (PR A) : `feat(b-zones): schema is_zone + zone_geometry dans sites_patrimoine.json`

Modifier `sites_patrimoine.json` pour ajouter aux 15 sites T1 :

```jsonc
{
  "slug": "reserve_de_scandola",
  "name": "Réserve de Scandola",
  "lat": 42.3589,
  "lon": 8.5615,
  /* ...autres champs existants inchangés... */
  
  "is_zone": true,
  "zone_geometry": {
    "type": "Polygon",
    // ⚠ Convention coords GeoJSON standard : [lon, lat] (PAS [lat, lon] comme pieves_polygons.json)
    "coordinates": [[
      [8.5500, 42.3500],
      [8.5700, 42.3500],
      [8.5700, 42.3700],
      [8.5500, 42.3700],
      [8.5500, 42.3500]   // fermeture obligatoire
    ]]
  },
  "zone_source": "INPN FR3600158 (RNN Scandola, téléchargé 2026-05-18, simplifié 50 points)",
  "zone_simplification_pts": 50
}
```

**⚠️⚠️⚠️ CRITIQUE — Convention coords GeoJSON `[lon, lat]` :**

- **`zone_geometry.coordinates`** : ordre `[longitude, latitude]` (GeoJSON RFC 7946 standard)
- **`lat` / `lon`** du site (champs existants) : restent en flottants séparés
- **`pieves_polygons.json` et `doyennes_polygons.json`** : utilisent `[lat, lon]` (convention historique Tellux)
- Code DOIT s'assurer que `zone_geometry` est en `[lon, lat]` cohérent avec GeoJSON
- **Smoke test obligatoire** : pour chaque polygone, vérifier que le centroïde tombe en Corse (lat 41.3-43.2, lon 8.5-9.7). Si hors Corse, c'est probablement une inversion lat/lon. STOP.

```python
# Smoke test Phase B obligatoire
from shapely.geometry import shape, Point

CORSE_BBOX = (8.5, 41.3, 9.7, 43.2)  # lon_min, lat_min, lon_max, lat_max

for site in sites_with_zone:
    geom = shape(site['zone_geometry'])
    centroid = geom.centroid
    if not (CORSE_BBOX[0] <= centroid.x <= CORSE_BBOX[2] and
            CORSE_BBOX[1] <= centroid.y <= CORSE_BBOX[3]):
        print(f"❌ FAIL {site['slug']}: centroïde ({centroid.x},{centroid.y}) HORS CORSE")
        sys.exit(1)
    print(f"✓ {site['slug']} centroïde OK")
```

#### Commit 2 (PR A) : `feat(patrimoine): renderer Leaflet polygones zones au hover`

Modifier `patrimoine.html` pour ajouter la logique de rendu :

**HTML/JS — Ajout dans la section site rendering :**

```javascript
// ===== B-ZONES rendering (Étape 4 pré-FEDER) =====
// Pour chaque site avec is_zone: true, le marqueur permanent reste affiché.
// Au mouseover, un polygone Leaflet apparaît avec fade-in 200ms.
// Au mouseout, fade-out 200ms.
// Sur mobile (no hover), le tap affiche le polygone pendant 1500ms puis ouvre le popup.

const zoneRenderCache = new WeakMap();  // marker -> active polygon (or null)
const ZONE_FILL_COLOR = '#C28533';      // --tx-ocre DA v2
const ZONE_STROKE_COLOR = '#C28533';
const ZONE_FILL_OPACITY = 0.3;
const ZONE_STROKE_OPACITY = 0.8;
const ZONE_STROKE_WEIGHT = 2;
const ZONE_FADE_MS = 200;
const ZONE_MOBILE_SHOW_MS = 1500;

function renderZonePolygon(site) {
  if (!site.is_zone || !site.zone_geometry) return null;
  // ⚠ Convention coords : GeoJSON [lon, lat], Leaflet attend [lat, lon]
  // Inversion obligatoire ici
  const leafletCoords = site.zone_geometry.coordinates[0].map(c => [c[1], c[0]]);
  return L.polygon(leafletCoords, {
    color: ZONE_STROKE_COLOR,
    weight: ZONE_STROKE_WEIGHT,
    opacity: ZONE_STROKE_OPACITY,
    fillColor: ZONE_FILL_COLOR,
    fillOpacity: ZONE_FILL_OPACITY,
    className: 'tlx-zone-hover',
    interactive: false,   // pas de capture click, le pin garde le focus
    pane: 'overlayPane'   // sous markerPane → pin reste cliquable
  });
}

function attachZoneHandlers(marker, site) {
  if (!site.is_zone) return;
  
  // Desktop : hover
  marker.on('mouseover', function() {
    if (zoneRenderCache.get(marker)) return;
    const poly = renderZonePolygon(site);
    if (poly) {
      poly.addTo(map);
      zoneRenderCache.set(marker, poly);
    }
  });
  marker.on('mouseout', function() {
    const poly = zoneRenderCache.get(marker);
    if (poly) {
      map.removeLayer(poly);
      zoneRenderCache.set(marker, null);
    }
  });
  
  // Mobile : tap = show 1500ms then popup
  // Détection mobile via matchMedia
  const isMobile = window.matchMedia('(hover: none)').matches;
  if (isMobile) {
    marker.off('click');  // override default click handler temporairement
    marker.on('click', function(e) {
      const existing = zoneRenderCache.get(marker);
      if (existing) {
        // Second tap : ouvrir popup
        marker.openPopup();
        return;
      }
      const poly = renderZonePolygon(site);
      if (poly) {
        poly.addTo(map);
        zoneRenderCache.set(marker, poly);
        setTimeout(() => {
          map.removeLayer(poly);
          zoneRenderCache.set(marker, null);
          marker.openPopup();
        }, ZONE_MOBILE_SHOW_MS);
      } else {
        marker.openPopup();
      }
    });
  }
}

// Dans la boucle existante de création des markers de sites :
sites.forEach(site => {
  const marker = L.marker([site.lat, site.lon], {...}).addTo(spotsLayer);
  marker.bindPopup(buildSitePopupHtml(site));
  attachZoneHandlers(marker, site);  // <-- nouveau
});
```

**CSS — Ajout `.tlx-zone-hover` :**

```css
.leaflet-overlay-pane .tlx-zone-hover {
  transition: opacity 200ms ease-out;
}
```

#### Commit 3 (PR A) : `feat(b-zones): tier 1 — 15 polygones (INPN/UNESCO/OSM/manuel)`

**Pour chaque site T1, suivre la prioritisation §2.1 :**

1. **Lancer Overpass** (si source = Overpass) :
   ```bash
   # Exemple
   curl -s "https://overpass-api.de/api/interpreter" \
     -d 'data=[out:json];relation["name"~"Vizzavona"](around:5000,42.13,9.13);out geom;'
   ```
   Extraire geometry, convertir en GeoJSON `[lon, lat]`.

2. **Si INPN** : télécharger geojson, extraire bbox ou polygone simplifié.

3. **Si UNESCO Golfe de Porto** : utiliser composante geojson depuis whc.unesco.org/en/list/258 (Réserve naturelle de Scandola = composante).

4. **Simplifier à 50-100 points max** via :
   ```python
   from shapely.geometry import shape, mapping
   geom = shape(geojson_geom).simplify(tolerance=0.0005, preserve_topology=True)
   # tolerance 0.0005° ≈ 55m, cohérent avec build_pieves_polygons.py
   simplified = mapping(geom)
   ```

5. **Si fallback tracé manuel** : utiliser **geojson.io** pour tracer 4-8 points, exporter GeoJSON, intégrer.

6. **Vérifier en sortie** : 
   - 4-8 points pour les manuels, 30-100 pour les sourcés
   - Fermeture du polygone (premier point = dernier point)
   - **Smoke test PIP Corse bbox** (cf. §4.1 commit 1)
   - **Validation containment doyenne** (le polygone du site doit majoritairement tomber dans le doyenné `doyenne_contemporain_slug` du site)

**Documenter `zone_source` précis** pour chaque site (`"INPN FR3600158"`, `"OSM relation 12345"`, `"manuel tellux 2026-05-18 (geojson.io)"`).

#### Commit 4 (PR A) : `docs(dettes,changelog): B-ZONES Tier 1`

`DETTES_TECHNIQUES.md` — ajouter en début préambule, ouvrir :
- `PATRIMOINE-B-ZONES-TIER1-001` (closed at merge — 15 sites zones polygonales actives)
- `PATRIMOINE-B-ZONES-TIER2-FAVORABLE-001` (ouverte — 8 sites à traiter PR B)
- `PATRIMOINE-B-ZONES-T2-DEFAVORABLE-001` (ouverte basse priorité — 3 sites à laisser pin, documentation décision)
- `PATRIMOINE-B-ZONES-ETANGS-CORPUS-001` (si étangs Diane/Urbino/Biguglia identifiés absents en Phase A)

`CHANGELOG.md` — ajouter section :

```markdown
## [B-ZONES Tier 1 — 2026-05-18] (Étape 4 pré-FEDER)

### Added (sites_patrimoine.json)
- Champs `is_zone`, `zone_geometry` (GeoJSON `[lon, lat]`), `zone_source`, `zone_simplification_pts` sur 15 sites
- Polygones B-ZONES Tier 1 :
  - 3 réserves officielles : Scandola, Désert Agriates, Calanques de Piana (INPN/UNESCO/Cdl)
  - 4 forêts domaniales : Vizzavona, Tartagine, Valdu Niellu, Cirque de Bonifato (OSM)
  - 4 gorges/défilés : Spelunca, Tavignano, Inzecca, Lancône (OSM/manuel)
  - 1 massif pics : Aiguilles de Bavella (OSM)
  - 2 massifs : Haut-Asco, Ospedale (OSM/manuel)
  - 1 plateau : Coscione (OSM/manuel)

### Added (patrimoine.html)
- Renderer Leaflet polygones zones au hover (desktop) + tap 1500ms (mobile)
- CSS `.tlx-zone-hover` fade in/out 200ms
- Smoke test PIP Corse bbox automatique avant merge

### Reference
- Audit : `docs/operations/B_ZONES_AUDIT_2026-05-18.md`
- Brief Code : `docs/operations/B_ZONES_BRIEF_CODE_2026-05-18.md`
- Doctrine : ADR-001 (navigation pédagogique), BP-FIX-RATTACHEMENT-COMPLET-001
```

#### Push + PR A

```bash
git push origin feat/b-zones-tier1-15-sites
# Ouvrir PR feat → dev sur GitHub
```

### 4.2 PR B — Tier 2 favorables (8 sites) — DÉMARRAGE APRÈS PR A MAIN MERGÉE

⚠️ **Workflow séquentiel strict :**
1. PR A merge dev → preview Cloudflare → validation Soleil
2. PR A merge dev → main → déploiement prod confirmé
3. **PUIS et seulement PUIS** PR B démarre

```bash
cd <tellux>
git checkout dev && git pull
git checkout main && git pull && git checkout dev   # confirmer main = dev synchro post-PR A
git checkout -b feat/b-zones-tier2-8-sites
```

#### Commit 1 (PR B) : `feat(b-zones): tier 2 favorables — 5 monts + 2 promontoires + 1 lac`

Idem PR A commit 3, mais pour les 8 sites T2 favorables :

| slug | Stratégie | Note Code |
|------|-----------|-----------|
| `monte_cinto` | Overpass `natural=peak` Cinto + extension manuelle ~3 km autour | Vérifier inclusion lacs glaciaires associés |
| `monte_san_petrone` | Overpass + extension ~2 km | Castagniccia summit |
| `monte_stello` | Overpass + extension crête | Cap Corse summit |
| `monte_d_oro` | Overpass + extension | Vivario summit |
| `monte_renoso` | Overpass + extension | Ghisoni summit |
| `capu_rossu` | Overpass `natural=cape` ou tracé manuel pointe 4-5 points | Promontoire Piana 331m |
| `cap_corse_extreme_nord` | Tracé manuel pointe Barcaggio 4-5 points | Capu Bianchi |
| `lac_de_nino` | Overpass `natural=water` Nino + extension pozzines | Lac + pozzines sacrées (zone humide) |

**Smoke test PIP Corse bbox + validation containment doyenne idem PR A.**

#### Commit 2 (PR B) : `docs(dettes,changelog): B-ZONES Tier 2 favorables`

Fermer `PATRIMOINE-B-ZONES-TIER2-FAVORABLE-001` (résolue). Mettre à jour CHANGELOG section dédiée. Compteur total 23 polygones active.

#### Push + PR B

```bash
git push origin feat/b-zones-tier2-8-sites
```

---

## 5. Phase C — Vérifications preview Cloudflare (chaque PR)

### 5.1 Tests obligatoires PR A (15 sites)

| Test | Procédure | Attendu |
|------|-----------|---------|
| **Hover desktop** | Survol chaque pin Tier 1 (15 sites) | Polygone ocre apparaît avec fade in 200ms, disparaît au mouseout |
| **Tap mobile** | Sur smartphone, tap chaque pin Tier 1 | Polygone 1.5s puis popup. Second tap réouvre popup direct |
| **Click pin desktop** | Click sur pin pendant que polygone affiché | Popup s'ouvre normalement, polygone disparaît au mouseout |
| **Z-index** | Survol pin sur fond pieve coloré | Pin reste cliquable au-dessus du polygone zone |
| **Performance** | Survol rapide 5+ pins | Pas de lag, polygones add/remove fluide |
| **Console** | DevTools | Aucune erreur, aucun warning Leaflet |
| **Smoke test PIP** | Inspecter chaque polygone en Network/DOM | Centroïde dans bbox Corse (lat 41.3-43.2, lon 8.5-9.7) |
| **Coords convention** | Pour chaque site, vérifier `zone_geometry.coordinates[0][0]` | Premier élément `[lon, lat]` (lon ≤ 9.7 et lat ≥ 41.3) |
| **Hash navigation** | URL `#vico/calanques_de_piana` | Site ciblé, marker centré, popup ouvert (le polygone n'apparaît que sur hover/tap) |

### 5.2 Tests régression non-zones

| Test | Attendu |
|------|---------|
| Site ponctuel quelconque (e.g. église, mégalithe) | Pin uniquement, aucun polygone |
| Hover sur site sans `is_zone` | Aucun polygone affiché (sécurité) |
| Tier 3 (lac_de_creno, etc.) | Restent pins, aucun comportement zone |
| Tier 2 défavorables (monte_genova, anneaux_cap) | Restent pins, aucun polygone |

### 5.3 Tests régression UI

| Test | Attendu |
|------|---------|
| Popup pieve (U1 cf. brief précédent) | Note `note_rattachement` s'affiche toujours, pas de fetchFiche |
| Drill-down doyenné → pieve → site | Navigation fluide, polygones zones n'interfèrent pas |
| Filtre axe_corpus | Activation/désactivation `patrimoine_naturel_sacre` masque/montre pins ET polygones (déjà masqués si pins le sont) |

### 5.4 Tests PR B (8 sites supplémentaires)

Idem PR A, focus sur les 8 nouveaux sites. Vérifier qu'aucune régression PR A.

---

## 6. Phase D — Workflow PR + merge

### 6.1 PR A (Tier 1)

1. Branche `feat/b-zones-tier1-15-sites` poussée.
2. PR A feat → dev. Preview Cloudflare URL générée.
3. Coller URL preview en chat à Soleil. Soleil valide §5.1 + §5.2 + §5.3.
4. **Attendre confirmation explicite Soleil** : `"OUI merge dev → main, B-ZONES Tier 1"`.
5. Merge feat → dev.
6. PR dev → main (préparation après `OUI` distinct).
7. **Attendre déploiement prod confirmé** (CF deploy hook + smoke test prod par Soleil).

### 6.2 PR B (Tier 2 favorables)

1. **NE PAS démarrer** avant que PR A soit en prod ET validée par Soleil.
2. Une fois OK, créer branche `feat/b-zones-tier2-8-sites` depuis `dev` à jour.
3. Suivre §4.2.
4. Workflow merge identique à PR A.

---

## 7. Règles strictes

### 7.1 Convention coords — RÈGLE CRITIQUE

- **`zone_geometry.coordinates`** : **`[lon, lat]` GeoJSON standard. JAMAIS `[lat, lon]`.**
- Quand Code lit `zone_geometry` pour passer à Leaflet `L.polygon()`, **inverser explicitement** : `[c[1], c[0]]`.
- **Tester chaque polygone via smoke test PIP bbox Corse** avant commit. Si centroïde hors Corse, **STOP** et corriger.
- Commenter explicitement la convention dans le code Leaflet (cf. §4.1 commit 2).

### 7.2 Doctrines

- **`BP-FIX-RATTACHEMENT-COMPLET-001`** : aucune zone ne doit avoir `pieve_slug` ou `doyenne_contemporain_slug` modifié par cette PR — ces champs restent inchangés (zones = sites, pas pieves).
- **Doctrine je-ne-sais-pas** :
  - Si Overpass ne retourne **rien** pour un site, fallback tracé manuel 5-8 points sur geojson.io (vérification visuelle obligatoire IGN/OSM).
  - Si INPN ou UNESCO code introuvable, fallback OSM Overpass.
  - Si toutes les sources échouent, **STOP** et remonter à Soleil pour décision (skip ce site ou polygone manuel grossier).
- **Pas de modification** de `pieves_polygons.json`, `doyennes_polygons.json`, `pieve_aliases.json`.
- **Pas de modification** des champs existants `lat`/`lon`/`pieve_slug`/`doyenne_contemporain_slug`/etc. — seulement **ajout** de `is_zone`, `zone_geometry`, `zone_source`, `zone_simplification_pts`.
- **Pas de touche** aux pieves (zones = sites uniquement).
- **Pas de touche** aux fiches markdown (cleanup distinct, cf. brief Code FICHES_PIEVES).

### 7.3 Performance

- Polygones rendus **on demand** (au hover/tap). Pas de pré-rendu de 23 polygones au load.
- Simplification ≤ 100 points par polygone. INPN/UNESCO bruts (potentiellement 1000+ points) doivent être simplifiés.
- `interactive: false` sur les polygones (pas d'event capture).

### 7.4 Sécurité / sandbox

- **Exécution Code en local Windows uniquement.** Pas depuis sandbox Cowork (git cassé, `OPS-COWORK-SANDBOX-GIT-DRIFT-001`).
- **Order PR strict** : PR A complète + main mergée + prod déployée AVANT PR B.
- **Pas de `git push --force`** sur `dev` ou `main`.

### 7.5 Smoke test PIP automatisé

À inclure comme script dans la PR (e.g. `scripts/b_zones_smoke_test.py`) :

```python
#!/usr/bin/env python3
"""Smoke test B-ZONES — vérifier que chaque polygone est en Corse + containment doyenne."""
import json
import sys
from shapely.geometry import shape

CORSE_BBOX = (8.5, 41.3, 9.7, 43.2)  # lon_min, lat_min, lon_max, lat_max

def main():
    with open('docs/data/sites_patrimoine.json') as f:
        sites = json.load(f)['sites']
    
    zones = [s for s in sites if s.get('is_zone')]
    print(f"B-ZONES à vérifier : {len(zones)}")
    
    fails = []
    for s in zones:
        geom = shape(s['zone_geometry'])
        c = geom.centroid
        if not (CORSE_BBOX[0] <= c.x <= CORSE_BBOX[2] and CORSE_BBOX[1] <= c.y <= CORSE_BBOX[3]):
            fails.append({"slug": s['slug'], "centroid": [c.x, c.y]})
            print(f"❌ {s['slug']}: centroïde ({c.x:.4f},{c.y:.4f}) HORS CORSE")
        else:
            print(f"✓ {s['slug']:35} centroïde ({c.x:.4f},{c.y:.4f}) OK")
    
    if fails:
        print(f"\n{len(fails)} polygones HORS CORSE — STOP avant commit")
        sys.exit(1)
    print("\nTous les polygones B-ZONES sont en Corse ✓")

if __name__ == '__main__':
    main()
```

Code DOIT le lancer avant chaque commit qui modifie `is_zone`/`zone_geometry`.

---

## 8. Livrables attendus de Code

### 8.1 PR A (Tier 1)

1. Branche `feat/b-zones-tier1-15-sites` poussée + PR feat→dev mergée (3-4 commits §4.1).
2. PR dev→main mergée après `OUI` Soleil distinct.
3. Script `scripts/b_zones_smoke_test.py` ajouté + lancé verts.
4. Rapport chat avec :
   - 15 sites T1 polygonés (slug + source effective utilisée par site)
   - Compteur points par polygone (range, médiane)
   - Smoke test PIP : 15/15 OK
   - URL preview Cloudflare avec screenshots de 3-4 zones échantillon (Scandola, Vizzavona, Calanques, Bavella par ex.)
   - Confirmation étangs Diane/Urbino/Biguglia : trouvés N, inclus en T1 oui/non
   - Dettes ouvertes / fermées
5. SHA des commits merged main.

### 8.2 PR B (Tier 2 favorables)

1. Branche `feat/b-zones-tier2-8-sites` poussée + PR feat→dev mergée (1-2 commits §4.2).
2. PR dev→main mergée après `OUI` Soleil distinct.
3. Smoke test PIP : 23/23 OK (T1 + T2 favorables).
4. Rapport chat avec compteur final : 23 zones actives + screenshots échantillon (Cinto, Capu Rossu, Lac Nino par ex.).

---

## 9. Pièges connus — à attention spéciale

- **Convention `[lon, lat]` vs `[lat, lon]`** : Pieves/doyennés utilisent `[lat, lon]`, B-ZONES utilisent `[lon, lat]` (GeoJSON standard). Si Code copie/colle du code existant pieve→zone sans inversion, **polygones en mer Tyrrhénienne** garanti. **Smoke test obligatoire avant chaque commit.**
- **Sandbox stale** : sandbox Cowork peut afficher pre-Phase 1 état. Code en local Windows à jour, pas concerné.
- **Overpass API timeout** : requêtes parfois lentes (~30s). Boucler avec timeout 60s + retry 2x. Si échec persistant, fallback geojson.io manuel.
- **INPN code Scandola** `FR3600158` : non vérifié en temps réel par Cowork (provenance restriction WebFetch). Code à confirmer Phase A.
- **UNESCO geojson Calanques** : composante du Golfe de Porto (whc.unesco.org/en/list/258). Vérifier que la composante "Réserve naturelle de Scandola" et "Calanques de Piana" sont **distinctes** dans le geojson UNESCO (sinon Scandola et Calanques se chevauchent).
- **Conservatoire du Littoral Agriates** : périmètre = parcelles foncières du Conservatoire (~5500 ha mais discontinu probablement). Si discontinu, simplifier à un seul polygone englobant la zone principale.
- **Monte Cinto et autres monts T2** : la définition "massif" peut varier. Soleil arbitre rayon ~2-3 km autour du sommet — Code suit cette convention (pas le bassin versant entier).
- **Lac de Nino + pozzines** : les pozzines sont des zones humides d'altitude protégées (Natura 2000 possiblement). Polygone doit englober lac + plaine pozzines (rayon ~500m-1km).
- **Tap mobile** : sur certains devices, `matchMedia('(hover: none)')` peut faillir. Tester sur iOS Safari + Chrome Android. Si comportement bizarre, fallback `'ontouchstart' in window`.
- **Z-index pin > polygone** : Leaflet `pane: 'overlayPane'` pour polygones, markers restent dans `markerPane` (default = au-dessus). Vérifier preview.
- **Filtres axe_corpus actifs** : si user désactive filtre `patrimoine_naturel_sacre`, le pin disparaît → le polygone hover ne s'affiche plus (cohérent, attendu).
- **PR A avant PR B** : ne pas démarrer PR B avant validation prod PR A. Lien explicite dans le commit message PR B : `"Prérequis : PR A B-ZONES Tier 1 mergée et validée prod (commit <SHA-A>)"`.

---

## 10. Estimation effort détaillée

### PR A (Tier 1, 15 sites)

| Tâche | Effort |
|-------|--------|
| Phase A vérifs + identification sources | 1h |
| Commit 1 (schema + lecture vérifs) | 30 min |
| Commit 2 (renderer patrimoine.html) | 1h |
| Commit 3 (15 polygones — Overpass + INPN + simplification + smoke test) | 5-6h |
| Commit 4 (dettes + changelog) | 30 min |
| Phase C tests preview | 1h |
| Phase D PR + merge | 30 min |
| **Total PR A** | **~9-10h** |

### PR B (Tier 2 favorables, 8 sites)

| Tâche | Effort |
|-------|--------|
| Commit 1 (8 polygones manuels OSM + manual) | 3h |
| Commit 2 (dettes + changelog) | 15 min |
| Phase C tests preview | 45 min |
| Phase D PR + merge | 30 min |
| **Total PR B** | **~4-5h** |

**Total cumulé : 13-15h (~2 jours Code).**

---

_Brief rédigé par Cowork (sandbox) le 2026-05-18, basé sur l'audit B_ZONES_AUDIT_2026-05-18.md + arbitrages Soleil intégrés. À transmettre à Claude Code après validation Soleil sur le scope final (étangs Diane/Urbino/Biguglia §3.2.2 à confirmer en Phase A)._
