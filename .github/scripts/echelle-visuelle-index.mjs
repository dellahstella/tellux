#!/usr/bin/env node
// Garde-fou échelle visuelle de `index.html` — espacement, taille de police,
// graisse, rayon de bordure, ombre.
//
// POURQUOI CE CHECK EXISTE
// ------------------------
// La charte visuelle v1 a été appliquée à `index.html` (PR #1469 et suivantes,
// 2026-09-14/15) : espacements 4·8·12·16·24·32·48·64, tailles 12·14·16·20·32·44,
// graisses 400·500·600, rayons 0/4px (50% admis sur un objet circulaire), zéro
// ombre. Rien ne la gardait : la prochaine édition pouvait y introduire une
// valeur hors échelle sans que personne le voie avant une revue humaine — si
// elle avait lieu. Ce script automatise la vérification de présence.
//
// LE DOCUMENT DE CHARTE N'EST PAS DANS CE DÉPÔT
// ----------------------------------------------
// Les cinq ensembles ci-dessous (ECHELLE_*) sont des littéraux, dérivés de ce
// que `index.html` emploie réellement au moment où ce script a été écrit
// (vérifié par audit dédié, 2026-09-16, zéro écart) — pas une lecture d'un
// fichier de charte externe, absent de ce dépôt. Modifier ces littéraux est un
// arbitrage éditorial (Cran C), jamais un geste mécanique.
//
// CE QUE CE CHECK COUVRE
// -----------------------
// - Les propriétés margin*/padding*/gap (espacement), font-size (taille),
//   font-weight (graisse), border-radius (rayon), box-shadow (ombre, dont la
//   seule valeur admise est : aucune occurrence).
// - Dans TOUS les blocs <style> du fichier ET dans chaque attribut
//   style="..." inline — un contrôle qui ne lirait que les balises <style>
//   laisserait passer une valeur glissée dans un attribut inline (2 trouvés
//   dans le fichier au moment de l'écriture, aucun hors échelle).
// - Les variables :root (var(--x)) sont résolues avant comparaison : une
//   valeur exprimée via une variable est jugée sur ce qu'elle vaut, pas sur
//   sa forme d'écriture.
// - Le breakpoint 768px n'est PAS un chiffre de cette famille : @media(...)
//   n'est pas parcouru pour lui-même, mais les déclarations qu'il contient
//   LE SONT (même extraction que le reste du CSS) — une valeur d'espacement
//   ou de taille glissée dans un bloc @media est donc bien couverte.
//
// CE QUE CE CHECK NE COUVRE PAS — ÉNUMÉRÉ ICI POUR NE PAS SE PERDRE
// -------------------------------------------------------------------
// - Les 8 autres surfaces publiques du dépôt (app.html, cadre-scientifique.html,
//   methode-limites-transparence.html, mentions-legales.html, geomagnetisme.html,
//   mairies.html, radon.html, patrimoine.html) — aucune n'est lue. Neuf à
//   l'inventaire du 2026-09-15 ; huit depuis le retrait de
//   guide-et-glossaire.html (PR #1479, 2026-09-15).
// - La couleur (bordures, palette DA v2) — hors des cinq familles nommées ici.
// - Le nombre et la valeur des breakpoints (une seule valeur, 768px, est
//   attendue sur le dépôt) — ce script ne vérifie pas qu'aucun AUTRE seuil
//   n'existe, seulement que les déclarations à l'intérieur de chaque @media
//   restent sur l'échelle des cinq familles couvertes.
// - La hauteur de ligne et les largeurs de contenu (charte v1 §4 et §9).
// - Tout style injecté au runtime par le JavaScript de la page (la mini-carte
//   SVG du hero, notamment) — ce script lit le fichier statique, jamais le DOM
//   après exécution.
// - `calc()` : traité comme un token NON RECONNU dans les cinq familles
//   contrôlées → échec. Jamais évalué. Absent du fichier au 2026-09-16 (vérifié
//   avant d'écrire ce script) ; s'il apparaissait un jour, ce script le
//   refuserait plutôt que de deviner sa valeur résolue.
// - Toute unité autre que px (rem, em, %, vh, vw…) sur l'espacement, la taille
//   ou le rayon (hors 50% explicitement admis pour ce dernier) : traitée comme
//   une valeur NOUVELLE, donc un échec — pas une forme silencieusement
//   ignorée. Aucune occurrence au 2026-09-16 (vérifié avant d'écrire ce
//   script, cf. session du même jour).
// - Plancher de couverture (PLANCHER_DECLARATIONS) : un fichier qui ne
//   produirait presque plus de déclarations contrôlées (extraction cassée,
//   fichier tronqué) échoue au lieu de se lire, à tort, comme conforme —
//   même discipline que CONTRAST_MIN_NOEUDS dans contrast-panels.yml.
//
// DETECT-AND-SIGNAL, PAS DE RÉÉCRITURE
// --------------------------------------
// Ce script ne modifie jamais `index.html`. Il rapporte chaque écart avec son
// emplacement (propriété + valeur brute), jamais une chaîne interpolée
// pouvant masquer la valeur réelle. Sortie 0 si l'ensemble des valeurs
// employées est un sous-ensemble des cinq échelles ci-dessous ET qu'aucune
// occurrence de box-shadow n'existe ; sortie 1 sinon.
//
// NON REQUIS DANS CE LOT
// ------------------------
// Ce check tourne sur chaque PR mais n'entre pas dans
// `required_status_checks` de `main` à sa création (2026-09-16) — le passer
// requis est un arbitrage distinct, une fois quelques runs observés. Pas de
// filtre `paths:` sur son déclenchement (cf. `.github/workflows/`, fichier
// jumeau) : un check appelé à devenir requis qui ne se déclenche pas sur une
// partie des PR gèle le dépôt sans le moindre rouge visible
// (schema-payload-guard.yml et contrast-panels.yml documentent tous deux ce
// précédent, sous INS-007/ADR-067 et ADR-045).

