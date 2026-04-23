# Audit §7 corpus — 4 points ouverts à arbitrer

**Date :** 2026-04-23
**Auteur :** Claude Code (audit read-only)
**Destinataire :** session claude.ai web suivante pour arbitrage Soleil
**Source canonique §7 :** `_corpus/HYPOTHESES_SCIENTIFIQUES.md` §7 « Arbitrages à signaler à Soleil » (lignes 983–1059)

---

## Contexte

Cet audit prépare l'arbitrage des 4 points ouverts identifiés en §7 du corpus
(`_corpus/HYPOTHESES_SCIENTIFIQUES.md`), conditionnant l'intégration du Pilier A
dans `corpus.html` (onglet dédié, format 1C, bandeau méthodologique, séquencement 2A).

§7 est structuré en 4 sous-sections : §7.1 (hypothèses à 3/5 critères), §7.2 (doubles
A+B), §7.3 (hypothèses abandonnées avec justification), §7.4 (hypothèses nouvelles).
Les 4 points ouverts sont distribués entre §7.1, §7.2 et §7.3.

---

## Point 1 — Double A+B H1/H18/H21

**Statut :** Partiellement résolu

**Description :**

Trois hypothèses historiques apparaissent simultanément dans les deux piliers :
- H1 → S11 (Pilier A : susceptibilité granit quantifiable) + P12 (Pilier B : « le granit chante-t-il ? »)
- H18 → S12 (Pilier A : score géomagnétique naturel × églises × substrat piézo) + P13 (Pilier B : « les antennes suivent-elles les crêtes des chapelles ? »)
- H21 → S1 (Pilier A : test Monte Carlo, coïncidence anomalies × sites anciens) + P1 (Pilier B : « pourquoi ces endroits précis ? »)

**§7.2 source (extrait) :** « Dans les 3 cas, la version Pilier A est rigoureuse et testable, la version Pilier B est narrative et engageante sans contredire la première. Arbitrage : valider le double usage ou décider d'exclure la version patrimoniale pour éviter confusion public/expert. »

**Statut détaillé :**

Le sous-problème H18 (incohérence titre/desc dans `patrimoine.html`) est **résolu** :
la Variante A (lecture RF, alignée P13) a été appliquée (commit `75f043a`, 2026-04-23).
H18 reformulée expose désormais la question RF topographique (antennes × crêtes × chapelles).

La mitigation architecturale est déjà en place dans le corpus (`TRANSITION_CORPUS_H1_H88_VERS_2_PILIERS_v1.md` §4.2) : chaque fiche B pointe vers sa fiche S via « Lien éventuel vers Pilier A » ; les fiches S ne pointent pas vers les fiches B (asymétrie intentionnelle, Pilier A reste scientifique).

**Ce qui reste ouvert :** l'arbitrage de principe sur le double usage lui-même. L'asymétrie de pointage est-elle suffisante pour éviter la confusion public/expert, ou faut-il supprimer les versions B de P1/P12/P13 du `corpus.html` (onglet Pilier A) et les réserver exclusivement à `patrimoine.html` ?

**Options :**

- **Option A — Valider le double usage (status quo) :** les fiches P1, P12, P13 restent dans les deux espaces. Chaque fiche B signale explicitement son pendant A. L'onglet `corpus.html` affiche uniquement les fiches S ; les fiches P sont dans leur espace propre. Pas de confusion si les deux onglets sont bien séparés visuellement. **Implication :** aucune modification structurelle, intégration immédiate possible.

- **Option B — Exclure les versions B de l'espace corpus.html :** les fiches P1/P12/P13 sont réservées à `patrimoine.html` ; l'onglet `corpus.html` n'affiche que les fiches S, sans mention du pendant patrimonial. **Implication :** supprime le risque de confusion, mais réduit la narrativité du corpus pour un lecteur non-spécialiste.

