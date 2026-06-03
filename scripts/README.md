# `verify_citation.py` — Résolveur de citations primaires (anti-Frankenstein)

> Outil CLI léger pour résoudre un DOI ou une URL d'article scientifique en quadruplet vérifié (auteurs, année, titre, journal/volume:pages) via Crossref REST + fallbacks PubMed E-utilities et bioRxiv API.
> Référentiel : `PROTOCOLE_AUTO_ITERATION.md` §10 (gate citations).

---

## Pourquoi

Quatre Frankensteins documentées en quatre boucles d'auto-itération recherche (compteur projet 2026-06-03) :

| Chantier | Mécanisme |
|---|---|
| Électroculture it. 001 | Auteur inventé sur papier réel (Bilalis → Spendier) |
| Électroculture it. 003 | Auteurs réels d'un autre papier collés sur PMC ID (Mildaziene & Sera → Leti) |
| Électroculture it. 004 | Auteur + journal vraisemblables + URL d'un autre papier (Calabrese) |
| EM méta-synthèse it. 001 | Auteur d'une réf. biblio + DOI page lue (Murr → Pohl & Todd) |
| EM méta-synthèse it. 002 | Frankenstein inversée évaluateur : recommandation Asprey → Aspray sur typo bibliographie secondaire |

**Cause racine** : générateur et évaluateur composent les citations par lecture de sources secondaires (audits, niches W, bibliographies de papiers ouverts). Le gate §10 attrape mais ne prévient pas. Cet outil **prévient** : il impose la résolution primaire avant écriture.

---

## Installation

Aucune dépendance externe : `urllib`, `json`, `argparse`, `re` de la stdlib Python 3.10+.

```bash
# Vérifier la version (3.10 minimum)
python3 --version

# Le script est exécutable directement
python3 scripts/verify_citation.py 10.1007/BF01426859
```

Pour automatiser au PATH :

```bash
chmod +x scripts/verify_citation.py
# puis depuis n'importe où :
./scripts/verify_citation.py 10.1007/BF01426859
```

---

## Usage

### Résolution simple (sortie JSON)

```bash
python3 scripts/verify_citation.py 10.1007/BF01426859
```

```json
{
  "auteurs": ["Murr L. E."],
  "annee": 1966,
  "titre": "The biophysics of plant growth in a reversed electrostatic field",
  "journal": "International Journal of Biometeorology",
  "volume": "10",
  "pages": "135-146",
  "doi": "10.1007/BF01426859",
  "url_canonique": "https://doi.org/10.1007/BF01426859",
  "source_api": "Crossref REST"
}
```

### Sortie markdown Tellux (à copier-coller dans un livrable)

```bash
python3 scripts/verify_citation.py 10.1007/BF01426859 --markdown
```

```
Murr L. E. (1966), The biophysics of plant growth in a reversed electrostatic field, **International Journal of Biometeorology** 10:135-146, [doi:10.1007/BF01426859](https://doi.org/10.1007/BF01426859)
```

### Ajouter au registre

```bash
python3 scripts/verify_citation.py 10.1007/BF01426859 \
  --register \
  --used-in axe_em/recherche/em-meta-synthese-2026-06-03/SYNTHESE.md
```

Le registre `scripts/citations_registry.json` consigne pour chaque DOI : quadruplet + date + API source + livrables où la citation a été utilisée.

### Vérifier qu'un DOI est déjà au registre

```bash
python3 scripts/verify_citation.py --check-registry 10.1007/BF01426859
```

Exit code `0` si présent, `1` si absent.

### À partir d'une URL (Nature, Springer, ScienceDirect, PMC, Wiley, MDPI, Frontiers, PNAS, bioRxiv)

```bash
python3 scripts/verify_citation.py https://www.sciencedirect.com/science/article/abs/pii/S0921800925003180
python3 scripts/verify_citation.py https://www.nature.com/articles/2011305a0
python3 scripts/verify_citation.py https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9415020/
```

---

