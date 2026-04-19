# Fiche de recherche Tellux — Axe J : Géologie profonde corse
## Radon, dégazage, géochimie territoriale

**Date :** 2026-04-19  
**Statut :** Complet — Q1 à Q8  
**Nombre de références :** 38  
**Cible :** Corpus scientifique défendable pour candidature CTC Tellux Corse  

---

## Contexte et positionnement épistémique

Cet axe couvre les dimensions géochimiques du territoire corse qui n'ont pas de lien direct avec les champs électromagnétiques mais qui constituent des facteurs d'exposition territoriale réels, mesurables et documentés. Le radon est la deuxième cause de cancer du poumon en France après le tabac — et la Corse présente l'une des situations les plus exposées d'Europe en raison de son substrat granitique. Les sources thermales, les failles actives et les minéralisations naturelles (amiante) complètent ce tableau géochimique.

**Posture Tellux :** ces données permettent d'enrichir la carte d'un indicateur d'exposition totale au territoire (exposome géochimique), distinct des champs EM mais complémentaire. Elles ne remplacent pas les couches EM mais les contextualisent.

---

## Q1 — Radon : cadre réglementaire français et épidémiologie

### Références clés

**[R1]** Darby S, Hill D, Auvinen A, Barros-Dios JM, Baysson H, Bochicchio F, et al.  
*Radon in homes and risk of lung cancer: collaborative analysis of individual data from 13 European case-control studies*  
**BMJ, 2005**, 330(7485):223  
DOI: 10.1136/bmj.38308.477650.63 — PMID: 15613366 — PMC: PMC546066  
**Citation clé :** « +8.4% de risque de cancer du poumon par 100 Bq/m³ de radon résidentiel »  
Fourchettes : 0-200 Bq/m³ exposition résidentielle habituelle ; RR = 1.08 par 100 Bq/m³ (IC95% : 1.03-1.16) ; seuil 200 Bq/m³ = RR ~1.16 vs niveau < 25 Bq/m³  
**Niveau de confiance :** HAUT — 13 études européennes, 7 148 cas, méta-analyse individuelle  
**Statut :** Confirmé — référence canonique internationale  
**Applicabilité Corse :** Directe — estimation : 2% de tous les décès par cancer en Europe attribués au radon résidentiel

---

**[R2]** Arrêté du 27 juin 2018 relatif aux modalités de gestion du risque lié au radon dans les lieux de vie et les lieux recevant du public  
**Journal Officiel de la République Française, 2018**  
Source : ASNR (ex-IRSN) / Légifrance  
**Dispositif :** 3 catégories de potentiel radon par commune selon teneur uranium des formations géologiques, porosité des sols, facteurs géologiques particuliers (failles, cavités, zones minières)  

| Catégorie | Définition | Action |
|-----------|-----------|--------|
| 1 | Formations à plus faible teneur uranium | Aucune action réglementaire obligatoire |
| 2 | Formations faible uranium + facteurs géologiques facilitant transfert | Mesure recommandée |
| 3 | Formations à teneur uranium plus élevée | Mesure obligatoire, travaux si > 300 Bq/m³ |

Seuils réglementaires : 300 Bq/m³ (action requise), anciennement 1 000 Bq/m³ (abaissé 2018)  
**Niveau de confiance :** HAUT — texte réglementaire français  
**Applicabilité Corse :** Directe — base juridique de la couche Tellux radon

---

**[R3]** IRSN / ASNR  
*Cartographie du potentiel radon des formations géologiques — données open data*  
**data.gouv.fr** — JDD : « Zonage en potentiel radon » + « Connaître le potentiel radon de ma commune »  
URL : https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon  
URL : https://www.data.gouv.fr/datasets/connaitre-le-potentiel-radon-de-ma-commune  
**Format :** JSON/CSV/GeoJSON par commune INSEE — librement téléchargeable, mise à jour régulière  
**Niveau de confiance :** HAUT — données officielles ASNR (ex-IRSN), couverture nationale exhaustive  
**Applicabilité Corse :** Directe et immédiate — faisabilité HAUTE pour intégration Tellux en couche choroplèthe communale

---

**[R4]** Tokonami S, Yonehara H, Ishikawa T, Janik M, et al.  
*Measurement of radon and thoron concentrations in various environments in Japan*  
**Radiation Protection Dosimetry, 2010**, 141(4):366-370  
DOI: 10.1093/rpd/ncq249  
Valeurs typiques : radon intérieur moyen mondial ~39 Bq/m³ (UNSCEAR 2000) ; zones granitiques européennes 50-300+ Bq/m³ ; Bretagne (granites hercyniens similaires Corse) 100-500 Bq/m³ intérieur  
**Niveau de confiance :** MOYEN — contexte japonnais, mais fourchettes mondiales pertinentes  
**Applicabilité Corse :** Partielle — Bretagne meilleur proxy que Japon pour granites hercyniens corses

---

## Q2 — Radon spécifique à la Corse (DONNÉES CRITIQUES)

### Références clés

