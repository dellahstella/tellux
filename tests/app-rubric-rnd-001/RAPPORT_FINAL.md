# RAPPORT FINAL — rnd-001 · Accessibilité `prefers-reduced-motion` (app.html)

**Date** : 2026-06-21
**Branche** : `claude/rnd-001-reduced-motion` · **PR** : #852 (draft)
**Statut** : ✅ **Seuil méthodologique atteint — clôture en 1 itération.**

> Premier item réel de la boucle R&D solutions-app (axe APP). Boucle générateur ≠ évaluateur (§2),
> sessions distinctes. Le score provient de l'**évaluateur** (session fraîche) ; le générateur ne s'auto-note pas.

---

## 1. Verdict

| | |
|---|---|
| **Verdict évaluateur** | ✅ **PASS — 8.73 / 10 pondéré** (seuil 7.0), 2 gates éliminatoires passés |
| **Artefact scoré** | head `0531ab3` (inchangé depuis l'éval) |
| **Itérations** | 1 / 3 — pas de plateau, pas d'escalade |
| **Gate G1 doctrine** | PASS (non déclenché — CSS de présentation, 0 contenu/mission EM) |
| **Gate G2 citations §10** | PASS (non déclenché — `citations_registry.json` non touché par la branche, vérifié `git diff dev..branch`) |

Détail des preuves : `feedback-001.md` (même dossier).

## 2. Score §5.1 (reporté de l'évaluateur)

| Critère | Poids | Note | Pondéré |
|---|---|---|---|
| Fonctionnalité | 0.35 | 8.5 | 2.975 |
| Non-régression données | 0.30 | 9.5 | 2.85 |
| Craft / UX | 0.20 | 8.5 | 1.70 |
| Robustesse | 0.15 | 8.0 | 1.20 |
| **TOTAL** | | | **8.73** |

Non-régression **prouvée deux fois** : (a) mode `no-preference` → durées d'origine intactes ;
(b) parité harness canonique `eval-app-rubric.mjs` candidat ≡ `main` (Δ=0, y compris le `RangeError`
pré-existant → non imputable).

## 3. Ce qui a été livré

| Fichier | Rôle |
|---|---|
| `app.html` (+12) | bloc `@media (prefers-reduced-motion: reduce)` additif (head `0531ab3`) |
| `tests/app-rubric-rnd-001/contrat.md` | contrat d'itération + critères falsifiables (gate-puis-score) |
| `tests/app-rubric-rnd-001/feedback-001.md` | verdict évaluateur (session fraîche) |
| `tests/app-rubric-rnd-001/RAPPORT_FINAL.md` | le présent rapport |

## 4. Reste hors-scope (assumé — single-concern respecté)

- **F1 → candidat rnd-003 (à curer par Soleil, file FEDER-first).** L'auto-pan Leaflet **JS**
  `map.panBy(…, {animate:true, duration:0.3})` à `app.html:5091` reste animé sous `prefers-reduced-motion` :
  un fix **CSS-only ne neutralise pas les animations JS** de Leaflet. Fermeture propre = lire
  `matchMedia('(prefers-reduced-motion: reduce)').matches` et passer `{animate:false}`. Impact WCAG 2.3.3
  faible (pan one-shot 0.3 s, pas décoratif continu). **Non créé d'office** : la file R&D est curée par Soleil.
- **F2 (nit, non corrigé volontairement).** Le commentaire `app.html:1174` évoque des listeners
  `transitionend` absents *en propre* ; l'évaluateur confirme que le choix `0.01ms`≠0 reste **correct**
  (bénéficiaire réel = cleanup zoom interne Leaflet). Re-toucher l'artefact scoré pour un commentaire exact
  ne le justifie pas ; à reformuler si rnd-003 ré-ouvre cette zone.

## 5. Clôture à deux étages (rappel brief)

**Étage 1 — méthodo : ATTEINT** (seuil §5.1 + gates passés).
**Étage 2 — intégration : décision Soleil.** La PR draft #852 **reste ouverte** ; passage *ready* et **merge =
arbitrage Soleil** (pas d'auto-merge, pas de déploiement, conformément au brief). L'évaluateur n'a rien mergé,
rien corrigé ; le générateur ne merge pas non plus.

---

*Fin du rapport. Boucle rnd-001 clôturée côté méthodologie. Intégration en attente d'arbitrage Soleil.*
