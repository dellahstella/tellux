"""
Veille Scholar automatisée — Tellux Corse.

Workflow hebdomadaire (cron lundi 8h UTC) :
1. Récupère les emails Google Scholar Alerts des 7 derniers jours via Gmail API.
2. Lit le prompt de veille depuis un dépôt de coordination interne.
3. Synthétise via Anthropic API.
4. Écrit le digest dans la file inbox du dépôt de coordination interne.

Garde-fou d'archi (décision 2026-06-08) : le cron hebdo collecte uniquement
et écrit dans `_inbox/scholar/syntheses/` du dépôt cible. Le commit ne va
jamais directement dans le corpus. L'intégration au corpus reste mensuelle,
séparée, gatée par `scripts/verify_citation.py` — RUN_INTEGRATION reste à "0"
en cron ; uniquement utilisable en manuel (override par workflow_dispatch
ou exécution locale).

Aucun secret en clair dans le script — tout vient de variables d'environnement
fournies par GitHub Actions Secrets.

Variables d'env requises :
    GMAIL_REFRESH_TOKEN   — refresh_token OAuth (compte de service)
    GMAIL_CLIENT_ID       — client_id OAuth Desktop
    GMAIL_CLIENT_SECRET   — client_secret OAuth Desktop
    ANTHROPIC_API_KEY     — clé API Anthropic
    GITHUB_PAT            — Personal Access Token avec scope `repo` sur le dépôt cible
    PRIVATE_REPO          — slug `owner/repo` du dépôt de coordination cible

Variables d'env optionnelles :
    PROMPT_PATH           — chemin du prompt dans le dépôt cible
                            (défaut : docs/pilotage/prompt_veille_tellux_v2.md)
    INTEGRATION_PROMPT_PATH — chemin du prompt d'intégration
                            (défaut : docs/pilotage/prompt_integration_corpus.md)
    ANTHROPIC_MODEL       — défaut : claude-sonnet-4-5
    LOOKBACK_DAYS         — fenêtre de recherche en jours (défaut : 7)
    OUTPUT_DIR            — dossier dans le dépôt cible pour les synthèses
                            (défaut : _inbox/scholar/syntheses ; garde-fou cron)
    INTEGRATION_OUTPUT_DIR — dossier pour la note d'intégration corpus
                            (défaut : _inbox/scholar/integrations)
    RUN_INTEGRATION       — si "1", exécute l'étape d'intégration corpus
                            (défaut "0" ; cron ne déclenche jamais l'intégration)
    DRY_RUN               — si "1", n'écrit rien dans le dépôt cible (debug)
"""

from __future__ import annotations

import base64
import datetime as dt
import json
import os
import sys
from email import message_from_bytes
from email.policy import default as email_default_policy
from typing import Any

import anthropic
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ---------------------------------------------------------------------------
# Config

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
SCHOLAR_FROM = "scholaralerts-noreply@google.com"

PROMPT_PATH = os.environ.get(
    "PROMPT_PATH", "docs/pilotage/prompt_veille_tellux_v2.md"
)
INTEGRATION_PROMPT_PATH = os.environ.get(
    "INTEGRATION_PROMPT_PATH", "docs/pilotage/prompt_integration_corpus.md"
)
PRIVATE_REPO = os.environ.get("PRIVATE_REPO", "")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
LOOKBACK_DAYS = int(os.environ.get("LOOKBACK_DAYS", "7"))
# Garde-fou cron : OUTPUT_DIR pointe sur la file inbox par défaut. Le commit
# direct dans le corpus est interdit en cron — l'intégration au corpus est un
# processus séparé, mensuel, gaté par scripts/verify_citation.py.
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "_inbox/scholar/syntheses")
INTEGRATION_OUTPUT_DIR = os.environ.get(
    "INTEGRATION_OUTPUT_DIR", "_inbox/scholar/integrations"
)
DRY_RUN = os.environ.get("DRY_RUN", "0") == "1"
# Étape d'intégration corpus : désactivée par défaut. Le cron ne lance que la
# collecte → digest. L'intégration au corpus public/_corpus_veille reste
# manuelle (curation + verify_citation.py).
RUN_INTEGRATION = os.environ.get("RUN_INTEGRATION", "0") == "1"

REQUIRED_SECRETS = [
    "GMAIL_REFRESH_TOKEN",
    "GMAIL_CLIENT_ID",
    "GMAIL_CLIENT_SECRET",
    "ANTHROPIC_API_KEY",
    "GITHUB_PAT",
    "PRIVATE_REPO",
]


# ---------------------------------------------------------------------------
# Helpers


def fail(msg: str, code: int = 1) -> None:
    print(f"[ERREUR] {msg}", file=sys.stderr)
    sys.exit(code)


