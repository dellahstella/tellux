# Rapport Brief 34 — Phases B-F + retry ABSENT (consolidé)

**Date** : 2026-05-06
**Périmètre cumulé** : 6 phases A-F sur 411 sites au total.
**Script** : `scripts/audit_gps_sites_patrimoine.py` (élargi avec mode `--retry-absent` et idempotency).

---

## Bilan global

| Phase | Sites | Tier 1 initial | Tier 1 post-retry | Total Tier 1 |
|---|---|---|---|---|
| A — Cap + Cortenais             | 96 | 10 | 0 | **10** |
| B — Plaine Orientale + Ajaccio  | 56 |  1 | 0 |  **1** |
| C — Golo + Balagne              | 79 |  5 | 0 |  **5** |
| D — Extrême-Sud + Piana-Vico    | 92 | 14 | 0 | **14** |
| E — Prunelli-Taravo-Valinco     | 36 |  0 | 0 |  **0** |
| F — sites doyenne=null          | 52 |  1 | 2 |  **3** |
| **Total** | **411** | **31** | **2** | **33** |

**33 sites mis à jour avec coords 5 décimales et `gps_audit=2026-05-06`** sur 411 audités (taux d'auto-apply ≈ 8%).

---

## Retry orthographique — bilan

Stratégie de variantes appliquée aux 82 sites ABSENT : strip parenthèses + suffixes locatifs (`haute`, `basse`, `village`, `intérieur`, `versant`, etc.) + variante FR (`San` → `Saint`, `Santa` → `Sainte`).

| Phase | ABSENT initial | Recovered (≥1 source) | Tier 1 ajout |
|---|---|---|---|
| A | 14 |  8 | 0 |
| B |  7 |  7 | 0 |
| C | 13 | 10 | 0 |
| D | 13 |  9 | 0 |
| E |  6 |  6 | 0 |
| F | 29 | 15 | 2 |
| **Total** | **82** | **55 (67%)** | **2** |

Les 55 sites recovered ont presque tous une distance new/old > 5 km — ils tombent dans le filtre `DIST_OVER_5000m` automatique. Stripper les parenthèses désambiguïsantes fait perdre la précision géographique : "San Giovanni (Bastelicaccia)" → "San Giovanni" peut matcher n'importe quel saint Jean en Corse.

**Seuls 2 sites Phase F ont survécu au filtre** :
- `pont_de_zippitoli_disparu_2023` (osm+wikidata, 3.6 km) — variante "Pont de Zippitoli"
- `tour_de_turghiu_capo_rosso` (osm+wikidata, 2.1 km) — variante "Tour de Turghiu"

Les 27 ABSENT restants (non recovered) sont des sites avec :
- nom déjà sans parenthèses (pas de variante générable)
- nom trop spécifique pour matcher (mégalithes locaux, mines, sources)
- nom trop générique pour ressortir parmi homonymes

---

## Bug détecté et corrigé en cours d'exécution

Lors du re-apply Phase F après retry, deux sites ont été appliqués à tort :
- `pietrapola_station_thermale` (10 km de l'original)
- `san_giuliano_cuttoli_haute` (65 km de l'original)

Cause : la condition `row['note'] == "DIST_OVER_5000m"` ne matchait pas le format combiné `"DIST_OVER_5000m | RETRY_VARIANT:..."` introduit par le retry. Les 2 sites passaient le filtre Tier 1 alors qu'ils étaient flaggés.

**Fix** : `"DIST_OVER_5000m" in row.get("note", "")` (substring match).

**Rollback** : les 2 sites ont été restaurés à leurs coords originales depuis `_drafts/sites_patrimoine.backup_2026-05-06.json`. Le `gps_audit` et `gps_source` ont été retirés du JSON pour ces 2 sites. Total final : 33 sites correctement audités.

---

## Idempotency ajoutée à `apply_updates`

Pour éviter d'empiler plusieurs lignes `gps_audit_2026-05: orig=(...)` dans le `notes` lors d'un re-apply (ex. retry-apply après initial-apply), `apply_updates` skip maintenant les sites dont `gps_audit == TODAY` ET `lat/lon == new_lat/new_lon`. Mention `applied=AlreadyApplied` dans le CSV.

---

## Fichiers livrés (Brief 34 Phases B-F + retry)

- `scripts/audit_gps_sites_patrimoine.py` — script enrichi (modes `--retry-absent`, idempotency, fix substring match)
- `docs/data/sites_patrimoine.json` — 33 sites cumulés audités
- `_drafts/audit_gps_phaseB_2026-05-06.csv` à `_drafts/audit_gps_phaseF_2026-05-06.csv` — full résultats incluant retries
- `_drafts/sites_patrimoine.backup_2026-05-06.json` — backup pre-Phase-A (point d'entrée rollback complet)
- `_drafts/RAPPORT_audit_gps_phaseB_*.md` à `phaseF_*.md` — rapports par phase
- `_drafts/RAPPORT_audit_gps_phases_BCDEF_retry_2026-05-06.md` — ce rapport global

---

## Recommandations Soleil

1. **Pour les ~378 sites non auto-appliqués (411 - 33)** : revue cartographique manuelle requise. Les CSV par phase contiennent toutes les coords candidates (OSM/Wikidata/IGN), distance à l'original, concordance pieve/doyenné — base solide pour valider/invalider visuellement.
2. **Pour les 27 ABSENT non recovered** : enrichissement manuel via Wikipedia (recherche par commune), Géoportail, archives départementales, ou photos terrain.
3. **Pour les 55 recovered avec dist >5km** : à examiner cartographiquement pour distinguer (a) coord originale fausse → adopter la nouvelle, (b) homonyme parasité → conserver l'original, (c) site disparu/déplacé.
4. **Phases ultérieures** : si besoin de re-auditer après corrections manuelles, utiliser `--from-csv` pour skip réseau et tester de nouveaux filtres heuristiques sans coût additionnel.
