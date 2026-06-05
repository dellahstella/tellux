# INVENTAIRE_VEILLE.md — Phase 0 du brief « Veille Scholar » (2026-06-04)

> Lu avec `CLAUDE.md`, `PROTOCOLE_AUTO_ITERATION.md`, et le brief Soleil « BRIEF CODE — Veille Scholar (réalisation autonome) » du 2026-06-04.
> Échéance Phase 1 : avant le cron du **lundi 8 juin 2026 8h UTC**.
> Production autonome Code, lecture seule sur Gmail et accès au clone privé `tellux-corpus-internal`.

---

## 0. Constat principal et correction du brief

Le brief mentionne en objet : *« workflow **n8n** sur Railway »*. **Le pipeline veille Scholar tourne déjà sur GitHub Actions, pas sur n8n/Railway.** Cette mémoire de coordination est obsolète et est explicitement signalée dans l'audit du 25 mai (`_corpus_veille/audits/SCHOLAR_PIPELINE_AUDIT_2026-05-25.md` §6 et §10.6, fichier vivant côté repo privé).

→ **Action implicite** : corriger ce détail dans la prochaine version du brief / mémoire de coordination. Le présent inventaire bâtit autour de la réalité GitHub Actions.

---

## 1. Pipeline existant — vue d'ensemble

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  Veille Scholar Tellux — pipeline réel                       │
│                                                                              │
│  CRON lundi 8h UTC  ──►  GitHub Actions (dellahstella/tellux)                │
│                          .github/workflows/veille_scholar.yml               │
│                          .github/scripts/veille_scholar.py                  │
│                                                                              │
│      ▼                                                                       │
│  ╔══════════════════════════════════════════════════════════════╗           │
│  ║  1. Gmail API (gmail.readonly, OAuth refresh_token)           ║           │
│  ║     filter: from:scholaralerts-noreply@google.com after:7d   ║           │
│  ║     cible: tellux.veille@gmail.com                            ║           │
│  ╚══════════════════════════════════════════════════════════════╝           │
│      ▼                                                                       │
│  ╔══════════════════════════════════════════════════════════════╗           │
│  ║  2. Fetch prompt veille depuis repo PRIVÉ                     ║           │
│  ║     dellahstella/tellux-corpus-internal                       ║           │
│  ║     docs/pilotage/prompt_veille_tellux_v2.md (19 836 bytes)   ║           │
│  ╚══════════════════════════════════════════════════════════════╝           │
│      ▼                                                                       │
│  ╔══════════════════════════════════════════════════════════════╗           │
│  ║  3. Synthèse via Anthropic API                                ║           │
│  ║     modèle: claude-sonnet-4-5  /  max_tokens: 8192            ║           │
│  ║     INPUT  : prompt + N emails (sujet, date, body texte)      ║           │
│  ║     OUTPUT : markdown synthèse                                ║           │
│  ╚══════════════════════════════════════════════════════════════╝           │
│      ▼                                                                       │
│  ╔══════════════════════════════════════════════════════════════╗           │
│  ║  4. Commit dans repo PRIVÉ via API GitHub (PAT)               ║           │
│  ║     _corpus_veille/syntheses/synthese_YYYY-MM-DD.md           ║           │
│  ║     preflight GET pour SHA si fichier existe (idempotence)   ║           │
│  ╚══════════════════════════════════════════════════════════════╝           │
│      ▼                                                                       │
│  ╔══════════════════════════════════════════════════════════════╗           │
│  ║  5. (best-effort) Note d'intégration corpus                   ║           │
│  ║     prompt: docs/pilotage/prompt_integration_corpus.md       ║           │
│  ║     commit: _corpus_veille/integrations/note_integration_*.md│           │
│  ╚══════════════════════════════════════════════════════════════╝           │
│      ▼                                                                       │
│  ╔══════════════════════════════════════════════════════════════╗           │
│  ║  6. (best-effort) Issue GitHub privée                         ║           │
│  ║     [veille] Synthèse + intégration — YYYY-MM-DD              ║           │
│  ╚══════════════════════════════════════════════════════════════╝           │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Inventaire détaillé (ce qui existe)

