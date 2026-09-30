// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Non-régression : le forfait BT ne dépend pas du stockage des lignes BT
// Création : 2026-09-29 · forfait BT fondé sur la longueur de réseau (btLongueurZone)
// ═══════════════════════════════════════════════════════════════════════════
//
// Contexte : jusqu'au 2026-09-29, le forfait BT de calcMagneticELF_v2 comptait des SEGMENTS. Ce nombre dépend de la
// façon dont les tracés sont découpés, pas du réseau : couper chaque segment en deux changeait le palier de l'Indice
// en 217 points sur 1 340. Le forfait se fonde désormais sur la LONGUEUR de réseau BT dans la zone.
//
// Ce test rejoue, DANS LA PAGE RÉELLE (fonctions servies, aucune réimplémentation du forfait), quatre perturbations
// qui ne changent pas le réseau physique, et exige que le forfait BT ne bouge en aucun des 236 points certifiés :
//   P2 — chaque segment coupé en son milieu ;
//   P3 — le premier sommet d'une ligne sur dix déplacé de 1 cm (1e-7° de latitude) ;
//   P4 — ordre des lignes inversé, une ligne sur deux retournée ;
//   P5 — pour une ligne sur dix, un segment de longueur nulle et un segment en double ajoutés.
// Les seuils, dérivés au chargement (BT_ZONE_SEUILS_M), ne doivent pas bouger non plus : à 1e-6 près pour P2, P4 et P5,
// à 1 % près pour P3. Motif de l'exception, mesuré le 2026-09-29 : un segment présent en double dans l'agrégat (même
// paire d'extrémités, dédoublonné) cesse d'être un double exact quand l'une de ses copies est décalée de 1 cm ; sa
// longueur compte alors deux fois (1 261 segments de plus). Seuils +1,2 m et +46 m (0,03 % et 0,4 %) ; forfait
// inchangé aux 236 points. Une première version de ce test, à 1 m près pour P3, a échoué pour cette raison.
//
// Contre-épreuve : le forfait par COMPTE de segments (seuils 96 / 290, #1636), recalculé sur la même grille
// (BT_SEGMENT_GRID, inchangée), DOIT changer sous P2. Sinon le test ne saurait pas voir le défaut qu'il garde.
//
// État restauré à la fin (grille reconstruite sur l'agrégat d'origine), et la restauration est vérifiée.
// Lancer : node tests/blindage-harness/non-regression-forfait-bt-decoupage.mjs   (code de sortie 1 en cas d'échec)
// ═══════════════════════════════════════════════════════════════════════════

import { createHarness } from './harness.mjs';

