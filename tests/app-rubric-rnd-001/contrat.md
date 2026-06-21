# CONTRAT D'ITÉRATION — rnd-001 · Accessibilité `prefers-reduced-motion` (app.html)

> À lire avec `PROTOCOLE_AUTO_ITERATION.md` (§2 séparation, §4 boucle, §5.1 rubrique APP).
> Premier item de la file R&D (bootstrap). File normalement curée par Soleil, priorisée FEDER-first.

```
CHANTIER   : rnd-001 — respect de prefers-reduced-motion sur app.html
AXE        : app
GÉNÉRATEUR : Code (Claude Code) — branche claude/rnd-001-reduced-motion
ÉVALUATEUR : session FRAÎCHE distincte (Playwright headless, env custom) — NE corrige pas
DATE       : 2026-06-21
```

## OBJECTIF (1 phrase)

Faire en sorte que `app.html` respecte la préférence système « réduire les animations »
(`prefers-reduced-motion: reduce`) en neutralisant transitions et animations, **sans changer le
comportement par défaut** ni toucher aux zones gelées.

## CONTEXTE (constat générateur)

- `app.html` déclare **46 `transition:`, 3 `animation:`, 3 `@keyframes`** mais **0** prise en compte de
  `prefers-reduced-motion` (grep verbatim, 2026-06-21).
- Défaut d'accessibilité reconnu : **WCAG 2.1 SC 2.3.3 (Animation from Interactions)** / **RGAA 13.8**.
  Angle FEDER : conformité RGAA d'un service numérique public.

## DANS LE PÉRIMÈTRE

- Un seul bloc CSS **additif**, derrière `@media (prefers-reduced-motion: reduce)`, inséré en fin du bloc
  `<style>` principal (avant `</style>` ~L1171). Neutralise animations/transitions globalement
  (`animation-duration`/`transition-duration: 0.01ms !important`, `animation-iteration-count: 1`,
  `scroll-behavior: auto`). Durée 0.01ms (≠ 0) pour préserver les listeners `transitionend`.

## HORS PÉRIMÈTRE

- Toute modification du comportement **par défaut** (mode motion normal).
- Zones gelées : fonctions `calc*`, coordonnées GPS, formules zone GELÉE
  (`EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, `calcGammaAmbient`), données scientifiques
  (`SITES`, `CHURCHES`, `HYPOTHESES`, etc.).
- JS, données, autres pages (`patrimoine.html`, `mairies.html`…).
- `<img alt>` manquant sur la légende WMS BRGM (app.html:2259) → reporté **rnd-002** (hors périmètre ici).
- Toute autre amélioration a11y (gabarit single-concern).

## CRITÈRES D'ACCEPTATION — structure GATE-puis-SCORE (D-4 actée)

### Couche 1 — Gates binaires éliminatoires (évalués EN PREMIER ; un échec = FAIL immédiat, on ne calcule pas §5.1)

| Gate | Attendu | Méthode |
|---|---|---|
| **G1 Conformité doctrine** | ✅ N/A déclenché — la solution n'affirme **aucun bénéfice EM**, ne touche **aucun** contenu scientifique/mission. Changement purement CSS a11y. | Inspection : le diff ne touche que du CSS de présentation. |
| **G2 Intégrité citations §10** | ✅ N/A déclenché — **aucune** référence/citation/corpus ajoutée ou éditée. | Inspection : pas de DOI/source touchée → `verify_citation.py` non requis. |

> Les deux gates passent par **non-déclenchement** : la solution n'a pas de surface doctrine ni citations.
> C'est volontaire pour ce 1ᵉʳ cycle (démontrer le flux gate→score sur un candidat propre).

### Couche 2 — Score pondéré §5.1 (calculé seulement si G1 ∧ G2 passent)

Rubrique §5.1 verbatim : Fonctionnalité 0.35 · Non-régression données 0.30 · Craft/UX 0.20 · Robustesse 0.15.
**Seuil : 7.0 / 10 pondéré.**

**Checks falsifiables spécifiques rnd-001 (à mener par l'évaluateur, Playwright headless) :**

1. **Mode reduced-motion ACTIF** — `page.emulateMedia({ reducedMotion: 'reduce' })` puis charger `app.html` :
   sur un échantillon d'éléments animés/transitionnés (ex. `#legende-toggle`, `#legende-content`,
   `.sidebar-toggle`, un élément à `@keyframes`), `getComputedStyle(el).transitionDuration` et
   `animationDuration` doivent être **≈ 0s** (`0.01ms`/`0s`). → confirme que le bloc s'applique.
2. **Mode motion NORMAL (non-régression)** — `page.emulateMedia({ reducedMotion: 'no-preference' })` :
   les transitions d'origine restent **non nulles** (ex. `#legende-toggle` garde `transition` ~`.2s`).
   → confirme **zéro régression** du comportement par défaut.
3. **Boot moteur intact** — les **9 couches** chargent comme avant (le bloc CSS ne touche pas la donnée) ;
   indice dual, toggle légende, drill-down, dashboard conditions fonctionnent (régression §5.1 baseline).
4. **Console propre** — 0 erreur rouge au boot + après interaction, dans les deux modes (bruit CORS
   localhost filtré, cf. `eval-app-rubric.mjs`).
5. **CI** — `validate-code` (node --check + htmlhint) reste vert sur la PR.

> Outil disponible : `tests/blindage-harness/eval-app-rubric.mjs` encode déjà les sondes §5.1 (socle de
> régression). L'évaluateur peut le **lancer comme outil** pour le signal de non-régression, puis ajouter
> les checks 1–2 spécifiques reduced-motion et rendre **son** verdict raisonné dans `feedback-NNN.md`.

## PARAMÈTRES DE BOUCLE

```
SEUIL DE RÉUSSITE : 7.0 / 10 pondéré (après passage des 2 gates)
MAX ITÉRATIONS    : 3   (provisoire — D-6 budget runs à confirmer Soleil)
ESCALADE          : plateau Δ<0.3 sur 3 itérations → stop + RAPPORT_FINAL.md
                    OU instabilité env / crash → stop + rapport immédiat
```

## NOTE PLAYWRIGHT — émulation reduced-motion

```js
import { chromium } from 'playwright';
const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ reducedMotion: 'reduce' }); // ou page.emulateMedia
const page = await ctx.newPage();
await page.goto(APP_URL, { waitUntil: 'domcontentloaded' });
const td = await page.evaluate(() =>
  getComputedStyle(document.querySelector('#legende-toggle')).transitionDuration);
// reduced → '0.00001s' / '0s' ; normal → '0.2s'
```

## SÉPARATION §2 (rappel)

Le générateur (ce commit) **ne s'évalue pas**. L'évaluateur tourne en **session fraîche**, écrit
`feedback-001.md` dans `tests/app-rubric-rnd-001/`, poste son verdict en commentaire de la PR, **ne corrige
rien**. FAIL → le générateur relit le feedback et itère. PASS → la PR draft **reste ouverte** ; merge = Soleil.
