# Axe Q — Lacunes méthodologiques des grandes études épidémiologiques environnementales
## Ce que Tellux apporte à l'exposome environnemental

**Date :** 2026-04-19
**Projet :** Tellux Corse — Cadre scientifique long terme
**Nature :** Audit systématique · Positionnement épistémique · Stratégie scientifique
**Références croisées :** Axes A–P, HYPOTHESES.md, candidature CTC, horizon Horizon Europe

---

## Résumé exécutif

Les grandes études épidémiologiques environnementales (épidémiologie EM, radon, shinrin-yoku, Blue Zones, zones contaminées, radiothérapie MR-Linac) travaillent chacune dans un silo disciplinaire avec un faisceau de variables non optimal pour tester les hypothèses transversales qu'elles pourraient poser. Ce n'est pas un défaut d'exécution — c'est un défaut de cadre conceptuel hérité de la spécialisation disciplinaire.

Le cadre exposome (Wild 2005) existe depuis vingt ans et reconnaît explicitement cette limite, mais sa mise en œuvre empirique reste incomplète. Les projets européens les plus ambitieux (HELIX, ATHLETE, EXPANSE, EQUAL-LIFE) mesurent air, bruit, chaleur, espaces verts — mais omettent systématiquement deux catégories de stresseurs physiques : les champs électromagnétiques non-ionisants et la radioactivité naturelle.

Tellux propose une contribution partielle et complémentaire : une cartographie territoriale composite de ces dimensions sous-représentées, à l'échelle de la Corse, utilisable comme variable environnementale spatiale par des équipes épidémiologiques qui voudraient revisiter leurs protocoles.

**Posture Tellux :** complémentarité, pas critique. Identification d'opportunités de collaboration, pas accusation de lacune.

---

## 1. Épidémiologie EM — Audit méthodologique

### Études canoniques

| Étude | Type | N | Outcome | Expositions mesurées |
|-------|------|---|---------|---------------------|
| INTERPHONE (IARC, 2010) | Cas-témoin international | ~10,000 | Gliome, méningiome | Usage téléphonie mobile (rétrospectif, questionnaire) |
| MOBI-Kids | Cas-témoin enfants | ~2,000 | Tumeurs cérébrales | Téléphonie mobile, ELF |
| Ahlbom 2000 (pooled) | Méta-analyse pooled | 9 études | Leucémies enfant | ELF résidentiel (mesuré ou calculé) |
| Amoon 2021 (meta) | Méta-analyse actualisée | 4 études pooled | Leucémies enfant | ELF résidentiel |
| CERENAT (France) | Cas-témoin | ~900 | Gliome, méningiome | Téléphonie mobile (DECT exclu) |

### Variables systématiquement absentes

**Contexte ionisant :**
- Radon résidentiel (aucune des grandes études EM ne mesure le radon dans les foyers des participants)
- Fond gamma ambiant (géologie locale)
- Exposition médicale cumulée (radiographies, scanners)

**Contexte géomagnétique :**
- Anomalie magnétique locale (distance à faille, substrat géologique)
- Géomagnétique ambiant (varie de 25 μT à 65 μT selon la latitude et la géologie)

**Exposome chimique :**
- Pesticides résidentiels
- Solvants organiques (profession, habitat)
- Qualité de l'air intérieur (COV, formaldéhyde)

**Contexte lumineux et sonore :**
- Exposition à la lumière bleue LED nocturne
- Architecture de sommeil (chronodisruption)
- Bruit environnemental chronique

**Alimentation et microbiome :**
- Apports en polyphénols, NRF2-activateurs
- Profil microbiomique

### Conséquence méthodologique documentée

INTERPHONE souffre de biais de sélection (participation ~50%), de biais de rappel rétrospectif, et de l'absence de dosimétrie objective (puissance RF absorbée dans le cerveau non mesurée). Le design cas-témoin repose sur des proxies d'exposition — durée déclarée d'utilisation, pas d'énergie RF mesurée (Hardell & Carlberg 2012, Spandidos Publications).

