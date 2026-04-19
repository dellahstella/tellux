# Axe N — Sites sacrés corses et co-exposition EM / ionisante
**Projet Tellux Corse — Cadre scientifique long terme**  
**Date : 2026-04-19**  
**Statut : document de recherche, corpus interne**  
**Nature : revue documentaire + cadre méthodologique pour test statistique territorial**

---

## Note préliminaire

Ce document ne cherche pas à démontrer que les constructeurs mégalithiques corses avaient une connaissance explicite des champs électromagnétiques ou de la radioactivité. Il établit le cadre documentaire et méthodologique pour tester une **corrélation statistique** entre la localisation des sites mégalithiques validés et des variables bio-géophysiques mesurables. Une corrélation ne prouve pas une causalité intentionnelle. Son absence serait un résultat scientifique tout aussi valable.

Aucune source ésotérique n'est citée dans ce document. Toutes les données de référence proviennent d'institutions scientifiques (BRGM, IRSN/ASNR, NOAA, académies) ou de publications peer-reviewed.

---

## 1. Inventaire géoréférencé validé des sites mégalithiques corses

### 1.1 État général du corpus

La Corse dispose d'un corpus mégalithique substantiel documenté depuis le premier inventaire d'Adrien de Mortillet (1893). La carte archéologique nationale recense actuellement **137 sites** regroupant **855 constructions** (40 coffres, 22 dolmens, menhirs simples, statues-menhirs, alignements, tours protohistoriques et castelli). Répartition géographique : la **Corse-du-Sud (2A)** concentre la majorité des sites emblématiques, notamment dans la région de Sartène.

Pour la **Haute-Corse (2B)** seule : 48 sites recensés, dont 8 pseudo-dolmens exclus, soit 40 sites mégalithiques authentiques contenant **113 mégalithes distincts** (sources : ADLFI — Archéologie de la France Informations, programme CNRS LAMPEA).

Les programmes de recherche les plus récents et les plus rigoureux sont ceux d'**André D'Anna** (Université d'Aix-Marseille/CNRS, LAMPEA), **Pascal Tramoni**, **Franck Leandri** (DRAC Corse, conservateur régional de l'archéologie), et **Kewin Peche-Quilichini** (UMR 5140, Archéologie des Sociétés Méditerranéennes).

### 1.2 Sites principaux avec données de localisation

| Site | Type | Commune | Coordonnées approximatives | Période | Références |
|---|---|---|---|---|---|
| **Filitosa** | Statues-menhirs, torre, village | Sollacaro | ~41.68N, 8.84E | Néolithique final - Bronze ancien | Grosjean 1957ss ; D'Anna et al. |
| **Palaggiu (Palaghju)** | Alignements (258 mégalithes, 70 menhirs) | Sartène | ~41.52N, 8.96E | ~-2000 BCE | D'Anna, Tramoni 2003 |
| **I Stantari** | Statues-menhirs en alignement (~12 statues) | Sartène (Cauria) | ~41.53N, 8.91E | Néolithique final - Bronze | D'Anna et al. 2003 |
| **Renaghju** | Alignement (entre 60 et 180 menhirs) | Sartène (Cauria) | ~41.53N, 8.91E | ~4500-1000 BCE | D'Anna, Tramoni 1995-2012 |
| **Dolmen de Fontanaccia** | Dolmen (chambre 2,6×1,6×1,8 m) | Sartène (Cauria) | **41.529559N, 8.918266E** | Néolithique | Inscrit MH 1889 |
| **Settiva** | Dolmen | Corse-du-Sud | ~41.65N, 9.02E | Néolithique | ADLFI |
| **Filitosa Torre** | Torre / castellu | Sollacaro | ~41.68N, 8.84E | Bronze ancien-moyen | Peche-Quilichini |
| **Cucuruzzu** | Castellu, tour | Levie | ~41.63N, 9.14E | Bronze | INRAP, CMN |
| **Capula** | Castellu | Levie | ~41.62N, 9.12E | Bronze-Fer | INRAP |
| **Monte Revincu** | Alignements, statues-menhirs | Santo-Pietro-di-Tenda | ~42.68N, 9.17E | Néolithique | D'Anna, Tramoni 1996 |
| **Capu Cassi** | Statue-menhir | Corse | À vérifier | Néolithique | DRAC Corse |

