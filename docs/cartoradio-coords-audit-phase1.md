# Audit Phase 1 — Régénération coordonnées CartoRadio

**Branche** : `data/cartoradio-real-coords`
**Date** : 2026-04-27
**Périmètre** : `public/data/cartoradio_certified_corse.json` (30 fiches ANFR/EXEM Corse)
**Mode** : read-only (aucune modification de production en phase 1)

---

## Verdict synthétique

- **Phase 2 viable** — API publique ANFR `https://www.cartoradio.fr/api/v1/mesures` retourne du GeoJSON avec lat/lon par bbox, sans authentification, en un seul appel pour toutes les fiches Corse.
- **Cas Liscia / Sant'Antonino résolu** : verdict **H2** (« Liscia » est un toponyme/lieu-dit dans la commune administrative Sant'Antonino, position GPS réelle ~9.4 km à l'est du chef-lieu).
- **30/30 fiches enrichissables.** Aucune fiche manquante côté ANFR.
- **Toutes les coordonnées actuelles sont fausses** au sens strict (centroïdes communaux). Distance médiane centroïde → vraie coord : **5.4 km**, max 47 km, min 0.33 km.
- **1 anomalie >30 km** : `192925` Olmo (Puntone) — centroïde actuel pointe vers la Balagne, position réelle en plaine orientale (Casinca). Erreur d'origine du centroïde dans le JSON, pas erreur API.
- **Offset Monticello (`id=193102`) deviendra inutile** post-régénération : 192990 et 193102 ont des coords distinctes naturellement (~30 m d'écart).
- **Estimation phase 2** : ~30 minutes (1 appel API + script de transformation + commit).

---

## 1. Dump des 30 fiches actuelles

Source : `public/data/cartoradio_certified_corse.json` v1.0 (date_maj 2026-04-23, extraction Cowork via OCR Tesseract des PDFs ANFR).

| id | site_nom | commune | dept | lat | lon | precision_coord | date_mesure | conforme |
|---|---|---|---|---|---|---|---|---|
| 188804 | Route des Sanguinaires | Ajaccio | 2A | 41.9191 | 8.7386 | secteur | 2024-05-28 | true |
| 188846 | Quartier Donateo | Calvi | 2B | 42.5619 | 8.7576 | secteur | 2024-05-29 | true |
| 190528 | Pinzalone | Zonza | 2A | 41.7484 | 9.1868 | secteur | 2024-09-18 | true |
| 190549 | Ancienne route de Sarténe | Ajaccio | 2A | 41.9191 | 8.7386 | secteur | 2024-09-18 | true |
| 190560 | Chemin de Pietralba | Ajaccio | 2A | 41.9191 | 8.7386 | secteur | 2024-09-18 | true |
| 190578 | Avenue Christophe Colomb | Calvi | 2B | 42.5619 | 8.7576 | secteur | 2024-09-19 | true |
| 190580 | Route du Stade | Calvi | 2B | 42.5619 | 8.7576 | secteur | 2024-09-19 | true |
| 190586 | Avenue de la Libération | Bastia | 2B | 42.6977 | 9.4514 | secteur | 2024-09-19 | true |
| 190593 | Route du Stade | Calvi | 2B | 42.5619 | 8.7576 | secteur | 2024-09-19 | true |
| 192060 | Stretta di a Damianaccia | Arbori | 2A | 42.0389 | 8.8503 | secteur | 2024-12-17 | true |
| 192091 | Chemin Saint-François | Monticello | 2B | 42.615 | 8.8822 | secteur | 2024-12-17 | true |
| 192095 | Chemin Saint-François | Monticello | 2B | 42.615 | 8.8822 | secteur | 2024-12-17 | true |
| 192909 | Route de Palombaggia | Porto Vecchio | 2A | 41.5911 | 9.2795 | secteur | 2025-03-20 | true |
| 192914 | 1290 Via Di Cirindinu | Zonza | 2A | 41.7484 | 9.1868 | secteur | 2025-03-20 | true |
| 192919 | Veta casanove | Grosseto Prugna | 2A | 41.87 | 8.8833 | secteur | 2025-03-21 | true |
| 192921 | Liscia | Sant Antonino | 2B | 42.5978 | 8.8025 | secteur | 2025-03-18 | true |
| 192924 | Fusajoli | Alata | 2A | 41.9708 | 8.7997 | secteur | 2025-03-21 | true |
| 192925 | Puntone | Olmo | 2B | 42.4722 | 8.8375 | secteur | 2025-03-19 | true |
| 192929 | Strada di a Madonna di e Grazie | Morsiglia | 2B | 43.0044 | 9.4167 | secteur | 2025-03-19 | true |
| 192940 | Petra Arrita | Barrettali | 2B | 42.955 | 9.3583 | secteur | 2025-03-19 | true |
| 192955 | Preschi | Oletta | 2B | 42.6803 | 9.3256 | secteur | 2025-03-19 | true |
| 192990 | San Quilico | Monticello | 2B | 42.615 | 8.8822 | secteur | 2025-03-20 | **false** |
| 193102 | San Quilico | Monticello | 2B | 42.615 | 8.8822 | secteur | 2025-04-01 | true |
| 194161 | Route du Lazaret | Ajaccio | 2A | 41.9191 | 8.7386 | secteur | 2025-10-07 | true |
| 194167 | Route du Lazaret | Ajaccio | 2A | 41.9191 | 8.7386 | secteur | 2025-10-07 | true |
| 194420 | Vespajo | Zonza | 2A | 41.7484 | 9.1868 | secteur | 2025-10-29 | true |
| 195003 | Stradd di Lisula | Speloncato | 2B | 42.47 | 8.9614 | secteur | 2026-01-14 | true |
| 195013 | Strada di Palumbaghja | Porto Vecchio | 2A | 41.5911 | 9.2795 | secteur | 2026-01-15 | true |
| 195014 | Strada di Chjuni | Piana | 2A | 42.2375 | 8.6356 | secteur | 2026-01-15 | true |
| 195158 | 58 Route de San Martino | Santa Maria Di Lota | 2B | 42.7481 | 9.4269 | secteur | 2026-01-14 | true |

**Communes avec ≥2 fiches au même point centroïde** (donc actuellement superposées à l'écran) :
- Ajaccio : 5 fiches (188804, 190549, 190560, 194161, 194167) toutes à 41.9191/8.7386
- Calvi : 4 fiches (188846, 190578, 190580, 190593) toutes à 42.5619/8.7576
- Monticello : 4 fiches (192091, 192095, 192990, 193102) toutes à 42.615/8.8822
- Zonza : 3 fiches (190528, 192914, 194420) toutes à 41.7484/9.1868
- Porto Vecchio : 2 fiches (192909, 195013) toutes à 41.5911/9.2795

Total : **18 fiches sur 30 superposées** par construction (centroïdes communaux).

---

## 2. Diagnostic du cas Liscia / Sant'Antonino — verdict **H2**

### Réponse API ANFR pour `id=192921`

URL : `https://www.cartoradio.fr/api/v1/mesures/192921`

Données structurées renvoyées (extrait) :
```json
{
  "numero": 192921,
  "laboratoire": "EXEM",
  "date": "18/03/2025",
  "adresse": {
    "voie": "Liscia",
    "code_postal": "20220",
    "commune": "SANT ANTONINO"
  },
  "milieu": "exterieur",
  "environnement": "Rue / Route / Parking",
  "protocole": "ANFR/DR 15-4",
  "conformite": "true",
  "mesureglobale": "3.12",
  "rapport": "RPUB_165945.pdf"
}
```

Coordonnées GeoJSON (via endpoint bbox) :
- **API ANFR** : `lon=8.916972`, `lat=42.598113`
- **JSON local actuel** : `lon=8.8025`, `lat=42.5978`
- **Distance** : **9.370 km** (cap 90° → est-nord-est)

### Trois hypothèses initiales

| Hypothèse | Plausibilité | Verdict |
|---|---|---|
| H1 — commune fausse côté ANFR (devrait être Calcatoggio/Sagone près du golfe de la Liscia 2A) | ÉCARTÉE — ANFR confirme commune `SANT ANTONINO`, code postal `20220`, dept 2B | × |
| H2 — « Liscia » est un toponyme local de la commune administrative Sant'Antonino (lieu-dit) | **CONFIRMÉE** — la commune Sant'Antonino s'étend de son chef-lieu (village perché 42.587/8.808) jusqu'à un secteur ~9 km à l'est, vers Costa/Belgodère/Speloncato. Le lieu-dit « Liscia » est un toponyme micro-local de cette extension communale. | ✓ |
| H3 — id obsolète ou erreur OCR | ÉCARTÉE — id 192921 résoluble sur l'API, mêmes adresse/date/laboratoire/valeur que dans le JSON local | × |

### Cause du bug visible

Le bug n'est pas une mauvaise commune ni un id pourri. **C'est l'effet structurel des centroïdes communaux** : la fiche est rendue au chef-lieu administratif Sant'Antonino (42.5978/8.8025), à 9.4 km de sa position GPS réelle (42.598/8.917). Le toponyme « Liscia » est légitime côté ANFR — c'est juste que le lieu-dit est éloigné du village perché. Tellux affichait la fiche « au village » alors que la mesure a eu lieu à un hameau extérieur de la même commune.

**Le canari est résolu par la régénération automatique : phase 2 placera la fiche à 42.598/8.917, position correcte ANFR.**

---

## 3. Cartographie des sources accessibles

### Source identifiée — Cas (a), API publique cartoradio.fr `/api/v1/mesures`

**URL** : `https://www.cartoradio.fr/api/v1/mesures?stationsRadioelec=true&objetsCom=true&anciennete=720&valeurLimiteMin=0&valeurLimiteMax=100&format=geojson&bbox=<lon_min>,<lat_min>,<lon_max>,<lat_max>`

**Caractéristiques** :
- API publique sans authentification ni clé
- Endpoint utilisé par la SPA officielle [cartoradio.fr](https://www.cartoradio.fr) (frontend Vue.js)
- Format de retour : **GeoJSON FeatureCollection**
  - `id` = numéro ANFR (correspond à `id` du JSON local)
  - `geometry.type = "Point"`, `coordinates = [lon, lat]` en EPSG:4326
  - `properties.objet_communicant` = booléen (filtrage protocole 9 kHz-100 kHz vs RF)
- Pas de robots.txt restrictif (404 sur `/robots.txt`)
- Données publiées sous "licence libre" selon [data.anfr.fr](https://data.anfr.fr/accueil) — usage légitime
- Pas de mentions-légales trouvées (404 sur `/mentions-legales` et `/cgu`)

**Détail endpoint individuel** : `https://www.cartoradio.fr/api/v1/mesures/{id}`
- Renvoie : `numero`, `laboratoire`, `date`, `heure`, `adresse{voie, code_postal, commune}`, `milieu`, `environnement`, `protocole`, `emetteurs[]`, `conformite`, `mesureglobale`, `services[]`, `rapport`
- **Pas de lat/lon dans cette réponse** — seule l'API GeoJSON bbox les fournit
- Utile en complément pour valider l'adresse (voie, code postal, commune) ANFR-canonique vs ce que dit le JSON local

**Coverage Corse** : un seul appel `bbox=8.4,41.3,9.6,43.1` retourne **30/30 features**, exactement les ids du JSON local. Aucun id manquant.

### Sources écartées

| Cas | Source | Statut | Note |
|---|---|---|---|
| (b) | `data.gouv.fr` global | inutilisé | Le dataset CartoRadio sur data.gouv.fr est limité à Orléans Métropole, pas de Corse. |
| (c) | scraping HTML cartoradio.fr | non testé | Inutile : l'API officielle suffit. La SPA est rendue côté JS, donc le HTML n'expose rien d'utile sans JS. |
| (d) | saisie manuelle CSV | écarté | Inutile : enrichissement automatique 30/30. |

### Endpoints API additionnels documentés (pour info)

Endpoints listés dans le bundle JS `0.29dafa9d596b6b031567.js` :
- `/api/v1/mesures` (liste / GeoJSON) — utilisé
- `/api/v1/mesures/{id}` (détail) — utilisé pour validation Liscia
- `/api/v1/sites/`, `/api/v1/cartes/`, `/api/v1/statistiques/...` — non pertinents pour ce chantier
- `/cartoradio/web/rapports/RPUB_xxx.pdf` — sert les PDFs publics par référence (`rapport` de `/api/v1/mesures/{id}`)
- `/geoserver/cartoradio/wms` — WMS GeoServer (couches admin uniquement, pas mesures)
- `/geoserver/cartoradio/wfs` — WFS (5 layers : commune, departement, direction, operateur, region — pas de layer mesures)

---

## 4. Échantillon de validation — 30/30 fiches comparées

Snapshot API : `scripts/carto_corse_geojson_snapshot_2026-04-27.json` (4139 octets, 30 features).

Tableau complet (trié par distance décroissante) :

| id | commune | site_nom | lat_old | lon_old | lat_new | lon_new | dist_km |
|---|---|---|---|---|---|---|---|
| **192925** | Olmo | Puntone | 42.4722 | 8.8375 | 42.501418 | 9.409726 | **47.034** ⚠ |
| 192914 | Zonza | 1290 Via Di Cirindinu | 41.7484 | 9.1868 | 41.652794 | 9.361854 | 18.006 |
| 194420 | Zonza | Vespajo | 41.7484 | 9.1868 | 41.673084 | 9.366594 | 17.114 |
| 192060 | Arbori | Stretta di a Damianaccia | 42.0389 | 8.8503 | 42.143845 | 8.800156 | 12.381 |
| 195003 | Speloncato | Stradd di Lisula | 42.47 | 8.9614 | 42.563852 | 8.982503 | 10.578 |
| **192921** | Sant Antonino | **Liscia** | 42.5978 | 8.8025 | 42.598113 | 8.916972 | **9.370** ← canari |
| 192929 | Morsiglia | Strada di a Madonna di e Grazie | 43.0044 | 9.4167 | 42.934888 | 9.367132 | 8.718 |
| 192940 | Barrettali | Petra Arrita | 42.955 | 9.3583 | 42.878441 | 9.348807 | 8.548 |
| 192919 | Grosseto Prugna | Veta casanove | 41.87 | 8.8833 | 41.894571 | 8.810155 | 6.643 |
| 192091 | Monticello | Chemin Saint-François | 42.615 | 8.8822 | 42.612517 | 8.963234 | 6.637 |
| 192095 | Monticello | Chemin Saint-François | 42.615 | 8.8822 | 42.611972 | 8.963127 | 6.631 |
| 192955 | Oletta | Preschi | 42.6803 | 9.3256 | 42.626152 | 9.349623 | 6.333 |
| 192990 | Monticello | San Quilico | 42.615 | 8.8822 | 42.616489 | 8.953664 | 5.850 |
| 193102 | Monticello | San Quilico | 42.615 | 8.8822 | 42.616497 | 8.953300 | 5.820 |
| 192909 | Porto Vecchio | Route de Palombaggia | 41.5911 | 9.2795 | 41.543943 | 9.294541 | 5.391 |
| 192924 | Alata | Fusajoli | 41.9708 | 8.7997 | 41.974025 | 8.740954 | 4.870 |
| 188804 | Ajaccio | Route des Sanguinaires | 41.9191 | 8.7386 | 41.910067 | 8.682874 | 4.719 |
| 195013 | Porto Vecchio | Strada di Palumbaghja | 41.5911 | 9.2795 | 41.560318 | 9.317820 | 4.677 |
| 195158 | Santa Maria Di Lota | 58 Route de San Martino | 42.7481 | 9.4269 | 42.727509 | 9.456807 | 3.348 |
| 190549 | Ajaccio | Ancienne route de Sarténe | 41.9191 | 8.7386 | 41.929017 | 8.770420 | 2.854 |
| 195014 | Piana | Strada di Chjuni | 42.2375 | 8.6356 | 42.217259 | 8.641970 | 2.311 |
| 190560 | Ajaccio | Chemin de Pietralba | 41.9191 | 8.7386 | 41.935445 | 8.754461 | 2.242 |
| 194161 | Ajaccio | Route du Lazaret | 41.9191 | 8.7386 | 41.929110 | 8.757069 | 1.890 |
| 194167 | Ajaccio | Route du Lazaret | 41.9191 | 8.7386 | 41.929254 | 8.756833 | 1.884 |
| 190586 | Bastia | Avenue de la Libération | 42.6977 | 9.4514 | 42.682980 | 9.444916 | 1.720 |
| 190528 | Zonza | Pinzalone | 41.7484 | 9.1868 | 41.750680 | 9.174335 | 1.065 |
| 190578 | Calvi | Avenue Christophe Colomb | 42.5619 | 8.7576 | 42.555531 | 8.760880 | 0.757 |
| 188846 | Calvi | Quartier Donateo | 42.5619 | 8.7576 | 42.562898 | 8.748708 | 0.737 |
| 190580 | Calvi | Route du Stade | 42.5619 | 8.7576 | 42.562848 | 8.753743 | 0.333 |
| 190593 | Calvi | Route du Stade | 42.5619 | 8.7576 | 42.562840 | 8.753743 | 0.333 |

**Statistiques** :
- min `0.333 km` (Calvi)
- médiane `5.391 km`
- moyenne `6.96 km`
- max `47.034 km` (Olmo, à creuser)
- 0 fiche identique au centroïde (toutes vont bouger)

### Anomalie >30 km — `192925` Olmo

- `commune` (JSON local) : "Olmo" / dept "2B"
- `lat_old/lon_old` (JSON local) : `42.4722, 8.8375` — pointe vers la **Balagne intérieure** (secteur Belgodère/Costa)
- `lat_new/lon_new` (API ANFR) : `42.501418, 9.409726` — pointe vers la **plaine orientale** (Casinca, près de Vescovato/Penta-di-Casinca)

**Diagnostic** : la commune `Olmo` (Haute-Corse) est effectivement située en plaine orientale. Le centroïde renseigné dans le JSON actuel (`42.4722, 8.8375`) est **erroné** — il pointe vers une autre zone géographique. C'est très probablement un bug d'extraction OCR ou une confusion avec un toponyme « Olmo » homonyme (lieu-dit en Balagne). La position API ANFR est cohérente avec la commune réelle Olmo (plaine orientale).

**Action en phase 2** : la régénération corrigera automatiquement cette erreur. Le flag `_distance_anomaly: true` sera ajouté pour traçabilité, mais la nouvelle coord est correcte.

### 3 fiches « contrôle » à inspection visuelle (Calvi)

Les 4 fiches Calvi (188846, 190578, 190580, 190593) actuellement à `42.5619, 8.7576` (centroïde unique) deviendront :
- 188846 « Quartier Donateo » → `42.562898, 8.748708` (~600 m nord-ouest du centroïde)
- 190578 « Avenue Christophe Colomb » → `42.555531, 8.760880` (~750 m sud-est)
- 190580 « Route du Stade » → `42.562848, 8.753743` (~330 m ouest)
- 190593 « Route du Stade » → `42.562840, 8.753743` (idem 190580 à 1 m près — protocole 9 kHz-100 kHz au même point physique que 190580 RF)

**Effet visuel attendu** : 4 fiches Calvi qui se superposaient deviennent 3 points distincts (190580 et 190593 collés au même endroit, ce qui est cohérent avec la note du JSON local : « Deux points de mesure réalisés lors de la même inspection »).

---

## 5. Évaluation de l'offset Monticello — sera **inutile** post-phase 2

État actuel `app.html` (lignes ~6390-6391, post-purge antOffshore lignes ~6388-6389) :
```js
if (m.id === '193102') { lat += 0.0015; lon += 0.0015; }
```

But : décaler visuellement la re-inspection 193102 (San Quilico, conforme) du point superposé 192990 (San Quilico, non-conforme).

**Post-régénération** :
- 192990 → `42.616489, 8.953664`
- 193102 → `42.616497, 8.953300`
- Distance naturelle entre les deux : **30 mètres** (au lieu de 0 actuellement)

L'offset manuel `+0.0015°` correspond à environ **165 m N / 124 m E**, soit 5× la distance naturelle réelle. Il deviendrait contre-productif (déplace 193102 au-delà de son vrai voisinage).

**Action en phase 2** : supprimer le bloc `if (m.id === '193102') { ... }` d'`app.html`.

**Note collatérale Monticello** : 192091 et 192095 (Chemin Saint-François) seront à `42.612517/8.963234` et `42.611972/8.963127` — distance naturelle ~60 m. Distincte de la paire San Quilico (192990/193102) située ~1 km plus au nord. Bonne dispersion sur la carte.

---

## 6. Recommandation — **Phase 2 viable**

### Plan d'exécution phase 2 (estimation 30 min)

1. Backup `cartoradio_certified_corse.json.backup-pre-real-coords` (commit séparé).
2. Re-fetch API GeoJSON avec timestamp à jour (le snapshot `scripts/carto_corse_geojson_snapshot_2026-04-27.json` peut être réutilisé tel quel si phase 2 se fait dans la journée).
3. Script Node : pour chaque fiche du JSON local :
   - Lookup par `id` dans le GeoJSON
   - Conserver originaux : `lat_centroid_old`, `lon_centroid_old`, `commune_old`
   - Mettre à jour `lat`, `lon` avec coords ANFR
   - `precision_coord` : `secteur` → `exacte`
   - Ajouter `_source_real_coords: { url: "...", date: "2026-04-27", method: "api/v1/mesures geojson bbox" }`
   - Pour 192925 Olmo : flag `_distance_anomaly: true` (mais coord correcte)
4. Pas de fiche `_enrichment_failed` : 30/30 enrichissables.
5. Pas de fiche `_commune_corrected: true` : la commune ANFR (cas Liscia) confirme la commune locale, c'est juste la position GPS dans la commune qui change.
6. Mettre à jour commentaire `app.html` lignes 6275-6276.
7. Supprimer bloc offset Monticello `app.html`.
8. `node --check` JS app.html + `node -e 'JSON.parse(...)'` JSON validation (pas de `jq` dans l'env Windows).
9. Rapport phase 2 + PR vers `dev`.

### Risques résiduels phase 2

- **Faible** : API ANFR pourrait ne pas renvoyer une fiche si elle a été dépubliée entre l'audit phase 1 (2026-04-27) et l'exécution phase 2 — mitigation : ré-appeler l'API et flagger toute fiche manquante.
- **Faible** : changement structurel de l'API (renommage du paramètre `anciennete=720`, modification du format GeoJSON). Mitigation : refaire la même requête, tester sur la fiche Liscia comme sentinelle.
- **Très faible** : décalage de quelques mètres entre le snapshot et la requête live (l'API ANFR ne change pas les coordonnées d'une mesure ponctuelle, c'est figé une fois la mesure publiée).
- **Aucun** : licence — l'ANFR publie ces données comme "licence libre" et expose une API publique non-authentifiée utilisée par leur frontend.

### Décisions à confirmer par Soleil avant phase 2

1. **Précision conservation** des coords centroïdes anciennes : conserve-t-on `lat_centroid_old` et `lon_centroid_old` dans la structure du JSON, ou remplacement total ? (recommandation : conserver pour traçabilité audit, le code rendu n'utilise que `lat/lon`)
2. **Flag `_distance_anomaly`** : seuil à 30 km (brief original), ou plus bas (par ex. 15 km, attraperait aussi les Zonza/Arbori) ?
3. **Reformulation `precision_coord`** : valeur cible « exacte » (brief original) ou « anfr » / « instrument » (plus descriptive) ? À l'usage UI le code lit-il cette valeur ? (à vérifier avant phase 2 — pas d'impact attendu mais à confirmer)

---

## Annexes

### Annexe A — Snapshot API utilisé pour l'audit

Fichier : `scripts/carto_corse_geojson_snapshot_2026-04-27.json` (4139 octets, 30 features).
Requête : `curl -A "Mozilla/5.0" "https://www.cartoradio.fr/api/v1/mesures?stationsRadioelec=true&objetsCom=true&anciennete=720&valeurLimiteMin=0&valeurLimiteMax=100&format=geojson&bbox=8.4,41.3,9.6,43.1"`
Date : 2026-04-27 ~10h UTC

### Annexe B — Script d'audit utilisé

Fichier : `scripts/carto_audit.cjs` — lit le JSON local et le snapshot API, calcule les distances Haversine et produit le tableau ci-dessus. Reproductible.

### Annexe C — Réponse API ANFR pour la fiche Liscia (192921)

Endpoint détail : `https://www.cartoradio.fr/api/v1/mesures/192921`
Endpoint position : extrait du GeoJSON bbox Corse.

```json
{
  "numero": 192921,
  "laboratoire": "EXEM",
  "date": "18/03/2025",
  "heure": "16h34",
  "adresse": { "voie": "Liscia", "code_postal": "20220", "commune": "SANT ANTONINO" },
  "milieu": "exterieur",
  "environnement": "Rue / Route / Parking",
  "protocole": "ANFR/DR 15-4",
  "conformite": "true",
  "mesureglobale": "3.12",
  "rapport": "RPUB_165945.pdf",
  "_geo_from_geojson_bbox": { "lon": 8.916972, "lat": 42.598113 }
}
```
