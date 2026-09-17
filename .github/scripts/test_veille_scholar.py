"""Contrôles hors ligne des bornes du corpus de veille_scholar.py (2026-09-10).

    python .github/scripts/test_veille_scholar.py

Aucun appel réseau : Anthropic, Gmail et l'API GitHub sont remplacés par des doubles ; le
comptage se fait à 4 caractères par token. Chaque contrôle est écrit pour ÉCHOUER si ce
qu'il garde disparaissait. La revue adversariale du 2026-09-10 l'a vérifié par mutation :
onze mutants restaient verts dans la première version, et chacun a désormais son contrôle
(M08 borne de corps, M09-M10 repli d'estimation, M12 écarts en plusieurs tours, M13-M14 et
M18-M20 déclarations au bilan, à l'en-tête et à l'issue, M15-M16 chemins de fetch).
Lancé par le workflow avant le run : une borne cassée arrête tout avant l'appel au modèle.

Ce que le module imprime pendant ces contrôles est capturé, jamais laissé passer : dans le
journal du workflow, une ligne « [gmail] 3 message(s) trouvé(s) » venue d'un double se lit
comme un événement réel (constaté au dry run du 2026-09-10). Le journal ne montre que les
lignes « ok : ».
"""

import base64
import importlib.util
import io
import json
import os
import sys
from contextlib import redirect_stderr, redirect_stdout
from email.message import EmailMessage
from pathlib import Path

import httplib2
from googleapiclient.errors import HttpError

os.environ.setdefault("CORPS_MAX_CARACTERES", "8000")
os.environ.setdefault("BUDGET_TOKENS_ENTREE", "150000")
os.environ.setdefault("ANTHROPIC_API_KEY", "factice")
os.environ.setdefault("GITHUB_PAT", "factice")
# Pas d'attente réelle en test (tests 16-18) : seule la logique de reprise est
# vérifiée, pas le minutage.
os.environ.setdefault("GMAIL_PAUSE_ENTRE_APPELS", "0")
_spec = importlib.util.spec_from_file_location("veille", Path(__file__).with_name("veille_scholar.py"))
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)


# --- doubles --------------------------------------------------------------------------

class _Comptage:
    """Double de client.messages : compte à `ratio` caractères par token."""

    def __init__(self, ratio: float = 4.0, echec: bool = False) -> None:
        self.ratio, self.echec, self.appels = ratio, echec, 0

    def count_tokens(self, model, messages):
        self.appels += 1
        if self.echec:
            raise RuntimeError("comptage indisponible")
        return type("R", (), {"input_tokens": int(len(messages[0]["content"]) / self.ratio) + 1})()


class _ComptageEchecPremier(_Comptage):
    """Le premier comptage échoue (529), les suivants réussissent."""

    def count_tokens(self, model, messages):
        self.appels += 1
        if self.appels == 1:
            raise RuntimeError("529 overloaded")
        return type("R", (), {"input_tokens": int(len(messages[0]["content"]) / self.ratio) + 1})()


class _Client:
    def __init__(self, **kw) -> None:
        self.messages = _Comptage(**kw)


class _Reponse:
    """Réponse de messages.create, arrêtée pour la raison `arret`. `texte` et `tokens` par
    défaut reproduisent le comportement d'origine (un seul appel, sans reprise)."""

    def __init__(self, arret: str, texte: str | None = None, tokens: int | None = None) -> None:
        self.content = [type("B", (), {"type": "text", "text": texte or "## Axe 1\n- article A, conclusi"})()]
        self.stop_reason = arret
        self.usage = type("U", (), {"output_tokens": tokens if tokens is not None else (8192 if arret == "max_tokens" else 1200)})()


class _StreamCM:
    """Double du context manager de client.messages.stream(...) (2026-09-17 : la
    production est passée de .create() à .stream() — un MAX_TOKENS_SORTIE élevé exige
    le streaming côté SDK réel). N'émet aucun évènement intermédiaire : seul
    get_final_message() est exercé, comme dans le code de production."""

    def __init__(self, reponse) -> None:
        self._reponse = reponse

    def __enter__(self) -> "_StreamCM":
        return self

    def __exit__(self, *exc: object) -> bool:
        return False

    def get_final_message(self):
        return self._reponse


