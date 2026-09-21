#!/usr/bin/env node
// precompute_emag2v3_corse.mjs
// Extrait une grille figée, datée et versionnée depuis le service NOAA EMAG2v3
// ImageServer (endpoint identify — le même que fetchEMAG2() dans app.html), pour
// remplacer à terme LCS1_GRID (24 points, provenance indéterminée, non corrélée
// à ce même service — cf. RAPPORT_LCS1_IDENTITE_IMPACT_2026-09-19.md, r=-0,10).
//
// TEMPS 1 SEUL (brief REMPLACEMENT_LCS1_GRID_2026-09-19) : ce script produit une
// donnée hors ligne, non branchée à aucun affichage public. Il ne modifie ni
// LCS1_GRID ni calcLCS1() ni aucune formule de score.
//
// Bbox reprise TELLE QUELLE de la convention déjà existante dans app.html pour
// EMAG2v3 (const wmsEmag, exportImage) : bbox=8.5,41.3,9.65,43.1 (lon_min,lat_min,
// lon_max,lat_max) — pas une bbox inventée pour ce script.
// Résolution : pas natif du service, confirmé EN DIRECT le 2026-09-19 via
// GET https://gis.ngdc.noaa.gov/arcgis/rest/services/EMAG2v3/ImageServer?f=json
// -> pixelSizeX=pixelSizeY=0.03333333333333333 (= 1/30°, 2 minutes d'arc),
// meanPixelSize=3710.6496931091187 m. Le script échantillonne EXACTEMENT à ce
// pas (aucune sur-résolution — cf. règle explicite du brief, étape c).
//
// Usage : node _scripts/precompute_emag2v3_corse.mjs
// Output : _data/emag2v3_corse_2026-09-19.json

import { writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

const BBOX = { lonMin: 8.5, latMin: 41.3, lonMax: 9.65, latMax: 43.1 };
const PITCH = 1 / 30; // 2 arc-min, = pixelSizeX/Y natif confirmé en direct (voir en-tête)
const ENDPOINT = 'https://gis.ngdc.noaa.gov/arcgis/rest/services/EMAG2v3/ImageServer/identify';
const CONCURRENCY = 6;
const MAX_RETRIES = 4;
const RETRY_BASE_MS = 600;
const TIMEOUT_MS = 8000;
const EXTRACTION_DATE = '2026-09-19';

function buildPoints() {
  const lats = [];
  for (let lat = BBOX.latMin; lat <= BBOX.latMax + 1e-9; lat += PITCH) lats.push(+lat.toFixed(6));
  const lons = [];
  for (let lon = BBOX.lonMin; lon <= BBOX.lonMax + 1e-9; lon += PITCH) lons.push(+lon.toFixed(6));
  const points = [];
  for (const lat of lats) for (const lon of lons) points.push({ lat, lon });
  return points;
}

async function fetchOne(lat, lon) {
  const url = `${ENDPOINT}?geometry=${lon.toFixed(6)},${lat.toFixed(6)}&geometryType=esriGeometryPoint&returnGeometry=false&returnCatalogItems=false&f=json`;
  for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
    try {
      const ctrl = new AbortController();
      const tid = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
      const r = await fetch(url, { signal: ctrl.signal });
      clearTimeout(tid);
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const j = await r.json();
      const v = parseFloat(j.value);
      if (!isNaN(v)) return { lat, lon, nT: Math.round(v * 100) / 100, status: 'ok' };
      // Réponse serveur valide, réellement hors couverture (même distinction que fetchEMAG2 app.html:6180-6182)
      return { lat, lon, nT: null, status: 'no_data' };
    } catch (e) {
      if (attempt === MAX_RETRIES) return { lat, lon, nT: null, status: 'fetch_failed', error: String(e.message || e) };
      const delay = RETRY_BASE_MS * Math.pow(2, attempt);
      await new Promise((res) => setTimeout(res, delay));
    }
  }
}

async function runPool(points) {
  const results = new Array(points.length);
  let next = 0;
  let done = 0;
  async function worker() {
    while (next < points.length) {
      const idx = next++;
      const p = points[idx];
      results[idx] = await fetchOne(p.lat, p.lon);
      done++;
      if (done % 200 === 0 || done === points.length) {
        console.error(`[precompute_emag2v3] ${done}/${points.length}`);
      }
    }
  }
  const workers = Array.from({ length: CONCURRENCY }, () => worker());
  await Promise.all(workers);
  return results;
}

function stats(values) {
  const n = values.length;
  if (n === 0) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mean = values.reduce((a, b) => a + b, 0) / n;
  const stdev = Math.sqrt(values.reduce((s, v) => s + (v - mean) ** 2, 0) / n);
  return {
    n, min: sorted[0], max: sorted[n - 1],
    median: sorted[Math.floor(n / 2)],
    mean: +mean.toFixed(2), stdev: +stdev.toFixed(2),
  };
}

