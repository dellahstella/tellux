# AUDIT — Pipeline veille Scholar (GitHub Actions)

**Date** : 2026-05-25 (lundi)
**Auteur** : Claude Code (session locale Windows, repo `tellux`)
**Cadrage** : audit lecture seule de la routine GitHub Actions de veille Scholar Alerts, suite au rapport Soleil « pipeline en fail ». Aucune modification effectuée.
**Brief source** : `BRIEF CODE — Audit routine veille Scholar Alerts (pipeline GitHub Actions)` du 2026-05-25.
**Audit Cowork de référence** : `_drafts/SCHOLAR_ALERTS_AUDIT_2026-05-25.md` (cycle 3, 13 mails INBOX, filtre Gmail OK).

---

## 1. Localisation du pipeline

**Repo** : `dellahstella/tellux` (le repo public principal, pas un repo séparé).

| Composant | Chemin |
|---|---|
| Workflow GitHub Actions | `.github/workflows/veille_scholar.yml` |
| Script Python | `.github/scripts/veille_scholar.py` (258 lignes) |
| Prompt LLM (repo privé) | `docs/pilotage/prompt_veille_tellux_v2.md` dans `dellahstella/tellux-corpus-internal` (non lu ici, hors scope) |
| Output (repo privé) | `_corpus_veille/syntheses/synthese_<YYYY-MM-DD>.md` |

**Pas de repo `tellux-veille` séparé** comme le suggérait la mémoire de coordination. Tout est dans le repo public principal.

---

## 2. Inventaire workflow

| Champ | Valeur |
|---|---|
| Nom | `Veille Scholar hebdomadaire` |
| Workflow ID | 274093367 |
| Trigger 1 | `schedule: cron '0 8 * * 1'` (chaque lundi 8h00 UTC = 9h Paris hiver / 10h été) |
| Trigger 2 | `workflow_dispatch` (inputs : `lookback_days` défaut 7, `dry_run` défaut 0) |
| Runner | `ubuntu-latest` |
| Timeout | 10 min |
| Statut workflow | **active** (confirmé par `gh workflow view`) |
| Dernière modif YAML | 2026-05-12 (selon mtime local) |

### Steps
1. `actions/checkout@v4` — checkout repo public
2. `actions/setup-python@v5` (Python 3.12)
3. `pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client anthropic requests`
4. `python .github/scripts/veille_scholar.py` avec env Gmail/Anthropic/GH PAT

### Secrets GitHub Actions référencés (sans lecture du contenu)

| Secret | Mappage env | Last update |
|---|---|---|
| `GMAIL_REFRESH_TOKEN` | `GMAIL_REFRESH_TOKEN` | 2026-05-10 09:30 UTC |
| `GMAIL_CLIENT_ID` | `GMAIL_CLIENT_ID` | 2026-05-10 09:31 UTC |
| `GMAIL_CLIENT_SECRET` | `GMAIL_CLIENT_SECRET` | 2026-05-10 09:32 UTC |
| `ANTHROPIC_API_KEY` | `ANTHROPIC_API_KEY` | 2026-05-11 05:48 UTC |
| `GH_PATH` (renommé pour éviter préfixe réservé `GITHUB_*`) | `GITHUB_PAT` | 2026-05-11 06:03 UTC |

Tous les 5 secrets requis sont déclarés. La date sera importante pour le diagnostic.

---

## 3. Inventaire alertes configurées

**Conclusion clé** : **le pipeline est alerte-agnostique**. Le script (`fetch_scholar_emails`, L101-143) interroge Gmail avec une seule requête générique :

```python
SCHOLAR_FROM = "scholaralerts-noreply@google.com"
query = f"from:{SCHOLAR_FROM} after:{after_date}"
```

→ Tous les mails Scholar Alerts arrivés sur `tellux.veille@gmail.com` sont ingérés indistinctement, quelle que soit l'alerte source. **Aucun filtre côté pipeline.**

### Conséquence
- La question « inventaire alertes configurées » ne s'applique pas au pipeline.
- La liste réelle des alertes vit **uniquement** dans l'interface Scholar de Soleil (`https://scholar.google.com/scholar_alerts?view_op=list_alerts&email_for_op=tellux.veille%40gmail.com`).
- Les 4 alertes silencieuses (2, 5, 8, 9) signalées par l'audit Cowork sont à vérifier **côté UI Scholar**, indépendamment du pipeline.