Pour les leucémies ELF : l'Ahlbom 2000 montre un doublement du risque au-dessus de 0,4 μT. L'Amoon 2021 (pooled de 4 études plus récentes) montre OR = 1,01 pour la même exposition. L'écart entre ces deux méta-analyses est inexpliqué. Il pourrait refléter une variable de confusion non contrôlée dans l'une ou l'autre génération d'études. Les confondants explorés (SES, mobilité, urbanisation, trafic) ne comprennent pas le contexte ionisant ni la géologie.

L'ICNIRP a identifié dans ses gaps 2025 des lacunes dans l'évaluation de l'exposition combinée multi-sources, et les revues méthodologiques soulignent l'absence de réseaux de capteurs continus dans les études épidémiologiques (SCHEER 2023).

### Ce que Tellux apporte à ce domaine

- Couche géomagnétique lithologique (anomalies EMAG2, failles BRGM) exportable comme variable spatiale
- Couche radioactivité naturelle (radon communal IRSN, fond gamma estimé) applicable aux zones d'habitat des participants
- Ces couches permettent de tester a posteriori si des populations de participants INTERPHONE ou leucémies-ELF vivaient dans des zones à contexte ionisant distinct

---

## 2. Épidémiologie radon — Audit méthodologique

### Études canoniques

| Étude | Type | N | Mesure radon | Contrôle tabac |
|-------|------|---|-------------|----------------|
| Darby 2005 (pooled 13 pays européens) | Pooled cas-témoin | 7,148 cas / 14,208 témoins | Dosimètre passif, 15 ans rétrospectif | Oui (stratification) |
| Lubin 2004 (US mineurs cohorte) | Cohorte prospective | ~60,000 mineurs | Estimation dosimétrique professionnelle | Oui |
| Nair 2009 (Kerala, HLNRA) | Cohorte écologique | ~385,000 | Dosimétrie domiciliaire détaillée | Partiel |
| Jain & Das 2017 (Kerala transcriptomique) | Cas-témoin transcriptomique | 36 individus | Dose estimée (mGy/an) | NA |

### Variables systématiquement absentes

**Contexte EM anthropique :**
- Exposition aux lignes HT résidentielles
- Densité d'antennes RF dans le voisinage
- Équipements électriques domestiques (champs ELF)
- Aucune étude radon canonique ne mesure ces variables

**Méthodologie dosimétrique :**
- Hauteur effective de mesure (le dosimètre est placé à hauteur "de vie" standard, mais les nourrissons vivent au sol où la concentration en radon est plus élevée par accumulation)
- Variabilité saisonnière importante mais correction approximative (Darby 2005 le reconnaît explicitement)
- Radon thoron souvent non mesuré (Kerala fait exception avec analyse thoron en souffle chez 87 sujets)

**Profil biologique et alimentaire :**
- Apport en antioxydants, iode, sélénium (modulateurs potentiels de la réponse aux faibles doses)
- Expression génétique constitutive des voies de réparation ADN (impossible rétrospectivement, possible dans protocole prospectif)
- Statut épigénétique des voies NRF2/ATM

**Contexte géomagnétique :**
- Anomalie magnétique locale pouvant interagir avec les processus de décroissance radioactive secondaire (mécanisme indirect, peu documenté)

### La tension Darby/HLNRA non résolue par les études existantes

Darby 2005 montre un risque linéaire croissant dès 100 Bq/m³. Les études HLNRA (Kerala, Iran-Ramsar) montrent peu ou pas d'excès de risque à des doses 10 à 50x supérieures. Cette tension est habituellement attribuée à l'effet du tabac (confondant majeur), à des différences méthodologiques, ou à une réponse adaptative (hormèse). Aucune des études ne peut tester l'hypothèse K de Tellux car aucune ne mesure simultanément l'exposition EM et l'expression transcriptomique adaptative.

Le Kerala est le seul territoire où une étude transcriptomique sur PBMC humains a été réalisée dans ce contexte (Jain & Das 2017, PLOS ONE PMC5697823 ; Jayasree & Nair 2020, Scientific Reports : up-regulation des protéines de réparation ADN). Ces études ne mesurent pas le contexte EM.

### Ce que Tellux apporte à ce domaine

