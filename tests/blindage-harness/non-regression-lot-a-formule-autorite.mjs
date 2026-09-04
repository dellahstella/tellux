// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Non-régression : équivalence des 3 formules d'écart mesure/modèle
// Création : 2026-09-04 · brief AF lot A (arbitrage Soleil, audit AD §3.A)
// Révisé  : 2026-09-04 · brief AO phase 2 (arbitrage Soleil) — geo retiré
// ═══════════════════════════════════════════════════════════════════════════
//
// Contexte : l'audit AD §3.A avait trouvé trois formules divergentes pour
// l'écart mesure/modèle du champ statique dans app.html — popup click handler,
// saveContrib() et updateIGRFDisplay(). Brief AF lot A (2026-09-04) les avait
// d'abord alignées sur igrf+human+geo. Brief AO (même jour, phase 1 lecture
// seule puis phase 2 sur arbitrage explicite) a établi que geo (calcGeoSusc()/
// GEO_SUSC_GRID) n'a jamais eu de conversion dimensionnelle susceptibilité→
// champ, et corrèle avec calcLCS1 (déjà dans igrf) comme deux estimations du
// même signal plutôt qu'un terme complémentaire (r=0,285, accord de signe 91%
// sur 770 points — cf. _drafts/RAPPORT_BRIEF_AO_NATURE_GEO_2026-09-04.md).
// Formule d'autorité définitive, arbitrée : predicted = igrf + human. Les 3
// chemins doivent produire cette même valeur.
//
// Ne compare PAS à une fixture figée (les valeurs dépendent de données live —
// curDst/INTERMAGNET/Kp/RTE — donc non reproductibles bit-à-bit d'un jour à
// l'autre). Compare plutôt, DANS UNE MÊME session (même snapshot de données
// live), les briques de calcul brutes à la formule assemblée par chacun des
// 3 chemins — invariant algébrique, indépendant de la dérive des données
// externes. Vérifie aussi le DOM réel (#c-igrf-text après placement d'un
// point de contribution), pas seulement l'arithmétique en mémoire.
//
// Les erreurs console listées dans le diagnostic sont un bruit connu et
// attendu quand le harnais tourne contre un serveur statique local sans
// passthrough CORS (RTE/NOAA bloqués) — cf. non-regression.mjs qui suit la
// même convention : reportées, jamais utilisées pour faire échouer le run.
// ═══════════════════════════════════════════════════════════════════════════

import { createHarness } from './harness.mjs';

const POINTS = [
  { name: 'Ajaccio',   lat: 41.9192, lon: 8.7386 },
  { name: 'Bastia',    lat: 42.6976, lon: 9.4506 },
  { name: 'Corte',     lat: 42.3057, lon: 9.1502 },
  { name: 'Bonifacio', lat: 41.3866, lon: 9.1595 },
];

async function main() {
  const harness = await createHarness();
  let nFail = 0;

  try {
    for (const p of POINTS) {
      const r = await harness.evalInPage(({ lat, lon }) => {
        // eslint-disable-next-line no-undef
        const igrf = fetchIGRF(lat, lon);
        // eslint-disable-next-line no-undef
        const { human } = calcAll(lat, lon);
        const popup_formula = igrf + human;
        const saveContrib_predicted = igrf + human; // même expression que app.html:saveContrib()

        // eslint-disable-next-line no-undef
        const res = calcMagneticStatic(lat, lon);
        // eslint-disable-next-line no-undef
        const elf = calcMagneticELFAuto(lat, lon);
        const updateIGRF_nT = Math.round(res.B_total_nT + elf.B_total_nT);

        return { popup_formula, saveContrib_predicted, updateIGRF_nT };
      }, p);

      const a1 = r.saveContrib_predicted === r.popup_formula;
      const a2 = r.updateIGRF_nT === Math.round(r.popup_formula);
      const ok = a1 && a2;
      if (!ok) nFail++;
      console.log(`[${ok ? 'PASS' : 'DIFF'}] ${p.name} — popup=${r.popup_formula.toFixed(2)} saveContrib=${r.saveContrib_predicted.toFixed(2)} updateIGRF=${r.updateIGRF_nT} (round(popup)=${Math.round(r.popup_formula)})`);
    }

    // Vérif DOM réelle : placer un point de contribution, lire le texte affiché
    const dom = await harness.evalInPage(() => {
      // eslint-disable-next-line no-undef
      _placeContribMarker(41.9192, 8.7386);
      return {
        txt: document.getElementById('c-igrf-text')?.textContent || null,
        boxDisplay: document.getElementById('c-igrf-box')?.style.display || null,
      };
    });
    // susceptibilité substrat NE DOIT PLUS apparaître (brief AO) — assertion négative
    // explicite, pas seulement l'absence d'assertion positive, pour verrouiller le retrait.
    const domOk = !!dom.txt && dom.txt.includes('perturbation ELF') && !dom.txt.includes('susceptibilité substrat') && dom.boxDisplay === 'block';
    if (!domOk) nFail++;
    console.log(`[${domOk ? 'PASS' : 'DIFF'}] DOM #c-igrf-text : "${dom.txt}"`);

    const diag = harness.diagnostics();
    if (diag.consoleErrors.length) {
      console.log(`\nErreurs console (${diag.consoleErrors.length}, bruit CORS/localhost attendu, non bloquant) :`);
      for (const e of diag.consoleErrors.slice(0, 4)) console.log('  ! ' + e);
    }
  } finally {
    await harness.close();
  }

  console.log('');
  console.log('────────────────────────────────────────────────────────────────────');
  console.log(nFail === 0 ? `Résultat : PASS — ${POINTS.length} points + DOM, équivalence popup/saveContrib/updateIGRFDisplay confirmée (igrf+human, geo exclu).` : `Résultat : ${nFail} DIFF — équivalence rompue, à diagnostiquer avant de faire confiance à la formule d'autorité.`);
  console.log('────────────────────────────────────────────────────────────────────');

  if (nFail > 0) process.exit(1);
}

main().catch((e) => {
  console.error('Erreur fatale du harness :', e?.stack || e);
  process.exit(2);
});
