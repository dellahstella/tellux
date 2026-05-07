# Rapport Brief 39bis — Corrections GPS Balagne

**Date** : 2026-05-07
**Pré-requis** : Brief 38 mergé (mécanisme `gps_locked` actif).

## Phase 1 — 2 corrections sites_patrimoine.json

| slug | new lat | new lon | écart | doyenne | pieve |
|---|---|---|---|---|---|
| la_trinite_d_aregno | 42.5822 | 8.8978 | ~70 m (corrigé partiellement Brief 35) | doyenne_balagne (inchangé) | pieve_balagne (inchangé) |
| **monte_genova** | 42.6883 | 9.1957 | 9.49 km | **doyenne_balagne → doyenne_du_golo** | pieve_nebbiu (inchangé) |

**Reclassement axe Monte Genova** :
- `axe_corpus` : `megalithes` → `remarquables_geologiques`
- `categorie` : `Mégalithique` → `Site naturel remarquable`
- `name` : "Monte Genova mégalithes" → "Monte Genova"
- `description` : réécrite (sommet 421m désert des Agriates, aucun mégalithe au sommet, Monte Revincu à 5km au sud)

⚠️ **Conflit source D'Anna 2019 vs audit Soleil** : la source académique D'Anna 2019 mentionne "ensemble mégalithique" au Monte Genova. L'audit terrain Soleil ne confirme aucun mégalithe au sommet. **Décision Brief 39bis : la version Soleil prime** (audit terrain), site reclassé en sommet. À arbitrer Soleil si nuance souhaitée.

## Phase 2 — Argentella : CORRECTION (pas création)

Soleil annonçait l'**ajout** d'un nouveau slug `mines_argentella_calenzana`. Vérification Cowork : `min_argentella` existe **déjà** dans le corpus (slug Brief 33 P1) avec coords erronées (42.354, 8.882) — placement au sud alors que l'Argentella historique est plage Calvi/Calenzana NORD.

**Décision** : ne pas créer de doublon, corriger `min_argentella` dans **les deux JSON** :

| fichier | avant | après |
|---|---|---|
| `sites_patrimoine.json` | (42.354, 8.882) doy=doyenne_balagne pieve=pieve_balagne | (42.46076, 8.70999) doy=doyenne_balagne pieve=pieve_balagne |
| `sites_em.json` | (42.354, 8.882) doy=(null) pieve=(null) | (42.46076, 8.70999) doy=doyenne_balagne pieve=pieve_balagne |

`gps_source` : "Soleil manuel + IGN — audit terrain Brief 39bis"
`gps_lock_reason` : "Brief 39bis audit Soleil — correction GPS Argentella plage Calvi/Calenzana"

Note enrichie : galène argentifère XIXe + projet nucléaire 1960 abandonné, vestiges usine/barrage/galeries, altitude ~35m, plage historique Calvi/Calenzana NORD.

**Question à Soleil** : confirme-t-il que `min_argentella` (corpus existant) et `mines_argentella_calenzana` (qu'il proposait d'ajouter) sont bien le **MÊME SITE** ? Cowork le pense (toponyme commun "Argentella", commune Calenzana, contexte historique "galène argentifère XIXe + projet nucléaire 1960" qui matche les deux descriptions).

Si NON, reverter le commit `96ec1f0` (backup `_drafts/sites_em.backup_pre_brief39bis_*` + `sites_patrimoine.backup_pre_brief39bis_*`) et créer `mines_argentella_calenzana` comme nouveau slug distinct.

## Phase 3 — Investigations Cowork TRANCHÉES

3 sites flaggés "à investiguer / supprimer si non confirmé" → tous **DOCUMENTÉS, conservés** :

| slug réel | source | coords actuelles | commune |
|---|---|---|---|
| alignement_montegrosso | Leandri 2023 | 42.608 / 8.869 | Montegrosso |
| casteddu_lozari | D'Anna 2019 | 42.56 / 8.87 | Belgodère (Lozari = lieu-dit cohérent) |
| menhir_calenzana | Leandri 2020 | 42.507 / 8.855 | Calenzana |

**Aucune suppression effectuée**.

## Phase 4 — Dédoublonnage la_trinite_d_aregno

Cowork confirme : 1 seule entrée trouvée, pas d'entrée fantôme avec icône ?. Le doublon Brief 35 cat 3a a été supprimé lors d'une vague antérieure. Pas d'action requise — juste la correction GPS Phase 1.1.

## Statistiques post-Brief 39bis

- **29 sites** avec `gps_locked: true` au total dans `sites_patrimoine.json` (15 Brief 38 + 11 Brief 39 + 3 Brief 39bis = 29)
- **4 sites** avec `gps_locked: true` dans `sites_em.json` (3 Brief 38 + 1 Brief 39bis = 4)
- `sites_patrimoine.json` : 451 sites (inchangé Brief 39)
- `sites_em.json` : 48 sites (inchangé Brief 38)

## Critères d'acceptation

| Critère | Statut |
|---|---|
| 3 sites corrigés (Trinité, Monte Genova, Argentella) gps_locked=true | ✅ |
| Monte Genova reclassé en sommet (axe remarquables_geologiques) | ✅ |
| min_argentella corrigé dans sites_em + sites_patrimoine | ✅ |
| 3 sites Soleil-doute (montegrosso/lozari/calenzana) intacts | ✅ |
| Sites Brief 38/39 (Cap, Golo) gps_locked respectés | ✅ |
| Backup pré-Brief 39bis conservé | ✅ |
| Régression 0 | ✅ |

## Pattern récurrent à signaler à Soleil

**3e brief consécutif** où des sites flaggés "probablement non documenté, à supprimer" se révèlent être DOCUMENTÉS dans le corpus avec sources académiques :

| Brief | Sites Soleil-doute confirmés documentés |
|---|---|
| Brief 38 | menhirs Cap (barcaggio, menhir_nonza — D'Anna 2019) |
| Brief 39 | dolmen_serra, mamucci, pieve_statues_menhirs (Santucci et al. 2004) |
| Brief 39bis | alignement_montegrosso, casteddu_lozari, menhir_calenzana (Leandri 2020/2023, D'Anna 2019) |

**Recommandation Cowork** : avant de flagger un site comme "non documenté", grep rapide :
```bash
grep -i "<nom_du_site>" docs/data/sites_corse.json
# ou directement
grep -i "<nom>" docs/data/sites_patrimoine.json
```
Cela évite d'envoyer des suppressions hâtives ensuite annulées par Cowork.

## Fichiers livrés

- `docs/data/sites_patrimoine.json` — 3 corrections + reclassement axe
- `docs/data/sites_em.json` — 1 correction (min_argentella)
- `_drafts/sites_patrimoine.backup_pre_brief39bis_2026-05-07.json` — backup rollback
- `_drafts/sites_em.backup_pre_brief39bis_2026-05-07.json` — backup rollback
- `_drafts/brief39bis_corrections_balagne_2026-05-07.md` — ce rapport

## Tests post-deploy

Sur `tellux.pages.dev/patrimoine` :
- [ ] Drill-down `#doyenne_balagne` : la_trinite_d_aregno + min_argentella visibles aux nouvelles coords
- [ ] Drill-down `#doyenne_du_golo` : monte_genova visible (NOUVEAU rattachement, plus dans Balagne)
- [ ] App.html (couche EM) : min_argentella visible plage Calvi/Calenzana NORD (vs sud avant)
- [ ] Monte Genova rendu cercle vert (`Site naturel remarquable`) — pas marker mégalithique

## Brief 39bis prêt à clore après validation MCP Soleil.
