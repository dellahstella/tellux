# TELLUX — Position épistémique

**Date :** 13 avril 2026
**Statut :** Document de référence interne — fondement de toutes les communications Tellux.
**Auteur :** Soleil / Opus (session 6)

---

## Préambule

Ce document fixe la position épistémique de Tellux : ce que le projet mesure, ce qu'il affirme, ce qu'il n'affirme pas, et pourquoi. Il sert de référence unique pour la rédaction de tous les dossiers, lettres, et supports de communication. Toute formulation dans un document Tellux qui contredit ce texte doit être corrigée.

La nécessité de ce document est apparue quand le porteur du projet a constaté que même les développeurs de Tellux n'étaient pas capables de formuler clairement ce que l'outil fait et ne fait pas. Si les développeurs ne sont pas clairs, les destinataires des lettres ne le seront pas non plus. La clarté épistémique est un test de maturité du projet.

---

## A1 — Ce que Tellux mesure et pourquoi

Tellux mesure le **champ électromagnétique total** en un point géographique donné. Ce champ est la superposition vectorielle de toutes les contributions présentes en ce point, quelle qu'en soit l'origine :

- Le champ magnétique terrestre (IGRF-14, ~46 µT en Corse)
- Les anomalies crustales locales (EMAG2v3 NOAA)
- L'effet piézoélectrique du substrat géologique sous contrainte tectonique
- Le champ magnétique des lignes haute tension (estimation Biot-Savart)
- Le champ électromagnétique des antennes-relais (ANFR)
- Les sources domestiques et industrielles à proximité

Toutes ces contributions obéissent aux mêmes équations de Maxwell. Elles s'expriment dans les mêmes unités (tesla, volt par mètre, décibel-milliwatt). Elles sont détectables par les mêmes instruments (magnétomètre, antenne RF, sonde ELF). Un capteur placé en un point ne distingue pas « l'origine » du champ qu'il mesure : il mesure la résultante.

**Le but de Tellux est d'élaborer le trait d'union entre toutes ces contributions** — pas de les séparer en deux mondes étanches. L'outil identifie les sources, estime leur contribution respective, et restitue une image spatiale du champ total. La séparation en couches (humaine, géologique, tellurique) est un outil d'analyse, pas une affirmation ontologique.

---

## A2 — Pourquoi le mot « naturel » est un piège

Les premières versions des documents Tellux utilisaient l'opposition « perturbation humaine / activité naturelle » comme si ces deux réalités étaient de nature différente. C'est inexact.

Le champ magnétique généré par une ligne HTA et celui généré par une faille tectonique active sont de même nature physique. Un magnétomètre ne fait pas la différence. Les équations de Maxwell ne distinguent pas les « intentions » de la source. Qualifier l'un d'« humain » et l'autre de « naturel » est une commodité de langage — pas une distinction physique.

Le mot « naturel » est particulièrement problématique parce qu'il suggère que le champ d'origine géologique est bénin ou normal, et que seul le champ d'origine humaine pose question. Or :

- Une anomalie magnétique crustale intense peut avoir des effets biologiques mesurables (Maffei 2014)
- Un champ d'antenne à très faible puissance peut être biologiquement négligeable
- L'effet sur un organisme dépend de l'intensité, de la fréquence et de la durée d'exposition — pas de l'origine

**Formulation correcte :** Tellux distingue les *sources* (géologiques, industrielles, domestiques, atmosphériques) pour les identifier et les quantifier séparément. Mais le champ résultant en un point est un seul et même phénomène physique. Dire « deux réalités différentes » est incorrect.

**Usage interne des termes :** Les indices « perturbation réseau » et « activité géologique » restent utilisables comme noms de couches dans l'interface, à condition de ne jamais laisser entendre qu'ils décrivent des phénomènes physiquement incomparables. La distinction est opérationnelle (identifier qui contribue quoi), pas ontologique (deux mondes séparés).

---

## A3 — Pourquoi les mesures s'additionnent

Les documents antérieurs contenaient la phrase : « Les deux ne s'additionnent pas. » C'est inexact. Voici pourquoi.

### Addition vectorielle du champ physique

En un point donné, le champ magnétique total est la somme vectorielle de toutes les contributions :

**B_total = B_terrestre + B_crustal + B_piézo + B_HTA + B_antennes + B_domestique**

C'est une loi fondamentale de l'électromagnétisme (principe de superposition). Les champs s'additionnent, point par point, vecteur par vecteur. Ils ne vivent pas dans des espaces séparés. Un capteur qui mesure 47 µT à un endroit mesure la résultante de toutes les contributions présentes — il n'est pas possible de dire « 46 µT viennent de la Terre et 1 µT vient de la ligne HTA » sans modélisation, parce que physiquement c'est un seul champ.

### Agrégation sémantique des indices Tellux

Le modèle Tellux calcule deux indices (perturbation réseau 0–5, activité géologique 0–5) pour des raisons de lisibilité. Ces indices ne sont pas des mesures physiques directes : ce sont des scores composites qui agrègent plusieurs facteurs (distance, puissance, type de source). Ils sont séparés pour permettre à l'utilisateur de comprendre d'où vient la contribution dominante.