**Note pour Soleil** : les coordonnées ci-dessus sont approximatives (sources touristiques validées ou extrapolées). Pour le test statistique, les coordonnées de précision GPS doivent être tirées du fichier `SITES_REFERENCE.json` du projet Tellux ou de la base nationale de données archéologiques (INRAP / Patriarche / DRAC Corse). La base Patriarche est la source d'autorité en France pour la localisation des sites archéologiques déclarés.

### 1.3 Typologie des sites et implications pour le test

Les sites mégalithiques corses peuvent être regroupés en 5 catégories selon l'intensité de travail impliquée et le potentiel de choix délibéré du site :

1. **Alignements de menhirs et statues-menhirs** (Palaggiu, Cauria, Renaghju, Monte Revincu) : travail considérable, sites planifiés, implantation évidemment délibérée.
2. **Dolmens** (Fontanaccia, Settiva) : structures funéraires pérennes, choix d'emplacement fort.
3. **Statues-menhirs isolées** : mobilité plus grande, contrôle spatial moins clair.
4. **Torre et castelli** (Filitosa, Cucuruzzu, Capula, Alo-Bisughjè) : sites fortifiés, contraintes défensives dominantes — **moins pertinents pour le test**, car le critère d'implantation défensif (plateau élevé, visibilité, rocher affleuring) est le déterminant premier.
5. **Coffres mégalithiques** : structures funéraires, potentiellement les plus intimes dans leur choix d'emplacement.

**Recommandation pour le test** : concentrer l'analyse sur les catégories 1 et 2 (alignements, dolmens) dont l'implantation implique le plus un choix actif et non-défensif. Les castelli sont à analyser séparément avec des critères distincts.

---

## 2. Jeux de données géophysiques utilisables

### 2.1 Potentiel radon IRSN — données disponibles

**Source** : Institut de Radioprotection et de Sûreté Nucléaire (IRSN, devenu ASNR depuis 2024).

**Disponibilité** : données en **open data sur data.gouv.fr**, deux jeux distincts :
- "Zonage en potentiel radon" : https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon
- "Connaître le potentiel radon de ma commune" : https://www.data.gouv.fr/datasets/connaitre-le-potentiel-radon-de-ma-commune
- Outil en ligne ASNR : https://recherche-expertise.asnr.fr/savoir-comprendre/environnement/connaitre-potentiel-radon-ma-commune

**Format** : données à l'échelon communal, classification en 3 catégories (1 = faible, 2 = moyen, 3 = élevé). Téléchargeable en CSV/shapefile.

