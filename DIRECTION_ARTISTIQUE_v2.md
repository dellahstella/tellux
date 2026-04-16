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
- **Pierre** `#F5F0E7` — fond du logo principal (v14).

### Données cartographiques
Conserver les échelles de couleur existantes (nT, dBm, scores) mais **harmoniser les rouges/oranges** sur le rouge porphyre et l'ocre myrte pour cohérence globale.

---

## Typographie (validée)

- **Titres & header** : Fraunces (serif contemporaine, caractère, Google Fonts gratuite).
- **Corps & UI** : IBM Plex Sans (neutre, excellente lisibilité technique).
- **Données / mono** : JetBrains Mono pour les scores numériques et les coordonnées.
- **Logo texte** : Cormorant Bold (serif humaniste, empattements en griffe, élégance classique).

Hiérarchie :
- H1 Fraunces 32-40px
- H2 Fraunces 22-26px
- Body IBM Plex Sans 14-16px
- Micro IBM Plex Sans 11-12px (légendes cartes)
- Scores JetBrains Mono 13-14px

---

## Logo-mark — Monogramme T tellurique (v14, validé)

**Statut :** validé — session du 16 avril 2026. Remplace le logo v7 (T-bouclier) devenu obsolète.

### Description formelle

T majuscule en Cormorant Bold, avec dégradé vertical continu du vert Maquis en haut vers l'ocre myrte en bas. La transition s'opère au niveau médian de la lettre, de manière fluide (sans rupture de ton).

Deux lignes courbes symétriques en ocre foncé entourent la base du T :
- Une **ligne d'horizon** convexe au-dessus, traversant toute la largeur du logo, avec fade aux extrémités pour un rendu léger.
- Son **miroir vertical concave** juste en dessous, dont le sommet (le point le plus bas de la courbe) reste au niveau de la base du T sans la dépasser.

Les deux courbes ne se rejoignent pas aux extrémités — elles suggèrent un cadre ouvert, un écho, pas une forme fermée.

### Symbolique

Le T tellurique évoque le lien à la terre (tellurique = qui appartient à la Terre, au sol). Le dégradé du vert au ocre figure la transition entre le vivant du maquis (surface visible) et la chaleur minérale du sol corse (profondeur). Les deux courbes symétriques suggèrent l'horizon et son miroir intérieur, sans chercher à imposer une lecture ésotérique.

### Palette du logo

- **T, dégradé** : `#3F5B3A` (Maquis) → `#C28533` (Ocre myrte)
- **Lignes** : `#B47328` (Ocre foncé)
- **Fond principal** : `#F5F0E7` (Pierre)

### Typographie

Cormorant Bold (serif humaniste, empattements en griffe, élégance classique proche du Garamond).

### Usage et déclinaisons

- Usage principal : fond Pierre
- Une déclinaison sur fond Ardoise sera produite ultérieurement si besoin
- Variante Bodoni Bold disponible dans `assets/logo/tellux_logo_bodoni.png` comme alternative éditoriale, non utilisée en production

### Fichiers disponibles

Tous dans `assets/logo/` :
- `tellux_logo.svg` — source vectorielle autonome (Cormorant vectorisé, pas de dépendance police)
- `tellux_logo_1200.png` — 1200×1200, usage web standard
- `tellux_logo_2400.png` — 2400×2400, impression, affiches
- `tellux_logo_800x600.png` — format compact
- `favicon_512.png`, `favicon_128.png` — favicons
- `tellux_logo_bodoni.png` — variante Bodoni (sauvegarde)

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
2. ✅ Typographie : Fraunces + IBM Plex Sans + JetBrains Mono + Cormorant Bold (logo texte).
3. ✅ Logo : Monogramme T tellurique v14 (Cormorant Bold, dégradé vert→ocre, validé le 16 avril 2026).
4. ✅ Tagline : « Mesurer le vivant ».
5. ✅ Nom affiché : « Tellux » (sans « Corse » dans le logo, « Corse » dans la tagline header).