- **Option C — Garder le double usage avec mention explicite dans le bandeau :** le bandeau méthodologique de `corpus.html` précise que certaines hypothèses ont une version « grand public » dans `patrimoine.html`, distincte de la formulation scientifique. **Implication :** transparence maximale, compatible avec séquencement 2A, sans suppression de contenu.

**Recommandation Claude Code :** Option C. Le bandeau méthodologique prévu (séquencement 2A) est l'emplacement naturel pour une note d'une phrase sur la distinction Pilier A / Pilier B. Cela lève le risque de confusion sans supprimer de contenu, et est cohérent avec la position épistémique Tellux (transparence sur le statut des hypothèses).

**Implications pour l'intégration :** N'influence pas l'intégration. Le contenu des fiches S est prêt ; l'arbitrage du principe double usage peut se résoudre dans la rédaction du bandeau.

---

## Point 2 — H20

**Statut :** À arbitrer

**Description :**

H20 (« alignements significatifs ») est présente dans l'array `HYPOTHESES` de `patrimoine.html`
(ligne ~677) sans formulation complète documentée. Dans `_corpus/HYPOTHESES_SCIENTIFIQUES.md`
§7.1, elle est classée parmi les candidates écartées du Pilier A avec justification :

> « H20 (alignements significatifs) : C4 fort (Broadbent 1980), mais C5 faible (méthodologique pur, pas spécifique Corse). Pourrait être intégrée S1 comme protocole subordonné plutôt que fiche autonome. Arbitrage : à confirmer par Soleil. »

