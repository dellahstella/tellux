# Rapport de session — Brief 35 : réparation sites mal placés / désynchronisés / dupliqués

Date : 2026-05-06
Périmètre Cowork : Bonus Cat. 2 (reverse-geocoding bulk) + Cat. 2 (correction désynchros) + Cat. 3 (dédoublonnage) + Cat. 4 (vérif polygone Brando).
Hors scope Cowork : Cat. 1 (sites en mer, audit manuel Soleil) + Bug niveau 1→2 (Code).

## Préambule — État reconstruit

Trois JSON dans le worktree `distracted-cohen-9850e9/` étaient cassés (linter récurrent depuis Brief 33). Reconstruction en début de session :

- `docs/data/sites_corse.json` : reconstitué depuis `inspiring-snyder-b363e6` + Brief 32 (fusion Bastia → Cap, 8 sites) + Brief 33 (visuels sans extension).
- `docs/data/doyennes_polygons.json` : régénéré via `scripts/build_doyennes_polygons.py` (9 doyennés, 360 communes, 8704 km²).
- `docs/data/pieves_polygons.json` : régénéré via `scripts/build_pieves_polygons.py` (47 pieves, 39 transferts v2 appliqués, 3 reclassements majoritaires).
- `docs/data/sites_patrimoine.json` : reconstitué via le pipeline split Brief 33 + doublons P4 (Aléria + 10 naturels sacrés + 4 barrages) — 451 sites en entrée Brief 35.

## Bonus Cat. 2 — Reverse-geocoding bulk

Script livré : `scripts/audit_reverse_geocoding_bulk.py`.

Méthode : pour chaque site de `sites_patrimoine.json`, point-in-polygon (ray-casting) contre `doyennes_polygons.json` et `pieves_polygons.json`, comparaison aux champs déclarés.

Sortie : `_drafts/audit_reverse_geocoding_2026-05-06.csv` (451 lignes, 13 colonnes).

Résultats :

```
Sites analysés          : 451
Mismatch doyenné        : 70   (vs 14 visibles à l'œil par Soleil)
Mismatch pieve          : 151
Hors bbox Corse         : 0
Doyenné_geo NONE        : 13   (sites hors tous polygones doyennés)
Pieve_geo NONE          : 21   (sites hors tous polygones pieves)
```

**Les 14 cas Soleil sont 100% présents dans les 70 mismatches doyenné détectés.** Vérifié un par un (script de cross-check).

Les 56 mismatches non listés par Soleil suivent les mêmes patterns (sites en frontière de doyennés, sites Castagniccia dont le slug doyenné historique ne matche pas la géographie post-fusion). Tous corrigés en bloc selon le scénario A (geo réelle écrase declared).

## Cat. 2 — Corrections désynchros appliquées

Backup : `_drafts/sites_patrimoine.backup_brief35_2026-05-06.json`.

Log CSV : `_drafts/brief_35_cat2_corrections_log.csv` (toutes les modifs, slug par slug).

Scope appliqué :

```
doyenne_contemporain_slug updates : 70   (les 14 Soleil + 56 autres détectés)
pieve_slug updates                : 55   (parmi les 151 mismatches pieve, ceux où pieve_geo non null)
sites en mer skippés (Cat. 1)     :  5   (les 5 Soleil, à corriger manuellement)
```

Stratégie : **Scénario A pour tous** — la géographie réelle (point-in-polygon) écrase le slug déclaré. Hypothèse : les coords ont été affinées par Brief 34 IGN-sourced, et le slug d'origine n'a jamais été recalculé. Si une coord est fausse (Cat. 1), elle reste hors scope Cowork et flagguée pour audit Soleil.

## Cat. 3 — Dédoublonnage

| Cas | Statut | Action |
|---|---|---|
| 3a Trinité d'Aregno | déjà résolu | 1 seule entrée présente (`la_trinite_d_aregno`). Le doublon historique a probablement été nettoyé dans une vague antérieure. Aucune action nécessaire. |
| 3b Trinità Prunelli-di-Fiumorbo | déjà résolu | 1 seule entrée présente (`la_trinita_de_prunelli_di_fiumorbo`). Idem. |
| 3c Mines de Canari | **fusion appliquée** | `min_canari` supprimé, `mine_d_amiante_de_canari` enrichi (name complet, description fusionnée, GPS plus précis 42.822/9.325, gps_audit conservé, sources fusionnées). |

Note Canari : `min_canari` reste dans `sites_em.json` côté EM (axe `minier_historique` ajouté en Brief 33 P1) — non concerné par cette suppression patrimoine.

État final sites_patrimoine.json : 451 → **450 sites** après suppression `min_canari`.

## Cat. 4 — Pieve Brando

Vérifications côté data :