### 2.1 Workflow GitHub Actions

| Champ | Valeur |
|---|---|
| Fichier | `.github/workflows/veille_scholar.yml` (61 lignes) |
| Nom | `Veille Scholar hebdomadaire` |
| Workflow ID | 274093367 (per audit 2026-05-25) |
| Trigger principal | `schedule: '0 8 * * 1'` — chaque lundi 8h UTC (~9h Paris hiver / 10h été) |
| Trigger manuel | `workflow_dispatch` avec inputs : `lookback_days` (défaut 7), `dry_run` (défaut 0) |
| Runner | `ubuntu-latest`, timeout 10 min |
| Steps | `actions/checkout@v5` → `setup-python@v6` (3.12) → pip install (google-auth-oauthlib, google-auth-httplib2, google-api-python-client, anthropic, requests) → `python .github/scripts/veille_scholar.py` |
| Statut | actif (5 synthèses produites en mai-juin) |

### 2.2 Script Python

| Champ | Valeur |
|---|---|
| Fichier | `.github/scripts/veille_scholar.py` (468 lignes) |
| Filtre Gmail | `from:scholaralerts-noreply@google.com after:YYYY/MM/DD` (alerte-agnostique : ingère TOUS les Scholar Alerts sans distinguer la requête source) |
| Modèle Claude | `claude-sonnet-4-5` (variable `ANTHROPIC_MODEL`) |
| Max tokens | 8192 |
| Repo cible synthèse | `dellahstella/tellux-corpus-internal` (privé, variable `PRIVATE_REPO`) |
| Output synthèse | `_corpus_veille/syntheses/synthese_YYYY-MM-DD.md` |
| Output intégration | `_corpus_veille/integrations/note_integration_YYYY-MM-DD.md` (best-effort) |
| Idempotence | preflight GET pour SHA si fichier existe → mode UPDATE ; sinon CREATE (correctif post-incident 2026-05-25 cron+manuel le même matin) |
| Notification | issue GitHub dans le repo privé liant synthèse + intégration |

### 2.3 Auth Gmail OAuth

