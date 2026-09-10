// ─── Non-régression : reprise de indexRadonZonesOfficial (lot radon, 2026-09-10) ────────────
// Le lot adopte indexRadonZonesOfficial() dans l'assistant de reprise partagé (#1366). Ce
// fichier est la RÉFUTATION écrite AVANT le lot : ce qui prouverait qu'il ne marche pas.
//
// CE QUE L'ÉCHEC PRODUIT — et pourquoi ce lot est « critique »
// RADON_L3_INSEE_SET démarre vide et indexRadonZonesOfficial() est son SEUL écrivain ;
// RADON_2A_APPLIES_ALL vaut false. Si le chargement échoue, calcRadonPotential() ne trouve plus
// aucun match officiel et rend la classe LITHOLOGIQUE : une commune classée L3 par l'arrêté du
// 27 juin 2018 retombe en 2 (schistes, ophiolite…) ou 1 (calcaire, alluvions), et le résultat
// garde confidence:'high'. Une classification réglementaire fausse, affichée avec une confiance
// haute, sans aucun signal.
//
// LE CODE SOUS TEST EST EXTRAIT DU app.html LIVRÉ, pas réécrit : l'assistant de reprise,
// indexRadonZonesOfficial, radonIndexComplet, normCommuneName — et l'APPEL d'enregistrement
// lui-même, évalué tel qu'il est écrit. Seuls fetch, setTimeout et le DOM sont simulés. Le
// GeoJSON servi est le VRAI fichier du dépôt.
// Temps compressé : setTimeout enregistre le délai demandé et déclenche aussitôt — on mesure les
// DÉCISIONS du code (délais, tentatives, état final), pas l'horloge.
//
// ISOLATION DES SCÉNARIOS — leçon du 2026-09-09 : la chaîne de reprise d'un test précédent avait
// fui ses délais dans le suivant et produit une courbe polluée. Chaque scénario attend donc un
// état TERMINAL, se vide, et repart d'une inscription neuve.
//
// CE QUE CE FICHIER NE PROUVE PAS : que les écouteurs `online` / `visibilitychange` relancent la
// ressource dans un vrai navigateur. Cela exige un DOM — et c'est l'amendement 6 de la conception
// qui a montré qu'un mécanisme de re-déclenchement pouvait être INERTE malgré des tests en temps
// compressé verts. Vérifié à part, dans un navigateur réel.
//
// Usage : node tests/blindage-harness/non-regression-reprise-radon.mjs   (sort 1 si un ✘)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..', '..');
const html = readFileSync(process.argv[2] || join(RACINE, 'app.html'), 'utf8');
const geojsonTexte = readFileSync(join(RACINE, 'public', 'data', 'radon_zones_corse.geojson'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');

let echecs = 0;
const verifier = (libelle, ok, detail = '') => {
  console.log(`  ${ok ? '✔' : '✘'} ${libelle}${detail ? ' — ' + detail : ''}`);
  if (!ok) echecs++;
};

// ─── Extraction du code livré ───────────────────────────────────────────────────────────────
function extraireFonction(nom) {
  const m = new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\([^)]*\\)\\s*\\{').exec(js);
  if (!m) throw new Error('fonction introuvable dans app.html : ' + nom);
  let d = 1, i = m.index + m[0].length;
  while (i < js.length && d > 0) { const c = js[i]; if (c === '{') d++; else if (c === '}') d--; i++; }
  return js.slice(m.index, i);
}
const debut = js.indexOf('const REPRISE_CLASSES');
const fin = js.indexOf('// Cached fetch wrapper');
if (debut < 0 || fin < 0 || fin < debut) throw new Error('bloc assistant introuvable — marqueurs changés ?');
const assistant = js.slice(debut, fin);

const inscriptions = js.match(/enregistrerReprise\(\s*'radon'\s*,[\s\S]*?\n\s*\}\);/g) || [];

// ─── S0 — câblage (lecture statique du fichier livré) ───────────────────────────────────────
console.log('S0 — câblage dans app.html');
verifier('inscription de la clé radon présente une seule fois', inscriptions.length === 1, `${inscriptions.length} trouvée(s)`);
const ligneBoot = js.split('\n').find((l) => l.includes('setTimeout(()=>Promise.all([')) || '';
verifier("le lot de boot passe par declenche('radon', …)", /declenche\(\s*'radon'/.test(ligneBoot));
verifier('le lot de boot n’appelle PLUS indexRadonZonesOfficial() en direct (sinon deux fetchs, garde contourné)',
  !/indexRadonZonesOfficial\s*\(/.test(ligneBoot));
if (inscriptions.length !== 1) { console.log('\nCâblage absent : scénarios dynamiques non exécutables.'); process.exit(1); }

// ─── Bac à sable ────────────────────────────────────────────────────────────────────────────
const vraiSetTimeout = setTimeout;
let delais = [];
const sbSetTimeout = (fn, d) => { delais.push(d); return vraiSetTimeout(fn, 0); };
let decider = () => 'ok';
let appelsRadon = 0;
const fetchStub = async (url) => {
  if (!String(url).includes('radon_zones_corse')) throw new Error('fetch inattendu : ' + url);
  const n = ++appelsRadon;
  const action = decider(n);
  await new Promise((r) => vraiSetTimeout(r, 15)); // une vraie latence : le garde de concurrence doit la voir
  if (action === 'reseau') throw new TypeError('Failed to fetch');
  if (action === 'http500') return { ok: false, status: 500, json: async () => ({}) };
  if (action === 'vide') return { ok: true, status: 200, json: async () => ({ type: 'FeatureCollection', features: [] }) };
  return { ok: true, status: 200, json: async () => JSON.parse(geojsonTexte) };
};
const ctx = {
  window: { addEventListener() {} },
  document: { addEventListener() {}, visibilityState: 'visible' },
  fetch: fetchStub, setTimeout: sbSetTimeout, clearTimeout, console: { log() {}, warn() {}, error: console.error },
  AbortSignal,
};
const corps = [
  'const { window, document, fetch, setTimeout, clearTimeout, console, AbortSignal } = ctx;',
  // Déclarations reproduites de app.html (L8589, L8635-8637) — triviales, et le lot n'y touche pas.
  'let RADON_2A_APPLIES_ALL = false;',
  'const RADON_L3_INSEE_SET = new Set();',
  'const RADON_L3_NAME_SET = new Set();',
  'let _radonGeojsonCache = null;',
  assistant,
  extraireFonction('normCommuneName'),
  extraireFonction('indexRadonZonesOfficial'),
  extraireFonction('radonIndexComplet'),
  'function __inscrire(){ ' + inscriptions[0] + ' }',
  'return { REPRISE_CLASSES, declenche, reprisesEtat, _reprises, radonIndexComplet, __inscrire,',
  '  ensemble: RADON_L3_INSEE_SET,',
  "  vider(){ _radonGeojsonCache = null; RADON_L3_INSEE_SET.clear(); RADON_L3_NAME_SET.clear(); _reprises.delete('radon'); },",
  '  poserCache(g){ _radonGeojsonCache = g; } };',
].join('\n');
const api = new Function('ctx', corps)(ctx);

const attendu = new Set(JSON.parse(geojsonTexte).features
  .filter((f) => f.properties && f.properties.categorie === 3 && f.properties.code_insee)
  .map((f) => f.properties.code_insee)).size;

async function scenario(nom, plan) {
  api.vider();
  delais = [];
  appelsRadon = 0;
  decider = plan;
  api.__inscrire();
  await api.declenche('radon', 'boot');
  const t0 = Date.now();
  let etat = api.reprisesEtat('radon');
  while (!['ok', 'abandoned'].includes(etat) && Date.now() - t0 < 5000) {
    await new Promise((r) => vraiSetTimeout(r, 5));
    etat = api.reprisesEtat('radon');
  }
  await new Promise((r) => vraiSetTimeout(r, 40)); // vidange : aucune fuite vers le scénario suivant
  console.log(`\n${nom}`);
  return { etat, fetchs: appelsRadon, taille: api.ensemble.size, delais: delais.slice() };
}

// ─── S1 — nominal ───────────────────────────────────────────────────────────────────────────
let r = await scenario('S1 — nominal : le GeoJSON arrive du premier coup', () => 'ok');
verifier("état final 'ok'", r.etat === 'ok', r.etat);
verifier('un seul fetch', r.fetchs === 1, `${r.fetchs}`);
verifier(`index complet (${attendu} communes cat. 3)`, r.taille === attendu, `${r.taille}`);

// ─── S2 — LA réfutation centrale : échec, échec, puis succès ────────────────────────────────
// Ce qui prouverait que le lot ne marche pas : après un premier échec, plus aucune requête ne
// part (mémo ou poison, amendement 2) et l'index reste vide. Les deux branches d'échec du
// chargeur sont exercées : erreur réseau (throw du fetch) et HTTP 500 (throw sur !r.ok).
r = await scenario('S2 — réseau KO, puis HTTP 500, puis succès', (n) => (n === 1 ? 'reseau' : n === 2 ? 'http500' : 'ok'));
verifier("état final 'ok'", r.etat === 'ok', r.etat);
verifier('trois fetchs réels — le chargeur refetch bien après échec', r.fetchs === 3, `${r.fetchs}`);
verifier(`index complet (${attendu})`, r.taille === attendu, `${r.taille}`);

// ─── S3 — échec permanent : bornage ─────────────────────────────────────────────────────────
r = await scenario('S3 — réseau KO en permanence', () => 'reseau');
verifier("état final 'abandoned' — la série se termine", r.etat === 'abandoned', r.etat);
verifier('plus d’une tentative — la reprise s’est armée', r.fetchs > 1, `${r.fetchs} fetchs`);
const croissants = r.delais.every((d, i) => i === 0 || d > r.delais[i - 1]);
verifier('délais strictement croissants (critère de l’amendement 4)', croissants,
  r.delais.map((d) => Math.round(d / 1000) + ' s').join(' · '));
verifier('index resté vide', r.taille === 0, `${r.taille}`);
console.log(`    (classe critique : ${api.REPRISE_CLASSES.critique.tentatives} tentatives déclarées · ${r.fetchs} fetchs mesurés)`);

// ─── S4 — charge vide : la garde contre la vérité vacante ───────────────────────────────────
// Un GeoJSON 200 mais sans aucune commune cat. 3 : every() sur un ensemble vide rendrait VRAI.
// LIMITE DÉCLARÉE ET ENCODÉE ICI : indexRadonZonesOfficial() met la charge en cache même vide
// (_radonGeojsonCache posé après r.ok) et ne refetch plus — l'assistant s'arrête en
// 'abandoned' sans amplification, mais sans reprise non plus. Ce test fige ce comportement pour
// qu'il ne change pas en silence.
r = await scenario('S4 — HTTP 200 mais GeoJSON vide', () => 'vide');
verifier("jamais 'ok' sur une charge vide", r.etat !== 'ok', r.etat);
verifier('un seul fetch — la charge vide est réutilisée, pas de rafale', r.fetchs === 1, `${r.fetchs}`);
verifier('index resté vide', r.taille === 0, `${r.taille}`);

// ─── S5 — le prédicat, isolé ────────────────────────────────────────────────────────────────
console.log('\nS5 — radonIndexComplet(), isolé');
api.vider();
verifier('faux sans cache', api.radonIndexComplet() === false);
const g = JSON.parse(geojsonTexte);
api.poserCache(g);
verifier('faux avec cache mais index vide', api.radonIndexComplet() === false);
g.features.filter((f) => f.properties && f.properties.categorie === 3).forEach((f) => api.ensemble.add(f.properties.code_insee));
verifier('vrai quand chaque commune cat. 3 est indexée', api.radonIndexComplet() === true);
api.ensemble.delete([...api.ensemble][0]);
verifier('faux s’il en manque UNE seule — identité, pas seuil', api.radonIndexComplet() === false);
api.vider();

// ─── S6 — le garde de concurrence ───────────────────────────────────────────────────────────
console.log('\nS6 — 50 déclenchements simultanés');
api.vider(); appelsRadon = 0; decider = () => 'ok'; api.__inscrire();
await Promise.all(Array.from({ length: 50 }, () => api.declenche('radon', 'salve')));
await new Promise((res) => vraiSetTimeout(res, 60));
verifier('une seule requête émise', appelsRadon === 1, `${appelsRadon}`);

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}`);
process.exit(echecs === 0 ? 0 : 1);
