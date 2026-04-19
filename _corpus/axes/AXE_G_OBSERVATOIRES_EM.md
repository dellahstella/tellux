# Fiche de recherche Tellux — Axe G : Observatoires EM territoriaux comparables

**Date :** 2026-04-19  
**Projet :** Tellux Corse — Cadre scientifique v2, benchmark méthodologique  
**Axe :** G — Benchmark international des projets cartographiques EM, positionnement Tellux  
**Statut :** Recherche complète — document de référence v1  
**Auteur corpus :** Cowork / Claude (Anthropic) sur brief Soleil, SARL Stella Canis Majoris

---

## Contexte et objectif

Cette fiche cartographie les projets similaires à Tellux à l'échelle nationale et internationale, pour positionner Tellux de façon précise dans le paysage existant — ni en doublon de l'existant, ni dans un vide absolu. Le résultat principal : **Tellux occupe une niche non couverte** (cartographie intégrée multi-couches avec modèle de calcul territorial, ancrage géologique et patrimonial, à l'échelle d'un territoire insulaire) tout en s'inscrivant dans des pratiques méthodologiques documentées.

---

## Q1 — Plateformes institutionnelles officielles

### 1.1 CartoRadio — ANFR, France

**Institution :** Agence Nationale des Fréquences (ANFR)  
**Nature :** Portail officiel de cartographie des stations radioélectriques et des mesures d'exposition en France.