async function main() {
  const points = buildPoints();
  console.error(`[precompute_emag2v3] ${points.length} points a extraire (bbox ${JSON.stringify(BBOX)}, pas ${PITCH.toFixed(6)}°)`);

  const results = await runPool(points);

  const ok = results.filter((r) => r.status === 'ok');
  const noData = results.filter((r) => r.status === 'no_data');
  const failed = results.filter((r) => r.status === 'fetch_failed');

  console.error(`[precompute_emag2v3] ok=${ok.length} no_data=${noData.length} fetch_failed=${failed.length}`);
  if (failed.length > 0) {
    console.error('[precompute_emag2v3] points en échec (retries épuisés) :');
    failed.forEach((f) => console.error(`  ${f.lat},${f.lon} — ${f.error}`));
  }

  const valueStats = stats(ok.map((r) => r.nT));

  const output = {
    _metadata: {
      description: 'Grille EMAG2v3 (anomalie magnétique crustale) pour la Corse, extraite du service NOAA ImageServer, préparée pour remplacer LCS1_GRID (app.html). NON BRANCHÉE (temps 1, brief REMPLACEMENT_LCS1_GRID_2026-09-19) — voir rapport privé pour comparaison contre LCS1_GRID actuelle et vérification d\'impact score.',
      produit: { valeur: 'EMAG2v3', source: '[REPO-LIVE] ImageServer?f=json au 2026-09-19 : name="EMAG2v3", serviceDescription="EMAG2v3", currentVersion=11.5 (version du service ArcGIS, PAS du produit scientifique)' },
      produit_scientifique: { valeur: 'EMAG2v3: Earth Magnetic Anomaly Grid (2-arc-minute resolution), Version 3', source: '[EXTERNE] Meyer, B.; Saltus, R.; Chulliat, A. 2017. NOAA NCEI, DOI 10.7289/V5H70CVX — fiche NCEI officielle, déjà citée ailleurs dans le dépôt public (transparence.html)' },
      doi: { valeur: '10.7289/V5H70CVX', source: '[EXTERNE] fiche NCEI officielle (idem ci-dessus)' },
      altitude_reference: { valeur: '4 km au-dessus du géoïde (grille continentale) ; produit séparé au niveau de la mer pour zones océaniques', source: '[EXTERNE] documentation publiée EMAG2v3 (Meyer, Saltus & Chulliat 2017) — cf. RAPPORT_ALTITUDE_EMAG2_2026-09-19.md §b. NE FIGURE PAS dans les métadonnées servies par l\'API elle-même (iteminfo vide, vérifié à nouveau le 2026-09-19).' },
      licence: { valeur: 'Domaine public / CC0 (États-Unis, NOAA)', source: '[EXTERNE] fiche NCEI officielle — cf. RAPPORT_ALTITUDE_EMAG2_2026-09-19.md §d. licenseInfo vide côté API (vérifié à nouveau le 2026-09-19, endpoint info/iteminfo).' },
      pas_natif_pixel: { valeur: '0.03333333333333333° (1/30°, 2 minutes d\'arc) ; meanPixelSize=3710.6496931091187 m', source: '[REPO-LIVE] ImageServer?f=json, champs pixelSizeX/pixelSizeY/meanPixelSize, vérifié en direct le 2026-09-19' },
      pas_extraction_utilise: { valeur: PITCH, note: 'Identique au pas natif — pas de sur-résolution (règle explicite du brief).' },
      echelle_legende_source: { valeur: 'Stretched, High=+200 nT, Low=-200 nT (échelle continue)', source: '[REPO-LIVE] ImageServer/legend?f=json, vérifié en direct le 2026-09-19 — identique au relevé du 2026-08-29 cité dans app.html:5079-5080 (aucune dérive)' },
      pixel_type: { valeur: 'F32 (flottant 32 bits), bandCount=1', source: '[REPO-LIVE] ImageServer?f=json, vérifié en direct le 2026-09-19' },
      endpoint_interroge: `${ENDPOINT}?geometry=LON,LAT&geometryType=esriGeometryPoint&returnGeometry=false&returnCatalogItems=false&f=json`,
      bbox_extraction: BBOX,
      bbox_provenance: 'Identique à la bbox déjà utilisée par wmsEmag (const wmsEmag, app.html:4405-4409) pour EMAG2v3 en Corse — pas une bbox inventée pour ce script.',
      date_extraction: EXTRACTION_DATE,
      nb_points_grille: points.length,
      nb_points_ok: ok.length,
      nb_points_no_data: noData.length,
      nb_points_fetch_failed: failed.length,
      stats_nT: valueStats,
      script_extracteur: '_scripts/precompute_emag2v3_corse.mjs',
      avertissement: 'Continuation vers le haut à l\'altitude déclarée par la source (4 km, cf. altitude_reference) — AUCUNE continuation vers le bas appliquée ici. Le code de app.html documente que ce chemin (NOAA live) sous-estime les crêtes d\'anomalies locales fortes (ex. Monte Maggiore -48 nT au lieu d\'une anomalie locale forte attendue) — cette grille hérite du même biais, à l\'altitude native de la source, sans correction.',
    },
    grille: results.map((r) => [r.lat, r.lon, r.nT]),
  };

  const outPath = join(ROOT, '_data', `emag2v3_corse_${EXTRACTION_DATE}.json`);
  writeFileSync(outPath, JSON.stringify(output, null, 1));
  console.error(`[precompute_emag2v3] écrit : ${outPath}`);
  console.log(JSON.stringify({ stats: valueStats, ok: ok.length, no_data: noData.length, fetch_failed: failed.length, total: points.length }, null, 2));
}

main().catch((e) => { console.error(e); process.exit(1); });
