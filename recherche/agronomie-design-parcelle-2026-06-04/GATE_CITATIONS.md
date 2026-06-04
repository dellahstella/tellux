# GATE_CITATIONS.md — Chantier 1 agronomie (design de parcelle)

> Session **ÉVALUATEUR** dédiée gate §10 (binaire). Code constate, ne corrige pas.
> Date : 2026-06-04 (post-clôture méthodologique 7.80/10).
> Outils : `scripts/verify_citation.py` (Crossref + fallbacks PubMed/bioRxiv/Semantic Scholar/HTML scrape) + requêtes Crossref par titre via urllib.
> Cible : `recherche/agronomie-design-parcelle-2026-06-04/SYNTHESE.md` (NON modifié).

---

## 0. Verdict global

```
RÉSOLUBLES TOTALES  : 12 (8 DOIs tableau 4.A + 4 PIIs tableau 4.B)
PASS                : 11
FAIL                : 1 (R-DI-rev — citation détournée : paper maïs cité pour soutenir affirmation sur olivier/grenadier/pêcher)
N/A (cadrage §6.2)  : 8 (R-till, R-rwh, R-clim, R-pedo, R-irr, R-cu, R-olive, R-agrofor)

VERDICT BINAIRE     : ★ GATE GLOBAL FAIL ★
```

Règle appliquée (brief §1, §6) : « une seule fail résoluble = gate global FAIL ». La fail R-DI-rev repart au générateur (Cowork) ; aucun patch silencieux côté évaluateur.

**Action générateur** : reformuler la phrase §3.1 (séparer cadrage méthodologique méditerranéen vs preuve par culture) ou retirer R-DI-rev. Voir §4 ci-dessous pour le motif détaillé.

---

## 1. Tableau exhaustif — verdict par référence

### 1.A — DOIs directs (tableau 4.A du brief — 8 entrées)

| ID | DOI canonique | Auteur (Crossref) | Année Crossref | Année SYNTHESE | Titre Crossref vs SYNTHESE | Soutien affirmation §3/§5 | Verdict |
|---|---|---|:--:|:--:|---|:--:|:--:|
| R-mulch-vine | `10.3390/agronomy11040787` | Warren Raffa D. et al. | 2021 | 2021 | **MATCH exact** | §3.2 vignoble Med, mulch couverture → propriétés sol court terme | **PASS** |
| R-agrofor-wheat | `10.3390/agronomy12020527` | Panozzo A. et al. | 2022 | 2022 | **MATCH exact** | §3.3 verger-allée olivier × blé dur, microclimat + édaphique | **PASS** |
| R-mulch-olive | `10.3390/plants13060900` | Hrameche O. et al. | 2024 | 2024 | **MATCH exact** | §3.2 oléiculture, mesures agroécologiques → MO + humidité | **PASS** |
| R-mulch-rev | `10.3389/fagro.2024.1361697` | Demo A. H., Asefa Bogale G. | 2024 | 2024 | **MATCH exact** | §3.2 revue dryland, paillage → rendement + humidité | **PASS** |
| R-DI-olive | `10.3389/fenvs.2023.1100552` | Ibba K. et al. | 2023 | 2023 | **MATCH (titre Crossref étendu** : « Assessing the impact of deficit irrigation strategies… implications for operational water management ». SYNTHESE raccourcit) | §3.1 RDI sur olivier Menara — Méditerranée aride | **PASS** |
| R-notill-legume | `10.1139/cjss-2023-0106` | Farina R. et al. | 2024 | 2024 | **MATCH exact** | §3.4 no-till + couvert légumineuse → qualité sol Med pluvial | **PASS** |
| R-escape | `10.3389/fpls.2017.01950` | Shavrukov Y. et al. | 2017 | 2017 | **MATCH exact** | §3.5 esquive de sécheresse / early flowering wheat | **PASS** |
| R-DI-rev | `10.3390/agronomy13010117` | Soares D., Paço T. A., Rolim J. | **2022** ⚠️ | 2023 ⚠️ | **MATCH titre** : « …—A Review of the Methodological Approaches Focusing on Maize Crop » (SYNTHESE met `(maïs)` en parenthèses → connaissance assumée du focus maïs) | §3.1 cité avec R-DI-olive pour soutenir « Démontrée sur **olivier, grenadier, pêcher** en contexte méditerranéen/aride » — **paper est une revue maïs**, ne soutient pas la liste des cultures | **★ FAIL ★** (motif §4) |

### 1.B — PIIs Elsevier (tableau 4.B du brief — 4 entrées)