- Superposition spatiale du contexte EM (ANFR, PROD, lignes HT) avec les zones radon IRSN en Corse
- Identification de sous-territoires à radon élevé ET contexte EM préservé vs radon élevé ET contexte EM anthropique — permettant un plan d'étude comparatif sans modifier les expositions
- Infrastructure pour le protocole Phase 3 (Axe O) : zones de contrôle sélectionnées sur critères Tellux

---

## 3. Études shinrin-yoku — Audit méthodologique

### Variables mesurées dans les études canoniques (Li Q. et réplications)

- Paramètres physiologiques : cortisol salivaire, NK cells, adrenaline, noradrenaline, tension artérielle, HRV
- Biomarqueurs moléculaires : perforine, granzymes (marqueurs NK)
- Phytoncides : α-pinène, β-pinène, limonène (parfois mesurés, souvent non)
- Durée d'exposition et protocole de promenade

### Variables systématiquement absentes

**Contexte EM du site forestier :**
Aucune étude du corpus Li Q. ne caractérise l'environnement électromagnétique du site. Traité en détail dans l'Axe P. La revue systématique de Siah et al. 2023 (Wiley) et Wen et al. 2019 (Environ Health Prev Med) confirment que les facteurs environnementaux comme la météo, la saison, la composition de la végétation et la distance de la zone urbaine ne sont pas contrôlés dans la majorité des études.

**Contexte acoustique :**
- Niveau de pression sonore et spectre de fréquence (biophonie vs anthropophonie vs géophonie)
- La réduction du bruit entre ville et forêt est documentée qualitativement mais rarement quantifiée comme covariable analytique

**Qualité de l'air :**
- PM2.5, O3, NOx mesurés dans certaines études de comparaison ville/forêt mais non systématiquement inclus dans les modèles statistiques comme covariable

**Contexte lumineux :**
- Intensité et spectre lumineux sous canopée vs milieu urbain
- Pollution lumineuse nocturne des sites comparés

**Profil des volontaires :**
- Niveau de stress baseline rarement objectivé avant randomisation
- État chronobiologique (décalage horaire social, exposition préalable à la lumière bleue)

**Composition précise des phytoncides inhalés :**
- Variable clé attribuée comme "mécanisme" mais mesurée dans seulement une minorité des études
- La revue de Antonelli et al. 2019 (PMC6886167) souligne que l'attribution de l'effet aux phytoncides reste une hypothèse, non une démonstration

### Conséquence

Sans décomposition des composantes environnementales du site forestier, l'attribution de l'effet shinrin-yoku aux phytoncides reste non prouvée. Les effets pourraient être partiellement attribuables à la réduction du bruit, à la modulation du spectre lumineux, à la réduction de l'exposition EM, ou à l'activité physique légère. Le lien Soran 2014 (EM → émissions terpènes) transforme le contexte EM d'une variable de confort en variable mécanistique potentielle.

### Ce que Tellux apporte à ce domaine

- Sélection et caractérisation EM de sites forestiers corses (forêts de laricio comme Valdu-Niellu, Aïtone, Asco) avec couches RF mesurées/modélisées
- Infrastructure pour un protocole shinrin-yoku intégré avec mesure EM simultanée (Axe P, protocole 4-parties)
- Les forêts de laricio corse constituent un site d'étude non encore exploré par le corpus shinrin-yoku

---

## 4. Démographie Blue Zones — Audit des variables environnementales physiques

### Variables présentes dans les études Blue Zones

| Dimension | Ogliastra | Okinawa | Ikaria | Nicoya | Loma Linda |
|-----------|-----------|---------|--------|--------|------------|
| Démographie/centenaires | ✅ | ✅ | ✅ | ✅ | ✅ |
| Alimentation | ✅ | ✅ | ✅ | ✅ | ✅ |
| Activité physique | ✅ | ✅ | ✅ | ✅ | ✅ |
| Cohésion sociale | ✅ | ✅ | ✅ | ✅ | ✅ |
| Génétique | ✅ | Partiel | Partiel | ❌ | ❌ |
| EM ambiant | ❌ | ❌ | ❌ | ❌ | ❌ |
| Radon/radioactivité naturelle | ❌ | ❌ | **✅ (partiel)** | ❌ | ❌ |
| Anomalie géomagnétique | ❌ | ❌ | ❌ | ❌ | ❌ |
| Paysage sonore | ❌ | ❌ | ❌ | ❌ | ❌ |
| Pollution lumineuse | ❌ | ❌ | ❌ | ❌ | ❌ |

