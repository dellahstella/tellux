#!/usr/bin/env node
// Garde revue publique — détecte un changement de texte visible sur une surface publique
// et exige une ligne `Revue-publique: <référence>` dans le corps de la PR.
//
// POURQUOI CE CHECK EXISTE
// ------------------------
// Trois franchissements les 17 et 18 septembre 2026 (#1512, #1517, phrase Bouygues sur
// #1519) : du contenu public neuf a été mergé sans que la revue web préalable ait
// tranché, dans les trois cas par un jugement humain de bonne foi ("ce n'est pas du
// contenu neuf" / "c'est un déplacement mécanique"). Ce garde-fou ne juge plus : il
// détecte mécaniquement un changement de texte visible et exige une trace de revue,
// sans évaluer si la revue elle-même était pertinente ou complète (ça reste humain).
//
// PORTÉE (Étage 1) — surfaces publiques
// --------------------------------------
// Une "surface publique" = (a) tout fichier `*.html` À LA RACINE du dépôt, tel qu'il
// existe dans l'arbre Git au commit examiné (JAMAIS une liste en dur : recalculée à
// chaque exécution par `git ls-tree`, même convention que scripts/generer_manifeste.mjs
// §5 / generer_etat.mjs P1 — "chaque *.html à la racine") ; (b) tout fichier
// `public/data/*.json` (enfants directs, ajouté suite à revue Soleil du 2026-09-18,
// Q2 — du texte affiché vit aussi dans ces fichiers de données, pas seulement dans le
// HTML/JS). Si une énumération échoue ou revient vide (côté HTML), le check ÉCHOUE
// explicitement (fail-closed) plutôt que de conclure silencieusement "aucune surface
// publique touchée" — de même pour toute lecture de fichier ou tout git diff qu'on SAIT
// nécessaire une fois une surface publique repérée comme touchée (Q5, cf. analyze()).
//
// DÉTECTION (Étage 2) — texte visible dans le diff
// ---------------------------------------------------
// Heuristique, PAS un parseur HTML/JS complet — assumé et documenté (cf. note de portée
// en fin de fichier et livrable "ce que la garde ne couvre pas"). Couvre :
//   - nœuds de texte HTML (contenu entre balises contenant au moins une lettre)
//   - attributs visibles : title / alt / aria-label / placeholder (PAS href/src/class/
//     id/data-*/style — changer une URL ou un sélecteur ne déclenche pas ce garde)
//   - littéraux de chaîne JavaScript à l'intérieur d'un bloc <script>, si la chaîne
//     contient soit une balise HTML (gabarits type LEGEND_HTML), soit une suite de mots
//     qui ressemble à de la prose (tables i18n : I18N_ENTRIES, EN_STRINGS, RICH_HTML_EN,
//     LEGEND_HTML_EN, etc. — jamais nommées en dur : la détection est structurelle,
//     n'importe quel nom de variable est couvert) ; un littéral D'UN SEUL MOT est
//     couvert séparément (peu importe le compte de mots) quand il alimente une
//     assignation dont on sait structurellement qu'elle rend du texte à l'écran —
//     .textContent=/.innerText=/.innerHTML=, setAttribute(visible, …) — sinon un
//     littéral d'un seul mot ne franchit jamais le seuil de 2 mots de la détection
//     générale (cf. domTextSinkFlags())
// Règle de prudence : en cas d'ambiguïté, le classifieur flag (faux positif accepté,
// faux négatif refusé). Les lignes de commentaire (JS `//`, `/* */` ; HTML `<!-- -->`
// sur une ligne entière) sont exclues — sinon ce garde serait rouge en permanence dans
// un dépôt qui commente abondamment.
//
// COUCHE COMPLÉMENTAIRE — lexique de termes verrouillés (revue Soleil 2026-09-18,
// point 1/2) : au-dessus de ce qui précède, tout terme listé dans
// garde-revue-publique-lexique.json déclenche un flag dès qu'il apparaît/disparaît sur
// une ligne changée ou une valeur JSON — INDÉPENDAMMENT du mécanisme (script, style,
// balisage statique, JSON) et INDÉPENDAMMENT du compte de mots. Comble spécifiquement
// le faux négatif résiduel d'un littéral JS nu hors sink structurel (ex. `var X =
// 'seuil';` sans `.textContent=` ni balise) — le cas qui compte le plus, car c'est lui
// qui bascule un sens réglementaire/scientifique, pas un état d'UI. Cf. le fichier
// lexique pour la liste et sa portée volontairement restreinte.
//
// EXIGENCE (Étage 3) — ligne Revue-publique
// --------------------------------------------
// Si (et seulement si) Étage 2 a flaggé au moins un extrait : le corps de la PR doit
// contenir une ligne `Revue-publique: <référence>` (n'importe quelle référence non
// vide — ce garde ne juge pas la revue elle-même, seulement sa trace). Absente → échec.
//
// LECTURE SEULE — ce script n'écrit rien sur le dépôt, n'appelle aucune API en écriture.

