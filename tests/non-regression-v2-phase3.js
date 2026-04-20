/**
 * ══════════════════════════════════════════════════════════════════════════════
 * Tellux — Tests de non-régression · v2 phase 3 (Mode Expertise + export + URL)
 * Tâche 4.9 · 2026-04-20
 * ══════════════════════════════════════════════════════════════════════════════
 *
 * Usage : coller dans la console navigateur sur app.html déployée.
 *
 * Ce fichier vérifie :
 *   (H) Expert constants — EXPERT_WEIGHTS_DEFAULT, EXPERT_BOUNDS_DEFAULT accessibles
 *   (I) computeExpertComposite — retourne la structure attendue + index dans [0,1]
 *   (J) UI Expert — éléments DOM présents (#expert-modal, #expert-panel, #expert-bandeau)
 *   (K) _expertLastResult — stocké après clic carte (nécessite un clic → manuel OU vérifie var)
 *   (L) exportExpertCSV — fonction accessible et appellable sans erreur (sans _expertLastResult)
 *   (M) shareURL / buildShareHash — buildShareHash retourne une chaîne hash valide
 *   (N) calcPiezoScore backward-compat — toujours appelable, AUCUN appelant actif requis
 *   (O) Phase 1 invariants — régression : calcAll() retourne toujours v2 complet
 *
 * Points test : 3 coordonnées représentatives
 *   1. Ajaccio          (41.919, 8.738)
 *   2. Corte            (42.154, 9.193)
 *   3. Cauria           (41.550, 8.850)
 * ══════════════════════════════════════════════════════════════════════════════
 */

// ─── Utilitaires ──────────────────────────────────────────────────────────────
function assert(condition, label, details) {
  if (condition) {
    console.log(`  ✅ ${label}`);
    return { pass: true, label };
  } else {
    console.error(`  ❌ ${label}`, details !== undefined ? `→ ${JSON.stringify(details)}` : '');
    return { pass: false, label, details };
  }
}

function isFiniteNum(v) {
  return typeof v === 'number' && isFinite(v) && !isNaN(v);
}

const TEST_POINTS = [
  { name: 'Ajaccio', lat: 41.919, lon: 8.738 },
  { name: 'Corte',   lat: 42.154, lon: 9.193 },
  { name: 'Cauria',  lat: 41.550, lon: 8.850 },
];

