// Phase 2 — regenerate cartoradio_certified_corse.json with real ANFR coords.
// Reads:  public/data/cartoradio_certified_corse.json (centroid version)
//         scripts/carto_corse_geojson_snapshot_2026-04-27.json (ANFR API snapshot)
// Writes: public/data/cartoradio_certified_corse.json (regenerated)
//
// Conventions (per Soleil's brief, validation 1 answers):
//   - lat_centroid_old, lon_centroid_old preserved on every fiche (traceability).
//   - precision_coord: "secteur" → "exacte" on every fiche (all 30 enriched).
//   - _distance_centroid_to_anfr_km: continuous, 2-decimal, on every fiche.
//   - _distance_anomaly: true only when dist >= 30 km (anchors Olmo Puntone bug data).
//   - _source_real_coords: provenance object on every fiche.
//   - top-level: bump version to 1.1, date_maj=2026-04-27, source updated.
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const JSON_PATH = path.join(ROOT, 'public', 'data', 'cartoradio_certified_corse.json');
const SNAPSHOT_PATH = path.join(ROOT, 'scripts', 'carto_corse_geojson_snapshot_2026-04-27.json');

const local = JSON.parse(fs.readFileSync(JSON_PATH, 'utf8'));
const remote = JSON.parse(fs.readFileSync(SNAPSHOT_PATH, 'utf8'));

const realById = {};
for (const f of remote.features) {
  realById[String(f.id)] = { lon: f.geometry.coordinates[0], lat: f.geometry.coordinates[1] };
}

function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const toRad = x => x * Math.PI / 180;
  const dLat = toRad(lat2 - lat1), dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat/2)**2 + Math.cos(toRad(lat1))*Math.cos(toRad(lat2))*Math.sin(dLon/2)**2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

const SOURCE_URL = 'https://www.cartoradio.fr/api/v1/mesures?stationsRadioelec=true&objetsCom=true&anciennete=720&valeurLimiteMin=0&valeurLimiteMax=100&format=geojson&bbox=8.4,41.3,9.6,43.1';
const SOURCE_DATE = '2026-04-27';
const SOURCE_METHOD = 'GeoJSON FeatureCollection from Cartoradio.fr public API (no auth, used by official SPA)';

const ANOMALY_THRESHOLD_KM = 30;

const enriched = [];
const stats = {
  total: 0,
  enriched: 0,
  failed: 0,
  anomalies: [],
};

for (const m of local.mesures) {
  stats.total++;
  const real = realById[String(m.id)];
  if (!real) {
    // Should not happen given phase 1 audit, but defensive: keep fiche untouched + flag.
    enriched.push({
      ...m,
      _enrichment_failed: 'id not present in ANFR API GeoJSON snapshot',
    });
    stats.failed++;
    continue;
  }
  const dist = haversineKm(m.lat, m.lon, real.lat, real.lon);
  const distRounded = Math.round(dist * 100) / 100;
  const out = {
    ...m,
    lat_centroid_old: m.lat,
    lon_centroid_old: m.lon,
    lat: Math.round(real.lat * 1e6) / 1e6,
    lon: Math.round(real.lon * 1e6) / 1e6,
    precision_coord: 'exacte',
    _distance_centroid_to_anfr_km: distRounded,
    _source_real_coords: {
      url: SOURCE_URL,
      date: SOURCE_DATE,
      method: SOURCE_METHOD,
    },
  };
  if (dist >= ANOMALY_THRESHOLD_KM) {
    out._distance_anomaly = true;
    stats.anomalies.push({ id: m.id, commune: m.commune, site_nom: m.site_nom, dist_km: distRounded });
  }
  enriched.push(out);
  stats.enriched++;
}

// Top-level metadata refresh.
local.version = '1.1';
local.date_maj = '2026-04-27';
local.source = 'Coordonnees regenerees depuis l\'API publique ANFR (https://www.cartoradio.fr/api/v1/mesures, format=geojson) le 2026-04-27. Les valeurs metiers (date_mesure, valeur_max_vm, conformite, services, etc.) restent issues de l\'extraction Cowork OCR du 23 avril 2026 sur les 30 PDFs ANFR/EXEM. Les centroides communaux precedents sont conserves dans lat_centroid_old/lon_centroid_old pour tracabilite.';
local.methodology = 'Coordonnees lat/lon: positions exactes ANFR via API GeoJSON publique (sans authentification, endpoint utilise par la SPA officielle cartoradio.fr). Donnees metier (mesures, conformite): 30 PDFs parses par OCR Tesseract 4.1.1 a 100 DPI le 23 avril 2026. Champ precision_coord passe de "secteur" (centroide commune) a "exacte" (point GPS de la mesure ANFR).';
local.statistiques.precision_coord_distribution = { exacte: stats.enriched, secteur: 0, manquante: stats.failed };
local.mesures = enriched;

const out = JSON.stringify(local, null, 2) + '\n';
fs.writeFileSync(JSON_PATH, out);

console.log('=== Regeneration complete ===');
console.log('Total fiches:', stats.total);
console.log('Enriched:', stats.enriched);
console.log('Failed:', stats.failed);
console.log('Distance anomalies (>=30 km):', stats.anomalies);
console.log('JSON written to:', JSON_PATH);
