/**
 * ══════════════════════════════════════════════════════════════════════════════
 * Tellux — Extension fixture regression test (35 points RF/gamma/ELF/M_static)
 * Créé : 2026-04-28
 * ══════════════════════════════════════════════════════════════════════════════
 *
 * ⚠️  PENDING — REQUIRES PHASE 0 ENGINE EXTRACTION
 *
 * Ce test est désactivé (tous les it() sont en skip) tant que le moteur n'est
 * pas extrait de app.html vers lib/tellux-engine.js (phase 0 du chantier
 * auto-affinage, cf. docs/auto-affinage-conception-v1.md §7 phase 0).
 *
 * Pour activer :
 *   1. Remplacer l'import ci-dessous par le chemin réel du module extrait.
 *   2. Retirer le marquage TODO:SKIP sur chaque it().
 *   3. Choisir un runner (node:test / vitest / jest) et ajouter package.json.
 *
 * Runner cible : node:test (zéro dépendance, cf. plan d'extraction §7.3)
 * Commande future : node --test tests/extension-regression.test.js
 *
 * Fixture : tests/fixtures/known-values-extension-coords.json
 *   - 35 points, captured_at_commit 1bf855d (main, 2026-04-28)
 *   - Champs exclus de la comparaison : voir NON_REPRODUCIBLE_PATHS ci-dessous
 * ══════════════════════════════════════════════════════════════════════════════
 */

// ─── Import moteur (PLACEHOLDER — à remplacer après phase 0) ─────────────────
// import { calcAll_v2 } from '../lib/tellux-engine/index.js';
// import { createEngineState } from '../lib/tellux-engine/loaders/node-loaders.js';
const calcAll_v2 = null;       // TODO:PHASE0 — décommenter l'import ci-dessus
const createEngineState = null; // TODO:PHASE0

// ─── Fixture ──────────────────────────────────────────────────────────────────
const path    = require('path');
const fs      = require('fs');
const FIXTURE = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'fixtures/known-values-extension-coords.json'), 'utf8')
);

// ─── Champs non reproductibles (repris du top-level de la fixture) ─────────────
// Format : chemin relatif à expected_values, séparateur '.'
// Exemples : 'metadata.timestamp' → obj.metadata.timestamp
const NON_REPRODUCIBLE_PATHS = (FIXTURE.non_reproducible_fields || [])
  .map(f => f
    .replace(/^expected_values\./, '')   // retirer le préfixe common
    .replace(/ \(.*\)$/, '')             // retirer les annotations parenthèses
  );
// Résultat attendu :
//   ['metadata.timestamp', 'metadata.kp_snapshot.timestamp', 'metadata.kp_snapshot.value']

// ─── Deep-equal avec exclusion de chemins ─────────────────────────────────────
/**
 * deepEqualExcluding(actual, expected, excludePaths, currentPath)
 *
 * Comparaison récursive stricte (===) entre actual et expected.
 * Les sous-chemins listés dans excludePaths sont silencieusement ignorés.
 * Retourne un tableau de différences [{path, actual, expected}].
 * Tableau vide = égalité.
 *
 * @param {*}      actual
 * @param {*}      expected
 * @param {string[]} excludePaths  - chemins à ignorer, séparés par '.'
 * @param {string}   currentPath   - chemin courant (usage interne récursif)
 * @returns {{path:string, actual:*, expected:*}[]}
 */
function deepEqualExcluding(actual, expected, excludePaths, currentPath = '') {
  const diffs = [];

  // Champ exclu → on passe
  if (excludePaths.includes(currentPath)) return diffs;

  // Types différents
  if (typeof actual !== typeof expected) {
    diffs.push({ path: currentPath, actual, expected });
    return diffs;
  }

  // null
  if (actual === null || expected === null) {
    if (actual !== expected) diffs.push({ path: currentPath, actual, expected });
    return diffs;
  }

  // Tableaux
  if (Array.isArray(actual) && Array.isArray(expected)) {
    if (actual.length !== expected.length) {
      diffs.push({ path: `${currentPath}.length`, actual: actual.length, expected: expected.length });
      return diffs;
    }
    for (let i = 0; i < actual.length; i++) {
      diffs.push(...deepEqualExcluding(actual[i], expected[i], excludePaths, `${currentPath}[${i}]`));
    }
    return diffs;
  }

  // Objets
  if (typeof actual === 'object') {
    const keys = new Set([...Object.keys(actual), ...Object.keys(expected)]);
    for (const k of keys) {
      const childPath = currentPath ? `${currentPath}.${k}` : k;
      if (excludePaths.includes(childPath)) continue;
      if (!(k in actual)) {
        diffs.push({ path: childPath, actual: undefined, expected: expected[k] });
      } else if (!(k in expected)) {
        diffs.push({ path: childPath, actual: actual[k], expected: undefined });
      } else {
        diffs.push(...deepEqualExcluding(actual[k], expected[k], excludePaths, childPath));
      }
    }
    return diffs;
  }

  // Primitives numériques : epsilon 1e-9
  if (typeof actual === 'number') {
    if (Math.abs(actual - expected) > 1e-9) {
      diffs.push({ path: currentPath, actual, expected });
    }
    return diffs;
  }

  // Autres primitives (string, boolean)
  if (actual !== expected) diffs.push({ path: currentPath, actual, expected });
  return diffs;
}