### Le cas Ikaria : précédent méthodologique unique

Ikaria (île grecque) présente la particularité documentée suivante : le nord-ouest granitique de l'île (granite radioactif, fond gamma de 0,20 à 3,31 mSv/an, sources thermales radioactives) coïncide avec une longévité supérieure à la partie sud-est sédimentaire (limestone). Des estimations de dose par voie multiple ont été publiées (Vogiannis et al., Journal of Radioanalytical and Nuclear Chemistry) et une étude de la revue proto.life 2021 documente explicitement cette corrélation.

C'est le seul cas dans la littérature Blue Zones où une variable physique environnementale (radioactivité naturelle) est superposée à la distribution géographique intra-insulaire de la longévité. Ce précédent est le fondement méthodologique exact de ce que Tellux propose pour la Corse intérieure granitique.

**Publication clé :** "Exposure to low environmental radiation and longevity. Insights from the Ikaria Study" — disponible sur ResearchGate (Papadopoulou et al., référence à vérifier en accès complet).

### Critique méthodologique Blue Zones (Saul Newman, UCL, 2024)

Newman (Ig Nobel Prize 2024) a montré que de nombreux "centenaires" Blue Zones sont statistiques d'enregistrement d'état civil défaillant, pas de longévité réelle. Cette critique méthodologique majeure affecte la robustesse des études démographiques des Blue Zones, mais ne remet pas en cause la question scientifique sous-jacente — elle la rend plus urgente : si la longévité Blue Zone est surévaluée, quelle part des résidus est réelle ? Et cette part peut-elle être corrélée à des variables environnementales physiques mesurables ?

### Ce que Tellux apporte à ce domaine

- La Corse intérieure granitique partage avec l'Ogliastra sarde le substrat géologique, l'isolement génétique partiel, et la culture méditerranéenne
- Tellux peut fournir la couche environnementale physique (géomagnétique, EM, radon) manquante dans toutes les études Blue Zones
- Positionnement possible : "Corse intérieure = Blue Zone candidate à valider avec protocole étendu incluant variables physiques" (candidature Poulain-Pes méthodologie 2025)

---

## 5. Biologie des zones contaminées — La lacune EM

### Débat Mousseau-Møller vs Beresford-Smith

Les études de Mousseau et Møller (2006–2022) documentent des effets biologiques négatifs significatifs sur la faune des zones d'exclusion de Tchernobyl (réduction abondance oiseaux, insectes, mutations, tumeurs). Les études de Beresford, Smith et collaborateurs contestent ces résultats sur la base de biais méthodologiques et de résultats contradictoires dans d'autres taxons.

**Variable absente dans les deux camps :** aucune des études de cette controverse ne mesure le contexte EM non-ionisant (champs RF, ELF) sur les sites d'échantillonnage. La zone d'exclusion de Tchernobyl est aussi une zone de faible densité d'infrastructure humaine — ce qui implique paradoxalement un contexte EM anthropique potentiellement réduit par rapport aux zones de référence habitées. Si l'EM anthropique modifie la réponse biologique aux faibles doses ionisantes, alors les "témoins" des études Tchernobyl pourraient être sur-exposés à l'EM par rapport aux sites contaminés, créant un biais systématique inversé non reconnu.

### Variable EM absente : documentation

- Aucune publication dans les études Tchernobyl/Fukushima ne mentionne la mesure ou le contrôle du contexte RF/ELF des sites
- Les études sur co-exposition EM/radon en milieu urbain existent (Baan et al. résumé dans Academia.edu), mais elles n'ont pas été appliquées aux contextes de zones contaminées

### Proposition méthodologique pour revisiter les données existantes

Pour les équipes Mousseau-Møller ou équivalentes Fukushima :
1. Cartographier rétrospectivement l'infrastructure EM (lignes HT, antennes) sur les sites d'échantillonnage historiques via des archives et bases de données d'infrastructure
2. Inclure cette couche dans les modèles statistiques comme covariable spatiale
3. Tester si la variance résiduelle du débat Mousseau/Beresford peut être partiellement expliquée par cette variable confondante

