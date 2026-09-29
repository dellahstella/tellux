// ─── Non-régression : couche RF « champ estimé d'après les mesures » (2026-09-29, brief RF_CHAMP_EMPIRIQUE) ──────────
// Ce que la couche promet, et ce que ce fichier vérifie :
//  (a) RF_EMPIRIQUE est défini après le boot, et sa relation (référence retenue) tombe à ±0,05 près sur a, b et σ de la
//      relation REDÉRIVÉE ICI, dans Node, depuis les deux fichiers servis (mesures certifiées, supports mobiles), avec le
//      filtre de calibrateRF() — pas lue dans la page. Seul écart déclaré : le filtre « hors portée » (champ du modèle sous
//      0,02 V/m) n'est pas rejoué ; il exclut 0 fiche au 2026-09-29, et le test échoue si la page en exclut une.
//      Même chose pour la borne unique des deux classes (décision du 2026-09-29) : redérivée ici — moyenne géométrique
//      des médianes des bandes 50–150 m et 150 m–1 km du pool, à un chiffre significatif — et comparée à la page.
//  (b) Aucune valeur limite « 28 à 61 V/m » (ou 28–61) nulle part dans le document rendu, en français puis en anglais
//      (page rechargée avec ?lang=en) : nœuds de texte et attributs visibles, hors scripts — depuis #1648 et #1650, plus
//      aucune ne s'affiche. Et, dans les surfaces de la couche RF (popup aux trois points fixes, légende, FR et EN) : la
//      même chaîne, et ni « exposition » ni « exposure ».
//  (c) Aux trois points fixes du brief, la classe RENDUE (pixel lu dans la tuile du canevas, zoom 15) et la médiane
//      annoncée par le popup concordent ; au-delà de la distance d'extinction, ni pixel ni estimation.
//  (d) Répartition des 4 004 points BT (échantillon de bandes_habitees.py : un tronçon sur `pas`, milieu des deux
//      premiers points) entre les deux classes et l'extinction : imprimée pour le digest ; le critère est qu'il n'y ait
//      que ces trois cas.
//  (e) Sous le zoom des classes (lecture de l'évaluateur du 2026-09-29 : l'île montre ce qu'on sait, le bourg ce qu'on
//      estime), seulement le mesuré : au zoom 9, rien sur un support loin de toute mesure ; un point de la teinte de sa
//      classe sur un lieu mesuré (Piana, fiche du 15/01/2026) ; une cellule pleine dans une zone d'interpolation.
//  (f) Masque terre (décision du 2026-09-29) : la surface estimée s'arrête à la côte. Deux points fixes, choisis hors
//      ligne sur les contours communaux BRUTS (sans tampon ni simplification), à plus de 400 m de la côte : en mer, dans
//      le golfe d'Ajaccio, à 1 199 m du support le plus proche ; à terre, à 1 185 m du sien. Sans masque, les deux
//      porteraient une estimation (en deçà de l'extinction). Au zoom 15 : rien en mer, une estimation à terre ; le popup
//      en mer le dit. Et : les petites îles (Lavezzi, Grande Sanguinaire) comptent comme terre ; aucun support mobile ni
//      lieu mesuré ne tombe en mer.
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
// Zoom 15 (≈ 3,5 m par pixel en Corse) : au zoom 13 (≈ 14 m), une fenêtre de quelques pixels déborde déjà une frontière
// de classe quand le point en est à 20 m — le test lirait sa propre fenêtre. (Au premier état, Ajaccio était à 86 m du
// support pour une borne à 103 m ; à deux classes, la borne est à 242 m, 2026-09-29.)
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
  pool.push({ x: Math.log(Math.max(d * 1000, 1)), y: Math.log(m.valeur_max_vm), d_m: d * 1000, v: m.valeur_max_vm, recente: String(m.date_mesure || '') >= '2021-01-01' });
}
const node = { pool: ajuste(pool), depuis2021: ajuste(pool.filter((p) => p.recente)) };
// Borne unique (décision du 2026-09-29) : bandes 50–150 m et 150 m–1 km de TOUT le pool, comme RF_BANDES_STATS ; médiane
// par interpolation linéaire des quantiles ; chacune d'au moins 10 mesures (RF_BANDE_N_MIN).
const medianeInterp = (v) => { const s = v.slice().sort((a, b) => a - b), i = (s.length - 1) * 0.5, lo = Math.floor(i), hi = Math.ceil(i); return s[lo] + (s[hi] - s[lo]) * (i - lo); };
const unChiffre = (x) => { const e = Math.floor(Math.log10(x)); return Math.round(x / Math.pow(10, e)) * Math.pow(10, e); };
const b1 = pool.filter((p) => p.d_m >= 50 && p.d_m < 150).map((p) => p.v), b2 = pool.filter((p) => p.d_m >= 150 && p.d_m < 1000).map((p) => p.v);
node.borne = b1.length >= 10 && b2.length >= 10 ? unChiffre(Math.sqrt(medianeInterp(b1) * medianeInterp(b2))) : null;
node.medianes_bandes = [medianeInterp(b1), medianeInterp(b2)];

