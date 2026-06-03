# FEEDBACK — Itération 004 (cycle évaluateur 003)

> **Évaluateur** : Cowork (session distincte du générateur)
> **Date** : 2026-06-03
> **Rubrique appliquée** : `PROTOCOLE_AUTO_ITERATION.md` §5.3 + spécificités `contrat.md` + charte agronomie §4-§6
> **Cible** : itération 004 de `SYNTHESE.md` (428 lignes, sur disque)
> **Mode** : vérification de sources (web), critique uniquement, pas de réécriture
> **Précédents feedbacks** : `feedback-001.md` 6.33/10 · `feedback-002.md` 6.85/10

---

## 0. Verdict global

**Score pondéré : 7.40 / 10** — **seuil de réussite 7.0 atteint**. Cible feedback-002 §9 (7.5) **quasi atteinte**. La boucle peut être déclarée close méthodologiquement, sous réserve d'arbitrage Soleil sur la justesse de fond (cf. contrat §ARBITRAGE).

**Progression** : Δ = +0.55 par rapport à 002 (6.85 → 7.40). Pas de plateau. Δ cumulé 001→004 = +1.07. Le générateur a démontré sa capacité à absorber les critiques sévères et à itérer sans dérive.

**Échec automatique** (charte §6 / contrat §CRITÈRES) : **non déclenché**. §0 maintient « hypothèse à tester », §2.5 distingue A1 (preuve faible) de A2 (non testée à tester), §12.6 ferme sur « test sérieux à conduire », §13.1 corrigée vers « candidat de premier test prioritaire » non « recommandation produit », §14.2 trois balises tenues, §13.4 ORMUS exclu sans appel. Charte respectée.

**Position résumée** : itération 004 a appliqué **les 12 points du plan §9 du feedback-002**. La quasi-totalité a été bien exécutée, plusieurs avec excellence (§12.4 hormèse, §12.1 trois cas USDA enrichis, §12.2 re-cadrée back-of-envelope explicite avec ASTM/NACE, §13.1 confrontation Spendier, §14 re-ancrée charte §3 sans brief extra-contractuel, §11.2 AOP correct). Le **pattern résiduel** est la persistance d'au moins une **citation Frankenstein** par itération (Bilalis→Spendier en 001, Mildaziene+Sera→Leti en 003, **Calabrese 2009 EnvPoll → 2017 Ecotox en 004**). C'est un risque systémique à acter comme tel.

---

## 1. Score par critère (rubrique §5.3)

| Critère | Poids | Note /10 | Pondéré | Évolution vs 002 |
|---|---|---|---|---|
| Couverture | 0.25 | **8.0** | 2.000 | +0.5 — §12.4 hormèse + §12.1 trois cas USDA + intégration Lonicera 2023 + §11.2 AOP correct |
| Sources | 0.25 | **7.0** | 1.750 | +0.5 — Mildaziene/Sera/Leti corrigés, ASTM cités, Brun en zone « à vérifier », **mais Calabrese §12.4 = nouvelle Frankenstein** |
| Citations & traçabilité | 0.15 | **7.0** | 1.050 | +1.0 — §12.2 explicitement back-of-envelope, §12.3 qualitatif, Lonicera 2023 cité primaire (titre vérifié sur MDPI), ASTM normatifs |
| Détection de contradictions | 0.15 | **8.0** | 1.200 | +1.0 — §12.4 hormèse est self-critique structurelle, §12.1 USDA trois cas, Spendier confronté §13.1, §12.5 enrichi |
| Défendabilité FEDER | 0.20 | **7.5** | 1.500 | +0.5 — §14 re-ancrée charte §3, §13.1 reformulé, §11.2 AOP correct, §12.5 caveats explicites |
| **Total pondéré** | | | **7.500** | **+0.65 vs 002, +1.17 vs 001** — **seuil 7.0 atteint, cible 7.5 atteinte** |

