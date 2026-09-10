#!/usr/bin/env node
// ─── generer_etat.mjs — l'état du projet, dérivé des sources à chaque exécution ─────────────
//
// Usage :  node scripts/generer_etat.mjs [--sortie ETAT.md] [--registre <DECISIONS.md>]
//                                        [--prod <url>] [--depot <propriétaire/dépôt>]
// Sortie : un document Markdown, sur stdout ou dans le fichier désigné par --sortie (UTF-8).
//          Une ligne de bilan sur stderr. Sort 0 quoi qu'il trouve : c'est un instrument de
//          mesure, pas une garde de CI.
//          Sous PowerShell 5.1, préférer --sortie à « > » : la redirection y ré-encode en UTF-16.
//          Ne pas écrire ETAT.md dans un clone partagé sans l'ignorer — il est dans .gitignore.
//
// ─── POURQUOI CE FICHIER EXISTE ────────────────────────────────────────────────────────────
// ETAT.md est fait pour être lu par une session qui ne peut rien vérifier — une session web,
// sans dépôt ni réseau utile. Il sera donc CRU. Trois règles en découlent, et elles sont tout
// le design :
//   1. Aucune valeur n'est écrite qui ne sorte d'une commande exécutée à la génération. Un
//      champ qu'on ne sait pas dériver sort INDISPONIBLE, avec la raison. Un manifeste qui
//      comble un trou est pire qu'un manifeste qui le laisse visible.
//   2. Prod et dépôt sont deux sources distinctes. Aucune ne remplace l'autre quand elle
//      manque : on écrit laquelle a échoué.
//   3. Ce que le générateur sait collecter est imprimé AVANT les valeurs. Un champ absent de
//      cette liste est hors de sa portée — le lecteur ne doit pas en conclure qu'il est vide.
//      Même conception que tests/blindage-harness/perimetre-reprise.mjs : le tampon de domaine
//      voyage avec la mesure au lieu de rester dans un fichier que le lecteur n'ouvrira pas.
//
// ─── STATUTS ───────────────────────────────────────────────────────────────────────────────
//   OK            dérivé à la génération, depuis la source nommée
//   INCERTAIN     dérivé, avec sa limite écrite à côté — dite ici, pas laissée à deviner
//   INDISPONIBLE  non écrit ; la raison est donnée
//
// ─── HISTORIQUE — chaque défaut a été trouvé en RELISANT la sortie contre les sources ─────
// v1 (2026-09-10), relue ligne à ligne contre git, GraphQL, curl et `git hash-object` :
//   (a) « check requis absent de la tête de main » — FAUSSE ALERTE. La protection s'évalue
//       sur la tête des PR ; un check qui ne tourne que sur `pull_request` n'apparaît jamais
//       sur `main`, et ce n'est pas une anomalie. La vraie question — un check requis
//       rapporte-t-il ? — se pose sur les PR : c'est D6.
//   (b) La cadence était calculée sur la première page d'API (100 commits) en se disant
//       « sur 7 jours » : il y en avait 188. Pagination, et une statistique qui répond à la
//       question du lecteur (la tête a-t-elle changé depuis ?) au lieu de l'intervalle médian,
//       que les rafales de merges écrasent.
//   (c) Un `cron:` cité dans un COMMENTAIRE était compté comme une planification.
//   (d) `hotrf` déclaré « sans bouton » : le bouton existe, sous `#b-hot-rf`. Un détecteur qui
//       cherche une forme trouve la forme, pas le sens — rapprochement de nom, dit comme tel.
//   (e) « 3 appels Supabase dynamiques » : la définition de `sbGet` elle-même, et deux
//       `Array.from(…)`. Il n'y en avait aucun.
//
// ─── CE QUI VIEILLIRA, ET COMMENT ON LE VERRA ─────────────────────────────────────────────
// Trois extractions reposent sur des FORMES de code : le registre `const LAYERS = {…}`, les
// boutons `id="b-<clé>"`, les appels Supabase nommés (`sbGet('…'`, `.from('…'`, `/rest/v1/…`).
// Une forme change sans prévenir. Quand une page cite le mot mais que la forme n'est plus
// reconnue, le champ sort INCERTAIN — « motif non reconnu » — au lieu de rendre un zéro qui
// serait lu comme un fait. Un zéro n'est écrit que s'il est un zéro.
//
// ─── CE QU'IL NE FAIT PAS, VOLONTAIREMENT ─────────────────────────────────────────────────
// Il n'écrit aucun fichier hors --sortie, ne modifie aucun dépôt (aucun fetch : la fraîcheur
// du registre se vérifie par `git ls-remote`, en lecture), n'imprime ni jeton ni clé, et
// n'écrit jamais le chemin du registre fourni par --registre.

import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const T0 = new Date();
const ICI = path.dirname(fileURLToPath(import.meta.url));
const MOI = path.basename(fileURLToPath(import.meta.url));
const iso = (d) => new Date(d).toISOString().replace(/\.\d{3}Z$/, 'Z');

// ─── arguments ────────────────────────────────────────────────────────────────────────────
const ARGS = {};
for (let i = 2; i < process.argv.length; i++) {
  const a = process.argv[i];
  if (['--sortie', '--registre', '--prod', '--depot'].includes(a)) ARGS[a.slice(2)] = process.argv[++i];
  else if (a === '-h' || a === '--help') { usage(); process.exit(0); }
  else { process.stderr.write(`argument inconnu : ${a}\n`); usage(); process.exit(2); }
}
function usage() {
  process.stderr.write(`usage : node scripts/${MOI} [--sortie ETAT.md] [--registre <DECISIONS.md>] [--prod <url>] [--depot <propriétaire/dépôt>]
  --sortie    fichier à écrire (UTF-8). Défaut : stdout.
  --registre  registre ADR à lire. Facultatif : il ne vit pas dans ce dépôt. Son chemin n'est jamais écrit dans la sortie.
  --prod      URL de production. Défaut : le champ « homepage » du dépôt sur GitHub.
  --depot     dépôt GitHub. Défaut : dérivé de « git remote get-url origin ».
`);
}