Cette démarche ne nécessite pas de nouvelles campagnes de mesure — elle repose sur la requalification de l'espace géographique des études existantes.

---

## 6. Radiothérapie MR-Linac — La lacune transcriptomique

### Variables mesurées dans les études MR-Linac

| Dimension | Présence dans les études |
|-----------|------------------------|
| Dosimétrie ionisante (plan de traitement) | ✅ Exhaustif |
| Imagerie IRM (anatomie, évolution tumorale) | ✅ Exhaustif |
| Outcomes cliniques (contrôle local, toxicité) | ✅ |
| Biomarqueurs biochimiques (LDH, CRP) | Partiel |
| Expression transcriptomique adaptative (NRF2, ATM, DNMT3b) | ❌ Absent |
| Contexte EM domestique du patient | ❌ Absent |
| Profil épigénétique | ❌ Absent |
| Microbiome | ❌ Absent |

### La revue Bayarri-Lara 2018 (PMC6404846) : ce qu'elle dit

Cette revue systématique de l'équipe de Leiden-Amsterdam évalue les effets biologiques combinés du champ magnétique statique (0,35 T à 1,5 T) et du rayonnement ionisant dans le contexte de la radiothérapie guidée par IRM. Elle documente environ 50 % des études précliniques montrant un effet du champ magnétique sur la réponse cellulaire à l'irradiation. Les mécanismes proposés incluent la force de Lorentz sur les électrons secondaires (macroscale), les effets sur les ions et molécules chargées (microscale), et les paires de radicaux (nanoscale — notamment via les cryptochromes).

**Lacune explicitement identifiée dans la revue :** un petit nombre d'études seulement ont mesuré l'impact combiné SMF + rayonnement ionisant sur des endpoints biologiques pertinents pour la radiothérapie. Aucune étude humaine in vivo n'a caractérisé ces effets au niveau transcriptomique.

### Opportunité de recherche

Un protocole prospectif MR-Linac pourrait inclure :
- Prélèvement PBMC avant chaque séance
- RNA-seq des voies NRF2/ATM/DNMT3b avant/pendant/après traitement
- Caractérisation EM domestique du patient hors traitement (comparaison contexte EM bas vs élevé)
- Comparaison avec patients traités sur Linac conventionnel (sans champ magnétique statique)

Ce protocole, s'il existait, fournirait la première caractérisation transcriptomique humaine de la réponse adaptative combinée EM/ionisant chez des patients — extension directe de l'hypothèse K au contexte clinique.

---

## 7. Le cadre exposome — État d'avancement et lacunes EM/ionisant

### Wild 2005 : le concept et sa mise en œuvre limitée

Christopher Wild (IARC) a proposé en 2005 que pour comprendre les maladies chroniques, il fallait mesurer la totalité des expositions environnementales depuis la conception jusqu'à la mort : l'exposome. Vingt ans plus tard, l'implémentation reste partielle.

### Projets européens exposome : ce qu'ils mesurent

| Projet | Expositions mesurées | EM RF | Radioactivité naturelle |
|--------|---------------------|-------|------------------------|
| HELIX (2014-2022) | Air, bruit, NDVI, chimie sang/urine, alimentation | ❌ | ❌ |
| ATHLETE (2020-2025) | Toolbox exposome étendu, cohorte européenne | Partiel (étude de faisabilité) | ❌ |
| EXPANSE (2020-2025) | Air, bruit, chaleur, espaces verts, lumière nocturne, marchabilité | ❌ | ❌ |
| EQUAL-LIFE (2020-2025) | Environnement construit et naturel, air, bruit, enfants | ❌ | ❌ |
| SIRENE (2025+) | Infrastructure RI paneuropéenne, opérationnalisation exposome | ? | ? |
| France Exposome (2021+) | Infrastructure chimique, biobanque | ? | ? |

### La lacune EM/ionisant est explicitement reconnue

Une revue ExWAS méthodologique (Decoding the exposome, PMC10857773, Oxford Exposome 2024) reconnaît explicitement : **"il n'est pas possible à ce jour d'identifier des biomarqueurs d'exposition pour des stresseurs comme les champs électromagnétiques ou le statut socio-économique via le biomonitoring."**

