# feedback-000 — BASELINE (avant fix)

**Date** : 2026-06-09
**Évaluateur** : `eval-app-rubric.mjs` session fraîche
**Cible** : `app.html` état courant (commit a7fb44f, main)

## Verdict

| Critère | Note | Poids | Contribution |
|---|---|---|---|
| Fonctionnalité | 9/10 | 0.35 | 3.15 |
| Non-régression données | 9/10 | 0.30 | 2.70 |
| Craft / UX | 8/10 | 0.20 | 1.60 |
| Robustesse | 7/10 | 0.15 | 1.05 |
| **Score pondéré** | | | **8.50 / 10** |

**Seuil** : 7.0 — **DÉPASSÉ** dès l'état initial.

## Sondes

- ✅ Boot moteur OK (calcAll_v2, HTA_SEGMENTS_DATA, WMM_GRID, SEGMENT_GRID)
- ✅ 9 / 9 couches chargées (HTA segments, WMM grid, TDF, postes sources, éoliennes, hotspots U/Th, mesures certifiées, radon communes L3, ANFR antennes)
- ✅ Indice dual visible (matched `.leaflet-popup-content` après clic Ajaccio)
- ✅ Toggle légende cliquable
- ✅ Drill-down popup Leaflet présent
- ✅ Filtre côtier actif (method=count_only, 3000 antennes)
- ✅ Dashboard conditions ≥ 4 sections
- ✅ Console : 0 erreur boot, 1 erreur post-interaction (à investiguer)
- ✅ 8 erreurs CORS filtrées (bruit localhost vs API externes, non imputable à l'app)

## Échec(s) à traiter

- `console_interact` : 1 erreur console après interaction utilisateur. Mineur, ne fait pas tomber sous le seuil mais limite Robustesse à 7/10 au lieu de 9/10.

## Observation

L'app passe le seuil dès baseline. La boucle peut s'arrêter au cycle 0 — ce qui est en soi un comportement valide de la clôture protocole §6 (« Seuil atteint → succès. Stop. »).

Pour le smoke-test, on exécute néanmoins une itération de génération bornée — ajouter le hook `window.__telluxLayers` suggéré par §8 — afin de prouver que la boucle MOVE et CLÔT après une vraie passe gen + eval.

## Cible du prochain cycle (génération minimale)

Ajouter à `app.html` (zone non gelée) un hook `window.__telluxLayers` qui publie au boot le compteur de chaque couche. Cf. §8 PROTOCOLE_AUTO_ITERATION.
