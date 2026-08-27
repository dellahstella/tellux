# Note de guidage préparatoire — légendes, badges, architecture (2026-08-27)

Note préparatoire, pas un brief. Objectif : garder le fil conducteur de plusieurs chantiers
ouverts ce jour-là mais explicitement reportés, pour qu'une session future (Code ou Soleil) les
reprenne sans perdre le contexte. Rien ici n'est à implémenter tel quel — c'est un point de
départ, pas une spec.

## 1. Panneau "?" — état après le 2026-08-27 et piste "décharger sur le corpus"

**État atteint ce jour** (brief "Panneau '?' sélectif") : le panneau "?" consolide maintenant
Champ magnétique composite, Champ électrique RF, Mesures EM et Fond magnétique régional
(compacté à une ligne) — Forêt dense et Anomalies mondiales n'ont plus aucune légende nulle
part (redondant avec title=/popup au clic). Gamma citoyen explicitement laissé de côté (la
donnée au point n'est pas visible sans clic, pas de légende utile tant que ça n'est pas réglé —
chantier séparé, pas ouvert).

**Piste évoquée par Soleil, pas développée** : plutôt que d'empiler du texte de légende dans le
panneau "?", décharger une partie de cette information vers le corpus (liens qui renvoient aux
sections correspondantes des textes du corpus, une fois la réécriture du corpus faite). Deux
questions à trancher plus tard, pas maintenant :

- Quel corpus exactement — cadre-scientifique.html (public) ? Une fiche publique dérivée du
  corpus scientifique interne ? Les deux avec un routage différent selon la profondeur d'info ?
- Quelle info reste dans le panneau "?" (repère rapide, lecture au survol) vs quelle info part
  vers le corpus (contexte, méthode, sources détaillées) ? Le panneau compact actuel
  (Fond magnétique régional, 1 ligne) est peut-être déjà proche de ce que "?" devrait
  systématiquement rester — un repère, pas une doc.

**Ne pas commencer avant la réécriture du corpus** (dépendance explicite posée par Soleil) —
mais le panneau "?" sélectif de ce jour est probablement compatible avec cette évolution
(structure déjà simplifiée, pas à défaire).

## 2. Distinction RF / Composite — implication sur les badges "calc-relevant"

L'audit du 2026-08-27 ([RAPPORT_BADGE_MODULE_CALCUL_2026-08-27.md](RAPPORT_BADGE_MODULE_CALCUL_2026-08-27.md))
a mis au jour un point qui dépasse la simple distinction calibration/entrée-directe demandée par
le brief : **pour Fond magnétique régional et Forêt dense, le toggle du bouton ne pilote pas du
tout le calcul** — le calcul les intègre en permanence sur tout clic carte, indépendamment de
l'état du bouton, qui ne contrôle que l'affichage visuel. Pour Fond magnétique régional
spécifiquement, la donnée affichée (EMAG2v3 en direct) diverge même en pratique de la donnée
réellement utilisée par le calcul (grille statique LCS1, faute d'un appel `preloadEMAG2()` qui
n'existe nulle part dans le code).

Ce constat touche directement "l'articulation avec les badges" évoquée par Soleil : avant de
choisir un nouveau libellé/badge, il faut décider si on veut aussi corriger cette
incompréhension plus profonde (le toggle n'affecte pas le calcul) ou seulement la distinction
calibration/entrée-directe demandée initialement. Les deux pistes proposées dans l'audit
(minimal vs plus complet) ne sont pas tranchées — à reprendre avec ce fil en tête, pas comme un
sujet neuf.

Rattaché aussi à la demande de "chat" de distinguer RF/composite — l'audit couvre déjà les deux
domaines (emag=composite, foretdense/con=RF) ; si "chat" a d'autres facteurs à faire remonter
sur cette distinction, les recouper avec l'audit existant plutôt que repartir de zéro.

## 3. Évolution d'architecture plus large — "ajout de carte ??"

Mentionné par Soleil comme réflexion en cours, sans détail donné : possible ajout d'une carte
supplémentaire à l'architecture du site (nature non précisée — nouvelle app dédiée type
radon.html/patrimoine.html ? Nouvelle couche sur app.html existante ? Autre chose ?). Rien à
en tirer aujourd'hui — noté ici uniquement pour que la prochaine session sache qu'un chantier
d'architecture plus vaste est en réflexion côté Soleil, et pose la question plutôt que de
supposer le périmètre si le sujet revient sans plus de contexte.

## 4. Point de vigilance — conflit connu avec PR #1062

Le retrait de `LEGEND_HTML['crustal']` (brief "Panneau '?' sélectif") a été fait sur une base
`main` antérieure à la PR [#1062](https://github.com/dellahstella/tellux/pull/1062) (appel à
mesure sites ophiolitiques, non mergée à l'écriture de cette note), qui modifiait cette même
entrée pour y ajouter une ligne d'invitation à mesure. Conflit git probable si les deux PR sont
mergées sans coordination — à résoudre en faveur du retrait (rien n'est perdu : le contenu
existe déjà dans le popup par marqueur, ajouté par #1062 dans `buildCrustalLayer()`, pas dans
`LEGEND_HTML`). Vérifier au moment de merger les deux PR que ce point a bien été traité, pas
juste résolu au hasard par git.