**Nature du conflit :** H20 porte sur la significativité statistique des alignements mégalithiques (test Broadbent 1980 sur randomisation). Ce protocole est déjà utilisé dans S1 (coïncidence anomalies × sites anciens, test Monte Carlo) et dans la Variante A de H18 (Monte Carlo spatial contraint par l'altitude). La question est donc : H20 est-elle une hypothèse autonome (question distincte sur les alignements en eux-mêmes) ou un protocole partagé subordonné à d'autres hypothèses ?

**Formulation actuelle dans les sources :**
- `patrimoine.html` : id `H20`, titre non affiché (dormante), desc non documentée dans ce document
- `_corpus/HYPOTHESES_SCIENTIFIQUES.md` §7.3 : listée parmi les abandonnées de `patrimoine.html` non retenues en Pilier A
- `_corpus/HYPOTHESES_PATRIMOINE_GAMIFIEES.md` §9.5 (P4) : candidate future Pilier A avec test Kendall statistique sur distribution aléatoire

**Options :**

- **Option A — Fiche autonome Pilier B (P4 confirmée) :** H20 reste une question patrimoniale gamifiée (« les alignements de Palaggiu sont-ils alignés plus que le hasard ? »). Elle appartient à `patrimoine.html` uniquement, sans fiche Pilier A correspondante. C5 faible justifie l'exclusion du corpus scientifique. **Implication :** pas de fiche S20 dans `corpus.html` ; P4 reste dans `patrimoine.html`.

- **Option B — Protocole subordonné à S1 (intégration dans note de bas de fiche) :** H20 n'a pas de fiche propre, mais la fiche S1 mentionne explicitement le protocole Broadbent 1980 comme méthode applicable aux alignements. Pas de doublon, pas de trou. **Implication :** aucune nouvelle fiche à créer, ajustement d'une note dans S1.

- **Option C — Fiche S15 conditionnelle « alignements Corse » :** H20 reçoit une fiche Pilier A conditionnelle, à activer si un corpus d'alignements corses est constitué (données archéologiques géoréférencées). Statut « en attente données terrain ». **Implication :** fiche S15 à rédiger, exposée dans `corpus.html` avec flag conditionnel.

**Recommandation Claude Code :** Option A ou B selon priorité. Si Soleil veut garder le corpus Pilier A minimal et propre (S1-S14 validés), Option B est plus sobre : le protocole Broadbent est déjà mentionnable dans S1 sans créer une fiche supplémentaire. Option C est pertinente si la valeur scientifique des alignements corses mérite une mise en avant autonome.

**Implications pour l'intégration :** N'influence pas l'intégration du Pilier A (`corpus.html`). H20 n'est pas une fiche S existante : son arbitrage ne bloque aucune des 14 fiches S1-S14 actuelles.

---

## Point 3 — H85-H87

**Statut :** À arbitrer

**Description :**

H85, H86, H87 apparaissent dans les sources sous **deux usages incompatibles** du même
identifiant, identifiés dans `docs/notes-tri/RELECTURE_H1_H88_POST_BIOTSAVART_v1.md` §3.5 :

> « H85–H87 : mines BRGM cibles EM » (légende `indu` app.html ligne ~2013) — usage 1
> « H85–H87 : FAUNE (ovins/caprins drone, balbuzard Scandola LPO) » (roadmap) — usage 2

**Formulation source (RELECTURE §3.5, extrait) :**
> « Deux usages différents du même identifiant — à clarifier avec Soleil avant toute classification ferme. »
> « Si H85–H87 visent à caractériser le rayonnement EM résiduel autour des anciennes mines (Argentella, Biguglia, Finosa…), v2 est utilisable pour modéliser la composante ELF anthropique au voisinage des lignes HTA d'alimentation résiduelle. Si les mêmes ids désignent FAUNE, aucune relation ELF directe. »

**`_corpus/HYPOTHESES_SCIENTIFIQUES.md` §7.3 (extrait) :**
> « H85–H87 (mines BRGM ou FAUNE) : identifiant ambigu dans les sources (cf. RELECTURE §3.5). Arbitrage : à trancher avec Soleil — si "mines EM", rattacher à S4/S9 ; si FAUNE, Pilier B. »

**`_corpus/HYPOTHESES_PATRIMOINE_GAMIFIEES.md` §9 :**
> « H85-H87 — ambiguës (cf. Pilier A §7). À clarifier côté Pilier A d'abord. »

**Nature du conflit :** l'identifiant H85/H86/H87 est utilisé dans deux contextes sans lien : (a) mines BRGM comme cibles de caractérisation EM anthropique résiduelle (Pilier A potentiel, testable avec v2 Biot-Savart), (b) faune sauvage avec comportements magnétoréception (Pilier B, hors protocole Tellux solo). Le corpus ne peut intégrer les deux interprétations sous le même identifiant.

**Options :**

- **Option A — Usage "mines EM" retenu (Pilier A) :** H85/H86/H87 deviennent des cibles de protocole ELF dans le prolongement de S4 (loi 1/d² distance HTA) et S9 (EMAG2 × score géo). Trois sites miniers corses (Argentella, Biguglia, Finosa) comme cas d'étude EM anthropique résiduel. **Implication :** fiches S15/S16/S17 potentielles à rédiger, ou intégration comme sous-protocole de S4/S9. Aucune exposition `corpus.html` avant fiche rédigée.

- **Option B — Usage "FAUNE" retenu (Pilier B) :** H85/H86/H87 rejoignent le Pilier B comme questions sur la magnétoréception animale (ovins/caprins, balbuzard). Côté Pilier B, déjà H84 (magnétoréception animale générale) et P14 (animaux qui migrent × champ magnétique). Intégration comme P21/P22/P23 potentielles. **Implication :** aucune fiche Pilier A concernée ; pas d'impact `corpus.html`.

- **Option C — Double usage partiel :** H85 = mines EM (Pilier A potentiel), H86/H87 = FAUNE (Pilier B). Séparer les trois identifiants si les sources permettent de les distinguer individuellement. **Implication :** nécessite une relecture des sources primaires (app.html lignes ~2013, roadmap) pour vérifier si les trois identifiants sont toujours groupés ou si certains sont individualisables.

**Recommandation Claude Code :** Point de validation nécessaire. L'audit n'a pas accès aux sources primaires permettant de confirmer si les trois identifiants sont distinguables individuellement (app.html lignes ~2013, TELLUX_ROADMAP.md). Option A ou B à trancher par Soleil selon la priorité scientifique : si Tellux a un protocole terrain envisageable sur les mines corses, Option A. Sinon, Option B est plus sobre.

**Implications pour l'intégration :** N'influence pas l'intégration du Pilier A actuel (aucune des fiches S1-S14 n'est H85-H87). L'arbitrage peut être différé après l'intégration de `corpus.html`.

