"""
Veille Scholar automatisée — Tellux Corse.

Workflow hebdomadaire (cron lundi 8h UTC) :
1. Récupère les emails Google Scholar Alerts des 7 derniers jours via Gmail API.
2. Lit le prompt de veille depuis le repo privé tellux-corpus-internal.
3. Synthétise via Anthropic API.
4. Commite la note dans le repo privé via API GitHub.

Aucun secret en clair dans le script — tout vient de variables d'environnement
fournies par GitHub Actions Secrets.

Variables d'env requises :
    GMAIL_REFRESH_TOKEN   — refresh_token OAuth (compte tellux.veille@gmail.com)
    GMAIL_CLIENT_ID       — client_id OAuth Desktop
    GMAIL_CLIENT_SECRET   — client_secret OAuth Desktop
    ANTHROPIC_API_KEY     — clé API Anthropic
    GITHUB_PAT            — Personal Access Token avec scope `repo` sur tellux-corpus-internal

Variables d'env optionnelles :
    PROMPT_PATH           — chemin du prompt dans le repo privé
                            (défaut : docs/pilotage/prompt_veille_tellux_v2.md)
    PRIVATE_REPO          — défaut : dellahstella/tellux-corpus-internal
    ANTHROPIC_MODEL       — défaut : claude-sonnet-4-5
    LOOKBACK_DAYS         — fenêtre de recherche en jours (défaut : 7)
    OUTPUT_DIR            — dossier dans le repo privé pour les synthèses
                            (défaut : _corpus_veille/syntheses)
    DRY_RUN               — si "1", n'écrit rien dans le repo privé (debug)
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
PRIVATE_REPO = os.environ.get("PRIVATE_REPO", "dellahstella/tellux-corpus-internal")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
LOOKBACK_DAYS = int(os.environ.get("LOOKBACK_DAYS", "7"))
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "_corpus_veille/syntheses")
DRY_RUN = os.environ.get("DRY_RUN", "0") == "1"

REQUIRED_SECRETS = [
    "GMAIL_REFRESH_TOKEN",
    "GMAIL_CLIENT_ID",
    "GMAIL_CLIENT_SECRET",
    "ANTHROPIC_API_KEY",
    "GITHUB_PAT",
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


def fetch_prompt_from_private_repo() -> str:
    """Récupère le prompt depuis le repo privé via API GitHub (PAT)."""
    url = f"https://api.github.com/repos/{PRIVATE_REPO}/contents/{PROMPT_PATH}"
    headers = {
        "Authorization": f"Bearer {os.environ['GITHUB_PAT']}",
        "Accept": "application/vnd.github.v3.raw",
    }
    print(f"[github] GET {url}")
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code == 404:
        fail(
            f"Prompt absent : {PROMPT_PATH} sur {PRIVATE_REPO}. "
            f"Vérifier que le fichier existe (le brief mentionne v2 — "
            f"si seulement v1 est dispo, surcharger PROMPT_PATH dans le workflow)."
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

    print(f"[github] PUT {url}")
    r = requests.put(url, headers=headers, json=payload, timeout=30)
    if r.status_code in (200, 201):
        print(f"[ok] Synthèse commitée : {path}")
    else:
        fail(f"Commit échoué : {r.status_code} — {r.text}")


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

    prompt = fetch_prompt_from_private_repo()
    synthesis = call_anthropic(prompt, emails)

    header = (
        f"# Synthèse veille Scholar — {today.isoformat()}\n\n"
        f"**Modèle** : {ANTHROPIC_MODEL}\n"
        f"**Fenêtre** : {LOOKBACK_DAYS} jours\n"
        f"**Emails analysés** : {len(emails)}\n"
        f"**Prompt source** : `{PROMPT_PATH}`\n\n"
        f"---\n\n"
    )
    commit_synthesis(header + synthesis, today)
    print("[done]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
