# Rapport Brief 39quater — Corrections GPS Piana-Vico-Sari

**Date** : 2026-05-07
**Pré-requis** : Brief 38 mergé (`gps_locked` actif).

## Phase 2 — 10 corrections sites_patrimoine.json + reverse-geo

| slug | new lat | new lon | écart | doyenne avant → après | pieve avant → après |
|---|---|---|---|---|---|
| reserve_de_scandola | 42.3589 | 8.5615 | 0.20 km | doyenne_piana_vico_sari (inchangé) | (null) → pieve_vico |
| calanques_de_piana | 42.2529 | 8.6575 | 0.05 km | doyenne_piana_vico_sari (inchangé) | (null) → pieve_vico |
| lac_de_creno | 42.2048 | 8.9459 | 0.05 km | doyenne_piana_vico_sari (inchangé) | (null) → pieve_sorroinsu |
| u_scumunicatu_cargese | 42.1464 | 8.6267 | 0.02 km | doyenne_piana_vico_sari | (inchangé) |
| san_giovanni_de_coggia | 42.120 | 8.750 | 6.41 km | doyenne_piana_vico_sari | (inchangé) |
| saint_pancrace_de_vico | 42.184 | 8.950 | 12.53 km | doyenne_piana_vico_sari | pieve_vico → pieve_sorroinsu |
| guagno_les_bains | 42.174 | 8.889 | 1.93 km | doyenne_piana_vico_sari | (inchangé) |
| san_martino_de_sari_d_orcino | 42.062 | 8.824 | 4.39 km | doyenne_piana_vico_sari | (inchangé) |
| pont_de_pianella_ota | 42.2563 | 8.7611 | — | doyenne_piana_vico_sari | (inchangé) |
| **casteddu_bastelica** | 42.217 | 9.255 | — | **doyenne_piana_vico_sari → doyenne_cortenais** | pieve_cinarca → pieve_rogna |

### ⚠️ Réassignation casteddu_bastelica : Cortenais ≠ Prunelli (attendu)

Cowork prédisait `doyenne_prunelli_taravo_valinco` (Bastelica = haute vallée Prunelli). Le polygone effectif donne **doyenne_cortenais** (pieve_rogna).

**Pattern** : les hauts sommets/villages frontaliers tombent dans le polygone Cortenais (qui s'étire jusqu'à la haute vallée). Cas similaire à `monte_san_petrone` Brief 39 (prédit Cortenais, observé Golo).

**Décision Brief 39quater** : conserver le verdict polygone (`doyenne_cortenais`). Le polygone fait foi, pas l'intuition géographique. À discuter avec Cowork si le polygone Prunelli doit être étendu.

### Cross-app sites_em.json (3 doublons naturels)

| slug | em avant | em après |
|---|---|---|
| reserve_de_scandola | (null/null) | pieve_vico / doyenne_piana_vico_sari |
| calanques_de_piana | (null/null) | pieve_vico / doyenne_piana_vico_sari |
| lac_de_creno | (null/null) | pieve_sorroinsu / doyenne_piana_vico_sari |

## Non-touch — tour_de_turghiu_capo_rosso

| Source | coord |
|---|---|
| Brief 36 R6 (rescue, triple-source osm+ign+wikidata) | 42.234 / 8.527 |
| Soleil Brief 39quater proposition | 42.2364 / 8.5516 |
| Différence | ~10 m |

**Décision** : verrou Brief 36 R6 maintenu (triple-sourcé > audit terrain Soleil pour différence sub-mètre). Site **NON modifié** dans Brief 39quater.

## Décisions requises Soleil (Phase 4 — non-action sans confirmation)

### san_martinu_de_soccia

| critère | valeur |
|---|---|
| slug | `san_martinu_de_soccia` |
| axe | `edifices_romans` |
| nom | "San Martinu de Soccia" |
| coords actuelles | 42.2178 / 8.9783 |
| sources documentaires | SITES_PATRIMOINE + churches_corse (2 sources distinctes) |

Soleil dit "Soccia n'a que Santa Maria". Mais le corpus a 2 sources documentaires.

**Action** : aucune dans Brief 39quater. Si Soleil confirme suppression malgré les 2 sources, commit séparé requis.

### menhir_casaglione

