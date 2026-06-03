# RAPPORT FINAL — Chantier recherche « État de l'art défendable : électroculture »

> **Date de clôture** : 2026-06-03
> **Référentiel** : `contrat.md` + `CHARTE_AGRONOMIE.md` + `PROTOCOLE_AUTO_ITERATION.md` §5.3
> **Statut boucle** : **CLOSE MÉTHODOLOGIQUEMENT** au seuil de réussite 7.0/10
> **En attente** : arbitrage Soleil sur la justesse de fond + 5 conditions post-boucle (§4)

---

## 1. Trajectoire de la boucle

Quatre itérations générateur (Cowork, session « générateur ») + trois cycles évaluateur (Cowork, session « évaluateur »), conformément à `PROTOCOLE_AUTO_ITERATION.md` §2 (séparation stricte).

| Cycle | Générateur | Évaluateur | Score | Δ |
|---|---|---|---|---|
| 1 | `SYNTHESE.md` itération 001 | `feedback-001.md` | 6.33 / 10 | — |
| 2 | itération 003 (002 fusionnée) | `feedback-002.md` | 6.85 / 10 | +0.52 |
| 3 | itération 004 | `feedback-003.md` | **7.40 / 10** | +0.55 |

**Δ cumulé 001 → 004 = +1.07.** Pas de plateau, pas d'escalade max-itérations (4 < 6). Seuil 7.0 atteint au cycle 3.

---

## 2. Verdict scientifique défendable (à arbitrer par Soleil)

### 2.1 Synthèse de la position

Le mot « électroculture » regroupe en réalité **plusieurs familles techniques très distinctes** (A1, A2, B, C, D, E, F, G — typologie §1 de `SYNTHESE.md`). Confondre ces familles est le levier rhétorique principal du discours grand public.

| Famille | Niveau de preuve (2026) | Position défendable Tellux |
|---|---|---|
| **A1 — Antenne cuivre seule (TikTok)** | Faible à nul (Chier et al. 2025, USDA 1926, mécanisme atmosphérique non plausible Rycroft et al. 2008) | À ne pas recommander, à exposer publiquement comme objet de réfutation |
| **A2 — Composite Cu/Zn (Christofleau)** | Non testée sérieusement par la littérature peer-reviewed récente ; lacune Bull. 1379 à auditer ; objection hormèse §12.4 affaiblit l'analogie | Objet de test contrôlé légitime, sous protocole §7, **après audit USDA Bull. 1379** |
| **B — Stimulation électrique active au sol** | Mixte, hétérogène, transposition champ non démontrée | Recherche académique légitime, pas un outil de production |
| **C — Magnetopriming** | Modéré avec hétérogénéité (Tapia-Belmonte 2023) ; étude négative Spendier 2018 explicite | Candidat de premier test prioritaire en Phase 1 protocole §7, **pas une recommandation produit** |
| **D — HVEF semences** | Émergent positif (Sun 2024, Lu 2025), pas de méta-analyse | À surveiller, partenariat académique |
| **E — eSoil PEDOT** | Une étude PNAS 2023 non répliquée à 2026 | Résultat prometteur isolé, à observer |
| **F — Foudre/orage** | Établi physico-chimie atmosphérique, **sans rapport** avec dispositif d'électroculture | À neutraliser explicitement dans toute communication |
| **G — Plasma seed treatment** | Peer-reviewed substantielle (Mildaziene/Ivankov/Sera 2022, Leti et al. 2022) | Légitime mais inaccessible déploiement Tellux court terme, partenariat académique |

**Conclusion défendable** : la littérature ne soutient **pas** l'usage de l'électroculture grand public comme outil agronomique. Elle soutient au mieux la **poursuite d'investigations contrôlées** sur des dispositifs spécifiques (A2 composite, C magnetopriming en premier lieu), dans un cadre de recherche encadré, avec témoin sham, pré-enregistrement, publication des résultats négatifs.

### 2.2 Innovation Tellux défendable FEDER

L'**innovation n'est pas l'électroculture**. Elle est dans le **couplage** :