Mais la question « quel est le niveau d'exposition total en ce point ? » a un sens physique. Et la réponse est bien une addition (vectorielle pour les champs, pondérée pour les scores). Les indices *peuvent* être combinés en un indice composite si l'on définit une pondération — et c'est d'ailleurs ce que Tellux fait implicitement quand il calcule un diagnostic de site.

### Ce que « ne s'additionnent pas » voulait dire — et pourquoi c'était mal formulé

L'intention initiale de la phrase était probablement : « un score humain de 3 et un score naturel de 3 ne signifient pas que le site est à 6 sur 10 ». C'est vrai si les échelles ne sont pas linéairement commensurables. Mais la formulation « les deux ne s'additionnent pas » laisse entendre que les phénomènes eux-mêmes sont indépendants, ce qui est physiquement faux.

**Formulation correcte :** « Les deux indices ne se somment pas arithmétiquement (un score de 3 + 3 ne fait pas 6) parce que leurs échelles respectives pondèrent des facteurs différents. Mais les champs physiques sous-jacents s'additionnent bien vectoriellement. Un lieu où les deux indices sont élevés est un lieu où le champ total est la résultante de contributions multiples — c'est précisément l'information que Tellux est conçu pour révéler. »

---

## A4 — Ce que Tellux n'est pas

1. **Tellux n'est pas un diagnostic médical.** L'outil ne fait aucune promesse de santé, ne prescrit aucun comportement, ne qualifie aucun lieu de « dangereux » ou « sain ». Il restitue des données et des estimations avec leurs incertitudes.

2. **Tellux n'est pas un instrument de mesure.** C'est un modèle spatial qui croise des données institutionnelles (ANFR, BRGM, NOAA, IGRF-14) et des mesures terrain contributives. Le modèle a des marges d'erreur documentées (±1 à 2 points sur 10, ±50 % sur les courants HTA). C'est un outil de comparaison relative (site A vs site B), pas une valeur absolue.

3. **Tellux n'est pas un produit commercial.** Pas de publicité, pas de revente de données, pas de solutions de « protection » à vendre. Le code est sous licence MIT. Le projet est porté par une SARL (Stella Canis Majoris) pour la structuration juridique, pas pour la commercialisation.

4. **Tellux n'est pas une plateforme militante.** L'outil ne prend pas position pour ou contre les antennes, les lignes HTA, ou la 5G. Il rend visible ce qui est mesurable et documenté. Les associations qui l'utilisent peuvent en tirer leurs propres conclusions.

5. **Tellux n'est pas terminé.** La base de mesures terrain est embryonnaire (29 mesures ANFR certifiées, zéro mesure citoyenne à ce jour). Le modèle agronomique repose sur des hypothèses formulées mais pas encore testées sur le terrain corse. Les alignements archéoastronomiques sont des résultats statistiques, pas des certitudes historiques. L'outil est en phase de validation, pas de démonstration.

---

## A5 — Ce que Tellux est

1. **Un outil de transparence spatiale.** Tellux rend visible, sur une carte unique, des données qui existent dans des bases séparées (ANFR, BRGM, NOAA, EDF SEI) et que personne n'avait encore croisées à l'échelle de la Corse. Le fait de superposer ces couches sur un même écran produit une information nouvelle que chaque base isolée ne contenait pas.

2. **Un pont entre les échelles.** Le champ électromagnétique en un point est la résultante de phénomènes à toutes les échelles — planétaire (champ terrestre), régionale (géologie crustale), locale (faille, substrat), humaine (antenne, ligne HTA, appareil domestique). Tellux est l'outil qui relie ces échelles et permet de voir leur contribution respective en un lieu donné. Toutes les unités sont impactées par les changements à différentes échelles humaine / non humaine.

3. **Un cadre pour la science participative.** Le formulaire de contribution, le protocole en aveugle parallèle, la hiérarchie de qualité des mesures (A = protocole aveugle parallèle, B = CSV smartphone, C = saisie manuelle unique, D = observation qualitative) — tout cela constitue un cadre méthodologique pour que les mesures citoyennes soient exploitables, et non un simple compteur de signalements.

4. **Un catalyseur de questions.** Les 80 hypothèses testables formulées dans Tellux ne sont pas des affirmations : ce sont des questions structurées, rattachées à des études existantes, avec un type de test explicite (automatique, terrain, crowdsourcé) et un niveau de crédibilité documenté. L'outil est conçu pour poser les bonnes questions, pas pour y répondre prématurément.

---

## A6 — Formulations par public

Le tableau ci-dessous fournit, pour chaque public cible, la formulation de référence à utiliser dans les communications Tellux. Ces formulations sont dérivées des sections A1 à A5 et doivent être considérées comme le standard de rédaction.

### Associations EM (PRIARTEM, CRIIREM, collectifs citoyens)

