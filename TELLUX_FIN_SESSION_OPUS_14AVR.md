# Tellux — Rapport de fin de session Opus 14 avril 2026

**Date :** 14 avril 2026
**Auteur :** Sonnet (session nettoyage post-Opus)

---

## 1. Audit d'etat initial

| Fichier | Valeur attendue | Valeur observee | Statut |
|---|---|---|---|
| `tellux_CORRECT.html` lignes | ~7625 | 7511 (working dir) / 7634 (git HEAD) | ⚠️ voir note |
| Features presentes | 4 | 6 occurrences (OK) | OK |
| `SITES_REFERENCE.json` sites | 112 | 112 | OK |
| Sites audites | 49 | 49 | OK |

**Note :** le working dir contient une version modifiee par l'outil Edit de la session Cowork A-4b (trailing whitespace supprime, 2 fonctions manquantes dans le diff). La version git HEAD (7634 lignes, commit `8fdc705`) est correcte et contient les 4 corrections A-4b. Soleil doit travailler a partir de git HEAD, pas du working dir actuel.

---

## 2. Inventaire fichiers projet

### Fichiers actifs (a conserver)

| Fichier | Categorie | Statut |
|---|---|---|
| `tellux_CORRECT.html` | code | Source de verite |
| `index.html` | code | Copie de tellux_CORRECT pour Cloudflare |
| `SITES_REFERENCE.json` | config | 112 sites, 49 audites |
| `DIRECTION_ARTISTIQUE_v2.md` | doc-active | DA gelee |
| `PROJECT_INSTRUCTIONS.md` | config | A completer (§1 bis, §3 bis manquants) |
| `TELLUX_ROADMAP.md` | roadmap | Date 13 avril, a mettre a jour |
| `ROADMAP_COURT_TERME.md` | roadmap | Cree le 13 avril |
| `TELLUX_RECOVERY_v6.md` | recovery | Cree le 13 avril |
| `WORKFLOW_GIT.md` | config | Procedures Git |
| `TELLUX_POSITION_EPISTEMIQUE.md` | doc-active | Document fondateur |
| `TELLUX_DOSSIER_ASSO_EM.md` | dossier-partenaires | Reecrit session 6 |
| `TELLUX_DOSSIER_AGRO_BIO.md` | dossier-partenaires | Reecrit session 6 |
| `TELLUX_DOSSIER_MAIRIES_PATRIMOINE.md` | dossier-partenaires | Reecrit session 6 |
| `TELLUX_DOSSIER_SCIENTIFIQUES.md` | dossier-partenaires | Modifie session 6 |
| `TELLUX_KIT_ENVOI_EM.md` | dossier-partenaires | Aligne session 6 |
| `TELLUX_AUDIT_A4B.md` | doc-active | Audit couches, session 14 avril |
| `TELLUX_AUDIT_CORPUS_SITES.md` | doc-active | Audit 116 sites, session 13 avril |
| `TELLUX_AUDIT_FLUX_MESURE.md` | doc-active | Audit mesure, session 5 |
| `TELLUX_AUDIT_INFRASTRUCTURE.md` | doc-active | Audit infra, session 4 |
| `TELLUX_AUDIT_MODELE.md` | doc-active | Audit modele scientifique |
| `TELLUX_TEST_FLUX_MESURE.md` | doc-active | Scenarios de test |
| `TELLUX_SESSION_2026-04-14.md` | doc-active | Recap session Opus |
| `TELLUX_MONTEE_EN_GAMME.md` | doc-active | Plan voie B |
| `TELLUX_FINANCEMENT.md` | doc-active | Strategie subventions |
| `TELLUX_STRUCTURE_JURIDIQUE.md` | doc-active | Comparatif juridique |
| `TELLUX_GUIDE_FICHES_PATRIMOINE.md` | doc-active | Guide B-VISITES |
| `TELLUX_LOGO_V7.html` | asset | Logo SVG |
| `Hypothese.json` | config | Hypotheses testables |
| `failles_corse.json` | config | Failles geologiques |
| `prod-electrique.json` | config | Sites production |
| `_migrations/001-003` | config | Migrations Supabase |
| `contactassoEM.pdf` | asset | Contact associations |

