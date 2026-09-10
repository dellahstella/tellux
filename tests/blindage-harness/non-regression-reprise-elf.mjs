// ─── Non-régression : reprise des postes sources et des éoliennes (lot ELF, 2026-09-10) ──────
// Le lot adopte loadPostesSources() et loadEoliennesData() dans l'assistant de reprise partagé
// (#1366). Ce fichier est la RÉFUTATION écrite AVANT le lot — et EXÉCUTÉE contre le code d'avant
// le lot, pour vérifier qu'elle attrape bien le défaut qu'elle prétend attraper.
//
// CE QUE L'ÉCHEC PRODUIT
// calcMagneticELF_v1/v2 ajoutent, près de chaque poste source (≤ 1 km), jusqu'à 500 nT, et près
// de chaque parc éolien (≤ 0,5 km), jusqu'à 300 nT. Si le chargement échoue, ces termes valent
// zéro — une valeur affichée fausse, pas une couche absente. Pour les éoliennes c'est pire qu'un
// terme manquant : le calcul saute SANS CONDITION les entrées « Eolien » de PROD_ELECTRIQUE au
// motif qu'elles sont « comptées via EOLIENNES_DATA ». Sans EOLIENNES_DATA, les parcs ne sont
// comptés nulle part.
//
// LE DÉFAUT QUE LE LOT CORRIGE — et que ce fichier doit attraper
// Les deux chargeurs mémoïsent leur promesse et AVALENT leur échec : après un échec, le mémo reste
// une promesse résolue et tout rappel retourne sans refetch. La reprise est alors impossible par
// construction — même patron que loadBTLinesAsync avant le lot 2.
// Contre le code d'avant le lot, S2 et S3 DOIVENT échouer. S'ils passaient, ce fichier ne
// prouverait rien.
//
// MODE AVANT-LOT : si l'inscription livrée d'une clé est absente de app.html, le harnais utilise
// l'inscription PRÉVUE (même classe, même prédicat) et le signale. S0 est alors en échec par
// construction ; les scénarios dynamiques tournent quand même, sur les chargeurs tels qu'ils sont.
//
// LE CODE SOUS TEST EST EXTRAIT DU app.html LIVRÉ, pas réécrit. Seuls fetch, setTimeout et le DOM
// sont simulés ; les JSON servis sont les VRAIS fichiers du dépôt. Temps compressé : setTimeout
// enregistre le délai demandé et déclenche aussitôt — on mesure les DÉCISIONS du code.
// Isolation : chaque scénario attend un état terminal, se vide, repart d'une inscription neuve
// (leçon du 2026-09-09 : une chaîne de reprise avait fui ses délais dans le test suivant).
//
// CE QUE CE FICHIER NE PROUVE PAS : la relance par `online` / `visibilitychange` dans un vrai
// navigateur. Vérifiée à part.
//
// Usage : node tests/blindage-harness/non-regression-reprise-elf.mjs   (sort 1 si un ✘)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..', '..');
const html = readFileSync(process.argv[2] || join(RACINE, 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
const lireJson = (f) => readFileSync(join(RACINE, 'public', 'data', f), 'utf8');

const RESSOURCES = {
  postes: {
    fragment: 'postes_sources_corse', texte: lireJson('postes_sources_corse.json'), cleJson: 'postes',
    chargeur: 'loadPostesSources',
    prevue: "enregistrerReprise('postes', loadPostesSources, {\n    classe: 'critique',\n    verifie: () => Array.isArray(POSTES_SOURCES) && POSTES_SOURCES.length > 0\n  });",
  },
  eoliennes: {
    fragment: 'eoliennes_corse', texte: lireJson('eoliennes_corse.json'), cleJson: 'eoliennes',
    chargeur: 'loadEoliennesData',
    prevue: "enregistrerReprise('eoliennes', loadEoliennesData, {\n    classe: 'critique',\n    verifie: () => Array.isArray(EOLIENNES_DATA) && EOLIENNES_DATA.length > 0\n  });",
  },
};
for (const [cle, r] of Object.entries(RESSOURCES)) r.attendu = (JSON.parse(r.texte)[r.cleJson] || []).length;

let echecs = 0;
const verifier = (libelle, ok, detail = '') => {
  console.log(`  ${ok ? '✔' : '✘'} ${libelle}${detail ? ' — ' + detail : ''}`);
  if (!ok) echecs++;
};

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

// ─── S0 — câblage ───────────────────────────────────────────────────────────────────────────
console.log('S0 — câblage dans app.html');
const ligneBoot = js.split('\n').find((l) => l.includes('setTimeout(()=>Promise.all([')) || '';
let modeAvant = false;
for (const [cle, r] of Object.entries(RESSOURCES)) {
  const trouvees = js.match(new RegExp("enregistrerReprise\\(\\s*'" + cle + "'\\s*,[\\s\\S]*?\\n\\s*\\}\\);", 'g')) || [];
  verifier(`inscription '${cle}' présente une seule fois`, trouvees.length === 1, `${trouvees.length} trouvée(s)`);
  verifier(`le lot de boot passe par declenche('${cle}', …)`, new RegExp("declenche\\(\\s*'" + cle + "'").test(ligneBoot));
  verifier(`le lot de boot n’appelle PLUS ${r.chargeur}() en direct`, !new RegExp('\\b' + r.chargeur + '\\s*\\(').test(ligneBoot));
  if (trouvees.length === 1) r.inscription = trouvees[0]; else { r.inscription = r.prevue; modeAvant = true; }
}
if (modeAvant) console.log('\n  ⚠ MODE AVANT-LOT : inscription(s) absente(s) — l’inscription PRÉVUE est utilisée.\n    Attendu dans ce mode : S2 et S3 en échec sur le mémo qui survit à l’échec.');

// ─── Bac à sable ────────────────────────────────────────────────────────────────────────────
const vraiSetTimeout = setTimeout;
let delais = [];
const sbSetTimeout = (fn, d) => { delais.push(d); return vraiSetTimeout(fn, 0); };
const plans = { postes: () => 'ok', eoliennes: () => 'ok' };
const appels = { postes: 0, eoliennes: 0 };
const fetchStub = async (url) => {
  const cle = Object.keys(RESSOURCES).find((k) => String(url).includes(RESSOURCES[k].fragment));
  if (!cle) throw new Error('fetch inattendu : ' + url);
  const n = ++appels[cle];
  const action = plans[cle](n);
  await new Promise((r) => vraiSetTimeout(r, 15));
  if (action === 'reseau') throw new TypeError('Failed to fetch');
  if (action === 'http500') return { ok: false, status: 500, json: async () => ({}) };
  if (action === 'vide') return { ok: true, status: 200, json: async () => ({ [RESSOURCES[cle].cleJson]: [] }) };
  return { ok: true, status: 200, json: async () => JSON.parse(RESSOURCES[cle].texte) };
};
const ctx = {
  window: { addEventListener() {} },
  document: { addEventListener() {}, visibilityState: 'visible' },
  fetch: fetchStub, setTimeout: sbSetTimeout, clearTimeout, console: { log() {}, warn() {}, error: console.error },
  AbortSignal,
};
const corps = [
  'const { window, document, fetch, setTimeout, clearTimeout, console, AbortSignal } = ctx;',
  // Déclarations reproduites de app.html (L7528-7529, L7551-7552) — le lot n'y touche pas.
  'let POSTES_SOURCES = []; let _postesLoadPromise = null;',
  'let EOLIENNES_DATA = []; let _eolLoadPromise = null;',
  assistant,
  extraireFonction('loadPostesSources'),
  extraireFonction('loadEoliennesData'),
  'function __inscrire(cle){',
  "  if (cle === 'postes') { " + RESSOURCES.postes.inscription + ' }',
  "  if (cle === 'eoliennes') { " + RESSOURCES.eoliennes.inscription + ' }',
  '}',
  'return { REPRISE_CLASSES, declenche, reprisesEtat, _reprises, __inscrire,',
  "  vider(cle){ if (cle === 'postes') { POSTES_SOURCES = []; _postesLoadPromise = null; }",
  "              if (cle === 'eoliennes') { EOLIENNES_DATA = []; _eolLoadPromise = null; }",
  '              _reprises.delete(cle); },',
  "  taille(cle){ return cle === 'postes' ? POSTES_SOURCES.length : EOLIENNES_DATA.length; },",
  "  direct(cle){ return cle === 'postes' ? loadPostesSources() : loadEoliennesData(); } };",
].join('\n');
const api = new Function('ctx', corps)(ctx);

async function scenario(cle, nom, plan) {
  api.vider(cle);
  delais = []; appels[cle] = 0; plans[cle] = plan;
  api.__inscrire(cle);
  await api.declenche(cle, 'boot');
  const t0 = Date.now();
  let etat = api.reprisesEtat(cle);
  while (!['ok', 'abandoned'].includes(etat) && Date.now() - t0 < 5000) {
    await new Promise((r) => vraiSetTimeout(r, 5));
    etat = api.reprisesEtat(cle);
  }
  await new Promise((r) => vraiSetTimeout(r, 40));
  console.log(`\n[${cle}] ${nom}`);
  return { etat, fetchs: appels[cle], taille: api.taille(cle), delais: delais.slice() };
}

for (const cle of Object.keys(RESSOURCES)) {
  const N = RESSOURCES[cle].attendu;

  let r = await scenario(cle, 'S1 — nominal', () => 'ok');
  verifier("état 'ok'", r.etat === 'ok', r.etat);
  verifier('un seul fetch', r.fetchs === 1, `${r.fetchs}`);
  verifier(`jeu complet (${N})`, r.taille === N, `${r.taille}`);

  // S6 enchaîne sur l'état de S1 : après un succès, un rappel direct (togPostesSources, loadProd)
  // ne doit PAS refetch — le mémo garde son rôle sur le chemin de succès.
  const avant = appels[cle];
  await api.direct(cle);
  verifier('S6 — après succès, un rappel direct ne refetch pas (mémo conservé sur succès)', appels[cle] === avant, `${appels[cle] - avant} fetch(s) de plus`);

  // S2 — LA réfutation centrale. Contre le code d'avant le lot : 1 seul fetch, jamais 'ok'.
  r = await scenario(cle, 'S2 — réseau KO, puis HTTP 500, puis succès', (n) => (n === 1 ? 'reseau' : n === 2 ? 'http500' : 'ok'));
  verifier("état 'ok'", r.etat === 'ok', r.etat);
  verifier('trois fetchs réels — le mémo est relâché sur échec', r.fetchs === 3, `${r.fetchs}`);
  verifier(`jeu complet (${N})`, r.taille === N, `${r.taille}`);

  r = await scenario(cle, 'S3 — réseau KO en permanence', () => 'reseau');
  verifier("état 'abandoned' — la série se termine", r.etat === 'abandoned', r.etat);
  verifier('plus d’une tentative RÉELLE — chaque reprise refetch', r.fetchs > 1, `${r.fetchs} fetchs`);
  verifier('délais strictement croissants', r.delais.every((d, i) => i === 0 || d > r.delais[i - 1]),
    r.delais.map((d) => Math.round(d / 1000) + ' s').join(' · '));

  // S4 — limite déclarée et figée : un JSON 200 mais vide est un SUCCÈS du chargeur (le mémo est
  // conservé), le prédicat le refuse, les reprises retombent sur le mémo sans refetch.
  r = await scenario(cle, 'S4 — HTTP 200 mais jeu vide', () => 'vide');
  verifier("jamais 'ok' sur un jeu vide", r.etat !== 'ok', r.etat);
  verifier('un seul fetch — pas de rafale', r.fetchs === 1, `${r.fetchs}`);

  // S5 — le mémo garde son rôle d'exclusion en vol : un appel direct concurrent d'une reprise
  // (togPostesSources, loadProd appellent le chargeur sans passer par l'assistant) partage la
  // même requête au lieu d'en lancer une seconde.
  api.vider(cle); appels[cle] = 0; plans[cle] = () => 'ok'; api.__inscrire(cle);
  await Promise.all([api.declenche(cle, 'boot'), api.direct(cle)]);
  await new Promise((res) => vraiSetTimeout(res, 40));
  console.log(`\n[${cle}] S5 — appel direct concurrent d'une reprise`);
  verifier('une seule requête', appels[cle] === 1, `${appels[cle]}`);

  api.vider(cle); appels[cle] = 0; plans[cle] = () => 'ok'; api.__inscrire(cle);
  await Promise.all(Array.from({ length: 50 }, () => api.declenche(cle, 'salve')));
  await new Promise((res) => vraiSetTimeout(res, 60));
  console.log(`\n[${cle}] S7 — 50 déclenchements simultanés`);
  verifier('une seule requête', appels[cle] === 1, `${appels[cle]}`);
}

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}${modeAvant ? '  (mode avant-lot)' : ''}`);
process.exit(echecs === 0 ? 0 : 1);
