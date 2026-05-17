# ADR-001 — Doctrine pièves Tellux

**Statut** : acté
**Date** : 2026-05-17
**Auteur** : Soleil (arbitrage), rédaction Cowork
**Remplace** : aucun (premier ADR sur le sujet)
**Contexte amont** : audit 47 pièves prod du 2026-05-17 (N1→D3), brief Cowork du même jour

---

## 1. Contexte

Tellux embarque actuellement, dans `docs/data/pieves_polygons.json`
(v3-stratA-canonicite-casta), **47 pièves** rattachées à 5 diocèses médiévaux
(Ajaccio, Aleria, Mariana, Sagone, Nebbiu) et à 9 doyennés contemporains.
Le rendu se fait dans `patrimoine.html` selon un drill-down doyenné → pieve.

L'audit du 17 mai 2026 a remonté quatre niveaux d'écarts :

- bugs nets (stats faussées, mojibake, champs manquants, entrée fantôme) ;
- incohérences de nommage (préfixe « Pieve di » à 8/47, collisions slug ↔
  diocèse pour 4 entrées, slugs reprenant des noms de villes modernes) ;
- découpages asymétriques (Balagne 46 communes, Filosorma 3 communes, dans
  le même doyenné) ;
- trois reclassifications polygonales forcées (`pieve_bastia`, `pieve_verde`,
  `pieve_vivario`), signal d'un mapping commune→pieve partiellement contredit
  par la géométrie réelle.

Avant de patcher au coup par coup, il faut acter **ce qu'est une pieve dans
Tellux** — et ce qu'elle n'est pas. Sans cette ligne, chaque renommage
ouvrirait un débat d'érudition.

## 2. Décision

### 2.1 Position doctrinale

**Tellux n'est pas un atlas Casta strict.**

Tellux est une application de cartographie territoriale destinée en premier
lieu à un public mixte (CTC, associations, agronomes, grand public corse) ;
la précision médiévale n'est pas un objectif en soi, et l'orthodoxie
historique cède devant la lisibilité géographique et pédagogique.

Le corpus Casta reste **référence informative**, pas tribunal de validation.
Quand le découpage Casta produit un objet illisible pour l'utilisateur final
(une pieve de 46 communes à côté d'une pieve de 3, des noms qui collisionnent
avec un diocèse parent, des libellés à diacritiques cassés), Tellux peut
s'en écarter, à condition de documenter l'écart.

### 2.2 Définition opératoire d'une pieve Tellux

> **Une pieve Tellux est une région géographique cohérente intra-doyenné,
> utilisée comme maille de navigation pédagogique entre la commune et le
> doyenné, dotée d'un nom lisible et stable.**

Conséquences directes :

- la pieve est un **objet de carto**, pas un objet d'érudition ;
- son périmètre doit être géographiquement contigu et reconnaissable ;
- son nom doit être lisible sans glossaire (breadcrumb, popup, hash URL) ;
- sa population de sites attendue est de l'ordre de 5 à 30 ; en dehors de
  cette plage, c'est un signal de redécoupage à examiner (pas une obligation
  immédiate, voir 2.4).

### 2.3 Rôle du diocèse médiéval

Le diocèse médiéval **devient une métadonnée informative** portée par chaque
pieve (`diocese_medieval`), affichable en popup pour contextualiser, mais
**plus un niveau de navigation primaire**. La hiérarchie de nav Tellux est :

```
Commune → Pieve (région cohérente) → Doyenné (contemporain)
```

Le diocèse médiéval n'apparaît pas dans le breadcrumb ni dans les hash
d'URL. Il reste dans les fiches détaillées et peut être exposé en couche
optionnelle (mode Expertise) si le besoin se confirme post-FEDER.

### 2.4 Critères de nommage des pièves

Par ordre de priorité :

1. **Lisibilité** : un nom qu'un Corse non historien reconnaît immédiatement.
2. **Géographie d'abord** : si un toponyme géographique (vallée, microrégion,
   plaine, golfe) couvre le territoire, on le préfère au nom diocésain.
3. **Pas de collision** avec un slug de diocèse ou de doyenné.
4. **Cohérence** : préfixe `Pieve di` uniformément retiré du `name` affiché
   (les slugs portent déjà `pieve_*`).
5. **Charge historique acceptée si non équivoque** : un nom médiéval reste
   le bienvenu (Bozio, Orezza, Nebbiu) tant qu'il ne crée pas de confusion.

Les noms de villes modernes utilisés comme noms de pieve (Bastia, Bonifacio,
Ajaccio) sont **à reconsidérer**, soit par renommage (toponyme régional),
soit par redéfinition de leur périmètre.

### 2.5 Stabilité des hash d'URL

Les slugs `pieve_*` actuellement exposés dans des URL communiquées
(candidatures, communications associations, partages publics) sont
considérés comme **partiellement publics**. Tout renommage d'un slug
existant doit :

- soit conserver un **alias de redirection** côté `patrimoine.html` (mapping
  ancien slug → nouveau slug appliqué au `applyHash` initial) ;
- soit attendre la **refonte post-FEDER** si l'alias coûte trop.

Aucun renommage ne casse silencieusement un lien public déjà partagé.

## 3. Conséquences

### 3.1 Sur les données

- `pieves_polygons.json` doit pouvoir évoluer en plusieurs passes sans
  reconstruction complète du mapping commune→pieve. Le pipeline
  `build_pieves_polygons.py` doit rester re-exécutable.
- `sites_patrimoine.json` doit suivre tout renommage de slug via retag.
- Un fichier d'alias `pieve_aliases.json` est à introduire pour préserver
  les hash URL.

### 3.2 Sur les arbitrages futurs

- Les renommages **R1 à R5** de l'audit sont arbitrables au cas par cas ;
  l'érudition seule ne suffit plus à les justifier ou les refuser.
- Le redécoupage **D2** (Balagne mégalithique) reste différé post-FEDER :
  on assume l'asymétrie en Phase 1 beta.
- Les collisions slug ↔ diocèse (R4) sont prioritaires : elles touchent
  la lisibilité du drill-down.

### 3.3 Sur la communication

- Quand un appel public ou une candidature mentionne le découpage Tellux,
  on dit « pièves » entre guillemets ou « régions Tellux », jamais
  « pièves médiévales canoniques ».
- Une note méthodologique sera ajoutée à `patrimoine.html` (popup info ou
  about) pour expliciter que Tellux suit Casta en référence informative,
  pas en autorité.

## 4. Choix non arbitrés ici

Cet ADR ne tranche pas :

- les renommages concrets (cf. `PIEVES_REFACTOR_PLAN_2026-05-17.md`) ;
- le sort exact de `pieve_mariana` (cf. plan, 3 options) ;
- le redécoupage Balagne / Cap (déféré post-FEDER) ;
- la question Nebbiu (mini-diocèse à 1 pieve, à discuter Phase 2).

## 5. Révision

Cet ADR est **stable** pour la Phase 1 beta Tellux (cartographie EM publique
+ patrimoine en accès direct non lié). Il sera réouvert si :

- une publication scientifique externe impose un alignement Casta strict ;
- une décision FEDER conditionne un financement à un découpage différent ;
- l'usage utilisateur fait émerger un troisième niveau de nav.

---

**Référence** : audit 2026-05-17, niveau N1→D3.
**Fichiers dérivés** :
- `docs/operations/PIEVES_REFACTOR_PLAN_2026-05-17.md`
- `docs/operations/PIEVES_REFACTOR_EXEC_CODE_2026-05-17.md`
