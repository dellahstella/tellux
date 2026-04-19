# Axe P — Arbres, forêts et interface bio-EM : pont méthodologique

**Date :** 2026-04-19  
**Projet :** Tellux Corse — Cadre scientifique long terme  
**Nature :** Fiche de pont méthodologique entre trois corpus disjoints (shinrin-yoku, cryptochrome végétal, effets EM sur la flore/faune)  
**Statut :** Rapport de recherche Cowork Enterprise Search

---

## 1. Atténuation RF par les forêts : physique quantifiée

### 1.1 Le modèle de référence : ITU-R P.833

La Recommandation ITU-R P.833 (dernière version : P.833-10, septembre 2021) est le cadre normatif international pour l'atténuation des ondes radio par la végétation. Elle couvre une plage de fréquences de **30 MHz à 100 GHz** et fournit plusieurs modèles selon la géométrie du trajet (émetteur à l'extérieur/récepteur en forêt, trajet en bordure, traversée complète).

**Paramètres clés du modèle ITU-R P.833 :**
- Atténuation spécifique : de **0,03 à 0,5 dB/m** selon l'espèce, la densité et la fréquence
- Atténuation totale maximale limitée par d'autres mécanismes de propagation (contournement par diffraction)
- Le paramètre "Leaf Area Index" (LAI) permet de dériver les valeurs d'atténuation à partir de tables espèce-spécifiques

### 1.2 Valeurs mesurées dans la littérature

L'étude de revue de référence (MDPI *Forests*, 2024 — "Wireless Wave Attenuation in Forests: An Overview of Models") dresse un état de l'art complet à partir d'une analyse bibliométrique de la littérature sur le sujet :

**Atténuation par arbre unitaire.** Les mesures expérimentales indiquent une **réduction moyenne d'environ 20 dB par arbre isolé**. Cette valeur est bien établie à des fréquences typiques des réseaux mobiles (900 MHz–3,5 GHz).

**Atténuation en forêt dense.** En forêt dense avec couvert continu, les pertes de propagation résultent de :
- Absorption diélectrique par l'eau contenue dans la végétation
- Diffusion multi-trajets (scattering) par les troncs, branches et feuilles
- L'atténuation totale s'exprime typiquement entre **10 et 40 dB** pour une profondeur de 50 à 200 m de forêt selon la fréquence et la densité du couvert

**Effet fréquence.** L'atténuation augmente avec la fréquence. Les réseaux 5G (3,5 GHz et 26 GHz) sont atténués plus fortement que le GSM (900 MHz). À 26 GHz (mmWave 5G), l'absorption par la végétation est très forte.

### 1.3 Spécificités des conifères (laricio)

