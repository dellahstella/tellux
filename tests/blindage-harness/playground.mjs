// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Playground : exemples d'usage du harness pour WS2
// (validation RF + sweep sensibilité EXPERT_WEIGHTS/BOUNDS)
// Création : 2026-06-06 · feat/blindage-harness
// ═══════════════════════════════════════════════════════════════════════════
//
// Ce fichier n'est pas un test : il sert d'exemple exécutable pour :
//   1. Charger les 30 mesures certifiées ANFR/EXEM et calculer le résidu vs
//      calcRF du moteur (boucle WS2 validation RF).
//   2. Variation des EXPERT_WEIGHTS / EXPERT_BOUNDS en sandbox (sans toucher
//      les constantes GELE-001 de prod) sur quelques points représentatifs
//      (boucle WS2 sensibilité).
//
// Usage :
//   node playground.mjs rf-residuals      # affiche les résidus RF sur 30 mesures
//   node playground.mjs sensitivity       # sweep EXPERT_WEIGHTS sur 5 points
//   node playground.mjs                   # liste les modes disponibles
// ═══════════════════════════════════════════════════════════════════════════

import { readFile } from 'node:fs/promises';
import { join, resolve as pathResolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHarness } from './harness.mjs';

const __filename = fileURLToPath(import.meta.url);
const HARNESS_DIR = pathResolve(__filename, '..');
const REPO_ROOT = pathResolve(HARNESS_DIR, '..', '..');

// ─── WS2 — Résidus RF sur 30 mesures certifiées EXEM ───────────────────────

async function modeRfResiduals() {
  const fp = join(REPO_ROOT, 'public', 'data', 'cartoradio_certified_corse.json');
  const data = JSON.parse(await readFile(fp, 'utf-8'));
  const mesures = data.mesures;
  console.log(`Chargé ${mesures.length} mesures certifiées (source : ${data.source.slice(0, 50)}...)`);
  console.log('');

  const harness = await createHarness();
  console.log('Harness ready.');
  console.log('');

  console.log('% diff = (predicted - measured) / measured');
  console.log('───────────────────────────────────────────────────────────────────────');
  console.log('  id      commune              measured(V/m)  predicted(V/m)   % diff');
  console.log('───────────────────────────────────────────────────────────────────────');

  const residuals = [];
  for (const m of mesures) {
    const v2 = await harness.calcAll_v2(m.lat, m.lon, {});
    const sUW_m2 = v2?.domains?.rf?.S_total_uW_m2 ?? 0;
    // Conversion µW/m² → V/m en champ lointain : E = √(S × 377), S en W/m²
    const sW_m2 = sUW_m2 * 1e-6;
    const predictedVm = Math.sqrt(Math.max(0, sW_m2) * 377);
    const measured = m.valeur_max_vm;
    const diffPct = measured > 0 ? ((predictedVm - measured) / measured) * 100 : null;
    residuals.push({ id: m.id, commune: m.commune, measured, predictedVm, diffPct });
    console.log(
      `  ${String(m.id).padEnd(7)} ${String(m.commune).padEnd(20)} ${String(measured.toFixed(3)).padStart(12)}  ${String(predictedVm.toFixed(3)).padStart(13)}  ${String(diffPct !== null ? diffPct.toFixed(1) + '%' : 'N/A').padStart(8)}`
    );
  }

  // Stats simples
  const valid = residuals.filter((r) => r.diffPct !== null && isFinite(r.diffPct));
  const pcts = valid.map((r) => r.diffPct).sort((a, b) => a - b);
  if (pcts.length > 0) {
    const median = pcts[Math.floor(pcts.length / 2)];
    const min = pcts[0], max = pcts[pcts.length - 1];
    const mean = pcts.reduce((a, b) => a + b, 0) / pcts.length;
    console.log('───────────────────────────────────────────────────────────────────────');
    console.log(`  Stats résidu relatif (% diff) : n=${pcts.length}  min=${min.toFixed(1)}%  median=${median.toFixed(1)}%  mean=${mean.toFixed(1)}%  max=${max.toFixed(1)}%`);
  }
  console.log('');
  console.log('NOTE : ces résidus sont un signal exploratoire. Le moteur calcRF utilise');
  console.log('un modèle propagation simplifié + densité de fond ; les mesures EXEM');
  console.log('sont en champ rayonné réel. L\'objectif est de quantifier le biais, pas');
  console.log('de prétendre matcher au volt près.');

  await harness.close();
}

