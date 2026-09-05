// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Vérification du VRAI chemin de chargement Supabase (brief BN, 2026-09-05)
// ═══════════════════════════════════════════════════════════════════════════
//
// POURQUOI CE SCRIPT EXISTE
// --------------------------
// Le brief BN pose un cache local Supabase pour les 10 autres scripts de ce
// dossier (cf. supabase-cache.mjs) — après sa mise en place, plus aucun d'eux
// n'exerce le vrai chemin réseau (fetch → pagination → parsing → construction
// des grilles) au-delà de la toute première exécution qui remplit le cache.
// Ce script-ci, lui, tourne TOUJOURS avec le cache désactivé
// (createHarness({cache:false}), équivalent explicite de
// TELLUX_HARNESS_CACHE=off) : sa seule raison d'être est de vérifier que ce
// chemin réel fonctionne encore, indépendamment de tout ce que le cache
// pourrait masquer.
//
// IL DOIT ÉCHOUER BRUYAMMENT, PAS SE REPLIER SILENCIEUSEMENT
// -------------------------------------------------------------
// (Retour Soleil, revue de conception brief BN.) app.html, lui, est CONÇU
// pour se replier proprement si Supabase est indisponible pour un vrai
// visiteur (_htaPreloadState='failed' + repli v1, ANFR_GRID={} vide + RF en
// TDF/FH seuls) — un comportement délibéré et correct en production. Ce
// script a l'objectif STRICTEMENT INVERSE : si l'un de ces replis se
// déclenche ICI, c'est que le chemin réel est cassé, et ce script doit le
// dire fort (process.exit(1), message explicite) plutôt que de le lire comme
// un état applicatif normal. Cette semaine a montré plusieurs fois ce que
// coûte une vérification qui passe sans rien vérifier (check contraste
// excluant le panneau couches, BOOT_CHECK_FN sur une dépendance disparue,
// eval-app-rubric cherchant un texte mort) — ce script n'a qu'un travail,
// il ne doit jamais le faire à moitié.
//
// MÉTHODE — attendre les VRAIES promesses de chargement, pas un sondage
// -------------------------------------------------------------------------
// loadHTADataOnly()/loadBTLinesAsync()/loadANFRForField() sont toutes trois
// idempotentes par construction (gardées par une promesse partagée ou un flag
// déjà-chargé) : les rappeler depuis ce script, une fois le boot lancé,
// retourne soit la promesse déjà en vol (on attend juste qu'elle aboutisse),
// soit un résultat déjà résolu. C'est plus robuste qu'un sondage sur une
// variable globale — pas de risque de condition "toujours vraie dès la
// déclaration" (piège rencontré en écrivant ce script : BT_SEGMENT_GRID est
// déclaré `let ... = null` dès le chargement du fichier, donc
// `typeof BT_SEGMENT_GRID !== 'undefined'` est vrai AVANT même que le
// chargement démarre — un sondage sur ce seul test n'aurait jamais attendu
// quoi que ce soit).
// ═══════════════════════════════════════════════════════════════════════════

import { createHarness } from './harness.mjs';

const LOAD_TIMEOUT_MS = Number(process.env.HARNESS_BOOT_TIMEOUT_MS) || 45000; // réseau réel, pas le cache