import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

const VISIBLE_ATTRS = ['title', 'alt', 'aria-label', 'placeholder'];
const ROOT_HTML_RE = /^[^/]+\.html$/;
// public/data/*.json : ajouté suite à la revue Soleil du 2026-09-18 (Q2) — du texte
// affiché par les pages publiques vit dans ces fichiers de données (labels, libellés),
// pas seulement dans le HTML/JS. Volontairement restreint aux enfants DIRECTS de
// public/data/ (pas les sous-dossiers type public/data/corse/*.geojson, hors périmètre
// de la demande — cf. note de portée en fin de fichier).
const JSON_DATA_RE = /^public\/data\/[^/]+\.json$/;

// Lexique de termes verrouillés (revue Soleil 2026-09-18, point 2) : détection
// INDÉPENDANTE du mécanisme de rendu et du compte de mots (donc du faux négatif Q1
// résiduel sur un littéral JS nu hors sink structurel) — cf. garde-revue-publique-
// lexique.json pour la provenance, la portée volontairement restreinte, et comment
// l'amender. Chargé une fois, jamais depuis le contenu diffé lui-même (c'est une
// config de la garde, pas du contenu du dépôt examiné).
const LEXICON_PATH = new URL('./garde-revue-publique-lexique.json', import.meta.url);
function loadLexiconTerms() {
  try {
    const raw = readFileSync(LEXICON_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed.termes) ? parsed.termes.filter(t => typeof t === 'string' && t.trim()) : [];
  } catch {
    // Fichier absent/invalide : dégrade vers un lexique vide plutôt que fail-closed —
    // ce n'est qu'une couche COMPLÉMENTAIRE à la détection heuristique principale
    // (Étage 2), pas la seule protection ; ne pas geler toute PR pour un lexique cassé.
    return [];
  }
}
const LEXICON_TERMS = loadLexiconTerms();

// Construit un motif par terme : limites de mot conscientes de l'unicode (les
// termes accentués comme "référence" ne passent pas par \b, qui ne connaît que
// [A-Za-z0-9_]) ; espaces flexibles pour les termes à plusieurs mots ("niveau de
// référence"). Insensible à la casse.
function buildLexiconRegexes(terms) {
  return terms.map(term => {
    const escaped = term.trim().split(/\s+/).map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('\\s+');
    // `_` compte comme caractère de mot (comme \w) en plus des lettres/chiffres unicode
    // — sinon un identifiant JS/CSS type `.seuil_legal_vm` (réel, app.html:14524)
    // matcherait "seuil" comme terme isolé alors que c'est un identifiant, pas du texte.
    return { term, re: new RegExp(`(?<![\\p{L}\\d_])${escaped}(?![\\p{L}\\d_])`, 'giu') };
  });
}
const LEXICON_REGEXES = buildLexiconRegexes(LEXICON_TERMS);

// Renvoie une entrée par OCCURRENCE trouvée (pas par terme unique) — pour que le
// comptage multiset de washOutUnchangedContent (déjà testé, Q3) s'applique ici
// exactement comme aux autres kinds : un terme verrouillé simplement déplacé dans
// le même fichier ne doit pas se compter comme un changement.
export function lexiconTermFlags(text) {
  const found = [];
  for (const { term, re } of LEXICON_REGEXES) {
    re.lastIndex = 0;
    let m;
    while ((m = re.exec(text)) !== null) {
      found.push(term);
      if (m.index === re.lastIndex) re.lastIndex++; // garde-fou boucle infinie sur motif vide
    }
  }
  return found;
}

function git(args) {
  return execFileSync('git', args, { encoding: 'utf8', maxBuffer: 1024 * 1024 * 64 });
}

