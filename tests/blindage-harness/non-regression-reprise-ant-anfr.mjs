// ─── Non-régression : couplage des reprises 'ant' et 'anfr', états affichés des antennes et des
// contributions (brief 2 « reprise », lot ant/anfr, 2026-09-11) ──────────────────────────────────────
// RÉFUTATION écrite AVANT le lot, et exécutée contre le code d'avant le lot pour vérifier qu'elle attrape
// les défauts qu'elle prétend attraper.
//
// LES DÉFAUTS, lus dans le code d'avant le lot
//   · 'ant' (classe contexte : 3 tentatives, pas de réveil sur `online`) et 'anfr' (critique : 6, réveil
//     sur `online`) lisent les MÊMES lignes Supabase (fetchAntennasCorseRaw). 'ant' abandonne la première.
//     Si Supabase revient ensuite, 'anfr' recalibre et les valeurs RF reviennent, mais les antennes jamais :
//     `abandoned` n'a qu'une sortie, repriseManuelle(), qui n'a aucun appelant.
//   · Sur échec de loadAnt(), l'en-tête et le panneau gardent « chargement… » : rien ne dit que les antennes
//     manquent. Le compte (« N antennes ») n'est pas traduit.
//   · Contributions : contribsDB est vide qu'elle soit chargée vide ou jamais chargée. La bascule
//     « Contributions » dit donc « 0 relevé(s) » pendant le chargement et pendant une panne de Supabase ; le
//     résumé des conditions et l'infobulle du point d'état comptent la liste locale comme un total.
//
// LE CONTRAT CHANGÉ (GO de Soleil, 2026-09-11) — une seconde sortie d'`abandoned`, sans geste utilisateur :
// quand une clé qui partage la source d'une autre vient de réussir, l'autre sort d'`abandoned` pour UNE
// tentative ; un échec l'y ramène directement. Vérifié ici : la sortie (A1), la préemption depuis `error`
// (A2), la borne d'une tentative (A3), l'absence de doublon (A4), et la borne AU PLUS UNE TENTATIVE PAR CLÉ
// ET PAR SOURCE DANS L'ONGLET, tenue par construction quel que soit le chemin qui relance calibrateRF() —
// appel direct ajouté, ou repriseManuelle('anfr'), qui sort une clé de `ok` (A7). La première version du lot
// s'en remettait à un inventaire statique de ces chemins ; la revue du 2026-09-11 en a contourné six formes.
// S0 garde cet inventaire, renforcé, comme signal et non comme borne.
//
// Contre le code d'avant le lot DOIVENT échouer : S0 (fonction, appelant, contrat écrit, clés, état de la
// liste), A1, A2, A3, B1, B2 (panneau), B3 [en], B4, B5 (indisponibilité dite), C1, C2, C6, C7, C8 (puce
// « Contribs »). A4, A5, A6, A7 et L1 sont des gardes, vraies sur main faute de couplage. Le chemin
// d'enregistrement (point d'état après un enregistrement réussi sur une liste jamais chargée, état de la liste
// inchangé par l'écriture) est vérifié dans non-regression-savecontrib-annulation.mjs, scénario G.
//
// CE QUI EST SIMULÉ, ET POURQUOI
//   · fetch : Supabase `antennas_corse` (lignes fictives) ; le VRAI fichier des mesures certifiées et le VRAI
//     fichier des émetteurs TDF du dépôt. sbGet (liste des contributions) : scripté. Latence : minuteurs réels.
//   · Les minuteurs DU CODE (backoff de la reprise, relance de loadDB) : une horloge MANUELLE — rien ne part
//     tant que le scénario ne le décide pas, pour qu'un état `error` reste `error` le temps de l'observer.
//   · RF_field(), la carte RF, Leaflet : des boîtes (mêmes stubs que les harnais 'anfr' et 'contexte').
//   · jt() et JS_STRINGS_EN sont les VRAIS : on lit la phrase affichée, en français et en anglais.
// Le reste est EXTRAIT d'app.html — assistant, chargeurs, calibrateRF, loadAnt, setStatus, statutAntennes,
// loadDB, la branche 'contrib' de tog(), les deux surfaces de compte — lu, pas recopié.
//
// Usage : node tests/blindage-harness/non-regression-reprise-ant-anfr.mjs [app.html]   (sort 1 si un ✘, 2 si témoin)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..', '..');
const html = readFileSync(process.argv[2] || join(RACINE, 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
// Le code sans ses commentaires, pour compter des appels : un commentaire qui nomme une fonction n'en est pas
// un appel. Les commentaires de fin de ligne aussi, sauf après « : » (les URL « https:// » restent).
const code = js.replace(/\/\*[\s\S]*?\*\//g, (s) => s.replace(/[^\n]/g, ' ')).replace(/(^|[^:])\/\/[^\n]*/g, '$1');
const lire = (f) => readFileSync(join(RACINE, 'public', 'data', f), 'utf8');
const FICHIERS = { carto: lire('cartoradio_certified_corse.json'), tdf: lire('tdf_emitters_corse.json') };

let echecs = 0;
const verifier = (libelle, ok, detail = '') => {
  console.log(`  ${ok ? '✔' : '✘'} ${libelle}${detail ? ' — ' + detail : ''}`);
  if (!ok) echecs++;
};
const temoin = (msg) => { console.error('\nTÉMOIN — ' + msg); process.exit(2); };

const existeFonction = (nom, src = js) => new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\(').test(src);
function extraireFonction(nom, src = js) {
  const m = new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\([^)]*\\)\\s*\\{').exec(src);
  if (!m) throw new Error('fonction introuvable dans app.html : ' + nom);
  let d = 1, i = m.index + m[0].length;
  while (i < src.length && d > 0) { const c = src[i]; if (c === '{') d++; else if (c === '}') d--; i++; }
  return src.slice(m.index, i);
}
const existeDeclaration = (nom) => new RegExp('^\\s*(?:let|var)\\s+' + nom + '\\s*=', 'm').test(js);
function extraireDeclaration(nom) {
  const m = new RegExp('^\\s*(?:let|var)\\s+' + nom + '\\s*=[^;]*;', 'm').exec(js);
  if (!m) throw new Error('déclaration introuvable dans app.html : ' + nom);
  return m[0].trim();
}
function extraireBranche(motif) {
  const n = code.split(motif).length - 1;
  if (n !== 1) temoin(`branche « ${motif} » trouvée ${n} fois`);
  const i = code.indexOf(motif);
  let d = 0, j = code.indexOf('{', i);
  for (; j < code.length; j++) { const c = code[j]; if (c === '{') d++; else if (c === '}') { d--; if (d === 0) break; } }
  return code.slice(i, j + 1);
}
const debut = js.indexOf('const REPRISE_CLASSES');
const fin = js.indexOf('// Cached fetch wrapper');
if (debut < 0 || fin < 0 || fin < debut) temoin('bloc assistant introuvable — marqueurs changés ?');
const assistant = js.slice(debut, fin);
const inscriptionDe = (cle) => js.match(new RegExp("enregistrerReprise\\(\\s*'" + cle + "'\\s*,[\\s\\S]*?\\n\\s*\\}\\);", 'g')) || [];
const blocEN = (js.match(/var JS_STRINGS_EN = \{[\s\S]*?\n\};/) || [null])[0];
if (!blocEN) temoin('dictionnaire JS_STRINGS_EN introuvable');
const dictEN = new Function(blocEN + '\nreturn JS_STRINGS_EN;')();

// ─── S0 — câblage, lu dans le code SANS ses commentaires ─────────────────────────────────────────
console.log('S0 — câblage dans app.html');
const codeAssistant = code.slice(code.indexOf('const REPRISE_CLASSES'), code.indexOf('async function fetchEnv'));
verifier('repriseParSource() définie dans l’assistant', existeFonction('repriseParSource', codeAssistant));
// Deux SIGNAUX statiques (revue du 2026-09-11). Chaque identifiant n'apparaît que sous les formes attendues, dans
// le code sans commentaires ET dans le balisage hors scripts (gestionnaires onclick). Chaque occurrence est classée :
// définition, appel, garde typeof, ou référence (passée en valeur : minuteur, écouteur, .bind, ?.()). On exige un
// nombre exact PAR FORME : un compte global se laisse tromper par deux éditions qui s'équilibrent, comme retirer
// une garde typeof et ajouter un écouteur (revue, passe 2). Ce ne sont PAS la borne : elle est tenue par
// construction dans repriseParSource() et vérifiée par son comportement (A7, A7bis).
// Limites de ce signal : la neutralisation des commentaires par expression régulière ignore les chaînes, si bien
// qu'une chaîne contenant « /* » masquerait la suite (aucune dans app.html au 2026-09-11) ; une chaîne qui nomme
// l'identifiant (un message de journal) compterait comme une référence, soit un faux rouge, dans le sens prudent.
const horsScripts = html.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<!--[\s\S]*?-->/g, '');
function formes(nom) {
  const f = { definitions: 0, appels: [], gardes: 0, references: [], balisage: 0 };
  for (const m of code.matchAll(new RegExp('\\b' + nom + '\\b', 'g'))) {
    const avant = code.slice(Math.max(0, m.index - 30), m.index);
    const apres = code.slice(m.index + nom.length, m.index + nom.length + 4);
    if (/function\s+$/.test(avant)) f.definitions++;
    else if (/typeof\s+$/.test(avant)) f.gardes++;
    else if (/^\s*\(/.test(apres)) f.appels.push(m.index);
    else f.references.push(code.slice(Math.max(0, m.index - 40), m.index + nom.length + 8).replace(/\s+/g, ' '));
  }
  f.balisage = [...horsScripts.matchAll(new RegExp('\\b' + nom + '\\b', 'g'))].length;
  return f;
}
const calibSource = existeFonction('calibrateRF', code) ? extraireFonction('calibrateRF', code) : '';
const debutCalib = calibSource ? code.indexOf(calibSource) : -1, finCalib = debutCalib + calibSource.length;
const rps = formes('repriseParSource');
const rpsDansCalib = rps.appels.length === 1 && rps.appels[0] > debutCalib && rps.appels[0] < finCalib
  && /\brepriseParSource\s*\(\s*'ant'/.test(calibSource);
verifier('repriseParSource : une définition, un seul appel (pour \'ant\', dans calibrateRF()), aucune référence, rien dans le balisage',
  rps.definitions === 1 && rpsDansCalib && rps.references.length === 0 && rps.balisage === 0,
  `${rps.definitions} définition(s), ${rps.appels.length} appel(s) (dans calibrateRF : ${rpsDansCalib}), ${rps.references.length} référence(s), ${rps.balisage} dans le balisage`);
const cal = formes('calibrateRF');
const seuleRefInscription = cal.references.length === 1 && /enregistrerReprise\(\s*'anfr'\s*,\s*calibrateRF/.test(cal.references[0]);
verifier('calibrateRF : une définition, aucun appel, une seule référence (l’inscription \'anfr\'), rien dans le balisage — la calibration ne passe que par la clé',
  cal.definitions === 1 && cal.appels.length === 0 && seuleRefInscription && cal.balisage === 0,
  `${cal.definitions} définition(s), ${cal.appels.length} appel(s), ${cal.references.length} référence(s) ${JSON.stringify(cal.references)}, ${cal.balisage} dans le balisage`);
verifier('repriseManuelle() est toujours là — la sortie par geste utilisateur n’est pas retirée', existeFonction('repriseManuelle', codeAssistant));
verifier('le contrat écrit au site ne dit plus « action utilisateur explicite seulement »',
  !/Sortie de `abandoned` : action utilisateur explicite seulement/.test(js));
const CLES = ['ant_compte_suffixe', 'ant_statut_indisponibles', 'contrib_toast_chargement', 'contrib_toast_non_chargees'];
const manquantes = CLES.filter((k) => !Object.prototype.hasOwnProperty.call(dictEN, k));
verifier('traductions anglaises présentes', manquantes.length === 0, manquantes.join(', '));
verifier('état de la liste des contributions déclaré (_contribsListe)', existeDeclaration('_contribsListe'));

// ─── Bac à sable ─────────────────────────────────────────────────────────────────────────────────
const vraiSetTimeout = setTimeout;
const attendre = (ms) => new Promise((r) => vraiSetTimeout(r, ms));
// Horloge manuelle pour les minuteurs du code.
const minuteurs = new Map();
let idMinuteur = 0;
const sbSetTimeout = (fn) => { const id = ++idMinuteur; minuteurs.set(id, fn); return id; };
const sbClearTimeout = (id) => { minuteurs.delete(id); };
const sonner = (id) => { const f = minuteurs.get(id); minuteurs.delete(id); if (f) f(); };

const plans = { anfr: () => 'ok', carto: () => 'ok', tdf: () => 'ok', db: () => 'ok' };
const appels = { anfr: 0, carto: 0, tdf: 0, db: 0 };
// Quatre lignes, trois positions. À terre : une commune. En mer : même position, sans commune — la grille
// RF les indexe (lat/lon), loadAnt() les écarte (nOnshore = 0).
const LIGNES_TERRE = [
  { lat: 41.9200, lon: 8.7400, generation: '4G', commune: 'stub', operateur: 'A' },
  { lat: 41.9200, lon: 8.7400, generation: '5G', commune: 'stub', operateur: 'B' },
  { lat: 42.7000, lon: 9.4500, generation: '4G', commune: 'stub', operateur: 'A' },
  { lat: 41.3900, lon: 9.1600, generation: '5G', commune: 'stub', operateur: 'C' },
];
const LIGNES_MER = LIGNES_TERRE.map((l) => ({ ...l, commune: null }));
let lignes = LIGNES_TERRE;
let lignesDB = [];
const fetchStub = async (url) => {
  const u = String(url);
  const cle = u.includes('antennas_corse') ? 'anfr' : u.includes('cartoradio_certified_corse') ? 'carto'
    : u.includes('tdf_emitters_corse') ? 'tdf' : null;
  if (!cle) throw new Error('fetch inattendu : ' + u);
  const action = plans[cle](++appels[cle]);
  await attendre(5);
  if (action === 'reseau') throw new TypeError('Failed to fetch');
  if (cle === 'anfr') {
    if (action === 'vide') return { ok: true, status: 200, json: async () => [] };
    const offset = +((u.match(/offset=(\d+)/) || [0, 0])[1]);
    return { ok: true, status: 200, json: async () => (offset === 0 ? lignes.map((l) => ({ ...l })) : []) };
  }
  return { ok: true, status: 200, json: async () => JSON.parse(FICHIERS[cle]) };
};
const sbGetStub = async () => {
  const action = plans.db(++appels.db);
  await attendre(5);
  if (action === 'reseau') throw new TypeError('Failed to fetch');
  return lignesDB.map((l) => ({ ...l }));
};
const journalConsole = [];
const noter = (...a) => { journalConsole.push(a.map(String).join(' ')); };
const ctx = {
  window: { addEventListener() {} },
  document: { addEventListener() {}, visibilityState: 'visible', documentElement: { lang: 'fr' } },
  fetch: fetchStub, sbGet: sbGetStub, setTimeout: sbSetTimeout, clearTimeout: sbClearTimeout,
  console: { log: noter, warn: noter, error: noter }, AbortSignal,
};
const declarations = ['ANFR_GRID', '_anfrLoadPromise', 'RF_CALIB_K', 'RF_CALIB_STATS', '_antennasCorseRawRows',
  '_antennasCorseRawPromise', 'ANFR_ONSHORE_COUNT', 'ANTENNES_LOCATIONS', 'TDF_EMITTERS', '_tdfLoadPromise',
  '_persistentStatus', 'contribsDB', ...['_statutAntennes', '_contribsListe'].filter(existeDeclaration)].map(extraireDeclaration);
// repriseParSource(), si elle existe, vit dans le bloc de l'assistant : elle vient avec lui.
const fonctions = ['fetchAntennasCorseRaw', 'loadANFRForField', 'calibrateRF', 'anfrGrillePrete', 'rfCalibre', 'loadTDFEmitters',
  'dessinerMarqueursTDF', 'loadAnt', 'setStatus', 'statutAntennes', 'loadDB', 'updateContribSummary', 'updateSupabaseStatusDot', 'syncBadges', 'jt']
  .map((n) => extraireFonction(n));
const brancheContrib = extraireBranche("if(id==='contrib'){");
const insAnt = inscriptionDe('ant'), insAnfr = inscriptionDe('anfr');
if (insAnt.length !== 1 || insAnfr.length !== 1) temoin(`inscriptions 'ant' (${insAnt.length}) et 'anfr' (${insAnfr.length}) attendues une fois chacune`);
const BOOT_ANT = "declenche('ant','boot').then(function(){if(ACTIVE.ant)lAnt.addTo(map);})";
const ligneBoot = js.split('\n').find((l) => l.includes('setTimeout(()=>Promise.all([')) || '';
if (!ligneBoot.includes(BOOT_ANT) || !/declenche\(\s*'anfr'\s*,\s*'boot'\s*\)/.test(ligneBoot)) temoin('ligne de démarrage changée : le boot simulé ne serait plus le vrai');
const OSM = '⚠ Secours OSM (Supabase indisponible) : 12 lignes — couverture communautaire partielle';

const corps = [
  'const { window, document, fetch, sbGet, setTimeout, clearTimeout, console, AbortSignal } = ctx;',
  "const SB_URL = 'https://stub.invalid'; function sbH(){ return {}; }",
  ...declarations,
  blocEN,
  'const ACTIVE = { ant: true, hotrf: true, contrib: false };',
  'const __el = {};',
  'function __reinit(){',
  '  __el["hdr-status"] = { textContent: "chargement…" };',
  '  __el["anfr-count"] = { textContent: "chargement…" };',
  '  __el["cond-summary-contribs"] = { textContent: "—" };',
  '  __el["contrib-panel"] = { style: { display: "none" } };',
  '  __el["sb-status-dot"] = { title: "Supabase connexion en cours…", _c: new Set(["status-dot--pending"]),',
  '    classList: { remove(...c){ c.forEach((x) => __el["sb-status-dot"]._c.delete(x)); }, add(c){ __el["sb-status-dot"]._c.add(c); } } };',
  // La puce « Contribs » du panneau Conditions, et la liste dont syncBadges() compte les lignes rendues.
  '  __el["badge-contribs-val"] = { textContent: "—" }; __el["contrib-list"] = { children: { length: 0 } };',
  '}',
  '__reinit();',
  // db-total : ABSENT, comme dans la page (aucun élément, aucun gabarit ne porte cet id).
  'document.getElementById = (id) => __el[id] || null;',
  'let __infos = [];',
  'function info(h, type){ __infos.push({ h: String(h), type }); }',
  // Leaflet : des boîtes qui comptent.
  'function __groupe(nom){ const g = { nom, _l: [], addLayer(x){ if (!g._l.includes(x)) g._l.push(x); return g; },',
  '  getLayers(){ return g._l.slice(); }, clearLayers(){ g._l = []; return g; }, addTo(m){ m.addLayer(g); return g; } }; return g; }',
  'const map = __groupe("carte"); map.hasLayer = (x) => map._l.includes(x);',
  'const lAnt = __groupe("lAnt"), lAntCluster = __groupe("lAntCluster"), lTDFCluster = __groupe("lTDFCluster"), lCon = __groupe("lCon");',
  'const L = { divIcon(o){ return o; }, marker(ll, o){ return { ll, o, bindTooltip(){ return this; }, bindPopup(){ return this; },',
  '  on(){ return this; }, addTo(g){ g.addLayer(this); return this; } }; } };',
  "const GC = { default: '#000', infra: '#000', infraText: '#000' };",
  'function mkIcon(){ return {}; } function _antTooltipHtml(){ return ""; } function syncAntCount(){}',
  'function addMarker(){} function renderList(){}',
  // RF : mêmes stubs que le harnais 'anfr'.
  'function __grille(){ return ANFR_GRID !== null && typeof ANFR_GRID === "object" && Object.keys(ANFR_GRID).length > 0; }',
  'function RF_field(lat, lon){ const e = (__grille() ? 2.0 : 0.09) * RF_CALIB_K; return { E_total_V_m: e, S_total_uW_m2: e * e / 377 * 1e6 }; }',
  'let __hotrf = [];',
  'const lHotRF = { clearLayers(){ __hotrf = []; }, getLayers(){ return __hotrf; } };',
  'function buildHotRF(){ __hotrf = [1]; }',
  assistant,
  ...fonctions,
  'function __inscrire(cle){ switch (cle) {',
  `    case 'ant': ${insAnt[0]} break;`,
  `    case 'anfr': ${insAnfr[0]} break;`,
  '  } }',
  'return { declenche, reprisesEtat, _reprises, __inscrire, loadDB, calibrateRF, repriseManuelle,',
  '  listeRendue(n){ __el["contrib-list"].children.length = n; }, etatListe(e){ _contribsListe = e; },',
  '  puce(){ syncBadges(); return __el["badge-contribs-val"].textContent; },',
  '  vider(){ ANFR_GRID = null; _anfrLoadPromise = null; RF_CALIB_K = 1; RF_CALIB_STATS = null;',
  '    _antennasCorseRawRows = null; _antennasCorseRawPromise = null; ANFR_ONSHORE_COUNT = null; ANTENNES_LOCATIONS = [];',
  '    TDF_EMITTERS = []; _tdfLoadPromise = null; _persistentStatus = ""; contribsDB = []; __infos = []; __hotrf = [];',
  '    if (typeof _statutAntennes !== "undefined") _statutAntennes = null;',
  '    if (typeof _contribsListe !== "undefined") _contribsListe = "attente";',
  '    _reprises.clear(); if (typeof _reprisesParSource !== "undefined") _reprisesParSource.clear(); __reinit(); [map, lAnt, lAntCluster, lTDFCluster].forEach((g) => g.clearLayers());',
  '    ACTIVE.ant = true; ACTIVE.hotrf = true; document.documentElement.lang = "fr"; },',
  '  langue(l){ document.documentElement.lang = l; },',
  '  osm(t){ setStatus(t, true); },',
  // Chemin HORS assistant, recopié : la ligne de démarrage (vérifiée ci-dessus, témoin).
  '  bootAnt(){ return declenche("ant", "boot").then(function(){ if (ACTIVE.ant) lAnt.addTo(map); }); },',
  // La VRAIE branche 'contrib' de tog(), extraite telle quelle.
  '  togContrib(){ const id = "contrib";',
  brancheContrib,
  '  },',
  '  resume(){ updateContribSummary(); },',
  '  point(n){ updateSupabaseStatusDot("ok", n); },',
  '  ajouterLocal(l){ contribsDB.unshift(l); },',
  '  dernierMessage(){ return __infos.length ? __infos[__infos.length - 1].h : null; },',
  '  r(cle){ const x = _reprises.get(cle); return x ? { etat: x.etat, tentatives: x.tentatives, minuteur: x.minuteur, enVol: x.enVol } : null; },',
  '  compte(){ return { antennes: lAntCluster.getLayers().length, tdf: lTDFCluster.getLayers().length, onshore: ANFR_ONSHORE_COUNT,',
  '    hdr: __el["hdr-status"].textContent, anfr: __el["anfr-count"].textContent, resume: __el["cond-summary-contribs"].textContent,',
  '    point: __el["sb-status-dot"].title }; } };',
].join('\n');
const api = new Function('ctx', corps)(ctx);

const calme = () => attendre(80);
const nb = (motif) => journalConsole.filter((l) => l.includes(motif)).length;
function remettre(p = {}) {
  api.vider();
  minuteurs.clear();
  journalConsole.length = 0;
  lignes = LIGNES_TERRE; lignesDB = [];
  for (const k of Object.keys(appels)) { appels[k] = 0; plans[k] = p[k] || (() => 'ok'); }
}
// Fait sonner, un à un, les minuteurs de reprise d'une clé jusqu'à son état terminal.
async function epuiser(cle) {
  for (let i = 0; i < 20; i++) {
    await calme();
    const x = api.r(cle);
    if (!x || ['ok', 'abandoned'].includes(x.etat)) return x && x.etat;
    if (x.minuteur !== null) sonner(x.minuteur);
  }
  return api.r(cle).etat;
}
// Préalable des scénarios A : 'ant' abandonnée après trois échecs de Supabase, 'anfr' pas encore partie.
async function antAbandonnee(p = {}) {
  remettre({ anfr: () => 'reseau', ...p });
  api.__inscrire('ant'); api.__inscrire('anfr');
  api.declenche('ant', 'boot');
  const e = await epuiser('ant');
  const echecs = nb('loadAnt erreur');
  if (e !== 'abandoned' || echecs !== 3) temoin(`préalable faux : 'ant' ${e} après ${echecs} échec(s), attendu abandoned après 3`);
  return { anfr: appels.anfr, tdf: appels.tdf, echecs, texte: api.compte() };
}
const N = { pos: new Set(LIGNES_TERRE.map((l) => l.lat.toFixed(5) + ',' + l.lon.toFixed(5))).size,
  tdf: (JSON.parse(FICHIERS.tdf).emitters || []).length };
const COMPTE = { fr: `${LIGNES_TERRE.length} antennes`, en: `${LIGNES_TERRE.length} antennas` };
const INDISPO = { fr: 'antennes indisponibles', en: 'antennas unavailable' };

// ─── Témoin — démarrage nominal, les deux clés en parallèle comme au boot ────────────────────────
remettre();
api.__inscrire('ant'); api.__inscrire('anfr');
await Promise.all([api.bootAnt(), api.declenche('anfr', 'boot')]);
await calme(); await calme();
let c = api.compte();
if (api.reprisesEtat('ant') !== 'ok' || api.reprisesEtat('anfr') !== 'ok' || c.antennes !== N.pos || c.tdf !== N.tdf) {
  temoin(`le nominal ne charge pas : ant ${api.reprisesEtat('ant')}, anfr ${api.reprisesEtat('anfr')}, ${c.antennes} marqueurs, ${c.tdf} TDF`);
}

// ─── A — le couplage ─────────────────────────────────────────────────────────────────────────────
let avant = await antAbandonnee();
console.log('\nA1 — \'ant\' abandonnée ; Supabase revient et \'anfr\' réussit');
verifier('pendant l’abandon, l’indisponibilité est dite (en-tête et panneau)', avant.texte.hdr === INDISPO.fr && avant.texte.anfr === INDISPO.fr, `${avant.texte.hdr} / ${avant.texte.anfr}`);
plans.anfr = () => 'ok';
await api.declenche('anfr', 'boot');
await calme(); await calme();
c = api.compte();
verifier("'anfr' en 'ok'", api.reprisesEtat('anfr') === 'ok', api.reprisesEtat('anfr'));
verifier("'ant' sort d'`abandoned` sans geste utilisateur, et réussit", api.reprisesEtat('ant') === 'ok', api.reprisesEtat('ant'));
verifier(`${N.pos} marqueurs d’antennes, compte posé (${LIGNES_TERRE.length})`, c.antennes === N.pos && c.onshore === LIGNES_TERRE.length, `${c.antennes} / ${c.onshore}`);
verifier('une seule requête Supabase après l’abandon, celle de \'anfr\' — la tentative de \'ant\' lit le cache', appels.anfr - avant.anfr === 1, `${appels.anfr - avant.anfr}`);
verifier('au plus une requête vers le fichier des émetteurs TDF', appels.tdf - avant.tdf <= 1, `${appels.tdf - avant.tdf}`);
verifier(`B4 — le compte remplace l’indisponibilité (« ${COMPTE.fr} »), en-tête et panneau`, c.hdr === COMPTE.fr && c.anfr === COMPTE.fr, `${c.hdr} / ${c.anfr}`);

remettre({ anfr: (n) => (n === 1 ? 'reseau' : 'ok') });
api.__inscrire('ant'); api.__inscrire('anfr');
await api.declenche('ant', 'boot');
await calme();
const r2 = api.r('ant');
if (r2.etat !== 'error' || r2.minuteur === null) temoin(`préalable A2 faux : 'ant' ${r2.etat}, minuteur ${r2.minuteur}`);
const idMinuteurAnt = r2.minuteur;
await api.declenche('anfr', 'boot');
await calme(); await calme();
console.log('\nA2 — \'ant\' en `error`, minuteur en attente ; \'anfr\' réussit');
verifier("'ant' réussit sans attendre son minuteur", api.reprisesEtat('ant') === 'ok', api.reprisesEtat('ant'));
verifier('son minuteur est annulé — il ne partira pas', !minuteurs.has(idMinuteurAnt));
const passagesA2 = nb('Total lignes DB');
[...minuteurs.keys()].forEach(sonner);
await calme();
verifier('aucune tentative de plus ensuite', nb('Total lignes DB') === passagesA2, `${passagesA2} → ${nb('Total lignes DB')}`);

avant = await antAbandonnee();
lignes = LIGNES_MER; plans.anfr = () => 'ok';
await api.declenche('anfr', 'boot');
await calme(); await calme();
const r3 = api.r('ant');
console.log('\nA3 — la tentative de sortie échoue (lignes sans antenne à terre)');
verifier("'anfr' en 'ok' — la grille RF indexe les positions, pas les communes", api.reprisesEtat('anfr') === 'ok', api.reprisesEtat('anfr'));
verifier("une tentative de 'ant', et une seule", nb('loadAnt erreur') === avant.echecs + 1, `${avant.echecs} → ${nb('loadAnt erreur')}`);
verifier("'ant' revient directement en `abandoned`", r3.etat === 'abandoned', r3.etat);
verifier('sans minuteur ni nouvelle série', r3.minuteur === null && minuteurs.size === 0, `minuteur ${r3.minuteur}, ${minuteurs.size} en attente`);
verifier('aucune requête Supabase de plus que celle de \'anfr\'', appels.anfr - avant.anfr === 1, `${appels.anfr - avant.anfr}`);

remettre();
api.__inscrire('ant'); api.__inscrire('anfr');
await Promise.all([api.bootAnt(), api.declenche('anfr', 'boot')]);
await calme(); await calme();
c = api.compte();
console.log('\nA4 — démarrage nominal : le réveil ne double rien');
verifier(`${N.pos} marqueurs d’antennes, pas le double`, c.antennes === N.pos, `${c.antennes}`);
verifier(`${N.tdf} marqueurs TDF, pas le double`, c.tdf === N.tdf, `${c.tdf}`);
verifier('un seul passage de loadAnt()', nb('Total lignes DB') === 1, `${nb('Total lignes DB')}`);
verifier('une requête Supabase, partagée', appels.anfr === 1, `${appels.anfr}`);

const cartoAvant = appels.carto;
const relance = await api.declenche('anfr', 'relance');
console.log('\nA5 — \'anfr\' en `ok` ne repart plus (ce qui borne le déclencheur à une fois par onglet)');
verifier('declenche() refuse, calibrateRF() ne s’exécute pas', relance === false && appels.carto === cartoAvant, `${relance}, ${appels.carto - cartoAvant} lecture(s)`);

avant = await antAbandonnee();
await api.declenche('anfr', 'boot');
await calme();
console.log('\nA6 — \'anfr\' échoue aussi : rien ne sort \'ant\' d’`abandoned`');
verifier("'ant' reste en `abandoned`, aucune tentative", api.reprisesEtat('ant') === 'abandoned' && nb('loadAnt erreur') === avant.echecs, `${api.reprisesEtat('ant')}, ${nb('loadAnt erreur')}`);

// A7 — la borne tient par construction : calibrateRF() relancée hors de la clé (un appel direct ajouté, puis
// repriseManuelle('anfr'), qui sort 'anfr' de `ok`) ne vaut pas une seconde tentative pour 'ant'.
avant = await antAbandonnee();
lignes = LIGNES_MER; plans.anfr = () => 'ok';
await api.declenche('anfr', 'boot');
await calme(); await calme();
const apresReveil = nb('loadAnt erreur');
await api.calibrateRF();
await calme(); await calme();
const apresAppelDirect = nb('loadAnt erreur');
api.repriseManuelle('anfr');
await calme(); await calme();
const apresManuelle = nb('loadAnt erreur');
console.log('\nA7 — calibrateRF() relancée hors de la clé, après un réveil qui a échoué');
verifier("aucune tentative de plus pour 'ant' : au plus une par clé et par source dans l’onglet",
  apresAppelDirect === apresReveil && apresManuelle === apresReveil && api.reprisesEtat('ant') === 'abandoned',
  `${avant.echecs} → réveil ${apresReveil} → appel direct ${apresAppelDirect} → repriseManuelle ${apresManuelle}, ${api.reprisesEtat('ant')}`);

// A7bis — « une fois par onglet », et non « une fois par abandon » (revue, passe 2). Suite d'A7 : 'ant' est remise
// à zéro par repriseManuelle('ant') (un geste utilisateur), abandonne de nouveau, puis calibrateRF() est relancée.
// Une garde par compteur de tentatives accorderait là une seconde tentative par la source ; la garde par clé et
// par source, non.
await api.repriseManuelle('ant');
await calme();
await epuiser('ant');
const avant7bis = nb('loadAnt erreur');
await api.calibrateRF();
await calme(); await calme();
console.log('\nA7bis — \'ant\' remise à zéro par un geste, abandonnée de nouveau, puis calibrateRF() relancée');
verifier('toujours aucune tentative par la source : la borne vaut pour l’onglet, pas pour un abandon',
  api.reprisesEtat('ant') === 'abandoned' && nb('loadAnt erreur') === avant7bis, `${avant7bis} → ${nb('loadAnt erreur')}, ${api.reprisesEtat('ant')}`);

avant = await antAbandonnee({ carto: () => 'reseau' });
plans.anfr = () => 'ok';
await api.declenche('anfr', 'boot');
await calme();
console.log('\nL1 — LIMITE DÉCLARÉE : grille revenue, mesures certifiées en échec');
verifier("'ant' n’est pas réveillée : le déclencheur est le SUCCÈS de la calibration, pas le retour de la grille", api.reprisesEtat('ant') === 'abandoned' && api.reprisesEtat('anfr') !== 'ok',
  `ant ${api.reprisesEtat('ant')}, anfr ${api.reprisesEtat('anfr')}`);

// ─── B — les textes d'état des antennes ──────────────────────────────────────────────────────────
for (const langue of ['fr', 'en']) {
  remettre({ anfr: () => 'reseau' }); api.langue(langue);
  api.__inscrire('ant');
  await api.declenche('ant', 'boot');
  await calme();
  c = api.compte();
  console.log(`\nB1 [${langue}] — échec de loadAnt(), case de l’en-tête libre`);
  verifier(`en-tête : « ${INDISPO[langue]} »`, c.hdr === INDISPO[langue], c.hdr);
  verifier(`panneau : « ${INDISPO[langue]} »`, c.anfr === INDISPO[langue], c.anfr);
}
remettre({ anfr: () => 'reseau' });
api.__inscrire('ant');
api.osm(OSM);
await api.declenche('ant', 'boot');
await calme();
c = api.compte();
console.log('\nB2 — échec de loadAnt() après l’avertissement persistant du secours OSM');
verifier('en-tête : l’avertissement OSM reste', c.hdr === OSM, c.hdr);
verifier(`panneau : « ${INDISPO.fr} »`, c.anfr === INDISPO.fr, c.anfr);
for (const langue of ['fr', 'en']) {
  remettre(); api.langue(langue);
  api.__inscrire('ant');
  await api.bootAnt();
  await calme();
  c = api.compte();
  console.log(`\nB3 [${langue}] — compte des antennes`);
  verifier(`en-tête et panneau : « ${COMPTE[langue]} »`, c.hdr === COMPTE[langue] && c.anfr === COMPTE[langue], `${c.hdr} / ${c.anfr}`);
}
remettre({ anfr: () => 'vide' });
api.__inscrire('ant');
api.declenche('ant', 'boot');
await epuiser('ant');
c = api.compte();
console.log('\nB5 — Supabase répond 200 avec zéro antenne');
verifier('aucun « 0 antennes »', !/\b0 antennes/.test(c.hdr + c.anfr), `${c.hdr} / ${c.anfr}`);
verifier('compte non posé', c.onshore === null, `${c.onshore}`);
verifier('l’indisponibilité est dite, en-tête et panneau', c.hdr === INDISPO.fr && c.anfr === INDISPO.fr, `${c.hdr} / ${c.anfr}`);

// ─── C — les comptes de contributions ne se disent que d'une liste chargée ─────────────────────────
const TOAST = {
  chargement: { fr: 'Contributions smartphone — chargement… · hors du calcul.', en: 'Smartphone contributions — loading… · outside the calculation.' },
  echec: { fr: 'Contributions smartphone — non chargées · hors du calcul.',
    en: 'Smartphone contributions — not loaded · outside the calculation.' },
};
const faux0 = /\b0 relevé|\b0 reading/;
for (const langue of ['fr', 'en']) {
  remettre(); api.langue(langue);
  api.togContrib();
  let m = api.dernierMessage();
  console.log(`\nC1 [${langue}] — bascule « Contributions » avant la fin du premier chargement`);
  verifier('pas de « 0 relevé(s) »', !!m && !faux0.test(m), m);
  verifier('le message dit le chargement', m === TOAST.chargement[langue], m);

  remettre({ db: () => 'reseau' }); api.langue(langue);
  await api.loadDB();
  api.togContrib();
  m = api.dernierMessage();
  c = api.compte();
  console.log(`\nC2 [${langue}] — Supabase en panne au chargement de la liste`);
  verifier('pas de « 0 relevé(s) »', !!m && !faux0.test(m), m);
  verifier('le message dit que la liste n’est pas chargée', m === TOAST.echec[langue], m);
  // Le résumé n'est recalculé que par updateContribSummary() : on l'appelle après une ligne ajoutée localement,
  // comme le fait un enregistrement réussi. Sans cet appel, ce contrôle ne testerait rien (revue du 2026-09-11).
  api.ajouterLocal({ id: 'local' }); api.resume();
  verifier('résumé des conditions, après une ligne ajoutée localement : le tiret reste, pas « 1 contribution »', api.compte().resume === '—', api.compte().resume);
  verifier('point d’état : hors ligne', c.point === 'Supabase hors ligne — données locales uniquement', c.point);
}
remettre();
lignesDB = [{ id: 1 }, { id: 2 }, { id: 3 }];
await api.loadDB();
api.togContrib();
c = api.compte();
console.log('\nC3 — liste chargée, trois contributions');
verifier('« 3 relevé(s) »', api.dernierMessage() === 'Contributions smartphone — 3 relevé(s) · hors du calcul.', api.dernierMessage());
verifier('résumé « 3 contributions », point « Supabase connecté · 3 contributions »', c.resume === '3 contributions' && c.point === 'Supabase connecté · 3 contributions', `${c.resume} / ${c.point}`);
plans.db = () => 'reseau';
await api.loadDB();
api.togContrib();
console.log('\nC5 — un rafraîchissement échoue après un chargement réussi');
verifier('le compte du dernier chargement réussi reste dit', api.dernierMessage() === 'Contributions smartphone — 3 relevé(s) · hors du calcul.', api.dernierMessage());
remettre();
await api.loadDB();
api.togContrib();
c = api.compte();
console.log('\nC4 — liste chargée, vide : le zéro est vrai');
verifier('« 0 relevé(s) »', api.dernierMessage() === 'Contributions smartphone — 0 relevé(s) · hors du calcul.', api.dernierMessage());
verifier('résumé « Aucune contribution »', c.resume === 'Aucune contribution', c.resume);
remettre();
api.point(null);
console.log('\nC6 — point d’état « connecté » sans compte connu');
verifier('« Supabase connecté », sans nombre', api.compte().point === 'Supabase connecté', api.compte().point);
remettre();
api.ajouterLocal({ id: 'local' });
api.resume();
console.log('\nC7 — liste jamais chargée, une ligne ajoutée localement (enregistrement réussi)');
verifier('résumé : le tiret reste, pas « 1 contribution »', api.compte().resume === '—', api.compte().resume);

// ─── C8 — la puce « Contribs » du panneau Conditions (syncBadges, toutes les 30 s) ─────────────────
// Elle compte les lignes rendues dans #contrib-list. Un enregistrement réussi y rend sa ligne même quand la liste
// n'a jamais été chargée : la puce affichait alors « 1 » comme un total (revue du 2026-09-11).
console.log('\nC8 — puce « Contribs » : le nombre de lignes rendues n’est un compte que d’une liste chargée');
for (const [etat, rendues, attendu] of [['attente', 1, '—'], ['echec', 1, '—'], ['ok', 3, '3'], ['ok', 0, '—']]) {
  remettre();
  api.etatListe(etat); api.listeRendue(rendues);
  const p = api.puce();
  verifier(`liste « ${etat} », ${rendues} ligne(s) rendue(s) → « ${attendu} »`, p === attendu, p);
}

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}`);
process.exit(echecs === 0 ? 0 : 1);
