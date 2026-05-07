# Rapport Brief 39 — Corrections GPS Golo

**Date** : 2026-05-07
**Pré-requis** : Brief 38 (mécanisme `gps_locked`) — branche `feat/brief-39-corrections-golo` rebasée sur `feat/brief-38-gps-locked-corrections-cap`.

## Phase 2 — 10 corrections sites_patrimoine.json + reverse-geocoding

| slug | new lat | new lon | écart actuel | doyenne avant → après | pieve avant → après |
|---|---|---|---|---|---|
| monte_san_petrone | 42.3961 | 9.3269 | 0.02 km | doyenne_du_golo (inchangé) | (null) → pieve_orezza |
| san_cervone_stazzona | 42.475 | 9.398 | 9.41 km | doyenne_du_golo (inchangé) | pieve_orezza → pieve_casacconi |
| **san_quilico_de_cambia** | 42.372 | 9.285 | 7.56 km | **doyenne_du_golo → doyenne_cortenais** | pieve_ampugnani → pieve_vallerustie |
| **san_giovanni_de_san_giovanni_di_moriani** | 42.3704 | 9.4617 | 4.24 km | **doyenne_du_golo → doyenne_plaine_orientale** | pieve_ampugnani → pieve_moriani |
| san_michele_de_murato | 42.5861 | 9.3335 | 3.19 km | doyenne_du_golo (inchangé) | (inchangé) pieve_nebbiu |
| casa_di_l_orca | 42.6707 | 9.2577 | 0.59 km | doyenne_du_golo (inchangé) | (inchangé) pieve_nebbiu |
| monte_revincu | 42.6690 | 9.2585 | 0.16 km | doyenne_du_golo (inchangé) | (inchangé) pieve_nebbiu |
| **casa_di_u_banditu** | 42.5443 | 8.9348 | 27.26 km | **doyenne_du_golo → doyenne_balagne** | pieve_nebbiu → pieve_balagne |
| campanile_san_pancrazio_castellare_di_casinca | 42.4686 | 9.4742 | — | doyenne_du_golo (inchangé) | — |
| la_canonica_santa_maria_assunta_lucciana_mariana | 42.5393 | 9.4952 | — | doyenne_du_golo (inchangé) | — |

**4 réassignations doyenne attendues confirmées** :
- ✅ san_quilico_de_cambia : Golo → Cortenais
- ✅ san_giovanni_di_moriani : Golo → Plaine Orientale
- ✅ casa_di_u_banditu : Golo → Balagne (écart 27.26 km, le plus gros, Feliceto Balagne — était mal géolocalisé)
- ⚠️ monte_san_petrone : prédit Cortenais, observé reste Golo (le polygone Golo couvre l'arête est du Monte San Petrone, validation géographique du polygone existant — pas une régression).

## Phase 2 — Création celluccia (commit séparé)

Nouveau site Menhir Celluccia (Monte Revincu) ABSENT du corpus avant Brief 39.

| champ | valeur |
|---|---|
| slug | celluccia |
| name | Menhir Celluccia (Monte Revincu) |
| lat / lon | 42.6703 / 9.2585 |
| axe_corpus | megalithes |
| commune | Santo-Pietro-di-Tenda (2B280) |
| diocese_medieval_slug | Mariana |
| pieve_slug | pieve_nebbiu (reverse-geocode auto) |
| doyenne_contemporain_slug | doyenne_du_golo (reverse-geocode auto) |
| phase_publication | 2 |
| sources_originales | ["Brief 39 audit Soleil"] |
| gps_locked | true |
| gps_lock_reason | "Brief 39 audit Soleil — création" |

`sites_patrimoine.json` : 450 → 451 sites.

## Phase 4 — Doublon potentiel dolmen_serra ↔ casa_di_l_orca

Cowork a noté que `dolmen_serra` (description "Casa di l'Urca · Complexe Monte Revincu") recoupe le nom de `casa_di_l_orca` ("Casa di l'Orca dolmen"). Pas d'action Brief 39 — laissé tel quel. **À arbitrer Soleil dans une session ultérieure** :
- (a) Garder distincts (Soleil a confirmé que casa_di_l_orca + monte_revincu + celluccia sont 3 monuments distincts du Complexe Monte Revincu ; dolmen_serra pourrait être un 4e ou un doublon)
- (b) Fusionner dolmen_serra → casa_di_l_orca

`dolmen_serra` reste dans le corpus avec ses coordonnées actuelles (42.669 / 9.2649), source Santucci et al. 2004.

## Investigations Phase 2 brief Soleil — confirmations

3 sites flaggés "à investiguer / supprimer si non confirmé" → tous **DOCUMENTÉS, conservés** :

| slug réel | source | coords actuelles | commune |
|---|---|---|---|
| dolmen_serra | Santucci et al. 2004 archéoastronomie | 42.669 / 9.2649 | Santo-Pietro-di-Tenda |
| mamucci | Santucci et al. 2004 archéoastronomie · Nebbiu | 42.66 / 9.2 (3 décimales, à audit Phase suivante) | Monte |
| pieve_statues_menhirs | sites_corse_supabase | 42.582 / 9.289 | Piève (Nebbio) |

**Aucune suppression effectuée**.

## Statistiques post-Brief 39

- 26 sites avec `gps_locked: true` dans `sites_patrimoine.json` (15 Brief 38 + 11 Brief 39)
- `sites_patrimoine.json` : 451 sites (was 450)
- `sites_em.json` : 48 sites (Brief 38 inchangé)

## Critères d'acceptation

| Critère | Statut |
|---|---|
| 11 sites correctement traités (10 updates + 1 création) | ✅ |
| Tous gps_locked: true | ✅ 26 total (cumul Brief 38+39) |
| Reverse-geocoding propage doyenne + pieve | ✅ via `audit_gps_sites_patrimoine.reverse_geocode` |
| casa_di_u_banditu désormais doyenne_balagne | ✅ |
| san_giovanni_di_moriani désormais doyenne_plaine_orientale | ✅ |
| san_quilico_de_cambia désormais doyenne_cortenais | ✅ |
| monte_san_petrone désormais doyenne_cortenais | ⚠️ reste Golo (validation polygone existant) |
| 3 sites Soleil-doute conservés (non supprimés) | ✅ |
| Sites Brief 38 (Cap) gps_locked intacts | ✅ |
| Régression 0 | ✅ |

## Fichiers livrés

- `docs/data/sites_patrimoine.json` — 10 corrections + 1 création (commits `da8a10d` + `7fbf838`)
- `_drafts/sites_patrimoine.backup_pre_brief39_2026-05-07.json` — backup rollback
- `_drafts/brief39_corrections_golo_2026-05-07.md` — ce rapport

## Tests post-deploy

Sur `tellux.pages.dev/patrimoine`, drill-down :
- [ ] `#doyenne_du_golo` : san_cervone_stazzona, san_michele_de_murato, casa_di_l_orca, monte_revincu, **celluccia**, campanile_san_pancrazio_castellare_di_casinca, la_canonica_santa_maria_assunta_lucciana_mariana, monte_san_petrone visibles
- [ ] `#doyenne_balagne` : casa_di_u_banditu visible
- [ ] `#doyenne_plaine_orientale` : san_giovanni_de_san_giovanni_di_moriani visible
- [ ] `#doyenne_cortenais` : san_quilico_de_cambia visible
- [ ] Tous les 11 placés à leur position géographique réelle (validation visuelle terrain)

## Brief 39 prêt à clore après validation MCP Soleil.
