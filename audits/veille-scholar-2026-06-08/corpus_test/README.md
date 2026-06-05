# Corpus de test Phase 1 — Veille Scholar

> Fixture pour la boucle d'itération Phase 1 (générateur ≠ évaluateur, §2 du protocole).
> Source : snapshot de mails Scholar Alerts réels reçus sur `tellux.veille@gmail.com` entre 2026-05-19 et 2026-06-04.
> Tous les payloads viennent directement de l'API Gmail via MCP — aucun credentials ni PII, juste le contenu HTML des alertes Scholar (publiquement repérable depuis tout abonné).

## Format

Chaque fichier `email_NNN.json` représente UN thread Gmail :

```json
{
  "id": "19e90b4da2e738e3",
  "subject": "1. (\"radiofrequency exposure\" OR ...) – de nouveaux résultats",
  "date": "2026-06-04T03:37:11Z",
  "sender": "scholaralerts-noreply@google.com",
  "html_body": "<html>...</html>",
  "alert_number": 1,
  "expected_refs": [
    {
      "title": "Workers' Exposure Due to Private 5G Networks",
      "first_author": "B Valič",
      "journal": "Telecom",
      "year": 2026,
      "url": "https://www.mdpi.com/2673-4001/7/3/63",
      "doi": null,
      "verifiable": "via URL → MDPI page parse"
    }
  ],
  "_meta": "Annotations manuelles 2026-06-04 — sert d'oracle pour la dédup et verify_citation."
}
```

## Inventaire (au 2026-06-04)

| # | Fichier | Origine alerte | Titre | Auteur principal | DOI / URL | Test |
|--:|---|:--:|---|---|---|---|
| 001 | `email_001.json` | #1 RF-EMF | Workers' Exposure Due to Private 5G Networks | B Valič | mdpi.com/2673-4001/7/3/63 | parse HTML + URL → DOI |
| 002 | `email_002.json` | #4 ELF | Cardiac Rhythms Shape Brain Oscillations | KS Sargent | escholarship.org/.../qt3rp2j7s0.pdf | parse HTML, no DOI direct (failsafe) |
| 003 | `email_003.json` | #1 RF-EMF | Cellular and Wireless Radiation, Public Health... | P Ben Ishai | DOI explicite `10.3389/fpubh.2026.1856852` | verify_citation Crossref PASS |
| 004 | `email_004.json` | #3 Radon | AI-Driven Image Analysis for Nanofiber Characterization | S Tort | DOI explicite `10.1021/acsomega.5c12433` | verify_citation Crossref PASS |
| 005 | `email_005_DUPLICATE.json` | #2 multi-EMF | (DOUBLON artificiel de email_001) Workers' Exposure... | B Valič | (idem) | dédup intra-run doit l'écarter |
| 006 | `email_006_NO_DOI.json` | #6 gamma | (DOUBLON artificiel de email_002, alert différente) | KS Sargent | (idem) | dédup + failsafe DOI absent |

→ **Total : 6 fichiers, 2 doublons artificiels (#005 = doublon de #001, #006 = doublon de #002).**
→ **Attendu après dédup intra-run : 4 références uniques.**
→ **Attendu verify_citation : 2 références PASS (#003, #004), 4 références NO_DOI (parse URL → tentative scrape).**

## Garde-fous

- Aucune donnée privée ou personnelle dans les fichiers (les Scholar Alerts ne contiennent que des titres/auteurs publics).
- `_meta` annotations sont des annotations Code (pas du contenu Gmail).
- Les doublons #005 et #006 sont des copies du #001/#002 avec `alert_number` modifié + `id` modifié — pas de vrais mails Gmail.

## Usage

Une fois Phase 1 implémentée, lancer :

```bash
# Mode test avec fixture (env var CORPUS_FIXTURE)
CORPUS_FIXTURE=audits/veille-scholar-2026-06-08/corpus_test \
  python3 .github/scripts/veille_scholar.py --dry-run-local
```

Le script doit alors :
1. Lire les 6 JSONs au lieu de l'API Gmail
2. Parser chaque html_body pour extraire les références
3. Dédupliquer intra-run → 4 références uniques attendues
4. Appeler verify_citation sur chaque ref avec DOI/URL
5. Logger `[dedup] 6 → 4` et `[verify] 4 DOI/URL, 2 verified, 2 no_doi_extracted_or_failed`
6. Produire une synthèse markdown (mode dry-run, pas de commit)

L'évaluateur lance ce harness en session fraîche et score contre la rubrique du `contrat.md` voisin.
