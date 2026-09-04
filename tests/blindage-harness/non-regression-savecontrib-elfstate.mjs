// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Non-régression : saveContrib() attend la résolution de elfState
// Création : 2026-09-04 · brief AF lot B, suite (arbitrage Soleil)
// ═══════════════════════════════════════════════════════════════════════════
//
// Contexte : la revue adversariale de PR #1243 (état d'attente ELF du popup) a trouvé que
// saveContrib() avait son propre calcul de `predicted`/`perturbation_humaine_nt` non gaté
// par elfState — une contribution soumise pendant la fenêtre de préchargement (2-6s mesurés,
// brief AP) écrivait en base une valeur dérivée du v1 approximatif, sans jamais le savoir.
// Contrairement à l'affichage du popup (corrigeable au clic suivant), une écriture Supabase
// est irréversible — Soleil : « le même sujet que le lot A — une formule qui écrit sans
// savoir sur quoi elle s'appuie ».
//
// Correctif : saveContrib() attend désormais la résolution de computeElfState() (avec un
// timeout de 20s, largement supérieur à la fenêtre mesurée) avant de calculer `predicted`.
// Si l'état reste non résolu au-delà du timeout, ou est 'failed' dès le départ, le
// contributeur en est informé (jamais silencieux).
//
// Teste la fonction RÉELLE, jamais réimplémentée : sbPost() est stubbée (aucune écriture
// Supabase réelle) pour intercepter la ligne qui AURAIT été écrite, sans jamais publier de
// données de test. `pending` est réassignée par son nom nu à chaque appel (variable
// script-scope, pas attachée à window — même piège que curKp/chargeFacteur documenté dans
// harness.mjs).
// ═══════════════════════════════════════════════════════════════════════════

import { createHarness } from './harness.mjs';

const TEST_POINT = { lat: 41.9192, lon: 8.7386 };

async function main() {
  const h = await createHarness();
  let nFail = 0;
  const assert = (cond, label) => { if (!cond) { nFail++; console.log('[DIFF] ' + label); } else { console.log('[PASS] ' + label); } };

  try {
    await h.evalInPage(() => {
      window.__capturedRows = [];
      window.__origSbPost = window.sbPost;
      window.sbPost = async (path, body) => { window.__capturedRows.push({ path, body }); return [{ id: 'fake-id-test' }]; };
      window.__infoMessages = [];
      const origInfo = window.info;
      window.info = (msg, type, dur) => { window.__infoMessages.push(msg); return origInfo ? origInfo(msg, type, dur) : undefined; };
      document.getElementById('c-rgpd').checked = true;
      document.getElementById('c-val').value = '46500';
      document.getElementById('c-unit').value = 'nT';
      document.getElementById('c-type').value = 'autre';
    });

    async function runSaveContrib() {
      await h.evalInPage(({ lat, lon }) => {
        window.__capturedRows.length = 0;
        window.__infoMessages.length = 0;
        // eslint-disable-next-line no-undef
        pending = L.marker([lat, lon]).addTo(map); // script-scope, nom nu — cf. commentaire d'en-tête
      }, TEST_POINT);
      await h.evalInPage(() => saveContrib());
      const rows = await h.evalInPage(() => window.__capturedRows);
      const msgs = await h.evalInPage(() => window.__infoMessages);
      return { row: rows[0]?.body?.[0] || null, msgs };
    }

    // ─── Cas 1 : elfState déjà 'ready' — écriture immédiate, pas de notice ───
    await h.evalInPage(() => new Promise((resolve) => {
      const check = () => { if (SEGMENT_GRID !== null) resolve(); else { loadHTADataOnly(); setTimeout(check, 300); } };
      check();
    }));
    const t0 = Date.now();
    const r1 = await runSaveContrib();
    const elapsed1 = Date.now() - t0;
    console.log(`Cas READY   — écrit en ${elapsed1}ms, perturbation_humaine_nt=${r1.row?.perturbation_humaine_nt}`);
    assert(r1.row !== null, 'READY → une ligne écrite');
    assert(elapsed1 < 3000, 'READY → aucune attente inutile');
    assert(!r1.msgs.some(m => m.includes('estimation simplifiée')), 'READY → pas de notice de repli');

    // Sauvegarder la vraie grille pendant qu'elle est peuplée — nécessaire pour le cas LOADING→READY.
    await h.evalInPage(() => { window.__realSegmentGrid = SEGMENT_GRID; window.__realHtaData = HTA_SEGMENTS_DATA; });

    // ─── Cas 2 : elfState='failed' dès le départ — pas d'attente, notice affichée ───
    await h.evalInPage(() => { SEGMENT_GRID = null; HTA_SEGMENTS_DATA = null; _htaPreloadState = 'failed'; });
    const t1 = Date.now();
    const r2 = await runSaveContrib();
    const elapsed2 = Date.now() - t1;
    console.log(`Cas FAILED  — écrit en ${elapsed2}ms, perturbation_humaine_nt=${r2.row?.perturbation_humaine_nt}`);
    assert(r2.row !== null, 'FAILED → une ligne écrite (v1, jamais bloqué)');
    assert(elapsed2 < 3000, 'FAILED → pas d\'attente (déjà résolu, pas loading)');
    assert(r2.msgs.some(m => m.includes('estimation simplifiée')), 'FAILED → notice de repli affichée (jamais silencieux)');

    // ─── Cas 3 : elfState='loading' au départ, résout en 'ready' pendant l'attente ───
    await h.evalInPage(() => { SEGMENT_GRID = null; HTA_SEGMENTS_DATA = null; _htaPreloadState = 'loading'; });
    h.evalInPage(() => { setTimeout(() => { SEGMENT_GRID = window.__realSegmentGrid; HTA_SEGMENTS_DATA = window.__realHtaData; _htaPreloadState = 'ready'; }, 1000); });
    const t2 = Date.now();
    const r3 = await runSaveContrib();
    const elapsed3 = Date.now() - t2;
    console.log(`Cas LOADING→READY — écrit en ${elapsed3}ms, perturbation_humaine_nt=${r3.row?.perturbation_humaine_nt}`);
    assert(r3.row !== null, 'LOADING→READY → une ligne écrite après résolution');
    assert(elapsed3 >= 900 && elapsed3 < 5000, 'LOADING→READY → a réellement attendu (~1s), sans traîner');
    assert(!r3.msgs.some(m => m.includes('estimation simplifiée')), 'LOADING→READY → pas de notice (résolu avant le timeout)');
    assert(r1.row.perturbation_humaine_nt === r3.row.perturbation_humaine_nt, 'LOADING→READY → valeur identique au cas READY direct (a bien attendu la VRAIE résolution, pas une valeur figée au moment du clic)');
    assert(r1.row.perturbation_humaine_nt !== r2.row.perturbation_humaine_nt, 'témoin : READY et FAILED donnent des valeurs DIFFÉRENTES à ce point (v2 vs v1, la mesure a un sens)');
  } finally {
    await h.evalInPage(() => { window.sbPost = window.__origSbPost; });
    await h.close();
  }

  console.log('');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log(nFail === 0 ? 'Résultat : PASS — saveContrib() attend la résolution de elfState avant d\'écrire, jamais silencieux en repli.' : `Résultat : ${nFail} DIFF.`);
  console.log('────────────────────────────────────────────────────────────────────');

  if (nFail > 0) process.exit(1);
}

main().catch((e) => {
  console.error('Erreur fatale du harness :', e?.stack || e);
  process.exit(2);
});