// ─── utilitaires ──────────────────────────────────────────────────────────────────────────
function cmd(bin, argv, cwd) {
  try {
    return execFileSync(bin, argv, { cwd, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 30000, windowsHide: true }).trim();
  } catch { return null; }
}
const cell = (s) => String(s ?? '').replace(/\|/g, '\\|').replace(/\r?\n/g, ' ').trim();
const court = (s, n = 80) => { s = cell(s); return s.length > n ? s.slice(0, n - 1) + '…' : s; };
function duree(ms) {
  if (!Number.isFinite(ms)) return '?';
  const m = Math.round(ms / 60000);
  if (m < 60) return `${m} min`;
  const h = Math.floor(m / 60), r = m % 60;
  return h < 48 ? `${h} h ${String(r).padStart(2, '0')}` : `${Math.round(h / 24)} j`;
}
const mediane = (xs) => { if (!xs.length) return NaN; const s = [...xs].sort((a, b) => a - b); const k = s.length >> 1; return s.length % 2 ? s[k] : (s[k - 1] + s[k]) / 2; };
const shaBlob = (buf) => createHash('sha1').update(Buffer.concat([Buffer.from(`blob ${buf.length}\0`), buf])).digest('hex');
const attendre = (ms) => new Promise((r) => setTimeout(r, ms));
async function parLots(items, n, fn) {
  const out = new Array(items.length); let i = 0;
  await Promise.all(Array.from({ length: Math.min(n, items.length) }, async () => {
    while (i < items.length) { const k = i++; out[k] = await fn(items[k], k); }
  }));
  return out;
}
const UA = { 'User-Agent': 'tellux-generer-etat' };
async function http(url, { headers = {}, method = 'GET', redirect = 'follow', timeout = 30000, corps = 'texte' } = {}) {
  try {
    const r = await fetch(url, { method, headers: { ...UA, ...headers }, redirect, signal: AbortSignal.timeout(timeout) });
    let body = null;
    if (method !== 'HEAD') {
      if (corps === 'octets') body = Buffer.from(await r.arrayBuffer());
      else if (corps === 'json') { const t = await r.text(); try { body = JSON.parse(t); } catch { body = null; } }
      else body = await r.text();
    }
    return { ok: r.ok, status: r.status, headers: r.headers, body };
  } catch (e) {
    return { ok: false, status: 0, erreur: e?.name === 'TimeoutError' ? `délai dépassé (${timeout / 1000} s)` : (e?.cause?.code || e?.message || String(e)) };
  }
}
const echec = (r) => (r.status ? `HTTP ${r.status}` : r.erreur);
const dernierRun = (runs, nom) => runs.filter((r) => r.name === nom).sort((a, b) => b.id - a.id)[0] || null;

// ─── ce que le générateur sait collecter — imprimé AVANT les valeurs ──────────────────────
const CATALOGUE = [
  ['D1', 'Tête de la branche par défaut', 'API GitHub', 'SHA, date et sujet du dernier commit', 'les branches non fusionnées'],
  ['D2', 'Cadence de la branche par défaut', 'API GitHub', 'tous les commits des 7 derniers jours ; intervalle médian ; part du temps où la tête changeait dans l’heure, 6 h, 24 h', 'l’avenir : ce sont des statistiques passées'],
  ['D3', 'PR mergées récemment', 'API GitHub', 'les 10 plus récentes parmi les 50 PR fermées mises à jour le plus récemment', 'les PR fermées sans merge'],
  ['D4', 'PR ouvertes', 'API GitHub', 'numéro, titre, état de fusion calculé par GitHub, ouverture', 'le contenu des PR'],
  ['D5', 'Protection de la branche par défaut', 'API GitHub, droit administrateur', 'checks requis, exigence « à jour »', 'sans droit administrateur, rien : sort INDISPONIBLE ; la date d’ajout d’un check requis'],
  ['D6', 'Checks requis sur les dernières PR mergées', 'API GitHub', 'présence et conclusion de chaque check requis (D5) sur la tête des PR de D3', 'les PR ouvertes ; quand un check est devenu requis'],
  ['D7', 'Checks sur la tête de la branche par défaut', 'API GitHub', 'check-runs du dernier commit', 'la protection, qui s’évalue sur la tête des PR (D6)'],
  ['D8', 'Workflows planifiés', 'API GitHub', 'fichiers de workflow déclarant `schedule:` à la tête, lignes commentées ignorées ; dernier run planifié', 'les runs lancés à la main'],
  ['P1', 'Pages servies', 'prod + arbre Git de la tête', 'chaque `*.html` à la racine, demandé à son URL propre ; identité par SHA de blob Git', 'les pages hors racine'],
  ['P2', 'Données servies', 'prod + arbre Git de la tête', 'chaque fichier de `public/data/`, demandé en prod ; identité par SHA de blob ; `generated_at` s’il existe', 'les données chargées d’ailleurs (Supabase : P4)'],
  ['P3', 'Couches déclarées par les pages servies', 'prod', 'clés de `const LAYERS = {…}` ; bouton `id="b-<clé>"` hors commentaires HTML, au besoin par rapprochement de nom (tirets et soulignés ignorés)', 'l’écran : un bouton créé en JS ou masqué en CSS échappe — « présent » n’est pas « visible »'],
  ['P4', 'Tables Supabase lues par les pages servies', 'Supabase — hôte et clé lus dans les pages servies', 'tables nommées littéralement dans `sbGet(…)`, `.from(…)` ou une URL `/rest/v1/<table>` ; lignes visibles avec la clé anon servie (HEAD, aucun corps)', 'ce qu’un visiteur ne voit pas : 0 visible ne prouve pas une table vide ; une requête qui ne passe par aucune de ces trois formes'],
  ['P5', 'Identifiant de version servi', 'prod, en-têtes HTTP', 'ETag, Last-Modified et en-têtes `x-*` de la page d’accueil', '—'],
  ['R1', 'Dernier ADR pris', 'registre fourni par --registre', 'plus grand `### ADR-NNN` sur la réf distante suivie ; fraîcheur par `git ls-remote`', 'sans --registre, rien : sort INDISPONIBLE'],
];

// ─── état de la génération ────────────────────────────────────────────────────────────────
const SOURCES = [];   // [nom, état, détail]
const CHAMPS = {};    // id → { statut, corps, requete, raison }
const champ = (id, statut, corps, extra = {}) => { CHAMPS[id] = { statut, corps, ...extra }; };
const indispo = (id, raison, requete) => champ(id, 'INDISPONIBLE', null, { raison, requete });
const IDS_DEPOT = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'];
const IDS_PROD = ['P1', 'P2', 'P3', 'P4', 'P5'];

