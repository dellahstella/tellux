# TELLUX — Direction artistique (v2)

**Statut :** validée — session du 8 avril 2026.

---

## Positionnement

Tellux n'est **ni** un outil scientifique austère, **ni** un site ésotérique. C'est une plateforme à la **jonction rigueur / sensibilité au territoire**. L'identité doit refléter cette jonction :

- **Rigueur** : typo lisible, données denses mais claires, palette neutre qui laisse parler la carte.
- **Sensibilité** : chaleur, évocation du minéral corse, des lumières du maquis, du rapport vivant à la terre.

À éviter : tout ce qui évoque le « new age générique » (bleus turquoise, chakras, géométries sacrées décoratives) et tout ce qui évoque le « dashboard SaaS aseptisé » (bleus corporate, gris froid).

---

## Palette (validée)

### Base neutre
- **Ardoise** `#1F2329` — texte principal, headers.
- **Pierre claire** `#F5F0E7` — fond principal, clair et chaud.
- **Mica** `#74706A` — texte secondaire.
- **Brume** `#E8E2D5` — fond secondaire, séparateurs.

### Accents
- **Maquis profond** `#3F5B3A` — accent primaire, zones OK, validations.
- **Ocre myrte** `#C28533` — accent secondaire, highlights, gamification.
- **Rouge porphyre** `#8E2F1F` — alertes, anomalies fortes, zones critiques.
- **Bleu nuit tyrrhénien** `#1F3A5F` — liens, mode analytique.

### Fond logo (référence)
- **Maquis sombre** `#2A3530` — fond du logo principal.

### Données cartographiques
Conserver les échelles de couleur existantes (nT, dBm, scores) mais **harmoniser les rouges/oranges** sur le rouge porphyre et l'ocre myrte pour cohérence globale.

---

## Typographie (validée)

- **Titres & header** : Fraunces (serif contemporaine, caractère, Google Fonts gratuite).
- **Corps & UI** : IBM Plex Sans (neutre, excellente lisibilité technique).
- **Données / mono** : JetBrains Mono pour les scores numériques et les coordonnées.
- **Logo texte** : Cinzel (majuscules élégantes, espacement large).

Hiérarchie :
- H1 Fraunces 32-40px
- H2 Fraunces 22-26px
- Body IBM Plex Sans 14-16px
- Micro IBM Plex Sans 11-12px (légendes cartes)
- Scores JetBrains Mono 13-14px

---

## Logo-mark — Monogramme T tellurique (v7, validé)

### Description

Le logo est un **T monumental** dont la structure porte une triple lecture symbolique :

**1. Partie haute — Le T-bouclier (plan matériel)**
La barre horizontale du T a des terminaisons qui descendent en angle (inspiration gothique). C'est cette barre qui **est** le bouclier — forme protectrice explicite. Le fût vertical descend comme une lame ou un clou, élancé et net. La lumière irradie depuis le cœur du fût.

**2. Ligne d'horizon — La courbure terrestre**
Une courbe convexe (bombée vers le haut) traverse l'axe du T au niveau médian. Elle évoque la **ligne d'horizon de la Terre vue depuis l'espace**. C'est une ligne séparée, structurelle — elle ne forme pas de contour en dessous.

**3. Partie basse — Le reflet éthérique (plan vibratoire)**
Sous l'horizon, le fût du T continue en miroir mais **flouté, semi-transparent, vibratoire** — c'est le reflet dans les « eaux d'en bas ». Les contours se dissolvent. À la base, une courbe symétrique inversée (convexe vers le bas), plus éthérique, fait écho à l'horizon.

**4. L'œil**
Les deux courbes (horizon matériel + courbe basse éthérique) **ne se rejoignent pas**. Ensemble, elles dessinent la forme d'un **œil** — point de convergence entre le visible et l'invisible, le mesuré et le ressenti.

### Palette du logo
- **Corps du T** : dégradé ivoire satiné `#F5EACC` → or chaud `#D4B870`
- **Fond référence** : maquis sombre `#2A3530`
- **Lumière intérieure** : or blanc `#FFF8E8` → ocre `#C28533` en radial
- **Horizon** : blanc lumineux `#FFFCF0` avec fade latéral
- **Courbe basse** : même teinte mais opacity réduite, flou gaussien

### Variantes de fond validées
1. **Ardoise** `#1F2329` — contextes neutres, UI
2. **Maquis** `#2A3530` — référence principale (web)
3. **Tyrrhénien** `#162540` — contexte nuit/mer
4. **Porphyre** `#3A1815` — contexte terre/roche
5. **Pierre** `#F5F0E7` — version claire inversée (exports PDF, impression)
6. **Crème** `#EFE7D5` — version papier

### Spécifications techniques
- Format source : SVG vectoriel inline (viewBox 400×560)
- Favicon : SVG optimisé 32×32 + PNG 180×180 (Apple Touch)
- Header app : SVG adapté au viewBox 220×300, 48×60px display
- `theme-color` meta : `#2E3A36`

---

## Règles d'usage

### Header du site
- Logo T à gauche (SVG inline, 48×60px), titre « Tellux » en Fraunces à côté, tagline « Mesurer le vivant · Corse » en dessous.
- Pas de gradient agressif. Fond pierre claire ou ardoise selon mode.

### Footer
- Crédits institutionnels sur une ligne : IGRF-14 · ANFR · BRGM · NOAA · EMAG2v3 · Dragon Project · Supabase.
- Mention « Projet Tellux, Corse 2026 » et lien CGU/contact.

### Popups cartes
- Fond blanc cassé (pierre claire), bordure fine ardoise 1px.
- Titre en serif (Fraunces), contenu en IBM Plex Sans.
- Scores numériques en mono (JetBrains Mono) pour bien ressortir.

### Exports PDF
- Template unifié : header Tellux (logo + nom), footer avec mentions données, contenu aéré, palette cohérente.

### Captures pour dossier candidature
- Toujours en light mode.
- Résolution 1920×1080 minimum.
- Éviter les UI states transitoires.

---

## Ton rédactionnel

- **Français soigné**, pas d'anglicismes gratuits.
- **Vouvoiement** pour les textes publics.
- **Concision** : une idée par phrase, verbes actifs.
- **Pas d'emphase marketing** : préférer des verbes concrets (« cartographie », « mesure », « croise »).
- **Rigueur épistémique** : distinguer ce qui est **mesuré**, **modélisé**, et **hypothèse en cours de test**.

---

## Décisions prises (session 8 avril 2026)

1. ✅ Palette : validée (7 couleurs + fond logo maquis).
2. ✅ Typographie : Fraunces + IBM Plex Sans + JetBrains Mono + Cinzel (logo texte).
3. ✅ Logo : Piste 1 retenue — Monogramme T tellurique v7.
4. ✅ Tagline : « Mesurer le vivant ».
5. ✅ Nom affiché : « Tellux » (sans « Corse » dans le logo, « Corse » dans la tagline header).
