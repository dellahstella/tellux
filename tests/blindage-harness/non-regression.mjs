// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Non-régression sur les 25 points de la fixture pre-extraction
// Création : 2026-06-06 · feat/blindage-harness
// ═══════════════════════════════════════════════════════════════════════════
//
// Boucle :
//   1. Charge tests/fixtures/known-values-pre-extraction.json
//   2. Crée un harness Playwright (cf. harness.mjs)
//   3. Pour chaque point : force le runtime_state (curKp + chargeFacteur),
//      appelle calcAll_v2(lat, lon, options), compare au expected
//   4. Reporte PASS/DIFF avec le diff exhaustif des écarts (chemin, valeur
//      attendue, valeur observée, ratio absolu/relatif)
//
// Champs ignorés (cf. notes_de_capture de la fixture) :
//   - expected.metadata.timestamp                (horodatage de capture)
//   - expected.metadata.kp_snapshot.timestamp    (idem)
//   - expected.metadata.kp_snapshot.value        (dépend de NOAA temps réel,
//                                                 mais comme on force curKp,
//                                                 on devrait pouvoir le
//                                                 comparer. On l'ignore par
//                                                 prudence — la fixture note
//                                                 l'exclusion.)
//
// Tolérance numérique : epsilon par défaut 1e-9 (les valeurs sont déjà
// arrondies par calcAll_v2). Configurable via NUMERIC_EPS env.
//
// ⚠ Tout écart est SIGNALÉ. La fixture N'EST PAS modifiée. Un écart est un
// signal à diagnostiquer (drift volontaire du moteur, dérive numérique,
// reproductibilité de runtime, etc.).
// ═══════════════════════════════════════════════════════════════════════════

import { readFile } from 'node:fs/promises';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { join, resolve as pathResolve } from 'node:path';
import { createHarness } from './harness.mjs';

const __filename = fileURLToPath(import.meta.url);
const HARNESS_DIR = pathResolve(__filename, '..');
const REPO_ROOT = pathResolve(HARNESS_DIR, '..', '..');
const FIXTURE_PATH = join(REPO_ROOT, 'tests', 'fixtures', 'known-values-pre-extraction.json');

const NUMERIC_EPS = Number(process.env.NUMERIC_EPS) || 1e-9;
const LIMIT_POINTS = Number(process.env.LIMIT_POINTS) || 0; // 0 = all
const SHOW_PASSES = process.env.VERBOSE === '1';

const IGNORED_PATHS = new Set([
  'metadata.timestamp',
  'metadata.kp_snapshot.timestamp',
  'metadata.kp_snapshot.value',
]);

// ─── Deep diff ───────────────────────────────────────────────────────────────

function isObject(x) {
  return x !== null && typeof x === 'object' && !Array.isArray(x);
}

function pathJoin(prefix, key) {
  return prefix ? prefix + '.' + key : String(key);
}

/**
 * Walk expected vs actual, collecting diffs at each leaf where values disagree.
 * @returns {Array<{path: string, expected: any, actual: any, kind: string}>}
 */
