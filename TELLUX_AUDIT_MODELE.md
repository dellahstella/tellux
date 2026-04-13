# TELLUX — Audit de solidité du modèle

**Date :** 9 avril 2026
**Objectif :** Évaluation honnête de ce que Tellux peut et ne peut pas affirmer, par axe et par cible.

---

## A. Modèle physique

### Ce qui est défendable devant un physicien

**calcHuman (Biot-Savart).** La loi de Biot-Savart est un résultat exact de l'électromagnétisme classique. L'appliquer aux lignes HTA/HTB pour estimer le champ magnétique à distance est physiquement correct dans son principe. Les données d'entrée (tracés EDF SEI, 33 sites de production, 974 antennes ANFR avec puissances CartoRadio) sont institutionnelles. Un physicien acceptera la démarche.

**calcHeritagePiezo.** Le score piézoélectrique repose sur un enchaînement de faits établis : le quartz est piézoélectrique (fait cristallographique), le granit corse contient du quartz (fait géologique), les contraintes tectoniques sont documentées (failles BRGM). Le score final est un composite pondéré — c'est un indicateur relatif, pas une mesure absolue. C'est défendable si présenté comme tel.

**IGRF-14.** Modèle de référence international du champ géomagnétique, publié par l'IAGA. L'utiliser est un gage de sérieux. La résolution spatiale (~50 km au sol) est une limite connue.

**EMAG2v3.** Modèle crustal NOAA, résolution 3,7 km. Documenté, peer-reviewed, largement utilisé en géophysique. Limite : ne capte pas les anomalies très locales (< 4 km).

### Marges d'erreur honnêtes à communiquer

| Composante | Marge d'erreur | Source de l'incertitude |
|---|---|---|
| Courants HTA | ±50 % | Courants réels non publiés par EDF SEI, estimation sur charge nominale |
| IGRF-14 interpolation | ±50–100 nT | Résolution spatiale du modèle au sol |
| EMAG2v3 | ±3,7 km | Résolution grille satellite |
| Score piézo facteur quartz | Arbitraire (0.5) | Pas de mesure terrain du taux de quartz par site |
| Bonus faille < 3 km | Seuil choisi, non calibré | Basé sur littérature (Ghilardi 2017) mais non validé localement |
| Bonus radon < 5 km | Seuil choisi, non calibré | Corrélation mégalithes/radon (Giannoulopoulou 2022), non causale |
| RF (29 mesures ANFR) | Insuffisant pour validation locale | Couverture spatiale trop faible |
| Score global 0–10 | ±1–2 points | Cumul des incertitudes ci-dessus |

**Ratio heritage/électrique ~1:10 à 1:20.** Ce ratio reflète la physique : les champs naturels (piézo, crustal) sont de l'ordre du nanotesla à quelques dizaines de nT, tandis que les champs artificiels (lignes HTA à 50 Hz) peuvent atteindre des microteslas à distance. Le ratio est réaliste mais il n'est pas documenté explicitement dans l'interface. L'utilisateur voit deux indices séparés (0–5 chacun), ce qui est la bonne approche — mais un encart explicatif précisant que les ordres de grandeur physiques sont très différents manque. **À corriger.**

### Verdict axe A

Le modèle physique est solide dans ses fondations (lois physiques exactes, données institutionnelles). Les faiblesses sont dans les paramètres de calibration (facteur quartz, seuils faille/radon, courants HTA estimés). Ces faiblesses sont documentables et honnêtes — c'est un modèle de première approximation, pas un instrument de mesure. Le double indice séparé est une excellente décision épistémique.

---

## B. Corpus niveau A (~85 études)

### Études clés pour les associations EM

| Étude | Revue | Apport pour Tellux | Solidité |
|---|---|---|---|
| Baydiili et al. 2025 | *Water Air & Soil Pollution* (Springer) | Première quantification impact HTA sur microbiome sol (−21,8 % biomasse, −25,3 % catalase) | Forte — données chiffrées, terrain réel, peer-reviewed |
| Hermans et al. 2023 | *iScience* (Cell Press) | Diversité microbiome sol −40 % à < 100 m d'une ligne HTB, mycorhizes affectés | Forte — Cell Press, données terrain, métagénomique |
| Czerwinski et al. 2020–2023 | Multiples revues | Effets CEM sur germination et croissance végétale, méta-analyse | Modérée à forte — compilation, pas toujours même protocole |
| Favre 2011 | *Apidologie* | Abeilles : signal de détresse sous exposition RF mobile | Modérée — étude isolée, pas répliquée à large échelle, mais protocole rigoureux |
| Maffei 2014 | *Trends in Plant Science* | Champs magnétiques faibles (15–60 µT) stimulent germination et croissance racinaire | Forte — revue de synthèse dans une top-revue, mécanismes documentés |
| Mshenskaya 2023 | *Plants* | Fréquence de Schumann protège le blé de la sécheresse | Modérée — résultat intéressant mais une seule expérience, pas répliquée |
| Jayakrishna 2025 | *ACS Agric. Sci. Technol.* | 4 mécanismes convergents EF/MF sur plantes (membranes, ROS, ions, gènes) | Forte — ACS, synthèse multi-mécanismes |