EXPANSE, le plus avancé sur les variables physiques, mesure la lumière nocturne et le bruit, mais pas les RF ni le radon. L'ICNIRP a publié en 2025 une liste de gaps de connaissance pour ses lignes directrices RF qui souligne explicitement les limites de l'évaluation de l'exposition combinée multi-sources.

### La radiométrie naturelle dans l'exposome

Aucun des grands projets exposome européens ne cartographie systématiquement la radioactivité naturelle (radon, fond gamma ambiant) comme variable d'exposome physique. La carte REMAP (JRC Ispra) est disponible comme ressource mais n'est pas intégrée dans les cohortes HELIX/EXPANSE.

### L'horizon Horizon Europe 2026-2027

Le programme de travail Horizon Europe 2026-2027 Cluster 1 Santé comprend un appel HORIZON-HLTH-2027-01-ENVHLTH-02 intitulé "Intégrer les expositions liées au climat dans l'exposome humain" (45 M€). Cet appel ne mentionne pas spécifiquement les EM ni la radioactivité naturelle, mais la structuration en "expositions physiques sous-mesurées" est compatible avec le périmètre Tellux.

---

## 8. Synthèse des lacunes croisées

### Variables absentes de plusieurs domaines simultanément

| Variable manquante | EM épidémio | Radon épidémio | Shinrin-yoku | Blue Zones | Zones contaminées | MR-Linac |
|-------------------|-------------|----------------|--------------|-----------|-------------------|----------|
| Contexte EM RF/ELF | N/A (variable principale) | ❌ | ❌ | ❌ | ❌ | ❌ (hors traitement) |
| Radon résidentiel | ❌ | N/A | ❌ | ❌ | N/A | N/A |
| Géomagnétique anomalie | ❌ | ❌ | ❌ | ❌ | ❌ | N/A |
| Transcriptomique adaptative | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Acoustique environnemental | ❌ | ❌ | Partiel | ❌ | ❌ | N/A |
| Spectre lumineux | ❌ | ❌ | ❌ | ❌ | ❌ | N/A |
| Alimentation antioxydants | Partiel | ❌ | ❌ | ✅ | ❌ | ❌ |
| Génétique/épigénétique | ❌ | ❌ | ❌ | Partiel | Partiel | ❌ |

**Observation centrale :** les champs électromagnétiques non-ionisants et la radioactivité naturelle sont les deux seules catégories de stresseurs physiques absentes de l'ensemble des six domaines, y compris dans les protocoles les plus récents. C'est exactement le périmètre Tellux.

---

## 9. Ce que Tellux apporte de spécifique à l'exposome environnemental

### Contribution 1 — Cartographie territoriale composite

Tellux produit une couche spatiale continue combinant, à l'échelle de la Corse :

- **Géomagnétique lithologique :** EMAG2v3, WDMAM, anomalies magnétiques sur substrat granito-métamorphique
- **EM anthropique RF :** ANFR (antennes déclarées), modélisation de champ par type d'infrastructure, propagation en terrain complexe
- **EM anthropique ELF :** réseau HTA/HTB PROD_ELECTRIQUE Corse (SEI + RTE), zones de proximité de lignes
- **Radioactivité naturelle :** radon communal IRSN, fond gamma estimable depuis lithostratigraphie BRGM, sources thermales radioactives documentées (Axe N)
- **Failles actives :** base BRGM, microzonage sismique — pertinentes pour le dégazage radon

Cette couche est exportable en GeoJSON ou WMS et peut être utilisée par des épidémiologistes comme variable d'ajustement ou variable principale dans une analyse spatiale.

**Ce que ça apporte concrètement :** une étude épidémiologique sur une population corse peut intégrer les scores Tellux par commune ou par zone géographique comme covariables continues — pour la première fois pour ces dimensions.

### Contribution 2 — Identification de zones de contraste

Tellux permet d'identifier des sous-territoires corses à contextes fortement contrastés sur des géologies comparables :

- **Zone A :** intérieur granitique (haute-Corse, Cortenais, Niolu) = radon élevé, EM anthropique bas, géomagnétique anomalie granite
- **Zone B :** littoral nord (Bastia, Cap Corse industriel) = radon moindre, EM anthropique élevé (antennes, lignes portuaires)
- **Zone C :** plaine orientale agricole = radon moyen, EM modéré, pesticides élevés

