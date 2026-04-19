# Fiche de recherche — Axe B : Thérapeutiques électromagnétiques
**Date :** 2026-04-19  
**Cible :** Cartographier les preuves cliniques peer-reviewed sur l'utilisation thérapeutique des champs électromagnétiques (PEMF, TMS, tACS, stimulation gamma 40 Hz) — construction du cadre scientifique long terme Tellux v2  
**Statut :** Complet — Q1 à Q6 documentés

---

## Contexte et posture épistémique

Cette fiche est de **catégorie Axe B** : elle ne concerne pas directement le code de `calcHuman()` ou les BT_ZONES. Elle alimente le cadre de connaissance scientifique de Tellux en vue de la candidature CTC et de la version 2 du projet.

**Distinction fondamentale à maintenir tout au long :**

| Dimension | Therapeutique (Axe B) | Territorial (Tellux) |
|-----------|----------------------|---------------------|
| Intensité typique | 0.1 mT – 2 T | 0.01 – 0.5 µT (ambient) |
| Fréquences | ELF 1–100 Hz, RF pulse | 50 Hz, RF continu |
| Durée | 20–90 min/session, protocole | Exposition chronique 24h/24 |
| Contrôle | Précis, localisé, prescrit | Non contrôlé, diffus, subi |
| Preuve d'effet | Niveau 1A (RCTs) pour certains | Corrélations épidémiologiques |
| Écart d'intensité | **5 à 6 ordres de grandeur** au-dessus des niveaux ambiants |

**Ce que Tellux peut dire :** les champs EM sont actifs biologiquement à des intensités bien définies — documenter l'environnement EM d'un territoire est donc scientifiquement pertinent.  
**Ce que Tellux NE peut PAS dire :** que les champs ambiants qu'il cartographie ont des effets thérapeutiques ou délétères sur la cognition à ces niveaux d'intensité.

---

## Q1 — PEMF : fondements, approbations, mécanismes

### Historique réglementaire FDA

Le PEMF (Pulsed Electromagnetic Field therapy) bénéficie de la plus longue histoire réglementaire parmi les thérapeutiques EM non ionisantes.

- **1974–1979** : Travaux pionniers de Carl Brighton et Andrew Bassett (Columbia University) sur la guérison des fractures osseuses par stimulation électrique et EM. Études sur chiens puis essais humains.
- **1979** : Première approbation FDA pour le traitement des **pseudo-arthroses** (non-union des fractures). Taux de succès : **73–85%** pour des fractures réfractaires à la chirurgie conventionnelle.
- **2004** : Approbation FDA pour la **dépression majeure résistante** (dispositif NeuroStar, puis Magstim) — mais via le mécanisme TMS qui est distinct du PEMF bas-champ (voir Q2).
- **Depuis 2010** : Prolifération des indications off-label et des dispositifs PEMF "wellness" — forte hétérogénéité réglementaire entre l'Europe (CE Mark classe II) et les États-Unis.

### Mécanismes d'action documentés

La biophysique du PEMF est maintenant bien caractérisée au niveau cellulaire :

**1. Canaux calciques voltage-dépendants (L-type VGCC)**  
Le mécanisme primaire identifié : l'oscillation EM induit une résonance sur les canaux calciques L-type → influx Ca²⁺ intracellulaire → cascade de signalisation en aval.  
- Élévation de [Ca²⁺]i observée sous exposition aiguë et chronique à ELF-EMF (Frontiers Neuroscience 2023, PMC10590107)
- Convergence avec les mécanismes du CEMI (Axe A) : les VGCC sont au carrefour des deux axes

**2. Cascade BMP2/Wnt/mTOR/MAPK**  
- BMP2 (Bone Morphogenetic Protein 2) : surexpression documentée sous PEMF → ostéogénèse
- Wnt signaling : activation → différenciation ostéoblastique
- mTOR : régulation anabolique
- MAPK (ERK1/2) : prolifération et survie cellulaire

**3. Voie Ca/CaM → NOS → NO (Nitric Oxide)**  
- Ca²⁺ → Calmoduline (CaM) → activation NOS (NO synthase) → production de monoxyde d'azote
- NO : vasodilatateur, neuro-modulateur, anti-inflammatoire
- Explication partielle des effets anti-douleur et des effets vasculaires

**4. TGF-β1 et facteurs de croissance**  
- Stimulation PEMF → sécrétion de TGF-β1 → réparation tissulaire

### Données cliniques — méta-analyses récentes

