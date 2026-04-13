# Tellux Corse — Dossier partenariat
## À l'attention des associations santé environnementale et sensibilisation aux CEM
### PRIARTEM · CRIIREM · associations locales corses · collectifs citoyens

---

## Tellux en trois phrases

Tellux est une carte interactive gratuite et open-source qui permet à chacun de visualiser les sources de champs électromagnétiques autour de chez soi — antennes, lignes haute tension, géologie active — et de les croiser avec les données officielles ANFR et BRGM. L'outil identifie chaque source séparément (réseau, géologie, atmosphère) et restitue leur contribution respective en un point donné, pour rendre lisible un phénomène physique unique : le champ électromagnétique total auquel un lieu est exposé. Les habitants, les associations et les chercheurs peuvent y ajouter leurs propres mesures terrain, qui viennent enrichir une base de données partagée.

---

## Ce que Tellux apporte à votre association

### 1. Un outil de visualisation citoyenne opérationnel

974 antennes ANFR sont visualisées sur la carte, avec leur type (4G, 5G, FM, relais…), leur opérateur et leur localisation précise. Contrairement à CartoRadio, Tellux permet de les croiser simultanément avec d'autres couches : réseau haute tension EDF SEI, zones géologiques BRGM, mesures terrain déclarées par des habitants. La carte est gratuite, accessible depuis un navigateur, sans inscription ni publicité.

### 2. Un double indice transparent — perturbation réseau / activité géologique

Le modèle Tellux calcule deux indices séparés pour chaque point de la carte :

- **Indice perturbation réseau** (0–5) : antennes ANFR, lignes HTA/HTB, courants Biot-Savart
- **Indice activité géologique** (0–5) : substrat, failles BRGM, anomalies magnétiques crustales EMAG2v3

Ces deux indices identifient les sources. Le champ physique en un point, lui, est une seule grandeur : la résultante vectorielle de toutes les contributions. Les indices ne se somment pas arithmétiquement (un score de 3 + 3 ne fait pas 6, car les échelles pondèrent des facteurs différents), mais les champs sous-jacents s'additionnent bien. Un lieu où les deux indices sont élevés est un lieu où le champ total résulte de contributions multiples — c'est précisément l'information que Tellux est conçu pour révéler.

Les limites du modèle sont documentées publiquement : ±1 à 2 points sur une échelle de 0 à 10, incertitude sur les courants HTA ±50 %, résolution EMAG2v3 de 3,7 km. L'outil est un comparatif relatif (site A vs site B), pas un diagnostic absolu.

### 3. Un formulaire de contribution terrain collaboratif

Les membres de votre association peuvent ajouter leurs propres mesures depuis la carte : magnétomètre (nT), signal RF (dBm), WiFi, ELF. Chaque mesure est géolocalisée, anonyme et versée à la base commune.

Tellux distingue quatre niveaux de qualité des contributions :

| Niveau | Description | Exploitabilité |
|---|---|---|
| **A** | Protocole en aveugle parallèle : deux opérateurs mesurent le même point indépendamment, écarts comparés a posteriori | Standard scientifique citoyen — exploitable pour la validation d'hypothèses |
| **B** | CSV exporté depuis une application smartphone (ex. PhyPhox), horodaté et géolocalisé automatiquement | Données structurées, exploitables en série |
| **C** | Saisie manuelle unique depuis le formulaire Tellux | Indicatif — utile pour la couverture spatiale |
| **D** | Observation qualitative (bruit, sensation, anomalie visuelle) | Signalement — non mesurable, mais peut guider une campagne de mesure |

Ce cadre permet à chaque contributeur de situer sa mesure : un membre avec un Trifield TF2 et un partenaire de mesure peut viser le niveau A ; un citoyen avec un smartphone peut contribuer utilement au niveau B ou C. Toute contribution a de la valeur si son niveau de qualité est explicité.

### 4. Des données scientifiques récentes directement intégrées

