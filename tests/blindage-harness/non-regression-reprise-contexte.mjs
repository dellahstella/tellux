// ─── Non-régression : reprise des chargeurs de contexte (lot contexte de la reprise, 2026-09-10) ──
// Le lot inscrit quatre chargeurs dans l'assistant de reprise partagé (#1366), en classe `contexte`
// (3 tentatives, sans réveil sur `online`) : sols, sites, mesures certifiées, antennes ANFR — et fait
// redessiner les marqueurs TDF après une reprise. Ce fichier est la RÉFUTATION écrite AVANT le lot, et
// exécutée contre le code d'avant le lot pour vérifier qu'elle attrape les défauts qu'elle prétend
// attraper.
//
// LES DÉFAUTS, lus dans le code d'avant le lot
//   · Sols, sites, mesures certifiées : le chargeur avale son échec dans une IIFE et garde son mémo —
//     une promesse RÉSOLUE. Tout rappel la rend sans refetch : la donnée ne revient plus de la session.
//   · Mesures certifiées : _renderMesuresCertifiees() pose son verrou `_certRendered` même sur un jeu
//     vide. Une couche rendue pendant la panne reste vide quand la donnée arrive.
//   · Antennes : loadAnt() n'a aucune reprise. Le bouton ne la rappelle pas non plus : il ne recharge
//     qu'une couche vide, et loadAnt() y a déjà posé ses deux groupes de grappes.
//   · Marqueurs TDF : dessinés dans loadAnt() seulement, après les antennes. Sautés si Supabase échoue,
//     jamais redessinés quand la reprise 'tdf' ramène les émetteurs, et dessinés une fois de plus à
//     chaque rappel de loadAnt().
// Contre le code d'avant le lot, S0 et, par clé, S2, S3 et S8 (sols, sites, mesures certifiées), C1,
// C2, T2 et T4 DOIVENT échouer.
//
// CE QUI EST SIMULÉ, ET POURQUOI
//   · fetch : les quatre fichiers statiques sont les VRAIS fichiers du dépôt (sols, sites, mesures
//     certifiées, émetteurs TDF) ; Supabase `antennas_corse` rend quatre lignes fictives à trois
//     positions distinctes. setTimeout : temps compressé.
//   · Leaflet (marqueurs, groupes, carte) : des boîtes qui comptent ce qu'on y met. On teste ce qui est
//     dessiné et combien de fois, pas le rendu.
//   · Sans effet sur la reprise, donc remplacés : l'audit des champs de sites_app.json, l'agrégation
//     des fiches résidentielles (identité ici), la dispersion des marqueurs certifiés, les infobulles.
// Le reste est EXTRAIT d'app.html — assistant, chargeurs, rendu des mesures certifiées, loadAnt,
// repriseTDF, déclarations, et les fonctions du lot si elles existent — lu, pas recopié.
//
// MODE AVANT-LOT : si une inscription manque, l'inscription PRÉVUE est utilisée, et l'enrobage prévu
// s'il manque aussi. Le harnais le dit.
//
// Usage : node tests/blindage-harness/non-regression-reprise-contexte.mjs [app.html]   (sort 1 si un ✘, 2 si témoin)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..', '..');
const html = readFileSync(process.argv[2] || join(RACINE, 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
const lire = (f) => readFileSync(join(RACINE, 'public', 'data', f), 'utf8');
const FICHIERS = {
  sols: lire('soilgrids_grid_corse.json'),
  sites: lire('sites_app.json'),
  cert: lire('cartoradio_certified_corse.json'),
  tdf: lire('tdf_emitters_corse.json'),
};

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
const inscriptionDe = (cle) => js.match(new RegExp("enregistrerReprise\\(\\s*'" + cle + "'\\s*,[\\s\\S]*?\\n\\s*\\}\\);", 'g')) || [];

// ─── Témoins sur la donnée : recalculés depuis les fichiers, jamais écrits en dur ─────────────────
const dSites = JSON.parse(FICHIERS.sites).sites || [];
const N = {
  sols: (JSON.parse(FICHIERS.sols).grid || []).length,
  sitesEM: dSites.filter((s) => s.type === 'site_em').length,
  sitesUTh: dSites.filter((s) => s.type === 'site_uth').length,
  cert: (JSON.parse(FICHIERS.cert).mesures || []).length,
  tdf: (JSON.parse(FICHIERS.tdf).emitters || []).length,
};
// Supabase : quatre lignes, trois positions — la deuxième double la première.
const LIGNES_ANFR = [
  { lat: 41.9200, lon: 8.7400, generation: '4G', commune: 'stub', operateur: 'A' },
  { lat: 41.9200, lon: 8.7400, generation: '5G', commune: 'stub', operateur: 'B' },
  { lat: 42.7000, lon: 9.4500, generation: '4G', commune: 'stub', operateur: 'A' },
  { lat: 41.3900, lon: 9.1600, generation: '5G', commune: 'stub', operateur: 'C' },
];
N.antPositions = new Set(LIGNES_ANFR.map((l) => l.lat.toFixed(5) + ',' + l.lon.toFixed(5))).size;
if (Object.values(N).some((n) => !(n > 0))) { console.error('TÉMOIN — un fichier de données est vide : ' + JSON.stringify(N)); process.exit(2); }

// ─── S0 — câblage ────────────────────────────────────────────────────────────────────────────────
console.log('S0 — câblage dans app.html');
const ligneBoot = js.split('\n').find((l) => l.includes('setTimeout(()=>Promise.all([')) || '';
const CHARGEURS = { sols: 'loadSoilGridsGrid', sites: 'loadPointsChaudsRadio', cert: 'loadMesuresCertifiees', ant: 'loadAnt' };
for (const [cle, chargeur] of Object.entries(CHARGEURS)) {
  const ins = inscriptionDe(cle);
  verifier(`inscription '${cle}' présente une seule fois, en classe contexte`, ins.length === 1 && /classe:\s*'contexte'/.test(ins[0]), `${ins.length} trouvée(s)`);
  verifier(`le lot de boot passe par declenche('${cle}', …)`, new RegExp("declenche\\(\\s*'" + cle + "'").test(ligneBoot));
  verifier(`le lot de boot n’appelle PLUS ${chargeur}() en direct`, !new RegExp('\\b' + chargeur + '\\s*\\(').test(ligneBoot));
}
verifier('le lot de boot n’appelle pas loadSitesApp() en direct non plus', !/\bloadSitesApp\s*\(/.test(ligneBoot));
// Fragments simulés par ce harnais : on vérifie qu'ils sont bien ceux d'app.html.
const BOOT_ANT = "declenche('ant','boot').then(function(){if(ACTIVE.ant)lAnt.addTo(map);})";
verifier('boot : la couche antennes rejoint la carte après la première tentative (fragment simulé)', ligneBoot.includes(BOOT_ANT));
const TOG_ANT = "if(id==='ant'&&lAnt.getLayers().length===0)loadAnt();";
verifier("tog('ant') ne rappelle loadAnt() que sur une couche vide — condition simulée", js.includes(TOG_ANT));
const TOG_CERT = /if\(id==='cert'\)\{[\s\S]{0,400}?loadMesuresCertifiees\(\)\.then\(function\(\)\{\s*_renderMesuresCertifiees\(\);/;
verifier("tog('cert') charge puis rend, sans l’assistant — chemin simulé", TOG_CERT.test(js));
verifier('rendu des marqueurs TDF sorti de loadAnt() : dessinerMarqueursTDF() existe', existeFonction('dessinerMarqueursTDF'));
verifier('loadAnt() délègue le rendu TDF, sans boucle propre', existeFonction('loadAnt')
  && extraireFonction('loadAnt').includes('dessinerMarqueursTDF()') && !extraireFonction('loadAnt').includes('TDF_EMITTERS.forEach'));
verifier('repriseTDF() redessine les marqueurs', existeFonction('repriseTDF') && extraireFonction('repriseTDF').includes('dessinerMarqueursTDF()'));
verifier('enrobage repriseMesuresCertifiees() présent', existeFonction('repriseMesuresCertifiees'));

const PREVUES = {
  sols: "enregistrerReprise('sols', loadSoilGridsGrid, {\n    classe: 'contexte',\n    verifie: () => Array.isArray(SOILGRIDS_CORSE) && SOILGRIDS_CORSE.length > 0\n  });",
  sites: "enregistrerReprise('sites', loadPointsChaudsRadio, {\n    classe: 'contexte',\n    verifie: () => SITES_REMARQUABLES.length > 0 && POINTS_CHAUDS_RADIO.length > 0\n  });",
  cert: "enregistrerReprise('cert', repriseMesuresCertifiees, {\n    classe: 'contexte',\n    verifie: () => Array.isArray(MESURES_CERTIFIEES) && MESURES_CERTIFIEES.length > 0\n  });",
  ant: "enregistrerReprise('ant', loadAnt, {\n    classe: 'contexte',\n    verifie: () => ANFR_ONSHORE_COUNT !== null && ANFR_ONSHORE_COUNT > 0\n  });",
};
const ENROBAGE_PREVU = 'async function repriseMesuresCertifiees() {\n  await loadMesuresCertifiees();\n'
  + '  if (!Array.isArray(MESURES_CERTIFIEES) || MESURES_CERTIFIEES.length === 0) return;\n'
  + '  _renderMesuresCertifiees();\n  if (ACTIVE.cert) lCert.addTo(map);\n}';
const inscriptions = {};
const modeAvant = [];
for (const cle of Object.keys(PREVUES)) {
  const ins = inscriptionDe(cle);
  if (ins.length === 1) inscriptions[cle] = ins[0];
  else { inscriptions[cle] = PREVUES[cle]; modeAvant.push(cle); }
}
const insTDF = inscriptionDe('tdf');
if (insTDF.length !== 1) { console.error("TÉMOIN — inscription 'tdf' introuvable : le lot RF est un prérequis."); process.exit(2); }
const enrobageCert = existeFonction('repriseMesuresCertifiees') ? extraireFonction('repriseMesuresCertifiees') : ENROBAGE_PREVU;
if (modeAvant.length || !existeFonction('repriseMesuresCertifiees')) {
  console.log('\n  ⚠ MODE AVANT-LOT : inscription(s) PRÉVUE(S) utilisée(s) pour ' + (modeAvant.join(', ') || '—')
    + (existeFonction('repriseMesuresCertifiees') ? '' : ' ; enrobage prévu repriseMesuresCertifiees()') + '.');
}

// ─── Bac à sable ─────────────────────────────────────────────────────────────────────────────────
const vraiSetTimeout = setTimeout;
const sbSetTimeout = (fn) => vraiSetTimeout(fn, 0);
const plans = { sols: () => 'ok', sites: () => 'ok', cert: () => 'ok', anfr: () => 'ok', tdf: () => 'ok' };
const appels = { sols: 0, sites: 0, cert: 0, anfr: 0, tdf: 0 };
const ROUTES = [['soilgrids_grid_corse', 'sols'], ['sites_app.json', 'sites'], ['cartoradio_certified_corse', 'cert'],
  ['antennas_corse', 'anfr'], ['tdf_emitters_corse', 'tdf']];
const fetchStub = async (url) => {
  const u = String(url);
  const route = ROUTES.find(([motif]) => u.includes(motif));
  if (!route) throw new Error('fetch inattendu : ' + u);
  const cle = route[1];
  const action = plans[cle](++appels[cle]);
  await new Promise((r) => vraiSetTimeout(r, 5));
  if (action === 'reseau') throw new TypeError('Failed to fetch');
  if (action === 'http500') return { ok: false, status: 500, json: async () => ({}) };
  if (cle === 'anfr') {
    if (action === 'vide') return { ok: true, status: 200, json: async () => [] };
    const offset = +((u.match(/offset=(\d+)/) || [0, 0])[1]);
    return { ok: true, status: 200, json: async () => (offset === 0 ? LIGNES_ANFR.map((l) => ({ ...l })) : []) };
  }
  if (action === 'vide') return { ok: true, status: 200, json: async () => ({}) };
  return { ok: true, status: 200, json: async () => JSON.parse(FICHIERS[cle]) };
};
const ctx = {
  window: { addEventListener() {} },
  document: { addEventListener() {}, visibilityState: 'visible', getElementById() { return null; } },
  fetch: fetchStub, setTimeout: sbSetTimeout, clearTimeout, console: { log() {}, warn() {}, error() {} },
  AbortSignal,
};
const declarations = ['SOILGRIDS_CORSE', '_soilGridsPromise', 'POINTS_CHAUDS_RADIO', '_sitesAppPromise', 'SITES_REMARQUABLES',
  'THERMAL_SOURCES_CORSE', 'MESURES_CERTIFIEES', '_certLoadPromise', '_certRendered', 'ANFR_ONSHORE_COUNT', 'ANTENNES_LOCATIONS',
  '_antennasCorseRawRows', '_antennasCorseRawPromise', 'TDF_EMITTERS', '_tdfLoadPromise', 'RF_CALIB_STATS'].map(extraireDeclaration);
const duLot = ['dessinerMarqueursTDF'].filter(existeFonction).map(extraireFonction);
const corps = [
  'const { window, document, fetch, setTimeout, clearTimeout, console, AbortSignal } = ctx;',
  "const SB_URL = 'https://stub.invalid'; function sbH(){ return {}; }",
  ...declarations,
  'const ACTIVE = { ant: true, cert: false };',
  // Leaflet : des boîtes qui comptent.
  'function __groupe(nom){ const g = { nom, _l: [], addLayer(x){ if (!g._l.includes(x)) g._l.push(x); return g; },',
  '  getLayers(){ return g._l.slice(); }, clearLayers(){ g._l = []; return g; }, addTo(m){ m.addLayer(g); return g; } }; return g; }',
  'const map = __groupe("carte"); map.hasLayer = (x) => map._l.includes(x);',
  'const lAnt = __groupe("lAnt"), lAntCluster = __groupe("lAntCluster"), lTDFCluster = __groupe("lTDFCluster"), lCert = __groupe("lCert");',
  'const L = { divIcon(o){ return o; }, marker(ll, o){ return { ll, o, bindTooltip(){ return this; }, bindPopup(){ return this; },',
  '  on(){ return this; }, addTo(g){ g.addLayer(this); return this; } }; } };',
  "const GC = { default: '#000', infra: '#000', infraText: '#000' };",
  'function mkIcon(){ return {}; } function _antTooltipHtml(){ return ""; } function setStatus(){} function syncAntCount(){} function info(){}',
  'function auditChampsSitesApp(){ return []; } function _certAggregateResidentialCoords(m){ return m; }',
  'function _certOffsetPositions(ms){ return ms.map((m) => ({ lat: m.lat, lon: m.lon })); } function _certIconHtml(){ return ""; }',
  'function _certFormatPopup(){ return ""; } function _certOpenCross(){} const _certMarkerById = {};',
  assistant,
  extraireFonction('loadSoilGridsGrid'),
  extraireFonction('loadSitesApp'), extraireFonction('adaptSiteEMFromApp'), extraireFonction('adaptSiteUthFromApp'),
  extraireFonction('loadPointsChaudsRadio'),
  extraireFonction('loadMesuresCertifiees'), extraireFonction('_renderMesuresCertifiees'), enrobageCert,
  extraireFonction('fetchAntennasCorseRaw'), extraireFonction('loadTDFEmitters'), extraireFonction('loadAnt'),
  extraireFonction('repriseTDF'),
  ...duLot,
  'function __inscrire(cle){ switch (cle) {',
  ...Object.entries(inscriptions).map(([cle, ins]) => `    case '${cle}': ${ins} break;`),
  `    case 'tdf': ${insTDF[0]} break;`,
  '  } }',
  'return { declenche, reprisesEtat, _reprises, __inscrire,',
  '  direct(cle){ return ({ sols: loadSoilGridsGrid, sites: loadSitesApp, cert: loadMesuresCertifiees, ant: loadAnt })[cle](); },',
  '  vider(){ SOILGRIDS_CORSE = null; _soilGridsPromise = null; SITES_REMARQUABLES = []; POINTS_CHAUDS_RADIO = [];',
  '    THERMAL_SOURCES_CORSE = []; _sitesAppPromise = null; MESURES_CERTIFIEES = []; _certLoadPromise = null; _certRendered = false;',
  '    ANFR_ONSHORE_COUNT = null; ANTENNES_LOCATIONS = []; _antennasCorseRawRows = null; _antennasCorseRawPromise = null;',
  '    TDF_EMITTERS = []; _tdfLoadPromise = null; RF_CALIB_STATS = null; _reprises.clear();',
  '    [map, lAnt, lAntCluster, lTDFCluster, lCert].forEach((g) => g.clearLayers()); ACTIVE.ant = true; ACTIVE.cert = false; },',
  '  actif(o){ Object.assign(ACTIVE, o); },',
  // Chemins HORS assistant, recopiés d'app.html — S0 vérifie qu'ils n'y ont pas changé.
  '  bootAnt(){ return declenche("ant", "boot").then(function(){ if (ACTIVE.ant) lAnt.addTo(map); }); },',
  '  togAnt(){ if (lAnt.getLayers().length === 0) loadAnt(); },',
  '  togCert(){ map.addLayer(lCert); ACTIVE.cert = true; return loadMesuresCertifiees().then(function(){ _renderMesuresCertifiees(); }); },',
  '  taille(cle){ return ({ sols: SOILGRIDS_CORSE === null ? null : SOILGRIDS_CORSE.length,',
  '    sites: SITES_REMARQUABLES.length + "/" + POINTS_CHAUDS_RADIO.length, cert: MESURES_CERTIFIEES.length,',
  '    ant: lAntCluster.getLayers().length })[cle]; },',
  '  compte(){ return { antennes: lAntCluster.getLayers().length, tdf: lTDFCluster.getLayers().length, cert: lCert.getLayers().length,',
  '    lieux: ANTENNES_LOCATIONS.length, onshore: ANFR_ONSHORE_COUNT, antSurCarte: map.hasLayer(lAnt), certSurCarte: map.hasLayer(lCert) }; } };',
].join('\n');
const api = new Function('ctx', corps)(ctx);

async function attendreTerminal(cles) {
  const t0 = Date.now();
  const fini = () => cles.every((c) => ['ok', 'abandoned'].includes(api.reprisesEtat(c)));
  while (!fini() && Date.now() - t0 < 8000) await new Promise((r) => vraiSetTimeout(r, 5));
  await new Promise((r) => vraiSetTimeout(r, 40));
  return Object.fromEntries(cles.map((c) => [c, api.reprisesEtat(c)]));
}
function remettre(p = {}) {
  api.vider();
  for (const k of Object.keys(appels)) { appels[k] = 0; plans[k] = p[k] || (() => 'ok'); }
}
const ATTENDU = {
  sols: String(N.sols), sites: `${N.sitesEM}/${N.sitesUTh}`, cert: String(N.cert), ant: String(N.antPositions),
};
const RESEAU = { sols: 'sols', sites: 'sites', cert: 'cert', ant: 'anfr' };
const TENTATIVES = 3; // classe contexte — lue dans REPRISE_CLASSES ci-dessous, pas supposée
const classeContexte = new Function(assistant.slice(0, assistant.indexOf('};') + 2) + '\nreturn REPRISE_CLASSES.contexte;')();
if (classeContexte.tentatives !== TENTATIVES) { console.error('TÉMOIN — classe contexte à ' + classeContexte.tentatives + ' tentatives, harnais écrit pour ' + TENTATIVES); process.exit(2); }

// ─── Par clé : S1 nominal · S2 échec puis retour · S3 panne permanente · S4 200 vide · S5 appel direct
//     concurrent · S7 salve · S8 appel direct après un échec ─────────────────────────────────────────
for (const cle of ['sols', 'sites', 'cert', 'ant']) {
  const res = RESEAU[cle];
  const lancer = async (titre, plan) => {
    remettre({ [res]: plan });
    api.__inscrire(cle);
    await api.declenche(cle, 'boot');
    const etat = (await attendreTerminal([cle]))[cle];
    console.log(`\n[${cle}] ${titre}`);
    return { etat, fetchs: appels[res], taille: String(api.taille(cle)) };
  };
  let r = await lancer('S1 — nominal', () => 'ok');
  verifier("état 'ok'", r.etat === 'ok', r.etat);
  verifier('une requête', r.fetchs === 1, `${r.fetchs}`);
  verifier(`jeu complet (${ATTENDU[cle]})`, r.taille === ATTENDU[cle], r.taille);
  if (r.taille !== ATTENDU[cle]) { console.error(`\nTÉMOIN — [${cle}] le nominal ne charge pas le jeu attendu : le reste serait comparé à un faux étalon.`); process.exit(2); }

  r = await lancer('S2 — échec au boot, puis retour', (n) => (n === 1 ? 'reseau' : 'ok'));
  verifier("état 'ok'", r.etat === 'ok', r.etat);
  verifier('deux requêtes — la reprise refait un vrai fetch', r.fetchs === 2, `${r.fetchs}`);
  verifier(`jeu complet au retour (${ATTENDU[cle]})`, r.taille === ATTENDU[cle], r.taille);

  r = await lancer('S3 — panne permanente', () => 'reseau');
  verifier("état 'abandoned' — la série se termine", r.etat === 'abandoned', r.etat);
  verifier(`${TENTATIVES} requêtes réelles — le mémo est relâché à chaque échec`, r.fetchs === TENTATIVES, `${r.fetchs}`);

  r = await lancer('S4 — réponse 200 vide', () => 'vide');
  verifier("jamais 'ok' sur un jeu vide", r.etat !== 'ok', r.etat);
  verifier('une seule requête — pas de rafale', r.fetchs === 1, `${r.fetchs}`);

  remettre(); api.__inscrire(cle);
  await Promise.all([api.declenche(cle, 'boot'), api.direct(cle)]);
  await new Promise((res2) => vraiSetTimeout(res2, 40));
  console.log(`\n[${cle}] S5 — appel direct concurrent d'une reprise`);
  verifier('une seule requête', appels[res] === 1, `${appels[res]}`);

  remettre(); api.__inscrire(cle);
  await Promise.all(Array.from({ length: 50 }, () => api.declenche(cle, 'salve')));
  await new Promise((res2) => vraiSetTimeout(res2, 60));
  console.log(`\n[${cle}] S7 — 50 déclenchements simultanés`);
  verifier('une seule requête', appels[res] === 1, `${appels[res]}`);

  remettre({ [res]: (n) => (n === 1 ? 'reseau' : 'ok') });
  await api.direct(cle);
  await api.direct(cle);
  console.log(`\n[${cle}] S8 — après un échec, un appel direct relance-t-il un vrai fetch ?`);
  verifier('deux requêtes réelles', appels[res] === 2, `${appels[res]}`);
  verifier(`jeu complet après le second appel (${ATTENDU[cle]})`, String(api.taille(cle)) === ATTENDU[cle], String(api.taille(cle)));
}

// ─── C — mesures certifiées : ce qui arrive doit se VOIR ─────────────────────────────────────────
remettre({ cert: (n) => (n === 1 ? 'reseau' : 'ok') });
api.actif({ cert: true });
api.__inscrire('cert');
await api.declenche('cert', 'boot');
await attendreTerminal(['cert']);
let c = api.compte();
console.log('\nC1 — mesures certifiées en échec au boot, couche allumée, puis retour');
verifier(`${N.cert} marqueurs rendus au retour`, c.cert === N.cert, `${c.cert}`);
verifier('la couche est sur la carte', c.certSurCarte === true);

remettre({ cert: (n) => (n <= 2 ? 'reseau' : 'ok') });
api.__inscrire('cert');
await api.declenche('cert', 'boot');                     // échec 1 (reprise)
await api.togCert();                                     // échec 2 : l'utilisateur allume pendant la panne
await attendreTerminal(['cert']);                        // la reprise ramène la donnée
c = api.compte();
console.log('\nC2 — couche allumée PENDANT la panne, puis la reprise ramène la donnée');
verifier(`${N.cert} marqueurs rendus — le rendu à vide n’a rien verrouillé`, c.cert === N.cert, `${c.cert}`);

remettre();
api.__inscrire('cert');
await api.declenche('cert', 'boot');
await api.togCert();
c = api.compte();
console.log('\nC3 — nominal, puis la couche allumée : pas de second rendu');
verifier(`${N.cert} marqueurs, pas le double`, c.cert === N.cert, `${c.cert}`);

// ─── T — antennes et marqueurs TDF, lancés ensemble comme au boot ────────────────────────────────
async function boot(p) {
  remettre(p);
  api.__inscrire('ant'); api.__inscrire('tdf');
  await Promise.all([api.bootAnt(), api.declenche('tdf', 'boot')]);
  await attendreTerminal(['ant', 'tdf']);
  return api.compte();
}
let t = await boot({});
console.log('\nT1 — nominal : antennes et émetteurs TDF');
verifier(`${N.antPositions} marqueurs d’antennes, ${N.antPositions} lieux pour « Mon lieu »`, t.antennes === N.antPositions && t.lieux === N.antPositions, `${t.antennes} / ${t.lieux}`);
verifier(`${N.tdf} marqueurs TDF, pas le double`, t.tdf === N.tdf, `${t.tdf}`);
verifier('la couche antennes est sur la carte', t.antSurCarte === true);

t = await boot({ tdf: (n) => (n === 1 ? 'reseau' : 'ok') });
console.log('\nT2 — émetteurs TDF en échec au boot, puis ramenés par la reprise « tdf »');
verifier(`${N.tdf} marqueurs TDF au retour`, t.tdf === N.tdf, `${t.tdf}`);
verifier(`antennes intactes (${N.antPositions})`, t.antennes === N.antPositions, `${t.antennes}`);

t = await boot({ anfr: (n) => (n === 1 ? 'reseau' : 'ok') });
console.log('\nT3 — Supabase en échec au boot, puis de retour');
verifier(`${N.antPositions} marqueurs d’antennes au retour`, t.antennes === N.antPositions, `${t.antennes}`);
verifier(`compte des antennes posé (${LIGNES_ANFR.length} lignes à terre)`, t.onshore === LIGNES_ANFR.length, `${t.onshore}`);
verifier(`${N.tdf} marqueurs TDF, pas le double`, t.tdf === N.tdf, `${t.tdf}`);
verifier('la couche antennes est sur la carte', t.antSurCarte === true);

t = await boot({ anfr: () => 'vide' });
console.log('\nT4 — Supabase répond 200 avec zéro antenne : loadAnt() est rappelée par la reprise');
verifier("jamais 'ok'", api.reprisesEtat('ant') !== 'ok', api.reprisesEtat('ant'));
verifier(`${N.tdf} marqueurs TDF, pas un lot de plus à chaque rappel`, t.tdf === N.tdf, `${t.tdf}`);
verifier('une seule requête Supabase — le vide est en cache, rien ne part en rafale', appels.anfr === 1, `${appels.anfr}`);

remettre({ anfr: () => 'reseau' });
api.__inscrire('ant');
await api.bootAnt();
api.togAnt();
await attendreTerminal(['ant']);
console.log('\nT5 — le bouton, pendant la panne : il ne rappelle pas loadAnt(), la reprise le fait');
verifier(`${TENTATIVES} requêtes Supabase, toutes de la reprise`, appels.anfr === TENTATIVES, `${appels.anfr}`);

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}${modeAvant.length ? '  (mode avant-lot)' : ''}`);
process.exit(echecs === 0 ? 0 : 1);
