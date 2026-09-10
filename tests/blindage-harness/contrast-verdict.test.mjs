/**
 * contrast-verdict.test.mjs — contrôle du VERDICT de contrast-panels (2026-09-10).
 *
 * CE QU'IL CONTRÔLE : ce que l'étape « Run contrast-panels » (id: contrast) du workflow
 * DIT d'un rapport — annotations et journal, résumé du job, sorties, code de sortie. Pas ce
 * que contrast-panels.mjs mesure : ça, c'est le rôle du check lui-même.
 *
 * POURQUOI : le 2026-09-09, 17 runs sont sortis en exit 2 sur les quatre mêmes dépassements
 * du plancher de #conditions-bar. Ni le journal ni le résumé ne les nommaient : le résumé ne
 * lisait pas resume.depassements et titrait « Régression de contraste » à 0/0. Neuf PR ont été
 * mergées sur un check qui a fini rouge, sans que ce rouge dise pourquoi. Et quand le rapport
 * était illisible, le garde remplaçait l'exit 2 du script par un exit 1 et sautait le résumé.
 *
 * COMMENT : il lit le VRAI bloc `run:` de l'étape dans le workflow et l'exécute sous
 * `bash -e -c` (le shell par défaut d'un `run:` sous Linux), avec un faux `node` placé en tête
 * du PATH, qui dépose un rapport connu et rend un code de sortie connu. Rien n'est recopié du
 * workflow : si le bloc change, c'est le bloc changé qui est contrôlé.
 *
 * Exige bash et jq, présents sur les runners GitHub, pas sur tous les postes.
 *
 *     node contrast-verdict.test.mjs              # les contrôles
 *     node contrast-verdict.test.mjs --montrer-bloc   # le bloc tel qu'il sera exécuté
 */
import { spawnSync } from 'node:child_process';
import { chmodSync, mkdirSync, mkdtempSync, readFileSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ICI = dirname(fileURLToPath(import.meta.url));
const WORKFLOW = join(ICI, '..', '..', '.github', 'workflows', 'contrast-panels.yml');

/** Le bloc `run: |` de l'étape `id: contrast`, désindenté. */
function blocRun() {
  const lignes = readFileSync(WORKFLOW, 'utf8').split('\n');
  const i = lignes.findIndex((l) => /^\s+id:\s*contrast\s*$/.test(l));
  if (i < 0) throw new Error('étape « id: contrast » introuvable dans le workflow');
  const j = lignes.findIndex((l, k) => k > i && /^\s+run:\s*\|\s*$/.test(l));
  if (j < 0) throw new Error("bloc « run: | » de l'étape contrast introuvable");
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

const BLOC = blocRun();
if (process.argv.includes('--montrer-bloc')) {
  process.stdout.write(BLOC);
  process.exit(0);
}

const jq = spawnSync('jq', ['--version'], { encoding: 'utf8' });
if (jq.error || jq.status !== 0) {
  console.error('ÉCHEC : jq introuvable. Ce contrôle exécute le vrai bloc du workflow, qui utilise jq '
    + '(présent sur les runners GitHub).');
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
  verifie(cas, /code de sortie du script\D{0,12}2/i.test(r.resume), 'le résumé donne le code de sortie du script');
  verifie(cas, /exit_code=2/.test(r.sorties), 'la sortie exit_code vaut 2');
  verifie(cas, r.erreurs.length > 0, 'une annotation d\'erreur est émise');
}
{
  const cas = 'rapport illisible, script en exit 0';
  const r = executer(POLLUE, 0);
  verifie(cas, r.code !== 0, `un rapport illisible ne peut pas accompagner un vert (obtenu : ${r.code})`);
  verifie(cas, /illisible/i.test(r.resume), 'le résumé dit que le rapport est illisible');
}
{
  const cas = 'rapport absent, script en échec (exit 1)';
  const r = executer(null, 1);
  verifie(cas, r.code === 1, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, /absent|illisible/i.test(r.resume), 'le résumé dit que le rapport manque');
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
}
{
  const cas = 'rapport lisible sans dépassement, script en échec (exit 1)';
  const r = executer(VERT, 1);
  verifie(cas, r.code === 1, `l'étape sort sur le code du script (obtenu : ${r.code})`);
  verifie(cas, !r.resume.includes('✅'), 'le résumé n\'est pas au vert');
  verifie(cas, /code de sortie\D{0,12}1/i.test(r.resume), 'le résumé donne le code de sortie');
}

console.log(`\n${total} contrôles, ${echecs.length} échec(s).`);
if (echecs.length) {
  console.log('Le verdict de l\'étape ne rapporte pas ce qu\'il doit :');
  for (const e of echecs) console.log(`  - ${e}`);
  process.exit(1);
}
