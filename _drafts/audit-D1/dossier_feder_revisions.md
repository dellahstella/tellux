# Livrable 3 — Révisions ciblées du dossier de pré-candidature FEDER

**Sprint** : audit-D1 (Phase D du 2026-05-01)
**Référence audit** : sections 5.1 (EUPL → MIT) et 5.2 (nuance hébergement Supabase)
**Source** : `DOSSIER_PRECANDIDATURE_FINAL.md` (808 lignes, état à la date de session)
**Statut** : draft markdown — diffs à appliquer en passe de relecture sur le fichier final, hors périmètre de ce sprint

---

## 1. Révision 5.1 — EUPL → MIT

### 1.1 Justification de la bascule

La licence MIT est compatible avec l'AAP « Data & IA au service de l'intérêt général » qui demande une publication open source sans imposer de licence européenne spécifique. La bascule vers MIT présente trois avantages opérationnels :

1. **Réutilisation plus large** : MIT est la licence open source la plus connue, la plus simple, et la plus permissive. Elle minimise les frictions juridiques pour un acteur tiers — laboratoire de recherche, collectivité étrangère, startup — qui souhaiterait intégrer le moteur Tellux dans son propre système d'information.
2. **Cohérence avec l'argument d'essaimage** : le plan d'essaimage (livrable L5.4) cible la Sardaigne, les Baléares, la Crète, Malte, et les territoires d'outre-mer. MIT est universellement reconnue dans ces écosystèmes ; EUPL est une licence quasi-exclusivement institutionnelle européenne, peu adoptée hors administrations publiques UE et qui peut être perçue comme un frein dans des contextes de réutilisation transversale.
3. **Cohérence avec l'état actuel du projet** : le code source de Tellux est déjà publié sous licence MIT (cf. fichier `LICENSE` du dépôt `dellahstella/tellux`, mention « Le code est sous licence MIT » présente dans `methode-et-limites.html` l.448). Maintenir EUPL dans le dossier de candidature créerait une incohérence avec le statut public observable de la plateforme.

L'argument de souveraineté UE n'est pas porté par la licence du code, mais par les choix d'hébergement, d'opérateurs de paiement et de juridiction applicable. La bascule vers MIT ne fragilise pas le positionnement souveraineté du projet — elle clarifie au contraire que la souveraineté est une question d'infrastructure et de droit applicable, pas de licence de copyright.

### 1.2 Inventaire exhaustif des occurrences à modifier

**Fichier cible** : `C:/Users/lucas/Documents/Claude/Projects/Tellux/DOSSIER_PRECANDIDATURE_FINAL.md`

Dix-sept occurrences identifiées dans le dossier de pré-candidature, regroupées par section.

| # | Ligne | Section | Occurrence à modifier |
|---|---|---|---|
| 1 | 36 | 2.1 Synthèse | « (livrables L3.1 et L3.2 sous licence European Union Public Licence) » |
| 2 | 84 | 2.2 Résultats visés | « publié sur le registre npm sous licence européenne » |
| 3 | 180 | 2.3.3 Bien commun | « code applicatif et des modules techniques sous licence European Union Public Licence 1.2 » |
| 4 | 254 | 2.3.4 Essaimage | « publié sur npm sous licence européenne » |
| 5 | 268 | 2.3.5 Charte data — principes 15/16 | « la publication de l'intégralité du code applicatif sous licence européenne » |
| 6 | 391 | 2.3.7 Propriété et ouverture | « selon la licence EUPL 1.2 » |
| 7 | 475 | 2.3.9 Calendrier mensuel — M2 | « publication open source EUPL des deux applications » |
| 8 | 515 | 2.3.10 Liste livrables — intro | « licence European Union Public Licence (EUPL) version 1.2, à l'exception des workflows d'automatisation N8N qui bénéficient de la licence MIT » |
| 9 | 548 | 2.3.10 Catégorie 3 — L3.1 | « publiée sous licence EUPL 1.2 sur les dépôts GitHub » |
| 10 | 550 | 2.3.10 Catégorie 3 — L3.2 | « publiée sous licence EUPL 1.2 selon les mêmes modalités que L3.1 » |
| 11 | 562 | 2.3.10 Catégorie 4 — L4.3 | « Interface web responsive, licence EUPL 1.2 » |
| 12 | 564 | 2.3.10 Catégorie 4 — L4.4 | « Licence EUPL 1.2 » |
| 13 | 566 | 2.3.10 Catégorie 4 — L4.5 | « Licence EUPL 1.2 » |
| 14 | 642 | 2.3.11 RCO13 | « publiées sous licence européenne » |
| 15 | 644 | 2.3.11 RCO13 | « publié sur npm sous licence européenne » |
| 16 | 727 | 2.4 Détail chiffrage | « Publication open source EUPL (licence, headers, documentation) | 8 j | 4 000 € » |
| 17 | 786 | 2.4 Avance projetée | « open source intégral du code applicatif et des modules techniques sous licence European Union Public Licence » |