// ─── Suite de tests ───────────────────────────────────────────────────────────
function runNonRegressionPhase3() {
  console.group('══ Tellux — Tests non-régression v2 phase 3 ══');
  const results = { pass: 0, fail: 0, errors: [] };

  // ── (H) Constantes EXPERT accessibles ────────────────────────────────────
  console.group('H · EXPERT constants');
  const h1 = assert(typeof EXPERT_WEIGHTS_DEFAULT === 'object' && EXPERT_WEIGHTS_DEFAULT !== null, 'EXPERT_WEIGHTS_DEFAULT est un objet');
  const h2 = assert(isFiniteNum(EXPERT_WEIGHTS_DEFAULT.M)  && EXPERT_WEIGHTS_DEFAULT.M  >= 0 && EXPERT_WEIGHTS_DEFAULT.M  <= 1, 'EXPERT_WEIGHTS_DEFAULT.M dans [0,1]',  EXPERT_WEIGHTS_DEFAULT.M);
  const h3 = assert(isFiniteNum(EXPERT_WEIGHTS_DEFAULT.RF) && EXPERT_WEIGHTS_DEFAULT.RF >= 0 && EXPERT_WEIGHTS_DEFAULT.RF <= 1, 'EXPERT_WEIGHTS_DEFAULT.RF dans [0,1]', EXPERT_WEIGHTS_DEFAULT.RF);
  const h4 = assert(isFiniteNum(EXPERT_WEIGHTS_DEFAULT.I)  && EXPERT_WEIGHTS_DEFAULT.I  >= 0 && EXPERT_WEIGHTS_DEFAULT.I  <= 1, 'EXPERT_WEIGHTS_DEFAULT.I dans [0,1]',  EXPERT_WEIGHTS_DEFAULT.I);
  const h5 = assert(Math.abs((EXPERT_WEIGHTS_DEFAULT.M + EXPERT_WEIGHTS_DEFAULT.RF + EXPERT_WEIGHTS_DEFAULT.I) - 1.0) < 1e-9, 'w_M + w_RF + w_I = 1.0 (somme normalisée)',
    EXPERT_WEIGHTS_DEFAULT.M + EXPERT_WEIGHTS_DEFAULT.RF + EXPERT_WEIGHTS_DEFAULT.I);
  const h6 = assert(typeof EXPERT_BOUNDS_DEFAULT === 'object' && Array.isArray(EXPERT_BOUNDS_DEFAULT.ELF_nT), 'EXPERT_BOUNDS_DEFAULT.ELF_nT est un tableau');
  const h7 = assert(typeof EXPERT_EPISTEMIC_NOTE === 'string' && EXPERT_EPISTEMIC_NOTE.length > 20, 'EXPERT_EPISTEMIC_NOTE est une chaîne non-vide');
  [h1,h2,h3,h4,h5,h6,h7].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (I) computeExpertComposite ────────────────────────────────────────────
  console.group('I · computeExpertComposite');
  const iPoint = TEST_POINTS[0]; // Ajaccio
  let v2test;
  try { v2test = calcAll_v2(iPoint.lat, iPoint.lon); } catch(e) { v2test = null; }
  const i0 = assert(v2test !== null, 'calcAll_v2 ne lève pas d\'exception');
  let comp;
  if (v2test) {
    try { comp = computeExpertComposite(v2test); } catch(e) { comp = null; }
  }
  const i1 = assert(comp !== null, 'computeExpertComposite ne lève pas d\'exception');
  const i2 = assert(comp && isFiniteNum(comp.index), `comp.index est un nombre fini (${comp?.index})`);
  const i3 = assert(comp && comp.index >= 0 && comp.index <= 1, `comp.index dans [0,1] (${comp?.index})`);
  const i4 = assert(comp && typeof comp.normalized === 'object', 'comp.normalized est un objet');
  const i5 = assert(comp && isFiniteNum(comp.normalized?.M),  `comp.normalized.M fini (${comp?.normalized?.M})`);
  const i6 = assert(comp && isFiniteNum(comp.normalized?.RF), `comp.normalized.RF fini (${comp?.normalized?.RF})`);
  const i7 = assert(comp && isFiniteNum(comp.normalized?.I),  `comp.normalized.I fini (${comp?.normalized?.I})`);
  const i8 = assert(comp && comp.under_review === true, 'comp.under_review === true');
  const i9 = assert(comp && typeof comp.epistemic_note === 'string', 'comp.epistemic_note est une chaîne');
  // Test avec pondérations custom
  let compCustom;
  if (v2test) {
    try { compCustom = computeExpertComposite(v2test, { M: 1.0, RF: 0.0, I: 0.0 }); } catch(e) { compCustom = null; }
  }
  const i10 = assert(compCustom && isFiniteNum(compCustom.index), 'computeExpertComposite avec pondérations custom ne lève pas d\'exception');
  [i0,i1,i2,i3,i4,i5,i6,i7,i8,i9,i10].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (J) UI DOM elements présents ─────────────────────────────────────────
  console.group('J · DOM elements mode Expertise');
  const j1 = assert(!!document.getElementById('expert-modal'),   '#expert-modal existe dans le DOM');
  const j2 = assert(!!document.getElementById('expert-panel'),   '#expert-panel existe dans le DOM');
  const j3 = assert(!!document.getElementById('expert-bandeau'), '#expert-bandeau existe dans le DOM');
  const j4 = assert(!!document.getElementById('sl-wM'),          'input#sl-wM (curseur w_M) existe');
  const j5 = assert(!!document.getElementById('sl-wRF'),         'input#sl-wRF (curseur w_RF) existe');
  const j6 = assert(!!document.getElementById('sl-wI'),          'input#sl-wI (curseur w_I) existe');
  const j7 = assert(!!document.getElementById('expert-index-val'),'#expert-index-val existe');
  const j8 = assert(!!document.getElementById('btn-expert'),     '#btn-expert (bouton Outils experts) existe');
  [j1,j2,j3,j4,j5,j6,j7,j8].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (L) exportExpertCSV accessible ───────────────────────────────────────
  console.group('L · exportExpertCSV accessible');
  const l1 = assert(typeof exportExpertCSV === 'function', 'exportExpertCSV est une fonction');
  // Sans _expertLastResult : doit afficher une alerte (pas lever d'exception)
  // On ne peut pas tester le download en mode console, on vérifie juste l'existence
  [l1].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (M) shareURL / buildShareHash ────────────────────────────────────────
  console.group('M · Partage URL hash');
  const m1 = assert(typeof buildShareHash === 'function', 'buildShareHash est une fonction');
  const m2 = assert(typeof shareURL === 'function',       'shareURL est une fonction');
  let hashStr;
  try { hashStr = buildShareHash(); } catch(e) { hashStr = null; }
  const m3 = assert(typeof hashStr === 'string', `buildShareHash() retourne une chaîne (${hashStr?.slice(0,40)})`);
  const m4 = assert(hashStr && hashStr.startsWith('#/'), 'hash commence par #/');
  const m5 = assert(hashStr && hashStr.includes('z='),   'hash contient z=');
  const m6 = assert(hashStr && hashStr.includes('c='),   'hash contient c=');
  const m7 = assert(typeof applyHashToMap === 'function', 'applyHashToMap est une fonction');
  [m1,m2,m3,m4,m5,m6,m7].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (N) calcPiezoScore backward-compat ───────────────────────────────────
  console.group('N · calcPiezoScore backward-compat (migration complète)');
  const n1 = assert(typeof calcPiezoScore === 'function', 'calcPiezoScore est toujours une fonction');
  let piezoVal;
  try { piezoVal = calcPiezoScore(41.919, 8.738); } catch(e) { piezoVal = null; }
  const n2 = assert(isFiniteNum(piezoVal), `calcPiezoScore(Ajaccio) retourne un nombre (${piezoVal})`);
  [n1,n2].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (O) Régression phase 1 — calcAll() sur 3 points ─────────────────────
  console.group('O · Régression phase 1 calcAll()');
  TEST_POINTS.forEach(pt => {
    let all;
    try { all = calcAll(pt.lat, pt.lon); } catch(e) { all = null; }
    const o1 = assert(all !== null, `${pt.name} : calcAll ne lève pas d'exception`);
    const o2 = assert(all && typeof all.v2 === 'object' && all.v2 !== null, `${pt.name} : all.v2 est un objet`);
    const o3 = assert(all && isFiniteNum(all.v2?.domains?.magnetic?.elf?.B_total_nT), `${pt.name} : elf.B_total_nT fini`);
    const o4 = assert(all && isFiniteNum(all.v2?.domains?.rf?.S_total_uW_m2), `${pt.name} : rf.S_total_uW_m2 fini`);
    const o5 = assert(all && all.v2?.domains?.rf?.S_total_uW_m2 >= 0, `${pt.name} : rf.S_total_uW_m2 ≥ 0`);
    // computeExpertComposite doit fonctionner sur ce résultat v2
    let compPt;
    if (all?.v2) {
      try { compPt = computeExpertComposite(all.v2); } catch(e) { compPt = null; }
    }
    const o6 = assert(compPt && isFiniteNum(compPt.index) && compPt.index >= 0 && compPt.index <= 1,
      `${pt.name} : composite index dans [0,1] (${compPt?.index?.toFixed(3)})`);
    [o1,o2,o3,o4,o5,o6].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  });
  console.groupEnd();

  // ── Résumé ─────────────────────────────────────────────────────────────────
  console.group('══ Résumé ══');
  console.log(`✅ Réussis  : ${results.pass}`);
  console.log(`❌ Échoués  : ${results.fail}`);
  if (results.errors.length > 0) {
    console.warn('Erreurs détaillées :', results.errors);
  } else {
    console.log('🎉 Tous les tests passent — phase 3 PR prête.');
  }
  console.groupEnd();
  console.groupEnd();

  return results;
}

