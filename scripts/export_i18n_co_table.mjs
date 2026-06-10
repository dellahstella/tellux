// ═══════════════════════════════════════════════════════════════════════════
// Tellux — Export de la table de revue FR↔CO (i18n corsu bêta)
// Création : 2026-06-10 · feat/i18n-corsu-beta
// ═══════════════════════════════════════════════════════════════════════════
//
// Extrait le dictionnaire I18N_ENTRIES (JSON pur entre les marqueurs
// I18N-CO-ENTRIES-BEGIN/END du bloc i18n de app.html) et régénère la table
// réviseur-friendly docs/i18n/REVUE_FR_CO_app.md : une ligne par chaîne,
// colonnes clé / FR / CO, pour relecture par un bilingue corse.
//
// Usage :
//   node scripts/export_i18n_co_table.mjs
//
// La section « Chaînes différées » du fichier de sortie est PRÉSERVÉE entre
// les marqueurs <!-- DEFERRED-BEGIN --> / <!-- DEFERRED-END --> : seule la
// table générée est réécrite. Si le fichier n'existe pas encore, un squelette
// complet est créé.
// ═══════════════════════════════════════════════════════════════════════════

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = resolve(dirname(__filename), '..');
const APP_HTML = join(REPO_ROOT, 'app.html');
const OUT_MD = join(REPO_ROOT, 'docs', 'i18n', 'REVUE_FR_CO_app.md');

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

