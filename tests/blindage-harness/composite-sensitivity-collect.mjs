// ═══════════════════════════════════════════════════════════════════════════
// Tellux — WS2 sensibilité de l'index composite Expert (sweep en sandbox)
// Création : 2026-06-06 · feat/blindage-harness (WS2)
// ═══════════════════════════════════════════════════════════════════════════
//
// Caractérise la robustesse-au-choix de computeExpertComposite en faisant
// varier weights et bounds EN ARGUMENT (GELE-001 jamais modifié).
//
// Procédure :
//   1. Harness : pour chaque point de la fixture, récupère v2 (calcAll_v2)
//      avec freezeTime + runtime_state forcés.
//   2. Extrait elf_nT, rf_uW, gamma_nSv_h par point.
//   3. Sweep en Node (réplique fidèle de computeExpertComposite) :
//      - Monte Carlo Dirichlet(1,1,1) : 200 vecteurs poids sur le simplexe
//      - OAT perturbation poids ±0.1 / ±0.2 avec rebalance proportionnel
//      - Sweep bornes (×0.5 / ×1.0 / ×2.0 sur upper, lower inchangé) : 27 combos
//   4. Tier hypothétique [0,0.33) / [0.33,0.66) / [0.66,1.0] :
//      - Tier sous default
//      - % de sweeps où le tier change
//      - Rangs (1-25) sous default + dispersion des rangs sous sweep
//   5. Sortie JSON exhaustive sur stdout.
//
// ⚠ Ce script ne valide PAS les poids GELE-001. Il mesure combien le
// choix des poids/bornes pèse — donc combien la validation physicien
// importera quand elle sera faite. Cf. rapport associé pour cadrage.
// ═══════════════════════════════════════════════════════════════════════════

import { readFile } from 'node:fs/promises';
import { join, resolve as pathResolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHarness } from './harness.mjs';
// Gabarit générique créé pour l'analyse de puissance résidu RF (2026-08-07),
// explicitement prévu par son propre en-tête pour être « réutilisé tel quel
// pour le futur travail sur les poids composites » — édité en place plutôt
// que dupliqué (règle fichiers). Pas de test de permutation ici : on ne teste
// pas une association externe, on mesure la stabilité interne du classement
// sous perturbation des poids, donc seul spearman() est utilisé.
import { spearman } from '../../_drafts/rf_power_analysis/spearman_power_lib.mjs';

const __filename = fileURLToPath(import.meta.url);
const HARNESS_DIR = pathResolve(__filename, '..');
const REPO_ROOT = pathResolve(HARNESS_DIR, '..', '..');
const FIXTURE_PATH = join(REPO_ROOT, 'tests', 'fixtures', 'known-values-pre-extraction.json');

// ─── Réplique fidèle de computeExpertComposite (lecture seule, app.html:4337) ──

const DEFAULT_WEIGHTS = { M: 0.4, RF: 0.4, I: 0.2 };
// RF_uW_m2 upper mis à jour 2026-08-07 : 1000 → 1500, aligné sur EXPERT_BOUNDS_DEFAULT
// actuel d'app.html (S5 / arbitrage B Soleil 2026-07-01, p99 spatial recalé — voir
// app.html ~L4459-4464). Le script datait du 2026-06-06, avant ce recalage ; la valeur
// 1000 était donc périmée d'une borne réelle depuis modifiée en prod, corrigée ici pour
// que ce sweep mesure la sensibilité autour de la config GELÉ-001a réellement déployée,
// pas une config antérieure. ELF_nT et GAMMA_nSv_h inchangés (confirmés identiques).
const DEFAULT_BOUNDS = { ELF_nT: [0, 1000], RF_uW_m2: [0, 1500], GAMMA_nSv_h: [50, 250] };

function clamp01(x) {
  return Math.min(1, Math.max(0, x));
}