def _client_complet(arret: str) -> _Client:
    c = _Client()
    c.messages.stream = lambda **kw: _StreamCM(_Reponse(arret))
    return c


class _MessagesSuite:
    """Double dont chaque appel à stream() rend la réponse suivante de `reponses`,
    répétant la dernière une fois la liste épuisée (utile pour "toujours max_tokens")."""

    def __init__(self, reponses: list[_Reponse]) -> None:
        self._reponses = reponses
        self.appels = 0

    def stream(self, **kw):
        r = self._reponses[min(self.appels, len(self._reponses) - 1)]
        self.appels += 1
        return _StreamCM(r)


class _ClientSuite:
    def __init__(self, reponses: list[_Reponse]) -> None:
        self.messages = _MessagesSuite(reponses)


class _Req:
    def __init__(self, r) -> None:
        self.r = r

    def execute(self):
        return self.r


def _service(messages) -> object:
    """Double du service Gmail autour d'un objet qui a list() et get()."""
    return type("S", (), {"users": lambda _s: type("U", (), {"messages": lambda _u: messages})()})()


def _http_error_quota(status: int = 403, reason: str = "rateLimitExceeded") -> HttpError:
    """Construit une HttpError dans sa forme réelle googleapiclient : resp avec un
    .status, content JSON avec error.errors[].reason — la même forme que celle
    rencontrée en production (403, reason=rateLimitExceeded, "Units per minute per
    user")."""
    contenu = json.dumps({
        "error": {
            "code": status,
            "message": "Quota exceeded for quota metric 'Total Query Cost' and limit "
                        "'Units per minute per user' of service 'gmail.googleapis.com'.",
            "errors": [{"message": "Quota exceeded", "domain": "usageLimits", "reason": reason}],
        }
    }).encode("utf-8")
    return HttpError(httplib2.Response({"status": status}), contenu)


class _MessagesQuota:
    """Double Gmail : .get() lève `erreur()` pour les `echecs` premiers appels sur l'id
    `cible`, réussit ensuite (et réussit du premier coup pour tout autre id)."""

    def __init__(self, echecs: int, cible: str, erreur=_http_error_quota) -> None:
        self.echecs, self.cible, self.erreur = echecs, cible, erreur
        self.appels: dict[str, int] = {}

    def list(self, userId, q, maxResults, pageToken=None):
        return _Req({"messages": [{"id": self.cible}]})

    def get(self, userId, id, format):
        self.appels[id] = self.appels.get(id, 0) + 1
        if id == self.cible and self.appels[id] <= self.echecs:
            raise self.erreur()
        m = _courriel("sujet retenté")
        m.set_content("corps ok")
        return _Req({"raw": _brut(m)})


def _brut(m: EmailMessage) -> str:
    return base64.urlsafe_b64encode(m.as_bytes()).decode()


def _courriel(sujet: str, date: str = "Mon, 07 Sep 2026 08:00:00 +0000") -> EmailMessage:
    m = EmailMessage()
    m["Subject"], m["Date"] = sujet, date
    return m


def verifie(cond: bool, msg: str) -> None:
    if not cond:
        print("ÉCHEC :", msg)
        sys.exit(1)
    print("ok :", msg)


def capture(f, *args):
    """Appelle f en capturant ce qu'elle imprime ; rend (résultat, texte imprimé)."""
    tampon = io.StringIO()
    with redirect_stdout(tampon):
        r = f(*args)
    return r, tampon.getvalue()


def capture_fail(f, *args):
    """Appelle f censée échouer via fail() (print stderr + sys.exit) ; rend (code, stderr).
    (code, stderr) = (None, "") si f n'a pas échoué. stdout est capturé aussi (jamais
    laissé passer, même si f imprime avant d'échouer) mais pas rendu : seul stderr porte
    le message de fail()."""
    tampon, tampon_out = io.StringIO(), io.StringIO()
    try:
        with redirect_stderr(tampon), redirect_stdout(tampon_out):
            f(*args)
        return None, ""
    except SystemExit as e:
        return e.code, tampon.getvalue()