function tryGit(args) {
  try { return git(args); } catch { return null; }
}

function listRootHtmlAt(ref) {
  const out = tryGit(['ls-tree', '-r', '--name-only', ref]);
  if (out == null) return null;
  return out.split('\n').map(s => s.trim()).filter(Boolean).filter(p => ROOT_HTML_RE.test(p));
}

function listJsonDataAt(ref) {
  const out = tryGit(['ls-tree', '-r', '--name-only', ref]);
  if (out == null) return null;
  return out.split('\n').map(s => s.trim()).filter(Boolean).filter(p => JSON_DATA_RE.test(p));
}

// Parcourt une valeur JSON déjà parsée et collecte toutes les chaînes-feuilles
// (valeurs string, à n'importe quelle profondeur — objets et tableaux). Les CLÉS ne
// sont jamais collectées (ce sont des identifiants, pas du texte affiché).
function collectJsonStrings(value, out) {
  if (typeof value === 'string') { out.push(value); return; }
  if (Array.isArray(value)) { for (const v of value) collectJsonStrings(v, out); return; }
  if (value && typeof value === 'object') { for (const v of Object.values(value)) collectJsonStrings(v, out); }
}

function fileAt(ref, path) {
  return tryGit(['show', `${ref}:${path}`]);
}

// Balaye un contenu de fichier ligne par ligne, renvoie deux tableaux booléens
// (script/style) où ctx[i] = true si la ligne (1-indexée) i est à l'intérieur du
// bloc correspondant. Heuristique ligne-à-ligne (pas de parseur) : une balise
// d'ouverture et de fermeture sur la même ligne se neutralise (bloc en ligne
// unique, hors scope de la détection dédiée — le contenu entre les deux passe par
// la voie "texte HTML" générique à la place, ce qui reste conservateur).
//
// <style> est trackée séparément de <script> : sans ce troisième état, une règle
// CSS ("margin-bottom: 16px;", ".page-header-top {") est un nœud-texte-HTML au
// sens de la détection générique (lettres présentes hors balises) — faux positif
// massif sur tout commit touchant un bloc <style> (le dépôt en a beaucoup, un par
// page). À l'intérieur de <style>, seul `content:"…"`/`content:'…'` (texte
// injecté par CSS via ::before/::after, seul mécanisme CSS qui rend du texte
// visible) reste vérifié — testé par jsStringTextFlags sur ce cas précis, cf.
// analyze().
function computeBlockContexts(content) {
  if (content == null) return { script: [], style: [] };
  const lines = content.split('\n');
  const script = new Array(lines.length + 1).fill(false);
  const style = new Array(lines.length + 1).fill(false);
  let inScript = false, inStyle = false;
  for (let i = 1; i <= lines.length; i++) {
    const line = lines[i - 1];
    script[i] = inScript;
    style[i] = inStyle;
    const sOpens = (line.match(/<script\b[^>]*>/gi) || []).length;
    const sCloses = (line.match(/<\/script\s*>/gi) || []).length;
    if (sOpens > sCloses) inScript = true;
    else if (sCloses > sOpens) inScript = false;
    const yOpens = (line.match(/<style\b[^>]*>/gi) || []).length;
    const yCloses = (line.match(/<\/style\s*>/gi) || []).length;
    if (yOpens > yCloses) inStyle = true;
    else if (yCloses > yOpens) inStyle = false;
  }
  return { script, style };
}