---

## Point 4 — H88/H91

**Statut :** À arbitrer (deux sous-points distincts)

**Description :**

H88 et H91 ont des statuts différents et sont groupés ici car tous deux listés en §7.3 avec arbitrage explicite, mais leur traitement est indépendant.

---

### Sous-point 4a — H88 (identifiant fourre-tout)

**Formulation source (`_corpus/HYPOTHESES_SCIENTIFIQUES.md` §7.3) :**
> « H88 (granit piézo / cortisol / géothermie) : identifiant surchargé dans les sources. Arbitrage : clarifier avant usage. »

**Sources primaires identifiées (RELECTURE §0.3) :**
> TELLUX_ROADMAP.md et TELLUX_ACTIONS_POST_RECHERCHE.md mentionnent H84-H94 dans un bloc « post-candidature » incluant : magnétoréception, faune, Kp cardio, granit piézo ITU-R P.2040-2, shinrin-yoku, cortisol CHU Ajaccio.

L'identifiant H88 dans ce bloc agrège au moins trois concepts distincts sans formulation structurée séparée :
1. Granit piézo (propriété physique du substrat) — couverte partiellement par S11, H1, H39
2. Cortisol / réponse stress humaine — dimension physiologique, hors périmètre EM strict
3. Géothermie — dimension thermique, distincte de l'EM

**Options :**

- **Option A — Décomposer H88 en 3 identifiants distincts :** H88a (granit piézo, Pilier A si protocole défini), H88b (cortisol × substrat, Pilier B ou future collaboration CHU Ajaccio), H88c (géothermie, Pilier A si gradient mesurable). **Implication :** 3 nouvelles fiches potentielles à rédiger ultérieurement ; l'identifiant H88 est retiré du corpus en attente de cette décomposition.

- **Option B — Retirer H88 du corpus actuel, différer :** aucune des 3 dimensions n'est prête pour une fiche structurée (C1-C5 incomplets pour les 3). H88 est marquée « non documentée » et n'apparaît pas dans `corpus.html`. Réévaluation lors d'une session corpus ultérieure. **Implication :** aucun impact intégration actuelle ; la question sera soulevée à nouveau au prochain enrichissement du corpus.

- **Option C — Retenir uniquement la dimension granit piézo comme H88 :** les deux autres dimensions (cortisol, géothermie) sont exclues explicitement. H88 = question physique sur le granit piézo, distincte de H91 (diélectrique). Évaluation C1-C5 à faire. **Implication :** fiche H88 potentiellement intégrable si C1-C5 remplis ; nécessite session dédiée.

**Recommandation Claude Code :** Option B pour l'intégration immédiate. H88 n'est pas documentée suffisamment pour exposer une formulation publique sans risque d'imprécision. La décomposition (Option A) est la bonne direction à terme mais nécessite une session dédiée avec les sources primaires (ROADMAP, ACTIONS_POST_RECHERCHE).

---

### Sous-point 4b — H91 (diélectrique granit, conditionnelle)

**Formulation source (`_corpus/HYPOTHESES_SCIENTIFIQUES.md` §7.3) :**
> « H91 (diélectrique granit ITU-R P.2040-2) : potentiel S scientifique, mais C3 protocole coûteux (labo diélectrique). Arbitrage : Pilier A bis si partenariat CEA/Génopode Corte confirmé. »

