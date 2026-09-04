// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Non-régression : état d'attente ELF (popup au clic)
// Création : 2026-09-04 · brief AF lot B (arbitrage Soleil, sur la base du brief AP)
// ═══════════════════════════════════════════════════════════════════════════
//
// Contexte : le popup au clic s'ouvre sans attendre SEGMENT_GRID (le délai d'ouverture
// ne change pas) mais tout ce qui dépend d'elle (bloc ELF, score Perturbation) doit
// montrer un état d'attente explicite pendant le préchargement plutôt qu'une valeur v1
// silencieuse — brief AP a mesuré que 33% des points changent de palier de score entre
// v1 et v2 (un quart du minimum au maximum). Le repli v1 reste affiché, marqué, pour la
// panne durable (_htaPreloadState==='failed') — jamais un état d'attente qui ne se
// termine pas.
//
// Simule un clic réel (map.fire('click', {latlng})) et lit le DOM du popup réellement
// rendu — pas une réimplémentation de la logique de rendu. Force les 3 états en
// manipulant SEGMENT_GRID/_htaPreloadState directement (mêmes globales que lit le code
// réel), comme harness.setRuntimeState() le fait déjà pour curKp.
// ═══════════════════════════════════════════════════════════════════════════

import { createHarness } from './harness.mjs';

const TEST_POINT = { lat: 41.9192, lon: 8.7386 }; // Ajaccio — zone dense, valeurs non nulles garanties

