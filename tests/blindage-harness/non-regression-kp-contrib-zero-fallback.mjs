// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Non-régression : Kp=0/Bz=0/attenuation=0 survivent à l'écriture
// Création : 2026-09-04 · dette KP-ZERO-FALLBACK-LIVE-ET-CONTRIB-001
// Révisé  : 2026-09-04 (revue adversariale PR #1233) — v1 réimplémentait le motif
// à la main sans jamais lire le code réel : un futur retour à `||null` dans
// saveContrib() serait resté invisible. v2 ajoute une assertion de SOURCE RÉELLE
// (saveContrib.toString()) en plus du test comportemental — la fonction n'est
// jamais invoquée (elle a des dépendances DOM lourdes et écrirait réellement en
// base), mais son code source tel que servi est inspecté directement.
// ═══════════════════════════════════════════════════════════════════════════
//
// Contexte : saveContrib() construisait kp/bz/densite_protons/flux_protons/
// attenuation_prevue_db avec `X||null` — une valeur 0 légitime (Kp calme,
// IMF Bz neutre, aucun matériau sélectionné) devenait indiscernable d'une
// valeur absente/invalide, puis le garde anti-PGRST204 (Object.keys(row).
// forEach(k=>{if(row[k]===null||row[k]===undefined)delete row[k];})) supprimait
// la clé avant l'INSERT Supabase — perte de donnée à l'écriture, pas un
// simple défaut d'affichage. Corrigé en Number.isFinite(x)?x:null.
//
// Ne déclenche AUCUN appel réseau/Supabase réel.
// ═══════════════════════════════════════════════════════════════════════════

import { createHarness } from './harness.mjs';

async function main() {
  const harness = await createHarness();
  let nFail = 0;

  try {
    // ── 1. Assertion de source réelle — lit saveContrib.toString() tel que servi ──
    const src = await harness.evalInPage(() => {
      // eslint-disable-next-line no-undef
      return typeof saveContrib === 'function' ? saveContrib.toString() : null;
    });
    if (!src) {
      nFail++;
      console.log('[DIFF] saveContrib introuvable dans la page — impossible de vérifier la source');
    } else {
      const sourceChecks = [
        { label: 'kp: Number.isFinite(...) présent', ok: /kp\s*:\s*Number\.isFinite\(kpNum\)/.test(src) },
        { label: 'bz: Number.isFinite(...) présent', ok: /bz\s*:\s*Number\.isFinite\(bzNum\)/.test(src) },
        { label: 'densite_protons: Number.isFinite(...) présent', ok: /densite_protons\s*:\s*Number\.isFinite\(densNum\)/.test(src) },
        { label: 'flux_protons: Number.isFinite(...) présent', ok: /flux_protons\s*:\s*Number\.isFinite\(fluxNum\)/.test(src) },
        { label: 'attenuation_prevue_db sans ||null', ok: /attenuation_prevue_db\s*:\s*attenPrevue\s*,/.test(src) && !/attenuation_prevue_db\s*:\s*attenPrevue\s*\|\|/.test(src) },
        { label: 'aucun regret vers parseFloat(curKp)||null', ok: !/kp\s*:\s*parseFloat\(curKp\)\s*\|\|\s*null/.test(src) },
      ];
      for (const c of sourceChecks) {
        if (!c.ok) nFail++;
        console.log(`[${c.ok ? 'PASS' : 'DIFF'}] source réelle — ${c.label}`);
      }
    }

    // ── 2. Comportement — mêmes globales que saveContrib() lit réellement (curKp/curBz/
    //    curDensity/curFlux, script-scope `let`, assignées par nom nu comme le fait déjà
    //    harness.setRuntimeState() pour curKp) ──
    const cases = [
      { value: '0', expectKept: true, expectValue: 0 },       // Kp calme / Bz neutre — le cas régressé
      { value: '-2.5', expectKept: true, expectValue: -2.5 }, // Bz sud négatif — jamais affecté (déjà truthy)
      { value: '3.7', expectKept: true, expectValue: 3.7 },
      { value: '', expectKept: false, expectValue: null },    // champ vide — absence réelle, doit rester null
      { value: 'N/A', expectKept: false, expectValue: null }, // fetch échoué / placeholder — absence réelle
    ];

    for (const c of cases) {
      const r = await harness.evalInPage((newVal) => {
        // eslint-disable-next-line no-undef
        curKp = newVal; // même variable script-scope que lit réellement saveContrib()
        // eslint-disable-next-line no-undef
        const kpNum = parseFloat(curKp); // ligne identique à celle de saveContrib()
        const value = Number.isFinite(kpNum) ? kpNum : null;
        const row = { kp: value };
        // Garde anti-PGRST204 identique à app.html (copié, pas exécutable autrement sans DOM complet)
        Object.keys(row).forEach(k => { if (row[k] === null || row[k] === undefined) delete row[k]; });
        return { value, kept: Object.prototype.hasOwnProperty.call(row, 'kp') };
      }, c.value);

      const ok = r.kept === c.expectKept && r.value === c.expectValue;
      if (!ok) nFail++;
      console.log(`[${ok ? 'PASS' : 'DIFF'}] curKp="${c.value}" → value=${r.value}, kept=${r.kept} (attendu value=${c.expectValue}, kept=${c.expectKept})`);
    }
  } finally {
    await harness.close();
  }

  console.log('');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log(nFail === 0 ? 'Résultat : PASS — source réelle + comportement conformes (Kp=0 survit, absence réelle reste null).' : `Résultat : ${nFail} DIFF.`);
  console.log('────────────────────────────────────────────────────────────────────');

  if (nFail > 0) process.exit(1);
}

main().catch((e) => {
  console.error('Erreur fatale du harness :', e?.stack || e);
  process.exit(2);
});
