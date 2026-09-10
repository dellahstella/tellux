// ─── Non-régression : « Annuler » pendant l'enregistrement d'une contribution (2026-09-10) ──────────
// RÉFUTATION écrite AVANT le correctif, et exécutée contre le code d'avant pour vérifier qu'elle attrape
// le défaut qu'elle prétend attraper.
//
// LE DÉFAUT (trouvé par la revue adverse du 2026-09-10, présent depuis 3c15032, 2026-04-18)
// saveContrib() lit la position du point (`pending`), puis attend : jusqu'à 20 s que le calcul ELF soit
// prêt (« Finalisation du calcul… »), puis la réponse de l'INSERT Supabase. Pendant ces deux attentes, des
// gestes peuvent retirer ou remplacer `pending` : Annuler (bouton ou clic hors du formulaire, cancelContrib),
// le bouton « + » qui referme le formulaire (startContribFromFAB), « Repositionner » (repositionMarker), et
// — après une annulation — un nouveau point (_placeContribMarker). Conséquences, avant correctif :
//   · une mesure annulée est ÉCRITE en base (l'INSERT part avec la position lue avant l'annulation) ;
//   · puis `map.removeLayer(pending)` reçoit null, Leaflet lève, et le catch affiche « Erreur : … » alors
//     que l'écriture a réussi. Un utilisateur qui relance écrit la même mesure une seconde fois.
//
// SUITE DE LA REVUE ADVERSE (2026-09-10) — le premier correctif refusait Annuler pendant l'envoi SANS
// BORNE : sbPost n'a pas de délai, un envoi sans réponse enfermait l'utilisateur. Et seul le point était figé
// au clic : décocher le consentement pendant l'attente n'empêchait pas l'écriture. Ce fichier vérifie donc
// aussi : le refus est borné (E1), une réponse tardive n'efface ni un nouveau point ni une nouvelle saisie
// (E2), le consentement et la saisie sont relus après l'attente (F1, F2), le drapeau retombe après un échec
// (C2, C3), un point REMPLACÉ (pas seulement retiré) abandonne l'enregistrement (A4), et le refus des gestes
// est constaté sur l'état (point, formulaire, boutons), pas sur un message.
//
// CE QUE LE CORRECTIF DOIT GARANTIR
//   · pendant l'attente du calcul, un point retiré ou remplacé, un consentement retiré ou une saisie
//     invalidée ABANDONNENT l'enregistrement : rien n'est écrit ;
//   · pendant l'envoi, Annuler, « + » et « Repositionner » sont refusés, et Annuler comme Repositionner sont
//     désactivés — pendant CONTRIB_ENVOI_REFUS_MS au plus ; au-delà, les gestes redeviennent possibles avec un
//     avertissement, et Enregistrer reste désactivé jusqu'à la réponse ;
//   · jamais de fausse erreur après une écriture réussie ; un vrai échec reste annoncé, formulaire ouvert.
// Contre origin/main d'avant le correctif, S0, A1-A4, B1-B3, E1, E2, F1 et F2 DOIVENT échouer.
//
// CE QUI EST SIMULÉ : le DOM (éléments qui retiennent leur état), la carte (removeLayer LÈVE sur null,
// comme Leaflet 1.9.4 : Util.stamp lit `_leaflet_id`), sbPost (délai et issue scriptés, une base en
// mémoire, ou une réponse que le scénario libère lui-même), computeElfState (« loading » pendant une durée
// scriptée), validateContrib (valeur vide = invalide), jt() (rend sa clé devant le texte), et les fonctions
// voisines sans effet sur la course. CONTRIB_ENVOI_REFUS_MS est lu dans app.html puis COMPRESSÉ à 300 ms,
// comme on compresse le temps ailleurs. Les cinq fonctions en cause sont EXTRAITES d'app.html telles quelles.
//
// Usage : node tests/blindage-harness/non-regression-savecontrib-annulation.mjs [app.html]   (sort 1 si un ✘)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import vm from 'node:vm';