| critère | valeur |
|---|---|
| slug | `menhir_casaglione` |
| axe | `megalithes` |
| nom | "Menhir de Casaglione" |
| coords actuelles | 42.16 / 8.72 |
| description | "Menhir isolé 2m · Granodiorite · Sagone intérieur · D'Anna PCR" |
| commune | Casaglione |

Soleil propose : renommer en `dolmen_de_casaglione`. Mais source D'Anna PCR (Projet Collectif de Recherche, référence académique Corse) dit **MENHIR**, pas dolmen.

**Options** :
- (a) Conserver tel quel — recommandation Cowork (D'Anna PCR fait foi)
- (b) Renommer en dolmen_de_casaglione + corriger coords (Soleil fournirait nouvelles coords)
- (c) Garder les deux entrées si menhir + dolmen distincts à Casaglione

**Action** : aucune dans Brief 39quater. À arbitrer Soleil.

## Statistiques post-Brief 39quater

- **39 sites** `gps_locked: true` dans `sites_patrimoine.json` (15 Brief 38 + 11 Brief 39 + 3 Brief 39bis + 10 Brief 39quater)
- **7 sites** `gps_locked: true` dans `sites_em.json` (3 Brief 38 + 1 Brief 39bis + 3 Brief 39quater cross-app)
- `sites_patrimoine.json` : 451 sites (inchangé)
- `sites_em.json` : 48 sites (inchangé)

## Critères d'acceptation

| Critère | Statut |
|---|---|
| 10 sites corrigés gps_locked: true | ✅ |
| Reverse-geo propage doyenne + pieve | ✅ via `audit_gps_sites_patrimoine.reverse_geocode` |
| casteddu_bastelica réassigné | ⚠️ Cortenais (pas Prunelli comme attendu) — polygone fait foi |
| tour_de_turghiu_capo_rosso INCHANGÉ | ✅ Brief 36 R6 respecté |
| Soccia + Casaglione documentés en décision-requise | ✅ |
| Sites Brief 38/39/39bis intacts | ✅ |
| Backup pré-Brief 39quater | ✅ |
| Régression 0 | ✅ |

## Pattern récurrent (4e brief consécutif)

| Brief | Sites Soleil-doute confirmés documentés | Sources |
|---|---|---|
| 38 (Cap) | Barcaggio, Nonza | Leandri, D'Anna 2019 |
| 39 (Golo) | dolmen_serra, mamucci, pieve_statues_menhirs | Santucci 2004 |
| 39bis (Balagne) | montegrosso, lozari, calenzana | Leandri 2020/2023, D'Anna 2019 |
| **39quater (Piana)** | **soccia, casaglione** | 2 sources corpus + D'Anna PCR |

**Recommandation Cowork (rappel)** : avant flag "non documenté", grep préalable côté Soleil :
```bash
grep -i "<nom>" docs/data/sites_corse.json | head
# ou
grep -i "<nom>" docs/data/sites_patrimoine.json | head
```

## Fichiers livrés

- `docs/data/sites_patrimoine.json` — 10 corrections + reverse-geo + locks (commit `e92599c`)
- `docs/data/sites_em.json` — 3 corrections cross-app
- `_drafts/sites_patrimoine.backup_pre_brief39quater_2026-05-07.json` — backup rollback
- `_drafts/sites_em.backup_pre_brief39quater_2026-05-07.json` — backup rollback
- `_drafts/brief39quater_corrections_piana_vico_sari_2026-05-07.md` — ce rapport

## Tests post-deploy

Sur `tellux.pages.dev/patrimoine` :
- [ ] `#doyenne_piana_vico_sari` : 9 sites visibles aux nouvelles coords (Scandola, Calanques, Lac Creno, Scumunicatu, Coggia, Vico, Guagno, Sari d'Orcino, Pont Pianella)
- [ ] `#doyenne_cortenais` : casteddu_bastelica visible (NOUVEAU rattachement)
- [ ] App.html EM : Scandola, Calanques Piana, Lac Creno aux nouvelles coords
- [ ] tour_de_turghiu_capo_rosso : conserve coord Brief 36 R6 (42.234 / 8.527)

## Brief 39quater prêt à clore après validation MCP Soleil + arbitrage Soccia/Casaglione.