def check_env() -> None:
    missing = [k for k in REQUIRED_SECRETS if not os.environ.get(k)]
    if missing:
        fail(f"Secrets manquants : {', '.join(missing)}")


def build_gmail_credentials() -> Credentials:
    """Reconstruit Credentials depuis le refresh_token et rafraîchit l'access_token."""
    creds = Credentials(
        token=None,
        refresh_token=os.environ["GMAIL_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GMAIL_CLIENT_ID"],
        client_secret=os.environ["GMAIL_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    creds.refresh(Request())
    return creds


def fetch_scholar_emails(service: Any, lookback_days: int) -> list[dict[str, str]]:
    """Récupère les emails Scholar Alerts des N derniers jours."""
    after_date = (dt.date.today() - dt.timedelta(days=lookback_days)).strftime("%Y/%m/%d")
    query = f"from:{SCHOLAR_FROM} after:{after_date}"
    print(f"[gmail] Requête : {query}")

    resp = service.users().messages().list(userId="me", q=query, maxResults=200).execute()
    messages = resp.get("messages", [])
    print(f"[gmail] {len(messages)} message(s) trouvé(s)")

    out: list[dict[str, str]] = []
    for m in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=m["id"], format="raw")
            .execute()
        )
        raw = base64.urlsafe_b64decode(msg["raw"])
        parsed = message_from_bytes(raw, policy=email_default_policy)

        subject = parsed.get("Subject", "(sans sujet)")
        date_hdr = parsed.get("Date", "")

        # Préfère le contenu text/plain, sinon text/html dépouillé
        body = ""
        if parsed.is_multipart():
            for part in parsed.walk():
                ctype = part.get_content_type()
                if ctype == "text/plain":
                    body = part.get_content()
                    break
            if not body:
                for part in parsed.walk():
                    if part.get_content_type() == "text/html":
                        body = part.get_content()
                        break
        else:
            body = parsed.get_content()

        out.append({"subject": subject, "date": date_hdr, "body": body})

    return out


def fetch_prompt_from_private_repo(path: str = PROMPT_PATH) -> str:
    """Récupère un prompt depuis le repo privé via API GitHub (PAT).

    Utilisée pour le prompt veille (PROMPT_PATH) et le prompt intégration
    (INTEGRATION_PROMPT_PATH).
    """
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_PAT']}",
        "Accept": "application/vnd.github.v3.raw",
    }
    print(f"[github] GET {url}")
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code == 404:
        fail(
            f"Prompt absent : {path} sur {PRIVATE_REPO}. "
            f"Vérifier que le fichier existe."
        )
    r.raise_for_status()
    return r.text


def call_anthropic(prompt: str, emails: list[dict[str, str]]) -> str:
    """Appelle l'API Anthropic pour synthétiser les emails selon le prompt."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    emails_md = "\n\n---\n\n".join(
        f"## Email {i + 1}\n\n"
        f"**Sujet** : {e['subject']}\n"
        f"**Date** : {e['date']}\n\n"
        f"{e['body']}"
        for i, e in enumerate(emails)
    )

    user_message = (
        f"{prompt}\n\n"
        f"---\n\n"
        f"# Corpus à synthétiser ({len(emails)} emails Scholar Alerts)\n\n"
        f"{emails_md}"
    )

    print(f"[anthropic] Modèle {ANTHROPIC_MODEL}, {len(user_message)} caractères en input")
    msg = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in msg.content if block.type == "text")


def commit_synthesis(content: str, today: dt.date) -> None:
    """Commit la note dans le repo privé via API GitHub."""
    filename = f"synthese_{today.isoformat()}.md"
    path = f"{OUTPUT_DIR}/{filename}"
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_PAT']}",
        "Accept": "application/vnd.github+json",
    }
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    payload = {
        "message": f"data: synthèse veille Scholar {today.isoformat()}",
        "content": encoded,
        "branch": "main",
    }

    if DRY_RUN:
        print(f"[dry-run] PUT {url} ({len(content)} chars)")
        print("--- Aperçu (300 premiers caractères) ---")
        print(content[:300])
        return

    # Preflight GET pour recuperer le SHA si le fichier existe deja.
    # GitHub API PUT /contents exige `sha` obligatoire en mode UPDATE,
    # sinon retourne 422 Validation Failed (cf. fail cron lundi 2026-05-25
    # quand le run scheduled re-ecrasait un fichier deja commite par le
    # run manuel rattrapage le meme matin).
    print(f"[github] GET {url} (preflight SHA check)")
    r_get = requests.get(url, headers=headers, params={"ref": "main"}, timeout=30)
    if r_get.status_code == 200:
        existing_sha = r_get.json().get("sha")
        if existing_sha:
            payload["sha"] = existing_sha
            print(f"[github] Fichier existant detecte (sha={existing_sha[:8]}), mode UPDATE")
    elif r_get.status_code == 404:
        print("[github] Fichier inexistant, mode CREATE")
    else:
        # Cas degraded : on continue en mode CREATE (sera 422 si fichier
        # existe), mais on log au moins le code retour pour diagnostic.
        # Ne fail() pas ici pour ne pas masquer un eventuel succes downstream.
        print(f"[github] Preflight GET retourne {r_get.status_code} (continue en CREATE)")

    print(f"[github] PUT {url}")
    r = requests.put(url, headers=headers, json=payload, timeout=30)
    if r.status_code in (200, 201):
        print(f"[ok] Synthèse commitée : {path}")
    else:
        fail(f"Commit échoué : {r.status_code} — {r.text}")


# ---------------------------------------------------------------------------
# Integration corpus (best-effort, etape 2 du run)


def call_anthropic_integration(integration_prompt: str, synthesis: str) -> str:
    """Appelle Claude API pour produire la note d'integration corpus.

    Input = synthese hebdo deja produite par l'etape 1. Output = note
    d'integration markdown (recommandations par axe, statuts epistemiques,
    candidats amendements corpus + implications appli flaggees "a arbitrer").
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    user_message = (
        f"{integration_prompt}\n\n"
        f"---\n\n"
        f"# Synthèse veille hebdomadaire à intégrer\n\n"
        f"{synthesis}"
    )

    print(f"[integration] Modèle {ANTHROPIC_MODEL}, {len(user_message)} caractères en input")
    msg = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=8192,
        messages=[{"role": "user", "content": user_message}],
    )
    return "".join(block.text for block in msg.content if block.type == "text")