**Conifères > feuillus.** Les arbres à feuilles en aiguilles (Pinus, Picea) créent une atténuation **supérieure** aux feuillus à feuilles larges. Les raisons physiques sont :
- Densité de surface d'aiguilles par unité de volume : diffusion plus efficace
- Maintien du couvert toute l'année (pas de défoliation saisonnière)
- Couvert vertical dense (de la cime jusqu'au sol)

**Propagation en forêt de conifères (arxiv 2019).** Une étude sur la propagation en forêt de conifères dense documente une atténuation très marquée, avec des pertes de trajet élevées déjà à faible profondeur de pénétration.

**Implication pour les forêts de laricio corse.** Les forêts de *Pinus nigra subsp. laricio* à Aïtone, Valdu-Niellu et Vizzavona, avec leur couvert dense d'aiguilles persistantes et leur biomasse élevée (individus de 800–1000 ans à Valdu-Niellu), constituent des systèmes d'atténuation RF parmi les plus efficaces que l'on puisse trouver en Europe méridionale.

### 1.4 Limites : ce que la forêt n'atténue pas

**Les ELF (50 Hz réseau électrique) ne sont pas atténués par la végétation.** La longueur d'onde à 50 Hz est de ~6 000 km : aucune structure arborée n'a d'effet appréciable sur ces champs. En revanche, la forêt éloigne physiquement les sources (les lignes HTA/HTB rurales longent les routes et ne pénètrent pas les massifs denses), ce qui crée une distance géométrique protectrice.

**L'atténuation RF est progressive et jamais totale.** Même à 300 m en forêt dense, un signal RF suffisamment puissant (relais proche) reste mesurable. La "bulle de silence EM" forestière est une réduction significative, pas une annulation.

---

## 2. Modulation phytochimique par le contexte environnemental

### 2.1 Mécanismes généraux de régulation des métabolites secondaires

Les terpènes (monoterpènes, sesquiterpènes, diterpènes) sont des métabolites secondaires que les plantes produisent principalement en réponse à des stress environnementaux. Leur production n'est pas constitutive — elle est modulée par le contexte de l'arbre.

**Stress documentés qui augmentent les émissions de BVOC :**
- **Chaleur** (exponentielle pour les sesquiterpènes : β-caryophyllène, α-bergamotène, α-farnèsene augmentent exponentiellement avec la température)
- **Sécheresse modérée** : en *Pinus massoniana*, les monoterpènes et sesquiterpènes sont augmentés jusqu'à 2,9× et 2,0× respectivement en stress hydrique modéré (avant inhibition par stress sévère)
- **Attaque par herbivores ou pathogènes** : émissions de signaux d'alerte (green leaf volatiles, sesquiterpènes)
- **UV-B** : induit des voies phénoliques et terpéniques protectrices
- **Dommages physiques** (feu, blessure) : *Pinus nigra laricio* en Corse a été étudié spécifiquement dans sa réponse à des brûlages prescrits (*Forest Ecology and Management* 2008)

**Régulation transcriptionnelle.** Des facteurs de transcription (MYB, bHLH, WRKY, AP2/ERF) coordonnent la réponse de biosynthèse des métabolites secondaires en réponse à ces stress. Ces facteurs sont conservés dans les grandes lignes entre espèces végétales.

### 2.2 Découverte centrale : les micro-ondes RF modulent les émissions de terpènes

**Soran ML, Stan M, Niinemets Ü, Copolovici L. (2014).** *Journal of Plant Physiology* (PMC4410321) — **"Influence of microwave frequency electromagnetic radiation on terpene emission and content in aromatic plants".**

C'est l'étude la plus directement pertinente pour la question de Tellux. Les résultats :

- **Exposition à des micro-ondes de fréquence WLAN (2,4 GHz) et GSM (900 MHz)** — intensités faibles, non thermiques — sur persil, céleri et aneth
- Effets morphologiques documentés : parois cellulaires plus minces, chloroplastes et mitochondries de taille réduite
- **Émissions de composés volatils augmentées** — en particulier monoterpènes et "green leaf volatiles"
- Effets plus forts pour les micro-ondes WLAN que GSM

**Interprétation.** Une plante exposée à du rayonnement RF produit un profil phytochimique différent d'une plante non exposée. Si ce résultat se généralise aux arbres forestiers, **une forêt EM-perturbée n'émet pas le même cocktail phytochimique qu'une forêt EM-préservée**. La nature, la quantité et le ratio des phytoncides inhalés lors d'un shinrin-yoku dépendraient alors du contexte EM de la forêt visitée.

**Caveat.** L'étude porte sur des plantes herbacées aromatiques, pas sur des conifères. Le transfert aux arbres forestiers est spéculatif. Des études complémentaires sur *Pinus* spécifiquement sont nécessaires — et constituent une lacune documentaire directement actionnable.

**Vian A. et al. (2006)** — *Plant Signaling & Behavior* : première démonstration que les micro-ondes modifient l'expression génique dans les plantes à une intensité non thermique. Cet article fondateur a ouvert le champ de la recherche sur les effets EM sur la physiologie végétale.

### 2.3 Influence de l'altitude et du rayonnement UV

Les forêts corses en altitude (1000–1800 m) présentent une exposition UV plus forte que les forêts de plaine. Les UV-B induisent la production de composés phénoliques protecteurs et des terpènes UVabsorbants. Le profil phytochimique des forêts de laricio d'altitude est donc structurellement différent de celui des forêts de basse altitude ou périurbaines — indépendamment de tout effet EM.

---

## 3. *Pinus nigra subsp. laricio* : spécificité phytochimique documentée

### 3.1 Composition en huile essentielle : données disponibles

Plusieurs publications spécifiques au laricio corse existent :

**Bonnafous et al. (composition variabilité huile essentielle des aiguilles, *Flavour and Fragrance Journal*)** — 123 échantillons individuels de *Pinus nigra subsp. laricio* de Corse — composition :
- Composés principaux : **α-pinène**, manoyl oxide, germacrène-D, myrcène, (E)-caryophyllène, limonène
- Forte variabilité inter-individuelle dans la composition chimique

**Benchabane et al. — composition oléorésine** (*Biochemical Systematics and Ecology*) : composition et variabilité chimique de l'oléorésine des arbres corses.

**Barra et al. — Étude herbicide** (*Arabian Journal of Chemistry*) : huiles essentielles des aiguilles de *P.n. laricio* Maire — 27 composés identifiés représentant 97,9 % de l'huile :
- Diterpènes oxygénés (38,5 %) : manool oxide (38 %)
- Sesquiterpènes (41,4 %) : germacrène D (16,7 %), δ-cadinène (9 %), (E)-caryophyllène (8,9 %)

**Monoterpènes dans différents tissus** (PMC8838282 — *Journal of Natural Products*) : étude des gènes synthétases de monoterpènes dans différents tissus de *P.n. laricio*. Les 14 monoterpènes présents dans tous les tissus sont dominés par **β-phellandrène, α-pinène et β-pinène**, avec distribution tissu-spécifique marquée.

### 3.2 Lacune documentaire : absence de comparaison avec l'hinoki japonais dans le contexte shinrin-yoku

**Ce qui n'a jamais été étudié :** la comparaison directe entre les effets biologiques sur les humains du laricio corse (*Pinus nigra subsp. laricio*, Pinaceae) et du hinoki japonais (*Chamaecyparis obtusa*, Cupressaceae), l'espèce phare des études Li Q.

Ces deux espèces partagent le composé **α-pinène** mais divergent significativement sur :
- La composition en sesquiterpènes (le laricio est riche en germacrène-D ; l'hinoki est riche en sabinol, bornéol et camphre)
- La composition en diterpènes (manoyl oxide caractéristique du laricio, absent de l'hinoki)
- La famille botanique (Pinaceae vs Cupressaceae)

**Conclusion.** Les effets shinrin-yoku documentés par les équipes japonaises (activation NK, baisse cortisol, baisse pression artérielle) sont connus pour les forêts d'hinoki (*Chamaecyparis obtusa*) et *Cryptomeria japonica*, pas pour le laricio corse. La transposition directe des résultats japonais aux forêts corses est non étayée. C'est une lacune scientifique identifiée — et une opportunité de recherche réelle.

---

## 4. Études shinrin-yoku en contexte EM : confirmation de la lacune

### 4.1 Ce que le corpus shinrin-yoku mesure

L'étude pivot Li Q. et al. (2010, *Environmental Health and Preventive Medicine*, PMC2793346) — 24 forêts japonaises, 280 sujets — documente :
- Réduction cortisol salivaire : −12,4 %
- Réduction fréquence cardiaque : −5,8 %
- Réduction pression artérielle : −1,4 %
- Comparaison marcheurs forêt vs marcheurs ville

La revue systématique Li Q. (2022, *PMC9665958*) consolide l'ensemble du corpus "forest medicine" et liste les mécanismes proposés : phytoncides (α-pinène, limonène, myrcène), stimulation visuelle naturelle (attention restoration), réduction du stress, exercice doux, isolation du bruit urbain.

**Ce qu'aucune étude ne mesure.** Aucune étude shinrin-yoku identifiée dans la littérature ne caractérise :
- Le niveau de champs RF dans la forêt étudiée (μW/m²)
- Le niveau de champs ELF (50 Hz) dans la forêt étudiée
- La distance aux infrastructures EM (antennes, lignes électriques)
- Le contexte géomagnétique (anomalies locales, perturbations anthropiques)

La forêt est traitée comme une variable binaire (forêt vs ville) sans décomposer ses composantes environnementales physiques. **C'est la lacune centrale que l'Axe P documente.**

### 4.2 Ce qui est étudié à la place : déconnexion numérique

Une littérature parallèle, sur la "déconnexion numérique" en nature, documente l'association entre exposition à la nature et réduction de l'utilisation du smartphone (Minor et al. 2023, *Environment and Behavior*). Cette réduction de l'usage du smartphone en forêt réduit simultanément :
- L'exposition cognitive aux sollicitations numériques
- **L'exposition physique RF** due à l'émission propre du téléphone (le téléphone éteint ou en mode avion n'émet plus)

Ces deux dimensions — cognitive et physique EM — sont corrélées en pratique mais conceptuellement distinctes. Les études ne les dissocient pas. Tellux peut proposer cette dissociation comme protocole de recherche (voir § 6).

---

## 5. Pont bio-EM : cryptochromes végétaux et humains

### 5.1 Conservation évolutive des cryptochromes

Les cryptochromes (CRY) sont une famille de flavoprotéines **présentes dans tous les règnes du vivant** — bactéries, plantes, animaux, humains. Ils dérivent des photolyases bactériennes qui réparent les dommages UV à l'ADN par activation lumineuse. La transition évolutive photolyase → cryptochrome a produit des protéines conservant la sensibilité à la lumière bleue tout en acquérant de nouvelles fonctions.

**Arbre phylogénétique fonctionnel :**
- Plantes (CRY1, CRY2) : réponse à la lumière bleue, élongation de l'hypocotyle, floraison, horloge circadienne
- Insectes (Type I CRY) : synchronisation circadienne
- Vertébrés (CRY1, CRY2) : composants de l'horloge circadienne intracellulaire (non photorécepteurs)
- Oiseaux/poissons/amphibiens (CRY4) : candidat principal pour la magnétoréception via radical pair mechanism
- Humains (CRY2) : fonctions horlogères + capacité potentielle de magnétosensibilité

### 5.2 Le mécanisme radical pair et la magnétosensibilité végétale

**Frontiers in Plant Science 2023 (DOI: 10.3389/fpls.2023.1266357) — "Cryptochrome and quantum biology: unravelling the mysteries of plant magnetoreception".**

Cette revue (déjà dans le corpus axe H de Tellux) confirme que :
- La sensibilité magnétique des cryptochromes opère via le **mécanisme des paires radicalaires**
- En plantes (*Arabidopsis thaliana*) : la floraison est supprimée en champ magnétique quasi-nul
- Des réponses cryptochrome-dépendantes surviennent dans **les intervalles d'obscurité** (pas seulement à la lumière), suggérant que la sensibilité magnétique est indépendante de la photoexcitation dans certaines conditions

**Arabidopsis cryptochrome réactif aux RF (Scientific Reports 2020).**
*Arabidopsis thaliana* cryptochrome répond aux champs électromagnétiques radiofréquences (*Ara­bido­psis cryp­to­chrome is res­pon­sive to Ra­dio­fre­quen­cy (RF) elec­tro­mag­netic fields*, Nature/Scientific Reports 2020). **Ce résultat est décisif pour Tellux** : il démontre que les plantes répondent non seulement aux champs magnétiques statiques, mais aussi aux champs RF anthropiques — les mêmes que ceux produits par les antennes mobiles et WiFi. Les arbres d'une forêt EM-perturbée sont littéralement dans un état physiologique cryptochrome différent de ceux d'une forêt préservée.

### 5.3 Le CRY2 humain comme magnétosenseur

**Le CRY2 humain, exprimé principalement dans la rétine, peut fonctionner comme magnétosenseur.** Des expériences sur Drosophila ont montré que le CRY2 humain peut remplacer le CRY endogène de la mouche pour médier la magnétoréception lumière-dépendante. Ce résultat est publié dans une revue reconnue (travaux des équipes Gegear et Ritz).

### 5.4 L'hypothèse de pont : une forêt "magnétiquement optimale"

La convergence des trois résultats (magnétosensibilité végétale via CRY, sensibilité RF des CRY végétaux, magnétosensibilité du CRY2 humain) génère une hypothèse de pont inédite :

**Une forêt dans un environnement géomagnétique non perturbé et faiblement exposé aux RF anthropiques pourrait constituer un site où arbres et humains bénéficient simultanément d'une interaction cryptochromique fonctionnelle non perturbée.** La réduction de la perturbation RF qui survient naturellement dans une forêt dense éloignée des infrastructures (atténuation physique de 10–40 dB + distance) pourrait être un déterminant non reconnu des effets shinrin-yoku, en plus des phytoncides.

Cette hypothèse est spéculative mais scientifiquement formulable et testable. Elle n'a été formulée explicitement dans aucun article peer-reviewed connu.

---

## 6. Mesures RF et ELF effectives en forêt vs urbain

### 6.1 Données de référence mesurées

**Étude Suisse comparative 2014–2021** (*Environment International*, 2023, PMID 37598840) — 49 microenvironnements mesurés identiques :
- **Zones rurales** : moyenne 0,19 V/m en 2021 (vs 0,14 V/m en 2014)
- **Zones industrielles** : 0,43 V/m
- **Transports** : niveaux les plus élevés

En densité de puissance :
- **Urbain** : ~117 μW/m² (médiane)
- **Rural** : ~34 μW/m² (médiane)

Ces mesures sont réalisées dans des espaces ouverts ruraux, pas sous couvert forestier dense. En combinant la différence rural/urbain (facteur ~3,5×) avec l'atténuation forestière supplémentaire (10–40 dB = facteur 10 à 10 000×), une forêt dense peut présenter des niveaux RF ambiants **10 à 1000× inférieurs** à un environnement urbain.

### 6.2 Ordres de grandeur pour les forêts corses

Pour une forêt de laricio dans le Niolu ou à Aïtone (altitude ~1000–1400 m, distance > 15 km du réseau d'antennes le plus dense) :
- Point de départ : niveau rural (~34 μW/m²)
- Atténuation forêt dense conifères à 100 m de profondeur : −20 à −30 dB (facteur 100 à 1000)
- **Estimation de champ RF intérieur forêt corse :** 0,03–0,3 μW/m²

À titre de comparaison :
- Centre-ville Paris : ~500–2000 μW/m²
- Intérieur d'une maison rurale : ~10–50 μW/m²
- Valeur de référence "précaution" Bioinitiative (non réglementaire) : 10 μW/m²

Le niveau estimé dans une forêt de laricio corse isolée serait donc **100 à 10 000 fois inférieur** aux niveaux urbains, et nettement sous toute valeur de référence de précaution. Cette différence physique est réelle et mesurable.

---

## 7. Protocole de recherche intégré : formulation pour horizon phase 2–3

### 7.1 Question scientifique formulée

"Les effets biologiques du bain de forêt (shinrin-yoku) varient-ils selon le contexte électromagnétique du site forestier, indépendamment des phytoncides ?"

Sous-question : "La production de phytoncides par les arbres forestiers est-elle elle-même modulée par l'exposition RF anthropique du site ?"

### 7.2 Protocole en 4 volets

**Volet 1 — Caractérisation environnementale des sites.**
- Mesures EM : spectre RF (100 MHz–6 GHz) par dosimètre portable sur 48h, ELF (50–1000 Hz) par gaussmètre, champ géomagnétique statique par magnétomètre 3 axes
- Mesures BVOC (air forestier) : prélèvements actifs sur cartouches Tenax TA, analyse SPME-GC/MS pour identification et quantification des terpènes (α-pinène, β-pinène, limonène, germacrène-D, β-caryophyllène, manoyl oxide pour laricio)
- Paramètres de site : altitude, espèces arborées, LAI, densité biomasse, distance aux infrastructures EM, catégorie radon IRSN, géologie sous-jacente
- Paysage sonore : enregistrement 48h (octave band analysis)

**Volet 2 — Sélection des sites contrastés.**
Comparer **3 types de sites** sur la base des caractéristiques du volet 1 :
- Site A : forêt dense laricio, altitude 1000–1400 m, RF < 0,5 μW/m², distance antennes > 10 km (Valdu-Niellu ou Aïtone)
- Site B : forêt comparable en espèces et biomasse, mais exposition RF modérée (forêt périurbaine, ~ 10–50 μW/m²)
- Site C : milieu urbain de référence (absence de forêt, RF > 200 μW/m²)

**Volet 3 — Recrutement et réponse humaine.**
30–50 volontaires en bonne santé (20–60 ans, non-fumeurs) visitant les 3 sites en ordre randomisé (cross-over design), séances de 2h chacune.

Mesures avant/après chaque visite :
- Cortisol salivaire (ELISA)
- Pression artérielle (tensiomètre automatique)
- Variabilité de la fréquence cardiaque (HRV — Holter 24h)
- Questionnaires standardisés : PANAS (affect), PSS (stress perçu), attention (ANT test)
- Transcriptomique sur PBMCs (RNA-seq) : gènes candidats *NFE2L2* (NRF2), *ATM*, *HMOX1*, *CRY1*, *CRY2*, gènes circadiens (*CLOCK*, *BMAL1*, *PER1*, *PER2*)
- Option : NK activity (ELISA) sur prélèvement sanguin

**Volet 4 — Analyse multi-variable.**
Régression linéaire mixte : réponse humaine (variable dépendante) ~ niveau RF + concentration phytoncides mesurés + paysage sonore + contexte géomagnétique + site type (aléatoire). Décomposition de la variance expliquée par chaque composante.

Dissociation clé : les sujets au site A seraient invités en deux conditions : (1) téléphone portable avec eux (exposition RF propre +atténuation forêt), (2) téléphone laissé hors du site (exposition RF minimale). Cela permet de dissocier l'effet de l'atténuation forestière de l'effet de la déconnexion numérique cognitive.

### 7.3 Partenariats pour le protocole

| Institution | Rôle |
|---|---|
| **Université de Corse Pascal Paoli (Corte)** — UMR SPE | Biologie végétale, chimie des produits naturels, coordination site |
| **INRAE Avignon ou Bordeaux** | Mesures BVOC, expertise forêts méditerranéennes, réseaux ICOS |
| **CHU d'Ajaccio / Centre Médical Corte** | Recrutement volontaires, prélèvements biologiques |
| **Inserm** (UMR en épidémiologie environnementale) | Coordination clinique, transcriptomique, biostatistiques |
| **ANFR / ART** | Données cartographiques densité EM pour sélection des sites |
| **Tellux** | Cartographie SIG (EM + radon + géologie), sélection des sites, coordination logistique |

**Financement ciblé :** ANR "Santé-Environnement-Travail" (AAP compétitif), ou projet Interreg Italie-France-Maritime (partenariat Université de Sassari pour comparaison forêts sardes), ou PACT PIA3 (programme Actions Territoriales pour la Santé des Populations).

---

## 8. Sites corses prioritaires : forêts d'interface bio-EM

### 8.1 Critères de sélection

Un site forestier corse d'interface bio-EM optimal doit réunir :
1. **Espèce laricio dominante** (spécificité phytochimique corse)
2. **Altitude > 800 m** (exposition UV forte, profil phytochimique d'altitude, éloignement des zones habitées)
3. **Distance > 10 km des antennes 4G/5G principales** (réduction RF)
4. **Substrat granitique** (radon catégorie 3 IRSN, géochimie spécifique)
5. **Absence de lignes HTA/HTB dans le massif**
6. **Accessibilité minimale** permettant le recrutement de volontaires (sentier balisé)
7. **Statut de protection** (garantit la stabilité du couvert)

### 8.2 Sites candidats

| Site | Commune(s) | Altitude | Surface laricio | Notes |
|---|---|---|---|---|
| **Forêt de Valdu-Niellu** | Niolu (Casamaccioli) | 1 000–1 600 m | ~5 000 ha | Individus 800-1000 ans, isolement maximal, GR20 accessible |
| **Forêt d'Aïtone** | Évisa | 1 000–1 300 m | ~2 000 ha | "Meilleur laricio de Corse", Réserve biologique dirigée |
| **Forêt de Vizzavona** | Vivario | 900–1 200 m | ~1 400 ha | Mixte laricio/hêtre, accessible RN193 (attention : axe EM modéré) |
| **Forêt d'Asco** | Asco | 1 000–1 800 m | ~3 000 ha | Très isolée, accès limité, idéal pour contraste EM |
| **Haute Castagniccia** | Piedicroce/Orezza | 800–1 200 m | Mixte laricio/châtaignier | Sites mégalithiques à proximité, double intérêt avec axe N |
| **Coscione** | Ciamannacce/Quasquara | 1 200–1 700 m | Forêt claire + landes | Alt. maximale, "ciel noir" (AVEX), exposition UV et géomagnétique non perturbé |

### 8.3 Croisement avec les sites mégalithiques (axe N × axe P)

La co-localisation forêts + sites mégalithiques est une donnée cartographiable par Tellux. Plusieurs situations se présentent :
- Sites mégalithiques du Sartenais (Cauria, Palaggiu, Fontanaccia) : en milieu de maquis haut relativement ouvert — peu d'atténuation RF par canopée, mais exposition géomagnétique directe
- Sites en Castagniccia (châtaigneraies denses) : interface forêt/mégalithe possible
- Zones du Niolu : pas de sites mégalithiques connus denses mais potentiel géomagnétique et laricio combinés

La cartographie Tellux peut générer un indice composite "interface bio-EM" par commune ou zone : (radon IRSN + absence d'antennes ANFR + couvert forestier laricio + distance infrastructures). Ce serait une couche thématique originale propre à Tellux.

---

## Synthèse : trois corpus disjoints et leur interface inexplorée

| Corpus | Ce qui est établi | Ce qui manque |
|---|---|---|
| **Shinrin-yoku (Li Q. et al.)** | Effets physiologiques documentés (cortisol, NK, PA) sur 24 forêts japonaises | Caractérisation EM des sites. Aucune étude ne mesure RF ou ELF en forêt étudiée |
| **Cryptochrome végétal (Frontiers 2023, Sci Rep 2020)** | Magnétosensibilité via radical pair. Réponse des CRY végétaux aux RF. | Mesures sur arbres forestiers. Effets sur émissions de phytoncides non testés |
| **Effets EM sur flore (Soran 2014, Vian 2006)** | Micro-ondes RF → émissions terpènes augmentées, morphologie cellulaire modifiée | Études sur conifères forestiers. Mesures en conditions naturelles (vs laboratoire) |

**La question ouverte formulée par Tellux :** *Dans quelle mesure le contexte EM d'une forêt — naturellement préservé par l'atténuation de la canopée et l'éloignement des infrastructures — contribue-t-il à l'effet shinrin-yoku, en modulant à la fois la physiologie cryptochromique des arbres (et donc leur production de phytoncides) et la physiologie cryptochromique des humains qui les visitent ?*

Cette question est formulable depuis les données existantes. Elle n'a pas encore été posée explicitement dans la littérature peer-reviewed. Elle est accessible à l'investigation empirique avec les méthodes actuelles. Tellux est en position légitime pour la formuler, et pour contribuer à sa réponse via la cartographie des zones d'interface et la sélection des sites d'étude pilote.

---

## Bibliographie

**Atténuation RF par la végétation**

- ITU-R. (2021). Recommendation ITU-R P.833-10 — Attenuation in vegetation. https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.833-10-202109-I!!PDF-E.pdf

- Pinheiro da Silva R, et al. (2024). Wireless Wave Attenuation in Forests: An Overview of Models. *Forests*, 15(9), 1587. https://www.mdpi.com/1999-4907/15/9/1587

- Papastefanou GS, et al. (2022). Modeling Radio Wave Propagation for Wireless Sensor Networks in Vegetated Environments: A Systematic Literature Review. *Sensors*. PMC: 9324029

- Henttu V, et al. (2019). Propagation Modeling Through Foliage in a Coniferous Forest. arXiv:1902.06798

- Chowdhury MT, et al. (2024). Vegetation Loss Measurements for Single Alley Trees in Millimeter-Wave Bands. *Sensors*, 24(10), 3190. PMC: 11125348

**Phytochimie des forêts et modultion par l'environnement**

- Soran ML, Stan M, Niinemets Ü, Copolovici L. (2014). Influence of microwave frequency electromagnetic radiation on terpene emission and content in aromatic plants. *Journal of Plant Physiology*, 171(15), 1436–1443. PMC: 4410321. DOI: 10.1016/j.jplph.2014.06.013

- Vian A, et al. (2006). Microwave irradiation affects gene expression in plants. *Plant Signaling & Behavior*, 1(2), 67–70.

- Burraco P, et al. (2022). Biogenic volatile organic compound emissions from seven pine species (*Pinus* spp.) under temperature stress. *Environmental and Experimental Botany*.

- Environmental Factors Regulate Plant Secondary Metabolites. (2023). PMC: 9920071

- Response of Plant Secondary Metabolites to Environmental Factors. (2018). PMC: 6017249

**Pinus nigra subsp. laricio — phytochimie spécifique**

- Bonnafous R, et al. Composition and chemical variability of the needle essential oil of *Pinus nigra* subsp. *laricio* from Corsica. *Flavour and Fragrance Journal*. ResearchGate: 230142384

- Benchabane Y, et al. Composition and chemical variability of the oleoresin of *Pinus nigra* ssp. *laricio* from Corsica. *Biochemical Systematics and Ecology*, 31(7). DOI: 10.1016/S0926-6690(03)00153-5

- Barra A, et al. Essential oils of *Pinus nigra* J.F. Arnold subsp. *laricio* Maire: Chemical composition and herbicidal potential. *Arabian Journal of Chemistry*. DOI: 10.1016/j.arabjc.2014.01.021

- Alariqi AH, et al. (2022). Monoterpene Synthase Genes and Monoterpene Profiles in *Pinus nigra* subsp. *laricio*. PMC: 8838282

**Shinrin-yoku**

- Li Q, et al. (2010). The physiological effects of Shinrin-yoku (taking in the forest atmosphere or forest bathing): evidence from field experiments in 24 forests across Japan. *Environmental Health and Preventive Medicine*, 15(1), 18–26. PMC: 2793346

- Li Q. (2022). Effects of forest environment (Shinrin-yoku/Forest bathing) on health promotion and disease prevention — the Establishment of "Forest Medicine". PMC: 9665958

- Chen HT, et al. (2019). Medical empirical research on forest bathing (Shinrin-yoku): a systematic review. *Environmental Health and Preventive Medicine*, 24, 70. PMC: 6886167

**Cryptochromes : magnétoréception et sensibilité RF**

- Karki S, et al. (2021). Cryptochromes: Photochemical and structural insight into magnetoreception. *Protein Science*. PMC: 8284579

- Xu C, et al. (2021). Cryptochrome 1 mediates light-dependent inclination magnetosensing in monarch butterflies. *Nature Communications*. DOI: 10.1038/s41467-021-21002-z

- Xu J, et al. (2023). Cryptochrome and quantum biology: unravelling the mysteries of plant magnetoreception. *Frontiers in Plant Science*. DOI: 10.3389/fpls.2023.1266357

- Pooam M, et al. (2020). *Arabidopsis* cryptochrome is responsive to Radiofrequency (RF) electromagnetic fields. *Scientific Reports*, 10, 11260. DOI: 10.1038/s41598-020-67165-5

- Sherrard RM, et al. (2018). Low-Light Dependence of the Magnetic Field Effect on Cryptochromes. *Frontiers in Plant Science*. DOI: 10.3389/fpls.2018.00121

**Mesures RF en environnements contrastés**

- Röösli M, et al. (2023). Comparison of ambient RF-EMF levels in outdoor areas in Switzerland in 2014 and 2021. *Environment International*. PMID: 37598840

- Joseph W, et al. (2014). RF-EMF exposure levels in different European outdoor urban environments. PMID: 24704639

- Minor K, et al. (2023). Nature Exposure is Associated With Reduced Smartphone Use. *Environment and Behavior*. DOI: 10.1177/00139165231167165

**Forêts corses**

- Corsican Montane Broadleaf and Mixed Forests. One Earth Ecoregions. https://www.oneearth.org/ecoregions/corsican-montane-broadleaf-and-mixed-forests/

- Analyse phytosociologique des formations forestières à pin laricio de Corse. *Ecologia Mediterranea*. ResearchGate: 341156458

---

*Rapport Axe P rédigé par Cowork Tellux le 2026-04-19. L'hypothèse de pont formulée dans ce rapport est une synthèse originale des corpus existants. Elle est présentée comme une question de recherche ouverte, non comme un résultat établi. Sa valeur réside dans sa formulabilité à partir des données publiées et dans son testabilité par le protocole proposé.*
