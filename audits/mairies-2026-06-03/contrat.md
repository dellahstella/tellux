# CONTRAT D'ITÉRATION — Reprise audit `mairies.html` (re-cadré 2026-06-03)

> À lire avec `PROTOCOLE_AUTO_ITERATION.md` à la racine du repo.
> Version d'origine archivée dans `contrat_initial_recu.md` du même dossier.

```
CHANTIER  : Reprise audit mairies.html — 3 onglets en production
AXE       : app
GÉNÉRATEUR: Code
ÉVALUATEUR: Code (session fraîche, mode Playwright)
DATE      : 2026-06-03
```

## OBJECTIF (1 phrase)

Valider en production les **3 onglets** de l'outil mairies — `Fiche commune` / `Générer un courrier` / `Cadre légal` (incluant la section interne « Checklist déploiement antenne ») — sur la base canonique `mairies.html`, après l'interruption due au crash MCP.

## DANS LE PÉRIMÈTRE

- Onglet **Générer un courrier** (export PDF via `pdfmake@0.2.12`, 6 modèles administratifs).
- Onglet **Cadre légal** incluant la section interne « Checklist déploiement antenne » (`<h3>` L574 dans le panneau `legal`).
- **Non-régression** de l'onglet `Fiche commune` (360 communes, ANFR live) déjà validé : vérifier qu'il marche toujours, sans le re-auditer en détail.

## HORS PÉRIMÈTRE

