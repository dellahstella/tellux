// ─── Périmètre de BOOT-ONLY-SANS-REDECLENCHEUR-001 ──────────────────────────────────────
// Combien de lecteurs réseau restent captifs du boot — c'est-à-dire : combien de travail
// reste au chantier de politique de reprise.
//
// Usage :  node perimetre-reprise.mjs [chemin/app.html]     (défaut : ../../app.html)
// Sortie : un résumé lisible + la liste nominative. Sort 0 quoi qu'il trouve : c'est un
//          instrument de mesure, pas une garde de CI — il ne fait échouer aucune PR.
//
// ─── PROPRIÉTÉ MESURÉE, écrite avant le chiffre ─────────────────────────────────────────
// Est CAPTIVE une fonction qui, toutes conditions réunies :
//   (1) lit le réseau, en clôture transitive des appels ;
//   (2) ne prend aucun argument — donc rien ne peut la relancer avec un contexte ;
//   (3) n'est atteinte par aucune chaîne de reprise, en clôture transitive.
// On déclare une propriété, on ne tient pas une liste : une liste redevient fausse au
// premier ajout, et personne ne le voit.
//
// ─── HISTORIQUE DE L'INSTRUMENT — chaque défaut a été trouvé en le RELANÇANT ─────────────
// v1 (2026-09-09) : (a) le code COMMENTÉ comptait comme vivant — `setInterval(loadChargeReseau)`
//     était détecté alors que #1363 l'avait supprimé, il ne subsistait qu'en commentaire ;
//     (b) l'accès réseau était cherché en DIRECT seulement, alors que `loadDB` passe par
//     `sbGet()` : il faut la clôture transitive.
// v2 (2026-09-09) : (a) et (b) corrigés. Annonçait 37 captifs.
// v3 (2026-09-09) : deux défauts de plus.
//     (c) L'instrument n'énumérait qu'UN mécanisme de reprise, `setInterval`, le seul qui
//     existait quand il a été écrit. Le chantier a installé le même jour un SECOND mécanisme
//     — `enregistrerReprise()` / `declenche()` (#1366, #1367, #1369) — et l'instrument ne le
//     voyait pas : `loadHTADataOnly` et `loadBTLinesAsync`, LES DEUX SEULS lecteurs adoptés,
//     étaient comptés captifs. Il sur-rapportait d'exactement l'adoption — l'avancement du
//     chantier était invisible à ce qui le mesure, et le chiffre se dégradait à mesure qu'on
//     avançait.
//     (d) Une mention de fonction DANS UNE CHAÎNE comptait comme un appel : `loadBTLinesAsync`
//     (app.html:6951) porte au 6955 le message « …, loadBT() rend bt_indisponible. », et
//     `loadBT` basculait dans les COUVERTS par la seule vertu d'un avertissement.
//     Résultat : 37 → 35.
//
// ─── LE PIÈGE DE (d), qui vaut d'être lu avant de retoucher ce fichier ──────────────────
// Neutraliser les chaînes EN BLOC supprime aussi de VRAIES arêtes. Cette application câble
// ses gestionnaires dans du HTML généré — `'<button onclick="startCrustalCorseMeasurement('
// + …` — et ces appels sont réels, c'est le navigateur qui les exécute au clic. Le premier
// essai faisait tomber `buildCrustalLayer` et `openPrescription` non pas d'un côté ou de
// l'autre, mais HORS comptabilité : 33 au lieu de 35. C'est le pire des trois résultats —
// une fonction doit être captive ou couverte, jamais escamotée.
// RÈGLE RETENUE : les chaînes ne sont pas du code, SAUF le contenu des attributs
// gestionnaires `on…="…"`, qui en est. Extraits par fonction avant neutralisation, puis
// réinjectés dans son corps aux seules fins du graphe d'appels.
//
// ─── CE QUI VIEILLIRA ENCORE, ET COMMENT ON LE VERRA ────────────────────────────────────
// MECANISMES ci-dessous est une ÉNUMÉRATION, et une énumération vieillit — c'est structurel,
// pas réparable ici. Un troisième mécanisme de reprise rendra cet instrument faux de la même
// façon que (c). Ce qu'on peut faire, et qui est fait : l'instrument IMPRIME ce qu'il sait
// reconnaître, à chaque exécution, AVANT son chiffre. L'oubli devient visible à qui lit la
// sortie au lieu d'être enfoui dans une regex. On ne supprime pas l'énumération, on la met
// sous les yeux du lecteur. (Même remède que pour `computeElfState()` — cf. la dette
// GARDE-QUI-ENUMERE-LES-TERMES-001 au registre interne.)
//
// ─── BIAIS RÉSIDUELS, déclarés avec leur sens ───────────────────────────────────────────
// · Les gabarits `…` sont laissés INTACTS : leur `${…}` contient du code exécuté, et le
//   vider ferait disparaître de vrais appels. Une mention en partie littérale d'un gabarit
//   reste donc un faux positif — sens qui SOUS-ESTIME le travail restant.
// · Le graphe est syntaxique, pas sémantique : un appel indirect (table de dispatch,
//   `window[nom]()`) n'est pas vu — sens qui SUR-ESTIME le travail restant.

