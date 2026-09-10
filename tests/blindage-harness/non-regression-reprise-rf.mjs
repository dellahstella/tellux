// ─── Non-régression : reprise des émetteurs TDF et de la forêt dense (lot RF, 2026-09-10) ─────────
// Le lot adopte loadTDFEmitters() et loadForetDenseGrid() dans l'assistant de reprise partagé
// (#1366). Ce fichier est la RÉFUTATION écrite AVANT le lot — et exécutée contre le code d'avant le
// lot, pour vérifier qu'elle attrape bien le défaut qu'elle prétend attraper.
//
// CE QUE L'ÉCHEC PRODUIT — mesuré le 2026-09-10 en navigateur (Chromium, ?no-bt=1)
//   · TDF : à 41,7347 / 8,7926 (à 300 m de l'émetteur Ajaccio Coti-Chiavari, 197 kW), RF_field donne
//     6 650 µW/m² avec les émetteurs, 148 sans — un facteur 45. Loin des émetteurs TDF
//     (41,3888 / 9,1595), écart négligeable : 12 320 contre 12 318 µW/m², le terme ANFR domine.
//   · Forêt dense : couche activée, au clic, rapport valeur non atténuée / atténuée de médiane 29
//     (quartiles 15 et 58, de 1,0 à 965) sur 48 points tirés dans les polygones — centre de boîte d'un
//     polygone sur 100, retenu s'il est en forêt. Si le chargement a échoué, le popup affiche la
//     valeur NON atténuée alors que l'interface promet « module la valeur µW/m² au clic ».
//
// LE DÉFAUT QUE LE LOT CORRIGE — et que ce fichier doit attraper
// Les deux chargeurs mémoïsent leur promesse et AVALENT leur échec : après un échec, le mémo reste
// une promesse résolue, et tout rappel retourne sans refetch — la reprise est impossible par
// construction. Pour la forêt dense c'est aussi le chemin de L'UTILISATEUR qui meurt : rebasculer la
// couche rappelle loadForetDenseGrid(), qui rend le mémo mort, sans aucun fetch.
// Et un rattrapage qui ne se VOIT pas n'en est qu'à moitié un : la carte de chaleur RF est
// reconstruite une fois, en fin de calibrateRF(), avec les émetteurs présents À CET INSTANT ; une
// couche forêt activée pendant la panne reste vide même quand la donnée arrive. D'où S9.
// Contre le code d'avant le lot, S2, S3, S8 et S9 DOIVENT échouer. S'ils passaient, ce fichier ne
// prouverait rien.
//
// CE QUE CE FICHIER NE TESTE PAS, ET OÙ C'EST TESTÉ
//   · La calibration : une panne TDF déplace-t-elle RF_CALIB_K ? Non, grille ANFR chargée
//     (Δk/k = 6 × 10⁻⁵, mesuré) — voir verif-calibration-rf-sans-tdf.mjs, qui la re-mesure et échoue
//     si elle devenait sensible. Grille ANFR vide, oui : défaut de loadANFRForField, hors de ce lot.
//   · La relance par `online` / `visibilitychange` dans un vrai navigateur : vérifiée à part.
//
// MODE AVANT-LOT : si l'inscription livrée d'une clé manque, l'inscription PRÉVUE est utilisée et le
// harnais le dit. Le code sous test est EXTRAIT du app.html livré — chargeurs, enrobages de reprise
// s'ils existent, et déclarations de leurs variables, lues dans le fichier, pas recopiées. Seuls
// fetch, setTimeout, le DOM et les fonctions d'affichage (rebuildHotDebounced, buildForetDenseLayer,
// la couche Leaflet) sont simulés ; les fichiers servis sont les VRAIS fichiers du dépôt.
// Temps compressé : on mesure les DÉCISIONS du code. Isolation : chaque scénario attend un état
// terminal, se vide, repart d'une inscription neuve.
//
// Usage : node tests/blindage-harness/non-regression-reprise-rf.mjs   (sort 1 si un ✘)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const RACINE = join(ICI, '..', '..');
const html = readFileSync(process.argv[2] || join(RACINE, 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
const lire = (f) => readFileSync(join(RACINE, 'public', 'data', f), 'utf8');

const texteForet = lire('foret_dense_corse.geojson');
const partiesForet = (() => {
  const g = JSON.parse(texteForet);
  const geom = g.features && g.features[0] && g.features[0].geometry;
  return geom && geom.type === 'MultiPolygon' ? geom.coordinates.length : geom && geom.type === 'Polygon' ? 1 : 0;
})();

const RESSOURCES = {
  tdf: {
    fragment: 'tdf_emitters_corse', texte: lire('tdf_emitters_corse.json'), vide: () => ({ emitters: [] }),
    chargeur: 'loadTDFEmitters', enrobage: 'repriseTDF', variables: ['TDF_EMITTERS', '_tdfLoadPromise'],
    attendu: (JSON.parse(lire('tdf_emitters_corse.json')).emitters || []).length,
    prevue: "enregistrerReprise('tdf', loadTDFEmitters, {\n    classe: 'critique',\n    verifie: () => Array.isArray(TDF_EMITTERS) && TDF_EMITTERS.length > 0\n  });",
  },
  foretdense: {
    fragment: 'foret_dense_corse', texte: texteForet, vide: () => ({ type: 'FeatureCollection', features: [] }),
    chargeur: 'loadForetDenseGrid', enrobage: 'repriseForetDense', variables: ['FORET_DENSE_PARTS', 'FORET_DENSE_BBOX_GLOBAL', '_foretDensePromise'],
    attendu: partiesForet,
    prevue: "enregistrerReprise('foretdense', loadForetDenseGrid, {\n    classe: 'critique',\n    verifie: () => Array.isArray(FORET_DENSE_PARTS) && FORET_DENSE_PARTS.length > 0\n  });",
  },
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

// ─── S0 — câblage ────────────────────────────────────────────────────────────────────────────────
console.log('S0 — câblage dans app.html');
const ligneBoot = js.split('\n').find((l) => l.includes('setTimeout(()=>Promise.all([')) || '';
let modeAvant = false;
for (const [cle, r] of Object.entries(RESSOURCES)) {
  const trouvees = js.match(new RegExp("enregistrerReprise\\(\\s*'" + cle + "'\\s*,[\\s\\S]*?\\n\\s*\\}\\);", 'g')) || [];
  verifier(`inscription '${cle}' présente une seule fois`, trouvees.length === 1, `${trouvees.length} trouvée(s)`);
  verifier(`le lot de boot passe par declenche('${cle}', …)`, new RegExp("declenche\\(\\s*'" + cle + "'").test(ligneBoot));
  verifier(`le lot de boot n’appelle PLUS ${r.chargeur}() en direct`, !new RegExp('\\b' + r.chargeur + '\\s*\\(').test(ligneBoot));
  verifier(`enrobage ${r.enrobage}() présent`, existeFonction(r.enrobage));
  if (trouvees.length === 1) r.inscription = trouvees[0]; else { r.inscription = r.prevue; modeAvant = true; }
}
const CONDITION_TOG_HOTRF = "if(id==='hotrf'&&lHotRF.getLayers().length===0)buildHotRF();";
verifier("tog('hotrf') ne reconstruit qu’une couche vide — condition simulée par rallumerRF()", js.includes(CONDITION_TOG_HOTRF));
if (modeAvant) console.log('\n  ⚠ MODE AVANT-LOT : inscription(s) absente(s) — l’inscription PRÉVUE est utilisée.\n    Attendu dans ce mode : S2, S3, S8 et S9 en échec.');

// ─── Bac à sable ─────────────────────────────────────────────────────────────────────────────────
const vraiSetTimeout = setTimeout;
let delais = [];
const sbSetTimeout = (fn, d) => { delais.push(d); return vraiSetTimeout(fn, 0); };
const plans = { tdf: () => 'ok', foretdense: () => 'ok' };
const appels = { tdf: 0, foretdense: 0 };
const fetchStub = async (url) => {
  const cle = Object.keys(RESSOURCES).find((k) => String(url).includes(RESSOURCES[k].fragment));
  if (!cle) throw new Error('fetch inattendu : ' + url);
  const n = ++appels[cle];
  const action = plans[cle](n);
  await new Promise((r) => vraiSetTimeout(r, 15));
  if (action === 'reseau') throw new TypeError('Failed to fetch');
  if (action === 'http500') return { ok: false, status: 500, json: async () => ({}) };
  if (action === 'vide') return { ok: true, status: 200, json: async () => RESSOURCES[cle].vide() };
  return { ok: true, status: 200, json: async () => JSON.parse(RESSOURCES[cle].texte) };
};
const ctx = {
  window: { addEventListener() {} },
  document: { addEventListener() {}, visibilityState: 'visible' },
  fetch: fetchStub, setTimeout: sbSetTimeout, clearTimeout, console: { log() {}, warn() {}, error: console.error },
  AbortSignal,
};
const declarations = Object.values(RESSOURCES).flatMap((r) => r.variables.map(extraireDeclaration));
const enrobages = Object.values(RESSOURCES).map((r) => r.enrobage).filter(existeFonction).map(extraireFonction);
const corps = [
  'const { window, document, fetch, setTimeout, clearTimeout, console, AbortSignal } = ctx;',
  ...declarations,
  // Simulations d'affichage : ce qui compte, c'est QUAND le code les appelle, pas ce qu'elles dessinent.
  'let RF_CALIB_STATS = null;',
  'const ACTIVE = {};',
  // La VRAIE rebuildHotDebounced, extraite : c'est elle qui décide quelles cartes se redessinent selon
  // ACTIVE. Seuls les dessins sont simulés (compteurs) ; un enrobage qui l'appellerait redessinerait
  // aussi composite et ELF, et S9b le voit.
  extraireDeclaration('_hotDebounce'),
  'let __hotrf = [], __constructionsRF = 0, __autres = 0;',
  'const lHotRF = { clearLayers(){ __hotrf = []; }, getLayers(){ return __hotrf; } };',
  'function buildHotRF(){ __constructionsRF++; __hotrf = [1]; }',
  'const lHot = { clearLayers(){} }; function buildHot(){ __autres++; } function buildElf(){ __autres++; }',
  extraireFonction('rebuildHotDebounced'),
  'let __couche = []; const lForetDense = { getLayers(){ return __couche; } };',
  'let __dessins = 0; function buildForetDenseLayer(){ __dessins++; __couche = (FORET_DENSE_PARTS && FORET_DENSE_PARTS.length) ? [1] : []; }',
  assistant,
  extraireFonction('loadTDFEmitters'),
  extraireFonction('loadForetDenseGrid'),
  ...enrobages,
  'function __inscrire(cle){',
  "  if (cle === 'tdf') { " + RESSOURCES.tdf.inscription + ' }',
  "  if (cle === 'foretdense') { " + RESSOURCES.foretdense.inscription + ' }',
  '}',
  'return { REPRISE_CLASSES, declenche, reprisesEtat, _reprises, __inscrire,',
  "  vider(cle){ if (cle === 'tdf') { TDF_EMITTERS = []; _tdfLoadPromise = null; }",
  "              if (cle === 'foretdense') { FORET_DENSE_PARTS = null; FORET_DENSE_BBOX_GLOBAL = null; _foretDensePromise = null; }",
  "              _reprises.delete(cle); RF_CALIB_STATS = null; ACTIVE.foretdense = undefined; __couche = []; __dessins = 0;",
  "              ACTIVE.hot = ACTIVE.hotrf = ACTIVE.elf = undefined; __hotrf = []; __constructionsRF = 0; __autres = 0; },",
  "  taille(cle){ return cle === 'tdf' ? (TDF_EMITTERS || []).length : (FORET_DENSE_PARTS ? FORET_DENSE_PARTS.length : 0); },",
  "  direct(cle){ return cle === 'tdf' ? loadTDFEmitters() : loadForetDenseGrid(); },",
  '  calibrationFaite(b){ RF_CALIB_STATS = b ? { n_used: 21 } : null; },',
  '  coucheActiveVide(b){ ACTIVE.foretdense = b ? true : undefined; __couche = []; },',
  '  carte(o){ ACTIVE.hot = o.hot; ACTIVE.hotrf = o.hotrf; ACTIVE.elf = o.elf; __hotrf = o.perimee ? [1] : []; },',
  // Rallumage de la carte RF : la condition de tog('hotrf') (branche ON), recopiée — S0 vérifie qu'elle
  // n'a pas changé dans app.html, sans quoi cette simulation mentirait.
  '  rallumerRF(){ ACTIVE.hotrf = true; if (lHotRF.getLayers().length === 0) buildHotRF(); return __constructionsRF; },',
  '  compteurs(){ return { constructionsRF: __constructionsRF, autres: __autres, dessins: __dessins }; } };',
].join('\n');
const api = new Function('ctx', corps)(ctx);

async function scenario(cle, nom, plan, avant = () => {}) {
  api.vider(cle);
  delais = []; appels[cle] = 0; plans[cle] = plan;
  avant();
  api.__inscrire(cle);
  await api.declenche(cle, 'boot');
  const t0 = Date.now();
  let etat = api.reprisesEtat(cle);
  while (!['ok', 'abandoned'].includes(etat) && Date.now() - t0 < 8000) {
    await new Promise((r) => vraiSetTimeout(r, 5));
    etat = api.reprisesEtat(cle);
  }
  await new Promise((r) => vraiSetTimeout(r, 40));
  console.log(`\n[${cle}] ${nom}`);
  return { etat, fetchs: appels[cle], taille: api.taille(cle), delais: delais.slice(), ...api.compteurs() };
}

for (const cle of Object.keys(RESSOURCES)) {
  const N = RESSOURCES[cle].attendu;

  let r = await scenario(cle, 'S1 — nominal', () => 'ok');
  verifier("état 'ok'", r.etat === 'ok', r.etat);
  verifier('un seul fetch', r.fetchs === 1, `${r.fetchs}`);
  verifier(`jeu complet (${N})`, r.taille === N, `${r.taille}`);
  const avant = appels[cle];
  await api.direct(cle);
  verifier('S6 — après succès, un appel direct ne refetch pas (mémo conservé sur succès)', appels[cle] === avant, `${appels[cle] - avant} fetch(s) de plus`);

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

  // S4 — limite déclarée et figée : un fichier 200 mais vide est un SUCCÈS du chargeur (mémo conservé),
  // le prédicat le refuse, les reprises retombent sur le mémo sans refetch. Pour la forêt dense, c'est
  // le « cas silencieux » : une géométrie absente donne FORET_DENSE_PARTS = [] (truthy), sans warn.
  r = await scenario(cle, 'S4 — HTTP 200 mais jeu vide', () => 'vide');
  verifier("jamais 'ok' sur un jeu vide", r.etat !== 'ok', r.etat);
  verifier('un seul fetch — pas de rafale', r.fetchs === 1, `${r.fetchs}`);

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

  // S8 — le chemin DIRECT après un échec, sans l'assistant : c'est celui de la bascule de la couche
  // forêt dense (loadForetDenseGrid().then(buildForetDenseLayer)) et de loadAnt() pour TDF. Contre le
  // code d'avant le lot, le second appel rend le mémo mort : AUCUN fetch, jeu toujours vide.
  api.vider(cle); appels[cle] = 0; plans[cle] = (n) => (n === 1 ? 'reseau' : 'ok');
  await api.direct(cle);
  await api.direct(cle);
  console.log(`\n[${cle}] S8 — après un échec, un appel direct (la bascule) relance-t-il un vrai fetch ?`);
  verifier('deux fetchs réels — le second appel refetch', appels[cle] === 2, `${appels[cle]}`);
  verifier(`jeu complet après le second appel (${N})`, api.taille(cle) === N, `${api.taille(cle)}`);
}

// ─── S9 — le rattrapage doit SE VOIR ─────────────────────────────────────────────────────────────
// TDF : la carte de chaleur RF est reconstruite en fin de calibrateRF(), avec les émetteurs présents à
// cet instant. Un retour TARDIF (calibration déjà faite) doit la rafraîchir — une fois, pas à chaque
// tentative, et ELLE SEULE : composite et ELF ne dépendent pas de TDF. Couche RF ÉTEINTE pendant la
// panne : elle doit se reconstruire au rallumage, sinon la carte d'avant, sans TDF, réapparaît
// (tog ne reconstruit qu'une couche vide). Au démarrage nominal (calibration pas encore faite), AUCUN
// rafraîchissement : c'est calibrateRF qui construira la carte — la construire avant, à k = 1,
// afficherait un instant des valeurs ×7,7 en S.
const toutAllume = { hot: true, hotrf: true, elf: true, perimee: true };
let r = await scenario('tdf', 'S9a — démarrage nominal, calibration pas encore faite', () => 'ok', () => api.carte(toutAllume));
verifier('aucune reconstruction de la carte RF', r.constructionsRF === 0, `${r.constructionsRF}`);
verifier('aucune autre carte redessinée', r.autres === 0, `${r.autres}`);
r = await scenario('tdf', 'S9b — retour tardif, carte RF allumée : KO puis succès',
  (n) => (n === 1 ? 'reseau' : 'ok'), () => { api.calibrationFaite(true); api.carte(toutAllume); });
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('carte RF reconstruite exactement une fois, au succès', r.constructionsRF === 1, `${r.constructionsRF}`);
verifier('reconstruction CIBLÉE — ni composite ni ELF redessinés', r.autres === 0, `${r.autres}`);
r = await scenario('tdf', 'S9e — retour tardif, carte RF ÉTEINTE pendant la panne, rallumée après',
  (n) => (n === 1 ? 'reseau' : 'ok'), () => { api.calibrationFaite(true); api.carte({ hotrf: false, perimee: true }); });
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('rien de construit tant que la couche est éteinte', r.constructionsRF === 0, `${r.constructionsRF}`);
verifier('au rallumage, la carte est reconstruite — pas celle d’avant, sans TDF', api.rallumerRF() === 1);
// S9f — LIMITE DÉCLARÉE ET FIGÉE : calibration échouée (RF_CALIB_STATS reste null), puis retour tardif
// de TDF → pas de reconstruction ; la carte se corrige au prochain zoom. Pour le code, « calibration
// échouée » et « pas encore faite » sont le même état : reconstruire ici, c'est reconstruire aussi à
// k = 1 au démarrage nominal (S9a). Si ce cas est un jour traité, ce scénario doit être réécrit.
r = await scenario('tdf', 'S9f — calibration échouée, retour tardif (limite déclarée)',
  (n) => (n === 1 ? 'reseau' : 'ok'), () => api.carte(toutAllume));
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('aucune reconstruction — la carte attend le prochain zoom', r.constructionsRF === 0, `${r.constructionsRF}`);
// Forêt dense : couche activée PENDANT la panne → tog() a tenté le dessin sur une couche vide. Au
// retour de la donnée, la couche doit être dessinée. Couche inactive → rien à dessiner.
r = await scenario('foretdense', 'S9c — couche activée pendant la panne, puis retour de la donnée',
  (n) => (n === 1 ? 'reseau' : 'ok'), () => api.coucheActiveVide(true));
verifier("état 'ok'", r.etat === 'ok', r.etat);
verifier('couche dessinée exactement une fois', r.dessins === 1, `${r.dessins}`);
r = await scenario('foretdense', 'S9d — couche inactive, retour de la donnée', () => 'ok');
verifier('aucun dessin — la couche n’est pas demandée', r.dessins === 0, `${r.dessins}`);

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}${modeAvant ? '  (mode avant-lot)' : ''}`);
process.exit(echecs === 0 ? 0 : 1);
