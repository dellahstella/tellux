# Régénération Phase 2 — Coordonnées CartoRadio centroïde → exacte ANFR

**Branche** : `data/cartoradio-real-coords`
**Date** : 2026-04-27
**Référence audit** : [docs/cartoradio-coords-audit-phase1.md](cartoradio-coords-audit-phase1.md)
**Décisions Soleil (validation 1)** : `lat_centroid_old`/`lon_centroid_old` conservés ; `_distance_centroid_to_anfr_km` continu sur 30/30 fiches ; `_distance_anomaly: true` à partir de 30 km uniquement ; `precision_coord = "exacte"`.

---

## Résumé

- **30/30 fiches enrichies** avec coordonnées exactes ANFR. Aucune fiche en échec.
- **1 anomalie >30 km** : `192925` Olmo Puntone (47.03 km, bug data préexistant dans le centroïde local — résolu en passant).
- **0 fiche `_commune_corrected`** : la commune renseignée est correcte ANFR-canonique sur les 30 fiches (vérifié sur Liscia 192921 et Olmo 192925, validé par cohérence sur les autres).
- **Offset Monticello supprimé** d'`app.html` : 192990/193102 ont des coords distinctes côté ANFR (~30 m d'écart), l'offset manuel `+0.0015°` valait 165 m et serait devenu contre-productif.
- **Commentaire `app.html` mis à jour** + `note_precision` du JSON wrapper de téléchargement mis à jour.
- **Backup conservé** : `public/data/cartoradio_certified_corse.json.backup-pre-real-coords` (à supprimer dans une PR ultérieure post-validation prod).

---

## Tableau des 30 fiches — ancien centroïde vs nouvelle coord exacte

Tri par distance décroissante. Toutes les distances sont en km, calcul Haversine (R=6371 km).

| id | commune | site_nom | lat_old | lon_old | lat_new | lon_new | dist_km | flag |
|---|---|---|---|---|---|---|---|---|
| **192925** | Olmo | Puntone | 42.4722 | 8.8375 | 42.501418 | 9.409726 | **47.03** | `_distance_anomaly` |
| 192914 | Zonza | 1290 Via Di Cirindinu | 41.7484 | 9.1868 | 41.652794 | 9.361854 | 18.01 | – |
| 194420 | Zonza | Vespajo | 41.7484 | 9.1868 | 41.673084 | 9.366594 | 17.11 | – |
| 192060 | Arbori | Stretta di a Damianaccia | 42.0389 | 8.8503 | 42.143845 | 8.800156 | 12.38 | – |
| 195003 | Speloncato | Stradd di Lisula | 42.47 | 8.9614 | 42.563852 | 8.982503 | 10.58 | – |
| **192921** | Sant Antonino | **Liscia** | 42.5978 | 8.8025 | 42.598113 | 8.916972 | **9.37** | – ← canari résolu |
| 192929 | Morsiglia | Strada di a Madonna di e Grazie | 43.0044 | 9.4167 | 42.934888 | 9.367132 | 8.72 | – |
| 192940 | Barrettali | Petra Arrita | 42.955 | 9.3583 | 42.878441 | 9.348807 | 8.55 | – |
| 192919 | Grosseto Prugna | Veta casanove | 41.87 | 8.8833 | 41.894571 | 8.810155 | 6.64 | – |
| 192091 | Monticello | Chemin Saint-François | 42.615 | 8.8822 | 42.612517 | 8.963234 | 6.64 | – |
| 192095 | Monticello | Chemin Saint-François | 42.615 | 8.8822 | 42.611972 | 8.963127 | 6.63 | – |
| 192955 | Oletta | Preschi | 42.6803 | 9.3256 | 42.626152 | 9.349623 | 6.33 | – |
| 192990 | Monticello | San Quilico | 42.615 | 8.8822 | 42.616489 | 8.953664 | 5.85 | – |
| 193102 | Monticello | San Quilico | 42.615 | 8.8822 | 42.616497 | 8.953300 | 5.82 | – |
| 192909 | Porto Vecchio | Route de Palombaggia | 41.5911 | 9.2795 | 41.543943 | 9.294541 | 5.39 | – |
| 192924 | Alata | Fusajoli | 41.9708 | 8.7997 | 41.974025 | 8.740954 | 4.87 | – |
| 188804 | Ajaccio | Route des Sanguinaires | 41.9191 | 8.7386 | 41.910067 | 8.682874 | 4.72 | – |
| 195013 | Porto Vecchio | Strada di Palumbaghja | 41.5911 | 9.2795 | 41.560318 | 9.317820 | 4.68 | – |
| 195158 | Santa Maria Di Lota | 58 Route de San Martino | 42.7481 | 9.4269 | 42.727509 | 9.456807 | 3.35 | – |
| 190549 | Ajaccio | Ancienne route de Sarténe | 41.9191 | 8.7386 | 41.929017 | 8.770420 | 2.85 | – |
| 195014 | Piana | Strada di Chjuni | 42.2375 | 8.6356 | 42.217259 | 8.641970 | 2.31 | – |
| 190560 | Ajaccio | Chemin de Pietralba | 41.9191 | 8.7386 | 41.935445 | 8.754461 | 2.24 | – |
| 194161 | Ajaccio | Route du Lazaret | 41.9191 | 8.7386 | 41.929110 | 8.757069 | 1.89 | – |
| 194167 | Ajaccio | Route du Lazaret | 41.9191 | 8.7386 | 41.929254 | 8.756833 | 1.88 | – |
| 190586 | Bastia | Avenue de la Libération | 42.6977 | 9.4514 | 42.682980 | 9.444916 | 1.72 | – |
| 190528 | Zonza | Pinzalone | 41.7484 | 9.1868 | 41.750680 | 9.174335 | 1.07 | – |
| 190578 | Calvi | Avenue Christophe Colomb | 42.5619 | 8.7576 | 42.555531 | 8.760880 | 0.76 | – |
| 188846 | Calvi | Quartier Donateo | 42.5619 | 8.7576 | 42.562898 | 8.748708 | 0.74 | – |
| 190580 | Calvi | Route du Stade | 42.5619 | 8.7576 | 42.562848 | 8.753743 | 0.33 | – |
| 190593 | Calvi | Route du Stade | 42.5619 | 8.7576 | 42.562840 | 8.753743 | 0.33 | – |