function diffDeep(expected, actual, prefix = '') {
  const diffs = [];

  if (IGNORED_PATHS.has(prefix)) return diffs;

  // Both null/undefined
  if (expected === null && actual === null) return diffs;
  if (expected === undefined && actual === undefined) return diffs;

  // One is null, the other isn't
  if (expected === null || actual === null || expected === undefined || actual === undefined) {
    if (expected !== actual) {
      diffs.push({ path: prefix || '<root>', expected, actual, kind: 'null-mismatch' });
    }
    return diffs;
  }

  // Numbers — tolerate epsilon
  if (typeof expected === 'number' && typeof actual === 'number') {
    if (Number.isNaN(expected) && Number.isNaN(actual)) return diffs;
    if (Number.isNaN(expected) || Number.isNaN(actual)) {
      diffs.push({ path: prefix || '<root>', expected, actual, kind: 'nan-mismatch' });
      return diffs;
    }
    if (!isFinite(expected) || !isFinite(actual)) {
      if (expected !== actual) {
        diffs.push({ path: prefix || '<root>', expected, actual, kind: 'infinity-mismatch' });
      }
      return diffs;
    }
    const absDiff = Math.abs(expected - actual);
    const denom = Math.max(Math.abs(expected), Math.abs(actual), 1);
    const relDiff = absDiff / denom;
    if (absDiff > NUMERIC_EPS) {
      diffs.push({
        path: prefix || '<root>',
        expected,
        actual,
        kind: 'numeric-diff',
        absDiff,
        relDiff,
      });
    }
    return diffs;
  }

  // Strings / booleans — strict equality
  if (typeof expected === 'string' || typeof expected === 'boolean') {
    if (expected !== actual) {
      diffs.push({ path: prefix || '<root>', expected, actual, kind: 'value-mismatch' });
    }
    return diffs;
  }

  // Arrays
  if (Array.isArray(expected)) {
    if (!Array.isArray(actual)) {
      diffs.push({ path: prefix || '<root>', expected, actual, kind: 'type-mismatch (expected array)' });
      return diffs;
    }
    if (expected.length !== actual.length) {
      diffs.push({
        path: prefix || '<root>',
        expected: `array(len=${expected.length})`,
        actual: `array(len=${actual.length})`,
        kind: 'length-mismatch',
      });
    }
    const maxLen = Math.max(expected.length, actual.length);
    for (let i = 0; i < maxLen; i++) {
      diffs.push(...diffDeep(expected[i], actual[i], pathJoin(prefix, '[' + i + ']')));
    }
    return diffs;
  }

  // Objects
  if (isObject(expected)) {
    if (!isObject(actual)) {
      diffs.push({ path: prefix || '<root>', expected, actual, kind: 'type-mismatch (expected object)' });
      return diffs;
    }
    const allKeys = new Set([...Object.keys(expected), ...Object.keys(actual)]);
    for (const key of allKeys) {
      diffs.push(...diffDeep(expected[key], actual[key], pathJoin(prefix, key)));
    }
    return diffs;
  }

  // Fallback
  if (expected !== actual) {
    diffs.push({ path: prefix || '<root>', expected, actual, kind: 'unknown-mismatch' });
  }
  return diffs;
}

// ─── Main ────────────────────────────────────────────────────────────────────

function fmt(v) {
  if (v === null) return 'null';
  if (v === undefined) return 'undefined';
  if (typeof v === 'object') return JSON.stringify(v).slice(0, 120);
  return String(v);
}

function summarizeDiffs(diffs, max = 12) {
  const out = diffs.slice(0, max).map((d) => {
    const tail = d.kind === 'numeric-diff'
      ? ` (abs=${d.absDiff.toExponential(3)}, rel=${(d.relDiff * 100).toFixed(3)}%)`
      : '';
    return `      ${d.path}: expected=${fmt(d.expected)} actual=${fmt(d.actual)}${tail}`;
  });
  if (diffs.length > max) out.push(`      ... (+${diffs.length - max} more)`);
  return out.join('\n');
}