### 1.3 Diffs avant / après

#### Diff #1 — L.36 (2.1 Synthèse)

```diff
- ...la consolidation et la publication open source des deux applications publiques (livrables L3.1 et L3.2 sous licence European Union Public Licence)...
+ ...la consolidation et la publication open source des deux applications publiques (livrables L3.1 et L3.2 sous licence MIT)...
```

#### Diff #2 — L.84 (2.2 Résultats visés)

```diff
- La mesure de ce résultat repose sur la publication du module Node.js d'extraction du moteur de calcul sur le registre npm sous licence européenne, et sur la rédaction du plan d'essaimage...
+ La mesure de ce résultat repose sur la publication du module Node.js d'extraction du moteur de calcul sur le registre npm sous licence MIT, et sur la rédaction du plan d'essaimage...
```

#### Diff #3 — L.180 (2.3.3 Bien commun numérique)

```diff
- Deuxièmement, la publication de l'intégralité du code applicatif et des modules techniques sous licence European Union Public Licence 1.2, garantissant la libre réutilisation, modification et redistribution dans le respect des conditions de la licence.
+ Deuxièmement, la publication de l'intégralité du code applicatif et des modules techniques sous licence MIT, garantissant la libre réutilisation, modification et redistribution dans le respect des conditions de la licence — choix d'une licence open source largement adoptée pour maximiser la réutilisation par des tiers publics et privés, en France et au-delà.
```

> **Note** : le paragraphe perd la mention « copyleft modéré » implicite à EUPL. MIT étant permissive (pas de copyleft), il faut le justifier explicitement par l'argument d'adoption maximale. C'est ce que fait l'ajout proposé.

#### Diff #4 — L.254 (2.3.4 Essaimage — deuxième trajectoire)

```diff
- Le module Node.js extraction du moteur (livrable L4.1), publié sur npm sous licence européenne, est l'outil technique principal d'essaimage : il permet à toute équipe technique territoriale d'intégrer le moteur de calcul Tellux dans son propre système d'information géographique.
+ Le module Node.js extraction du moteur (livrable L4.1), publié sur npm sous licence MIT, est l'outil technique principal d'essaimage : il permet à toute équipe technique territoriale d'intégrer le moteur de calcul Tellux dans son propre système d'information géographique, sans friction de licence dans les contextes français, italien, espagnol, grec ou ultramarin ciblés par le plan d'essaimage.
```

#### Diff #5 — L.268 (2.3.5 Charte data — principes 15 et 16)

```diff
- Les principes n°15 « Ouverture des algorithmes » et n°16 « Privilégier l'open source » sont respectés par la publication de l'intégralité du code applicatif sous licence européenne.
+ Les principes n°15 « Ouverture des algorithmes » et n°16 « Privilégier l'open source » sont respectés par la publication de l'intégralité du code applicatif sous licence MIT, conformément au principe de priorité open source de la Charte qui n'impose pas une famille de licences spécifique.
```

#### Diff #6 — L.391 (2.3.7 Propriété et ouverture)

```diff
- Stella Canis Majoris conserve la qualité d'auteur initial des deux applications publiques `app.html` et `mairies.html`, en cohérence avec l'historique de production préexistant à la convention FEDER. Cette qualité d'auteur n'entrave pas la réutilisation par des tiers selon la licence EUPL 1.2.
+ Stella Canis Majoris conserve la qualité d'auteur initial des deux applications publiques `app.html` et `mairies.html`, en cohérence avec l'historique de production préexistant à la convention FEDER. Cette qualité d'auteur n'entrave pas la réutilisation par des tiers selon la licence MIT.
```

