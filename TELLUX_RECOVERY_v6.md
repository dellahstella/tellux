# TELLUX — Document de reprise (Recovery v6)

**Date :** 13 avril 2026
**Usage :** Fournir à tout nouveau chat/session le contexte minimum pour reprendre le travail sans perte.

---

## Code — Source de vérité

**Fichier canonique :** `tellux_CORRECT.html`
Ce fichier est la seule référence pour le code en production. Toute modification doit être faite dans ce fichier ou y être reportée en fin de session.

**Fichier de travail :** `tellux_v6_design.html` — contient les derniers ajouts (module géométrie, orientation astrale) qui doivent encore être reportés dans `tellux_CORRECT.html`.

**Taille :** ~7 000 lignes, monofichier HTML/CSS/JS. Stack : Leaflet, Supabase JS, vanilla JS. Pas de framework, pas de bundler.

---

## Infrastructure

| Service | URL / Référence | État |
|---|---|---|
| Hébergement | Cloudflare Pages — `tellux.pages.dev` | Actif |
| Backend | Supabase PostGIS — `knckulwghgfrxmbweada` | Actif, 3 migrations |
| Git | GitHub `dellahstella/tellux.git` — branches `main` + `dev` | Nettoyé 13 avril |
| Mirror | GitLab (synchro auto) | À vérifier Soleil |
| Backup Supabase | `SupaData-backup/` (7 tables CSV) | Export session 4 |

**⚠️ Pas Netlify.** L'ancien miroir Netlify n'est plus maintenu. Cloudflare Pages est le seul hébergement actif.

---

## Dernières sessions (résumé)

| Session | Date | Contenu principal |
|---|---|---|
| 5 — Flux mesure | 10 avril | 3 bugs Supabase + FAB mini-menu + prescription + audit |
| 6 — Épistémique | 12 avril | Position épistémique créée, 5 dossiers réécrits, 3 erreurs corrigées |
| Sonnet Patrimoine | 13 avril | Audit 116 sites, module géométrie avancée, orientation astrale, migration 003 |
| Sonnet Contexte | 13 avril | Mise à jour roadmap, recovery, instructions, nettoyage fichiers |

---

## Ce que la prochaine session doit savoir

1. **Reporter le module géométrie** de `tellux_v6_design.html` vers `tellux_CORRECT.html` (~600 lignes : CSS, HTML panneaux, JS 21 fonctions, SITES_ORIENTATION, modifications SITES.forEach).
2. **Section 3.0 du roadmap** est un placeholder `[À COMPLÉTER SESSION 14 AVRIL]` pour les finitions UX pré-envoi EM.
3. **Position épistémique** : lire `TELLUX_POSITION_EPISTEMIQUE.md` avant toute rédaction. Ne jamais écrire "deux réalités différentes", "les mesures ne s'additionnent pas", "naturel = bénin".
4. **Règle L.rectangle** : tout `L.rectangle` doit avoir `interactive:false`.
5. **Règle FAB** : le FAB doit appeler `startContribFromFAB()`, avec `map.once` dans `setTimeout(0)`.

---

*Documents de référence : `TELLUX_ROADMAP.md`, `PROJECT_INSTRUCTIONS.md`, `DIRECTION_ARTISTIQUE_v2.md`*
