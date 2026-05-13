# Sprint 3a Phase B — Mapping pieve_slug + commune_insee des 28 tours Cap Corse + Balagne

**Date :** 2026-05-13
**Session :** Cowork
**Statut :** Phase B terminée — diff prêt, **pas de commit ni push effectué** (à reprendre par Claude Code locale)
**Cible :** `docs/data/sites_patrimoine.json`
**Base canonique :** `origin/dev` post-Sprint 3a (commit `1af8c53`, 14 055 lignes)

---

## Décompte final

| Métrique | Avant (origin/dev) | Après Phase B | Δ |
|---|---|---|---|
| Total sites | 500 | 500 | 0 |
| Total tours | 43 | 43 | 0 |
| Tours Sprint 3a sans `pieve_slug` | 28 | **0** | -28 |
| Tours Sprint 3a sans `commune_insee` | 28 | **0** | -28 |
| Tours Phase 1 / Phase 2 latent | 41 / 2 | **40 / 3** | Farinole reclassé P2 |
| Mégalithes | 70 | 70 | 0 (inchangé Sprint 2 Phase B préservé) |
| Diff size | — | 578 lignes patch | +89 / -89 (symétrique) |
| `python -m json.tool` | OK | **OK** | — |

## Mapping appliqué — 28 tours

### Cap Corse — `doyenne_du_cap` (17 tours, 10 communes)

| slug | Commune | INSEE | pieve_slug |
|---|---|---|---|
| tour_de_centuri | Centuri | 2B086 | pieve_pino |
| tour_de_ciocce_pino | Pino | 2B233 | pieve_pino |
| tour_de_farinole | Farinole | 2B109 | pieve_nebbiu |
| tour_de_finocchiarola_rogliano | Rogliano | 2B261 | pieve_rogliano |
| tour_de_fornali_saint_florent | Saint-Florent | 2B298 | pieve_nebbiu |
| tour_de_giottani_barrettali | Barrettali | 2B030 | pieve_canari |
| tour_de_l_osse_cagnano | Cagnano | 2B048 | pieve_brando |
| tour_de_meria | Meria | 2B159 | pieve_luri |
| tour_de_negro_olmeta | Olmeta-di-Capocorso | 2B187 | pieve_nonza |
| tour_de_nonza | Nonza | 2B178 | pieve_nonza |
| tour_de_poggio_ersa | Ersa | 2B107 | pieve_rogliano |
| tour_de_poggio_tomino | Tomino | 2B327 | pieve_rogliano |
| tour_de_scalo_pino | Pino | 2B233 | pieve_pino |
| tour_de_tollare_ersa | Ersa | 2B107 | pieve_rogliano |
| tour_della_parocchia_rogliano | Rogliano | 2B261 | pieve_rogliano |
| tour_di_miomu_santa_maria_lota | Santa-Maria-di-Lota | 2B309 | pieve_brando |
| tour_saint_jean_morsiglia | Morsiglia | 2B170 | pieve_pino |

### Balagne — `doyenne_balagne` (11 tours, 7 communes)

| slug | Commune | INSEE | pieve_slug |
|---|---|---|---|
| torre_mozza_calenzana | Calenzana | 2B049 | pieve_balagne |
| torre_truccia_calenzana | Calenzana | 2B049 | pieve_balagne |
| tour_de_caldanu_lumio | Lumio | 2B150 | pieve_balagne |
| tour_de_galeria | Galéria | 2B121 | pieve_filosorma |
| tour_de_la_pietra_ile_rousse | L'Île-Rousse | 2B134 | pieve_balagne |
| tour_de_losari_belgodere | Belgodère | 2B034 | pieve_balagne |
| tour_de_maraghiu_galeria | Galéria | 2B121 | pieve_filosorma |
| tour_de_saleccia_monticello | Monticello | 2B166 | pieve_balagne |
| tour_de_scalo_ile_rousse | L'Île-Rousse | 2B134 | pieve_balagne |
| tour_de_spano_lumio | Lumio | 2B150 | pieve_balagne |
| tour_du_sel_calvi | Calvi | 2B050 | pieve_balagne |