#### Diff #7 — L.475 (2.3.9 Calendrier mensuel — M2)

```diff
- | M2 | Consolidation `mairies.html` finalisée ; publication open source EUPL des deux applications ; migration vers infrastructure souveraine UE ; audit de sécurité initial | L3.1, L3.2 | 35 j |
+ | M2 | Consolidation `mairies.html` finalisée ; publication open source MIT des deux applications ; migration vers infrastructure souveraine UE ; audit de sécurité initial | L3.1, L3.2 | 35 j |
```

#### Diff #8 — L.515 (2.3.10 Liste livrables — paragraphe d'introduction)

```diff
- L'engagement open source est intégral. Le code applicatif est publié sous licence European Union Public Licence (EUPL) version 1.2, à l'exception des workflows d'automatisation N8N qui bénéficient de la licence MIT pour faciliter leur reprise par d'autres écosystèmes territoriaux. Les datasets relèvent selon leur nature de la Licence Ouverte Etalab 2.0, de la Open Database Licence (ODbL), ou de la Creative Commons Attribution 4.0 (CC-BY 4.0).
+ L'engagement open source est intégral. Le code applicatif et les modules techniques sont publiés sous licence MIT, choix d'une licence open source largement adoptée et permissive qui maximise la réutilisation par des tiers publics et privés, en France et au-delà. La licence MIT est compatible avec les exigences open source de l'AAP, qui n'impose pas une famille de licences spécifique. Les datasets relèvent selon leur nature de la Licence Ouverte Etalab 2.0, de la Open Database Licence (ODbL), ou de la Creative Commons Attribution 4.0 (CC-BY 4.0).
```

> **Note** : la mention spécifique des workflows N8N en MIT disparaît mécaniquement (puisque tout passe en MIT). Le paragraphe gagne en lisibilité.

#### Diff #9 — L.548 (2.3.10 Catégorie 3 — L3.1)

```diff
- Le livrable L3.1 correspond à l'application `app.html` de cartographie électromagnétique territoriale, articulant les quatre domaines physiques sur l'ensemble de la Corse. Cette application est consolidée selon le périmètre Phase 1 strict, purgée des résidus de modules dormants, et publiée sous licence EUPL 1.2 sur les dépôts GitHub `dellahstella/tellux` et Codeberg `dellahstella/tellux` en miroir européen.
+ Le livrable L3.1 correspond à l'application `app.html` de cartographie électromagnétique territoriale, articulant les quatre domaines physiques sur l'ensemble de la Corse. Cette application est consolidée selon le périmètre Phase 1 strict, purgée des résidus de modules dormants, et publiée sous licence MIT sur les dépôts GitHub `dellahstella/tellux` et Codeberg `dellahstella/tellux` en miroir européen.
```

#### Diff #10 — L.550 (2.3.10 Catégorie 3 — L3.2)

```diff
- Le livrable L3.2 correspond à l'application `mairies.html` outillant les communes corses dans l'exercice de leurs prérogatives Loi Abeille. Cette application comprend un sélecteur des trois cent soixante communes corses, quatre onglets opérationnels, six modèles de courriers institutionnels et quatre templates citoyens. Elle est publiée sous licence EUPL 1.2 selon les mêmes modalités que L3.1.
+ Le livrable L3.2 correspond à l'application `mairies.html` outillant les communes corses dans l'exercice de leurs prérogatives Loi Abeille. Cette application comprend un sélecteur des trois cent soixante communes corses, quatre onglets opérationnels, six modèles de courriers institutionnels et quatre templates citoyens. Elle est publiée sous licence MIT selon les mêmes modalités que L3.1.
```

#### Diff #11 — L.562 (2.3.10 Catégorie 4 — L4.3)

```diff
- Le livrable L4.3 est le dashboard administrateur destiné aux collectivités utilisatrices. Il permet la visualisation des contributions sur le territoire d'une collectivité donnée, la gestion des signalements citoyens, l'export de bilans synthétiques. Interface web responsive, licence EUPL 1.2.
+ Le livrable L4.3 est le dashboard administrateur destiné aux collectivités utilisatrices. Il permet la visualisation des contributions sur le territoire d'une collectivité donnée, la gestion des signalements citoyens, l'export de bilans synthétiques. Interface web responsive, licence MIT.
```