// ─── Suite de tests ───────────────────────────────────────────────────────────
// node:test API (activé quand node >= 18 + runner branché en phase 0)
// Pour l'instant : stub qui n'exécute rien mais valide la structure du fichier.

const SKIP_REASON = 'PENDING: moteur non encore extrait (phase 0 requis)';

/**
 * runExtensionRegressionTests()
 *
 * Point d'entrée principal.
 * - En mode stub (calcAll_v2 === null) : vérifie uniquement la structure de la
 *   fixture (champs présents, types, 35 points).
 * - En mode actif (calcAll_v2 importé) : compare chaque point à expected_values.
 */
function runExtensionRegressionTests() {
  console.group('══ Tellux — Extension regression (35 points RF/gamma/ELF/M_static) ══');

  // ── 0. Vérification structure fixture ──────────────────────────────────────
  console.group('0 · Structure fixture');
  _assert(Array.isArray(FIXTURE.points),           'fixture.points est un tableau');
  _assert(FIXTURE.points.length === 35,            `35 points présents (trouvé : ${FIXTURE.points.length})`);
  _assert(typeof FIXTURE.captured_at === 'string', 'captured_at présent');
  _assert(typeof FIXTURE.captured_at_commit === 'string', 'captured_at_commit présent');
  _assert(Array.isArray(FIXTURE.non_reproducible_fields), 'non_reproducible_fields présent');
  _assert(NON_REPRODUCIBLE_PATHS.length === 3,     `3 chemins non-reproductibles parsés (trouvé : ${NON_REPRODUCIBLE_PATHS.length})`);

  // Vérifier que tous les points ont expected_values non-null
  const nullCount = FIXTURE.points.filter(p => p.expected_values === null).length;
  _assert(nullCount === 0, `Tous les expected_values sont remplis (null count : ${nullCount})`);

  // Vérifier la répartition par domaine
  const byDomain = {};
  for (const p of FIXTURE.points) {
    byDomain[p.domain_priority] = (byDomain[p.domain_priority] || 0) + 1;
  }
  _assert(byDomain.RF        === 15, `15 points RF (trouvé : ${byDomain.RF})`);
  _assert(byDomain.I_gamma   === 10, `10 points I_gamma (trouvé : ${byDomain.I_gamma})`);
  _assert(byDomain.M_elf     === 8,  `8 points M_elf (trouvé : ${byDomain.M_elf})`);
  _assert(byDomain.M_static  === 2,  `2 points M_static (trouvé : ${byDomain.M_static})`);
  console.groupEnd();

  // ── 1. Tests de non-régression (SKIP jusqu'à phase 0) ─────────────────────
  console.group('1 · Non-régression point par point');
  console.warn(`⏸  ${SKIP_REASON}`);

  if (calcAll_v2 === null) {
    console.info('  → Tests sautés. Pour activer : extraire le moteur (lib/tellux-engine.js) et brancher l\'import en tête de fichier.');
    console.groupEnd();
    console.groupEnd();
    return;
  }

  // TODO:PHASE0 — Ce bloc s'exécute quand calcAll_v2 est importé.
  //
  // Initialisation de l'état du moteur (loaders Node.js) :
  //   const state = await createEngineState();
  //
  // Pour chaque point :
  let pass = 0, fail = 0;
  for (const pt of FIXTURE.points) {
    const actual = calcAll_v2(pt.lat, pt.lon, { altitude_m: 5, commune_info: null /*, state */ });
    const diffs  = deepEqualExcluding(actual, pt.expected_values, NON_REPRODUCIBLE_PATHS);
    if (diffs.length === 0) {
      console.log(`  ✅ ${pt.id} — ${pt.label}`);
      pass++;
    } else {
      console.error(`  ❌ ${pt.id} — ${pt.label}`);
      for (const d of diffs) {
        console.error(`       path: ${d.path} | actual: ${JSON.stringify(d.actual)} | expected: ${JSON.stringify(d.expected)}`);
      }
      fail++;
    }
  }
  console.log(`\n  Résultat : ${pass} ✅  ${fail} ❌  (total ${pass + fail})`);
  console.groupEnd();
  console.groupEnd();
}

// ─── Utilitaire assert interne ─────────────────────────────────────────────────
function _assert(cond, label) {
  if (cond) console.log(`  ✅ ${label}`);
  else      console.error(`  ❌ ${label}`);
}

// ─── Exécution ─────────────────────────────────────────────────────────────────
// En console navigateur : coller et appeler runExtensionRegressionTests()
// En Node.js (phase 0)  : node tests/extension-regression.test.js
if (typeof module !== 'undefined') {
  // Contexte Node.js — exécution directe
  runExtensionRegressionTests();
}
// Contexte navigateur — export global pour appel manuel
if (typeof window !== 'undefined') {
  window.runExtensionRegressionTests = runExtensionRegressionTests;
  console.info('Tellux regression test chargé. Appeler runExtensionRegressionTests() pour lancer.');
}