### Notes par cas non-trivial

- **Galéria (tours 9 + 14)** : `pieve_filosorma` (PAS `pieve_balagne`). La commune est dans le **doyenné** moderne de Balagne mais relève historiquement de la **pieve de Filosorma**. Cohérent avec l'unique site existant `san_paolo_de_galeria` qui utilise `pieve_filosorma`.
- **Cagnano (tour 11)** : `pieve_brando` retenu (frontière historique entre brando-sud et luri-nord ; Casta médiévale rattache majoritairement Cagnano à pieve_brando). Arbitrage Soleil 2026-05-13.
- **Olmeta-di-Capocorso (tour 16)** : `pieve_nonza` retenu (la Tour del Negro est sur la côte ouest → pieve_nonza, pas pieve_nebbiu qui couvre le versant sud).
- **Meria (tour 15)** : `pieve_luri` retenu (Casta rattache Meria à pieve_luri ; ignorer l'attribution `pieve_sorroinsu` présente dans la data pré-existante — erreur géographique, à signaler comme dette).

## Anomalie 1 — Tour de Farinole : reclassement P2 latent (Option A)

Modifications appliquées sur `tour_de_farinole` :

| Champ | Avant | Après |
|---|---|---|
| `phase_publication` | 1 | **2** |
| `precision_coord` | (absent) | `"±2km"` |
| `gps_status` | (absent) | `"centroid_a_preciser"` |
| `gps_audit` | `"2026-05-13_sprint3a_wikipedia_fr"` | `"commune_centroid_2026-05-13"` |
| `notes` | (Sprint 3a) | (Sprint 3a) + mapping + arbitrage Option A 2026-05-13 |
| `lat` / `lon` | 42.7333 / 9.3333 | **inchangés** |
| `commune_insee` | null | 2B109 |
| `pieve_slug` | null | pieve_nebbiu |

Activation Phase 2 → Phase 1 ultérieure conditionnée audit GPS précis via fiche Wikipedia dédiée ou Wikidata. Source MH POP : PA00125391.

## Anomalie 2 — Maison-tour Poggio Ersa PA2B000009 : skip confirmé

Vérification Phase A :
- `tour_de_poggio_ersa` (MH **PA2B000369**, tour génoise XVIe) est **déjà présente** en Sprint 3a (lat 43.005, lon 9.385). Mappée en Phase B.
- **Maison-tour Poggio Ersa** (MH **PA2B000009**, bâti médiéval XVe-XVIe) est un **site distinct** dont le GPS était anomal dans la liste Wikipedia originale.

Décision Soleil 2026-05-13 : **skip Sprint 3a confirmé**. La maison-tour PA2B000009 ne sera pas ajoutée en Phase B. Report en Sprint 3b ou ultérieur avec GPS validé (centroid hameau Poggio ~43.0042/9.3858 si absence d'autre source).

## Dettes pré-existantes (hors périmètre Phase B)

Tours déjà présentes avant Sprint 3a et toujours sans mapping complet (à traiter dans un sprint ultérieur) :

### 6 tours sans `pieve_slug`

| slug | commune_nom |
|---|---|
| tour_d_agnello_cap_corse | (null) |
| tour_d_isolella_sette_navi | (null) |
| tour_de_capo_di_muro | Coti-Chiavari |
| tour_de_giraglia_ilot | (null) |
| tour_de_la_mortella | (null) |
| tour_genoise_chiappa | (null) |

### 8 tours sans `commune_insee`

Les 6 ci-dessus plus :
- `tour_de_capitello_castelluccio` (pieve_ornano présent, INSEE manquant)
- `tour_de_turghiu_capo_rosso` (pieve_vico présent, INSEE manquant)

### Autres dettes signalées (data quality)

- **Meria pieve_sorroinsu erronée** : un site Meria a `pieve_sorroinsu` (pieve géographiquement incompatible — sorroinsu est en région Vico/Sagone, pas Cap Corse). À corriger dans un sprint dédié dette.
- **Olmeta-di-Capocorso pieve_nebbiu vs pieve_nonza** : la base contient les deux pour la même commune. À harmoniser (probablement pieve_nonza pour les sites côtiers, pieve_nebbiu seulement si versant sud).
- **Saint-Florent pieve_balagne** présent : Saint-Florent étant géographiquement en limite Nebbio/Balagne, vérifier que ce site n'est pas mal attribué.

## Vérification post-édition

```
wc -l docs/data/sites_patrimoine.json   →  inchangé (mêmes lignes, modifs intra-lignes uniquement)
python3 -m json.tool                    →  JSON_VALID
diff vs origin/dev                      →  +89 / -89 (symétrique — pas d'ajout/suppression structurel)
Total sites                             →  500 (inchangé)
Tours Sprint 3a sans pieve/INSEE        →  0 / 0 ✓
Mégalithes total                        →  70 (Sprint 2 Phase B préservé) ✓
_meta                                   →  intact ✓
```

## Recommandation commit pour Code locale

**Branche suggérée :** `data/sprint3a-mapping-pieve-insee-2026-05-13`

**Message de commit :**
```
data(patrimoine): Sprint 3a mapping pieve_slug + commune_insee 28 tours

- 28 tours littorales Sprint 3a (Cap Corse 17 + Balagne 11) : pieve_slug
  et commune_insee peuplés depuis référentiel Casta + INSEE COG.
- Anomalie GPS tour_de_farinole arbitrée Soleil Option A : reclassée
  P2 latent avec markers centroid_a_preciser / precision_coord=±2km /
  gps_audit=commune_centroid_2026-05-13. lat/lon inchangés (à affiner
  ultérieurement via Wikipedia ou Wikidata Tour de Farinole).
- Anomalie Maison-tour Poggio Ersa PA2B000009 : skip Sprint 3a
  confirmé Soleil (distinct de tour_de_poggio_ersa PA2B000369 déjà
  présente). Report Sprint 3b ou ultérieur avec GPS validé.

Cas non-triviaux notables :
- Galéria → pieve_filosorma (pas pieve_balagne, historique Filosorma)
- Cagnano → pieve_brando (frontière brando/luri, arbitrage Soleil)
- Olmeta-di-Capocorso → pieve_nonza (côte ouest, pas pieve_nebbiu)
- Meria → pieve_luri (ignorer pieve_sorroinsu erronée pré-existante)

Dettes signalées hors périmètre : 6 tours pré-Sprint 3a sans pieve,
8 sans INSEE, 3 sites avec attribution pieve erronée (à traiter dans
un sprint dédié dette qualité).
```

**Avant push** :
1. `git fetch && git checkout dev && git pull` côté Windows pour partir d'un état canon
2. Appliquer le patch `outputs/mapping_tours/diff.patch` via `git apply` (ou exécuter `outputs/mapping_tours/apply_mapping.py` qui est reproductible)
3. Vérifier `python -m json.tool docs/data/sites_patrimoine.json > /dev/null && echo OK`
4. Vérifier `wc -l docs/data/sites_patrimoine.json` (attendu 14 055)
5. Commit avec message ci-dessus, push sur la branche `data/sprint3a-mapping-pieve-insee-2026-05-13`, PR vers `dev`

## Livrables

- `docs/data/sites_patrimoine.json` (working tree modifié, 89 insertions / 89 suppressions vs origin/dev)
- `outputs/mapping_tours/diff.patch` (578 lignes — diff reproductible exact)
- `outputs/mapping_tours/apply_mapping.py` (119 lignes — script Python reproductible, idempotent)
- `outputs/mapping_tours/restitution.md` (ce fichier)
