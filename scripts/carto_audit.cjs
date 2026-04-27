// Phase 1 audit script — compares centroid coords (current JSON) to real ANFR coords (geojson API).
// One-shot: runs read-only, prints a markdown table to stdout.
const fs = require('fs');
const path = require('path');

const local = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'public', 'data', 'cartoradio_certified_corse.json'), 'utf8'));
const remote = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

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

const rows = [];
for (const m of local.mesures) {
  const real = realById[m.id];
  if (!real) {
    rows.push({ id: m.id, commune: m.commune, site_nom: m.site_nom, status: 'MISSING_API', dist: null });
    continue;
  }
  const dist = haversineKm(m.lat, m.lon, real.lat, real.lon);
  rows.push({
    id: m.id,
    commune: m.commune,
    site_nom: m.site_nom,
    lat_old: m.lat, lon_old: m.lon,
    lat_new: real.lat, lon_new: real.lon,
    dist_km: dist
  });
}

rows.sort((a, b) => (b.dist_km || 0) - (a.dist_km || 0));

console.log('| id | commune | site_nom | lat_old | lon_old | lat_new | lon_new | dist_km |');
console.log('|---|---|---|---|---|---|---|---|');
for (const r of rows) {
  if (r.status === 'MISSING_API') {
    console.log(`| ${r.id} | ${r.commune} | ${r.site_nom} | – | – | – | – | MISSING |`);
  } else {
    console.log(`| ${r.id} | ${r.commune} | ${r.site_nom} | ${r.lat_old} | ${r.lon_old} | ${r.lat_new.toFixed(6)} | ${r.lon_new.toFixed(6)} | ${r.dist_km.toFixed(3)} |`);
  }
}

console.log('\nTotal local mesures:', local.mesures.length, '— remote features:', remote.features.length);
const matched = rows.filter(r => r.status !== 'MISSING_API');
const distances = matched.map(r => r.dist_km).sort((a,b) => a-b);
const median = distances[Math.floor(distances.length/2)];
const max = distances[distances.length-1];
const min = distances[0];
const sum = distances.reduce((a,b) => a+b, 0);
console.log('Distance min:', min.toFixed(3), 'km');
console.log('Distance median:', median.toFixed(3), 'km');
console.log('Distance mean:', (sum/distances.length).toFixed(3), 'km');
console.log('Distance max:', max.toFixed(3), 'km');
console.log('Anomalies (>30 km):', matched.filter(r => r.dist_km > 30).map(r => r.id));
console.log('Identical (dist <0.001 km):', matched.filter(r => r.dist_km < 0.001).map(r => r.id));
