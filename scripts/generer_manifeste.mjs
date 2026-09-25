#!/usr/bin/env node
// ─── generer_manifeste.mjs — manifeste d'état pour le Projet claude.ai (session web) ───────
//
// Usage : node scripts/generer_manifeste.mjs [--sortie MANIFESTE.md] [--prive <chemin local>]
//                                             [--prod <url>] [--depot <propriétaire/dépôt>]
//                                             [--sans-navigateur]
// Sortie : Markdown, stdout ou --sortie (UTF-8). Sort 0 quoi qu'il trouve.
//
// ─── CE QUE C'EST, ET CE QUE CE N'EST PAS ──────────────────────────────────────────────────
// Pas un remplaçant de scripts/generer_etat.mjs (ETAT.md) : ETAT.md est exhaustif, pour un
// lecteur qui ne peut RIEN vérifier. Celui-ci est ciblé, pour un lecteur qui a un Projet
// claude.ai mal synchronisé — il ne porte QUE les faits d'état de l'A.0 bis (v4.12) : ce qui
// dérive entre deux dépôts manuels du Projet. Il ne remplace NI les instructions NI les
// canons, il dit où les lire. Pas destiné à Code (qui lit la source directement) : destiné à
// la session web, pour réduire les allers-retours en cours de chantier.
// Vérifié avant d'écrire ce script (règle « je-ne-sais-pas », étape 1 du brief) : ETAT.md ne
// couvre pas le dernier INS, les dettes ouvertes, le triptyque calculé/pondéré/rendu par
// composante, la calibration RF live, ni — par construction, puisque ça n'existe pas encore —
// l'inventaire des fichiers du Projet web. Ce script les ajoute ; il réutilise ETAT.md pour
// tout le reste plutôt que de le refaire (repo, PR, checks : mêmes techniques, dupliquées ici
// en plus petit — les deux scripts n'ont pas vocation à partager un module tant qu'un
// troisième cas d'usage ne le justifie pas).
//
// ─── LA GARDE DE FRAÎCHEUR ──────────────────────────────────────────────────────────────────
// L'en-tête porte la date de génération en TOUTES LETTRES, littérale — jamais recalculée à la
// lecture (un fichier statique ne peut pas savoir quel jour on est). Le seuil (5 jours) est
// écrit en clair : c'est la session web qui fait la soustraction, elle connaît la date du
// jour, ce fichier ne la connaîtra jamais après coup.
//
// ─── CONFIDENTIALITÉ ────────────────────────────────────────────────────────────────────────
// Ce fichier est destiné à passer par un Projet claude.ai externe au dépôt. Le nom du dépôt
// privé n'est JAMAIS écrit (mécanisme identique à --registre dans generer_etat.mjs : le
// chemin fourni par --prive n'est jamais imprimé). Faire relire la sortie par le scan
// anti-fuite avant de la déposer — ce script ne le fait pas lui-même.
//
// ─── CE QUI VIEILLIRA ───────────────────────────────────────────────────────────────────────
// La liste des fichiers du Projet claude.ai (section 7) est saisie à la main ci-dessous
// (CONFIG_FICHIERS_PROJET) : rien ne peut la découvrir automatiquement, le Projet web est un
// espace distinct du dépôt (A.0 ter), sans API. Elle dérivera comme tout ce que ce manifeste
// corrige ailleurs — la section le dit explicitement plutôt que de laisser croire à un
// inventaire constaté.