| Élément | Valeur |
|---|---|
| Compte | `tellux.veille@gmail.com` |
| Scope | `https://www.googleapis.com/auth/gmail.readonly` (lecture seule, conforme au garde-fou du brief) |
| App GCP | `tellux-veille-github-actions` |
| Statut GCP | **Production** (confirmé audit 2026-05-25 — Soleil a publié l'app pour éviter la ré-expiration 7j du token Testing) |
| Secrets GitHub Actions | `GMAIL_REFRESH_TOKEN`, `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET` (last update 2026-05-10) |
| Procédure refresh | `.github/scripts/refresh_oauth_token.py` (162 lignes) — outillé, documenté |
| Procédure Soleil | fichier temp `~/.tellux_oauth_temp.json` → script lance flow OAuth local → upload via `gh secret set` (stdin, jamais arg CLI) → suppression temp |

### 2.4 Anthropic API

| Élément | Valeur |
|---|---|
| Secret | `ANTHROPIC_API_KEY` (last update 2026-05-11) |
| Modèle | `claude-sonnet-4-5` |
| 2 appels par run | étape 3 synthèse (8192 tokens) + étape 5 intégration best-effort (8192 tokens) |

### 2.5 GitHub PAT (commit repo privé)

| Élément | Valeur |
|---|---|
| Secret | `GH_PATH` (renommé du `GITHUB_PAT` car le préfixe `GITHUB_` est réservé par GitHub Actions) — mappé sur env var `GITHUB_PAT` côté script |
| Scope requis | `repo` sur `dellahstella/tellux-corpus-internal` |
| Usage | GET prompt veille + GET prompt intégration + PUT synthèse + PUT intégration + POST issue notification |

### 2.6 Prompts veille (clone privé)

| Fichier | Taille | Dernière modif | Usage |
|---|---:|---|---|
| `docs/pilotage/prompt_veille_tellux_v2.md` | 19 836 b | 2026-05-17 | Synthèse hebdo (étape 3) |
| `docs/pilotage/prompt_veille_tellux_v1.md` | 13 683 b | 2026-05-17 | Archive v1 (non utilisé par le script v2) |
| `docs/pilotage/prompt_integration_corpus.md` | 14 815 b | **2026-06-03** | Note d'intégration corpus (étape 5) — mis à jour très récemment |
| `docs/pilotage/note_synthese_exemple.md` | 26 651 b | 2026-05-17 | Référence de format pour la synthèse |
| `docs/pilotage/COWORK_MENAGE_2026-05-09_pour_*.md` | — | 2026-05-17 | Archives Cowork |

### 2.7 Outputs déjà produits (clone privé, 30 derniers jours)

**Synthèses** (`_corpus_veille/syntheses/`) :
- `synthese_2026-05-11.md` (cycle 2)
- `synthese_2026-05-25.md` (rattrapage post-fix OAuth)
- `synthese_2026-06-01.md` (cycle 5 scheduled)
- `synthese_2026-06-02.md` (manuel)
- `synthese_2026-06-03.md` (manuel)

**Intégrations** (`_corpus_veille/integrations/`) :
- `note_integration_2026-06-*.md` (2 fichiers, juin)
- `COWORK_LECTURE_BEN_ISHAI*` (lecture papier — flow Cowork distinct)

**Extractions historiques** (`_corpus_veille/extractions/`) :
- `scholar_alerts_2026-04-28*.md` (2 fichiers)
- `scholar_alerts_2026-04-30*.md`
- `scholar_alerts_batch4.md` à `batch6b.md`
- `scholar_alert_2026-05-06.md`
→ Pré-pipeline (avril–mai) : extractions manuelles, remplacées depuis par les synthèses pipeline.

### 2.8 Outil anti-Frankenstein (existant, **NON câblé dans la veille**)

| Élément | Valeur |
|---|---|
| Fichier | `scripts/verify_citation.py` (résolveur Crossref + bioRxiv + PubMed + Semantic Scholar + scrape HTML, ~840 lignes selon `wc -l` non vérifié) |
| Dépendances | stdlib uniquement (urllib, json, argparse, re) — Python 3.10+ |
| Registre | `scripts/citations_registry.json` |
| Tests | `scripts/test_verify_citation.sh` (6 tests primaires, tous PASS attendu) |
| Doc | `scripts/README.md` (162 lignes) — workflow Cowork + workflow évaluateur §10 documentés |
| Référent | `PROTOCOLE_AUTO_ITERATION.md` §10 (gate citations) |
| **Statut veille** | **Pas appelé** par `.github/scripts/veille_scholar.py`. Utilisé en post-traitement par les chantiers recherche (Cowork) sur les livrables produits, pas en amont sur les références veille. |

---

## 3. Inventaire alertes Scholar (côté Gmail)

Le brief annonce *« 4 requêtes Scholar »*. L'inventaire Gmail (lecture seule, échantillon de 50 threads sur 90 jours via MCP `search_threads`) révèle **au moins 10 requêtes numérotées**, dont **7 actives observées** dans les 90 derniers jours :

| # | Domaine (déduit du sujet) | Vue récemment ? | Échantillon de hit |
|--:|---|:--:|---|
| **1** | RF-EMF exposure (`"radiofrequency exposure" OR "RF-EMF" OR ...`) | ✓ 2026-06-04 | Workers' Exposure Due to Private 5G Networks (Telecom 2026) |
| **2** | Multi-EMF (`"radiofrequency" OR "ELF" OR "electromagnetic"`) | ✓ 2026-05-31 | DOM fluorescence sensors (off-topic visible) |
| **3** | Radon (`radon AND (mapping OR modeling OR lithology)`) | ✓ 2026-05-19 | Indoor & outdoor radiological hazards |
| **4** | ELF/50Hz (`"ELF magnetic field" OR "power frequency" OR "50 Hz"`) | ✓ 2026-05-29 | Cardiac Rhythms Shape Brain Oscillations |
| **5** | — | ✗ silence sur 90j | — |
| **6** | Gamma terrestre (`"terrestrial gamma radiation" OR "background"`) | ✓ 2026-05-29 | Yield of Salsola & Suaeda + Tamil Nadu radiological hazards |
| **7** | Non-thermal (`"non-thermal" AND "electromagnetic"`) | ✓ 2026-05-23 | Nano-Bio Systems Terahertz |
| **8** | — | ✗ silence sur 90j | — |
| **9** | — | ✗ silence sur 90j | — |
| **10** | Géomagnétisme (`"geomagnetic" OR "IGRF" OR "magnetic anomaly"`) | ✓ 2026-06-03 | Sea Turtles magnetic sensing / Lohmeyer satellites |

**Décalage brief vs réalité** : le brief annonce « 4 requêtes ». La réalité montre **10 requêtes numérotées dont 7 actives + 3 silencieuses (#5, #8, #9)**. L'audit Cowork 2026-05-25 mentionnait 6 actives et 4 silencieuses (#2, #5, #8, #9) — la #2 s'est réveillée depuis (vue 2026-05-31).

→ **Interprétation probable du brief** : Soleil prévoit de **réécrire les 3-4 requêtes silencieuses** (#5, #8, #9 — éventuellement #2 si elle a déjà été réécrite). Côté Code, pas d'action sur les requêtes elles-mêmes.

**Aucun label utilisateur Gmail dédié à la veille.** Le pipeline filtre uniquement sur `from:scholaralerts-noreply@google.com`. Aucune création/suppression de label par le script. Conforme au garde-fou du brief (Gmail lecture seule, pas de règle/filtre persistant).

---

## 4. Audit récent disponible (référence)

`SCHOLAR_PIPELINE_AUDIT_2026-05-25.md` dans le clone privé (`_corpus_veille/audits/`, 18 455 bytes, mis à jour 2026-06-03 — fichier vivant). Ce document est la **source de référence** sur :
- §1-2 : localisation pipeline (GitHub Actions, pas n8n)
- §3 : pipeline alerte-agnostique (filtre Gmail unique)
- §4 : historique runs jusqu'au 2026-05-18 (1 fail OAuth)
- §5 : cause racine fail = refresh token OAuth expiré (app Testing 7j)
- §6 : cohérence audit Cowork ↔ pipeline (mémoire « n8n » à corriger)
- §7 : plan de réparation (Option A Production / Option B regen token)
- §10 : recommandation finale
- §11 : commandes utiles (gh CLI)
- §12 : procédure refresh OAuth outillée (script `.github/scripts/refresh_oauth_token.py`)

Cet audit a été produit **avant** la résolution du fail. La résolution est **acquise depuis** (5 synthèses produites en mai-juin, dont une dans la fenêtre post-fix 2026-05-25 et trois en juin).

---

## 5. Gaps identifiés par le brief vs existant

Mapping brief Phase 1 ↔ état pipeline :

| # | Brief Phase 1 | État pipeline | Gap ? |
|--:|---|---|---|
| 1 | **Ingestion Gmail lecture seule** | ✓ `gmail.readonly`, filtre `from:scholaralerts-noreply@google.com`, parse subject/date/body | ✓ aucun gap |
| 2 | **Dédup / filtrage par pertinence d'axe** | délégué au prompt Claude, **pas de code explicite** | ⚠️ **gap structurel** — le prompt fait le tri narrativement, mais aucune dédup hash/canonique côté code |
| 3 | **Tag par axe (agronomie / EM / bâtiment)** | délégué au prompt | ⚠️ **gap structurel** — pas de structure machine-readable (JSON, frontmatter), tout en prose |
| 4 | **Pré-qualification via `verify_citation.py`** | `verify_citation.py` existe mais **non câblé** dans la veille | ⚠️ **gap clair** — opportunité de durcir en amont |
| 5 | **Sortie : digest format à fixer** | format actuel = synthèse markdown Claude (Phase 1 §5) | ⚠️ format à arbitrer Soleil (le format actuel est-il celui qu'on veut conserver ?) |
| 6 | **Orchestration n8n/Railway OU script+cron** | déjà script + cron GitHub Actions ; n8n non utilisé | ✓ orchestration en place, n8n hors-scope |

### Gaps **non-bloquants** pour le cron du 8 juin

- §2 et §3 (dédup + tag par axe) : le prompt fait actuellement le travail de manière satisfaisante (5 synthèses produites, format stable). Une amélioration vers une structure machine-readable est un durcissement, pas un blocage. Le cron du 8 juin peut tourner sur le pipeline actuel sans cette amélioration.
- §4 (verify_citation pré-qualification) : opportunité, pas blocage. La gate §10 du protocole reste appliquée en aval sur les livrables recherche.

### Gaps **à arbitrer avec Soleil** avant Phase 1

- §5 (format digest) : faut-il un format différent de la synthèse Markdown actuelle, ou est-elle satisfaisante ? Le brief dit *« digest (format à fixer en Phase 0) »* → c'est précisément cette question.

---

## 6. Plan Phase 1 ajusté (proposé sur la base de l'inventaire)

> Ce plan est **proposé** par Code et soumis à arbitrage Soleil. La doctrine RECOMMANDE-pas-APPLIQUE s'applique : aucune modification du code de veille avant validation.

### 6.1 — Hygiène pré-cron (avant lundi 8 juin)

| Tâche | Acteur | Effort | Bénéfice |
|---|---|---|---|
| Soleil réécrit les requêtes Scholar #5, #8, #9 (et éventuellement #2) | Soleil | UI Scholar | Réveiller les 3-4 axes silencieux |
| Dry-run du pipeline (`gh workflow run veille_scholar.yml -f dry_run=1`) avant lundi pour vérifier qu'aucun warning n'est apparu depuis le dernier run | Soleil ou Code | 1 min | Validation préventive |
| Vérifier que `GMAIL_REFRESH_TOKEN` n'a pas expiré silencieusement (un dry-run le révélerait) | Code | inclus ci-dessus | Sécurité OAuth |
| **AUCUN changement de code** | Code | 0 | Stabilité avant échéance |

### 6.2 — Améliorations Phase 1 (post-cron 8 juin, si Soleil arbitre OK)

> **Hors scope avant le cron**. Construction itérative générateur ≠ évaluateur (§2 du protocole), boucle ouverte sur évaluation à partir d'emails de test.

1. **Dédup hash-based amont de Claude** (gap §2 du brief) :
   - Hash SHA-1 sur `(titre normalisé + premier auteur)` calculé côté Python avant envoi à Claude.
   - Persister un index dédup hebdomadaire dans le repo privé (`_corpus_veille/.dedup_index.json`).
   - Évite de re-soumettre à Claude un papier déjà traité (économie tokens, déterminisme).

2. **Tag par axe machine-readable** (gap §3 du brief) :
   - Soit prompt structuré demandant à Claude un YAML frontmatter en tête de synthèse (`axes: [em, agro, batiment]` par item).
   - Soit second appel Claude bref pour classifier chaque référence dans `{em, agro, batiment, off-topic}` AVANT la synthèse longue.
   - **Avantage** : permet de générer des digests par axe (filtre `axes=[em]`) sans re-parser le narratif.

3. **Pré-qualification verify_citation** (gap §4 du brief) :
   - Pour chaque référence extraite des emails Scholar, lancer `verify_citation.py` (ou import direct du module Python) sur le DOI/URL si présent.
   - Annoter chaque référence avec quadruplet vérifié + flag `verified: true/false` dans la synthèse.
   - **Coût** : 1 appel Crossref par référence (~50 réf/run, négligeable).
   - **Bénéfice** : anti-Frankenstein **en amont**, plus seulement en aval (gate §10).

4. **Format digest** (gap §5 du brief) :
   - À arbitrer après la décision §1-§3. La synthèse markdown actuelle est valide ; ajouter un index par axe en tête est l'évolution minimale.

### 6.3 — Boucle d'auto-itération (générateur ≠ évaluateur)

Application du §2 du protocole sur la construction Phase 1 :
- **Générateur** = Code (cette session ou une suivante, sur la branche `feat/veille-scholar-2026-06-08`).
- **Évaluateur** = session fraîche distincte qui teste sur un corpus de mails Scholar de référence (ex. snapshot des 20 dernières alertes captées dans Gmail), vérifie :
  - dédup correct (aucun doublon dans la synthèse)
  - tag par axe correct (taux d'erreur < 10% sur le corpus de test)
  - verify_citation passe sur toutes les DOI extraites
  - digest produit lisible et complet
- **Seuil** : 7.0 sur la rubrique §5.1 adaptée (Fonctionnalité 0.35 / Non-régression 0.30 / Craft 0.20 / Robustesse 0.15).
- **Max itérations** : 8.

---

## 7. Ce qui exige Soleil (questions ouvertes)

| # | Question | Bloquant Phase 1 ? |
|--:|---|:--:|
| Q1 | Confirmation : la mémoire « n8n sur Railway » du brief est-elle un legacy à corriger, ou un plan futur ? Si futur : pourquoi vs GitHub Actions actuel ? | non |
| Q2 | Quel est l'arbitrage sur les 4 requêtes Scholar à réécrire ? (#5, #8, #9 silencieuses + une autre ?) Si tu as déjà la liste, je peux la consigner dans l'inventaire. | non — Code ne touche pas aux requêtes |
| Q3 | Format digest final souhaité : (a) statu quo synthèse markdown Claude, (b) ajout YAML frontmatter avec tags axes, (c) JSON structuré, (d) autre ? | oui pour Phase 1 §6.2.4 |
| Q4 | Pré-qualification `verify_citation.py` : à câbler en Phase 1 ou à différer ? Cf. §6.2.3. | oui pour Phase 1 §6.2.3 |
| Q5 | Le `prompt_veille_tellux_v2.md` (19 836 b, modifié 2026-05-17) demande-t-il une révision suite aux 5 synthèses produites depuis ? Si oui, c'est Cowork (Soleil arbitre), pas Code. | non — hors scope Code |
| Q6 | Le `prompt_integration_corpus.md` mis à jour le 2026-06-03 : la note d'intégration produite par le pipeline est-elle satisfaisante, ou faut-il un autre ajustement ? Si oui, Cowork. | non — hors scope Code |

---

## 8. Récapitulatif — ce qu'il reste à câbler

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Avant lundi 8 juin 8h UTC (cron) :                                      │
│  ─ Soleil : réécriture des requêtes Scholar silencieuses (UI Scholar)    │
│  ─ Code   : dry-run préventif du workflow                                │
│  ─ Code   : AUCUN changement de code                                     │
│                                                                          │
│  Après le cron du 8 juin (si Soleil arbitre OK sur §6.2 et §7 Q3-Q4) :   │
│  ─ Code   : dédup hash-based amont Claude                                │
│  ─ Code   : tag par axe machine-readable                                 │
│  ─ Code   : pré-qualification verify_citation.py câblée                  │
│  ─ Code   : digest format ajusté selon Q3                                │
│  ─ Code   : boucle générateur ≠ évaluateur sur corpus de mails test      │
│                                                                          │
│  Hors scope Code :                                                       │
│  ─ Révision prompt_veille_v2 ou prompt_integration_corpus → Cowork       │
│  ─ Réécriture requêtes Scholar → Soleil (UI)                             │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Garde-fous appliqués pendant cet inventaire

Conformément au brief :
- ✓ Gmail interrogé en **lecture seule** via MCP `search_threads` (échantillon 50 threads sur 90 jours).
- ✓ Aucune création/modification/suppression de label Gmail.
- ✓ Aucune création/modification de règle ou filtre Gmail.
- ✓ Aucun push public, aucune PR ouverte sans validation Soleil. Cet inventaire est commité sur branche dédiée `feat/veille-scholar-2026-06-08`, en attente d'arbitrage.
- ✓ Lecture seule sur le clone privé `tellux-corpus-internal` (aucun commit pour cette Phase 0).
- ✓ Les 4 requêtes Scholar sont du ressort de Soleil — non modifiées par Code.

---

*Inventaire Phase 0 — Code, session locale 2026-06-04. À arbitrer par Soleil avant lancement Phase 1.*
