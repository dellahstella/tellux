/**
 * ══════════════════════════════════════════════════════════════════════════════
 * Tellux — Tests de non-régression · v2 phase 1 refactor
 * Tâche 4.10 · 2026-04-19
 * ══════════════════════════════════════════════════════════════════════════════
 *
 * Usage : coller dans la console navigateur sur la page app.html déployée,
 *         ou exécuter via l'onglet Console des DevTools après chargement complet.
 *
 * Ce fichier vérifie :
 *   (A) Invariants de structure — calcAll() retourne les champs attendus (legacy + v2)
 *   (B) Cohérence ELF — calcAll().human ≈ calcAll().v2.domains.magnetic.elf.B_total_nT
 *   (C) Typage — tous les champs numériques sont bien des nombres non-NaN
 *   (D) RF — v2.domains.rf.S_total_uW_m2 est un nombre ≥ 0
 *   (E) Heritage — calcHeritageDensity() retourne l'objet structuré v2
 *   (F) Substrate — calcSubstrateContext() retourne lithologie + susceptibilité
 *   (G) Deprecated — calcPiezoScore() est toujours appelable (backward-compat)
 *
 * Points test : 5 coordonnées représentatives de la Corse
 *   1. Ajaccio          (41.919, 8.738)  — zone urbaine dense, réseau HTA fort
 *   2. Bastia           (42.703, 9.450)  — ville + port + Cap Corse
 *   3. Corte            (42.154, 9.193)  — intérieur, faible anthropique
 *   4. Porto-Vecchio    (41.578, 9.267)  — littoral sud, patrimoine fort
 *   5. Cauria (alignements) (41.550, 8.850) — zone mégalithique dense, granit biotite
 *
 * RÉSULTATS DE RÉFÉRENCE (pre-merge, run 2026-04-19 sur docs/corpus-infrastructure) :
 *   Voir section BASELINE_RESULTS en bas de fichier.
 * ══════════════════════════════════════════════════════════════════════════════
 */

// ─── Configuration ────────────────────────────────────────────────────────────
const TEST_POINTS = [
  { name: 'Ajaccio',        lat: 41.919, lon: 8.738  },
  { name: 'Bastia',         lat: 42.703, lon: 9.450  },
  { name: 'Corte',          lat: 42.154, lon: 9.193  },
  { name: 'Porto-Vecchio',  lat: 41.578, lon: 9.267  },
  { name: 'Cauria',         lat: 41.550, lon: 8.850  },
];

// Tolérance pour la comparaison human vs ELF (les deux calculent Biot-Savart
// mais calcHuman inclut calcSimDelta et les FH_POINTS en mode intégral,
// tandis que calcMagneticELF est le refactor pur sans FH sur la même base)
const ELF_TOLERANCE_NT   = 100; // nT — acceptable pendant la transition (delta = FH)
const ELF_MAX_DIVERGENCE = 0.5; // ratio — les deux doivent être du même ordre de grandeur

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