const DEPOT = ARGS.depot || (() => {
  const url = cmd('git', ['remote', 'get-url', 'origin'], ICI);
  const m = url && url.match(/github\.com[/:]([^/]+)\/([^/]+?)(?:\.git)?\/?$/);
  return m ? `${m[1]}/${m[2]}` : null;
})();
const JETON = process.env.GH_TOKEN || process.env.GITHUB_TOKEN || cmd('gh', ['auth', 'token'], ICI) || null;
const AUTH = process.env.GH_TOKEN ? 'jeton GH_TOKEN' : process.env.GITHUB_TOKEN ? 'jeton GITHUB_TOKEN' : JETON ? 'jeton de « gh auth token »' : 'aucune (quota public : 60 requêtes/h)';
function gh(p, brut = false) {
  const h = { Accept: brut ? 'application/vnd.github.raw+json' : 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' };
  if (JETON) h.Authorization = `Bearer ${JETON}`;
  return http(`https://api.github.com${p}`, { headers: h, corps: brut ? 'texte' : 'json' });
}

// ─── dépôt ────────────────────────────────────────────────────────────────────────────────
let REPO = null, BRANCHE = null, TETE = null, ARBRE = null, ARBRE_TRONQUE = false, REQUIS = null, MERGEES = null, PROBA = null;

async function collecterDepot() {
  if (!DEPOT) {
    SOURCES.push(['API GitHub', 'INDISPONIBLE', 'dépôt non dérivable : « git remote get-url origin » ne désigne pas GitHub — passer --depot']);
    for (const id of IDS_DEPOT) indispo(id, 'dépôt non dérivable (voir Sources)');
    return;
  }
  const r = await gh(`/repos/${DEPOT}`);
  if (!r.ok) {
    SOURCES.push(['API GitHub', 'ÉCHEC', `GET /repos/${DEPOT} → ${echec(r)}`]);
    for (const id of IDS_DEPOT) indispo(id, 'API GitHub en échec (voir Sources)');
    return;
  }
  REPO = r.body; BRANCHE = REPO.default_branch;
  SOURCES.push(['API GitHub', 'joignable', `dépôt \`${DEPOT}\` · branche par défaut \`${BRANCHE}\` · authentification : ${AUTH}`]);

  // D1 — tête
  let q = `GET /repos/${DEPOT}/commits/${BRANCHE}`;
  const c = await gh(`/repos/${DEPOT}/commits/${encodeURIComponent(BRANCHE)}`);
  if (!c.ok) indispo('D1', `${q} → ${echec(c)}`, q);
  else {
    TETE = { sha: c.body.sha, date: c.body.commit.committer.date, sujet: c.body.commit.message.split('\n')[0] };
    champ('D1', 'OK', `\`${BRANCHE}\` @ \`${TETE.sha.slice(0, 7)}\` (${TETE.sha}) — commité le ${iso(TETE.date)}\n\n> ${cell(TETE.sujet)}`, { requete: q });
  }

  // D2 — cadence, sur TOUS les commits de la fenêtre (paginé, plafonné à 10 pages)
  const depuis = new Date(T0 - 7 * 864e5).toISOString();
  q = `GET /repos/${DEPOT}/commits?sha=${BRANCHE}&since=${iso(depuis)}&per_page=100&page=1…`;
  const dates = []; let pages = 0, plafond = false, erreurD2 = null;
  for (let page = 1; page <= 10; page++) {
    const l = await gh(`/repos/${DEPOT}/commits?sha=${encodeURIComponent(BRANCHE)}&since=${depuis}&per_page=100&page=${page}`);
    if (!l.ok || !Array.isArray(l.body)) { erreurD2 = echec(l); break; }
    pages = page;
    for (const x of l.body) dates.push(+new Date(x.commit.committer.date));
    if (l.body.length < 100) break;
    if (page === 10) plafond = true;
  }
  if (!dates.length && erreurD2) indispo('D2', `${q} → ${erreurD2}`, q);
  else {
    const t = dates.sort((a, b) => a - b);
    const ecarts = t.slice(1).map((v, i) => v - t[i]);
    const somme = ecarts.reduce((a, b) => a + b, 0);
    // Part du temps où, depuis un instant pris au hasard, la tête changeait dans les X suivantes :
    // sur un écart g entre deux commits, cet instant tombe à moins de X du suivant pendant min(g, X).
    const part = (X) => Math.round((100 * ecarts.reduce((a, g) => a + Math.min(g, X), 0)) / somme);
    PROBA = somme > 0 ? { h1: part(3600e3), h6: part(6 * 3600e3), h24: part(24 * 3600e3) } : null;
    const incomplet = plafond || !!erreurD2;
    const corps = PROBA
      ? `${incomplet ? 'au moins ' : ''}${t.length} commits sur \`${BRANCHE}\` en 7 jours (${pages} page(s) d’API) · intervalle médian entre deux : ${duree(mediane(ecarts))} · le plus long : ${duree(Math.max(...ecarts))}.\n\n`
        + `Depuis un instant pris au hasard entre le premier et le dernier de ces commits, la tête a changé **dans l’heure ${PROBA.h1} % du temps**, dans les 6 h ${PROBA.h6} %, dans les 24 h ${PROBA.h24} %. L’intervalle médian, lui, est écrasé par les rafales de merges : il ne dit pas combien de temps un état reste vrai.`
      : `${t.length} commit(s) sur \`${BRANCHE}\` en 7 jours — trop peu pour une statistique.`;
    champ('D2', incomplet ? 'INCERTAIN' : 'OK', corps, { requete: q, raison: plafond ? 'plafond de 10 pages atteint : statistiques sur les 1000 commits les plus récents' : erreurD2 ? `pagination interrompue (${erreurD2}) : statistiques sur les commits lus` : null });
  }

  // D3 — PR mergées récemment
  q = `GET /repos/${DEPOT}/pulls?state=closed&sort=updated&direction=desc&per_page=50`;
  const f = await gh(`/repos/${DEPOT}/pulls?state=closed&sort=updated&direction=desc&per_page=50`);
  if (!f.ok || !Array.isArray(f.body)) indispo('D3', `${q} → ${echec(f)}`, q);
  else {
    MERGEES = f.body.filter((p) => p.merged_at).sort((a, b) => b.merged_at.localeCompare(a.merged_at)).slice(0, 10);
    champ('D3', 'OK', MERGEES.length
      ? '| PR | titre | mergée le |\n|---|---|---|\n' + MERGEES.map((p) => `| #${p.number} | ${court(p.title)} | ${iso(p.merged_at)} |`).join('\n')
      : 'aucune PR mergée parmi les 50 PR fermées les plus récemment mises à jour.', { requete: q });
  }

  // D4 — PR ouvertes
  q = `GET /repos/${DEPOT}/pulls?state=open&per_page=100, puis GET …/pulls/<n> pour chacune`;
  const o = await gh(`/repos/${DEPOT}/pulls?state=open&per_page=100`);
  if (!o.ok || !Array.isArray(o.body)) indispo('D4', `${q} → ${echec(o)}`, q);
  else {
    const lignes = await parLots(o.body, 4, async (p) => {
      let d = await gh(`/repos/${DEPOT}/pulls/${p.number}`);
      if (d.ok && d.body.mergeable_state === 'unknown') { await attendre(2500); d = await gh(`/repos/${DEPOT}/pulls/${p.number}`); }
      return { p, etat: d.ok ? d.body.mergeable_state : `illisible (${echec(d)})` };
    });
    const inconnu = lignes.some((x) => x.etat === 'unknown' || x.etat.startsWith('illisible'));
    champ('D4', inconnu ? 'INCERTAIN' : 'OK', lignes.length
      ? '| PR | titre | brouillon | état de fusion | ouverte le | branche |\n|---|---|---|---|---|---|\n'
        + lignes.map(({ p, etat }) => `| #${p.number} | ${court(p.title, 70)} | ${p.draft ? 'oui' : 'non'} | \`${etat}\` | ${iso(p.created_at)} | \`${court(p.head.ref, 50)}\` |`).join('\n')
        + '\n\nÉtats GitHub : `clean` fusionnable · `behind` en retard sur la base · `blocked` bloquée par un check requis ou une revue · `dirty` conflit · `unstable` check non requis en échec · `unknown` pas encore calculé.'
      : 'aucune PR ouverte à la génération.', { requete: q, raison: inconnu ? 'état de fusion non calculé par GitHub pour au moins une PR, même après une seconde lecture' : null });
  }

  // D5 — protection
  q = `GET /repos/${DEPOT}/branches/${BRANCHE}/protection`;
  const pr = await gh(`/repos/${DEPOT}/branches/${encodeURIComponent(BRANCHE)}/protection`);
  if (pr.ok) {
    const rsc = pr.body.required_status_checks;
    REQUIS = rsc ? (rsc.checks?.length ? rsc.checks.map((x) => x.context) : rsc.contexts || []) : [];
    champ('D5', 'OK', rsc
      ? `**${REQUIS.length} check(s) requis** sur \`${BRANCHE}\` : ${REQUIS.map((x) => `\`${x}\``).join(' · ')}\n\nExigence « branche à jour avant merge » (\`strict\`) : ${rsc.strict ? 'oui' : 'non'}.`
      : 'protection présente, aucun check requis.', { requete: q });
  } else if (pr.status === 404 && /not protected/i.test(pr.body?.message || '')) { REQUIS = []; champ('D5', 'OK', `\`${BRANCHE}\` n’est pas protégée.`, { requete: q }); }
  else indispo('D5', `${echec(pr)} — lecture réservée aux administrateurs du dépôt ; authentification : ${AUTH}`, q);

  // D6 — les checks requis rapportent-ils ? La question se pose sur les PR, pas sur main.
  if (REQUIS === null) indispo('D6', 'protection illisible (D5) : on ne sait pas quels checks sont requis');
  else if (!MERGEES) indispo('D6', 'liste des PR mergées indisponible (D3)');
  else if (!REQUIS.length) champ('D6', 'OK', 'aucun check requis (D5).');
  else if (!MERGEES.length) champ('D6', 'OK', 'aucune PR mergée récente sur laquelle vérifier (D3).');
  else {
    const vus = await parLots(MERGEES, 4, async (p) => {
      const k = await gh(`/repos/${DEPOT}/commits/${p.head.sha}/check-runs?per_page=100`);
      return { p, ok: k.ok, runs: k.ok ? (k.body.check_runs || []) : [] };
    });
    const illisibles = vus.filter((x) => !x.ok).map((x) => `#${x.p.number}`);
    const lus = vus.filter((x) => x.ok);
    const lignes = REQUIS.map((ctx) => {
      const avec = lus.filter((x) => dernierRun(x.runs, ctx));
      const reussi = avec.filter((x) => dernierRun(x.runs, ctx).conclusion === 'success').length;
      const sans = lus.filter((x) => !dernierRun(x.runs, ctx)).map((x) => `#${x.p.number}`);
      return `| \`${ctx}\` | ${avec.length}/${lus.length} | ${reussi} | ${sans.length ? sans.join(', ') : '—'} |`;
    });
    champ('D6', illisibles.length ? 'INCERTAIN' : 'OK',
      `Sur la tête des ${lus.length} dernières PR mergées (D3) :\n\n| check requis | présent sur | dont réussi (dernier run) | absent de |\n|---|---|---|---|\n${lignes.join('\n')}\n\n`
      + 'Une absence ne tranche rien seule : l’API ne date pas l’ajout d’un check à la protection, et une PR mergée avant cet ajout n’avait pas à le porter.',
      { requete: 'GET …/commits/<tête de chaque PR de D3>/check-runs', raison: illisibles.length ? `check-runs illisibles pour ${illisibles.join(', ')}` : null });
  }

  // D7 — checks sur la tête de la branche par défaut
  if (!TETE) indispo('D7', 'tête inconnue (D1 indisponible)');
  else {
    q = `GET /repos/${DEPOT}/commits/${TETE.sha.slice(0, 7)}/check-runs?per_page=100`;
    const k = await gh(`/repos/${DEPOT}/commits/${TETE.sha}/check-runs?per_page=100`);
    if (!k.ok) indispo('D7', `${q} → ${echec(k)}`, q);
    else {
      const runs = k.body.check_runs || [];
      champ('D7', 'OK', (runs.length
        ? '| check | requis | état | conclusion | terminé le |\n|---|---|---|---|---|\n'
          + runs.map((x) => `| ${cell(x.name)} | ${REQUIS ? (REQUIS.includes(x.name) ? 'oui' : 'non') : '?'} | ${x.status} | ${x.conclusion ?? '—'} | ${x.completed_at ? iso(x.completed_at) : '—'} |`).join('\n')
        : 'aucun check-run sur la tête.')
        + `\n\nLa protection s’évalue sur la tête des PR (D6), pas sur celle de \`${BRANCHE}\` : un check qui ne tourne que sur les PR n’apparaît pas ici, et ce n’est pas une anomalie.`,
        { requete: q });
    }
  }

  // D8 — workflows planifiés
  if (!TETE) indispo('D8', 'tête inconnue (D1 indisponible)');
  else {
    q = `GET /repos/${DEPOT}/actions/workflows, contenu de chaque fichier à la tête, puis …/runs?event=schedule&per_page=1`;
    const w = await gh(`/repos/${DEPOT}/actions/workflows?per_page=100`);
    if (!w.ok) indispo('D8', `${q} → ${echec(w)}`, q);
    else {
      const wfs = w.body.workflows || [];
      const res = await parLots(wfs, 4, async (wf) => {
        const src = await gh(`/repos/${DEPOT}/contents/${wf.path}?ref=${TETE.sha}`, true);
        if (!src.ok) return { wf, lisible: false };
        if (!/^[ \t]*schedule[ \t]*:/m.test(src.body)) return { wf, lisible: true, planifie: false };
        const crons = [...new Set([...src.body.matchAll(/^[ \t]*-?[ \t]*cron[ \t]*:[ \t]*['"]([^'"]+)['"]/gm)].map((m) => m[1]))];
        const run = await gh(`/repos/${DEPOT}/actions/workflows/${wf.id}/runs?event=schedule&per_page=1`);
        return { wf, lisible: true, planifie: true, crons, dernier: run.ok ? run.body.workflow_runs?.[0] || null : undefined };
      });
      const plan = res.filter((x) => x.planifie);
      const illisibles = res.filter((x) => !x.lisible);
      let corps = plan.length
        ? '| workflow | cron déclaré | état | dernier run planifié | conclusion |\n|---|---|---|---|---|\n'
          + plan.map(({ wf, crons, dernier }) => `| \`${wf.path.split('/').pop()}\` | ${crons.map((x) => `\`${x}\``).join(', ') || '—'} | ${wf.state} | ${dernier === undefined ? 'illisible' : dernier ? iso(dernier.created_at) : 'aucun'} | ${dernier ? (dernier.conclusion ?? dernier.status) : '—'} |`).join('\n')
        : 'aucun workflow ne déclare `schedule:` à la tête.';
      corps += `\n\n${wfs.length} workflow(s) au total, dont ${plan.length} planifié(s). Un cron déclaré n’est pas une cadence tenue : GitHub retarde ou saute des déclenchements planifiés — comparer avec la date du dernier run.`;
      if (illisibles.length) corps += ` Fichier illisible pour : ${illisibles.map((x) => `\`${x.wf.path}\``).join(', ')}.`;
      champ('D8', illisibles.length ? 'INCERTAIN' : 'OK', corps, { requete: q, raison: illisibles.length ? 'au moins un fichier de workflow illisible : sa planification est inconnue' : null });
    }
  }

  // arbre de la tête (pour P1/P2)
  if (TETE) {
    const t = await gh(`/repos/${DEPOT}/git/trees/${TETE.sha}?recursive=1`);
    if (t.ok) { ARBRE = t.body.tree || []; ARBRE_TRONQUE = !!t.body.truncated; }
  }
}

// ─── prod ─────────────────────────────────────────────────────────────────────────────────
let PROD = null;
const SERVI = {};   // page → texte servi

async function collecterProd() {
  PROD = (ARGS.prod || REPO?.homepage || '').replace(/\/+$/, '') || null;
  const origineUrl = ARGS.prod ? 'argument --prod' : 'champ « homepage » du dépôt';
  if (!PROD) {
    SOURCES.push(['Prod', 'INDISPONIBLE', 'URL non dérivable : aucun --prod, et homepage du dépôt vide ou API injoignable']);
    for (const id of IDS_PROD) indispo(id, 'URL de prod inconnue (voir Sources)');
    return;
  }
  const accueil = await http(`${PROD}/`, { redirect: 'manual' });
  if (!accueil.status) {
    SOURCES.push(['Prod', 'ÉCHEC', `${PROD}/ → ${accueil.erreur}`]);
    for (const id of IDS_PROD) indispo(id, 'prod injoignable (voir Sources)');
    return;
  }
  SOURCES.push(['Prod', 'joignable', `${PROD} (URL : ${origineUrl}) · \`/\` → HTTP ${accueil.status}`]);

  // P5 — identifiant de version servi
  const xs = [...accueil.headers.keys()].filter((h) => h.startsWith('x-'));
  const etag = accueil.headers.get('etag'), lm = accueil.headers.get('last-modified');
  if (etag || lm) champ('P5', 'OK', `ETag : ${etag ? `\`${etag}\`` : '—'} · Last-Modified : ${lm || '—'}${xs.length ? ` · en-têtes x-* : ${xs.join(', ')}` : ''}`, { requete: `GET ${PROD}/ (en-têtes)` });
  else indispo('P5', `la page d’accueil n’envoie ni ETag ni Last-Modified${xs.length ? ` (en-têtes x-* présents : ${xs.join(', ')})` : ''} — l’identité de contenu (P1, P2) tient lieu de version`, `GET ${PROD}/ (en-têtes)`);

  if (!ARBRE) {
    for (const id of ['P1', 'P2']) indispo(id, 'arbre Git de la tête inconnu (API GitHub) : pas de liste de fichiers ni de SHA à comparer — la prod n’est pas sondée à l’aveugle');
  } else {
    // P1 — pages
    const pages = ARBRE.filter((e) => e.type === 'blob' && !e.path.includes('/') && e.path.endsWith('.html'));
    const res = await parLots(pages, 4, async (e) => {
      const chemin = e.path === 'index.html' ? '/' : `/${e.path.slice(0, -5)}`;
      const r = await http(`${PROD}${chemin}`, { redirect: 'manual', corps: 'octets' });
      if (r.status === 200) { SERVI[e.path] = r.body.toString('utf8'); return { e, chemin, rep: 'HTTP 200', id: shaBlob(r.body) === e.sha }; }
      if (r.status >= 300 && r.status < 400) return { e, chemin, rep: `HTTP ${r.status} → ${r.headers.get('location') || '?'}`, id: null };
      return { e, chemin, rep: echec(r), id: null };
    });
    const ident = res.filter((x) => x.id === true).length, diff = res.filter((x) => x.id === false);
    champ('P1', ARBRE_TRONQUE ? 'INCERTAIN' : 'OK',
      `**${ident}/${res.length} pages servies identiques** au contenu de \`${BRANCHE}\` @ \`${TETE.sha.slice(0, 7)}\`${diff.length ? ` — **${diff.length} différente(s)** ; si la tête vient de changer, voir D7 : son déploiement peut être en cours` : ''}.\n\n`
      + '| page | URL demandée | réponse | contenu |\n|---|---|---|---|\n'
      + res.map((x) => `| \`${x.e.path}\` | \`${x.chemin}\` | ${x.rep} | ${x.id === true ? 'identique' : x.id === false ? '**différent**' : '—'} |`).join('\n'),
      { requete: `GET ${PROD}/<page> sans suivre les redirections ; SHA-1 de blob Git comparé à l’arbre de la tête`, raison: ARBRE_TRONQUE ? 'arbre Git tronqué par l’API : des pages peuvent manquer' : null });

    // P2 — données
    const donnees = ARBRE.filter((e) => e.type === 'blob' && e.path.startsWith('public/data/'));
    const rd = await parLots(donnees, 6, async (e) => {
      const r = await http(`${PROD}/${e.path.split('/').map(encodeURIComponent).join('/')}`, { redirect: 'manual', corps: 'octets', timeout: 60000 });
      if (r.status !== 200) return { e, rep: r.status ? `HTTP ${r.status}` : r.erreur, id: null, gen: null };
      let gen = null;
      if (/\.(geo)?json$/.test(e.path)) { try { const j = JSON.parse(r.body.toString('utf8')); if (j && typeof j === 'object' && !Array.isArray(j) && 'generated_at' in j) gen = String(j.generated_at); } catch { /* non JSON : pas d'horodatage */ } }
      return { e, rep: 'HTTP 200', id: shaBlob(r.body) === e.sha, gen };
    });
    const identD = rd.filter((x) => x.id === true).length;
    champ('P2', ARBRE_TRONQUE ? 'INCERTAIN' : 'OK',
      `**${identD}/${rd.length} fichiers de \`public/data/\` servis identiques** à la tête.\n\n`
      + '| fichier | taille (dépôt) | réponse | contenu | `generated_at` |\n|---|---|---|---|---|\n'
      + rd.map((x) => `| \`${x.e.path.slice('public/data/'.length)}\` | ${x.e.size ?? '?'} o | ${x.rep} | ${x.id === true ? 'identique' : x.id === false ? '**différent**' : '—'} | ${x.gen ? `\`${cell(x.gen)}\`` : '—'} |`).join('\n'),
      { requete: `GET ${PROD}/public/data/<fichier> ; SHA-1 de blob Git comparé à l’arbre de la tête`, raison: ARBRE_TRONQUE ? 'arbre Git tronqué par l’API : des fichiers peuvent manquer' : null });
  }

  // P3 — couches
  const pagesServies = Object.keys(SERVI);
  if (!pagesServies.length) indispo('P3', 'aucune page servie lue (P1) : rien à analyser');
  else {
    const norm = (x) => x.replace(/[-_]/g, '').toLowerCase();
    const blocs = []; const nonReconnu = [];
    for (const p of pagesServies) {
      const s = SERVI[p];
      const m = s.match(/const\s+LAYERS\s*=\s*\{([^}]*)\}/);
      if (!m) { if (/\bLAYERS\b/.test(s)) nonReconnu.push(p); continue; }
      const cles = m[1].split(',').map((x) => x.split(':')[0].trim()).filter(Boolean);
      const vivant = s.replace(/<!--[\s\S]*?-->/g, '');
      const idsVivants = [...new Set([...vivant.matchAll(/id=["']b-([A-Za-z0-9_-]+)["']/g)].map((x) => x[1]))];
      const idsTous = [...new Set([...s.matchAll(/id=["']b-([A-Za-z0-9_-]+)["']/g)].map((x) => x[1]))];
      const pris = new Set();
      const lignes = cles.map((k) => {
        const exact = idsVivants.find((i) => i === k);
        if (exact) { pris.add(exact); return `| \`${k}\` | présent |`; }
        const proche = idsVivants.find((i) => !pris.has(i) && norm(i) === norm(k));
        if (proche) { pris.add(proche); return `| \`${k}\` | présent sous \`#b-${proche}\` — rapprochement de nom |`; }
        const enCommentaire = idsTous.find((i) => norm(i) === norm(k));
        if (enCommentaire) return `| \`${k}\` | **seulement dans un commentaire HTML** |`;
        return `| \`${k}\` | **absent du HTML statique** |`;
      });
      const sansCle = idsVivants.filter((i) => !pris.has(i));
      blocs.push(`**\`${p}\`** — ${cles.length} clé(s) dans \`LAYERS\` :\n\n| clé | bouton \`#b-<clé>\` hors commentaires |\n|---|---|\n${lignes.join('\n')}`
        + (sansCle.length ? `\n\nBoutons \`#b-*\` présents sans clé \`LAYERS\` correspondante : ${sansCle.map((x) => `\`${x}\``).join(', ')}.` : ''));
    }
    if (!blocs.length) champ('P3', 'INCERTAIN', nonReconnu.length ? `les pages ${nonReconnu.map((x) => `\`${x}\``).join(', ')} citent \`LAYERS\`, mais la forme \`const LAYERS = {…}\` n’y est plus reconnue.` : 'aucune page servie ne déclare `const LAYERS = {…}`.', { raison: 'motif non reconnu — un zéro ici serait une forme de code changée, pas une app sans couches' });
    else champ('P3', nonReconnu.length ? 'INCERTAIN' : 'OK', blocs.join('\n\n') + (nonReconnu.length ? `\n\nMotif non reconnu sur : ${nonReconnu.join(', ')}.` : ''), { requete: 'analyse statique des pages servies lues en P1', raison: nonReconnu.length ? 'motif `LAYERS` non reconnu sur au moins une page' : null });
  }

  // P4 — Supabase
  await collecterSupabase(pagesServies);
}

