// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Vérification lexicale i18n corse (bêta) contre INFCOR (ADECEC)
// Création 2026-06-10 · itération 3 (post feedback-002) : distinction
// « attesté-direct » (forme exacte rejouable dans INFCOR) vs « flexion-inférée »
// (forme régulière d'un lemme attesté, mais forme exacte NON rejouable).
// ═══════════════════════════════════════════════════════════════════════════
//
// Lit I18N_ENTRIES (app.html) + docs/i18n/verification_co.tokens.json, tokenise
// chaque chaîne CO, classe chaque mot de contenu, calcule le STATUT par chaîne.
// Écrit docs/i18n/verification_co.tsv (clé, statut, source, note).
//
// STATUT (du plus faible au plus fort) :
//   flaggé          : >=1 mot non attesté forme exacte / faux-sens / dialecte.
//   à confirmer     : >=1 mot non encore vérifié.
//   vérifié (flexion): tous les mots attestés, mais >=1 est une flexion-inférée
//                      (lemme attesté, forme exacte non rejouable telle quelle).
//   vérifié         : tous les mots de contenu attestés-DIRECT (forme exacte rejouable).
//
// Doctrine : aucune valeur inventée. « vérifié » n'est attribué que si CHAQUE mot
// est rejouable par forme exacte sur INFCOR. Usage : node scripts/verify_i18n_co.mjs
// ═══════════════════════════════════════════════════════════════════════════
import { readFile, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const html = await readFile(join(ROOT, 'app.html'), 'utf8');
const tok = JSON.parse(await readFile(join(ROOT, 'docs/i18n/verification_co.tokens.json'), 'utf8'));
const m = html.match(/\/\* I18N-CO-ENTRIES-BEGIN \*\/([\s\S]*?)\/\* I18N-CO-ENTRIES-END \*\//);
if (!m) { console.error('marqueurs I18N introuvables'); process.exit(1); }
const entries = JSON.parse(m[1]);

const BASE_SKIP = `u a i e o di da de à è in per cù con un una uni unu lu li la le d l n s c m t
si chì ùn ci se ellu ella elli più prima po quì sottu ch sì ma nant nant'à nantà du al à
stu sta sti sto so mo to tu noi voi me mi vi ti hè hà ha anu sò esse essa fà fa via tuttu tutta tutte tutti
ogni qual qualchì qualcosa qualchissia ciò chè què d'esse s'ellu d'apre d'attività d'acqua d'impattu
tellux corsica supabase anfr tdf edf sei brgm noaa emag igrf wmm rte asnr exem cartoradio osm ign onf rgpd`
  .split(/\s+/).filter(Boolean);
const SKIP = new Set([...BASE_SKIP, ...(tok.skip_extra || [])]);
const V = tok.verified || {};       // attesté-direct
const I = tok.inferred || {};       // flexion-inférée (lemme attesté)
const F = tok.flags || {};

function toks(co) {
  return (co || '').toLowerCase()
    .replace(/[\u{1F000}-\u{1FAFF}\u{2600}-\u{27BF}←-⇿■-◿★◆●✕→↓↑·…]/gu, ' ')
    .replace(/[0-9]+/g, ' ').replace(/[^\p{L}’' ]/gu, ' ')
    .split(/\s+/).map(t => t.replace(/^['’]+|['’]+$/g, '')).filter(t => t.length > 1);
}

let nV = 0, nVf = 0, nF = 0, nT = 0;
const lines = ['clé\tstatut\tsource\tnote'];
const worklist = new Map();
for (const [key, , , , co] of entries) {
  let flagged = false, unknown = false, hasInferred = false;
  const dIds = new Set(), iIds = new Set(), notes = [];
  for (const t of toks(co)) {
    if (SKIP.has(t)) continue;
    if (t in F) { flagged = true; notes.push(`${t} — ${F[t]}`); }
    else if (t in V) { dIds.add(V[t]); }
    else if (t in I) { hasInferred = true; iIds.add(I[t]); }
    else { unknown = true; worklist.set(t, (worklist.get(t) || 0) + 1); }
  }
  let statut, source;
  if (flagged) { statut = 'flaggé'; source = '— (cf. note)'; nF++; }
  else if (unknown) { statut = 'à confirmer'; source = '—'; nT++; }
  else if (hasInferred) {
    statut = 'vérifié (flexion)';
    source = (dIds.size ? `INFCOR ${[...dIds].sort((a,b)=>a-b).join(', ')} · ` : '') +
      `flexion: ${[...iIds].sort((a,b)=>a-b).join(', ')}`;
    notes.push('contient une/des flexion(s) régulière(s) d\'un lemme attesté ; forme exacte non rejouable telle quelle dans INFCOR.');
    nVf++;
  } else {
    statut = 'vérifié'; source = `INFCOR ${[...dIds].sort((a,b)=>a-b).join(', ')}`; nV++;
  }
  lines.push(`${key}\t${statut}\t${source}\t${notes.join(' || ')}`);
}
await writeFile(join(ROOT, 'docs/i18n/verification_co.tsv'), lines.join('\n') + '\n', 'utf8');
console.log(`STATUT : vérifié=${nV}  vérifié-flexion=${nVf}  flaggé=${nF}  à-confirmer=${nT}  (total=${entries.length})`);
console.log(`Lexique : ${Object.keys(V).length} formes attestées-direct, ${Object.keys(I).length} flexions-inférées, ${Object.keys(F).length} flaggées.`);
const wl = [...worklist.entries()].sort((a, b) => b[1] - a[1]);
if (process.argv.includes('--worklist')) console.log(wl.map(([t, f]) => `${f}\t${t}`).join('\n'));