import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ICI = dirname(fileURLToPath(import.meta.url));
const CIBLE = process.argv[2] || join(ICI, '..', '..', 'app.html');

const html = readFileSync(CIBLE, 'utf8');
let js = [...html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)].map((m) => m[1]).join('\n');

// Commentaires — remplacés par du vide de MÊME longueur de ligne, pour que rien ne se
// recolle et que les positions restent comparables. TOUJOURS avant les chaînes : les
// apostrophes françaises des commentaires (« l'étiquette », « n'est ») ouvriraient sinon
// des chaînes fantômes qui avaleraient du code réel. L'ordre n'est pas commutatif.
js = js.replace(/\/\*[\s\S]*?\*\//g, (s) => s.replace(/[^\n]/g, ' '))
       .replace(/^([ \t]*)\/\/.*$/gm, (s, i) => i);

// ⚠ CES DEUX FONCTIONS VONT PAR PAIRE. Si tu durcis `videChaines`, lis ceci d'abord.
//
// Les chaînes ne sont pas du code — SAUF le contenu des attributs gestionnaires `on…="…"`,
// qui en est : cette application câble ses clics dans du HTML généré
// (`'<button onclick="startCrustalCorseMeasurement(' + …`), et c'est le navigateur qui les
// exécute. `gestionnairesDe` les rattrape AVANT que `videChaines` ne les efface ; les deux
// résultats sont recollés en `corps` plus bas.
//
// SUPPRIMER OU DURCIR CE RATTRAPAGE FAIT DISPARAÎTRE DES FONCTIONS DU DÉCOMPTE — pas les
// faire basculer d'un côté ou de l'autre, les faire SORTIR. Mesuré le 2026-09-09 :
// `buildCrustalLayer` et `openPrescription` s'évaporaient, 33 captifs au lieu de 35. Une
// fonction doit être captive ou couverte, jamais escamotée : un mauvais compte se voit, un
// escamotage non.
//
// Vérification en une commande après toute retouche ici — les deux compteurs doivent rester
// à 56 et 44, qui sont insensibles aux mécanismes de reprise et ne bougent QUE si le graphe
// d'appels a changé :
//     node perimetre-reprise.mjs | grep -E 'lecteurs réseau|sans argument'
const videChaines = (s) => s.replace(/'(?:\\.|[^'\\\n])*'|"(?:\\.|[^"\\\n])*"/g,
  (x) => x[0] + x.slice(1, -1).replace(/[^\n]/g, ' ') + x[0]);
const gestionnairesDe = (s) => [...s.matchAll(/\bon[a-z]+\s*=\s*(?:"([^"]*)|'([^']*))/gi)]
  .map((x) => x[1] ?? x[2] ?? '').join('\n');

