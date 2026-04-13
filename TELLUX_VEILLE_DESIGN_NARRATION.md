# Veille — Design carte & Narration corse
*Tellux Corse · Avril 2026 · Pour session Opus B-VISITES*

---

## 1. Design de cartes — références visuelles

### Modèle "collection & découverte"

**Ingress (Niantic)** — [intel.ingress.com](https://intel.ingress.com/)
Modèle fondateur de la cartographie ARG (Alternate Reality Game). Portails situés sur des lieux réels d'intérêt public (monuments, murales, bâtiments historiques). Esthétique cyberpunk avec stratification par faction, contrôle territorial, légende iconique claire. Exploitable : architecture "découverte par territoire", symboles faction = couches Tellux (EM naturel vs. EM artificiel), dynamique de contrôle visuel.

**Pokémon Go** — hérite des données Ingress. Système de progression (découvertes cumulatives), événementiel territorial, récompense narrative. Référent direct pour la logique de collection fiches patrimoine Tellux.

**Atlas Obscura** — [atlasobscura.com](https://www.atlasobscura.com/)
31 100+ lieux répertoriés, approche curatoriale et narrative. Descriptions longues, esthétique "cabinet de curiosités". Directement exploitable : narration ancrée au lieu, curation éditoriale du patrimoine, tone of voice "wonder". C'est l'ancêtre éditorial le plus proche de ce que Tellux veut faire.

**Fog of World / Wandrer** — cartes de progression personnelle. Le "brouillard de guerre" qui se lève au fur et à mesure des visites est une métaphore parfaite pour le système de déblocage fiches Tellux.

### Cartes patrimoine & archéologie

**ArcheoGeolocalisation.com** — [archeogeolocalisation.com](https://archeogeolocalisation.com/)
Carte interactive collaborative, filtrage par région/période/type de site. Système de filtrage multi-critères directement applicable au panneau Tellux. Base collaborative extensible.

**ArchéOdyssée** — 800+ sites avec fiches descriptives (fouilles, plans, photos, images aériennes). Structure de popup riche : image + métadonnées + sources. Modèle pour les popups Tellux patrimoine.

### Customisation visuelle

**Mapbox Studio** — [mapbox.com/mapbox-studio](https://www.mapbox.com/mapbox-studio)
Tuiles vectorielles entièrement customisables (palette, polices, symboles). La palette Tellux (Ardoise, Pierre, Maquis, Ocre, Porphyre, Tyrrhénien) est directement applicable comme style de fond de carte. À étudier pour la voie B.

### Architecture popup idéale (synthèse)

```
[Image du site ou vue aérienne IGN]
─────────────────────────────────────
Titre narratif (Fraunces 18px)
─────────────────────────────────────
Score Tellux : X.X/10  |  Type : Mégalithe
─────────────────────────────────────
Fragment de légende orale ou narration courte (2-3 phrases)
─────────────────────────────────────
[Bouton "Fiche A — Territoire"]  [Bouton "Fiche B — Tellux" 🔒]
```

---

## 2. Folklore et traditions corses

### Créatures et figures mythiques — inventaire utilisable

**Les Mazzeri** — [fr.wikipedia.org/wiki/Mazzérisme](https://fr.wikipedia.org/wiki/Mazz%C3%A9risme)
Chasseurs d'âmes. Individus capables de voir la mort en rêve — don involontaire, tragique. Solitaires, visionnaires, mélancoliques. Pacifiques contrairement aux Streghe. C'est la figure corse qui se rapproche le plus du "chercheur de champs invisibles" : quelqu'un qui perçoit ce que les autres ne voient pas, à son corps défendant. Potentiel fort comme figure narrative de Tellux (le capteur terrain qui mesure l'imperceptible).

**La Stregha** — sorcière maléfique, magie volontaire. Antagoniste du Mazzeru. Dualisme utilisable : forces naturelles (Mazzeru/EM naturel) vs. forces artificielles (Stregha/pollution EM).

**L'Oghju** — mauvais œil. Malédiction par jalousie. Thématique de la protection des lieux, du regard qui altère.

**Squadra d'Arrozza** — procession de défunts en rêve. Précurseur de mort. Narration temporelle, apparitions cycliques. Lien possible avec les sites où les mesures EM sont anormalement élevées.

### Légendes liées aux mégalithes

Sources : [Art & Âme Corse](https://art-et-ame-culture-corse.fr/croyances-et-legendes-corses/) | [France Pittoresque](https://www.france-pittoresque.com/spip.php?article7600=)

- Dolmens = "tola di u peccatu" (table du péché) ou "tola di u turmentu" (table des tourments)
- Menhirs = "idoli dei Mori" (idoles des Maures, des Anciens) — désignation chrétienne post-romane d'un passé révolu
- "Stantara" = pierre qui se lève — pétrification par colère divine (transgression morale). La figure humaine figée dans la pierre.
- Alignements : marquent l'organisation sociale et spirituelle préhistorique. Liés à l'eau, aux cols, aux passages.

### Toponymie sacrée (exploitable directement dans les fiches)

Chaque nom de lieu porte une histoire. Exemples :
- "Castello Araggio" = "riche en pierres levées"
- Les noms de sources et de cols encodent souvent une mémoire du sacré
- À documenter site par site dans `SITES_REFERENCE.json`

### Ressources orales archivées

**M3C — Médiathèque Culturelle de la Corse et des Corses** — [m3c.universita.corsica](https://m3c.universita.corsica/)
43 000+ documents. Contes, traditions, légendes en audio, ressources audiovisuelles. Open access gratuit. Source primaire indispensable pour les fiches patrimoine. À explorer avant la rédaction de chaque fiche.

---

## 3. Style littéraire — références

### Géopoétique : Kenneth White

[geopoetics.org.uk](https://www.geopoetics.org.uk/kenneth-whites-works/) | [terrestres.org](https://www.terrestres.org/2021/02/25/geopoetiser-avec-kenneth-white/)

Discipline créée par White : fusion géographie physique + paysage mental + paysage verbal. Triple relation :
> *landscape → mindscape → wordscape*

Chaque texte traverse ces trois couches. Ce n'est pas de la description, c'est une transformation.

**Œuvre directement pertinente :** "Corsica, l'itinéraire des rives et des monts" (1999) — comment Sénèque s'ouvrait aux sciences terrestres en Corse. Rigueur géographique + ouverture sensible. C'est exactement le registre que Tellux cherche.

**Ce que ça donne pour Tellux :**
- Couche 1 (landscape) : données EM, géologie, position GPS
- Couche 2 (mindscape) : ce que le chercheur ressent en arrivant sur le site
- Couche 3 (wordscape) : le texte narratif de la Fiche A, qui transforme

### Nature writing à la française

[bibliotheques.paris.fr](https://bibliotheques.paris.fr/nature-writing-la-litterature-des-grands-espaces.aspx)

Accepte la fiction + non-fiction contrairement au genre anglo-saxon. André Bucher : "Écrire dans la nature plutôt que sur la nature" — géographie intime, le corps dans le paysage.

**Règle utile :** Le lieu n'est pas un décor, il est un personnage.

### Alain Corbin — histoire du sensible

Historien des sensibilités, Paris-I. Œuvres clés :
- "Le Territoire du vide" (1990) — comment les Occidentaux ont appris à désirer la mer
- "Les Cloches de la terre" (1994) — paysage sonore et culture sensible
- "L'Homme dans le paysage" — comment les formes de sensibilité au paysage varient par époque et classe sociale

**Idée exploitable :** Tellux invente une sensibilité nouvelle aux champs EM, comme le XIXe siècle a inventé une sensibilité nouvelle à la mer. "Comment apprend-on à voir ce qu'on ne voyait pas avant ?" C'est le fil narratif de toute la plateforme.

### Auteurs corses de référence

**Patrice Franceschi** — [babelio.com](https://www.babelio.com/livres/Franceschi-Dictionnaire-amoureux-de-la-Corse/1414569)
Romancier, aviateur, marin. Prix Goncourt de la nouvelle 2015. "Dictionnaire amoureux de la Corse" (2022) — pas un dictionnaire, un "dictionnaire d'amour" : entrées libres, angles personnels et inattendus, anti-stéréotypes. Napoléon, Paoli, Colomba, mystères, outlaws d'honneur. Tone à la fois savant et poétique. **Modèle rédactionnel direct pour les fiches A.**

**Ghjuvan Ghjaseppiu Franchi** — génération Riacquistu. Littérature, linguistique, transcription de contes corses. Source pour les formulations en corse.

**Ressource :** [Corsicathèque](https://www.corsicatheque.com/) — 1er média culturel corse. Auteurs en corse et en français.

### Revues de référence

**Les Carnets du Paysage** — [ecole-paysage.fr](https://www.ecole-paysage.fr/fr/publications/les-carnets-du-paysage)
Depuis 1998. Multidisciplinaire : savoirs + design + sciences humaines + arts + littérature. Ton critique, dialogue, proposition. Modèle éditorial : rigueur + pluralité disciplinaire + poésie. Série récente sur les quatre éléments.

---

## 4. Imagerie visuelle corse — sources

**Peintres corses XIXe** — [art-et-ame-culture-corse.fr](https://art-et-ame-culture-corse.fr/peintres-corses/)
Lucien Peri, Canniccioni — paysages corses, maquis, lumière méditerranéenne.

**Gallica BnF** — [gallica.bnf.fr](https://gallica.bnf.fr/)
Fonds numérisé : gravures historiques corses, cartes anciennes, illustrations XIXe. Domaine public. Source pour les images de fiches patrimoine.

**Direction visuelle recommandée pour les images générées :**
Style gravure naturaliste sobre (référents : Atlas de Desmarest 1794, illustrations botaniques BRGM, gravures de voyage corses XVIIIe-XIXe). Palette Tellux : Pierre, Ocre, Maquis, Porphyre. Pas de photorealisme, pas d'illustration numérique générique. Quelque chose entre le carnet de terrain de naturaliste et la planche d'encyclopédie.

---

## 5. Synthèse actionnable pour la session Opus

### Ce que cette veille confirme pour Tellux

1. **Le registre existe** — géopoétique (White), nature writing, dictionnaire amoureux (Franceschi). Tellux n'invente pas un genre, il s'inscrit dans une tradition française vivante.

2. **La figure du Mazzeru est exactement la bonne** — le capteur de l'invisible, le voyant involontaire. Figure pour les contributeurs terrain Tellux.

3. **Atlas Obscura est le concurrent/modèle le plus proche** — mais sans la couche scientifique instrumentée. Tellux est Atlas Obscura avec des données.

4. **Fog of war = système de déblocage** — la métaphore est juste. La carte belle crée l'envie. Le brouillard qui se lève sur les sites visités est le moteur de la collection.

5. **M3C est une mine** — 43 000 documents audio/visuels corses en open access. À exploiter avant de rédiger chaque fiche.

6. **Le style Corbin** — raconter l'apprentissage d'une sensibilité nouvelle aux champs EM comme on raconte l'invention du désir de mer. C'est le fil directeur de toute la narration Tellux.

### Questions à poser à Soleil en session Opus

- Connais-tu le livre de Kenneth White sur la Corse ? C'est un modèle direct.
- As-tu une figure locale (géobiologue, archéologue, berger) qui pourrait être une voix narrative dans les fiches ?
- Quelles images corses t'ont marquée — pas touristiques, des images qui tiennent ensemble la rugosité et la beauté ?
