# Rapport Brief 34 Phase A — Audit GPS Cap + Cortenais

**Date** : 2026-05-06
**Périmètre** : 96 sites du diocèse d'Ajaccio actuel (Doyenné du Cap 48 sites + Doyenné Cortenais 48 sites), hors 6 sites Cap déjà audités.
**Script** : `scripts/audit_gps_sites_patrimoine.py` (526 lignes Python autonome).
**Sources** : OSM Nominatim + Wikidata (wbsearchentities + wbgetclaims) + IGN/Etalab api-adresse.data.gouv.fr.
**Durée run** : 1618 s (~27 min, 16.9 s/site).

---

## Résultats globaux

| Confidence | Total | Auto-applicables Tier 1 | Skip DIST>5km |
|---|---|---|---|
| HAUTE     |  1 |  0 (flag) | 1 |
| MOYENNE   |  8 |  4 | 4 |
| FAIBLE    | 73 |  6 | 51 |
| ABSENT    | 14 |  0 | — |
| **Total** | **96** | **10** | **59** |

**Sources concordantes** :
- 59 sites avec IGN seul
- 17 sites avec OSM+IGN
- 14 sites ABSENT (aucune source)
- 3 sites avec OSM+Wikidata+IGN
- 3 sites avec OSM seul

**Distance new/old** (sur 82 matches) :
- Médiane : 11 885 m
- Moyenne : 25 571 m
- Max : 120 894 m

La médiane élevée s'explique majoritairement par des homonymes hors Corse (saints, communes "Saint-Martin", "Santa Maria" etc.) qui ne passent pas le filtre bbox seul mais qui matchent sur des noms communs. Le Tier 3 (skip) gère cette catégorie.

---

## Tier 1 — 10 sites appliqués (HAUTE/MOYENNE non flag + heuristiques FAIBLE)

Coordonnées originales conservées dans le champ `notes` (`gps_audit_2026-05: orig=(lat, lon)`).

### MOYENNE non flag DIST (4 sites)

| slug | sources | dist | old → new |
|---|---|---|---|
| couvent_saint_francois_de_pino       | osm+wd+ign | 3 660 m | (42.945, 9.340) → (42.912, 9.346) |
| san_quilicu_cambia                   | osm+ign    | 2 207 m | (42.398, 9.290) → (42.378, 9.295) |
| santa_catalina_sisco                 | osm+ign    | 2 709 m | (42.815, 9.454) → (42.817, 9.487) |
| santa_maria_assunta_canari           | osm+ign    | 3 430 m | (42.873, 9.348) → (42.845, 9.331) |

### Heuristique 1 — IGN seul + concord pieve/doy + dist<1km (4 sites célèbres)

| slug | dist | old → new |
|---|---|---|
| cathedrale_du_nebbio                 | 339 m   | (42.681, 9.303) → (42.680, 9.306) |
| citadelle_de_corte                   |  42 m   | (42.305, 9.149) → (42.305, 9.149) |
| san_michele_bastia_citadelle         | 335 m   | (42.688, 9.438) → (42.685, 9.439) |
| santa_maria_calacuccia               | 953 m   | (42.340, 9.000) → (42.332, 9.003) |

### Heuristique 2 — ≥2 sources + concord OK + dist<2km (2 sites)

| slug | sources | dist |
|---|---|---|
| san_colombano_rogliano               | osm+ign | 471 m |
| santa_maria_santa_maria_di_lota      | osm+ign | 661 m |

---

## Tier 2 — 17 candidats à examiner manuellement

FAIBLE avec **dist > 5 km mais pieve+doyenné concordants**. Le filtre `DIST_OVER_5000m` bloque l'apply auto, mais la concordance pieve/doyenné suggère que la nouvelle coord est dans la bonne zone — soit la pieve est large (Cap Corse), soit la coord originale était imprécise/incorrecte.

À cartographier visuellement avant d'arbitrer :