import fs from 'node:fs';

const ECHELLE_ESPACEMENT = [4, 8, 12, 16, 24, 32, 48, 64];
const ECHELLE_TAILLE = [12, 14, 16, 20, 32, 44];
const ECHELLE_GRAISSE = [400, 500, 600];
const ECHELLE_RAYON_PX = [0, 4]; // + 50% admis sur un objet circulaire (charte v1 §5)

// Plancher de couverture (même discipline que CONTRAST_MIN_NOEUDS dans
// contrast-panels.yml) : 114 déclarations contrôlées mesurées le 2026-09-16.
// Un fichier tronqué, un bloc <style> mal fermé, ou une extraction cassée par
// un futur remaniement ferait tomber ce compte à (près de) zéro — un fichier
// qui ne dit plus rien ne doit jamais se lire comme un fichier conforme.
const PLANCHER_DECLARATIONS = 60;

const path = process.argv[2] || 'index.html';
if (!fs.existsSync(path)) {
  console.error(`échelle-visuelle-index : fichier introuvable : ${path}`);
  process.exit(1);
}
const html = fs.readFileSync(path, 'utf8');

// --- Extraction : tous les blocs <style> + tous les attributs style="..." inline ---
const styleBlocks = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(m => m[1]);
const inlineStyles = [...html.matchAll(/\sstyle="([^"]*)"/g)].map(m => m[1].replace(/;?\s*$/, ';'));
let css = styleBlocks.concat(inlineStyles).join('\n');

// @font-face ne porte pas d'usage visuel de graisse sur un élément rendu —
// seulement les graisses disponibles au chargement de la police. Exclu pour
// ne pas polluer la famille GRAISSE avec des déclarations qui n'en sont pas.
css = css.replace(/@font-face\s*\{[\s\S]*?\}/g, '');

// --- :root : table de résolution des var(--x) ---
const rootVars = {};
const rootMatch = css.match(/:root\s*\{([\s\S]*?)\}/);
if (rootMatch) {
  for (const m of rootMatch[1].matchAll(/--([\w-]+)\s*:\s*([^;]+);/g)) {
    rootVars[m[1]] = m[2].trim();
  }
}
const cssForDecls = css.replace(/:root\s*\{[\s\S]*?\}/, '');

function resolveToken(tok) {
  const m = tok.match(/^var\(--([\w-]+)\)$/);
  return (m && rootVars[m[1]] !== undefined) ? rootVars[m[1]] : tok;
}

// --- Déclarations sur les propriétés contrôlées ---
const CONTROLLED = /^(margin|padding|gap|font-size|font-weight|border-radius|box-shadow)(-(top|right|bottom|left))?$/;
const decls = [...cssForDecls.matchAll(/([\w-]+)\s*:\s*([^;{}]+);/g)]
  .map(m => ({ prop: m[1].trim(), value: m[2].trim() }))
  .filter(d => CONTROLLED.test(d.prop));

