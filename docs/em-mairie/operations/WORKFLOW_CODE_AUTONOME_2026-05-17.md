# Doctrine workflow Code autonome avec vérifs preview CF

**Date** : 2026-05-17
**Statut** : acté Soleil
**Référence** : PR `refactor/pieves-2026-05-17`

---

## Workflow merge Code autonome (depuis 2026-05-17)

Claude Code opère en mode autonome sur le cycle push → preview Cloudflare → PR → merge. La validation passe par les vérifications fonctionnelles sur la preview CF, pas par un acquittement Soleil systématique.

### Étapes

1. `git push origin <branche>` après vérifications locales (tests JSON valides, smoke tests scripts si applicable, console serveur local propre).
2. Attendre que Cloudflare Pages termine le build preview (~1-3 min). URL preview accessible via dashboard CF ou GitHub PR check.
3. Vérifications sur la preview CF :
   - pages canoniques (`index.html`, `app.html`, `patrimoine.html`) chargent sans erreur console ;
   - fonctionnalité touchée par la PR opère correctement ;
   - aucune régression visible sur les pages non touchées.
4. Ouvrir la PR avec rapport synthétique (commits, phases, dettes, tests effectués).
5. Merger sur la branche cible (dev ou main) après preview green.
6. Supprimer la branche source post-merge.

### Confirmation Soleil OBLIGATOIRE uniquement pour

- Opérations destructrices irréversibles (force-push, suppression de branches non mergées, reset --hard sur branche partagée).
- Premier merge sur main d'une PR qui touche le périmètre EM scientifique : modifications de fonctions `calc*`, coordonnées GPS, formules zone GELÉE (`EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, `calcGammaAmbient`).
- Toute déviation par rapport au plan documenté de la session.

### Règle « je-ne-sais-pas » MAINTENUE

Tout état imprévu (build CF échoue, console errors inattendus, comportement divergent, divergence git inattendue, conflit non résolu, commits anonymes) → STOP, signaler à Soleil, ne pas merger.

---

## Note

Cette doctrine annule l'ancienne règle « merge avec confirmation explicite obligatoire dans le chat avant chaque merge » documentée précédemment.

Le `.claude/CLAUDE.md` local de chaque worktree est mis à jour avec une section pointant vers ce document. Le fichier `.claude/CLAUDE.md` reste gitignored par convention (cf. ADR-001 §implicite : configuration locale Claude Code, non versionnée).
