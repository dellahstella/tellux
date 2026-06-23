---
name: controle-rendu-visible-headless
description: >-
  Vérifier en CI headless qu'un élément est effectivement RENDU ET VISIBLE (pas un panneau
  « quasi uniformément sombre » ou vide) — sans dépendance image. Combine un contrôle de
  STRUCTURE (le contenu attendu est dans le DOM + élément visible) et un contrôle PIXEL
  (écart-type de luminance d'un screenshot d'élément, re-décodé par un canvas navigateur).
  À utiliser pour un smoke-test visuel d'une landing/hero, ou toute garde anti-régression de
  contraste/visibilité. Déclencheurs : smoke visuel, hero map invisible, anti-régression
  contraste, panneau sombre, rendu effectif, Playwright headless, luminance, screenshot canvas.
  Adossé au PROTOCOLE §11.3 ; complète checklist-anti-regression-landing et hero-map-lazy-init.
---

# controle-rendu-visible-headless — « rendu ET visible », pas juste « présent »

Un check headless qui dit « l'élément existe » (HTTP 200, sélecteur présent) NE prouve PAS
qu'il est **visible**. Une carte/panneau peut être dans le DOM mais rendu « quasi uniformément
sombre » (build échoué, fills sans contraste, opacité 0). Ce skill détecte ce cas sans lib image.

## Quand l'utiliser
Smoke-test post-déploiement d'une page statique, ou garde anti-régression sur un élément
visuel clé (hero map, graphe, vignette) dont la disparition/aplatissement serait silencieuse.

## Procédure
1. **Viewport adéquat** : si l'élément est masqué en responsive (`display:none` < Npx), tester
   au viewport où il est visible. Attendre le **build différé** (`waitForSelector` sur le
   contenu réel, ex. le `svg` injecté — pas seulement le conteneur).
2. **Structure (signal fiable, en premier)** : le contenu attendu est dans le DOM (compter les
   enfants significatifs : paths/points/barres ≥ seuil) ET l'élément est visible
   (`display`/`visibility`/`opacity` + bounding box non nulle).
3. **Pixels (complément anti-contraste)** : screenshot de l'élément (CSS appliqué), puis le
   re-décoder **par le navigateur** — `data:image/png;base64,…` → `Image` → `canvas` →
   `getImageData` — et calculer la **moyenne et l'ÉCART-TYPE de luminance**. Pas de lib image
   (zéro dépendance) ; le canvas natif fait le décodage PNG.
4. **Seuil calibré empiriquement** : mesurer le **sain** vs un **état plat** (même élément,
   contenu retiré → panneau uniforme). Un panneau plat a un écart-type très bas ; le sain est
   nettement plus haut. Placer le seuil **entre les deux, avec marge des deux côtés**.
   Échec = structure manquante **OU** écart-type < seuil.

## Garde-fous
- **Calibrer** le seuil sur des mesures réelles (sain et plat), jamais à la louche ; viser une
  marge généreuse pour ne pas faire de **faux positif** sur un design volontairement sombre.
- **Structure d'abord** : c'est le signal le plus fiable (attrape « n'a pas buildé ») ; le
  pixel attrape « buildé mais invisible/plat ».
- Le screenshot capture le **rendu réel** (CSS inclus) — ne pas analyser un SVG sérialisé
  isolé (les styles externes ne s'appliqueraient pas).
- Données du hero servies en asset statique (atteignable depuis un runner CI) ≠ back-end data
  (souvent injoignable depuis une IP datacenter) : ne pas confondre les deux familles.

## Sortie
Un verdict `{ visible: bool, structure: {…}, luminance: {mean, stdev, …}, problems[] }`.
Un échec (structure absente ou écart-type sous le seuil calibré) doit **signaler** (issue/log),
pas corriger.
