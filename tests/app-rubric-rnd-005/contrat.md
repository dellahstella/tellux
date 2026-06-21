# CONTRAT D'ITÉRATION — rnd-005 · Réactivité mid-session de `prefers-reduced-motion`

> À lire avec `PROTOCOLE_AUTO_ITERATION.md` (§2, §4, §5.1). Item de file : issue #857.
> Origine = réserve #3 / critique craft de l'éval rnd-003 (`feedback-001.md`, PR #854).

```
CHANTIER   : rnd-005 — prefers-reduced-motion réactif en cours de session (app.html)
AXE        : app · PRIORITÉ : basse (edge rare)
GÉNÉRATEUR : Code (Claude Code) — branche claude/rnd-005-reduced-motion-reactive (base dev)
ÉVALUATEUR : session FRAÎCHE distincte (Playwright headless) — NE corrige pas
DATE       : 2026-06-21
DÉPEND DE  : rnd-003 (#854, mergé dans dev — helper tlxReduceMotion présent)
```

## OBJECTIF (1 phrase)

Honorer un changement OS de `prefers-reduced-motion` **en cours de session** pour les animations de la carte
Leaflet, sans changer le comportement au boot ni toucher aux zones gelées.

## CONTEXTE

rnd-003 lit la préférence (a) à l'init pour les options d'animation carte, (b) à l'appel pour les pans
explicites. Les pans sont donc **déjà réactifs** ; seules les options init (`zoomAnimation`/`fadeAnimation`/
`markerZoomAnimation`) ne l'étaient pas. Le helper `TLX_RM_QUERY` (un `MediaQueryList`) n'était pas écouté.

## CE QUI A ÉTÉ FAIT (1 site, +13 lignes)

Après l'init carte, un listener :
```js
if (TLX_RM_QUERY && typeof TLX_RM_QUERY.addEventListener === 'function') {
  TLX_RM_QUERY.addEventListener('change', function(){
    var rm = tlxReduceMotion();
    map.options.zoomAnimation = !rm;
    map.options.fadeAnimation = !rm;
    map.options.markerZoomAnimation = !rm;
    if (typeof L !== 'undefined' && L.Browser) { map._zoomAnimated = !rm && !!L.Browser.any3d; }
  });
}
```
`map._zoomAnimated` est resynchronisé car Leaflet le fige à l'init (sinon le **geste de zoom** n'honorerait pas
le changement). Les pans explicites restent réactifs par lecture à l'appel (inchangés).

## DANS LE PÉRIMÈTRE
Le seul listener ci-dessus. Single-concern.

## HORS PÉRIMÈTRE
- Zones gelées (`calc*`, GPS scientifiques, GELÉE, données `SITES/CHURCHES/HYPOTHESES`). Aucune coordonnée modifiée.
- Le gating statique rnd-003 (déjà dans la base), autres pages.

## CRITÈRES D'ACCEPTATION — gate-puis-score (D-4)

### Couche 1 — Gates éliminatoires
- **G1 doctrine** : PASS attendu par non-déclenchement (helper JS seul, 0 contenu/mission EM).
- **G2 citations §10** : PASS attendu par non-déclenchement (0 référence/corpus/coordonnée).

### Couche 2 — §5.1 (seuil 7.0) — checks falsifiables Playwright
1. **Réactivité OFF→ON** : charger en `reducedMotion:'no-preference'` (au boot `map.options.zoomAnimation===true`),
   puis `page.emulateMedia({reducedMotion:'reduce'})` **après boot** → `map.options.zoomAnimation/fadeAnimation/
   markerZoomAnimation` basculent à **false** et `map._zoomAnimated===false` ; un `panBy`/`setView` déclenché
   **après** le changement est **non animé** (déjà réactif via rnd-003, à reconfirmer).
2. **Réactivité ON→OFF** : inverse → options repassent à `true`, animations réactivées.
3. **Non-régression boot** : au chargement initial, comportement **strictement identique à rnd-003**
   (mêmes options selon la préférence au boot ; pans inchangés). Le listener n'agit qu'au `change`.
4. **CI** : `validate-code` (node --check) vert.

## NOTE PLAYWRIGHT
```js
const ctx = await browser.newContext({ reducedMotion: 'no-preference' });
const page = await ctx.newPage();
await page.goto(APP_URL, { waitUntil: 'domcontentloaded' });
// boot : zoomAnimation === true
await page.emulateMedia({ reducedMotion: 'reduce' });          // change mid-session
const after = await page.evaluate(() => ({ z: map.options.zoomAnimation, za: map._zoomAnimated, rm: tlxReduceMotion() }));
// attendu : { z:false, za:false, rm:true }
```

## PARAMÈTRES DE BOUCLE
```
SEUIL : 7.0 / 10 pondéré (après gates) · MAX ITÉRATIONS : 3 · ESCALADE : plateau Δ<0.3 sur 3 → stop + RAPPORT_FINAL.md
```

## SÉPARATION §2
Le générateur (ce commit) ne s'évalue pas. Évaluateur = session fraîche (idéalement réseau Supabase-joignable
pour lever la réserve de non-régression absolue), écrit `feedback-001.md` ici + commente la PR, ne corrige rien.
PASS → PR draft reste ouverte ; merge = Soleil.