// ─── Suite de tests ───────────────────────────────────────────────────────────
function runNonRegression() {
  console.group('══ Tellux — Tests non-régression v2 phase 1 ══');
  const results = { pass: 0, fail: 0, errors: [] };

  // ── (G) Fonctions dépréciées accessibles ──────────────────────────────────
  console.group('G · Backward-compat deprecated functions');
  const g1 = assert(typeof calcPiezoScore === 'function', 'calcPiezoScore est encore une fonction');
  const g2 = assert(typeof calcHuman === 'function', 'calcHuman est encore une fonction');
  [g1, g2].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (F) calcSubstrateContext ───────────────────────────────────────────────
  console.group('F · calcSubstrateContext structure');
  const sPoint = TEST_POINTS[4]; // Cauria — granit biotite attendu
  let subst;
  try { subst = calcSubstrateContext(sPoint.lat, sPoint.lon); } catch(e) { subst = null; }
  const f1 = assert(subst !== null, 'calcSubstrateContext ne lève pas d\'exception à Cauria');
  const f2 = assert(subst && typeof subst.lithology === 'string', 'subst.lithology est une chaîne', subst?.lithology);
  const f3 = assert(subst && isFiniteNum(subst.susceptibility_nT), 'subst.susceptibility_nT est un nombre fini', subst?.susceptibility_nT);
  const f4 = assert(subst && [1, 2, 3].includes(subst.radon_potential_class), 'subst.radon_potential_class ∈ {1,2,3}', subst?.radon_potential_class);
  const f5 = assert(subst && isFiniteNum(subst.distance_fault_m), 'subst.distance_fault_m est un nombre fini', subst?.distance_fault_m);
  const f6 = assert(subst && subst.lithology.includes('granit'), 'Cauria détectée en zone granitique', subst?.lithology);
  [f1,f2,f3,f4,f5,f6].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (E) calcHeritageDensity ────────────────────────────────────────────────
  console.group('E · calcHeritageDensity structure');
  const hPoint = TEST_POINTS[4]; // Cauria — densité patrimoniale maximale attendue
  let hDens;
  try { hDens = calcHeritageDensity(hPoint.lat, hPoint.lon); } catch(e) { hDens = null; }
  const e1 = assert(hDens !== null, 'calcHeritageDensity ne lève pas d\'exception à Cauria');
  const e2 = assert(hDens && isFiniteNum(hDens.density_sites_km2), 'hDens.density_sites_km2 est un nombre fini', hDens?.density_sites_km2);
  const e3 = assert(hDens && hDens.density_sites_km2 > 0, 'Cauria : densité patrimoniale > 0', hDens?.density_sites_km2);
  const e4 = assert(hDens && isFiniteNum(hDens._score_legacy), 'hDens._score_legacy (backward-compat) est un nombre fini', hDens?._score_legacy);
  const e5 = assert(hDens && hDens.confidence === 'high', 'hDens.confidence === "high"', hDens?.confidence);
  const e6 = assert(hDens && hDens.nearest_site !== null, 'hDens.nearest_site non-null à Cauria', hDens?.nearest_site);
  [e1,e2,e3,e4,e5,e6].forEach(r => { r.pass ? results.pass++ : (results.fail++, results.errors.push(r)); });
  console.groupEnd();

  // ── (A)(B)(C)(D) calcAll par point ────────────────────────────────────────
  TEST_POINTS.forEach(pt => {
    console.group(`Point · ${pt.name} (${pt.lat}, ${pt.lon})`);
    let all;
    try { all = calcAll(pt.lat, pt.lon); } catch(e) { all = null; console.error('calcAll a levé une exception:', e); }

    // (A) Structure legacy
    const a1 = assert(all !== null, 'calcAll ne lève pas d\'exception');
    const a2 = assert(all && isFiniteNum(all.human),    `all.human est un nombre fini (${all?.human} nT)`);
    const a3 = assert(all && isFiniteNum(all.water),    `all.water est un nombre fini (${all?.water})`);
    const a4 = assert(all && isFiniteNum(all.geo),      `all.geo est un nombre fini (${all?.geo} nT)`);
    const a5 = assert(all && isFiniteNum(all.score),    `all.score est un nombre fini (${all?.score})`);
    const a6 = assert(all && all.score >= 0,            `all.score ≥ 0 (${all?.score})`);

    // (A) Structure v2
    const a7 = assert(all && typeof all.v2 === 'object' && all.v2 !== null, 'all.v2 est un objet');
    const a8 = assert(all && all.v2?.domains?.magnetic?.elf !== undefined, 'all.v2.domains.magnetic.elf existe');
    const a9 = assert(all && all.v2?.domains?.rf !== undefined, 'all.v2.domains.rf existe');
    const a10 = assert(all && all.v2?.context?.substrate !== undefined, 'all.v2.context.substrate existe');
    const a11 = assert(all && all.v2?.context?.heritage !== undefined, 'all.v2.context.heritage existe');
    const a12 = assert(all && all.v2?.metadata?.timestamp !== undefined, 'all.v2.metadata.timestamp existe');

    // (C) Types numériques v2
    const elfNT = all?.v2?.domains?.magnetic?.elf?.B_total_nT;
    const rfUW  = all?.v2?.domains?.rf?.S_total_uW_m2;
    const c1 = assert(isFiniteNum(elfNT), `v2.elf.B_total_nT est un nombre fini (${elfNT} nT)`);
    const c2 = assert(isFiniteNum(rfUW),  `v2.rf.S_total_uW_m2 est un nombre fini (${rfUW} µW/m²)`);

    // (D) RF ≥ 0
    const d1 = assert(rfUW >= 0, `v2.rf.S_total_uW_m2 ≥ 0 (${rfUW})`);

    // (B) Cohérence human ≈ ELF
    // calcHuman = calcMagneticELF + calcSimDelta + FH_POINTS
    // calcMagneticELF = HTA + PROD_ELECTRIQUE + BT_ZONES (sans FH_POINTS séparés)
    // Δ attendu = FH contribution + bruit fond CartoRadio
    const humanLegacy = all?.human ?? 0;
    const elfNew = elfNT ?? 0;
    const ratio = elfNew > 0 ? humanLegacy / elfNew : (humanLegacy === 0 ? 1 : 99);
    const b1 = assert(
      ratio > ELF_MAX_DIVERGENCE && ratio < (1 / ELF_MAX_DIVERGENCE),
      `human/ELF ratio dans les bornes [${ELF_MAX_DIVERGENCE}–${1/ELF_MAX_DIVERGENCE}] → ratio=${ratio.toFixed(2)}`,
      { humanLegacy, elfNew, ratio: ratio.toFixed(3) }
    );

    [a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,c1,c2,d1,b1].forEach(r => {
      r.pass ? results.pass++ : (results.fail++, results.errors.push({ point: pt.name, ...r }));
    });
    console.groupEnd();
  });

  // ── Résumé ─────────────────────────────────────────────────────────────────
  console.group('══ Résumé ══');
  console.log(`✅ Réussis  : ${results.pass}`);
  console.log(`❌ Échoués  : ${results.fail}`);
  if (results.errors.length > 0) {
    console.warn('Erreurs détaillées :', results.errors);
  } else {
    console.log('🎉 Tous les tests passent — PR prête.');
  }
  console.groupEnd();
  console.groupEnd();

  return results;
}

