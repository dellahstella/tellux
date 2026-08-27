# Suivi des briefs — Tellux

Fichier créé le 2026-08-27 (brief "3 corrections UI menu EM", point 4, décision Soleil).

**But** : que le suivi des briefs envoyés par Soleil survive à la fermeture d'une session de
chat — consultable par n'importe quelle session future (Claude Code ou une prochaine
conversation Claude), sans dépendre de la mémoire de conversation ni d'une relecture manuelle.

**Portée** : non rétroactif. Ne couvre que les briefs reçus **à partir du 2026-08-27**, pas
l'historique de session antérieur (traçable par ailleurs via `git log`/PR GitHub pour tout ce
qui a produit du code).

**Règle de mise à jour** : Code met à jour ce fichier à chaque réception de brief (nouvelle
ligne, statut `reçu`) et à chaque clôture (statut mis à jour). Ne pas laisser un brief sans
ligne correspondante ici, y compris ceux qui n'aboutissent à aucune action (`sans suite
assumée` — avec la raison).

**Statuts possibles** : `reçu` (pas encore commencé) · `en cours` · `traité` (avec lien
PR/commit si applicable) · `bloqué` (avec la raison et ce qui débloquerait) · `sans suite
assumée` (avec la raison — ex. décision de ne pas donner suite, doublon, hors scope).

## Briefs

| Date | Résumé | Statut |
|---|---|---|
| 2026-08-27 | 3 corrections UI menu EM (doublon panneau "?"/légende RF, retrait intro "Contexte naturel", badge "Mesures EM" trompeur) + mise en place de ce suivi (point 4) | traité (partiel, assumé) — points 2 et 3 faits intégralement. Point 1 : fermeture améliorée (croix + Échap) faite, mais duplication/positionnement PAS résolus — Soleil veut garder le panneau "?" pour des légendes sélectives par couche, décision reportée à une consultation avec chat (autres facteurs à considérer). Point 1 reste une ligne ouverte tant que cette décision n'est pas prise — voir aussi commentaire en l'état dans app.html (bloc `@media (max-width:768px)` autour de `#legende`). |
| 2026-08-27 | GPS "Plage d'Albu" mal placé (~8,7 km d'erreur, signalé par Soleil après mise en ligne de #1059) | traité — PR #1061 mergée (corrigé dans sites_app.json + sites_corse.json deprecated) |
| 2026-08-27 | Afficher un appel à mesure (pas de valeur inventée) sur les 3 sites ophiolitiques Corse pour les rendre actionnables | traité — PR #1062 mergée (conflit avec #1063 sur LEGEND_HTML['crustal'] résolu en faveur du retrait au moment du merge, cf. ligne suivante — rien perdu, contenu déjà dans le popup par marqueur) |
| 2026-08-27 | Panneau "?" sélectif par couche active (triage : forêt dense + anomalies mondiales retirées, fond magnétique régional compacté, RF/Mesures EM gardés, gamma citoyen différé) + fix urgent chevauchement bouton fermeture/sélecteur fond de carte + audit "Module le calcul" (RF/Composite) | traité — PR #1063 mergée. Point A implémenté et vérifié en live (dont le fix urgent, repro capture Soleil confirmée puis résolue) ; point B = rapport d'audit livré ([RAPPORT_BADGE_MODULE_CALCUL_2026-08-27.md](RAPPORT_BADGE_MODULE_CALCUL_2026-08-27.md)), aucun changement de badge implémenté (gate = recherche seulement). Note de guidage créée pour les 3 fils reportés ([NOTE_GUIDAGE_LEGENDES_ARCHITECTURE_2026-08-27.md](NOTE_GUIDAGE_LEGENDES_ARCHITECTURE_2026-08-27.md)). Conflit avec #1062 résolu en faveur du retrait au merge de #1062. |
| 2026-08-27 (antérieur, redécouvert à la clôture) | Bug #2 — bloc légende cross-onglets mobile | **jamais traité explicitement** — probablement résolu en effet de bord de la refonte nav mobile (#1050), mais jamais confirmé/vérifié directement. Ne PAS considérer comme résolu tant qu'une vérification dédiée n'a pas été faite. |
| 2026-08-27 (antérieur, redécouvert à la clôture) | Bug #3 — bandeau KP/Réseau/Live/Orage qui disparaît ou se comporte mal au scroll | **jamais traité** — jamais reproduit en repro (condition de déclenchement non identifiée). Bloqué faute de repro, pas résolu. |
| 2026-08-27 (antérieur, redécouvert à la clôture) | Bloc glossaire sous la carte — hypothèse de doublon avec `.glossary-drawer` | **jamais traité** — hypothèse posée, jamais vérifiée (pas confirmée, pas infirmée). |
| 2026-08-27 (antérieur, redécouvert à la clôture) | Disparition des points Corse sur "Anomalies de référence (mondiales)" | **⚠️ CORRECTION à la clôture — ce point a en réalité été traité en profondeur dans cette même session**, contrairement à la prémisse du brief de clôture (rédigé avant/sans tenir compte de ce travail). Investigation complète faite : la couche "Anomalies de référence (mondiales)" (b-crustal) n'a jamais eu de points en Corse (5 sites mondiaux fixes depuis sa création le 2026-04-23) — confusion de nommage avec sa voisine "Anomalies de substrat", retirée le 2026-08-20 (#998). Diagnostic donné avec citations exactes (commits/PR/dates). Suite à ce diagnostic : réintégration décidée par Soleil de 3 sites Corse réels dans b-crustal (PR #1059), GPS d'un de ces sites corrigé après signalement (PR #1061), et ajout d'un appel à mesure sur ces 3 sites (PR #1062) — les trois mergées. **Statut réel : traité et clos**, pas "en attente". |
| 2026-08-27 | Brief de clôture de session (piste "forêt générateur", confirmation des 4 points ci-dessus, état repo) | traité — piste "forêt générateur" notée dans le corpus privé (`axe_em/niches/PISTE_FORET_GENERATEUR_ELECTRIQUE_2026-08-27.md`, commit `5759f16`), 4 points ci-dessus tracés avec statut réel (1 correction faite sur la prémisse). **État repo à la clôture — PAS entièrement propre au premier contrôle** : PR [#1056](https://github.com/dellahstella/tellux/pull/1056) ("Failles tectoniques + Émergences thermales" sur radon.html, ouverte depuis 08:01 ce même jour) traînait encore ouverte, `BEHIND` main — mise à jour (merge de main dans la branche, sans conflit), CI reverifiée verte, mergée avant de considérer la session close. Après ce merge : `main` à jour, aucune branche `claude/*` résiduelle datée du 2026-08-27. Signalé sans être traité (hors périmètre de ce brief, pré-existant) : plusieurs PR bot `intermagnet-*` (#1049/#1051/#1052/#1053/#1064) empilées ouvertes sans merge depuis le 2026-08-26, cohérent avec #934 (fix du retarget auto-merge de ce bot, ouverte depuis le 2026-07-08, jamais mergée) — probablement le même problème de fond, non résolu ; et #1034/#1035, qui semblent être des PR de première mouture pour les fonctions `calcVegetationAttenuation()`/`calcSoilConductivityEffective()` depuis supersédées par #1038/#1037 (mergées, cf. mémoire de session) — à confirmer et probablement fermer, pas fait ici. |
