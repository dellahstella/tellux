#!/usr/bin/env node
// precompute_alignments.mjs
// Pre-calcule les alignements megalithiques pour eviter le O(n^3) runtime.
// Usage : node _scripts/precompute_alignments.mjs
// Output : _data/alignments_precomputed.json

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');

// --- Step 1: Extract SITES from index.html ---
const html = readFileSync(join(ROOT, 'index.html'), 'utf8');

// Find the inline SITES array
const sitesMatch = html.match(/let SITES\s*=\s*\[([\s\S]*?)\n\];/);
if (!sitesMatch) {
  console.error('ERREUR: impossible de trouver "let SITES=[...]" dans index.html');
  process.exit(1);
}

// Parse each [lat, lon, 'name', ...] entry
const siteEntries = [];
const lineRe = /\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*'([^']*)'/g;
let m;
while ((m = lineRe.exec(sitesMatch[1])) !== null) {
  siteEntries.push({ lat: parseFloat(m[1]), lon: parseFloat(m[2]), name: m[3] });
}
console.log(`[precompute] ${siteEntries.length} sites extraits de index.html`);

if (siteEntries.length < 4) {
  console.error('ERREUR: moins de 4 sites, impossible de detecter des alignements');
  process.exit(1);
}

// --- Step 2: detectAlignments (copie fidele de index.html) ---
const R = 6371000;

function bear(a, b) {
  const dL = (b[1] - a[1]) * Math.PI / 180;
  const la = a[0] * Math.PI / 180;
  const lb = b[0] * Math.PI / 180;
  const y = Math.sin(dL) * Math.cos(lb);
  const x = Math.cos(la) * Math.sin(lb) - Math.sin(la) * Math.cos(lb) * Math.cos(dL);
  return Math.atan2(y, x) * 180 / Math.PI;
}

function hdist(a, b) {
  const la = a[0] * Math.PI / 180;
  const lb = b[0] * Math.PI / 180;
  const dl = (b[0] - a[0]) * Math.PI / 180;
  const dg = (b[1] - a[1]) * Math.PI / 180;
  const s = Math.sin(dl / 2) ** 2 + Math.cos(la) * Math.cos(lb) * Math.sin(dg / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(s));
}

function crossTrackDist(p, a, b) {
  const dAP = hdist(a, p) / R;
  const bAP = bear(a, p) * Math.PI / 180;
  const bAB = bear(a, b) * Math.PI / 180;
  return Math.abs(Math.asin(Math.sin(dAP) * Math.sin(bAP - bAB)) * R);
}

function detectAlignments(points, maxDev, minPts, minKm) {
  maxDev = maxDev || 400;
  minPts = minPts || 4;
  minKm = minKm || 8;
  const lines = [];
  const seen = new Set();
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      const dij = hdist(points[i], points[j]);
      if (dij < minKm * 1000) continue;
      const lp = [i, j];
      for (let k = 0; k < points.length; k++) {
        if (k === i || k === j) continue;
        const ct = crossTrackDist(points[k], points[i], points[j]);
        if (ct < maxDev) lp.push(k);
      }
      if (lp.length >= minPts) {
        const key = lp.slice().sort().join('-');
        if (!seen.has(key)) {
          seen.add(key);
          const az = bear(points[i], points[j]);
          const len = Math.max(...lp.map(idx => hdist(points[i], points[idx]))) / 1000;
          lines.push({
            indices: lp, count: lp.length,
            azimuth: Math.round(((az % 360) + 360) % 360),
            length_km: Math.round(len * 10) / 10,
            points: lp.map(idx => points[idx])
          });
        }
      }
    }
  }
  lines.sort((a, b) => b.count - a.count || b.length_km - a.length_km);
  // Dedup: si deux lignes partagent >70% de points, garder la meilleure
  const dedup = [];
  lines.forEach(l => {
    const overlap = dedup.some(d => {
      const shared = l.indices.filter(i => d.indices.includes(i)).length;
      return shared / Math.min(l.count, d.count) > 0.7;
    });
    if (!overlap) dedup.push(l);
  });
  return dedup.slice(0, 15);
}

// --- Step 3: Monte Carlo p-value (Broadbent 1980), 500 sims ---
function monteCarloPvalue(nSites, bbox, maxDev, minPts, minKm, nSims) {
  nSims = nSims || 500;
  const counts = [];
  for (let s = 0; s < nSims; s++) {
    const pts = [];
    for (let i = 0; i < nSites; i++) {
      pts.push([
        bbox[0] + Math.random() * (bbox[2] - bbox[0]),
        bbox[1] + Math.random() * (bbox[3] - bbox[1])
      ]);
    }
    counts.push(detectAlignments(pts, maxDev, minPts, minKm).length);
    if ((s + 1) % 100 === 0) process.stdout.write(`  Monte Carlo: ${s + 1}/${nSims}\r`);
  }
  console.log(`  Monte Carlo: ${nSims}/${nSims} done`);
  counts.sort((a, b) => a - b);
  return counts;
}

// --- Step 4: Run ---
const pts = siteEntries.map(s => [s.lat, s.lon]);
const bbox = [41.3, 8.5, 43.1, 9.7];

console.log('[precompute] Detection des alignements...');
const lines = detectAlignments(pts, 400, 4, 8);
console.log(`[precompute] ${lines.length} alignements detectes`);

console.log('[precompute] Monte Carlo (500 simulations)...');
const mcCounts = monteCarloPvalue(pts.length, bbox, 400, 4, 8, 500);
const mcMedian = mcCounts[Math.floor(mcCounts.length / 2)];

// Compute p-value per line
const output = {
  computed_at: new Date().toISOString(),
  n_sites: pts.length,
  mc_median: mcMedian,
  mc_n_sims: 500,
  lines: lines.map(l => {
    const pval = mcCounts.filter(c => c >= l.count).length / mcCounts.length;
    return {
      indices: l.indices,
      points: l.points,
      count: l.count,
      azimuth: l.azimuth,
      length_km: l.length_km,
      p_value: Math.round(pval * 1000) / 1000,
      significant: pval < 0.05,
      names: l.indices.map(i => siteEntries[i] ? siteEntries[i].name : '?')
    };
  })
};

const nSig = output.lines.filter(l => l.significant).length;
console.log(`\n=== RESULTAT ===`);
console.log(`Sites : ${output.n_sites}`);
console.log(`Alignements : ${output.lines.length} (${nSig} significatifs, ${output.lines.length - nSig} non significatifs)`);
console.log(`Mediane Monte Carlo : ${mcMedian} alignements pour ${pts.length} points aleatoires`);
output.lines.forEach((l, i) => {
  console.log(`  #${i + 1}: ${l.count} sites, ${l.length_km} km, ${l.azimuth} deg, p=${l.p_value} ${l.significant ? '*** SIGNIFICATIF' : ''}`);
  console.log(`       ${l.names.join(' -> ')}`);
});

// --- Step 5: Write JSON ---
const outPath = join(ROOT, '_data', 'alignments_precomputed.json');
writeFileSync(outPath, JSON.stringify(output, null, 2));
console.log(`\n[precompute] JSON ecrit dans ${outPath}`);
