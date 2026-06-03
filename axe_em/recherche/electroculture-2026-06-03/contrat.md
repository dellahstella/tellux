# CONTRAT D'ITÉRATION — État de l'art défendable : électroculture

> Référentiel éditorial : `@CHARTE_AGRONOMIE.md`
> Lu avec `PROTOCOLE_AUTO_ITERATION.md`. Rubrique applicable : §5.3 (recherche).

```
CHANTIER  : État de l'art défendable — électroculture (cultures comestibles)
AXE       : agronomie
GÉNÉRATEUR: Cowork (tâche « générateur »)
ÉVALUATEUR: Cowork (tâche distincte « évaluateur »)
MODE ÉVAL : vérification de sources (recherche web / connecteurs) — PAS Playwright
```

## OBJECTIF (1 phrase)

Produire une synthèse **défendable** de l'état de la preuve sur l'électroculture appliquée aux cultures comestibles — distinguant clairement hypothèses, données faibles et résultats solides — et poser ce qui constituerait un **test contrôlé** valable.

## DANS LE PÉRIMÈTRE

- Histoire et **typologie** des techniques dites d'électroculture : antennes atmosphériques (ex. Christofleau, années 1920-30), électrodes/courants appliqués, champs magnétiques, traitements électrostatiques de semences, etc.
- **État réel de la preuve par technique** : littérature évaluée par les pairs, réplications, revues systématiques et méta-analyses — **y compris et surtout les résultats négatifs ou nuls**.
- **Mécanismes proposés** confrontés à leur plausibilité physique/agronomique.
- **Protocole de test contrôlé minimal** (témoin, randomisation, réplication, taille d'effet) qui validerait ou invaliderait une technique — et son articulation possible avec la boucle de science participative Tellux.

## HORS PÉRIMÈTRE

- Toute recommandation d'installation ou de pratique présentée comme **bénéfique**.
- Les autres sujets agronomie (associations végétales, design de parcelle…) → chantiers séparés.
- L'UI, le dispositif applicatif, le code.

## CRITÈRES D'ACCEPTATION

Rubrique §5.3 (Couverture 0.25 · Sources 0.25 · Citations 0.15 · Contradictions 0.15 · Défendabilité 0.20) **plus** les spécificités falsifiables :

- **Couverture** : les principales familles de techniques sont identifiées ; pour chacune, mécanisme proposé + état de preuve.
- **Sources** : priorité aux sources **primaires évaluées par les pairs** et revues récentes. Les sources commerciales, militantes ou « fringe » sont identifiées **comme telles**, pas mêlées aux sources scientifiques.
- **Citations** : chaque affirmation factuelle est sourcée et vérifiable.
- **Détection de contradictions (obligatoire)** : les résultats positifs — souvent anciens, à faible effectif — sont **confrontés** aux réplications et méta-analyses négatives. Une synthèse qui n'expose que le versant favorable est un **échec** sur ce critère, quel que soit le reste.
- **Défendabilité FEDER** (charte §4-§5) :
  - L'électroculture est présentée comme **hypothèse à tester**, jamais comme bénéfice acquis.
  - Le mot **« preuve »** est réservé à ce qui est contrôlé. « Absence de preuve » est distinguée de « preuve d'absence », mais la faiblesse de la littérature est documentée honnêtement.
  - Au moins une **revue systématique ou méta-analyse critique/négative** est citée si elle existe ; si la littérature contrôlée est rare, le dire explicitement.
  - **Échec automatique** : présenter un effet non validé comme acquis, ou qualifier de « preuve » de la donnée non contrôlée.

## PARAMÈTRES DE BOUCLE

```
SEUIL DE RÉUSSITE : 7.0 / 10 (pondéré)
MAX ITÉRATIONS    : 6
ESCALADE          : plateau (Δ < 0.3 sur 3 itérations) → stop + RAPPORT_FINAL.md
```

## ARBITRAGE SOLEIL (obligatoire après clôture méthodologique)

La boucle valide la **rigueur** ; Soleil valide la **justesse de la conclusion**. Concrètement : si la synthèse conclut « preuve majoritairement faible/non répliquée », c'est probablement le résultat honnête — mais c'est Soleil qui acte que c'est bien la position assumée dans le dossier, et comment elle se reformule en force (rigueur scientifique affichée) plutôt qu'en faiblesse.

## LIVRABLES (dossier `recherche/electroculture-2026-06-03/`)

| Fichier | Rôle |
|---|---|
| `contrat.md` | Ce contrat |
| `SYNTHESE.md` | Livrable du générateur (la synthèse) |
| `feedback-001.md`, … | Verdict évaluateur, un par cycle |
| `RAPPORT_FINAL.md` | Synthèse de clôture + protocole de test proposé + point d'arbitrage Soleil |