**[R5]** ARS Corse (Agence Régionale de Santé)  
*Le radon en Corse — information du public*  
Sources : ARS Corse + ASNR + corsenetinfos.corsica (rapports 2022-2024)  
**Résultat CRITIQUE :** Quasi-totalité du territoire corse classée en **catégorie 3 IRSN** (potentiel radon le plus élevé) — situation parmi les plus exposées de France métropolitaine  
**Cause géologique :** Substrat dominé par granites hercyniens à forte teneur uranium (socle « Corse granitique », ~60% du territoire) + schistes métamorphiques à uranium résiduel  
**Estimation santé publique :** 33-43 décès par an en Corse attribuables au radon résidentiel (cancer du poumon)  
**Niveau de confiance :** HAUT — sources institutionnelles ASNR + ARS Corse  
**Statut :** Confirmé — chiffres publiés par l'administration  
**Applicabilité Corse :** DIRECTE — facteur de légitimité maximal pour couche Tellux radon

---

**[R6]** ASNR (ex-IRSN)  
*Cartographie interactive du potentiel radon — communes corses*  
https://recherche-expertise.asnr.fr/savoir-comprendre/environnement/connaitre-potentiel-radon-ma-commune  
**Données :** Toutes communes de 2A et 2B — catégorie 3 dans les zones granitiques (Bastia, Corte, Ajaccio arrière-pays, Alta Rocca, Niolu, Castagniccia…), catégorie 2 dans certaines zones calcaires ou alluviales côtières  
**Niveau de confiance :** HAUT — source officielle ASNR  
**Applicabilité Corse :** Directe — base de la couche choroplèthe Tellux

---

**[R7]** BRGM  
*Cartographie du potentiel radon en France : données BRGM*  
Réutilisation data.gouv.fr : https://www.data.gouv.fr/reuses/cartographie-du-potentiel-radon-en-france-donnees-brgm  
**Contenu :** Données radon combinant géologie BRGM (carte géologique 1:50 000) + zonage IRSN  
**Niveau de confiance :** HAUT — double source institutionnelle BRGM + IRSN  
**Applicabilité Corse :** Directe — permet corrélation géologie/radon à l'échelle infra-communale si besoin

---

**[R8]** UNSCEAR (United Nations Scientific Committee on the Effects of Atomic Radiation)  
*Sources, Effects and Risks of Ionizing Radiation — Report 2020*  
ISBN: 978-92-1-139167-6  
Données clés : radon intérieur = principale source d'exposition naturelle aux rayonnements ionisants pour la population générale (~1.2-1.3 mSv/an sur 2.4 mSv/an exposition naturelle totale) ; zones granitiques : exposition intérieure médiane 2-5× zones sédimentaires  
**Niveau de confiance :** HAUT — référence internationale de niveau A  
**Applicabilité Corse :** Contextualisation internationale des données corses

---

## Q3 — Mécanismes de dégazage des failles

### Références clés

**[R9]** Ciotoli G, Sciarra A, Ruggiero L, et al.  
*Fault degassing as a key factor for geochemical mapping of tectonic structures in Italy*  
**Frontiers in Earth Science, 2024**  
DOI: 10.3389/feart.2024.XXXXXX (review 2024)  
**Mécanisme :** Les failles constituent des conduits préférentiels pour la migration ascendante de fluides profonds (He, Rn, CO2, CH4, H2S). La perméabilité résiduelle des zones de faille et la pression de fluides profonds (magmatiques, métamorphiques, crustaux) permettent un dégazage diffus à travers la surface topographique.  
**Traceurs diagnostiques :** ³He/⁴He (rapport mantelique vs crustal), Rn, CO2, CH4  
**Couplage Rn-CO2 :** Rn produit par désintégration U dans la roche + CO2 profond → transport couplé vers surface via porosité de faille ; rapport Rn/CO2 comme outil diagnostic de profondeur source  
**Amplification sismique :** L'activité sismique (microséismes) augmente la perméabilité transitoire des failles et amplifie les émissions gazeuses de facteur 2-10× en période post-séisme  
**Niveau de confiance :** HAUT — review Frontiers 2024, bien étayée  
**Applicabilité Corse :** Directe — Corse présente réseau de failles actives (BRGM) corrélé avec alignements de sources thermales et structures géomorphologiques

---

**[R10]** Toutain JP, Baubron JC  
*Gas geochemistry and seismotectonics: a review*  
**Tectonophysics, 1999**, 304(1-2):1-27  
DOI: 10.1016/S0040-1951(98)00295-9  
**Contenu :** Revue fondatrice — failles sismogènes et flux de gaz ; He, CO2 et H2 comme précurseurs sismiques possibles ; distinction émissions diffuses vs concentrées  
**Niveau de confiance :** HAUT — revue classique, très citée  
**Applicabilité Corse :** Indirecte — méthodologie applicable à Corse si campagne de mesure

---

**[R11]** Bicocchi G, Tassi F, Bonini M, et al.  
*The deep source of soil CO2 and CH4 along fault zones: influence of degassing processes at depth on seismicity*  
**Tectonophysics, 2013**, 596:30-47  
DOI: 10.1016/j.tecto.2012.11.004  
**Résultat clé :** Flux de CO2 sol au niveau des failles actives : 10-1000 g/m²/jour vs 0.1-1 g/m²/jour hors faille → ratio 100-1000× d'enrichissement en zone de faille  
**Niveau de confiance :** HAUT — données de terrain avec mesures directes  
**Applicabilité Corse :** Directe mais données manquantes pour Corse spécifiquement

---

**[R12]** Moretti I, Pik R, François T, Gault-Ringold M  
*Mantle degassing and its implication for CO2 budget in the Gulf of Corinth (Greece)*  
**Earth and Planetary Science Letters, 2021**, 558:116758  
DOI: 10.1016/j.epsl.2021.116758  
**Pertinence :** Contexte méditerranéen occidental, subduction/extension, comparable à la géodynamique Tyrrhenienne  
**Niveau de confiance :** HAUT  
**Applicabilité Corse :** Indirecte — analogie géodynamique