async function main() {
  const t0 = Date.now();
  console.log('────────────────────────────────────────────────────────────────────');
  console.log('Tellux blindage harness — non-régression sur known-values-pre-extraction');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log('Fixture :', FIXTURE_PATH);
  console.log('Epsilon numérique :', NUMERIC_EPS);
  console.log('Variables d\'environnement supportées :');
  console.log('  HARNESS_URL=https://tellux.pages.dev/app.html  (par défaut : serveur local)');
  console.log('  HARNESS_PORT=3779                              (port du serveur local)');
  console.log('  HARNESS_HEADFUL=1                              (lance Chromium visible)');
  console.log('  NUMERIC_EPS=1e-6                               (tolérance numérique)');
  console.log('  LIMIT_POINTS=5                                 (limiter aux N premiers)');
  console.log('  VERBOSE=1                                      (afficher aussi les PASS)');
  console.log('');

  // Charger fixture
  const raw = await readFile(FIXTURE_PATH, 'utf-8');
  const fixture = JSON.parse(raw);
  const points = LIMIT_POINTS > 0 ? fixture.points.slice(0, LIMIT_POINTS) : fixture.points;
  console.log(`Fixture : ${fixture.points.length} points (${fixture.captured_at_revision}, ${fixture.captured_at})`);
  console.log(`État à reproduire : curKp=${fixture.runtime_state_at_capture.curKp}, chargeFacteur=${fixture.runtime_state_at_capture.chargeFacteur}`);
  console.log(`Exécution sur ${points.length} point(s)`);
  console.log('');

  // Créer harness — on freeze l'horloge à la date de capture pour
  // reproduire `calcSq(lat)` qui lit `new Date()` directement (app.html:3012).
  console.log('Démarrage harness Playwright (Date frozen à', fixture.captured_at, ')...');
  const harness = await createHarness({ freezeTime: fixture.captured_at });
  console.log('Boot OK. URL :', harness._internal.url);
  const stateAfterBoot = await harness.getRuntimeState();
  console.log('État runtime au boot :', JSON.stringify(stateAfterBoot));
  console.log('');

  // Forcer le runtime_state pour reproductibilité
  const wantState = fixture.runtime_state_at_capture;
  const setState = await harness.setRuntimeState({
    curKp: wantState.curKp,
    chargeFacteur: wantState.chargeFacteur,
  });
  console.log('Runtime state forcé :', JSON.stringify(setState));
  console.log('');

  // Boucle de comparaison
  let nPass = 0;
  let nDiff = 0;
  let nErr = 0;
  const allFails = [];
  for (let i = 0; i < points.length; i++) {
    const p = points[i];
    // Reset runtime state per point in case a previous calc has mutated something
    await harness.setRuntimeState({ curKp: wantState.curKp, chargeFacteur: wantState.chargeFacteur });

    let actual;
    try {
      actual = await harness.calcAll_v2(p.lat, p.lon, p.options || {});
    } catch (e) {
      nErr++;
      console.log(`  [${i + 1}/${points.length}]  ERR  ${p.id}  (${p.lat.toFixed(4)}, ${p.lon.toFixed(4)})  → ${e?.message || e}`);
      allFails.push({ id: p.id, kind: 'error', error: String(e?.message || e) });
      continue;
    }

    if (p.expected === undefined || p.expected === null) {
      console.log(`  [${i + 1}/${points.length}]  SKIP ${p.id}  (pas de champ expected dans la fixture)`);
      continue;
    }

    if (p.capture_error) {
      console.log(`  [${i + 1}/${points.length}]  SKIP ${p.id}  (capture_error présent dans la fixture : ${JSON.stringify(p.capture_error)})`);
      continue;
    }

    const diffs = diffDeep(p.expected, actual, '');
    if (diffs.length === 0) {
      nPass++;
      if (SHOW_PASSES) {
        console.log(`  [${i + 1}/${points.length}]  PASS ${p.id}`);
      }
    } else {
      nDiff++;
      console.log(`  [${i + 1}/${points.length}]  DIFF ${p.id}  (${p.lat.toFixed(4)}, ${p.lon.toFixed(4)})  ${diffs.length} écart(s)`);
      console.log(summarizeDiffs(diffs));
      allFails.push({ id: p.id, kind: 'diff', count: diffs.length, sample: diffs.slice(0, 5) });
    }
  }

  // Diagnostics console
  const diag = harness.diagnostics();
  if (diag.consoleErrors.length || diag.consoleWarns.length) {
    console.log('');
    console.log('--- Console navigateur ---');
    if (diag.consoleErrors.length) {
      console.log('Erreurs (' + diag.consoleErrors.length + ') :');
      for (const e of diag.consoleErrors.slice(0, 6)) console.log('  ! ' + e);
      if (diag.consoleErrors.length > 6) console.log('  ... (+' + (diag.consoleErrors.length - 6) + ' more)');
    }
    if (diag.consoleWarns.length) {
      console.log('Warnings (' + diag.consoleWarns.length + ') :');
      for (const w of diag.consoleWarns.slice(0, 6)) console.log('  ~ ' + w);
      if (diag.consoleWarns.length > 6) console.log('  ... (+' + (diag.consoleWarns.length - 6) + ' more)');
    }
  }

  await harness.close();

  // Résumé
  const dt = (Date.now() - t0) / 1000;
  console.log('');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log(`Résultat : ${nPass} PASS · ${nDiff} DIFF · ${nErr} ERR  (sur ${points.length} points, ${dt.toFixed(1)}s)`);
  console.log('────────────────────────────────────────────────────────────────────');

  // Exit code : 0 si tout PASS, 1 si DIFF ou ERR
  if (nDiff > 0 || nErr > 0) {
    process.exit(1);
  }
}

main().catch((e) => {
  console.error('Erreur fatale du harness :', e?.stack || e);
  process.exit(2);
});