**Contexte :** H91 porte sur la permittivité diélectrique du granit corse et son effet sur la propagation RF (norme ITU-R P.2040-2). Le critère C3 (protocole testable) est bloqué par l'absence d'équipement de mesure diélectrique en accès Tellux. Un partenariat avec CEA ou Génopode Corte lèverait ce blocage.

**`_corpus/HYPOTHESES_PATRIMOINE_GAMIFIEES.md` §9 :**
> « H91 (diélectrique) — conditionnelle. En veille. »

**Options :**

- **Option A — Fiche S15 conditionnelle « en attente partenariat » :** H91 reçoit une fiche Pilier A dans `corpus.html` avec statut explicite « en attente données terrain (labo diélectrique) ». Le bandeau signale que cette fiche est conditionnelle. **Implication :** expose la question scientifiquement valide tout en étant transparent sur le blocage ; peut servir d'outil de démarchage partenaire.

- **Option B — Veille pure, hors `corpus.html` :** H91 n'est pas exposée dans `corpus.html` tant que C3 n'est pas levé. Elle reste dans le corpus interne comme candidate conditionnelle. **Implication :** pas d'exposition prématurée, mais perd l'effet démarchage.

- **Option C — Mention dans une section « hypothèses en veille » de `corpus.html` :** séparée des fiches S actives, une section légère liste les hypothèses conditionnelles. H91 y figure avec 2 lignes : question + condition de déblocage. **Implication :** exposition minimale, transparence sur le pipeline, sans fiche complète.

**Recommandation Claude Code :** Option A ou C selon l'objectif stratégique Soleil. Si l'onglet `corpus.html` vise à crédibiliser Tellux pour le démarchage physicien/partenaire, exposer H91 avec son statut conditionnel (Option A) est pertinent : ça montre que le corpus a été pensé pour s'étendre. Option C est un compromis si Soleil veut garder la section principale propre et sans fiches incomplètes.

**Implications pour l'intégration :** N'influence pas l'intégration des 14 fiches S1-S14 actives. H91 peut être tranchée en parallèle ou après l'intégration principale.

---

## Synthèse pour Soleil

| Point | Sous-point | Statut | Bloquant intégration ? | Complexité arbitrage | Recommandation Claude Code |
|-------|-----------|--------|------------------------|----------------------|----------------------------|
| 1 | Double A+B H1/H18/H21 | Partiellement résolu (H18 réparé) | Non | Faible (principe à valider) | Option C (mention dans bandeau) |
| 2 | H20 | À arbitrer | Non | Faible | Option A ou B (H20 hors Pilier A actuel) |
| 3 | H85-H87 | À arbitrer | Non | Modérée (nécessite sources primaires) | Trancher selon priorité terrain mines vs faune |
| 4a | H88 | À arbitrer | Non | Modérée (décomposition à faire) | Option B (différer, hors corpus.html) |
| 4b | H91 | À arbitrer | Non | Faible (décision stratégique) | Option A ou C selon objectif démarchage |

**Conclusion :** Aucun des 4 points n'est bloquant pour l'intégration des 14 fiches S1-S14 dans `corpus.html`. L'intégration peut démarrer après arbitrage de principe sur le Point 1 (bandeau méthodologique). Les Points 2, 3, 4 peuvent être arbitrés en parallèle ou différés sans bloquer la publication.

---

## Zones d'incertitude résiduelles

1. **Formulation actuelle de H20 dans `patrimoine.html`** : l'audit n'a pas relu directement la ligne H20 de l'array HYPOTHESES (lignes ~677 de `patrimoine.html`). La desc exacte n'est pas extraite dans ce document. Si Soleil opte pour Option B (protocole subordonné S1), une vérification de l'alignement avec S1 est nécessaire.