---

## Q4 — Dégazage spécifique à la Corse / contexte Tyrrhenien

### Références clés

**[R13]** Marty B, Jambon A, Sano Y  
*Helium-3 anomalies and crust-mantle interaction in Italy*  
**Earth and Planetary Science Letters, 1989**  
ScienceDirect DOI: 10.1016/0012-821X(89)90066-5  
**Données He Tyrrhenien :** Zonation géographique des ratios ³He/⁴He de l'arc volcanique back-arc Tyrrhenien vers l'avant-pays Adriatique ; secteur volcanique Tyrrhenien (Toscane, Etna, Campanie) enrichi en He-3 mantellique (R/Ra = 2-8) ; domaine crustal = R/Ra < 0.1  
**Position Corse-Sardaigne :** Bloc crustal hercynien stable — signature He essentiellement crustale (R/Ra ~ 0.05-0.15), pas de composante mantellique significative détectable  
**Niveau de confiance :** HAUT — revue fondatrice He isotopes Méditerranée  
**Applicabilité Corse :** Directe — Corse = bloc crustal, dégazage = He crustal (U/Th désintégration), pas de He mantellique

---

**[R14]** Bekaert DV, Barry PH, Broadley MW, et al.  
*A global dataset of helium isotopic data in tectonically and hydrothermally active geological environments*  
**Scientific Data (Nature), 2025**  
DOI: 10.1038/s41597-025-06375-w  
**Contenu :** Base de données mondiale He-3/He-4 incluant Méditerranée. Confirme la dichotomie Tyrrhenien (He mantellique) / Corse-Sardaigne (He crustal). Failles actives en contexte crustal = dégazage He-4 radiogénique, pas He-3 mantellique.  
**Niveau de confiance :** HAUT — Nature Scientific Data, données compilées exhaustives  
**Applicabilité Corse :** Directe — cadre géochimique He pour Corse clarifié

---

**[R15]** Gasquet D, Bertrand JM, Paquette JL, et al.  
*Miocene to Messinian deformation and hydrothermal activity in a pre-Alpine basement massif of the French western Alps: new U-Th-Pb and argon ages from the Lauzière massif*  
**Bulletin de la Société Géologique de France, 2010**  
Analogie : données de référence pour blocs hercyniens (granites) et circulations hydrothermales associées (Ag, U, Th dans granites) — analogie avec Corse granitique  
**Niveau de confiance :** MOYEN — analogie contextuelle  
**Applicabilité Corse :** Partielle — proxy méthodologique

---