async function main() {
  const h = await createHarness();
  let nFail = 0;
  const assert = (cond, label) => { if (!cond) { nFail++; console.log('[DIFF] ' + label); } else { console.log('[PASS] ' + label); } };

  async function clickAndReadPopup(lat, lon) {
    return await h.evalInPage(({ lat, lon }) => new Promise((resolve) => {
      // eslint-disable-next-line no-undef
      if (typeof map !== 'undefined' && map.closePopup) map.closePopup();
      // eslint-disable-next-line no-undef
      map.fire('click', { latlng: L.latLng(lat, lon) });
      let tries = 0;
      const poll = () => {
        tries++;
        const popupEl = document.querySelector('.delta-popup .leaflet-popup-content');
        const txt = popupEl ? popupEl.innerHTML : null;
        const stillCalculating = txt && txt.includes('calcul…');
        if ((txt && !stillCalculating) || tries > 60) {
          // eslint-disable-next-line no-undef
          resolve({ html: txt, elfState: window._geoLastPoint ? window._geoLastPoint.elfState : null });
        } else {
          setTimeout(poll, 200);
        }
      };
      setTimeout(poll, 200);
    }), { lat, lon });
  }

  function extractSnippets(html) {
    if (!html) return { scoreHeader: '', elfBlock: '' };
    const scoreMatch = html.match(/<div style="font-weight:700[^>]*>([\s\S]{0,800}?)<\/div>\s*<\/div>/);
    const elfIdx = html.indexOf('ELF anthropique 50 Hz</div>');
    const rfIdx = html.indexOf('Radiofréquence');
    const elfRaw = (elfIdx !== -1 && rfIdx !== -1) ? html.slice(elfIdx + 'ELF anthropique 50 Hz</div>'.length, rfIdx) : '';
    return {
      scoreHeader: scoreMatch ? scoreMatch[1].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim() : '',
      elfBlock: elfRaw.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim(),
    };
  }

  try {
    // ─── État LOADING : SEGMENT_GRID null, préchargement pas encore tenté/pas fini ───
    await h.evalInPage(() => { SEGMENT_GRID = null; HTA_SEGMENTS_DATA = null; _htaPreloadState = 'pending'; });
    const r1 = await clickAndReadPopup(TEST_POINT.lat, TEST_POINT.lon);
    const s1 = extractSnippets(r1.html);
    console.log('État LOADING — elfState=' + r1.elfState + ' | score="' + s1.scoreHeader + '" | elf="' + s1.elfBlock.slice(0, 60) + '..."');
    assert(r1.elfState === 'loading', 'LOADING → elfState==loading');
    assert(!/\d\/5/.test(s1.scoreHeader), 'LOADING → aucun chiffre de score affiché');
    assert(!/\d+\s*nT/.test(s1.elfBlock), 'LOADING → aucune valeur nT affichée dans le bloc ELF');
    assert(s1.scoreHeader.toLowerCase().includes('préparation') && s1.elfBlock.includes('Préparation du calcul'), 'LOADING → texte d\'attente présent (score + bloc ELF)');

    // ─── État FAILED : SEGMENT_GRID null, échec durable ───
    await h.evalInPage(() => { SEGMENT_GRID = null; HTA_SEGMENTS_DATA = null; _htaPreloadState = 'failed'; });
    const r2 = await clickAndReadPopup(TEST_POINT.lat, TEST_POINT.lon);
    const s2 = extractSnippets(r2.html);
    console.log('État FAILED  — elfState=' + r2.elfState + ' | score="' + s2.scoreHeader + '" | elf="' + s2.elfBlock.slice(0, 60) + '..."');
    assert(r2.elfState === 'failed', 'FAILED → elfState==failed');
    assert(/\d\/5/.test(s2.scoreHeader) && (s2.scoreHeader.includes('≈') || s2.scoreHeader.includes('estimation')), 'FAILED → score affiché ET marqué ≈/estimation');
    assert(/\d+\s*nT/.test(s2.elfBlock) && (s2.elfBlock.includes('≈') || s2.elfBlock.includes('estimation')), 'FAILED → bloc ELF affiché ET marqué ≈/estimation');

    // ─── État READY : chargement réel complété (SEGMENT_GRID peuplée) ───
    await h.evalInPage(() => new Promise((resolve) => {
      const check = () => { if (SEGMENT_GRID !== null) resolve(); else { loadHTADataOnly(); setTimeout(check, 300); } };
      check();
    }));
    const r3 = await clickAndReadPopup(TEST_POINT.lat, TEST_POINT.lon);
    const s3 = extractSnippets(r3.html);
    console.log('État READY   — elfState=' + r3.elfState + ' | score="' + s3.scoreHeader + '" | elf="' + s3.elfBlock.slice(0, 60) + '..."');
    assert(r3.elfState === 'ready', 'READY → elfState==ready');
    assert(/\d\/5/.test(s3.scoreHeader) && !s3.scoreHeader.includes('estimation'), 'READY → score affiché SANS marquage');
    assert(/\d+\s*nT/.test(s3.elfBlock) && !s3.elfBlock.includes('estimation'), 'READY → bloc ELF affiché SANS marquage');

    // ─── Contrainte Soleil : le reste du popup (statique/RF/substrat) reste normal
    //     dans les 3 états — présence, pas valeur exacte (RF/antennes chargent de façon
    //     asynchrone indépendamment de SEGMENT_GRID, une variation de valeur est normale). ───
    for (const [label, r] of [['LOADING', r1], ['FAILED', r2], ['READY', r3]]) {
      const hasStatic = /Champ statique géomagnétique<\/div>[\s\S]{0,60}?\d/.test(r.html);
      const hasRF = /Radiofréquence[\s\S]{0,200}?[\d.]+\s*.{0,2}W\/m/.test(r.html);
      const hasSubstrat = /Substrat (à forte|à susceptibilité|neutre|standard)/.test(r.html);
      assert(hasStatic && hasRF && hasSubstrat, label + ' → statique/RF/substrat tous présents (inchangés par elfState)');
    }
  } finally {
    await h.close();
  }

  console.log('');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log(nFail === 0 ? 'Résultat : PASS — état d\'attente ELF correct dans les 3 états (loading/failed/ready), reste du popup inchangé.' : `Résultat : ${nFail} DIFF.`);
  console.log('────────────────────────────────────────────────────────────────────');

  if (nFail > 0) process.exit(1);
}

main().catch((e) => {
  console.error('Erreur fatale du harness :', e?.stack || e);
  process.exit(2);
});
