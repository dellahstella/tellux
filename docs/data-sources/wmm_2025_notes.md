# WMM 2025 — grille précalculée Corse

**Fichier :** `public/data/wmm_2025_grid_corse.json`
**Script de génération :** `scripts/generate_wmm_grid_corse.py`
**Date de génération :** 2026-04-21
**Modèle :** WMM 2025 (World Magnetic Model)
**Source :** NOAA/BGS, coefficients publics domaine public

## Méthodologie

Grille précalculée **offline** via Python + `pygeomag` (bundled WMM 2025 coefficients). Évite :
- Parser le format `.COF` côté navigateur
- Implémenter les harmoniques sphériques WMM en JS (~200 lignes, dépendance supplémentaire)
- Ajouter une lib CDN externe

Voie cohérente avec l'approche IGRF existante (`IGRF14_GRID` interpolée par IDW).

### Spec grille

- **Couverture** : Corse (41.3–43.1 N, 8.5–9.6 E)
- **Résolution** : 0.05° × 0.05° (~5.5 km × 4.1 km à 42°N)
- **Altitude** : 0 km (référence niveau mer)
- **Date de référence** : date de génération, en année décimale
- **851 points**, fichier **124 KB**

### Exemples (2026-04, niveau mer)

| Point | Lat | Lon | F (nT) | D (°) | I (°) |
|-------|-----|-----|--------|-------|-------|
| Ajaccio | 41.95 | 8.75 | 46 633 | 3.39 | 58.03 |
| Bastia | 42.70 | 9.45 | 46 951 | 3.55 | 58.92 |
| Monte Cinto | 42.40 | 8.95 | 46 807 | 3.45 | 58.55 |

Gamme Corse : F ∈ [46 380, 47 100] nT, gradient ~700 nT N-S.

## Usage Tellux

**Cross-check IGRF-14 vs WMM 2025** dans la modale Mode Expertise.

Au clic carte :
1. `igrfFallback(lat, lon)` → valeur IGRF-14 interpolée
2. `calcMagneticWMM(lat, lon)` → valeur WMM 2025 interpolée bilinéaire
3. Affichage `|Δ|` = `|IGRF − WMM|` dans le panneau Expert

### Code couleur

- `Δ < 100 nT` : blanc Pierre (convergence normale)
- `100 nT ≤ Δ < 500 nT` : Ocre (alerte modérée)
- `Δ ≥ 500 nT` : Porphyre clair (divergence significative — investigation recommandée)

Un tooltip au survol affiche IGRF, WMM et l'écart détaillé.

## Limitations

IGRF-14 et WMM 2025 sont deux modèles globaux du champ magnétique principal (noyau terrestre). Un écart important indique :

- **Zone peu dense en observations** (mer, haute montagne)
- **Anomalies crustales non modélisées** — traitées séparément par EMAG2v3
- **Divergence fin de cycle** — les modèles sont ajustés tous les 5 ans

Ces modèles ne couvrent **pas** :
- Les variations temporelles (Kp, Dst, Sq) — calculées séparément par Tellux
- Les anomalies locales < 10 km (granit, gabbro, skarn)
- Les variations journalières ionosphériques

## Régénération

À exécuter tous les 1–2 ans, ou à la sortie du modèle suivant (**WMM 2030**) :

```bash
pip install pygeomag  # si nouvelle version disponible
python3 scripts/generate_wmm_grid_corse.py
git add public/data/wmm_2025_grid_corse.json scripts/generate_wmm_grid_corse.py
git commit -m "chore: regenerate WMM grid"
```

Le script est idempotent, bornes et résolution codées en constantes.

## GELE-001

Cette grille est un **outil de cross-check**, pas une composante du modèle composite. Les pondérations `w_M = 0.40, w_RF = 0.40, w_I = 0.20` restent inchangées.

## Licence

WMM 2025 coefficients : **domaine public** NOAA/BGS (17 U.S.C. 403).