const ICI = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(process.argv[2] || join(ICI, '..', '..', 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
// Le code sans ses commentaires : un commentaire qui nomme le drapeau n'est pas une garde.
const code = js.replace(/\/\*[\s\S]*?\*\//g, (s) => s.replace(/[^\n]/g, ' ')).replace(/\/\/[^\n]*/g, '');

let echecs = 0;
const verifier = (libelle, ok, detail = '') => {
  console.log(`  ${ok ? '✔' : '✘'} ${libelle}${detail ? ' — ' + detail : ''}`);
  if (!ok) echecs++;
};
function extraire(source, nom) {
  const m = new RegExp('(?:async\\s+)?function\\s+' + nom + '\\s*\\([^)]*\\)\\s*\\{').exec(source);
  if (!m) throw new Error('fonction introuvable dans app.html : ' + nom);
  let d = 1, i = m.index + m[0].length;
  while (i < source.length && d > 0) { const c = source[i]; if (c === '{') d++; else if (c === '}') d--; i++; }
  return source.slice(m.index, i);
}
const NOMS = ['saveContrib', 'cancelContrib', 'repositionMarker', 'startContribFromFAB', '_placeContribMarker'];
const FONCTIONS = NOMS.map((n) => extraire(js, n));
const REFUS_MS_TEST = 300;

// ─── S0 — câblage, lu dans le code SANS ses commentaires ─────────────────────────────────────────
console.log('S0 — câblage dans app.html');
const declDrapeau = code.match(/^\s*let\s+_contribEnvoiEnCours\s*=\s*false\s*;/m);
const declBorne = code.match(/^\s*const\s+CONTRIB_ENVOI_REFUS_MS\s*=\s*(\d+)\s*;/m);
verifier('drapeau d’envoi en cours déclaré (_contribEnvoiEnCours)', !!declDrapeau);
verifier('borne du refus déclarée (CONTRIB_ENVOI_REFUS_MS)', !!declBorne, declBorne ? declBorne[1] + ' ms' : '');
for (const f of ['cancelContrib', 'repositionMarker', 'startContribFromFAB']) {
  verifier(`${f}() refuse pendant l’envoi — garde dans le code, pas dans un commentaire`, /if\s*\(\s*_contribEnvoiEnCours\s*\)\s*return/.test(extraire(code, f)));
}
const apresEnvoi = extraire(code, 'saveContrib').split('sbPost(')[1] || '';
verifier('saveContrib() ne retire plus pending sans le vérifier', !/\n\s*map\.removeLayer\(pending\);pending=null;/.test(apresEnvoi.replace(/if\s*\(\s*pending[^)]*\)\s*\{\s*\n?\s*map\.removeLayer\(pending\);pending=null;/g, '')));
verifier('saveContrib() arme un minuteur borné par CONTRIB_ENVOI_REFUS_MS', /setTimeout\([\s\S]*?CONTRIB_ENVOI_REFUS_MS\s*\)/.test(extraire(code, 'saveContrib')));

// ─── Bac à sable ─────────────────────────────────────────────────────────────────────────────────
function monter({ elfLoadingMs = 0, sbDelayMs = 400, sbEchec = false, sbManuel = false } = {}) {
  const t0 = Date.now();
  const journal = [];
  const base = [];
  const els = {};
  const el = (id) => els[id] || (els[id] = {
    id, value: '', checked: false, disabled: false, textContent: '', innerHTML: '',
    style: { display: '' }, classList: { add() {}, remove() {}, toggle() {} }, setAttribute() {},
  });
  el('c-rgpd').checked = true; el('c-val').value = '48000'; el('c-unit').value = 'nT';
  el('c-type').value = 'smartphone_mag'; el('cform').style.display = 'block';
  el('btn-save').textContent = 'Enregistrer dans Supabase';
  el('btn-reposition');   // créé d'avance : l'état « désactivé » se lit même si le code ne l'a pas encore touché
  const annuler = el('btn-cancel');
  let idLeaflet = 0;
  const marqueur = (lat, lng) => ({ _leaflet_id: ++idLeaflet, lat, getLatLng: () => ({ lat, lng }), addTo() { return this; } });
  const reponse = {};
  const ctx = {
    console, setTimeout, clearTimeout, Date, Promise, parseFloat, parseInt, Number, Math, Object, Array, JSON, String, TypeError, isNaN,
    _nativeMag: false, stopNativeMagCapture() {},
    document: {
      getElementById: el,
      querySelectorAll: () => [],
      querySelector: (s) => (/btn-cancel/.test(s) ? annuler : null),
    },
    window: { _csvStats: null, _nativeCaptureUsed: false },
    validateContrib: () => (el('c-val').value === '' ? { ok: false, msg: 'Valeur numerique requise pour cet instrument.' } : { ok: true }),
    map: {
      // Leaflet 1.9.4 : removeLayer(null) → Util.stamp(null) lit null._leaflet_id et LÈVE.
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
      if (sbManuel) {
        // Réponse libérée par le scénario lui-même : l'envoi reste « en vol » aussi longtemps qu'il le faut.
        await new Promise((r) => { reponse.liberer = r; });
      } else {
        await new Promise((r) => setTimeout(r, sbDelayMs));
      }
      if (sbEchec) throw new Error('Failed to fetch');
      base.push(lignes[0]);
      return [{ id: base.length, ...lignes[0] }];
    },
    contribsDB: [], addMarker() {},
    cformOverlayHide() {}, setCtx() {}, cformShowStep() {}, cformUpdateStep1NextState() {},
    updateSupabaseStatusDot() {}, updateContribSummary() {}, renderList() {},
    _armContribClick() {}, _setContribPlacementHint() {}, _scrollMapIntoViewIfMobile() {}, tog() {},
    ACTIVE: { contrib: true },
    _contribClickHandler: null, _contribAwaitingFirstPlacement: false, _pendingPrescription: null,
    pending: null,
  };
  vm.createContext(ctx);
  // Déclarations d'app.html rejouées telles quelles — la borne est compressée à REFUS_MS_TEST.
  const decls = (declDrapeau ? declDrapeau[0].trim() + '\n' : '')
    + (declBorne ? declBorne[0].trim().replace(/=\s*\d+/, '=' + REFUS_MS_TEST) + '\n' : '');
  vm.runInContext(decls + FONCTIONS.join('\n'), ctx);
  const original = marqueur(41.9200, 8.7400);
  ctx.pending = original;
  const lancer = () => vm.runInContext('saveContrib()', ctx);
  const appeler = (f, ...args) => vm.runInContext(f + '(' + args.map((a) => JSON.stringify(a)).join(',') + ')', ctx);
  const drapeau = () => { try { return vm.runInContext('_contribEnvoiEnCours', ctx); } catch { return undefined; } };
  return { ctx, els, annuler, base, journal, lancer, appeler, drapeau, original, reponse, t0 };
}
const attendre = (ms) => new Promise((r) => setTimeout(r, ms));
const erreurs = (j) => j.filter((e) => e.type === 'error').map((e) => e.msg);
const succes = (j) => j.filter((e) => e.type === 'success').map((e) => e.msg);
const annonce = (j, motif) => j.some((e) => e.msg.includes(motif));

// Un geste au temps `a`, avec l'état constaté JUSTE après lui.
async function scenario(titre, opts, geste) {
  const s = monter(opts);
  const p = s.lancer();
  if (geste) {
    await attendre(geste.a);
    s.avantGeste = { annuler: s.annuler.disabled, repos: s.els['btn-reposition'].disabled };
    s.appeler(geste.f);
    s.apresGeste = { pendingIntact: s.ctx.pending === s.original, formOuvert: s.els.cform.style.display === 'block' };
  }
  await p;
  console.log(`\n${titre}`);
  return s;
}

// ─── T0 — témoin : aucun geste pendant l'enregistrement ─────────────────────────────────────────
let s = await scenario('T0 — témoin, aucun geste', {});
verifier('une ligne écrite', s.base.length === 1, `${s.base.length}`);
verifier('succès annoncé, aucune erreur', succes(s.journal).length === 1 && erreurs(s.journal).length === 0, JSON.stringify(s.journal));
verifier('formulaire refermé, bouton réactivé', s.els.cform.style.display === 'none' && s.els['btn-save'].disabled === false);
if (s.base.length !== 1) { console.error('\nTÉMOIN — le chemin nominal n’écrit pas : le bac à sable est faux.'); process.exit(2); }

// ─── A — pendant l'attente du calcul : le point retiré ou remplacé ABANDONNE l'enregistrement ────
for (const [id, f] of [['A1', 'cancelContrib'], ['A2', 'startContribFromFAB'], ['A3', 'repositionMarker']]) {
  s = await scenario(`${id} — ${f}() pendant « Finalisation du calcul… »`, { elfLoadingMs: 700, sbDelayMs: 200 }, { a: 250, f });
  verifier('aucune ligne écrite — la mesure retirée n’est pas enregistrée', s.base.length === 0, `${s.base.length}`);
  verifier('aucune erreur affichée', erreurs(s.journal).length === 0, JSON.stringify(erreurs(s.journal)));
  verifier('aucun succès annoncé', succes(s.journal).length === 0, JSON.stringify(succes(s.journal)));
  verifier('bouton d’enregistrement réactivé', s.els['btn-save'].disabled === false);
}
s = monter({ elfLoadingMs: 700, sbDelayMs: 200 });
let p = s.lancer();
await attendre(150); s.appeler('cancelContrib');
await attendre(150); s.appeler('_placeContribMarker', 42.15, 9.10);   // un NOUVEAU point, non nul
await p;
console.log('\nA4 — annulé, puis un nouveau point posé pendant l’attente du calcul');
verifier('aucune ligne écrite — ni à l’ancienne position ni à la nouvelle', s.base.length === 0, JSON.stringify(s.base.map((r) => r.lat)));
verifier('le nouveau point est toujours là', !!s.ctx.pending && s.ctx.pending.lat === 42.15, `${s.ctx.pending && s.ctx.pending.lat}`);

// ─── B — pendant l'envoi : le geste est REFUSÉ, constaté sur l'état ─────────────────────────────
for (const [id, f] of [['B1', 'cancelContrib'], ['B2', 'startContribFromFAB'], ['B3', 'repositionMarker']]) {
  s = await scenario(`${id} — ${f}() pendant l’envoi à Supabase`, { elfLoadingMs: 0, sbDelayMs: 250 }, { a: 100, f });
  verifier('au geste : le point est intact et le formulaire ouvert — le geste est refusé', s.apresGeste.pendingIntact && s.apresGeste.formOuvert, JSON.stringify(s.apresGeste));
  verifier('Annuler et Repositionner étaient désactivés pendant l’envoi', s.avantGeste.annuler === true && s.avantGeste.repos === true, JSON.stringify(s.avantGeste));
  verifier('une ligne écrite — l’envoi était parti', s.base.length === 1, `${s.base.length}`);
  verifier('aucune fausse erreur après l’écriture réussie', erreurs(s.journal).length === 0, JSON.stringify(erreurs(s.journal)));
  verifier('le succès est annoncé', succes(s.journal).length === 1, JSON.stringify(s.journal));
  verifier('Annuler et Repositionner réactivés après', s.annuler.disabled === false && s.els['btn-reposition'].disabled === false);
}

// ─── C — un vrai échec reste annoncé ; le drapeau retombe, les gestes refonctionnent ────────────
s = await scenario('C — l’envoi échoue (réseau)', { sbEchec: true, sbDelayMs: 100 });
verifier('aucune ligne écrite', s.base.length === 0, `${s.base.length}`);
verifier('l’erreur est annoncée', erreurs(s.journal).length === 1, JSON.stringify(s.journal));
verifier('le formulaire reste ouvert, le point en place', s.els.cform.style.display === 'block' && s.ctx.pending !== null);
verifier('boutons réactivés (Enregistrer, Annuler)', s.els['btn-save'].disabled === false && s.annuler.disabled === false);
s.appeler('cancelContrib');
console.log('\nC2 — après l’échec, Annuler');
verifier('Annuler fonctionne : point retiré, formulaire fermé, « Mesure annulée. »', s.ctx.pending === null && s.els.cform.style.display === 'none' && annonce(s.journal, 'Mesure annulée'));
s = await scenario('C3 — après l’échec, le bouton « + » referme', { sbEchec: true, sbDelayMs: 100 });
s.appeler('startContribFromFAB');
verifier('« + » referme : point retiré, formulaire fermé', s.ctx.pending === null && s.els.cform.style.display === 'none');

// ─── D — Annuler après la fin de l'envoi : l'annulation normale reste possible ──────────────────
s = monter({});
await s.lancer();
s.appeler('cancelContrib');
console.log('\nD — Annuler hors enregistrement (après la fin de l’envoi)');
verifier('Annuler fonctionne à nouveau (« Mesure annulée. »)', annonce(s.journal, 'Mesure annulée'), JSON.stringify(s.journal.slice(-1)));

// ─── E — le refus est BORNÉ ; une réponse tardive n'efface rien de ce qui a suivi ───────────────
s = monter({ sbManuel: true });
p = s.lancer();
await attendre(REFUS_MS_TEST + 200);
console.log(`\nE1 — l’envoi ne répond pas : au-delà de la borne (${REFUS_MS_TEST} ms en test)`);
verifier('le drapeau est retombé', s.drapeau() === false, `${s.drapeau()}`);
verifier('Annuler et Repositionner sont réactivés', s.annuler.disabled === false && s.els['btn-reposition'].disabled === false);
verifier('l’avertissement est affiché (clé save_envoi_sans_reponse)', annonce(s.journal, '[save_envoi_sans_reponse]'), JSON.stringify(s.journal));
verifier('Enregistrer reste désactivé — pas de second envoi pendant l’incertitude', s.els['btn-save'].disabled === true);
s.appeler('cancelContrib');
verifier('Annuler fonctionne : formulaire fermé, « Mesure annulée. »', s.els.cform.style.display === 'none' && annonce(s.journal, 'Mesure annulée'));
if (s.reponse.liberer) s.reponse.liberer();
await p;
verifier('la réponse tardive arrive : une ligne écrite, succès annoncé, aucune erreur', s.base.length === 1 && succes(s.journal).length === 1 && erreurs(s.journal).length === 0, JSON.stringify(s.journal));

s = monter({ sbManuel: true });
p = s.lancer();
await attendre(REFUS_MS_TEST + 200);
s.appeler('cancelContrib');
s.appeler('_placeContribMarker', 42.15, 9.10);   // l'utilisateur passe à une autre mesure
s.els['c-val'].value = '51000';
if (s.reponse.liberer) s.reponse.liberer();
await p;
console.log('\nE2 — réponse tardive, alors qu’une autre mesure est commencée');
verifier('le nouveau point est toujours là', !!s.ctx.pending && s.ctx.pending.lat === 42.15, `${s.ctx.pending && s.ctx.pending.lat}`);
verifier('la nouvelle saisie n’est pas effacée', s.els['c-val'].value === '51000', `« ${s.els['c-val'].value} »`);
verifier('la ligne écrite est celle de la première mesure', s.base.length === 1 && s.base[0].lat === 41.92, JSON.stringify(s.base.map((r) => r.lat)));
verifier('aucune erreur', erreurs(s.journal).length === 0, JSON.stringify(erreurs(s.journal)));

// ─── F — consentement et saisie relus après l'attente du calcul ─────────────────────────────────
s = monter({ elfLoadingMs: 700, sbDelayMs: 100 });
p = s.lancer();
await attendre(250); s.els['c-rgpd'].checked = false;
await p;
console.log('\nF1 — consentement décoché pendant « Finalisation du calcul… »');
verifier('aucune ligne écrite — pas d’écriture contre un consentement retiré', s.base.length === 0, `${s.base.length}`);
verifier('le message de consentement est affiché', erreurs(s.journal).some((m) => /conditions de stockage/.test(m)), JSON.stringify(s.journal));
verifier('bouton d’enregistrement réactivé', s.els['btn-save'].disabled === false);

s = monter({ elfLoadingMs: 700, sbDelayMs: 100 });
p = s.lancer();
await attendre(250); s.els['c-val'].value = '';
await p;
console.log('\nF2 — valeur vidée pendant « Finalisation du calcul… »');
verifier('aucune ligne écrite — pas de ligne sans valeur', s.base.length === 0, `${s.base.length}`);
verifier('le message de validation est affiché', erreurs(s.journal).some((m) => /Valeur numerique requise/.test(m)), JSON.stringify(s.journal));

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}`);
process.exit(echecs === 0 ? 0 : 1);
