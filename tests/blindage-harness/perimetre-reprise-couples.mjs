// ─── Extension par COUPLE de perimetre-reprise.mjs ──────────────────────────────────────
// perimetre-reprise.mjs répond « combien de FONCTIONS restent captives ». Cette question
// n'est pas celle qui gouverne l'adoption : une même fonction peut toucher plusieurs
// ressources distinctes (captive sur l'une, couverte sur l'autre n'est pas possible pour une
// fonction déjà couverte — mais NON captive au sens strict, deux ressources comptent double
// dans le travail restant) ; une même ressource peut avoir un consommateur couvert et un
// autre qui l'appelle en direct, hors de l'assistant. Ce script énumère par COUPLE
// (ressource, consommateur), pas par fonction — définition établie au brief du 2026-09-14,
// cf. INS-022 (`REGISTRE_INSTRUMENTS.md`, dépôt privé).
//
// Usage :  node perimetre-reprise-couples.mjs [chemin/app.html]     (défaut : ../../app.html)
// Sort 0 quoi qu'il trouve — instrument de mesure, pas garde de CI, comme son parent.
//
// ─── CE QUE CE SCRIPT RÉUTILISE, SANS LE MODIFIER ───────────────────────────────────────
// Même parsing (extraction des <script> inline, neutralisation commentaires/chaînes,
// rattrapage des attributs gestionnaires on…="…"), même graphe d'appels syntaxique, mêmes
// biais résiduels déclarés dans perimetre-reprise.mjs — non redupliqués ici, lire l'en-tête
// de ce fichier avant de douter d'un chiffre. Ce script AJOUTE une couche : pour chaque
// fonction captive (au sens du parent), il détaille SES ressources directes (fetch/XHR/
// sendBeacon trouvés dans son propre corps) et SES appels vers d'AUTRES fonctions réseau
// (1 niveau de transitivité, suffisant à date — aucune chaîne rencontrée n'en a exigé deux).
//
// ─── BIAIS PROPRE À CETTE COUCHE, absent du parent ──────────────────────────────────────
// Le graphe d'appels est syntaxique : il voit qu'une fonction A appelle une fonction B, mais
// PAS avec quelle valeur d'argument, ni si cette valeur atteint réellement une branche
// réseau à l'intérieur de B. Sens du biais : SUR-ESTIME le travail restant — une attribution
// réseau peut être mécaniquement réelle (l'appel a lieu) sans jamais s'exécuter en pratique.
//
// Cas concret trouvé et vérifié À LA MAIN le 2026-09-14 (app.html @ cdbdc97) : `tog(id,cls,
// btn)` est un aiguilleur de couche dont ~12 branches testent `id===<littéral>`. Cinq
// fonctions doivent 100 % de leur attribution réseau à un appel `tog('contrib', …)` — via
// `startContribFromFAB`, direct ou à 2 niveaux (`startCrustalCorseMeasurement`,
// `startFromPrescription`). Aucune branche de `tog` ne teste `id==='contrib'` pour lancer un
// chargement : cette branche affiche un toast sur un état déjà connu (`_contribsListe`), rien
// de plus. Les 5 sont donc FAUX CAPTIFS — vérifié en lisant `tog()` en entier, pas en grepant.
//
// CE SCRIPT NE CORRIGE PAS CE BIAIS EN GÉNÉRAL — il n'existe pas de détection mécanique
// fiable d'un aiguilleur argument-dépendant sans risquer un nouveau défaut dans l'instrument
// lui-même (règle du dépôt : chaque défaut d'un instrument se trouve en le RELANÇANT, pas en
// l'anticipant par une regex de plus). Il se contente de VÉRIFIER MÉCANIQUEMENT si les 5 noms
// connus sont toujours dans la sortie, et de le dire — même patron que les « mécanismes
// reconnus » imprimés avant le chiffre dans perimetre-reprise.mjs : le doute voyage avec la
// mesure au lieu de rester dans un commentaire que le lecteur du chiffre n'ouvrira pas.
//
// Ce qui SIGNALERAIT qu'il en existe un 6e (ou un nouveau) : n'importe quel captif dont TOUTE
// l'attribution réseau, directe et transitive, passe par un seul et même intermédiaire —
// c'est le patron à chercher à la main si la liste SUSPECTS_CONNUS ci-dessous cesse de
// couvrir ce que la sortie rapporte.
//
// ─── SECOND BIAIS, DE SENS OPPOSÉ : LA TRANSITIVITÉ S'ARRÊTE À 1 NIVEAU ─────────────────
// Volontaire, pas un oubli : approfondir sans borne fait exploser le compte des 5 SUSPECTS
// ci-dessus (leur unique intermédiaire, `tog`, appelle lui-même ~8 chargeurs — les compter
// à un 2e niveau ferait passer un faux captif de 1 ressource fictive à 8). Aucune profondeur
// fixe ne sert les deux cas à la fois : 1 niveau est le choix qui NE ment PAS par excès sur
// les 5 déjà identifiés comme faux. Conséquence assumée, sens du biais : SOUS-ESTIME dans le
// cas inverse — un intermédiaire à 1 niveau qui touche LUI-MÊME plusieurs ressources n'est
// compté qu'une fois. Cas trouvé et corrigé À LA MAIN le 2026-09-14 : `myPlaceAnalyze` (lue
// en entier) appelle `reverseGeocodeCommune` ET `fetchAltitudeIGN`, deux ressources externes
// distinctes (API Adresse reverse, IGN Géoplateforme) — ce script ne rapporte qu'« 1 via
// myPlaceAnalyze » pour `myPlaceRequestGeolocation`/`myPlaceSearchAddress`, sous-comptant
// chacune de 1. Voir SOUS_COMPTES_CONNUS ci-dessous — même traitement que les suspects :
// déclaré et vérifié mécaniquement présent, jamais corrigé en silence dans le chiffre.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const CIBLE = process.argv[2] || join(ICI, '..', '..', 'app.html');

