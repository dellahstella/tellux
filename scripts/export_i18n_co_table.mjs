// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Export de la table de revue FR↔CO (i18n corsu bêta)
// Création : 2026-06-10 · feat/i18n-corsu-beta
// Étendu 2026-06-10 : fusion du sidecar de vérification (colonnes STATUT/SOURCE).
// ═══════════════════════════════════════════════════════════════════════════
//
// Extrait le dictionnaire I18N_ENTRIES (JSON pur entre les marqueurs
// I18N-CO-ENTRIES-BEGIN/END du bloc i18n de app.html) et régénère la table
// réviseur-friendly docs/i18n/REVUE_FR_CO_app.md : une ligne par chaîne,
// colonnes clé / type / FR / CO / STATUT / SOURCE.
//
// Les colonnes STATUT/SOURCE proviennent de docs/i18n/verification_co.tsv
// (généré par scripts/verify_i18n_co.mjs). Si le sidecar est absent, ces
// colonnes restent vides — la table reste générable.
//
// Usage :
//   node scripts/verify_i18n_co.mjs        # (1) régénère le sidecar TSV
//   node scripts/export_i18n_co_table.mjs  # (2) régénère cette table
//
// La section « Chaînes différées » est PRÉSERVÉE entre les marqueurs
// <!-- DEFERRED-BEGIN --> / <!-- DEFERRED-END --> : seule la table est réécrite.
// ═══════════════════════════════════════════════════════════════════════════

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = resolve(dirname(__filename), '..');
const APP_HTML = join(REPO_ROOT, 'app.html');
const OUT_MD = join(REPO_ROOT, 'docs', 'i18n', 'REVUE_FR_CO_app.md');
const VERIF_TSV = join(REPO_ROOT, 'docs', 'i18n', 'verification_co.tsv');

const ATTR_LABEL = {
  '': 'texte',
  'tf': 'texte (1er nœud)',
  'doc-title': 'titre de page',
  'title': 'tooltip',
  'aria-label': 'aria-label',
  'placeholder': 'placeholder',
  'label': 'label (optgroup)',
};

function mdEscape(s) {
  return String(s).replace(/\|/g, '\\|').replace(/\r?\n/g, ' ');
}

// Sidecar de vérification (clé -> {statut, source}). Optionnel.
const verif = new Map();
try {
  const tsv = await readFile(VERIF_TSV, 'utf8');
  for (const line of tsv.split(/\r?\n/).slice(1)) {
    if (!line.trim()) continue;
    const [key, statut, source] = line.split('\t');
    verif.set(key, { statut: statut || '', source: source || '' });
  }
} catch { /* pas encore de passe de vérification */ }

const html = await readFile(APP_HTML, 'utf8');
const m = html.match(/\/\* I18N-CO-ENTRIES-BEGIN \*\/([\s\S]*?)\/\* I18N-CO-ENTRIES-END \*\//);
if (!m) {
  console.error('ERREUR : marqueurs I18N-CO-ENTRIES introuvables dans app.html');
  process.exit(1);
}
const entries = JSON.parse(m[1]);
console.log(entries.length + ' entrées extraites de app.html');

const rows = entries.map(([key, _sel, attr, fr, co]) => {
  const v = verif.get(key) || { statut: '', source: '' };
  return '| `' + key + '` | ' + (ATTR_LABEL[attr] ?? attr) + ' | ' + mdEscape(fr) + ' | ' + mdEscape(co) + ' | ' + mdEscape(v.statut) + ' | ' + mdEscape(v.source) + ' |';
}).join('\n');

const tableBlock = [
  '<!-- TABLE-BEGIN — section régénérée par scripts/export_i18n_co_table.mjs, ne pas éditer à la main -->',
  '',
  '**' + entries.length + ' chaînes** traduites (chrome UI). Pour corriger une traduction : éditer la valeur CO',
  'dans le bloc i18n de `app.html` (marqueurs `I18N-CO-ENTRIES-BEGIN/END`), puis relancer',
  '`node scripts/verify_i18n_co.mjs` puis `node scripts/export_i18n_co_table.mjs`.',
  '',
  'Colonnes STATUT/SOURCE = passe de vérification lexicale contre INFCOR (ADECEC), cf.',
  '`scripts/verify_i18n_co.mjs` et `docs/i18n/co-verification-2026-06-10/`. STATUT : `vérifié`',
  '(tous les mots de contenu attestés-DIRECT, forme exacte rejouable), `vérifié (flexion)` (tous',
  '  attestés mais >=1 flexion régulière d\'un lemme attesté, forme exacte non rejouable), `flaggé`',
  '  (au moins un mot non attesté / faux-sens /',
  'dialecte — voir `FLAGGED_CO_NATIF.md`), `à confirmer` (au moins un mot non encore vérifié cette',
  'passe). SOURCE = id(s) unique INFCOR (citables, rejouables).',
  '',
  '| Clé | Type | FR (source de vérité) | CO (à réviser) | STATUT | SOURCE |',
  '|---|---|---|---|---|---|',
  rows,
  '',
  '<!-- TABLE-END -->',
].join('\n');

const existing = await readFile(OUT_MD, 'utf8');
const out = existing.replace(/<!-- TABLE-BEGIN[\s\S]*?<!-- TABLE-END -->/, tableBlock);
if (out === existing && !existing.includes('<!-- TABLE-BEGIN')) {
  console.error('ERREUR : marqueurs TABLE-BEGIN/END absents du fichier existant');
  process.exit(1);
}

await mkdir(dirname(OUT_MD), { recursive: true });
await writeFile(OUT_MD, out, 'utf8');
console.log('Table écrite : ' + OUT_MD);