#### Diff #12 — L.564 (2.3.10 Catégorie 4 — L4.4)

```diff
- Le livrable L4.4 est le module de calibration manuelle assistée. Il fournit aux acteurs scientifiques une interface d'ajustement des constantes du modèle composite à partir des résiduals accumulés, avec traçabilité complète des modifications et historique versionné. Licence EUPL 1.2.
+ Le livrable L4.4 est le module de calibration manuelle assistée. Il fournit aux acteurs scientifiques une interface d'ajustement des constantes du modèle composite à partir des résiduals accumulés, avec traçabilité complète des modifications et historique versionné. Licence MIT.
```

#### Diff #13 — L.566 (2.3.10 Catégorie 4 — L4.5)

```diff
- Le livrable L4.5 est l'ensemble des connecteurs et API d'intégration au SPDIAC. Il comprend une API REST documentée selon le standard OpenAPI 3.0, des connecteurs spécifiques pour le SIG jumeau numérique de la Corse mentionné dans la délibération 2026E1009, et la spécification technique des formats d'échange. Licence EUPL 1.2.
+ Le livrable L4.5 est l'ensemble des connecteurs et API d'intégration au SPDIAC. Il comprend une API REST documentée selon le standard OpenAPI 3.0, des connecteurs spécifiques pour le SIG jumeau numérique de la Corse mentionné dans la délibération 2026E1009, et la spécification technique des formats d'échange. Licence MIT.
```

#### Diff #14 — L.642 (2.3.11 Indicateurs RCO13)

```diff
- Les services numériques produits comprennent deux applications publiques consolidées et publiées sous licence européenne (`app.html`, `mairies.html`), cinq modules techniques nouveaux librement réutilisables, vingt-quatre livrables structurés (datasets, documentation, corpus scientifique), et l'intégration native au Service Public de la Donnée et de l'IA de la Corse.
+ Les services numériques produits comprennent deux applications publiques consolidées et publiées sous licence MIT (`app.html`, `mairies.html`), cinq modules techniques nouveaux librement réutilisables, vingt-quatre livrables structurés (datasets, documentation, corpus scientifique), et l'intégration native au Service Public de la Donnée et de l'IA de la Corse.
```

#### Diff #15 — L.644 (2.3.11 Indicateurs RCO13 — argument essaimage)

```diff
- ...La valeur produite bénéficie de fait à un nombre d'acteurs économiques nettement supérieur à un projet de transformation numérique d'entreprise classique. Le module Node.js d'extraction du moteur de calcul (livrable L4.1), publié sur npm sous licence européenne, est par exemple réutilisable par tout système d'information géographique territorial existant en France et au-delà.
+ ...La valeur produite bénéficie de fait à un nombre d'acteurs économiques nettement supérieur à un projet de transformation numérique d'entreprise classique. Le module Node.js d'extraction du moteur de calcul (livrable L4.1), publié sur npm sous licence MIT, est par exemple réutilisable par tout système d'information géographique territorial existant en France et au-delà.
```

#### Diff #16 — L.727 (2.4 Détail chiffrage des prestations Tellux)

```diff
- | Publication open source EUPL (licence, headers, documentation) | 8 j | 4 000 € |
+ | Publication open source MIT (licence, headers, documentation) | 8 j | 4 000 € |
```

#### Diff #17 — L.786 (2.4 Avance projetée — Premier engagement)

```diff
- Premier engagement : open source intégral du code applicatif et des modules techniques sous licence European Union Public Licence, garantissant l'inclusion et l'équité d'accès au-delà du périmètre du projet.
+ Premier engagement : open source intégral du code applicatif et des modules techniques sous licence MIT, garantissant l'inclusion et l'équité d'accès au-delà du périmètre du projet, choix d'une licence permissive maximisant l'adoption par des tiers en France et à l'international.
```

---

## 2. Révision 5.2 — Nuance hébergement Supabase

### 2.1 Localisation des passages à modifier

