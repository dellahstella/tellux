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
    GMAIL_REFRESH_TOKEN   — refresh_token OAuth utilisateur (client Desktop, pas un service account)
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
    CORPS_MAX_CARACTERES  — longueur maximale d'un corps d'alerte, après extraction
                            du texte (défaut : 8000) ; au-delà, le corps est tronqué
                            et la coupe est écrite dans le corps
    BUDGET_TOKENS_ENTREE  — plafond de l'entrée envoyée au modèle, compté par l'API
                            avant l'envoi (défaut : 150000, pour 200 000 de contexte)
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
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

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
# Bornes du corpus envoyé au modèle (2026-09-10). Jusque-là, le script concaténait le
# corps entier de chaque alerte, sans borne. C'était juste tant qu'arrivaient 5 à 8
# alertes par semaine (58 k à 117 k caractères). C'est devenu faux quand le volume a
# changé : 47 puis 48 alertes, 1,05 M puis 1,17 M caractères, et « prompt is too long »
# (439 250 puis 496 893 tokens pour 200 000) les 31/08 et 07/09. Le script n'avait pas
# changé ; le monde autour de lui, si. Deux bornes, et chacune se déclare dans la
# synthèse et dans l'issue de notification :
#   - CORPS_MAX_CARACTERES : longueur maximale d'un corps, APRÈS extraction du texte ;
#   - BUDGET_TOKENS_ENTREE : plafond de l'entrée complète, compté par l'API elle-même
#     (messages.count_tokens) avant l'envoi, pas estimé.
CORPS_MAX_CARACTERES = int(os.environ.get("CORPS_MAX_CARACTERES", "8000"))
BUDGET_TOKENS_ENTREE = int(os.environ.get("BUDGET_TOKENS_ENTREE", "150000"))
# Repli si le comptage par l'API échoue : le pire rapport mesuré, arrondi vers le
# prudent — 2,36 sur le HTML brut du 07/09 (1 174 133 caractères pour 496 893 tokens),
# 2,38 sur le texte extrait du dry run du 10/09 (353 659 pour 148 766). Appliqué aux
# OCTETS UTF-8 et non aux caractères : sur ce texte presque ASCII c'est la même chose,
# et une écriture idéographique (3 octets, environ 1 token) n'est pas sous-estimée.
OCTETS_PAR_TOKEN_PIRE_CAS = 2.3
# En dessous de cette borne, on n'ampute plus les corps : on écarte les alertes les
# plus anciennes, en les nommant.
BORNE_PLANCHER = 500
# Plafond de sortie de la synthèse. BUDGET_TOKENS_ENTREE + MAX_TOKENS_SORTIE doit rester
# sous la fenêtre de contexte du modèle (200 000).
MAX_TOKENS_SORTIE = 8192
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


def _cible_de_lien(href: str | None) -> str | None:
    """Cible réelle d'un lien d'alerte, ou None pour un lien sans information d'article.
    Scholar enveloppe ses liens d'article dans une redirection (…/scholar_url?url=<cible>&…) :
    on garde <cible>, plus courte et plus utile à citer que la redirection."""
    if not href or href.startswith(("mailto:", "#")):
        return None
    u = urlparse(href)
    if u.netloc.startswith("scholar.google."):
        if u.path == "/scholar_url":
            return parse_qs(u.query).get("url", [href])[0]
        # Les autres liens Scholar sont des actions (enregistrer, partager, gérer
        # l'alerte), sans texte ni information d'article. Sur les 51 alertes réelles
        # gardées au dépôt privé, ils faisaient les deux tiers du corps extrait (revue
        # adversariale du 2026-09-10).
        return None
    return href


_REDIRECTION_SCHOLAR = re.compile(r"https?://scholar\.google\.[a-z.]+/scholar_url\?[^\s<>\"')\]]+")


def _derouler_liens_scholar(texte: str) -> str:
    """Remplace, dans un texte, chaque redirection Scholar par sa cible."""
    return _REDIRECTION_SCHOLAR.sub(lambda m: _cible_de_lien(m.group(0)) or m.group(0), texte)