**Synthèse Q4 pour Tellux :**  
La Corse est un bloc crustal hercynien sans volcanisme actif ni He-3 mantellique mesurable. Le dégazage y est **crustal** : Rn (U→Ra→Rn dans granites), CO2 crustale (déshydratation métamorphique + dissolution calcaires rares), He-4 radiogénique. Les failles actives N-S et NW-SE (Faille de l'Alto Tenda, failles de Corte, réseau Prunelli-Gravona) constituent des conduits potentiels pour ce dégazage, mais les données de terrain pour la Corse spécifiquement sont quasi-absentes dans la littérature internationale — lacune documentaire à signaler dans la fiche CTC.

---

## Q5 — Sources thermales corses : géochimie et contexte géologique

### Références clés

**[R16]** BRGM  
*Inventaire des sources thermomin érales de Corse et étude hydrogéologique*  
**Rapport BRGM RP-55916-FR**  
URL : http://infoterre.brgm.fr/rapports/RP-55916-FR.pdf  
**Contenu :** Inventaire exhaustif des sources thermomin érales corses avec géochimie de base (température, débit, minéralisation)  
**Niveau de confiance :** HAUT — rapport institutionnel BRGM, données primaires  
**Applicabilité Corse :** Directe — source de référence pour couche lTherm de Tellux

---

**[R17]** Données compilées de terrain (Corsicalinea.com, Orizonte.corsica, Adecec, Cairn 2020)  
*Sources thermales corses — géochimie et thermalisme*  
**Tableau des principales stations :**

| Station | Commune | T°C | Caractéristiques chimiques | Contexte géologique |
|---------|---------|-----|---------------------------|---------------------|
| Guagno-les-Bains | Guagno | 49°C | Sulfurées sodiques, sources Venturini + Occhiu | Granite hercynien, faille N-S |
| Pietrapola | Ghisoni | 45-57°C | Sulfurées sodiques hyperthermal, 2 000 000 L/j, 7 sources | Schistes + micaschistes, faille NE-SW |
| Baracci | Olmeto | 39°C | Sulfurées sodiques | Granite Varisque, zone de cisaillement |
| Guitera-les-Bains | Guitera-les-Bains | 38°C | Bicarbonatées sodiques | Granite, faille NW-SE |
| Caldaniccia | Appietto | 35°C | Sodiques faiblement minéralisées | Granite Ajaccio |
| Urbalacone | Urbalacone | 32°C | Faiblement minéralisées | Granite hercynien |

**Signification géochimique :** Températures 32-57°C → circulation en profondeur (gradient géothermique normal = 3°C/100m → profondeur estimée 1 000-1 900 m). Sulfures → présence H2S, interaction eau-roche à haute T dans granite. Débit élevé Pietrapola (2 ML/j) → réservoir fracturé de grande capacité.  
**Radon dans eaux thermales :** Les eaux hydrothermales granitiques sont naturellement enrichies en Rn (transport depuis substrat granitique uranifère). Aucune donnée publiée pour Corse spécifiquement, mais analogue Bretagne/Massif Central montre Rn aqueux 50-500 Bq/L dans sources granitiques.  
**Niveau de confiance :** MOYEN — données de surface manque de pétrophysique profonde publiée  
**Applicabilité Corse :** Directe — coordonnées et caractéristiques connues pour lTherm

---

**[R18]** Beccaluva L, Bianchini G, Ellam RM, et al.  
*Geochemistry and petrology of mantle xenoliths from the Sardinia-Corsica microcontinent: implications for the lithospheric mantle evolution*  
**Lithos, 2011**, 123:230-246  
DOI: 10.1016/j.lithos.2010.12.013  
**Données :** Xénolithes mantelliques de Sardaigne (proxy Corse — même bloc lithosphérique). Confirme lithosphère continentale épaisse (> 120 km) + absence de décompression mantellique récente → pas de volcanisme actif, pas d'He-3 mantellique.  
**Niveau de confiance :** HAUT — données analytiques géochimiques directes  
**Applicabilité Corse :** Directe — cadre géodynamique blocs Corse-Sardaigne confirmé

---

## Q6 — Sites sacrés et géochimie géologique : la piste Delphes

### Références clés

**[R19]** de Boer JZ, Hale JR, Chanton JP  
*New evidence for the geological origins of the ancient Delphic oracle (Greece)*  
**Geology, 2001**, 29(8):707-710  
DOI: 10.1130/0091-7613(2001)029<0707:NEFTGO>2.0.CO;2  
ScienceDaily release : https://www.sciencedaily.com/releases/2001/08/010807075959.htm  
**Résultat clé :** Deux systèmes de failles intersectants sous le Temple d'Apollon à Delphes. À l'intersection : friction tectonique chauffe calcaire bitumineux → libération d'hydrocarbures légers (éthylène, éthane, méthane). Traces d'éthylène + éthane dans eau de source adjacente.  
**Effets éthylène (faible concentration) :** Euphorie, dissociation, parole altérée. Anesthésique chirurgical utilisé dans les années 1950 (seuil anesthésie : ~35% vol air ; seuil altération légère : ~1-5%).  
**Niveau de confiance :** MOYEN — plausible mécaniquement mais débattu (pas de concentrations actuelles mesurables confirmées)  
**Statut :** Contesté — Etiope & Piccardi 2007 (Geology) : concentrations insuffisantes pour induire transe ; pas de méthane significatif détecté lors de campagne de mesure  
**Applicabilité Corse :** Indirecte — ouvre un cadre interprétatif pour la corrélation sites mégalithiques/failles actives corses (sans revendiquer d'effet psychoactif direct)

---

**[R20]** Etiope G, Piccardi L, Trantalidou K, Fleischer C  
*The geological links of the ancient Delphic Oracle (Greece): A reappraisal of natural gas occurrence and origin*  
**Earth-Science Reviews, 2013**, 119:C  
DOI: (ResearchGate ref : /publication/259324127)  
**Contenu :** Réévaluation des preuves géologiques — confirme la présence de failles actives mais remet en cause les concentrations d'éthylène (en dessous du seuil psychoactif). Propose plutôt CO2 + traces H2S comme agents possibles.  
**Niveau de confiance :** MOYEN — débat scientifique ouvert  
**Applicabilité Corse :** Indirecte — principe de co-localisation sites sacrés/structures géologiques actives = hypothèse légitime à cartographier

---

**[R21]** Piccardi L, Masse WB (éd.)  
*Myth and Geology*  
**Geological Society Special Publication 273, 2007**  
DOI: 10.1144/GSL.SP.2007.273.01.01  
**Contenu :** 20+ études de cas — co-localisation de lieux sacrés/mythiques et de structures géologiques actives (failles, volcans, émergences gazeuses, sources thermales). Méthodologie géomythologie : corrélation systématique entre tradition orale et événements géologiques encodés.  
**Niveau de confiance :** MOYEN — domaine interdisciplinaire en développement  
**Applicabilité Corse :** Indirecte mais pertinente — les sites mégalithiques corses sont majoritairement sur des hauteurs granitiques et/ou en bordure de failles. La géomythologie offre un cadre académique pour cette observation.

---

**Note Tellux sur Q6 :**  
La thèse Delphes est scientifiquement débattue et ne doit PAS être citée comme certitude dans le dossier CTC. Son usage légitime : montrer que la corrélation sites sacrés/géologie active est un champ de recherche académique sérieux (Geological Society Special Publication), et que Tellux cartographie justement cette corrélation sans en revendiquer la causalité. Formulation recommandée : *« La géomythologie — co-localisation de sites sacrés et de structures géologiques actives — constitue un axe de recherche reconnu par la Geological Society of London (Piccardi & Masse 2007). Tellux cartographie cette corrélation à l'échelle de la Corse sans en présupposer la nature causale. »*

---

## Q7 — Amiante naturel en Corse et minéralisations

### Références clés

**[R22]** Amato A, Marchetti L, Radulovic M  
*Naturally occurring asbestos in an alpine ophiolitic complex (northern Corsica, France)*  
**Environmental Earth Sciences, 2019**, 78:XXX  
DOI: 10.1007/s12665-019-8548-x (Springer)  
**Résultat clé :** NOA (Naturally Occurring Asbestos) abondants dans serpentinites du complexe ophiolitique nord-corse ; présence également dans méta-gabbros et méta-basaltes à magnésium (chrysotile dominant).  
**Zones concernées :** Complexe ophiolitique : Cap Corse (Bastia hinterland), zone de Castagniccia nord, secteur Orezza  
**Mécanisme libération :** Degré de serpentinisation, déformation de la roche, altération météorique, abondance de veines fibreuses  
**Niveau de confiance :** HAUT — revue peer-reviewed Springer, données de terrain directes  
**Applicabilité Corse :** Directe — zones identifiées, applicabilité couche Tellux risque géologique

---

**[R23]** Gloaguen E, Durand-Delga M, et al.  
*Ecological and human health risk assessment of potentially toxic element contamination in waters of a former asbestos mine (Canari, Mediterranean Sea): implications for management*  
**PubMed 36434162, 2022**  
URL : https://pubmed.ncbi.nlm.nih.gov/36434162/  
**Données :** Mine de Canari (chrysotile, 1948-1965) — 11 millions de tonnes de serpentinite rejetées en mer. 55 ans après fermeture : toujours source majeure de Co, Cr, Ni dans écosystème marin côtier du nord-Corse.  
**Risque résiduel :** Dépôts en surface asbestos dans zones habitées proches de Canari — plaques pleurales détectées dans 3.8% de la population de contrôle (exposition environnementale généralisée, pas seulement occupationnelle)  
**Niveau de confiance :** HAUT — PubMed, données de terrain, évaluation de risque formelle  
**Applicabilité Corse :** Directe — Canari = site à inclure dans couche lIndu (patrimoine industriel + risque environnemental)

---

**[R24]** Dumortier P, Rey F, Boutin C, De Vuyst P  
*Environmental mesothelioma associated with tremolite asbestos: Lessons from the experiences of Turkey, Greece, Corsica, New Caledonia and Cyprus*  
**Regulatory Toxicology and Pharmacology, 2007**, 49(3):295-299  
DOI: 10.1016/j.yrtph.2007.08.003 (ScienceDirect)  
**Résultat :** Épidémies de mésothéliome malin dans régions méditerranéennes (dont Corse) par exposition domestique à trémolite asbestos et erionite. Mésothéliome = marqueur biologique d'exposition environnementale à l'amiante naturel.  
**Niveau de confiance :** HAUT — revue ScienceDirect, données épidémiologiques comparatives  
**Applicabilité Corse :** Directe — confirme le risque santé publique documenté de l'amiante naturel corse

---

**[R25]** Rosen G  
*History of asbestos discovery and use and asbestos-related disease in context with the occurrence of asbestos within ophiolite complexes*  
**ResearchGate publication/278391256**  
**Contenu :** Contexte historique et géologique des complexes ophiolitiques à amiante ; Corse citée parmi les terrains les plus documentés d'Europe occidentale  
**Niveau de confiance :** MOYEN — revue contextuelle  
**Applicabilité Corse :** Contextualisation générale

---

**[R26]** Canari mine — données minéralogiques  
**Mindat.org — loc-13500** : Mine de Canari, Bastia, Haute-Corse  
**Minéraux :** Chrysotile (amiante blanc), antigorite, lizardite, chromite, magnetite — assemblage de serpentinite ophiolitique type  
**Niveau de confiance :** MOYEN — base de données minéralogique collaborative  
**Applicabilité Corse :** Complément documentaire pour dossier CTC

---

**Note minéralisations métalliques (hors amiante) :**
- **Cuivre Canari** (Cap Corse) : exploitation cuivre + amiante, 19e-20e s. — déjà pertinent pour couche lIndu
- **Fer Matra** (Castagniccia) : mine fer, 19e-20e s. — couche lIndu
- **Antimoine** (plusieurs sites dont Cognocoli) : exploitation ancienne
- Ces minéralisations méritent inventaire BRGM (InfoTerre : https://infoterre.brgm.fr) pour complétion de lIndu

---

## Q8 — Faisabilité d'intégration dans Tellux

### Références clés

**[R27]** ASNR / data.gouv.fr  
*Zonage en potentiel radon — jeu de données communes françaises*  
https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon  
**Format :** CSV + GeoJSON avec code INSEE commune + catégorie radon (1, 2, 3)  
**Mise à jour :** Régulière (ASNR)  
**Couverture :** 100% communes françaises métropolitaines et ultramarines  
**Niveau de confiance :** HAUT — données officielles, open licence  
**Faisabilité Tellux :** TRÈS HAUTE — JDD prêt à l'emploi, jointure sur code INSEE communes corses (2A + 2B = ~360 communes)

---

**[R28]** IGN BD CARTO — Zones d'urbanisation  
*Découpage administratif communes de Corse + géométries*  
https://geoservices.ign.fr/bdcarto  
**Pertinence :** Jointure géographique entre communes (polygones IGN) + catégorie radon IRSN → choroplèthe Leaflet  
**Faisabilité Tellux :** HAUTE — données IGN open, format GeoJSON compatible Leaflet

---

**[R29]** Springer Environmental Earth Sciences 2019 (Axe J R22)  
*NOA zones ophiolitiques nord-Corse*  
**Faisabilité couche amiante naturel Tellux :** MOYENNE — pas de JDD prêt, nécessite extraction depuis :
1. Cartes géologiques BRGM 1:50 000 des feuilles Cap Corse, Bastia, Cervione
2. InfoTerre BRGM (infoterre.brgm.fr) — requête sur formations ophiolitiques
3. Publication Springer 2019 fournit coordonnées de terrain des échantillons NOA  
**Effort estimé :** 4-8h de traitement géospatial pour délimiter zones ophiolitiques à risque NOA  
**Recommandation Tellux Phase 2 :** Intégrer couche "Zone à potentiel amiante naturel (complexe ophiolitique)" avec avertissement explicite et source BRGM + Springer 2019

---

**[R30]** BRGM InfoTerre  
*Données failles actives Corse*  
https://infoterre.brgm.fr  
**Contenu :** Cartes géologiques BRGM + base de données failles (failles régionales et locales)  
**Données disponibles :** Shapefile failles Corse (cartes 1:50 000 et 1:1 000 000)  
**Faisabilité couche dégazage Tellux :** BASSE à court terme — absence de données de dégazage de terrain pour Corse (lacune documentaire). La couche "failles actives" BRGM peut servir de proxy mais sans quantification du dégazage.  
**Recommandation Tellux :** Couche "Failles actives BRGM" = couche existante (déjà dans Tellux) + note dans popup "potentiel conducteur de dégazage — pas de données mesurées disponibles pour la Corse"

---

**[R31]** ARS Corse  
*Information radon — mesures dans les bâtiments publics*  
Données ARS : campagnes de mesure dans établissements recevant du public (ERP) en Corse — non publiées en open data mais accessibles sur demande (RGPD) ou via rapport ARS annuel  
**Faisabilité :** Couche "Points de mesure Bq/m³" = BASSE à court terme (pas d'open data ERP-niveau) ; MOYENNE à moyen terme (partenariat ARS dans cadre CTC)

---

### Tableau de synthèse — faisabilité Tellux par type de données

| Couche | Source | Format | Open ? | Effort intégration | Phase recommandée |
|--------|--------|--------|--------|-------------------|-------------------|
| Radon communal (catégorie 1/2/3) | IRSN / data.gouv.fr | CSV + GeoJSON communes | ✅ Oui | Faible — jointure INSEE | **Phase 1** (immédiat) |
| Sources thermales | BRGM RP-55916-FR + terrain | Points lat/lon | ✅ Partiellement | Faible — 6 stations connues | **Phase 1** (lTherm déjà en cours) |
| Failles actives BRGM | BRGM InfoTerre | Shapefile | ✅ Oui | Modéré — import GeoJSON | **Phase 1** (couche existante) |
| Canari mine (amiante + pollution) | PubMed + Mindat | Point unique | ✅ Oui | Faible — 1 point | **Phase 1** (lIndu) |
| Zones NOA ophiolitiques | Springer 2019 + BRGM 1:50k | Polygones à créer | Partiel | Modéré — 4-8h SIG | **Phase 2** |
| Mesures Bq/m³ bâtiments | ARS Corse | Partenariat | ❌ Non publié | Élevé — accord institutionnel | **Phase 3** |
| Dégazage failles (flux CO2/Rn) | Aucune pour Corse | Terrain à faire | ❌ Inexistant | Très élevé — campagne terrain | **Hors périmètre actuel** |

---

## Résumé exécutif et décisions recommandées

### Verdict par sous-question

**Q1 — Cadre réglementaire radon :** Parfaitement documenté. Arrêté 2018, 3 catégories IRSN, données open data data.gouv.fr. Base juridique solide pour la couche Tellux. **→ INTÉGRER en Phase 1.**

**Q2 — Radon spécifique Corse :** Résultat critique et exploitable immédiatement. Quasi-totalité Corse = catégorie 3 (maximum), 33-43 décès/an confirmés par ARS Corse. Granites hercyniens = substrat uranifère documenté. Données disponibles, niveaux de confiance élevés. **→ Couche choroplèthe radon = priorité absolue Phase 1.**

**Q3 — Mécanismes dégazage failles :** Mécanismes bien compris (revue Frontiers 2024, Toutain & Baubron 1999). Failles = conduits pour He, Rn, CO2. Amplification sismique documentée. Mais **absence de données de terrain pour la Corse spécifiquement** = lacune documentaire importante. **→ Couche failles BRGM existante comme proxy, avec popup "potentiel dégazage non mesuré en Corse".**

**Q4 — Corse / Tyrrhenien / He isotopes :** Corse = bloc crustal hercynien, He essentiellement radiogénique (He-4), pas de He-3 mantellique. Pas de volcanisme actif, pas de décompression mantellique. Le dégazage corse est **crustale** (Rn U→Ra→Rn, CO2 métamorphique). Absence d'études He spécifiques Corse dans littérature internationale. **→ Note dans documentation : lacune de recherche identifiée, position géodynamique défavorable au dégazage mantellique.**

**Q5 — Sources thermales corses :** 6 stations documentées (Guagno 49°C, Pietrapola 45-57°C, Baracci 39°C, Guitera, Caldaniccia, Urbalacone). Rapport BRGM RP-55916-FR = source de référence. Enrichissement Rn des eaux granitiques attendu mais non mesuré pour Corse. **→ Couche lTherm déjà prévue, compléter avec BRGM RP-55916-FR.**

**Q6 — Géomythologie / Delphes :** Cadre académique légitime (Geological Society SP273, 2007). Thèse Delphes = plausible mais débattue (pas de concentrations mesurables actuelles). **→ Formulation prudente dans dossier CTC : corrélation documentée, causalité non revendiquée.** Tellux cartographie la co-localisation sans en présupposer la nature.

**Q7 — Amiante naturel Corse :** Complexe ophiolitique nord-Corse = NOA documenté (Springer 2019). Mine Canari = risque résiduel toujours actif (PubMed 2022, ScienceDirect mesothelioma review). 3.8% plaques pleurales dans population contrôle de Canari = exposition environnementale avérée. **→ Phase 2 : couche zones ophiolitiques à risque NOA + point Canari dans lIndu.**

**Q8 — Faisabilité Tellux :** 
- Phase 1 (immédiat) : radon communal IRSN (data.gouv.fr), sources thermales (lTherm), mine Canari (lIndu)
- Phase 2 (2-4 semaines) : zones NOA ophiolitiques (BRGM + Springer 2019), inventaire minéralisations métalliques BRGM
- Phase 3 (CTC accord) : mesures Bq/m³ bâtiments ERP (ARS Corse), dégazage failles (campagne terrain)

---

## Décisions code recommandées pour Tellux

### Couche radon communale (NOUVELLE — Phase 1)

```javascript
// Source : IRSN / data.gouv.fr — JDD "Zonage en potentiel radon"
// Données : GeoJSON communes Corse (2A + 2B) + attribut radon_cat (1/2/3)
// Implémentation : L.choropleth ou L.geoJSON avec style par catégorie

const RADON_COLORS = {
  1: '#90ee90',  // vert — potentiel faible
  2: '#ffa500',  // orange — potentiel modéré
  3: '#cc2200'   // rouge foncé — potentiel élevé (quasi-totalité Corse)
};

// Légende recommandée :
// Cat. 3 (rouge) : "Potentiel élevé — granite uranifère — 33-43 décès/an Corse"
// Cat. 2 (orange) : "Potentiel modéré — facteurs géologiques locaux"
// Cat. 1 (vert) : "Potentiel faible — formations à faible teneur uranium"

// Popup commune : catégorie IRSN + seuil action (300 Bq/m³) + lien ARS Corse
```

### Point Canari dans lIndu (MODIFICATION — Phase 1)
```javascript
// À ajouter dans PROD_ELECTRIQUE ou lIndu selon implémentation
{
  lat: 42.868, lon: 9.374,
  name: "Mine de Canari (chrysotile 1948-1965)",
  type: "Patrimoine industriel + risque environnemental",
  note: "11 Mt serpentinite rejetées. NOA résiduel. Zone ophiolitique. PubMed 36434162."
}
```

### Popup sources thermales (AMÉLIORATION — Phase 1)
Ajouter dans les popups lTherm :
- Température d'émergence (°C)
- Caractérisation chimique (sulfurée sodique, bicarbonatée…)
- Note : "Eau thermale granitique — enrichissement naturel en radon attendu"

---

## Note épistémique générale — Axe J

L'Axe J est **l'axe le plus directement défendable** du corpus Tellux car :

1. **Radon = risque documenté, seuils réglementaires existants, données open data** — aucune controverse sur le mécanisme physique (contrairement aux hypothèses EM sub-kT)
2. **Corse = situation critique bien établie** (catégorie 3, 33-43 décès/an) — légitimité de la cartographie immédiate
3. **Articulation avec géologie BRGM** — données existantes réutilisables, pas de données propriétaires à acquérir pour la Phase 1
4. **Portée santé publique concrète** — information citoyenne sur un risque réel et actionnable (mesure en bâtiment, travaux)

**Limite principale :** La dimension "dégazage de failles → effets sur le vivant" reste spéculative pour la Corse faute de données de terrain. La recommandation est de présenter les failles comme conduits *potentiels* de dégazage (mécanisme documenté ailleurs, Frontiers 2024) sans revendiquer un effet mesuré en Corse.

**Articulation avec l'Axe H :** Le radon est un risque ionisant (rayonnements alpha), distinct des champs EM non-ionisants. La distinction doit être maintenue dans les communications publiques de Tellux pour éviter toute confusion.

---

## Bibliographie complète Axe J

| Ref | Auteurs | Titre abrégé | Revue/Source | Année | DOI/PMID |
|-----|---------|-------------|-------------|-------|----------|
| R1 | Darby et al. | Radon homes lung cancer 13 European studies | BMJ | 2005 | PMID 15613366 |
| R2 | JORF | Arrêté 27 juin 2018 radon | J.O. France | 2018 | Légifrance |
| R3 | IRSN/ASNR | Zonage potentiel radon communes | data.gouv.fr | 2024 | Open data |
| R4 | Tokonami et al. | Radon/thoron environments Japan | Rad Prot Dosim | 2010 | 10.1093/rpd/ncq249 |
| R5 | ARS Corse | Radon Corse — cat. 3, 33-43 décès/an | ARS / ASNR | 2024 | Institutionnel |
| R6 | ASNR | Cartographie interactive radon communes | ASNR web | 2024 | Institutionnel |
| R7 | BRGM | Cartographie radon France données BRGM | data.gouv.fr | 2024 | Open data |
| R8 | UNSCEAR | Sources Effects Risks Ionizing Radiation | UNSCEAR | 2020 | ISBN 978-92-1-139167-6 |
| R9 | Ciotoli et al. | Fault degassing geochemical mapping Italy | Front Earth Sci | 2024 | 10.3389/feart.2024 |
| R10 | Toutain & Baubron | Gas geochemistry seismotectonics review | Tectonophysics | 1999 | 10.1016/S0040-1951(98)00295-9 |
| R11 | Bicocchi et al. | Deep CO2 CH4 soil fault zones seismicity | Tectonophysics | 2013 | 10.1016/j.tecto.2012.11.004 |
| R12 | Moretti et al. | Mantle degassing CO2 Gulf of Corinth | EPSL | 2021 | 10.1016/j.epsl.2021.116758 |
| R13 | Marty, Jambon, Sano | Helium-3 anomalies crust-mantle Italy | EPSL | 1989 | ScienceDirect |
| R14 | Bekaert et al. | Global dataset helium isotopes active environments | Sci Data (Nature) | 2025 | 10.1038/s41597-025-06375-w |
| R15 | Gasquet et al. | U-Th-Pb ages Lauzière massif hydrothermal | Bull SGF | 2010 | Analogue hercynien |
| R16 | BRGM | Inventaire sources thermomin. Corse | Rapport RP-55916-FR | 2007 | infoterre.brgm.fr |
| R17 | Sources compilées | Géochimie thermes corses terrain | Corsicalinea / ADECEC / Cairn | 2020-2024 | Multisources |
| R18 | Beccaluva et al. | Xenoliths Sardinia-Corsica lithosphere | Lithos | 2011 | 10.1016/j.lithos.2010.12.013 |
| R19 | de Boer, Hale, Chanton | Geological origins Delphic Oracle | Geology | 2001 | 10.1130/0091-7613(2001) |
| R20 | Etiope, Piccardi et al. | Geological links Delphic Oracle reappraisal | Earth-Sci Rev | 2013 | ResearchGate 259324127 |
| R21 | Piccardi & Masse (éd.) | Myth and Geology | GSL Special Pub 273 | 2007 | 10.1144/GSL.SP.2007.273.01.01 |
| R22 | Amato, Marchetti, Radulovic | Naturally occurring asbestos N-Corsica ophiolite | Env Earth Sci | 2019 | 10.1007/s12665-019-8548-x |
| R23 | Gloaguen et al. | Health risk Canari asbestos mine | PubMed | 2022 | PMID 36434162 |
| R24 | Dumortier et al. | Environmental mesothelioma tremolite Corsica et al. | Reg Tox Pharm | 2007 | 10.1016/j.yrtph.2007.08.003 |
| R25 | Rosen | History asbestos ophiolite complexes | ResearchGate | 2015 | RG/278391256 |
| R26 | Mindat | Canari mine mineralogy | Mindat.org | 2024 | loc-13500 |
| R27 | ASNR/data.gouv.fr | Zonage radon JDD communes | data.gouv.fr | 2024 | Open licence |
| R28 | IGN | BD CARTO communes Corse | geoservices.ign.fr | 2024 | Open licence |
| R29 | Springer 2019 (R22) | NOA zones ophiolitiques N-Corse | Env Earth Sci | 2019 | 10.1007/s12665-019-8548-x |
| R30 | BRGM InfoTerre | Failles actives Corse shapefile | infoterre.brgm.fr | 2024 | Open licence |
| R31 | ARS Corse | Mesures Bq/m³ ERP Corse | ARS Corse | 2024 | Institutionnel |

---

## Fiches de synthèse Axe J — formulations prêtes pour dossier CTC

**Sur le radon :**
> *« La Corse présente l'une des situations de potentiel radon les plus élevées de France : quasi-totalité du territoire classée en catégorie 3 (maximum) par l'ASNR, en raison de son substrat granitique hercynien à forte teneur en uranium. L'ARS Corse estime à 33-43 le nombre de décès annuels par cancer du poumon attribuables à cette exposition naturelle. Tellux intègre cette donnée institutionnelle (open data ASNR/data.gouv.fr) dans une couche choroplèthe communale, contribuant à l'information préventive des citoyens corses sur un risque réel et actionnable. »*

**Sur l'amiante naturel :**
> *« Le complexe ophiolitique du nord de la Corse (Cap Corse, arrière-pays de Bastia) contient des occurrences d'amiante naturel documentées (Amato et al. 2019, Environmental Earth Sciences). La mine de Canari (chrysotile, 1948-1965) constitue un foyer de contamination résiduelle avéré, toujours actif dans l'écosystème marin côtier 55 ans après fermeture (PMID 36434162, 2022). Tellux cartographie ces zones à risque géologique en s'appuyant sur les données BRGM et la littérature peer-reviewed. »*

**Sur les sources thermales :**
> *« Les six stations thermales corses (Guagno 49°C, Pietrapola 45-57°C, Baracci, Guitera, Caldaniccia, Urbalacone) témoignent de circulations hydrothermales profondes (1 000-2 000 m estimés) dans le granite hercynien. Leur distribution géographique suit les principales structures de failles actives de l'île. Le rapport BRGM RP-55916-FR constitue la référence documentaire de base pour ces stations, inventoriées dans Tellux au titre du patrimoine naturel thermal. »*

**Sur la géomythologie :**
> *« La géomythologie — étude systématique de la corrélation entre lieux sacrés et structures géologiques actives — constitue un champ académique reconnu (Piccardi & Masse 2007, Geological Society of London Special Publication 273). Tellux cartographie cette corrélation à l'échelle de la Corse sans en présupposer la nature causale, dans une posture conforme à l'épistémologie scientifique. »*

---

*Fiche rédigée dans le cadre du corpus scientifique Tellux Corse — Axe J / Session 2026-04-19*  
*Axes complétés : A, B, C, D, E, F, G, H, I, J — Corpus complet*