Trois passages du dossier mentionnent Supabase. Le passage principal à reformuler intégralement est dans la sous-section 2.3.7 (Souveraineté). Deux passages secondaires nécessitent un alignement de cohérence.

| # | Ligne | Section | Statut |
|---|---|---|---|
| A | 310 | 2.3.6 Stack applicative | Imprécision factuelle à corriger |
| B | 367 | 2.3.7 Souveraineté | **Reformulation principale demandée par l'audit** |
| C | 204 | 2.3.3 Durabilité post-FEDER | Mention secondaire à aligner sur B |

### 2.2 Diff principal — L.367 (2.3.7 Souveraineté)

**Formulation actuelle** :

> La migration depuis l'infrastructure actuelle de Tellux Corse (Cloudflare Pages et Supabase, dont l'entité juridique mère relève du droit étatsunien) vers l'infrastructure souveraine UE est inscrite dans le périmètre du projet, à exécution en mois deux du calendrier d'exécution. Cette migration est documentée techniquement et auditable : elle inclut l'export complet des données, la migration des configurations, la vérification de l'intégrité, la bascule effective des noms de domaine, et le décommissionnement des ressources étatsuniennes.

**Formulation reformulée intégralement** (suit la consigne du prompt « migration du backend depuis Supabase (entité juridique américaine, instance hébergée actuellement en eu-west-1 Irlande) vers un opérateur souverain européen pleinement soumis au droit européen, en mois deux du projet, avec audit juridique de la conformité au CLOUD Act ») :

```diff
- La migration depuis l'infrastructure actuelle de Tellux Corse (Cloudflare Pages et Supabase, dont l'entité juridique mère relève du droit étatsunien) vers l'infrastructure souveraine UE est inscrite dans le périmètre du projet, à exécution en mois deux du calendrier d'exécution. Cette migration est documentée techniquement et auditable : elle inclut l'export complet des données, la migration des configurations, la vérification de l'intégrité, la bascule effective des noms de domaine, et le décommissionnement des ressources étatsuniennes.
+ L'infrastructure actuelle de Tellux Corse présente une situation de souveraineté hybride qui motive la migration prévue au mois deux du projet. Le frontend statique est servi par Cloudflare Pages depuis un CDN mondial dont l'entité juridique mère, Cloudflare Inc., relève du droit étatsunien ; les pages servies en Europe transitent toutefois par des nœuds européens. Le backend opérationnel est porté par Supabase, dont l'entité juridique mère, Supabase Inc., relève également du droit étatsunien, et dont l'instance utilisée par Tellux est hébergée actuellement en région `eu-west-1` (Dublin, Irlande, Union européenne) — l'infrastructure technique est donc localisée dans l'Union, mais l'éditeur du service reste soumis à la juridiction américaine, ce qui inclut le CLOUD Act.
+
+ La migration prévue en mois deux du projet vise à substituer à cette configuration hybride une infrastructure pleinement souveraine au sens du droit européen. Concrètement, le backend opérationnel est migré depuis Supabase vers un opérateur souverain européen pleinement soumis au droit européen — articulation prioritaire avec la plateforme d'hébergement souveraine du SPDIAC mentionnée dans le rapport délibératif 2026E1009, à défaut un opérateur tiers européen qualifié (OVHcloud SecNumCloud, Scaleway, Outscale ou équivalent). Cette migration est encadrée par un audit juridique de la conformité au CLOUD Act, conduit en début de projet, qui caractérise l'exposition résiduelle de la situation actuelle, valide la conformité européenne de la cible, et trace les modalités de bascule.
+
+ Le périmètre opérationnel de la migration inclut l'export complet des données, la migration des schémas et configurations, la vérification de l'intégrité, la bascule effective des noms de domaine, et le décommissionnement des ressources hébergées par des éditeurs étatsuniens. La portabilité technique est intégrale : Supabase étant bâti sur PostgreSQL et PostGIS, standards ouverts maîtrisés par tout administrateur compétent, aucun verrou propriétaire ne contraint la migration.
```

### 2.3 Diff secondaire A — L.310 (2.3.6 Stack applicative)

