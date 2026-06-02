# État de fin de session — sprint pré-FEDER 2026-05-18

**Date :** session du 2026-05-18 (clôture documentaire 2026-05-21).
**Périmètre :** `patrimoine.html` + pipeline pieves/doyennés. Aucune modification du moteur EM.

---

## Travaux accomplis cette session

Sprint pré-FEDER massif — chantiers groupés, ~14 PRs mergées en production.

### Stratégie D — containment pieve ⊂ doyenné
- **Phase 1** (PR #635) — fix containment : split `pieve_mariana` (→ `biguglia`, `castagniccia`, `balagne`), création `pieve_altiani`, 42 sites retag. 45 → 47 pieves.
- **Phase 2** (PR #637) — splits `pieve_vico` (×3) + `pieve_balagne` (×3) : création `piana`, `sagone`, `aregno`, `calenzana`, `ostriconi`. 47 → 51 pieves.

### Navigation & mécanismes
- **§6** (PR #639) — navigation N2 → N2 directe (sans repasser par N1).
- **§7** (PR #642) — cleanup des fiches fantômes.
- **§8** (PR #643) — mécanisme `doyenne_contemporain_override` (prime sur le majoritaire calculé). Application à `pieve_bozio` (Cortenais doctrinal malgré ratio géo PO 53/47).
- PR #621 — fix UX transitions patrimoine.

### Sprint pré-FEDER — Étapes
- **Étape 1** (PR #646) — sprint hygiène : 7 dettes traitées (corrections data + invalidations).
- **Étape 3** (PR #648) — fusion `pieve_bastia` + `pieve_brando` → `pieve_lota` (7 communes), labels diocèse. 51 → 50 pieves.
- **Étape 4 — B-ZONES** (Tier 1 + Tier 2) — 23 sites naturels transformés en zones polygonales interactives au survol (`is_zone` / `zone_geometry`, renderer Leaflet ocre).
- **Étape 5 — cleanup mapping amont** (PRs #654 / #656 / #658) :
  - **D1** — mapping v4 cleanup (`_drafts/pieves_communes_mapping_v4_cleanup_2026-05-18.json`), `scripts/validate_mapping.py` REV2.
  - **D2** — archivage de 5 scripts one-shot vers `scripts/archive/phase_oneshots/`, intégration des métadonnées QW dans `build_pieves_polygons.py`.
  - **D3 / D4** — rebuild voie-a de `pieves_polygons.json` (v7) + containment check renforcé mapping ↔ dérivé.

---

## État production final

| Indicateur | Valeur |
|------------|--------|
| Pipeline | `v7-cleanup-mapping-amont-rebuild-2026-05-18` |
| Pieves | **50** |
| Communes | **360** |
| Doyennés | 9 |
| Aliases v4 | 5 (`ajaccio→gulfo`, `mariana→castagniccia`, `balagne→aregno`, `bastia→lota`, `brando→lota`) |
| Override actif | `pieve_bozio` → `doyenne_cortenais` |
| Sites B-ZONES | 23 (polygones au hover) |
| Surface totale | 8703.3 km² |
| Polygones invalides | 0 |
| Voie-a (rebuild) | viable — mapping amont ↔ dérivé alignés |

**Phase 1 beta patrimoine : production-grade.**

Garde-fous actifs : containment check commune ↔ pieve ↔ doyenné (post-build) + containment check renforcé mapping ↔ dérivé (`--strict-mapping`). `scripts/validate_mapping.py` REV2 vérifie la cohérence interne du mapping (0 zombie, 0 manquante, 360 communes).

---

## Dettes ouvertes (toutes non bloquantes)

- `PATRIMOINE-FICHES-PIEVES-VAGUE4-POST-FEDER-001` — 19 pieves sans fiche rédactionnelle (vague 4, post-FEDER).
- `MAPPING-PREQW-ORIGIN-UNKNOWN-001` — origine de `pieve_patrimonio` / `pieve_zicavo` non tracée (basse priorité).
- `PATRIMOINE-PIEVES-V7-RESHAPE-INSPECTION-001` — 11 pieves reshapées par le rebuild v7, inspection visuelle Soleil à faire (basse priorité, aucun bug identifié).
- `PATRIMOINE-B-ZONES-T2-DEFAVORABLE-001` / `PATRIMOINE-B-ZONES-ETANGS-CORPUS-001` — compléments B-ZONES post-FEDER.
- Dettes EM/physique pré-existantes (`GELÉ-001`, `NCRP-001`, `TÉLÉ-001`, etc.) — hors périmètre patrimoine.

---

## Prochaines étapes envisageables

1. **Inspection visuelle des 11 pieves reshapées** par Soleil (cf. `PATRIMOINE-PIEVES-V7-RESHAPE-INSPECTION-001`).
2. **Bascule FEDER OS1.2** — chantier de fond.
3. Investigation du diocèse `"?"` résiduel (~104.7 km² dans les stats v7).
4. Vague rédactionnelle 4 — fiches pieves (post-FEDER).

---

_Sessions Code et Cowork fermées en fin de session 2026-05-18 (clôture doc 2026-05-21). Voir `HANDOFF_NEXT_SESSION_2026-05-18.md` pour la reprise._
