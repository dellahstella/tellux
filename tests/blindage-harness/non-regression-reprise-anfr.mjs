// ─── Non-régression : reprise de la grille ANFR et calibration RF (lot B de la reprise, 2026-09-10) ─
// Le lot inscrit calibrateRF() dans l'assistant de reprise partagé (#1366). Ce fichier est la
// RÉFUTATION écrite AVANT le lot — et exécutée contre le code d'avant le lot, pour vérifier qu'elle
// attrape bien le défaut qu'elle prétend attraper.
//
// LE DÉFAUT — mesuré le 2026-09-10 en navigateur (Chromium, serveur local, ?no-bt=1)
// Sur échec de Supabase, loadANFRForField() pose ANFR_GRID = {} — une valeur VRAIE — et ne relâche
// jamais son mémo : la grille ne revient plus de la session. calibrateRF() dérive alors k sur les
// émetteurs TDF et les faisceaux seuls, et la calibration se déclare faite :
//   · 41,7347 / 8,7926 (près de l'émetteur TDF d'Ajaccio) : k = 22,2 → 96,4 V/m, contre 1,58 ;
//   · 41,3888 / 9,1595 (valeur dominée par ANFR) : 1,33 V/m grille vide, puis 132,8 V/m si la grille
//     revient SANS recalibrer (terme ANFR × k² ≈ 493), 2,16 V/m si elle revient PUIS on recalibre.
// D'où le lot : (1) ne plus empoisonner la grille ; (2) calibrateRF() refuse de dériver k sur une
// grille vide ; (3) la reprise recalibre au retour ; (4) une recalibration sans point exploitable
// n'écrase jamais un k valide ; (5) la carte RF éteinte pendant la panne se reconstruit au rallumage ;
// (6) les libellés publics disent « non calibré » tant que k ne l'est pas (rfCalibre()).
// Contre le code d'avant le lot, S0, S2, S3, S4, S5, S7 et S9 DOIVENT échouer.
//
// CE QUI EST SIMULÉ, ET POURQUOI
//   · RF_field() : champ brut constant, 2,0 V/m grille chargée, 0,09 V/m grille vide, × k — le
//     rapport ≈ 22 reproduit l'ordre de grandeur mesuré. On teste la DÉCISION de calibrer, pas la
//     physique : les valeurs réelles sont mesurées en navigateur (voir la PR).
//   · fetch (Supabase antennas_corse, fichier des mesures certifiées), setTimeout (temps compressé),
//     la carte (buildHotRF, lHotRF, ACTIVE).
//   · Le fichier des mesures certifiées est le VRAI fichier du dépôt : les filtres de calibrateRF()
//     (éligibilité, conformité, extérieur) s'y appliquent réellement.
// Le reste est EXTRAIT d'app.html — assistant, fetchAntennasCorseRaw, loadANFRForField,
// calibrateRF, déclarations, et les fonctions du lot si elles existent — lu, pas recopié.
//
// MODE AVANT-LOT : si l'inscription 'anfr' manque, l'inscription PRÉVUE est utilisée et le harnais
// le dit.
//
// Usage : node tests/blindage-harness/non-regression-reprise-anfr.mjs [app.html]   (sort 1 si un ✘, 2 si témoin)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..', '..');
const html = readFileSync(process.argv[2] || join(RACINE, 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
const texteCarto = readFileSync(join(RACINE, 'public', 'data', 'cartoradio_certified_corse.json'), 'utf8');

let echecs = 0;
const verifier = (libelle, ok, detail = '') => {
  console.log(`  ${ok ? '✔' : '✘'} ${libelle}${detail ? ' — ' + detail : ''}`);
  if (!ok) echecs++;
};

const existeFonction = (nom) => new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\(').test(js);
function extraireFonction(nom) {
  const m = new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\([^)]*\\)\\s*\\{').exec(js);
  if (!m) throw new Error('fonction introuvable dans app.html : ' + nom);
  let d = 1, i = m.index + m[0].length;
  while (i < js.length && d > 0) { const c = js[i]; if (c === '{') d++; else if (c === '}') d--; i++; }
  return js.slice(m.index, i);
}
function extraireDeclaration(nom) {
  const m = new RegExp('^\\s*let\\s+' + nom + '\\s*=[^;]*;', 'm').exec(js);
  if (!m) throw new Error('déclaration introuvable dans app.html : ' + nom);
  return m[0].trim();
}
const debut = js.indexOf('const REPRISE_CLASSES');
const fin = js.indexOf('// Cached fetch wrapper');
if (debut < 0 || fin < 0 || fin < debut) throw new Error('bloc assistant introuvable — marqueurs changés ?');
const assistant = js.slice(debut, fin);

// ─── Témoin sur la donnée : ce que calibrateRF() doit retenir du vrai fichier ─────────────────────
// Recalculé depuis le fichier (pas écrit en dur) : si la donnée change, l'attendu suit.
const mesures = (JSON.parse(texteCarto).mesures || []).filter((m) =>
  m.calib_eligible !== false && m.conforme !== false && m.valeur_max_vm != null && m.lat != null && m.lon != null
  && m.type_environnement === 'exterieur_public');
const N_ATTENDU = mesures.length;
const trie = mesures.map((m) => m.valeur_max_vm / 2.0).sort((a, b) => a - b);
const K_ATTENDU = trie.length % 2 ? trie[(trie.length - 1) / 2] : (trie[trie.length / 2 - 1] + trie[trie.length / 2]) / 2;
if (!(N_ATTENDU > 0)) { console.error('TÉMOIN — aucun point exploitable dans le fichier des mesures certifiées.'); process.exit(2); }

// ─── S0 — câblage ────────────────────────────────────────────────────────────────────────────────
console.log('S0 — câblage dans app.html');
const ligneBoot = js.split('\n').find((l) => l.includes('setTimeout(()=>Promise.all([')) || '';
const inscriptions = js.match(/enregistrerReprise\(\s*'anfr'\s*,[\s\S]*?\n\s*\}\);/g) || [];
verifier("inscription 'anfr' présente une seule fois", inscriptions.length === 1, `${inscriptions.length} trouvée(s)`);
verifier("le lot de boot passe par declenche('anfr', …)", /declenche\(\s*'anfr'/.test(ligneBoot));
verifier('le lot de boot n’appelle PLUS calibrateRF() en direct', !/\bcalibrateRF\s*\(/.test(ligneBoot));
verifier('prédicat de grille anfrGrillePrete() présent', existeFonction('anfrGrillePrete'));
verifier('état de calibration rfCalibre() présent — la source des libellés conditionnels', existeFonction('rfCalibre'));
const CONDITION_TOG_HOTRF = "if(id==='hotrf'&&lHotRF.getLayers().length===0)buildHotRF();";
verifier("tog('hotrf') ne reconstruit qu’une couche vide — condition simulée par rallumerRF()", js.includes(CONDITION_TOG_HOTRF));
// Les surfaces publiques qui disent « calibré » doivent avoir leur variante, et la consulter. Contrôle de
// FORME — le sens (ce que le visiteur lit vraiment) est vérifié en navigateur, voir la PR.
const manquants = [
  ["popup : libellé non calibré", js.includes("jt('detail_rf_label_noncal'")],
  ['popup : traduction anglaise', /detail_rf_label_noncal\s*:/.test(js)],
  ['légende : variante française', js.includes("hotrf_noncal:'<div class=\"leg-block\"><b class=\"leg-title\">Champ électrique RF")],
  ['légende : variante anglaise', js.includes("hotrf_noncal:'<div class=\"leg-block\"><b class=\"leg-title\">RF electric field")],
  ['légende : legendHtmlFor() consulte rfCalibre()', existeFonction('legendHtmlFor') && extraireFonction('legendHtmlFor').includes('rfCalibre')],
  ['sous-titre mobile : variante et traduction', js.includes("hotrf_noncal:'Modèle Tellux NON calibré") && /mleg_sub_hotrf_noncal\s*:/.test(js)
    && existeFonction('updateInlineLegendMobile') && extraireFonction('updateInlineLegendMobile').includes('hotrf_noncal')],
  ['note Expert : computeExpertComposite() choisit la variante', existeFonction('computeExpertComposite') && extraireFonction('computeExpertComposite').includes('EXPERT_EPISTEMIC_NOTE_NONCAL')],
].filter(([, ok]) => !ok).map(([nom]) => nom);
verifier('chaque surface qui dit « calibré » a sa variante « non calibré »', manquants.length === 0, manquants.join(' · '));
// La note Expert non calibrée est construite par replace() sur une phrase ancre : si l'ancre disparaît,
// replace() rend la note d'origine SANS erreur. On l'évalue pour de vrai.
const ligneNote = js.match(/^const EXPERT_EPISTEMIC_NOTE\s*=.*;$/m);
const ligneNoteNC = js.match(/^const EXPERT_EPISTEMIC_NOTE_NONCAL\s*=.*;$/m);
let notesDistinctes = false;
if (ligneNote && ligneNoteNC) {
  try {
    const [n1, n2] = new Function(ligneNote[0] + '\n' + ligneNoteNC[0] + '\nreturn [EXPERT_EPISTEMIC_NOTE, EXPERT_EPISTEMIC_NOTE_NONCAL];')();
    notesDistinctes = n1 !== n2 && !n2.includes('calibration interne sur mesures certifiées');
  } catch (err) { notesDistinctes = false; }
}
verifier('note Expert « non calibré » distincte, sans « calibration interne sur mesures certifiées »', notesDistinctes);
const PREVUE = "enregistrerReprise('anfr', calibrateRF, {\n    classe: 'critique',\n    verifie: () => ANFR_GRID !== null && Object.keys(ANFR_GRID).length > 0 && RF_CALIB_STATS !== null\n  });";
const modeAvant = inscriptions.length !== 1;
const inscription = modeAvant ? PREVUE : inscriptions[0];
if (modeAvant) console.log('\n  ⚠ MODE AVANT-LOT : inscription absente — l’inscription PRÉVUE est utilisée.\n    Attendu dans ce mode : S2, S3, S4, S5, S7 et S9 en échec.');

// ─── Bac à sable ─────────────────────────────────────────────────────────────────────────────────
const vraiSetTimeout = setTimeout;
const sbSetTimeout = (fn) => vraiSetTimeout(fn, 0);
const plans = { anfr: () => 'ok', carto: () => 'ok' };
const appels = { anfr: 0, carto: 0 };
// Trois lignes fictives, dans trois cellules distinctes de la grille 0,05°.
const LIGNES_ANFR = [
  { lat: 41.92, lon: 8.74, generation: '4G', commune: 'stub', operateur: 'stub' },
  { lat: 42.70, lon: 9.45, generation: '5G', commune: 'stub', operateur: 'stub' },
  { lat: 41.39, lon: 9.16, generation: '4G', commune: 'stub', operateur: 'stub' },
];
const fetchStub = async (url) => {
  const u = String(url);
  const cle = u.includes('antennas_corse') ? 'anfr' : u.includes('cartoradio_certified_corse') ? 'carto' : null;
  if (!cle) throw new Error('fetch inattendu : ' + u);
  const n = ++appels[cle];
  const action = plans[cle](n);
  await new Promise((r) => vraiSetTimeout(r, 10));
  if (action === 'reseau') throw new TypeError('Failed to fetch');
  if (action === 'http500') return { ok: false, status: 500, json: async () => ({ message: 'erreur' }) };
  if (cle === 'anfr') {
    if (action === 'vide') return { ok: true, status: 200, json: async () => [] };
    const offset = +((u.match(/offset=(\d+)/) || [0, 0])[1]);
    return { ok: true, status: 200, json: async () => (offset === 0 ? LIGNES_ANFR.map((l) => ({ ...l })) : []) };
  }
  if (action === 'vide200') return { ok: true, status: 200, json: async () => ({}) };
  return { ok: true, status: 200, json: async () => JSON.parse(texteCarto) };
};
const ctx = {
  window: { addEventListener() {} },
  document: { addEventListener() {}, visibilityState: 'visible' },
  fetch: fetchStub, setTimeout: sbSetTimeout, clearTimeout, console: { log() {}, warn() {}, error: console.error },
  AbortSignal,
};
const declarations = ['ANFR_GRID', '_anfrLoadPromise', 'RF_CALIB_K', 'RF_CALIB_STATS', '_antennasCorseRawRows', '_antennasCorseRawPromise'].map(extraireDeclaration);
const duLot = ['anfrGrillePrete', 'rfCalibre'].filter(existeFonction).map(extraireFonction);
const corps = [
  'const { window, document, fetch, setTimeout, clearTimeout, console, AbortSignal } = ctx;',
  "const SB_URL = 'https://stub.invalid'; function sbH(){ return {}; }",
  ...declarations,
  'const ACTIVE = { hotrf: true };',
  'function __grille(){ return ANFR_GRID !== null && typeof ANFR_GRID === "object" && Object.keys(ANFR_GRID).length > 0; }',
  'function RF_field(lat, lon){ const e = (__grille() ? 2.0 : 0.09) * RF_CALIB_K; return { E_total_V_m: e, S_total_uW_m2: e * e / 377 * 1e6 }; }',
  'let __hotrf = [], __cartes = [];',
  'const lHotRF = { clearLayers(){ __hotrf = []; }, getLayers(){ return __hotrf; } };',
  'function buildHotRF(){ __cartes.push({ k: RF_CALIB_K, grille: __grille() }); __hotrf = [1]; }',
  assistant,
  extraireFonction('fetchAntennasCorseRaw'),
  extraireFonction('loadANFRForField'),
  extraireFonction('calibrateRF'),
  ...duLot,
  'function __inscrire(){ ' + inscription + ' }',
  'return { declenche, reprisesEtat, _reprises, __inscrire, calibrateRF,',
  '  vider(){ ANFR_GRID = null; _anfrLoadPromise = null; _antennasCorseRawRows = null; _antennasCorseRawPromise = null;',
  '    RF_CALIB_K = 1; RF_CALIB_STATS = null; _reprises.delete("anfr"); __hotrf = []; __cartes = []; ACTIVE.hotrf = true; },',
  '  etat(){ return { k: RF_CALIB_K, nUsed: RF_CALIB_STATS ? RF_CALIB_STATS.n_used : null,',
  '    grille: ANFR_GRID === null ? null : Object.keys(ANFR_GRID).length, cartes: __cartes.slice(), carteRF: __hotrf.length }; },',
  '  carte(o){ ACTIVE.hotrf = o.hotrf; __hotrf = o.perimee ? [1] : []; },',
  // Rallumage de la carte RF : la condition de tog('hotrf') (branche ON), recopiée — S0 vérifie
  // qu'elle n'a pas changé dans app.html.
  '  rallumerRF(){ ACTIVE.hotrf = true; if (lHotRF.getLayers().length === 0) buildHotRF(); return __cartes.slice(); },',
  '  calibre(){ return typeof rfCalibre === "function" ? rfCalibre() : undefined; } };',
].join('\n');
const api = new Function('ctx', corps)(ctx);

async function attendreTerminal() {
  const t0 = Date.now();
  let etat = api.reprisesEtat('anfr');
  while (!['ok', 'abandoned'].includes(etat) && Date.now() - t0 < 8000) {
    await new Promise((r) => vraiSetTimeout(r, 5));
    etat = api.reprisesEtat('anfr');
  }
  await new Promise((r) => vraiSetTimeout(r, 40));
  return etat;
}
async function scenario(nom, planAnfr, planCarto, avant = () => {}) {
  api.vider();
  appels.anfr = 0; appels.carto = 0; plans.anfr = planAnfr; plans.carto = planCarto;
  avant();
  api.__inscrire();
  await api.declenche('anfr', 'boot');
  const etat = await attendreTerminal();
  console.log(`\n${nom}`);
  return { etat, anfr: appels.anfr, carto: appels.carto, ...api.etat() };
}
const egal = (a, b) => typeof a === 'number' && Math.abs(a - b) <= 1e-12 * Math.max(1, Math.abs(b));

// ─── S1 — nominal ────────────────────────────────────────────────────────────────────────────────
let r = await scenario('S1 — nominal : grille et mesures chargées', () => 'ok', () => 'ok');
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('une requête ANFR, une lecture des mesures', r.anfr === 1 && r.carto === 1, `${r.anfr} / ${r.carto}`);
verifier(`k dérivé sur la grille chargée (${K_ATTENDU})`, egal(r.k, K_ATTENDU), `${r.k}`);
verifier(`${N_ATTENDU} points utilisés — ceux que le fichier impose`, r.nUsed === N_ATTENDU, `${r.nUsed}`);
verifier('une carte RF, construite avec ce k et la grille', r.cartes.length === 1 && r.cartes[0].grille && egal(r.cartes[0].k, K_ATTENDU));
if (!egal(r.k, K_ATTENDU)) { console.error('\nTÉMOIN — le nominal ne donne pas le k attendu : tout le reste serait comparé à un faux étalon.'); process.exit(2); }
const kRef = r.k;

// ─── S2 — LA réfutation centrale : Supabase en échec au boot, puis de retour ─────────────────────
r = await scenario('S2 — grille ANFR en échec au boot, puis de retour', (n) => (n === 1 ? 'reseau' : 'ok'), () => 'ok');
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('deux requêtes ANFR — la grille n’est pas empoisonnée, la reprise la recharge', r.anfr === 2, `${r.anfr}`);
verifier('aucune carte construite avec un k dérivé sur une grille vide', r.cartes.every((c) => c.grille), JSON.stringify(r.cartes));
verifier('k final = k nominal, au bit — recalibré au retour de la grille', egal(r.k, kRef), `${r.k}`);
verifier('mesures lues une seule fois — pas de calibration tentée sur la grille vide', r.carto === 1, `${r.carto}`);

// ─── S3 — panne permanente ───────────────────────────────────────────────────────────────────────
r = await scenario('S3 — grille ANFR en échec permanent', () => 'reseau', () => 'ok');
verifier("état 'abandoned' — la série se termine", r.etat === 'abandoned', r.etat);
verifier('chaque tentative refait une vraie requête — le mémo est relâché', r.anfr === 6, `${r.anfr}`);
verifier('la grille reste absente (null), jamais {} vrai-mais-vide', r.grille === null, `${r.grille}`);
verifier('k reste 1 — non calibré, jamais dérivé sur la grille vide', r.k === 1, `${r.k}`);
verifier('aucune carte RF construite par la calibration', r.cartes.length === 0, `${r.cartes.length}`);

// ─── S4 — limite déclarée et figée : Supabase répond 200 avec zéro ligne ─────────────────────────
// fetchAntennasCorseRaw() met en cache le tableau vide (partagé avec loadAnt) : la reprise ne peut
// pas le refaire. Ce qui compte : k n'est jamais dérivé dessus, et rien ne part en rafale.
r = await scenario('S4 — Supabase répond 200 avec zéro antenne', () => 'vide', () => 'ok');
verifier("jamais 'ok' sur une grille vide", r.etat !== 'ok', r.etat);
verifier('k reste 1 — calibration refusée', r.k === 1, `${r.k}`);
verifier('aucune carte RF construite par la calibration', r.cartes.length === 0, `${r.cartes.length}`);
verifier('une seule requête — pas de rafale', r.anfr === 1, `${r.anfr}`);

// ─── S5 — garde : une recalibration sans point exploitable n'écrase pas un k valide ──────────────
// Le JSON vide reçu en 200 : le cas qui ressemble le plus à un succès.
r = await scenario('S5 — k valide, puis une recalibration reçoit un JSON vide en 200', () => 'ok', (n) => (n === 1 ? 'ok' : 'vide200'));
verifier('première calibration faite', egal(r.k, kRef), `${r.k}`);
await api.calibrateRF();
let e = api.etat();
verifier('k valide conservé — jamais remis à 1 sans point exploitable', egal(e.k, kRef), `${e.k}`);
verifier('statistiques de calibration conservées', e.nUsed === r.nUsed, `${e.nUsed}`);

// ─── S6 — mesures certifiées en échec au boot, grille chargée ────────────────────────────────────
r = await scenario('S6 — mesures certifiées en échec au boot, puis de retour', () => 'ok', (n) => (n === 1 ? 'reseau' : 'ok'));
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('grille chargée une seule fois, mesures relues', r.anfr === 1 && r.carto === 2, `${r.anfr} / ${r.carto}`);
verifier('k nominal au retour', egal(r.k, kRef), `${r.k}`);

// ─── S7 — carte RF éteinte pendant la panne, rallumée après ──────────────────────────────────────
// Une carte construite pendant la panne (non calibrée) ne doit pas réapparaître au rallumage.
r = await scenario('S7 — carte RF éteinte pendant la panne, rallumée après', (n) => (n === 1 ? 'reseau' : 'ok'), () => 'ok',
  () => api.carte({ hotrf: false, perimee: true }));
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('au retour, la couche éteinte est vidée — rien n’est construit tant qu’elle l’est', r.carteRF === 0 && r.cartes.length === 0,
  `couche ${r.carteRF}, constructions ${r.cartes.length}`);
const cartes7 = api.rallumerRF();
verifier('au rallumage, la carte est construite avec le k calibré', cartes7.length === 1 && cartes7[0].grille && egal(cartes7[0].k, kRef),
  JSON.stringify(cartes7));

// ─── S8 — 50 déclenchements simultanés ───────────────────────────────────────────────────────────
api.vider(); appels.anfr = 0; appels.carto = 0; plans.anfr = () => 'ok'; plans.carto = () => 'ok'; api.__inscrire();
await Promise.all(Array.from({ length: 50 }, () => api.declenche('anfr', 'salve')));
await new Promise((res) => vraiSetTimeout(res, 60));
console.log('\nS8 — 50 déclenchements simultanés');
verifier('une seule requête ANFR, une seule lecture des mesures', appels.anfr === 1 && appels.carto === 1, `${appels.anfr} / ${appels.carto}`);

// ─── S9 — l'état que lisent les libellés publics ─────────────────────────────────────────────────
api.vider(); appels.anfr = 0; appels.carto = 0; plans.anfr = (n) => (n === 1 ? 'reseau' : 'ok'); plans.carto = () => 'ok'; api.__inscrire();
const avantBoot = api.calibre();
await api.declenche('anfr', 'boot');
const pendantPanne = api.calibre();
await attendreTerminal();
const apresRetour = api.calibre();
console.log('\nS9 — rfCalibre(), la source des libellés « calibré / non calibré »');
verifier('faux avant la calibration du boot', avantBoot === false, `${avantBoot}`);
verifier('faux pendant la panne — la grille manque, k n’est pas calibré', pendantPanne === false, `${pendantPanne}`);
verifier('vrai après la recalibration', apresRetour === true, `${apresRetour}`);

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}${modeAvant ? '  (mode avant-lot)' : ''}`);
process.exit(echecs === 0 ? 0 : 1);
