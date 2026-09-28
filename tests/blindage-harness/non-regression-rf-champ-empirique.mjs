// ─── Non-régression : couche RF « champ estimé d'après les mesures » (2026-09-29, brief RF_CHAMP_EMPIRIQUE) ──────────
// Ce que la couche promet, et ce que ce fichier vérifie :
//  (a) RF_EMPIRIQUE est défini après le boot, et sa relation (référence retenue) tombe à ±0,05 près sur a, b et σ de la
//      relation REDÉRIVÉE ICI, dans Node, depuis les deux fichiers servis (mesures certifiées, supports mobiles), avec le
//      filtre de calibrateRF() — pas lue dans la page. Seul écart déclaré : le filtre « hors portée » (champ du modèle sous
//      0,02 V/m) n'est pas rejoué ; il exclut 0 fiche au 2026-09-29, et le test échoue si la page en exclut une.
//  (b) Aucune chaîne « 28 à 61 V/m » dans les surfaces de la couche RF : popup aux trois points fixes et légende RF, FR et
//      EN. (La légende d'une AUTRE couche, « Antennes ANFR et émetteurs TDF », porte encore cette ligne au 2026-09-29 :
//      hors du périmètre du brief, signalée à part, pas masquée ici.)
//  (c) Aux trois points fixes du brief, la classe RENDUE (pixel lu dans la tuile du canevas, zoom 15) et la médiane
//      annoncée par le popup concordent ; au-delà de la distance d'extinction, ni pixel ni estimation.
//  (d) Répartition des 4 004 points BT (échantillon de bandes_habitees.py : un tronçon sur `pas`, milieu des deux
//      premiers points) entre les classes : imprimée pour le digest, pas un critère.
// Ce qui ferait échouer ce fichier : une relation absente ou dérivée d'autres données, une ligne de popup qui ne
// correspond pas à la couleur dessinée, une classe dessinée au-delà de l'extinction, la ligne des valeurs limites revenue.
//
// Usage : node tests/blindage-harness/non-regression-rf-champ-empirique.mjs   (sort 1 si un ✘)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { createHarness } from './harness.mjs';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..', '..');
const POINTS = { Monticello: [42.6177, 8.9536], Asco: [42.4386, 8.9924], Ajaccio: [41.9263, 8.7375] };
// Zoom 15 (≈ 3,5 m par pixel en Corse) : au zoom 13 (≈ 14 m), une fenêtre de quelques pixels déborde déjà la frontière
// de classe quand le point en est à 20 m (Ajaccio : 86 m du support, borne à 103 m) — le test lirait sa propre fenêtre.
const ZOOM_CLASSES_TEST = 15;
let echecs = 0;
const ok = (cond, msg) => { console.log((cond ? '  ✔ ' : '  ✘ ') + msg); if (!cond) echecs++; };

// ─── Relation redérivée dans Node, sans la page ──────────────────────────────────────────────────────────────────────
function dist(a, b, c, d) { const R = 6371, dL = (c - a) * Math.PI / 180, dM = (d - b) * Math.PI / 180; const x = Math.sin(dL / 2) ** 2 + Math.cos(a * Math.PI / 180) * Math.cos(c * Math.PI / 180) * Math.sin(dM / 2) ** 2; return R * 2 * Math.atan2(Math.sqrt(x), Math.sqrt(1 - x)); }
function bandeMhz(p) { if (!p) return null; const m = /(\d+(?:[.,]\d+)?)\s*(kHz|MHz|GHz)\s*-\s*(\d+(?:[.,]\d+)?)\s*(kHz|MHz|GHz)/i.exec(p); if (!m) return null; const k = { khz: 1e-3, mhz: 1, ghz: 1e3 }; return parseFloat(m[3].replace(',', '.')) * k[m[4].toLowerCase()]; }
function ajuste(pts) { const n = pts.length, mx = pts.reduce((s, p) => s + p.x, 0) / n, my = pts.reduce((s, p) => s + p.y, 0) / n; let sxy = 0, sxx = 0; for (const p of pts) { sxy += (p.x - mx) * (p.y - my); sxx += (p.x - mx) ** 2; } const b = sxy / sxx, a = my - b * mx; const ss = pts.reduce((s, p) => s + (p.y - a - b * p.x) ** 2, 0); return { a, b, sigma: Math.sqrt(ss / (n - 2)), n }; }
const supports = JSON.parse(readFileSync(join(RACINE, 'public/data/supports_mobiles_anfr_corse_2026-09-28.json'), 'utf8')).supports.filter((x) => x && x.lat != null && x.lon != null);
const mesures = JSON.parse(readFileSync(join(RACINE, 'public/data/cartoradio_certified_corse.json'), 'utf8')).mesures || [];
const pool = [];
for (const m of mesures) {
  if (m.calib_eligible === false || m.conforme === false) continue;
  const bm = bandeMhz(m.protocole); if (bm != null && bm < 87.5) continue;
  if (m.valeur_max_vm == null || m.lat == null || m.lon == null || !(m.valeur_max_vm > 0) || m.type_environnement !== 'exterieur_public') continue;
  let d = Infinity; for (const s of supports) { const k = dist(m.lat, m.lon, s.lat, s.lon); if (k < d) d = k; }
  pool.push({ x: Math.log(Math.max(d * 1000, 1)), y: Math.log(m.valeur_max_vm), recente: String(m.date_mesure || '') >= '2021-01-01' });
}
const node = { pool: ajuste(pool), depuis2021: ajuste(pool.filter((p) => p.recente)) };

