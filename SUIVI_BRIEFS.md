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
| 2026-08-27 | Afficher un appel à mesure (pas de valeur inventée) sur les 3 sites ophiolitiques Corse pour les rendre actionnables | traité — PR #1062 CI verte, en attente confirmation merge (contenu public neuf, décision de fond déjà actée en conversation directe avec Soleil après consultation chat) |