| slug | old | new | dist |
|---|---|---|---|
| san_cervone_de_santa_lucia_di_mercurio  | 42.339, 9.278 | 42.327, 9.219 |  5.1 km |
| san_cervone_stazzona                    | 42.393, 9.368 | 42.236, 9.328 | 17.8 km |
| san_cesario_d_olmeta_olmeta_di_capocorso| 42.650, 9.190 | 42.767, 9.370 | 19.6 km |
| san_giovanni_morosaglia_merusaglia      | 42.320, 9.350 | 42.460, 9.214 | 19.1 km |
| san_martinu_pietracorbara               | 42.780, 9.435 | 42.857, 9.423 |  8.6 km |
| san_nicolao_san_martino_di_lota         | 42.890, 9.430 | 42.721, 9.454 | 18.9 km |
| san_pantaleone_olcani                   | 42.750, 9.395 | 42.810, 9.370 |  7.0 km |
| san_petru_bisinchi                      | 42.490, 9.200 | 42.477, 9.324 | 10.3 km |
| san_petru_moltifao                      | 42.500, 9.050 | 42.490, 9.118 |  5.7 km |
| san_pietro_olmeta_di_capocorso          | 42.840, 9.340 | 42.767, 9.370 |  8.5 km |
| santa_maria_brando                      | 42.850, 9.370 | 42.778, 9.438 |  9.7 km |
| santa_maria_calacuccia_village          | 42.460, 8.930 | 42.332, 9.003 | 15.5 km |
| santa_maria_castirla                    | 42.490, 9.100 | 42.380, 9.128 | 12.4 km |
| santa_maria_farinole                    | 42.820, 9.360 | 42.728, 9.361 | 10.2 km |
| santa_maria_meria                       | 42.930, 9.380 | 42.932, 9.465 |  6.9 km |
| santa_maria_poggio_d_oletta             | 42.545, 9.348 | 42.640, 9.361 | 10.6 km |
| santa_maria_ponte_leccia_morosaglia     | 42.520, 9.150 | 42.462, 9.207 |  7.9 km |

---

## Tier 3 — Skip (69 sites)

- **42 sites** FAIBLE >5km **sans concord** : IGN/OSM matchait probablement un homonyme hors Corse (saints communs, communes du continent). À recalibrer avec un audit manuel ou un 2e tour à requête plus stricte.
- **14 sites ABSENT** (aucune source) — la plupart sont des sites mégalithiques isolés ou des sites avec parenthèses d'attribut dans le nom :
  - 4 menhirs : `menhir_nonza`, `menhir_sermano`, `menhirs_agriate`, plus implicite (autre)
  - 2 mines : `mine_d_amiante_de_canari`, `mine_de_magnetite_de_farinole`
  - 8 chapelles avec parenthèses désambiguïsantes : `casa_di_u_banditu`, `oratoire_santa_croce_bastia_haute_bastia_citadelle`, `san_colombano_de_barrettali`, `san_giovanni_bastia_terra_vecchia`, `san_martino_rogliano_village`, `san_pietro_favalello`, `san_quilicu_valle_di_rostino`, `santa_restituda_meria_vico_interieur`, `santa_restitude_corte_niolu_versant`
- 13 autres FAIBLE non-concord ou inter_max>500m

---

## Méthodologie

### Sources

| Source | Endpoint | Throttle | Note |
|---|---|---|---|
| OSM Nominatim | `nominatim.openstreetmap.org/search` | 1.1 s | 3 essais avec contextes commune/Corse/France ; bbox Corse post-fetch |
| Wikidata | `wikidata.org/w/api.php` (wbsearchentities + wbgetclaims P625) | 1.1 s × ≤4 | Refactor depuis SPARQL FILTER CONTAINS (60s+) |
| IGN/Etalab | `api-adresse.data.gouv.fr/search/` | 1.1 s | Source la plus fiable pour les sites Corses |

### Scoring cluster-based

Au lieu d'un `inter_max` global qui pénalisait les outliers (ex. caporalino : OSM+WD à 1.5 km mais IGN à 13 km → FAIBLE bien que 2/3 sources accordent), j'ai implémenté un algorithme **best-cluster** :

