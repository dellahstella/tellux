# Synthèse session 4 — Tellux Corse
*9 avril 2026 · Session de clôture voie A*

---

## Ce qui a été accompli

### Fixes code (HTML gelé après cette session)

**FAB mesure — restauration comportement original**
Le bouton + en bas à droite fonctionnait correctement avant : bleu au repos, rouge (× via rotation CSS) quand actif, fermeture au second clic. Ce comportement avait été cassé lors d'une session précédente où le bouton avait été reconnecté à `openProspecteurWithForm()` au lieu de `startContribFromFAB()`. Fixes appliqués :
- Bouton reconnecté à `startContribFromFAB()`
- `startContribFromFAB()` enrichi : ouvre le panneau prospecteur, lie `prosp-mesure-details`, passe le FAB en rouge + innerHTML `+` (rotation CSS → ×)
- `saveContrib()` : réinitialise FAB après sauvegarde
- Bouton Annuler : réinitialise FAB + supprime marqueur violet
- **Fix double-clic** (dernier bug) : `map.once('click')` dans `startContrib()` enveloppé dans `setTimeout(0)` — le listener se lie après la fin de l'événement click sur le bouton FAB, évitant qu'il consomme le clic du bouton lui-même

**A-7 — Popup bloqué par zones quadrillées anomalies**
Résolu définitivement. Les rectangles `buildHotLocal` (mode simulation haute résolution) étaient créés sans `interactive:false` et interceptaient les clics avant qu'ils atteignent `map.on('click')`. Trois rectangles mis à jour :
- `buildHotLocal` rectangles → `interactive:false`
- `rectPreview` (aperçu dessin bâtiment) → `interactive:false`
- Rectangle bâtiment `addRectBuilding()` → `interactive:false`
Les rectangles de `buildHot` principal avaient déjà été corrigés en session 3.

### Roadmap mise à jour (v4)

`TELLUX_ROADMAP.md` refondu avec :
- Tableau de statut clair : tous A-xx résolus + FAB double-clic
- Section "prochaines actions côté Soleil" distincte du code
- Chantiers B-VISITES, B-AGRO, B-GEO documentés avec prochaines étapes
- Agenda S16-S20 actualisé
- Critère de gel voie A : atteint

### Guide fiches patrimoine (v2)

`TELLUX_GUIDE_FICHES_PATRIMOINE.md` refondu avec la double structure :

**Fiche A — Territoire** : narration, mythologie, légende, histoire, terroir. Libre d'accès. Ton validé : rigueur + sensibilité, ni notice de musée ni tract ésotérique. 600-900 mots.

**Fiche B — Tellux** : score EM, hypothèses H-xx intégrées avec niveau de crédibilité (A/B/C), outils Tellux pertinents par couche, préconisations. Débloquée par visite terrain (géoloc ±100m) OU résolution d'hypothèse associée.

**Gamification** :
- Style Pokémon Go : la beauté de la carte crée l'envie d'explorer
- Fog of war : brouillard qui se lève sur les sites visités
- 5 badges (Mégalitheur, Investigateur, Permaculteur, Sentinelle, Archiviste Corse)
- Image générée par site (style gravure naturaliste — palette Tellux)
- Langue : français. Noms corses dans les titres dès maintenant. Traduction corse intégrale = levier financement FEADER/CTC.

### Veille design & narration

`TELLUX_VEILLE_DESIGN_NARRATION.md` — synthèse exploitable :

**Design** : Atlas Obscura (modèle éditorial le plus proche), Ingress/PGo (gamification), ArcheoGeolocalisation (filtrage multi-critère), Mapbox Studio (customisation voie B)

**Folklore corse** : Mazzeri (figure du capteur de l'invisible → archétype du contributeur terrain Tellux), Stregha, Oghju. Légendes mégalithes : "tola di u peccatu", "stantara", "idoli dei Mori". M3C (43 000 docs audio/visuels corses, open access).

**Style littéraire** : Kenneth White ("Corsica, l'itinéraire des rives et des monts" — géopoétique, triple couche landscape/mindscape/wordscape), Alain Corbin (inventer une sensibilité nouvelle aux champs EM comme le XIXe a inventé le désir de mer), Patrice Franceschi ("Dictionnaire amoureux de la Corse" — modèle rédactionnel direct)

---

## État à la clôture de session

### Ce qui est gelé

- `tellux_CORRECT.html` — v7, tous bugs A-xx résolus. Ne plus modifier sauf régression critique.
- `DIRECTION_ARTISTIQUE_v2.md` — validée
- `TELLUX_GUIDE_FICHES_PATRIMOINE.md` — v2, en attente arbitrages Soleil (longueur, style image)

### Ce que Soleil fait de son côté

1. **Vérification structure juridique** (SARL Stella Canis Majoris vs. autres options)
2. **Récupération contacts** : associations EM, mairies, scientifiques
3. **Adaptation documentation par cible** : chaque partenaire reçoit un angle différent
4. **GPS audit sites** : session Google Earth pour vérifier SITES[]
5. **Captures A-8** : après mise en ligne sur serveur HTTP (pas file://)

### Arbitrages en attente (pour session Opus)

- Longueur fiches : légère (300 mots) vs. complète (600 mots) par type de site ?
- Style image générée : gravure naturaliste / vectoriel sobre / photomontage ?
- Déblocage Fiche B : géoloc ±100m stricte ou tolérance élargie ?
- Mots corses dès maintenant dans les titres ou attendre traduction intégrale ?

---

## Prochaines sessions recommandées

### Session Opus — B-VISITES

Dédiée à la mise sur les rails du sous-projet fiches patrimoine. Préparer :
1. Lire `TELLUX_GUIDE_FICHES_PATRIMOINE.md` + `TELLUX_VEILLE_DESIGN_NARRATION.md`
2. Arbitrer les 4 questions en suspens
3. Rédiger les 2 premières fiches pilotes (Filitosa et Cauria) pour valider le format
4. Définir le style image (séance de travail dédiée)
5. Concevoir l'architecture de `SITES_REFERENCE.json`

### Session code (si nécessaire)

Seulement si une régression est constatée après les tests. Le HTML est gelé — toute modification doit être motivée par un bug reproductible.

### Session Framer (voie B, horizon S20+)

Landing page marketing indépendante de l'app carte. Components JSX exportables depuis Claude. Ne touche pas au HTML.

---

## Ce que cette session a confirmé

- L'app Tellux est stable et livrable aux partenaires tests
- Le FAB mesure fonctionne comme prévu (bleu → rouge → fermeture)
- Les popups s'affichent correctement même sur les zones quadrillées d'anomalies
- Le guide de rédaction des fiches pose des bases solides pour le sous-projet éditorial
- La veille confirme que le registre Tellux (géopoétique + rigueur scientifique) est ancré dans une tradition française existante — ce n'est pas une invention, c'est un positionnement

---

*Session clôturée. La voie A est gelée. Bonne route côté terrain.*