### Affirmations dans l'interface qui pourraient dépasser le corpus

**Risque identifié n°1 — Recommandations culturales par score EM.** Le module agronomie recommande des cultures « résilientes » par profil EM. Or aucune étude du corpus n'a directement mesuré la résilience EM de variétés corses spécifiques (Niellucciu, Sciaccarellu, etc.). L'hypothèse H64 est formulée comme telle dans le code, mais la présentation à l'utilisateur pourrait laisser croire que c'est un fait validé. **À vérifier dans l'interface : le disclaimer H64 est-il suffisamment visible ?**

**Risque identifié n°2 — Score piézo et mycorhizes.** Le lien entre piézoélectricité du substrat et colonisation mycorhizienne est suggéré par Bishop 1981 et Maffei 2014, mais jamais mesuré directement sur granit corse. L'interface présente un « bonus faille » et un « bonus radon » comme s'ils renforçaient la vie du sol — c'est plausible mais non prouvé localement.

**Risque identifié n°3 — Les « 130 études ».** Le chiffre est impressionnant mais inclut ~35 études exploratoires (niveau B) et ~10 exclues (niveau C). Dire « fondé sur 130 études scientifiques » sans préciser la ventilation est trompeur. Le dossier candidature mentionne « 3 niveaux de crédibilité » — c'est le bon cadrage. L'interface devrait faire de même systématiquement.

### Verdict axe B

Le corpus niveau A est solide pour un projet citoyen. Les études clés (Baydiili, Hermans, Maffei, Jayakrishna) sont publiées dans des revues à comité de lecture de bon niveau. C'est suffisant pour justifier l'existence de l'outil auprès d'associations EM — à condition de ne jamais extrapoler au-delà de ce que chaque étude affirme réellement. Trois points de vigilance à corriger dans l'interface.

---

## C. Ce que Tellux peut honnêtement promettre à une association EM

### Affirmations solides (niveau A, défendables)

1. **Tellux agrège des données institutionnelles vérifiables (ANFR, IGRF-14, EMAG2v3, BRGM) sur une carte interactive gratuite.** Aucune autre plateforme ne le fait pour la Corse. C'est un fait technique, pas une interprétation.

2. **Le modèle physique distingue explicitement perturbation humaine et activité naturelle.** Le double indice 0–5 / 0–5 est une décision de conception qui évite la confusion « tout EM = danger ». C'est un apport réel au discours associatif, souvent piégé par l'amalgame naturel/artificiel.

3. **Les 8 incertitudes du modèle sont documentées dans l'interface.** Aucun outil concurrent (CartoRadio, OpenCelliD) ne publie ses limites aussi explicitement. C'est un argument de crédibilité fort.

4. **Le formulaire de contribution terrain permet le crowdsourcing citoyen avec protocole en aveugle parallèle.** Deux opérateurs indépendants, non communication pendant la mesure. C'est le standard minimum pour une donnée exploitable, et Tellux l'intègre nativement.

5. **Le corpus est structuré en 3 niveaux de crédibilité, les sources de niveau C sont explicitement exclues du modèle.** Le nettoyage avril 2026 (retrait Schauberger, Marc Henry) est un acte de rigueur qui peut être montré comme preuve de bonne foi épistémique.

### Limites à communiquer proactivement

1. **Le modèle est un comparatif relatif, pas un diagnostic absolu.** Le score Tellux d'un point donné n'a de sens que comparé à un autre point. Dire « ce lieu a un score de 3,7 » isolément ne signifie rien de cliniquement ou biologiquement interprétable. L'outil ne permet pas de conclure qu'un lieu est « dangereux » ou « sain ».

2. **Les courants HTA sont estimés, pas mesurés.** EDF SEI ne publie pas les courants réels en temps réel. Le modèle utilise des charges nominales avec ±50 % d'incertitude. Un relevé terrain avec un gaussmètre à un point donné peut diverger significativement du modèle.

3. **La couverture en mesures terrain est embryonnaire.** 29 mesures ANFR certifiées sur toute la Corse, zéro mesure citoyenne à ce stade. Le modèle repose quasi-exclusivement sur des calculs, pas sur des mesures réelles. C'est honnête à dire, et c'est exactement pourquoi le crowdsourcing est nécessaire.

---

