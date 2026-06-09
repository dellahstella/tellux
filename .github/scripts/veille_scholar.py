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
import re
import subprocess
import sys
from email import message_from_bytes
from email.policy import default as email_default_policy
from pathlib import Path
from typing import Any

import anthropic
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Force UTF-8 sur stdout/stderr pour éviter UnicodeEncodeError sur consoles
# Windows (cp1252) lors des tests locaux. Sur GitHub Actions Linux, locale est
# déjà UTF-8 et ce no-op est silencieux.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:  # noqa: BLE001 — best-effort, ne doit pas casser le run
            pass

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


# ---------------------------------------------------------------------------
# Gate §10 — verify_citation.py
#
# Garde-fou anti-Frankenstein : toute citation produite par l'étape
# d'intégration doit être résolvable par scripts/verify_citation.py
# (Crossref / PubMed / bioRxiv) avant d'écrire quoi que ce soit dans le
# dépôt cible. Si une seule citation échoue, l'intégration est avortée
# avec un exit non-zéro — aucune écriture.


# DOI canonical pattern (Crossref doc) : 10.{4-9 digits}/{path}. La partie
# locale tolère caractères URL-safe ; on coupe la ponctuation finale au
# nettoyage.
_DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"<>()\[\]]+", re.IGNORECASE)

# Chemins du script gate (résolus depuis la racine du repo).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_VERIFY_CITATION_PATH = _REPO_ROOT / "scripts" / "verify_citation.py"


class CitationGateError(RuntimeError):
    """Levée si le gate §10 bloque une ou plusieurs citations.

    Cette exception est explicitement PROPAGÉE (pas avalée par les
    try/except best-effort) — gate failure = exit non-zéro, aucun
    commit corpus.
    """


def _extract_dois(markdown: str) -> list[str]:
    """Extrait l'ensemble des DOIs uniques du markdown, ponctuation nettoyée."""
    raw = _DOI_RE.findall(markdown)
    seen: list[str] = []
    for doi in raw:
        cleaned = doi.rstrip(".,;:)]\"'>").lower()
        if cleaned and cleaned not in seen:
            seen.append(cleaned)
    return seen


# Pattern d'article ID parasite (style Oxford Academic) : DOI canonique
# suivi de `/<digits>` correspondant à l'ID d'article dans l'URL publisher.
# Exemple récurrent : URL https://academic.oup.com/jrr/advance-article/doi/
# 10.1093/jrr/rrag041/8702477 → le DOI Crossref canonique est en réalité
# 10.1093/jrr/rrag041 (sans /8702477). Le regex `_DOI_RE` est volontairement
# greedy pour capter tous les caractères du suffixe DOI, mais cela emporte
# au passage ce type d'ID quand le markdown contient l'URL publisher.
_TRAILING_ARTICLE_ID_RE = re.compile(r"^(10\.\d{4,9}/[^\s]+?)/(\d+)$", re.IGNORECASE)


def _normalize_doi_candidates(doi: str) -> list[str]:
    """Retourne le DOI tel quel, puis ses normalisations candidates.

    Tronque récursivement les segments finaux `/<digits>` (article IDs
    publisher) tant que le pattern se répète. Garantit que l'ordre essayé
    par le gate est : original d'abord, puis truncated. Si l'original résout,
    on ne sait jamais qu'on aurait pu tronquer ; si l'original échoue, on
    tente les candidats progressivement.
    """
    candidates = [doi]
    current = doi
    while True:
        m = _TRAILING_ARTICLE_ID_RE.match(current)
        if not m:
            break
        truncated = m.group(1)
        if truncated == current or truncated in candidates:
            break
        candidates.append(truncated)
        current = truncated
    return candidates


def _verify_single_doi(doi: str) -> tuple[bool, str]:
    """Lance verify_citation.py sur un seul DOI. Retourne (ok, message).

    ok=True si rc=0. message contient la dernière ligne stderr (cause) si
    rc≠0, ou un libellé d'exception si subprocess plante.
    """
    try:
        result = subprocess.run(
            [sys.executable, str(_VERIFY_CITATION_PATH), doi],
            capture_output=True,
            text=True,
            timeout=45,
        )
        if result.returncode == 0:
            return True, ""
        stderr_brief = (result.stderr or "").strip().splitlines()
        last = stderr_brief[-1] if stderr_brief else f"rc={result.returncode}"
        return False, f"rc={result.returncode} — {last[:200]}"
    except subprocess.TimeoutExpired:
        return False, "timeout 45s"
    except Exception as exc:  # noqa: BLE001 — robustesse runtime cron
        return False, f"exception : {str(exc)[:200]}"