function composite(elf_nT, rf_uW, gamma_nSv_h, weights = DEFAULT_WEIGHTS, bounds = DEFAULT_BOUNDS) {
  const n_M = clamp01((elf_nT - bounds.ELF_nT[0]) / (bounds.ELF_nT[1] - bounds.ELF_nT[0]));
  const n_RF = clamp01((rf_uW - bounds.RF_uW_m2[0]) / (bounds.RF_uW_m2[1] - bounds.RF_uW_m2[0]));
  const n_I = clamp01((gamma_nSv_h - bounds.GAMMA_nSv_h[0]) / (bounds.GAMMA_nSv_h[1] - bounds.GAMMA_nSv_h[0]));
  const raw = weights.M * n_M + weights.RF * n_RF + weights.I * n_I;
  return Math.round(raw * 1000) / 1000;
}

// ─── Sweep : Monte Carlo Dirichlet(1,1,1) sur le simplexe ─────────────────────

// PRNG déterministe (Mulberry32) pour reproductibilité du sweep entre runs
function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function sampleDirichletUniform(rng) {
  // Dirichlet(1,1,1) = uniform sur le simplexe. Implémentation par exponentielles.
  const x = [-Math.log(1 - rng()), -Math.log(1 - rng()), -Math.log(1 - rng())];
  const s = x[0] + x[1] + x[2];
  return [x[0] / s, x[1] / s, x[2] / s];
}

// ─── Tiers hypothétiques (PAS dans le moteur — outil d'analyse uniquement) ───

function tier(idx) {
  if (idx < 0.33) return 'T_low';
  if (idx < 0.66) return 'T_mid';
  return 'T_high';
}

// ─── Stats utilitaires ───────────────────────────────────────────────────────

function statsBasic(arr) {
  const a = arr.filter(Number.isFinite).slice().sort((x, y) => x - y);
  if (!a.length) return null;
  const mean = a.reduce((s, x) => s + x, 0) / a.length;
  const variance = a.reduce((s, x) => s + (x - mean) * (x - mean), 0) / a.length;
  return {
    n: a.length,
    min: a[0],
    q1: a[Math.floor(a.length * 0.25)],
    median: a[Math.floor(a.length / 2)],
    q3: a[Math.floor(a.length * 0.75)],
    max: a[a.length - 1],
    mean,
    stdev: Math.sqrt(variance),
    range: a[a.length - 1] - a[0],
    iqr: a[Math.floor(a.length * 0.75)] - a[Math.floor(a.length * 0.25)],
  };
}

