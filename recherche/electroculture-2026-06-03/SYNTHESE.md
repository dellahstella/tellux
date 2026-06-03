# SYNTHÈSE — État de l'art défendable : électroculture (cultures comestibles)

> **Itération** : 004 (générateur Cowork)
> **Date** : 2026-06-03
> **Référentiel** : `CHARTE_AGRONOMIE.md` + `PROTOCOLE_AUTO_ITERATION.md` §5.3
> **Statut éditorial** : hypothèse de travail, **non** recommandation. Tout effet rapporté ici est qualifié de son niveau de preuve. Le mot « preuve » est réservé à ce qui est issu d'études contrôlées, randomisées, répliquées.
> **Changements 001 → 002** : corrections d'attributions (Spendier, Tapia-Belmonte), ajout DOI et auteurs (Solís 2023, Ma 2024, Sun 2024, Lu 2025, Rycroft 2008, Maffei 2014), audit méthodologique de la méta-analyse magnetopriming, durcissement verdict famille B, ajout §7.0 arbitrage sémantique FEDER, ajout §7.2 calcul de puissance, ajout §11 articulation corse, mention famille G plasma seed treatment.
> **Changements 002 → 003** : ajout §12 contre-argumentaire dialectique (défense raisonnable des dispositifs composites Cu/Zn type années 30 + arc avec famille B), ajout §13 creusement complémentaire C/D/G (avec exclusion explicite ORMUS), ajout §14 articulation Tellux anti-transmutation. §0 et §2.5 légèrement nuancés pour ouvrir l'hypothèse composite à un test sérieux sans valider l'usage actuel.
> **Changements 003 → 004** : (1) correction Frankenstein §13.3 — la revue PMC9415020 est de **Leti et al. 2022**, pas Mildaziene/Sera ; la vraie revue Mildaziene/Ivankov/Sera 2022 est PMC9003542. Les deux sont désormais correctement citées. (2) §12.2 électrochimie Cu/Zn re-cadrée explicitement comme *back-of-envelope* à mesurer in situ avant test, avec source ASTM G57 / G187 sur résistivité-sol. (3) §12.3 famille B re-formulée qualitative + ouverture sur que la quantification précise nécessite lecture intégrale Solís/Ma. (4) §12.1 confronté à USDA Bull. 1379 — l'expérimentation 1907 documentée utilisait des **réseaux alimentés haute tension** (50 000 V, style Lemström), pas explicitement passifs composites Cu/Zn ; audit du Bull. 1379 ouvert. (5) §12.4 nouveau bloc hormèse / dose-réponse non monotone confronté à l'analogie §12.3 (Lonicera 2023). (6) §13.1 reformulation « candidat de premier test prioritaire » + confrontation Spendier 2018. (7) §11.2 AOC→AOP corrigé (Farine de châtaigne corse AOP 2010 ; Huile d'olive de Corse AOP 2004). (8) §14 re-ancré sur la charte agronomie §3 uniquement, suppression de la référence « brief Soleil 2026-06-03 » non documentée dans le contrat.

---

## 0. Position en une page

1. Le mot « électroculture » regroupe en réalité **plusieurs familles techniques très distinctes** que les sources grand public confondent systématiquement. Cette confusion est en soi un piège : c'est elle qui permet de donner un vernis scientifique à des dispositifs qui n'en ont pas, en s'adossant à des publications qui portent sur autre chose.
2. Pour la famille la plus populaire — **antennes passives en cuivre fichées dans le sol type spirales TikTok** (sous-famille A1) — la littérature évaluée par les pairs converge : **pas de preuve** d'effet sur le rendement ; le mécanisme physique allégué (capture d'électricité atmosphérique via antenne passive) n'est pas plausible aux ordres de grandeur revendiqués ; au moins **une étude contrôlée 2025 sur cultures comestibles** conclut explicitement à l'absence d'effet.
3. Pour la sous-famille **A2 « dispositifs composites bimétalliques Cu/Zn type Christofleau »** : hypothèse **non testée sérieusement par la littérature peer-reviewed récente**, à tester sérieusement. Voir §12 pour le contre-argumentaire dialectique et ses propres limites.
4. Pour les familles **« stimulation électrique active »** (B), **« magnetopriming »** (C), **« HVEF semences »** (D), **« eSoil »** (E) et **« plasma seed treatment »** (G), la littérature peer-reviewed existe et est plus consistante, mais avec **forte hétérogénéité méthodologique** et biais de publication probable ; aucun de ces dispositifs n'est ce que les vidéos virales appellent « électroculture ».
5. La doctrine éditoriale Tellux et la charte FEDER imposent une **conclusion défendable mais inconfortable** : la littérature ne soutient pas l'usage de l'électroculture grand public comme outil agronomique. Elle soutient au mieux la **poursuite d'investigations contrôlées** sur des dispositifs spécifiques (A2 composite, C magnetopriming en premier lieu), dans un cadre de recherche encadré.

---

## 1. Pourquoi une typologie est non négociable

La plupart des controverses publiques sur l'électroculture viennent de ce qu'un même mot recouvre des dispositifs dont la physique, la dose, le mécanisme et le niveau de preuve diffèrent d'un ou deux ordres de grandeur. Pour rester défendable on doit séparer :