**Ce qu'on dit :**
Tellux cartographie toutes les sources de champ électromagnétique présentes sur le territoire corse — antennes, lignes haute tension, géologie active — et restitue leur contribution respective en chaque point. L'outil permet de voir, pour la première fois sur une même carte, quelles sources dominent en un lieu donné, avec quel niveau de confiance, et selon quelles données.

**Ce qu'on ne dit plus :**
« Deux réalités différentes. » « Les deux ne s'additionnent pas. » « Perturbation humaine vs activité naturelle » comme opposition ontologique.

**Ce qu'on dit à la place :**
Les indices « perturbation réseau » et « activité géologique » identifient les sources. Mais le champ physique en un point est une seule grandeur, résultante de toutes les contributions. Les indices ne se somment pas arithmétiquement — mais les champs, eux, s'additionnent vectoriellement. C'est cette résultante que Tellux est conçu pour rendre lisible.

---

### Agronomie et permaculture (groupements bio, LPO, chambres d'agriculture)

**Ce qu'on dit :**
Tellux est le premier outil gratuit qui croise le profil électromagnétique d'une parcelle avec son substrat géologique et des recommandations culturales. Les études récentes (Baydiili 2025, Hermans 2023) montrent un impact mesurable des lignes HTA sur le microbiome du sol. Tellux permet de visualiser où ces impacts sont les plus probables, et quelles cultures locales corses y sont les plus résilientes.

**Ce qu'on ne dit plus :**
« Les deux ne s'additionnent pas » dans le contexte agronomique. (Le champ total est ce que le sol et les organismes subissent.)

**Ce qu'on dit à la place :**
Le champ au niveau du sol est la résultante de toutes les contributions. Un sol situé sous une ligne HTA, sur un substrat granitique piézoélectrique actif, est exposé à un champ total qui combine ces deux contributions — et c'est ce champ total qui a un effet biologique.

---

### Mairies et patrimoine (communes, DRAC, associations patrimoine)

**Ce qu'on dit :**
Tellux cartographie les 116 sites mégalithiques et les 314 églises romanes de Corse avec leur profil géophysique. Le modèle géométrique (alignements Broadbent 1980, orientations solsticiales Hoskin/Santucci) et l'analyse du substrat (piézoélectricité, anomalies crustales) ouvrent des pistes sur le choix d'implantation des constructeurs anciens. Ce sont des résultats statistiques vérifiables, pas des certitudes historiques.

**Ce qu'on ne dit plus :**
Rien de spécifiquement erroné dans l'ancien dossier mairies sur ce plan — mais les formulations doivent intégrer le fait que l'environnement EM d'un site patrimonial est une seule réalité physique, mesurable, qui résulte de la superposition de toutes les sources.

---

### Scientifiques (géophysiciens, bioEM, archéoastronomie, agronomie EM)

**Ce qu'on dit :**
Le modèle Tellux calcule la contribution estimée de chaque source EM identifiable en un point géographique, à partir de données institutionnelles vérifiables. 80 hypothèses testables sont formulées, classées par type de test et niveau de crédibilité. Le corpus comprend 130 études sur 3 niveaux (A = peer-reviewed intégrées, B = exploratoires documentées, C = exclues avec justification). Les limites du modèle sont documentées dans l'interface.

**Ce qu'on ne dit plus :**
Toute formulation qui laisserait entendre que les « contributions humaines » et les « contributions naturelles » sont de nature physique différente. Pour un physicien, c'est une erreur. Pour un biologiste, c'est trompeur (l'organisme subit le champ total). Pour un agronome, c'est sous-informant (le sol ne distingue pas la source).

---

### CTC / OEC / ADEME (dossier candidature institutionnel)

**Ce qu'on dit :**
Tellux est un outil de transparence territoriale qui rend visible, sur une carte interactive unique, l'environnement électromagnétique de chaque point du territoire corse. L'outil croise des données institutionnelles (ANFR, BRGM, NOAA, EDF SEI) avec un système de contribution citoyenne structuré. Il est open-source, gratuit, et ne commercialise aucun service. Il est conçu pour servir de support de dialogue entre les habitants, les élus, les associations et les chercheurs — sur une base factuelle, documentée, avec ses incertitudes expliquées.

**Ce qu'on ne dit plus :**
Toute opposition « humain / naturel » présentée comme deux mondes séparés. Toute formulation qui laisserait entendre que Tellux est un outil de dénonciation ou un diagnostic de santé.

---

## Synthèse : les trois erreurs à ne plus commettre

1. **« Deux réalités différentes »** → Non. Un seul phénomène physique, des sources multiples identifiables séparément.

2. **« Les mesures ne s'additionnent pas »** → Inexact. Les champs s'additionnent vectoriellement. Les indices ne se somment pas arithmétiquement, mais cela ne signifie pas que les phénomènes sont indépendants.

3. **« Naturel = bénin, humain = problématique »** → Raccourci non fondé. L'effet biologique dépend de l'intensité, de la fréquence et de la durée — pas de l'étiquette de la source.

---

*Ce document est la référence épistémique de Tellux. Tout dossier, lettre ou support de communication doit être relu à la lumière de ce texte avant envoi.*
