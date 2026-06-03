"""
refresh_oauth_token.py — Régénère le refresh_token Gmail OAuth et upload
les secrets GitHub correspondants.

Procédure de bout en bout (Option B+D du brief 2026-05-26) :

1. Soleil reset le Client Secret côté GCP Console (politique Google : le
   Secret n'est visible qu'une seule fois à la création).
2. Soleil crée le fichier temp `~/.tellux_oauth_temp.json` :
       {"client_id": "<...apps.googleusercontent.com>",
        "client_secret": "<...>"}
3. Code lance ce script : ouverture browser, Soleil clique « Autoriser ».
4. Script récupère le refresh_token et upload les 3 secrets dans GitHub
   via `gh secret set` (lecture stdin, pas d'arg CLI exposant le secret).
5. Script supprime le fichier temp.

Pré-requis :
- google-auth-oauthlib installé (`pip install google-auth-oauthlib`)
- gh CLI authentifié sur `dellahstella/tellux`
- App OAuth GCP en statut « Production » (sinon le refresh_token re-expire
  tous les 7 jours)

Usage :
    python .github/scripts/refresh_oauth_token.py

Aucun secret n'est imprimé en stdout. La longueur du refresh_token est
affichée à titre de validation.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TEMP_PATH = Path.home() / ".tellux_oauth_temp.json"
REPO = "dellahstella/tellux"


def fail(msg: str, code: int = 1) -> None:
    print(f"[ERREUR] {msg}", file=sys.stderr)
    sys.exit(code)


def load_temp_credentials() -> tuple[str, str]:
    """Charge client_id + client_secret depuis le fichier temp local."""
    if not TEMP_PATH.exists():
        fail(
            f"Fichier temp absent : {TEMP_PATH}\n"
            f"  Crée-le avec le format :\n"
            f'    {{"client_id": "<...apps.googleusercontent.com>", "client_secret": "<...>"}}\n'
            f"  Source : GCP Console > APIs & Services > Credentials > "
            f"OAuth 2.0 Client IDs > tellux-veille-github-actions.\n"
            f"  Si le Client Secret est masqué, faire 'Reset secret' "
            f"sur la même fiche."
        )
    try:
        data = json.loads(TEMP_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        fail(f"JSON invalide dans {TEMP_PATH} : {e}")

    if "client_id" not in data or "client_secret" not in data:
        fail(
            f"Clés manquantes dans {TEMP_PATH}. "
            f"Format attendu : {{'client_id': ..., 'client_secret': ...}}."
        )
    return data["client_id"], data["client_secret"]


def run_oauth_flow(client_id: str, client_secret: str) -> str:
    """Lance le flow Desktop OAuth (browser local). Retourne le refresh_token."""
    config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost"],
        }
    }
    flow = InstalledAppFlow.from_client_config(config, SCOPES)

    print("[info] Ouverture du navigateur pour autorisation Google...")
    print("[info] Compte cible : tellux.veille@gmail.com")
    print("[info] Scope demandé : gmail.readonly")
    # access_type=offline + prompt=consent garantit la délivrance d'un
    # refresh_token même si le compte a déjà autorisé ce client (sans
    # ces flags, Google ne renvoie qu'un access_token et le refresh_token
    # est null → impossible de l'utiliser dans GitHub Actions).
    flow.run_local_server(
        port=0,
        open_browser=True,
        access_type="offline",
        prompt="consent",
    )

    refresh_token = flow.credentials.refresh_token
    if not refresh_token:
        fail(
            "Aucun refresh_token retourné par Google. Causes possibles :\n"
            "  - Compte a déjà autorisé le client sans demander refresh\n"
            "  - Révoquer l'accès sur https://myaccount.google.com/permissions"
            " puis relancer ce script\n"
            "  - Vérifier que l'app GCP est bien en statut 'Production'",
            code=2,
        )
    return refresh_token


def upload_secret(name: str, value: str) -> None:
    """Upload un secret dans GitHub via `gh secret set` (lecture stdin)."""
    result = subprocess.run(
        ["gh", "secret", "set", name, "--repo", REPO],
        input=value,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        fail(
            f"Upload secret {name} échoué (rc={result.returncode}) : "
            f"{result.stderr.strip()}"
        )
    print(f"[ok] Secret {name} uploadé sur {REPO}")


def main() -> int:
    print(f"[start] Refresh OAuth token Tellux veille — {TEMP_PATH}")
    client_id, client_secret = load_temp_credentials()

    refresh_token = run_oauth_flow(client_id, client_secret)
    print(f"[ok] Refresh token généré (longueur : {len(refresh_token)} chars)")

    # Upload des 3 secrets. Tous ré-uploadés systématiquement :
    # - GMAIL_REFRESH_TOKEN change forcément
    # - GMAIL_CLIENT_SECRET peut avoir été reset par Soleil (cas Option B)
    # - GMAIL_CLIENT_ID idempotent si inchangé
    print()
    print("[upload] Mise à jour des secrets GitHub...")
    upload_secret("GMAIL_CLIENT_ID", client_id)
    upload_secret("GMAIL_CLIENT_SECRET", client_secret)
    upload_secret("GMAIL_REFRESH_TOKEN", refresh_token)

    # Nettoyage : suppression du fichier temp.
    TEMP_PATH.unlink(missing_ok=True)
    print(f"[clean] {TEMP_PATH} supprimé")

    print()
    print("[done] Refresh OAuth terminé. Prochaine étape :")
    print(
        "  gh workflow run veille_scholar.yml "
        "-f lookback_days=14 -f dry_run=0 --repo dellahstella/tellux"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
