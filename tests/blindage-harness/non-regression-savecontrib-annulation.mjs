// ─── Non-régression : « Annuler » pendant l'enregistrement d'une contribution (2026-09-10) ──────────
// RÉFUTATION écrite AVANT chaque version du correctif, et exécutée contre le code d'avant pour vérifier
// qu'elle attrape le défaut qu'elle prétend attraper.
//
// LE DÉFAUT (trouvé par la revue adverse du 2026-09-10, présent depuis 3c15032, 2026-04-18)
// saveContrib() lit la position du point (`pending`), puis attend : jusqu'à 20 s que le calcul ELF soit
// prêt (« Finalisation du calcul… »), puis la réponse de l'INSERT Supabase. Pendant ces deux attentes, des
// gestes peuvent retirer ou remplacer `pending` : Annuler (bouton ou clic hors du formulaire, cancelContrib),
// le bouton « + » qui referme (startContribFromFAB), « Repositionner » (repositionMarker), puis un nouveau
// point (_placeContribMarker). Avant correctif : la mesure annulée est ÉCRITE, puis removeLayer(null) lève
// dans Leaflet et « Erreur : … » s'affiche après une écriture réussie ; une relance l'écrit deux fois.
//
// CONCEPTION RETENUE (troisième, 2026-09-11) — un envoi parti ne s'annule pas, il se DÉTACHE.
//   · Pendant l'attente du calcul : point retiré ou remplacé, consentement retiré, saisie invalidée →
//     l'enregistrement est ABANDONNÉ, rien n'est écrit.
//   · Pendant l'envoi : fermer le formulaire (Annuler, « + ») reste possible à tout moment ; l'envoi est
//     détaché et le message le dit. Repositionner est refusé et désactivé tant que l'envoi est attaché.
//   · La réponse d'un envoi détaché ne touche ni au formulaire suivant, ni à ses boutons, ni au « + », ni à
//     l'envoi suivant ; elle annonce sa propre issue : enregistrée, ou NON CONFIRMÉE (un rejet ne prouve pas
//     l'absence d'écriture : la connexion peut tomber après la validation côté serveur) — jamais « Erreur : ».
// Deux conceptions précédentes ont été écartées par la revue adverse : refuser Annuler pendant l'envoi
// enfermait l'utilisateur (sbPost n'a pas de délai) ; borner ce refus reportait le blocage sur la mesure
// suivante et laissait « Mesure annulée. » précéder une écriture. Ce fichier les fait donc échouer aussi.
//
// CE QUI EST SIMULÉ : le DOM (éléments qui retiennent leur état), la carte (removeLayer LÈVE sur null,
// comme Leaflet 1.9.4), sbPost (délai et issue scriptés, ou réponse libérée par le scénario, une base en
// mémoire — y compris « écrit, puis réponse perdue »), computeElfState (« loading » pendant une durée
// scriptée), validateContrib (valeur vide = invalide), jt() (rend sa clé devant le texte). Les fonctions en
// cause sont EXTRAITES d'app.html telles quelles, avec les déclarations et _detacherEnvoiContrib().
//
// SUITE (2026-09-11, lot ant/anfr) — G : un enregistrement réussi sur une liste des contributions jamais
// chargée ne transmet pas de compte au point d'état, parce que la liste locale n'est pas un total. Contre
// le code d'avant ce lot, G1 et G2 DOIVENT échouer.
//
// SUITE (2026-09-11, lot D2) — H : un rafraîchissement de la liste qui relit la table APRÈS la validation de
// l'INSERT mais AVANT sa réponse y a déjà mis la ligne. saveContrib() ne doit ni l'ajouter une seconde fois,
// ni redessiner son marqueur, ni la compter deux fois. Dédoublonnage sur l'id que renvoie l'INSERT. Contre le
// code d'avant ce lot, H1 DOIT échouer ; H2 (sans rafraîchissement) et H3 (réponse sans ligne, donc sans id)
// sont des témoins ; H4 et H5 sont des gardes. Revue adverse du 2026-09-11, deux passes :
//   · H1 : le rafraîchissement REMPLACE la liste, comme loadDB(), la ligne étant tour à tour en tête et hors de
//     la tête ;
//   · H5 : la liste relue pendant l'envoi ne contient pas encore la ligne, qui doit être ajoutée ;
//   · H4 : deux vrais enregistrements identiques successifs, réponses sans ligne ; deux lignes sans id ne sont
//     jamais prises pour la même.
// Chaque version plus étroite laissait passer un mutant : lecture de la liste d'avant l'envoi, comparaison de la
// seule tête ou exclusion de la tête, dédoublonnage par position, par session ou par contenu, liste remplacée
// prise pour une preuve de présence.
//
// Usage : node tests/blindage-harness/non-regression-savecontrib-annulation.mjs [app.html]   (sort 1 si un ✘)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import vm from 'node:vm';

