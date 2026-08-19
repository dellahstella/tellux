// ═══════════════════════════════════════════════════════════════════════════
// Tellux — WS2 collecte des résiduels RF (analyse via harness)
// Création : 2026-06-06 · feat/blindage-harness (WS2)
// ═══════════════════════════════════════════════════════════════════════════
//
// Pour chacune des 30 mesures certifiées ANFR/EXEM :
//   - charge le harness une seule fois (mode local)
//   - appelle calcAll_v2(lat, lon) → récupère domains.rf
//   - calcule predicted (E en V/m) − measured (valeur_max_vm)
//   - stocke ratio = predicted / measured et log10(ratio)
//   - stratifie indoor/outdoor + commune
//
// Sortie : un objet JSON sur stdout avec :
//   - meta : version harness, n mesures, scope analyse
//   - per_point : 30 entrées détaillées
//   - stats : globales + par strate
//
// USAGE : node rf-residuals-collect.mjs > /tmp/rf-residuals.json
//
// ⚠ Ce script NE fait PAS de claim de validation. Il extrait les résiduels
// bruts pour analyse honnête dans un rapport séparé. Voir le rapport dans
// _drafts/RF_RESIDUALS_WS2_*.md pour l'interprétation cadrée.
// ═══════════════════════════════════════════════════════════════════════════

import { readFile } from 'node:fs/promises';
import { join, resolve as pathResolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHarness } from './harness.mjs';

const __filename = fileURLToPath(import.meta.url);
const HARNESS_DIR = pathResolve(__filename, '..');
const REPO_ROOT = pathResolve(HARNESS_DIR, '..', '..');
const MESURES_PATH = join(REPO_ROOT, 'public', 'data', 'cartoradio_certified_corse.json');
const FREEZE_TIME = process.env.FREEZE_TIME || '2026-04-26T08:46:55.403Z';

// Quartiles / stats utilitaires
function stats(arr) {
  const a = arr.filter(Number.isFinite).slice().sort((x, y) => x - y);
  if (a.length === 0) return null;
  const sum = a.reduce((s, x) => s + x, 0);
  const mean = sum / a.length;
  const median = a[Math.floor(a.length / 2)];
  const q1 = a[Math.floor(a.length * 0.25)];
  const q3 = a[Math.floor(a.length * 0.75)];
  const min = a[0], max = a[a.length - 1];
  const variance = a.reduce((s, x) => s + (x - mean) * (x - mean), 0) / a.length;
  const stdev = Math.sqrt(variance);
  const rmse = Math.sqrt(a.reduce((s, x) => s + x * x, 0) / a.length);
  const mae = a.reduce((s, x) => s + Math.abs(x), 0) / a.length;
  return { n: a.length, min, q1, median, q3, max, mean, stdev, rmse, mae };
}

function isIndoor(m) {
  // Heuristique : type_environnement contient "residentiel" / "interieur" / "ERP"
  // OU adresse_complete suggère un bâtiment. La fixture brief brief dit 29/30 indoor.
  // En pratique : si on n'a pas un marqueur explicite "exterieur", on assume indoor.
  if (!m) return false;
  const env = (m.type_environnement || '').toLowerCase();
  if (env.includes('exterieur') || env.includes('extérieur') || env === 'open') return false;
  return true; // indoor par défaut, cf. brief
}