### Suggestions de suppression (doublons et obsoletes)

| Fichier | Justification |
|---|---|
| `tellux.html` | Ancienne version v5.9, remplacee par `tellux_CORRECT.html` |
| `tellux_v6_design.html` | Branche de travail, tout reporte dans `tellux_CORRECT.html` |
| `TELLUX_BRIEFING.md` | Remplace par `PROJECT_INSTRUCTIONS.md` + `TELLUX_RECOVERY_v6.md` |
| `TELLUX_SAUVEGARDE.md` | Remplace par `TELLUX_RECOVERY_v6.md` |
| `TELLUX_SESSION4_SYNTHESE.md` | Contenu integre dans le roadmap |
| `TELLUX_SESSION6_SYNTHESE.md` | Contenu integre dans le roadmap |
| `session_2026-04-08.md` | Notes de session ponctuelles, perimees |
| `TELLUX_WORKFLOW_VERSIONS.md` | Remplace par `WORKFLOW_GIT.md` |
| `TELLUX_VEILLE_DESIGN_NARRATION.md` | Pre-DA v2, plus utilise depuis le gel design |
| `failles-corse.json` | Doublon de `failles_corse.json` (tiret vs underscore) |
| `_prompts_code_claude/AUDIT_DECOUPE_HTML.md` | Prompt one-shot execute, plus necessaire |

**Total : 11 fichiers a archiver ou supprimer.**

### Fichiers attendus mais manquants

| Fichier | Commentaire |
|---|---|
| `CANDIDATURE_TELLUX_v7.docx` | Probablement sur le disque local de Soleil, pas dans le repo Git |
| `Modellogo_optimal.png` | Idem — asset local |
| `TELLUX_CORPUS_COMPLET_v6.md` | Jamais cree dans le Project. A generer si necessaire |
| `TELLUX_HYPOTHESES_COMPLET.md` | Jamais cree. Les hypotheses sont dans `Hypothese.json` |

---

## 3. Validation regles de conduite

### PROJECT_INSTRUCTIONS.md

| Section | Present | Commentaire |
|---|---|---|
| §1 HTML canonique | Oui | |
| §1 bis audit d'etat | **Non** | Posee en session Opus 14 avril, pas encore ajoutee |
| §2 economie de tokens | Oui | |
| §3 workflow modification code | Oui | |
| §3 bis deploiement explicite | **Non** | Posee en session Opus 14 avril, pas encore ajoutee |
| Garde-fous domaine | Partiel | Manque : Monte d'Oro, ratio heritage/electrique, Unicode, figures humaines |
| Choix modele | Oui | |
| Candidature CTC | Oui | |
| Refus systematiques | Oui | |

**Action requise :** ajouter §1 bis, §3 bis, et completer les garde-fous domaine dans `PROJECT_INSTRUCTIONS.md`.

### TELLUX_ROADMAP.md

| Point | Conforme | Commentaire |
|---|---|---|
| Date mise a jour | 13 avril | A passer au 14 avril apres ajout B-CLUSTER/B-ZONES |
| Voie A = livraison immediate | Oui | |
| Voie B = montee en gamme | Oui | |
| B-CLUSTER | **Non** | Ajoute en session Opus, pas dans le roadmap |
| B-ZONES | **Non** | Idem |
| Section 3.0 finitions EM | Oui (placeholder) | |
| Agenda S16+ | Oui | |

### SITES_REFERENCE.json

Validation structurelle : **OK**. IDs sequentiels, champs obligatoires presents, bornes Corse respectees, types valides, 112 sites, 49 audites.

---

## 4. Verification Git

Branche courante : `dev`. Dernier commit : `8fdc705 fix(ux): audit A-4b couche↔panneau↔légende — 4 corrections`.

