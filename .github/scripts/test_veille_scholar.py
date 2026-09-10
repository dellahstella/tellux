"""Contrôles hors ligne des bornes du corpus de veille_scholar.py (2026-09-10).

    python .github/scripts/test_veille_scholar.py

Aucun appel réseau : le client Anthropic et Gmail sont remplacés par des doubles ; le
comptage se fait à 4 caractères par token. Chaque contrôle est écrit de façon à ÉCHOUER
si la borne qu'il vise n'existait pas — le cas n°3 reproduit le run réel du 07/09.
Lancé par le workflow avant le run : une borne cassée arrête tout avant l'appel au modèle.
"""

import base64
import importlib.util
import os
import sys
from email.message import EmailMessage
from pathlib import Path

os.environ.setdefault("CORPS_MAX_CARACTERES", "8000")
os.environ.setdefault("BUDGET_TOKENS_ENTREE", "150000")
_spec = importlib.util.spec_from_file_location("veille", Path(__file__).with_name("veille_scholar.py"))
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)


class _Comptage:
    """Double de client.messages : compte à `ratio` caractères par token."""

    def __init__(self, ratio: float = 4.0, echec: bool = False) -> None:
        self.ratio, self.echec, self.appels = ratio, echec, 0

    def count_tokens(self, model, messages):
        self.appels += 1
        if self.echec:
            raise RuntimeError("comptage indisponible")
        return type("R", (), {"input_tokens": int(len(messages[0]["content"]) / self.ratio) + 1})()


class _Client:
    def __init__(self, **kw) -> None:
        self.messages = _Comptage(**kw)


def verifie(cond: bool, msg: str) -> None:
    if not cond:
        print("ÉCHEC :", msg)
        sys.exit(1)
    print("ok :", msg)


# 1. HTML → texte : styles écartés, entités décodées, redirection Scholar déroulée
html = ('<html><head><style>.x{color:red}</style></head><body><div>'
        '<a href="https://scholar.google.com/scholar_url?url=https://doi.org/10.1000/abc&amp;hl=fr&amp;sa=X">'
        'Titre de l&#39;article</a><br>Auteurs A, B</div></body></html>')
t = v.texte_de_html(html)
verifie("color:red" not in t, "le CSS n'arrive pas dans le texte")
verifie("<https://doi.org/10.1000/abc>" in t, "la redirection Scholar est déroulée vers sa cible")
verifie("Titre de l'article" in t and "Auteurs A, B" in t, "le texte et les entités HTML sont gardés et décodés")

# 2. text/plain : redirections déroulées, le reste intact
brut = "Voir https://scholar.google.fr/scholar_url?url=https://example.org/p.pdf&hl=fr&sa=X&ei=abc ici"
verifie(v._derouler_liens_scholar(brut) == "Voir https://example.org/p.pdf ici", "redirection déroulée dans un text/plain")

# 3. le run du 07/09 : 48 alertes de 24 000 caractères — sous le budget, aucune écartée
emails = [{"subject": f"alerte {i}", "date": "", "body": "x" * 24000} for i in range(48)]
msg, bilan = v.ajuster_au_budget(_Client(), "PROMPT", emails)
verifie(bilan["tokens"] <= v.BUDGET_TOKENS_ENTREE, f"entrée sous le budget ({bilan['tokens']} tokens)")
verifie(bilan["retenus"] == 48 and not bilan["ecartes"], "les 48 alertes sont gardées")
verifie(bilan["tronques"] == 48 and msg.count("[… corps tronqué") == 48, "chaque corps tronqué le dit dans le message")
verifie(v.pied_ecartes(bilan) == "", "sans écartée, pas de pied de synthèse")