L'imprécision actuelle (« Supabase actuelle, hébergée sur entité étatsunienne ») confond deux choses : l'éditeur (entité juridique américaine) et l'instance (hébergée en Irlande UE). À aligner sur la nuance introduite en 2.3.7.

```diff
- Le backend opérationnel est porté par Supabase, une plateforme open source bâtie sur PostgreSQL avec extensions PostGIS pour les données géographiques, et offrant Row Level Security pour la conformité RGPD. La configuration Supabase actuelle, hébergée sur entité étatsunienne, est migrée en mois deux du projet vers une infrastructure souveraine UE équivalente, conformément à la sous-section 5.7 (Souveraineté). PostgreSQL et PostGIS étant des standards ouverts maîtrisés par tout administrateur compétent, la portabilité est intégrale.
+ Le backend opérationnel est porté par Supabase, une plateforme open source bâtie sur PostgreSQL avec extensions PostGIS pour les données géographiques, et offrant Row Level Security pour la conformité RGPD. L'instance Supabase actuelle, opérée par Supabase Inc. (entité juridique américaine) sur une infrastructure technique hébergée en région `eu-west-1` (Dublin, Irlande, Union européenne), est migrée en mois deux du projet vers une infrastructure pleinement souveraine au sens du droit européen, conformément à la sous-section 5.7 (Souveraineté). PostgreSQL et PostGIS étant des standards ouverts maîtrisés par tout administrateur compétent, la portabilité est intégrale.
```

### 2.4 Diff secondaire C — L.204 (2.3.3 Durabilité post-FEDER)

Mention secondaire à aligner avec la nuance introduite en 2.3.7. Pas de reformulation lourde, juste précision de la cible.

```diff
- Troisième garantie : l'hébergement souverain UE en clôture du projet. La migration depuis Cloudflare et Supabase vers infrastructure souveraine UE, exécutée en mois deux du projet, garantit que les services restent disponibles dans le cadre réglementaire européen, indépendamment d'évolutions politiques transatlantiques. L'articulation avec la plateforme d'hébergement du SPDIAC, financée par la Collectivité de Corse, mutualise les coûts de maintenance d'infrastructure.
+ Troisième garantie : l'hébergement pleinement souverain au sens du droit européen en clôture du projet. La migration depuis Cloudflare Pages et Supabase (dont les éditeurs sont des entités juridiques américaines même lorsque les instances techniques sont localisées en Union européenne) vers une infrastructure soumise au seul droit européen, exécutée en mois deux du projet, garantit que les services restent disponibles dans le cadre réglementaire européen, indépendamment d'évolutions politiques transatlantiques et du CLOUD Act. L'articulation prioritaire avec la plateforme d'hébergement du SPDIAC, financée par la Collectivité de Corse, mutualise les coûts de maintenance d'infrastructure.
```

### 2.5 Vérification de cohérence avec 2.3.5 (RGPD) et 2.3.10 (datasets)

**Sous-section 2.3.5 (Cadre éthique — Protection des contributeurs)** : pas d'incohérence détectée. La sous-section ne mentionne pas Supabase nommément ; elle parle de pseudonymisation, agrégation, droits RGPD. La nuance introduite en 2.3.7 ne contredit rien dans 2.3.5.

**Sous-section 2.3.10 (Liste des livrables — colonne Hébergement du tableau l.348-358)** : le tableau mentionne « `data.corsica` + miroir consortium UE », « Hébergement souverain UE restreint, accès agrément », « Hébergement consortium puis `data.corsica` ». Aucune mention Supabase dans ce tableau. Pas d'incohérence à signaler.

**Mention résiduelle L.683 (2.3.11 RCR11)** : « Au moins cinquante contributions citoyennes terrain validées (...), mesurées via la base Supabase du projet ». Cette mention parle de la base actuelle au moment de la mesure ; elle deviendra factuellement caduque après migration. À l'intégration, le rédacteur peut soit conserver la formulation (la base est Supabase au moment de la rédaction), soit la généraliser : « mesurées via la base de contributions du projet ». Recommandation : généraliser pour pérennité du dossier au-delà de M2.