> donnée environnementale corse (EM ANFR + RF + magnétique + géologie BRGM + microclimat + pédologie) × aide à la décision agronomique terrain × collecte structurée d'observations à grande échelle (science participative encadrée § Phase 1 → Phase 2 → Phase 3)

L'électroculture est dans cette architecture **un objet de test parmi d'autres** — pas un produit phare. Tellux ne vend pas l'électroculture ; Tellux propose un dispositif de **vérification structurée d'hypothèses populaires**, capable de publier l'absence d'effet aussi bien qu'un effet validé.

---

## 3. Protocole de test contrôlé proposé (§7 de `SYNTHESE.md`)

Pour mémoire — détails complets en `SYNTHESE.md` §7.

- **Arbitrage sémantique préalable** (§7.0) : Option E (« électroculture » assumée encadrée, public-facing) vs Option S (« test contrôlé de stimulations EM », académique). **Décision Soleil à prendre.**
- **Question falsifiable** §7.1 : une seule technique, une seule culture, un seul paramètre principal.
- **Témoins** §7.2 : négatif + sham obligatoires. Randomisation. Aveuglement partiel. Pré-enregistrement OSF.
- **Puissance statistique** §7.2 : n ≥ 12 réplicats par bras pour détecter Δ = 15 % à α = 0.05 / puissance 0.80 (calculé sur CV 25-35 % observée dans Chier et al. 2025). n ≥ 25 si Δ = 10 % visé.
- **Variables** §7.3 : rendement commercialisable, masse sèche, indice de germination. Contexte : pluviométrie, températures, conductivité sol, pH, N-P-K initial, **teneur Cu et Zn pré/post** essai.
- **Durée** §7.4 : minimum 2 saisons × 2 sites contrastés.
- **Phases science participative** §7.5 : Phase 1 contrôlée → Phase 2 observation collective étiquetée génération d'hypothèses → Phase 3 retour contrôlé si signal.

---

## 4. Conditions post-boucle (TODO avant export FEDER)

Ces 5 conditions sont **hors périmètre de la boucle d'auto-itération** (qui a fait son travail méthodologique). Elles relèvent de la phase de validation externe avant tout usage du livrable dans un dossier de financement.

### 4.1 [TODO-1] Audit citations en bloc — pattern Frankenstein × 3

