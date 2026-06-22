---
name: capitalisation-retro-s11
description: >-
  Capitalisation RÉTROACTIVE d'un chantier clos avant l'existence du PROTOCOLE §11 (ou dont
  la capitalisation a été oubliée à la clôture). Produit ce que §11 aurait généré à la
  clôture (décisions ADR / skills / patterns) dans un draft, sans re-recherche ni écriture
  canonique. À utiliser quand un chantier clos n'a pas été capitalisé. Déclencheurs :
  capitalisation rétroactive, §11, back-fill, chantier clos, ADR oublié, amorçage,
  patterns rencontrés. Adossé au PROTOCOLE §11 et à CHARTE_DECISION (crans A/B/C).
---

# capitalisation-retro-s11 — Back-fill de la capitalisation §11

Produit, pour un chantier déjà clos, ce que la capitalisation §11 aurait généré à la clôture :
décisions, skills et patterns. **Capitalisation, pas re-recherche.** Tout reste **proposition**
(adoption canonique = Cran C). (Adossé au PROTOCOLE §11 + CHARTE_DECISION.)

## Quand l'utiliser
Un chantier a été clos **avant** l'existence du PROTOCOLE §11, ou sa capitalisation a été
oubliée à la clôture, et on veut récupérer ses acquis sans rouvrir la recherche.

## Procédure
1. **Lire les sources de clôture** du chantier : SYNTHESE + feedback(s) + contrat +
   RAPPORT_FINAL. Ne rien lire d'autre comme source d'acquis.
2. **Extraire** trois blocs, chaque entrée **rattachée à une ligne précise** d'une source :
   - **§11.1 Décisions** — au format ADR (numéros provisoires à partir du prochain libre),
     confrontées à l'existant `DECISIONS.md` pour éviter le doublon ; statut proposé `Candidat` ;
   - **§11.2 Skills** — procédures réutilisables (déclencheur + esquisse + rattachement) ;
   - **§11.3 Patterns / anti-patterns** rencontrés.
3. **Produire** `_drafts/CAPITALISATION_RETRO_<chantier>.md` avec :
   - un **en-tête de conformité** (les fichiers gouvernance lus, le mode défaut-action tenu) ;
   - un **digest d'arbitrage Cran C groupé** en fin de fichier (un seul passage).
4. **Statut** : les candidats restent des **propositions**. Aucune écriture canonique
   (`DECISIONS.md`, création de skill, mention publique) sans GO (Cran C).

## Garde-fous
- **Zéro invention** : chaque entrée porte un `[rattachement]` à une ligne de source ; rien
  d'extrapolé.
- **Aucune écriture canonique sans GO** : la sortie va dans `_drafts/` (vérifier le chemin
  gitignored avant écriture) ; l'adoption en `DECISIONS.md` / la création de skill / toute
  mention publique sont du Cran C.
- **Confidentialité** : si le chantier porte un volet dormant/confidentiel, la sortie reste
  en `_drafts/` gitignored, sans mention de financement en cours ni exposition du contenu.
- **0 guillemet courbe** dans la sortie.

## Sortie
Un fichier `_drafts/CAPITALISATION_RETRO_<chantier>.md` : en-tête conformité + §11.1/§11.2/§11.3
rattachés + digest Cran C. Candidats = propositions ; adoption canonique = Cran C.
