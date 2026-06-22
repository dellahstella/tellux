#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tellux — R3 Moniteur liens morts / URL obsolètes.

Scanne les URL externes des fichiers trackés (app.html, pages, corpus .md, et
les url_canonique du registry) et les teste : 404, redirections, timeouts. Cas
de référence : IRSN -> ASNR. DÉTECTE et SIGNALE uniquement — ne corrige ni ne
remplace aucun lien (Cran C).

Anti-faux-positifs : User-Agent réaliste, HEAD puis repli GET, retries sur
timeout, et distinction lien VRAIMENT mort (404/410/DNS/refus) vs simplement
PROTÉGÉ (401/403/429 = anti-bot, pas mort). Seuls les morts font échouer.

Sortie : JSON sur stdout { total_urls, dead[], redirects[], blocked[] }. Exit 0
si aucun lien mort, 2 sinon.
"""
from __future__ import annotations

import concurrent.futures
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
TIMEOUT = 12
RETRIES = 2
MAX_URLS = 1200  # garde-fou ; on log si dépassé (pas de troncature silencieuse)

URL_RE = re.compile(r"https?://[^\s\"'<>)\]}\\`]+")
# Hôtes/patterns à ignorer : namespaces, exemples, schémas non navigables, ET
# les previews Cloudflare Pages éphémères (<hash>.tellux.pages.dev,
# claude-*.tellux.pages.dev) présentes dans les docs de feedback rnd — elles
# expirent par design, ce ne sont pas des liens « morts » à signaler. La prod
# `tellux.pages.dev` (sans sous-domaine) reste scannée.
SKIP_HOST_RE = re.compile(
    r"(^|//)(localhost|127\.0\.0\.1|example\.(com|org)|www\.w3\.org|schema\.org|"
    r"[a-z0-9-]+\.tellux\.pages\.dev|"
    r"\{|\$\{)", re.I)
TRAILING = ".,;:!?)]}>\"'`"


def _clean(u: str) -> str:
    u = u.strip()
    while u and u[-1] in TRAILING:
        u = u[:-1]
    return u


def _collect_urls() -> list[str]:
    seen: set[str] = set()
    # 1) fichiers texte trackés
    for pat in ("*.html", "*.md"):
        for p in REPO_ROOT.rglob(pat):
            sp = str(p)
            if ".git" in sp or "node_modules" in sp:
                continue
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for m in URL_RE.findall(txt):
                u = _clean(m)
                if u and not SKIP_HOST_RE.search(u):
                    seen.add(u)
    # 2) url_canonique du registry
    reg = REPO_ROOT / "scripts" / "citations_registry.json"
    if reg.exists():
        try:
            data = json.loads(reg.read_text(encoding="utf-8"))
            for entry in (data.values() if isinstance(data, dict) else []):
                u = _clean(str((entry or {}).get("url_canonique") or ""))
                if u.startswith("http") and not SKIP_HOST_RE.search(u):
                    seen.add(u)
        except Exception:
            pass
    return sorted(seen)


def _probe(url: str) -> dict:
    """Retourne {url, status, final_url, verdict}. verdict in alive/redirect/dead/blocked/other.

    DEAD (signalé, fait échouer) = 404/410 OU échec de connexion persistant (DNS,
    refus, timeout après retries). BLOCKED = 401/403/405/429 (anti-bot). OTHER =
    autre code HTTP obtenu (400, 5xx…) : rapporté mais NON imputé comme mort (ex.
    URL gabarit avec placeholder, 5xx transitoire).
    """
    last_http = None
    last_err = ""
    for method in ("HEAD", "GET"):
        for _attempt in range(RETRIES + 1):
            try:
                req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "*/*"})
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    final = resp.geturl()
                    code = resp.status
                    verdict = "redirect" if final.rstrip("/") != url.rstrip("/") else "alive"
                    return {"url": url, "status": code, "final_url": final, "verdict": verdict}
            except urllib.error.HTTPError as e:
                last_http = e.code
                if e.code in (404, 410):
                    return {"url": url, "status": e.code, "final_url": url, "verdict": "dead"}
                if e.code in (401, 403, 405, 429):
                    if method == "HEAD":
                        break  # repli GET
                    return {"url": url, "status": e.code, "final_url": url, "verdict": "blocked"}
                if method == "HEAD":
                    break  # repli GET pour les autres codes (400/5xx…)
            except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
                last_err = str(getattr(e, "reason", e))[:120]
            except Exception as e:
                last_err = str(e)[:120]
    if last_http is not None:
        # Un code HTTP a été obtenu mais ni 2xx/3xx, ni 404/410, ni anti-bot.
        return {"url": url, "status": last_http, "final_url": url, "verdict": "other", "error": f"HTTP {last_http}"}
    # Aucune réponse HTTP : échec de connexion persistant => mort.
    return {"url": url, "status": None, "final_url": url, "verdict": "dead", "error": last_err or "timeout/connexion"}


def main() -> int:
    urls = _collect_urls()
    capped = False
    if len(urls) > MAX_URLS:
        capped = True
        urls = urls[:MAX_URLS]

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        for r in ex.map(_probe, urls):
            results.append(r)

    dead = [r for r in results if r["verdict"] == "dead"]
    redirects = [r for r in results if r["verdict"] == "redirect"]
    blocked = [r for r in results if r["verdict"] == "blocked"]
    other = [r for r in results if r["verdict"] == "other"]
    report = {
        "total_urls": len(urls),
        "capped": capped,
        "cap": MAX_URLS if capped else None,
        "dead_count": len(dead),
        "redirect_count": len(redirects),
        "blocked_count": len(blocked),
        "other_count": len(other),
        "dead": dead,
        "redirects": redirects,
        "blocked": blocked,
        "other": other,
        "note": "blocked (401/403/429) = anti-bot probable ; other (400/5xx) = gabarit/transitoire — "
                "NON imputés comme morts. Détecté uniquement ; aucun lien corrigé/remplacé (Cran C).",
    }
    if capped:
        print(f"[warn] {MAX_URLS} URL max scannées (cap atteint) — couverture partielle.", file=sys.stderr)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not dead else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
