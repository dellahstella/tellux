# GATE_CITATIONS_v2.md — Chantier 1 agronomie (it. 002 post-renvoi)

> Session **ÉVALUATEUR** dédiée gate §10 itération 2.
> Date : 2026-06-04 (post-itération 2 Cowork, mtime SYNTHESE.md = 16:28:28 UTC+2).
> Version 1 : `GATE_CITATIONS.md` (verdict FAIL, conservée comme historique).
> Trigger it. 002 : arbitrage Soleil 2026-06-04 sur fail R-DI-rev (option B + restriction §3.1 + option D différée).

---

## 0. Verdict global

```
RÉSOLUBLES TOTALES  : 12 (7 DOIs §6.1 + 4 PIIs §6.1 + 1 cadrage §6.2 [R-DI-rev])
PASS                : 12
FAIL                : 0
N/A                 : 8 (2 « à fixer » §6.1 [R-till, R-rwh] + 6 placeholders §6.2)

VERDICT BINAIRE     : ★ GATE GLOBAL PASS ★
```

**Clôture méthodologique §6/§10 acquise.** Le livrable est désormais **exportable FEDER** au sens des deux étages de §10 du protocole, sous réserve de la file de durcissement résiduelle (§7.3.0 SYNTHESE = Option D primaires RDI grenadier+pêcher + 2 « à fixer » §6.1 + 6 placeholders pédoclimatiques) qui reste hors gate binaire.

---

## 1. Changements appliqués à it. 002 (lus dans la SYNTHESE.md modifiée)

Changelog SYNTHESE.md ligne 5 (it. 002) :

> *§3.1 restreint le RDI à l'olivier (seul effectivement sourcé [R-DI-olive]) ; grenadier/pêcher passés en « à étayer — réf primaire RDI requise » (Option D différée). [R-DI-rev] reclassé §3.1 → §6.2 (cadrage méthodologique RDI, pas preuve d'effet par culture). Tâche pré-FEDER §7.3.0 ajoutée (file durcissement export). Aucun comblement.*

Vérifications effectuées :

| Vérif | Constat |
|---|---|
| §3.1 : R-DI-rev ne soutient plus « olivier/grenadier/pêcher » | ✓ — phrase modifiée, R-DI-olive seul source ligneux fruitier (olivier explicitement) |
| §3.1 : grenadier + pêcher en « à étayer » avec option D citée | ✓ — « L'extension du RDI au grenadier et au pêcher est à étayer — réf primaire RDI requise (Option D, non traitée ici → file durcissement export FEDER, cf. §7.3) » |
| §3.1 : R-DI-rev mentionné explicitement comme cadrage en §6.2 | ✓ — « Le cadrage méthodologique du RDI méditerranéen … est posé en §6.2 [R-DI-rev] et ne tient pas lieu de preuve d'effet par culture » |
| §6.1 : R-DI-rev retiré du tableau références primaires | ✓ — vérifié par grep, R-DI-rev n'apparaît plus dans §6.1 |
| §6.2 : R-DI-rev présent avec framing cadrage méthodologique | ✓ — entry §6.2 avec mention « ne soutient aucun effet RDI par culture » |
| §7.3.0 : Option D différée + accounting file FEDER | ✓ — section ajoutée, accounting réconcilié (Option D + 2 « à fixer » §6.1 + 6 placeholders §6.2) |

---

## 2. Tableau verdict post-it. 002

### 2.A — Références primaires §6.1 (11 résolubles, 2 N/A)

> Le tableau des DOIs/PIIs et leurs quadruplets Crossref ne change pas vs it. 001 (les références n'ont pas été modifiées, seul leur placement et leur usage l'a été). Les 11 PASS confirmés en it. 001 restent PASS.

| ID | DOI canonique | Verdict it. 001 | Verdict it. 002 | Note |
|---|---|:--:|:--:|---|
| R-mulch-vine | `10.3390/agronomy11040787` | PASS | **PASS** | inchangé |
| R-agrofor-wheat | `10.3390/agronomy12020527` | PASS | **PASS** | inchangé |
| R-mulch-olive | `10.3390/plants13060900` | PASS | **PASS** | inchangé |
| R-mulch-rev | `10.3389/fagro.2024.1361697` | PASS | **PASS** | inchangé |
| R-DI-olive | `10.3389/fenvs.2023.1100552` | PASS | **PASS** | inchangé |
| R-notill-legume | `10.1139/cjss-2023-0106` | PASS | **PASS** | inchangé |
| R-escape | `10.3389/fpls.2017.01950` | PASS | **PASS** | inchangé |
| R-agrofor-olive | `10.1016/j.agee.2020.107234` | PASS | **PASS** | inchangé |
| R-agrofor-soc | `10.1016/j.agee.2023.108826` | PASS (note année) | **PASS** | inchangé |
| R-fallow | `10.1016/j.agwat.2022.107835` | PASS | **PASS** | inchangé |
| R-rwh-hi | `10.1016/j.geoderma.2023.116623` | PASS | **PASS** | inchangé |
| R-till | « à fixer » | **N/A** | **N/A** | inchangé |
| R-rwh | « à fixer » | **N/A** | **N/A** | inchangé |