import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const T0 = new Date();
const ICI = path.dirname(fileURLToPath(import.meta.url));
const iso = (d) => new Date(d).toISOString().replace(/\.\d{3}Z$/, 'Z');
const jourFr = (d) => new Date(d).toLocaleDateString('fr-FR', { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' });

// ─── config maintenue à la main — section 7, cf. bandeau ci-dessus ────────────────────────
// dépôt: 'public' | 'prive'. chemin : relatif à la racine de ce dépôt-là.
// Sans chemin (dépôt privé seulement) : chemin résolu à l'exécution, par le nom du fichier, dans
// l'arbre du dépôt privé (cf. trouverSurMain) — pour un fichier dont le chemin serait lui-même une
// exposition, ce script étant public et servi.
// « à lever » : ambiguïté connue et non résolue, à porter au manifeste tel quel, pas à trancher ici.
const CONFIG_FICHIERS_PROJET = [
  { nom: 'ARCHITECTURE.md', depot: 'public', chemin: 'ARCHITECTURE.md' },
  { nom: 'README.md', depot: 'public', chemin: 'README.md', aLever: 'lequel des deux (public ou privé) est réellement déposé ? jamais tranché — les deux candidats sont listés' },
  { nom: 'README.md (candidat privé)', depot: 'prive', chemin: 'docs/README.md', aLever: 'voir la ligne README.md ci-dessus — même ambiguïté, deuxième candidat' },
  { nom: 'TELLUX_MODELE_CALCUL.md', depot: 'prive', chemin: 'docs/corpus_scientifique/00_canon/TELLUX_MODELE_CALCUL.md' },
  { nom: 'TELLUX_HYPOTHESES_PROTOCOLES.md', depot: 'prive', chemin: 'docs/corpus_scientifique/00_canon/TELLUX_HYPOTHESES_PROTOCOLES.md' },
  { nom: 'INDEX_DOCUMENTS_SCIENTIFIQUES.md', depot: 'prive', chemin: 'docs/corpus_scientifique/00_canon/INDEX_DOCUMENTS_SCIENTIFIQUES.md' },
  { nom: 'DOSSIER_PRESENTATION_v1.md', depot: 'prive' }, // chemin résolu à l'exécution, cf. ci-dessus
  { nom: 'auto-affinage-conception-v1.md', depot: 'prive', chemin: 'docs/internal/from-public-cleanup-p1/docs/em-mairie/auto-affinage-conception-v1.md' },
  { nom: 'PROJECT_INSTRUCTIONS_v4.12.md', depot: 'prive', chemin: 'docs/instructions/PROJECT_INSTRUCTIONS_v4.12.md' },
];
const CONFIG_FICHIERS_PROJET_MAJ = '2026-09-14'; // date de CETTE liste, pas de sa vérité — à mettre à jour à la main quand le Projet change.

// ─── arguments ──────────────────────────────────────────────────────────────────────────────
const ARGS = { depot: 'dellahstella/tellux' };
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (['--sortie', '--prive', '--prod', '--depot'].includes(a)) ARGS[a.slice(2)] = process.argv[++i];
  else if (a === '--sans-navigateur') ARGS.sansNavigateur = true;
  else if (a === '-h' || a === '--help') { usage(); process.exit(0); }
  else { process.stderr.write(`argument inconnu : ${a}\n`); usage(); process.exit(2); }
}
function usage() {
  process.stderr.write(`usage : node scripts/generer_manifeste.mjs [--sortie MANIFESTE.md] [--prive <chemin local du dépôt privé>] [--prod <url>] [--depot <propriétaire/dépôt>] [--sans-navigateur]
  --prive           chemin local du clone privé (docs/instructions, docs/internal…). Son chemin n'est jamais écrit dans la sortie. Sans lui : sections privées INDISPONIBLE.
  --sans-navigateur  saute la calibration RF live et le triptyque « rendu » (pas de Playwright) — sections marquées INDISPONIBLE au lieu d'échouer.
`);
}

// ─── utilitaires (dupliqués de generer_etat.mjs à dessein, cf. bandeau) ───────────────────
// maxBuffer explicite (même valeur dans generer_etat.mjs). Le défaut de Node, 1 Mio, a été dépassé
// par DETTES_TECHNIQUES.md (1 053 784 o, 2026-09-23) : execFileSync levait ENOBUFS, l'erreur était
// avalée ici, et le §6 imprimait « absent de origin/main » pour un fichier bien présent.
function cmd(bin, argv, cwd) { try { return execFileSync(bin, argv, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 30000, windowsHide: true, maxBuffer: 64 * 1024 * 1024 }).trim(); } catch { return null; } }
// Un échec de lecture n'est pas une absence : `git cat-file -e` départage avant d'écrire « absent ».
const present = (ref, chemin, cwd) => cmd('git', ['cat-file', '-e', `${ref}:${chemin}`], cwd) !== null;
const cell = (s) => String(s ?? '').replace(/\|/g, '\\|').replace(/\r?\n/g, ' ').trim();
const UA = { 'User-Agent': 'tellux-generer-manifeste' };
async function http(url, { headers = {}, corps = 'texte', timeout = 20000 } = {}) {
  try {
    const r = await fetch(url, { headers: { ...UA, ...headers }, signal: AbortSignal.timeout(timeout) });
    const body = corps === 'json' ? await r.json().catch(() => null) : await r.text();
    return { ok: r.ok, status: r.status, body };
  } catch (e) { return { ok: false, status: 0, erreur: e?.name === 'TimeoutError' ? 'délai dépassé' : (e?.cause?.code || e?.message || String(e)) }; }
}
const JETON = process.env.GH_TOKEN || process.env.GITHUB_TOKEN || cmd('gh', ['auth', 'token'], ICI) || null;
async function gh(p) {
  const h = { Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' };
  if (JETON) h.Authorization = `Bearer ${JETON}`;
  return http(`https://api.github.com${p}`, { headers: h, corps: 'json' });
}
const echec = (r) => r.status ? `HTTP ${r.status}` : r.erreur;
const DEPOT = ARGS.depot;
const PROD = (ARGS.prod || 'https://tellux.pages.dev').replace(/\/+$/, '');

// ─── lecture d'un fichier tracké sur origin/main d'un dépôt local, sans jamais imprimer racineLocale ───
// Même principe que R1 de generer_etat.mjs : c'est racineLocale (le clone local fourni par --prive,
// donc potentiellement le nom du dépôt privé) qui n'est jamais imprimé — PAS cheminRelatif, le chemin
// RELATIF À L'INTÉRIEUR de ce dépôt (ex. docs/internal/DECISIONS.md), qui n'a rien de confidentiel en
// lui-même : §6 l'imprime déjà pour DETTES_TECHNIQUES.md sans que ça expose quoi que ce soit. Les deux
// ne se protègent pas de la même chose ; ne pas les confondre a produit l'incohérence §1/§6 constatée
// le 2026-09-14 — corrigée en alignant §1 sur ce que fait déjà §6.
function lireTrackeSurMain(racineLocale, cheminRelatif, quel) {
  if (!racineLocale) return { statut: 'INDISPONIBLE', raison: `${quel} : aucun chemin fourni (--prive)` };
  const ref = 'origin/main';
  cmd('git', ['fetch', 'origin', 'main', '--quiet'], racineLocale); // lecture seule : fetch, jamais pull/merge
  const distant = (cmd('git', ['ls-remote', 'origin', 'refs/heads/main'], racineLocale) || '').split(/\s/)[0] || null;
  const contenu = cmd('git', ['show', `${ref}:${cheminRelatif}`], racineLocale);
  if (contenu === null) return { statut: 'INDISPONIBLE', raison: present(ref, cheminRelatif, racineLocale)
    ? `${quel} : présent sur ${ref} mais illisible (lecture git échouée) sur le dépôt fourni (chemin non imprimé)`
    : `${quel} : absent de ${ref} sur le dépôt fourni (chemin non imprimé)` };
  const modif = cmd('git', ['log', '-1', '--format=%cI', ref, '--', cheminRelatif], racineLocale);
  return { statut: 'OK', contenu, distant, modif: modif ? iso(modif) : null };
}
// Chemin d'un fichier du dépôt privé retrouvé par son NOM dans l'arbre de origin/main, pour les
// entrées de CONFIG_FICHIERS_PROJET sans chemin. Exactement une correspondance exigée : zéro ou
// plusieurs → INDISPONIBLE, jamais un choix au hasard. Le chemin trouvé n'est pas imprimé.
function trouverSurMain(racineLocale, nomFichier) {
  if (!racineLocale) return { chemin: null, raison: `${nomFichier} : aucun chemin fourni (--prive)` };
  cmd('git', ['fetch', 'origin', 'main', '--quiet'], racineLocale); // lecture seule, comme lireTrackeSurMain
  const arbre = cmd('git', ['ls-tree', '-r', '-z', '--name-only', 'origin/main'], racineLocale);
  if (arbre === null) return { chemin: null, raison: `${nomFichier} : arbre de origin/main illisible sur le dépôt fourni (chemin non imprimé)` };
  const trouves = arbre.split('\0').filter((c) => c === nomFichier || c.endsWith(`/${nomFichier}`));
  if (trouves.length !== 1) return { chemin: null, raison: `${nomFichier} : ${trouves.length} emplacement(s) sur origin/main du dépôt fourni, 1 attendu (chemin non imprimé)` };
  return { chemin: trouves[0] };
}
const RACINE_PUBLIQUE = cmd('git', ['rev-parse', '--show-toplevel'], ICI) || ICI;
function lireTrackePublic(cheminRelatif, quel) {
  // cwd = racine du dépôt, jamais scripts/ : un pathspec `-- <chemin>` est relatif au cwd de
  // git, pas à la racine — l'erreur qui rendait ARCHITECTURE.md `null` au premier essai.
  const distant = (cmd('git', ['ls-remote', 'origin', 'refs/heads/main'], RACINE_PUBLIQUE) || '').split(/\s/)[0] || null;
  const contenu = cmd('git', ['show', `origin/main:${cheminRelatif}`], RACINE_PUBLIQUE);
  if (contenu === null) return { statut: 'INDISPONIBLE', raison: present('origin/main', cheminRelatif, RACINE_PUBLIQUE)
    ? `${quel} : présent sur origin/main mais illisible (lecture git échouée)`
    : `${quel} : absent de origin/main` };
  const modif = cmd('git', ['log', '-1', '--format=%cI', 'origin/main', '--', cheminRelatif], RACINE_PUBLIQUE);
  return { statut: 'OK', contenu, distant, modif: modif ? iso(modif) : null };
}

const L = []; // sortie
const s = (...x) => L.push(...x);

// ════════════════════════════════════════════════════════════════════════════════════════
async function main() {
  cmd('git', ['fetch', 'origin', 'main', '--quiet'], ICI);

  // ─── EN-TÊTE — la garde ──────────────────────────────────────────────────────────────
  s(`# MANIFESTE D'ÉTAT TELLUX — généré le ${jourFr(T0)} à ${T0.toISOString().slice(11, 19)} UTC (${iso(T0)})`, '');
  s('**Ce manifeste a une durée de vie de 5 jours.** Comparer la date ci-dessus à aujourd\'hui : au-delà de 5 jours, tenir les faits qui suivent pour probablement périmés et en redemander un neuf plutôt que de s\'y fier. Cette règle est écrite ici en toutes lettres — ce fichier ne peut pas savoir, après coup, quel jour on est.', '');
  s('Ne remplace ni les instructions ni les canons : ne porte que les faits d\'état qui dérivent entre deux dépôts manuels (§A.0 bis, PROJECT_INSTRUCTIONS_v4.12.md). Chaque fait porte la commande qui le redonne — la revérifier vaut mieux que la croire. Destiné à la session web du Projet claude.ai ; Code lit ses sources directement et n\'a pas besoin de ce fichier.', '');

  // ─── 1. ÉTAT DÉPÔT ───────────────────────────────────────────────────────────────────
  s('## 1. État dépôt', '');
  const cPub = await gh(`/repos/${DEPOT}/commits/main`);
  if (cPub.ok) s(`- **Dernier commit \`main\` public** : \`${cPub.body.sha.slice(0, 7)}\` — ${cell(cPub.body.commit.message.split('\n')[0])} (${iso(cPub.body.commit.committer.date)}). <sub>\`gh api repos/${DEPOT}/commits/main\`</sub>`);
  else s(`- **Dernier commit \`main\` public** : INDISPONIBLE (${echec(cPub)}). <sub>\`gh api repos/${DEPOT}/commits/main\`</sub>`);

  if (ARGS.prive) {
    const shaPrive = cmd('git', ['rev-parse', 'origin/main'], ARGS.prive);
    const msgPrive = cmd('git', ['log', '-1', '--format=%s', 'origin/main'], ARGS.prive);
    const datePrive = cmd('git', ['log', '-1', '--format=%cI', 'origin/main'], ARGS.prive);
    s(shaPrive ? `- **Dernier commit \`main\` privé** : \`${shaPrive.slice(0, 7)}\` — ${cell(msgPrive)} (${datePrive ? iso(datePrive) : '?'}). <sub>\`git log -1 origin/main\` sur le dépôt privé</sub>` : `- **Dernier commit \`main\` privé** : INDISPONIBLE (--prive fourni mais lecture échouée).`);
  } else s('- **Dernier commit `main` privé** : INDISPONIBLE — `--prive` non fourni.');

  // dernier ADR / INS, mergés sur main du privé (pas committés localement)
  if (ARGS.prive) {
    for (const [label, fichier, motif] of [['ADR', 'docs/internal/DECISIONS.md', /^###\s+ADR-(\d+)/gm], ['INS', 'docs/internal/REGISTRE_INSTRUMENTS.md', /^##\s+INS-(\d+)/gm]]) {
      const r = lireTrackeSurMain(ARGS.prive, fichier, `dernier ${label}`);
      if (r.statut !== 'OK') { s(`- **Dernier ${label} mergé** : INDISPONIBLE (${r.raison}).`); continue; }
      const nums = [...r.contenu.matchAll(motif)].map((m) => +m[1]);
      const dernier = nums.length ? Math.max(...nums) : null;
      s(dernier !== null
        ? `- **Dernier ${label} mergé** : **${label}-${String(dernier).padStart(3, '0')}** (\`${fichier}\`, dépôt privé — modifié \`${r.modif || '?'}\` sur \`origin/main\`). <sub>\`git show origin/main:${fichier}\` sur le dépôt privé</sub>`
        : `- **Dernier ${label} mergé** : aucune entrée \`${label}-NNN\` trouvée.`);
    }
  } else s('- **Dernier ADR / INS mergés** : INDISPONIBLE — `--prive` non fourni.');

  // PR ouvertes + branches vivantes
  const prOuvertes = await gh(`/repos/${DEPOT}/pulls?state=open&per_page=30`);
  if (prOuvertes.ok) s(prOuvertes.body.length ? `- **PR ouvertes (${prOuvertes.body.length})** : ${prOuvertes.body.map((p) => `#${p.number} (\`${p.head.ref}\`)`).join(', ')}.` : '- **PR ouvertes** : aucune.', '<sub>`gh pr list --state open`</sub>');
  else s(`- **PR ouvertes** : INDISPONIBLE (${echec(prOuvertes)}).`);
  const branches = await gh(`/repos/${DEPOT}/branches?per_page=100`);
  if (branches.ok) { const vivantes = branches.body.map((b) => b.name).filter((n) => n !== 'main'); s(vivantes.length ? `- **Branches vivantes hors \`main\` (${vivantes.length})** : ${vivantes.map((n) => `\`${n}\``).join(', ')}.` : '- **Branches vivantes hors `main`** : aucune.', '<sub>`gh api repos/'+DEPOT+'/branches`</sub>'); }
  else s(`- **Branches vivantes** : INDISPONIBLE (${echec(branches)}).`);

  // ─── 2. CI ───────────────────────────────────────────────────────────────────────────
  s('', '## 2. CI — required checks', '');
  const prot = await gh(`/repos/${DEPOT}/branches/main/protection/required_status_checks`);
  if (prot.ok) {
    const noms = prot.body.checks?.length ? prot.body.checks.map((c) => c.context) : (prot.body.contexts || []);
    s(`**${noms.length} check(s) requis**, noms exacts tels que rendus par l'API : ${noms.map((n) => `\`${n}\``).join(' · ')}.`, '', `\`strict\` (branche à jour avant merge) : ${prot.body.strict ? 'oui' : 'non'}.`, '<sub>`gh api repos/'+DEPOT+'/branches/main/protection/required_status_checks`</sub>');
  } else s(`INDISPONIBLE (${echec(prot)}) — lecture réservée aux administrateurs du dépôt.`);

  // ─── prod : arbre + pages, pour 3 et 5 ────────────────────────────────────────────────
  const accueil = await http(`${PROD}/`);
  let appJs = null;
  if (accueil.ok) { const r = await http(`${PROD}/app`); if (r.ok) appJs = r.body; }

  // Une seule session navigateur pour §3 (rendu) et §4 (calibration live) — cf. commentaire
  // sur sessionNavigateur().
  let nav = null;
  if (!ARGS.sansNavigateur) {
    try { nav = await sessionNavigateur(); }
    catch (e) {
      // Trouvé en relançant depuis un worktree NEUF (pas celui, déjà `npm ci`, où le script a
      // été développé) : playwright n'est déclaré que dans tests/blindage-harness/package.json,
      // et son node_modules n'est jamais tracké par git — un clone ou worktree fraîchement créé
      // ne l'a donc pas tant que `npm ci` n'y a pas tourné. Message actionnable plutôt que
      // l'erreur brute de résolution de module, pour que ce défaut ne se répète pas en silence
      // à la première génération dans un nouvel espace de travail.
      const manquePlaywright = /Cannot find module ['"]playwright['"]/.test(e.message);
      nav = { erreur: manquePlaywright ? `playwright non installé — lancer \`npm ci\` dans tests/blindage-harness/ puis relancer ce script (ou --sans-navigateur pour ignorer §3/§4)` : e.message };
    }
  }

  // ─── 3. COMPOSANTES SERVIES — trois lectures ──────────────────────────────────────────
  s('', '## 3. Composantes servies — trois lectures séparées', '', 'Le DOM seul donne une fausse réponse : une composante peut être calculée et pondérée sans jamais apparaître à l\'écran (cas réel, gamma terrestre, retiré du popup le 2026-09-01 sans que le calcul ni le poids ne changent).', '');
  let poids = null, domaines = [];
  if (appJs) {
    const mw = appJs.match(/const\s+EXPERT_WEIGHTS_DEFAULT\s*=\s*\{([^}]*)\}/);
    if (mw) { poids = {}; for (const m of mw[1].matchAll(/(\w+)\s*:\s*([\d.]+)/g)) poids[m[1]] = +m[2]; }
    domaines = [
      { nom: 'Magnétique (ELF)', cle: 'M', fonctionCalc: /function\s+calcMagneticELF/ },
      { nom: 'Radiofréquences', cle: 'RF', fonctionCalc: /function\s+calcRF\b/ },
      { nom: 'Ionisant (gamma terrestre)', cle: 'I', fonctionCalc: /function\s+calcGammaAmbient/ },
    ];
  }
  if (!appJs || !poids) s('INDISPONIBLE — page `/app` ou `EXPERT_WEIGHTS_DEFAULT` illisible en prod à la génération.');
  else {
    const lignes = domaines.map((d) => {
      const calcule = d.fonctionCalc.test(appJs) ? 'oui (fonction présente)' : 'non trouvée';
      const p = poids[d.cle];
      const pondere = p > 0 ? `oui, poids ${p}` : (p === 0 ? 'poids 0' : 'non lu');
      return { nom: d.nom, cle: d.cle, calcule, pondere };
    });
    const rendu = nav?.page ? await lireRenduPopup(nav.page) : null;
    s('| composante | calculée | pondérée (composite) | rendue à l\'écran (popup live) |', '|---|---|---|---|');
    for (const l of lignes) s(`| ${l.nom} | ${l.calcule} | ${l.pondere} | ${rendu ? (rendu[l.cle] ?? 'INDISPONIBLE') : `INDISPONIBLE (${ARGS.sansNavigateur ? '--sans-navigateur' : nav?.erreur || 'popup illisible'})`} |`);
    if (rendu?._point) s('', `<sub>clic live sur ${PROD}/app, point fixe en Corse (substrat granit — même point que la vérification gamma-JRC du 2026-09-14), texte du popup principal lu après calcul</sub>`);
    s('', `Poids source : \`EXPERT_WEIGHTS_DEFAULT\` lu dans \`/app\` servi en direct (pas le dépôt local). <sub>\`curl ${PROD}/app | grep EXPERT_WEIGHTS_DEFAULT\`</sub>`);
  }

  // ─── 4. CALIBRATION EN VIGUEUR ─────────────────────────────────────────────────────────
  s('', '## 4. Calibration en vigueur — constantes lues en live', '');
  if (appJs) {
    const mb = appJs.match(/const\s+EXPERT_BOUNDS_DEFAULT\s*=\s*(\{[^;]*?\})\s*;/);
    if (poids) s(`- **Poids composite** : M=${poids.M ?? '?'} · RF=${poids.RF ?? '?'} · I=${poids.I ?? '?'} (GELÉ-001a).`);
    if (mb) s(`- **Bornes de normalisation** : \`${mb[1].replace(/\s+/g, ' ')}\` (GELÉ-001b, ELF/RF re-dérivables, gamma re-dérivable).`);
  }
  const calib = nav?.page ? await lireCalibrationLive(nav.page) : null;
  if (calib?.k != null) s(`- **k RF calibré (live)** : **${calib.k}** · dispersion ×÷${calib.disp ?? '?'} · n=${calib.n ?? '?'} points. <sub>lu sur l'identifiant \`RF_CALIB_STATS\` dans le contexte JS de ${PROD}/app (pas \`window.\` — variable \`let\`, cf. code)</sub>`);
  else s(`- **k RF calibré (live)** : INDISPONIBLE (${calib?.raison || (ARGS.sansNavigateur ? '--sans-navigateur' : nav?.erreur) || 'calibration non atteinte dans le délai imparti'}).`);
  s('', 'Aucune valeur ci-dessus ne vient d\'un document ou d\'un récap — un document qui les recopierait dériverait au prochain déploiement de mesures certifiées.');
  if (nav?.browser) await nav.browser.close().catch(() => {});

  // ─── 5. FICHIERS PUBLICS SERVIS ────────────────────────────────────────────────────────
  s('', '## 5. Fichiers publics servis — vérifiés par requête', '');
  const arbre = await gh(`/repos/${DEPOT}/git/trees/main?recursive=1`);
  if (!arbre.ok) s(`INDISPONIBLE (${echec(arbre)}).`);
  else {
    const pages = arbre.body.tree.filter((e) => e.type === 'blob' && !e.path.includes('/') && e.path.endsWith('.html'));
    const res = await Promise.all(pages.map(async (e) => { const chemin = e.path === 'index.html' ? '/' : `/${e.path.slice(0, -5)}`; const r = await http(`${PROD}${chemin}`); return { chemin, ok: r.status === 200 }; }));
    const dispo = res.filter((r) => r.ok);
    s(`**${dispo.length}/${res.length} pages HTML de la racine répondent 200** sur ${PROD} : ${res.map((r) => `\`${r.chemin}\`${r.ok ? '' : ' (échec)'}`).join(', ')}.`, '', `<sub>\`curl -o /dev/null -s -w '%{http_code}' ${PROD}<page>\` pour chacune ; liste des pages : \`git ls-tree -r origin/main --name-only\`</sub>`);
  }

  // ─── 6. DETTES OUVERTES ────────────────────────────────────────────────────────────────
  s('', '## 6. Dettes ouvertes — identifiants et statuts, pas le contenu', '');
  if (!ARGS.prive) s('INDISPONIBLE — `--prive` non fourni.');
  else {
    const r = lireTrackeSurMain(ARGS.prive, 'docs/internal/DETTES_TECHNIQUES.md', 'dettes');
    if (r.statut !== 'OK') s(`INDISPONIBLE (${r.raison}).`);
    else {
      const entrees = [...r.contenu.matchAll(/^###\s+([A-Z0-9-]+)\s+—.*$/gm)];
      // Palier 1 de INS-028 (2026-09-14, corrigé le jour même de la première génération) : le
      // premier essai ne reconnaissait que `**Statut**` + `:` HORS gras (21/213), et affirmait
      // 192 entrées « sans statut structuré ». Mesure exécutée (git blame + classement par
      // étiquette exacte, cf. INS-028) : 104 des 192 portent en réalité `**Statut :**` — les
      // DEUX-POINTS DANS le gras, MÊME CHAMP, seule la ponctuation du gras diffère. Le défaut
      // était dans CE LECTEUR, pas dans le registre. Vrai compte structuré : 125/213 ; seules
      // 88 entrées n'ont structurellement aucun champ Statut, sous quelque forme que ce soit.
      let structurees = 0, hautes = [];
      for (const m of entrees) {
        const suite = r.contenu.slice(m.index + m[0].length, m.index + m[0].length + 400);
        const st = /\*\*Statut\*\*\s*:|\*\*Statut\s*:\*\*/.test(suite);
        if (st) structurees++;
        if (/priorit[ée]\s+HAUTE/i.test(suite)) hautes.push(`\`${m[1]}\``);
      }
      s(`**${entrees.length} entrées** dans le registre (\`docs/internal/DETTES_TECHNIQUES.md\`, dépôt privé) — trop pour tenir ici, volontairement non énumérées (cf. contrainte de longueur). **${structurees}/${entrees.length}** portent un statut structuré (\`**Statut** :\` ou \`**Statut :**\` — les deux formes reconnues, même champ, cf. INS-028) ; les ${entrees.length - structurees} autres n'ont structurellement aucun champ Statut — pas une forme non lue, une absence réelle.`);
      if (hautes.length) s('', `**Priorité HAUTE explicite (${hautes.length})** : ${hautes.join(', ')}.`);
      s('', '<sub>`grep -c \'^### \' docs/internal/DETTES_TECHNIQUES.md` pour le compte ; lire le fichier pour le détail — jamais recopié ici</sub>');
    }
  }

  // ─── 7. FICHIERS DU PROJET CLAUDE.AI ───────────────────────────────────────────────────
  s('', '## 7. Fichiers du Projet claude.ai — où vit leur source, et depuis quand', '');
  s(`**Liste maintenue à la main dans ce script, dernière mise à jour le ${CONFIG_FICHIERS_PROJET_MAJ}.** Rien ne peut la découvrir automatiquement (le Projet web est hors dépôt, hors API — A.0 ter) : elle dérivera comme tout ce que ce manifeste corrige ailleurs si elle n'est pas tenue à jour à la main. Ce qui suit constate l'état de la SOURCE de chaque fichier connu, pas le contenu du Projet lui-même.`, '');
  s('| fichier | dépôt | dernière modif. source | à lever |', '|---|---|---|---|');
  for (const f of CONFIG_FICHIERS_PROJET) {
    let r;
    if (f.depot === 'public') r = lireTrackePublic(f.chemin, f.nom);
    else if (f.chemin) r = lireTrackeSurMain(ARGS.prive, f.chemin, f.nom);
    else {
      const t = trouverSurMain(ARGS.prive, f.nom);
      r = t.chemin ? lireTrackeSurMain(ARGS.prive, t.chemin, f.nom) : { statut: 'INDISPONIBLE', raison: t.raison };
    }
    const dateAff = r.statut === 'OK' ? r.modif : `INDISPONIBLE${!ARGS.prive && f.depot === 'prive' ? ' (--prive non fourni)' : ` (${r.raison})`}`;
    s(`| ${f.nom} | ${f.depot} | ${dateAff} | ${f.aLever ? cell(f.aLever) : '—'} |`);
  }

  s('', '---', '', `_Généré en ${((Date.now() - T0) / 1000).toFixed(1)} s par \`scripts/generer_manifeste.mjs\`._`);
}

// ─── navigateur (Playwright, une seule session pour §3 « rendu » ET §4 « k live ») ─────────
// UNE session partagée : lancer un Chromium headless coûte l'essentiel du temps (mesuré :
// ~130 s pour deux lancements séparés lors du premier essai de ce script) ; les deux lectures
// ne coûtent presque rien de plus une fois la page chargée.
async function sessionNavigateur() {
  // playwright n'est déclaré que dans tests/blindage-harness/package.json (déjà utilisé par
  // contrast-panels.mjs) — résolu explicitement depuis ce node_modules-là plutôt que dupliqué.
  const pkgHarnais = path.join(ICI, '..', 'tests', 'blindage-harness', 'package.json');
  const { chromium } = createRequire(pkgHarnais)('playwright');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto(`${PROD}/app`, { waitUntil: 'load', timeout: 30000 });
  // Trouvé en relisant la sortie du premier essai (rendu INDISPONIBLE malgré une calibration
  // OK sur la même page) : un écran de bienvenue plein cadre masque la carte au premier
  // chargement (« Accéder à la carte ») — sans ce clic, le clic de §3 atteint le modal, jamais
  // Leaflet. Confirmé en direct avant le premier correctif. Deuxième défaut, trouvé à la
  // RELECTURE de ce correctif-là (toujours INDISPONIBLE ensuite) : un `count()` pris sans
  // attendre pouvait s'exécuter avant que le modal n'existe dans le DOM — d'où l'attente
  // explicite de son apparition avant de cliquer, et de sa disparition avant de continuer,
  // plutôt qu'un point de contrôle unique dans le temps.
  const bouton = page.getByText('Accéder à la carte', { exact: false });
  const apparu = await bouton.first().waitFor({ state: 'visible', timeout: 8000 }).then(() => true).catch(() => false);
  if (apparu) {
    await bouton.first().click().catch(() => {});
    await bouton.first().waitFor({ state: 'hidden', timeout: 5000 }).catch(() => {});
  }
  await page.evaluate(() => { try { window.map?.invalidateSize?.(); } catch {} }).catch(() => {});
  await page.waitForTimeout(1000);
  return { browser, page, modalVu: apparu };
}
async function lireCalibrationLive(page) {
  try {
    // RF_CALIB_K/STATS sont déclarées `let`/`const` en tête de script, PAS `var` : elles
    // n'existent donc jamais sous `window.RF_CALIB_*` (bug du premier essai, confirmé en
    // direct sur la page live avant correction) — seul l'identifiant nu, dans le contexte
    // d'évaluation de la page, les atteint.
    await page.waitForFunction('typeof RF_CALIB_STATS !== "undefined" && RF_CALIB_STATS !== null', { timeout: 15000 }).catch(() => {});
    const stats = await page.evaluate('(typeof RF_CALIB_STATS !== "undefined") ? RF_CALIB_STATS : null');
    return stats ? { k: stats.k_med, disp: stats.disp_geo, n: stats.n_used } : { raison: 'RF_CALIB_STATS toujours null après 15 s — calibration non aboutie (grille ANFR ou mesures certifiées indisponibles)' };
  } catch (e) { return { raison: `lecture échouée (${e.message})` }; }
}
async function lireRenduPopup(page) {
  // Point de test fixe, déjà utilisé cette session pour la vérification gamma-JRC (granit, Corse).
  const LAT = 42.53689200787317, LNG = 8.997802734375002;
  try {
    const box = await page.locator('#map').boundingBox();
    if (!box) return null;
    await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2);
    await page.waitForSelector('.leaflet-popup-content', { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(1500); // le popup s'ouvre en "⏳ calcul…" avant son contenu réel
    const texte = await page.evaluate(() => document.querySelector('.leaflet-popup-content')?.innerText || '');
    if (!texte) return null;
    return {
      M: /\bnT\b/.test(texte) ? 'oui (unité nT présente)' : 'non',
      RF: /µW\/m²|W\/m²/.test(texte) ? 'oui (unité RF présente)' : 'non',
      I: /nSv\/h|Sv\/h/.test(texte) ? 'oui (unité dose présente)' : 'non',
      _point: `${LAT},${LNG}`,
    };
  } catch { return null; }
}

await main();
process.stdout.write(L.join('\n') + '\n');
if (ARGS.sortie) { const { writeFileSync } = await import('node:fs'); writeFileSync(ARGS.sortie, L.join('\n') + '\n', 'utf8'); }
process.stderr.write(`manifeste généré en ${((Date.now() - T0) / 1000).toFixed(1)} s\n`);