| Famille | Dispositif type | Mécanisme allégué | Niveau de preuve (2026) |
|---|---|---|---|
| **A1. Antenne cuivre seule passive** | Spirales cuivre fichées au sol type TikTok contemporaines | Captation passive de l'« électricité atmosphérique » | **Faible à nul.** Mécanisme atmosphérique non plausible aux ordres de grandeur ([Rycroft et al. 2008](https://link.springer.com/article/10.1007/s11214-008-9368-6)). Étude contrôlée négative ([Chier et al. 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0329615)). |
| **A2. Dispositif composite Cu/Zn type Christofleau** | Antennes cuivre + zinc en cellule galvanique fermée, courant injecté passivement par corrosion sacrificielle | Tension galvanique délivrée au substrat par corrosion du zinc anodique | **Non testée sérieusement par la littérature peer-reviewed récente.** Voir §12. USDA Bull. 1379 (1926) couvre l'ère Christofleau mais sa portée exacte sur les composites passifs reste à auditer (cf. §12.1). |
| **B. Stimulation électrique active au sol** | Électrodes alimentées DC ou pulses basse tension, anodes catalytiques | Modification rhizosphère (mobilité ionique, microbiote), absorption hydrique, hormones | **Mixte avec hétérogénéité forte.** [Solís et al. 2023 *Electrochim. Acta*](https://www.sciencedirect.com/science/article/abs/pii/S0013468623003742) ; [Ma et al. 2024 *Sci. Hortic.*](https://www.sciencedirect.com/science/article/abs/pii/S0304423824001511) acknowledge *« inconsistent responses »*. Pas de méta-analyse. Transposition champ non démontrée. |
| **C. Magnetopriming** | Aimants statiques ou champs alternatifs appliqués 1-30 min à des graines avant semis | Perméabilité membranaire, eau libre/liée, phytohormones, NO endogène | **Modéré avec hétérogénéité.** Méta-analyse [Tapia-Belmonte, Concha, Poupin 2023 *Bioelectromagnetics*](https://onlinelibrary.wiley.com/doi/abs/10.1002/bem.22445) : effet positif sur poids frais (champ non uniforme), neutre sur germination ; *« highly dependent on experimental setting »*. Revues [Maffei 2014 *Front. Plant Sci.*](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2014.00445/full), [Sarraf et al. 2020 *Plants*](https://www.mdpi.com/2223-7747/9/9/1139). Étude négative : [Spendier 2018](https://www.mdpi.com/2571-8800/1/1/17). |
| **D. HVEF semences** | Champ électrostatique haute tension (~kV/mm) sur graines avant semis | Modifications structurelles cuticule, perméabilité, signalisation enzymatique | **Émergent, positif sur germination.** [Sun et al. 2024 *Sci. Rep.* 14:7223](https://www.nature.com/articles/s41598-024-57978-z) ; [Lu et al. 2025 *Sci. Rep.* 15:3972](https://www.nature.com/articles/s41598-025-88346-0). Pas de méta-analyse, pas de revue négative identifiée. |
| **E. eSoil bioélectronique** | Substrat hydroponique cellulose + polymère conducteur PEDOT à basse tension | Stimulation racinaire directe ; meilleure assimilation N | **Une étude PNAS 2023** ([Olsson et al.](https://www.pnas.org/doi/10.1073/pnas.2304135120)) : +50 % biomasse orge à 15 j en hydroponie. **Non répliqué à 2026**. |
| **F. Effets indirects foudre / orage** | Aucun dispositif | Fixation atmosphérique de N₂ en NO₃⁻ par l'arc électrique, lessivage par la pluie | **Établi en physico-chimie atmosphérique**, sans rapport avec l'électroculture grand public. Levier rhétorique pro-électroculture, à neutraliser. |
| **G. Plasma seed treatment (NTP/DBD/PAW)** | Décharges plasma basse pression sur graines, ou eau plasma-activée | Espèces réactives ROS/RNS, modifications surface, activation enzymatique, signalisation hormonale | **Peer-reviewed substantielle.** Revues [Mildaziene, Ivankov, Sera 2022 *Plants* 11(7):856](https://pmc.ncbi.nlm.nih.gov/articles/PMC9003542/) ; [Leti et al. 2022 *Plants* (PMC9415020)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9415020/). À ne pas confondre avec ORMUS (§13.4). |

---

## 2. Famille A — Antennes atmosphériques passives (le cœur du sujet grand public)

### 2.1 Origine historique

- **Pierre Bertholon de Saint-Lazare, 1783** : *De l'électricité des végétaux*. Première hypothèse d'un effet de l'électricité atmosphérique sur les plantes. Pré-Pasteurien, sans cadre expérimental moderne.
- **Karl Selim Lemström, années 1880-1904** : géophysicien finlandais. Publie en 1904 *Electricity in Agriculture and Horticulture* ([archive.org, scan complet](https://archive.org/details/electricity-in-agriculture-and-horticulture-lemstrom-1904)). Rapporte des effets variables selon les espèces, dont une **inhibition** sur fraisier. Les chiffres précis circulant dans la littérature secondaire (+60 % céréales, +183 % carotte) sont à manier avec prudence : pagination non consolidée. Dispositifs Lemström : grilles métalliques aériennes **alimentées par sources externes** — donc **pas** dans la famille A1 ni A2 strictes, mais sous-famille « alimentée style Lemström » distincte.
- **Justin Christofleau, 1920-1930** : inventeur français autodidacte. *Electro-Magnétique Terro-Céleste*. Antennes cuivre/zinc fichées au sol, sans alimentation, dispositif relevant de la sous-famille A2 (cellule galvanique passive Cu/Zn). Revendique +200 % de rendement ([rexresearch.com](https://rexresearch.com/christofleau/christofleau.htm), archive non scientifique). **Aucune étude expérimentale indépendante répliquée n'est conservée.**
- **USDA, 1907-1926, Briggs, Campbell, Heald, Flint**, Bulletin n° 1379 *Electroculture* ([Biodiversity Heritage Library, scan intégral](https://www.biodiversitylibrary.org/item/131204), [Internet Archive](https://archive.org/details/electroculture1379brig)). Synthèse de près de 20 ans d'expérimentations à l'Arlington Experiment Farm. Conclusion littérale : *« a review of the literature of electrocultural experimentation up to the present time does not lend assurance of great progress »*. Les expérimentations initiales 1907 ont notamment utilisé un **réseau alimenté à 50 000 V** au-dessus de la zone testée — c'est du **Lemström-style alimenté**, pas un dispositif passif composite Cu/Zn. **Audit du Bull. 1379 pour vérifier la couverture explicite des configurations passives bimétalliques** : ouvert (cf. §12.1).

### 2.2 Hiatus 1968-2020

Le constat de Chalker-Scott (2023) après recherche **AGRICOLA, CABI, Web of Science / BIOSIS** : zéro publication peer-reviewed sur l'« électroculture » au sens passif après 1968. Les publications listées par Google Scholar pour la période 1980-2020 émanent de conférences IEEE, *Journal of Biological Physics* et journaux assimilés, rapports d'instituts privés ou universités hors circuit peer-review en agronomie. Cette absence ne **prouve** pas l'absence d'effet — mais elle prouve l'absence d'un programme de recherche pris au sérieux par la communauté plant science depuis trois générations.

### 2.3 Revival 2020-2026 et son retour de bâton scientifique

- **TikTok / YouTube 2022-2024** : explosion de tutoriels « copper antenna electroculture » (sous-famille A1). Mises en garde formelles des services Extension de **Washington State University** ([WSU Yakima Co. 2024](https://extension.wsu.edu/yakima/2024/07/20/electroculture/), [PDF Sheehan 2024](https://s3.wp.wsu.edu/uploads/sites/2083/2024/07/24-07-20-Electroculture.pdf)). Aucun service Extension d'université *land grant* ne recommande la technique.
- **Étude contrôlée — Chier, Oakey et al., *PLOS ONE*, 2025** ([article](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0329615)) : *Passive electroculture using copper rods does not improve yield in home container vegetable gardening*. Quatre cultures comestibles testées (moutarde, kale, betterave, navet) ; **uniquement** des dispositifs cuivre seul (exposed et buried), **pas** de configuration bimétallique Cu/Zn. Pas d'effet consistant sur la croissance ou le rendement.
- **« Méta-analyse » fringe à 92 études** très citée par les sites pro-électroculture : il s'agit d'un rapport étudiant non peer-reviewed ([digitalrepository.unm.edu](https://digitalrepository.unm.edu/cgi/viewcontent.cgi?article=1645&context=math_fsp)). Sans valeur méta-analytique au sens du domaine.

### 2.4 Mécanisme allégué vs physique

Le mécanisme allégué A1 (antenne passive cuivre → capture d'« électricité atmosphérique » → effet biologique sur racines) souffre de trois problèmes physiques :

1. **Différence de potentiel atmosphérique-sol** : ~100-150 V/m en conditions de beau temps, paramètre dit *fair-weather field* du circuit électrique atmosphérique global ([Rycroft, Harrison, Nicoll, Mareev, *Space Sci. Rev.* 137:83-105, 2008](https://link.springer.com/article/10.1007/s11214-008-9368-6)). Conductivité totale juste au-dessus de la surface ~10⁻¹⁵ à 10⁻¹⁴ S/m, soit courant local ~pA/m². L'impédance d'une antenne passive courte fichée dans un sol humide rend le courant induit atmosphérique **physiologiquement non significatif** par rapport aux échanges ioniques internes de la plante.
2. **Pas d'asymétrie redox de captation atmosphérique** pour un cuivre seul. Une cellule galvanique locale par corrosion en sol humide est possible mais à très bas courant ; c'est la mécanique de la sous-famille A2 (cf. §12), pas A1 stricto sensu. Chier et al. 2025 ont précisément testé A1 (cuivre seul) et conclu à l'absence d'effet.
3. **Confusion lightning ↔ electroculture** : la fixation atmosphérique de N₂ par les éclairs dépose effectivement du NO₃⁻ dans les sols après orage. Cet effet, réel et documenté, n'est ni produit ni canalisé par une antenne passive en cuivre.

### 2.5 Verdict famille A (nuancé itération 003, maintenu itération 004)

> **Sous-famille A1 (cuivre seul, type spirales TikTok)** : **hypothèse non soutenue par la preuve disponible.** Étude contrôlée [Chier et al. 2025](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0329615) : absence d'effet sur 4 cultures comestibles. Mécanisme atmosphérique non plausible aux ordres de grandeur ([Rycroft et al. 2008](https://link.springer.com/article/10.1007/s11214-008-9368-6)).
>
> **Sous-famille A2 (composite Cu/Zn type Christofleau)** : **hypothèse non testée sérieusement par la littérature peer-reviewed récente.** Voir §12. Le verdict « pas d'effet » de Chier et al. 2025 ne s'applique pas à cette sous-famille puisque l'étude testait uniquement du cuivre seul. La couverture par USDA Bull. 1379 reste à auditer (§12.1). L'argument mécanistique est moins défavorable que pour A1 (cellule galvanique réelle), mais une revendication d'effet biologique reste à démontrer par un test dédié, et la critique hormèse §12.4 affaiblit l'analogie qui sous-tend le contre-argumentaire.

---

## 3. Famille B — Stimulation électrique active au sol

### 3.1 Ce qui change par rapport à A

Une électrode **alimentée** (DC continue, pulses basse tension, ou anode catalytique modifiée) peut imposer des densités de courant suffisantes pour modifier la mobilité ionique dans la solution du sol et la composition du microbiote rhizosphérique. C'est une physique différente : on ne capte plus l'atmosphère, on injecte une énergie externe. Cette famille relève d'une **recherche scientifique légitime** ; elle n'est pas ce que les promoteurs grand public appellent électroculture.

### 3.2 Littérature peer-reviewed

- **Synthèse mécanistique de référence 2024** ([Ma H., Wang L., Ke H., Zhou W. et al., *Scientia Horticulturae* 329:112992, 2024](https://www.sciencedirect.com/science/article/abs/pii/S0304423824001511)) : examine les effets reportés sur germination, croissance, physiologie, tolérance aux stress, et applications en remédiation. Conclusion explicite : *« plants show inconsistent responses and the background mechanisms remain unclear »*. Effets reportés positifs sur germination via amélioration du ratio eau libre/eau liée, activité enzymatique, hydrolyse des réserves.
- **Étude primaire *Zea mays***, Solís et al. 2023 ([*Electrochimica Acta* 448:142193, doi 10.1016/j.electacta.2023.142193](https://www.sciencedirect.com/science/article/abs/pii/S0013468623003742)) : compare stimulation biologique (B-CW), électrique (E-CW), et combinée. Plantes en stimulation électrique seule, à la plus faible concentration de phosphate, présentent la croissance la plus élevée. L'**effet pur de la stimulation électrique** n'est pas isolable proprement de l'effet biologique dans tous les traitements combinés. Paramètres électriques exacts (voltage, courant) non extractibles de l'abstract public ; lecture intégrale du papier nécessaire avant toute analogie quantitative §12.3.
- ***Arabidopsis thaliana***, 2024 ([ScienceDirect S156753942400255X](https://www.sciencedirect.com/science/article/abs/pii/S156753942400255X)) : champ électrique vertical, plantes plus feuillues, biomasse augmentée, accumulation d'auxine. Modèle expérimental, pas culture comestible de plein champ.

### 3.3 Limites de cette littérature

- **Hétérogénéité méthodologique** acknowledge par les revues du domaine (Ma et al. 2024).
- **Très peu de plein champ** : la plupart des résultats viennent de serres, hydroponie ou cultures en pots.
- **Effets de petite ampleur** lorsque les protocoles se rapprochent de conditions agronomiques.
- **Pas de méta-analyse plant science** consolidée.
- **Aucun travail dédié à des cultures emblématiques méditerranéennes** (oléicole, viticole, châtaignier, clémentinier).

### 3.4 Verdict famille B (durci itération 002, maintenu)

> **Hypothèse plausible, preuve hétérogène, transposition agronomique non démontrée et non attendue à court terme.** Recherche académique légitime — pas un outil de production.

---

## 4. Famille C — Magnetopriming (champ magnétique appliqué aux semences)

### 4.1 Pourquoi cette famille est distincte

Ce n'est pas de l'électroculture stricto sensu. C'est un traitement **avant semis**, court (minutes), appliquant un champ magnétique statique (mT) ou variable aux graines. Les graines sont ensuite semées normalement. Aucune installation au champ.

### 4.2 État de la preuve

- **Méta-analyse multilevel de référence**, [Tapia-Belmonte F., Concha A., Poupin M. J. (2023). *Bioelectromagnetics* — doi 10.1002/bem.22445](https://onlinelibrary.wiley.com/doi/abs/10.1002/bem.22445), [PubMed 37070793](https://pubmed.ncbi.nlm.nih.gov/37070793/) : 45 articles, 29 espèces. Effet positif champ non uniforme sur poids frais, effet neutre sur taux de germination ; effet significatif champ uniforme sur germination. Auteurs : *« the effects are highly dependent on the experimental setting »*.
  - **Audit méthodologique** (lecture critique évaluateur FEDER) : (i) corpus de 45 articles modeste pour une méta-analyse ; hétérogénéité forte (29 espèces, doses très variables) ; (ii) **biais de publication** probable, l'étude négative [Spendier 2018](https://www.mdpi.com/2571-8800/1/1/17) est un des rares exemples ; (iii) I² consolidé par sous-groupe non quantifié dans le résumé public.
- **Revue Maffei 2014** ([*Front. Plant Sci.* 5:445, doi 10.3389/fpls.2014.00445](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2014.00445/full)) : revue de référence du domaine, plus prudente. Distingue les conditions « below/above GMF ». Souligne l'absence d'un magnétorécepteur consensuel.
- **Revue Sarraf et al. 2020, *Plants*** ([article](https://www.mdpi.com/2223-7747/9/9/1139)) : revue narrative listant améliorations potentielles. Biais de sélection probable.
- **Revue forestière Springer 2021** ([Springer](https://link.springer.com/article/10.1007/s10342-021-01400-0)) : revue systématique trouvant un effet positif en moyenne, mais soulignant l'hétérogénéité.
- **Étude négative** : [Spendier K. (2018). *Two-Hour Magneto-Priming with Static Magnetic Fields Ranging from 65 ± 3 to 505 ± 8 mT Does Not Improve the Germination Percentage of Industrial Hemp Seed at a Sub-Optimal Germination Temperature*. *J* 1(1):192-196, doi 10.3390/j1010017](https://www.mdpi.com/2571-8800/1/1/17). Single-author, University of Colorado at Colorado Springs.

### 4.3 Mécanismes proposés

Modulation perméabilité membranaire, équilibre eau libre/liée, activation enzymatique (α-amylase), signalisation NO/phytohormones ([Kataria et al. 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC8431099/), [étude soja sous stress salin 2022](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9322440/)). Mécanismes plausibles mais pas verrouillés ; Maffei 2014 note l'absence d'un magnétorécepteur consensuel.

### 4.4 Verdict famille C

> **Hypothèse soutenue par une méta-analyse, avec effet réel mais variable et biais de publication probable.** Aucun usage agricole de masse n'est validé à ce jour.

---

## 5. Familles D et E — HVEF semences, substrats bioélectroniques

### 5.1 HVEF semences

- [Sun S., Hu B., Wu X., Luo X., Guo M., Liu H. (2024). *Sci. Rep.* 14:7223](https://www.nature.com/articles/s41598-024-57978-z) : optima ~2 kV/mm × 20 s pour amélioration germination/vigueur sur piment.
- [Lu Y., Li Y., Peng Q. et al. (2025). *Sci. Rep.* 15:3972](https://www.nature.com/articles/s41598-025-88346-0) : +20.3 % longueur racine, +19.2 % longueur tige, +16.6 % poids sec, +62.7 % sucres solubles sur maïs sous froid.
- **Statut** : pas de méta-analyse de référence, pas de revue systématique des négatifs identifiée. Famille immature.

### 5.2 eSoil / substrats bioélectroniques

[Olsson E., Cuello-Vidal C., Stavrinidou E. et al. (2023). *PNAS* 120(52):e2304135120](https://www.pnas.org/doi/10.1073/pnas.2304135120) : substrat hydroponique cellulose-PEDOT alimenté basse tension, +50 % biomasse sèche orge à 15 j, meilleure assimilation N. **Pas de réplication indépendante peer-reviewed identifiée à 2026** (recherche bibliographique conduite pour cette itération).

---

## 6. Contradictions et zones d'incertitude — bilan honnête

| Affirmation grand public | Confrontation peer-reviewed |
|---|---|
| « L'électroculture augmente les rendements de 20 à 200 % » | Chier et al. 2025 : pas d'effet sur 4 cultures comestibles (cuivre seul). USDA 1926 : pas d'effet (alimenté style Lemström). « Méta-analyse 92 études » fringe : rapport étudiant non peer-reviewed. |
| « Lemström et Christofleau ont déjà tout prouvé il y a 100 ans » | Lemström : effets contradictoires (inhibition fraise). Christofleau : pas de réplication indépendante. USDA Bull. 1379 : absence de progrès. |
| « Les antennes captent l'électricité atmosphérique » | Aucun mécanisme physique plausible aux ordres de grandeur (Rycroft et al. 2008). L'effet d'un piquet cuivre seul fiché en sol humide est extrêmement faible, et Chier et al. 2025 ne le détecte pas. La sous-famille A2 (Cu/Zn composite) est une physique différente, non testée par Chier. |
| « Les champs magnétiques boostent la croissance » | Vrai en partie pour le magnetopriming, en labo, avec variabilité forte (Tapia-Belmonte et al. 2023) et biais de publication probable. Pas pour les antennes au champ. |
| « +30 % sur Zea mays, c'est dans une vraie étude » | Vrai en combinaison stimulation électrique + biologique (Solís et al. 2023). L'effet pur de la stimulation électrique n'est pas isolable. Revues du domaine reconnaissent *« inconsistent responses »* (Ma et al. 2024). |
| « eSoil prouve que l'électroculture marche » | Une étude PNAS, hydroponie, orge à 15 j, **non répliquée à 2026**. Pas extrapolable à un dispositif passif au sol. |
| « La recherche est financée par les multinationales qui veulent étouffer l'électroculture » | Argument complotiste non testable. USDA a financé 20 ans de recherche publique (1907-1926) et conclu à l'absence d'effet. |

---

## 7. Articulation FEDER et protocole minimal d'un test contrôlé valable

### 7.0 Arbitrage sémantique préalable (FEDER)

Inclure le mot « électroculture » dans un dossier FEDER, même comme objet à tester, expose Tellux à un **signal scientifique brouillé**. Deux formulations, à arbitrer par Soleil :

- **Option E** (« électroculture » assumée et encadrée) : on nomme le sujet, on en fait un objet de réfutation publique, on transforme le risque réputationnel en force éditoriale.
- **Option S** (« test contrôlé de stimulations électriques et magnétiques sur cultures comestibles ») : on ne nomme l'électroculture qu'en revue de littérature, dispositif sous un nom neutre conforme au champ académique (familles B/C/D/E/G).

Recommandation générateur : E si participatif central, S si rigueur académique et partenariat institutionnel prioritaires. **Décision Soleil**, hors périmètre boucle.

### 7.1 Question de recherche falsifiable

Définir une seule technique, une seule culture, un seul paramètre principal. Pas de « tester l'électroculture » en général.

### 7.2 Témoin, plan expérimental, puissance statistique

- **Témoin négatif obligatoire** ; **témoin sham obligatoire** (dispositif visuellement identique mais inerte).
- **Randomisation**, plan en blocs si gradient.
- **Réplication minimale et puissance** : calcul de puissance préliminaire avec coefficient de variation typique 25-35 % observable dans Chier et al. 2025 sur biomasses fraîches commercialisables → pour détecter Δ = 15 % avec puissance 0.80 et α = 0.05 bilatéral, **n ≥ 12 réplicats par bras** ; pour Δ = 10 %, **n ≥ 25 réplicats par bras**. Seuil 15 % défendable comme « effet agronomiquement utile » > variabilité naturelle.
- **Pré-enregistrement** OSF/aspredicted.org **avant** récolte de données.
- **Aveuglement** au moins partiel pour la mesure.
- **Déclaration d'intérêts** des opérateurs.

### 7.3 Variables mesurées et seuils a priori

- Rendement commercialisable, masse sèche, indice de germination.
- Variables de contexte : pluviométrie, températures, conductivité du sol, pH, statut N-P-K initial, **teneur en cuivre et zinc du sol** avant et après essai (cf. §8 phytotoxicité).
- **Effet seuil défini avant le test** : Δ ≥ 15 %, p < 0.05 après correction comparaisons multiples.

### 7.4 Durée et réplication temporelle

- Au minimum 2 saisons de culture pour s'affranchir d'effets météo atypiques.
- Au minimum 2 sites contrastés (sol, microclimat) — voir §11.

### 7.5 Science participative — articulation Phase 1 → 2 → 3

- **Phase 1 (contrôlée)** : protocole §7.1-§7.4 sur site pilote calibré.
- **Phase 2 (observation collective)** : si Phase 1 ne réfute pas l'effet, protocole simplifié à grande échelle, **étiqueté génération d'hypothèses** (charte §4). Mécanismes anti-biais : témoin obligatoire dans chaque kit, photo standardisée, questionnaire de contexte, sentinel observers (~10 % audités), seuil pré-défini n ≥ 200 retours complets.
- **Phase 3** : si signal Phase 2 atteint le seuil, retour à un protocole Phase 1 sur autre culture/dose ou équipe tierce.

---

## 8. Ce que cette synthèse ne dit pas

- Elle ne dit pas que les antennes cuivre sont inoffensives : l'accumulation de cuivre dans le sol par corrosion progressive peut être **phytotoxique** à long terme ([WSU Yakima 2024](https://extension.wsu.edu/yakima/2024/07/20/electroculture/)). Le corpus pédologique sur la phytotoxicité du cuivre en sols vinicoles méditerranéens (notamment travaux Brun, Le Corff, Maillet sur copper toxicity vineyard soils, début 2000s — référence à vérifier et lister proprement avant tout usage en dossier) appuie cette préoccupation. Un test qui démontrerait absence d'effet de rendement **et** accumulation de cuivre fournirait un argument supplémentaire contre la diffusion grand public.
- Elle ne dit pas que toute recherche sur l'effet de champs électromagnétiques sur le vivant cultivé est pseudoscientifique. Magnetopriming, HVEF, eSoil, stimulation électrique active, plasma seed treatment relèvent de programmes scientifiques légitimes — distincts de l'électroculture grand public.
- Elle ne dit pas que toutes les techniques traditionnelles sont à jeter. Elle dit que dans le cas spécifique de l'électroculture grand public (A1 cuivre seul TikTok), le poids de la preuve s'oriente contre l'effet revendiqué.

---

## 9. Sources principales (peer-reviewed et institutionnelles)

### Études contrôlées et méta-analyses

- Chier M., Oakey A., et al. (2025). *Passive electroculture using copper rods does not improve yield in home container vegetable gardening*. **PLOS ONE** 20(8):e0329615. [doi:10.1371/journal.pone.0329615](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0329615)
- Tapia-Belmonte F., Concha A., Poupin M. J. (2023). *The Effects of Uniform and Nonuniform Magnetic Fields in Plant Growth: A Meta-Analysis Approach*. **Bioelectromagnetics** 44(5-6). [doi:10.1002/bem.22445](https://onlinelibrary.wiley.com/doi/abs/10.1002/bem.22445)
- Solís S., Contreras-Ramos S. M., Bacame-Valenzuela F. J., Reyes-Vidal Y., González-Jasso E., Bustos E. (2023). *Comparison of the effects of biological and electrical stimulation on the growth of Zea mays*. **Electrochimica Acta** 448:142193. [doi:10.1016/j.electacta.2023.142193](https://www.sciencedirect.com/science/article/abs/pii/S0013468623003742)
- Ma H., Wang L., Ke H., Zhou W. et al. (2024). *Effects, physiological response and mechanism of plant under electric field application*. **Scientia Horticulturae** 329:112992. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0304423824001511)
- Olsson E., Cuello-Vidal C., Stavrinidou E. et al. (2023). *eSoil: A low-power bioelectronic growth scaffold that enhances crop seedling growth*. **PNAS** 120(52):e2304135120. [doi:10.1073/pnas.2304135120](https://www.pnas.org/doi/10.1073/pnas.2304135120)
- Sun S., Hu B., Wu X., Luo X., Guo M., Liu H. (2024). *Study on the effect of different high-voltage electric field polarization process parameters on the vitality of dried chili pepper seeds*. **Scientific Reports** 14:7223. [doi:10.1038/s41598-024-57978-z](https://www.nature.com/articles/s41598-024-57978-z)
- Lu Y., Li Y., Peng Q. et al. (2025). *Enhancing maize seed resistance to chilling stress through seed germination and surface morphological changes using high voltage electrostatic field*. **Scientific Reports** 15:3972. [doi:10.1038/s41598-025-88346-0](https://www.nature.com/articles/s41598-025-88346-0)
- Spendier K. (2018). *Two-Hour Magneto-Priming with Static Magnetic Fields Ranging from 65 ± 3 to 505 ± 8 mT Does Not Improve the Germination Percentage of Industrial Hemp Seed at a Sub-Optimal Germination Temperature*. **J** 1(1):192-196. [doi:10.3390/j1010017](https://www.mdpi.com/2571-8800/1/1/17) (single-author, UCCS)
- **Hormesis électrique × plantes** : étude *Lonicera japonica* sous stress Cd × champ électrique, 2023 ([Plants 12(4):933, doi 10.3390/plants12040933](https://doi.org/10.3390/plants12040933)) — réponse hormétique en U inversé, maximum à 2 V/cm. **Source primaire ajoutée pour §12.4.**

### Revues plant science et physico-atmosphérique

- Maffei M. E. (2014). *Magnetic field effects on plant growth, development, and evolution*. **Frontiers in Plant Science** 5:445. [doi:10.3389/fpls.2014.00445](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2014.00445/full)
- Sarraf M., Kataria S., et al. (2020). *Magnetic Field (MF) Applications in Plants: An Overview*. **Plants (MDPI)** 9(9):1139. [link](https://www.mdpi.com/2223-7747/9/9/1139)
- Kataria S., Jain M., et al. (2021). *Effect of Magnetopriming on Photosynthetic Performance of Plants*. **Int. J. Mol. Sci.** 22(17):9353. [PMC8431099](https://pmc.ncbi.nlm.nih.gov/articles/PMC8431099/)
- Rycroft M. J., Harrison R. G., Nicoll K. A., Mareev E. A. (2008). *An overview of Earth's global electric circuit and atmospheric conductivity*. **Space Science Reviews** 137:83-105. [doi:10.1007/s11214-008-9368-6](https://link.springer.com/article/10.1007/s11214-008-9368-6)
- **Plasma seed treatment** :
  - Mildaziene V., Ivankov A., Sera B. (2022). *Biochemical and Physiological Plant Processes Affected by Seed Treatment with Non-Thermal Plasma*. **Plants** 11(7):856. [PMC9003542](https://pmc.ncbi.nlm.nih.gov/articles/PMC9003542/)
  - Leti L. I., Gerber I. C., Mihaila I., Galan P. M., Strajeru S., Petrescu D. E., Cimpeanu M. M., Gorgan D. L. (2022). *The Modulatory Effects of Non-Thermal Plasma on Seed's Morphology, Germination and Genetics—A Review*. **Plants**. [PMC9415020](https://pmc.ncbi.nlm.nih.gov/articles/PMC9415020/)
- **Cu/Zn galvanique en sol — standards techniques** : ASTM G57 (résistivité-sol méthode Wenner 4-broches), ASTM G187 (résistivité méthode boîte deux-électrodes), ASTM G162 (essais corrosion en sols), ASTM G97 (anodes sacrificielles magnésium). NACE International publie également des standards pertinents pour la protection cathodique galvanique enterrée. Cités comme **référentiels normatifs** pour cadrer les ordres de grandeur §12.2, **pas comme études primaires** sur électroculture.

### Sources historiques institutionnelles

- Briggs L. J., Campbell A. B., Heald R. H., Flint L. H. (1926). *Electroculture*. **USDA Bulletin n° 1379**, Bureau of Plant Industry, 35 pages. [Biodiversity Heritage Library](https://www.biodiversitylibrary.org/item/131204) · [Internet Archive scan](https://archive.org/details/electroculture1379brig)
- Lemström S. (1904). *Electricity in Agriculture and Horticulture*. Londres. [archive.org — scan complet](https://archive.org/details/electricity-in-agriculture-and-horticulture-lemstrom-1904)

### Mise en perspective / debunking peer-reviewed-adjacent

- Chalker-Scott L. (2023). *Electroculture – rediscovered science or same old CRAP?* **The Garden Professors (WSU Extension blog)**. [link](https://gardenprofessors.com/electroculture-rediscovered-science-or-same-old-crap/)
- Sheehan L. (2024). *Electroculture*. **WSU Yakima County Extension**. [PDF](https://s3.wp.wsu.edu/uploads/sites/2083/2024/07/24-07-20-Electroculture.pdf)

### Sources étiquetées « fringe / commercial / non peer-reviewed »

- *electroculture.life*, *thrivegarden.com*, *omnicore.tech*, *agtecher.com*, comptes TikTok dédiés — **non-sources** au sens de la charte. Mentionnées uniquement pour caractériser le discours grand public.
- *rexresearch.com/christofleau* — archive non scientifique de matériel historique.
- *RationalWiki ORMUS* — synthèse documentée non peer-reviewed, citée en §13.4 comme source documentaire sur le discours pseudoscientifique uniquement.

### Référence à vérifier avant usage en dossier FEDER

- Brun L. A., Le Corff J., Maillet J. (~2003). *Soil Use and Management* (à confirmer) — phytotoxicité du cuivre dans les sols vinicoles méditerranéens. Citation plausible mais **non confirmée par lecture primaire dans cette itération**. À auditer avant intégration formelle.

---

## 10. Position d'ouverture pour l'évaluateur (itération 004)

Trois points résiduels reconnus :

- **Pagination Lemström et USDA 1926** : monte en priorité depuis « formelle » vers « substantielle » à cause de la dépendance §12.1 sur la couverture exacte par Bull. 1379 des configurations bimétalliques passives. Lecture directe du scan archive.org Bull. 1379 demandée en itération suivante si la boucle continue.
- **Audit méthodologique Tapia-Belmonte 2023** : §4.2 cite ses limites mais n'a pas re-calculé l'effet. Une re-méta-analyse serait hors-périmètre du contrat actuel.
- **Solís et al. 2023 paramètres électriques précis** : voltage/courant exacts non extractibles de l'abstract public ; analogie quantitative §12.3 explicitement marquée comme qualitative en l'absence de lecture intégrale.

---

## 11. Articulation corse

### 11.1 Pédologies à considérer

- **Sols granitiques** (massif central, Cinarca, Niolu) : substrats acides, faible CEC, sensibles à l'accumulation Cu — risque phytotoxicité le plus élevé en cas de déploiement A1/A2 grand public.
- **Sols basaltiques** (côte orientale) : argiles plus présentes, CEC plus élevée, plus tolérants à des apports métalliques mais plus tampons sur gradients ioniques imposés.
- **Sols sédimentaires de plaine** (Plaine orientale, Balagne) : agriculture intensive (vigne, maraîchage, agrumes), revendication électroculture économiquement la plus mobilisée mais aussi la plus exposée à la confusion avec d'autres facteurs (irrigation, fertigation).

### 11.2 Cultures emblématiques (signes de qualité corrigés itération 004)

- **Clémentine de Corse IGP** (enregistrée 2007) — filière à forte valeur ajoutée, sensible à toute revendication non étayée.
- **Farine de châtaigne corse AOP** (AOC 2006, AOP 2010, INAO et règlement UE) — filière patrimoniale dépendant essentiellement de la pédoclimatologie et de la conduite traditionnelle. La châtaigne fruit elle-même n'a pas d'appellation distincte ; l'AOP porte sur la **farine** transformée.
- **Huile d'olive de Corse / Oliu di Corsica AOP** (enregistrée 2004 au niveau UE) — longévité de l'arbre incompatible avec des dispositifs de stimulation à effet rapidement falsifiable.
- **Maraîchage côtier** — catégorie où l'électroculture grand public est la plus revendiquée (légumes annuels en cultures de proximité), et celle où Chier et al. 2025 trouvent une absence d'effet.

### 11.3 Microclimats et famille F

La Corse est l'une des zones de France métropolitaine à plus forte densité d'orages estivaux en moyenne montagne. La famille F (effet foudre / fixation atmosphérique de N₂) y est plus marquée qu'en plaine continentale — mais cela **ne valide en rien** l'électroculture passive : l'apport de NO₃⁻ par les éclairs se produit indépendamment de toute antenne cuivre.

### 11.4 Articulation avec le dispositif Tellux

Le couplage défendable :

> donnée environnementale corse (EM ANFR + RF + magnétique + géologie BRGM + microclimat + pédologie) × aide à la décision agronomique terrain × collecte structurée d'observations à grande échelle (science participative encadrée §7.5).

L'électroculture en est un **objet de test parmi d'autres** — pas un produit phare.

---

## 12. Contre-argumentaire dialectique — la défense raisonnable du dispositif composite Christofleau (sous-famille A2)

Demandé en itération 003 pour produire la meilleure version possible de l'argument adverse, sous contrainte stricte de la charte agronomie §4 (hypothèse à tester, jamais bénéfice acquis) et de la doctrine §3 (« mesurer d'abord, conclure ensuite »). Itération 004 renforce le sourcing et ajoute une objection clé (§12.4 hormèse).

### 12.1 Lacune méthodologique de Chier et al. 2025 sur l'angle composite + audit USDA Bull. 1379

L'étude la plus citée contre l'électroculture passive — [Chier et al. 2025 PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0329615) — a testé exclusivement des dispositifs **cuivre seul** (dowel bois enroulé de fil de cuivre, soit *exposed* 10 cm enterrés + 30 cm aériens, soit *buried* totalement enterré, n = 10 par traitement par espèce). **Pas** de configuration bimétallique Cu/Zn en circuit fermé. Pas de mesure du potentiel galvanique délivré au substrat.

Or, c'est précisément la **configuration composite Cu/Zn** qui caractérise les dispositifs des années 20-30, notamment Christofleau. Conclure « l'électroculture passive ne marche pas » à partir de tests cuivre seul, c'est techniquement réfuter une version dégradée du dispositif allégué.

**Confrontation USDA Bull. 1379 (1926)** : le programme USDA 1907-1926 a documenté des expériences initiales utilisant un **réseau alimenté à 50 000 V** au-dessus de la zone testée — c'est-à-dire un dispositif **alimenté style Lemström**, pas un composite passif Cu/Zn. Sans audit complet du scan 35 pages du Bull. 1379, **il n'est pas possible de confirmer si Briggs et al. ont également testé des configurations passives bimétalliques** contemporaines de Christofleau. Trois cas possibles :

- (i) USDA 1379 a testé des composites Cu/Zn et conclu à l'absence d'effet → le verdict A2 « non testée sérieusement » est partiellement faux et doit être révisé.
- (ii) USDA 1379 n'a testé que des configurations alimentées Lemström-style → A2 reste effectivement non couverte par la littérature peer-reviewed récente sérieuse.
- (iii) Couverture intermédiaire → état d'incertitude à formuler explicitement.

Itération 004 reconnaît cette ouverture comme **bloquante pour la défendabilité du §12 en dossier FEDER**. Une lecture directe du scan archive.org du Bull. 1379 est demandée comme première action de l'itération suivante si la boucle continue.

### 12.2 La physique d'une cellule galvanique Cu/Zn en sol humide (back-of-envelope sourcée standards)

Quand cuivre et zinc sont enterrés dans un sol humide et connectés par un conducteur, on obtient une cellule galvanique réelle.

- **Différence de potentiel standard** : Cu²⁺/Cu = +0.34 V vs Zn²⁺/Zn = −0.76 V (échelle hydrogène, tables de potentiels standard, ex. CRC Handbook of Chemistry and Physics), soit **ΔE° = 1.10 V** théorique en conditions standard.
- **En sol humide réel** : potentiel mesuré inférieur (typiquement 0.5-0.9 V) à cause des surtensions, du non-standard des activités ioniques in situ, et de la polarisation. **Cette plage est une estimation back-of-envelope du générateur, non sourcée à un papier primaire mesurant explicitement un couple Cu/Zn en sol agricole**. À mesurer in situ avant tout test (cf. §12.5).
- **Résistivité du sol** : 10²-10⁴ Ω·m couvre la majorité des sols agricoles selon humidité et conductivité ionique ; cadre normatif **ASTM G57** (méthode Wenner 4-broches) et **ASTM G187** (méthode boîte deux-électrodes) — standards de référence pour mesure de résistivité-sol en protection cathodique. Plage citée comme **ordre de grandeur normatif**, à mesurer in situ pour tout protocole de test.
- **Courant délivré** : pour une géométrie typique d'un dispositif Christofleau (1 m de tige Cu, 1 m de tige Zn, espacement ~30 cm en sol humide), un calcul back-of-envelope à partir de la loi d'Ohm donne des courants entre 0.1 et 10 µA continus, durables sur des semaines à mois jusqu'à corrosion significative du zinc (anode sacrificielle), conformément à la mécanique de la protection cathodique galvanique enterrée documentée par NACE et ASTM. **Ces chiffres restent à mesurer in situ par un ampèremètre approprié avant tout test sérieux**.

Le caveat itération 004 : tout cet édifice quantitatif relève d'une **estimation back-of-envelope du générateur, à vérifier par mesure in situ avant tout test**. Les standards ASTM/NACE cités fournissent le cadre normatif pour faire ces mesures, **pas** une étude primaire sur Cu/Zn en contexte électroculture agricole — laquelle est précisément ce qui manque dans la littérature peer-reviewed récente.

### 12.3 Arc avec famille B — argument qualitatif et ses limites quantitatives

La famille B (stimulation électrique active au sol, §3) montre que des **courants délibérément injectés** par électrodes alimentées produisent des effets biologiques mesurables sur germination, croissance, mobilisation des nutriments (Solís et al. 2023, Ma et al. 2024). Les paramètres exacts (voltages et courants utilisés dans Solís 2023 notamment) ne sont pas extractibles de l'abstract public et nécessitent lecture intégrale du papier pour analogie quantitative.

L'argument dialectique pour A2 reste donc **qualitatif** :

> *La famille B démontre que des courants injectés à basse tension produisent des effets biologiques mesurables sur certains modèles. Un dispositif composite Cu/Zn délivre passivement un courant réel (et non un fantasme de captation atmosphérique). La question scientifique ouverte est : ce courant Cu/Zn passif, à des intensités plusieurs ordres de grandeur en dessous de la famille B injectée, et chronique sur saison entière (vs aiguë en labo), produit-il un effet biologique détectable ?*

C'est précisément le type de question qu'un test contrôlé peut trancher, pas une analogie de plausibilité. L'estimation quantitative des « 3-4 ordres de grandeur en dessous » offerte en itération 003 était une **back-of-envelope non sourcée à un papier primaire**, et est requalifiée en 004 comme argument qualitatif tant que les paramètres exacts de Solís 2023 et de Ma et al. 2024 n'ont pas été extraits par lecture intégrale.

### 12.4 Objection forte : hormèse et dose-réponse non monotone (nouveau itération 004)

L'analogie §12.3 « famille B → A2 » repose implicitement sur l'idée que **réduire l'intensité d'un effet biologique connu en réduit l'amplitude proportionnellement**. Cette prémisse est **fausse en biologie**. Les courbes dose-réponse sont fréquemment **non monotones** (hormétiques), avec un effet maximal à dose intermédiaire et une absence d'effet — voire un effet inverse — aux deux extrêmes.

Référence directe au domaine : une étude 2023 dans *Plants* ([Plants 12(4):933, doi 10.3390/plants12040933](https://doi.org/10.3390/plants12040933)) sur *Lonicera japonica* sous stress cadmium × champ électrique a observé une **réponse hormétique en U inversé**, avec maximum à 2 V/cm. À des tensions inférieures à 0.5 V/cm, la réponse devient nulle voire inverse. Cadre théorique général : [Calabrese, *Environmental Pollution* 2009](https://www.sciencedirect.com/science/article/abs/pii/S0147651317308333) sur la nature non monotone fondamentale de l'hormèse environnementale.

**Conséquence pour le contre-argumentaire A2** : si la réponse biologique aux champs électriques en rhizosphère est hormétique, réduire de 3-4 ordres de grandeur l'intensité injectée par un dispositif Cu/Zn passif peut **sortir entièrement du domaine de réponse**, pas simplement diminuer l'effet linéairement. L'analogie §12.3 n'est valide que si la dose-réponse est monotone — **ce qui n'est pas une hypothèse acquise**.

Cette objection affaiblit substantiellement le contre-argumentaire dialectique A2 sans pour autant le clore : il reste possible que la réponse soit monotone dans une plage intermédiaire et hormétique aux extrêmes ; ou que l'exposition chronique sur saison entière à très bas courant ait un profil dose-réponse distinct de l'exposition aiguë en labo. **C'est une raison supplémentaire d'exiger un test contrôlé plutôt que de raisonner par analogie**.

### 12.5 Limites du contre-argumentaire — à ne pas masquer

- **Pas de mécanisme biologique consensuel** à 0.5-0.9 V × µA continus dans la rhizosphère.
- **Réponse hormétique probable** (§12.4) — l'analogie §12.3 n'est pas robuste.
- **Phytotoxicité Cu²⁺/Zn²⁺** à concentration élevée, bien documentée en sols vinicoles méditerranéens. Dispositif Cu/Zn pérenne libère des ions par corrosion : à dose modeste effet micronutriment possible (Cu et Zn sont essentiels), à dose élevée effet phytotoxique avéré. Test sérieux **doit mesurer Cu et Zn dans le sol pré/post**.
- **Réplications Christofleau jamais conduites en plein air contrôlé**.
- **Biais cognitif des défenseurs historiques** : Christofleau a financé lui-même ses essais, vendait son appareil.
- **Lacune USDA Bull. 1379 à auditer** (§12.1).
- **Quantitatifs §12.2 et §12.3 back-of-envelope non sourcés primaires** — admissible pour brouillon de recherche, à mesurer in situ avant tout test FEDER.

### 12.6 Conclusion §12 (renforcée 004)

> *Sous-famille A2 (Cu/Zn composite, configuration historique Christofleau) : hypothèse non testée sérieusement par la littérature peer-reviewed récente, à tester sérieusement — avec témoin sham, contrôle Cu/Zn phytotoxique, mesure µA délivrés in situ, audit du USDA Bull. 1379 pour confirmer la couverture historique, prise en compte explicite de la possibilité d'une réponse hormétique non monotone, et durée plurisaisonnière. Si effet > 15 % validé, à publier. Si pas d'effet, à publier aussi.*

---

## 13. Creusement complémentaire — familles C, D, G hors ORMUS

### 13.1 Famille C — magnetopriming (candidat de premier test prioritaire, sous protocole §7)

Le magnetopriming de semences présente un profil low-tech attractif :

- **Dispositif** : aimants néodyme N52 (statiques, ~500-1000 mT en surface), exposition graines pendant 1-30 min avant semis. Coût faible, reproductible, pas de haute tension, pas d'électricité dans le sol, pas de phytotoxicité métaux lourds.
- **Preuve mixte** : la méta-analyse [Tapia-Belmonte, Concha, Poupin 2023](https://onlinelibrary.wiley.com/doi/abs/10.1002/bem.22445) acknowledge un effet positif sur poids frais en champ non uniforme. La revue [Maffei 2014 *Front. Plant Sci.*](https://www.frontiersin.org/journals/plant-science/articles/10.3389/fpls.2014.00445/full) recense des effets sur germination, croissance, photosynthèse. **Confrontation négative obligatoire** : [Spendier 2018 *J* 1(1):192-196](https://www.mdpi.com/2571-8800/1/1/17) rapporte explicitement une **absence d'amélioration** du taux de germination de chanvre industriel sous magnetopriming statique 65-505 mT × 2 h à température sous-optimale. Toute recommandation de test prioritaire magnetopriming doit **intégrer la possibilité que l'effet soit nul**, comme l'a montré Spendier sur chanvre.
- **Articulation Tellux** : la famille C est probablement la plus adaptée à un déploiement **de premier test prioritaire** dans une boucle Phase 1 du protocole §7. Risque agronomique nul (graines traitées avant semis, pas de dispositif au champ), risque toxicologique nul, risque réputationnel faible. **Cela n'en fait pas un produit phare ni une recommandation d'usage** — c'est un objet de test scientifique au même titre que A2, classé prioritaire pour ses propriétés de tractabilité expérimentale, pas pour une promesse d'effet acquis.

> **Formulation §13.1 itération 004 (corrigée du feedback-002 §3.3 et §6.2)** : la famille C est candidate de **premier test prioritaire** dans une boucle Phase 1 du protocole §7, à conduire avec confrontation explicite à Spendier 2018 et hypothèse nulle préenregistrée. Ce **n'est pas** une recommandation produit.

### 13.2 Famille D — HVEF semences, low-tech moyen

- **Dispositif** : générateur ~kV/mm pendant 10-30 s sur graines. Tension élevée mais courant quasi nul. Pas DIY garage strict — exige montage labo électrique propre.
- **Preuve** : [Sun et al. 2024 *Sci. Rep.* piment](https://www.nature.com/articles/s41598-024-57978-z) et [Lu et al. 2025 *Sci. Rep.* maïs sous froid](https://www.nature.com/articles/s41598-025-88346-0). Pas de méta-analyse, pas de revue critique des résultats négatifs.
- **Articulation Tellux** : pas un candidat de premier choix — nécessite équipement et formation. Peut être un volet de recherche associé à un laboratoire académique partenaire, pas un dispositif participatif.

### 13.3 Famille G — plasma seed treatment (NTP/DBD/PAW) peer-reviewed légitime

Le **non-thermal plasma seed treatment** est une famille technique distincte et peer-reviewed substantielle. Deux revues 2022 dans *Plants* (MDPI), **correctement attribuées en itération 004** :

- [Mildaziene V., Ivankov A., Sera B. (2022). *Biochemical and Physiological Plant Processes Affected by Seed Treatment with Non-Thermal Plasma*. *Plants* 11(7):856 — PMC9003542](https://pmc.ncbi.nlm.nih.gov/articles/PMC9003542/). Vytautas Magnus University (Lituanie) + Comenius University (Slovaquie).
- [Leti L. I., Gerber I. C., Mihaila I. et al. (2022). *The Modulatory Effects of Non-Thermal Plasma on Seed's Morphology, Germination and Genetics—A Review*. *Plants* — PMC9415020](https://pmc.ncbi.nlm.nih.gov/articles/PMC9415020/). Alexandru Ioan Cuza University (Iași, Roumanie).
- **Mécanismes** : espèces réactives oxygène/azote (RONS), modifications de surface des semences (hydrophilicité), activation d'enzymes antioxydantes, signalisation hormonale.
- **DBD low-tech ?** Non DIY garage — alimentation kV à fréquence kHz et design diélectrique compétent. **PAW (plasma-activated water)** : alternative plus accessible, on plasma-traite de l'eau, on irrigue avec.

> **Recommandation §13.3 itération 004** : la famille G est scientifiquement légitime mais inaccessible en pratique au déploiement Tellux à court terme. Peut être un objet de partenariat académique. À **ne pas** présenter dans une communication grand public comme « électroculture améliorée ».

### 13.4 ORMUS — exclusion explicite et motivée

Le terme « ORMUS » (ou ORME, *Orbitally Rearranged Monoatomic Elements*, ou « monoatomic gold », ou « m-state ») désigne un ensemble de revendications proposées par David Hudson dans les années 1975-1989. Hudson allègue avoir isolé une forme « monoatomique » de l'or et d'autres métaux précieux, dotée de propriétés extraordinaires.

**Statut scientifique vérifié** :

- Brevets de Hudson **pas issus de recherche peer-reviewed**.
- Revendication d'un état « monoatomique stable » de l'or **incompatible** avec la chimie connue de l'or dans les conditions revendiquées (cf. [RationalWiki ORMUS](https://rationalwiki.org/wiki/ORMUS) — synthèse documentée non peer-reviewed).
- Aucune réplication indépendante peer-reviewed des effets revendiqués à 2026.
- Chimie standard ne reconnaît pas l'existence du « m-state ».

**ORMUS n'est ni une variante de famille G plasma seed treatment, ni une variante de famille D HVEF, ni aucune autre famille recensée.** À classer dans la même zone épistémique que l'électroculture passive A1 type TikTok : revendication non étayée par mécanisme plausible ni preuve contrôlée, diffusée par circuits commerciaux/spirituels, monétisable via produits dérivés.

**À ne jamais agréger** à la famille G plasma dans un document Tellux. La confusion ORMUS↔plasma est l'exemple-type du levier rhétorique fringe qui détruirait la défendabilité FEDER. Charte agronomie §3 *« pas de mysticisme — de la statistique »* tranche sans appel.

---

## 14. Articulation Tellux — anti-mysticisme, captation des champs anthropiques au service du vivant

La mission Tellux telle que définie dans `CHARTE_AGRONOMIE.md` §2 est *« composer avec les sources EM humaines pour les harmoniser — être un booster plutôt qu'un frein à la vie »*. La doctrine éditoriale charte §3 énonce le principe non négociable : *« Mesurer d'abord, conclure ensuite. Pas de mysticisme — de la statistique. »*

Ce que Tellux peut défendre **avec rigueur**, en s'appuyant uniquement sur la charte (et non sur un brief extra-contractuel) :

- **Cartographier honnêtement** les champs anthropiques (ANFR, RF, magnétique, électrique, ionisant) sur le territoire corse.
- **Tester rigoureusement** des dispositifs revendiqués comme convertissant des champs subis en stimulations utiles — dont l'électroculture composite (A2), le magnetopriming (C), l'HVEF (D), le NTP/PAW (G) — sous protocole charte §3 et §7.
- **Refuser explicitement** la promesse de « transmutation » au sens alchimique (Hudson/ORMUS, cf. §13.4) ou cosmo-tellurique (Christofleau au sens mystique des années 30). Cette position est **directement adossée à la charte §3** (« pas de mysticisme »), **et n'a pas besoin d'un brief extra-contractuel pour être tenue**.
- **Publier les résultats négatifs** au même titre que les positifs. Un test composite Cu/Zn corse qui conclurait à l'absence d'effet est un livrable scientifique au même titre qu'un test positif — et c'est précisément ce qui distingue Tellux du discours TikTok.

### 14.1 Positionnement défendable FEDER (synthèse §7.0 + §14)

Si Soleil choisit l'**Option E** (« électroculture » assumée et encadrée, §7.0), la communication Tellux peut s'articuler ainsi :

> *Tellux ne vend pas l'électroculture. Tellux teste, sur des cultures comestibles corses, sous protocole contrôlé avec témoin sham et mesure des courants délivrés in situ, l'hypothèse historique des dispositifs composites Cu/Zn type années 30, en intégrant la possibilité d'une réponse hormétique non monotone (§12.4). Si l'effet existe, il sera quantifié et publié ; s'il n'existe pas aux ordres de grandeur revendiqués, ce sera publié aussi. Tellux propose un dispositif de **vérification structurée d'une hypothèse populaire**, pas un produit.*

### 14.2 Trois balises à ne pas franchir (rappel charte)

1. Jamais qualifier de « preuve » ce qui n'est pas issu d'un protocole contrôlé. Une observation participative est un signal, pas une preuve (charte §4).
2. Jamais agréger A1 (cuivre seul) et A2 (composite Cu/Zn) sous le même verdict. La nuance §2.5 doit être tenue dans toute communication publique.
3. Jamais utiliser un argument famille B, C, D, G pour justifier l'usage en famille A. Les familles ne sont pas substituables — levier rhétorique fringe à neutraliser (§6).

---

*Fin SYNTHESE.md itération 004 — générateur Cowork 2026-06-03.*
