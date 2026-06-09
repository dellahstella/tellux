# feedback-000 — BASELINE (avant fix)

**Date** : 2026-06-09
**Évaluateur** : `eval-app-rubric.mjs` (sonde stricte état main pré-#825 — `ok: onshore > 0 && offshore > 0`)
**Cible** : `app.html` état courant (origin/main `b2d0a32`)

## Verdict global

| Critère | Note | Poids | Contribution |
|---|---|---|---|
| Fonctionnalité | 7/10 | 0.35 | 2.45 |
| Non-régression données | 9/10 | 0.30 | 2.70 |
| Craft / UX | 8/10 | 0.20 | 1.60 |
| Robustesse | 7/10 | 0.15 | 1.05 |
| **Score pondéré** | | | **7.80 / 10** |

**Seuil** : 7.0 — atteint au global, **mais le défaut spécifique est bien remonté** par le check `filtre_cotier` (l'eval fait son travail).

## Détail du fail

```
filtre_cotier : False
filtre_cotier_method : commune_filter (hook)
fail detail : filtre offshore : method=commune_filter (hook), ok=false
```

La sonde lit `window.__telluxLayers.antennes_offshore = 0`. Le hook est en place mais la valeur reflète le bug latent de `loadAnt()` : test `!f.commune` au lieu de `!f.code_insee_commune`. Le champ `commune` est rempli pour les 3 000 antennes (legacy, pollué) → `nOffshore` reste à 0.

## Cible du prochain cycle

Appliquer le fix borné identifié dans `contrat.md` (4 sites dans `loadAnt()` lignes 5104-5140 — SELECT, commentaire, test offshore, log console). Préserver le champ legacy `commune` dans le SELECT pour le label du tooltip.

## Prédiction (à vérifier en iter 1)

- `filtre_cotier: True` (mécanisme actif + offshore observable > 0)
- `ANFR_antennes: 3000 → 2986` (14 reclassées offshore)
- `antennes_offshore: 0 → 14` (10 Cerbicale + 4 môle Bastia, doc-confirmées)
- Score : ~7.8 → ~8.5 (gain ≈ 0.7 sur Fonctionnalité)
- Pas de changement sur les calc* (garde-fou calcul : `nOffshore`/`nOnshore` ne sortent que vers le hook debug et le label header)