49 fichiers dirty dans le working directory (modifications Cowork non commitees). `main` est en avance sur `dev` avec les merge commits de la session Opus. Le commit attendu `resolve: index.html = dev version (disclaimer GPS)` est present sur `main`.

**Rappel pour Soleil :**
- `dev` et `main` doivent etre synchronises sur `origin` apres commit des fichiers dirty
- `tellux_CORRECT.html` et `index.html` doivent etre identiques sur les deux branches
- `SITES_REFERENCE.json` a 112 sites sur les deux branches

---

## 5. Tickets ouverts consolides

| ID | Ticket | Source | Priorite | Voie | Proprietaire |
|---|---|---|---|---|---|
| A-1g | GPS sites restants (partiellement fait : 49/112 audites, 25 megalithiques non trouves en ligne) | Roadmap + Session 14avr | 🟡 | A | Soleil (terrain) |
| A-4b | Audit couches ↔ panneau ↔ legende | Roadmap | 🟡 | A | **Fait** (session Cowork 14avr, 4 fixes) |
| A-8 | Captures HD pour dossier CTC | Roadmap | 🟡 | A | Soleil |
| 3.0 | Finitions UX pre-envoi EM (placeholder) | Roadmap §3.0 | 🔴 | A | Opus |
| PI-1 | Ajouter §1 bis et §3 bis dans PROJECT_INSTRUCTIONS.md | Session 14avr | 🟡 | A | Cowork |
| PI-2 | Completer garde-fous domaine (Monte d'Oro, Unicode, etc.) | Session 14avr | 🟡 | A | Cowork |
| RM-1 | Ajouter B-CLUSTER et B-ZONES dans TELLUX_ROADMAP.md | Session 14avr | 🟡 | A | Cowork |
| ERR-1 | Erreurs console `loadAnt: Failed to fetch` | Session 14avr | 🟡 | A | Opus |
| ERR-2 | Erreurs console `orientation contributions: Failed to fetch` | Session 14avr | 🟡 | A | Opus |
| GPS-1 | 25 sites megalithiques non trouves dans sources web | Session 14avr | 🟢 | A/terrain | Soleil |
| GPS-2 | 6 sites non-megalithiques ambigus | Session 14avr | 🟢 | A | Soleil |
| S-1 | Arbitrage structure juridique | Roadmap §6 | 🟡 | transversal | Soleil |
| B-CLUSTER | Clustering contributions (Leaflet.markercluster) | Session 14avr | 🟢 | B | Cowork |
| B-ZONES | Representation polygonale sites etendus | Session 14avr | 🟢 | B | Cowork |
| B-EGL | Audit GPS 314 eglises romanes | Session 14avr | 🟢 | B | Cowork |

**Total : 15 tickets. 1 fait (A-4b). 1 bloquant envoi EM (3.0). 8 avant depot CTC. 5 voie B ou terrain.**

---

## 6. Recommandations prochaine session

1. **Priorite immediate :** completer `PROJECT_INSTRUCTIONS.md` avec §1 bis, §3 bis et garde-fous manquants, puis ajouter B-CLUSTER et B-ZONES dans `TELLUX_ROADMAP.md`. Tache rapide Cowork/Sonnet.

2. **Avant envoi EM :** remplir la section 3.0 du roadmap (finitions UX). Necessite une session Opus dediee pour identifier et corriger les textes d'interface.

3. **Attention working dir :** le `tellux_CORRECT.html` dans le working dir est legerement altere (7511 vs 7634 lignes). Soleil devrait faire `git checkout HEAD -- tellux_CORRECT.html` pour restaurer la version propre avant tout commit.

4. **Git cleanup :** 49 fichiers dirty dans le working dir, nombreuses branches orphelines (`fix/mesure-bugs-bloquants`, `fix/mesure-umesla-csv`, `staging-clean`, `claude/silly-kilby`). Un nettoyage Git serait utile avant le gel voie A.
