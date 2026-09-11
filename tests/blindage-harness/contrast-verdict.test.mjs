/**
 * contrast-verdict.test.mjs — contrôle du VERDICT de contrast-panels (2026-09-10).
 *
 * CE QU'IL CONTRÔLE : ce que l'étape « Run contrast-panels » (id: contrast) du workflow
 * DIT d'un rapport — annotations et journal, résumé du job, sorties, code de sortie. Pas ce
 * que contrast-panels.mjs mesure : ça, c'est le rôle du check lui-même.
 *
 * POURQUOI : le 2026-09-09, 17 runs sont sortis en exit 2 sur les quatre mêmes dépassements
 * du plancher de #conditions-bar. Ni le journal ni le résumé ne les nommaient : le résumé ne
 * lisait pas resume.depassements et titrait « Régression de contraste », à 0/0 sur un rapport
 * propre, aux valeurs vides sur un rapport pollué. Neuf PR ont été mergées sur un check qui a
 * fini rouge, sans que ce rouge dise pourquoi. Et le garde posé par #1371 remplaçait, sur un
 * rapport illisible, l'exit 2 du script par un exit 1 et sautait le résumé.
 *
 * COMMENT : il lit le VRAI bloc `run:` de l'étape dans le workflow et l'exécute sous
 * `bash -e -c` (le shell par défaut d'un `run:` sous Linux), avec un faux `node` placé en tête
 * du PATH, qui dépose un rapport connu et rend un code de sortie connu. Rien n'est recopié du
 * workflow : si le bloc change, c'est le bloc changé qui est contrôlé.
 *
 * Exige bash et jq, présents sur les runners GitHub, pas sur tous les postes.
 *
 * En CI (GITHUB_ACTIONS), chacun de ses échecs devient aussi une annotation d'erreur et une
 * ligne du résumé du job : un rouge de ce contrôle dit ce qui a échoué, comme ceux qu'il
 * contrôle. Son premier rouge (run 34532236088) ne montrait, dans l'onglet Checks, que
 * « Process completed with exit code 1. ».
 *
 *     node contrast-verdict.test.mjs              # les contrôles
 *     node contrast-verdict.test.mjs --montrer-bloc   # le bloc tel qu'il sera exécuté
 */