**Contexte** : trois itérations sur trois ont produit une citation erronée du même type (auteur réel + journal vraisemblable + URL/DOI mal couplé) :
- itération 001 : « Bilalis et al. 2018 hemp magnetopriming » → vrais auteurs **Spendier K. 2018** ([PMC vérifié](https://www.mdpi.com/2571-8800/1/1/17)). Corrigée en 003.
- itération 003 : « Mildaziene & Sera 2022 *Plants* PMC9415020 » → vrais auteurs **Leti L.I., Gerber I.C. et al. 2022** (Iași, Roumanie). Corrigée en 004.
- itération 004 : « Calabrese *Environmental Pollution* 2009 » avec URL `S0147651317308333` → URL pointe vers ***Ecotoxicology and Environmental Safety* 2017** (ISSN S0147-6513). **Non corrigée à la clôture.**

**Action** : audit systématique URL ↔ DOI ↔ titre ↔ auteurs ↔ année ↔ journal pour **chaque** référence listée en `SYNTHESE.md` §9. Effort estimé 1-2 h. Préférable en mode read-only par Code ou par un tiers (pas par le même générateur qui a produit les erreurs).

**Bloquant pour** : tout export FEDER ou tout export public du livrable.

### 4.2 [TODO-2] Lecture intégrale USDA Bulletin n° 1379 (1926)

**Contexte** : §2.1 cite Briggs et al. 1926 comme preuve massue contre famille A après 20 ans d'expérimentations. §12.1 (contre-argumentaire A2) reconnaît trois cas possibles sur la couverture exacte par USDA des dispositifs composites passifs Cu/Zn :
- (i) USDA a testé des composites Cu/Zn → verdict A2 « non testée sérieusement » est partiellement faux.
- (ii) USDA n'a testé que des configurations alimentées Lemström-style (« 50 000 V » mentionné en §12.1 mais non sourcé à la page) → A2 reste non couverte.
- (iii) Couverture intermédiaire.

**Action** : lire le scan 35 pages disponible sur [Biodiversity Heritage Library](https://www.biodiversitylibrary.org/item/131204) et [Internet Archive](https://archive.org/details/electroculture1379brig). Trancher les trois cas. Paginer la citation littérale « *does not lend assurance of great progress* » et la mention « 50 000 V » 1907. Mettre à jour §2.1, §12.1, §2.5 A2 en conséquence.

**Bloquant pour** : tout usage du §12 contre-argumentaire dans un dossier FEDER. L'évaluateur FEDER lira §2.1 + §12.1 + §2.5 ensemble et exigera le tranchage.

### 4.3 [TODO-3] Lecture intégrale Solís 2023, Ma 2024, Lonicera 2023

**Contexte** :
- §12.3 (arc famille B → A2) est honnêtement requalifié « qualitatif » tant que voltage/courant exacts de Solís 2023 (*Electrochim. Acta* 448:142193) et Ma et al. 2024 (*Sci. Hortic.* 329:112992) ne sont pas extraits à la lecture des Materials & Methods.
- §12.4 (objection hormèse) cite Lonicera japonica 2023 (*Plants* 12(4):933, [titre confirmé sur MDPI](https://www.mdpi.com/2223-7747/12/4/933) : *Hormesis Responses of Growth and Photosynthetic Characteristics in Lonicera japonica Thunb. to Cadmium Stress: Whether Electric Field Can Improve or Not?*) avec un chiffre précis « **U inversé, maximum à 2 V/cm** » non vérifié au niveau table/figure.

**Action** : lire les trois papiers, extraire voltages/courants exacts (Solís + Ma) et chiffre exact de l'optimum hormétique (Lonicera). Renforcer §12.3 (passer de qualitatif à quantitatif si la dose-réponse documentée le permet) et fixer la pagination §12.4.

**Bloquant pour** : un évaluateur scientifique rigoureux relira §12.3 et §12.4 et exigera ces chiffres.

### 4.4 [TODO-4] Pagination Lemström 1904

**Contexte** : §2.1 mentionne « +60 % céréales, +183 % carotte, inhibition fraise » avec disclaimer « pagination non consolidée ». Auto-flaggée en §10. Faible enjeu argumentatif (les chiffres sont stables d'un compilateur à l'autre), enjeu de traçabilité formelle.

**Action** : lecture du [scan archive.org](https://archive.org/details/electricity-in-agriculture-and-horticulture-lemstrom-1904), extraction des pages exactes pour les trois chiffres. Mise à jour §2.1.

**Non bloquant** pour la clôture interne, recommandé avant export externe.

### 4.5 [TODO-5] Vérification Brun et al. 2003 (Soil Use Manage., phytotoxicité Cu sols vinicoles méditerranéens)

**Contexte** : référence mentionnée dans §8 (corps) et listée en §9 dans la sous-section « Référence à vérifier avant usage en dossier FEDER ». Auteurs (Brun L. A., Le Corff J., Maillet J.) et année (~2003) plausibles mais **non confirmés par lecture primaire** dans aucune itération de la boucle.

**Action** : recherche bibliographique ciblée (Google Scholar, Web of Science, base INRAE). Si confirmée → migrer en §9 sources principales avec DOI. Si non confirmée → retirer du §8.

**Bloquant pour** : argument de phytotoxicité Cu en §8 et §11.1 si maintenu dans dossier FEDER.

---

## 5. Point d'arbitrage Soleil (obligatoire — contrat §ARBITRAGE)

La boucle a validé la **rigueur méthodologique**. Soleil arbitre la **justesse de fond** et acte trois décisions :

### 5.1 La conclusion défendable est-elle bien celle assumée ?

> *« La littérature ne soutient pas l'usage de l'électroculture grand public comme outil agronomique. La position défendable Tellux est de l'assumer comme une force (rigueur scientifique affichée) plutôt que comme une faiblesse. »*

**Confirmer (OUI / NON / NUANCER)** la position assumée dans le dossier de candidature FEDER.

### 5.2 Option E vs Option S (§7.0)

Choix de formulation publique de l'objet de test :
- **Option E** — « électroculture » assumée et encadrée. Avantage : lisibilité publique, levier de science participative, transformation d'un risque réputationnel en force éditoriale. Inconvénient : signal scientifique brouillé pour un évaluateur FEDER académique.
- **Option S** — « test contrôlé de stimulations électriques et magnétiques sur cultures comestibles ». Avantage : rigueur lisible pour évaluateurs académiques et partenaires institutionnels (INRAE, universités). Inconvénient : moins lisible côté participation citoyenne.

**Choisir E ou S** (ou hybride avec justification).

### 5.3 Exécution post-boucle des 5 conditions §4

**Ordonner par priorité et assigner** :
- TODO-1 audit citations (Frankenstein × 3) → Code locale en read-only ? Tiers ?
- TODO-2 lecture USDA Bull. 1379 → Soleil ? Cowork dans session dédiée ?
- TODO-3 lecture Solís + Ma + Lonicera → Cowork session dédiée ?
- TODO-4 pagination Lemström → optionnel
- TODO-5 vérification Brun et al. 2003 → Cowork ou Code (recherche bibliographique)

---

## 6. Livrables et fichiers produits

Tous dans `recherche/electroculture-2026-06-03/` :

| Fichier | Rôle | Statut |
|---|---|---|
| `contrat.md` | Contrat d'itération arbitré Soleil amont | ✓ Définitif |
| `SYNTHESE.md` | Livrable du générateur (itération 004, 428 lignes) | ✓ Clôture |
| `feedback-001.md` | Verdict évaluateur cycle 1 (score 6.33) | ✓ |
| `feedback-002.md` | Verdict évaluateur cycle 2 (score 6.85) | ✓ |
| `feedback-003.md` | Verdict évaluateur cycle 3 (score 7.40) | ✓ |
| `RAPPORT_FINAL.md` | Le présent fichier | ✓ |

Aucun autre artefact n'est produit par la boucle. Pas de fichier intermédiaire de travail, pas de doublon, pas de fichier de log de session.

---

## 7. Hors-périmètre conservé

Le contrat §HORS PÉRIMÈTRE excluait explicitement :
- Toute recommandation d'installation ou de pratique présentée comme **bénéfique** — **respecté** (§13.1 reformulé « candidat de premier test prioritaire », jamais « recommandation produit »).
- Les autres sujets agronomie (associations végétales, design de parcelle…) — **respecté** (aucun débordement).
- L'UI, le dispositif applicatif, le code — **respecté** (synthèse purement scientifique).

Charte agronomie §6 échec automatique : **non déclenché** sur aucune itération.

---

## 8. Note de clôture

Quatre itérations, Δ +1.07, seuil 7.0 atteint à 7.40, cible 7.5 quasi atteinte. C'est un cas où la boucle générateur/évaluateur a fait ce qu'elle devait faire : produire une synthèse défendable structurellement, identifier honnêtement ses limites, et marquer clairement la frontière entre ce qui est clos par la boucle (rigueur méthodologique) et ce qui reste à Soleil (justesse de fond) ou à une phase de validation externe (5 conditions post-boucle).

Le **pattern Frankenstein × 3 sur citations** est le seul signal résiduel préoccupant pour un usage externe immédiat. Il est traçable, identifié, et corrigeable en 1-2 h d'audit dédié.

La synthèse est prête à passer en **phase d'arbitrage Soleil + 5 conditions post-boucle** avant tout export FEDER, partenariat académique ou communication publique.

---

*Fin RAPPORT_FINAL.md — chantier `recherche/electroculture-2026-06-03/` — clôture méthodologique 2026-06-03.*
