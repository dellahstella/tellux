# Axe R — Modélisation multi-échelles et interface humain-environnement
## Positionnement de Tellux dans l'écologie des modèles santé-environnement

**Date :** 2026-04-19
**Projet :** Tellux Corse — Cadre scientifique long terme
**Nature :** Pont conceptuel · Audit épistémique · Stratégie scientifique
**Références croisées :** Axes H, K, O, P, Q — HYPOTHESES.md — candidature CTC

---

## Résumé exécutif

Entre la physique de l'exposition (ce que Tellux cartographie) et la biologie moléculaire de la réponse adaptative (ce que les axes H, K et O documentent), il existe un vide de modélisation multi-échelles. Les modèles qui font ce pont sont soit volontairement simplistes pour être réglementairement opérationnels (LNT, ICNIRP), soit sophistiqués pour des substances chimiques mais non transposables aux expositions physiques (PBPK), soit formellement proposés mais non encore pleinement implémentés (exposome, AOP physiques).

Tellux n'est pas un constructeur de modèles. Il est un producteur de variables environnementales spatialisées — les variables d'entrée que ces modèles multi-échelles nécessitent mais ne trouvent pas. Cette contribution est modeste, précise et complémentaire. Elle a une valeur réelle à court terme (candidature CTC, études pilotes Corse) et une valeur stratégique à moyen terme (cohortes nationales, Horizon Europe).

---

## 1. Cartographie des modèles actuels — Limites de chacun

### 1.1 Modèles dose-réponse plats (LNT, ICNIRP, OEL, WHO noise)

**Principe :** Une dose unique d'une exposition unique → un risque sanitaire unique, via une fonction linéaire ou par paliers.

**Forces :** Opérationnels, reproductibles, régulièrement mis à jour, base de la protection réglementaire internationale.

**Limites reconnues dans la littérature :**

*Non-linéarité ignorée.* Le LNT postule une relation linéaire sans seuil depuis zéro pour les rayonnements ionisants. Un éditorial de 2024 dans le Journal of Nuclear Medicine intitulé "Facilitating the End of the Linear No-Threshold Model Era" documente les preuves d'une réponse non-linéaire à faible dose, notamment la réduction de l'incidence tumorale dans la gamme 0,3–0,7 Gy dans les données des survivants d'Hiroshima-Nagasaki. La NRC américaine a néanmoins maintenu le LNT en 2021 : absence de consensus alternatif opérationnel, pas invalidation scientifique du LNT à haute dose.

*Indépendance des expositions postulée.* LNT et ICNIRP traitent chaque agent séparément. Aucun modèle réglementaire ne traite la co-exposition ionisant + EM non-ionisant. L'ICNIRP reconnaît cette lacune explicitement dans ses gaps 2025 (Health Physics 2025) : "further research exploring both heat and biological impacts of 5G multi-frequencies and 5G with co-exposures should be an urgent priority."

*Homogénéité populationnelle postulée.* Les limites ICNIRP et LNT postulent une population homogène. L'ICNIRP reconnaît que "children, the elderly, and some chronically ill people possibly having lower tolerance than the rest of the population." Aucune stratification par phénotype de réparation ADN, par profil nutritionnel ou par co-exposition n'est intégrée dans les modèles réglementaires actuels.

*Temporalité simplifiée.* Dose aiguë vs dose cumulée vs débit de dose — les modèles réglementaires peinent à intégrer la temporalité fine de l'exposition chronique à faible dose.

**Conclusion :** Ces modèles sont des outils de protection, pas des outils de compréhension mécanistique. Leur simplicité est un choix, pas une erreur. Mais elle crée un écran entre protection et science.

---

### 1.2 Modèles PBPK (Physiologically Based Pharmacokinetics)