2. **Sources primaires H85-H87** : l'audit s'appuie sur le résumé RELECTURE §3.5. Les lignes exactes de `app.html` (~2013) et du ROADMAP n'ont pas été relues directement dans cette session. Si Soleil veut vérifier l'usage individuel H85 / H86 / H87 (pas seulement le bloc), une lecture directe est nécessaire avant Option C.

3. **Sources primaires H88** : le contenu exact de TELLUX_ROADMAP.md et TELLUX_ACTIONS_POST_RECHERCHE.md n'a pas été relu dans cette session pour la section H84-H94. L'audit se base sur le résumé §0.3 de HYPOTHESES_SCIENTIFIQUES.md. Si Soleil veut vérifier si H88 est individualisable, une lecture de ces fichiers est nécessaire.

4. **Statut partenariat CEA/Génopode Corte pour H91** : l'audit ne peut pas évaluer si des démarches ont été faites depuis la rédaction de HYPOTHESES_SCIENTIFIQUES.md. Si le partenariat est en cours, l'Option A pour H91 devient plus urgente.

---

## Prochaine étape

Arbitrage Soleil sur les 5 sous-points (Points 1, 2, 3, 4a, 4b) dans une session
claude.ai web, puis rédaction du prompt d'intégration `corpus.html` dans une session
Claude Code dédiée.

Point 1 peut être résolu directement dans la rédaction du bandeau (`corpus.html`).
Points 2, 4a, 4b sont indépendants et peuvent être tranchés en 1-2 phrases chacun.
Point 3 (H85-H87) peut nécessiter une courte session de relecture des sources primaires
(`app.html` lignes ~2013, ROADMAP) si Soleil veut vérifier avant de trancher.

---

## Arbitrage Soleil — 2026-04-23

Les 4 points ouverts ont été arbitrés comme suit :

### Point 1 — Double A+B H1/H18/H21 : SOLDÉ

Traitement dans le bandeau méthodologique de `corpus.html` (chantier d'intégration Pilier A).
Le bandeau inclura : « Certaines hypothèses existent en double formulation dans le corpus Tellux :
une version scientifique testable (Pilier A) et une version patrimoniale accessible (Pilier B,
non publiée à ce stade). Chaque version relève d'une démarche distincte et ne préjuge pas du
résultat de l'autre. »

Référence : prompt d'intégration `corpus.html` du 2026-04-23.

### Point 2 — H20 : DIFFÉRÉ

Non bloquant pour l'intégration des 14 fiches S1-S14 dans `corpus.html`.
À arbitrer en session dédiée ultérieure : fiche Pilier B autonome (P4) ou protocole
subordonné mentionné dans S1 ?

### Point 3 — H85-H87 : DIFFÉRÉ

Non bloquant pour les 14 fiches S1-S14 (H85-H87 ne sont pas dans le périmètre exposé).
À arbitrer en session dédiée ultérieure : priorité terrain entre (a) mines BRGM -> Pilier A
sous S4/S9, et (b) faune (ovins/balbuzard LPO) -> Pilier B.

### Point 4a — H88 fourre-tout : DIFFÉRÉ

Non bloquant pour S1-S14. Recommandation : décomposition en session dédiée (granit piézo,
cortisol, géothermie sont trois sujets distincts qui méritent chacun une fiche séparée).

### Point 4b — H91 diélectrique granit : DIFFÉRÉ

Non bloquant pour S1-S14. Scientifiquement valide mais bloqué sur labo diélectrique
(critère C3 non satisfait). À réactiver lors d'un démarchage partenaire labo ultérieur.
Option envisageable : fiche "en veille" dans une future section `corpus.html` si utile
pour la crédibilité du démarchage partenaire.

### Conclusion

Aucun des 4 points ne bloque l'intégration du Pilier A (S1-S14) dans `corpus.html`.
L'intégration peut démarrer sur la base des 14 fiches documentées, avec le bandeau
méthodologique soldant le Point 1. Les autres points restent documentés dans cet audit
et pourront être repris en sessions dédiées selon la priorité projet.