const CSS_CONTENT_PROP_RE = /\bcontent\s*:\s*(["'])((?:\\.|(?!\1)[^\\])*)\1/g;

function cssContentPropertyFlags(line) {
  const flags = [];
  let m;
  CSS_CONTENT_PROP_RE.lastIndex = 0;
  while ((m = CSS_CONTENT_PROP_RE.exec(line)) !== null) {
    const s = m[2];
    if (HAS_LETTER_RUN.test(s)) flags.push(s.trim().slice(0, 160));
  }
  return flags;
}

function isCommentOnly(line) {
  const t = line.trim();
  if (t === '') return true;
  if (t.startsWith('//')) return true;
  if (t.startsWith('/*') || t.startsWith('*') || t.endsWith('*/')) return true;
  if (t.startsWith('<!--') && t.endsWith('-->')) return true;
  return false;
}

function stripTags(line) {
  return line.replace(/<[^>]*>/g, ' ');
}

// Au moins une lettre Unicode (couvre les accents français) dans le texte hors balises.
const HAS_LETTER_RUN = /\p{L}{2,}/u;

export function htmlTextNodeFlag(line) {
  const stripped = stripTags(line);
  return HAS_LETTER_RUN.test(stripped) ? stripped.trim().slice(0, 160) : null;
}

export function visibleAttrFlag(line) {
  const re = new RegExp(`\\b(${VISIBLE_ATTRS.join('|')})\\s*=\\s*(["'])([\\s\\S]*?)\\2`, 'i');
  const m = line.match(re);
  return m ? `${m[1]}="${m[3]}"` : null;
}

// Chaînes JS candidates : simple/double quote ou template literal, non vide.
const STRING_LITERAL_RE = /(["'`])((?:\\.|(?!\1)[^\\])*)\1/g;

// Exclusions "code évident" : couleur hex, chemin/URL, identifiant nu (sans espace),
// nombre/unité, clé i18n courte type snake_case — pour garder une précision minimale
// sur les faux positifs, sans jamais exclure une chaîne qui contiendrait une balise
// ou une suite de mots façon prose (ces deux inclusions passent AVANT ces exclusions).
const CODE_LIKE_RE = /^(#[0-9a-fA-F]{3,8}|https?:\/\/\S*|\.?\/\S*|#[\w-]+|[\w-]+\.(png|jpg|jpeg|svg|json|geojson|js|css|html)|[a-zA-Z_][\w-]*|[\d.]+%?|[a-zA-Z]{1,3})$/;

// Assignations/appels DOM dont on SAIT structurellement qu'ils rendent du texte à
// l'écran : .textContent=/.innerText=/.innerHTML= et setAttribute() sur l'un des
// 4 attributs visibles. Flagués quel que soit le nombre de mots (même un seul) —
// contrairement à la détection générale ci-dessous qui exige ≥2 mots pour limiter
// le bruit sur les innombrables littéraux d'UN mot qui sont des valeurs d'état
// interne (ex. 'loading'/'error'/'active'), pas du texte affiché. Ici la structure
// de l'appel lève l'ambiguïté : un seul mot suffit. Cas réel qui a motivé cet ajout
// (revue Soleil, PR #1522) : `lvEl.textContent='indisponible'` (app.html) — un mot,
// aucune balise, sous le seuil de 2 mots de la détection générale — manqué avant ce
// correctif, alors qu'une retouche comme celle de #1517 sur ce littéral serait
// exactement invisible pour le garde tel qu'il existait.
const DOM_TEXT_SINK_RE = /\.(?:textContent|innerText|innerHTML)\s*=\s*(["'`])((?:\\.|(?!\1)[^\\])*)\1|\.setAttribute\(\s*(["'])(title|alt|aria-label|placeholder)\3\s*,\s*(["'])((?:\\.|(?!\5)[^\\])*)\5\s*\)/g;

export function domTextSinkFlags(line) {
  const flags = [];
  let m;
  DOM_TEXT_SINK_RE.lastIndex = 0;
  while ((m = DOM_TEXT_SINK_RE.exec(line)) !== null) {
    const s = m[2] !== undefined ? m[2] : m[6];
    if (s != null && HAS_LETTER_RUN.test(s)) flags.push(s.trim().slice(0, 160));
  }
  return flags;
}

// Décision partagée « cette chaîne ressemble-t-elle à du texte affiché ? », utilisée
// à la fois pour les littéraux JS (jsStringTextFlags) et pour les valeurs-feuilles
// JSON de public/data/*.json (Q2, revue Soleil 2026-09-18) — même filtre partout,
// pour ne pas faire dériver deux heuristiques qui devraient dire la même chose.
export function isTextLikeString(s) {
  if (!s) return false;
  const containsTag = /<[a-zA-Z/][^>]*>/.test(s);
  const words = s.split(/\s+/).filter(w => /\p{L}{2,}/u.test(w));
  const looksLikeProse = words.length >= 2;
  if (!containsTag && !looksLikeProse) return false;
  // Une balise HTML explicite l'emporte toujours sur l'exclusion code-like (un
  // gabarit LEGEND_HTML peut être une chaîne courte contenant '<b>').
  if (containsTag) return true;
  return !CODE_LIKE_RE.test(s.trim());
}

export function jsStringTextFlags(line) {
  const flags = new Set();
  for (const f of domTextSinkFlags(line)) flags.add(f);

  let m;
  STRING_LITERAL_RE.lastIndex = 0;
  while ((m = STRING_LITERAL_RE.exec(line)) !== null) {
    const s = m[2];
    if (!s) continue;
    if (isTextLikeString(s)) flags.add(s.trim().slice(0, 160));
  }
  return [...flags];
}

// Parse un diff unifié (-U0) en lignes changées, avec leur numéro dans le fichier
// concerné (ancien pour '-', nouveau pour '+') et le nom du fichier.
function parseUnifiedDiff(diffText) {
  const changes = []; // {file, side:'old'|'new', lineNo, content}
  let file = null, oldLine = 0, newLine = 0;
  for (const raw of diffText.split('\n')) {
    if (raw.startsWith('+++ b/')) { file = raw.slice(6); continue; }
    if (raw.startsWith('--- ') || raw.startsWith('diff --git')) continue;
    const hunk = raw.match(/^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
    if (hunk) { oldLine = parseInt(hunk[1], 10); newLine = parseInt(hunk[2], 10); continue; }
    if (raw.startsWith('+') && !raw.startsWith('+++')) {
      changes.push({ file, side: 'new', lineNo: newLine, content: raw.slice(1) });
      newLine++;
    } else if (raw.startsWith('-') && !raw.startsWith('---')) {
      changes.push({ file, side: 'old', lineNo: oldLine, content: raw.slice(1) });
      oldLine++;
    } else if (raw.startsWith(' ')) {
      oldLine++; newLine++;
    }
  }
  return changes;
}

// Une ligne peut changer pour une raison invisible (un attribut non surveillé,
// un onclick, une classe) tout en portant, sur la MÊME ligne, un extrait de texte
// visible byte-identique avant/après — cas réel observé (app.html:2346, exclusion
// mutuelle hot/hotrf/elf, titre+texte ELF inchangés, seul le handler a bougé).
// Un extrait qui réapparaît à l'identique côté + après avoir disparu côté - (même
// fichier, même nature) n'est PAS un changement de texte visible : il a été
// retiré puis remis tel quel — un déplacement, par définition. Compense côté -
// et + à due proportion (extrait×N retiré, extrait×M ajouté → |N-M| flags nets,
// du côté qui l'emporte) plutôt que tout supprimer, pour ne pas masquer un ajout
// ou un retrait réel qui coexisterait avec des occurrences réellement stables.
function washOutUnchangedContent(flags) {
  const key = f => JSON.stringify([f.file, f.kind, f.extract]);
  const oldBuckets = new Map(), newBuckets = new Map();
  for (const f of flags) {
    const m = f.side === 'old' ? oldBuckets : newBuckets;
    const k = key(f);
    if (!m.has(k)) m.set(k, []);
    m.get(k).push(f);
  }
  const kept = [];
  const seenKeys = new Set([...oldBuckets.keys(), ...newBuckets.keys()]);
  for (const k of seenKeys) {
    const olds = oldBuckets.get(k) || [];
    const news = newBuckets.get(k) || [];
    const net = news.length - olds.length;
    if (net > 0) kept.push(...news.slice(0, net));
    else if (net < 0) kept.push(...olds.slice(0, -net));
    // net === 0 : entièrement compensé, rien retenu.
  }
  // Ordre d'origine (fichier:ligne) plutôt que l'ordre de bucket, pour un résumé lisible.
  const order = new Map(flags.map((f, i) => [f, i]));
  kept.sort((a, b) => (order.get(a) ?? 0) - (order.get(b) ?? 0));
  return kept;
}

export function analyze({ base, head, prBody }) {
  const rootHtmlHead = listRootHtmlAt(head);
  if (rootHtmlHead == null) {
    return { fatal: `Énumération des surfaces publiques (git ls-tree ${head}) a échoué — fail-closed.` };
  }
  if (rootHtmlHead.length === 0) {
    return { fatal: `Énumération des surfaces publiques (git ls-tree ${head}) est vide — fail-closed (surface indéterminable).` };
  }

  // Échec de `git diff --name-only` (base/head invalides, dépôt corrompu, etc.) :
  // AUPARAVANT défauté silencieusement en '' → aucun fichier touché → vert. Fail-closed
  // depuis la revue Soleil du 2026-09-18 (Q5) — un garde qui ne peut pas savoir ce qui a
  // changé ne peut pas honnêtement dire « rien n'a changé ».
  const nameOnlyOut = tryGit(['diff', '--name-only', `${base}...${head}`]);
  if (nameOnlyOut == null) {
    return { fatal: `Liste des fichiers changés (git diff --name-only ${base}...${head}) a échoué — fail-closed.` };
  }
  const changedFiles = nameOnlyOut.split('\n').map(s => s.trim()).filter(Boolean);

  // Échec de l'énumération BASE : même traitement fail-closed que HEAD (ci-dessus),
  // pour la même raison — un défaut silencieux vers [] masquerait une page publique
  // supprimée dans ce diff (elle n'apparaîtrait dans aucune des deux énumérations).
  const rootHtmlBase = listRootHtmlAt(base);
  if (rootHtmlBase == null) {
    return { fatal: `Énumération des surfaces publiques (git ls-tree ${base}) a échoué — fail-closed.` };
  }

  const allKnownRoot = new Set([...rootHtmlHead, ...rootHtmlBase]);
  const touchedPublicHtml = changedFiles.filter(f => allKnownRoot.has(f) || ROOT_HTML_RE.test(f));

  // Une page publique touchée que NI l'énumération HEAD NI l'énumération BASE ne
  // connaissent : signalée, pas silencieusement ignorée. Honnêteté sur sa portée
  // réelle (revue Soleil 2026-09-18, Q6) : depuis que les deux échecs d'énumération
  // ci-dessus (HEAD et BASE) sont eux-mêmes fail-closed, ce filtre est structurellement
  // INATTEIGNABLE en fonctionnement normal — tout fichier listé par `git diff
  // --name-only` existe par construction à BASE ou à HEAD (invariant git), et les deux
  // énumérations correspondantes, si elles ont réussi (sinon on ne serait pas ici),
  // sont exhaustives sur leur référence. Conservé comme redondance défensive (coût
  // nul) plutôt que retiré, au cas où une évolution future réintroduirait un chemin
  // d'échec asymétrique — mais la protection réelle contre « page inconnue de la
  // classification » tient aux deux `fatal` d'énumération ci-dessus, pas à ce filtre.
  const unknownPublicTouch = touchedPublicHtml.filter(f => ROOT_HTML_RE.test(f) && !rootHtmlHead.includes(f) && !rootHtmlBase.includes(f));

  // public/data/*.json (Q2, revue Soleil 2026-09-18) : même traitement fail-closed
  // que les surfaces HTML sur l'énumération, symétrique BASE/HEAD.
  const jsonDataHead = listJsonDataAt(head);
  if (jsonDataHead == null) {
    return { fatal: `Énumération de public/data/*.json (git ls-tree ${head}) a échoué — fail-closed.` };
  }
  const jsonDataBase = listJsonDataAt(base);
  if (jsonDataBase == null) {
    return { fatal: `Énumération de public/data/*.json (git ls-tree ${base}) a échoué — fail-closed.` };
  }
  const touchedJsonData = changedFiles.filter(f => JSON_DATA_RE.test(f));

  const touchedPublic = [...touchedPublicHtml, ...touchedJsonData];

  if (touchedPublic.length === 0) {
    return { flags: [], touchedPublic: [], unknownPublicTouch: [], verdict: 'vert', reason: 'Aucune surface publique (*.html racine, public/data/*.json) touchée par ce diff.' };
  }

  const headContentCache = new Map();
  const baseContentCache = new Map();
  const headCtxCache = new Map();
  const baseCtxCache = new Map();

  const flags = [];

  if (touchedPublicHtml.length > 0) {
    // Échec de `git diff -U0` UNE FOIS qu'on sait que des pages HTML publiques SONT
    // touchées : auparavant défauté vers '' → aucune ligne changée trouvée → vert,
    // alors qu'on SAIT qu'il y a un diff à lire. Fail-closed (Q5).
    const diffOut = tryGit(['diff', '-U0', `${base}...${head}`, '--', ...touchedPublicHtml]);
    if (diffOut == null) {
      return { fatal: `Lecture du diff (git diff -U0 ${base}...${head}) a échoué sur ${touchedPublicHtml.length} page(s) publique(s) pourtant touchée(s) — fail-closed.` };
    }
    const changes = parseUnifiedDiff(diffOut);
    analyzeHtmlChanges(changes, { base, head, headContentCache, baseContentCache, headCtxCache, baseCtxCache, flags });
  }

  if (touchedJsonData.length > 0) {
    const jsonFatal = analyzeJsonDataChanges(touchedJsonData, { base, head, jsonDataBase, jsonDataHead, flags });
    if (jsonFatal) return { fatal: jsonFatal };
  }

  const washedFlags = washOutUnchangedContent(flags);
  const verdict = washedFlags.length > 0 ? (hasRevuePubliqueLine(prBody) ? 'vert' : 'rouge') : 'vert';
  return { flags: washedFlags, touchedPublic, touchedPublicHtml, touchedJsonData, unknownPublicTouch, verdict, revueLine: extractRevuePubliqueLine(prBody) };
}

function analyzeHtmlChanges(changes, { base, head, headContentCache, baseContentCache, headCtxCache, baseCtxCache, flags }) {
  for (const ch of changes) {
    if (isCommentOnly(ch.content)) continue;

    // Lexique de termes verrouillés (point 2, revue Soleil 2026-09-18) : INDÉPENDANT
    // du mécanisme de rendu — appliqué au texte brut de la ligne, avant toute
    // classification script/style/HTML, avant tout filtre de compte de mots. Cf.
    // garde-revue-publique-lexique.json.
    for (const term of lexiconTermFlags(ch.content)) {
      flags.push({ file: ch.file, line: ch.lineNo, side: ch.side, kind: 'terme verrouillé', extract: term });
    }

    const ref = ch.side === 'new' ? head : base;
    const contentCache = ch.side === 'new' ? headContentCache : baseContentCache;
    const ctxCache = ch.side === 'new' ? headCtxCache : baseCtxCache;
    if (!contentCache.has(ch.file)) contentCache.set(ch.file, fileAt(ref, ch.file));
    if (!ctxCache.has(ch.file)) ctxCache.set(ch.file, computeBlockContexts(contentCache.get(ch.file)));
    const ctx = ctxCache.get(ch.file);
    const inScript = ctx.script[ch.lineNo] === true;
    const inStyle = ctx.style[ch.lineNo] === true;

    if (inScript) {
      const jsFlags = jsStringTextFlags(ch.content);
      for (const f of jsFlags) {
        flags.push({ file: ch.file, line: ch.lineNo, side: ch.side, kind: 'littéral JS texte', extract: f });
      }
    } else if (inStyle) {
      // CSS : seul `content:"…"` (::before/::after) rend du texte visible — tout le
      // reste (sélecteurs, propriétés, valeurs) n'est structurellement pas du texte.
      const cssFlags = cssContentPropertyFlags(ch.content);
      for (const f of cssFlags) {
        flags.push({ file: ch.file, line: ch.lineNo, side: ch.side, kind: 'CSS content: visible', extract: f });
      }
    } else {
      const attr = visibleAttrFlag(ch.content);
      if (attr) flags.push({ file: ch.file, line: ch.lineNo, side: ch.side, kind: 'attribut visible', extract: attr });
      const textNode = htmlTextNodeFlag(ch.content);
      if (textNode) flags.push({ file: ch.file, line: ch.lineNo, side: ch.side, kind: 'texte HTML', extract: textNode });
    }
  }
}

// public/data/*.json (Q2, revue Soleil 2026-09-18) : diff SÉMANTIQUE (parse + walk),
// pas ligne-à-ligne — un JSON peut être minifié sur une seule ligne, et même
// pretty-imprimé, une valeur déplacée par un reformatage ne doit pas se lire comme
// un changement. Chaque valeur-feuille candidate (isTextLikeString, même filtre que
// jsStringTextFlags) est poussée en side='old'/'new' avec line=null — netée ensuite
// par le MÊME washOutUnchangedContent() que les flags HTML/JS (comptage par
// occurrence, testé Q3 : une valeur déplacée sans changer nette à zéro, une valeur
// réellement ajoutée en plus d'un déplacement reste comptée).
// Renvoie une chaîne d'erreur fatale, ou null si tout s'est bien passé.
function analyzeJsonDataChanges(touchedJsonData, { base, head, jsonDataBase, jsonDataHead, flags }) {
  for (const f of touchedJsonData) {
    const existedAtBase = jsonDataBase.includes(f);
    const existedAtHead = jsonDataHead.includes(f);

    for (const [existed, ref, side] of [[existedAtBase, base, 'old'], [existedAtHead, head, 'new']]) {
      if (!existed) continue; // fichier ajouté/supprimé de ce côté : aucune chaîne de ce côté, normal.
      const content = fileAt(ref, f);
      if (content == null) {
        return `Lecture de ${f} (${ref}) a échoué alors que le fichier est connu à cette référence — fail-closed.`;
      }
      let parsed;
      try { parsed = JSON.parse(content); }
      catch { return `${f} n'est plus un JSON valide (${ref}) — fail-closed (diff de valeurs de texte impossible).`; }
      const strings = [];
      collectJsonStrings(parsed, strings);
      for (const s of strings) {
        if (isTextLikeString(s)) flags.push({ file: f, line: null, side, kind: 'valeur JSON texte', extract: s.trim().slice(0, 160) });
        // Lexique (point 2) : indépendant d'isTextLikeString — un code court comme
        // 'nSv' ne passerait jamais le filtre ≥2 mots ci-dessus, mais reste verrouillé.
        for (const term of lexiconTermFlags(s)) {
          flags.push({ file: f, line: null, side, kind: 'terme verrouillé', extract: term });
        }
      }
    }
  }
  return null;
}

function extractRevuePubliqueLine(body) {
  if (!body) return null;
  const m = body.match(/^Revue-publique:\s*(\S.*)$/mi);
  return m ? m[1].trim() : null;
}

function hasRevuePubliqueLine(body) {
  return extractRevuePubliqueLine(body) != null;
}

// --- CLI --------------------------------------------------------------------
function main() {
  const base = process.env.GRP_BASE || process.argv[2];
  const head = process.env.GRP_HEAD || process.argv[3] || 'HEAD';
  const prBody = process.env.GRP_PR_BODY ?? (process.argv[4] ? readFileSync(process.argv[4], 'utf8') : '');

  if (!base) {
    console.error('Usage: GRP_BASE=<sha> GRP_HEAD=<sha> [GRP_PR_BODY=...] node garde-revue-publique.mjs');
    process.exit(2);
  }

  const result = analyze({ base, head, prBody });

  if (result.fatal) {
    console.log(`::error::${result.fatal}`);
    console.log(result.fatal);
    process.exitCode = 1;
    return;
  }

  const nHtml = result.touchedPublicHtml?.length ?? 0;
  const nJson = result.touchedJsonData?.length ?? 0;
  console.log(`Surfaces publiques examinées : ${nHtml} page(s) HTML racine, ${nJson} fichier(s) public/data/*.json — ${result.touchedPublic?.length ?? 0} au total sur ce diff.`);
  if (result.unknownPublicTouch?.length) {
    console.log(`::error::Page(s) publique(s) touchée(s) hors classification (ni au BASE ni au HEAD connus) : ${result.unknownPublicTouch.join(', ')}`);
    process.exitCode = 1;
    return;
  }
  if (!result.flags || result.flags.length === 0) {
    // Résumé explicite même en vert (Q7, revue Soleil 2026-09-18) : un vert muet ne
    // permet à personne de repérer un vert invraisemblable (ex. 0 extrait sur une PR
    // qui touche visiblement `lyr_gammajrc_hint`).
    console.log(result.reason || `0 extrait de texte visible retenu sur ${result.touchedPublic?.length ?? 0} surface(s) publique(s) examinée(s).`);
    console.log('Garde revue publique : OK (rien à revoir).');
    return;
  }

  console.log(`Extraits considérés comme du texte visible (${result.flags.length}) :`);
  for (const f of result.flags) {
    const loc = f.line == null ? f.file : `${f.file}:${f.line}`;
    console.log(`  ${loc} [${f.side === 'new' ? '+' : '-'}] (${f.kind}) ${JSON.stringify(f.extract)}`);
  }

  if (result.revueLine) {
    console.log(`Ligne Revue-publique trouvée : "${result.revueLine}"`);
  } else {
    console.log('Aucune ligne "Revue-publique: <référence>" trouvée dans le corps de la PR.');
  }

  if (result.verdict === 'rouge') {
    console.log('::error::Texte visible modifié sur une surface publique sans ligne Revue-publique dans le corps de la PR.');
    process.exitCode = 1;
  } else {
    console.log('Garde revue publique : OK (ligne Revue-publique présente).');
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main();
}