// ─── WS2 — Sweep sensibilité EXPERT_WEIGHTS / EXPERT_BOUNDS ─────────────────

async function modeSensitivity() {
  const fp = join(REPO_ROOT, 'tests', 'fixtures', 'known-values-pre-extraction.json');
  const fixture = JSON.parse(await readFile(fp, 'utf-8'));
  // Échantillon : 5 points (1 urbain, 1 rural, 1 éloigné, 1 site_ref, 1 complement)
  const samples = ['elf-urbain-ajaccio-centre', 'elf-rural-hta-castagniccia', 'elf-eloign-monte-cinto-sommet', 'elf-site-ref-filitosa', 'complement-thermal-pietrapola'];
  const picks = fixture.points.filter((p) => samples.includes(p.id));

  const harness = await createHarness();
  console.log('Harness ready.');
  console.log('');

  const defaults = await harness.getExpertDefaults();
  console.log('GELE-001 (lecture seule) :');
  console.log('  EXPERT_WEIGHTS_DEFAULT :', JSON.stringify(defaults.weights));
  console.log('  EXPERT_BOUNDS_DEFAULT  :', JSON.stringify(defaults.bounds));
  console.log('');

  // Grille de pondérations à somme = 1
  const weightsGrid = [
    { M: 0.6, RF: 0.2, I: 0.2 },
    { M: 0.4, RF: 0.4, I: 0.2 }, // défaut GELE-001
    { M: 0.2, RF: 0.6, I: 0.2 },
    { M: 0.4, RF: 0.2, I: 0.4 },
    { M: 0.2, RF: 0.2, I: 0.6 },
  ];

  console.log('Sweep pondérations (5 combinaisons × ' + picks.length + ' points = ' + (5 * picks.length) + ' éval) :');
  console.log('─────────────────────────────────────────────────────────────────────────────');
  console.log('  point                                         index (M=…, RF=…, I=…)');
  for (const p of picks) {
    await harness.setRuntimeState({ curKp: fixture.runtime_state_at_capture.curKp, chargeFacteur: fixture.runtime_state_at_capture.chargeFacteur });
    const v2 = await harness.calcAll_v2(p.lat, p.lon, p.options || {});
    const indices = [];
    for (const w of weightsGrid) {
      const r = await harness.computeExpertComposite(v2, w, undefined);
      indices.push(`${w.M.toFixed(1)}/${w.RF.toFixed(1)}/${w.I.toFixed(1)}=${r.index.toFixed(3)}`);
    }
    console.log(`  ${p.id.padEnd(45)} ${indices.join('  ')}`);
  }
  console.log('');
  console.log('Lecture : pour chaque point, l\'index composite varie selon le poids dominant.');
  console.log('Un point est dit "robuste" si l\'index reste stable (±0.05) sur l\'enveloppe ;');
  console.log('"volatil" si l\'index bascule de tier (0-0.33 / 0.33-0.66 / 0.66-1.0).');

  await harness.close();
}

// ─── CLI dispatch ──────────────────────────────────────────────────────────

const mode = process.argv[2];
if (!mode) {
  console.log('Tellux blindage harness — playground (exemples WS2)');
  console.log('');
  console.log('Modes disponibles :');
  console.log('  node playground.mjs rf-residuals    Résidus RF sur 30 mesures EXEM/ANFR');
  console.log('  node playground.mjs sensitivity     Sweep EXPERT_WEIGHTS sur 5 points');
  process.exit(0);
} else if (mode === 'rf-residuals') {
  await modeRfResiduals();
} else if (mode === 'sensitivity') {
  await modeSensitivity();
} else {
  console.error('Mode inconnu : ' + mode);
  process.exit(2);
}