async function main() {
  console.log('[loading-path-live-check] cache désactivé explicitement — réseau Supabase réel pour tout ce run.');
  const harness = await createHarness({ cache: false, bootTimeoutMs: LOAD_TIMEOUT_MS });
  let nFail = 0;
  const details = {};

  try {
    // ── HTA : attend _htaPreloadState via sondage (pas de promesse partagée
    //    exposée pour loadHTADataOnly() elle-même — mais son flag tri-état,
    //    lui, transitionne correctement loading→ready|failed, contrairement
    //    à un sondage direct sur SEGMENT_GRID). ──
    let htaState = 'undefined';
    try {
      await harness._internal.page.waitForFunction(() => {
        // eslint-disable-next-line no-undef
        return typeof _htaPreloadState !== 'undefined' && (_htaPreloadState === 'ready' || _htaPreloadState === 'failed');
      }, undefined, { timeout: LOAD_TIMEOUT_MS, polling: 500 });
    } catch (e) {
      nFail++;
      console.log('[FAIL BRUYANT] HTA : _htaPreloadState n\'a atteint ni "ready" ni "failed" dans le délai (' + LOAD_TIMEOUT_MS + ' ms) — ' + e.message);
    }
    htaState = await harness.evalInPage(() => (typeof _htaPreloadState !== 'undefined' ? _htaPreloadState : 'undefined')); // eslint-disable-line no-undef
    details.htaPreloadState = htaState;

    if (htaState === 'failed') {
      nFail++;
      console.log('[FAIL BRUYANT] HTA : _htaPreloadState="failed" — le vrai chargement Supabase a échoué, app.html serait en repli v1 pour un visiteur réel en ce moment même.');
    } else if (htaState === 'ready') {
      const segmentGridBuilt = await harness.evalInPage(() => (typeof SEGMENT_GRID !== 'undefined' && !!SEGMENT_GRID)); // eslint-disable-line no-undef
      details.segmentGridBuilt = segmentGridBuilt;
      if (!segmentGridBuilt) {
        nFail++;
        console.log('[FAIL BRUYANT] HTA : _htaPreloadState="ready" mais SEGMENT_GRID n\'est pas construit — incohérence interne, pas un simple aléa réseau.');
      } else {
        console.log('[PASS] HTA : _htaPreloadState="ready", SEGMENT_GRID construit.');
      }
    }
    // (htaState ni ready ni failed après le timeout : déjà compté en échec ci-dessus.)

    // ── BT : appelle directement loadBTLinesAsync() — idempotente, retourne
    //    la promesse déjà en vol ou un résultat déjà résolu si le boot l'a
    //    déjà lancée. ──
    await harness.evalInPage(() => (typeof loadBTLinesAsync === 'function' ? loadBTLinesAsync() : null)); // eslint-disable-line no-undef
    const bt = await harness.evalInPage(() => ({
      // eslint-disable-next-line no-undef
      segmentsData: typeof BT_SEGMENTS_DATA !== 'undefined' && BT_SEGMENTS_DATA ? BT_SEGMENTS_DATA.length : null,
      // eslint-disable-next-line no-undef
      gridTiles: typeof BT_SEGMENT_GRID !== 'undefined' && BT_SEGMENT_GRID ? Object.keys(BT_SEGMENT_GRID).length : null,
    }));
    details.bt = bt;
    if (bt.segmentsData === null) {
      nFail++;
      console.log('[FAIL BRUYANT] BT : BT_SEGMENTS_DATA reste null après attente de loadBTLinesAsync() — le chargement n\'a jamais abouti à une construction de grille.');
    } else if (bt.segmentsData === 0 || bt.gridTiles === 0) {
      nFail++;
      console.log(`[FAIL BRUYANT] BT : grille construite mais VIDE (segments=${bt.segmentsData}, tuiles=${bt.gridTiles}) — 156 130 lignes/249 682 segments attendus (brief BL), la table a répondu vide ou la pagination s'est arrêtée immédiatement.`);
    } else {
      console.log(`[PASS] BT : ${bt.segmentsData} segments, ${bt.gridTiles} tuiles.`);
    }

    // ── Antennes : idem, loadANFRForField() est idempotente. Rappel : le code
    //    de production remplace ANFR_GRID par {} (vide, mais défini) même en
    //    cas d'ÉCHEC réseau (repli RF=TDF+FH seuls, cf. son propre commentaire
    //    dans app.html) — vérifier seulement "ANFR_GRID !== null/undefined"
    //    serait exactement le repli silencieux que ce script doit refuser. ──
    await harness.evalInPage(() => (typeof loadANFRForField === 'function' ? loadANFRForField() : null)); // eslint-disable-line no-undef
    const anfrGridKeys = await harness.evalInPage(() => (
      // eslint-disable-next-line no-undef
      typeof ANFR_GRID !== 'undefined' && ANFR_GRID ? Object.keys(ANFR_GRID).length : null
    ));
    details.anfrGridKeys = anfrGridKeys;
    if (anfrGridKeys === null) {
      nFail++;
      console.log('[FAIL BRUYANT] Antennes : ANFR_GRID reste undefined/null après attente de loadANFRForField().');
    } else if (anfrGridKeys === 0) {
      nFail++;
      console.log('[FAIL BRUYANT] Antennes : ANFR_GRID est VIDE (0 case) — c\'est précisément le repli silencieux de production (échec réseau avalé, RF retombe sur TDF+FH seuls) : le chemin réel est cassé, même si aucune exception n\'a remonté jusqu\'ici.');
    } else {
      console.log(`[PASS] Antennes : ANFR_GRID construit, ${anfrGridKeys} cases.`);
    }

    // ── Erreurs console pendant le boot — hors bruit CORS externe déjà
    //    documenté ailleurs dans ce dossier (RTE/NOAA/Dst depuis localhost,
    //    cf. non-regression-lot-a-formule-autorite.mjs : "bruit CORS/localhost
    //    attendu, non bloquant"). Le texte de console ne porte pas toujours le
    //    domaine (ex. "Failed to load resource: net::ERR_FAILED" nu) — on
    //    exclut par le préfixe applicatif de ces appels (loadNOAA/loadAQU/
    //    loadDst/loadMeteo/loadLightning), tous des correctifs externes de
    //    contexte, aucun n'a de rapport avec bt_lines/hta_lines/antennas_corse.
    //    Ce filtre reste délibérément étroit : il ne masque QUE ce motif déjà
    //    documenté ailleurs, jamais une erreur générique non identifiée. ──
    const KNOWN_EXTERNAL_NOISE = /rte-france\.com|swpc\.noaa\.gov|CORS policy|loadNOAA|loadAQU|loadDst|loadMeteo|loadLightning|net::ERR_FAILED/i;
    const consoleErrors = harness.diagnostics().consoleErrors.filter((e) => !KNOWN_EXTERNAL_NOISE.test(e));
    if (consoleErrors.length > 0) {
      nFail++;
      console.log(`[FAIL BRUYANT] ${consoleErrors.length} erreur(s) console non liée(s) au bruit CORS externe connu :`);
      consoleErrors.forEach((e) => console.log('  ! ' + e));
    } else {
      console.log('[PASS] Aucune erreur console inattendue pendant le chargement.');
    }
  } finally {
    await harness.close();
  }

  console.log('');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log('État observé :', JSON.stringify(details));
  console.log(nFail === 0
    ? 'Résultat : PASS — le chemin de chargement réel (réseau Supabase, sans cache) fonctionne.'
    : `Résultat : ${nFail} FAIL BRUYANT — le chemin de chargement réel est cassé ou dégradé. Voir le détail ci-dessus.`);
  console.log('────────────────────────────────────────────────────────────────────');

  if (nFail > 0) process.exit(1);
}

main().catch((e) => {
  console.error('[FAIL BRUYANT] Erreur fatale — le harness lui-même a planté, pas seulement un chargement de données :', e?.stack || e);
  process.exit(2);
});