**Arthrose (ostéoarthrite) :**
- Revue systématique + méta-analyse (2024) : 17 RCTs, **1197 patients**
- Réduction de la douleur (VAS) : **60%**
- Amélioration fonctionnelle (WOMAC) : **42%**
- Source : PMC11012419

**Épaule :**
- Méta-analyse (2024) : 4 RCTs, 252 participants
- Efficacité confirmée pour tendinopathie et douleur post-chirurgicale
- Source : PMC12088032

**Douleurs neuropathiques :**
- Efficace pour douleurs spinales et radiculaires
- Résultats limités pour neuropathies périphériques diffuses
- Source : PMC12943413

**Revue générale (2024) :**
- Source : PMC11506130

### Sources Q1

| Source | Type | Revue | Année |
|--------|------|-------|-------|
| Brighton & Bassett (FDA premarket approval) | Essais cliniques | FDA PMA | 1979 |
| PMC11012419 | Méta-analyse, 17 RCTs, 1197 pts | Int J Environ Res Public Health | 2024 |
| PMC12088032 | Méta-analyse, 4 RCTs, 252 pts | — | 2024 |
| PMC12943413 | Revue systématique | — | 2024 |
| PMC11506130 | Revue générale PEMF | — | 2024 |
| PMC10590107 | Revue ELF in vivo | Frontiers Neuroscience | 2023 |

**Niveau de confiance Q1 :** Élevé pour l'orthopédie. Moyen pour les autres indications (hétérogénéité des dispositifs, des protocoles, des intensités).

**Applicabilité Tellux :** Directe pour le cadre rhétorique — les PEMF sont des preuves que les champs EM agissent biologiquement. L'écart d'intensité avec l'ambiant territorial reste à souligner (thérapeutique : 0.1–10 mT ; Tellux territorial : 0.01–0.5 µT, soit **100× à 1000× moindre**).

---

## Q2 — TMS/rTMS : stimulation magnétique transcrânienne

### Approbations FDA (chronologie)