## D. Ce qui manque par cible

### Associations EM — Prêt à envoyer ?

| Critère | État | Bloquant ? |
|---|---|---|
| Données ANFR lisibles sur carte | ✅ Opérationnel | — |
| Double indice documenté | ✅ Opérationnel | — |
| Formulaire mesure terrain | ✅ Opérationnel | — |
| Incertitudes visibles dans l'interface | ✅ Documentées | — |
| Disclaimer « pas un outil de diagnostic santé » | ✅ Présent | — |
| Ratio naturel/artificiel expliqué | ⚠️ Manque encart explicatif | Non bloquant |
| Corrections voie A (A-1, A-4, A-5, A-7) | ⚠️ En cours | Non bloquant pour démo |
| Captures HD pour dossier | ⏳ Après corrections | Non bloquant pour email |

**Verdict : PRÊT À ENVOYER** pour un premier contact par email avec lien démo. Les corrections voie A sont cosmétiques pour ce public. Le ratio heritage/électrique et les disclaimers sur H64 sont à améliorer mais pas bloquants.

### Agronomie / permaculture — Prêt à envoyer ?

| Critère | État | Bloquant ? |
|---|---|---|
| Module diagnostic parcelle opérationnel | ✅ | — |
| 9 cultures corses avec résilience EM | ✅ | — |
| Couches AOC/IGP | ✅ | — |
| Études peer-reviewed intégrées | ✅ (Baydiili, Hermans, Maffei, Jayakrishna) | — |
| Disclaimer H64 (résilience variétés locales) | ⚠️ À renforcer dans l'interface | Modéré |
| Parcelles pilotes avec mesures terrain | ❌ Zéro mesure terrain agro | Bloquant pour crédibilité |
| Validation H63 (microbiome sous HTA) | ❌ Non démarrée | Bloquant pour affirmations fortes |

**Verdict : ENVOYABLE AVEC PRÉCAUTIONS.** Le dossier agro (TELLUX_DOSSIER_AGRO_BIO.md) est bien fait. Mais tant qu'aucune mesure terrain n'est faite sur sol corse, les recommandations restent théoriques. Critère « prêt à envoyer avec confiance » : au moins 3 relevés terrain sur parcelles contrastées (H63).

### Mairies / patrimoine — Prêt à envoyer ?

| Critère | État | Bloquant ? |
|---|---|---|
| 116 sites GPS cartographiés | ✅ mais GPS à vérifier (A-1) | Modéré |
| 314 églises romanes | ✅ | — |
| Alignements Broadbent calculés | ✅ (15 alignements precomputed) | — |
| Anneaux du Cap Corse documentés | ✅ | — |
| Fiches de visite enrichies | ❌ Non démarrées (B-VISITES) | Bloquant pour communes |
| Liste des communes concernées | ⚠️ Mentionnée dans le dossier, pas générée | Non bloquant |

**Verdict : ENVOYABLE POUR DRAC ET ASSOCIATIONS PATRIMOINE.** Pour les mairies individuelles, attendre les fiches de visite (B-VISITES) — sans contenu éditorial par commune, l'outil reste abstrait pour un élu. Critère « prêt à envoyer aux mairies » : au moins 5 fiches de visite opérationnelles sur des sites phares (Cauria, Filitosa, Revincu, Bavella, Anneaux Cap Corse).

### Scientifiques / laboratoires — Prêt à envoyer ?

| Critère | État | Bloquant ? |
|---|---|---|
| Corpus 3 niveaux documenté | ✅ | — |
| Modèle physique avec incertitudes | ✅ | — |
| Code source ouvert | ✅ (MIT) | — |
| Hypothèses testables formulées | ✅ (88) | — |
| Publication scientifique | ❌ Aucune | Bloquant pour certains labos |
| Données brutes téléchargeables | ❌ Pas d'API ni d'export JSON | Bloquant pour collaboration |
| Reproductibilité du modèle | ⚠️ Code monolithique, pas de tests unitaires | Modéré |

**Verdict : ENVOYABLE POUR PREMIER CONTACT INFORMEL.** Un chercheur curieux peut tester la démo et lire le corpus. Mais pour une collaboration formelle (co-publication, ANR), il faut : (a) un article préliminaire ou un rapport technique structuré, (b) des données exportables, (c) un code auditable. Critère « prêt à proposer une collaboration » : rapport technique publié + API de données ou export JSON.

---

## E. Veille corpus — Options d'automatisation

### Option A — Veille manuelle assistée par Claude

**Protocole :** Soleil soumet une étude (DOI ou PDF) → Claude l'évalue (pertinence Tellux, qualité méthodologique, revue, année) → classement A/B/C proposé avec justification → Soleil valide → ajout au corpus avec fiche normalisée.