L'étude Baydiili et al. (2025, *Water Air & Soil Pollution*, Springer) est la première à quantifier l'impact des lignes haute tension sur le microbiome du sol : **−21,8 % de biomasse microbienne** et −25,3 % d'activité catalase à proximité directe des lignes HTA. Ces résultats sont directement lisibles dans Tellux, couche HTA activée, diagnostic de site.

D'autres études sont intégrées au corpus (130 études, 3 niveaux de crédibilité documentés) : Hermans 2023 (*iScience*), Maffei 2014 (*Trends in Plant Science*), Favre 2011 (abeilles et CEM RF). Les sources de niveau C — non peer-reviewed ou non réplicables — sont explicitement exclues du modèle et des recommandations.

### 5. Open-source, sans publicité, sans revente de données

Le code source est publié sous licence MIT. Aucune donnée utilisateur n'est revendue ou transmise à un tiers. Il n'y a pas de publicité. Les données crowdsourcées sont anonymisées. Tellux ne commercialise aucune solution de protection contre les CEM et ne fait aucune promesse de santé : c'est un outil de transparence et de dialogue citoyen, pas un produit commercial.

### 6. Un outil pédagogique pour vos événements et formations

La carte peut être projetée lors de réunions publiques, utilisée en atelier de mesures terrain, ou partagée en ligne à vos membres. Elle est conçue pour un public non technique : les résultats sont affichés avec leur interprétation en français, les sources sont citées, les incertitudes sont expliquées.

### 7. Corse en cas d'usage concret

La Corse est particulièrement intéressante pour les associations CEM : déploiement 5G en zones rurales isolées sans évaluation fine des impacts cumulés, réseau HTA EDF SEI étendu sur une géologie granitique active, faible densité de mesures terrain disponibles. Tellux est le premier outil à agréger ces données sur ce territoire.

---

## Ce que nous vous demandons — et ce que nous vous proposons

Notre démarche est d'abord une demande d'expertise. Votre association a une expérience de terrain, une connaissance des enjeux CEM et une légitimité que notre outil technique n'a pas. Avant de vous proposer quoi que ce soit, nous souhaitons votre regard critique sur Tellux.

**1. Tester l'outil et nous faire un retour critique**
Accédez à la carte, activez les couches antennes et HTA, cliquez sur une zone que vous connaissez. Les données correspondent-elles à votre expérience de terrain ? Les formulations sont-elles claires ? Les limites sont-elles bien communiquées ? Un retour de 15 minutes nous est plus utile qu'une lettre de soutien.

**2. Nous aider à identifier ce qui manque**
Quelles données votre association utilise-t-elle que Tellux n'intègre pas encore ? Quels outils utilisez-vous actuellement pour visualiser les CEM ? Quels formats de restitution seraient les plus utiles pour vos adhérents ?

**3. Partager l'outil à vos membres** *(si le retour est positif)*
Diffusez le lien dans votre newsletter ou lors de vos prochaines réunions. Nous pouvons préparer un mode d'emploi simplifié de deux pages adapté à votre public.

**4. Co-organiser une session de mesures terrain** *(si la collaboration se confirme)*
Si vous avez des membres équipés (magnétomètre, Trifield TF2, smartphone avec capteur) ou souhaitez organiser une campagne de mesures sur un secteur précis, nous pouvons définir ensemble un protocole, intégrer les données dans la base Tellux et vous restituer les résultats sous forme de carte.

**5. Fournir une lettre de soutien** *(uniquement si vous estimez l'outil utile)*
Dans le cadre du dépôt de candidature à l'OEC/ADEME (juin 2026), une lettre d'une association reconnue dans le domaine CEM renforce considérablement le dossier. Mais nous ne la sollicitons qu'après votre propre évaluation de l'outil — pas avant.

---

## Contact

**Soleil — SARL Stella Canis Majoris**
Résidence Lorenzi, Chemin de Montepiano, 20200 Bastia
stelladluca@proton.me · 06 18 04 25 44

**Accès à la carte :** https://tellux.pages.dev

*Tellux Corse · Données : IGRF-14 · ANFR · BRGM · NOAA · EMAG2v3 · Supabase · Licence MIT*
