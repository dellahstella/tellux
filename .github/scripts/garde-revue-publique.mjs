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
// Une "surface publique" = tout fichier `*.html` À LA RACINE du dépôt, tel qu'il existe
// dans l'arbre Git au commit HEAD examiné. JAMAIS une liste en dur : recalculée à chaque
// exécution par `git ls-tree`, pour ne jamais dériver quand une page est ajoutée/retirée
// (même convention que scripts/generer_manifeste.mjs §5 / generer_etat.mjs P1 — "chaque
// *.html à la racine"). Si cette énumération échoue ou revient vide, le check ÉCHOUE
// explicitement (fail-closed) plutôt que de conclure silencieusement "aucune surface
// publique touchée".
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
//     n'importe quel nom de variable est couvert)
// Règle de prudence : en cas d'ambiguïté, le classifieur flag (faux positif accepté,
// faux négatif refusé). Les lignes de commentaire (JS `//`, `/* */` ; HTML `<!-- -->`
// sur une ligne entière) sont exclues — sinon ce garde serait rouge en permanence dans
// un dépôt qui commente abondamment.
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

function htmlTextNodeFlag(line) {
  const stripped = stripTags(line);
  return HAS_LETTER_RUN.test(stripped) ? stripped.trim().slice(0, 160) : null;
}

function visibleAttrFlag(line) {
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

function jsStringTextFlags(line) {
  const flags = [];
  let m;
  STRING_LITERAL_RE.lastIndex = 0;
  while ((m = STRING_LITERAL_RE.exec(line)) !== null) {
    const s = m[2];
    if (!s) continue;
    const containsTag = /<[a-zA-Z/][^>]*>/.test(s);
    const words = s.split(/\s+/).filter(w => /\p{L}{2,}/u.test(w));
    const looksLikeProse = words.length >= 2;
    if (containsTag || looksLikeProse) {
      if (!CODE_LIKE_RE.test(s.trim())) {
        flags.push(s.trim().slice(0, 160));
      } else if (containsTag) {
        // Une balise HTML explicite l'emporte toujours sur l'exclusion code-like
        // (un gabarit LEGEND_HTML peut être une chaîne courte contenant '<b>').
        flags.push(s.trim().slice(0, 160));
      }
    }
  }
  return flags;
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

  const changedFiles = (tryGit(['diff', '--name-only', `${base}...${head}`]) || '')
    .split('\n').map(s => s.trim()).filter(Boolean);

  const rootHtmlBase = listRootHtmlAt(base) || [];
  const allKnownRoot = new Set([...rootHtmlHead, ...rootHtmlBase]);
  const touchedPublic = changedFiles.filter(f => allKnownRoot.has(f) || ROOT_HTML_RE.test(f));

  // Une page publique touchée que l'énumération HEAD ne connaît PAS (renommage non
  // suivi, extension inattendue) : signalée, pas silencieusement ignorée.
  const unknownPublicTouch = touchedPublic.filter(f => ROOT_HTML_RE.test(f) && !rootHtmlHead.includes(f) && !rootHtmlBase.includes(f));

  if (touchedPublic.length === 0) {
    return { flags: [], touchedPublic: [], unknownPublicTouch: [], verdict: 'vert', reason: 'Aucune surface publique (*.html racine) touchée par ce diff.' };
  }

  const diffText = tryGit(['diff', '-U0', `${base}...${head}`, '--', ...touchedPublic]) || '';
  const changes = parseUnifiedDiff(diffText);

  const headContentCache = new Map();
  const baseContentCache = new Map();
  const headCtxCache = new Map();
  const baseCtxCache = new Map();

  const flags = [];

  for (const ch of changes) {
    if (isCommentOnly(ch.content)) continue;
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

  const washedFlags = washOutUnchangedContent(flags);

  const verdict = washedFlags.length > 0 ? (hasRevuePubliqueLine(prBody) ? 'vert' : 'rouge') : 'vert';
  return { flags: washedFlags, touchedPublic, unknownPublicTouch, verdict, revueLine: extractRevuePubliqueLine(prBody) };
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

  console.log(`Surfaces publiques (racine) au HEAD : ${result.touchedPublic?.length ?? 0} touchée(s) sur ce diff.`);
  if (result.unknownPublicTouch?.length) {
    console.log(`::error::Page(s) publique(s) touchée(s) hors classification (ni au BASE ni au HEAD connus) : ${result.unknownPublicTouch.join(', ')}`);
    process.exitCode = 1;
    return;
  }
  if (!result.flags || result.flags.length === 0) {
    console.log(result.reason || 'Aucun texte visible détecté dans ce diff.');
    console.log('Garde revue publique : OK (rien à revoir).');
    return;
  }

  console.log(`Extraits considérés comme du texte visible (${result.flags.length}) :`);
  for (const f of result.flags) {
    console.log(`  ${f.file}:${f.line} [${f.side === 'new' ? '+' : '-'}] (${f.kind}) ${JSON.stringify(f.extract)}`);
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
