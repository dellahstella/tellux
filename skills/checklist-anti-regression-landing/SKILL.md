---
name: checklist-anti-regression-landing
description: >-
  Vérifie mécaniquement une refonte de page statique (landing/HTML) AVANT clôture, pour
  attraper les régressions silencieuses d'une passe de recomposition : accents perdus
  (encodage UTF-8 dégradé), markdown non rendu (tirets bas littéraux), contenu coupé,
  liens/ancres cassés, nits de rendu, et confusion régression vs choix intentionnel.
  À utiliser à chaque édition diff-driven d'une page HTML existante (index.html, pages
  publiques). Déclencheurs : landing, refonte page, redo, recompose, régression,
  anti-régression, tirets bas, accents perdus, contenu supprimé, diff pré-redo, baseline.
  Adossé à CHARTE_DECISION (crans A/B/C) et au PROTOCOLE §11.
---

# checklist-anti-regression-landing — Baseline propre avant clôture d'une refonte HTML

Une passe de recomposition d'une page statique perd du contenu **en silence** : un outil
dégrade l'encodage, un paragraphe est raccourci, une section devient une carte. Le `git diff`
contre l'état **pré-refonte** dit exactement quoi a bougé — zéro devinette. Ce skill est la
checklist falsifiable à passer avant de déclarer la baseline propre.

## Quand l'utiliser
Toute édition d'une page HTML **existante** qui repart d'une refonte récente (le « redo ») :
correction diff-driven, restauration de contenu, baseline avant refonte Design. Pas pour une
page neuve sans antécédent.

## Procédure

1. **Établir la référence pré-refonte.** Identifier le commit du « redo » (`git log --oneline -- <page>`)
   et son parent = état pré-refonte. Toute la suite se vérifie contre `git diff <pré-refonte> HEAD -- <page>`.

2. **Encodage (l'artefact n°1).** Diff mot-à-mot : aucun accent perdu (`à→a`, `é→e`, `è→e`,
   `ê→e`…). C'est la régression la plus fréquente d'une passe d'outil, y compris dans les
   commentaires (signal qu'une passe a dégradé l'UTF-8 — vérifier alors le texte visible).

3. **Markdown non rendu.** `grep` du texte visible : aucun `_emphasis_` ni `**gras**` affiché
   littéralement. **Exclure les faux positifs** : noms de variables (`w_M`, `F_obs`),
   identifiants JS/DOM (`id="e_mag"`, `_escapeHtml`), notation scientifique (`λ_dip`).

4. **Contenu préservé.** Lire le `diff` des paragraphes : flaguer toute coupe de mots
   (« avec la même rigueur », « lignes »…), toute tuile/section supprimée, toute étiquette
   sémantique perdue (« NIVEAU 1/2/3 » → « 1/2/3 »).

5. **Liens & ancres.** Tous résolus : fichiers cibles existent ; ancres `#…` présentes dans
   la page **et** cross-page (`#section` du fichier lié existe).

6. **Rendu live (desktop + mobile).** Servir la page, vérifier : console **propre** (zéro
   erreur/warning) ; aucun chiffre/mot qui passe à la ligne de façon non voulue ; responsive
   (CTA nav, grilles qui stackent) ; états/animations fonctionnels.

7. **Régression vs intentionnel.** Avant de « restaurer », distinguer ce qui a été retiré
   **exprès** (ex. identité société d'un footer, choix de couleur CTA) — ne pas le ré-injecter.
   En cas de doute, porter au digest d'arbitrage plutôt que restaurer par défaut.

## Garde-fous
- **Le diff pré-refonte fait foi**, pas le souvenir : chaque constat « manque X » se prouve
  contre le diff, jamais « il me semble ».
- **Ne pas restaurer un retrait intentionnel** (cf. étape 7) : une suppression voulue n'est
  pas une régression.
- **Gate doctrine / §10** : tout contenu réinjecté repasse le filtre overclaim (pas de
  superlatif invérifiable réintroduit par la restauration).
- **Logger les arbitrages de forme** (placement, section vs carte) en Cran A, ou les porter
  au digest si l'ambiguïté est réelle — ne pas les trancher en silence.

## Sortie
Une baseline où chaque régression listée a été corrigée **contre le diff**, chaque retrait
intentionnel a été préservé, et le rendu live (desktop + mobile) est vérifié — prête pour
PR (Cran A/B), le merge/déploiement restant Cran C.