import { spawnSync } from 'node:child_process';
import { appendFileSync, chmodSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ICI = dirname(fileURLToPath(import.meta.url));
const WORKFLOW = join(ICI, '..', '..', '.github', 'workflows', 'contrast-panels.yml');
const EN_CI = Boolean(process.env.GITHUB_ACTIONS);

/** En CI, une annotation d'erreur ; `%`, CR et LF échappés comme dans le workflow. */
function annoter(msg) {
  if (!EN_CI) return;
  const m = msg.replace(/%/g, '%25').replace(/\r/g, '%0D').replace(/\n/g, '%0A');
  console.log(`::error title=Contrôle du verdict::${m}`);
}

/** Le bloc `run: |` de l'étape `id: contrast`, désindenté. */
function blocRun() {
  const lignes = readFileSync(WORKFLOW, 'utf8').split('\n');
  const i = lignes.findIndex((l) => /^\s+id:\s*contrast\s*$/.test(l));
  if (i < 0) throw new Error('étape « id: contrast » introuvable dans le workflow');
  // Le `run: |` est cherché DANS l'étape : une ligne moins indentée que ses clés la termine.
  // Sans cette borne, un `run:` d'une autre forme ici faisait lire en silence le bloc de
  // l'étape suivante (relecture adverse du 2026-09-10).
  const retraitCles = lignes[i].match(/^\s*/)[0].length;
  let j = -1;
  for (let k = i + 1; k < lignes.length; k++) {
    const l = lignes[k];
    if (l.trim() !== '' && l.match(/^\s*/)[0].length < retraitCles) break;
    if (/^\s+run:\s*\|[-+]?\s*$/.test(l)) {
      j = k;
      break;
    }
  }
  if (j < 0) throw new Error("bloc « run: | » introuvable dans l'étape contrast");
  const cle = lignes[j].match(/^\s*/)[0].length;
  const bloc = [];
  for (let k = j + 1; k < lignes.length; k++) {
    const l = lignes[k];
    if (l.trim() !== '' && l.match(/^\s*/)[0].length <= cle) break;
    bloc.push(l);
  }
  while (bloc.length && bloc[bloc.length - 1].trim() === '') bloc.pop();
  const retrait = Math.min(...bloc.filter((l) => l.trim()).map((l) => l.match(/^\s*/)[0].length));
  return bloc.map((l) => l.slice(retrait)).join('\n') + '\n';
}

let BLOC;
try {
  BLOC = blocRun();
} catch (e) {
  annoter(e.message);
  throw e;
}
if (process.argv.includes('--montrer-bloc')) {
  process.stdout.write(BLOC);
  process.exit(0);
}

const jq = spawnSync('jq', ['--version'], { encoding: 'utf8' });
if (jq.error || jq.status !== 0) {
  console.error('ÉCHEC : jq introuvable. Ce contrôle exécute le vrai bloc du workflow, qui utilise jq '
    + '(présent sur les runners GitHub).');
  annoter('jq introuvable : ce contrôle exécute le vrai bloc du workflow, qui utilise jq.');
  process.exit(2);
}

/**
 * Exécute le bloc : le faux `node` dépose `rapport` (objet → JSON, chaîne → telle quelle,
 * null → aucun fichier) dans contrast-result.json et sort en `codeScript`.
 */
function executer(rapport, codeScript) {
  const dir = mkdtempSync(join(tmpdir(), 'contrast-verdict-'));
  const bin = join(dir, 'bin');
  const travail = join(dir, 'travail');
  mkdirSync(bin);
  mkdirSync(travail);
  let depot = '';
  if (rapport !== null) {
    const fixture = join(dir, 'rapport');
    writeFileSync(fixture, typeof rapport === 'string' ? rapport : JSON.stringify(rapport, null, 2));
    depot = `cp '${fixture}' contrast-result.json\n`;
  }
  writeFileSync(join(bin, 'node'), `#!/usr/bin/env bash\n${depot}exit ${codeScript}\n`);
  chmodSync(join(bin, 'node'), 0o755);
  const resume = join(dir, 'resume.md');
  const sorties = join(dir, 'sorties.txt');
  writeFileSync(resume, '');
  writeFileSync(sorties, '');
  const r = spawnSync('bash', ['-e', '-c', BLOC], {
    cwd: travail,
    encoding: 'utf8',
    env: { ...process.env, PATH: `${bin}:${process.env.PATH}`, GITHUB_STEP_SUMMARY: resume, GITHUB_OUTPUT: sorties },
  });
  const journal = `${r.stdout || ''}${r.stderr || ''}`;
  return {
    code: r.status,
    journal,
    erreurs: journal.split('\n').filter((l) => l.startsWith('::error')),
    resume: readFileSync(resume, 'utf8'),
    sorties: readFileSync(sorties, 'utf8'),
  };
}

// ─── Rapports connus ─────────────────────────────────────────────────────────
function rapport(resume, violationsCritiques = []) {
  return {
    outil: 'contrast-panels',
    resume: {
      violations: 0, critique: 0, aa: 0, plafond_critique: 0, plafond_aa: 0,
      plancher_noeuds: 75, depassements: [], panneaux_mesures: 14, noeuds_mesures: 193, ...resume,
    },
    violations_critiques: violationsCritiques,
    violations_aa: [],
  };
}

// Le `resume` réel du run 34355870401 (#1352, 2026-09-09 13:14Z) : rouge, rapport propre.
const DEP_0909 = ['calme', 'modéré', 'actif', 'tempête'].map((s) => `balayage #conditions-bar sous son plancher : `
  + `scénario « ${s} » (état : mesuré, 8 nœud(s) < 10) — la barre ne s'est pas peuplée sous fixture, les branches `
  + 'de couleur ne sont pas exercées');
const ROUGE_0909 = rapport({ depassements: DEP_0909, noeuds_mesures: 191 });
const VERT = rapport({});
const CRITIQUE = rapport({ violations: 2, critique: 2, depassements: ['critique : 2 > plafond 0'] }, [
  { panel: 'Popup au clic', ratio: 2.41, couleur: '#9aa0a6', fond_effectif: '#ffffff', texte: 'Confiance' },
  { panel: 'Mon lieu', ratio: 2.87, couleur: '#a3a3a3', fond_effectif: '#f7f4ee', texte: 'Sources' },
]);
const DOUZE = rapport({ depassements: Array.from({ length: 12 }, (_, i) => `surface requise sous son plancher : `
  + `« Surface ${String(i + 1).padStart(2, '0')} » (état : introuvable)`) });
const ECHAPPEMENT = rapport({ depassements: ['couverture insuffisante : 42 nœuds (100 % visés)\r\nseconde ligne'] });
const POLLUE = '[contrast-panels] [supabase-cache] MISS/expiré — https://exemple.invalid → réseau réel.\n'
  + JSON.stringify(ROUGE_0909);
const AA = rapport({ violations: 3, aa: 3, depassements: ['aa : 3 > plafond 0'] });
const DIX = rapport({ depassements: DOUZE.resume.depassements.slice(0, 10) });
// La forme du rapport qu'écrit le catch de contrast-panels.mjs (`main().catch`) quand une
// exception interrompt le script : ni `resume` ni impression, une pile. La pile est un exemple.
const EXCEPTION = {
  outil: 'contrast-panels',
  erreur: 'TimeoutError: page.goto: Timeout 30000ms exceeded.\n'
    + '    at main (file:///home/runner/work/tellux/tellux/tests/blindage-harness/contrast-panels.mjs:512:14)',
};
const SANS_RESUME = { outil: 'contrast-panels' };
// Deux dérives du format : ces rapports sont écrits à la main, et le format du script peut
// changer sous eux. Le verdict doit alors refuser le rapport, pas se taire.
const CLE_RENOMMEE = structuredClone(ROUGE_0909);
CLE_RENOMMEE.resume.alertes = CLE_RENOMMEE.resume.depassements;
delete CLE_RENOMMEE.resume.depassements;
const OBJETS = structuredClone(ROUGE_0909);
OBJETS.resume.depassements = DEP_0909.map((message) => ({ type: 'plancher', message }));

// ─── Contrôles ───────────────────────────────────────────────────────────────
const echecs = [];
let total = 0;
function verifie(cas, cond, msg) {
  total += 1;
  if (cond) {
    console.log(`ok     : [${cas}] ${msg}`);
  } else {
    console.log(`ÉCHEC  : [${cas}] ${msg}`);
    echecs.push(`[${cas}] ${msg}`);
  }
}

{
  const cas = 'rouge de plancher du 2026-09-09, exit 2';
  const r = executer(ROUGE_0909, 2);
  verifie(cas, r.code === 2, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, DEP_0909.every((d) => r.resume.includes(d)), 'le résumé nomme chacun des 4 dépassements');
  verifie(cas, DEP_0909.every((d) => r.erreurs.some((e) => e.includes(d))),
    'chaque dépassement devient une annotation d\'erreur');
  verifie(cas, !r.resume.includes('Régression de contraste'),
    'le résumé ne titre pas « Régression de contraste » quand aucun plafond de contraste n\'est dépassé');
  verifie(cas, /exit_code=2/.test(r.sorties), 'la sortie exit_code vaut 2');
}
{
  const cas = 'rapport illisible, script en exit 2';
  const r = executer(POLLUE, 2);
  verifie(cas, r.code === 2, `le garde garde le code du script au lieu de le remplacer (obtenu : ${r.code})`);
  verifie(cas, /illisible/i.test(r.resume), 'le résumé dit que le rapport est illisible');
  verifie(cas, /^### ❌ Rapport illisible — code de sortie du script : 2$/m.test(r.resume),
    'le titre du résumé donne le code de sortie du script');
  verifie(cas, /exit_code=2/.test(r.sorties), 'la sortie exit_code vaut 2');
  verifie(cas, r.erreurs.length > 0, 'une annotation d\'erreur est émise');
}
{
  const cas = 'rapport illisible, script en exit 0';
  const r = executer(POLLUE, 0);
  verifie(cas, r.code !== 0, `un rapport illisible ne peut pas accompagner un vert (obtenu : ${r.code})`);
  verifie(cas, /illisible/i.test(r.resume), 'le résumé dit que le rapport est illisible');
  verifie(cas, /^### ❌ Rapport illisible — code de sortie du script : 0$/m.test(r.resume),
    'le titre donne le code du script (0), pas celui de l\'étape');
}
{
  const cas = 'rapport absent, script en échec (exit 1)';
  const r = executer(null, 1);
  verifie(cas, r.code === 1, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, /^### ❌ Rapport absent — code de sortie du script : 1$/m.test(r.resume) && !/illisible/i.test(r.resume),
    'le titre dit que le rapport manque, sans le dire illisible');
  verifie(cas, !/artefact/i.test(r.resume), 'le résumé ne renvoie pas à un artefact qui n\'existe pas');
  verifie(cas, /exit_code=1/.test(r.sorties), 'la sortie exit_code vaut 1');
}
{
  const cas = 'vert, aucun dépassement';
  const r = executer(VERT, 0);
  verifie(cas, r.code === 0, `l'étape passe (obtenu : ${r.code})`);
  verifie(cas, r.erreurs.length === 0, 'aucune annotation d\'erreur');
  verifie(cas, r.resume.includes('✅'), 'le résumé est au vert');
}
{
  const cas = 'régression de contraste, critique 2 > 0';
  const r = executer(CRITIQUE, 2);
  verifie(cas, r.code === 2, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, r.resume.includes('critique : 2 > plafond 0'), 'le résumé nomme le dépassement');
  verifie(cas, r.resume.includes('Popup au clic') && r.resume.includes('Mon lieu'),
    'le résumé liste les violations critiques');
  verifie(cas, r.resume.includes('Régression de contraste'), 'le résumé titre « Régression de contraste »');
  verifie(cas, r.erreurs.some((e) => e.includes('critique : 2 > plafond 0')), 'le dépassement devient une annotation');
}
{
  const cas = '12 dépassements';
  const r = executer(DOUZE, 2);
  const noms = DOUZE.resume.depassements;
  verifie(cas, noms.every((d) => r.resume.includes(d)), 'le résumé nomme les 12 dépassements');
  verifie(cas, r.erreurs.length <= 10, `au plus 10 annotations, la limite de GitHub par étape (obtenu : ${r.erreurs.length})`);
  const annotes = noms.filter((d) => r.erreurs.some((e) => e.includes(d))).length;
  const reste = r.erreurs.map((e) => e.match(/(\d+) autre/)).find(Boolean);
  verifie(cas, annotes > 0 && reste && annotes + Number(reste[1]) === 12,
    `les annotations nomment ou comptent les 12, sans coupe silencieuse (nommés : ${annotes}, comptés : ${reste ? reste[1] : 'aucun'})`);
}
{
  const cas = 'échappement des annotations';
  const r = executer(ECHAPPEMENT, 2);
  verifie(cas, r.erreurs.some((e) => e.includes('100 %25 visés)%0D%0Aseconde ligne')),
    'le %, le retour chariot et le retour à la ligne sont échappés : l\'annotation ne se coupe pas');
}

{
  const cas = 'script sorti en 0 avec des dépassements dans son rapport';
  const r = executer(ROUGE_0909, 0);
  verifie(cas, r.code !== 0, `un désaccord entre le code et le rapport ne passe pas au vert (obtenu : ${r.code})`);
  verifie(cas, !r.resume.includes('✅'), 'le résumé n\'est pas au vert');
  verifie(cas, DEP_0909.every((d) => r.resume.includes(d)), 'le résumé nomme les dépassements');
  verifie(cas, r.erreurs.some((e) => /incohérence/i.test(e)), 'une annotation dit l\'incohérence');
  verifie(cas, /incohérence/i.test(r.resume), 'le résumé dit l\'incohérence');
}
{
  const cas = 'rapport lisible sans dépassement, script en échec (exit 1)';
  const r = executer(VERT, 1);
  verifie(cas, r.code === 1, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, !r.resume.includes('✅'), 'le résumé n\'est pas au vert');
  verifie(cas, /code de sortie\D{0,12}1/i.test(r.resume), 'le résumé donne le code de sortie');
}

{
  const cas = 'régression AA, aa 3 > 0';
  const r = executer(AA, 2);
  verifie(cas, r.resume.includes('Régression de contraste'), 'le résumé titre « Régression de contraste »');
  verifie(cas, r.erreurs.some((e) => e.includes('aa : 3 > plafond 0')), 'le dépassement devient une annotation');
}
{
  const cas = '10 dépassements';
  const r = executer(DIX, 2);
  const noms = DIX.resume.depassements;
  const annotes = noms.filter((d) => r.erreurs.some((e) => e.includes(d))).length;
  const reste = r.erreurs.map((e) => e.match(/(\d+) autre/)).find(Boolean);
  verifie(cas, r.erreurs.length === 10, `10 annotations, la limite du runner (obtenu : ${r.erreurs.length})`);
  verifie(cas, annotes === 9 && reste && Number(reste[1]) === 1,
    `9 nommés et 1 compté (nommés : ${annotes}, comptés : ${reste ? reste[1] : 'aucun'})`);
}
{
  const cas = 'exception rattrapée par le script (rapport sans resume, exit 1)';
  const r = executer(EXCEPTION, 1);
  const tete = 'TimeoutError: page.goto: Timeout 30000ms exceeded.';
  verifie(cas, r.code === 1, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, r.erreurs.some((e) => e.includes(tete)), 'une annotation nomme l\'exception');
  verifie(cas, /^### ❌ Échec du script/m.test(r.resume), 'le titre du résumé dit l\'échec du script');
  verifie(cas, r.resume.includes(tete) && r.resume.includes('contrast-panels.mjs:512:14'), 'le résumé donne la pile');
  verifie(cas, r.journal.includes('contrast-panels.mjs:512:14'), 'le journal de l\'étape donne la pile');
  verifie(cas, !/\bnull\b/.test(r.resume), 'le résumé n\'affiche aucun « null » en guise de mesure');
  verifie(cas, /exit_code=1/.test(r.sorties), 'la sortie exit_code vaut 1');
}
{
  const cas = 'rapport lisible sans resume ni erreur, exit 1';
  const r = executer(SANS_RESUME, 1);
  verifie(cas, r.code === 1, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, r.erreurs.some((e) => /sans verdict/i.test(e)), 'une annotation dit que le rapport ne porte pas de verdict');
  verifie(cas, /^### ❌ Rapport sans verdict/m.test(r.resume), 'le titre du résumé le dit');
  verifie(cas, !/\bnull\b/.test(r.resume), 'le résumé n\'affiche aucun « null » en guise de mesure');
}
{
  const cas = 'rapport lisible sans resume ni erreur, exit 0';
  const r = executer(SANS_RESUME, 0);
  verifie(cas, r.code !== 0, `un rapport sans verdict n'accompagne pas un vert (obtenu : ${r.code})`);
  verifie(cas, !r.resume.includes('✅'), 'le résumé n\'est pas au vert');
}
for (const [nom, rap] of [['clé depassements renommée', CLE_RENOMMEE], ['dépassements en objets', OBJETS]]) {
  const cas = `format dérivé : ${nom}, exit 2`;
  const r = executer(rap, 2);
  verifie(cas, r.code === 2, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, r.erreurs.some((e) => /sans verdict/i.test(e)), 'une annotation dit que le rapport ne se lit pas');
  verifie(cas, /^### ❌ Rapport sans verdict/m.test(r.resume), 'le titre du résumé le dit');
}
{
  const cas = '12 dépassements, script sorti en 0';
  const r = executer(DOUZE, 0);
  const noms = DOUZE.resume.depassements;
  const gardees = r.erreurs.slice(0, 10);
  verifie(cas, r.code !== 0, `un désaccord entre le code et le rapport ne passe pas au vert (obtenu : ${r.code})`);
  verifie(cas, r.erreurs.length <= 10, `au plus 10 annotations, au-delà le runner les jette (obtenu : ${r.erreurs.length})`);
  verifie(cas, gardees.some((e) => /incohérence/i.test(e)), 'l\'incohérence est parmi les 10 annotations gardées');
  const annotes = noms.filter((d) => gardees.some((e) => e.includes(d))).length;
  const reste = gardees.map((e) => e.match(/(\d+) autre/)).find(Boolean);
  verifie(cas, annotes > 0 && reste && annotes + Number(reste[1]) === 12,
    `les annotations gardées nomment ou comptent les 12 (nommés : ${annotes}, comptés : ${reste ? reste[1] : 'aucun'})`);
  verifie(cas, /incohérence/i.test(r.resume), 'le résumé dit l\'incohérence');
}

console.log(`\n${total} contrôles, ${echecs.length} échec(s).`);
if (echecs.length) {
  console.log('Le verdict de l\'étape ne rapporte pas ce qu\'il doit :');
  for (const e of echecs) console.log(`  - ${e}`);
  // Même règle que pour le verdict contrôlé : 9 annotations au plus, une dixième qui compte
  // les autres, et la liste entière dans le résumé du job.
  for (const e of echecs.slice(0, 9)) annoter(e);
  if (echecs.length > 9) annoter(`… et ${echecs.length - 9} autre(s), tous listés dans le résumé du job.`);
  if (EN_CI && process.env.GITHUB_STEP_SUMMARY) {
    appendFileSync(process.env.GITHUB_STEP_SUMMARY, [
      '## Contrôle du verdict de contraste', '',
      `### ❌ ${echecs.length} échec(s) sur ${total} contrôles — le verdict ne rapporte pas ce qu'il doit`, '',
      ...echecs.map((e) => `- ${e}`), '',
    ].join('\n'));
  }
  process.exit(1);
}