```diff
- Au moins cinquante contributions citoyennes terrain validées et intégrées au modèle d'auto-affinage en clôture, mesurées via la base Supabase du projet et stratifiées par domaine physique, par zone géographique, et par profil de contributeur.
+ Au moins cinquante contributions citoyennes terrain validées et intégrées au modèle d'auto-affinage en clôture, mesurées via la base de contributions du projet et stratifiées par domaine physique, par zone géographique, et par profil de contributeur.
```

---

## 3. Note de fin — synthèse des changements à appliquer

### 3.1 Actions à conduire en passe de relecture sur `DOSSIER_PRECANDIDATURE_FINAL.md`

**Révision 5.1 — EUPL → MIT** :
- Appliquer 17 diffs textuels (cf. section 1.3).
- Pour les 5 diffs qui justifient la bascule (#3, #4, #5, #8, #17), conserver les arguments rédactionnels ajoutés (« licence permissive », « adoption maximale », « réutilisation par des tiers publics et privés ») — ils servent l'argumentaire d'essaimage et de bien commun.
- Vérifier le fichier `LICENSE` du dépôt GitHub : déjà en MIT côté observable, donc cohérence acquise.
- Vérifier que la mention spécifique « workflows N8N en MIT » de la l.515 est bien retirée par la reformulation du diff #8 (puisque tout passe en MIT).

**Révision 5.2 — Nuance Supabase** :
- Appliquer la reformulation principale en 2.3.7 (diff B sur l.367) : passage de quatre paragraphes structurés autour de l'audit CLOUD Act.
- Appliquer le diff secondaire A en 2.3.6 (l.310) pour aligner sur la nuance.
- Appliquer le diff secondaire C en 2.3.3 (l.204) pour cohérence post-FEDER.
- Appliquer la généralisation L.683 (2.3.11 RCR11) pour pérennité du dossier au-delà du mois 2.

**Volumétrie estimée** : ~20 modifications ponctuelles, dont une reformulation majeure (paragraphe Supabase 2.3.7). Charge de travail estimée : 30-45 minutes en relecture concentrée, plus relecture de cohérence finale.

### 3.2 Actions à conduire dans des fichiers connexes (hors `DOSSIER_PRECANDIDATURE_FINAL.md`)

**Sur `FEDER_OS1_2_DOSSIER_CONSOLIDE_2026-05-01.md`** : ce document de travail mentionne EUPL et MIT comme deux options en analyse comparative (l.306-309 : « Recommandation : EUPL pour cohérence souveraineté UE et alignement narratif FEDER. Alternative : MIT pour simplicité maximale. »). Cette analyse devient obsolète une fois la décision prise. Soit le document est archivé en l'état (trace de la décision), soit une note est ajoutée en tête : « Décision prise le 2026-05-01 : MIT retenue. Voir `DOSSIER_PRECANDIDATURE_FINAL.md` pour la formulation finale. » Recommandation : option archive avec note de tête, pour préserver la trace historique du raisonnement.

**Sur la page Transparence du site public (`transparence.html`)** : la nouvelle section « Cadres éthiques de référence » du livrable 2 mentionne MIT comme licence actuelle du code. Cohérence acquise — pas de modification supplémentaire requise.

**Sur la landing (`index.html`)** : la nouvelle section « Inscription territoriale » du livrable 1 ne mentionne pas la licence du code. Pas de modification supplémentaire requise.

---

## 4. Incohérences détectées hors périmètre (sans correction d'autorité)

En lisant le dossier pour les révisions 5.1 et 5.2, plusieurs points de cohérence interne méritent d'être signalés à Soleil pour décision en passe de relecture séparée. Ces points ne sont **pas corrigés** dans le présent livrable conformément à la règle stricte du prompt.

### 4.1 Variation rhétorique sur le caractère novateur

- **L.32 (2.1 Synthèse)** affirme : « Elle constitue à ce jour le **premier référentiel territorial électromagnétique intégré pour la Corse** ».
- **L.72 (2.2 Caractéristiques structurantes)** affirme : « **premier référentiel territorial EM intégré** pour la Corse ».
- **L.218-220 (2.3.4 Caractère novateur)** atténue : « **À la connaissance des porteurs du projet**, aucun outil n'articule à ce jour les quatre domaines physiques EM (...) sur un territoire français à l'échelle régionale. »

La revendication « premier référentiel » est portée explicitement dans le dossier institutionnel, mais le prompt audit-D1 demande de **ne pas l'utiliser sur la landing publique** (formulation prudente « Aucun équivalent open et intégré n'existe à ce jour pour ce territoire » à conserver). À noter pour cohérence narrative landing/dossier : la communication publique reste prudente, la candidature institutionnelle peut assumer la revendication. C'est défendable mais demande une attention si l'audit FEDER lit les deux supports en miroir.

