// ─── Vérification navigateur : la calibration RF ne dépend pas des émetteurs TDF (lot RF, 2026-09-10) ──
//
// LA QUESTION
// Le lot RF de la reprise adopte loadTDFEmitters() dans l'assistant de reprise partagé (#1366).
// Question posée à la revue : calibrateRF() dérive RF_CALIB_K UNE seule fois au boot, et n'attend pas
// les émetteurs TDF. Si TDF échoue au boot puis revient par la reprise, k reste-t-il dérivé sur un
// modèle sans TDF — la calibration se déclarant faite sur un coefficient déplacé ? Si oui, le lot
// devrait recalibrer au retour de TDF.
//
// LA RÉPONSE, MESURÉE le 2026-09-10 (Chromium, ?no-bt=1, grille ANFR chargée) : NON.
//   · 21 points éligibles (état actuel) : k = 0,36060937 avec TDF, 0,36063255 sans — Δk/k = 6 × 10⁻⁵.
//   · pool élargi hypothétique (les 206 fiches Cartoradio non éligibles rendues éligibles, 150 points
//     utilisés) : Δk/k = 7 × 10⁻⁴. Mesuré pour borner la décision, PAS pour proposer ce changement :
//     l'éligibilité de ces fiches relève d'un arbitrage GELÉ-001b distinct.
//   k est la médiane des rapports mesure / prédiction sur ces points ; aucun n'est dominé par un
//   émetteur TDF. D'où la décision du lot : PAS de recalcul de k au retour de TDF. Il ajouterait une
//   intervention dans la chaîne de calibration pour un effet non mesurable.
//
// CE FICHIER EST LE CHAMP 4 DE CETTE DÉCISION
// Il re-mesure Δk/k et ÉCHOUE au-delà de SEUIL. La décision n'est vraie que dans le domaine où elle a
// été mesurée ; le jour où le pool de calibration change (nouvelles fiches, émetteurs, filtres), c'est
// ce contrôle qui dit si elle tient encore.
//
// SEUIL = 1 %, LITTÉRAL. Au-delà, l'effet sur la valeur affichée (S ∝ k², soit ~2 % de S) cesserait
// d'être négligeable devant rien de plus qu'un arrondi, et le retour de TDF devrait déclencher une
// recalibration. Il reste très en dessous de la dispersion propre de k (IQR 0,18 – 0,50) : il ne
// cherche pas une précision que le modèle n'a pas, il cherche un changement de régime.
//
// TÉMOINS — le script s'arrête au lieu de conclure si la mesure ne peut pas être valide :
//   · la grille ANFR doit être chargée : sans elle, la prédiction se réduit à TDF + faisceaux et k
//     dépendrait de TDF par construction — un rouge faux, mesuré sur un modèle empoisonné ;
//   · des émetteurs TDF doivent être chargés : sinon on comparerait « sans TDF » à « sans TDF » ;
//   · la recalibration avec TDF doit redonner k à l'identique (idempotence annoncée par le code) :
//     sinon Δk mesurerait une dérive de calibrateRF, pas l'effet de TDF.
//
// Réseau : charge app.html comme le harnais (serveur local, cache Supabase du dossier). Pas en CI.
// Usage : node tests/blindage-harness/verif-calibration-rf-sans-tdf.mjs   (sort 1 si rouge, 2 si témoin)

import { createHarness } from './harness.mjs';

const SEUIL = 0.01;
const PORT = 3781;

const h = await createHarness({ url: `http://127.0.0.1:${PORT}/app.html?no-bt=1`, port: PORT, bootTimeoutMs: 60000 });
let code = 0;
try {
  const r = await h.evalInPage(async () => {
    const t0 = performance.now();
    // eslint-disable-next-line no-undef
    while (!(typeof RF_CALIB_STATS !== 'undefined' && RF_CALIB_STATS) && performance.now() - t0 < 45000) {
      await new Promise((res) => setTimeout(res, 500));
    }
    // eslint-disable-next-line no-undef
    if (!RF_CALIB_STATS) return { erreur: 'calibration du boot non observée en 45 s' };
    /* eslint-disable no-undef */
    const anfr = ANFR_GRID ? Object.keys(ANFR_GRID).length : 0;
    const kBoot = RF_CALIB_K;
    const sauve = TDF_EMITTERS;
    try {
      TDF_EMITTERS = [];
      await calibrateRF();
      const kSans = RF_CALIB_K;
      TDF_EMITTERS = sauve;
      await calibrateRF();
      const kAvec = RF_CALIB_K;
      return { anfr_cellules: anfr, tdf: sauve.length, n_used: RF_CALIB_STATS.n_used, k_boot: kBoot, k_sans_tdf: kSans, k_avec_tdf: kAvec };
    } finally {
      TDF_EMITTERS = sauve;
      RF_CALIB_K = kBoot;
    }
    /* eslint-enable no-undef */
  });

  console.log(JSON.stringify(r, null, 1));
  if (r.erreur) { console.error('TÉMOIN — ' + r.erreur); code = 2; }
  else if (!(r.anfr_cellules > 0)) { console.error('TÉMOIN — grille ANFR vide : mesure sur un modèle empoisonné, arrêt.'); code = 2; }
  else if (!(r.tdf > 0)) { console.error('TÉMOIN — aucun émetteur TDF chargé : rien à comparer, arrêt.'); code = 2; }
  else if (r.k_avec_tdf !== r.k_boot) { console.error(`TÉMOIN — recalibration non idempotente (${r.k_boot} → ${r.k_avec_tdf}) : Δk ne mesurerait pas TDF, arrêt.`); code = 2; }
  else {
    const ecart = Math.abs(r.k_boot - r.k_sans_tdf) / r.k_boot;
    const ok = ecart < SEUIL;
    console.log(`\n${ok ? '✔' : '✘'} Δk/k = ${ecart.toExponential(2)} sur ${r.n_used} points (seuil ${SEUIL})`);
    if (!ok) {
      console.log('  La calibration dépend désormais des émetteurs TDF : le retour de TDF par la reprise');
      console.log('  doit déclencher une recalibration. La décision du lot RF (2026-09-10) ne tient plus.');
      code = 1;
    }
  }
} finally {
  await h.close();
}
process.exit(code);
