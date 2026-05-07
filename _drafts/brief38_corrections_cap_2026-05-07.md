# Rapport Brief 38 — Corrections GPS Cap + mécanisme gps_locked

**Date** : 2026-05-07

## Phase 1 — Mécanisme gps_locked (commit `012e8ca`)

Ajout du garde-fou `gps_locked: true` dans `scripts/audit_gps_sites_patrimoine.py` :
- `filter_phase_sites` : skip + log les sites avec `gps_locked` au début de la boucle
- `rescue_orphans` (mode `--rescue-orphans`) : idem skip + log
- Doc en tête mise à jour

Le filter intervient AVANT toute query OSM/Wikidata/IGN, garantissant que les corrections manuelles Soleil ne seront jamais touchées par les futurs runs automatiques.

Test unitaire : `filter_phase_sites([{slug:b, gps_locked:true}])` → exclu + log `[gps_locked] b ignoré (lock: ...)`.

## Phase 2 — Corrections sites_patrimoine.json (11 sites)

| slug | new lat | new lon | note |
|---|---|---|---|
| mine_de_magnetite_de_farinole | 42.7336 | 9.3626 | ex-`_orphan_brief35` flag retiré |
| san_giovanni_de_pino | 42.908 | 9.351 | Pino Cap Corse |
| tour_de_la_chiappella_rogliano | 42.9908 | 9.4518 | pointe nord |
| mine_d_amiante_de_canari | 42.8208 | 9.3281 | précision Soleil |
| couvent_saint_francois_de_pino | 42.912 | 9.3457 | bord de mer |
| cathedrale_du_nebbio | 42.6799 | 9.3111 | centre Saint-Florent |
| tour_de_seneque_pino_luri | 42.9058 | 9.3728 | Tour de Sénèque |
| pinzu_a_vergine | 42.8799 | 9.3780 | mégalithique Barrettali |
| san_colombano_de_barrettali | 42.878 | 9.356 | col San Colombano |
| san_martino_de_patrimonio | 42.7007 | 9.3620 | hameau Cardeto |
| monte_stello | 42.7886 | 9.4181 | sommet Cap (cross-app, voir em) |

## Phase 2bis — menhirs Cap Corse (2 sites)

Décision post-investigation Cowork : sites documentés D'Anna 2019, illustrations existantes (`docs/assets/visuels/barcaggio_tellux_v2.*` + 3 WebP, idem `menhir_nonza`). Soleil confirme on garde + corrections Soleil prévalent.

| slug | new lat | new lon | écart |
|---|---|---|---|
| barcaggio | 43.0055 | 9.4027 | 3.75 km (dérive Casta soupçonnée) |
| menhir_nonza | 42.785 | 9.346 | 0.89 km |

## Phase 2 — Corrections sites_em.json (3 entrées)

| slug | new lat | new lon | extra |
|---|---|---|---|
| min_ersa | 42.976 | 9.389 | rename → "Mine d'antimoine d'Ersa (filon Granaggiolo)", description fer→antimoine, note filon secondaire 42.982/9.378 |
| min_meria | 42.926 | 9.452 | name déjà OK |
| monte_stello | 42.7886 | 9.4181 | doublon cross-app patrimoine |

## Phase 3 — Suppression

| slug | action | conservation |
|---|---|---|
| min_morsiglia | retiré de `sites_em.json` | conservé dans `sites_patrimoine.json` (axe `patrimoine_divers`) |

Backup pré-modification : `_drafts/sites_em.backup_pre_brief38_2026-05-07.json` (rollback complet possible).

## Champs appliqués sur chaque correction

```json
{
  "lat": <new>, "lon": <new>,
  "gps_audit": "2026-05-07",
  "gps_source": "Soleil manuel — audit terrain Brief 38",
  "gps_locked": true,
  "gps_lock_reason": "Brief 38 audit Soleil — ne pas modifier automatiquement",
  "notes": "<existing> | GPS corrigé manuellement par Soleil le 2026-05-07. Coord originale: (X, Y). Coord corrigée: (X', Y')."
}
```

## Statistiques post-Brief 38

- 15 sites avec `gps_locked: true` dans `sites_patrimoine.json` (11 phase 2 + 2 phase 2bis + 2 mines `min_ersa`/`min_meria` cross-applied)
- 3 sites avec `gps_locked: true` dans `sites_em.json`
- `sites_em.json` : 49 → 48 sites (suppression `min_morsiglia`)
- `sites_patrimoine.json` : 450 sites (count inchangé)

## Critères d'acceptation

| Critère | Statut |
|---|---|
| Schéma sites_patrimoine + sites_em acceptent gps_locked | ✅ champs optionnels, JSON sans schéma strict |
| Script audit_gps_sites_patrimoine.py skip locked | ✅ test unitaire OK + log par site |
| 13 sites corrigés gps_locked=true | ✅ 11 phase 2 + 2 phase 2bis = 13 |
| min_morsiglia absent de sites_em.json | ✅ |
| Décision menhir_barcaggio + menhir_nonza appliquée | ✅ phase 2bis appliquée |
| Backup pré-Brief 38 conservé | ✅ 2 fichiers backup `_drafts/` |
| Régression Briefs 27-37 | ✅ aucun fichier touché hors patrimoine.json + em.json + script |

## Fichiers livrés

- `scripts/audit_gps_sites_patrimoine.py` — mécanisme gps_locked (commit `012e8ca`)
- `docs/data/sites_patrimoine.json` — 13 corrections + verrouillage (commit `911678b`)
- `docs/data/sites_em.json` — 3 corrections + suppression min_morsiglia + verrouillage
- `_drafts/sites_patrimoine.backup_pre_brief38_2026-05-07.json` — backup rollback
- `_drafts/sites_em.backup_pre_brief38_2026-05-07.json` — backup rollback
- `_drafts/brief38_corrections_cap_2026-05-07.md` — ce rapport

## Tests post-deploy

Sur `tellux.pages.dev/patrimoine` :
- [ ] Drill-down `#doyenne_du_cap` → 7 pievi visibles (dont pieve_brando avec ses sites)
- [ ] Cliquer Mine de magnétite Farinole, Cathédrale du Nebbio, Tour de Sénèque, Tour d'Erbalunga, etc. → vérifier position visuelle terrain
- [ ] menhir_nonza et barcaggio visibles aux nouvelles coords
- [ ] Console : aucune erreur, schéma chargement OK
- [ ] App.html (couche EM) : 48 markers (vs 49 avant), `min_morsiglia` absent

Si une coord reste suspecte après inspection visuelle, déclencher un mini-Brief 38bis avec correction additionnelle (gps_locked toujours appliqué).

## Brief 38 prêt à clore après validation MCP Soleil.