# --- 1. HTML → texte ------------------------------------------------------------------
html = ('<html><head><style>.x{color:red}</style></head><body><div>'
        '<a href="https://scholar.google.com/scholar_url?url=https://doi.org/10.1000/abc&amp;hl=fr&amp;sa=X">'
        'Titre de l&#39;article</a><br>Auteurs A, B</div>'
        '<a href="https://scholar.google.com/citations?update_op=email_library_add&amp;info=x&amp;citsig=y"><img src="e.png"></a>'
        '<a href="https://scholar.google.com/scholar_share?ss=tw&amp;url=https://doi.org/10.1000/abc&amp;rt=Titre"><img src="t.png"></a>'
        '</body></html>')
t = v.texte_de_html(html)
verifie("color:red" not in t, "le CSS n'arrive pas dans le texte")
verifie("<https://doi.org/10.1000/abc>" in t, "la redirection Scholar est déroulée vers sa cible")
verifie("Titre de l'article" in t and "Auteurs A, B" in t, "le texte et les entités HTML sont gardés et décodés")
verifie("citations?" not in t and "scholar_share" not in t, "les liens d'action de Scholar (enregistrer, partager) sont écartés")

t = v.texte_de_html('<!doctype html><html><head><meta charset="utf-8"><title>Alerte</title><body><h3>Titre A</h3></body></html>')
verifie("Titre A" in t, "un HTML sans </head> garde son texte")
t, sortie = capture(v.texte_de_html, "<html><head><style>p{margin:0}<body><p>corps perdu</p></body></html>")
verifie("corps perdu" in t and "extraction HTML vide" in sortie, "une extraction vide rend le HTML brut, et le journal le dit")

# --- 2. text/plain : redirections déroulées, le reste intact ----------------------------
brut = "Voir https://scholar.google.fr/scholar_url?url=https://example.org/p.pdf&hl=fr&sa=X&ei=abc ici"
verifie(v._derouler_liens_scholar(brut) == "Voir https://example.org/p.pdf ici", "redirection déroulée dans un text/plain")

# --- 3. le run du 07/09 : 48 alertes de 24 000 caractères -------------------------------
emails = [{"subject": f"alerte {i}", "date": "", "body": "x" * 24000} for i in range(48)]
msg, bilan = v.ajuster_au_budget(_Client(), "PROMPT", emails)
verifie(bilan["tokens"] <= v.BUDGET_TOKENS_ENTREE, f"entrée sous le budget ({bilan['tokens']} tokens)")
verifie(bilan["retenus"] == 48 and not bilan["ecartes"], "les 48 alertes sont gardées")
verifie(bilan["borne"] == v.CORPS_MAX_CARACTERES, "sous le budget, la borne reste CORPS_MAX_CARACTERES")
verifie(bilan["tronques"] == 48 and msg.count("[… corps tronqué") == 48, "chaque corps tronqué le dit dans le message")
verifie(f"48 corps tronqués à {v.CORPS_MAX_CARACTERES}" in v.decrire_bilan(bilan, 48), "la ligne de bilan déclare les corps tronqués")
verifie(v.pied_ecartes(bilan) == "", "sans écartée, pas de pied de synthèse")
msg, bilan = v.ajuster_au_budget(_Client(), "PROMPT", [{"subject": f"s{i}", "date": "", "body": "q" * 20000} for i in range(2)])
verifie(bilan["tronques"] == 2 and "q" * (v.CORPS_MAX_CARACTERES + 1) not in msg,
        "petit volume : chaque corps reste borné à CORPS_MAX_CARACTERES")

# --- 4. volume extrême : 2000 alertes ---------------------------------------------------
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