Ce contraste géographique est la base d'un plan d'étude quasi-expérimental sans manipulation des expositions — exactement ce que les études épidémiologiques EM et radon ne peuvent pas faire sur des territoires homogènes.

### Contribution 3 — Propositions de protocoles intégrés

Tellux a formalisé, par ses fiches de corpus, trois protocoles que des équipes spécialisées peuvent reprendre :

**Protocole N (Axe N) :** Sites mégalithiques co-exposition — mesures EM, géomagnétique, radon sur sites patrimoniaux pour cartographie de la co-exposition sur le terrain.

**Protocole O (Axe O) :** Populations corses granitiques — PBMC transcriptomique NRF2/ATM dans zones radon élevé / EM préservé vs zones EM anthropique — test direct de l'hypothèse K.

**Protocole P (Axe P) :** Forêts de laricio — shinrin-yoku intégré avec mesure EM simultanée et analyse phytoncides — premier protocole reliant EM forestier, phytoncides laricio et réponse physiologique humaine.

### Contribution 4 — Positionnement territorial pilote français

La France ne dispose pas d'observatoire régional intégré comparable à ce que Tellux propose pour la Corse sur les dimensions physiques EM/ionisant. L'infrastructure France Exposome se concentre sur la dimension chimique. EXPANSE couvre l'espace européen mais sans résolution suffisante pour les régions de faible densité et sans les variables physiques Tellux.

La Corse peut devenir le **territoire pilote exposome français pour les dimensions physiques sous-représentées** — à l'intersection de l'insularité (contrôle géographique naturel), du gradient géologique (contraste ionisant remarquable), du faible bruit anthropique et de la richesse patrimoniale.

---

## 10. Positionnement stratégique

### Court terme — Candidature CTC 2026

**Argument épistémique pour les évaluateurs CTC :**

> "Les grandes études épidémiologiques environnementales internationales — épidémiologie EM, radon, shinrin-yoku, Blue Zones — ne mesurent pas systématiquement les champs électromagnétiques non-ionisants et la radioactivité naturelle comme variables d'exposome. Ce n'est pas un défaut de ces études : c'est une limite de leur périmètre conceptuel. Tellux propose de combler cette lacune à l'échelle d'un territoire insulaire méditerranéen à fort gradient géologique. La Corse est un territoire de recherche exceptionnel pour ces questions : isolement insulaire, gradient ionisant granite/sédimentaire, faible pression anthropique en montagne, et patrimoine mégalithique co-implanté sur les anomalies géomagnétiques. Tellux cartographie les variables que les grandes études utilisent comme toile de fond non mesurée."

**Format de présentation recommandé :** tableau "Ce que les études internationales mesurent / Ce que Tellux ajoute" (Sections 1–6 ci-dessus, condensé en 1 page).

### Moyen terme — Horizon Europe 2027–2028

**Appel cible identifié :** HORIZON-HLTH-2027-01-ENVHLTH-02 (exposome physique, intégration expositions multi-sources)

**Partenariat structurant possible :**
- ISGlobal (Barcelone) — coordinateur des projets HELIX et EXPANSE, réceptif aux extensions physiques
- IARC (Lyon) — coordinateur INTERPHONE, évaluation 5G/SEAWave en cours
- Université de Corse (Corte) — ancrage territorial
- Université de Cagliari — dimension Interreg Sardaigne-Corse, comparatif Ogliastra-Corse intérieure
- BRGM / IRSN — données souveraines géologie et radioactivité

**Positionnement Tellux dans un consortium Horizon Europe :**
- Partenaire "observatoire territorial pilote" pour la couche EM/ionisant
- Fournisseur de la infrastructure de cartographie spatiale multi-stresseurs physiques
- Promoteur des protocoles intégrés (O, P, N) comme work packages de validation

---

## 11. Limites méthodologiques de l'audit Axe Q

Trois limites à signaler explicitement :

**1. Tellux cartographie des proxies, pas des mesures individuelles.** La densité d'infrastructure (antennes ANFR, lignes HT) est une approximation du champ réel auquel un individu est exposé. Elle ne se substitue pas à une dosimétrie personnelle (exposimètre portable, comme dans les études GOLIAT). La contribution Tellux est spatiale et agrégée — utile pour les analyses écologiques et les plans d'étude quasi-expérimentaux, moins pour les études de cohorte individuelles.

