# Scripts one-shot historiques — archive

**Date d'archivage :** 2026-05-18 (Étape 5 PR B — D2 archivage scripts ad hoc).
**Référence :** audit interne PIEVE_MAPPING_AMONT 2026-05-18 + brief D2.

Ces scripts ont patché directement les JSON dérivés prod (« voie-b ») lors des
refontes pieves de mai 2026. Ils sont **one-shot** : leur effet est déjà appliqué
en production et ils ne sont **plus exécutables proprement** (ils supposent un état
antérieur du dépôt). Ils sont conservés ici **pour traçabilité uniquement** —
**ne plus exécuter en production**.

Leur logique a été soit :
- **intégrée dans `scripts/build_pieves_polygons.py`** — cas `phase_qw_pieves.py`
  (constantes `DIOCESES_TO_ADD` + strip du préfixe « Pieve di / d' »), Étape 5 PR B ;
- **absorbée dans le mapping amont v4** — cas Stratégie D / Étape 3
  (`_drafts/pieves_communes_mapping_v4_cleanup_2026-05-18.json`, Étape 5 PR A).

## Inventaire

| Script | Phase | Effet (déjà en prod) |
|--------|-------|----------------------|
| `phase_d3_pieves.py` | D-3 (2026-05-17) | Alignement `doyenne_contemporain_majoritaire` de 3 pieves. |
| `phase_qw_pieves.py` | QW (2026-05-17) | Ajout `diocese_medieval` (4 pieves), strip préfixe « Pieve di » (7 noms), recalc stats. |
| `phase_r3_rename_ajaccio.py` | R-3 (2026-05-17) | Rename `pieve_ajaccio` → `pieve_gulfo_d_aiacciu`. |
| `phase_strat_d_patch_derive.py` | Strat D Phase 1 (2026-05-17) | Patch dérivé : split `pieve_mariana`, création `castagniccia`/`biguglia`/`altiani`. |
| `phase_strat_d_phase2_splits.py` | Strat D Phase 2 (2026-05-18) | Splits `pieve_vico` ×3 + `pieve_balagne` ×3 (piana, sagone, aregno, calenzana, ostriconi). |
| `phase_strat_d_etape3_fusion_lota.py` | Étape 3 (2026-05-18) | **Reconstitué rétroactivement** — fusion `pieve_bastia` + `pieve_brando` → `pieve_lota` (exécutée par PR #648). |

## Scripts NON archivés (conservés dans `scripts/`)

`phase_strat_d_retag_sites.py` et `phase_strat_d_phase2_retag_sites.py` — retag de
sites idempotents, conservés à la racine `scripts/`.
