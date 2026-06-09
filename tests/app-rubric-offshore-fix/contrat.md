# CHANTIER — fix catégorisation offshore antennes ANFR

**Date** : 2026-06-09
**AXE** : app
**GÉNÉRATEUR** : Code (Claude Code)
**ÉVALUATEUR** : `tests/blindage-harness/eval-app-rubric.mjs` (sonde stricte état main)

---

## Objectif (1 phrase)

Corriger dans `loadAnt()` la catégorisation offshore antennes — passage du champ legacy `f.commune` (pollué) au champ source de vérité `f.code_insee_commune` — première cible réelle de la boucle gen→eval.

## Dans le périmètre

- `app.html` `loadAnt()` ligne 5104-5140 (rayon contained, voir RAYON_DE_SOUFFLE.md ci-après).
- 4 sites identifiés : SELECT, test offshore, commentaire de doc, log console.
- Vérification que le hook `window.__telluxLayers` reflète bien les compteurs corrects.

## Hors périmètre

- Toute autre amélioration de app.html.
- Modification des zones gelées (EXPERT_WEIGHTS/BOUNDS, calcGammaAmbient, GELE-001, NCRP-001).
- Couches calc* (`calcRF`, `calcAll_v2`, etc.) — non impactées par la catégorisation antennes.
- Toggle légende, drill-down, dashboard conditions (autres sondes).

## Critères d'acceptation

Rubrique §5.1 verbatim. Sonde `probeIsLandFilter` resserrée (état main pré-#825) — exige `onshore > 0 && offshore > 0` via le hook. Le fix doit faire :
- `onshore` passe de 3000 → ~2986
- `offshore` passe de 0 → ~14 (10 Cerbicale + 4 môle Bastia)

## Garde-fou calcul

Confirmer que la reclassification ne déplace AUCUNE valeur du moteur calc*. Spécifiquement :
- `calcRF` n'utilise pas le compteur d'antennes (utilise `CARTORADIO_CERTIFIED` + densité spatiale, pas le SELECT antennas_corse).
- `calcAll_v2` ne dépend pas de `lAnt` (couche Leaflet).
- `nOffshore` / `nOnshore` / `nSeaFiltered` ne sortent QUE vers le hook debug et le label du header → pas dans une formule.

## Garde NULL=OFFSHORE

Les 14 antennes avec `code_insee_commune IS NULL` sont déjà documentées
comme offshore réelles dans `docs/em-mairie/data-sources/antennes_corse_notes.md` §2 :
- 10 antennes à (41.856667, 9.403889) — îles Cerbicale au sud-est de Porto-Vecchio
- 4 antennes à (42.679444, 9.301111) — môle nord port de Bastia

« Ces valeurs NULL sont conformes et n'indiquent pas une régression. »

## Changement visible assumé

- Compteur affiché « X antennes » : 3000 → 2986 (correction visible).
- Couche Leaflet `lAnt` : 14 markers en moins (ces 14 étaient des marqueurs aberrants en mer).
- Aucune valeur du moteur calc* ne change.

## Seuil de réussite

7.0 / 10 pondéré (défaut §5.1).

## Max itérations

3.

## Condition d'escalade

Plateau Δ < 0.3 sur 2 → stop + rapport.

## Cible commit

Branche `feat/fix-offshore-categorization`, PR vers `dev`, **PAS d'auto-merge**.

---

## RAYON_DE_SOUFFLE (grep `f.commune` + logique onshore/offshore)

| Ligne | Code | Action |
|---|---|---|
| 5104 | `select=lat,lon,generation,commune,operateur` | **AJOUTER `code_insee_commune`** |
| 5119 | Commentaire `On utilise desormais le champ commune ...` | **RÉÉCRIRE** (cible code_insee_commune) |
| 5131 | `if(!f.commune){nOffshore++;return;}` | **REMPLACER** par `if(!f.code_insee_commune){...}` |
| 5136 | `info((f.commune||'Corse')+' · '+(f.operateur||'?'))` | **CONSERVER** (string d'affichage du tooltip, pas une catégorisation) |
| 5140 | `'offshore commune-null'` dans le log | **METTRE À JOUR** texte du log |

Autres mentions `commune` dans app.html : `isCommuneRadonL3` (radon, hors scope), `PROD_ELECTRIQUE[].commune` (production électrique, hors scope), `m.commune` (markers patrimoine, hors scope), reverse geocoding (hors scope). Toutes confirmées indépendantes de la catégorisation offshore antennes.