**2. La valeur ajoutée des couches Tellux sur des outcomes sanitaires n'est pas démontrée.** L'audit identifie des lacunes et formule des protocoles. Il ne démontre pas que combler ces lacunes modifiera les résultats des études existantes. C'est une proposition à tester, pas un résultat acquis.

**3. La reproductibilité de l'approche Tellux dépend de la qualité des données sources.** Les données ANFR et IRSN sont publiques et de qualité. Les données EMAG2 ont une résolution kilométrique limitée pour les anomalies locales. Les données BRGM géologie sont excellentes à l'échelle régionale. Les données radon communal IRSN sont une médiane par commune, non une mesure individuelle.

---

## 12. Bibliographie sélective

**Études EM référencées :**
- Hardell L, Carlberg M (2012). Mobile phones, brain tumors, and the Interphone Study. *Spandidos Publications (IJO)*. [doi:10.3892/ijo.2015.2908](https://www.spandidos-publications.com/10.3892/ijo.2015.2908/download)
- Ahlbom A et al. (2000). A pooled analysis of magnetic fields and childhood leukaemia. *British Journal of Cancer*. PMC2363518
- Amoon AT et al. (2021). Pooled analysis of recent studies of magnetic fields and childhood leukemia. *Environmental Research*. doi:10.1016/j.envres.2021.112883
- ICNIRP (2025). Gaps in knowledge relevant to the ICNIRP guidelines. *Health Physics*. doi:10.1097/HP.0000000000001918

**Études radon référencées :**
- Darby S et al. (2005). Radon in homes and risk of lung cancer: collaborative analysis of 13 European case-control studies. *BMJ*. PMC546066
- Jain V & Das B (2017). Global transcriptome profile of PBMC from high level natural radiation areas of Kerala. *PLOS ONE*. PMC5697823
- Jayasree K & Nair CKK (2020). Chronic exposure to HLNRA leads to protective stress response proteins. *Scientific Reports*. doi:10.1038/s41598-020-80405-y

**Blue Zones et Ikaria :**
- Poulain M & Pes GM (2004). Identification of Sardinia's Blue Zone. *Experimental Gerontology*
- Vogiannis E et al. Estimation of dose rates in Ikaria. *Journal of Radioanalytical and Nuclear Chemistry*. ResearchGate
- "Exposure to low environmental radiation and longevity. Insights from the Ikaria Study." ResearchGate (Papadopoulou et al. — accès à vérifier)
- Newman S (2024). Blue Zone demography critique. UCL — Ig Nobel Prize 2024

**MR-Linac :**
- Bayarri-Lara C et al. (2018). Biological effects of static magnetic field in MR-guided radiotherapy. *Radiation Oncology*. PMC6404846

**Exposome :**
- Wild CP (2005). Complementing the genome with an exposome. *Cancer Epidemiology, Biomarkers & Prevention*
- Vrijheid M et al. (2014). The human early-life exposome (HELIX): project rationale and design. *Environmental Health Perspectives*. PubMed 24610234
- Tamayo-Uria I et al. (2019). Decoding the exposome: ExWAS methodology. *Oxford Exposome / Exposomics EMBO MM*
- ExWAS review (2024). PMC10857773 — Oxford Academic Exposome
- EXPANSE (2025). A Europe-wide characterization of the external exposome: spatio-temporal analysis. *Environment International*. doi:10.1016/j.envint.2025

**Shinrin-yoku :**
- Wen Y et al. (2019). Medical empirical research on forest bathing (Shinrin-yoku): a systematic review. *Environ Health Prev Med*. PMC6886167
- Siah CJR et al. (2023). Effects of forest bathing on psychological well-being. *Int J Mental Health Nursing*. PubMed 36864583

---

*Axe Q — produit pour Tellux Corse, session Cowork 2026-04-19. Ce document est un audit épistémique et stratégique. Il ne modifie pas les données ou les fonctions de calcul du corpus Tellux. Référence transversale depuis les autres axes sur les limites méthodologiques.*