def commit_integration(content: str, today: dt.date) -> str:
    """Commit la note d'integration dans le repo prive. Retourne le path."""
    filename = f"note_integration_{today.isoformat()}.md"
    path = f"{INTEGRATION_OUTPUT_DIR}/{filename}"
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_PAT']}",
        "Accept": "application/vnd.github+json",
    }
    encoded = base64.b64encode(content.encode("utf-8")).decode("ascii")
    payload = {
        "message": f"data: note d'intégration veille Scholar {today.isoformat()}",
        "content": encoded,
        "branch": "main",
    }

    if DRY_RUN:
        print(f"[dry-run] integration PUT {url} ({len(content)} chars)")
        return path

    # Preflight GET pour SHA si fichier existe (idempotence cron, cf. commit_synthesis)
    print(f"[integration] GET {url} (preflight SHA check)")
    r_get = requests.get(url, headers=headers, params={"ref": "main"}, timeout=30)
    if r_get.status_code == 200:
        existing_sha = r_get.json().get("sha")
        if existing_sha:
            payload["sha"] = existing_sha
            print(f"[integration] Fichier existant (sha={existing_sha[:8]}), mode UPDATE")
    elif r_get.status_code == 404:
        print("[integration] Fichier inexistant, mode CREATE")
    else:
        print(f"[integration] Preflight GET retourne {r_get.status_code} (continue en CREATE)")

    print(f"[integration] PUT {url}")
    r = requests.put(url, headers=headers, json=payload, timeout=30)
    if r.status_code in (200, 201):
        print(f"[ok] Note d'intégration commitée : {path}")
        return path
    else:
        # Best-effort : on log l'erreur mais on ne fail() pas — la synthese
        # a deja ete commitee avec succes a l'etape 1, on ne casse pas le run.
        raise RuntimeError(f"Commit integration échoué : {r.status_code} — {r.text[:200]}")


def run_integration_step(today: dt.date, synthesis_content: str) -> str | None:
    """Lance l'etape integration best-effort. Retourne le path commite ou None.

    Encapsule fetch prompt + call Claude + commit dans try/except global. Toute
    erreur logge un WARN mais ne fait pas echouer le run (la synthese passe
    quand meme, la note d'integration est un bonus du cycle).
    """
    try:
        print(f"[integration] start")
        integration_prompt = fetch_prompt_from_private_repo(INTEGRATION_PROMPT_PATH)
        note = call_anthropic_integration(integration_prompt, synthesis_content)
        header = (
            f"# Note d'intégration veille Scholar — {today.isoformat()}\n\n"
            f"**Modèle** : {ANTHROPIC_MODEL}\n"
            f"**Synthèse source** : `{OUTPUT_DIR}/synthese_{today.isoformat()}.md`\n"
            f"**Prompt intégration** : `{INTEGRATION_PROMPT_PATH}`\n\n"
            f"---\n\n"
        )
        path = commit_integration(header + note, today)
        print(f"[integration] done")
        return path
    except Exception as e:
        print(f"[integration] WARN — étape échouée (non fatale) : {e}")
        return None


