# TELLUX — Recap session Claude Code du 15 avril 2026

**Session :** Claude Code (Opus 4.6) via worktree silly-kilby
**Duree :** ~4h (session longue, 12 PRs)
**Remote :** origin = GitHub (dellahstella/tellux) — unique remote actif
**Branche de travail :** dev (toutes les PRs mergees dans dev)

---

## PRs mergees dans dev (dans l'ordre)

| # | Titre | Type | Fichiers |
|---|---|---|---|
| 2 | chore: remove obsolete parallel HTML files | cleanup | -tellux_v6_design.html, -tellux.html, -tellux_CORRECT.html, -TELLUX_LOGO_V7.html |
| 3 | docs: refonte PROJECT_INSTRUCTIONS.md | docs | PROJECT_INSTRUCTIONS.md |
| 4 | feat: pre-calcul alignements megalithiques (zero lag) | perf | +_scripts/precompute_alignments.mjs, +_data/alignments_precomputed.json, +_scripts/README.md, index.html |
| 5 | fix: active-state CSS for 3 missing layer buttons | CSS | index.html (.on-radon, .on-emag, .on-wdmam) |
| 6 | docs: local test workflow + pedagogical posture | docs | PROJECT_INSTRUCTIONS.md (A.11 + B.1.bis) |
| 7 | feat: separate production electric layer from HT | feature | index.html (lProd, loadProd, b-prod) |
| 8 | chore: clean antenna debug code from production | cleanup | index.html (-101 lignes diagnostic) |
| 9 | fix: cleanup geometrie avancee selections on close | bugfix | index.html (1 ligne : clearGeomSelection au lieu de _clearGeomVisuals) |
| 10 | feat: statistical labels for geometrie avancee | feature | index.html (Monte Carlo p-value par categorie) |
| 11 | feat: restrict contributions to Corsica bbox | feature | index.html (filtre bbox dans _placeContribMarker + saveContrib) |
| 12 | fix: improve geometrie avancee statistical labels | iteration | index.html (per-detection badges, density feedback, alignments/arcs MC) |

## PR ouverte (en attente de validation Soleil)

| # | Titre | Branche | A tester |
|---|---|---|---|
| 13 | feat: contributions display + marker clustering | feat/contributions-display-and-cluster | Contributions visibles au demarrage, clusters violets, toggle, nouvelle mesure |

---

## Etat du repo apres cette session

### Fichier canonique
`index.html` a la racine — seul fichier HTML. Les 4 paralleles (tellux_v6_design.html, tellux.html, tellux_CORRECT.html, TELLUX_LOGO_V7.html) ont ete supprimes (PR #2).

### Branches locales actives
- `main` — production (behind origin/main, a synchroniser)
- `dev` — travail courant (worktree principal)
- `feat/contributions-display-and-cluster` — PR #13 en attente

### Fichiers nouveaux a connaitre
- `_scripts/precompute_alignments.mjs` — script Node pour pre-calculer les alignements
- `_data/alignments_precomputed.json` — JSON pre-calcule (15 alignements, 116 sites)
- `_scripts/README.md` — instructions pour relancer le script
- `wrangler.jsonc` — config Cloudflare Workers (assets statiques depuis racine)

### Migrations Supabase appliquees
- `001_contributions_contexte_batiment.sql` — colonnes contexte batiment (session precedente)
- `002_csv_stats.sql` — colonnes csv_stats (jsonb) + unite_saisie (text) — appliquee via MCP Supabase
- `003_orientations.sql` — table orientations_contributions (session precedente)

---

## Decisions structurelles prises dans cette session

1. **Source unique confirmee** : index.html. Plus de fichiers paralleles.
2. **Remote unique** : GitHub. GitLab deconnecte.
3. **Workflow git** : branches ephemeres -> PR vers dev -> merge manuel Soleil pour dev->main
4. **Fin economie tokens** : lire largement, verifier tout, repeter les commandes
5. **Test local obligatoire** : python -m http.server 8000 (file:// casse les fetch)
6. **Posture pedagogique** : commandes completes a chaque fois, pas de "tu connais"

## Points d'attention pour la prochaine session

1. **PR #13 a merger** : contributions display + clustering. Tester les 5 scenarios avant merge.
2. **Relancer precompute_alignments.mjs** si SITES est modifie : `node _scripts/precompute_alignments.mjs`
3. **dev -> main** : quand dev est stable et teste, creer une PR dev->main pour deployer sur tellux.pages.dev. Soleil seul merge sur main.
4. **Branches locales a nettoyer** : les branches ephemeres des PRs mergees peuvent etre supprimees (`git branch -d <branch>`). Les branches de worktree (claude/silly-kilby, fix/mesure-bugs-bloquants) seront nettoyees en sortant du worktree.
5. **Performance geometrie avancee** : les MC per-type (200 sims) peuvent ralentir sur 15+ sites. Si freeze > 3s signale par Soleil, reduire nSims a 100.

---

*Recap genere automatiquement en fin de session Claude Code du 15 avril 2026.*