const html = readFileSync(CIBLE, 'utf8');
let js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');

js = js.replace(/\/\*[\s\S]*?\*\//g, (s) => s.replace(/[^\n]/g, ' '))
       .replace(/^([ \t]*)\/\/.*$/gm, (s, i) => i);

const videChaines = (s) => s.replace(/'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*"/g,
  (x) => x[0] + x.slice(1, -1).replace(/[^\n]/g, ' ') + x[0]);
const gestionnairesDe = (s) => [...s.matchAll(/\bon[a-z]+\s*=\s*(?:"([^"]*)|'([^']*))/gi)]
  .map((x) => x[1] ?? x[2] ?? '').join('\n');

const fns = new Map();
const decl = /(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(([^)]*)\)\s*\{/g;
let m;
while ((m = decl.exec(js))) {
  let d = 1, i = decl.lastIndex;
  while (i < js.length && d > 0) { const c = js[i]; if (c === '{') d++; else if (c === '}') d--; i++; }
  const brut = js.slice(decl.lastIndex, i - 1);
  fns.set(m[1], { args: m[2].trim(), corpsBrut: brut, corps: videChaines(brut) + '\n' + gestionnairesDe(brut) });
}
const noms = [...fns.keys()];
const appels = (n) => noms.filter((c) => c !== n &&
  new RegExp('\\b' + c.replace(/\$/g, '\\$') + '\\s*\\(').test(fns.get(n).corps));

const PRIM = /\bfetch\s*\(|XMLHttpRequest|navigator\.sendBeacon/;
const reseau = new Set(noms.filter((n) => PRIM.test(fns.get(n).corps)));
for (let chg = true; chg;) {
  chg = false;
  for (const n of noms) if (!reseau.has(n) && appels(n).some((c) => reseau.has(c))) { reseau.add(n); chg = true; }
}

const MECANISMES = [
  { trouve: (src) => [...src.matchAll(/setInterval\s*\(\s*([A-Za-z_$][\w$]*)\s*[,)]/g)].map((x) => x[1]) },
  { trouve: (src) => { const out = []; for (const mm of src.matchAll(/setInterval\s*\(\s*(?:async\s*)?\(\s*\)\s*=>\s*\{([\s\S]{0,400}?)\}/g)) for (const c of noms) if (new RegExp('\\b' + c + '\\s*\\(').test(mm[1])) out.push(c); return out; } },
  // Biais trouvé et corrigé le 2026-09-15 (brief S2 lot 2), même correctif que
  // perimetre-reprise.mjs (dupliqué ici, cf. en-tête « réutilise sans modifier ») : le 2e
  // argument d'enregistrerReprise n'est pas toujours un identifiant nu — le ternaire de la
  // clé 'bt' (PR #1458, agrégat BT) faisait disparaître 'bt' des mécanismes reconnus.
  { trouve: (src) => {
      const identifiantNu = [...src.matchAll(/enregistrerReprise\s*\(\s*['"][^'"]*['"]\s*,\s*([A-Za-z_$][\w$]*)\s*[,)]/g)].map((x) => x[1]);
      const ternaireTypeof = [...src.matchAll(/enregistrerReprise\s*\(\s*['"][^'"]*['"]\s*,\s*typeof\s+[A-Za-z_$][\w$]*\s*===\s*['"]function['"]\s*\?\s*([A-Za-z_$][\w$]*)\s*:\s*([A-Za-z_$][\w$]*)\s*[,)]/g)]
        .flatMap((x) => [x[1], x[2]]);
      return identifiantNu.concat(ternaireTypeof);
    } },
];
const racines = new Set();
for (const meca of MECANISMES) for (const n of new Set(meca.trouve(js))) racines.add(n);
const couvert = new Set();
const pile = [...racines];
while (pile.length) { const n = pile.pop(); if (couvert.has(n)) continue; couvert.add(n); if (fns.has(n)) for (const c of appels(n)) pile.push(c); }

const lecteurs = noms.filter((n) => reseau.has(n));
const sansArg = lecteurs.filter((n) => fns.get(n).args === '');
const captifs = sansArg.filter((n) => !couvert.has(n));

function ressourcesDirectes(nom) {
  const corpsBrut = fns.get(nom).corpsBrut;
  const out = [];
  for (const mm of corpsBrut.matchAll(/fetch\s*\(\s*([^,)]+)/g)) out.push({ type: 'fetch', arg: mm[1].trim().slice(0, 90) });
  for (const mm of corpsBrut.matchAll(/new\s+XMLHttpRequest/g)) out.push({ type: 'XMLHttpRequest', arg: '(voir .open() plus loin dans le corps)' });
  for (const mm of corpsBrut.matchAll(/navigator\.sendBeacon\s*\(\s*([^,)]+)/g)) out.push({ type: 'sendBeacon', arg: mm[1].trim().slice(0, 90) });
  return out;
}
function intermediairesReseau(nom) {
  return appels(nom).filter((c) => reseau.has(c));
}

// Noms dont TOUTE l'attribution réseau a été vérifiée FAUSSE à la main le 2026-09-14 (chaîne
// tog('contrib', …), cf. en-tête). Vérité mécanique de la présence, pas du jugement : ce
// script constate qu'ils sont toujours rapportés, il ne les retranche pas de la liste
// ci-dessus — au lecteur de refaire la vérification si le contexte a changé.
const SUSPECTS_CONNUS = {
  startContribFromFAB: "tog('contrib',…) — id==='contrib' n'affiche qu'un toast, aucune branche réseau",
  chooseContribLevelN0: "hérite de startContribFromFAB, même chaîne",
  contribFabAction: "hérite de startContribFromFAB, même chaîne",
  buildCrustalLayer: "via startCrustalCorseMeasurement → startContribFromFAB, même chaîne à 2 niveaux",
  openPrescription: "via startFromPrescription → startContribFromFAB, même chaîne à 2 niveaux",
};

// Symétrique de SUSPECTS_CONNUS pour le biais inverse (sous-comptage, cf. en-tête) : un
// intermédiaire à 1 niveau qui touche lui-même 2+ ressources n'est compté qu'une fois ici.
const SOUS_COMPTES_CONNUS = {
  myPlaceRequestGeolocation: "via myPlaceAnalyze, qui touche 2 ressources (reverseGeocodeCommune + fetchAltitudeIGN) — +1 réel",
  myPlaceSearchAddress: "idem myPlaceAnalyze — +1 réel, en plus de son fetch direct déjà compté",
};

console.log(`cible : ${CIBLE}\n`);
console.log(`CAPTIFS (fonction, hérité de perimetre-reprise.mjs) : ${captifs.length}\n`);

let totalCouples = 0;
const ressourcesVues = new Set();
for (const n of captifs) {
  const directes = ressourcesDirectes(n);
  const inter = intermediairesReseau(n);
  console.log(`### ${n}${SUSPECTS_CONNUS[n] ? '  ⚠ SUSPECT CONNU (sur-compte)' : ''}${SOUS_COMPTES_CONNUS[n] ? '  ⚠ SOUS-COMPTE CONNU' : ''}`);
  if (SUSPECTS_CONNUS[n]) console.log(`  ⚠ ${SUSPECTS_CONNUS[n]} — à revérifier à la main avant de compter, PAS retranché ici`);
  if (SOUS_COMPTES_CONNUS[n]) console.log(`  ⚠ ${SOUS_COMPTES_CONNUS[n]} — PAS ajouté ici, seulement signalé`);
  console.log(`  accès réseau DIRECTS dans le corps : ${directes.length}`);
  directes.forEach((d) => { console.log(`    - ${d.type} : ${d.arg}`); ressourcesVues.add(d.arg); });
  console.log(`  appelle d'AUTRES fonctions réseau (transitif, 1 niveau) : ${inter.length ? inter.join(', ') : '(aucune)'}`);
  inter.forEach((c) => ressourcesVues.add('via:' + c));
  const nbCouples = directes.length + inter.length;
  totalCouples += nbCouples;
  console.log(`  => couples (ressource, ${n}) identifiés mécaniquement : ${nbCouples}`);
  console.log('');
}

console.log('─'.repeat(78));
console.log(`Total couples (mécanique, brut, AVANT toute correction déclarée) : ${totalCouples}`);

const suspectsPresents = captifs.filter((n) => SUSPECTS_CONNUS[n]);
console.log(`Suspects connus (sur-compte) toujours présents : ${suspectsPresents.length} / ${Object.keys(SUSPECTS_CONNUS).length} attendus`);
const disparusSuspects = Object.keys(SUSPECTS_CONNUS).filter((n) => !captifs.includes(n));
if (disparusSuspects.length) console.log(`  ABSENTS de cette exécution (adoptés, renommés, ou retirés — à re-vérifier si inattendu) : ${disparusSuspects.join(', ')}`);

const sousComptesPresents = captifs.filter((n) => SOUS_COMPTES_CONNUS[n]);
console.log(`Sous-comptes connus toujours présents : ${sousComptesPresents.length} / ${Object.keys(SOUS_COMPTES_CONNUS).length} attendus`);
const disparusSousComptes = Object.keys(SOUS_COMPTES_CONNUS).filter((n) => !captifs.includes(n));
if (disparusSousComptes.length) console.log(`  ABSENTS de cette exécution — à re-vérifier si inattendu : ${disparusSousComptes.join(', ')}`);

// Compte corrigé = brut, moins 1 couple par suspect connu présent (leur unique attribution
// est fausse), plus 1 par sous-compte connu présent (leur intermédiaire touche 1 ressource
// de plus que rapporté). N'ajoute AUCUNE correction qui ne soit nommément déclarée ci-dessus
// — un 6e cas non listé reste dans le chiffre brut tel quel, jamais deviné.
const coupleCorrige = totalCouples - suspectsPresents.length + sousComptesPresents.length;
console.log('');
console.log(`Couples réellement captifs (brut − suspects présents + sous-comptes présents) : ${coupleCorrige}`);
console.log(`Fonctions réellement captives (${captifs.length} brutes − ${suspectsPresents.length} suspects présents) : ${captifs.length - suspectsPresents.length}`);
console.log(`Ressources distinctes (approximatif — dédoublonnage textuel des littéraux, pas sémantique) : ${ressourcesVues.size}`);