def gate_citations(markdown: str, source_label: str = "intégration") -> None:
    """Exécute verify_citation.py sur chaque DOI extrait de `markdown`.

    Lève CitationGateError si au moins une citation échoue. Aucune écriture
    en sortie — c'est un gate pur.

    Pour chaque DOI extrait, tente verify_citation sur l'original PUIS sur
    ses candidats normalisés (cf. `_normalize_doi_candidates`). Cela évite
    les faux positifs récurrents sur les URL publisher Oxford Academic et
    équivalents (DOI suivi d'un article ID numérique).

    Args:
        markdown: contenu markdown à scanner pour DOIs.
        source_label: étiquette pour les logs (ex. "intégration", "test").
    """
    if not _VERIFY_CITATION_PATH.exists():
        raise CitationGateError(
            f"[gate] verify_citation.py introuvable à {_VERIFY_CITATION_PATH} — "
            f"gate §10 indisponible, intégration bloquée par précaution."
        )

    dois = _extract_dois(markdown)
    if not dois:
        print(f"[gate] {source_label} — aucun DOI détecté ; gate passe par défaut.")
        return

    print(f"[gate] {source_label} — {len(dois)} DOI(s) à vérifier via "
          f"scripts/verify_citation.py")
    passed: list[str] = []
    failed: list[tuple[str, str]] = []
    for doi in dois:
        candidates = _normalize_doi_candidates(doi)
        resolved_as: str | None = None
        last_error: str = ""
        for candidate in candidates:
            ok, msg = _verify_single_doi(candidate)
            if ok:
                resolved_as = candidate
                break
            last_error = msg
        if resolved_as is None:
            failed.append((doi, last_error))
            print(f"[gate] FAIL  {doi} — {last_error}")
        elif resolved_as == doi:
            passed.append(doi)
            print(f"[gate] PASS  {doi}")
        else:
            passed.append(doi)
            print(f"[gate] PASS  {doi} (normalisé → {resolved_as})")

    print(f"[gate] {source_label} — résultat : {len(passed)} OK, {len(failed)} échec(s)")
    if failed:
        details = "\n".join(f"  - {doi} :: {reason}" for doi, reason in failed)
        raise CitationGateError(
            f"{len(failed)} citation(s) bloquée(s) sur {len(dois)} — "
            f"intégration corpus avortée (aucune écriture).\n{details}"
        )


def run_integration_step(today: dt.date, synthesis_content: str) -> str | None:
    """Lance l'étape intégration. Le gate §10 sur les citations EST FATAL.

    Le commit / réseau / appel Claude restent best-effort (non fatals). Mais
    une CitationGateError remonte volontairement à l'appelant pour avorter
    le run avec exit non-zéro et SANS commit.
    """
    print(f"[integration] start")
    try:
        integration_prompt = fetch_prompt_from_private_repo(INTEGRATION_PROMPT_PATH)
        note = call_anthropic_integration(integration_prompt, synthesis_content)
    except Exception as e:
        print(f"[integration] WARN — préparation note échouée (non fatale) : {e}")
        return None

    # Gate §10 — AVANT toute écriture. Levée d'exception fatale si KO.
    gate_citations(note, source_label="intégration corpus")

    if DRY_RUN:
        print("[integration] DRY_RUN=1 — gate validé, écriture corpus skippée "
              "(mode dry-run explicit demandé).")
        return None

    try:
        header = (
            f"# Note d'intégration veille Scholar — {today.isoformat()}\n\n"
            f"**Modèle** : {ANTHROPIC_MODEL}\n"
            f"**Synthèse source** : `{OUTPUT_DIR}/synthese_{today.isoformat()}.md`\n"
            f"**Prompt intégration** : `{INTEGRATION_PROMPT_PATH}`\n\n"
            f"**Gate §10 (`verify_citation.py`)** : ✅ toutes citations validées.\n\n"
            f"---\n\n"
        )
        path = commit_integration(header + note, today)
        print(f"[integration] done")
        return path
    except Exception as e:
        print(f"[integration] WARN — commit échoué (non fatal) : {e}")
        return None


# ---------------------------------------------------------------------------
# Notification (best-effort)