# --- 4b. écarts en plusieurs tours : récentes longues, anciennes courtes ----------------
budget = v.BUDGET_TOKENS_ENTREE
v.BUDGET_TOKENS_ENTREE = 3000
emails = ([{"subject": f"sujet-{i:03d}", "date": "", "body": "r" * 5000} for i in range(50)]
          + [{"subject": f"sujet-{i:03d}", "date": "", "body": "r" * 10} for i in range(50, 100)])
msg, bilan = v.ajuster_au_budget(_Client(), "PROMPT", emails)
pied = v.pied_ecartes(bilan)
v.BUDGET_TOKENS_ENTREE = budget
verifie(bilan["retenus"] + len(bilan["ecartes"]) == 100
        and all((f"**Sujet** : {e['subject']}\n" in msg) != (f"— {e['subject']}\n" in pied) for e in emails),
        "écarts en plusieurs tours : chaque alerte est soit lue, soit nommée en pied — jamais les deux, jamais aucune")

# --- 5. comptage de l'API indisponible : estimation prudente, déclarée -----------------
emails = [{"subject": f"alerte {i}", "date": "", "body": "z" * 24000} for i in range(60)]
(msg, bilan), sortie = capture(v.ajuster_au_budget, _Client(echec=True), "PROMPT", emails)
verifie("estimés" in bilan["methode"] and "estimés" in v.decrire_bilan(bilan, 60),
        "l'estimation de repli se déclare, jusque dans la ligne de bilan")
verifie("estimation prudente" in sortie, "l'échec du comptage est signalé au journal")
verifie(len(msg) / 2.36 <= v.BUDGET_TOKENS_ENTREE,
        "l'estimation de repli est prudente : au pire rapport mesuré (2,36), l'entrée tient dans le budget")

# --- 6. petit volume : rien de tronqué, un seul comptage --------------------------------
cli = _Client()
msg, bilan = v.ajuster_au_budget(cli, "PROMPT", [{"subject": "a", "date": "", "body": "court"}])
verifie(bilan["tronques"] == 0 and cli.messages.appels == 1, "rien de tronqué, un seul comptage")

# --- 7. l'écartée est la plus ancienne par sa DATE, pas la dernière de la liste ---------
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


# --- 8. Gmail : toutes les pages, et chaque forme de corps par le vrai chemin de fetch ---
def _html_seul(sujet: str, corps: str) -> str:
    m = _courriel(sujet)
    m.set_content(corps, subtype="html")
    return _brut(m)


def _alternative_html(sujet: str, corps: str) -> str:
    m = _courriel(sujet)
    m.add_alternative(corps, subtype="html")
    return _brut(m)


def _texte(sujet: str, corps: str) -> str:
    m = _courriel(sujet)
    m.set_content(corps)
    return _brut(m)


class _Messages:
    pages = {None: {"messages": [{"id": "a"}, {"id": "b"}], "nextPageToken": "p2"}, "p2": {"messages": [{"id": "c"}]}}
    corps = {
        "a": lambda: _html_seul("sujet a", "<style>p{margin:0}</style><p>corps a</p>"),
        "b": lambda: _alternative_html("sujet b", "<style>p{margin:0}</style><p>corps b</p>"),
        "c": lambda: _texte("sujet c", "Voir https://scholar.google.fr/scholar_url?url=https://example.org/p.pdf&hl=fr&sa=X ici"),
    }

    def list(self, userId, q, maxResults, pageToken=None):
        return _Req(self.pages[pageToken])

    def get(self, userId, id, format):
        return _Req({"raw": self.corps[id]()})


recus, sortie = capture(v.fetch_scholar_emails, _service(_Messages()), 7)
verifie([e["subject"] for e in recus] == ["sujet a", "sujet b", "sujet c"], "toutes les pages de Gmail sont lues")
verifie("3 message(s) trouvé(s)" in sortie, "le compte annoncé au journal couvre toutes les pages")
verifie(recus[0]["body"] == "corps a" and recus[1]["body"] == "corps b",
        "un corps HTML, seul ou dans un multipart, arrive en texte, sans son style")
verifie("https://example.org/p.pdf" in recus[2]["body"] and "scholar_url" not in recus[2]["body"],
        "un text/plain arrive avec ses redirections Scholar déroulées")