const ICI = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(process.argv[2] || join(ICI, '..', '..', 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
// Le code sans ses commentaires : un commentaire qui nomme une garde n'en est pas une.
const code = js.replace(/\/\*[\s\S]*?\*\//g, (s) => s.replace(/[^\n]/g, ' ')).replace(/\/\/[^\n]*/g, '');

let echecs = 0;
const verifier = (libelle, ok, detail = '') => {
  console.log(`  ${ok ? '✔' : '✘'} ${libelle}${detail ? ' — ' + detail : ''}`);
  if (!ok) echecs++;
};
const existe = (source, nom) => new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\(').test(source);
function extraire(source, nom) {
  const m = new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\([^)]*\\)\\s*\\{').exec(source);
  if (!m) throw new Error('fonction introuvable dans app.html : ' + nom);
  let d = 1, i = m.index + m[0].length;
  while (i < source.length && d > 0) { const c = source[i]; if (c === '{') d++; else if (c === '}') d--; i++; }
  return source.slice(m.index, i);
}
const NOMS = ['saveContrib', 'cancelContrib', 'repositionMarker', 'startContribFromFAB', '_placeContribMarker',
  ...(existe(js, '_detacherEnvoiContrib') ? ['_detacherEnvoiContrib'] : [])];
const FONCTIONS = NOMS.map((n) => extraire(js, n));
// Déclarations de l'état d'envoi, quelle que soit la version : rejouées telles quelles.
const DECLS = [/^\s*let\s+_contribEnvoiEnVol\s*=\s*null\s*;/m, /^\s*let\s+_contribEnvoiEnCours\s*=\s*false\s*;/m,
  /^\s*const\s+CONTRIB_ENVOI_REFUS_MS\s*=\s*\d+\s*;/m, /^\s*let\s+_contribsListe\s*=\s*'[a-z]+'\s*;/m]
  .map((re) => (code.match(re) || [''])[0].trim()).filter(Boolean);

// ─── S0 — câblage, lu dans le code SANS ses commentaires ─────────────────────────────────────────
console.log('S0 — câblage dans app.html');
verifier('état d’envoi déclaré (_contribEnvoiEnVol)', /^\s*let\s+_contribEnvoiEnVol\s*=\s*null\s*;/m.test(code));
verifier('_detacherEnvoiContrib() existe', existe(code, '_detacherEnvoiContrib'));
verifier('cancelContrib() détache l’envoi', existe(code, 'cancelContrib') && /_detacherEnvoiContrib\s*\(\s*\)/.test(extraire(code, 'cancelContrib')));
verifier('startContribFromFAB() détache l’envoi en refermant', /_detacherEnvoiContrib\s*\(\s*\)/.test(extraire(code, 'startContribFromFAB')));
verifier('repositionMarker() refuse tant que l’envoi est attaché', /if\s*\(\s*_contribEnvoiEnVol\s*&&\s*!\s*_contribEnvoiEnVol\.detache\s*\)\s*return/.test(extraire(code, 'repositionMarker')));
verifier('aucun refus d’Annuler par un drapeau d’envoi', !/if\s*\(\s*_contribEnvoiEnCours\s*\)\s*return/.test(extraire(code, 'cancelContrib')));

// ─── Bac à sable ─────────────────────────────────────────────────────────────────────────────────
function monter({ elfLoadingMs = 0, sbDelayMs = 150, sbEchec = false, sbManuel = false } = {}) {
  const t0 = Date.now();
  const journal = [];
  const base = [];
  const els = {};
  const el = (id) => els[id] || (els[id] = {
    id, value: '', checked: false, disabled: false, textContent: '', innerHTML: '',
    style: { display: '' }, classList: { _c: new Set(), add(c) { this._c.add(c); }, remove(c) { this._c.delete(c); }, contains(c) { return this._c.has(c); }, toggle() {} },
    setAttribute() {},
  });
  el('c-rgpd').checked = true; el('c-val').value = '48000'; el('c-unit').value = 'nT';
  el('c-type').value = 'smartphone_mag'; el('cform').style.display = 'block';
  el('btn-save').textContent = 'Enregistrer dans Supabase';
  el('btn-reposition'); el('fab-mesure').classList.add('fab-active');
  const annuler = el('btn-cancel');
  let idLeaflet = 0;
  const marqueur = (lat, lng) => ({ _leaflet_id: ++idLeaflet, lat, getLatLng: () => ({ lat, lng }), addTo() { return this; } });
  const reponses = [];
  const ctx = {
    console, setTimeout, clearTimeout, Date, Promise, parseFloat, parseInt, Number, Math, Object, Array, JSON, String, TypeError, isNaN,
    _nativeMag: false, stopNativeMagCapture() {},
    document: { getElementById: el, querySelectorAll: () => [], querySelector: (s) => (/btn-cancel/.test(s) ? annuler : null) },
    window: { _csvStats: null, _nativeCaptureUsed: false },
    validateContrib: () => (el('c-val').value === '' ? { ok: false, msg: 'Valeur numerique requise pour cet instrument.' } : { ok: true }),
    map: {
      removeLayer(l) { if (l == null) throw new TypeError("Cannot read properties of null (reading '_leaflet_id')"); return this; },
      off() {}, once() {}, addLayer() {},
    },
    L: { marker: (ll) => marqueur(ll[0], ll[1]) },
    mkIcon: () => ({}), updateIGRFDisplay() {}, _openContribFormAfterPlacement() {},
    computeElfState: () => (Date.now() - t0 < elfLoadingMs ? 'loading' : 'ready'),
    jt: (k, fr) => '[' + k + ']' + fr,
    info: (msg, type) => journal.push({ t: Date.now() - t0, type: type || null, msg: String(msg) }),
    fetchIGRF: () => 45000, calcAll: () => ({ human: 12, water: 3 }),
    INSTRUMENT_CONSTRAINTS: {}, curKp: '2', curBz: '1', curDensity: '3', curFlux: '4',
    btTermeInclus: () => true, sessionId: 'sx_test', ctxContrib: 'exterieur',
    sbPost: async (chemin, lignes) => {
      const ligne = lignes[0];
      let issue = sbEchec ? 'echec' : 'ok';
      if (sbManuel) issue = await new Promise((r) => { reponses.push(r); });
      else await new Promise((r) => setTimeout(r, sbDelayMs));
      if (issue === 'echec') throw new Error('Failed to fetch');
      // Le serveur a validé l'INSERT, puis la connexion tombe : la ligne existe, fetch rejette.
      if (issue === 'ecrit-perdu') { base.push(ligne); throw new TypeError('Failed to fetch'); }
      // La réponse ne porte pas la ligne (scénario H3) : pas d'id à lire.
      if (issue === 'sans-ligne') { base.push(ligne); return []; }
      base.push(ligne);
      return [{ id: base.length, ...ligne }];
    },
    // Les marqueurs posés sont ENREGISTRÉS (scénario H) : l'id de chaque ligne dessinée.
    contribsDB: [], addMarker(c) { (ctx.__marqueurs = ctx.__marqueurs || []).push(c && c.id); },
    cformOverlayHide() {}, setCtx() {}, cformShowStep() {}, cformUpdateStep1NextState() {},
    // Le point d'état est ENREGISTRÉ (scénario G) : état et compte transmis.
    updateSupabaseStatusDot(e, n) { (ctx.__points = ctx.__points || []).push({ e, n }); }, updateContribSummary() {}, renderList() {},
    _armContribClick() {}, _setContribPlacementHint() {}, _scrollMapIntoViewIfMobile() {}, tog() {},
    ACTIVE: { contrib: true },
    _contribClickHandler: null, _contribAwaitingFirstPlacement: false, _pendingPrescription: null,
    pending: null,
  };
  vm.createContext(ctx);
  vm.runInContext(DECLS.join('\n') + '\n' + FONCTIONS.join('\n'), ctx);
  const original = marqueur(41.9200, 8.7400);
  ctx.pending = original;
  const lancer = () => vm.runInContext('saveContrib()', ctx);
  const appeler = (f, ...args) => vm.runInContext(f + '(' + args.map((a) => JSON.stringify(a)).join(',') + ')', ctx);
  // Remplir une nouvelle mesure comme le ferait l'utilisateur (le formulaire a pu être vidé par l'annulation).
  const remplir = (val = '48000') => { el('c-val').value = val; el('c-rgpd').checked = true; el('cform').style.display = 'block'; };
  const liberer = (i, issue = 'ok') => { if (reponses[i]) reponses[i](issue); };
  return { ctx, els, annuler, base, journal, lancer, appeler, remplir, liberer, reponses, original, t0 };
}
const attendre = (ms) => new Promise((r) => setTimeout(r, ms));
const erreurs = (j) => j.filter((e) => e.type === 'error').map((e) => e.msg);
const succes = (j) => j.filter((e) => e.type === 'success').map((e) => e.msg);
const annonce = (j, motif) => j.some((e) => e.msg.includes(motif));
const compte = (j, motif) => j.filter((e) => e.msg.includes(motif)).length;

// ─── T0 — témoin : aucun geste pendant l'enregistrement ─────────────────────────────────────────
let s = monter({});
await s.lancer();
console.log('\nT0 — témoin, aucun geste');
verifier('une ligne écrite', s.base.length === 1, `${s.base.length}`);
verifier('succès annoncé, aucune erreur', succes(s.journal).length === 1 && erreurs(s.journal).length === 0, JSON.stringify(s.journal));
verifier('formulaire refermé, bouton réactivé, « + » rendu', s.els.cform.style.display === 'none' && s.els['btn-save'].disabled === false && !s.els['fab-mesure'].classList.contains('fab-active'));
if (s.base.length !== 1) { console.error('\nTÉMOIN — le chemin nominal n’écrit pas : le bac à sable est faux.'); process.exit(2); }

// ─── A — pendant l'attente du calcul : l'enregistrement est ABANDONNÉ ───────────────────────────
for (const [id, f] of [['A1', 'cancelContrib'], ['A2', 'startContribFromFAB'], ['A3', 'repositionMarker']]) {
  s = monter({ elfLoadingMs: 600 });
  const p = s.lancer();
  await attendre(200); s.appeler(f);
  await p;
  console.log(`\n${id} — ${f}() pendant « Finalisation du calcul… »`);
  verifier('aucune ligne écrite — la mesure retirée n’est pas enregistrée', s.base.length === 0, `${s.base.length}`);
  verifier('aucune erreur, aucun succès', erreurs(s.journal).length === 0 && succes(s.journal).length === 0, JSON.stringify(s.journal));
  verifier('bouton d’enregistrement réactivé', s.els['btn-save'].disabled === false);
}
// A4 et A5 : le point est REMPLACÉ, et la saisie comme le consentement sont valides — seule la comparaison
// au point de départ peut arrêter l'écriture (un test « le point est-il nul ? » la laisserait partir).
for (const [id, retrait] of [['A4', 'cancelContrib'], ['A5', 'repositionMarker']]) {
  s = monter({ elfLoadingMs: 700 });
  const p = s.lancer();
  await attendre(150); s.appeler(retrait);
  await attendre(100); s.appeler('_placeContribMarker', 42.15, 9.10); s.remplir();
  await p;
  console.log(`\n${id} — ${retrait}() puis un NOUVEAU point, saisie remplie, pendant l’attente du calcul`);
  verifier('aucune ligne écrite — ni à l’ancienne position ni à la nouvelle', s.base.length === 0, JSON.stringify(s.base.map((r) => r.lat)));
  verifier('le nouveau point est toujours là', !!s.ctx.pending && s.ctx.pending.lat === 42.15, `${s.ctx.pending && s.ctx.pending.lat}`);
}

// ─── B — pendant l'envoi : fermer DÉTACHE l'envoi, Repositionner est refusé ─────────────────────
for (const [id, f] of [['B1', 'cancelContrib'], ['B2', 'startContribFromFAB']]) {
  s = monter({ sbManuel: true });
  const p = s.lancer();
  await attendre(50);
  const reposPendant = s.els['btn-reposition'].disabled;
  s.appeler(f);
  const apresGeste = { form: s.els.cform.style.display, pending: s.ctx.pending, btnSave: s.els['btn-save'].disabled,
    texteSave: s.els['btn-save'].textContent, repos: s.els['btn-reposition'].disabled };
  s.liberer(0, 'ok');
  await p;
  console.log(`\n${id} — ${f}() pendant l’envoi, puis l’envoi aboutit`);
  verifier('Repositionner était désactivé pendant l’envoi', reposPendant === true, `${reposPendant}`);
  verifier('le formulaire se ferme tout de suite — pas de blocage', apresGeste.form === 'none' && apresGeste.pending === null, JSON.stringify(apresGeste));
  verifier('Enregistrer est rendu au formulaire suivant dès la fermeture, avec son libellé', apresGeste.btnSave === false && apresGeste.texteSave === 'Enregistrer dans Supabase', JSON.stringify(apresGeste));
  verifier('Repositionner est rendu aussi', apresGeste.repos === false, `${apresGeste.repos}`);
  verifier('le message dit que l’envoi était parti (clé contrib_envoi_detache), pas « Mesure annulée. »', annonce(s.journal, '[contrib_envoi_detache]') && !annonce(s.journal, 'Mesure annulée'), JSON.stringify(s.journal));
  verifier('l’issue est annoncée pour ce qu’elle est (clé contrib_envoi_detache_ok)', annonce(s.journal, '[contrib_envoi_detache_ok]'), JSON.stringify(s.journal));
  verifier('une ligne écrite, aucune erreur', s.base.length === 1 && erreurs(s.journal).length === 0, JSON.stringify(erreurs(s.journal)));
}
s = monter({ sbManuel: true });
let p = s.lancer();
await attendre(50);
s.appeler('repositionMarker');
const b3 = { pendingIntact: s.ctx.pending === s.original, form: s.els.cform.style.display };
s.liberer(0, 'ok');
await p;
console.log('\nB3 — repositionMarker() pendant l’envoi');
verifier('refusé : le point est intact, le formulaire ouvert', b3.pendingIntact && b3.form === 'block', JSON.stringify(b3));
verifier('une ligne écrite, succès annoncé, aucune erreur', s.base.length === 1 && succes(s.journal).length === 1 && erreurs(s.journal).length === 0, JSON.stringify(s.journal));
verifier('Repositionner et Enregistrer réactivés après', s.els['btn-reposition'].disabled === false && s.els['btn-save'].disabled === false);

for (const [id, issue, lignes] of [['B4', 'echec', 0], ['B5', 'ecrit-perdu', 1]]) {
  s = monter({ sbManuel: true });
  p = s.lancer();
  await attendre(50); s.appeler('cancelContrib');
  s.liberer(0, issue);
  await p;
  console.log(`\n${id} — fermé pendant l’envoi, puis l’envoi est rejeté (${issue === 'echec' ? 'rien n’est écrit' : 'la ligne est écrite, la réponse se perd'})`);
  verifier(`${lignes} ligne(s) en base`, s.base.length === lignes, `${s.base.length}`);
  verifier('l’issue est dite INCONNUE (clé contrib_envoi_detache_incertain), sans « Erreur : »', annonce(s.journal, '[contrib_envoi_detache_incertain]') && erreurs(s.journal).length === 0, JSON.stringify(s.journal));
  verifier('aucun message n’affirme que la mesure n’a pas été enregistrée', !s.journal.some((e) => /n.a pas été enregistrée|has not been saved/.test(e.msg)), JSON.stringify(s.journal));
}

// ─── C — un vrai échec, envoi attaché : annoncé, formulaire ouvert, les gestes refonctionnent ────
s = monter({ sbEchec: true, sbDelayMs: 80 });
await s.lancer();
console.log('\nC — l’envoi échoue (réseau), formulaire ouvert');
verifier('aucune ligne écrite, erreur annoncée', s.base.length === 0 && erreurs(s.journal).length === 1, JSON.stringify(s.journal));
verifier('le formulaire reste ouvert, le point en place, boutons réactivés', s.els.cform.style.display === 'block' && s.ctx.pending !== null && s.els['btn-save'].disabled === false && s.els['btn-reposition'].disabled === false);
s.appeler('cancelContrib');
verifier('C2 — Annuler ensuite : point retiré, formulaire fermé, « Mesure annulée. »', s.ctx.pending === null && s.els.cform.style.display === 'none' && annonce(s.journal, 'Mesure annulée'));
s = monter({ sbEchec: true, sbDelayMs: 80 });
await s.lancer();
s.appeler('startContribFromFAB');
verifier('C3 — « + » ensuite : point retiré, formulaire fermé', s.ctx.pending === null && s.els.cform.style.display === 'none');

// ─── D — Annuler hors enregistrement : l'annulation normale reste « Mesure annulée. » ───────────
s = monter({});
await s.lancer();
s.appeler('cancelContrib');
console.log('\nD — Annuler hors enregistrement');
verifier('« Mesure annulée. », sans message d’envoi détaché', annonce(s.journal, 'Mesure annulée') && !annonce(s.journal, '[contrib_envoi_detache]'), JSON.stringify(s.journal.slice(-1)));

// ─── E — deux envois : l'ancien, détaché, ne touche pas au nouveau — ni à son SUIVI ─────────────
s = monter({ sbManuel: true });
const p1 = s.lancer();
await attendre(50); s.appeler('cancelContrib');                 // envoi 1 détaché
s.appeler('_placeContribMarker', 42.15, 9.10); s.remplir('51000');  // une nouvelle mesure
const nouveau = s.ctx.pending;
s.els['fab-mesure'].classList.add('fab-active');
const p2 = s.lancer();                                            // envoi 2, attaché
await attendre(50);
s.liberer(0, 'ok');                                               // l'ancien répond pendant le nouveau
await p1;
console.log('\nE — l’ancien envoi (détaché) répond pendant un nouvel envoi');
verifier('Enregistrer reste désactivé : le nouvel envoi est toujours en vol', s.els['btn-save'].disabled === true, `${s.els['btn-save'].disabled}`);
verifier('Repositionner reste désactivé pour le nouvel envoi', s.els['btn-reposition'].disabled === true);
verifier('le nouveau point et la nouvelle saisie sont intacts', s.ctx.pending === nouveau && s.els['c-val'].value === '51000', `${s.els['c-val'].value}`);
verifier('le « + » garde son état « en cours »', s.els['fab-mesure'].classList.contains('fab-active'));
verifier('le message parle de la mesure envoyée avant (clé contrib_envoi_detache_ok), pas du score d’une autre', annonce(s.journal, '[contrib_envoi_detache_ok]') && !succes(s.journal).some((m) => m.includes('Score')), JSON.stringify(s.journal));
// Le nouvel envoi est-il toujours SUIVI ? Fermer maintenant doit le détacher, pas l'« annuler ».
const detachesAvant = compte(s.journal, '[contrib_envoi_detache]');
s.appeler('cancelContrib');
verifier('fermer pendant le nouvel envoi le détache aussi — pas de « Mesure annulée. » avant une écriture', compte(s.journal, '[contrib_envoi_detache]') === detachesAvant + 1 && !annonce(s.journal, 'Mesure annulée'), JSON.stringify(s.journal));
s.liberer(1, 'ok');
await p2;
verifier('le nouvel envoi aboutit, détaché : deux lignes, les bonnes positions, son issue annoncée', s.base.length === 2 && s.base[0].lat === 41.92 && s.base[1].lat === 42.15 && compte(s.journal, '[contrib_envoi_detache_ok]') === 2, JSON.stringify(s.base.map((r) => r.lat)));
verifier('aucune erreur de bout en bout', erreurs(s.journal).length === 0, JSON.stringify(erreurs(s.journal)));

// ─── F — consentement et saisie relus après l'attente du calcul ─────────────────────────────────
for (const [id, geste, motif] of [['F1', (x) => { x.els['c-rgpd'].checked = false; }, /conditions de stockage/],
  ['F2', (x) => { x.els['c-val'].value = ''; }, /Valeur numerique requise/]]) {
  s = monter({ elfLoadingMs: 600 });
  p = s.lancer();
  await attendre(200); geste(s);
  await p;
  console.log(`\n${id} — ${id === 'F1' ? 'consentement décoché' : 'valeur vidée'} pendant « Finalisation du calcul… »`);
  verifier('aucune ligne écrite', s.base.length === 0, `${s.base.length}`);
  verifier('le message habituel est affiché', erreurs(s.journal).some((m) => motif.test(m)), JSON.stringify(s.journal));
}

// ─── G — un enregistrement réussi ne donne pas le total d'une liste jamais chargée (2026-09-11) ────
// Lot ant/anfr. contribsDB est vide qu'elle soit chargée vide ou jamais chargée : l'enregistrement y ajoute sa
// ligne, et le point d'état affichait « Supabase connecté · 1 contribution » comme un total. Le compte n'est
// transmis que d'une liste chargée (_contribsListe === 'ok') ; sinon null, et le point dit « connecté » seul.
for (const [id, etat, deja] of [['G1', 'attente', 0], ['G2', 'echec', 0], ['G3', 'ok', 2]]) {
  s = monter({});
  vm.runInContext(`_contribsListe = '${etat}'; for (let i = 0; i < ${deja}; i++) contribsDB.push({ id: 'd' + i });`, s.ctx);
  await s.lancer();
  const points = s.ctx.__points || [];
  const dernier = points[points.length - 1];
  console.log(`\n${id} — enregistrement réussi, liste des contributions : ${etat}${deja ? `, ${deja} déjà chargées` : ''}`);
  verifier('le point d’état passe à « connecté » — l’écriture a réussi', !!dernier && dernier.e === 'ok', JSON.stringify(dernier));
  verifier(etat === 'ok' ? `compte transmis : ${deja + 1}` : 'aucun compte transmis (null) — la liste locale n’est pas un total',
    !!dernier && dernier.n === (etat === 'ok' ? deja + 1 : null), JSON.stringify(dernier));
  const etatApres = vm.runInContext('_contribsListe', s.ctx);
  verifier('l’écriture ne change pas l’état de la liste (_contribsListe)', etatApres === etat, etatApres);
}

// ─── H — une ligne déjà relue par un rafraîchissement n'est pas ajoutée deux fois (2026-09-11, lot D2) ──
// Le serveur valide l'INSERT ; avant que sa réponse arrive, loadDB() (toutes les 5 min, ou 30 s après un échec)
// relit la table : la ligne est déjà dans contribsDB, avec son marqueur. La réponse arrive ensuite.
const avecId = (liste, id) => liste.filter((c) => c && c.id === id).length;
// Le rafraîchissement est simulé comme le fait le vrai loadDB() : il REMPLACE contribsDB par un tableau neuf, trié
// du plus récent au plus ancien. Deux positions : la ligne en tête (le cas courant) et hors de la tête (un autre
// contributeur a écrit après nous). Ne tester qu'une position laissait passer son miroir.
let marques, pointsH;
for (const [position, liste] of [
  ['en tête', "[{ id: 1, lat: 41.92, lon: 8.74 }, { id: 'autre', lat: 42.00, lon: 9.00 }, { id: 'plus-ancienne', lat: 42.10, lon: 9.10 }]"],
  ['hors de la tête', "[{ id: 'autre', lat: 42.00, lon: 9.00 }, { id: 1, lat: 41.92, lon: 8.74 }, { id: 'plus-ancienne', lat: 42.10, lon: 9.10 }]"],
]) {
  s = monter({ sbManuel: true });
  vm.runInContext("_contribsListe = 'ok'", s.ctx);
  p = s.lancer();
  await attendre(50);
  vm.runInContext('contribsDB = ' + liste, s.ctx);
  s.liberer(0, 'ok');
  await p;
  marques = s.ctx.__marqueurs || [];
  pointsH = s.ctx.__points || [];
  console.log(`\nH1 [${position}] — la liste est relue (remplacée) entre la validation de l’INSERT et sa réponse`);
  verifier('la ligne n’est présente qu’une fois dans la liste relue', avecId(s.ctx.contribsDB, 1) === 1, `${avecId(s.ctx.contribsDB, 1)} fois`);
  verifier('aucun second marqueur pour elle', marques.filter((x) => x === 1).length === 0, JSON.stringify(marques));
  verifier('le point d’état compte les lignes de la liste relue (3), sans la doubler', pointsH.length > 0 && pointsH[pointsH.length - 1].n === 3, JSON.stringify(pointsH[pointsH.length - 1]));
}

// H5 — le rafraîchissement a lu la table AVANT la validation de l'INSERT et s'applique pendant l'envoi : la liste
// relue ne contient pas la ligne, qui doit être ajoutée une fois, avec son marqueur.
s = monter({ sbManuel: true });
vm.runInContext("_contribsListe = 'ok'", s.ctx);
p = s.lancer();
await attendre(50);
vm.runInContext("contribsDB = [{ id: 'autre', lat: 42.00, lon: 9.00 }, { id: 'plus-ancienne', lat: 42.10, lon: 9.10 }]", s.ctx);
s.liberer(0, 'ok');
await p;
marques = s.ctx.__marqueurs || [];
pointsH = s.ctx.__points || [];
console.log('\nH5 — garde : la liste relue pendant l’envoi ne contient pas encore la ligne');
verifier('la ligne est ajoutée une fois, avec son marqueur', avecId(s.ctx.contribsDB, 1) === 1 && marques.filter((x) => x === 1).length === 1,
  `${avecId(s.ctx.contribsDB, 1)} / ${JSON.stringify(marques)}`);
verifier('le point d’état compte 3 lignes', pointsH.length > 0 && pointsH[pointsH.length - 1].n === 3, JSON.stringify(pointsH[pointsH.length - 1]));

s = monter({});
vm.runInContext("_contribsListe = 'ok'", s.ctx);
await s.lancer();
marques = s.ctx.__marqueurs || [];
console.log('\nH2 — témoin : aucun rafraîchissement pendant l’envoi');
verifier('la ligne est ajoutée une fois, avec son marqueur', avecId(s.ctx.contribsDB, 1) === 1 && marques.filter((x) => x === 1).length === 1,
  `${avecId(s.ctx.contribsDB, 1)} / ${JSON.stringify(marques)}`);

s = monter({ sbManuel: true });
p = s.lancer();
await attendre(50);
s.liberer(0, 'sans-ligne');
await p;
marques = s.ctx.__marqueurs || [];
console.log('\nH3 — témoin : la réponse ne porte pas la ligne (pas d’id), l’ajout se fait comme avant');
verifier('la ligne envoyée est ajoutée une fois, avec un marqueur', s.ctx.contribsDB.length === 1 && marques.length === 1,
  `${s.ctx.contribsDB.length} / ${JSON.stringify(marques)}`);

// Deux VRAIS enregistrements successifs, au même point et avec la même valeur, dont les réponses ne portent pas la
// ligne : deux lignes en base, donc deux dans la liste. Une ligne de départ fabriquée, réduite à trois champs,
// laissait passer un dédoublonnage des lignes sans id sur la session ou sur le contenu.
s = monter({ sbManuel: true });
p = s.lancer();
await attendre(50);
s.liberer(0, 'sans-ligne');
await p;
s.appeler('_placeContribMarker', 41.92, 8.74); s.remplir('48000');
p = s.lancer();
await attendre(50);
s.liberer(1, 'sans-ligne');
await p;
marques = s.ctx.__marqueurs || [];
console.log('\nH4 — garde : deux enregistrements identiques successifs, réponses sans ligne');
verifier('deux lignes en base, deux dans la liste, deux marqueurs — des lignes sans id ne sont jamais « la même »',
  s.base.length === 2 && s.ctx.contribsDB.length === 2 && marques.length === 2, `base ${s.base.length}, liste ${s.ctx.contribsDB.length}, marqueurs ${marques.length}`);

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}`);
process.exit(echecs === 0 ? 0 : 1);