// ─── Exécution immédiate ───────────────────────────────────────────────────────
const NR_RESULTS = runNonRegression();

/**
 * ══════════════════════════════════════════════════════════════════════════════
 * BASELINE_RESULTS — valeurs de référence (run 2026-04-19)
 * À mettre à jour si les données sources changent (HTA_SEGS, PROD_ELECTRIQUE, etc.)
 * ══════════════════════════════════════════════════════════════════════════════
 *
 * Point            | human (nT)  | water  | geo (nT) | score  | elf_nT | rf_µW
 * ─────────────────┼─────────────┼────────┼──────────┼────────┼────────┼──────
 * Ajaccio          | ~290–350    | 0–50   | ~18      | ~310+  | ~200+  | ~80+
 * Bastia           | ~200–280    | 0      | ~5       | ~210+  | ~170+  | ~100+
 * Corte            | ~80–150     | 0      | ~20      | ~100+  | ~60+   | ~40+
 * Porto-Vecchio    | ~60–120     | 0      | ~15      | ~70+   | ~50+   | ~30+
 * Cauria           | ~20–60      | 0      | ~25–35   | ~30+   | ~15+   | ~15+
 *
 * Notes :
 * - Les plages sont larges car certaines contributions dépendent de chargeFacteur (global).
 * - Cauria : geo élevé (granit biotite, susceptibilité ~25-35 nT), heritage dense.
 * - Bastia : proche de FH Col de Teghime (200 µW/m²), contribution RF forte.
 * - Ajaccio : nœud HTA réseau SEI → human fort.
 *
 * INVARIANTS FORTS (ne doivent jamais être violés après merge) :
 * 1. all.score est toujours un entier ≥ 0 et isFinite
 * 2. all.v2 est toujours un objet avec la structure complète (domains + context + metadata)
 * 3. v2.domains.magnetic.elf.B_total_nT ≥ 0
 * 4. v2.domains.rf.S_total_uW_m2 ≥ 0
 * 5. calcHeritageDensity()._score_legacy est toujours un nombre (backward-compat Tâche 4.5)
 * 6. calcPiezoScore() est toujours appelable sans exception (ticket B-corpus-hypotheses)
 * ══════════════════════════════════════════════════════════════════════════════
 */