const h = await createHarness({ bootTimeoutMs: 60000 });
const page = h._internal.page;
try {
  await page.waitForFunction(() => typeof RF_EMPIRIQUE !== 'undefined' && RF_EMPIRIQUE !== null, undefined, { timeout: 60000, polling: 500 });
  // Le masque terre se charge avec la couche : tant qu'il est attendu, aucune tuile ne dessine d'estimé (cf. app.html).
  await page.waitForFunction(() => typeof TERRE_CORSE_ETAT !== 'undefined' && TERRE_CORSE_ETAT !== 'attente', undefined, { timeout: 60000, polling: 500 });

  console.log('(a) relation au boot, contre la relation redérivée dans Node');
  const R = await page.evaluate(() => ({ ...RF_EMPIRIQUE, oor: RF_CALIB_STATS && RF_CALIB_STATS.n_excl_oor }));
  const ref = R.reference === 'depuis2021' ? node.depuis2021 : node.pool;
  ok(R.oor === 0, `aucune fiche exclue « hors portée » par la page (n_excl_oor = ${R.oor}) — sinon la redérivation ne rejoue plus le filtre`);
  ok(R.n === node.pool.n && R.n21 === node.depuis2021.n, `effectifs : page ${R.n} / ${R.n21}, Node ${node.pool.n} / ${node.depuis2021.n}`);
  for (const [cle, v, w] of [['a', R.ar, ref.a], ['b', R.br, ref.b], ['σ', R.sr, ref.sigma]]) ok(Math.abs(v - w) <= 0.05, `${cle} (référence ${R.reference}) : page ${v.toFixed(3)}, Node ${w.toFixed(3)}`);
  ok(Array.isArray(R.bornes_vm) && R.bornes_vm.length === 1 && node.borne != null && Math.abs(R.bornes_vm[0] - node.borne) < 1e-9,
    `une seule borne, redérivée : page ${JSON.stringify(R.bornes_vm)} V/m, Node ${node.borne} V/m (√(${node.medianes_bandes.map((x) => x.toFixed(3)).join(' × ')}), un chiffre significatif)`);
  // La garde de séparation : elle doit signaler le cas qui a décidé des deux classes (trois classes au 2026-09-29, mesures
  // comparables depuis 2021 : 36 à 1,05 V/m, 19 à 1,14, 5 à 0,32), et rester muette sur les deux classes servies.
  const garde = await page.evaluate(() => ({
    troisClasses: rfEmpiriqueNonSeparees([{ n: 36, med: 1.05 }, { n: 19, med: 1.14 }, { n: 5, med: 0.32 }]),
    servies: rfEmpiriqueNonSeparees(RF_EMPIRIQUE.classes_mesures),
    medianes: RF_EMPIRIQUE.classes_mesures.map((c) => (c.n ? +c.med.toFixed(3) : null)), effectifs: RF_EMPIRIQUE.classes_mesures.map((c) => c.n) }));
  ok(JSON.stringify(garde.troisClasses) === '[[0,1]]', `la garde signale le cas des trois classes (1,05 puis 1,14 V/m) : ${JSON.stringify(garde.troisClasses)}`);
  ok(garde.servies.length === 0, `deux classes servies : médianes mesurées ${garde.medianes.join(' / ')} V/m (${garde.effectifs.join(' / ')} mesures), séparées`);

  console.log('(b) pas de valeur limite 28–61 V/m affichée ; surfaces RF sans « exposition »');
  // Texte du document tel qu'une personne peut le rencontrer : nœuds de texte et attributs visibles, hors scripts et
  // styles (un commentaire de code cite encore « ICNIRP 28-61 V/m » : ce n'est pas de l'affichage).
  const LIMITE = /(?<![\d.,])28\s*(?:à|to|–|-)\s*61(?!\d)/;
  const texteDom = () => page.evaluate(() => {
    const out = [document.title], w = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT,
      { acceptNode: (n) => (n.nodeType === 1 && /^(SCRIPT|STYLE|TEMPLATE|NOSCRIPT)$/.test(n.tagName) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT) });
    for (let n = w.nextNode(); n; n = w.nextNode()) { if (n.nodeType === 3) out.push(n.nodeValue); else for (const a of ['title', 'aria-label', 'alt', 'placeholder']) { const v = n.getAttribute(a); if (v) out.push(v); } }
    return { lang: document.documentElement.lang, texte: out.join(' ') };
  });
  const domFr = await texteDom();
  const mFr = domFr.texte.match(LIMITE);
  ok(!mFr, `document rendu (${domFr.lang || 'fr'}, ${domFr.texte.length} caractères) : aucune valeur limite 28–61 V/m${mFr ? ' — trouvé « ' + domFr.texte.slice(Math.max(0, mFr.index - 40), mFr.index + 40) + ' »' : ''}`);
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

  console.log('(e) sous le zoom des classes (zoom 9) : seulement le mesuré');
  const lirePixel = async (la, lo, z, rayon) => {
    await page.evaluate(([la, lo, z]) => map.setView([la, lo], z, { animate: false }), [la, lo, z]);
    return await page.evaluate(async ([la, lo, rayon]) => {
      const couche = lHotRF.getLayers()[0]; if (!couche) return { erreur: 'couche RF absente' };
      const z = map.getZoom(), p = map.project([la, lo], z), tx = Math.floor(p.x / 256), ty = Math.floor(p.y / 256), cle = tx + ':' + ty + ':' + z;
      for (let k = 0; k < 60 && !(couche._tiles[cle] && couche._tiles[cle].loaded); k++) await new Promise((r) => setTimeout(r, 250));
      const t = couche._tiles[cle]; if (!t) return { erreur: 'tuile ' + cle + ' absente' };
      const px = Math.floor(p.x - tx * 256), py = Math.floor(p.y - ty * 256), x0 = Math.max(0, px - rayon), y0 = Math.max(0, py - rayon), w = 2 * rayon + 1;
      const d = t.el.getContext('2d').getImageData(x0, y0, w, w).data;
      let rgb = null, best = Infinity;
      for (let yy = 0; yy < w; yy++) for (let xx = 0; xx < w; xx++) { const i = (yy * w + xx) * 4, q = (x0 + xx - px) ** 2 + (y0 + yy - py) ** 2; if (d[i + 3] > 0 && q < best) { best = q; rgb = [d[i], d[i + 1], d[i + 2]]; } }
      return { rgb };
    }, [la, lo, rayon]);
  };
  const cibles = await page.evaluate(() => {
    const sites = rfSitesMesures(), mesure = rfSurfaceMesuree();
    const loin = SUPPORTS_MOBILES.find((s) => mesure(s.lat, s.lon) === undefined && sites.every((x) => dist(s.lat, s.lon, x.lat, x.lon) > 5));
    const piana = sites.find((x) => Math.abs(x.lat - 42.217259) < 1e-4 && Math.abs(x.lon - 8.64197) < 1e-4);
    const c = INTERP_ZONES['Bonifacio']; let cellule = null;
    for (let i = -20; i <= 20 && !cellule; i++) for (let j = -20; j <= 20 && !cellule; j++) {
      const la = c.lat + i * 0.004, lo = c.lon + j * 0.005, v = mesure(la, lo);
      if (v !== undefined && rfEmpiriqueClasse(v) != null && sites.every((x) => dist(la, lo, x.lat, x.lon) > 2.5)) cellule = { la, lo, v, classe: rfEmpiriqueClasse(v) };
    }
    return { loin: loin && { la: loin.lat, lo: loin.lon }, piana: piana && { la: piana.lat, lo: piana.lon, classe: rfEmpiriqueClasse(piana.v) }, cellule, palette: RF_EMPIRIQUE_RGB };
  });
  if (!cibles.loin || !cibles.piana || !cibles.cellule) ok(false, '(e) cibles introuvables : ' + JSON.stringify(cibles));
  else {
    const r1 = await lirePixel(cibles.loin.la, cibles.loin.lo, 9, 2);
    ok(!r1.erreur && r1.rgb == null, `support loin de toute mesure (${cibles.loin.la.toFixed(4)}, ${cibles.loin.lo.toFixed(4)}) : rien d'estimé au zoom 9 (${r1.erreur || (r1.rgb ? 'pixel ' + r1.rgb.join(',') : 'aucun pixel')})`);
    const r2 = await lirePixel(cibles.piana.la, cibles.piana.lo, 9, 1), c2 = cibles.palette[cibles.piana.classe];
    ok(!r2.erreur && r2.rgb && r2.rgb.join(',') === c2.join(','), `lieu mesuré de Piana (10,32 V/m) : point de la classe ${cibles.piana.classe} (${c2.join(',')}) — lu ${r2.erreur || (r2.rgb ? r2.rgb.join(',') : 'aucun pixel')}`);
    const r3 = await lirePixel(cibles.cellule.la, cibles.cellule.lo, 9, 1), c3 = cibles.palette[cibles.cellule.classe];
    ok(!r3.erreur && r3.rgb && r3.rgb.join(',') === c3.join(','), `cellule mesurée (zone Bonifacio, ${cibles.cellule.v} V/m) : pleine, classe ${cibles.cellule.classe} (${c3.join(',')}) — lue ${r3.erreur || (r3.rgb ? r3.rgb.join(',') : 'aucun pixel')}`);
  }

  console.log('(f) masque terre : la surface estimée s\'arrête à la côte');
  const MER = [41.906, 8.741], TERRE = [41.94, 8.701];   // points fixes, cf. l'en-tête (contours communaux bruts)
  const ile = await page.evaluate(([mer, terre]) => ({
    etat: TERRE_CORSE_ETAT, lavezzi: rfATerre(41.3375, 9.256), sanguinaire: rfATerre(41.8772, 8.593),
    mer: rfATerre(mer[0], mer[1]), terre: rfATerre(terre[0], terre[1]),
    dMer: rfChampEmpiriqueEn(mer[0], mer[1]).d_m, dTerre: rfChampEmpiriqueEn(terre[0], terre[1]).d_m, extinction: RF_EMPIRIQUE.d_extinction_m,
    supportsEnMer: SUPPORTS_MOBILES.filter((s) => rfATerre(s.lat, s.lon) === false).length,
    lieuxEnMer: rfSitesMesures().filter((s) => rfATerre(s.lat, s.lon) === false).length, nLieux: rfSitesMesures().length,
    popupMer: rfPopupHTML(mer[0], mer[1]).replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' '),
  }), [MER, TERRE]);
  ok(ile.etat === 'ok', `masque terre chargé (${ile.etat})`);
  ok(ile.lavezzi === true && ile.sanguinaire === true, `les petites îles comptent comme terre : Lavezzi ${ile.lavezzi}, Grande Sanguinaire ${ile.sanguinaire}`);
  ok(ile.supportsEnMer === 0 && ile.lieuxEnMer === 0, `aucun support mobile en mer (${ile.supportsEnMer}), aucun lieu mesuré en mer (${ile.lieuxEnMer} sur ${ile.nLieux})`);
  ok(ile.mer === false && ile.terre === true && ile.dMer < ile.extinction && ile.dTerre < ile.extinction && Math.abs(ile.dMer - ile.dTerre) <= 20,
    `points fixes : en mer à ${Math.round(ile.dMer)} m d'un support, à terre à ${Math.round(ile.dTerre)} m, tous deux en deçà de l'extinction (${Math.round(ile.extinction)} m)`);
  const pMer = await lirePixel(MER[0], MER[1], 15, 3), pTerre = await lirePixel(TERRE[0], TERRE[1], 15, 3);
  ok(!pMer.erreur && pMer.rgb == null, `en mer (golfe d'Ajaccio), zoom 15 : aucune estimation dessinée (${pMer.erreur || (pMer.rgb ? 'pixel ' + pMer.rgb.join(',') : 'aucun pixel')})`);
  ok(!pTerre.erreur && pTerre.rgb != null, `à terre, même distance, zoom 15 : estimation dessinée (${pTerre.erreur || (pTerre.rgb ? 'pixel ' + pTerre.rgb.join(',') : 'aucun pixel')})`);
  ok(/En mer : pas d’estimation/.test(ile.popupMer) && !/Champ estimé ici/.test(ile.popupMer), 'popup en mer : « En mer : pas d’estimation », aucun champ estimé');
  // Contre-épreuve : masque retiré le temps d'une lecture, le même point en mer porte une estimation — ce test mesure
  // bien le masque, pas une tuile vide pour une autre raison. Puis le masque est remis.
  await page.evaluate(() => { window.__terreTest = TERRE_CORSE; TERRE_CORSE = null; TERRE_CORSE_ETAT = 'echec'; rfRedessiner(); });
  const pSans = await lirePixel(MER[0], MER[1], 15, 3);
  await page.evaluate(() => { TERRE_CORSE = window.__terreTest; TERRE_CORSE_ETAT = 'ok'; delete window.__terreTest; rfRedessiner(); });
  ok(!pSans.erreur && pSans.rgb != null, `contre-épreuve : sans masque, le même point en mer porte une estimation (${pSans.erreur || (pSans.rgb ? 'pixel ' + pSans.rgb.join(',') : 'aucun pixel')})`);

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
      const e = rfChampEmpiriqueEn(la, lo), k = e && e.terre === false ? 'en mer' : e && e.classe != null ? 'classe ' + e.classe : 'éteint';
      c[k] = (c[k] || 0) + 1; n++;
    }
    return { n, pas, comptes: c, reference: RF_EMPIRIQUE.reference, bornes: RF_EMPIRIQUE.bornes_vm, d_extinction_m: Math.round(RF_EMPIRIQUE.d_extinction_m) };
  });
  console.log('  ' + JSON.stringify(rep));
  ok(rep.n === 4004, `échantillon de ${rep.n} points (attendu 4 004 avec le fichier du 2026-09-28)`);
  const cas = Object.keys(rep.comptes).sort().join(', ');
  ok(cas === 'classe 0, classe 1, éteint' || cas === 'classe 0, classe 1', `deux classes et l'extinction, rien d'autre (aucun point BT en mer) : ${cas}`);

  console.log('(b, suite) le document rendu en anglais (?lang=en)');
  const url = new URL(page.url()); url.searchParams.set('lang', 'en');
  await page.goto(url.href, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForFunction(() => document.documentElement.lang === 'en' && typeof RF_EMPIRIQUE !== 'undefined' && RF_EMPIRIQUE !== null, undefined, { timeout: 60000, polling: 500 });
  await page.waitForTimeout(1500);
  const domEn = await texteDom();
  const mEn = domEn.texte.match(LIMITE);
  ok(domEn.lang === 'en' && !mEn, `document rendu (${domEn.lang}, ${domEn.texte.length} caractères) : aucune valeur limite 28–61 V/m${mEn ? ' — trouvé « ' + domEn.texte.slice(Math.max(0, mEn.index - 40), mEn.index + 40) + ' »' : ''}`);

  const diag = h.diagnostics();
  const erreursRF = diag.consoleErrors.filter((e) => /RF|tuile|rf[A-Z]/i.test(e));
  ok(erreursRF.length === 0, `aucune erreur console liée à la couche RF (${erreursRF.length})`);
} finally {
  await h.close();
}
console.log(echecs ? `\n${echecs} échec(s)` : '\ntout est vert');
process.exit(echecs ? 1 : 0);
