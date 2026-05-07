# Rapport Brief 36 — R5 + R6 (clos)

**Date** : 2026-05-07 (R6 réseau exécuté tard 2026-05-06 → CSV daté 2026-05-07)

## R5 — 22 orphans traités (Cowork)

| Action | Nombre | Détail |
|---|---|---|
| ASSIGNED | 7 | pieve_slug + doyenne_contemporain_slug attribués |
| FLAGGED_ORPHAN | 15 | `_orphan_brief35: true`, dist > 5km de tout polygone |

**Sites assignés** : couvent_saint_francois_de_pino, san_giovanni_de_pino, san_martinu_alando, sant_andria_sermano_haut, santa_maria_assunta_ajaccio_bazzicacce, santa_maria_campile, tour_de_la_chiappella_rogliano.

Log Cowork : `_drafts/brief_36_r5_orphans_log.csv`.

## R6 — Rescue orphans (Code, mode `--rescue-orphans`)

### Note méthodo

Le script `audit_gps_rescue_mode.py` annoncé n'a pas été livré par Cowork. J'ai intégré la logique au script existant `scripts/audit_gps_sites_patrimoine.py` (Brief 34) avec un nouveau mode `--rescue-orphans` qui :

1. Filtre les sites `_orphan_brief35: true`
2. Tente nom original + 2-3 variantes orthographiques sur OSM/Wikidata/IGN
3. Reverse-geocode → détermine pieve/doyenné
4. Applique garde-fous renforcés post audit dry-run

### Garde-fous

- **Auto-accept** si `dist new/old < 1km` (cas îlots côtiers type Giraglia)
- **Reject homonyme** si `pieve_geo ≠ pieve_decl` ET `dist > 5km` (ex. san_nicolao matche un homonyme dans pieve_moriani au lieu de pieve_bozio)
- **HAUTE/MOYENNE** in-Corse OK (3 sources concordantes)
- **FAIBLE ≥2 sources** in-Corse OK

Le 1er dry-run sans garde-fou homonyme a accepté 7 sites mais 3 étaient des homonymes à >20km. Garde-fou ajouté → 5 RESCUE_OK propres.

### Résultats

| Statut | Nombre | Détail |
|---|---|---|
| RESCUE_OK | 5 | tours côtières + Giraglia |
| RESCUE_REJECTED | 7 | 5 homonymes + 2 hors-Corse |
| RESCUE_ABSENT | 3 | aucune source |

**5 sites rescued** :
| slug | confiance | sources | dist | pieve_geo | doyenne_geo |
|---|---|---|---|---|---|
| tour_d_erbalunga_brando | HAUTE | osm+ign+wd | 16.4 km | pieve_brando | doyenne_du_cap |
| tour_d_omigna_cargese | MOYENNE | osm+ign+wd | 1.1 km | pieve_vico | doyenne_piana_vico_sari |
| tour_de_capitello_castelluccio | MOYENNE | osm+ign+wd | 2.1 km | pieve_ornano | (null) |
| tour_de_giraglia_ilot | HAUTE | osm+ign+wd | 130 m | (îlot) | (îlot) |
| tour_de_turghiu_capo_rosso | MOYENNE | osm+wd | 0.5 m | pieve_vico | doyenne_piana_vico_sari |

**10 sites restent flagged** :
- 7 RESCUE_REJECTED (homonymes ou hors-Corse) : castellu_di_bozzi_guitera, couvent_sant_antoni_de_calvi, san_giovanni_de_santa_maria_siche, san_nicolao_pianello_bozio, san_nicolao_sermano, santa_maria_carpineto, santa_maria_della_neve_grosseto_prugna_basse
- 3 RESCUE_ABSENT (aucune source) : menhir_sermano, mine_de_magnetite_de_farinole, tour_de_capo_di_muro

Ces 10 sites nécessitent un audit manuel Soleil (Google Earth + Wikipedia) si Soleil veut les visibles au drill-down.

## Bilan Brief 36

| Sub-brief | Statut |
|---|---|
| R4 sticker niveau 2 | ✅ PR #398 mergée |
| R5 37 orphans | ✅ 22 traités (7 ASSIGNED + 15 FLAGGED) |
| R6 5 sites en mer | ✅ 5 rescued + 10 flagged résiduels |
| R7 vundefined log | ✅ PR #398 mergée |
| Bug niveau 1→2 systémique | ✅ couvert par Cat. 2 Brief 35 (70 réalignements) + R5 (7 ASSIGNED) |

Brief 36 est prêt à clore après validation MCP Soleil sur prod.

## Fichiers livrés

- `scripts/audit_gps_sites_patrimoine.py` — mode `--rescue-orphans` ajouté (commit 33aa2c8)
- `docs/data/sites_patrimoine.json` — 5 sites rescued + 10 résiduels flagged
- `_drafts/audit_gps_rescue_2026-05-07.csv` — full résultats 15 lignes
- `_drafts/sites_patrimoine.backup_rescue_2026-05-07.json` — backup pre-apply
- `_drafts/brief_36_r5_orphans_log.csv` — log R5 Cowork (22 lignes)

## Recommandations Soleil (10 résiduels)

Pour chaque site ci-dessous, ouvrir Google Earth + Wikipedia, relever lat/lon précises, transmettre à Cowork pour patch direct.

**Sites avec homonymes potentiels** (priorité haute, le site existe probablement) :
- castellu_di_bozzi_guitera (Guitera-les-Bains)
- couvent_sant_antoni_de_calvi (Calvi)
- san_giovanni_de_santa_maria_siche (Santa-Maria-Siché)
- san_nicolao_pianello_bozio (Pianello / Bozio — désambiguïsation requise)
- san_nicolao_sermano (Sermano)
- santa_maria_carpineto (Carpineto)
- santa_maria_della_neve_grosseto_prugna_basse (Grosseto-Prugna)

**Sites absents** (peu documentés, peut nécessiter sources alternatives) :
- menhir_sermano
- mine_de_magnetite_de_farinole (mine industrielle XIX-XXe)
- tour_de_capo_di_muro

Si certains sites n'existent plus matériellement (ruines effondrées, sites disparus), envisager un flag `_archive_only: true` pour les retirer du drill-down sans les supprimer du corpus.