Note de l'évaluateur : j'arrondis le score affiché à **7.40 / 10** dans le verdict §0 pour intégrer la pénalité résiduelle « pattern Frankenstein » (§2.1 ci-dessous) — la moyenne pondérée brute des notes par critère donne 7.50, mais le risque systémique mérite −0.10. La boucle reste **réussie**.

---

## 2. Erreurs de fait identifiées (nouvelles)

### 2.1 ERREUR DE FAIT — Attribution Calabrese §12.4 (NOUVELLE, troisième Frankenstein consécutive)

§12.4 cite : « Cadre théorique général : [Calabrese, *Environmental Pollution* 2009](https://www.sciencedirect.com/science/article/abs/pii/S0147651317308333) sur la nature non monotone fondamentale de l'hormèse environnementale. »

**Vérification web** :
- L'URL pointe vers PII `S0147651317308333` — préfixe **S0147-6513** = journal *Ecotoxicology and Environmental Safety*, **pas** *Environmental Pollution* (préfixe S0269-7491).
- Le segment « 17 » du PII indique typiquement une publication **2017**, pas 2009.
- Calabrese a effectivement publié plusieurs articles fondateurs sur l'hormèse, notamment dans *Environmental Pollution* — il existe un Calabrese E.J. 2009 dans *Env. Pollution* (DOI 10.1016/j.envpol.2009.10.041, PII S0269749109005405) — **ce n'est pas le papier que l'URL fournit**.

C'est la **troisième attribution erronée** repérée sur trois itérations évaluées :
- 001 : Bilalis et al. 2018 → vrais auteurs Spendier 2018 ✓ corrigée en 002→003.
- 003 : Mildaziene & Sera 2022 → vrais auteurs Leti et al. 2022 ✓ corrigée en 003→004 (et la vraie Mildaziene/Ivankov/Sera 2022 PMC9003542 ajoutée).
- 004 : Calabrese *Env. Pollution* 2009 → URL pointe vers *Ecotox & Env. Safety* 2017.

**Pattern systémique confirmé** : le générateur produit des références « plausibles » (auteur réel, journal vraisemblable, sujet correct) avec des **URL ou identifiants mal couplés**. Acceptable une fois (typo), problématique deux fois, **structurel à trois reprises consécutives**.

Recommandation Soleil : ce pattern n'est pas un bloquant pour la clôture méthodologique de la boucle (le seuil 7.0 est atteint), mais il **doit être traité comme risque résiduel connu** avant tout usage en dossier FEDER. Une **passe d'audit citations en bloc** par un tiers (ou par Code en mode read-only avec vérification systématique URL ↔ DOI ↔ auteurs) est recommandée avant export externe du livrable.

### 2.2 Affirmation §12.1 « 50 000 V » non sourcée inline

§12.1 ajoute en 004 : « Le programme USDA 1907-1926 a documenté des expériences initiales utilisant un **réseau alimenté à 50 000 V** au-dessus de la zone testée — c'est-à-dire un dispositif **alimenté style Lemström**, pas un composite passif Cu/Zn. »

Cette tension précise (50 000 V) est **affirmée sans citation inline à la page** du Bull. 1379. C'est précisément ce que le feedback-002 §3.1 demandait de vérifier directement dans le scan. La synthèse 004 a **partiellement** fait le travail : elle ouvre formellement les trois cas possibles (i)/(ii)/(iii) et reconnaît l'audit Bull. 1379 comme « bloquant pour la défendabilité du §12 en dossier FEDER ». **Mais** l'affirmation « 50 000 V » nouvelle reste elle-même non paginée. Soit la pagination est extraite et le voltage cité avec page exacte (idéal), soit le « 50 000 V » est retiré tant qu'il n'est pas sourcé.

### 2.3 Lonicera 2023 §12.4 — claim « max à 2 V/cm » non vérifié à la table

§12.4 affirme une « réponse hormétique en U inversé, avec maximum à 2 V/cm » sur l'étude *Plants* 12(4):933 (2023). Vérification effectuée : **le titre du papier est** « Hormesis Responses of Growth and Photosynthetic Characteristics in *Lonicera japonica* Thunb. to Cadmium Stress: Whether Electric Field Can Improve or Not? » — titre, journal, sujet (hormèse × champ électrique × Cd × Lonicera) tous confirmés sur MDPI.

**Le chiffre précis « 2 V/cm »** n'a pas été extrait au niveau table/figure dans cette évaluation (papier MDPI, full text accessible, lecture intégrale possible en itération suivante si besoin). À vérifier à la lecture des résultats avant tout usage public — c'est précisément le type de chiffre cité-en-passant qui doit être paginé pour être défendable.

---

## 3. Audit du plan §9 feedback-002 — point par point

| # | Plan-002 | Statut 004 | Note évaluateur |
|---|---|---|---|
| 1 | Corriger Mildaziene/Sera → Leti et al. | ✓ **Fait, et bien** | Les deux refs (PMC9003542 Mildaziene/Ivankov/Sera + PMC9415020 Leti et al.) sont distinguées dans §13.3 et §9. Bonne exécution. |
| 2 | Sourcer §12.2 voltages/courants Cu/Zn primaires | ✓ **Re-cadré honnêtement** | Pas de papier primaire trouvé → §12.2 explicitement étiqueté « back-of-envelope, à mesurer in situ ». ASTM G57/G187/G162/G97 et NACE cités comme cadre normatif. C'est la bonne réponse, pas un faux-fuyant. |
| 3 | Sourcer §12.3 voltage/courant famille B | ✓ **Re-cadré qualitatif** | L'« 3-4 ordres de grandeur » retiré. §12.3 explicitement qualitatif tant que Solís 2023 et Ma 2024 ne sont pas lus intégralement. Bon. |
| 4 | Auditer USDA Bull. 1379 sur composites Cu/Zn | ⚠ **Partiel** | Trois cas (i)/(ii)/(iii) explicitement ouverts ; mention du « réseau alimenté 50 000 V » 1907 (non sourcé à la page, cf. §2.2 ci-dessus). Audit complet du scan toujours dû en itération suivante. |
| 5 | Recadrer §14 sur charte §3, supprimer brief Soleil | ✓ **Fait** | §14 retitré « anti-mysticisme », ancré exclusivement charte §3. Le mot « transmutation » subsiste en référence à Hudson/Christofleau, pas en référence à un brief Soleil. Bon. |
| 6 | Brun et al. 2003 vérifié ou retiré | ⚠ **Acceptable** | Listée dans nouvelle sous-section §9 « Référence à vérifier avant usage en dossier FEDER » — déplacement épistémique correct. Reste cependant dans le corps §8 (« corpus pédologique... Brun, Le Corff, Maillet »). Tolérable. |
| 7 | Vérifier deux refs 2024 plasma de §13.3 (Plasma Chem. + Crit. Rev. Plant Sci.) | ⚠ **Drop silencieux** | Les deux refs absentes de 004. Le générateur les a retirées plutôt que vérifiées. Acceptable comme prudence, mais non-traçable comme décision dans le changelog §0. |
| 8 | §11.2 AOC → AOP | ✓ **Fait** | Châtaigne AOP 2010 (farine), Olive AOP 2004, Clémentine IGP 2007 maintenu. Note historique « AOC 2006, AOP 2010 » bien rendue. |
| 9 | §13.1 reformuler « candidat de premier test prioritaire » | ✓ **Fait** | Formulation corrigée mot-pour-mot dans §13.1 + boîte explicite. Bon. |
| 10 | §13.1 confronter Spendier 2018 négatif | ✓ **Fait** | Spendier 2018 maintenant cité dans le bullet « preuve mixte » de §13.1, avec rappel explicite « absence d'amélioration » sur chanvre 65-505 mT × 2 h sous-optimal. Bon. |
| 11 | Critiquer §12.3 sur monotonie dose-réponse | ✓ **Excellent** | §12.4 entièrement nouveau, hormèse Lonicera 2023 + cadre Calabrese (caveat §2.1). L'objection est intellectuellement solide et affaiblit substantiellement l'analogie §12.3 sans la clore — c'est la posture correcte. |
| 12 | Pagination Lemström + USDA 1379 → priorité substantielle | ⚠ **Reconnue, non exécutée** | Le générateur reconnaît en §10 que la pagination passe à « substantielle » mais ne l'a pas faite. Reportée à itération suivante. |

**Bilan plan §9** : 8/12 fait, 4/12 partiel/différé. Le différé est honnêtement déclaré dans §10 et dans le changelog. Acceptable pour cette itération.

---

## 4. Points forts à conserver

- **§12.4 hormèse Lonicera 2023** — c'est la meilleure contribution intellectuelle de 004. La critique de l'analogie §12.3 par non-monotonie de la dose-réponse est exactement ce qu'un évaluateur sévère exige. Le verdict §2.5 A2 est légitimement nuancé par cette objection.
- **§12.2 back-of-envelope explicite** — le générateur a choisi l'honnêteté plutôt que la simulation de sourcing. C'est la bonne réponse à un feedback dur. ASTM/NACE comme **cadre normatif** (pas primaire) est précisément la distinction épistémique demandée.
- **§12.1 trois cas USDA formellement ouverts** — auto-flagge l'audit Bull. 1379 comme bloquant. Permet à l'évaluateur FEDER de voir la limite du contre-argumentaire A2.
- **§13.1 candidat de test prioritaire confronté Spendier 2018** — recommandation reformulée sans valoir promesse, négatif explicite côte à côte avec positif. C'est de la défendabilité §5.3 textbook.
- **§14 re-ancré sur charte §3 seulement** — suppression propre de la référence « brief Soleil transmutation 2026-06-03 ». La position anti-mysticisme tient sur la charte seule, ce qui est plus solide qu'avec un brief non documenté.
- **§9 Référence à vérifier avant usage en dossier FEDER** — nouvelle sous-section. Pattern transposable à d'autres chantiers : une zone explicite « à auditer avant export » dans la liste de sources.
- **§11.2 AOP corrigée avec note historique** — l'AOC 2006 → AOP 2010 pour la Farine de châtaigne corse est précisément rendue.
- **§13.4 ORMUS exclusion** maintenue avec la prophylaxie « jamais agréger à G plasma ».

---

## 5. Points résiduels (non bloquants, à arbitrer)

### 5.1 Audit USDA Bull. 1379 — bloquant pour défendabilité FEDER seule

Si Soleil clôt la boucle ici, l'audit Bull. 1379 reste à faire **avant tout usage du §12 dans un dossier FEDER**. L'évaluateur FEDER lira §2.1 + §12.1 + §2.5 A2 ensemble et verra l'ouverture des trois cas. C'est défendable comme honnêteté épistémique tant que c'est explicite — ce qu'elle est. Mais le dossier complet exige le tranchage.

### 5.2 Pattern Frankenstein citations

Trois Frankenstein consécutives. Audit en bloc recommandé avant export externe. Pas de blocage de clôture interne de la boucle.

### 5.3 Lonicera 2023 — paginer « 2 V/cm »

Avant export FEDER. Lecture du papier sur MDPI accessible (full text gratuit).

### 5.4 Solís 2023 + Ma 2024 — voltage/courant exacts

§12.3 reste honnêtement qualitatif tant que ces deux papiers ne sont pas lus intégralement. Lire les papiers permettrait soit de renforcer §12.3 (si dose-réponse documentée), soit de l'affaiblir encore (si hormèse confirmée).

### 5.5 Pagination Lemström

Faible enjeu argumentatif, à faire à l'occasion. Non bloquant.

---

## 6. Recommandation de clôture

**Score atteint 7.40 / 10 ≥ seuil 7.0.** **Recommandation : déclarer la boucle méthodologiquement close** et passer à `RAPPORT_FINAL.md` + arbitrage Soleil sur la justesse de fond.

Justification :
1. Δ +1.07 sur 4 itérations, progression substantielle et non saturée.
2. Toutes les corrections bloquantes des feedbacks précédents intégrées.
3. Les nouveaux défauts (Calabrese, USDA 50 000 V, Lonicera page) sont mineurs et non bloquants, **et identifiés explicitement dans cette session d'évaluation** — ils peuvent passer en zone « à auditer avant export » sans bloquer la clôture.
4. La synthèse est désormais **structurellement défendable** : typologie A1/A2/B/C/D/E/F/G, position épistémique nette, contradictions traitées, protocole §7 calculable, articulation FEDER explicite §7.0 + §14.
5. Charte agronomie §4-§6 respectée : aucun effet présenté comme acquis, « preuve » réservée au contrôlé, méta-analyses critiques intégrées (Tapia-Belmonte avec son audit limites), résultats négatifs nommément cités (Chier 2025, Spendier 2018, USDA 1926).

**Point d'arbitrage Soleil obligatoire** (contrat §ARBITRAGE) : la boucle a validé la **rigueur**. Reste à Soleil d'acter que « la littérature ne soutient pas l'usage de l'électroculture grand public comme outil agronomique, et la position défendable Tellux est de l'assumer » est bien la position du dossier — et de choisir Option E vs Option S §7.0 pour la formulation publique.

Conditions résiduelles avant export externe FEDER, à exécuter par le générateur ou par Code en mode read-only, hors boucle d'itération scientifique :
1. **Audit citations en bloc** (pattern Frankenstein × 3) — vérifier systématiquement URL ↔ DOI ↔ titre ↔ auteurs pour toutes les références §9.
2. **Lecture du USDA Bull. 1379** (35 pages, scan archive.org accessible) — extraire la couverture explicite ou son absence des composites passifs Cu/Zn, paginer le « 50 000 V », clore les trois cas §12.1.
3. **Lecture intégrale Solís 2023 + Ma 2024 + Lonicera 2023** — extraire paramètres électriques exacts (voltage, courant, durée) pour le §12.3 et le chiffre « 2 V/cm » §12.4.
4. **Pagination Lemström** + **citation à la page du Bull. 1379** pour la formule « does not lend assurance ».
5. **Vérification Brun et al. 2003** (Soil Use Manage., phytotoxicité Cu sols vinicoles méditerranéens) — soit confirmée et listée en §9 sources, soit retirée du corps §8.

Ces 5 conditions sont **post-boucle**, pas des itérations supplémentaires. La boucle d'auto-itération générateur/évaluateur a fait ce qu'elle pouvait faire ; le reste relève de la phase de validation externe avant dossier.

---

## 7. Note évaluateur

Quatre itérations, Δ +1.07, seuil 7.0 atteint à 7.40. C'est un cas d'école de boucle générateur/évaluateur qui converge proprement quand le générateur absorbe les critiques sans dérive. La synthèse résultante est défendable structurellement, modulo les 5 points post-boucle ci-dessus.

Le **pattern Frankenstein × 3** est le seul vrai signal préoccupant — pas pour la clôture interne de la boucle, mais pour l'usage externe du livrable. Une lecture extérieure rigoureuse (évaluateur FEDER, pair scientifique, journaliste éclairé) repérera tôt ou tard ces décorrélations URL/auteur/journal/année si elles ne sont pas corrigées. Le coût d'un audit citation en bloc est faible (1-2 h) ; le coût d'une référence erronée repérée par un évaluateur externe est élevé.

La recommandation §6 « clôturer la boucle, arbitrer Soleil, exécuter les 5 conditions post-boucle » est l'usage le plus économique du dispositif d'auto-itération à ce stade.

---

*Fin feedback-003.md (cycle 003 évaluateur, évaluant itération 004) — évaluateur Cowork 2026-06-03.*