# 4. volume extrême : 2000 alertes — borne au plancher avant tout écart, écartées nommées
emails = [{"subject": f"alerte {i}", "date": "", "body": "y" * 24000} for i in range(2000)]
msg, bilan = v.ajuster_au_budget(_Client(), "PROMPT", emails)
verifie(bilan["tokens"] <= v.BUDGET_TOKENS_ENTREE, "même à 2000 alertes, l'entrée tient dans le budget")
verifie(bilan["borne"] == v.BORNE_PLANCHER, "la borne descend au plancher avant qu'une alerte soit écartée")
verifie(bilan["ecartes"] and all(e["subject"] != "alerte 0" for e in bilan["ecartes"]), "à dates égales, l'ordre reçu est gardé")
verifie(bilan["retenus"] + len(bilan["ecartes"]) == 2000, "aucune alerte hors comptabilité")
ligne = v.decrire_bilan(bilan, 2000)
verifie("écartés faute de place" in ligne and "alerte " not in ligne,
        "la ligne de bilan compte les écartées sans les nommer (elle part dans un journal public)")
pied = v.pied_ecartes(bilan)
verifie(all(f"— {e['subject']}\n" in pied for e in bilan["ecartes"]), "le pied de synthèse nomme chaque écartée")

# 5. comptage de l'API indisponible : estimation prudente, et elle se déclare
msg, bilan = v.ajuster_au_budget(_Client(echec=True), "PROMPT", [{"subject": "a", "date": "", "body": "z" * 1000}])
verifie("estimés" in bilan["methode"], "l'estimation de repli se déclare dans le bilan")

# 6. petit volume : rien de tronqué, un seul appel de comptage
cli = _Client()
msg, bilan = v.ajuster_au_budget(cli, "PROMPT", [{"subject": "a", "date": "", "body": "court"}])
verifie(bilan["tronques"] == 0 and cli.messages.appels == 1, "rien de tronqué, un seul comptage")

# 7. l'écartée est la plus ancienne par sa DATE, pas la dernière de la liste
budget = v.BUDGET_TOKENS_ENTREE
v.BUDGET_TOKENS_ENTREE = 350
emails = [{"subject": s, "date": d, "body": "w" * 24000} for s, d in [
    ("ancienne", "Mon, 31 Aug 2026 08:00:00 +0000"),
    ("recente", "Sun, 06 Sep 2026 08:00:00 +0000"),
    ("milieu", "Thu, 03 Sep 2026 08:00:00 +0000"),
]]
msg, bilan = v.ajuster_au_budget(_Client(), "PROMPT", emails)
v.BUDGET_TOKENS_ENTREE = budget
verifie([e["subject"] for e in bilan["ecartes"]] == ["ancienne"],
        "l'écartée est la plus ancienne selon l'en-tête Date, pas la dernière reçue")


# 8. Gmail : toutes les pages lues, un corps HTML seul arrive en texte
def _brut(sujet: str, corps_html: str) -> str:
    m = EmailMessage()
    m["Subject"], m["Date"] = sujet, "Mon, 07 Sep 2026 08:00:00 +0000"
    m.set_content(corps_html, subtype="html")
    return base64.urlsafe_b64encode(m.as_bytes()).decode()


class _Req:
    def __init__(self, r) -> None:
        self.r = r

    def execute(self):
        return self.r


class _Messages:
    pages = {None: {"messages": [{"id": "a"}, {"id": "b"}], "nextPageToken": "p2"}, "p2": {"messages": [{"id": "c"}]}}

    def list(self, userId, q, maxResults, pageToken=None):
        return _Req(self.pages[pageToken])

    def get(self, userId, id, format):
        return _Req({"raw": _brut(f"sujet {id}", f"<style>p{{margin:0}}</style><p>corps {id}</p>")})


class _Service:
    def users(self):
        return type("U", (), {"messages": lambda _self: _Messages()})()


recus = v.fetch_scholar_emails(_Service(), 7)
verifie([e["subject"] for e in recus] == ["sujet a", "sujet b", "sujet c"], "toutes les pages de Gmail sont lues")
verifie(recus[2]["body"] == "corps c", "un corps HTML seul arrive en texte, sans son style")

print("tous les contrôles passent")