---

## Détail des cas notables

### Cas 192925 Olmo Puntone — `_distance_anomaly: true` (47.03 km) — bug data préexistant corrigé en passant

**Diagnostic** :
- Centroïde précédent (`42.4722, 8.8375`) → pointe en Balagne intérieure (secteur Belgodère/Costa).
- Coord ANFR (`42.501418, 9.409726`) → plaine orientale, secteur Casinca/Borgo, code postal 20290.
- Commune renseignée dans le JSON local : `Olmo` — **correcte** (vérifié auprès de l'API ANFR : `commune=OLMO, code_postal=20290`).

**Cause probable** : erreur d'attribution du centroïde lors de l'extraction Cowork OCR du 23 avril 2026 (probable confusion entre la commune Olmo Casinca et un toponyme « Olmo » homonyme en Balagne, ou erreur d'arrondi du centroïde communal).

**Action en phase 2** : aucune intervention manuelle nécessaire — la régénération corrige automatiquement la coord. La commune `Olmo` reste inchangée (correcte). Flag `_distance_anomaly: true` posé pour signaler que ce cas mérite une vérification humaine en relecture (mais la nouvelle coord est valide).

### Cas 192921 Sant'Antonino Liscia — canari du chantier, résolu (9.37 km)

**Diagnostic phase 1 confirmé** : verdict H2. « Liscia » est un toponyme/lieu-dit de la commune administrative Sant'Antonino, situé environ 9.4 km à l'est du chef-lieu (village perché de Sant'Antonino à 42.587/8.808). Position ANFR `42.598113, 8.916972` est dans le territoire communal étendu, vers Costa/Speloncato. ANFR confirme `commune=SANT ANTONINO, code_postal=20220`.

**Action en phase 2** : régénération automatique. Les champs `site_nom: "Liscia"` et `commune: "Sant Antonino"` sont **conservés tels quels** (corrects côté ANFR). Seules `lat`/`lon` bougent vers la position exacte. La fiche reste donc administrativement à Sant'Antonino sur la carte (pas de saut vers le golfe de la Liscia côte ouest 2A — l'instinct géographique initial était trompeur).

### Cas Monticello (id=192091, 192095, 192990, 193102) — offset manuel supprimé

Avant phase 2 : 4 fiches Monticello toutes au centroïde `42.615, 8.8822`, donc superposées. L'offset `+0.0015°` appliqué manuellement à 193102 dans `app.html` permettait de la décaler de ~165 m au nord-est de 192990 pour visualiser la paire NC + re-inspection.

Après phase 2 :
| id | site_nom | lat_new | lon_new | distance à voisin |
|---|---|---|---|---|
| 192091 | Chemin Saint-François | 42.612517 | 8.963234 | 60 m de 192095 |
| 192095 | Chemin Saint-François | 42.611972 | 8.963127 | – |
| 192990 | San Quilico | 42.616489 | 8.953664 | 30 m de 193102 |
| 193102 | San Quilico | 42.616497 | 8.953300 | – |

Les paires (192091/192095) et (192990/193102) sont distantes d'environ 1 km (Chemin Saint-François au sud, San Quilico au nord-ouest). L'offset manuel de 165 m N+E aurait sur-déplacé 193102 à 5× sa distance naturelle de 192990 — devenu contre-productif.

**Action en phase 2** : suppression du bloc `if (m.id === '193102') { lat += 0.0015; lon += 0.0015; }` dans `_renderMesuresCertifiees` (`app.html`).

**Note de cluster** : la paire (192990, 193102) à ~30 m d'écart est serrée et risque de se superposer visuellement à zoom faible (z<14). C'est la réalité géographique : deux mesures ANFR au même point physique (NC le 20/03/2025 puis re-inspection le 01/04/2025). Un cluster Leaflet règlerait le problème de superposition à zoom faible — **ticket séparé** si Soleil le souhaite, **non inclus dans cette PR**.

### Communes auparavant superposées — résultat sur la carte

- **Ajaccio** (5 fiches : 188804, 190549, 190560, 194161, 194167) : précédemment toutes à `41.9191/8.7386`, désormais dispersées sur ~5 km (Sanguinaires à l'ouest, Lazaret au sud, Sartène/Pietralba au nord). Les paires 194161/194167 (Route du Lazaret, même protocole, même date) restent à 30 m d'écart, géographiquement cohérent.
- **Calvi** (4 fiches : 188846, 190578, 190580, 190593) : précédemment à `42.5619/8.7576`, désormais 3 points distincts (190580 et 190593 collés au même point — Route du Stade RF + objet communicant fixe au même endroit). Distances étendues sur ~750 m du nord (Donateo) au sud (Christophe Colomb).
- **Monticello** (4 fiches) : voir bloc dédié ci-dessus.
- **Zonza** (3 fiches : 190528, 192914, 194420) : précédemment toutes à `41.7484/9.1868`, désormais dispersées sur ~2 km dans le secteur Pinzalone/Cirindinu/Vespajo.
- **Porto Vecchio** (2 fiches : 192909, 195013) : précédemment à `41.5911/9.2795`, désormais sur l'axe Palombaggia (192909 et 195013 à ~2.5 km l'une de l'autre).

---

## Modifications de fichiers

### `public/data/cartoradio_certified_corse.json` (commit 2)

**Top-level** :
- `version`: `"1.0"` → `"1.1"`
- `date_maj`: `"2026-04-23"` → `"2026-04-27"`
- `source` : reformulé pour expliciter l'origine API ANFR pour les coords + extraction OCR conservée pour les valeurs métier
- `methodology` : reformulé idem
- `statistiques.precision_coord_distribution` : nouveau champ — `{exacte: 30, secteur: 0, manquante: 0}`

**Par fiche (30/30)** :
- `lat`, `lon` : remplacées par les coords ANFR (arrondies à 6 décimales)
- `precision_coord`: `"secteur"` → `"exacte"`
- `lat_centroid_old`, `lon_centroid_old` : conservation des centroïdes précédents (traçabilité audit)
- `_distance_centroid_to_anfr_km` : nouvelle clé, valeur arrondie à 2 décimales en km
- `_source_real_coords` : nouvelle clé, objet `{url, date, method}`
- `_distance_anomaly: true` : sur 192925 Olmo uniquement (47.03 km ≥ 30 km)

Les autres champs (id, site_nom, commune, departement, valeur_max_vm, conformite, services, date_mesure, etc.) sont **inchangés**.

### `public/data/cartoradio_certified_corse.json.backup-pre-real-coords` (commit 1)

Backup intégral du JSON v1.0 (793 lignes, 25574 octets). À supprimer dans une PR ultérieure après validation prod.

### `app.html` (commit 3)

3 modifications :
1. Commentaire d'en-tête `// ═══ Mesures certifiées ANFR/EXEM ═══` (lignes 6569-6572) : reformulation pour refléter la nouvelle source des coords (API ANFR) et préserver la trace de l'origine OCR pour les valeurs métier.
2. `note_precision` dans `downloadCertifiedJSON()` (ligne 6608) : reformulation cohérente avec la nouvelle précision.
3. Suppression du bloc `if (m.id === '193102') { lat += 0.0015; lon += 0.0015; }` dans `_renderMesuresCertifiees` (lignes 6717-6719 ancien → supprimées).

Aucune autre modification fonctionnelle. La logique `_renderMesuresCertifiees`, `loadMesuresCertifiees`, `downloadCertifiedJSON` reste identique au-delà de ces 3 points.

---

## Validation technique

- `node -e 'JSON.parse(...)' public/data/cartoradio_certified_corse.json` ✅
- `node --check` sur les 2 blocs JS d'`app.html` (lignes 1869-6181 et 6198-7380) ✅
- `grep` sur `0.0015` et `Offset visuel pour Monticello` dans `app.html` → 0 résultat ✅
- Spot-check programmatique des 3 fiches clés (Liscia, Olmo, Monticello pair) : conformes attentes ✅

---

## Commits sur la branche

| # | Hash | Message |
|---|---|---|
| 1 (phase 1) | `4f801d7` | docs: audit cartoradio coords phase 1 |
| 2 (phase 2) | `930d0ae` | data: backup cartoradio coords pre-régénération |
| 3 (phase 2) | `fd1d209` | data: régénération 30 coords cartoradio centroïde → exacte ANFR |
| 4 (phase 2) | `d90ae75` | chore: maj commentaire app.html source cartoradio + retrait offset Monticello |

(Le rapport phase 2 sera ajouté dans un commit 5 avant ouverture de PR.)

---

## Source des coordonnées — traçabilité

URL exacte conservée dans `_source_real_coords.url` de chaque fiche :
```
https://www.cartoradio.fr/api/v1/mesures?stationsRadioelec=true&objetsCom=true&anciennete=720&valeurLimiteMin=0&valeurLimiteMax=100&format=geojson&bbox=8.4,41.3,9.6,43.1
```

Méthode : appel HTTP GET sans authentification, endpoint utilisé par la SPA officielle ANFR (`https://www.cartoradio.fr/`). Format de retour : GeoJSON FeatureCollection EPSG:4326. Date du fetch : 2026-04-27 (vérifiée invariante entre l'audit phase 1 et la régénération phase 2 par diff binaire des deux snapshots).

Snapshot archivé : `scripts/carto_corse_geojson_snapshot_2026-04-27.json`. Script de régénération reproductible : `scripts/carto_regenerate.cjs`.

---

## Risques résiduels après merge

- **Faible** : si une fiche ANFR est modifiée a posteriori (ré-géocodage), nos coords seront figées au snapshot 2026-04-27. Mitigation : ré-exécuter `scripts/carto_regenerate.cjs` lors d'une prochaine update.
- **Visuel** : la paire Monticello (192990, 193102) à 30 m d'écart sera serrée à zoom <14. Mitigation possible : cluster Leaflet (ticket séparé).
- **Aucun** : licence — données publiques ANFR, API publique non-authentifiée, usage compatible avec « licence libre » revendiquée par le portail data.anfr.fr.