const html = await readFile(APP_HTML, 'utf8');
const m = html.match(/\/\* I18N-CO-ENTRIES-BEGIN \*\/([\s\S]*?)\/\* I18N-CO-ENTRIES-END \*\//);
if (!m) {
  console.error('ERREUR : marqueurs I18N-CO-ENTRIES introuvables dans app.html');
  process.exit(1);
}
const entries = JSON.parse(m[1]);
console.log(`${entries.length} entrées extraites de app.html`);

const rows = entries.map(([key, _sel, attr, fr, co]) =>
  `| \`${key}\` | ${ATTR_LABEL[attr] ?? attr} | ${mdEscape(fr)} | ${mdEscape(co)} |`
).join('\n');

const tableBlock = [
  '<!-- TABLE-BEGIN — section régénérée par scripts/export_i18n_co_table.mjs, ne pas éditer à la main -->',
  '',
  `**${entries.length} chaînes** traduites (chrome UI). Pour corriger une traduction : éditer la valeur CO`,
  'dans le bloc i18n de `app.html` (marqueurs `I18N-CO-ENTRIES-BEGIN/END`), puis relancer',
  '`node scripts/export_i18n_co_table.mjs` pour régénérer cette table.',
  '',
  '| Clé | Type | FR (source de vérité) | CO (à réviser) |',
  '|---|---|---|---|',
  rows,
  '',
  '<!-- TABLE-END -->',
].join('\n');

let out;
try {
  const existing = await readFile(OUT_MD, 'utf8');
  out = existing.replace(/<!-- TABLE-BEGIN[\s\S]*?<!-- TABLE-END -->/, tableBlock);
  if (out === existing && !existing.includes('<!-- TABLE-BEGIN')) {
    console.error('ERREUR : marqueurs TABLE-BEGIN/END absents du fichier existant');
    process.exit(1);
  }
} catch {
  // Première génération : squelette complet
  out = `# Revue bilingue FR ↔ CO — app.html (chrome UI, bêta)

**Statut** : bêta — accessible uniquement via \`app.html?lang=co\` (aucun bouton public).
Promotion en toggle visible seulement APRÈS validation par un relecteur bilingue corse.

**Doctrine** : FR est la source de vérité. Le corse ci-dessous est produit par modèle,
approximatif par construction — c'est précisément l'objet de cette table : chaque ligne
est un point de revue humaine. Le mécanisme i18n est additif et gardé par le FR verbatim
(si le FR de l'app dérive, la chaîne est sautée, jamais écrasée — voir \`window.__telluxI18n.skipped\`).

**Comment réviser** : corriger la colonne CO directement dans le bloc i18n de \`app.html\`
(entrées JSON entre \`I18N-CO-ENTRIES-BEGIN\` et \`I18N-CO-ENTRIES-END\`), puis régénérer
cette table avec \`node scripts/export_i18n_co_table.mjs\`.

---

## Table de revue

${tableBlock}

---

## Chaînes différées (hors périmètre de cette passe)

<!-- DEFERRED-BEGIN -->

Conformément au brief (chrome UI seulement), les chaînes suivantes restent en FR sous
\`?lang=co\` et sont listées ici pour les passes futures :

### Prose scientifique / canon (ne pas traduire sans validation scientifique)
- **Panneau Méthodologie & Audit** : tout le contenu (protocole de mesure en aveugle,
  incertitudes documentées, données validées, références peer-reviewed, roadmap).
  Seul le titre du panneau est traduit.
- **Modal À propos** : paragraphes du corps (ce que Tellux n'est pas, position épistémique,
  sources de données, note pondérations). Seuls le titre et les intertitres h4 sont traduits.
- **Modal Mode Expertise** : les 2 paragraphes d'avertissement (pondérations w_M/w_RF/w_I).
- **Panneau Expertise** : paragraphe d'introduction, note « pondérations provisoires »,
  ligne « Écart IGRF/WMM », note d'usage du bandeau.
- **Disclaimer** : les 3 textes de blocs (champs EM, contribuer, données & vie privée) —
  nuances épistémiques et RGPD.
- **Sidebar** : \`cat-header-text\` et les 3 \`subgroup-text\` (distinction couches
  calcul/contexte — nuance épistémique).
- **Guide d'interprétation rapide** (mode Prospecteur) : seuils Δ nT et leur lecture.
- **acq-target-hint** (fenêtres d'acquisition EM).
- **Panneau stats corpus** : titre (corpus CartoRadio EXEM), titre des barres, ligne
  laboratoire/conformité, libellés de données (min/max V/m · communes).
- **Tooltips spécifications matériaux** (σ, µr, dB RF des 17 mat-chips) + les 3
  intertitres de familles de matériaux.
- **Entrées du glossaire** (titres + corps) et guides pratiques du drawer — contenu
  pédagogique ; seul le chrome du drawer est traduit.

### Textes légaux (ne pas traduire sans validation juridique)
- **Consentement RGPD** du formulaire contribution (\`.rgpd-row\`) + lien « En savoir plus ».
- **Consentement capteurs** (\`.cap-consent\`).
- **Note protocole aveugle** (explication sous la case ★★★).

### Chaînes générées en JS (différées — passe future si CO promu)
- \`setStatus()\` : « N antennes » du header (10 sites d'appel).
- \`info()\` : ~41 messages contextuels de la barre info.
- \`alert()/confirm()\` : 13 messages.
- Popups Leaflet (contenus dynamiques par couche), \`updateLegendPanel()\`,
  textes interprétation grand public (\`ib-*-text\`, \`interp-conseil\`,
  \`interp-score-label\`), résumés conditions (\`cond-summary-*\` post-boot),
  \`#c-igrf-text\`, \`#csv-summary\`, \`#native-mag-status\`, \`#lightning-warn\`,
  libellés dynamiques du toggle sidebar.
- Rapport de site imprimable (\`exportTerrainReport\`, HTML généré).

### SEO / meta (hors bêta)
- \`<meta name="description">\`, balises OpenGraph/Twitter — pas de version CO
  tant que la langue n'est pas publique.

<!-- DEFERRED-END -->

---

*Généré par \`scripts/export_i18n_co_table.mjs\` — feat/i18n-corsu-beta, 2026-06-10.*
`;
}

await mkdir(dirname(OUT_MD), { recursive: true });
await writeFile(OUT_MD, out, 'utf8');
console.log(`Table écrite : ${OUT_MD}`);