# --- 9. une réduction décidée sur l'estimation de repli est déclarée --------------------
cli = _Client()
cli.messages = _ComptageEchecPremier()
emails = [{"subject": f"alerte {i}", "date": "", "body": "x" * 24000} for i in range(48)]
(msg, bilan), sortie = capture(v.ajuster_au_budget, cli, "PROMPT", emails)
verifie(bilan["sur_estimation"] == 1 and bilan["borne"] == 4000 and bilan["methode"] == "comptés par l'API",
        "une borne réduite sur estimation, puis comptée par l'API")
verifie("sur estimation" in v.decrire_bilan(bilan, 48), "le bilan dit que la coupe a été décidée sur estimation")

# --- 10. le repli ne sous-estime pas une écriture idéographique -------------------------
(n_est, par_api), sortie = capture(v.compter_tokens, _Client(echec=True), "漢" * 1000)
verifie(not par_api and n_est >= 1000, f"1000 idéogrammes estimés à {n_est} tokens, pas moins de 1000")

# --- 11. une synthèse arrêtée à max_tokens se déclare ; une synthèse complète, non ------
_origine = v.anthropic.Anthropic
for arret in ("max_tokens", "end_turn"):
    v.anthropic.Anthropic = lambda api_key, _a=arret: _client_complet(_a)
    (texte, bilan), sortie = capture(v.call_anthropic, "PROMPT", [{"subject": "a", "date": "", "body": "court"}])
    ligne, pied = v.decrire_bilan(bilan, 1), v.pied_interruption(bilan)
    if arret == "max_tokens":
        verifie("SYNTHÈSE INTERROMPUE" in ligne and "max_tokens" in pied and "synthèse interrompue" in sortie,
                "une synthèse arrêtée à max_tokens est déclarée au bilan, en fin de synthèse et au journal")
    else:
        verifie("INTERROMPUE" not in ligne and pied == "" and "Synthèse complète" in sortie,
                "une synthèse complète n'est pas déclarée interrompue")
v.anthropic.Anthropic = _origine

# --- 11b. reprise sur sortie saturée : les textes se concatènent, le total conclut -----
v.anthropic.Anthropic = lambda api_key: _ClientSuite([
    _Reponse("max_tokens", texte="Première moitié. ", tokens=40000),
    _Reponse("end_turn", texte="seconde moitié.", tokens=1500),
])
(texte, bilan), sortie = capture(v.call_anthropic, "PROMPT", [{"subject": "a", "date": "", "body": "court"}])
v.anthropic.Anthropic = _origine
verifie(texte == "Première moitié. seconde moitié.",
        "une sortie saturée puis complète reprend au bon endroit : les deux textes se concatènent dans l'ordre")
verifie(bilan["arret"] == "end_turn" and "INTERROMPUE" not in v.decrire_bilan(bilan, 1) and v.pied_interruption(bilan) == "",
        "une synthèse complétée par une reprise n'est pas déclarée interrompue")
verifie(bilan["tokens_sortie"] == 40000 + 1500,
        "le compte de tokens de sortie cumule les deux appels de la reprise, pas seulement le dernier")

# --- 11c. sortie saturée à chaque appel : la reprise s'arrête à son plafond, sans avaler --
v.anthropic.Anthropic = lambda api_key: _ClientSuite([_Reponse("max_tokens", texte="bloqué. ", tokens=40000)])
(texte, bilan), sortie = capture(v.call_anthropic, "PROMPT", [{"subject": "a", "date": "", "body": "court"}])
v.anthropic.Anthropic = _origine
verifie(bilan["arret"] == "max_tokens", "toujours saturé : l'arrêt déclaré reste max_tokens, jamais avalé au plafond de reprises")
verifie(bilan["tokens_sortie"] == v.SORTIE_TENTATIVES_MAX * 40000,
        f"le compte de tokens de sortie couvre les {v.SORTIE_TENTATIVES_MAX} tentatives tentées, pas seulement la dernière")