def notify_run_complete(
    today: dt.date,
    n_emails: int,
    synthesis_path: str,
    integration_path: str | None,
    gate_failed: bool = False,
    gate_error_message: str = "",
) -> None:
    """Ouvre une issue dans le repo prive pour signaler la production du run.

    L'issue lie la synthese ET la note d'integration (si produite). Si la note
    d'integration a echoue, l'issue le signale explicitement pour que Soleil
    sache que le cycle est partiel.

    Si `gate_failed=True`, le titre et le corps signalent explicitement que
    l'intégration a été bloquée par le gate §10 (verify_citation.py) et que
    le run a été marqué en échec (exit non-zéro). Aucune écriture corpus n'a
    eu lieu.

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
    if gate_failed:
        title = f"[veille] ⛔ Gate §10 BLOQUE — intégration avortée — {today.isoformat()}"
    else:
        title = f"[veille] Synthèse + intégration — {today.isoformat()}"

    integration_section = ""
    if gate_failed:
        integration_section = (
            f"\n## Note d'intégration corpus\n\n"
            f"⛔ **Intégration corpus AVORTÉE par le gate §10** "
            f"(`scripts/verify_citation.py`).\n\n"
            f"Aucune écriture corpus n'a eu lieu. Le run est marqué en échec "
            f"(exit non-zéro) afin d'apparaître clairement dans l'historique "
            f"GitHub Actions.\n\n"
            f"**Détail du blocage** :\n\n"
            f"```\n{gate_error_message}\n```\n"
        )
    elif integration_path:
        integration_url = f"https://github.com/{PRIVATE_REPO}/blob/main/{integration_path}"
        integration_section = (
            f"\n## Note d'intégration corpus\n\n"
            f"- **Fichier** : `{integration_path}`\n"
            f"- **Lien** : {integration_url}\n"
            f"- **Gate §10** : ✅ toutes citations validées.\n"
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

    # Etape 2 — Note d'integration corpus.
    # Garde-fou cron : désactivée par défaut (RUN_INTEGRATION=0). L'intégration
    # au corpus reste mensuelle, séparée, gatée par scripts/verify_citation.py.
    # Si RUN_INTEGRATION=1, le gate §10 EST FATAL — toute citation non résolue
    # avorte le run avec exit 2 et aucune écriture.
    integration_path = None
    if RUN_INTEGRATION:
        try:
            integration_path = run_integration_step(today, synthesis_full)
        except CitationGateError as e:
            print(f"[gate] FATAL — intégration corpus avortée par le gate §10.")
            print(str(e))
            # Best-effort : on essaie quand même de notifier le blocage (signal
            # visible), mais on exit non-zéro pour que la run apparaisse en
            # échec dans GitHub Actions.
            try:
                notify_run_complete(
                    today, len(emails), synthesis_path, None,
                    gate_failed=True, gate_error_message=str(e),
                )
            except Exception as notify_exc:
                print(f"[notify] WARN — notification gate-fail échouée : {notify_exc}")
            return 2
    else:
        print("[skip] Étape d'intégration corpus désactivée (RUN_INTEGRATION=0) — "
              "le cron ne fait que collecter ; l'intégration est manuelle et gatée.")

    # Etape 3 — Notification issue (best-effort, lie synthese + integration)
    notify_run_complete(today, len(emails), synthesis_path, integration_path)

    print("[done]")
    return 0


def cli_test_gate() -> int:
    """CLI : `python veille_scholar.py --test-gate <path>`.

    Lit le markdown du fichier, extrait les DOIs, exécute le gate §10
    (verify_citation.py) sur chacun, sans aucun side-effect réseau au-delà
    des appels Crossref/PubMed/bioRxiv eux-mêmes. Exit 0 si gate OK, exit 2
    si gate bloque (cohérent avec verify_citation.py).

    Usage prouvable :
        python .github/scripts/veille_scholar.py --test-gate path/to/file.md
    """
    if len(sys.argv) < 3:
        print("Usage : python veille_scholar.py --test-gate <path/to/markdown>", file=sys.stderr)
        return 1
    target = Path(sys.argv[2])
    if not target.exists():
        print(f"[test-gate] Fichier introuvable : {target}", file=sys.stderr)
        return 1
    content = target.read_text(encoding="utf-8")
    print(f"[test-gate] source : {target} ({len(content)} chars)")
    try:
        gate_citations(content, source_label=f"test-gate ({target.name})")
        print("[test-gate] OK — gate §10 validé (aucune citation bloquée).")
        return 0
    except CitationGateError as exc:
        print(f"[test-gate] BLOQUÉ — {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    # Mode test isolé : `--test-gate <path>` exécute uniquement le gate sur
    # un fichier markdown, sans toucher au reste du pipeline (pas de Gmail,
    # pas d'Anthropic, pas de commit).
    if len(sys.argv) >= 2 and sys.argv[1] == "--test-gate":
        sys.exit(cli_test_gate())
    sys.exit(main())