# ---------------------------------------------------------------------------
# Notification (best-effort)


def notify_run_complete(
    today: dt.date,
    n_emails: int,
    synthesis_path: str,
    integration_path: str | None,
) -> None:
    """Ouvre une issue dans le repo prive pour signaler la production du run.

    L'issue lie la synthese ET la note d'integration (si produite). Si la note
    d'integration a echoue, l'issue le signale explicitement pour que Soleil
    sache que le cycle est partiel.

    Best-effort : si l'API GitHub echoue, on log un warning sans faire echouer
    le run (la synthese et eventuellement la note sont deja commitees, la
    notification est un bonus).
    """
    if DRY_RUN:
        print(f"[dry-run] notification issue skipped")
        return

    synthesis_url = f"https://github.com/{PRIVATE_REPO}/blob/main/{synthesis_path}"
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/issues"
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_PAT']}",
        "Accept": "application/vnd.github+json",
    }
    title = f"[veille] Synthèse + intégration — {today.isoformat()}"

    integration_section = ""
    if integration_path:
        integration_url = f"https://github.com/{PRIVATE_REPO}/blob/main/{integration_path}"
        integration_section = (
            f"\n## Note d'intégration corpus\n\n"
            f"- **Fichier** : `{integration_path}`\n"
            f"- **Lien** : {integration_url}\n"
        )
    else:
        integration_section = (
            f"\n## Note d'intégration corpus\n\n"
            f"⚠️ **Étape intégration échouée** ce cycle (best-effort, non fatal). "
            f"Voir les logs du run pour la cause. La synthèse hebdo ci-dessus est en place.\n"
        )

    body = (
        f"Run veille hebdomadaire terminé pour le **{today.isoformat()}**.\n\n"
        f"## Synthèse veille\n\n"
        f"- **Fenêtre** : {LOOKBACK_DAYS} jours\n"
        f"- **Emails analysés** : {n_emails}\n"
        f"- **Modèle** : `{ANTHROPIC_MODEL}`\n"
        f"- **Fichier** : `{synthesis_path}`\n"
        f"- **Lien** : {synthesis_url}\n"
        f"{integration_section}\n"
        f"---\n\n"
        f"Issue générée automatiquement par le workflow `veille_scholar.yml`. "
        f"Fermer (ou laisser) sans impact ; sert uniquement de signal de production hebdomadaire."
    )
    payload = {"title": title, "body": body}

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        if r.status_code in (200, 201):
            issue_url = r.json().get("html_url", "")
            print(f"[notify] Issue ouverte : {issue_url}")
        else:
            print(f"[notify] WARN — POST issues retourne {r.status_code} : {r.text[:200]}")
    except Exception as e:
        print(f"[notify] WARN — exception (non fatale) : {e}")


# ---------------------------------------------------------------------------
# Main


def main() -> int:
    check_env()
    today = dt.date.today()
    print(f"[start] Veille Scholar — {today.isoformat()}")

    creds = build_gmail_credentials()
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)
    emails = fetch_scholar_emails(service, LOOKBACK_DAYS)

    if not emails:
        print("[stop] Aucun email Scholar trouvé — pas de synthèse à produire.")
        return 0

    # Etape 1 — Synthese veille (etape critique, fail si KO)
    prompt = fetch_prompt_from_private_repo()
    synthesis = call_anthropic(prompt, emails)

    synthesis_header = (
        f"# Synthèse veille Scholar — {today.isoformat()}\n\n"
        f"**Modèle** : {ANTHROPIC_MODEL}\n"
        f"**Fenêtre** : {LOOKBACK_DAYS} jours\n"
        f"**Emails analysés** : {len(emails)}\n"
        f"**Prompt source** : `{PROMPT_PATH}`\n\n"
        f"---\n\n"
    )
    synthesis_full = synthesis_header + synthesis
    commit_synthesis(synthesis_full, today)
    synthesis_path = f"{OUTPUT_DIR}/synthese_{today.isoformat()}.md"

    # Etape 2 — Note d'integration corpus (best-effort, ne casse pas le run)
    # Garde-fou cron : désactivée par défaut (RUN_INTEGRATION=0). L'intégration
    # au corpus reste mensuelle, séparée, gatée par scripts/verify_citation.py.
    integration_path = None
    if RUN_INTEGRATION:
        integration_path = run_integration_step(today, synthesis_full)
    else:
        print("[skip] Étape d'intégration corpus désactivée (RUN_INTEGRATION=0) — "
              "le cron ne fait que collecter ; l'intégration est manuelle et gatée.")

    # Etape 3 — Notification issue (best-effort, lie synthese + integration)
    notify_run_complete(today, len(emails), synthesis_path, integration_path)

    print("[done]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