verifie(sortie.count("sortie saturée") == v.SORTIE_TENTATIVES_MAX - 1,
        f"exactement {v.SORTIE_TENTATIVES_MAX} tentatives sont faites (la dernière ne déclare plus de reprise) : le plafond est respecté")
verifie("SYNTHÈSE INTERROMPUE" in v.decrire_bilan(bilan, 1) and "synthèse interrompue" in sortie,
        "le plafond de reprises atteint sans conclure reste déclaré interrompu, jamais avalé en silence")

# --- 12. l'aperçu DRY_RUN n'imprime que l'en-tête ---------------------------------------
v.DRY_RUN = True
contenu = ("# Synthèse veille Scholar — 2026-09-10\n\n**Emails analysés** : 3 reçus · 3 retenus\n\n---\n\n"
           "SYNTHESE-PRIVEE : ce texte ne doit pas atteindre le journal public")
_, sortie = capture(v.commit_synthesis, contenu, v.dt.date(2026, 9, 10))
v.DRY_RUN = False
verifie("SYNTHESE-PRIVEE" not in sortie and "3 reçus" in sortie, "l'aperçu DRY_RUN n'imprime que l'en-tête")


# --- 13. main() de bout en bout : le bilan atteint l'en-tête commité et l'issue ---------
class _MessagesMain:
    def list(self, userId, q, maxResults, pageToken=None):
        return _Req({"messages": [{"id": f"{i:02d}"} for i in range(30)]})

    def get(self, userId, id, format):
        m = _courriel(f"sujet-main-{id}", f"Mon, {7 - int(id) // 10:02d} Sep 2026 08:{int(id):02d}:00 +0000")
        m.set_content("<p>" + "mot " * 1500 + "</p>", subtype="html")
        return _Req({"raw": _brut(m)})


class _RepHttp:
    def __init__(self, code: int, js=None) -> None:
        self.status_code, self._js, self.text = code, js or {}, ""

    def json(self):
        return self._js


envois: dict[str, str] = {}


def _put(url, headers=None, json=None, timeout=None):
    envois["synthese"] = base64.b64decode(json["content"]).decode("utf-8")
    return _RepHttp(201)


def _post(url, headers=None, json=None, timeout=None):
    envois["issue"] = json["body"]
    return _RepHttp(201, {"html_url": "https://example.invalid/issue"})


remplaces = {
    "check_env": lambda: None,
    "build_gmail_credentials": lambda: None,
    "build": lambda *a, **k: _service(_MessagesMain()),
    "fetch_prompt_from_private_repo": lambda *a, **k: "PROMPT",
}
sauves = {k: getattr(v, k) for k in remplaces}
sauves_http = (v.requests.get, v.requests.put, v.requests.post)
sauves_etat = (v.BUDGET_TOKENS_ENTREE, v.DRY_RUN, v.RUN_INTEGRATION)
for k, f in remplaces.items():
    setattr(v, k, f)
v.requests.get, v.requests.put, v.requests.post = (lambda *a, **k: _RepHttp(404)), _put, _post
v.anthropic.Anthropic = lambda api_key: _client_complet("end_turn")
v.BUDGET_TOKENS_ENTREE, v.DRY_RUN, v.RUN_INTEGRATION = 3000, False, False
try:
    rc, sortie = capture(v.main)
finally:
    for k, f in sauves.items():
        setattr(v, k, f)
    v.requests.get, v.requests.put, v.requests.post = sauves_http
    v.anthropic.Anthropic = _origine
    v.BUDGET_TOKENS_ENTREE, v.DRY_RUN, v.RUN_INTEGRATION = sauves_etat
entete = envois.get("synthese", "").split("\n---\n\n", 1)[0]
verifie(rc == 0 and "corps tronqués à" in entete and "écartés faute de place" in entete,
        "main() : l'en-tête de la synthèse commitée porte le bilan, coupes comprises")
verifie("## Alertes écartées faute de place" in envois.get("synthese", ""), "main() : la synthèse commitée nomme les écartées en pied")
verifie("corps tronqués à" in envois.get("issue", "") and "écartés faute de place" in envois.get("issue", ""),
        "main() : l'issue porte le bilan")