> Méthodologie de résolution : `verify_citation.py <PII_URL>` a échoué (Semantic Scholar 429 rate-limit + ScienceDirect 403 anti-bot). Fallback **résolu via Crossref title query** (`api.crossref.org/works?query.title=<titre attendu>`) puis `verify_citation.py <DOI_canonique>` pour validation finale.

> **Incident méthodologique signalé** : sur R-agrofor-olive, le premier `verify_citation.py` (PII URL) a renvoyé via fallback HTML scrape un DOI complètement différent (`10.21203/rs.3.rs-3953133/v1` — preprint Research Square sur DayCent), qui est **un faux positif** du scrape HTML lorsque Semantic Scholar est rate-limité. Cas à durcir dans `verify_citation.py` (hors scope ce gate). Pour ce gate, le DOI canonique a été retrouvé via Crossref title query (méthode plus fiable pour PIIs).

| ID | DOI canonique résolu | Auteur (Crossref) | Année Crossref | Année SYNTHESE | Titre Crossref vs SYNTHESE | Soutien affirmation §3/§5 | Verdict |
|---|---|---|:--:|:--:|---|:--:|:--:|
| R-agrofor-olive | `10.1016/j.agee.2020.107234` | Temani F. et al. | 2021 | 2021 | **MATCH exact** — *Olive agroforestry can improve land productivity even under low water availability in the South Mediterranean* | §3.3 agroforesterie oléicole, LER > 1 sous faible eau, Sud Méditerranée | **PASS** |
| R-agrofor-soc | `10.1016/j.agee.2023.108826` | Aguilera-Huertas J. et al. | **2024** ⚠️ | 2023 ⚠️ | **MATCH titre exact** (decalage online 2023 / print 2024 typique AEE) | §3.3 intercalaire oliveraie pluviale → qualité sol + stockage carbone | **PASS** (note année §3) |
| R-fallow | `10.1016/j.agwat.2022.107835` | Wuest S. B., Schillinger W. F. | 2022 | 2022 | **MATCH exact** | §3.4 calage temporel travail du sol → stockage eau long fallow Med | **PASS** |
| R-rwh-hi | `10.1016/j.geoderma.2023.116623` | Rojano-Cruz R. et al. | 2023 | 2023 | **MATCH titre exact** — Impacts of a hydroinfiltrator rainwater harvesting system, olive groves semi-arid Mediterranean | §3.1 cité **comme cas `NON VALIDÉ`** (gains non répliqués) — usage critique conforme à la position du papier (essai isolé) | **PASS** |

### 1.C — Sources de cadrage §6.2 (tableau 4.C du brief — 8 entrées)

> Hors gate binaire — pas de référence primaire identifiée à résoudre. Marquées **N/A** comme prévu au brief §4.C. Signalées comme **bloquant export distinct** : à fixer en chantier pré-FEDER (cf. SYNTHESE §7.3 tâche 1-2).

| ID | Nature | Statut | Motif N/A |
|---|---|:--:|---|
| R-till | Reduced tillage + couverts → SOC sequestration Med drylands | **N/A** | « à fixer » dans SYNTHESE §6.1 — pas de DOI/PII fixé |
| R-rwh | Microcatchment / in-situ rainwater harvesting olive Med | **N/A** | « à fixer » dans SYNTHESE §6.1 — pas de DOI/PII fixé |
| R-clim | Classification Köppen Csa, régimes pluvio/ETP/aridité Med | **N/A** | source de cadrage §6.2 — référentiel primaire à identifier (ex. Köppen-Geiger updated, FAO-56) |
| R-pedo | Gammes pédologiques méditerranéennes | **N/A** | source de cadrage §6.2 — manuel sols Med / FAO à fixer |
| R-irr | Salinisation eaux/sols littoraux méditerranéens | **N/A** | source de cadrage §6.2 — référence primaire non identifiée |
| R-cu | Accumulation Cu sols viticoles/arboricoles méditerranéens | **N/A** | source de cadrage §6.2 — référence primaire non identifiée |
| R-olive | Agronomie oléicole méditerranéenne (général) | **N/A** | source de cadrage §6.2 — référence primaire non identifiée |
| R-agrofor | Microclimat de versant adret/ubac | **N/A** | source de cadrage §6.2 — référence primaire non identifiée |

---

## 2. Comptage final

| Catégorie | Compte |
|---|---:|
| Total références dans SYNTHESE §6 | 20 |
| Résolubles (DOI direct + PII) | **12** |
| Sources de cadrage §6.2 (hors gate binaire) | **8** |
| **PASS** (résolu + soutient affirmation) | **11** |
| **FAIL** | **1** |
| **N/A** (rien à résoudre) | **8** |

---

## 3. Liste nominale des FAIL

