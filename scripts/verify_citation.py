#!/usr/bin/env python3
"""
verify_citation.py — Resolveur de citations primaires (anti-Frankenstein gate §10).

Prend un DOI ou une URL d'article scientifique et retourne un quadruplet verifie
(auteurs, annee, titre, journal/volume:pages, DOI canonique) via :
  1. Crossref REST     — https://api.crossref.org/works/{doi}
  2. PubMed E-utilities  — fallback pour journaux non-Crossref
  3. bioRxiv details API — fallback pour preprints biorxiv

Usage :
  python3 verify_citation.py 10.1007/BF01426859
  python3 verify_citation.py https://www.nature.com/articles/2011305a0
  python3 verify_citation.py 10.1007/BF01426859 --markdown
  python3 verify_citation.py 10.1007/BF01426859 --register   # ajoute au registry
  python3 verify_citation.py --check-registry 10.1007/BF01426859

Dependances : urllib (stdlib), json (stdlib), argparse (stdlib), re (stdlib).
Aucune dependance externe — pour minimiser les risques de drift en sandbox bash.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any

# Force UTF-8 sur stdout/stderr pour eviter UnicodeEncodeError sur Windows (cp1252)
# face aux noms de famille diacritiques courants en literature scientifique
# (e.g. nom croate "Karačić", grec "Spendier", suedois "Lindström").
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass

REGISTRY_PATH = Path(__file__).parent / "citations_registry.json"
USER_AGENT = "Tellux-CitationVerifier/0.1 (https://github.com/dellahstella/tellux ; mailto:contact@tellux.pages.dev)"
CROSSREF_URL = "https://api.crossref.org/works/{doi}"
PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
BIORXIV_DETAILS = "https://api.biorxiv.org/details/biorxiv/{doi}"

DOI_RE = re.compile(r"\b(10\.\d{4,9}/[^\s\"<>]+)\b")
PMC_RE = re.compile(r"PMC(\d+)", re.IGNORECASE)
BIORXIV_DOI_RE = re.compile(r"10\.1101/\d+")
SCIENCEDIRECT_PII_RE = re.compile(r"/pii/(S[A-Z0-9]+)", re.IGNORECASE)


def http_get(url: str, timeout: int = 15) -> bytes:
    """GET HTTP avec User-Agent identifiant Tellux (politesse Crossref)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def extract_doi(arg: str) -> str | None:
    """Extrait un DOI depuis une chaine brute ou une URL.

    Strategies :
      - chaine commence par '10.' -> DOI direct
      - URL doi.org -> extraction apres le dernier slash compose
      - URL ScienceDirect S0000000000XXXXX -> resoudre via Crossref query par PII
      - URL PMC -> resoudre via PubMed
      - URL bioRxiv -> extraction 10.1101/...
      - Autres URLs (Nature, Springer, Wiley, MDPI, Frontiers) -> regex DOI dans le path
    """
    s = arg.strip()
    if s.lower().startswith("10."):
        return s
    if "doi.org/" in s:
        return s.split("doi.org/", 1)[1].rstrip("/")
    m = DOI_RE.search(s)
    if m:
        return m.group(1)
    return None


