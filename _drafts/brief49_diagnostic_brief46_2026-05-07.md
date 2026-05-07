# Brief 49 — Diagnostic Brief 46 (2026-05-07)

## Problème constaté

Brief 46 déclaré "mergé" mais audit MCP post-merge sur `https://tellux.pages.dev/app?bust=br46postmerge` confirme que le pattern toggle légende n'a **jamais atteint la prod**.

### Éléments absents en prod

| Élément attendu | État prod |
|---|---|
| `document.getElementById('legende')` | `null` |
| `document.getElementById('legende-toggle')` | `null` |
| `document.getElementById('legende-content')` | `null` |
| `#tellux-leg-panel` intégré dans overlay | Toujours Leaflet control `bottomright`, 170×370px |
| `#conditions-panel` intégré dans overlay | Toujours bandeau fullwidth 1364×159px |
| Mobile : panel replié par défaut | Non implémenté |

### Cause probable

Brief 46 a été implémenté dans une session Claude Code dans un worktree isolé (`claude/sweet-buck-7ccde0`) mais les commits n'ont jamais été poussés ni une PR créée. Le statut "mergé" était une confusion de session.

## Ce qui a été fait dans Brief 49

### Fichier modifié : `app.html`

**CSS ajouté** (avant `</style>`) :
- `#legende` : `position:absolute;bottom:14px;right:12px;z-index:1000` — floating bottom-right de `.map-col`
- `#legende-toggle` : cercle 36×36px, fond `rgba(245,240,231,0.95)`, cohérent avec patrimoine.html
- `#legende-content` : panel beige, `max-width:320px`, `max-height:calc(100vh-120px)`, scroll
- `#legende.collapsed #legende-content` : `display:none`
- Responsive mobile ≤600px : offsets réduits

**HTML** (`#conditions-panel` retiré du flux document, intégré dans `#legende`) :
- `<aside id="legende" class="collapsed">` inséré dans `.map-col` après `<div id="map">`
- Section "Conditions actuelles" : contient l'intégralité de l'ancien `#conditions-panel`
- Section "Légende EM" : contient `<div id="tellux-leg-panel">` (rempli dynamiquement)
- `<div id="legende-em-empty">` : message si aucune couche EM active

**JS modifié** :
- `updateLegendPanel()` : suppression du Leaflet control `_legendCtrl` (bottomright) — rendu direct dans `#tellux-leg-panel` dans l'overlay + gestion `#legende-em-empty`
- `_legendCtrl = null` (déclaration) : supprimée
- `initLegende()` IIFE ajoutée en fin de script : localStorage `tlx_app_legende_open`, mobile ≤600px replié par défaut, desktop ouvert par défaut

## Critères d'acceptation post-deploy

```js
document.getElementById('legende')         // → Element (pas null)
document.getElementById('legende-toggle')  // → button, 36×36
document.getElementById('legende-content') // → Element
// Mobile 380×800 : legende.classList.contains('collapsed') === true au boot
// Clic toggle → panel s'ouvre / se referme
// Cohérence visuelle avec patrimoine.html
```