const h = await createHarness({ bootTimeoutMs: 60000 });
const page = h._internal.page;
try {
  await page.waitForFunction(() => typeof RF_EMPIRIQUE !== 'undefined' && RF_EMPIRIQUE !== null, undefined, { timeout: 60000, polling: 500 });

  console.log('(a) relation au boot, contre la relation redérivée dans Node');
  const R = await page.evaluate(() => ({ ...RF_EMPIRIQUE, oor: RF_CALIB_STATS && RF_CALIB_STATS.n_excl_oor }));
  const ref = R.reference === 'depuis2021' ? node.depuis2021 : node.pool;
  ok(R.oor === 0, `aucune fiche exclue « hors portée » par la page (n_excl_oor = ${R.oor}) — sinon la redérivation ne rejoue plus le filtre`);
  ok(R.n === node.pool.n && R.n21 === node.depuis2021.n, `effectifs : page ${R.n} / ${R.n21}, Node ${node.pool.n} / ${node.depuis2021.n}`);
  for (const [cle, v, w] of [['a', R.ar, ref.a], ['b', R.br, ref.b], ['σ', R.sr, ref.sigma]]) ok(Math.abs(v - w) <= 0.05, `${cle} (référence ${R.reference}) : page ${v.toFixed(3)}, Node ${w.toFixed(3)}`);

  console.log('(b) pas de ligne des valeurs limites dans les surfaces RF');
  const surfaces = await page.evaluate((pts) => {
    const out = [];
    for (const [la, lo] of Object.values(pts)) out.push(rfPopupHTML(la, lo));
    const prev = document.documentElement.lang;
    document.documentElement.lang = 'en'; for (const [la, lo] of Object.values(pts)) out.push(rfPopupHTML(la, lo)); document.documentElement.lang = prev;
    out.push(LEGEND_HTML.hotrf, LEGEND_HTML_EN.hotrf);
    document.querySelectorAll('#leg-rf-classes,#leg-rf-reference').forEach((el) => out.push(el.innerHTML));
    return out.join('\n');
  }, POINTS);
  ok(!/28 à 61 V\/m|28 to 61 V\/m/.test(surfaces), 'ni « 28 à 61 V/m » ni « 28 to 61 V/m » dans le popup (3 points, FR et EN) ni dans la légende RF');
  ok(!/exposition|exposure/i.test(surfaces), 'ni « exposition » ni « exposure » dans ces mêmes surfaces');

  console.log('(c) classe dessinée et popup, aux trois points fixes (zoom ' + ZOOM_CLASSES_TEST + ')');
  for (const [nom, [la, lo]] of Object.entries(POINTS)) {
    await page.evaluate(([la, lo, z]) => map.setView([la, lo], z, { animate: false }), [la, lo, ZOOM_CLASSES_TEST]);
    const r = await page.evaluate(async ([la, lo]) => {
      const couche = lHotRF.getLayers()[0];
      if (!couche) return { erreur: 'couche RF absente' };
      const z = map.getZoom(), p = map.project([la, lo], z), tx = Math.floor(p.x / 256), ty = Math.floor(p.y / 256);
      const cle = tx + ':' + ty + ':' + z;
      for (let k = 0; k < 60 && !(couche._tiles[cle] && couche._tiles[cle].loaded); k++) await new Promise((r) => setTimeout(r, 250));
      const t = couche._tiles[cle];
      if (!t) return { erreur: 'tuile ' + cle + ' absente' };
      const px = Math.floor(p.x - tx * 256), py = Math.floor(p.y - ty * 256);
      // Pixel coloré le plus proche du point (la hachure laisse un pixel sur deux transparent), à 3 px au plus.
      const x0 = Math.max(0, px - 3), y0 = Math.max(0, py - 3), d = t.el.getContext('2d').getImageData(x0, y0, 7, 7).data;
      let rgb = null, best = Infinity;
      for (let yy = 0; yy < 7; yy++) for (let xx = 0; xx < 7; xx++) { const i = (yy * 7 + xx) * 4, q = (x0 + xx - px) ** 2 + (y0 + yy - py) ** 2; if (d[i + 3] > 0 && q < best) { best = q; rgb = [d[i], d[i + 1], d[i + 2]]; } }
      const txt = rfPopupHTML(la, lo).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
      const m = txt.match(/Champ estimé ici d’après la distance : médiane ([\d,]+) V\/m/);
      const med = m ? parseFloat(m[1].replace(',', '.')) : null;
      const attendue = med != null ? rfEmpiriqueClasse(rfChampEmpiriqueEn(la, lo).champ.med) : null;
      return { rgb, med, pasEstimation: /pas d’estimation/.test(txt), attendue, palette: RF_EMPIRIQUE_RGB };
    }, [la, lo]);
    if (r.erreur) { ok(false, `${nom} : ${r.erreur}`); continue; }
    if (r.med == null) {
      ok(r.pasEstimation && r.rgb == null, `${nom} : au-delà de l'extinction — popup « pas d'estimation », aucun pixel dessiné (${r.rgb ? 'pixel ' + r.rgb.join(',') : 'aucun pixel'})`);
    } else {
      const c = r.palette[Math.min(r.attendue, r.palette.length - 1)];
      ok(r.rgb && r.rgb.join(',') === c.join(','), `${nom} : popup médiane ${r.med} V/m → classe ${r.attendue} (${c.join(',')}), pixel dessiné ${r.rgb ? r.rgb.join(',') : 'aucun'}`);
    }
  }

  console.log('(d) répartition des 4 004 points BT (pour le digest)');
  const rep = await page.evaluate(async () => {
    const bt = await (await fetch('public/data/bt_lines_agregat.json')).json();
    const pas = Math.max(1, Math.floor(bt.length / 4000)), c = {};
    let n = 0;
    for (let i = 0; i < bt.length; i += pas) {
      const p = bt[i] && bt[i].pts; if (!Array.isArray(p) || p.length < 2) continue;
      let la, lo; const [a, b] = p;
      if (!Array.isArray(a)) { la = (a.lat + b.lat) / 2; lo = (a.lon + b.lon) / 2; } else { la = (a[0] + b[0]) / 2; lo = (a[1] + b[1]) / 2; }
      if (la < 20) [la, lo] = [lo, la];
      const e = rfChampEmpiriqueEn(la, lo), k = e && e.classe != null ? 'classe ' + e.classe : 'éteint';
      c[k] = (c[k] || 0) + 1; n++;
    }
    return { n, pas, comptes: c, reference: RF_EMPIRIQUE.reference, bornes: RF_EMPIRIQUE.bornes_vm, d_extinction_m: Math.round(RF_EMPIRIQUE.d_extinction_m) };
  });
  console.log('  ' + JSON.stringify(rep));
  ok(rep.n === 4004, `échantillon de ${rep.n} points (attendu 4 004 avec le fichier du 2026-09-28)`);

  const diag = h.diagnostics();
  const erreursRF = diag.consoleErrors.filter((e) => /RF|tuile|rf[A-Z]/i.test(e));
  ok(erreursRF.length === 0, `aucune erreur console liée à la couche RF (${erreursRF.length})`);
} finally {
  await h.close();
}
console.log(echecs ? `\n${echecs} échec(s)` : '\ntout est vert');
process.exit(echecs ? 1 : 0);