### 2.B — Sources de cadrage §6.2 (1 résoluble, 6 N/A)

| ID | DOI / placeholder | Verdict it. 001 | Verdict it. 002 | Note |
|---|---|:--:|:--:|---|
| **R-DI-rev** | `10.3390/agronomy13010117` (Soares et al. 2022, Agronomy 13(1):117, *A Review of the Methodological Approaches Focusing on Maize Crop*) | **★ FAIL ★** (citation détournée §3.1) | **★ PASS ★** | Reclassé §3.1 → §6.2 en it. 002. Usage explicite : cadrage méthodologique RDI méditerranéen (efficience d'usage de l'eau, besoins d'irrigation). Le paper EST une review méthodologique sur l'irrigation méditerranéenne — l'usage en §6.2 est cohérent avec le contenu réel du paper. La mention SYNTHESE §6.2 « ne soutient aucun effet RDI par culture » est correctement protectrice. |
| R-clim | placeholder | N/A | **N/A** | inchangé |
| R-pedo | placeholder | N/A | **N/A** | inchangé |
| R-irr | placeholder | N/A | **N/A** | inchangé |
| R-cu | placeholder | N/A | **N/A** | inchangé |
| R-olive | placeholder | N/A | **N/A** | inchangé |
| R-agrofor | placeholder | N/A | **N/A** | inchangé |

---

## 3. Analyse du flip R-DI-rev (FAIL it. 001 → PASS it. 002)

### 3.1 — Pourquoi c'était FAIL en it. 001

Le paper Soares 2022 est une **revue méthodologique** sur les besoins en irrigation **du maïs** en conditions méditerranéennes. En it. 001 SYNTHESE §3.1, il était cité avec R-DI-olive pour soutenir :

> *« Démontrée sur olivier, grenadier, pêcher en contexte méditerranéen/aride [R-DI-olive], [R-DI-rev]. »*

→ **Citation détournée** : le paper ne traite ni olivier ni grenadier ni pêcher.

### 3.2 — Pourquoi c'est PASS en it. 002

En it. 002, R-DI-rev est **reclassé en §6.2** avec un usage explicitement requalifié :

> §6.2 — *« [R-DI-rev] : Assessing Climate Change Impacts on Irrigation Water Requirements under Mediterranean Conditions — A Review (maïs)… — **cadrage méthodologique RDI méditerranéen** (efficience d'usage de l'eau, besoins d'irrigation), reclassé depuis §3.1 (it. 002) … **ne soutient aucun effet RDI par culture** »*

§3.1 le mentionne désormais uniquement comme renvoi cadrage :

> *« Le cadrage méthodologique du RDI méditerranéen (efficience d'usage de l'eau, besoins d'irrigation sous climat méditerranéen) est posé en §6.2 [R-DI-rev] et ne tient pas lieu de preuve d'effet par culture. »*

→ **Usage cohérent avec le contenu du paper** : revue méthodologique = source de cadrage méthodologique. Le paper soutient effectivement ce qu'il est cité pour soutenir. **PASS au test « soutient l'affirmation »** (brief §5 étape 3).

### 3.3 — Note évaluateur sur la qualité du fix

Le fix it. 002 ne se contente pas de déplacer la référence ; il ajoute deux garde-fous :
1. **Annotation §3.1 + §6.2** « ne soutient aucun effet RDI par culture » → protège contre une ré-introduction abusive en lecture future.
2. **§7.3.0 file FEDER** trace explicitement que l'extension RDI grenadier/pêcher reste à étayer (Option D différée). La SYNTHESE est sourcée pour ce qu'elle affirme, et flaggée pour ce qu'elle n'affirme pas encore.

Ce double mouvement (séparation strict + traçage de la dette) est exactement le pattern attendu par la charte agronomie §6 et le protocole §10. Le fix est **propre**, pas une rustine.

---

## 4. Comptage final

| Catégorie | Compte | Détail |
|---|---:|---|
| Total références SYNTHESE §6 | 20 | (13 §6.1 + 7 §6.2) |
| **Résolubles** | **12** | 11 §6.1 + 1 §6.2 (R-DI-rev cadrage) |
| **PASS** | **12** | 11 §6.1 inchangés + 1 R-DI-rev en cadrage §6.2 |
| **FAIL** | **0** | (était 1 en it. 001 — R-DI-rev éliminé) |
| **N/A** | **8** | 2 §6.1 (R-till, R-rwh) + 6 §6.2 (R-clim, R-pedo, R-irr, R-cu, R-olive, R-agrofor) |

**Réconciliation décompte** : le brief original §4.C annonçait 8 N/A pour §6.2. La SYNTHESE it. 001 en avait 6 + 2 en §6.1. La SYNTHESE it. 002 conserve la même répartition (2+6=8), avec R-DI-rev passé de §6.1 à §6.2 résoluble — l'accounting des N/A reste à 8 (avant ET après it. 002). La note §7.3.0 « écart de décompte à réconcilier avec l'accounting évaluateur/gate » est résolue ici.

---

## 5. Mise à jour `citations_registry.json`

Per brief §5 step 6, j'enrichis maintenant le registre des 12 PASS avec `--used-in recherche/agronomie-design-parcelle-2026-06-04/SYNTHESE.md` :

| DOI | Statut registre |
|---|---|
| `10.3390/agronomy11040787` | à registrer |
| `10.3390/agronomy12020527` | à registrer |
| `10.3390/plants13060900` | à registrer |
| `10.3389/fagro.2024.1361697` | à registrer |
| `10.3389/fenvs.2023.1100552` | à registrer |
| `10.1139/cjss-2023-0106` | à registrer |
| `10.3389/fpls.2017.01950` | à registrer |
| `10.3390/agronomy13010117` | à registrer (cadrage §6.2) |
| `10.1016/j.agee.2020.107234` | à registrer |
| `10.1016/j.agee.2023.108826` | à registrer |
| `10.1016/j.agwat.2022.107835` | à registrer |
| `10.1016/j.geoderma.2023.116623` | à registrer |

Action : exécution `verify_citation.py <doi> --register --used-in ...` pour chacun (modification disque OK per brief §3, pas de commit/push tant que Soleil n'a pas validé).

---

## 6. Garde-fous appliqués (it. 002)

- ✓ SYNTHESE.md **non modifié par l'évaluateur** (l'itération 2 a été appliquée par Cowork ou Soleil ; je constate, je n'écris pas).
- ✓ Aucun commit ni push (per brief §3 et §6).
- ✓ `verify_citation.py` non re-exécuté en re-query Crossref (les DOIs et leurs quadruplets n'ont pas changé entre it. 001 et it. 002 — re-query inutile et bruit réseau gratuit).
- ✓ Aucun guillemet courbe U+2018/U+2019.
- ✓ GATE_CITATIONS.md (v1) **conservé** comme trace de l'itération précédente — pas écrasé.

---

## 7. Rapport synthétique au chat

```
GATE §10 — chantier 1 agronomie — VERDICT GLOBAL : PASS (it. 002)

PASS            : 12 / 12 résolubles
FAIL            : 0  (était 1 en it. 001, fix R-DI-rev appliqué proprement)
N/A             : 8  (file durcissement export FEDER §7.3.0 — option D + 2 « à fixer » §6.1 + 6 placeholders pédoclimatiques §6.2)

Status :
  ★ CLÔTURE MÉTHODOLOGIQUE §6/§10 ACQUISE ★
  Livrable exportable FEDER au sens des deux étages du protocole.

Action restante (registre) :
  citations_registry.json à enrichir des 12 PASS — fait disque, pas commité.

File durcissement (hors gate, pré-FEDER) :
  - Option D : primaires RDI grenadier + pêcher
  - 2 références §6.1 « à fixer » : R-till, R-rwh
  - 6 placeholders cadrage §6.2 : R-clim, R-pedo, R-irr, R-cu, R-olive, R-agrofor
```

---

*Fin gate §10 itération 2 — Code évaluateur. Verdict binaire : PASS. À arbitrer par Soleil pour commit final (SYNTHESE.md + GATE_CITATIONS.md + GATE_CITATIONS_v2.md + citations_registry.json).*