**Ce que CartoRadio fait :**
- Localisation de toutes les stations radioélectriques autorisées (mobiles, radiodiffusion, liaisons fixes) sur le territoire national
- Simulation du champ électrique (V/m à 1,5m du sol) par modélisation — cumul de toutes les émissions des opérateurs mobiles autorisés
- Publication des mesures de terrain réalisées sur demande (gratuites, accès libre)
- Open data depuis le 1er janvier 2014 : [data.anfr.fr](https://data.anfr.fr)
- Statistiques par commune/département/région depuis octobre 2021 (dont 5G par opérateur)
- Outil de simulation de projet de construction d'antenne

**Ce que CartoRadio ne fait pas :**
- Aucune couche géologique
- Aucune couche patrimoniale
- Aucun score composite ou indicateur territorial
- Pas de champ ELF (50 Hz, réseau électrique) — uniquement RF
- Pas d'intégration des sources HTA/HTB ou EMAG2
- Pas de donnée corse spécifique : même interface nationale que partout

**Limites méthodologiques documentées :**
- Les cartes d'exposition sont des **modèles prédictifs**, pas des mesures. Calibration sur les mesures terrain, mais non validation point-à-point.
- La résolution spatiale de la simulation est limitée par le modèle de propagation (bâtiments intégrés annuellement).
- L'affichage est en V/m (RF uniquement) — pas convertible directement en nT Tellux sans hypothèse d'onde plane.

**Source :** [cartoradio.fr](https://www.cartoradio.fr/) | [ANFR présentation](https://www.anfr.fr/en/maitriser/cartoradio/presentation-cartoradio) | [BEREC France EMF](https://www.berec.europa.eu/en/berec/emf-related-country-specific-information-for-france)

**Niveau de confiance :** Source primaire officielle.  
**Applicabilité Tellux :** CartoRadio est déjà intégré à Tellux comme source de données. Tellux ne remplace pas CartoRadio — il l'intègre et le contextualise.

---

### 1.2 EMF-Datenportal / EMF-Karte — Bundesnetzagentur, Allemagne

**Institution :** Bundesnetzagentur (Agence fédérale des réseaux allemande) + BfS (Bundesamt für Strahlenschutz)

**Nature :** Cadastre national des sites radioélectriques et des mesures EM.

**Ce que le système allemand fait :**
- EMF-Datenportal : base de données librement accessible des sites certifiés (certification de site obligatoire en Allemagne)
- EMF-Karte : carte nationale de tous les sites certifiés
- Mesures de terrain : > 1 000 visites annuelles de la Bundesnetzagentur
- Accès sécurisé pour les autorités municipales (cadastre communal)
- Résultats des séries de mesures publiés en ligne

**Différences avec CartoRadio :**
- Accent sur la certification de site (Standortbescheinigung) plutôt que sur la simulation continue
- Accès différencié : public (consultation) vs municipal (administration)
- BfS assure la recherche scientifique en parallèle

**Sources :** [bundesnetzagentur.de EMF](https://emf2.bundesnetzagentur.de/) | [BEREC Germany EMF](https://www.berec.europa.eu/en/tasks/electromagnetic-fields/emf-related-country-specific-information-for-germany)

---

### 1.3 Sitefinder — Ofcom, Royaume-Uni (FERMÉ)

**Institution :** Ofcom (Office of Communications)  
**Nature :** Base de données des antennes mobiles au Royaume-Uni.  
**Dates :** Créé → ouverture publique partielle 2013 (sous pression légale) → fermeture en 2015.

**Historique et raisons de fermeture :**
Sitefinder a été établi à la suite des recommandations du rapport Stewart (2000) pour informer le public sur les sites individuels. La publication complète des données a été obtenue en mars 2013 après **une bataille juridique extrêmement longue** sous les Environmental Information Regulations.

**Résistances documentées à la publication :**
1. Risque de vandalisme : la publication exacte des localisations permettrait de cibler les pylônes pour vol de métaux (contexte 2013 : prix des métaux élevés)
2. Risque terroriste : carte complète d'un réseau = carte d'attaque
3. Problèmes commerciaux : données sensibles pour la compétition entre opérateurs

**Fermeture en 2015 :** Arrêt du service Ofcom Sitefinder. Les données ont été archivées à l'Université d'Édimbourg (Datashare).

**Remplaçant actuel :** Pas de successeur direct public national équivalent au Royaume-Uni. Les opérateurs publient des données partielles.

**Leçons pour Tellux :**
- La sécurité et la confidentialité commerciale sont des obstacles réels à la transparence des données EM
- Un portail purement "où sont les antennes" sans valeur ajoutée analytique est fragile institutionnellement
- La valeur ajoutée de Tellux (modèle de calcul + contexte territorial) le différencie de Sitefinder

**Sources :** [Sitefinder Archive Edinburgh](https://datashare.ed.ac.uk/handle/10283/2626) | Pinsent Masons — Ofcom appeals | WhatDoTheyKnow FOI

---

### 1.4 BEREC — Panorama européen

**Institution :** Body of European Regulators for Electronic Communications  
**Nature :** Instance de coordination des régulateurs nationaux européens, publie des fiches pays sur les dispositifs EMF.

**Disponibilité par pays :** France, Allemagne, Belgique, Italie, Roumanie, etc. — fiches standardisées.

**Intérêt pour Tellux :** Source de comparaison des approches réglementaires européennes. La France (CartoRadio + mesures gratuites) est citée comme bonne pratique.

**Source :** [BEREC EMF](https://www.berec.europa.eu/en/tasks/electromagnetic-fields)

---

## Q2 — Projets de recherche académiques européens

### 2.1 GERoNiMO — FP7 European Commission

**Titre complet :** Generalised EMF Research using Novel Methods — an integrated approach: from research to risk assessment and support to risk management

**Financement :** FP7 European Commission, grant agreement 603794  
**Coordinateur :** ISGlobal Barcelona (Prof. Elisabeth Cardis)  
**Partenaires :** 19 institutions de recherche, 13 pays  
**Durée :** 2013-2019  
**CORDIS :** [cordis.europa.eu/project/id/603794](https://cordis.europa.eu/project/id/603794)

**Ce que GERoNiMO a fait :**
- Évaluation des effets sur la santé (développement cognitif enfants, risque cancer, effets reproductifs) d'exposition RF et IF
- Développement de méthodes d'évaluation de l'exposition RF (dont contribution par sources)
- Mécanismes biologiques (cancer, Alzheimer, vieillissement)
- Modélisation de l'impact sanitaire et outil d'aide à la décision
- Publication clé : *"Radio-frequency electromagnetic field exposure and contribution of sources in the general population: an organ-specific integrative exposure assessment"* — J Exposure Science & Environmental Epidemiology, Nature (2021)

**Ce que GERoNiMO n'a pas fait :**
- Pas de cartographie territoriale intégrée avec géologie ou patrimoine
- Pas de plateforme publique interactive
- Pas de dimension corse ou méditerranéenne spécifique

**Intérêt pour Tellux :** GERoNiMO a produit les méthodologies d'évaluation de l'exposition RF les plus rigoureuses disponibles en Europe. Ses publications peuvent être citées pour justifier les méthodes d'agrégation de Tellux.

---

### 2.2 Programme Horizon Europe — EMF et santé

**CORDIS programme :** HORIZON-HLTH-2021-ENVHLTH-02-01 — "Exposure to electromagnetic fields (EMF) and health"

La Commission européenne continue de financer des projets EMF et santé dans le cadre d'Horizon Europe, signalant que le sujet est reconnu comme priorité de recherche en Europe.

---

### 2.3 Méthodologie optimale de cartographie EM — publications récentes

**Publication de référence (2024) :**
- **Auteurs :** Lopez-Espi P.-L. et al.
- **Titre :** "Optimal design of electromagnetic field exposure maps in large areas"
- **Revue :** Environmental Impact Assessment Review
- **Année :** 2024
- **Accès :** [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0195925524001124) | [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4719378)

**Données clés :**
- Grille de 250 m de côté comme unité de base recommandée
- Densité de points de mesure : **8 à 10 points par km² en zone urbaine**
- Conditions LOS (Line of Sight) pour réduire le nombre de points requis
- Analyse en zones urbaines ET rurales documentée

**Publication complémentaire (2025) :**
- **Titre :** "Efficient design of electromagnetic field exposure maps with multi-method evolutionary ensembles"
- **Revue :** Environment International
- **PubMed :** PMID:40250582
- **Accès :** [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0013935125008874)

**Revue ML/taxonomy (2025) :**
- "Electromagnetic Field Distribution Mapping: A Taxonomy and Comprehensive Review of Computational and Machine Learning Methods" — MDPI Electronics 2025. Modèles analytiques, interpolation géostatistique, apprentissage profond.

**Application Tellux :** Ces publications fournissent la base méthodologique peer-reviewed pour la Phase 2 de contribution citoyenne. Le grid de 250m recommandé est directement applicable au protocole de collecte Tellux.

---

## Q3 — Initiatives associatives et militantes avec dimension cartographique

### 3.1 ElectrosmogMap — statut ambigu

**Résultat de la recherche :** Le nom "ElectrosmogMap" n'est pas indexé dans les bases de données scientifiques. Plusieurs plateformes de cartographie EM citoyenne existent sous des noms variables, mais aucune n'a de publication peer-reviewed associée.

**Ce qui existe dans ce registre :**

| Plateforme | Nature | Qualité données | Documentation |
|-----------|--------|----------------|---------------|
| ElectroSmart (France) | RF-EMF via smartphone | ±30–300% | Publication ResearchGate partielle |
| Next-Up (France) | Asso anti-ondes, mesures terrain | Non calibrées systématiquement | Non peer-reviewed |
| WaveMapper (USA) | Crowdsourced RF | Qualité variable | Application mobile |
| MapEM (Wavecontrol) | Solution commerciale professionnelle | Professionnelle | Documentation constructeur |

**Verdict :** Il n'existe pas de plateforme associative de cartographie EM crédible scientifiquement et bien documentée en Europe à ce stade. La niche existe. Tellux peut revendiquer de la combler.

---

### 3.2 Design intégré d'une plateforme résidentielle RF — étude académique

**Référence :**
- "Design of an Integrated Platform for Mapping Residential Exposure to RF-EMF Sources" — *International Journal of Environmental Research and Public Health*, MDPI, 2020, 17(15):5339

Cette étude académique documente une architecture de plateforme intégrée pour mesurer l'exposition résidentielle RF. Elle est plus proche de ce que Tellux vise que les initiatives associatives.

---

## Q4 — Plateformes hybrides citizen-institutionnel : les modèles de référence

### 4.1 Sensor.Community (ex-Luftdaten.info) — modèle de référence pour Tellux Phase 2

**Nature :** Réseau mondial de science citoyenne pour la qualité de l'air et l'environnement.  
**Origine :** OK Lab (Open Knowledge Lab) Stuttgart — Allemagne.  
**Évolution :** Luftdaten.info (avant novembre 2019) → Sensor.Community.

**Données clés :**
- **~35 346 stations actives dans le monde** (données récentes)
- Capteurs DIY : PM2.5, PM10, bruit, température, humidité
- **Pas de mesure EM** — c'est la différence avec Tellux
- Hardware open source (plans de construction libres)
- Données libres, API ouverte, format JSON/CSV

**Modèle organisationnel :**
- Pas de financement central initial — croissance organique par les communautés locales
- OK Lab Stuttgart → réplication dans +100 villes
- Gouvernance décentralisée : chaque laboratoire est autonome
- Validation croisée avec stations officielles documentée

**Leçons transposables à Tellux :**

| Aspect Sensor.Community | Transposition Tellux |
|------------------------|---------------------|
| Hardware open source → confiance | Protocole de mesure open source + liste appareils recommandés |
| API ouverte → réutilisation | API Supabase ouverte en lecture publique |
| Communauté locale autonome | Groupes contributeurs par micro-région corse |
| Validation vs données officielles | Validation vs ANFR CartoRadio + données BRGM |
| Grille de snap géographique | Snap 250m zones résidentielles (RGPD) |

**Sources :** [sensor.community](https://sensor.community/en/) | [aqicn.org/network/luftdaten](https://aqicn.org/network/luftdaten/) | Nature article npj Climate Atmospheric Science 2025

---

### 4.2 OpenAQ — agrégation données officielles + citoyennes

**Nature :** Plateforme open source d'agrégation de données qualité de l'air, officielles ET citoyennes.  
**Modèle :** Pas de collecte propre — agrégation de sources hétérogènes dans un format unifié.

**Principe intéressant pour Tellux :** L'architecture OpenAQ permet d'ingérer des données de qualité et de résolution variables, avec métadonnées de qualité associées. Un modèle similaire pour Tellux Phase 2 permettrait d'ingérer les mesures ANFR officielles ET les mesures contributeurs citoyens dans le même flux, avec scoring de fiabilité.

---

## Q5 — Observatoires environnementaux institutionnels : benchmarks d'architecture

### 5.1 Atmo France — réseau national qualité de l'air

**Nature :** Réseau de 18 Associations Agréées de Surveillance de la Qualité de l'Air (AASQA), une par région administrative.

**Caractéristiques clés :**
- **Modèle réglementaire :** Agrément étatique, financement mixte (État, collectivités, industriels)
- **Méthode :** Mesures fixes + campagnes mobiles + **modélisation numérique** (météorologie, émissions, topographie, chimie atmosphérique)
- **Résolution atteinte :** 25 mètres (par modélisation urbaine fine)
- **Production quotidienne :** > 300 cartes/jour par AASQA
- **Données ouvertes :** Atmo Data [atmosud.org/atmo-data]

**Modèle organisationnel transposable à Tellux :**
- La Corse est actuellement couverte par **AtmoSud** (région PACA + Corse)
- L'antenne corse de cette association est relativement peu développée
- Un partenariat Tellux-AtmoSud permettrait d'ajouter une couche qualité de l'air aux couches existantes

**Source :** [atmo-france.org/article/la-cartographie](https://www.atmo-france.org/article/la-cartographie) | Notice technique AASQA 2020

---

### 5.2 Bruitparif — l'observatoire du bruit comme modèle le plus proche de Tellux

**Nature :** Observatoire du bruit de l'Île-de-France, association à but non lucratif créée en 2004 par le Conseil régional d'Île-de-France.

**Ce qui le rend remarquable (Guinness World Records 2022) :**
- Réseau RUMEUR : **~200 stations de mesure permanentes** — plus grand réseau urbain de surveillance du bruit au monde (reconnu par le Livre Guinness 2022)

**Méthode documentée :**
- Mesures permanentes + campagnes ponctuelles
- **Modélisation numérique** (bruit n'est pas mesuré partout — il est calculé à partir du modèle)
- Cartographies stratégiques (EU Environmental Noise Directive)
- Croisement bruit + qualité de l'air avec Airparif (2024 : première cartographie croisée qualité-air-son en Île-de-France)

**Analogies avec Tellux :**

| Bruitparif | Tellux |
|-----------|--------|
| Bruit (dB) en zone urbaine | EM territorial (nT, dBm) |
| Modèle de calcul territorial | Modèle de calcul territorial |
| Données officielles + mesures terrain | Données ANFR + contributions citoyennes |
| Multi-sources agrégées | Multi-sources agrégées |
| Croisement avec qualité de l'air | Croisement avec géologie + patrimoine |
| Observatoire régional (Île-de-France) | Observatoire territorial (Corse) |
| Financement Conseil régional | Financement CTC potentiel |

**Bruitparif est le modèle institutionnel le plus proche de ce que Tellux pourrait devenir.** Même logique, même positionnement (observatoire territorial mandaté par la collectivité), même méthode hybride mesures+modélisation.

**Source :** [bruitparif.fr](https://www.bruitparif.fr/) | Airparif croisement 2024

---

## Q6 — Cadres méthodologiques pour observatoires scientifiques

### 6.1 LTER — Long-Term Ecological Research Network

**Institution :** NSF (USA) + International LTER (ILTER, 44 réseaux nationaux)  
**Fondé :** 1980 (NSF LTER)  
**Échelle :** 27 sites USA, >700 sites ILTER internationaux, >1800 chercheurs

**Principes LTER applicables à Tellux :**

1. **Long-terme obligatoire :** Les processus écologiques ne se comprennent qu'avec des séries temporelles longues. Idem pour les EM territoriaux.
2. **Basé sur un lieu (place-based) :** Chaque site LTER est ancré dans un territoire spécifique — exactement comme Tellux est ancré en Corse.
3. **Données FAIR :** Environmental Data Initiative (EDI) = dépôt de référence, aligné FAIR.
4. **Science ouverte et inclusive :** Open data, publications open access recommandées.
5. **Gouvernance explicite :** Chaque site a une politique de gestion des données documentée.

**Source :** [lternet.edu/about](https://lternet.edu/about/) | BioScience 72(9):814 (2022) — Long-Term Ecological Research on Ecosystem Responses to Climate Change. PMC9405729.

---

### 6.2 Zones Ateliers CNRS (ZA/RZA)

**Institution :** CNRS/InEE (Institut national d'écologie et de l'environnement)  
**Nature :** Infrastructure nationale de recherche — 16 zones labélisées, réseau LTSER (Long-Term Socio-Ecological Research)

**Caractéristiques :**
- **>1800 personnels de recherche** de 25 organismes, 80 universités, 26 écoles d'ingénieurs
- **>200 publications peer-reviewed par an** (données 2020)
- Approche : sciences naturelles + sciences humaines + ingénierie = transdisciplinarité
- Organisé autour d'un élément structurant : fleuve, littoral, parc naturel, agglomération
- Couplage bio-géophysique + écologique + sociétal

**Zones Ateliers existantes :**
- ZA Bassin du Rhône, ZA Moselle, ZA Armorique, ZA Alpes, ZA Fessenheim (nucléaire)...
- **Pas de Zone Atelier en Corse** — lacune institutionnelle potentiellement comblée par Tellux à terme

**Pertinence pour Tellux :**
Si Tellux atteint une masse critique de données et de partenariats institutionnels, il pourrait se positionner comme embryon d'une **Zone Atelier corse** — l'équivalent CNRS d'un observatoire territorial multi-dimensionnel. La Corse correspond exactement à la définition (île, littoral, maquis, sites patrimoniaux, tensions anthropiques mesurables).

**Source :** [inee.cnrs.fr/fr/zones-ateliers](https://www.inee.cnrs.fr/fr/zones-ateliers) | [za-inee.org](https://www.za-inee.org/fr/reseau)

---

## Q7 — Échecs documentés : cas d'étude

### 7.1 Sitefinder UK (2000–2015) — analyse détaillée

**Leçon principale :** Un portail qui liste uniquement des localisations de sites (pin points) sans valeur ajoutée analytique est institutionnellement fragile.

**Chronologie :**
- 2000 : Rapport Stewart recommande la transparence sur les sites
- 2000–2013 : Ofcom maintient Sitefinder, résiste à la publication complète
- 2013 : Publication forcée des données sous Environmental Information Regulations après bataille juridique
- 2015 : Fermeture du service Sitefinder

**Raisons de résistance documentées :**
- **Sécurité :** Vandalisme des pylônes (vol de métaux — contexte économique 2010-2013), risques terroristes
- **Commercial :** Données sensibles pour la compétition inter-opérateurs
- **Légitimité limitée :** "Pas destiné à être un outil d'ingénierie ou de planification, mais une ressource générale"

**Ce que Sitefinder n'a jamais été :**
- Un outil de modélisation d'exposition
- Un outil de contextualisation territoriale
- Un outil scientifique

**Leçon pour Tellux :** La valeur de Tellux réside dans son modèle de calcul et son intégration territoriale — pas dans la simple liste de sites. Un outil qui calcule est plus défendable qu'un outil qui liste.

---

### 7.2 Projets EM en sommeil ou insuffisamment structurés

**Pattern observé dans la recherche :**
- Les initiatives associatives de cartographie EM n'ont pas de publication peer-reviewed associée
- La plupart n'ont pas de protocole de calibration documenté
- La plupart n'ont pas de gouvernance des données explicite (licence, RGPD)
- Résultat : crédibilité limitée auprès des institutions, durée de vie courte

**Piège à éviter :** Ne pas reproduire ce pattern. Tellux doit avoir dès le lancement : protocole documenté, licence open data, gouvernance RGPD, validation croisée avec données officielles.

---

## Q8 — Positionnement Tellux dans le paysage international

### 8.1 Tableau comparatif synthétique

| Projet | Institution | Périmètre | Modèle de calcul | Géologie/Patrimoine | Contribution citoyenne | Gouvernance |
|--------|-----------|----------|-----------------|--------------------|-----------------------|------------|
| **CartoRadio** | ANFR (F) | RF national | Oui (simulation V/m) | Non | Non | Publique réglementaire |
| **EMF-Datenportal** | BNetzA (D) | RF national | Mesures (pas modèle continu) | Non | Non | Publique réglementaire |
| **Sitefinder** | Ofcom (UK) | RF national | Non (pin points) | Non | Non | Publique (fermé 2015) |
| **GERoNiMO** | ISGlobal/FP7 | Exposition populationnelle | Oui (exposition individuelle) | Non | Non | Académique européen |
| **ElectroSmart** | Startup (F) | RF urbain | Non (mesures smartphone) | Non | Oui (non calibré) | Privé |
| **Sensor.Community** | OK Lab (D) | Air + environnement | Non (mesures) | Non | Oui (DIY calibré) | Open source |
| **Bruitparif** | Collectivité (F) | Bruit Île-de-France | Oui (modélisation numérique) | Non | Non | Observatoire régional |
| **Atmo France** | AASQA (F) | Air qualité régional | Oui (modélisation chimique) | Non | Partielle | Agréé État |
| **LTER** | NSF/CNRS | Écologie long terme | Oui (multi-variables) | Oui (partiel) | Partielle | Scientifique national |
| **TELLUX** | SARL/CTC (Corse) | EM multi-couches + patrimoine Corse | **Oui (calcul territorial)** | **Oui (géologie + sites)** | Phase 2 (calibré) | Territorial insulaire |

**Tellux est le seul projet qui combine :**
1. Modèle de calcul territorial (pas juste affichage de sites)
2. Intégration géologie + champ anthropique + patrimoine
3. Échelle d'un territoire insulaire avec identité propre
4. Ouverture vers la contribution citoyenne avec protocole calibré

---

### 8.2 Paragraphe de positionnement — utilisable directement dans le dossier CTC

*"Tellux Corse s'inscrit dans un paysage européen d'outils cartographiques électromagnétiques en plein développement, tout en occupant une niche spécifique non couverte. Les portails institutionnels existants (CartoRadio ANFR en France, EMF-Datenportal en Allemagne) se limitent aux sources radioélectriques autorisées, sans modèle territorial intégré ni contextualisation géologique ou patrimoniale. Les projets académiques européens (GERoNiMO, FP7) s'intéressent à l'exposition populationnelle mais ne produisent pas d'outil territorial interactif. Les initiatives associatives de mesure participative ne disposent pas de protocoles de calibration scientifiquement défendables.*

*Tellux s'inspire du modèle Bruitparif (observatoire territorial mandaté par une collectivité, combinant modélisation et mesures de terrain) et des bonnes pratiques de science citoyenne de Sensor.Community (hardware calibré, open data, validation croisée), en les appliquant pour la première fois au contexte électromagnétique d'un territoire insulaire méditerranéen. L'intégration des données ANFR CartoRadio, BRGM, IGRF-14 et EMAG2 dans un modèle de calcul unifié, couplée à un inventaire patrimonial actualisé (sites mégalithiques, patrimoine roman) et à une ouverture vers les contributions citoyennes calibrées, constitue une contribution originale que ni les outils institutionnels ni les plateformes associatives existants ne proposent.*

*Tellux ne remplace pas CartoRadio — il l'intègre. Il ne doublon pas les projets associatifs — il les complète par une rigueur méthodologique documentée. Il ne prétend pas être un observatoire scientifique validé — il en pose les fondations institutionnelles pour la Corse."*

---

### 8.3 Opportunités de partenariats identifiées

| Partenaire potentiel | Nature | Type de partenariat |
|---------------------|--------|---------------------|
| **ANFR** | Portail réglementaire national | Données CartoRadio (déjà intégré) — possibilité d'accord formel pour données Corse |
| **BRGM** | Géologie et risques | Données géologiques, failles, lithologies corses |
| **AtmoSud** | Qualité de l'air régional | Croisement couches EM + qualité air Corse |
| **Université de Corse — laboratoire SPE (UMR 6134)** | Recherche environnementale | Validation scientifique, publications communes |
| **ISGlobal Barcelona** | Épidémiologie environnementale | Méthodologies d'exposition (GERoNiMO) |
| **CNRS/InEE** | Infrastructure nationale | Embryon de Zone Atelier corse (horizon 5-10 ans) |
| **INRAP Corse** | Archéologie | Données patrimoniales actualisées |
| **Office de l'Environnement de la Corse (OEC)** | Données milieux naturels | Couches environnementales (zones protégées, biodiversité) |

---

## Bonnes pratiques méthodologiques synthèse

### Issues des benchmarks, transposables à Tellux Phase 2

**1. Grille de mesure standardisée (Lopez-Espi 2024)**
- 250 m de côté comme unité de base
- 8–10 points/km² en zone urbaine
- Conditions LOS documentées
- → Protocole de contribution citoyenne Tellux Phase 2

**2. Modélisation + mesures = approche hybride (Bruitparif, Atmo)**
- Les mesures seules ne couvrent pas tout le territoire
- La modélisation seule manque de validation terrain
- L'hybride mesures + modèle est la norme dans les observatoires matures

**3. Open data dès le départ (Sensor.Community, LTER)**
- Les données ouvertes dès le lancement créent la confiance institutionnelle
- Licence ODbL pour les données, CC-BY pour les cartes dérivées

**4. Gouvernance explicite (LTER, Zones Ateliers)**
- Politique de données documentée et publique
- Comité scientifique ou de validation (même informel au départ)
- Processus de révision des données erronées

**5. Validation croisée précoce (Safecast, Sensor.Community)**
- La première campagne de validation (mesures Tellux vs mesures ANFR) est fondatrice de la crédibilité

---

## Bibliographie Axe G

1. **ANFR** — CartoRadio : présentation, méthodologie et open data. [anfr.fr](https://www.anfr.fr/en/maitriser/cartoradio/presentation-cartoradio) | [data.anfr.fr](https://data.anfr.fr)

2. **BEREC** — "EMF related country-specific information for France / Germany / Belgium / Italy." Body of European Regulators for Electronic Communications. [berec.europa.eu/en/tasks/electromagnetic-fields](https://www.berec.europa.eu/en/tasks/electromagnetic-fields)

3. **Bundesnetzagentur** — EMF-Datenportal, EMF-Karte. Agence fédérale des réseaux, Allemagne. [emf2.bundesnetzagentur.de](https://emf2.bundesnetzagentur.de/)

4. **Sitefinder Archive** — Sitefinder Mobile Phone Base Station Database (archivé). University of Edinburgh DataShare. [datashare.ed.ac.uk/handle/10283/2626](https://datashare.ed.ac.uk/handle/10283/2626)

5. **CORDIS / ISGlobal** — GERoNiMO project (FP7, grant 603794). 2013-2019. [cordis.europa.eu/project/id/603794](https://cordis.europa.eu/project/id/603794)

6. **Lopez-Espi P.-L. et al.** (2024). "Optimal design of electromagnetic field exposure maps in large areas." *Environmental Impact Assessment Review*. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0195925524001124)

7. **PubMed 40250582** (2025). "Efficient design of electromagnetic field exposure maps with multi-method evolutionary ensembles." *Environment International*. [ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0013935125008874)

8. **MDPI Electronics 2025** — "Electromagnetic Field Distribution Mapping: A Taxonomy and Comprehensive Review." [mdpi.com/2073-431X/14/9/373](https://www.mdpi.com/2073-431X/14/9/373)

9. **Sensor.Community** — Réseau mondial science citoyenne qualité de l'air. [sensor.community/en](https://sensor.community/en/) | Nature npj Climate & Atmospheric Science 2025.

10. **Atmo France** — Réseau AASQA, cartographie, modélisation. [atmo-france.org/article/la-cartographie](https://www.atmo-france.org/article/la-cartographie)

11. **Bruitparif** — Observatoire du bruit d'Île-de-France, réseau RUMEUR. [bruitparif.fr](https://www.bruitparif.fr/) | Airparif croisement qualité-air-son 2024.

12. **LTER Network** — About the Network. [lternet.edu/about](https://lternet.edu/about/) | Peters D.P.C. et al. (2022) "Long-Term Ecological Research on Ecosystem Responses to Climate Change." *BioScience*, 72(9):814. PMC9405729.

13. **CNRS/InEE** — Réseau des Zones Ateliers (RZA). [inee.cnrs.fr/fr/zones-ateliers](https://www.inee.cnrs.fr/fr/zones-ateliers) | [za-inee.org](https://www.za-inee.org/fr/reseau)

14. **MDPI IJERPH 2020** — "Design of an Integrated Platform for Mapping Residential Exposure to RF-EMF Sources." 17(15):5339. [mdpi.com/1660-4601/17/15/5339](https://www.mdpi.com/1660-4601/17/15/5339)

---

## Note épistémique finale

La recherche Axe G confirme une conclusion structurelle importante : **Tellux n'a pas d'équivalent direct.** Ce n'est pas un signe d'isolement — c'est une preuve de positionnement dans une niche non encore occupée.

Les outils institutionnels couvrent les sites officiels. Les projets académiques couvrent l'exposition populationnelle. Les initiatives associatives couvrent la sensibilisation militante. Les observatoires environnementaux matures couvrent d'autres dimensions (bruit, air). **Aucun ne combine calcul territorial EM + géologie + patrimoine + ancrage insulaire + ouverture citoyenne calibrée.**

La prochaine étape institutionnelle logique pour Tellux, après la candidature CTC, serait d'engager des discussions avec AtmoSud (Corse), le laboratoire SPE de l'Université de Corse, et éventuellement CNRS/InEE pour explorer les possibilités d'une Zone Atelier corse à spectre élargi incluant la dimension EM. Ce serait le passage de "projet Tellux" à "infrastructure de recherche territoriale".

---

*Document Tellux — Usage interne et candidature CTC — Ne pas diffuser sans accord Soleil, SARL Stella Canis Majoris*