// ─── fonctions nommées et leur corps (accolades équilibrées) ───
// `corps` sert au graphe d'appels : chaînes vidées, PLUS les gestionnaires extraits du
// corps d'origine, qui sont du code exécuté par le navigateur.
const fns = new Map();
const decl = /(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(([^)]*)\)\s*\{/g;
let m;
while ((m = decl.exec(js))) {
  let d = 1, i = decl.lastIndex;
  while (i < js.length && d > 0) { const c = js[i]; if (c === '{') d++; else if (c === '}') d--; i++; }
  const brut = js.slice(decl.lastIndex, i - 1);
  fns.set(m[1], { args: m[2].trim(), corps: videChaines(brut) + '\n' + gestionnairesDe(brut) });
}
const noms = [...fns.keys()];
const appels = (n) => noms.filter((c) => c !== n &&
  new RegExp('\\b' + c.replace(/\$/g, '\\$') + '\\s*\\(').test(fns.get(n).corps));

// ─── (1) lit le réseau : primitive directe, puis point fixe sur le graphe d'appels ───
const PRIM = /\bfetch\s*\(|XMLHttpRequest|navigator\.sendBeacon/;
const reseau = new Set(noms.filter((n) => PRIM.test(fns.get(n).corps)));
for (let chg = true; chg;) {
  chg = false;
  for (const n of noms) if (!reseau.has(n) && appels(n).some((c) => reseau.has(c))) { reseau.add(n); chg = true; }
}

// ─── (3) racines de reprise — L'ÉNUMÉRATION, déclarée puis imprimée ───
const MECANISMES = [
  {
    nom: 'setInterval(fn, …)',
    depuis: 'origine',
    trouve: (src) => [...src.matchAll(/setInterval\s*\(\s*([A-Za-z_$][\w$]*)\s*[,)]/g)].map((x) => x[1]),
  },
  {
    nom: 'setInterval(() => { … })',
    depuis: 'origine',
    trouve: (src) => {
      const out = [];
      for (const mm of src.matchAll(/setInterval\s*\(\s*(?:async\s*)?\(\s*\)\s*=>\s*\{([\s\S]{0,400}?)\}/g))
        for (const c of noms) if (new RegExp('\\b' + c + '\\s*\\(').test(mm[1])) out.push(c);
      return out;
    },
  },
  {
    // Assistant de reprise partagé (#1366). L'INSCRIPTION VAUT COUVERTURE, et c'est vérifié
    // et non supposé : `reveille()` est appelé par les écouteurs `online` et
    // `visibilitychange`, qui balaient TOUTES les clés (`_reprises.forEach`, app.html:3930
    // et 3933). Une fonction inscrite est donc bien atteinte par une chaîne de reprise.
    nom: 'enregistrerReprise(clé, fn, …)',
    depuis: '#1366 (2026-09-09)',
    trouve: (src) => [...src.matchAll(/enregistrerReprise\s*\(\s*['"][^'"]*['"]\s*,\s*([A-Za-z_$][\w$]*)\s*[,)]/g)].map((x) => x[1]),
  },
];

const racines = new Set();
const parMecanisme = MECANISMES.map((meca) => {
  const trouves = [...new Set(meca.trouve(js))];
  trouves.forEach((n) => racines.add(n));
  return { ...meca, trouves };
});

const couvert = new Set();
const pile = [...racines];
while (pile.length) {
  const n = pile.pop();
  if (couvert.has(n)) continue;
  couvert.add(n);
  if (fns.has(n)) for (const c of appels(n)) pile.push(c);
}

const lecteurs = noms.filter((n) => reseau.has(n));
const sansArg = lecteurs.filter((n) => fns.get(n).args === '');
const couverts = sansArg.filter((n) => couvert.has(n));
const captifs = sansArg.filter((n) => !couvert.has(n));

// ─── sortie : d'abord CE QUI EST RECONNU, ensuite seulement le chiffre ───
console.log(`cible : ${CIBLE}`);
console.log('');
console.log('mécanismes de reprise reconnus par cet instrument —');
console.log("  s'il en manque un, tous les chiffres ci-dessous sont sur-évalués :");
for (const meca of parMecanisme) {
  console.log(`  · ${meca.nom}  [${meca.depuis}]  → ${meca.trouves.length ? meca.trouves.join(', ') : '(aucune racine)'}`);
}
console.log('');
console.log('lecteurs réseau (transitif) :', lecteurs.length);
console.log('  dont sans argument        :', sansArg.length);
console.log('  couverts par une reprise  :', couverts.length, couverts.length ? '→ ' + couverts.join(', ') : '');
console.log('CAPTIFS                     :', captifs.length);
for (const n of captifs) console.log('   ' + n);