| Année | Indication | Dispositif/Fabricant |
|-------|-----------|---------------------|
| 2008 | **Dépression majeure** (TRD) | NeuroStar (Neuronetics) |
| 2013 | **Migraine** (traitement aigu de l'aura) | Spring TMS (Neuralieve) |
| 2017 | **TOC** (Trouble Obsessionnel Compulsif) | Deep TMS H7 coil (BrainsWay) |
| 2021 | **Dépression + anxiété** | NeuroStar + Brainsway |
| 2022 | **Arrêt tabac** (dépendance nicotine) | Deep TMS (BrainsWay) |

Source : PMC8864803 (FDA TMS milestones timeline), FDA press release OCD 2018

### Mécanismes neurophysiologiques

**Modulation de l'excitabilité corticale :**
- Haute fréquence (≥10 Hz, "rTMS HF") → augmentation excitabilité → potentialisation à long terme (LTP)
- Basse fréquence (≤1 Hz, "rTMS LF") → diminution excitabilité → dépression à long terme (LTD)
- Cible principale pour la dépression : **cortex préfrontal dorsolatéral gauche (LDLPFC)**

**Theta Burst Stimulation (TBS) :**
- Protocole condensé (3 min au lieu de 30 min)
- iTBS (intermittent TBS) : équivalent fonctionnel de la rTMS HF — excitateur
- cTBS (continuous TBS) : inhibiteur
- FDA clearance pour iTBS : 2018 (dépression)
- Nature Medicine 2023 : connectivity-guided iTBS supérieure à rTMS conventionnelle en TRD (PMC — DOI 10.1038/s41591-023-02764-z)

### Données méta-analytiques

**Efficacité en dépression (umbrella meta-analysis, Psychiatrist.com 2024) :**
- Effet rTMS vs sham : **Hedges g = 0.791** (large effect size)
- Réponse thérapeutique en TRD : **OR = 3.27** vs sham
- Rémission en TRD : **OR = 2.83** vs sham
- Source : PMC10375664

**Dose-réponse (Sabé et al. 2024, JAMA Network Open) :**
- 110 études, 4820 participants (TMS + tDCS, tous troubles confondus)
- Courbe dose-réponse en cloche pour HF-LDLPFC TRD : ED95 = **12 374 pulses**
- Courbe ascendante pour BLDLPFC : ED95 = **34 773 pulses**
- Implication : il existe une dose optimale — au-delà, l'effet ne croît plus
- Source : JAMA Network Open 2024;7(5):e2412616

**Theta burst pour dépression résistante (méta-analyse Molecular Psychiatry 2024) :**
- Source : PMC11609094

### Sources Q2

| Source | Type | Revue | Année |
|--------|------|-------|-------|
| PMC10377201 | Regulatory review TMS psychiatry | J Clin Med | 2023 |
| PMC8864803 | FDA TMS timeline | PLOS ONE | 2022 |
| PMC10375664 | Méta-analyse TRD rTMS | BMC Psychiatry | 2023 |
| JAMA Network Open 2024;7(5):e2412616 (Sabé) | Dose-response meta-analysis | JAMA Network Open | 2024 |
| Nature Medicine DOI:10.1038/s41591-023-02764-z | RCT connectivity-guided iTBS | Nature Medicine | 2023 |
| PMC11609094 | Méta-analyse theta burst | Molecular Psychiatry | 2024 |

**Niveau de confiance Q2 :** Très élevé pour la dépression (preuves de niveau 1A, FDA clearance). Élevé pour TOC et migraine. En développement pour les autres indications.

**Applicabilité Tellux :** Le TMS est un exemple paradigmatique de l'action biologique des champs EM sur le cerveau, à des intensités mesurables et contrôlées (champ à la surface du cortex : **~1–2 T** pendant les pulses). L'écart avec les champs ambiants est ici extrême — le TMS opère à des niveaux **10⁸ fois supérieurs** aux champs ambiants Tellux. L'argument n'est pas que Tellux opère comme le TMS, mais que les champs EM sont réels et biologiquement actifs — ce qui justifie leur cartographie.

---

## Q3 — tACS et stimulation gamma 40 Hz

### Principe de la tACS

La tACS (transcranial Alternating Current Stimulation) diffère de la tDCS (courant continu) :
- **tDCS** : courant continu → polarisation membranaire → modulation tonique de l'excitabilité
- **tACS** : courant alternatif à fréquence spécifique → **entraînement des oscillations neuronales** à la fréquence appliquée
- La tACS à 40 Hz entraine les oscillations **gamma** cérébrales

### Mécanismes de la tACS 40 Hz en pathologie neurodégénérative

**Restauration des oscillations gamma :**
Dans la maladie d'Alzheimer, les oscillations gamma (30–80 Hz) sont réduites en amplitude et en cohérence. La tACS à 40 Hz :
1. Synchronise les **interneurones parvalbuminergiques** (PV interneurons) → restoration du balance E/I (excitation/inhibition)
2. Réduit la **neuroinflammation** (activation microgliale aberrante)
3. Améliore la **perfusion cérébrale** et le métabolisme
4. Facilite la **réduction de formation d'oligomères** amyloïdes
Source : PMC11210106 (Translational Neurodegeneration 2024)

**Mécanisme synaptique proposé :**
- tACS module la probabilité de libération de glutamate pré-synaptique
- Modifie l'efficacité des récepteurs post-synaptiques (AMPA, NMDA)
- Améliore la communication entre neurones excitateurs

### Essai clinique TRANSFORM-AD

- Design : RCT contrôlé sham, croisé
- Population : patients avec MA légère
- Protocole : 30 sessions de 60 minutes sur 15 jours consécutifs — 40 Hz tACS vs sham
- Résultats : résultats prometteurs sur cognition et mémoire (détails complets : PMC11395938)
- Sources : PMC7158579 (protocole), PMC11395938 (résultats)

**Méta-analyse tACS cognition (2023) :**
- Populations MCI/MA légère
- Effets cognitifs et mnésiques positifs
- Source : PMC10862495

**RCT crossover double-aveugle (2025) :**
- 40 Hz tACS + exercices cognitifs pour démence
- PMC12029112

### Sources Q3

| Source | Type | Revue | Année |
|--------|------|-------|-------|
| PMC11210106 | Revue tACS Alzheimer | Translational Neurodegeneration | 2024 |
| PMC11395938 | RCT TRANSFORM-AD résultats | Alzheimer's Research & Therapy | 2024 |
| PMC7158579 | TRANSFORM-AD protocole | — | 2020 |
| PMC10862495 | Revue littérature tACS MCI/MA | — | 2023 |
| PMC12029112 | RCT tACS + cognition | — | 2025 |

**Niveau de confiance Q3 :** Moyen-élevé pour les mécanismes (bien documentés in vitro et in vivo animal). Moyen pour les effets cliniques humains (essais encore en cours, effectifs limités). En croissance rapide.

**Applicabilité Tellux :** La tACS illustre que la **fréquence** spécifique est aussi importante que l'intensité. Le fait que 40 Hz soit une fréquence naturelle du cerveau (oscillations gamma endogènes) et que la tACS à cette fréquence ait des effets cognitifs documentés ouvre la question — sans y répondre — de ce que font les champs oscillants à d'autres fréquences sur les oscillations cérébrales. Fréquence de la résonance de Schumann (~7.83 Hz) = theta cérébral. Ce pont est épistémiquement légitime mais reste exploratoire.

---

## Q4 — GENUS / Tsai MIT / Cognito Therapeutics

### Le protocole GENUS

**GENUS = Gamma ENtrainment Using Sensory stimuli**  
Laboratoire Li-Huei Tsai — Picower Institute for Learning and Memory, MIT

Contrairement à la tACS (courant électrique transcrânien), le GENUS utilise des **stimuli sensoriels non-invasifs** pour entraîner les oscillations gamma :
- **Stimulation visuelle** : lumière scintillante à 40 Hz (LED flickering)
- **Stimulation auditive** : sons cliquetants à 40 Hz
- **Combinaison audiovisuelle** : synergique, plus efficace que chaque modalité seule

### Résultats précliniques (souris modèle Alzheimer)

Premiers résultats publiés *Nature* 2016 (Tsai et al.) :
- Réduction significative des plaques amyloïdes après 1 heure de stimulation visuelle 40 Hz
- Mécanisme : activation microgliale → phagocytose accrue des dépôts amyloïdes

### Essais cliniques humains

**Phase II (Cognito Therapeutics / MIT collaboration) :**
- Résultat principal : **ralentissement de l'atrophie cérébrale** et améliorations cognitives vs contrôles non-traités
- Durée : plusieurs semaines à mois

**Étude d'extension ouverte (2024-2025) :**
- 2 ans de stimulation audiovisuelle 40 Hz quotidienne
- Sécurité : confirmée, faisabilité : bonne
- **Réduction du pTau217** (biomarqueur phosphorylé corrélé à la pathologie Alzheimer) chez 2 patients MA à début tardif
- Résultats négatifs chez 2 patients MA à début précoce (hétérogénéité des profils)
- Source : PMC12552893 ; MIT News novembre 2025

**Phase III (Cognito Therapeutics, en cours 2025) :**
- Essai national multicentrique aux États-Unis
- Encore actif au moment de la rédaction (avril 2026)

**Expansion vers la prévention :**
- MIT Aging Brain Initiative : recrutement de sujets 55+ cognitivement normaux avec antécédents familiaux d'Alzheimer
- Question : la stimulation GENUS avant apparition de la maladie a-t-elle un effet préventif ?

### Bilan MIT News mars 2025

"Evidence that 40Hz gamma stimulation promotes brain health is expanding" (MIT News 2025-03-03) :
- Les mécanismes se précisent : neuroinflammation, lymphatiques cérébraux, sommeil
- La stimulation GENUS augmente l'activité du système lymphatique cérébral pendant le sommeil → meilleure élimination des déchets métaboliques

### Sources Q4

| Source | Type | Revue | Année |
|--------|------|-------|-------|
| PMC12552893 | Extension ouverte GENUS 2 ans | — | 2024-2025 |
| MIT News 2025-11 | Communiqué Picower Institute | MIT | 2025 |
| MIT News 2025-03 | Revue preuves gamma brain health | MIT | 2025 |
| Tsai et al. 2016 | Article fondateur GENUS | Nature | 2016 |

**Niveau de confiance Q4 :** Élevé pour les mécanismes précliniques. Moyen pour l'efficacité clinique (effectifs phase II petits, phase III encore en cours). Potentiel thérapeutique fort mais non encore démontré en niveau 1A.

**Applicabilité Tellux :** Le programme GENUS est l'exemple le plus médiatisé de l'idée que l'environnement EM à fréquences spécifiques peut moduler l'état cérébral. Il valide la légitimité scientifique de la question — sans la transférer directement à l'ambiant territorial.

---

## Q5 — Critique du corpus : placebo, hétérogénéité, variabilité individuelle

### Le problème du placebo en neuromodulation

La neuromodulation électromagnétique est particulièrement exposée aux effets placebo pour plusieurs raisons :
1. **Somatic cues** : certains dispositifs TMS créent des sensations physiques (bruit, sensation de picotement) difficiles à masquer avec un sham parfait
2. **Expectation effects** : les patients avec TRD ont souvent de fortes attentes ; l'espoir d'un traitement "high-tech" amplifie la réponse

**Nature Mental Health 2023 (méta-analyse 27 ans) :**
- Placebo response en TMS dépression : **d = 1.016** (très large)
- La réponse placebo **augmente chaque année** dans les essais
- La réponse active augmente en parallèle — ratio actif/placebo reste relativement stable
- Implication : les essais cliniques de TMS mesurent de plus en plus un effet "soin + technique" difficile à décomposer

**Schizophrénie (hallucinations auditives) :**
- Hétérogénéité I² = **94%** pour les études rTMS vs sham
- Pas de différence significative entre actif et sham dans certaines méta-analyses

**Symptômes négatifs schizophrénie :**
- Placebo g = **0.44** (significatif) avec I² = 43%

### Hétérogénéité structurelle du corpus

Les méta-analyses TMS/PEMF sont systématiquement affectées par :

| Source d'hétérogénéité | Détail |
|------------------------|--------|
| **Protocoles** | Fréquence (1 Hz vs 10 Hz vs TBS), intensité (% MT), nombre de pulses, durée totale |
| **Cibles** | LDLPFC gauche, BDLPFC bilatéral, M1, cibles individualisées par IRM fonctionnelle |
| **Populations** | Âge, sévérité, durée de la maladie, traitements concurrent |
| **Dispositifs** | Bobines plates vs H-coil (BrainsWay) vs figure-8 |
| **Sham** | Bobine déviée, shield passif, résistances d'impédance — aucun gold standard |
| **Financement** | Industrie vs académique → biais de publication documenté |

### Variabilité individuelle de réponse

- Certains patients répondent remarquablement bien au TMS (>50% amélioration durable)
- D'autres ne répondent pas du tout — même au-delà du sham
- Les marqueurs prédictifs de réponse font l'objet de recherches actives (connectivité DLPFC-cortex subgénual)

### Dose-réponse : une avancée méthodologique (Sabé 2024)

La méta-analyse dose-réponse de Sabé et al. (2024) représente une avancée méthodologique importante :
- Dépasse le binaire "actif vs sham" pour modéliser la relation dose-effet
- Courbes en cloche : trop peu de pulses = inefficace ; trop de pulses = diminution d'effet (LTD-like ?)
- Ouvre la voie à une médecine de précision TMS personnalisée

### Sources Q5

| Source | Type | Revue | Année |
|--------|------|-------|-------|
| Nature Mental Health 2023 | Méta-analyse placebo TMS 27 ans | Nature Mental Health | 2023 |
| PMC4753589 | Placebo rTMS hallucinations schizophrénie | — | 2016 |
| JAMA Network Open 2024;7(5):e2412616 (Sabé) | Dose-réponse | JAMA Network Open | 2024 |
| Frontiers Psychiatry 2024 PMC — placebo rTMS schizophrénie | Méta-analyse | Frontiers Psychiatry | 2024 |

**Niveau de confiance Q5 :** Élevé — la critique du corpus est elle-même bien documentée.

**Applicabilité Tellux :** Cette section est un garde-fou. Tellux doit s'appuyer sur les preuves les plus solides (niveau 1A avec sham adéquat) et ne pas sur-interpréter les études à fort effet placebo. La dépression TRD (OR=3.27 vs sham) reste valide malgré le bruit. L'arthrose PEMF (17 RCTs, 60% réduction VAS) aussi.

---

## Q6 — La frontière : thérapeutique vs ambiant territorial

### L'écart d'intensité est fondamental

| Type de champ | Intensité typique | Fréquence |
|---------------|-------------------|-----------|
| PEMF orthopédique | 0.1 – 10 mT (100 – 10 000 µT) | 1 – 100 Hz |
| TMS (pulse) | 1 – 2 T (= 10⁶ µT) | ~3000 Hz bref |
| tACS | ~1–2 mA → ~0.5 mV/mm intracortical | 10 – 80 Hz |
| GENUS (indirect, sensoriel) | < 0.001 µT (stimulation lumineuse, pas EM direct) | 40 Hz |
| **Champ ambiant urbain (Tellux)** | **0.01 – 0.5 µT** | 50 Hz + RF |
| Recommandation ANSES précautionnelle | < 0.4 µT (leucémies infantiles, ELF) | 50 Hz |

L'écart entre PEMF thérapeutique et ambiant territorial est de **3 à 6 ordres de grandeur** (×1000 à ×1 000 000).

### Ce que dit la recherche sur l'exposition chronique basse intensité

**Études in vivo animales (50 Hz ELF, intensités proches de l'ambiant) :**
- LC-NA system "set-point" : 21 jours à 0.1 mT 50 Hz → modifications de l'activité du locus coeruleus-noradrénaline chez le rat (ScienceDirect 2024). **Note : 0.1 mT = 100 µT, soit encore 200× au-dessus de l'ambiant urbain Tellux.**
- Effets reproductifs à 1.2 mT 50 Hz chez souris gravides (poids fœtal, taux de naissance) — cette intensité est **1000–12 000× au-dessus des niveaux ambiants**
- Source : Frontiers Neuroscience PMC10590107 (revue systématique 2023)

**Études épidémiologiques occupationnelles :**
- 132 travailleurs centrales électriques (exposés) vs 143 témoins
- Exposition chronique ELF-EMF → association avec dépression, anxiété, mauvaise qualité de sommeil (PubMed PMID:30547710)
- **Niveau d'exposition occupationnelle : plusieurs µT** — encore au-dessus des niveaux résidentiels

**Conclusions réglementaires (ANSES/OMS) :**
> "ELF-EMFs surrounding occupational and living environments are only several µT or <0.1 µT, giving confidence that biological health would not be harmed by ELF-EMFs in surroundings from power transmission lines, electrical appliances, base stations, mobile phones, etc."
- Source : Frontiers Neuroscience 2023 (PMC10590107) — citation des conclusions ANSES/OMS

**Seuil précautionnel 0.4 µT (ANSES 2010) :**
- Basé sur méta-analyses épidémiologiques leucémies infantiles (OR ≈ 2.0 pour exposition >0.4 µT prolongée)
- Ce seuil est **indicatif, pas réglementaire** — il identifie une zone de vigilance, non une certitude de risque
- Les zones Tellux les plus exposées (centre Bastia, axe A193) pourraient atteindre ce seuil près d'équipements HTA/HTB — mais c'est déjà modélisé dans `calcHuman()` via Biot-Savart

### Champs RF : études de stimulation transcrânienne vs ambiant

**tACS (courant alternatif transcrânien) :**
- L'intensité intracorticale effective de 0.5 mV/mm est **suffisante pour entraîner des oscillations neuronales**
- Les champs ambiants RF atteignent au maximum quelques mV/m (= 0.001–0.01 mV/cm dans les tissus) → **2 à 3 ordres de grandeur en dessous du seuil tACS**

**Conclusion sur la frontière :**
- Les études cliniques TMS/PEMF/tACS démontrent la biologie-activité des champs EM
- Elles ne permettent PAS de conclure à des effets à des intensités ambiantes
- La zone grise épistémique concerne les **expositions chroniques cumulatives** à faible intensité, pour lesquelles les mécanismes comme les VGCC pourraient opérer à des niveaux plus bas que les seuils aigus
- C'est précisément dans cette zone grise que Tellux s'inscrit — non pas comme réponse mais comme **infrastructure de mesure**

### Sources Q6

| Source | Type | Revue | Année |
|--------|------|-------|-------|
| PMC10590107 | Revue in vivo ELF effets système | Frontiers Neuroscience | 2023 |
| PMID:30547710 | Étude occupationnelle exposition ELF | — | 2019 |
| ScienceDirect 2024 DOI:10.1016/j.brainres.2024 | LC-NA set-point 50 Hz | Brain Research | 2024 |
| ANSES avis 2010 (ELF, seuil 0.4 µT) | Avis réglementaire | ANSES | 2010 |
| Frontiers Neuroscience PMC11298025 | Effets RF et ELF sur SNC | Front Neurosci | 2024 |

**Niveau de confiance Q6 :** Élevé pour l'écart d'intensité (physique, incontestable). Moyen pour les effets à faible intensité chronique (études animales à intensités encore supérieures à l'ambiant). Bas pour l'extrapolation directe aux niveaux territoriaux Tellux.

---

## Synthèse exécutive

### Tableau récapitulatif Axe B

| Thérapeutique | FDA/CE | Mécanisme principal | Niveau preuve | Intensité (vs ambiant Tellux) |
|---------------|--------|--------------------|--------------|-----------------------------|
| PEMF os | FDA 1979 | VGCC → Ca²⁺ → BMP2/Wnt | 1A (RCTs) | 100–10 000 µT (×200 à ×20 000) |
| PEMF arthrose | Off-label | Ca/CaM → NO | 1A (méta) | 100–10 000 µT |
| rTMS dépression | FDA 2008 | LTP/LTD DLPFC | 1A | ~10⁶ µT (pulse) |
| rTMS OCD | FDA 2017 | H-coil deep TMS | 1B | ~10⁶ µT (pulse) |
| iTBS dépression | FDA 2018 | LTP condensée | 1A | ~10⁶ µT (pulse) |
| tACS 40 Hz MA | Phase III | Gamma PV interneurons | 2A | 1–100 µT |
| GENUS audiovisuel | Phase III | Sensoriel → gamma endogène | 2A | Indirect (< 0.001 µT EM direct) |

### Formulation défendable pour le document Tellux v2

> "Un corpus clinique établi démontre que les champs électromagnétiques pulsés (PEMF) et la stimulation magnétique transcrânienne (TMS) ont des effets biologiques documentés et des applications thérapeutiques approuvées par les autorités réglementaires (FDA, CE). Ces effets sont obtenus à des intensités comprises entre 100 µT et 2 T — soit deux à six ordres de grandeur au-dessus des niveaux ambiants que cartographie Tellux dans l'environnement territorial corse. Les recherches sur la stimulation gamma à 40 Hz (programme GENUS, MIT-Tsai) illustrent la spécificité fréquentielle de l'interaction champs EM – cerveau. Tellux s'inscrit dans ce contexte en fournissant la cartographie fine de l'environnement électromagnétique du territoire, condition première d'une recherche épidémiologique rigoureuse sur les effets éventuels de l'exposition chronique à faible intensité."

### Ce que Tellux PEUT et NE PEUT PAS dire

**✅ Peut dire :**
- "Les champs EM sont biologiquement actifs à des intensités mesurables"
- "Des thérapeutiques approuvées exploitent ce principe (PEMF, TMS)"
- "La cartographie de l'environnement EM territorial est une infrastructure scientifique pertinente"
- "La question des effets à faible intensité chronique reste ouverte et activement étudiée"

**❌ Ne peut pas dire :**
- "Les antennes ANFR cartographiées par Tellux ont des effets sur la cognition"
- "Les zones rouges du score Tellux présentent un risque sanitaire démontré"
- "Les champs ambiants ont des effets thérapeutiques ou délétères aux intensités mesurées"
- "Tellux mesure l'exposition au sens médical/réglementaire"

---

## Décisions code (différées — non urgentes pour la candidature CTC)

Ces éléments n'ont pas d'impact immédiat sur le code `tellux_FINAL_CLEAN1.html` mais informent les choix futurs :

1. **Seuil 0.4 µT (400 nT) ANSES** : peut être utilisé comme breakpoint dans `normalizeToLevel()` pour calibrer le niveau "Modéré/Élevé" en ELF. Ce n'est pas un seuil réglementaire mais une valeur de vigilance documentée. À ajouter au code comment de Zone 4.

2. **Commentaire code général** (à ajouter dans `calcAll()`) :
```javascript
// NOTE ÉPISTÉMIQUE — Cadre thérapeutique vs territorial :
// Les thérapeutiques EM validées (PEMF FDA 1979, TMS FDA 2008) opèrent à
// 100 µT – 2 T, soit 200 à 4 000 000× au-dessus des niveaux ambiants Tellux.
// Le score Tellux est un indicateur d'exposition territoriale, non un indicateur
// de risque sanitaire démontré. Seuil de vigilance documenté ANSES : 0.4 µT (400 nT)
// pour ELF 50 Hz (leucémies infantiles, méta-analyses épidémiologiques).
// Sources : ANSES 2010, OMS EHC 238, PMC10590107.
```

3. **Interface utilisateur** : envisager un disclaimer clair dans le popup principal de la carte, distinguant "niveau EM mesuré" et "risque sanitaire".

---

## Bibliographie complète Axe B

### PEMF
- Brighton, C.T. & Bassett, C.A.L. (1979). FDA Premarket Approval (PMA) P790002 — Electrical bone stimulation for fracture non-union. FDA.
- PMC11012419 — PEMF osteoarthritis meta-analysis, 17 RCTs, 1197 patients (2024)
- PMC12088032 — PEMF shoulder, 4 RCTs, 252 participants (2024)
- PMC12943413 — PEMF neuropathic pain systematic review (2024)
- PMC11506130 — PEMF general review (2024)

### TMS/rTMS
- PMC10377201 — Regulatory clearance TMS psychiatric disorders (2023). J Clin Med.
- PMC8864803 — FDA TMS milestones timeline (2022). PLOS ONE.
- PMC10375664 — rTMS adjunctive MDD meta-analysis (2023). BMC Psychiatry.
- Sabé M. et al. (2024). Transcranial Magnetic Stimulation and Transcranial Direct Current Stimulation Across Mental Disorders: A Systematic Review and Dose-Response Meta-Analysis. *JAMA Network Open*, 7(5):e2412616.
- Bhatt P. et al. (2024). Connectivity-guided iTBS vs rTMS TRD. *Nature Medicine*. DOI:10.1038/s41591-023-02764-z
- PMC11609094 — Theta burst depression Molecular Psychiatry meta-analysis (2024)

### tACS / Gamma
- PMC11210106 — tACS 40 Hz Alzheimer review. *Translational Neurodegeneration* (2024)
- PMC11395938 — TRANSFORM-AD results. *Alzheimer's Research & Therapy* (2024)
- PMC7158579 — TRANSFORM-AD protocol (2020)
- PMC10862495 — tACS cognitive effects MCI/MA review (2023)
- PMC12029112 — RCT 40 Hz tACS + cognitive exercises (2025)

### GENUS / MIT-Tsai
- PMC12552893 — GENUS open-label extension 2 years (2024-2025)
- MIT News 2025-11-14 — "40Hz sensory stimulation may benefit Alzheimer's patients for years"
- MIT News 2025-03-03 — "Evidence 40Hz gamma stimulation promotes brain health expanding"
- Iaccarino H.F. et al. (2016). Gamma frequency entrainment attenuates amyloid load and modifies microglia. *Nature*, 540, 230–235.

### Placebo / Critique
- Brunoni A.R. et al. (2023). Growing placebo response in TMS treatment for depression. *Nature Mental Health*.
- PMC4753589 — Placebo rTMS hallucinations schizophrenia (2016)
- Sabé M. et al. (2024). Dose-response meta-analysis. JAMA Network Open.

### ELF ambiant / Frontière
- PMC10590107 — ELF in vivo effects review. *Frontiers Neuroscience* (2023)
- PMC11298025 — RF and ELF effects on CNS. *Frontiers Neuroscience* (2024)
- PMID:30547710 — Chronic ELF occupational exposure, sleep/mood (2019)
- ScienceDirect 2024 — LC-NA set-point 50 Hz ELF, *Brain Research* (2024)
- ANSES. (2010). Avis relatif aux effets sanitaires des champs électromagnétiques d'extrêmement basse fréquence. ANSES.
- OMS. (2007). *Environmental Health Criteria 238 — Extremely Low Frequency Fields*. WHO.

---

## Note épistémique générale — Axe B

L'Axe B permet à Tellux de s'inscrire dans un contexte scientifique où les champs EM sont pris au sérieux par la médecine (FDA, CE, RCTs de niveau 1A). Cette légitimité ne se transfère pas automatiquement aux niveaux ambiants — **mais elle justifie de les mesurer**.

La formulation la plus rigoureuse pour Tellux est celle de l'**infrastructure épistémique** : avant de répondre à la question "les champs ambiants ont-ils des effets à ces niveaux ?", il faut disposer d'une cartographie fine de ces champs. C'est exactement ce que fait Tellux. Les Axes A et B construisent la crédibilité scientifique du projet sans outrepasser les limites de la preuve disponible.

**Cohérence interne des trois axes Tellux :**

| Axe | Question | Niveau de preuve actuel | Rôle de Tellux |
|-----|----------|------------------------|----------------|
| Axe A | Champs EM endogènes et conscience | Débattu, cadre établi | Cadre conceptuel |
| Axe B | Champs EM comme thérapeutiques | Prouvé à intensité élevée | Légitimation scientifique |
| Score Tellux | Cartographie EM territoriale | Infrastructure de mesure | Outil de recherche |

Le score Tellux est une donnée, pas une conclusion. C'est sa force scientifique et sa protection juridique.

---

*Recherche effectuée le 2026-04-19 — Sources : PubMed/PMC, JAMA Network, Nature, MIT News, FDA.gov*  
*Rédaction : Cowork / Soleil (Tellux Corse, SARL Stella Canis Majoris)*