- Implémentation d'un export DOCX (le contrat initial le mentionnait — re-cadrage 2026-06-03 : la base canonique livre du PDF via pdfmake, et le périmètre « reprise d'audit » exclut toute nouvelle implémentation).
- Conversion de la « Checklist » en onglet séparé (la version actuelle l'intègre comme section `<h3>` dans `Cadre légal`).
- Refonte UI, nouvelles fonctionnalités, autres pages (`patrimoine.html`, `app.html`).
- Toute modification non strictement nécessaire à corriger un défaut détecté par l'évaluateur.

## CRITÈRES D'ACCEPTATION

Rubrique §5.1 du protocole (Fonctionnalité 0.35 / Non-régression 0.30 / Craft 0.20 / Robustesse 0.15) **plus** les spécificités falsifiables ci-dessous.

### Générer un courrier (PDF)

- Sélectionner une commune + un modèle de courrier (cards de `#mr-courriers-list`) rend correctement la preview HTML du courrier dans le panneau d'aperçu.
- Cliquer sur `#mr-btn-download` (« Télécharger le PDF ») déclenche un téléchargement réel — captable par `page.waitForEvent('download')`.
- Le PDF reçu est valide (header `%PDF-` en début de fichier, ouvrable par lecteur PDF, non corrompu).
- Le PDF contient les bonnes données de la commune sélectionnée (nom de commune, champs personnalisés saisis dans le formulaire).
- Lazy-load de `pdfmake` (~600 ko) + `vfs_fonts` (~200 ko) se déclenche uniquement au premier clic sur `#mr-btn-download` (vérifier réseau au boot : aucun fetch CDN pdfmake).
- Aucune erreur console pendant la sélection de modèle, le remplissage, la génération PDF.
- Les **6 modèles** de courriers (Mairie + Citoyen) se rendent tous correctement en preview HTML.

### Cadre légal (+ Checklist intégrée)

- L'onglet `legal` (panneau `data-panel="legal"`) s'affiche entièrement, contenu textuel et liens présents.
- La section « Checklist déploiement antenne » (`<h3 class="mr-legal-title">` ~L574) s'affiche dans le panneau `legal` et n'est pas vide.
- Les items de la checklist (à inventorier en première itération) sont visibles à l'écran. Si interactifs (cases à cocher) : leur état persiste au moins le temps d'une navigation aller-retour entre onglets dans la même session.
- Navigation entre sections internes du panneau `legal` (ancres internes si présentes) fonctionne sans erreur console.
- Les références juridiques mentionnées (Loi Abeille, articles du CGCT, etc.) sont présentes et lisibles.

### Non-régression Fiche commune

- L'onglet `fiche` charge bien les 360 communes corses.
- Sélection d'une commune affiche les données ANFR live correspondantes (compteur antennes, supports, etc.) — sans erreur console rouge.
- Le bandeau atypique du contrôle ANFR (`mr-atyp-link` L2155-2156) reste fonctionnel : les liens vers les autres onglets fonctionnent.

## PARAMÈTRES DE BOUCLE

```
SEUIL DE RÉUSSITE : 7.0 / 10 (pondéré)
MAX ITÉRATIONS    : 8
ESCALADE          : plateau (Δ < 0.3 sur 3 itérations)  → stop + RAPPORT_FINAL.md
                    OU instabilité MCP / crash session  → stop + rapport immédiat
```

## NOTE PLAYWRIGHT — capture du téléchargement PDF

L'export PDF est un téléchargement : l'évaluateur doit capter l'événement `download`, pas seulement cliquer.

```js
import { chromium } from '@playwright/test';
import fs from 'node:fs';

const browser = await chromium.launch();
const page = await browser.newPage();
const errors = [];
page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

await page.goto('http://localhost:3000/mairies.html', { waitUntil: 'networkidle' });

// 1) Onglet "Générer un courrier"
await page.click('.mr-tab[data-tab="courrier"]');

// 2) Sélectionner une commune + un modèle (sélecteurs à confirmer à l'audit)
//    Ex. : await page.selectOption('#mr-commune-select', 'Ajaccio');
//          await page.click('.mr-card[data-template="dim-info"]');
//          (remplir les champs autofill / requis)

// 3) Capter le téléchargement déclenché par #mr-btn-download
const [ download ] = await Promise.all([
  page.waitForEvent('download'),
  page.click('#mr-btn-download'),
]);
const dlPath = await download.path();
const dlName = download.suggestedFilename(); // doit se terminer par .pdf

// 4) Validation du PDF reçu
const head = fs.readFileSync(dlPath).subarray(0, 5).toString('ascii');
if (head !== '%PDF-') throw new Error('PDF header invalide : ' + head);

// 5) Présence du nom de commune dans le texte du PDF :
//    soit pdf-parse / pdfjs-dist côté Node, soit re-ouvrir le PDF dans la page
//    et lire le contenu via PDF.js. À expliciter en première itération.

console.log(JSON.stringify({
  download_filename: dlName,
  download_path: dlPath,
  errors_console: errors,
}, null, 2));

await browser.close();
```

> Si le crash MCP d'origine venait de la génération PDF lourde côté client (pdfmake + vfs_fonts), le flaguer en **Robustesse** et le noter dans le feedback plutôt que de relancer la boucle à l'aveugle.

---

## Journal de re-cadrage 2026-06-03

**Constat initial Code** : le contrat reçu (archivé en `contrat_initial_recu.md`) mentionne 4 onglets (dont un onglet *Checklist* séparé) et un export `.docx`. Inspection de `mairies.html` (base canonique, commit `1bae243` sur `main`) :

- 3 onglets DOM seulement : `data-tab="fiche"`, `data-tab="courrier"`, `data-tab="legal"` (L460-463).
- Export : **PDF** via `pdfmake@0.2.12` (commentaire L29 ; bouton L640 `onclick="downloadPdf()"` ; lazy-load L1180-1218). Aucune référence DOCX/JSZip/docx-templater dans le fichier.
- « Checklist déploiement antenne » = `<h3 class="mr-legal-title">` à L574, **section interne du panneau `legal`** (pas un onglet).

**Arbitrage Soleil 2026-06-03** : option « Re-cadrer » retenue (vs « implémenter DOCX + onglet Checklist »). Le présent contrat reflète la réalité du DOM ; aucune nouvelle fonctionnalité à implémenter.