function roleJeton(j) {
  try { return JSON.parse(Buffer.from(j.split('.')[1].replace(/-/g, '+').replace(/_/g, '/'), 'base64').toString('utf8')).role || null; } catch { return null; }
}

async function collecterSupabase(pagesServies) {
  if (!pagesServies.length) { SOURCES.push(['Supabase', 'INDISPONIBLE', 'aucune page servie lue : hôte et clé inconnus']); indispo('P4', 'aucune page servie lue (P1)'); return; }
  const parHote = new Map();  // hôte → { cle, tables: Map(table → Set(pages)), dyn, pagesSansTable }
  const alertes = [];
  for (const p of pagesServies) {
    const s = SERVI[p];
    const hotes = [...new Set([...s.matchAll(/https:\/\/([a-z0-9]+)\.supabase\.co/g)].map((m) => m[0]))];
    if (!hotes.length) continue;
    const jetons = [...new Set(s.match(/eyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}/g) || [])];
    let cleAnon = null;
    for (const j of jetons) { const r = roleJeton(j); if (r === 'anon') cleAnon ??= j; else if (r) alertes.push(`jeton de rôle \`${r}\` présent dans la page servie \`${p}\` — non utilisé ici`); }
    const noms = [...s.matchAll(/\bsbGet\(\s*['"`]([a-z0-9_]+)|\.from\(\s*['"`]([a-z0-9_]+)|\/rest\/v1\/([a-z0-9_]+)/g)].map((m) => m[1] || m[2] || m[3]);
    // appel dont le premier argument n'est pas une chaîne littérale — la définition de sbGet exclue
    const dyn = (s.match(/(?<!function\s+)\bsbGet\(\s*(?!['"]|`[a-z0-9_]|\))/g) || []).length;
    for (const h of hotes) {
      if (!parHote.has(h)) parHote.set(h, { cle: null, tables: new Map(), dyn: 0, pagesSansTable: [] });
      const e = parHote.get(h); e.cle ??= cleAnon; e.dyn += dyn;
      if (!noms.length) e.pagesSansTable.push(p);
      for (const t of noms) { if (!e.tables.has(t)) e.tables.set(t, new Set()); e.tables.get(t).add(p); }
    }
  }
  if (!parHote.size) { SOURCES.push(['Supabase', 'sans objet', 'aucune page servie ne cite d’hôte Supabase']); champ('P4', 'OK', 'aucune page servie ne cite d’hôte Supabase.'); return; }
  const blocs = []; let incertain = alertes.length > 0; let joint = false;
  for (const [h, e] of parHote) {
    if (!e.cle) { blocs.push(`**${h}** — aucune clé \`anon\` dans les pages qui le citent : comptes non demandés.`); incertain = true; continue; }
    const rows = await parLots([...e.tables.keys()].sort(), 4, async (t) => {
      const r = await http(`${h}/rest/v1/${t}?select=*`, { method: 'HEAD', headers: { apikey: e.cle, Authorization: `Bearer ${e.cle}`, Prefer: 'count=exact' } });
      if (r.status) joint = true;
      const n = r.headers?.get?.('content-range')?.match(/\/(\d+)$/)?.[1];
      let vis;
      if (r.status === 200 || r.status === 206) vis = n === undefined ? 'compte non renvoyé' : n === '0' ? '**0 visible** — ne prouve pas une table vide' : `**${n}**`;
      else if (r.status === 401 || r.status === 403) vis = `**non lisible par un visiteur** (HTTP ${r.status})`;
      else if (r.status === 404) vis = '**absente de l’API** (HTTP 404)';
      else vis = r.status ? `HTTP ${r.status}` : `injoignable (${r.erreur})`;
      return `| \`${t}\` | ${[...e.tables.get(t)].map((x) => `\`${x}\``).join(', ')} | ${vis} |`;
    });
    blocs.push(`**${h}**\n\n| table | citée par | lignes visibles avec la clé anon servie |\n|---|---|---|\n${rows.join('\n')}`
      + `\n\nAppels \`sbGet(…)\` dont la table n’est pas une chaîne littérale : ${e.dyn}${e.dyn ? ' — leurs tables échappent à cette liste' : ''}.`
      + (e.pagesSansTable.length ? `\n\nPages citant l’hôte sans table nommée : ${e.pagesSansTable.map((x) => `\`${x}\``).join(', ')}.` : ''));
  }
  if (alertes.length) blocs.push(`**⚠ ${alertes.join(' ; ')}.**`);
  SOURCES.push(['Supabase', joint ? 'joignable' : 'ÉCHEC', `hôte(s) lu(s) dans les pages servies : ${[...parHote.keys()].join(', ')} · clé : celle servie aux visiteurs (rôle anon), jamais imprimée`]);
  if (!joint) indispo('P4', 'Supabase injoignable (voir Sources)');
  else champ('P4', incertain ? 'INCERTAIN' : 'OK', blocs.join('\n\n'), { requete: 'HEAD <hôte>/rest/v1/<table>?select=* avec Prefer: count=exact — aucun corps transféré', raison: incertain ? (alertes.length ? 'jeton non anon présent dans une page servie' : 'un hôte sans clé anon') : null });
}

// ─── registre ADR ─────────────────────────────────────────────────────────────────────────
function collecterRegistre() {
  if (!ARGS.registre) { SOURCES.push(['Registre ADR', 'non fourni', 'aucun --registre : le registre ne vit pas dans ce dépôt']); indispo('R1', 'aucun registre fourni (--registre) — il ne vit pas dans ce dépôt'); return; }
  const f = path.resolve(ARGS.registre);
  if (!existsSync(f)) { SOURCES.push(['Registre ADR', 'ÉCHEC', 'fichier fourni introuvable']); indispo('R1', 'fichier fourni par --registre introuvable'); return; }
  const racine = cmd('git', ['rev-parse', '--show-toplevel'], path.dirname(f));
  const maxAdr = (txt) => { const n = [...txt.matchAll(/^###\s+ADR-(\d+)/gm)].map((m) => +m[1]); return n.length ? Math.max(...n) : null; };
  const fmt = (n) => `ADR-${String(n).padStart(3, '0')}`;
  if (!racine) {
    const n = maxAdr(readFileSync(f, 'utf8'));
    SOURCES.push(['Registre ADR', 'lu hors Git', 'fichier fourni, hors dépôt Git']);
    if (n === null) indispo('R1', 'aucune entrée `### ADR-NNN` dans le fichier fourni');
    else champ('R1', 'INCERTAIN', `**≥ ${fmt(n)}**`, { raison: 'fichier hors dépôt Git : sa fraîcheur est invérifiable' });
    return;
  }
  const rel = path.relative(racine, f).split(path.sep).join('/');
  let ref = cmd('git', ['symbolic-ref', '--short', 'refs/remotes/origin/HEAD'], racine);
  if (!ref) { const s = cmd('git', ['ls-remote', '--symref', 'origin', 'HEAD'], racine); const m = s && s.match(/ref:\s+refs\/heads\/(\S+)\s+HEAD/); ref = m ? `origin/${m[1]}` : null; }
  if (!ref) { SOURCES.push(['Registre ADR', 'ÉCHEC', 'branche par défaut du dépôt du registre indéterminable']); indispo('R1', 'branche par défaut du dépôt du registre indéterminable'); return; }
  const contenu = cmd('git', ['show', `${ref}:${rel}`], racine);
  if (contenu === null) { SOURCES.push(['Registre ADR', 'ÉCHEC', `fichier absent de ${ref}`]); indispo('R1', `le fichier fourni n’existe pas sur ${ref} (non suivi, ou sur une autre branche)`); return; }
  const n = maxAdr(contenu);
  const local = cmd('git', ['rev-parse', ref], racine);
  const distant = (cmd('git', ['ls-remote', 'origin', `refs/heads/${ref.replace(/^origin\//, '')}`], racine) || '').split(/\s/)[0] || null;
  const modif = cmd('git', ['log', '-1', '--format=%cI', ref, '--', rel], racine);
  const commun = cmd('git', ['rev-parse', '--git-common-dir'], racine);
  let dernierFetch = null;
  try { const fh = path.resolve(racine, commun || '.git', 'FETCH_HEAD'); if (existsSync(fh)) dernierFetch = iso(statSync(fh).mtime); } catch { /* inconnu */ }
  const ajoutSeul = /append-only|ajout seul/i.test(contenu);
  const borne = ajoutSeul ? 'le registre se déclarant en ajout seul, le vrai dernier numéro est au moins celui-ci' : 'le registre ne se déclare pas en ajout seul : même cette borne est incertaine';
  SOURCES.push(['Registre ADR', distant ? 'joignable' : 'distant injoignable', `fichier fourni par --registre (chemin non imprimé) · lu sur \`${ref}\`, pas sur la copie de travail`]);
  if (n === null) { indispo('R1', `aucune entrée \`### ADR-NNN\` sur ${ref}`); return; }
  const suffixe = `dernière modification du registre sur \`${ref}\` : ${modif ? iso(modif) : '?'}`;
  if (distant && local === distant) champ('R1', 'OK', `**${fmt(n)}** — \`${ref}\` identique au distant (vérifié par \`git ls-remote\` à la génération) · ${suffixe}.`, { requete: `git show ${ref}:<registre> ; git ls-remote origin` });
  else if (distant) champ('R1', 'INCERTAIN', `**≥ ${fmt(n)}** — \`${ref}\` est en retard sur le distant (dernier fetch : ${dernierFetch || 'inconnu'}) ; ${borne} · ${suffixe}.`, { requete: `git show ${ref}:<registre> ; git ls-remote origin`, raison: `réf locale ${ref} en retard sur le distant` });
  else champ('R1', 'INCERTAIN', `**≥ ${fmt(n)}** — distant injoignable, fraîcheur invérifiable (dernier fetch : ${dernierFetch || 'inconnu'}) ; ${borne} · ${suffixe}.`, { requete: `git show ${ref}:<registre>`, raison: 'distant injoignable' });
}

// ─── hors portée — et la raison de chaque exclusion, vérifiée quand elle peut l'être ──────
function horsPortee() {
  const calib = Object.entries(SERVI).filter(([, s]) => /function\s+calibrateRF\s*\(/.test(s)).map(([p]) => p);
  const raisonCalib = !Object.keys(SERVI).length
    ? 'raison non vérifiée à cette génération : aucune page servie lue'
    : calib.length
      ? `le k RF est calculé au démarrage, dans le navigateur, par \`calibrateRF()\` — présente dans la page servie ${calib.map((x) => `\`${x}\``).join(', ')}`
      : '**`calibrateRF()` n’est plus dans les pages servies : la raison de cette exclusion est peut-être périmée**';
  return [
    `**Valeurs de calibration live** — ${raisonCalib}. Aucune lecture statique ne les donne ; les obtenir demande d’exécuter l’application (harnais), ce que ce générateur ne fait pas.`,
    '**Ce qu’un visiteur voit à l’écran** — DOM, CSS, état JS : aucun navigateur n’est lancé.',
    '**Le contenu des tables Supabase** au-delà de ce que voit la clé anon, et toute requête qui ne nomme pas sa table littéralement.',
    '**La date à laquelle un check est devenu requis** — l’API de protection ne la donne pas.',
    '**Les fichiers servis hors de la racine et de `public/data/`.**',
    '**Un déploiement en cours** : seul le check-run de la tête est lu (D7).',
    '**Tout ce qui vit hors des dépôts et de la prod** : instructions de projet, mémoires, décisions non consignées.',
  ];
}

// ─── rendu ────────────────────────────────────────────────────────────────────────────────
function versionDuScript() {
  const h = cmd('git', ['log', '-1', '--format=%h', '--', MOI], ICI);
  const sale = cmd('git', ['status', '--porcelain', '--', MOI], ICI);
  if (!h) return 'hors dépôt ou non suivie';
  return sale ? `\`${h}\`, modifiée localement depuis` : `\`${h}\``;
}
function rendre() {
  const L = [];
  L.push(`# ÉTAT — mesure du ${iso(T0).slice(0, 10)} à ${iso(T0).slice(11)}`, '');
  L.push(`> **Ceci est une mesure datée, pas l’état présent.** Produite le ${iso(T0)} par \`scripts/${MOI}\` (version ${versionDuScript()})${DEPOT ? ` sur le dépôt \`${DEPOT}\`` : ''}${PROD ? ` et la prod ${PROD}` : ''}. Tout ce qui suit décrit le monde à cet instant-là.`);
  L.push('>');
  L.push('> Chaque champ porte un statut : **OK** — dérivé à la génération depuis la source nommée · **INCERTAIN** — dérivé, avec sa limite écrite à côté · **INDISPONIBLE** — non écrit, avec la raison. Aucun champ n’est complété de mémoire, et une liste vide est écrite vide, avec la requête qui l’a produite.');
  if (PROBA) { L.push('>'); L.push(`> **Ancienneté** — sur les 7 jours précédant la génération, depuis un instant pris au hasard, la tête de \`${BRANCHE}\` changeait dans l’heure ${PROBA.h1} % du temps, dans les 6 h ${PROBA.h6} %, dans les 24 h ${PROBA.h24} % (D2). Plus ce document est lu tard après sa génération, plus il a de chances de décrire une tête dépassée, et les champs de dépôt avec elle.`); }
  L.push('', '## Ce que ce générateur sait collecter', '', '**Tout champ absent de cette liste est hors de sa portée** — son absence ne signifie pas qu’il est vide.', '');
  L.push('| champ | quoi | source | méthode | ne mesure pas |', '|---|---|---|---|---|');
  for (const [id, quoi, src, meth, pas] of CATALOGUE) L.push(`| ${id} | ${quoi} | ${src} | ${meth} | ${pas} |`);
  L.push('', '## Sources, à la génération', '', '| source | état | détail |', '|---|---|---|');
  for (const [n, e, d] of SOURCES) L.push(`| ${n} | ${e} | ${d} |`);
  L.push('', 'Aucune source n’en remplace une autre : un champ dont la source a échoué sort INDISPONIBLE, jamais complété par une autre.');
  const section = (titre, ids) => {
    L.push('', `## ${titre}`);
    for (const id of ids) {
      const c = CHAMPS[id]; const nom = CATALOGUE.find((x) => x[0] === id)[1];
      L.push('', `### ${id} · ${nom} — ${c ? c.statut : 'INDISPONIBLE'}`, '');
      if (!c) { L.push('_non collecté (défaut du générateur)._'); continue; }
      if (c.corps) L.push(c.corps);
      if (c.raison) { if (c.corps) L.push(''); L.push(`_${c.statut === 'INDISPONIBLE' ? 'Raison' : 'Limite'} : ${c.raison}._`); }
      if (c.requete) L.push('', `<sub>requête : ${cell(c.requete)}</sub>`);
    }
  };
  section(`Dépôt${DEPOT ? ` — \`${DEPOT}\`` : ''}`, IDS_DEPOT);
  section(`Prod${PROD ? ` — ${PROD}` : ''}`, IDS_PROD);
  section('Registre ADR', ['R1']);
  L.push('', '## Hors de portée — déclaré, pour ne pas être deviné', '');
  for (const h of horsPortee()) L.push(`- ${h}`);
  const st = Object.values(CHAMPS).map((c) => c.statut);
  const bilan = `${st.filter((s) => s === 'OK').length} OK · ${st.filter((s) => s === 'INCERTAIN').length} INCERTAIN · ${st.filter((s) => s === 'INDISPONIBLE').length} INDISPONIBLE`;
  L.push('', '---', '', `_Bilan : ${bilan}. Générée en ${((Date.now() - T0) / 1000).toFixed(1)} s._`, '');
  return { texte: L.join('\n'), bilan };
}

// ─── exécution ────────────────────────────────────────────────────────────────────────────
await collecterDepot();
await collecterProd();
collecterRegistre();
const { texte, bilan } = rendre();
if (ARGS.sortie) writeFileSync(ARGS.sortie, texte, 'utf8'); else process.stdout.write(texte);
process.stderr.write(`ETAT : ${bilan} · sources : ${SOURCES.map(([n, e]) => `${n} ${e}`).join(', ')}\n`);
