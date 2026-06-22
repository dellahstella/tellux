---
name: hero-map-lazy-init
description: >-
  Affiche une carte/visualisation de données réelle en hero d'une page statique SANS dégrader
  le premier rendu : données projetées hors-ligne en SVG léger, construites en différé (idle),
  fetch caché, et ne pas construire quand l'élément est masqué (mobile). À utiliser dès qu'on
  veut remplacer un placeholder décoratif par une vraie donnée en hero d'une landing/page.
  Déclencheurs : hero map, carte hero, vrai placeholder, lazy-init, requestIdleCallback,
  carte SVG, données réelles landing, perf hero, non-bloquant. Adossé à CHARTE_DECISION + §11.3.
---

# hero-map-lazy-init — Une vraie carte en hero, sans coût de chargement

Un hero qui promet « cartographie » doit montrer de la **vraie donnée**, pas un placeholder
factice — mais sans peser sur le premier rendu. Le pattern : projeter la donnée hors-ligne en
SVG léger, et construire la carte **en différé** une fois la page peinte.

## Quand l'utiliser
Remplacer un faux visuel hero (grille + pins décoratifs) par une carte/visualisation issue de
données réelles déjà présentes dans le repo, sur une page statique (landing, page produit).

## Procédure
1. **Projeter hors-ligne** : un script (Python/Node) lit la donnée source (GeoJSON, CSV de
   points…), simplifie (RDP/décimation) et projette en coordonnées SVG (équirectangulaire avec
   correction `cos(lat)` pour du géo). Sortie : un JSON compact `{viewBox, W, H, <géométries>, <points>}`
   dans `public/data/`. Vise quelques dizaines de Ko, pas des centaines.
2. **Construire en différé** : `requestIdleCallback(build, {timeout:1200})` (fallback `setTimeout`),
   `fetch(..., {cache:'force-cache'})`. La construction est **hors du chemin critique** du premier rendu.
3. **Fit robuste** : le `<svg>` reçoit `preserveAspectRatio="xMidYMid meet"` et est dimensionné par
   un conteneur à **taille définie** (ex. `position:absolute; inset:Npx` ou flex à hauteur fixe).
   Ne pas compter sur `height:%` d'un enfant de grille auto-sizée — le % ne se résout pas et le SVG
   rend à sa taille intrinsèque (débordement/clipping). Vérifier que toute la géométrie + tous les
   points tiennent dans le cadre (0 clippé).
4. **Ne pas construire si masqué** : si la carte est `display:none` sous un breakpoint, court-circuiter
   (`matchMedia('(min-width:Xpx)').matches`) pour ne pas fetch + bâtir des centaines de nœuds invisibles.
5. **Fade-in** discret à l'apparition (classe ajoutée en `requestAnimationFrame`), neutralisé sous
   `prefers-reduced-motion:reduce` (cf. [[scroll-reveal-reduced-motion]]).

## Garde-fous
- **Données réelles, pas inventées** : la carte hero ne doit pas suggérer des valeurs fabriquées ;
  donnée institutionnelle déjà publique uniquement (cohérent doctrine mesure-d'abord).
- **Committer le JSON projeté** : sans le fichier de données, la carte casse en prod (untracked = piège).
- **Perf falsifiable** : mesurer que le premier rendu ne dépend pas de la carte (idle + cache),
  et la taille du JSON ; si on parle de « léger », le prouver (Ko).
- **Vérifier le fit en live** : compter les éléments hors-cadre (`getBoundingClientRect`), pas se fier
  à l'œil — le clipping d'un SVG mal dimensionné est silencieux.

## Sortie
Un hero qui affiche une carte de données réelle, construite en différé, intégralement visible
(0 clippé), masquée proprement sur mobile, et dont le JSON de données est committé.