### 3.1 — `R-DI-rev` (Soares et al. 2022, *Agronomy* 13(1):117)

**DOI** : `10.3390/agronomy13010117` (résolu OK, paper existe, métadonnées cohérentes).

**Motif FAIL** : **citation détournée** (per brief §5 étape 3 et §6 « référence réelle mais détournée = FAIL »).

Le paper est une **revue méthodologique focalisée sur le maïs** :
- Titre Crossref complet : *« Assessing Climate Change Impacts on Irrigation Water Requirements under Mediterranean Conditions—A Review of the Methodological Approaches Focusing on Maize Crop »*
- SYNTHESE §6.1 met explicitement `(maïs)` en parenthèses → la nature maïs du papier est connue du générateur.

Citation problématique en SYNTHESE §3.1 :
> *« L'irrigation déficitaire régulée (RDI/SDI) consiste à apporter moins d'eau que l'optimum, en ciblant les phases peu sensibles, pour maximiser l'efficience d'usage de l'eau au prix d'une baisse de rendement contrôlée. Démontrée sur olivier, grenadier, pêcher en contexte méditerranéen/aride [R-DI-olive], [R-DI-rev]. »*

La paire `[R-DI-olive], [R-DI-rev]` est posée APRÈS l'affirmation « Démontrée sur olivier, grenadier, pêcher ». Lecture stricte évaluateur :
- `R-DI-olive` (Ibba et al. 2023, Menara olive cultivar) → supporte « olivier ». PASS.
- `R-DI-rev` (Soares et al. 2022, revue maïs) → **ne supporte PAS** « olivier, grenadier, pêcher ». Le paper traite des méthodologies d'irrigation pour le maïs en conditions méditerranéennes — pas des cultures pérennes mentionnées.

Pas une Frankenstein **stricte** (DOI/auteur/titre tous corrects), mais une **overgeneralization** au sens du brief : le paper réel ne soutient pas l'usage qui en est fait. La règle binaire §10 ne distingue pas Frankenstein vs overgeneralization — toute citation qui ne soutient pas l'affirmation = FAIL.

**Bonus signal** : discrepance d'année Crossref 2022 vs SYNTHESE 2023 (online publication 2022 / volume 13(1) print 2023, typique MDPI Agronomy). Non bloquante isolément mais cumulée au motif principal.

**Options pour le générateur** (Cowork — hors scope évaluateur) :
- **Option A** : reformuler §3.1 pour distinguer explicitement le cadrage méthodologique méditerranéen (où R-DI-rev a sa place) vs la preuve par culture spécifique (où seul R-DI-olive est compétent). Exemple : *« …Démontrée sur olivier en contexte méditerranéen/aride [R-DI-olive] ; le cadre méthodologique général des besoins d'irrigation sous Méditerranée a fait l'objet de revues comparatives [R-DI-rev]. »*
- **Option B** : retirer R-DI-rev de §3.1 et le placer en §6.2 (cadrage) ou en bibliographie générale §3.1.
- **Option C** : ajouter explicitement une mention « (revue méthodologique sur maïs, transposition partielle) » à côté de la citation §3.1.
- **Option D** : trouver une référence primaire couvrant grenadier ou pêcher en RDI méditerranéen pour remplacer R-DI-rev sur ce point précis.

L'évaluateur ne tranche pas. Le brief §6 stipule explicitement : « toute fail repart au générateur, pas de patch silencieux ».

---

## 4. Notes additionnelles (non bloquantes)

### 4.1 — Discrepances d'année Crossref vs SYNTHESE (signal d'usage)