def fetch_crossref(doi: str) -> dict[str, Any] | None:
    """Interroge Crossref REST pour un DOI."""
    url = CROSSREF_URL.format(doi=urllib.parse.quote(doi, safe="/"))
    try:
        raw = http_get(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    payload = json.loads(raw.decode("utf-8"))
    return payload.get("message")


def fetch_biorxiv(doi: str) -> dict[str, Any] | None:
    """Interroge bioRxiv details API pour un DOI 10.1101/..."""
    url = BIORXIV_DETAILS.format(doi=urllib.parse.quote(doi, safe="/"))
    try:
        raw = http_get(url)
    except urllib.error.HTTPError:
        return None
    payload = json.loads(raw.decode("utf-8"))
    collection = payload.get("collection") or []
    return collection[0] if collection else None


def fetch_pubmed_by_pmc(pmc_id: str) -> dict[str, Any] | None:
    """Resout un PMC ID en PMID puis interroge ESummary."""
    # 1) PMC -> PMID via ESearch
    qs = urllib.parse.urlencode({"db": "pubmed", "term": f"PMC{pmc_id}[pmc]", "retmode": "json"})
    try:
        raw = http_get(f"{PUBMED_ESEARCH}?{qs}")
    except urllib.error.HTTPError:
        return None
    payload = json.loads(raw.decode("utf-8"))
    ids = payload.get("esearchresult", {}).get("idlist") or []
    if not ids:
        return None
    pmid = ids[0]
    # 2) PMID -> details via ESummary
    qs = urllib.parse.urlencode({"db": "pubmed", "id": pmid, "retmode": "json"})
    try:
        raw = http_get(f"{PUBMED_ESUMMARY}?{qs}")
    except urllib.error.HTTPError:
        return None
    payload = json.loads(raw.decode("utf-8"))
    return payload.get("result", {}).get(pmid)


def crossref_to_quad(msg: dict[str, Any]) -> dict[str, Any]:
    """Normalise un message Crossref en quadruplet Tellux."""
    authors_raw = msg.get("author") or []
    authors = []
    for a in authors_raw:
        family = a.get("family") or ""
        given = a.get("given") or ""
        # Normalise la casse du nom de famille : "MURR" -> "Murr" (Crossref renvoie
        # parfois en MAJUSCULES selon le formatage source). On conserve les noms
        # composes a tirets ("Wigton-Jones") et particules ("van der", "de la").
        if family.isupper() and len(family) >= 2:
            family = "-".join(part.capitalize() for part in family.split("-"))
        initials = " ".join(p[0].upper() + "." for p in given.replace("-", " ").split() if p)
        authors.append(f"{family} {initials}".strip())
    issued = msg.get("issued", {}).get("date-parts") or [[None]]
    year = issued[0][0] if issued and issued[0] else None
    title_arr = msg.get("title") or [""]
    container = msg.get("container-title") or [""]
    return {
        "auteurs": authors,
        "annee": year,
        "titre": title_arr[0] if title_arr else "",
        "journal": container[0] if container else "",
        "volume": msg.get("volume") or "",
        "pages": msg.get("page") or "",
        "doi": msg.get("DOI") or "",
        "url_canonique": msg.get("URL") or (f"https://doi.org/{msg.get('DOI')}" if msg.get("DOI") else ""),
        "source_api": "Crossref REST",
    }


def biorxiv_to_quad(rec: dict[str, Any]) -> dict[str, Any]:
    """Normalise une entree bioRxiv en quadruplet."""
    authors_raw = rec.get("authors") or ""
    # bioRxiv renvoie "Lastname F.; Lastname G." -> split sur ; ou ,
    parts = [p.strip() for p in re.split(r"[;,]", authors_raw) if p.strip()]
    return {
        "auteurs": parts,
        "annee": int((rec.get("date") or "")[:4]) if rec.get("date") else None,
        "titre": rec.get("title") or "",
        "journal": "bioRxiv (preprint)",
        "volume": "",
        "pages": "",
        "doi": rec.get("doi") or "",
        "url_canonique": f"https://www.biorxiv.org/content/{rec.get('doi')}" if rec.get("doi") else "",
        "source_api": "bioRxiv details API",
    }


def pubmed_to_quad(rec: dict[str, Any]) -> dict[str, Any]:
    """Normalise une entree PubMed ESummary en quadruplet."""
    authors = [a.get("name") for a in (rec.get("authors") or []) if a.get("name")]
    pubdate = rec.get("pubdate") or ""
    year = None
    m = re.match(r"(\d{4})", pubdate)
    if m:
        year = int(m.group(1))
    return {
        "auteurs": authors,
        "annee": year,
        "titre": rec.get("title") or "",
        "journal": rec.get("fulljournalname") or rec.get("source") or "",
        "volume": rec.get("volume") or "",
        "pages": rec.get("pages") or "",
        "doi": next((aid.get("value") for aid in (rec.get("articleids") or []) if aid.get("idtype") == "doi"), ""),
        "url_canonique": f"https://pubmed.ncbi.nlm.nih.gov/{rec.get('uid')}/" if rec.get("uid") else "",
        "source_api": "PubMed E-utilities",
    }


def resolve(arg: str) -> dict[str, Any] | None:
    """Resout un argument (DOI ou URL) en quadruplet verifie."""
    doi = extract_doi(arg)
    if doi:
        # 1) Crossref direct
        msg = fetch_crossref(doi)
        if msg:
            return crossref_to_quad(msg)
        # 2) bioRxiv si DOI matche
        if BIORXIV_DOI_RE.fullmatch(doi):
            rec = fetch_biorxiv(doi)
            if rec:
                return biorxiv_to_quad(rec)
        # 3) Fallback PubMed si DOI non resolu
        # (PubMed ESearch par DOI)
        qs = urllib.parse.urlencode({"db": "pubmed", "term": f"{doi}[doi]", "retmode": "json"})
        try:
            raw = http_get(f"{PUBMED_ESEARCH}?{qs}")
            payload = json.loads(raw.decode("utf-8"))
            ids = payload.get("esearchresult", {}).get("idlist") or []
            if ids:
                qs2 = urllib.parse.urlencode({"db": "pubmed", "id": ids[0], "retmode": "json"})
                raw2 = http_get(f"{PUBMED_ESUMMARY}?{qs2}")
                payload2 = json.loads(raw2.decode("utf-8"))
                rec = payload2.get("result", {}).get(ids[0])
                if rec:
                    return pubmed_to_quad(rec)
        except urllib.error.HTTPError:
            pass
        return None
    # Pas de DOI extrait : tenter PMC dans l'URL
    m = PMC_RE.search(arg)
    if m:
        rec = fetch_pubmed_by_pmc(m.group(1))
        if rec:
            return pubmed_to_quad(rec)
    # ScienceDirect PII (Elsevier) : quatre strategies dans l'ordre.
    pii_match = SCIENCEDIRECT_PII_RE.search(arg)
    if pii_match:
        pii = pii_match.group(1)
        # 1) Semantic Scholar resout les PII en DOI (gratuit, anonyme, rate-limit ~100/5min)
        doi_from_s2 = fetch_doi_from_semantic_scholar_pii(pii)
        if doi_from_s2:
            msg = fetch_crossref(doi_from_s2)
            if msg:
                return crossref_to_quad(msg)
        # 2) OpenAlex search par PII (gratuit, anonyme, rate-limit genereux ~100k/jour)
        doi_from_openalex = fetch_doi_from_openalex_pii(pii)
        if doi_from_openalex:
            msg = fetch_crossref(doi_from_openalex)
            if msg:
                return crossref_to_quad(msg)
        # 3) HTML scrape (ScienceDirect retourne souvent 403 pour les bots,
        #    mais utile pour les editeurs plus permissifs sous le meme pattern PII)
        doi_from_html = fetch_doi_from_html(arg)
        if doi_from_html:
            msg = fetch_crossref(doi_from_html)
            if msg:
                return crossref_to_quad(msg)
    elif arg.startswith("http"):
        # URL d'editeur non-Elsevier : tenter scrape meta-tags directement
        doi_from_html = fetch_doi_from_html(arg)
        if doi_from_html:
            msg = fetch_crossref(doi_from_html)
            if msg:
                return crossref_to_quad(msg)
    return None


def fetch_doi_from_openalex_pii(pii: str) -> str | None:
    """Resout un PII Elsevier en DOI via OpenAlex.

    Note : OpenAlex n'indexe pas directement les PII Elsevier comme cle de
    recherche. La strategie qui fonctionne empiriquement est de chercher par
    titre — donc cette resolution PII-direct echoue silencieusement la plupart
    du temps. Conservee comme stub pour signaler la limite et pour invocation
    explicite avec un mot-cle de titre via --search (hors scope CLI actuel).

    Si vous connaissez le titre de l'article, faire la recherche manuellement :
        curl 'https://api.openalex.org/works?search=<titre>&per-page=3'
    et passer le DOI trouve a verify_citation.py.
    """
    qs = urllib.parse.urlencode({"search": pii, "per-page": "3"})
    try:
        raw = http_get(f"https://api.openalex.org/works?{qs}", timeout=15)
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return None
    for w in data.get("results", []) or []:
        doi_url = w.get("doi") or ""
        if "doi.org/" in doi_url:
            return doi_url.split("doi.org/", 1)[1]
    return None


def fetch_doi_from_semantic_scholar_pii(pii: str) -> str | None:
    """Resout un PII Elsevier en DOI via Semantic Scholar Graph API.

    Endpoint anonyme : ~100 req/5min. Retourne None en cas de 429 (rate-limit)
    pour ne pas bloquer le script — on documente la limite plutot que de retry.
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/PII:{pii}?fields=externalIds"
    try:
        raw = http_get(url, timeout=15)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"[INFO] Semantic Scholar rate-limit (429) pour PII:{pii} — fallback HTML", file=sys.stderr)
        return None
    except urllib.error.URLError:
        return None
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        return None
    ext = data.get("externalIds") or {}
    return ext.get("DOI") or None


META_DOI_RE = re.compile(
    r'<meta[^>]+(?:name|property)=["\'](?:citation_doi|prism\.doi|dc\.identifier(?:\.doi)?|DC\.Identifier)["\']'
    r'[^>]*content=["\'](?:doi:)?([^"\'>]+)["\']',
    re.IGNORECASE,
)


def fetch_doi_from_html(url: str) -> str | None:
    """Recupere une page HTML d'editeur et extrait le DOI des meta tags."""
    try:
        raw = http_get(url, timeout=20)
    except urllib.error.HTTPError:
        return None
    except urllib.error.URLError:
        return None
    try:
        text = raw.decode("utf-8", errors="replace")
    except Exception:
        return None
    m = META_DOI_RE.search(text)
    if m:
        candidate = m.group(1).strip()
        # Nettoyer un prefixe "doi:" eventuellement non capture
        if candidate.lower().startswith("doi:"):
            candidate = candidate[4:].strip()
        if DOI_RE.fullmatch(candidate):
            return candidate
    # Fallback : chercher un DOI brut dans le HTML
    m2 = DOI_RE.search(text)
    if m2:
        return m2.group(1).rstrip(".\"'<>)")
    return None


def to_markdown(q: dict[str, Any]) -> str:
    """Formatte un quadruplet en ligne markdown Tellux."""
    authors = q.get("auteurs") or []
    if len(authors) > 3:
        authors_str = ", ".join(authors[:3]) + " et al."
    else:
        authors_str = ", ".join(authors) if authors else "—"
    year = q.get("annee") or "—"
    title = q.get("titre") or "—"
    journal = q.get("journal") or "—"
    vol = q.get("volume") or ""
    pages = q.get("pages") or ""
    vol_pages = f"{vol}:{pages}" if vol and pages else (vol or pages or "")
    doi = q.get("doi") or ""
    url = q.get("url_canonique") or ""
    if doi:
        ref_tail = f"[doi:{doi}]({url})" if url else f"doi:{doi}"
    elif url:
        ref_tail = f"[lien]({url})"
    else:
        ref_tail = ""
    pieces = [f"{authors_str} ({year}), {title}", f"**{journal}**"]
    if vol_pages:
        pieces[-1] += f" {vol_pages}"
    if ref_tail:
        pieces.append(ref_tail)
    return ", ".join(pieces)


def load_registry() -> dict[str, Any]:
    if not REGISTRY_PATH.exists():
        return {}
    try:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def save_registry(reg: dict[str, Any]) -> None:
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def register_quad(q: dict[str, Any], used_in: list[str] | None = None) -> None:
    reg = load_registry()
    doi = q.get("doi") or ""
    if not doi:
        return
    entry = {
        "auteurs": q.get("auteurs"),
        "annee": q.get("annee"),
        "titre": q.get("titre"),
        "journal": q.get("journal"),
        "volume": q.get("volume"),
        "pages": q.get("pages"),
        "url_canonique": q.get("url_canonique"),
        "verified_date": date.today().isoformat(),
        "verified_by": q.get("source_api"),
    }
    if used_in:
        prev = (reg.get(doi) or {}).get("used_in") or []
        entry["used_in"] = sorted(set(prev + used_in))
    elif doi in reg and reg[doi].get("used_in"):
        entry["used_in"] = reg[doi]["used_in"]
    reg[doi] = entry
    save_registry(reg)


def check_registry(doi: str) -> dict[str, Any] | None:
    return load_registry().get(doi)


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolveur de citations primaires Tellux (anti-Frankenstein).")
    parser.add_argument("arg", nargs="?", help="DOI ou URL de l'article a verifier")
    parser.add_argument("--markdown", action="store_true", help="Sortie au format markdown Tellux")
    parser.add_argument("--register", action="store_true", help="Ajouter le quadruplet au registry")
    parser.add_argument("--used-in", action="append", default=[], help="Chemin du livrable utilisateur (multi)")
    parser.add_argument("--check-registry", metavar="DOI", help="Verifier si un DOI est deja dans le registry")
    args = parser.parse_args()

    if args.check_registry:
        entry = check_registry(args.check_registry)
        if entry:
            print(json.dumps(entry, indent=2, ensure_ascii=False))
            return 0
        print(f"[NOT_FOUND] {args.check_registry} absent du registry.", file=sys.stderr)
        return 1

    if not args.arg:
        parser.print_help()
        return 1

    quad = resolve(args.arg)
    if not quad:
        print(f"[UNRESOLVED] Aucune source API n'a resolu : {args.arg}", file=sys.stderr)
        return 2

    if args.register:
        register_quad(quad, used_in=args.used_in or None)

    if args.markdown:
        print(to_markdown(quad))
    else:
        print(json.dumps(quad, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
