---
name: invasivite-screen-cbnc
description: >-
  Filtre une liste d'espèces végétales pour l'invasivité (statut EEE) AVANT toute
  qualification d'aptitude ou recommandation agronomique en Corse. À utiliser dès qu'une
  liste d'espèces ou de variétés végétales doit être qualifiée pour la Corse. Déclencheurs :
  espèce, variété, invasivité, CBNC, EEE, plante envahissante, plantation, agronomie Corse,
  aptitude espèce, cahier des charges espèces. Adossé à ADR-014 (verrou d'invasivité).
---

# invasivite-screen-cbnc — Verrou d'invasivité avant toute reco d'espèce

Toute liste d'espèces végétales destinée à une qualification d'aptitude passe ce verrou
**avant** publication. Une espèce classée envahissante est exclue ; une espèce non confirmée
NON-EEE n'est jamais recommandée. (Adossé à ADR-014.)

## Quand l'utiliser
Dès qu'un livrable agronomique (cahier des charges espèces, qualification d'aptitude, liste
de candidates) propose des espèces/variétés végétales pour la Corse, et avant d'énoncer la
moindre aptitude ou recommandation.

## Procédure
1. **Entrée** : liste d'espèces en nom latin (binôme). Normaliser la nomenclature.
2. **Match** de chaque espèce contre les référentiels, dans cet ordre :
   - **CBNC 2019** (Conservatoire botanique national de Corse) — référentiel local prioritaire ;
   - **IUCN GISD** (Global Invasive Species Database) ;
   - **USDA FEIS** (Fire Effects Information System) — appui complémentaire.
3. **Statut par espèce** :
   - `EXCLU` — listée EEE Majeure : verrou fermé, retirée du livrable ;
   - `NON recommandé` — listée Alerte / émergente : signalée, non recommandée ;
   - `candidate sous réserve` — non listée : reste candidate, jamais recommandée tant que
     non confirmée NON-EEE ;
   - `indigène hors-champ EEE` — espèce indigène, hors périmètre invasivité.
4. **Blocage** : interdiction d'énoncer une aptitude/reco pour toute espèce non confirmée
   NON-EEE. Le verrou prime sur l'intérêt agronomique.

## Garde-fous
- Ne jamais recommander une espèce dont le statut d'invasivité n'est pas confirmé.
- **Toujours citer l'édition** du référentiel (ex. CBNC 2019), pas une version floue.
- En cas de divergence entre référentiels, retenir le statut le plus restrictif.
- Ce skill ne prescrit pas de plantation : il **qualifie** un statut d'invasivité (voir le
  principe « aptitude qualifiée, jamais prescription », ADR-015).

## Sortie
Un tableau espèce -> statut (parmi les 4 ci-dessus) + référentiel et édition cités. Les
espèces non confirmées NON-EEE sont explicitement marquées comme non recommandables.