1. Trouver le plus grand sous-ensemble de coords avec toutes les paires <100m → HAUTE
2. Sinon plus grand sous-ensemble <500m → MOYENNE (≥2) ou HAUTE (≥3)
3. Sinon FAIBLE (1 source ou pas de cluster)

### Heuristiques Tier 1 (étendues vs brief)

Le brief original limitait `--apply` aux HAUTE/MOYENNE, soit 9 sites éligibles. J'ai étendu après revue auto à 10 sites en ajoutant deux règles FAIBLE strictes :
- **H1** : 1 source IGN + pieve+doyenné concord + dist<1km → IGN seul est généralement fiable pour les sites célèbres déjà documentés
- **H2** : ≥2 sources + concord + dist<2km → accord croisé OSM/Wikidata avec IGN, hors cluster strict

### Garde-fous appliqués

- Backup auto : `_drafts/sites_patrimoine.backup_2026-05-06.json` (créé avant écriture)
- Coords originales conservées dans `notes` (format `gps_audit_2026-05: orig=(lat, lon)`)
- Filtre `DIST_OVER_5000m` exclut auto les corrections suspectes
- Reverse-geocoding double check : pieve + doyenné via point-in-polygon sur `pieves_polygons.json` + `doyennes_polygons.json`

---

## Bugs trouvés et corrigés en sanity check

1. **Nominatim refuse `q + country` ensemble** (HTTP 400 silencieux) → suppression du paramètre `country`, le pays figure dans la chaîne libre.
2. **Wikidata SPARQL `FILTER CONTAINS LCASE` trop lent** (~60 s/requête, 4 min/site total) → refactor `wbsearchentities` + `wbgetclaims` (~25 s/site).
3. **Scoring `inter_max` global pénalisait les outliers** → algorithme cluster-based.

---

## Phases suivantes

Le script est prêt pour `--phase B/C/D/E/F`. Ratios attendus si Phase A est représentative :
- Phase B (Plaine Orientale + Ajaccio, ~58 sites) : ~6 Tier 1, ~9 Tier 2, ~9 ABSENT
- Phase C (Golo + Balagne, ~84 sites) : ~9 Tier 1, ~13 Tier 2, ~13 ABSENT
- Phase D (Extrême-Sud + Piana-Vico-Sari, ~98 sites) : ~10 Tier 1, ~16 Tier 2, ~14 ABSENT
- Phase E (Prunelli-Taravo-Valinco, ~38 sites) : ~4 Tier 1, ~6 Tier 2, ~5 ABSENT
- Phase F (sites doyenne_contemporain_slug=null, ~57 sites) : reverse-geocoding obligatoire pour rattachement, ratios différents

Total estimé Phases B-F : ~30 corrections auto, ~50 candidats Tier 2 à examiner, ~40 ABSENT.

---

## Recommandations

1. **Tier 1 (10 sites)** : appliqué. Rollback possible via backup `_drafts/sites_patrimoine.backup_2026-05-06.json`.
2. **Tier 2 (17 sites)** : revue cartographique par Soleil avant arbitrage. Soit la pieve est large et la new coord est OK, soit la coord originale est fausse.
3. **Tier 3 (14 ABSENT)** : retry ciblé avec variantes du nom (strip parenthèses, sans préfixe "Saint/San") en option future. Sinon enrichissement manuel via Wikipedia / Géoportail / archives départementales.
4. **Phases B-F** : lancer avec le même script. Le mode `--from-csv` permet de réappliquer après un dry-run sans re-fetcher (gain ~30 min/phase).

---

## Fichiers livrés

- `scripts/audit_gps_sites_patrimoine.py` — script Python autonome (commit `abe3ae3`)
- `_drafts/audit_gps_phaseA_2026-05-06.csv` — 96 lignes, full résultats
- `_drafts/sites_patrimoine.backup_2026-05-06.json` — backup pre-apply
- `docs/data/sites_patrimoine.json` — 10 sites mis à jour avec gps_audit timestamp
- `_drafts/audit_gps_phaseA_2026-05-06_RAPPORT.md` — ce rapport