## Sources de résolution (par ordre de tentative)

1. **Crossref REST** — `https://api.crossref.org/works/{doi}`. Couverture la plus large pour les journaux Crossref-indexés. Pas de clé API requise pour usage modeste (rate limit Crossref public ≈ 50 req/s).
2. **bioRxiv details API** — pour DOI `10.1101/...`.
3. **PubMed E-utilities** — fallback `esearch` + `esummary` pour les journaux non-Crossref ou les PMC IDs.
4. **Semantic Scholar Graph API** — fallback pour les **PII ScienceDirect (Elsevier)** : `https://api.semanticscholar.org/graph/v1/paper/PII:{pii}` résout PII → DOI, puis on rebascule sur Crossref pour le quadruplet canonique. Rate-limit anonyme ~100 req/5 min.
5. **HTML meta-tags scrape** — dernier recours pour les URLs éditeur qui exposent `citation_doi` / `prism.doi` / `dc.identifier` dans le `<head>`. ScienceDirect bloque les bots non-authentifiés (403) — c'est pour ça que Semantic Scholar passe en priorité sur Elsevier.

Aucun secret, aucune clé API. Les requêtes sont identifiées par un `User-Agent` Tellux (politesse Crossref).

---

## Workflow Cowork (générateur)

1. Rédiger le livrable avec DOI / URL bruts (placeholder `[CITATION_X]` ou DOI direct).
2. Avant clôture, lancer `verify_citation.py --markdown --register` sur chaque DOI/URL.
3. Coller le markdown retourné à la place de la citation manuelle dans le livrable.
4. Au passage, le registre est mis à jour automatiquement.

## Workflow évaluateur (gate §10)

1. Pour chaque citation du livrable, extraire DOI/URL.
2. Lancer `verify_citation.py` et comparer la sortie à la citation telle qu'écrite.
3. Toute divergence (auteur, année, titre, journal, volume:pages) = Frankenstein potentielle, gate **FAIL**.
4. Le `GATE_CITATIONS.md` du chantier consigne le verdict par citation.

---

## Limites connues

- **Pre-1968 / archives institutionnelles** : Crossref peut ne pas avoir l'entrée. Tenter PubMed ou Google Scholar manuellement.
- **Pages préfixées en lettres** (ex. `e0123456` PLoS, `R201` Cancer Res) : sortie OK, mais le formatage volume:pages peut différer du style classique.
- **Auteurs anonymes ou collectifs** : Crossref renvoie souvent `author: []` — le quadruplet sortira sans auteur, à compléter à la main.
- **PII ScienceDirect (Elsevier)** : ScienceDirect bloque les bots non-authentifiés (403). Le script bascule sur Semantic Scholar pour résoudre PII → DOI, mais Semantic Scholar a un rate-limit anonyme (~100 req/5 min). En cas de 429, fournir le DOI directement plutôt que l'URL PII.
- **Pas de validation sémantique** : l'outil vérifie que la citation existe ; il ne vérifie pas que **le contenu du papier soutient l'affirmation citée**. Cette validation reste à la charge du générateur et de l'évaluateur (lecture des passages cités).

---

## Tests

```bash
bash scripts/test_verify_citation.sh
```

6 tests primaires (Murr 1966, Pohl & Todd 1981, Murr 1964 Nature, Beerling 2024, Sidaway & Asprey 1968 orthographe correcte, Wigton-Jones 2025 résolu depuis URL). Tous doivent retourner PASS.

---

## Évolutions possibles (hors scope itération 1)

- Intégration CI (pré-commit hook qui exige `verify_citation.py --check-registry` pour chaque DOI du diff).
- Wrapper léger autour de `habanero` ou `crossref-commons` pour les cas Crossref complexes (multi-affiliation, ORCID).
- Export BibTeX / CSL JSON à partir du registre.
- Support DataCite (datasets), arXiv, OSF.

À arbitrer par Soleil et Cowork en fonction des besoins concrets des prochaines boucles recherche.