**Situation de la Corse** : la quasi-totalité du territoire corse est en **catégorie 3** (potentiel radon élevé) en raison du substrat granitique varisque dominant. Les zones de Corse alpine (schistes lustrés, ophiolites de l'est) pourraient être en catégorie inférieure. La discrimination spatiale au niveau communal est donc grossière mais utilisable.

**Limites** : résolution communale uniquement. Pour un test infra-communal (site par site), cette donnée est insuffisante seule — il faut la coupler aux données radiométriques BRGM (Q3) ou à la carte géologique au 1:50 000 pour les substrats locaux.

**Usage dans le test** : variable proxy pour le potentiel radon local. Alternative : utiliser directement la nature lithologique du substrat (granite leucocrate vs. granite porphyrique vs. schiste lustré) comme variable continue de teneur en uranium.

### 2.2 Radiométrie aéroportée BRGM

**Disponibilité** : la recherche documentaire ne retrouve pas de **campagne aéroportée gamma-ray spectrometry dédiée à la Corse** publiée par le BRGM. Ce type de levé existe à l'échelle nationale (BRGM a conduit des levés en Bretagne, Massif central, Vosges) mais sa couverture corse reste à vérifier directement auprès du BRGM.

**Action recommandée pour Soleil** : contacter directement BRGM Corse (agence régionale à Bastia) et l'InfoTerre. L'adresse de l'agence BRGM Corse est connue (plusieurs références trouvées). Les levés aéroradiométriques du BRGM sont normalement versés dans InfoTerre.

**Alternative** : les cartes radiométriques globales (IAEA Global Airborne Radioactivity Survey — GARAS) couvrent la Méditerranée. La résolution est typiquement de 1 à 10 km selon les campagnes disponibles.

**Format si disponible** : raster (GeoTIFF), canaux K, U, Th séparément. Extractible en Python (rasterio/GDAL) ou QGIS.

### 2.3 Anomalies magnétiques — EMAG2 et données BRGM

**EMAG2** (Earth Magnetic Anomaly Grid, NOAA/USGS) :
- Résolution : 2 minutes d'arc (≈ 3,7 km à la latitude de la Corse) — résolution grossière pour un test site-par-site mais utilisable pour des gradients régionaux.
- Altitude : 4 km au-dessus du géoïde.
- Accès : https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ngdc.mgg.geophysical_models:EMAG2
- Format : netCDF, GeoTIFF, ASCII.
- Couvre la Méditerranée, Corse incluse.
- **Directement utilisable** dans le cadre d'un test à résolution régionale.

**Aeromagnetic Anomaly Map of Europe** (Commission Européenne / JRC/ESDAC) :
- Disponible sur : https://esdac.jrc.ec.europa.eu/content/aeromagnetic-anomaly-map
- Résolution meilleure qu'EMAG2 pour l'Europe.
- Couvre la France et la Corse.

**Données BRGM / levés aéromagnétiques nationaux** :
- Le BRGM a conduit des levés aéromagnétiques sur plusieurs régions de France. Pour la Corse, leur disponibilité est à vérifier sur InfoTerre (service WMS "aéromagnétisme" disponible selon les régions).
- InfoTerre URL : https://infoterre.brgm.fr

**Référence scientifique clé — susceptibilité magnétique des granitoïdes corses** :
- **Gattacceca J., Orsini J.-B., Bellot J.-P. et al. (2004)**. Magnetic fabric of granitoids from Southern Corsica and Northern Sardinia and implications for Late Hercynian tectonic setting. *Journal of the Geological Society*, 161(2):277-289.
- L'étude porte sur 180 sites dans les granitoïdes hercyniens du bloc corso-sarde. Deux groupes principaux définis par pétrographie et chronologie montrent des susceptibilités contrastées. Les granitoïdes à foliations magnétiques sub-horizontales suggèrent des structures en feuillets ou entonnoirs à haut niveau structural.
- **Implication pour Tellux** : la susceptibilité magnétique varie spatialement à l'intérieur du socle corse. Cette variabilité peut être utilisée comme variable dans le test statistique à condition de disposer de la carte géologique au 1:50 000 (BRGM, disponible en WMS sur InfoTerre) permettant de déterminer le faciès granitique local de chaque site.

### 2.4 Failles actives et sismotectonique

**Référence principale** :
- **Larroque C. et al. (2021)**. Seismotectonics of southeast France: from the Jura mountains to Corsica. *Comptes Rendus Géoscience*, 353(1):1-51. [HAL hal-03348930]
- Couvre la période instrumentale 1996-2019. Analyse la répartition des séismes par domaine géologique, mécanismes focaux.
- Pour la Corse : domaine Mer Ligure-Corse inclus. La marge corse est caractérisée par une sismicité modérée avec des structures héritées de la collision alpine réactivées.

**Séquences notables** :
- Larroque et al. (2016, Tectonophysics) : "The sequence of moderate-size earthquakes at the junction of the Ligurian basin and the Corsica margin: The initiation of an active deformation zone revealed?"
- Ce travail documente l'existence d'une zone de déformation active à la marge nord de la Corse.

**Bases de données des failles actives** :
- **BRGM InfoTerre** : cartes géologiques 1:50 000 incluent les failles cartographiées (pas toutes actives, mais base utilisable pour la distance à la faille la plus proche).
- **FA.RE.MON** (Failles actives du pourtour Méditerranéen, CNRS/INSU) : base de données des failles actives méditerranéennes incluant potentiellement la Corse.
- **SHARE (Seismic Hazard Assessment for Europe)** : base de données européenne des zones sismogènes.

**Données directement exploitables** :
- Pour le test statistique, la variable pertinente est la **distance euclidienne** du site mégalithique à la faille cartographiée la plus proche, calculée sous SIG à partir de la couche BRGM.
- La résolution des cartes géologiques 1:50 000 (précision kilométrique) est adaptée.

---

## 3. Cadre méthodologique : génération de points témoins et contrôle des biais

### 3.1 Biais d'implantation des sites mégalithiques

Les sites mégalithiques corses ne sont pas distribués aléatoirement dans l'espace. Leur implantation répond à des logiques culturelles et pratiques qui constituent des **biais confondants** pour le test statistique :

**Biais 1 — Accessibilité** : les sites sont majoritairement situés à altitude modérée (200-600 m), accessibles depuis les vallées agricoles. Les altitudes extrêmes (>1000 m) sont pratiquement vides de sites — pas parce qu'elles seraient géophysiquement différentes, mais parce qu'elles étaient inaccessibles ou non utilisées par les populations néolithiques.

**Biais 2 — Visibilité** : les alignements et dolmens sont souvent placés sur des replats ou éminences avec vues dégagées. La visibilité (viewshed) est un déterminant documenté dans la littérature archéologique (Lake & Woodman 2003).

**Biais 3 — Disponibilité du substrat granitique** : les statues-menhirs corses sont taillées dans le granite local. Les sites sont donc, par définition, proches de zones à affleurement granitique — ce qui corrèle automatiquement avec le radon élevé, sans que ce soit une corrélation Bio-géophysique significative en soi.

**Biais 4 — Biais de découverte** : les zones accessibles, étudiées et proches des centres habités sont surreprésentées dans les inventaires. Des zones reculées peuvent contenir des sites non découverts.

### 3.2 Protocole de génération des points témoins

**Méthode recommandée (standard en landscape archaeology SIG)** :

**Étape 1 — Tirage initial** : générer N points aléatoires sur la surface de la Corse (N ≥ 500, idéalement 1000-2000 pour la puissance statistique). Outils : `random_points_in_layer_bounds` (QGIS) ou `RandomPoints()` en R (`sp::spsample`) ou Python (`shapely` + `geopandas`).

**Étape 2 — Filtrage accessibilité** : conserver uniquement les points situés :
- à une altitude comprise dans l'intervalle [min_altitude_sites - 50 m ; max_altitude_sites + 50 m] d'après le MNT IGN (RGE Alti 5m, disponible gratuitement)
- à moins de X km de la vallée la plus proche (seuil défini d'après la distribution des sites réels)

**Étape 3 — Filtrage substrat** : conserver uniquement les points situés sur un substrat granitique (d'après la carte géologique 1:50 000 BRGM WMS), pour contrôler le biais de disponibilité des matériaux.

**Étape 4 — Filtrage visibilité (optionnel mais recommandé)** : calcul du viewshed (zone visible) depuis chaque point via le MNT. Calcul d'un score de visibilité cumulé (CVA). Filtrer pour ne garder que les points dont le score CVA est comparable à la distribution des sites réels.

**Étape 5 — Validation du jeu de contrôle** : vérifier que les points témoins filtrés sont comparables aux sites réels sur les variables de contrôle (altitude, pente, distance à une vallée). Si des différences subsistent, les inclure comme covariables dans le modèle de régression logistique.

### 3.3 Approche statistique — logistic regression vs. tests bivariés

**Option A — Tests bivariés (Wilcoxon/Mann-Whitney)** : comparer la distribution de chaque variable géophysique (radon, susceptibilité magnétique, distance faille) entre les sites mégalithiques et les points témoins. Simple, interprétatble, adapté à des distributions non-normales.

**Option B — Régression logistique** (recommandée comme test principal) :
- Variable réponse : présence/absence de site mégalithique (1/0)
- Prédicteurs : radon (catégorie IRSN ou valeur continue), susceptibilité magnétique locale, distance à la faille la plus proche, + variables de contrôle (altitude, pente, distance vallée)
- La régression logistique contrôle simultanément tous les biais et permet de tester si les variables géophysiques ajoutent un pouvoir prédictif **au-delà des variables d'accessibilité/visibilité**
- Cette approche a été validée pour des sites néolithiques et Bronze Age en Chine (MDPI Sustainability 2022) et en Israël/Chine (ScienceDirect 2018)

**Option C — MaxEnt** : souvent utilisé pour modéliser les distributions d'espèces, de plus en plus utilisé en archéologie. Comparable à la régression logistique mais mieux adapté aux données biaisées (corriger le biais de découverte par pondération).

**Tests à pré-enregistrer avant l'analyse** :
- H1 : les sites mégalithiques sont localisés sur des communes à potentiel radon 3 dans une proportion supérieure aux points témoins après contrôle des biais.
- H2 : les sites mégalithiques sont localisés dans des zones à anomalie magnétique positive (susceptibilité élevée) dans une proportion supérieure aux points témoins.
- H3 : la distance médiane entre un site mégalithique et la faille la plus proche est significativement inférieure à celle des points témoins.
- H4 : les trois variables géophysiques combinées (régression logistique) améliorent significativement la prédiction de la présence d'un site au-delà des seules variables topographiques.

**Correction pour tests multiples** : correction de Bonferroni (alpha ajusté = 0.05/4 = 0.0125 pour 4 hypothèses testées).

**Pré-enregistrement** : déposer le protocole sur le registre OSF (Open Science Framework) avant de regarder les résultats, pour éviter le p-hacking involontaire.

---

## 4. Littérature comparative internationale

### 4.1 La géomythologie : cadre disciplinaire fondateur

**Piccardi L. & Masse W.B. (éds) (2007)**. Myth and Geology. Geological Society Special Publication no. 273, 350 pp. ISBN 978-1-86239-216-8.

Premier volume peer-reviewed dédié à l'intersection entre géologie et mythologie. Contributions de spécialistes multidisciplinaires. Sujets couverts : séismes, tsunamis, éruptions volcaniques, impacts cosmiques, valeurs sacrées associées aux formations géologiques. Couverture géographique : Europe, Méditerranée, Afghanistan, Cameroun, Inde, Australie, Japon, Pacifique, Amériques.

Contexte pour Tellux : ce volume légitime la démarche de croiser archéologie et géologie. Il ne traite pas spécifiquement de la Corse mais fournit le cadre épistémologique et bibliographique de référence pour l'Axe N.

### 4.2 L'Oracle de Delphes : le cas le plus documenté

**Piccardi L. (2000)**. Active faulting at Delphi, Greece: Seismotectonic remarks and a hypothesis for the geologic environment of a myth. *Geology* (GSA), 28(7):651-654. [DOI:10.1130/0091-7613]

**De Boer J.Z., Hale J.R., Chanton J. (2001)**. Scent of a myth: tectonics, geochemistry and geomythology at Delphi. *Journal of the Geological Society*, 165(1):5-20.

Résultats : Delphes est implantée directement sur l'une des principales failles antithétiques du rift du Golfe de Corinthe. Des émanations de gaz (H₂S, CO₂, hydrocarbures légers) liées à la faille et aux séismes anciens pourraient expliquer les effets d'altération de la conscience de la Pythie. Les niches votives, sculptures et inscriptions sur des **surfaces de failles** documentent des santcuaires sacrés délibérément construits sur des traces de failles actives dans toute l'Antiquité grecque.

**Kasatkina E.A. et al. (2017)**. Seismic faults and sacred sanctuaries in Aegean antiquity. *Acta Geodaetica et Geophysica*. [ScienceDirect]

Étendu à plusieurs sanctuaires des Cyclades et de Grèce continentale : corrélation documentée entre localisation des sites sacrés et présence de failles sismiques actives.

**Pertinence pour Tellux** : c'est le précédent méthodologique le plus proche de l'Axe N. La démarche est identique — superposer la carte des sanctuaires avec la carte des structures géologiques (ici failles) et tester la corrélation. La différence est que Delphi-Corinthe est une zone sismique très active, tandis que la Corse est modérément sismique. Cela ne rend pas le test sans intérêt mais modère l'ampleur de l'effet attendu pour la variable "faille active".

### 4.3 Stonehenge : survei géophysique d'un site mégalithique

**The Stonehenge Hidden Landscape Project** (Universitées de Birmingham, Vienne, Bradford, St Andrews, Nottingham, Ghent, National Trust, English Heritage) :
- Magnétométrie sur 12 km² autour de Stonehenge, résolution 10×25 cm
- GPR (ground-penetrating radar), résistivité électrique, EMI (electromagnetic induction)
- Résultats : révélation de structures souterraines inédites, complexité du paysage rituel bien plus grande qu'attendu
- Historic England (2013) : rapport spécifique sur la susceptibilité magnétique des sols de Stonehenge

**Pertinence pour Tellux** : Stonehenge démontre l'utilisation des méthodes géophysiques (magnétométrie, EMI) dans l'investigation archéologique d'un site mégalithique. Ces méthodes sont exactement celles qui pourraient être appliquées sur des sites corses. Note : les recherches de Stonehenge s'intéressent à la géophysique **du site lui-même** (pour la découverte archéologique), pas à la corrélation **du site** avec le contexte géologique régional — démarche inverse de celle de Tellux.

Une publication identifiée dans cette recherche (ResearchGate) propose même Stonehenge comme "dispositif d'hormésis géomagnétique" — article anecdotique et non retenu comme référence fiable, mais sa simple existence indique que des chercheurs ont formulé des hypothèses similaires à l'hypothèse K pour d'autres sites. Cela suggère que l'axe N de Tellux s'inscrit dans un espace de recherche au moins partiellement reconnu.

### 4.4 Carnac : le contexte le plus proche géologiquement

Les alignements de Carnac (Bretagne, 4600-4300 BCE) constituent le corpus mégalithique le plus riche d'Europe (3000+ menhirs en granite local). Le contexte géologique de la Bretagne (granite armoricain) est comparable à celui de la Corse cristalline. Cependant, la recherche documentaire de cette fiche **n'a pas identifié de publication peer-reviewed** croisant spécifiquement les coordonnées GPS des alignements de Carnac avec des mesures de radioactivité, de radon ou d'anomalies magnétiques.

**C'est précisément la lacune que l'Axe N de Tellux peut combler pour la Corse.** Si l'approche méthodologique Tellux fonctionne pour la Corse, elle est transposable à Carnac — ce qui ouvre une perspective de publication comparative d'intérêt international.

### 4.5 Radon dans des structures archéologiques souterraines

Des études ont mesuré des concentrations de radon élevées dans des structures archéologiques **fermées** :
- Pyramide du Soleil à Teotihuacan (Mexique) : 700-5500 Bq/m³ (Stoker & Lawrence 1997, *Applied Radiation and Isotopes*)
- Catacombes romaines : concentrations variables selon la géologie locale, corrélées à la température et l'humidité (PMC12296779, 2025)
- Tombes égyptiennes de Saqqara : mesures de sûreté radiologique documentées

**Note importante** : ces études portent sur des **espaces confinés**, où le radon s'accumule. Les sites mégalithiques corses sont pour la plupart en plein air (à ciel ouvert) — le radon ne s'accumule pas de la même façon. Pour le test Tellux, ce qui est pertinent n'est pas la concentration en radon à l'intérieur des dolmens, mais le **potentiel d'exhalation du sol** lié à la géologie locale (teneur en uranium et radium du substrat, porosité, présence de failles).

---

## 5. Protocole de test : étapes concrètes pour l'exécution

Ce protocole est conçu pour être exécuté par Soleil ou un collaborateur disposant de compétences SIG (QGIS) et de base en statistiques (R ou Python).

### Étape 1 — Constitution du jeu de données sites (environ 1 semaine)

1.1 Extraire de la base `SITES_REFERENCE.json` les coordonnées GPS de tous les sites typologiquement retenus (alignements + dolmens = priorité 1 ; statues-menhirs isolées = priorité 2 ; castelli = traitement séparé).

1.2 Vérifier chaque coordonnée sur Google Maps / Geoportail IGN pour s'assurer de la précision. Corriger les éventuelles erreurs.

1.3 Créer un fichier SIG (GeoPackage, projection WGS84 puis re-projeter en Lambert-93 EPSG:2154 pour les calculs de distance).

1.4 Documenter : nom du site, type, période, département (2A ou 2B), source de la coordonnée.

### Étape 2 — Acquisition des jeux de données géophysiques (environ 2-3 jours)

2.1 **Radon IRSN** : télécharger le shapefile "Zonage en potentiel radon" sur data.gouv.fr. Jointure spatiale avec les communes corses (IGN GeoFLA ou COG Admin Express). Vérifier que chaque site est attribué à une commune avec catégorie radon.

2.2 **Anomalie magnétique EMAG2** : télécharger le GeoTIFF depuis NCEI/NOAA. Extraire la valeur de l'anomalie magnétique en nT au point GPS de chaque site (outil QGIS : "Extract raster values to points" ou Python `rasterio`).

2.3 **Carte géologique** : accéder via InfoTerre BRGM (service WMS "BDLISA" ou cartes géologiques 1:50 000). Identifier le faciès lithologique du substrat sous chaque site (granite leucocrate S/I-type, granite porphyrique, micaschiste, schiste lustré, etc.).

2.4 **Failles** : accéder à la couche des failles de la carte géologique BRGM (service WMS). Calculer la distance de chaque site à la faille la plus proche (outil QGIS : "Distance to nearest feature" ou Python `geopandas.sjoin_nearest`).

### Étape 3 — Génération des points témoins (environ 2 jours)

3.1 Générer 1000 points aléatoires sur le polygone de la Corse (MaskLayer = contour administratif Corse).

3.2 Filtrer par altitude (MNT RGE Alti 5m IGN, gratuit) : garder seulement les points entre 50 m et 900 m d'altitude.

3.3 Filtrer par substrat : garder seulement les points sur substrat granitique (même faciès que les sites mégalithiques).

3.4 Calculer les mêmes 4 variables géophysiques (radon catégorie, anomalie magnétique, faciès lithologique, distance faille) pour chaque point témoin.

3.5 Objectif : obtenir ≥ 300 points témoins valides après filtrage.

### Étape 4 — Tests statistiques (environ 1-2 jours)

4.1 Vérifier la normalité des distributions (Shapiro-Wilk). Si non-normale (probable) : utiliser des tests non-paramétriques.

4.2 **Test H1 (radon)** : test de Fisher (tableau de contingence) sur la proportion de sites catégorie 3 vs. points témoins catégorie 3.

4.3 **Tests H2, H3** (magnétisme, distance faille) : test de Wilcoxon-Mann-Whitney bilatéral (sites vs. témoins).

4.4 **Test H4** (régression logistique) :
- Variable réponse : 1 = site mégalithique, 0 = point témoin
- Modèle nul : altitude + pente seulement
- Modèle complet : altitude + pente + radon + anomalie magnétique + distance faille
- Comparer AIC et likelihood ratio test (Chi2) entre modèle nul et modèle complet
- Un gain significatif (p < 0.0125 après Bonferroni) indique que les variables géophysiques ajoutent un pouvoir prédictif au-delà des seuls critères topographiques

4.5 **Calcul des odds ratios** et intervalles de confiance pour les variables significatives.

4.6 Documenter et publier les résultats **quelle que soit leur orientation**.

### Étape 5 — Interprétation et rédaction

5.1 Si corrélation significative : rédiger la note de résultats pour intégration dans HYPOTHESES.md. L'hypothèse 2 ("implantation mégalithique orientée par signature géologique") passe de "formulée testable" à "testée — corrélation partielle ou totale confirmée". Envisager une publication dans Journal of Archaeological Science ou Quaternary International.

5.2 Si résultat partiel ou nul : documenter rigoureusement. Le résultat négatif est scientifiquement valide et publiable. Met à jour HYPOTHESES.md avec le statut "testée — non confirmée" ou "testée — résultat partiel".

5.3 Dans tous les cas : rédiger une courte note pour le dossier CTC expliquant la démarche (qu'elle soit confirmée ou non) comme preuve de rigueur scientifique du projet.

---

## 6. Bibliographie

### Archéologie mégalithique corse
- D'Anna A., Tramoni P. et al. (2003). Les alignements de menhirs de Renaghju dans leur contexte du plateau de Cauria. *Documents d'Archéologie Méridionale / Mémoires d'Archéologie Méridionale*, vol. 15.
- D'Anna A. et al. (2012). Espaces, territoires et mégalithes. Programme collectif de recherche sur le plateau de Cauria, finalisé 2012.
- Peche-Quilichini K., Leandri F. et al. "Le mégalithisme de la Corse : une approche interactive." UMR 5140.
- Peche-Quilichini K. "Les torre. Tours de l'âge du Bronze de Corse." [Academia.edu]
- Mortillet A. de (1893). Premier inventaire des mégalithes de Corse.
- ADLFI (Archéologie de la France Informations). "Inventaire des mégalithes de Haute-Corse." OpenEdition Journals. https://journals.openedition.org/adlfi/19045
- ADLFI. "Mégalithisme de la Corse." https://journals.openedition.org/adlfi/23366
- Menhirs et statues-menhirs de Corse, nouvelles recherches sur les alignements du plateau de Cauria. HAL-SHS https://shs.hal.science/halshs-00260351
- Wikipedia FR : Sites mégalithiques de la Corse. https://fr.wikipedia.org/wiki/Sites_m%C3%A9galithiques_de_la_Corse
- Collectivité de Corse. Sites archéologiques du pianu de Cauria. https://www.isula.corsica/patrimoine/Les-sites-archeologiques-du-pianu-de-Cauria_a11.html

### Géophysique corse — Sources de données
- Gattacceca J., Orsini J.-B., Bellot J.-P., Henry B., Rochette P., Rossi P., Cherchi G. (2004). Magnetic fabric of granitoids from Southern Corsica and Northern Sardinia and implications for Late Hercynian tectonic setting. *Journal of the Geological Society*, 161(2):277-289. https://pubs.geoscienceworld.org/gsl/jgs/article-abstract/161/2/277
- Larroque C. et al. (2021). Seismotectonics of southeast France: from the Jura mountains to Corsica. *Comptes Rendus Géoscience*, 353(1). HAL hal-03348930. https://hal.science/hal-03348930
- EMAG2 : Earth Magnetic Anomaly Grid, 2 arcmin. NOAA/NCEI. https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ngdc.mgg.geophysical_models:EMAG2
- Aeromagnetic Anomaly Map of Europe. JRC/ESDAC European Commission. https://esdac.jrc.ec.europa.eu/content/aeromagnetic-anomaly-map
- BRGM InfoTerre (données géologiques, géophysiques Corse). https://infoterre.brgm.fr
- BRGM Corse. https://www.brgm.fr/en/regional-agency/corsica
- IRSN/ASNR. Zonage en potentiel radon — data.gouv.fr. https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon
- ASNR. Connaître le potentiel radon de ma commune. https://recherche-expertise.asnr.fr/savoir-comprendre/environnement/connaitre-potentiel-radon-ma-commune

### Géomythologie et corrélations géologiques / sites sacrés
- Piccardi L. & Masse W.B. (éds) (2007). Myth and Geology. *Geological Society Special Publication*, n° 273. https://pubs.geoscienceworld.org/gsl/books/edited-volume/1643/Myth-and-Geology
- Piccardi L. (2000). Active faulting at Delphi, Greece: Seismotectonic remarks and a hypothesis for the geologic environment of a myth. *Geology*, 28(7):651-654. https://pubs.geoscienceworld.org/gsa/geology/article-abstract/28/7/651
- De Boer J.Z., Hale J.R., Chanton J. (2008). Scent of a myth: tectonics, geochemistry and geomythology at Delphi. *Journal of the Geological Society*, 165(1):5-20. https://jgs.lyellcollection.org/content/165/1/5.short
- Kasatkina E.A. et al. (2017). Seismic faults and sacred sanctuaries in Aegean antiquity. *Acta Geodaetica et Geophysica*. https://www.sciencedirect.com/article/pii/S0016787817301190
- Stonehenge Hidden Landscape Project. Magnetometry survey data and description. LBI Archaeoprosepction. https://lbi-archpro.org/cs/stonehenge/magnetic.html
- Historic England (2013). Report on Magnetic Susceptibility Survey, Stonehenge. https://historicengland.org.uk/research/results/reports/6133/

### Méthodes SIG archéologiques — Contrôle des biais et tests statistiques
- Lake M.W., Woodman P.E. (2003). Visibility Studies in Archaeology: A Review and Case Study. *Environment and Planning B*, 30(5):689-707.
- Kohler T.A., Parker S.C. (1986). Predictive models for archaeological resource location. *Advances in Archaeological Method and Theory*, 9:397-452.
- Verhagen P. et al. (2018). Predictive modeling for archaeological site locations: Comparing logistic regression and maximal entropy in north Israel and north-east China. *Journal of Archaeological Science*, 92:1-10. https://www.sciencedirect.com/science/article/abs/pii/S0305440318300293
- Cao R. et al. (2022). A Prediction Study on Archaeological Sites Based on Geographical Variables and Logistic Regression — Neolithic Era and Bronze Age of Xiangyang. *Sustainability*, 14(23):15675. https://www.mdpi.com/2071-1050/14/23/15675
- Entropy-Based Methods to Address Sampling Bias in Archaeological Predictive Modeling (2025). arXiv. https://arxiv.org/html/2508.02272

### Radon dans les structures archéologiques
- Stoker A.C., Lawrence S.H. (1997). Radon concentrations in the pyramid of the sun at Teotihuacan. *Applied Radiation and Isotopes*, 48(2). https://www.sciencedirect.com/article/abs/pii/S1350448797001613
- Monitoring radon concentration in roman catacombs: a long-term analysis (2025). *Environmental Geochemistry and Health*. PMC12296779. https://pmc.ncbi.nlm.nih.gov/articles/PMC12296779/

---

*Document produit le 2026-04-19 pour le corpus Tellux Corse — Axe N. Usage interne. Ce document ne contient aucune référence à des sources ésotériques. Toutes les données citées proviennent d'institutions scientifiques reconnues ou de publications peer-reviewed.*
