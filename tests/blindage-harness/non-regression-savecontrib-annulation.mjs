// ─── Non-régression : « Annuler » pendant l'enregistrement d'une contribution (2026-09-10) ──────────
// RÉFUTATION écrite AVANT le correctif, et exécutée contre le code d'avant pour vérifier qu'elle attrape
// le défaut qu'elle prétend attraper.
//
// LE DÉFAUT (trouvé par la revue adverse du 2026-09-10, présent depuis 3c15032, 2026-04-18)
// saveContrib() lit la position du point (`pending`), puis attend : jusqu'à 20 s que le calcul ELF soit
// prêt (« Finalisation du calcul… »), puis la réponse de l'INSERT Supabase. Pendant ces deux attentes, quatre
// chemins peuvent retirer ou remplacer `pending` : Annuler (bouton ou clic hors du formulaire, cancelContrib),
// le bouton « + » qui referme le formulaire (startContribFromFAB), « Repositionner » (repositionMarker), et
// un nouveau placement. Conséquences, avant correctif :
//   · une mesure annulée est ÉCRITE en base (l'INSERT part avec la position lue avant l'annulation) ;
//   · puis `map.removeLayer(pending)` reçoit null, Leaflet lève, et le catch affiche « Erreur : … » alors
//     que l'écriture a réussi. Un utilisateur qui relance écrit la même mesure une seconde fois.
//
// CE QUE LE CORRECTIF DOIT GARANTIR, et que ce fichier vérifie
//   · pendant l'attente du calcul, un changement de `pending` ABANDONNE l'enregistrement : rien n'est écrit ;
//   · pendant l'envoi (qu'on ne peut plus rappeler), Annuler, « + » et « Repositionner » sont REFUSÉS, et le
//     bouton Annuler est désactivé ; l'écriture aboutit et le succès est annoncé ;
//   · jamais de fausse erreur après une écriture réussie ; un vrai échec reste annoncé, formulaire ouvert.
// Contre le code d'avant le correctif, S0 et A1, A2, A3, B1, B2, B3 DOIVENT échouer.
//
// CE QUI EST SIMULÉ : le DOM (éléments qui retiennent leur état), la carte (removeLayer LÈVE sur null,
// comme Leaflet 1.9.4 : Util.stamp lit `_leaflet_id`), sbPost (délai et issue scriptés, une base en
// mémoire), computeElfState (« loading » pendant une durée scriptée), et les fonctions voisines sans effet
// sur la course. Les quatre fonctions en cause sont EXTRAITES d'app.html telles quelles.
//
// Usage : node tests/blindage-harness/non-regression-savecontrib-annulation.mjs [app.html]   (sort 1 si un ✘)

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import vm from 'node:vm';