verifie("sujet-main-" not in sortie, "main() : le journal ne nomme aucune alerte")

# --- 14. UNTIL_DATE : requête bornée des deux côtés, et fenêtre glissante inchangée sans lui ---
_, sortie_bornee = capture(v.fetch_scholar_emails, _service(_Messages()), 7, v.dt.date(2026, 9, 8))
verifie(f"from:{v.SCHOLAR_FROM} after:2026/09/01 before:2026/09/08" in sortie_bornee,
        "UNTIL_DATE fixé : la requête devient after:(UNTIL_DATE - lookback) before:UNTIL_DATE")

# Régression : mêmes deux arguments qu'au test 8 (aucun until_date) — la requête ne doit
# porter aucun before: et rester la fenêtre glissante jusqu'à aujourd'hui, comme avant
# l'ajout d'UNTIL_DATE.
_, sortie_glissante = capture(v.fetch_scholar_emails, _service(_Messages()), 7)
verifie("before:" not in sortie_glissante and f"from:{v.SCHOLAR_FROM} after:" in sortie_glissante,
        "sans UNTIL_DATE, la requête reste la fenêtre glissante d'origine (comportement inchangé)")

# --- 15. UNTIL_DATE malformée : fail() explicite, jamais un before: silencieusement faux ---
verifie(v.parse_until_date("") is None, "UNTIL_DATE absente : pas de borne de fin (défaut)")
verifie(v.parse_until_date("2026-09-08") == v.dt.date(2026, 9, 8), "UNTIL_DATE ISO valide est parsée")
code, err = capture_fail(v.parse_until_date, "08/09/2026")
verifie(code == 1 and "UNTIL_DATE" in err, "UNTIL_DATE illisible échoue clairement via fail() (sys.exit(1))")
code, err = capture_fail(v.parse_until_date, "2026-13-40")
verifie(code == 1 and "UNTIL_DATE" in err, "UNTIL_DATE calendaire impossible échoue aussi via fail()")

# --- 16. quota Gmail : reprise avec backoff jusqu'au succès, la reprise se déclare -----
service_quota = _MessagesQuota(echecs=2, cible="q1")
recus, sortie = capture(v.fetch_scholar_emails, _service(service_quota), 7)
verifie(len(recus) == 1 and recus[0]["subject"] == "sujet retenté",
        "le message finit par être récupéré après reprise sur dépassement de quota")
verifie(service_quota.appels["q1"] == 3, "2 échecs de quota puis un succès : 3 tentatives au total")
verifie("quota" in sortie.lower() and "tentative 1/5" in sortie and "tentative 2/5" in sortie,
        "chaque reprise se déclare au journal (une ligne par tentative retentée)")

# --- 17. quota Gmail épuisé : le run échoue plutôt que de continuer sans le message -----
service_epuise = _MessagesQuota(echecs=99, cible="q2")  # ne réussit jamais
code, err = capture_fail(v.fetch_scholar_emails, _service(service_epuise), 7)
verifie(code == 1 and "quota" in err.lower() and "q2" in err and "5 tentative" in err,
        "l'épuisement des 5 tentatives fait échouer tout le run, en nommant le message et le compte")
verifie(service_epuise.appels["q2"] == v.GMAIL_TENTATIVES_MAX,
        "exactement GMAIL_TENTATIVES_MAX tentatives sont faites, jamais plus (borné)")

# --- 18. une HttpError sans motif de quota n'est jamais retentée -----------------------
service_404 = _MessagesQuota(echecs=99, cible="q3", erreur=lambda: _http_error_quota(status=404, reason="notFound"))
leve = False
try:
    capture(v.fetch_scholar_emails, _service(service_404), 7)
except HttpError:
    leve = True
verifie(leve and service_404.appels["q3"] == 1,
        "une 404 (message supprimé, permission refusée) remonte au premier échec, sans être retentée")

print("tous les contrôles passent")