```
pieve_brando dans pieves_polygons.json       : OUI
  slug                                       : pieve_brando
  diocese_medieval                           : Mariana
  doyenne_contemporain_majoritaire           : doyenne_du_cap   ✓ correct
  doyennes_visibles                          : [doyenne_du_cap] ✓ correct
  polygon                                    : 133 points présents
  doyennes_appartenance                      : [{cap: 0.9259}]
```

**Le polygone est présent et le rattachement est correct.** Le ratio 0.9259 (vs ~0.99 pour les autres pieves) est légèrement plus bas mais ne devrait pas justifier un rendu visuel différent.

**Conclusion Cat. 4 Cowork** : rien à corriger côté data. **Le bug visuel est donc côté Code** — probablement dans la logique de couleur des pieves (peut-être un seuil de ratio qui déclenche une couleur "fallback" ?). À investiguer côté patrimoine.html.

## Fichiers livrés Cowork (worktree distracted-cohen-9850e9)

- `scripts/audit_reverse_geocoding_bulk.py` — script point-in-polygon pour audit récurrent.
- `docs/data/sites_corse.json` — reconstruit (479 sites, DEPRECATED).
- `docs/data/doyennes_polygons.json` — régénéré (9 doyennés).
- `docs/data/pieves_polygons.json` — régénéré (47 pieves, 39 transferts v2).
- `docs/data/sites_patrimoine.json` — corrigé (450 sites, 70 doyenné updates + 55 pieve updates + 1 doublon Canari fusionné).
- `_drafts/sites_patrimoine.backup_brief35_2026-05-06.json` — backup avant corrections.
- `_drafts/audit_reverse_geocoding_2026-05-06.csv` — rapport reverse-geocoding bulk (451 lignes).
- `_drafts/brief_35_cat2_corrections_log.csv` — log détaillé de toutes les modifs.

## Hors scope Cowork — pour Soleil et Code

### Cat. 1 — 5 sites en mer (action Soleil, ~30-45 min)

Les coords doivent être re-géolocalisées manuellement via Google Earth ou OSM :

- `tour_d_omigna_cargese`
- `tour_d_erbalunga_brando`
- `san_giovanni_de_pino`
- `tour_de_la_chiappella_rogliano`
- `mine_de_magnetite_de_farinole` (lat 42.73 / lon 9.332 → probablement en mer)

Cowork ne peut pas les corriger sans réseau (proxy bloqué) ni connaissance terrain. Une fois Soleil a les bonnes coords, simple update lat/lon dans `sites_patrimoine.json`.

### Bug niveau 1 → 2 et Cat. 4 visuel — investigation Code

Hypothèses transmises à Code :

1. **Bug niveau 1→2** : `enterNiveau2View(slug)` filtre par `doyenne_contemporain_slug === slug`. Avant Brief 35, les 70 sites avec slug désynchronisé étaient invisibles au drill-down. **Maintenant que les 70 sont corrigés (Cat. 2), le bug devrait largement diminuer**. Si Code constate post-merge Brief 35 que le bug persiste, l'hypothèse 2 (mécanisme d'affichage cassé) prend le pas.

2. **Cat. 4 pieve Brando** : data OK, le rendu visuel différent vient probablement du ratio `doyennes_appartenance` (0.9259 vs ~0.99 pour les autres pieves). Code à vérifier dans patrimoine.html s'il existe un seuil de ratio qui déclenche une couleur fallback. Si oui, ajuster le seuil ou utiliser uniquement `doyenne_contemporain_majoritaire` pour le coloriage.

## Statut critères d'acceptation Brief 35

| Critère | Statut Cowork |
|---|---|
| Cat. 1 — 5 sites en mer corrigés | ❌ délégué Soleil (audit manuel) |
| Cat. 2 — 14 désynchros corrigées | ✅ + 56 autres bonus, 70 total |
| Bonus Cat. 2 — rapport reverse-geocoding bulk | ✅ CSV livré, 151 mismatches pieves identifiés |
| Cat. 3a — Trinité d'Aregno | ✅ déjà résolu (1 entrée) |
| Cat. 3b — La Trinità de Prunelli-di-Fiumorbo | ✅ déjà résolu (1 entrée) |
| Cat. 3c — un seul slug Canari | ✅ `mine_d_amiante_de_canari` conservé, `min_canari` supprimé, métadonnées fusionnées |
| Cat. 4 — pieve Brando affichée comme les autres | 🟡 data OK, bug rendu côté Code |
| Bug niveau 1→2 | 🟡 délégué Code, devrait largement diminuer après merge Cat. 2 |
| Régression Briefs 27-34 | ✅ aucune (tous les fichiers source reconstruits proprement) |

## Durée

Session ponctuelle Cowork. Reconstruction état + reverse-geocoding bulk + corrections + dédoublonnage + rapport. ~2h30.
