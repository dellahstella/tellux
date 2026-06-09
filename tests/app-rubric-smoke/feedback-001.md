# feedback-001 — après génération 1 (fix : ajout `window.__telluxLayers` hook)

**Date** : 2026-06-09
**Évaluateur** : `eval-app-rubric.mjs` session fraîche (sous-process distinct du pas de génération)
**Cible** : `app.html` avec le hook `window.__telluxLayers` ajouté à la fin de `loadAnt()`

---

## Verdict

| Critère | Note | Poids | Contribution |
|---|---|---|---|
| Fonctionnalité | 7/10 | 0.35 | 2.45 |
| Non-régression données | 9/10 | 0.30 | 2.70 |
| Craft / UX | 7/10 | 0.20 | 1.40 |
| Robustesse | 7/10 | 0.15 | 1.05 |
| **Score pondéré** | | | **7.80 / 10** |

**Seuil** : 7.0 — **DÉPASSÉ**. ✅

**Δ vs feedback-000 (baseline)** : −0.70 (8.50 → 7.80)

---

## Sondes

- ✅ Boot moteur OK
- ✅ 9 / 9 couches détectées via le hook `window.__telluxLayers` (HTA, WMM, TDF, postes, éoliennes, hotspots, mesures certifiées, radon L3, antennes ANFR)
- ✅ Indice dual visible (clic Ajaccio → popup avec Perturbation X/5 · Activité naturelle Y/5)
- ✅ Toggle légende cliquable (disclaimer overlay correctement dismissé)
- ✅ Drill-down popup Leaflet présent
- ⚠ Filtre côtier : `method=commune_filter (hook)`, mais `ok=false`
- ✅ Dashboard conditions ≥ 4 sections
- ✅ Console : 0 erreur boot, 1 erreur post-interaction (RangeError préexistant, hors scope smoke)

---

## Analyse de la baisse de score

Avant le fix : la sonde `probeIsLandFilter` retombait sur la méthode `count_only` (lecture du compteur visible dans le header), qui retourne `ok=true` dès que `onshore > 0`. Le hook n'existant pas, ce fallback validait largement.

Après le fix : la sonde lit `window.__telluxLayers.antennes_anfr` ET `window.__telluxLayers.antennes_offshore` (méthode `commune_filter (hook)`). La condition d'acceptation devient `onshore > 0 && offshore > 0`. Dans les données Supabase actuelles, `nOffshore = 0` (aucune antenne avec `commune` null — la cleanup du dataset semble avoir réassigné les 14 anciennes offshore). Donc `ok=false`.

**Cette baisse est un signal réel** — l'eval est devenue plus précise avec le hook et a révélé que le mécanisme de filtrage offshore est en place mais n'a rien à filtrer dans le dataset courant. La rubrique §5.1 dit « Le filtre côtier rejette bien les antennes en mer » — mais s'il n'y a pas d'antennes en mer dans le dataset, le filtre ne peut pas démontrer son action.

Deux lectures possibles :
1. **Pragmatique** : le mécanisme existe (compteur câblé, hook expose les bonnes données), donc considérer `ok=true` dès lors que la mécanique est en place — ce qui demanderait un ajustement de la sonde côté évaluateur (non fait en cours de boucle, principe de stabilité de l'eval).
2. **Stricte** : la sonde a raison de demander un offshore observable > 0. Le fix attendu côté générateur est soit (a) restaurer une antenne offshore-volontaire dans le dataset, soit (b) flagger explicitement dans le hook que le filtre est inactif faute de matière.

Score reste **au-dessus du seuil** : pas de blocage. La régression est signalée pour information.

---

## Conditions de stop (protocole §6)

- ✅ **Seuil atteint** (7.80 ≥ 7.0). La boucle clôt.

Pas de cycle 2 nécessaire. Conformément à `contrat.md`, la boucle s'arrête ici (anti-sur-itération).

---

## Pour `RAPPORT_FINAL.md`

Le smoke-test démontre que la boucle gen→eval clôt correctement :
- iter 0 baseline = 8.50 (déjà au-dessus du seuil → clôture aurait pu être immédiate)
- iter 1 après un fix borné (ajout du hook §8) = 7.80 (toujours au-dessus du seuil → clôture)
- Δ négatif assumé : l'eval est devenue plus précise avec le hook ; régression signalée pour suivi.
- Pas de boucle infinie, pas de sur-itération.