async function main() {
  const t0 = Date.now();
  const raw = await readFile(MESURES_PATH, 'utf-8');
  const data = JSON.parse(raw);
  const mesures = data.mesures || [];

  const harness = await createHarness({ freezeTime: FREEZE_TIME });

  const perPoint = [];
  for (const m of mesures) {
    const v2 = await harness.calcAll_v2(m.lat, m.lon, {});
    const rf = v2?.domains?.rf || {};
    const predicted_uW_m2 = rf.S_total_uW_m2 ?? null;
    const predicted_vm = rf.E_total_V_m ?? null;
    const measured_vm = m.valeur_max_vm ?? null;

    // Ratio + log10 ratio (log pour mieux visualiser les ordres de grandeur)
    const ratio =
      predicted_vm !== null && measured_vm !== null && measured_vm > 0
        ? predicted_vm / measured_vm
        : null;
    const log10_ratio = ratio !== null && ratio > 0 ? Math.log10(ratio) : null;
    const residual_vm = predicted_vm !== null && measured_vm !== null ? predicted_vm - measured_vm : null;
    const abs_residual = residual_vm !== null ? Math.abs(residual_vm) : null;

    perPoint.push({
      id: m.id,
      site_nom: m.site_nom,
      commune: m.commune,
      departement: m.departement,
      lat: m.lat,
      lon: m.lon,
      precision_coord: m.precision_coord,
      type_environnement: m.type_environnement,
      indoor: isIndoor(m),
      measured_vm,
      predicted_vm,
      predicted_uW_m2,
      residual_vm,
      abs_residual,
      ratio,
      log10_ratio,
      contributions: (rf.contributions || []).map((c) => ({
        source_type: c.source_type,
        S_uW_m2: c.S_uW_m2,
        distance_m: c.distance_m,
        path_name: c.path_name,
      })),
      conforme_anfr: m.conforme,
      seuil_legal_vm: m.seuil_legal_vm,
      // Modèle interne notes
      calibrated_flag: rf.calibrated,
      confidence_flag: rf.confidence,
    });
  }

  await harness.close();

  // ─── Stats globales et stratifiées ────────────────────────────────────────

  const all_residuals = perPoint.map((p) => p.residual_vm);
  const all_abs_residuals = perPoint.map((p) => p.abs_residual);
  const all_ratios = perPoint.map((p) => p.ratio);
  const all_log_ratios = perPoint.map((p) => p.log10_ratio);

  const indoor_points = perPoint.filter((p) => p.indoor);
  const outdoor_points = perPoint.filter((p) => !p.indoor);

  const stratify = (pts) => ({
    n: pts.length,
    residual_vm: stats(pts.map((p) => p.residual_vm)),
    abs_residual_vm: stats(pts.map((p) => p.abs_residual)),
    ratio: stats(pts.map((p) => p.ratio)),
    log10_ratio: stats(pts.map((p) => p.log10_ratio)),
    measured_vm: stats(pts.map((p) => p.measured_vm)),
    predicted_vm: stats(pts.map((p) => p.predicted_vm)),
  });

  // Par commune (top 5 communes par n mesures)
  const byCommune = {};
  for (const p of perPoint) {
    if (!byCommune[p.commune]) byCommune[p.commune] = [];
    byCommune[p.commune].push(p);
  }
  const topCommunes = Object.entries(byCommune)
    .sort((a, b) => b[1].length - a[1].length)
    .slice(0, 5)
    .map(([commune, pts]) => ({ commune, n: pts.length, ratio: stats(pts.map((p) => p.ratio)) }));

  // Par contribution dominante du modèle (FH / broadcast_TDF / fond_departemental)
  const by_dominant = { FH: [], broadcast_TDF: [], fond_departemental: [], mixed: [], none: [] };
  for (const p of perPoint) {
    const sorted = (p.contributions || []).slice().sort((a, b) => b.S_uW_m2 - a.S_uW_m2);
    if (sorted.length === 0) by_dominant.none.push(p);
    else if (sorted.length === 1) by_dominant[sorted[0].source_type]?.push(p);
    else {
      const dom = sorted[0];
      const second = sorted[1];
      if (dom.S_uW_m2 > 2 * second.S_uW_m2) by_dominant[dom.source_type]?.push(p);
      else by_dominant.mixed.push(p);
    }
  }
  const dominantStats = Object.fromEntries(
    Object.entries(by_dominant).map(([k, pts]) => [k, { n: pts.length, ratio: stats(pts.map((p) => p.ratio)) }])
  );

  const result = {
    meta: {
      generated_at: new Date().toISOString(),
      harness: 'tests/blindage-harness@feat/blindage-harness',
      app_revision: 'origin/dev HEAD',
      freeze_time: FREEZE_TIME,
      n_mesures: mesures.length,
      mesures_source: data.source || null,
      mesures_extraction_date: data.date_maj || null,
      scope: 'WS2 résiduels RF — analyse exploratoire, PAS une validation',
      duration_s: (Date.now() - t0) / 1000,
    },
    stats: {
      global: {
        residual_vm: stats(all_residuals),
        abs_residual_vm: stats(all_abs_residuals),
        ratio_predicted_over_measured: stats(all_ratios),
        log10_ratio: stats(all_log_ratios),
      },
      indoor: stratify(indoor_points),
      outdoor: stratify(outdoor_points),
      top_communes: topCommunes,
      by_dominant_model_contribution: dominantStats,
    },
    per_point: perPoint,
  };

  process.stdout.write(JSON.stringify(result, null, 2));
}

main().catch((e) => {
  console.error('Erreur fatale :', e?.stack || e);
  process.exit(1);
});