### 4.2 Calendrier 6 mois vs étalement 24 mois

- **L.32 (2.1 Synthèse)** : « Le projet se déploie sur **six mois** ».
- **L.602-611 (2.3.10 Calendrier agrégé)** : tableau sur **6 mois**, M1 à M6, avec livrables associés.
- **L.529 (2.3.10 Catégorie 1)** : « première version aux **mois trois, six et neuf** du projet, version stabilisée au mois quinze, version finale enrichie au mois **vingt-quatre** ».
- **L.617 (2.3.10 Calendrier agrégé)** : « Le projet est conçu pour un calendrier de production étalé sur les **vingt-quatre mois** du projet, avec des jalons trimestriels ».

**Incohérence factuelle** : le projet est annoncé sur 6 mois en 2.1 et 2.3.10 calendrier agrégé tableau, mais le tableau lui-même mentionne « vingt-quatre mois » dans son paragraphe d'introduction et plusieurs livrables ont des jalons à M9, M15, M24. Probable confusion entre calendrier d'exécution FEDER (6 mois) et calendrier de cycle de vie complet du projet (24 mois post-démarrage avec embargo et levée). À clarifier explicitement par Soleil : « 6 mois d'exécution FEDER, puis 18 mois post-FEDER de pérennité avec engagement de levée d'embargo en M21 ».

### 4.3 Périmètre exclu vs revendication d'essaimage

- **L.124-130 (2.3.1 Périmètre exclu)** : « les modules thématiques connexes (patrimoine mégalithique, agronomie EM, dimension bâtiment et urbanisme) (...) sont conservés dormants pour la phase de financement présente. »
- **L.256 (2.3.4 Essaimage — troisième trajectoire)** : « Les modules nouveaux développés dans le cadre du projet (auto-affinage par crowdsourcing scientifique, dashboard administrateur, calibration manuelle assistée) sont publiés en open source et **réutilisables par tout projet de cartographie environnementale collaborative, électromagnétique ou non**. »

Pas une incohérence stricte, mais une zone de tension : le périmètre exclu Phase 1 mentionne que les modules thématiques restent dormants, alors que l'essaimage troisième trajectoire évoque la réutilisation par des projets « non-EM ». À ne pas confondre — le dossier le fait correctement, mais la formulation gagnerait peut-être à préciser que l'essaimage non-EM concerne les modules techniques génériques (auto-affinage, dashboard) et non les modules thématiques dormants.

### 4.4 Consortium — composition prévisionnelle floue

- **L.32 (2.1 Synthèse)** : « partenaires complémentaires éventuels » et « selon configuration finale du consortium ».
- **L.443-454 (2.3.8 Composition prévisionnelle)** : non lue intégralement dans ce sprint, mais signalée pour relecture par Soleil.
- **L.32** mentionne « une commune corse en qualité de territoire pilote pour `mairies.html` et une institution scientifique partenaire pour le volet auto-affinage » — formulation conditionnelle qui peut affaiblir l'argumentaire si elle est répétée en fin de dossier sans précision sur la situation effective au moment du dépôt. À vérifier en passe de relecture finale.

### 4.5 Mention `tellux.corsica` à arbitrer

- **L.596 (2.3.10 Catégorie 7 L7.3)** : « acquisition et la mise en service d'un domaine `.corsica`, conformément à l'engagement explicité au paragraphe IV du cahier des charges (...). Le domaine cible est `tellux.corsica`, **sous réserve de disponibilité**. »

Cohérent avec le prompt audit-D1 qui dit « Pas de mention du domaine `tellux.corsica` non encore acquis » côté communication publique. Le dossier institutionnel peut l'assumer en livrable contractuel — mais la formulation « sous réserve de disponibilité » est prudente et probablement à conserver.

---

**Fin du livrable 3.**