const findings = [];

for (const { prop, value } of decls) {
  if (prop === 'box-shadow') {
    findings.push({ famille: 'OMBRE', prop, value, motif: 'toute occurrence de box-shadow est refusée (charte v1 §6 : zéro ombre)' });
    continue;
  }

  if (/calc\s*\(/i.test(value)) {
    findings.push({ famille: familleDe(prop), prop, value, motif: 'calc() non pris en charge — token non reconnu, jamais évalué' });
    continue;
  }

  if (prop === 'font-weight') {
    const resolved = resolveToken(value);
    const n = parseFloat(resolved);
    if (Number.isNaN(n)) {
      findings.push({ famille: 'GRAISSE', prop, value, motif: `valeur non numérique (${resolved})` });
    } else if (!ECHELLE_GRAISSE.includes(n)) {
      findings.push({ famille: 'GRAISSE', prop, value, motif: `${n} hors échelle (${ECHELLE_GRAISSE.join('·')})` });
    }
    continue;
  }

  // Espacement, taille, rayon : décomposer en tokens (shorthand multi-valeurs)
  const tokens = value.split(/\s+/).map(resolveToken);
  for (const tok of tokens) {
    if (tok === '0' || tok === 'auto') continue;

    if (prop === 'border-radius') {
      if (tok === '50%') continue; // objet circulaire, charte v1 §5
      const m = tok.match(/^(-?\d+(?:\.\d+)?)px$/);
      if (!m || !ECHELLE_RAYON_PX.includes(parseFloat(m[1]))) {
        findings.push({ famille: 'RAYON', prop, value, motif: `token "${tok}" hors échelle (0, 4px, 50% sur objet circulaire)` });
      }
      continue;
    }

    if (prop === 'font-size') {
      const m = tok.match(/^(-?\d+(?:\.\d+)?)px$/);
      if (!m || !ECHELLE_TAILLE.includes(parseFloat(m[1]))) {
        findings.push({ famille: 'TAILLE', prop, value, motif: `token "${tok}" hors échelle (${ECHELLE_TAILLE.join('·')})` });
      }
      continue;
    }

    // margin*/padding*/gap
    const m = tok.match(/^(-?\d+(?:\.\d+)?)px$/);
    if (!m || !ECHELLE_ESPACEMENT.includes(parseFloat(m[1]))) {
      findings.push({ famille: 'ESPACEMENT', prop, value, motif: `token "${tok}" hors échelle (${ECHELLE_ESPACEMENT.join('·')})` });
    }
  }
}

function familleDe(prop) {
  if (/^(margin|padding|gap)/.test(prop)) return 'ESPACEMENT';
  if (prop === 'font-size') return 'TAILLE';
  if (prop === 'font-weight') return 'GRAISSE';
  if (prop === 'border-radius') return 'RAYON';
  if (prop === 'box-shadow') return 'OMBRE';
  return '?';
}

if (decls.length < PLANCHER_DECLARATIONS) {
  console.error(`échelle-visuelle-index : ${decls.length} déclaration(s) contrôlée(s) trouvée(s), sous le plancher de ${PLANCHER_DECLARATIONS}.`);
  console.error('Un fichier conforme ne se distingue pas d\'un fichier qui ne dit plus rien : extraction cassée (bloc <style> mal fermé ?), fichier tronqué, ou remaniement qui a fait fondre le nombre de déclarations contrôlées. Constat ambigu = échec, pas un passage silencieux.');
  process.exit(1);
}

if (findings.length === 0) {
  console.log(`échelle-visuelle-index : ${path} — conforme (${decls.length} déclaration(s) contrôlée(s), 0 écart).`);
  process.exit(0);
}

console.error(`échelle-visuelle-index : ${findings.length} écart(s) sur ${path}\n`);
for (const f of findings) {
  console.error(`  [${f.famille}] ${f.prop}: ${f.value}`);
  console.error(`    -> ${f.motif}\n`);
}
console.error('La garde refuse la valeur, elle ne la corrige pas. Ramener la déclaration sur l\'échelle, ou si la valeur doit réellement entrer dans le vocabulaire, en discuter avant de l\'écrire ici : ce script ne doit jamais être élargi en silence pour faire passer une PR.');
process.exit(1);
