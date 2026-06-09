# feedback-001 — après génération 1 (fix `loadAnt()`)

**Date** : 2026-06-09
**Évaluateur** : même eval qu'iter 0 (sonde stricte état main pré-#825)
**Cible** : `app.html` avec fix offshore appliqué (4 sites touchés dans `loadAnt()`)

## Verdict global

| Critère | Note | Poids | Contribution |
|---|---|---|---|
| Fonctionnalité | 9/10 | 0.35 | 3.15 |
| Non-régression données | 9/10 | 0.30 | 2.70 |
| Craft / UX | 8/10 | 0.20 | 1.60 |
| Robustesse | 7/10 | 0.15 | 1.05 |
| **Score pondéré** | | | **8.50 / 10** |

**Δ vs feedback-000** : **+0.70** (7.80 → 8.50). Le défaut spécifique flaggé en iter 0 est **résolu** : `filtre_cotier: True`.

## Sondes

| Sonde | iter 0 | iter 1 | Δ |
|---|---|---|---|
| `couches_chargees` | 9/9 | 9/9 | = |
| `indice_dual` | matched | matched | = |
| `toggle_legend` | True | True | = |
| `drill_down` | True | True | = |
| `filtre_cotier` | **False** | **True** | ✅ corrigé |
| `filtre_cotier_method` | commune_filter (hook), ok=false | commune_filter (hook), ok=true | ✅ |
| `dashboard_sections` | 5 | 5 | = |
| `erreurs_console_boot` | 0 | 0 | = |
| `erreurs_console_interact` | 1 | 1 | = (RangeError préexistant, hors scope) |

## Hook `window.__telluxLayers` — vérification post-fix

```json
{
  "antennes_anfr": 2986,
  "antennes_offshore": 14,
  "antennes_sea_filtered": 0
}
```

Total reconstitué : 2 986 + 14 + 0 = **3 000** ✅ (cohérent avec le total Supabase `SELECT count(*) FROM antennas_corse`).

Les 14 offshore correspondent exactement aux groupes documentés dans `docs/em-mairie/data-sources/antennes_corse_notes.md` §2 :
- 10 antennes à (41.856667, 9.403889) — Cerbicale (Bouygues + Free + SFR)
- 4 antennes à (42.679444, 9.301111) — môle nord port de Bastia (Orange)

## Garde-fous post-fix

| Garde-fou | Statut |
|---|---|
| Zones gelées (EXPERT_WEIGHTS_DEFAULT, EXPERT_BOUNDS_DEFAULT, calcGammaAmbient, GELE-001, NCRP-001) | ✅ Intactes — grep diff app.html ne renvoie rien |
| Calc* (calcRF, calcAll_v2, computeExpertComposite) | ✅ Aucune valeur calculée déplacée — la sonde `indice_dual` reste matched, score Non-régression reste à 9/10 |
| Tooltip d'antenne (l.5136) | ✅ Conservé — `f.commune||'Corse'` continue d'afficher le label legacy informatif |
| Bbox safeguard | ✅ Préservé — `if(f.lon<8.30||f.lon>9.65||f.lat<41.35||f.lat>43.03){nSeaFiltered++;return;}` inchangé |
| Compteur header | Modifié `3000 antennes` → `2986 antennes` — visible, intentionnel, correct |
| Couche Leaflet `lAnt` | Modifiée — 14 markers en moins (les marqueurs offshore aberrants sont retirés) |

## Conditions de stop (protocole §6)

- ✅ **Seuil atteint** (8.50 ≥ 7.0)
- ✅ **Défaut cible résolu** (filtre_cotier passe de False à True)
- ✅ **Aucune régression** sur les autres critères

**La boucle clôt en 1 itération de génération.** Max itérations = 3, on a utilisé 1. Pas de plateau.

## Pour `RAPPORT_FINAL.md`

La boucle gen→eval a démontré sa valeur sur une cible réelle :
1. La sonde stricte a flaggé un défaut effectif (`filtre_cotier=False`).
2. Le diagnostic préalable (#825 DIAGNOSTIC_nOffshore.md) avait identifié le bug : `loadAnt()` lit `f.commune` (legacy pollué) au lieu de `f.code_insee_commune` (source de vérité).
3. Le fix borné dans `loadAnt()` (4 sites touchés, contained) a fait passer le check.
4. Iter 1 PASS, boucle clôt.