const ICI = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(process.argv[2] || join(ICI, '..', '..', 'app.html'), 'utf8');
const js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');
const code = js.replace(/\/\*[\s\S]*?\*\//g, (s) => s.replace(/[^\n]/g, ' ')).replace(/^([ \t]*)\/\/.*$/gm, (s, i) => i);

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
const FONCTIONS = ['saveContrib', 'cancelContrib', 'repositionMarker', 'startContribFromFAB'].map(extraireFonction);

// ─── S0 — câblage ────────────────────────────────────────────────────────────────────────────────
console.log('S0 — câblage dans app.html');
const corpsDe = (f) => { const t = extraireFonction(f); return t; };
verifier('drapeau d’envoi en cours déclaré (_contribEnvoiEnCours)', /^\s*let\s+_contribEnvoiEnCours\s*=\s*false\s*;/m.test(code));
verifier('cancelContrib() refuse pendant l’envoi', /_contribEnvoiEnCours/.test(corpsDe('cancelContrib')));
verifier('repositionMarker() refuse pendant l’envoi', /_contribEnvoiEnCours/.test(corpsDe('repositionMarker')));
verifier('startContribFromFAB() refuse de refermer pendant l’envoi', /_contribEnvoiEnCours/.test(corpsDe('startContribFromFAB')));
verifier('saveContrib() ne retire plus pending sans le vérifier', !/\n\s*map\.removeLayer\(pending\);pending=null;\n/.test(corpsDe('saveContrib').split('sbPost(')[1] || ''));

// ─── Bac à sable ─────────────────────────────────────────────────────────────────────────────────
function monter({ elfLoadingMs = 0, sbDelayMs = 400, sbEchec = false } = {}) {
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
  const annuler = el('btn-cancel');
  let idLeaflet = 0;
  const marqueur = (lat, lng) => ({ _leaflet_id: ++idLeaflet, getLatLng: () => ({ lat, lng }), addTo() { return this; } });
  const ctx = {
    console, setTimeout, clearTimeout, Date, Promise, parseFloat, parseInt, Number, Math, Object, Array, JSON, String, TypeError,
    _nativeMag: false, stopNativeMagCapture() {},
    document: {
      getElementById: el,
      querySelectorAll: () => [],
      querySelector: (s) => (/btn-cancel/.test(s) ? annuler : null),
    },
    window: { _csvStats: null, _nativeCaptureUsed: false },
    validateContrib: () => ({ ok: true }),
    map: {
      // Leaflet 1.9.4 : removeLayer(null) → Util.stamp(null) lit null._leaflet_id et LÈVE.
      removeLayer(l) { if (l == null) throw new TypeError("Cannot read properties of null (reading '_leaflet_id')"); return this; },
      off() {}, once() {}, addLayer() {},
    },
    L: { marker: (ll) => marqueur(ll[0], ll[1]) },
    computeElfState: () => (Date.now() - t0 < elfLoadingMs ? 'loading' : 'ready'),
    jt: (k, fr) => fr,
    info: (msg, type) => journal.push({ t: Date.now() - t0, type: type || null, msg: String(msg) }),
    fetchIGRF: () => 45000, calcAll: () => ({ human: 12, water: 3 }),
    INSTRUMENT_CONSTRAINTS: {}, curKp: '2', curBz: '1', curDensity: '3', curFlux: '4',
    btTermeInclus: () => true, sessionId: 'sx_test', ctxContrib: 'exterieur',
    sbPost: async (chemin, lignes) => {
      await new Promise((r) => setTimeout(r, sbDelayMs));
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
  // Le drapeau, s'il existe dans app.html, est une déclaration `let` : on la rejoue telle quelle.
  const decl = code.match(/^\s*let\s+_contribEnvoiEnCours\s*=\s*false\s*;/m);
  vm.runInContext((decl ? decl[0] + '\n' : '') + FONCTIONS.join('\n'), ctx);
  ctx.pending = marqueur(41.9200, 8.7400);
  const lancer = () => vm.runInContext('saveContrib()', ctx);
  const appeler = (f) => vm.runInContext(f + '()', ctx);
  return { ctx, els, annuler, base, journal, lancer, appeler, t0 };
}
const attendre = (ms) => new Promise((r) => setTimeout(r, ms));
const erreurs = (j) => j.filter((e) => e.type === 'error').map((e) => e.msg);
const succes = (j) => j.filter((e) => e.type === 'success').map((e) => e.msg);
const annonce = (j, motif) => j.some((e) => e.msg.includes(motif));

async function scenario(titre, opts, geste) {
  const s = monter(opts);
  const p = s.lancer();
  if (geste) { await attendre(geste.a); s.annulerDesactiveAuGeste = s.annuler.disabled; s.appeler(geste.f); }
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

// ─── A — pendant l'attente du calcul : le geste ABANDONNE l'enregistrement ──────────────────────
for (const [id, f] of [['A1', 'cancelContrib'], ['A2', 'startContribFromFAB'], ['A3', 'repositionMarker']]) {
  s = await scenario(`${id} — ${f}() pendant « Finalisation du calcul… »`, { elfLoadingMs: 700, sbDelayMs: 200 }, { a: 250, f });
  verifier('aucune ligne écrite — la mesure retirée n’est pas enregistrée', s.base.length === 0, `${s.base.length}`);
  verifier('aucune erreur affichée', erreurs(s.journal).length === 0, JSON.stringify(erreurs(s.journal)));
  verifier('aucun succès annoncé', succes(s.journal).length === 0, JSON.stringify(succes(s.journal)));
  verifier('bouton d’enregistrement réactivé', s.els['btn-save'].disabled === false);
}

// ─── B — pendant l'envoi : le geste est REFUSÉ, l'écriture aboutit et se dit ────────────────────
for (const [id, f] of [['B1', 'cancelContrib'], ['B2', 'startContribFromFAB'], ['B3', 'repositionMarker']]) {
  s = await scenario(`${id} — ${f}() pendant l’envoi à Supabase`, { elfLoadingMs: 0, sbDelayMs: 500 }, { a: 150, f });
  verifier('une ligne écrite — l’envoi était parti', s.base.length === 1, `${s.base.length}`);
  verifier('aucune fausse erreur après l’écriture réussie', erreurs(s.journal).length === 0, JSON.stringify(erreurs(s.journal)));
  verifier('le succès est annoncé', succes(s.journal).length === 1, JSON.stringify(s.journal));
  verifier('le geste a été refusé — pas de « Mesure annulée. »', !annonce(s.journal, 'Mesure annulée'), JSON.stringify(s.journal));
  if (f === 'cancelContrib') {
    verifier('Annuler était désactivé pendant l’envoi', s.annulerDesactiveAuGeste === true, `${s.annulerDesactiveAuGeste}`);
    verifier('Annuler est réactivé après', s.annuler.disabled === false);
  }
}

// ─── C — un vrai échec reste annoncé, formulaire ouvert ─────────────────────────────────────────
s = await scenario('C — l’envoi échoue (réseau)', { sbEchec: true, sbDelayMs: 100 });
verifier('aucune ligne écrite', s.base.length === 0, `${s.base.length}`);
verifier('l’erreur est annoncée', erreurs(s.journal).length === 1, JSON.stringify(s.journal));
verifier('le formulaire reste ouvert, le point en place', s.els.cform.style.display === 'block' && s.ctx.pending !== null);
verifier('boutons réactivés (Enregistrer, Annuler)', s.els['btn-save'].disabled === false && s.annuler.disabled === false);

// ─── D — Annuler après la fin de l'envoi : l'annulation normale reste possible ──────────────────
s = monter({});
await s.lancer();
s.appeler('cancelContrib');
console.log('\nD — Annuler hors enregistrement (après la fin de l’envoi)');
verifier('Annuler fonctionne à nouveau (« Mesure annulée. »)', annonce(s.journal, 'Mesure annulée'), JSON.stringify(s.journal.slice(-1)));

console.log(`\n${echecs === 0 ? 'TOUT VERT' : echecs + ' ÉCHEC(S)'}`);
process.exit(echecs === 0 ? 0 : 1);