### Cross-référence audit Cowork
- 13 mails Scholar reçus dans la période 2026-05-09 → 2026-05-25 (audit Cowork section 2).
- 16 résultats compilés sur 6 alertes actives (1, 3, 4, 6, 7, 10).
- Filtre Gmail OK, 0 spam, tout en INBOX.
- → Si le pipeline tournait, il aurait traité ces 13 mails et produit une synthèse hebdo.

---

## 4. Historique runs 30 derniers jours

`gh run list --workflow=veille_scholar.yml --limit 100` retourne **7 runs total** :

| Date UTC | Trigger | Durée | Conclusion |
|---|---|---|---|
| 2026-05-18 11:38 | schedule (lundi) | 29s | **failure** |
| 2026-05-11 10:54 | schedule (lundi) | 2m18s | success |
| 2026-05-11 06:22 | workflow_dispatch | 1m59s | success |
| 2026-05-11 06:13 | workflow_dispatch | 1m48s | success |
| 2026-05-11 06:08 | workflow_dispatch | 47s | failure |
| 2026-05-10 11:08 | workflow_dispatch | 36s | failure |
| 2026-05-10 10:22 | workflow_dispatch | 35s | failure |

### Synthèse
- **Dernière exécution réussie** : 2026-05-11 10:54 UTC (cycle 2, scheduled).
- **Premier scheduled fail** : 2026-05-18 11:38 UTC (cycle 3 prévu).
- **Run du 2026-05-25 (aujourd'hui)** : **n'a pas eu lieu**. Vérifié via `gh run list --created '2026-05-25..2026-05-26'` (vide). Le cron `0 8 * * 1` aurait dû déclencher à 8h00 UTC, on est ~14h après sans aucune trace de run.

### Hypothèse pour le 2026-05-25 manquant
GitHub Actions documente que les cron schedules en free tier sont best-effort : « scheduled events can be delayed during periods of high loads… high load times include the start of every hour ». Pile à `0 8 * * 1` (heure ronde) est typique de la fenêtre de pic GitHub. Le run a probablement été silencieusement skippé. Non bloquant pour le diagnostic puisque le bug racine identifié au §5 aurait produit un échec identique.

---

## 5. Cause racine du fail (preuve)

**Cause** : `GMAIL_REFRESH_TOKEN` expiré côté Google OAuth.

### Preuve — extrait `gh run view 26031147375 --log-failed`

```
2026-05-18T11:39:09.6310459Z Traceback (most recent call last):
2026-05-18T11:39:09.6329943Z   _client._handle_error_response(response_data, retryable_error)
2026-05-18T11:39:09.6330651Z   File ".../google/oauth2/_client.py", line 73, in _handle_error_response
2026-05-18T11:39:09.6331269Z     raise exceptions.RefreshError(
2026-05-18T11:39:09.6331973Z google.auth.exceptions.RefreshError: ('invalid_grant: Token has been expired or revoked.', {'error': 'invalid_grant', 'error_description': 'Token has been expired or revoked.'})
2026-05-18T11:39:09.7671219Z ##[error]Process completed with exit code 1.
```

L'erreur survient à l'étape `build_gmail_credentials()` (script L87-98), `creds.refresh(Request())`. Le refresh token est rejeté par `oauth2.googleapis.com/token`.

### Classification

| Classification | Match |
|---|---|
| **Auth Gmail expirée (OAuth refresh token grillé)** | **✅ CAUSE CONFIRMÉE** |
| Quota GitHub Actions épuisé | ❌ (workflow active, runs récents OK budget) |
| Workflow désactivé auto | ❌ (`gh workflow view` → active) |
| Erreur de parsing mail Scholar | ❌ (échec avant lecture Gmail) |
| Erreur destination commit | ❌ (échec avant écriture privée) |
| Modification accidentelle script | ❌ (script identique au commit du 2026-05-12 qui a fait tourner le run 2026-05-18) |
| Secret expiré/supprimé côté GitHub | ⚠️ partiellement — le secret existe (`gh secret list`), c'est sa **valeur** qui est invalide côté Google |

### Pourquoi 7 jours pile entre dernier succès et premier fail ?

L'app OAuth Tellux est très probablement en statut **"Testing"** dans Google Cloud Console (Cloud Console → OAuth consent screen → Publishing status). Pour les apps Testing avec scopes sensibles (`gmail.readonly` en fait partie), Google **expire automatiquement les refresh tokens après 7 jours**. C'est la cause la plus documentée du pattern observé :
- Token créé 2026-05-10 09:30 UTC
- Dernier usage réussi 2026-05-11 10:54 UTC
- Premier échec 2026-05-18 11:38 UTC = **+7j04h après dernier succès** → match parfait avec l'expiration Testing 7 jours.

Référence Google : https://support.google.com/cloud/answer/15549257 (Testing apps OAuth, point « refresh tokens expire »).

---

## 6. Cohérence audit Cowork ↔ pipeline

| Constat audit Cowork | Constat pipeline | Compatible ? |
|---|---|---|
| 13 mails Scholar reçus 2026-05-09 → 2026-05-25 | Si pipeline tournait, il aurait ingéré ces 13 mails | ✅ cohérent |
| Filtre Gmail OK (0 spam, tout INBOX) | Pas en cause | ✅ |
| 6 alertes actives, 4 silencieuses | Pipeline alerte-agnostique → silence vu uniquement par audit | ✅ orthogonal |
| Hypothèse C : « pipeline n8n/github a pris le relais » | Pipeline est GitHub Actions (pas n8n). Tournait, ne tourne plus depuis 2026-05-18. | ⚠️ à corriger dans audit Cowork |
| Cycle 2 production : synthèse mergée dans privé 2026-05-11 | Run 2026-05-11 10:54 UTC succès = ce commit | ✅ traçabilité OK |

**Conclusion** : la mémoire de coordination est partiellement obsolète (n8n vs GitHub Actions), mais l'audit Cowork reste valide sur l'état Gmail. Aucun mail perdu, juste 2 cycles (semaines 2026-05-18 et 2026-05-25) non synthétisés par le pipeline.

---

## 7. Évaluation effort réparation

### Cause racine = refresh token OAuth expiré → 2 options de fix

#### Option A — Passer l'app OAuth en statut "Production" (durable)

1. **Soleil** : Google Cloud Console → projet Tellux → APIs & Services → OAuth consent screen.
2. Vérifier statut courant (« Testing » probable).
3. Cliquer « Publish app » → statut « In production ».
4. Vérification Google **généralement non requise** pour `gmail.readonly` sur un usage perso (compte unique propriétaire). Si Google demande verification (rare), backup Option B.
5. Régénérer un nouveau refresh_token via flow OAuth local (script jetable ou OAuth Playground Google).
6. Upload nouveau token dans GitHub secret `GMAIL_REFRESH_TOKEN`.

**Coût** : 15-20 min Soleil. **Durabilité** : ad vitam (le token Production n'expire pas par inactivité).

#### Option B — Régénérer le refresh token sans changer le statut (workaround)

1. **Soleil** : générer nouveau refresh_token via OAuth Playground (`https://developers.google.com/oauthplayground`) avec scope `https://www.googleapis.com/auth/gmail.readonly` et credentials de l'app Tellux.
2. Upload nouveau token dans GitHub secret `GMAIL_REFRESH_TOKEN`.

**Coût** : 10 min Soleil. **Durabilité** : 7 jours seulement → besoin de re-régénération hebdomadaire ou utilisation au moins 1 fois par semaine pour garder le token vivant (le run scheduled hebdomadaire le ferait, ce qui rend la solution viable si on accepte le risque d'expiration en cas de panne d'un run intermédiaire).

### Coût Code après refresh token (les 2 options)

- 0 min : aucun changement code requis. Une fois le secret mis à jour, le prochain run scheduled (ou un `workflow_dispatch` immédiat) doit passer.
- Vérification post-fix : relancer `workflow_dispatch` avec `lookback_days=14` pour rattraper le rapport manquant (2026-05-11 → 2026-05-25).

### Recommandations alertes silencieuses (cycle 3, audit Cowork)

Hors scope du pipeline (alerte-agnostique côté code) mais utile à grouper pour Soleil :
- **Action UI** : vérifier les alertes 2, 5, 8, 9 sur https://scholar.google.com/scholar_alerts?view_op=list_alerts&email_for_op=tellux.veille%40gmail.com
- Cf. audit Cowork §7 R1 pour le détail.

---

## 8. Faisabilité avant 01/06/2026 (lundi)

**OK, largement.**

| Tâche | Acteur | Effort | Délai |
|---|---|---|---|
| Refresh OAuth (Option A ou B) | Soleil | 10-20 min | Faisable cette semaine |
| Upload nouveau secret `GMAIL_REFRESH_TOKEN` | Soleil | 2 min | Immédiat post-refresh |
| Relance `workflow_dispatch` avec `lookback_days=14` | Soleil ou Code (si lockfile public) | 1 min | Immédiat post-upload |
| Vérification visuelle commit dans repo privé `_corpus_veille/syntheses/` | Soleil | 5 min | T+3 min après run |
| Vérification UI alertes silencieuses 2/5/8/9 | Soleil | 5 min | Indépendant |
| **Total Soleil** | | **~25 min** | |
| **Total Code** | | **0 min** post-fix Soleil | |

Le prochain run scheduled est lundi 2026-06-01 à 8h UTC. Si le fix est appliqué d'ici dimanche soir, le cycle 4 démarre automatiquement.

### Plan B si Soleil indisponible avant 01/06

- Code peut générer un digest manuel des 13 mails déjà compilés par l'audit Cowork (`_drafts/SCHOLAR_ALERTS_DIGEST_MAI_2026.md`) et le pousser manuellement dans le privé via le repo `tellux-corpus-internal`. Tient lieu de synthèse cycle 3 en attendant la réparation pipeline. ~20 min.

---

## 9. Risques résiduels post-réparation

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Récidive expiration token (si Option B retenue) | Moyenne (7j inactivité) | Pipeline KO hebdo | Préférer Option A ; sinon prévoir alerte interne sur 2e failure consécutif |
| Google demande verification app pour passer Production | Faible (gmail.readonly + 1 user) | +délai 1-4 semaines | Fallback Option B en attendant |
| Run scheduled GitHub skipé (cron 8h UTC sur fenêtre chargée) | Modérée | Décalage de 1-2h, pas KO | Cf. doc GitHub, ou changer cron à `13 8 * * 1` (offset minutes) |
| Quota free tier GitHub Actions épuisé | Très faible (1 run/sem × 2 min = 8 min/mois sur 2000 dispo) | KO | Surveillance via `gh workflow view` |
| Repo privé `tellux-corpus-internal` indisponible (PAT révoqué) | Faible | KO commit synthèse | Le secret `GH_PATH` est récent (2026-05-11), TTL des PATs habituel 90j+ |
| Prompt `prompt_veille_tellux_v2.md` introuvable dans privé | Faible | KO step `fetch_prompt_from_private_repo` | Le script remonte un 404 explicite avec message d'aide |

---

## 10. Recommandation finale (synthèse)

1. **Cause racine** : refresh token Gmail OAuth expiré (pattern Testing app 7j).
2. **Action prioritaire Soleil** : Option A (passer en Production) > Option B (régénérer token Testing).
3. **Aucune intervention Code** nécessaire avant le refresh Soleil. Script et workflow OK.
4. **Calendrier** : faisable largement avant 2026-06-01.
5. **Cycle 3 (mails du 2026-05-09 → 2026-05-25)** : 2 options de rattrapage :
   - Relance `workflow_dispatch` `lookback_days=14` après refresh (automatique).
   - Génération manuelle via digest Cowork déjà existant (`SCHOLAR_ALERTS_DIGEST_MAI_2026.md`).
6. **Audit Cowork à corriger** : mention « n8n/github » → c'est uniquement GitHub Actions, pas n8n. Mémoire de coordination à mettre à jour.
7. **Hors pipeline** : Soleil vérifier les 4 alertes silencieuses (2, 5, 8, 9) côté UI Scholar (action indépendante).

---

## 11. Annexes

### 11.1 Commandes utiles (pour Soleil ou follow-up Code)

```bash
# Voir runs récents
gh run list --workflow=veille_scholar.yml --limit 10

# Voir log d'un run
gh run view <RUN_ID> --log-failed

# Relancer manuellement après refresh OAuth
gh workflow run veille_scholar.yml -f lookback_days=14 -f dry_run=0

# Tester en dry-run (n'écrit pas le commit privé)
gh workflow run veille_scholar.yml -f lookback_days=7 -f dry_run=1

# Lister secrets (noms uniquement)
gh secret list
```

### 11.2 Pas de secret exposé dans logs

Vérification rapide des logs du run 2026-05-18 : aucun secret en clair fuite. Les `***` masquent correctement les valeurs sensibles. RAS sécurité.

### 11.3 Refs techniques

- Workflow : `.github/workflows/veille_scholar.yml`
- Script : `.github/scripts/veille_scholar.py`
- Repo privé cible : `dellahstella/tellux-corpus-internal`
- Output : `_corpus_veille/syntheses/synthese_<YYYY-MM-DD>.md` dans le repo privé
- Audit Cowork couplé : `_drafts/SCHOLAR_ALERTS_AUDIT_2026-05-25.md`
- Digest manuel disponible : `_drafts/SCHOLAR_ALERTS_DIGEST_MAI_2026.md`
- Doc Google sur Testing app token expiration : https://support.google.com/cloud/answer/15549257

---

## 12. Procédure de refresh OAuth (ajout 2026-05-26)

Suite au brief `BRIEF CODE — Régénération refresh token Gmail + rattrapage cycle 3` (2026-05-26). Procédure outillée par `.github/scripts/refresh_oauth_token.py`.

### Prérequis
- App OAuth GCP `tellux-veille` en statut **Production** (action Soleil 2026-05-25 — confirmée). Sans cela, le nouveau refresh token ré-expirera après 7 jours.
- `google-auth-oauthlib` installé localement (déjà dispo).
- `gh` CLI authentifié sur `dellahstella/tellux`.

### Procédure (Option B + D — recommandée)

**Étape Soleil 1 — Reset Client Secret (si Client Secret introuvable)**

GCP Console → APIs & Services → Credentials → OAuth 2.0 Client IDs → `tellux-veille-github-actions` → bouton **« Reset secret »**. Le nouveau Client Secret s'affiche une seule fois.

**Étape Soleil 2 — Créer fichier temp local**

Créer `~/.tellux_oauth_temp.json` (sur Windows : `C:\Users\<user>\.tellux_oauth_temp.json`) :

```json
{
  "client_id": "<...apps.googleusercontent.com>",
  "client_secret": "<le-nouveau-secret-affiché>"
}
```

**Étape Code 3 — Lancer le script**

```bash
python .github/scripts/refresh_oauth_token.py
```

Comportement :
- Ouvre le navigateur sur l'écran de consentement Google (compte `tellux.veille@gmail.com`).
- Soleil clique « Autoriser ».
- Script récupère le refresh_token et upload **3 secrets** dans GitHub via `gh secret set` (lecture stdin, jamais d'arg CLI exposant la valeur) :
  - `GMAIL_REFRESH_TOKEN` (toujours nouveau)
  - `GMAIL_CLIENT_SECRET` (re-upload depuis le temp, prend en compte le reset éventuel)
  - `GMAIL_CLIENT_ID` (idempotent si inchangé)
- Script supprime le fichier temp.

**Étape Code 4 — Rattrapage cycle 3**

```bash
gh workflow run veille_scholar.yml -f lookback_days=14 -f dry_run=0 \
  --repo dellahstella/tellux
gh run watch  # suivre le run
```

`lookback_days=14` couvre la fenêtre 2026-05-11 → 2026-05-25 (les 2 cycles manqués). Output attendu : commit `_corpus_veille/syntheses/synthese_2026-05-26.md` dans le repo privé.

### Sécurité

- Le script ne fait aucun `print()` du Client Secret ni du refresh token (seule la longueur du token est affichée).
- `gh secret set` lit via stdin (pas d'arg CLI), donc rien dans `ps`/historique shell.
- Le fichier temp est en `~/.tellux_oauth_temp.json` (hors repo, jamais commité).
- Suppression automatique en fin de script.

### Fallback en cas d'échec

Si `flow.run_local_server()` ne renvoie pas de refresh_token (compte ayant déjà autorisé sans refresh), révoquer l'accès sur https://myaccount.google.com/permissions puis relancer le script. Le script utilise `prompt='consent'` + `access_type='offline'` pour forcer la délivrance du refresh — donc le cas null devrait être rare.

---

**Fin d'audit. Script `.github/scripts/refresh_oauth_token.py` créé et committé sur branche `chore/refresh-oauth-token-26052026`. En attente action Soleil pour exécution.**