// ─── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const t0 = Date.now();
  const fixture = JSON.parse(await readFile(FIXTURE_PATH, 'utf-8'));
  const points = fixture.points;

  // Phase 1 — collecte des v2 (inputs du composite) pour chaque point
  const harness = await createHarness({ freezeTime: fixture.captured_at });
  await harness.setRuntimeState({
    curKp: fixture.runtime_state_at_capture.curKp,
    chargeFacteur: fixture.runtime_state_at_capture.chargeFacteur,
  });

  const collected = [];
  for (const p of points) {
    const v2 = await harness.calcAll_v2(p.lat, p.lon, p.options || {});
    const elf_nT = v2?.domains?.magnetic?.elf?.B_total_nT ?? 0;
    const rf_uW = v2?.domains?.rf?.S_total_uW_m2 ?? 0;
    const gamma_nSv_h = v2?.domains?.ionizing?.gamma?.dose_rate_nSv_h ?? 0;
    collected.push({
      id: p.id,
      category: p.category,
      lat: p.lat,
      lon: p.lon,
      altitude_m: p.altitude_m,
      inputs: { elf_nT, rf_uW, gamma_nSv_h },
    });
  }
  await harness.close();

  // Phase 2 — sweep en pur Node (réplique fidèle)

  // Default index per site
  for (const c of collected) {
    c.default_index = composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h);
    c.default_tier = tier(c.default_index);
    const { elf_nT, rf_uW, gamma_nSv_h } = c.inputs;
    c.default_normalized = {
      n_M: clamp01((elf_nT - DEFAULT_BOUNDS.ELF_nT[0]) / (DEFAULT_BOUNDS.ELF_nT[1] - DEFAULT_BOUNDS.ELF_nT[0])),
      n_RF: clamp01((rf_uW - DEFAULT_BOUNDS.RF_uW_m2[0]) / (DEFAULT_BOUNDS.RF_uW_m2[1] - DEFAULT_BOUNDS.RF_uW_m2[0])),
      n_I: clamp01((gamma_nSv_h - DEFAULT_BOUNDS.GAMMA_nSv_h[0]) / (DEFAULT_BOUNDS.GAMMA_nSv_h[1] - DEFAULT_BOUNDS.GAMMA_nSv_h[0])),
    };
  }

  // Default rank (1 = lowest, n = highest)
  const sortedDefault = collected.slice().sort((a, b) => a.default_index - b.default_index);
  sortedDefault.forEach((c, i) => { c.default_rank = i + 1; });

  // ── Sweep 1 : Monte Carlo Dirichlet sur les poids ──────────────────────────
  const N_MC = 200;
  const rng = mulberry32(42);
  const mcWeightVectors = [];
  for (let i = 0; i < N_MC; i++) {
    const [wM, wRF, wI] = sampleDirichletUniform(rng);
    mcWeightVectors.push({ M: wM, RF: wRF, I: wI });
  }

  for (const c of collected) {
    const indices = [];
    const tiers = [];
    for (const w of mcWeightVectors) {
      const idx = composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h, w, DEFAULT_BOUNDS);
      indices.push(idx);
      tiers.push(tier(idx));
    }
    c.mc_weight_sweep = {
      n: N_MC,
      stats_value: statsBasic(indices),
      tier_default: c.default_tier,
      tier_distribution: { T_low: 0, T_mid: 0, T_high: 0 },
      tier_switches: 0,
    };
    for (const t of tiers) c.mc_weight_sweep.tier_distribution[t]++;
    c.mc_weight_sweep.tier_switches = tiers.filter((t) => t !== c.default_tier).length;
    c.mc_weight_sweep.tier_switch_pct = (c.mc_weight_sweep.tier_switches / N_MC) * 100;
  }

  // ── Sweep 2 : perturbation poids OAT (±0.1, ±0.2 avec rebalance) ──────────
  const PERTURB_DELTAS = [-0.2, -0.1, 0.1, 0.2];
  const oatVectors = [];
  for (const dim of ['M', 'RF', 'I']) {
    for (const delta of PERTURB_DELTAS) {
      const w = { ...DEFAULT_WEIGHTS };
      const wOld = w[dim];
      const wNew = Math.min(1, Math.max(0, wOld + delta));
      const actualDelta = wNew - wOld;
      w[dim] = wNew;
      // Redistribuer le delta sur les 2 autres proportionnellement
      const others = ['M', 'RF', 'I'].filter((x) => x !== dim);
      const sumOthers = others.reduce((s, k) => s + DEFAULT_WEIGHTS[k], 0);
      if (sumOthers > 0) {
        for (const k of others) {
          w[k] = Math.max(0, DEFAULT_WEIGHTS[k] - actualDelta * (DEFAULT_WEIGHTS[k] / sumOthers));
        }
      }
      // Re-normalise pour somme = 1 (sécurité numérique)
      const sNorm = w.M + w.RF + w.I;
      if (sNorm > 0) {
        w.M /= sNorm; w.RF /= sNorm; w.I /= sNorm;
      }
      oatVectors.push({ dim, delta, weights: w });
    }
  }

  for (const c of collected) {
    c.oat_weight_sweep = oatVectors.map((o) => {
      const idx = composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h, o.weights, DEFAULT_BOUNDS);
      return {
        perturbed_dim: o.dim, delta: o.delta, weights: o.weights,
        index: idx, delta_index: idx - c.default_index,
        tier: tier(idx), tier_switched: tier(idx) !== c.default_tier,
      };
    });
    // élasticité approximative pour chaque dim (∂idx/∂w autour de défaut, normée par +0.1)
    const elasticity = {};
    for (const dim of ['M', 'RF', 'I']) {
      const plus = c.oat_weight_sweep.find((o) => o.perturbed_dim === dim && o.delta === 0.1);
      const minus = c.oat_weight_sweep.find((o) => o.perturbed_dim === dim && o.delta === -0.1);
      if (plus && minus) elasticity[dim] = (plus.index - minus.index) / 0.2;
    }
    c.oat_elasticity = elasticity;
  }

  // ── Sweep 3 : bornes (upper × {0.5, 1.0, 2.0}, lower inchangé) ─────────────
  const BOUND_FACTORS = [0.5, 1.0, 2.0];
  const boundsVectors = [];
  for (const fM of BOUND_FACTORS) {
    for (const fRF of BOUND_FACTORS) {
      for (const fI of BOUND_FACTORS) {
        const b = {
          ELF_nT: [DEFAULT_BOUNDS.ELF_nT[0], DEFAULT_BOUNDS.ELF_nT[1] * fM],
          RF_uW_m2: [DEFAULT_BOUNDS.RF_uW_m2[0], DEFAULT_BOUNDS.RF_uW_m2[1] * fRF],
          GAMMA_nSv_h: [DEFAULT_BOUNDS.GAMMA_nSv_h[0], DEFAULT_BOUNDS.GAMMA_nSv_h[1] * fI],
        };
        boundsVectors.push({ factors: { M: fM, RF: fRF, I: fI }, bounds: b });
      }
    }
  }

  for (const c of collected) {
    const indices = [];
    const tiers = [];
    for (const bv of boundsVectors) {
      const idx = composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h, DEFAULT_WEIGHTS, bv.bounds);
      indices.push(idx); tiers.push(tier(idx));
    }
    c.bounds_sweep = {
      n: boundsVectors.length,
      stats_value: statsBasic(indices),
      tier_distribution: { T_low: 0, T_mid: 0, T_high: 0 },
      tier_switches: 0,
    };
    for (const t of tiers) c.bounds_sweep.tier_distribution[t]++;
    c.bounds_sweep.tier_switches = tiers.filter((t) => t !== c.default_tier).length;
    c.bounds_sweep.tier_switch_pct = (c.bounds_sweep.tier_switches / boundsVectors.length) * 100;
  }

  // ── Sweep 4 : rangs sous Monte Carlo (utile pour le top/bottom-N) ─────────
  const rankHistories = collected.map(() => []);
  for (const w of mcWeightVectors) {
    const indices = collected.map((c) => composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h, w, DEFAULT_BOUNDS));
    const ranked = collected.map((c, i) => ({ i, idx: indices[i] })).sort((a, b) => a.idx - b.idx);
    ranked.forEach((r, k) => { rankHistories[r.i].push(k + 1); });
  }
  collected.forEach((c, i) => {
    c.rank_stats_under_mc = statsBasic(rankHistories[i]);
    c.rank_min = c.rank_stats_under_mc.min;
    c.rank_max = c.rank_stats_under_mc.max;
    c.rank_range = c.rank_max - c.rank_min;
  });

  // ── Sweep 5 : corrélation de rang (Spearman) — classement des 25 sites sous
  //     config par défaut vs sous chaque config perturbée (brief étape 4) ────
  const defaultIndices = collected.map((c) => c.default_index);

  const oatSpearman = oatVectors.map((o) => {
    const perturbedIndices = collected.map((c) =>
      composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h, o.weights, DEFAULT_BOUNDS)
    );
    return { perturbed_dim: o.dim, delta: o.delta, weights: o.weights, rho: spearman(defaultIndices, perturbedIndices) };
  });

  const mcSpearmanRhos = mcWeightVectors.map((w) => {
    const perturbedIndices = collected.map((c) =>
      composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h, w, DEFAULT_BOUNDS)
    );
    return spearman(defaultIndices, perturbedIndices);
  });

  const boundsSpearman = boundsVectors.map((bv) => {
    const perturbedIndices = collected.map((c) =>
      composite(c.inputs.elf_nT, c.inputs.rf_uW, c.inputs.gamma_nSv_h, DEFAULT_WEIGHTS, bv.bounds)
    );
    return { factors: bv.factors, rho: spearman(defaultIndices, perturbedIndices) };
  });

  const rankCorrelation = {
    method: 'spearman() — corpus/rf_power_analysis/spearman_power_lib.mjs, réutilisé tel quel (aucune modification)',
    note:
      'rho = 1 → classement des 25 sites identique au classement par défaut (0,4/0,4/0,2). ' +
      'rho proche de 0 ou négatif → classement substantiellement remanié par la perturbation.',
    oat_weights: oatSpearman,
    oat_weights_min_rho: Math.min(...oatSpearman.map((o) => o.rho)),
    mc_weights: statsBasic(mcSpearmanRhos),
    bounds: {
      stats: statsBasic(boundsSpearman.map((b) => b.rho)),
      min_entry: boundsSpearman.reduce((a, b) => (b.rho < a.rho ? b : a)),
    },
  };

  // ── Stats globales ────────────────────────────────────────────────────────

  const allStdev = collected.map((c) => c.mc_weight_sweep.stats_value.stdev);
  const allTierSwitches = collected.map((c) => c.mc_weight_sweep.tier_switch_pct);
  const allBoundsTierSwitches = collected.map((c) => c.bounds_sweep.tier_switch_pct);
  const allRangeRanks = collected.map((c) => c.rank_range);

  // ─── Sortie ─────────────────────────────────────────────────────────────────

  const out = {
    meta: {
      generated_at: new Date().toISOString(),
      harness: 'tests/blindage-harness@feat/blindage-harness',
      fixture: FIXTURE_PATH,
      n_sites: collected.length,
      freeze_time: fixture.captured_at,
      scope: 'WS2 sensibilité composite — mesure de la robustesse-au-choix, PAS validation des poids',
      sweep: {
        weights_monte_carlo_n: N_MC,
        weights_monte_carlo_seed: 42,
        weights_monte_carlo_distribution: 'Dirichlet(1,1,1) uniform sur le simplexe',
        weights_oat_deltas: PERTURB_DELTAS,
        bounds_factors_upper: BOUND_FACTORS,
        bounds_combinations: boundsVectors.length,
      },
      defaults: {
        weights: DEFAULT_WEIGHTS,
        bounds: DEFAULT_BOUNDS,
        note: 'Défauts GELE-001 (lecture only). Sweeps appliqués via paramètre, jamais par mutation des constantes.',
      },
      tiers_hypothetical: {
        T_low: '[0, 0.33)',
        T_mid: '[0.33, 0.66)',
        T_high: '[0.66, 1.0]',
        note: 'Tiers NON présents dans le moteur ; outil d\'analyse uniquement. Sert à mesurer la stabilité de classification, proxy de la fragilité interprétative.',
      },
      duration_s: (Date.now() - t0) / 1000,
    },
    global: {
      mc_stdev_index: statsBasic(allStdev),
      mc_tier_switch_pct: statsBasic(allTierSwitches),
      bounds_tier_switch_pct: statsBasic(allBoundsTierSwitches),
      mc_rank_range: statsBasic(allRangeRanks),
    },
    rank_correlation: rankCorrelation,
    per_site: collected,
  };

  process.stdout.write(JSON.stringify(out, null, 2));
}

main().catch((e) => {
  console.error('Erreur :', e?.stack || e);
  process.exit(1);
});
