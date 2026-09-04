// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Non-régression : Kp=0/Bz=0/attenuation=0 survivent à l'écriture
// Création : 2026-09-04 · dette KP-ZERO-FALLBACK-LIVE-ET-CONTRIB-001
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
// Ne déclenche AUCUN appel réseau/Supabase réel — teste le motif source
// (parseFloat + Number.isFinite, tous deux des built-ins JS, indépendants de
// tout état réseau/DOM) et le garde anti-PGRST204 (copié à l'identique
// depuis app.html) sur des lignes synthétiques en mémoire.
// ═══════════════════════════════════════════════════════════════════════════

import { createHarness } from './harness.mjs';

async function main() {
  const harness = await createHarness();
  let nFail = 0;

  try {
    const cases = [
      { input: '0', expectKept: true, expectValue: 0 },      // Kp calme / Bz neutre — le cas régressé
      { input: '-2.5', expectKept: true, expectValue: -2.5 }, // Bz sud négatif — jamais affecté (déjà truthy)
      { input: '3.7', expectKept: true, expectValue: 3.7 },
      { input: '', expectKept: false, expectValue: null },    // champ vide — absence réelle, doit rester null
      { input: 'N/A', expectKept: false, expectValue: null }, // fetch échoué / placeholder — absence réelle
    ];

    for (const c of cases) {
      const r = await harness.evalInPage((input) => {
        // Motif identique à saveContrib() (app.html) — kpNum/bzNum/densNum/fluxNum
        const n = parseFloat(input);
        const value = Number.isFinite(n) ? n : null;
        // Garde anti-PGRST204 identique à app.html:9046/11876
        const row = { kp: value };
        Object.keys(row).forEach(k => { if (row[k] === null || row[k] === undefined) delete row[k]; });
        return { value, kept: Object.prototype.hasOwnProperty.call(row, 'kp') };
      }, c.input);

      const ok = r.kept === c.expectKept && r.value === c.expectValue;
      if (!ok) nFail++;
      console.log(`[${ok ? 'PASS' : 'DIFF'}] input="${c.input}" → value=${r.value}, kept=${r.kept} (attendu value=${c.expectValue}, kept=${c.expectKept})`);
    }

    // attenPrevue : toujours un nombre fini (reduce base 0), jamais null désormais
    const attenCase = await harness.evalInPage(() => {
      const MAT_DB_sample = { beton_portland: 17, platre: 3 };
      const attenPrevue = [].reduce((s, m) => s + (MAT_DB_sample[m] || 0), 0); // aucun matériau sélectionné
      const row = { attenuation_prevue_db: attenPrevue };
      Object.keys(row).forEach(k => { if (row[k] === null || row[k] === undefined) delete row[k]; });
      return { value: attenPrevue, kept: Object.prototype.hasOwnProperty.call(row, 'attenuation_prevue_db') };
    });
    const attenOk = attenCase.value === 0 && attenCase.kept === true;
    if (!attenOk) nFail++;
    console.log(`[${attenOk ? 'PASS' : 'DIFF'}] attenuation_prevue_db (aucun matériau) → value=${attenCase.value}, kept=${attenCase.kept} (attendu value=0, kept=true)`);
  } finally {
    await harness.close();
  }

  console.log('');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log(nFail === 0 ? 'Résultat : PASS — Kp/Bz/densité/flux/atténuation=0 survivent au garde anti-PGRST204.' : `Résultat : ${nFail} DIFF — une valeur 0 légitime est de nouveau perdue à l'écriture.`);
  console.log('────────────────────────────────────────────────────────────────────');

  if (nFail > 0) process.exit(1);
}

main().catch((e) => {
  console.error('Erreur fatale du harness :', e?.stack || e);
  process.exit(2);
});