async function main() {
  const h = await createHarness();
  let nFail = 0;
  const assert = (cond, label) => { if (!cond) { nFail++; console.log('[DIFF] ' + label); } else { console.log('[PASS] ' + label); } };
  try {
    await h.waitForFieldData({ requireBT: true, requireHTA: true, requireANFR: false, requireCalibratedRF: false });
    const r = await h.evalInPage(async () => {
      const rows = await (await fetch('public/data/bt_lines_agregat.json')).json();
      const pts = (await (await fetch('public/data/cartoradio_certified_corse.json')).json()).mesures.map(m => [m.lat, m.lon]);
      /* eslint-disable no-undef */
      const forfait = () => pts.map(([a, o]) => {
        const c = calcMagneticELF_v2(a, o).contributions.find(x => x.source_type === 'BT_zone_densite');
        return c ? c.B_nT : 0;
      });
      const compte = () => pts.map(([a, o]) => {
        const n = (BT_SEGMENT_GRID[tileKey(a, o)] || []).length;
        return n >= 290 ? 180 : n >= 96 ? 115 : n >= 1 ? 70 : 0;
      });
      const P = {
        P2_decoupage: L => L.map(r => ({ ...r, pts: Array.isArray(r.pts) ? r.pts.flatMap((p, i) => i === 0 ? [p] : [[(r.pts[i - 1][0] + p[0]) / 2, (r.pts[i - 1][1] + p[1]) / 2], p]) : r.pts })),
        P3_coupure: L => L.map((r, i) => i % 10 === 0 && Array.isArray(r.pts) && r.pts.length > 1 ? { ...r, pts: [[r.pts[0][0] + 1e-7, r.pts[0][1]], ...r.pts.slice(1)] } : r),
        P4_ordre: L => L.slice().reverse().map((r, i) => i % 2 && Array.isArray(r.pts) ? { ...r, pts: r.pts.slice().reverse() } : r),
        P5_degeneres: L => [...L, ...L.filter((r, i) => i % 10 === 0 && Array.isArray(r.pts) && r.pts.length > 1).flatMap(r => [{ ...r, pts: [r.pts[0], r.pts[0]] }, { ...r, pts: [r.pts[0], r.pts[1]] }])],
      };
      buildBTSegmentGrid(rows);
      const base = forfait(), baseCompte = compte(), seuils = BT_ZONE_SEUILS_M ? BT_ZONE_SEUILS_M.slice() : null;
      const out = { points: pts.length, seuils, base_non_nuls: base.filter(x => x > 0).length, perturbations: {} };
      for (const [k, f] of Object.entries(P)) {
        buildBTSegmentGrid(f(rows));
        const v = forfait(), c = compte();
        out.perturbations[k] = { forfait_change: v.filter((x, i) => x !== base[i]).length, compte_change: c.filter((x, i) => x !== baseCompte[i]).length,
          seuils: BT_ZONE_SEUILS_M ? BT_ZONE_SEUILS_M.slice() : null };
      }
      buildBTSegmentGrid(rows);
      const rest = forfait();
      out.restaure = rest.every((x, i) => x === base[i]) && JSON.stringify(BT_ZONE_SEUILS_M) === JSON.stringify(seuils);
      /* eslint-enable no-undef */
      return out;
    });
    console.log('points : ' + r.points + ' ; forfait BT non nul en ' + r.base_non_nuls + ' ; seuils (m) : ' + (r.seuils ? r.seuils.map(x => x.toFixed(1)).join(' / ') : 'aucun'));
    assert(Array.isArray(r.seuils) && r.seuils[0] > 0 && r.seuils[1] > r.seuils[0], 'seuils dérivés au chargement, positifs et ordonnés');
    assert(r.base_non_nuls > 0, 'le forfait BT est présent en au moins un point (sinon le test ne mesure rien)');
    for (const [k, p] of Object.entries(r.perturbations)) {
      assert(p.forfait_change === 0, k + ' : forfait BT inchangé aux ' + r.points + ' points (' + p.forfait_change + ' changent)');
      const rel = k === 'P3_coupure' ? 0.01 : 1e-6;
      assert(p.seuils && Math.abs(p.seuils[0] - r.seuils[0]) <= rel * r.seuils[0] && Math.abs(p.seuils[1] - r.seuils[1]) <= rel * r.seuils[1],
        k + ' : seuils inchangés à ' + (k === 'P3_coupure' ? '1 %' : '1e-6 en relatif') + ' près (' + (p.seuils ? p.seuils.map(x => x.toFixed(1)).join(' / ') : 'aucun') + ')');
    }
    assert(r.perturbations.P2_decoupage.compte_change > 0, 'contre-épreuve : le forfait par compte de segments change sous P2 (' + r.perturbations.P2_decoupage.compte_change + ' points)');
    assert(r.restaure, 'état restauré (forfaits et seuils d\'origine)');
  } finally {
    await h.close();
  }
  console.log(nFail ? '\n' + nFail + ' échec(s)' : '\nTout est vert.');
  process.exitCode = nFail ? 1 : 0;
}
main().catch(e => { console.error(e); process.exitCode = 1; });