| ID | Crossref | SYNTHESE | Interprétation |
|---|:--:|:--:|---|
| R-agrofor-soc | 2024 | 2023 | DOI préfixe `agee.2023.*` = online 2023, print 2024 (volume 361). **Pas Frankenstein** — même papier. À harmoniser éventuellement dans une future révision SYNTHESE (privilégier l'année print pour citation académique). |
| R-DI-rev | 2022 | 2023 | DOI préfixe `agronomy.13010117` = online 2022, volume 13(1) print 2023. **Pas Frankenstein** isolément. Cumulé au motif §3.1 ci-dessus → FAIL. |

Ces discrepances reflètent les délais entre publication online et publication papier dans un volume — classique en édition académique. **Non comptées comme fail** isolément. Signal d'amélioration : la SYNTHESE pourrait préciser la version (« online 2022 / print 2023 ») pour les citations futures.

### 4.2 — Faux positif du fallback HTML scrape de `verify_citation.py`

Sur la résolution initiale du PII `S0167880920304205` (R-agrofor-olive), `verify_citation.py` a renvoyé un DOI non pertinent (preprint Research Square DayCent au lieu du papier AEE attendu). Cas observé :

```
[INFO] Semantic Scholar rate-limit (429) pour PII:S0167880920304205 — fallback HTML
{
  "auteurs": ["Laub M.", ...],
  "titre": "A novel approach to use the DayCent model for simulating agroforestry systems with multiple components",
  "doi": "10.21203/rs.3.rs-3953133/v1",
  ...
}
```

Le scrape HTML a probablement chopé un DOI cité dans la page ScienceDirect (références bibliographiques mentionnant DayCent) plutôt que le DOI canonique du paper lui-même. Comportement à durcir dans `verify_citation.py` :
- Quand Semantic Scholar 429 → ne PAS fallback automatiquement sur HTML scrape (qui est très bruité sur ScienceDirect)
- Préférer un retour `unresolved + raison: semantic_scholar_429` qui force l'utilisateur à retenter plus tard ou utiliser Crossref title query

**Hors scope ce gate** — à signaler au backlog `verify_citation.py` (chantier outil).

### 4.3 — Stratégie de contournement pour les PIIs Elsevier (méthodologique pour évaluateurs futurs)

ScienceDirect bloque les bots anonymes (403 sur toutes les pages PII). Semantic Scholar a un rate-limit anonyme (~100 req/5 min). Le fallback HTML scrape de `verify_citation.py` est bruité.

**Stratégie qui a fonctionné** pour ce gate : query Crossref par titre (`api.crossref.org/works?query.title=<titre>&rows=2`) — l'API est ouverte, fiable, et matche par similarity sur le titre. Une fois le DOI canonique trouvé, `verify_citation.py <DOI>` finalise via Crossref direct.

Recommandation pour `verify_citation.py` v2 : ajouter une méthode `resolve_by_title(title)` qui interroge Crossref title query, retourne top-2 résultats avec similarity score, et permet à l'utilisateur de confirmer le match avant `--register`.

---

## 5. Registre `citations_registry.json` — non touché

Per brief §3 : « **Écriture autorisée uniquement** sur `GATE_CITATIONS.md` (création) et, sur option `--register`, sur `scripts/citations_registry.json` ».

Étant donné le **verdict global FAIL**, je **n'ajoute aucune référence** au registre — le gate n'est pas passé, donc aucune citation de ce chantier n'est encore « confirmée exportable » per protocole §10. Une fois le générateur corrige R-DI-rev et l'évaluateur repasse, alors les 11 PASS pourront être registrés en bloc avec `--register --used-in recherche/agronomie-design-parcelle-2026-06-04/SYNTHESE.md`.

---

## 6. Garde-fous appliqués pendant ce gate

Conformément au brief §3 et §6 :
- ✓ `SYNTHESE.md` **non modifié** (lecture seule confirmée).
- ✓ Aucune citation corrigée par l'évaluateur (séparation §2 maintenue).
- ✓ Aucun commit ni push (per brief §3 et §6).
- ✓ `citations_registry.json` non touché (justifié §5 ci-dessus).
- ✓ Aucun guillemet courbe U+2018/U+2019 (vérification au final).
- ✓ Règle « je-ne-sais-pas » appliquée : signal du faux positif R-agrofor-olive HTML scrape, signal des discrepances d'année, sans tenter de patch silencieux.
- ✓ Verdict binaire strict appliqué : 1 fail = global FAIL, sans tentative de minimiser.

---

## 7. Rapport synthétique au chat (per brief §7)

```
GATE §10 — chantier 1 agronomie — VERDICT GLOBAL : FAIL

PASS         : 11 / 12 résolubles
FAIL         : 1
N/A (cadrage): 8 (non bloquant gate binaire, mais bloquant export FEDER per §7.3 SYNTHESE)

Liste nominale FAIL :
  - R-DI-rev (Soares et al. 2022, Agronomy 13(1):117, DOI 10.3390/agronomy13010117)
    Motif : citation détournée — paper revue MAÏS cité §3.1 pour soutenir 
    "Démontrée sur olivier, grenadier, pêcher en contexte méditerranéen/aride".
    Le générateur (Cowork) connaissait le focus maïs (mention "(maïs)" §6.1)
    mais l'a utilisé dans la liste support des cultures pérennes.

→ ARBITRAGE SOLEIL ATTENDU
  Renvoi générateur (Cowork) avec 4 options de reformulation §3 du gate.
  Aucune mise à jour citations_registry.json tant que gate non passé.
```

---

*Fin gate §10 — Code évaluateur (session locale Windows 2026-06-04). Verdict binaire : FAIL. À arbitrer par Soleil avant tout retour générateur ou commit.*