**Principe :** Modéliser comment une substance absorbée par l'organisme se distribue dans ses compartiments (sang, foie, rein, tissu adipeux...), se métabolise et s'élimine. Paramétré sur des données physiologiques mesurables (flux sanguins, volumes d'organes, cinétiques enzymatiques).

**État de l'art :** Revue bibliométrique 2024 (PMC11209072) recense 3 974 articles sur PBPK de 1996 à 2024, avec croissance rapide des applications en santé environnementale pour les polluants persistants (PCB, phtalates, bisphénol, PFAS). Reconnus par l'EPA et l'EMA pour l'évaluation du risque chimique.

**Lacune pour les expositions physiques :**

Les PBPK sont fondamentalement des modèles de transport de molécules dans des compartiments aqueux et lipidiques. Les expositions physiques (EM, ionisants, bruit) ne se transportent pas — elles pénètrent instantanément les tissus et exercent leurs effets in situ. Le concept de "compartiment" n'a pas d'équivalent pour un champ électromagnétique.

Pour les radionucléides incorporés, l'ICRP dispose de modèles biocinétiques compartimentaux (ICRP publications 66, 89, 103, 130) qui décrivent la distribution temporelle des radionucléides dans les organes — et constituent en ce sens le seul équivalent PBPK pour une "exposition physique". Mais ces modèles calculent la dose déposée, pas la réponse biologique à cette dose.

**Conclusion :** PBPK est le modèle le plus avancé pour les toxiques chimiques. Il n'est pas directement transposable aux expositions physiques. Le vide entre physique de l'exposition et biologie de la réponse n'est pas comblé par cet outil.

---

### 1.3 Adverse Outcome Pathways (AOP)

**Principe :** Cadre OCDE fondé par Ankley et al. 2010 (Environmental Toxicology and Chemistry). Un AOP articule une chaîne causale de "key events" depuis un Événement Initiateur Moléculaire (EIM / MIE) jusqu'à un Adverse Outcome (AO) en passant par des key events cellulaires, tissulaires et organiques. Base de données AOP-Wiki maintenue par l'OCDE.

**Forces :** Langage commun pour différentes disciplines, facilite la prédiction d'effets sans tests sur animaux, utilisé en toxicologie réglementaire (REACH, EPA new approach methodologies).

**Extension aux stresseurs physiques :**

Des travaux publiés dans Radiation Research montrent que le cadre AOP peut être étendu aux rayonnements ionisants. Le MIE est "dépôt d'énergie ionisante" — ce qui correspond à un concept physique, non chimique. L'OCDE a publié en octobre 2023 l'AOP #272 "Deposition of ionizing energy leading to lung cancer" avec une chaîne complète de key events.

Un article dans ALTEX (Alternatives to Animal Experimentation) identifie les "challenges" spécifiques des stresseurs non-chimiques dans le cadre AOP : "How to incorporate ionizing events type, dose rate, energy deposition, and how to account for targeting multiple macromolecules." Ces challenges concernent au premier chef les EM non-ionisants.

L'OCDE/NEA maintient un groupe de travail "Radiation and Chemical AOP Joint Topical Group (Rad/Chem AOP JTG)" dont la mission est précisément de développer des AOP pour les expositions aux rayonnements. Ce groupe travaille à la convergence entre les AOP chimiques (toxicologie) et les AOP radiation (radioprotection).

**Lacune actuelle :** Aucun AOP publié pour les champs EM non-ionisants (RF, ELF) comme stresseurs primaires. La chaîne hypothétique VGCCs → influx calcium → ROS → NF-κB → inflammation (Pall 2013) n'a pas encore été formalisée en AOP validé selon les critères OCDE.

**Ce que Tellux pourrait contribuer :** les données de cartographie Tellux fournissent la "dose d'exposition physique" au niveau territorial qui pourrait servir d'entrée à des AOP environnementaux si ces AOP étaient développés pour les EM non-ionisants.

---

### 1.4 Biologie des systèmes et réseaux de signalisation

**Principe :** Modélisation mathématique des réseaux de régulation génique, des interactomes protéiques et des voies de signalisation cellulaire. Outils : équations différentielles ordinaires, modèles stochastiques, inférence de réseau depuis données transcriptomiques.

**État de l'art :** Les outils de reconstruction de réseaux de régulation génique (GRN) ont fait des progrès majeurs avec l'avènement du single-cell RNA-seq et de l'intelligence artificielle. Des modèles de type transformeur permettent l'inférence de réseaux de régulation à l'échelle du génome (Nature npj Systems Biology 2023).

**Lien avec l'exposition environnementale :** Des études montrent que 41% des perturbations génétiques expérimentales ont un effet mesurable sur l'état transcriptionnel, avec des patterns de régulation différents selon la nature des perturbations (génétiques vs environnementales). La limite principale reste l'échelle : ces modèles sont construits à partir de cultures cellulaires ou d'organismes modèles in vitro, pas à partir de données humaines in vivo dans des contextes d'exposition environnementale chronique.

**Vide non comblé :** La connexion entre un niveau d'exposition environnementale spatialisé (par exemple : 1 μW/m² RF + 50 Bq/m³ radon, conditions Corse montagnarde) et un état de réseau de régulation génique dans des PBMCs humains n'a jamais été modélisée. Ce serait le protocole Phase 3 de Tellux (Axe O).

---

### 1.5 Exposome computationnel

**Principe :** Analyser simultanément des centaines ou milliers d'expositions et leurs associations avec des outcomes de santé, par des méthodes statistiques adaptées à la haute dimensionnalité.

**Méthodes principales :**

| Méthode | Principe | Forces | Limites |
|---------|----------|--------|---------|
| ExWAS (Patel 2010) | Test massif univarié exposition→outcome, correction FDR | Explorateur, puissant | Ignore interactions, corrélations |
| WQS regression | Mélanges, pondération par quartiles, direction contrainte | Mixture, interprétable | Direction unique (all positive) |
| BKMR | Bayésien, interactions non-linéaires, kernel | Interactions, non-linéaire | Computationnellement lourd |
| ML/XGBoost | Capture non-linéarités complexes | Prédictif | Non-causal, boîte noire |
| Repeated exposome ExWAS | Données longitudinales | Temporalité | Données rares |

**Lacune reconnue explicitement :** La revue PMC10857773 (Oxford Exposome 2024) reconnaît que "it is not possible at this time to identify biomarkers of exposure for stressors such as electromagnetic fields using biomonitoring." Cette limitation transforme les expositions physiques en données manquantes systématiques dans toutes les ExWAS actuelles — à moins d'utiliser des données spatiales externes comme celles de Tellux.

---

## 2. Le vide modélisation multi-échelles — Diagramme des six niveaux

```
NIVEAU 6 — PAYSAGE ET POPULATIONS
  Cohortes géoréférencées, landscape epidemiology, exposome territorial
  Outils : SIG, GeoJSON, rasters spatiaux, analyse spatiale
  ┆
  ┆ VIDE 2 : données spatiales EM/ionisant manquantes
  ┆ → Tellux intervient ici : couche physique territoriale
  ┆
NIVEAU 5 — OUTCOMES CLINIQUES ET ÉPIDÉMIOLOGIQUES
  Cancers, maladies cardiovasculaires, longévité, naissances
  Outils : cohortes, cas-témoins, méta-analyses (INTERPHONE, Darby, NLNR)
  ┆
  ┆ Connexion bien établie pour expositions chimiques et ionisants forts
  ┆ Connexion faible pour EM non-ionisant et faibles doses ionisantes
  ┆
NIVEAU 4 — PHYSIOLOGIE TISSULAIRE ET SYSTÉMIQUE
  Inflammation chronique, réponse adaptative au niveau organe
  Cortisol, HRV, cytokines, marqueurs cardiovasculaires
  ┆
  ┆ Partiellement opérationnel en toxicologie chronique
  ┆
NIVEAU 3 — BIOLOGIE MOLÉCULAIRE DE LA RÉPONSE
  Voies ATM/ATR/NRF2/p53, épigénétique, transcriptomique PBMC
  Jain & Das 2017, Jayasree & Nair 2020 (Kerala)
  ┆
  ┆ VIDE 1 : pont physique ↔ biologie moléculaire sous-modélisé
  ┆ Mécanismes (VGCC, RPM, ROS) documentés, AOP non formalisés
  ┆
NIVEAU 2 — PHYSICO-CHIMIE DE L'INTERACTION BIOLOGIQUE
  VGCCs et flux ioniques (Pall 2013), mécanisme paires de radicaux (RPM)
  Ionisations produisant ROS, effets cryptochrome
  ┆
NIVEAU 1 — PHYSIQUE DE L'EXPOSITION
  Biot-Savart (EM), dosimétrie ionisante, acoustique, optique
  Opérationnels, précis spatialement
  → Tellux intervient ici : cartographie physique niveau 1
```

**Les deux vides critiques :**

**Vide 1 (niveaux 1-2 → 3) :** Entre la physique de l'exposition et la biologie moléculaire de la réponse. Le pont mécanistique existe en partie (VGCCs, RPM, ROS documentés) mais n'est pas formalisé en AOP validé pour les EM non-ionisants, et la transposition à l'exposition chronique à faible niveau n'a pas été démontrée quantitativement.

**Vide 2 (niveau 5 → 6) :** Entre les outcomes cliniques épidémiologiques et l'échelle paysagère. Les cohortes existent mais sans couche EM/ionisant spatialisée. Les outils statistiques (ExWAS, BKMR) existent mais sans les données d'entrée pour les stresseurs physiques.

**Position Tellux dans ce diagramme :**
- Actif au **niveau 1** (cartographie physique de l'exposition)
- Actif au **niveau 6** (couche paysage exportable pour études épidémiologiques)
- Formule des **protocoles de pont niveaux 2-3** (AXE O : transcriptomique PBMC) sans les exécuter lui-même
- Ne prétend pas modéliser les niveaux 2 à 5

---

## 3. Précédents landscape epidemiology — Projets phares

### 3.1 Spatial epidemiology : l'héritage Elliott-Wakefield-Briggs

Elliott P, Wakefield J, Best N, Briggs DJ (eds). *Spatial Epidemiology: Methods and Applications*. Oxford University Press, 2000. Ce livre fondateur a structuré le champ en documentant l'utilisation des SIG pour mapper les variations géographiques de maladies en relation avec des variables environnementales. La discipline s'est développée pour les maladies infectieuses (épidémiologie du paysage au sens Pavlovsky) puis étendue aux maladies chroniques.

**Variables environnementales typiquement cartographiées dans landscape epidemiology :**
- Pollution de l'air (PM2.5, NO2, O3)
- Bruit routier et ferroviaire
- Verdure (NDVI)
- Chaleur urbaine
- Densité de population
- Accessibilité aux soins

**Variables absentes :** EM non-ionisant, radioactivité naturelle, anomalies géomagnétiques.

### 3.2 UK Biobank

La plus grande cohorte géoréférencée du monde (500 000 participants, géolocalisation résidentielle détaillée). Un article de 2023 dans *Journal of Exposure Science & Environmental Epidemiology* décrit la méthodologie de liaison entre géolocalisation UK Biobank et cartes environnementales spatio-temporelles, appliquée à la pollution de l'air (grilles Defra).

**Avancée cruciale :** La méthodologie est en place pour lier n'importe quelle carte raster géoréférencée à une cohorte. **Ce n'est pas l'outil qui manque — ce sont les cartes.** Une carte EM ou radon au même format que les cartes air (grille 25×25m, résolution temporelle annuelle) pourrait être intégrée directement dans le pipeline UK Biobank.

**EM dans UK Biobank :** Inexistant à ce jour. L'exposition ELF résidentielle de proximité des lignes HT est connue pour ~150,000 participants (calcul de distance, pas mesure), mais la couche RF anthropique n'existe pas.

### 3.3 CONSTANCES (Inserm, France)

Cohorte française de 200 000 volontaires adultes avec géolocalisation. Le CASD (Centre d'Accès Sécurisé aux Données) confirme que pour l'ionisant, l'exposition résidentielle est estimée par "cartes et bases de données spatiales du radon, rayonnement cosmique et terrestre" et qu'un sous-groupe de 1 000 participants a des mesures de dosimètres radon dans leur domicile.

**Portée Corse :** CONSTANCES couvre la Corse (centres d'examens de santé CPAM/Sécurité Sociale en Corse). Des participants CONSTANCES résidant en Corse pourraient être enrichis avec les couches Tellux (EM, radon IRSN, géomagnétique BRGM) — pour une analyse pilote d'association entre exposome physique corse et variables de santé CONSTANCES.

### 3.4 EPIC, SAPALDIA, E3N

- **EPIC (European Prospective Investigation into Cancer)** : cohorte multi-pays, géolocalisation partielle. Enrichissement EM non documenté.
- **SAPALDIA (Suisse)** : pollution air et fonction respiratoire, géolocalisation précise. Pionnier de la liaison données spatiales-cohorte en Europe.
- **E3N (France)** : 99 000 femmes, cancer, alimentation. Extension environnementale en développement.

**Constat général :** Aucune de ces cohortes n'intègre de couche EM RF ou géomagnétique lithologique. La couche radon est présente dans CONSTANCES à l'échelle communale (données IRSN). C'est le niveau de maturité maximal atteint pour les expositions physiques dans les cohortes françaises.

---

## 4. Identification du vide conceptuel

### Ce qui existe et fonctionne

Pour les substances chimiques (PBPK + AOP + ExWAS) :
- Physique → absorption ADME (PBPK) ✅
- ADME → réponse moléculaire (AOP) ✅ pour de nombreuses substances
- Réponse moléculaire → outcome clinique (AOP + épidémiologie) ✅
- Outcome clinique → paysage (ExWAS + cohortes géoréférencées) ✅ avec quelques lacunes

Pour les expositions physiques fortes (radiothérapie, expositions professionnelles) :
- Physique → dose d'organe (ICRP biocinétique, dosimétrie) ✅
- Dose d'organe → réponse cellulaire (radiobiologie) ✅
- Réponse cellulaire → outcome clinique (études de cohortes exposées) ✅
- Outcome → paysage (géo-épidémiologie cancer) ✅ partiellement

### Ce qui est vide

Pour les expositions physiques chroniques à faible niveau (EM non-ionisant résidentiel, faibles doses ionisantes naturelles) :
- Physique → interaction biologique cellulaire : mécanismes proposés (VGCCs, RPM) mais **AOP non formalisés** ⚠️
- Interaction cellulaire → transcriptomique chronique in vivo : **une seule étude humaine connue** (Jain 2017, Kerala) ⚠️
- Transcriptomique → outcome clinique : **non établi** ❌
- Outcome → paysage : **données physiques manquantes dans les cohortes** ❌

C'est dans ce carré vide que se situe l'ambition scientifique de Tellux à long terme.

---

## 5. Contributions Tellux dans ce paysage

### Court terme (2026–2027) — Ce que Tellux peut faire maintenant

**Couche d'entrée niveau 1 :** Tellux produit des rasters GeoJSON combinant EM RF (ANFR modélisé), ELF (PROD_ELECTRIQUE), géomagnétique (EMAG2), radon (IRSN), failles (BRGM). Ces rasters sont au format standard exportable vers SIG (QGIS, ArcGIS, R spatial).

**Protocoles clés en main (niveaux 1 → 3) :** Les protocoles des axes N, O, P fournissent des designs d'étude prêts à soumettre à des collaborateurs qui ont les capacités de biologie moléculaire.

**Argument CTC :** Tellux permet à un épidémiologiste corse d'intégrer une couche physique multi-variable dans ses modèles statistiques — ce que la carte IRSN radon seule ne permet pas. C'est la valeur ajoutée immédiate, concrète, documentable.

### Moyen terme (2028–2030) — Ce que Tellux peut alimenter

**Enrichissement CONSTANCES Corse :** Liaison des adresses CONSTANCES corses (via CASD accès sécurisé) aux couches Tellux → première ExWAS multi-stresseurs physiques sur une sous-cohorte insulaire française.

**Publication méthodologique :** Article dans *Environmental Health Perspectives* ou *International Journal of Epidemiology* décrivant la méthodologie de cartographie Tellux et sa validation sur la Corse — ouvre la porte à des citations dans des protocoles de cohorte internationaux.

**Contribution à AOP Rad/Chem OCDE :** Les données de co-exposition radon + EM de la Corse peuvent alimenter le groupe de travail OCDE/NEA sur les AOP radiation, dont l'objectif est précisément de développer des AOP pour les co-expositions.

### Long terme (2031+) — Ce que Tellux peut devenir

**Territoire pilote français pour l'exposome physique :** Si les projets European Human Exposome Network (SIRENE, EHEN successeurs) font entrer les variables EM et ionisant dans leurs protocoles, la Corse — avec son infrastructure Tellux déjà en place — serait naturellement le premier territoire français calibré pour cette dimension.

**Modèle réplicable :** Bretagne (granit armoricain, radon élevé, densification EM côtier), Massif Central (socle cristallin, radon, altitude) pourraient reproduire la méthodologie Tellux avec des adaptations régionales.

---

## 6. Limites de Tellux dans ce paysage — Honnêteté requise

**Tellux ne mesure pas directement.** Il cartographie des proxies géographiques (densité d'infrastructure, géologie, altitude). La mesure individuelle (exposimètre portable, dosimètre radon personnel) est une étape séparée, plus coûteuse, que Tellux ne prétend pas avoir réalisée.

**Tellux ne valide pas ses couches sur des outcomes sanitaires.** À ce jour, aucune étude ne démontre que les scores Tellux prédisent un outcome de santé. C'est une proposition à tester, pas un résultat. Cette honnêteté est indispensable dans les communications scientifiques.

**Résolution spatiale limitée pour certaines couches :** EMAG2v3 a une résolution de 2 arcminutes (~3 km), insuffisante pour des variations micro-locales (anomalie magnétique d'un dolmen). Les données ANFR ont une précision GPS des antennes déclarées, mais la propagation RF en terrain complexe corse est une estimation, pas une mesure.

**Pas d'AOP propre.** Tellux n'a pas la capacité de construire des modèles mécanistiques de type biologie des systèmes. Il identifie les hypothèses, formule les protocoles, et s'appuie sur les équipes partenaires pour la mise en œuvre moléculaire.

---

## 7. Scénarios de projet et positionnement stratégique

### Scénario A — CTC 2026 (court terme, voie A)

**Argument narratif central :**
> "Entre la physique de l'exposition que mesurent les physiciens et les réponses biologiques que mesurent les biologistes, il existe un vide de modélisation. Les outils existent (AOP, ExWAS, systems biology) mais ils manquent de données d'entrée pour les stresseurs physiques EM et ionisants. Tellux produit ces données d'entrée à l'échelle d'un territoire insulaire français, de manière systématique et spatialisée. C'est une infrastructure méthodologique, pas un résultat en soi."

**Format recommandé pour évaluateurs CTC :**
- Diagramme six niveaux simplifié (1 demi-page)
- Tableau "ce qui existe / ce qui manque / ce que Tellux apporte" (3 colonnes, 6 lignes)
- Référence à CONSTANCES comme partenaire naturel (faisabilité pilote Corse)

### Scénario B — ANR 2027-2028 (moyen terme)

**Appel cible :** ANR PRC (Programme de Recherche Collaborative) Santé-Environnement ou Environnement-Écosystèmes
**Partenaires structurants :**
- Inserm UMR Corse (Corte) — porteur territorial
- CONSTANCES (Inserm VilleJuif) — accès cohorte
- BRGM / IRSN — données souveraines
- CHU Ajaccio/Bastia — biobanque clinique locale

**Budget estimé :** 500 K€ – 1,5 M€ pour une étude d'enrichissement CONSTANCES Corse avec transcriptomique pilote (200 participants, 4 zones contrastées)

### Scénario C — Horizon Europe 2028-2030 (long terme)

**Appel cible :** HORIZON-HLTH-2027-01-ENVHLTH-02 "Intégrer les expositions physiques dans l'exposome humain" ou successeur
**Positionnement Tellux :** Partenaire "observatoire territorial pilote" dans un consortium coordiné par ISGlobal (HELIX/EXPANSE) ou IARC
**Valeur ajoutée de la Corse :** contrôle insulaire naturel, gradient géologique remarquable, données Tellux déjà structurées
**Contribution budgétaire Corse :** WP "Pilot territory" estimé 1–2 M€ sur un consortium 10–15 M€

---

## 8. Bibliographie

**Dose-réponse et modèles réglementaires :**
- Portess DI et al. (2007). Low-dose irradiation of non-transformed cells stimulated the selective removal of precancerous cells via intercellular induction of apoptosis. *Cancer Research*
- Hendry JH et al. (2024). Facilitating the End of the Linear No-Threshold Model Era. *Journal of Nuclear Medicine*. doi:10.2967/jnumed.124.267868
- ICNIRP (2025). Gaps in knowledge relevant to the ICNIRP guidelines. *Health Physics*. doi:10.1097/HP.0000000000001918
- PMC3834742 — Linear No-Threshold Model vs Radiation Hormesis review (2013)

**PBPK et pharmacocinétique :**
- Guo J et al. (2024). Recent Progress on PBPK Model: A Review Based on Bibliometrics. *Toxics*. PMC11209072
- ICRP Publication 130. Occupational Intakes of Radionuclides. 2015
- ICRP Publication 103. Recommendations of the ICRP. 2007

**AOP et systems biology :**
- Ankley GT et al. (2010). Adverse outcome pathways: A conceptual framework. *Environmental Toxicology and Chemistry*. doi:10.1002/etc.34
- Leist M et al. (2017). The Adverse Outcome Pathway: A Multifaceted Framework. *Toxicological Sciences*. PMC5906804
- OECD/NEA Radiation and Chemical AOP Joint Topical Group. [oecd-nea.org](https://www.oecd-nea.org/jcms/pl_89086/)
- Sleiman C et al. (2024). AOP #272: Deposition of energy leading to learning and memory impairment. *Environmental and Molecular Mutagenesis*. doi:10.1002/em.22622
- OECD (2023). AOP on deposition of energy leading to lung cancer. Series on Adverse Outcome Pathways No. 32

**Exposome computationnel :**
- Patel CJ et al. (2010). An environment-wide association study on type 2 diabetes mellitus. *PLOS Genetics*
- Tamayo-Uria I et al. (2024). Decoding the exposome: data science methodologies and implications in ExWASs. *Oxford Exposome*. PMC10857773
- Vrijheid M et al. (2014). The human early-life exposome (HELIX). *Environmental Health Perspectives*. PubMed 24610234

**Landscape epidemiology :**
- Elliott P, Wakefield J, Best N, Briggs DJ (eds). *Spatial Epidemiology: Methods and Applications*. Oxford University Press, 2000
- Beale L et al. (2008). Methodological Issues and Approaches to Spatial Epidemiology. *EHP*. PMC2516558
- Hodgson S et al. (2023). Reconstructing individual-level exposures in cohort analyses: UK Biobank example. *Journal of Exposure Science & Environmental Epidemiology*. doi:10.1038/s41370-023-00635-w

**CONSTANCES :**
- Zins M et al. (2010). The CONSTANCES cohort. *European Journal of Epidemiology*
- CASD (2024). Environment and health data from CONSTANCES cohort. [casd.eu](https://www.casd.eu/en/environnement-et-sante-des-donnees-riches-et-detaillees-provenant-de-la-cohorte-constances/)

---

*Axe R — produit pour Tellux Corse, session Cowork 2026-04-19. Document conceptuel et stratégique. Ne modifie pas les données ni les fonctions de calcul du corpus Tellux. Axe le plus méta du corpus : positionnement de Tellux dans l'écologie des modèles santé-environnement.*