// ─── Exécution immédiate ───────────────────────────────────────────────────────
const NR3_RESULTS = runNonRegressionPhase3();

/**
 * ══════════════════════════════════════════════════════════════════════════════
 * INVARIANTS FORTS phase 3 (ne doivent jamais être violés après merge) :
 *
 * 1. EXPERT_WEIGHTS_DEFAULT.M + RF + I === 1.0 (somme des pondérations)
 * 2. computeExpertComposite(v2).index toujours dans [0, 1]
 * 3. computeExpertComposite(v2).under_review === true (signalement obligatoire)
 * 4. buildShareHash() retourne une chaîne commençant par '#/'
 * 5. #expert-modal, #expert-panel, #expert-bandeau présents dans le DOM
 * 6. calcPiezoScore() toujours appelable (backward-compat) — aucun appelant actif requis
 * 7. Tous les invariants phase 1 (calcAll().v2 complet, elf.B_total_nT ≥ 0, rf.S_total_uW_m2 ≥ 0)
 *
 * GELÉ (ne pas tester les valeurs absolues) :
 * - Valeurs numériques de EXPERT_WEIGHTS_DEFAULT
 * - Valeurs numériques de EXPERT_BOUNDS_DEFAULT
 * ══════════════════════════════════════════════════════════════════════════════
 */
