# CHANTIER — smoke-test boucle Axe APP

**Date** : 2026-06-09
**AXE** : app
**GÉNÉRATEUR** : Code (Claude Code)
**ÉVALUATEUR** : `tests/blindage-harness/eval-app-rubric.mjs` (session séparée, Playwright headless)

---

## Objectif (1 phrase)

Smoke-test : exercer la boucle générer → évaluer → itérer sur l'axe APP avec un fix borné, et prouver que la boucle clôt (atteint le seuil et s'arrête).

## Dans le périmètre

- Une seule modification app.html ciblée : exposer un hook de debug `window.__telluxLayers` qui publie le compteur de chaque couche du moteur (le protocole §8 le suggère explicitement « facilite énormément les sondes »).
- Faire tourner l'évaluateur AVANT et APRÈS le fix pour mesurer le delta.

## Hors périmètre

- Toute autre amélioration de fond de app.html.
- Modification des zones gelées (GELÉ-001 / NCRP-001 / formules calc*).
- Refonte de l'UX.
- Merge sur main (le smoke reste sur la branche).

## Critères d'acceptation

Rubrique §5.1 du PROTOCOLE_AUTO_ITERATION (verbatim) :

| Critère | Poids |
|---|---|
| Fonctionnalité | 0.35 |
| Non-régression données | 0.30 |
| Craft / UX | 0.20 |
| Robustesse | 0.15 |

Sondes Playwright (verbatim, encodées dans `eval-app-rubric.mjs`) :
1. Boot : 9 couches chargent
2. Indice Tellux dual visible (format Perturbation X/5 · Activité naturelle Y/5)
3. Toggle légende fonctionne
4. Drill-down poupée russe (Brief 47)
5. Filtre côtier (rejet antennes offshore)
6. Dashboard conditions affiche ≥ 4 sections
7. Console : zéro erreur rouge (CORS noise filtrée)

## Seuil de réussite

**7.0 / 10 pondéré** (défaut §5).

## Max itérations

**3** — petite enveloppe car smoke-test, pas vraie campagne.

## Condition d'escalade

- Plateau Δ < 0.3 sur 2 itérations consécutives → stop + rapport.
- Max itérations atteint → stop + rapport.

## Cible commit

Branche `feat/app-rubric-harness` (l'outillage et le smoke-test partagent la branche pour cette pose initiale).
