# Rapport de session — Brief 36 R5 + R6

Date : 2026-05-06
Périmètre Cowork : R5 (37 orphans) + R6 (5 sites en mer + tours côtières).

## R5 — 37 orphans

### Inventaire

22 candidats orphans détectés (sites avec `pieve_geo NONE` OR `doyenne_geo NONE` au reverse-geocoding bulk Brief 35). Le compte Soleil de 37 inclut probablement aussi les sites avec `doyenne_contemporain_slug = null` ou un autre critère prod (62 dans cette catégorie). J'ai retenu la définition la plus stricte : sites hors polygones.

### Méthode

Nearest neighbor par centroïde de polygone (pieve + doyenné) :
- Distance < 5 km au plus proche → assigner `pieve_slug` et `doyenne_contemporain_slug`
- Distance >= 5 km → flag `_orphan_brief35: true` + champs `_orphan_nearest_pieve` et `_orphan_nearest_pieve_dist_km` pour audit Soleil

### Résultats

```
Total candidats        : 22
Assignés (<5km)        :  7
Flaggés orphan (>=5km) : 15
```

**7 assignés :**

| slug | pieve_dist_km | nouveau pieve | nouveau doyenné |
|---|---|---|---|
| couvent_saint_francois_de_pino | 4.88 | (plus proche) | (plus proche) |
| san_giovanni_de_pino | 2.57 | (plus proche) | (plus proche) |
| san_martinu_alando | 3.37 | (plus proche) | (plus proche) |
| sant_andria_sermano_haut | 4.54 | (plus proche) | (plus proche) |
| santa_maria_assunta_ajaccio_bazzicacce | 4.79 | (plus proche) | (plus proche) |
| santa_maria_campile | 3.22 | (plus proche) | (plus proche) |
| tour_de_la_chiappella_rogliano | 4.10 | (plus proche) | (plus proche) |

**15 flaggés orphan résiduels** (probablement Cat. 1 sites en mer ou tours côtières/îlots) :

- castellu_di_bozzi_guitera (16.27 km — site éloigné de tout polygone)
- couvent_sant_antoni_de_calvi (10.42 km — couvent Calvi périphérique)
- menhir_sermano (6.76 km)
- mine_de_magnetite_de_farinole (5.84 km — Cat. 1 site en mer)
- san_giovanni_de_santa_maria_siche (11.17 km)
- san_nicolao_pianello_bozio (5.87 km)
- san_nicolao_sermano (6.76 km)
- santa_maria_carpineto (5.73 km)
- santa_maria_della_neve_grosseto_prugna_basse (7.77 km)
- tour_d_erbalunga_brando (9.14 km — Cat. 1)
- tour_d_omigna_cargese (13.90 km — Cat. 1)
- tour_de_capitello_castelluccio (6.13 km)
- tour_de_capo_di_muro (22.57 km — pointe extrême)
- tour_de_giraglia_ilot (5.37 km — îlot)
- tour_de_turghiu_capo_rosso (10.21 km — pointe Capo Rosso)

Log détaillé : `_drafts/brief_36_r5_orphans_log.csv`.

## R6 — 5 sites en mer + script rescue

### Livrable

`scripts/audit_gps_rescue_mode.py` — script spécialisé avec :
- Cibles hardcodées : 5 sites en mer Brief 36 + 4 tours côtières flaggées orphan R5 (= 9 cibles totales)
- Variantes orthographiques étendues (corse / français / italien) : 4-5 variants par slug
- DIST_MAX_AUTO_M relâché à 8000 m (sites côtiers peuvent être éloignés du centre commune)
- `viewbox` Corse contraint pour éviter les faux positifs continentaux
- Croisement OSM + Wikidata avec validation bbox Corse
- Suppression du flag `_orphan_brief35` si rescue réussit

### Cibles hardcodées (9)

**Cat. 1 sites en mer (5) :**
- tour_d_omigna_cargese
- tour_d_erbalunga_brando
- san_giovanni_de_pino
- tour_de_la_chiappella_rogliano
- mine_de_magnetite_de_farinole

**Bonus tours côtières flaggées R5 (4) :**
- tour_de_giraglia_ilot
- tour_de_capitello_castelluccio
- tour_de_capo_di_muro
- tour_de_turghiu_capo_rosso

### Exécution

Comme pour Brief 34, le sandbox Cowork a un proxy bloqué pour OSM/Wikidata. **Code ou Soleil doit lancer le script en local** :

```
python scripts/audit_gps_rescue_mode.py --dry-run        # rapport CSV seul
python scripts/audit_gps_rescue_mode.py --apply          # backup auto + update JSON
```

Sortie CSV : `_drafts/audit_gps_rescue_{TODAY}.csv` (12 colonnes incluant variant_matched).

Backup : `_drafts/sites_patrimoine.backup_rescue_{TODAY}.json` avant `--apply`.

## Fichiers livrés Cowork

- `scripts/audit_gps_rescue_mode.py` — script rescue R6.
- `docs/data/sites_patrimoine.json` — corrections R5 appliquées (7 orphans assignés, 15 flaggés).
- `_drafts/brief_36_r5_orphans_log.csv` — log détaillé des 22 traitements.

## Statut Brief 36

| Item | Type | Statut |
|---|---|---|
| R4 — Sticker Brief 30 niveau 2 | Code pur | 📤 message Code transmis (vague précédente) |
| R5 — 37 orphans | Cowork | ✅ 22 candidats traités, 7 assignés, 15 flaggés |
| R6 — 5 sites en mer | Cowork prépare + Code/Soleil exécute | ✅ script livré, exécution réseau déléguée |
| R7 — vundefined log | Code pur | 📤 message Code transmis (vague précédente) |

## Prochaine étape

Soleil ou Code lance `audit_gps_rescue_mode.py --apply` en local. Si certains des 15 flaggés résiduels restent sans match, audit Google Earth manuel par Soleil (ou suppression du JSON s'ils sont vraiment fantômes).

## Durée

Session ponctuelle Cowork. Identification orphans + nearest neighbor + script rescue + rapport. ~1h.
