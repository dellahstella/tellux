---
name: scroll-reveal-reduced-motion
description: >-
  Ajoute des apparitions au scroll (reveals) staggered sur une page, en respectant impérativement
  prefers-reduced-motion (accessibilité) : IntersectionObserver, décalage par enfant, et un bloc
  reduce qui neutralise TOUTE animation/transition. À utiliser dès qu'on anime l'entrée d'éléments
  au scroll d'une landing/page. Déclencheurs : reveal, scroll reveal, staggered, animation entrée,
  prefers-reduced-motion, accessibilité motion, IntersectionObserver, fade-up. Adossé à §11.3.
---

# scroll-reveal-reduced-motion — Reveals au scroll, accessibilité d'abord

Les apparitions au scroll donnent du rythme, mais le mouvement non maîtrisé est un **problème
d'accessibilité** (vestibulaire). Règle non négociable : tout mouvement décoratif s'éteint sous
`prefers-reduced-motion: reduce`, et le contenu reste **immédiatement visible** (jamais bloqué à
`opacity:0`).

## Quand l'utiliser
Animer l'entrée d'éléments au scroll d'une page (cartes, étapes, sections) — reveal simple ou
staggered (cascade).

## Procédure
1. **État + transition** : `.reveal{opacity:0;transform:translateY(Npx);transition:…}` →
   `.reveal.visible{opacity:1;transform:none}`. Un `filter:blur()` optionnel pour un rendu plus doux.
2. **Déclenchement** : un `IntersectionObserver` ajoute `.visible` à l'intersection puis `unobserve`.
   Fallback sans observer : tout révéler immédiatement (`.visible` sur tous).
3. **Stagger** : décaler par enfant via `transition-delay` (`:nth-child(n)`), PAS via N timers JS.
   Cibler les vraies grilles (cartes, étapes) ; ne pas empiler reveal-de-section ET reveal-d'enfants
   au point de rendre la cascade boueuse.
4. **EXIGENCE DURE — reduced-motion** : un bloc
   `@media(prefers-reduced-motion:reduce){ .reveal{opacity:1!important;transform:none!important;filter:none!important;transition:none!important;} }`
   qui garantit le contenu visible sans mouvement. Mettre les animations décoratives en boucle
   (scan, pulse, parallaxe) sous `@media(prefers-reduced-motion:no-preference)` pour qu'elles
   n'existent QUE si l'utilisateur ne demande pas la réduction.
5. **Vérifier** : le contenu est lisible même si le JS échoue (ne jamais laisser un élément
   piégé à `opacity:0`) ; et l'absence de mouvement résiduel sous reduce (inspection du code si
   l'outil de test n'émule pas le media feature).

## Garde-fous
- **Jamais de contenu piégé invisible** : si l'observer ne tourne pas (pas de JS, vieux navigateur),
  le contenu doit s'afficher. Fallback obligatoire.
- **Le bloc `reduce` doit tout couvrir** : reveals, fades de composants, animations en boucle.
  Une seule animation oubliée hors du guard = échec accessibilité.
- **Stagger en CSS, pas en JS** : `transition-delay`/`nth-child` plutôt que des `setTimeout` en
  cascade (plus simple, interruptible, sans fuite de timers).

## Sortie
Des reveals au scroll (staggered le cas échéant) qui enrichissent la page sans jamais la rendre
inaccessible : sous `prefers-reduced-motion:reduce`, tout est visible et immobile.
