# CONTRAT D'ITÉRATION — rnd-003 · Gating animations JS Leaflet sous `prefers-reduced-motion`

> À lire avec `PROTOCOLE_AUTO_ITERATION.md` (§2 séparation, §4 boucle, §5.1 rubrique APP).
> Item issu de la file R&D : issue #853. Origine = constat **F1** de l'éval rnd-001 (`feedback-001.md`, PR #852).

```
CHANTIER   : rnd-003 — animations JS Leaflet respectent prefers-reduced-motion (app.html)
AXE        : app
GÉNÉRATEUR : Code (Claude Code) — branche claude/rnd-003-leaflet-reduced-motion (base dev)
ÉVALUATEUR : session FRAÎCHE distincte (Playwright headless) — NE corrige pas
DATE       : 2026-06-21
DÉPEND DE  : rnd-001 (#852, mergé dans dev — CSS reduced-motion présent dans la base)
```

## OBJECTIF (1 phrase)

Faire respecter `prefers-reduced-motion` aux animations **JS Leaflet** d'`app.html` (que le CSS de rnd-001
ne peut pas gater), **sans changer le comportement par défaut** ni toucher aux zones gelées.

## CONTEXTE (audit générateur — surface complète, pas seulement L5091)

Inventaire des points d'animation Leaflet dans `app.html` (base dev) :
- **Init carte** `L.map('map',{maxZoom:20})` — `zoomAnimation`/`fadeAnimation`/`markerZoomAnimation` non spécifiés → **défaut `true`** (tout zoom/fondu s'anime).
- **`panBy({animate:true, duration:0.3})`** ×2 (recentrage popup dans le viewport, via `requestAnimationFrame`).
- **`panTo(...)`** (lien croisé Monticello) — `panTo` **anime par défaut**.
- **`setView([lat,lng], z)`** (deep-link `?c=&z=`) — peut paner-animer selon la distance.

## CE QUI A ÉTÉ FAIT (5 sites, +helper)

Helper lu à l'init **et** à chaque appel (pans = dynamiques) :
```js
const TLX_RM_QUERY = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
function tlxReduceMotion(){ return !!(TLX_RM_QUERY && TLX_RM_QUERY.matches); }
```
- Init carte : `zoomAnimation:!tlxReduceMotion(), fadeAnimation:…, markerZoomAnimation:…`.
- `panBy` ×2 : `{animate: !tlxReduceMotion(), duration: 0.3}`.
- `panTo` : `{animate: !tlxReduceMotion()}`.
- `setView` deep-link : `tlxReduceMotion() ? {animate:false} : undefined`.

**Invariant non-régression** : en mode normal, `!tlxReduceMotion() === true === défaut Leaflet`, et `setView`
reçoit `undefined` (= comportement d'origine). Le diff est donc un **no-op fonctionnel** hors reduced-motion.

## DANS LE PÉRIMÈTRE
Les 5 sites ci-dessus + le helper. Single-concern.

## HORS PÉRIMÈTRE
- Zones gelées (`calc*`, GPS scientifiques, formules GELÉE, données `SITES/CHURCHES/HYPOTHESES`). Aucune coordonnée modifiée — seul un drapeau `animate` est ajouté.
- Le CSS de rnd-001 (déjà dans la base), autres pages.
- **Limite assumée** : les options d'animation de carte (`zoomAnimation`…) sont lues **à l'init** ; un changement OS de la préférence **en cours de session** n'est honoré que pour les pans explicites (lus à l'appel), pas pour le zoom (Leaflet recalcule `_zoomAnimated` à l'init seulement). Edge-case rare, documenté.

## CRITÈRES D'ACCEPTATION — gate-puis-score (D-4)

### Couche 1 — Gates éliminatoires (évalués EN PREMIER)
- **G1 doctrine** : PASS attendu par **non-déclenchement** — aucun contenu/mission EM, drapeau `animate` JS seul.
- **G2 citations §10** : PASS attendu par **non-déclenchement** — aucune référence/corpus touché.

### Couche 2 — §5.1 (seuil 7.0) — checks falsifiables Playwright
1. **`reducedMotion:'reduce'`** — au boot, `map.options.zoomAnimation/fadeAnimation/markerZoomAnimation === false` ;
   `tlxReduceMotion() === true`. Déclencher un pan (clic marqueur certifié → `panTo`, ou popup volumineux →
   `panBy`) : le recentrage se fait **sans animation** (position finale ~instantanée, pas de frames intermédiaires).
2. **`reducedMotion:'no-preference'` (non-régression)** — `map.options.zoomAnimation === true` (défaut) ;
   l'animation d'origine **fonctionne** (pan/zoom animés). Comportement strictement inchangé.
3. **Non-régression moteur** — 9 couches au boot, indice dual, drill-down, dashboard, console propre 2 modes.
   Parité `main`/`dev` via `tests/blindage-harness/eval-app-rubric.mjs` (lancé comme outil).
4. **CI** — `validate-code` (node --check) reste vert. (Note : `htmlhint` cible des fichiers `corpus.html`/
   `agronomie.html` retirés de dev — staleness CI pré-existante, **non imputable à rnd-003**.)

## NOTE PLAYWRIGHT
```js
const ctx = await browser.newContext({ reducedMotion: 'reduce' });
const page = await ctx.newPage();
await page.goto(APP_URL, { waitUntil: 'domcontentloaded' });
const opts = await page.evaluate(() => ({
  zoom: map.options.zoomAnimation, fade: map.options.fadeAnimation, marker: map.options.markerZoomAnimation,
  rm: tlxReduceMotion()
}));
// reduce → {zoom:false, fade:false, marker:false, rm:true} ; no-preference → {...true, rm:false}
```

## PARAMÈTRES DE BOUCLE
```
SEUIL : 7.0 / 10 pondéré (après gates)
MAX ITÉRATIONS : 3
ESCALADE : plateau Δ<0.3 sur 3 → stop + RAPPORT_FINAL.md
```

## SÉPARATION §2
Le générateur (ce commit) **ne s'évalue pas**. Évaluateur = session fraîche, écrit `feedback-001.md` ici +
commente la PR, **ne corrige rien**. FAIL → le générateur itère. PASS → PR draft reste ouverte ; merge = Soleil.