| Critère | Évaluation |
|---|---|
| Effort setup | 🟢 Nul — déjà possible en session Cowork |
| Effort maintenance | 🟡 ~30 min par étude soumise |
| Risque qualité | 🟢 Faible — validation humaine systématique |
| Couverture | 🔴 Faible — dépend de ce que Soleil trouve ou reçoit |
| Scalabilité | 🔴 Ne scale pas au-delà de ~5 études/mois |

**Recommandation :** C'est le protocole de base, déjà en place de facto. Le maintenir comme socle.

### Option B — Veille semi-automatique (alertes + évaluation Claude)

**Protocole :** Configurer Google Scholar Alerts sur 8–10 requêtes ciblées → résultats hebdomadaires par email → Soleil transfère le digest à Claude → Claude filtre, évalue la pertinence, propose un classement A/B/C pour chaque nouvelle étude → Soleil valide → ajout au corpus.

Requêtes Scholar suggérées :
- `"electromagnetic field" AND agriculture AND soil`
- `"power line" AND microbiome OR mycorrhiza`
- `archaeoastronomy AND Mediterranean OR Corsica`
- `piezoelectric AND megalith OR standing stone`
- `"Schumann resonance" AND plant OR crop`
- `EMF AND "honey bee" OR pollinator`
- `electroculture AND review`
- `IGRF AND geomagnetic anomaly AND heritage`

| Critère | Évaluation |
|---|---|
| Effort setup | 🟢 ~1h (configurer 8 alertes Scholar) |
| Effort maintenance | 🟢 ~15 min/semaine (forward digest, valider propositions Claude) |
| Risque qualité | 🟢 Faible — même pipeline de validation que A, mais sourcing automatisé |
| Couverture | 🟡 Bonne pour la littérature anglophone peer-reviewed |
| Scalabilité | 🟡 Suffisante pour le stade actuel (5–15 études/mois à trier) |

**Recommandation :** Adopter immédiatement. C'est le meilleur rapport effort/couverture pour un projet solo. Coût zéro, setup en 1 heure, résultats dès la première semaine.

### Option C — Veille crowdsourcée utilisateurs Tellux

**Protocole :** Interface dans l'app « Proposer une étude » → formulaire (titre, DOI, résumé, domaine) → stockage Supabase → évaluation Claude via API Anthropic → résultat affiché (pertinent/non pertinent, classement proposé) → Soleil modère et valide → étude visible dans le corpus public.

| Critère | Évaluation |
|---|---|
| Effort setup | 🔴 Élevé — formulaire UI, endpoint Supabase, intégration API Claude, modération |
| Effort maintenance | 🟡 Variable — dépend du volume de soumissions |
| Risque qualité | 🟡 Moyen — nécessite modération pour éviter les soumissions de niveau C/pseudoscience |
| Couverture | 🟢 Potentiellement la meilleure — accès aux niches (électroculture, géobiologie) |
| Scalabilité | 🟢 Scale avec la base d'utilisateurs |

**Recommandation :** Reporter à la voie B (après 200+ utilisateurs actifs). Tant que la base d'utilisateurs est < 100, l'effort d'infrastructure n'est pas justifié. Prévoir comme feature voie B, axe 3 (automatisation N8N).

### Synthèse veille

| Phase | Option | Quand |
|---|---|---|
| Immédiat | B (Scholar Alerts + Claude) | Semaine prochaine |
| Socle permanent | A (manuelle assistée) | Toujours actif |
| Voie B | C (crowdsourcée) | Après 200 utilisateurs |

---

## F. Synthèse des actions prioritaires

1. **Interface — Ajouter un encart « Ordres de grandeur » dans le popup Double Indice** expliquant que les champs naturels sont ~1000× plus faibles que les champs artificiels, et que les deux indices ne sont pas comparables en valeur absolue.
2. **Interface — Renforcer le disclaimer H64** (résilience variétés locales) dans le module agronomie pour que l'utilisateur comprenne que c'est une hypothèse en investigation.
3. **Interface — Préciser systématiquement « 85 études intégrables / 130 documentées »** au lieu de « 130 études scientifiques ».
4. **Terrain — Organiser 3 relevés sur parcelles contrastées** (zone calme, zone modérée, zone HTA) pour commencer à valider H63. C'est le critère de passage pour la cible agronomie.
5. **Veille — Configurer 8 alertes Google Scholar** cette semaine.
6. **Documentation — Produire un rapport technique structuré** (10–15 pages, format article) résumant le modèle, le corpus et les premiers résultats. C'est le sésame pour les contacts scientifiques.

---

*Ce document est un audit interne. Il n'est pas destiné à être envoyé tel quel aux partenaires, mais sert de base pour calibrer les messages de chaque dossier.*