class _TexteDeHtml(HTMLParser):
    """Texte lisible d'un corps HTML : le texte, plus la cible de chaque lien d'article.
    Styles et scripts écartés."""

    # Ni `head` ni `title` : leur balise de fin est facultative en HTML5 et HTMLParser n'en
    # infère aucune — un `</head>` omis aurait vidé tout le corps (revue du 2026-09-10).
    _IGNORES = {"style", "script"}
    _BLOCS = {"br", "p", "div", "tr", "li", "table", "h1", "h2", "h3", "h4", "h5", "h6"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._morceaux: list[str] = []
        self._ignore = 0
        self._liens: list[str | None] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self._IGNORES:
            self._ignore += 1
        elif tag == "a":
            self._liens.append(dict(attrs).get("href"))
        elif tag in self._BLOCS:
            self._morceaux.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in self._IGNORES:
            self._ignore = max(0, self._ignore - 1)
        elif tag == "a" and self._liens:
            cible = _cible_de_lien(self._liens.pop())
            if cible and not self._ignore:
                self._morceaux.append(f" <{cible}>")
        elif tag in self._BLOCS:
            self._morceaux.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._ignore:
            self._morceaux.append(data)

    def texte(self) -> str:
        lignes = (re.sub(r"[ \t\xa0 ]+", " ", ligne).strip() for ligne in "".join(self._morceaux).splitlines())
        return "\n".join(ligne for ligne in lignes if ligne)


def texte_de_html(html_brut: str) -> str:
    """Texte d'un corps HTML. Si l'extraction échoue, ou si elle ne rend rien d'un HTML
    qui n'est pas vide, le HTML est rendu tel quel, et le journal le dit : il sera borné
    plus loin comme tout corps. Un corps vidé en silence serait une coupe silencieuse."""
    p = _TexteDeHtml()
    try:
        p.feed(html_brut)
        p.close()
    except Exception as e:  # noqa: BLE001 — un corps illisible ne doit pas tuer le run
        print(f"[texte] WARN — extraction HTML échouée ({type(e).__name__}) ; corps gardé brut, borné plus loin")
        return html_brut
    texte = p.texte()
    if not texte and html_brut.strip():
        print("[texte] WARN — extraction HTML vide ; corps gardé brut, borné plus loin")
        return html_brut
    return texte


def fetch_scholar_emails(service: Any, lookback_days: int) -> list[dict[str, str]]:
    """Récupère les emails Scholar Alerts des N derniers jours."""
    after_date = (dt.date.today() - dt.timedelta(days=lookback_days)).strftime("%Y/%m/%d")
    query = f"from:{SCHOLAR_FROM} after:{after_date}"
    print(f"[gmail] Requête : {query}")

    # Toutes les pages. Jusqu'au 2026-09-10, seule la première était lue (200 messages
    # au plus) et le surplus disparaissait sans un mot. Le volume est désormais borné
    # plus loin, à l'entrée du modèle, où chaque coupe se déclare.
    messages: list[dict[str, Any]] = []
    page: str | None = None
    while True:
        params: dict[str, Any] = {"userId": "me", "q": query, "maxResults": 200}
        if page:
            params["pageToken"] = page
        resp = service.users().messages().list(**params).execute()
        messages.extend(resp.get("messages", []))
        page = resp.get("nextPageToken")
        if not page:
            break
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

        # Préfère le contenu text/plain, sinon le texte extrait du text/html. Jusqu'au
        # 2026-09-10, ce commentaire annonçait déjà un HTML « dépouillé », mais le code
        # l'envoyait brut, styles compris. Les redirections Scholar sont déroulées
        # dans les deux cas : elles gonflent un corps sans rien lui apporter.
        body = ""
        if parsed.is_multipart():
            for part in parsed.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_content()
                    break
            if not body:
                for part in parsed.walk():
                    if part.get_content_type() == "text/html":
                        body = texte_de_html(part.get_content())
                        break
        else:
            body = parsed.get_content()
            if parsed.get_content_type() == "text/html":
                body = texte_de_html(body)
        body = _derouler_liens_scholar(body)

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


def construire_corpus(prompt: str, emails: list[dict[str, str]], borne: int) -> tuple[str, int]:
    """Message complet, chaque corps borné à `borne` caractères ; la coupe est écrite
    dans le corps lui-même. Rend (message, nombre de corps tronqués)."""
    tronques = 0
    blocs = []
    for i, e in enumerate(emails):
        corps = e["body"]
        if len(corps) > borne:
            corps = corps[:borne] + f"\n\n[… corps tronqué : {borne} caractères gardés sur {len(e['body'])}]"
            tronques += 1
        blocs.append(f"## Email {i + 1}\n\n**Sujet** : {e['subject']}\n**Date** : {e['date']}\n\n{corps}")
    message = (
        f"{prompt}\n\n"
        f"---\n\n"
        f"# Corpus à synthétiser ({len(emails)} emails Scholar Alerts)\n\n"
        + "\n\n---\n\n".join(blocs)
    )
    return message, tronques


def compter_tokens(client: Any, message: str) -> tuple[int, bool]:
    """Tokens de l'entrée : (n, True) s'ils sont comptés par l'API (messages.count_tokens),
    (estimation prudente, False) si le comptage échoue — voir OCTETS_PAR_TOKEN_PIRE_CAS."""
    try:
        r = client.messages.count_tokens(model=ANTHROPIC_MODEL, messages=[{"role": "user", "content": message}])
        return int(r.input_tokens), True
    except Exception as e:  # noqa: BLE001 — le comptage est un garde, pas une étape critique
        estime = int(len(message.encode("utf-8")) / OCTETS_PAR_TOKEN_PIRE_CAS) + 1
        print(f"[anthropic] WARN — count_tokens indisponible ({str(e)[:200]}) ; estimation prudente : {estime} tokens")
        return estime, False


def _horodatage(e: dict[str, str]) -> float:
    """Horodatage d'une alerte d'après son en-tête Date ; illisible, elle compte comme
    la plus ancienne."""
    try:
        return parsedate_to_datetime(e["date"]).timestamp()
    except (TypeError, ValueError, IndexError, OverflowError):
        return float("-inf")


def ajuster_au_budget(client: Any, prompt: str, emails: list[dict[str, str]]) -> tuple[str, dict[str, Any]]:
    """Construit un message qui tient dans BUDGET_TOKENS_ENTREE.

    1. Chaque corps est borné à CORPS_MAX_CARACTERES.
    2. Si l'entrée dépasse encore le budget, la borne est divisée par deux, jusqu'à
       BORNE_PLANCHER caractères : on garde toutes les alertes, moins profondément.
    3. Au-delà, les alertes les plus anciennes sont écartées, d'après leur en-tête Date
       (une date illisible compte comme la plus ancienne) : d'abord en proportion de
       l'excès, puis au moins une par tour.
    Tout ce qui est coupé ou écarté est compté et rendu : rien ne disparaît en silence.
    Une réduction décidée sur l'estimation de repli (comptage de l'API en échec) est
    comptée à part : l'estimation est prudente, la coupe a pu être plus forte que
    nécessaire, et le bilan le dit.
    """
    # Du plus récent au plus ancien. L'ordre de Gmail n'est pas garanti, on ne s'y fie
    # pas ; le tri est stable.
    retenus = sorted(emails, key=_horodatage, reverse=True)
    ecartes: list[dict[str, str]] = []
    borne = max(CORPS_MAX_CARACTERES, BORNE_PLANCHER)
    sur_estimation = 0  # réductions décidées alors que l'API ne comptait pas
    while True:
        message, tronques = construire_corpus(prompt, retenus, borne)
        n, par_api = compter_tokens(client, message)
        if n <= BUDGET_TOKENS_ENTREE:
            methode = ("comptés par l'API" if par_api else
                       f"estimés à {OCTETS_PAR_TOKEN_PIRE_CAS} octets par token, le comptage de l'API ayant échoué")
            return message, {"tokens": n, "methode": methode, "borne": borne, "tronques": tronques,
                             "retenus": len(retenus), "ecartes": ecartes, "sur_estimation": sur_estimation}
        if not par_api:
            sur_estimation += 1
        if borne > BORNE_PLANCHER:
            borne = max(BORNE_PLANCHER, borne // 2)
            continue
        if len(retenus) <= 1:
            fail(f"Même une seule alerte bornée à {borne} caractères dépasse le budget "
                 f"({n} > {BUDGET_TOKENS_ENTREE} tokens) : le prompt seul est-il trop long ?")
        garder = max(1, min(len(retenus) - 1, int(len(retenus) * BUDGET_TOKENS_ENTREE / n)))
        ecartes = retenus[garder:] + ecartes
        retenus = retenus[:garder]


def decrire_bilan(bilan: dict[str, Any], n_recus: int) -> str:
    """Une ligne, en nombres seulement : ce que le modèle a réellement reçu.

    Cette ligne part dans le journal du workflow, qui est PUBLIC (dépôt public) : elle
    ne contient aucun sujet d'alerte. Les sujets écartés sont nommés par pied_ecartes,
    qui ne va que dans le dépôt privé."""
    morceaux = [f"{n_recus} reçus", f"{bilan['retenus']} retenus"]
    if bilan["tronques"]:
        morceaux.append(f"{bilan['tronques']} corps tronqués à {bilan['borne']} caractères")
    if bilan["ecartes"]:
        morceaux.append(f"{len(bilan['ecartes'])} écartés faute de place, les plus anciens "
                        f"(liste en fin de synthèse)")
    if bilan["sur_estimation"]:
        morceaux.append(f"{bilan['sur_estimation']} réduction(s) décidée(s) sur estimation, le comptage de "
                        f"l'API ayant échoué : la coupe a pu être plus forte que nécessaire")
    morceaux.append(f"entrée de {bilan['tokens']} tokens, {bilan['methode']}")
    if bilan.get("arret") not in (None, "end_turn"):
        morceaux.append(f"SYNTHÈSE INTERROMPUE (stop_reason={bilan['arret']}, "
                        f"{bilan.get('tokens_sortie')} tokens de sortie) : elle s'arrête en cours de texte")
    return " · ".join(morceaux)


def pied_ecartes(bilan: dict[str, Any]) -> str:
    """Section de fin de synthèse qui nomme chaque alerte écartée ; vide sinon. Elle ne va
    que dans le dépôt privé : l'aperçu de DRY_RUN n'imprime que l'en-tête."""
    if not bilan["ecartes"]:
        return ""
    lignes = "\n".join(f"- {e['date']} — {e['subject']}" for e in bilan["ecartes"])
    cause = (f"le budget d'entrée ({BUDGET_TOKENS_ENTREE} tokens) était atteint"
             + (", selon une estimation prudente (comptage de l'API en échec) qui a pu exagérer"
                if bilan["sur_estimation"] else ""))
    return (f"\n\n---\n\n## Alertes écartées faute de place ({len(bilan['ecartes'])})\n\n"
            f"Le modèle ne les a pas lues : {cause}.\n\n{lignes}\n")


def pied_interruption(bilan: dict[str, Any]) -> str:
    """Avertissement de fin de synthèse si le modèle s'est arrêté avant la fin ; vide sinon."""
    if bilan.get("arret") in (None, "end_turn"):
        return ""
    return (f"\n\n---\n\n**⚠ Synthèse interrompue** (`stop_reason` = `{bilan['arret']}`, "
            f"{bilan.get('tokens_sortie')} tokens de sortie sur {MAX_TOKENS_SORTIE}) : "
            f"le texte ci-dessus s'arrête en cours de route.\n")


def call_anthropic(prompt: str, emails: list[dict[str, str]]) -> tuple[str, dict[str, Any]]:
    """Synthétise les alertes, l'entrée bornée par ajuster_au_budget.
    Rend (texte, bilan) : le bilan dit ce qui a été tronqué ou écarté."""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    user_message, bilan = ajuster_au_budget(client, prompt, emails)
    print(f"[anthropic] Modèle {ANTHROPIC_MODEL}, {len(user_message)} caractères en input · "
          f"{decrire_bilan(bilan, len(emails))}")
    msg = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS_SORTIE,
        messages=[{"role": "user", "content": user_message}],
    )
    # Une sortie coupée se déclare comme une entrée coupée (2026-09-10). Jusque-là,
    # stop_reason n'était jamais lu : une synthèse arrêtée à max_tokens au milieu d'une
    # phrase était commitée comme complète.
    bilan["arret"] = msg.stop_reason
    bilan["tokens_sortie"] = msg.usage.output_tokens
    if msg.stop_reason != "end_turn":
        print(f"[anthropic] WARN — synthèse interrompue : stop_reason={msg.stop_reason}, "
              f"{msg.usage.output_tokens} tokens de sortie sur {MAX_TOKENS_SORTIE}")
    else:
        print(f"[anthropic] Synthèse complète : {msg.usage.output_tokens} tokens de sortie sur {MAX_TOKENS_SORTIE}")
    return "".join(block.text for block in msg.content if block.type == "text"), bilan


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
        # L'en-tête seul, qui ne contient que des nombres : le journal est public. Jusqu'au
        # 2026-09-10, les 300 premiers caractères partaient, et avec eux le début de la
        # synthèse privée (113 caractères avant le correctif de troncature, 11 au dry run).
        print("--- Aperçu (en-tête seul) ---")
        print(content.split("\n---\n\n", 1)[0])
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
    bilan_texte: str = "",
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
        f"- **Emails analysés** : {bilan_texte or n_emails}\n"
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
    synthesis, bilan = call_anthropic(prompt, emails)
    bilan_ligne = decrire_bilan(bilan, len(emails))

    synthesis_header = (
        f"# Synthèse veille Scholar — {today.isoformat()}\n\n"
        f"**Modèle** : {ANTHROPIC_MODEL}\n"
        f"**Fenêtre** : {LOOKBACK_DAYS} jours\n"
        f"**Emails analysés** : {bilan_ligne}\n"
        f"**Prompt source** : `{PROMPT_PATH}`\n\n"
        f"---\n\n"
    )
    synthesis_full = synthesis_header + synthesis + pied_interruption(bilan) + pied_ecartes(bilan)
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
                    bilan_texte=bilan_ligne,
                )
            except Exception as notify_exc:
                print(f"[notify] WARN — notification gate-fail échouée : {notify_exc}")
            return 2
    else:
        print("[skip] Étape d'intégration corpus désactivée (RUN_INTEGRATION=0) — "
              "le cron ne fait que collecter ; l'intégration est manuelle et gatée.")

    # Etape 3 — Notification issue (best-effort, lie synthese + integration)
    notify_run_complete(today, len(emails), synthesis_path, integration_path, bilan_texte=bilan_ligne)

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
