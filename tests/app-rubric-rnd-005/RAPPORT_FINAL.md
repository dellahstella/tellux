# RAPPORT FINAL — rnd-005 · Réactivité mid-session de `prefers-reduced-motion`

**Date** : 2026-06-21
**Branche** : `claude/rnd-005-reduced-motion-reactive` · **PR** : #858 (draft) · **Closes** #857
**Statut** : ✅ **Seuil méthodologique atteint — clôture en 1 itération.**

> Boucle R&D solutions-app, axe APP. Générateur ≠ évaluateur (§2). Score = évaluateur (session fraîche).

---

## 1. Verdict

| | |
|---|---|
| **Verdict évaluateur** | ✅ **PASS — 8.55 / 10 pondéré** (seuil 7.0), 2 gates passés |
| Score §5.1 | Fonctionnalité 9 · Non-régression 8 · Craft 9 · Robustesse 8 |
| Artefact scoré | head `e33b2bc` (inchangé depuis l'éval) |
| Itérations | 1 / 3 — pas de plateau, pas d'escalade |
| Gates | G1 doctrine PASS (non déclenché) · G2 citations §10 PASS/N-A (non déclenché, 0 coordonnée) |

**rnd-005 ferme la réserve #3 de rnd-003** : le helper `TLX_RM_QUERY` n'était pas écouté. Évolution
8.0 (rnd-003) → 8.55, gap comblé avec le pattern idiomatique `addEventListener('change')`.

## 2. Preuves (évaluateur, Playwright, `emulateMedia` après boot, vs base `dev`)

- **OFF→ON** et **ON→OFF** : `map.options.{zoom,fade,markerZoom}Animation` **et** `map._zoomAnimated` rebasculent
  dans les deux sens ; pan post-changement (non-)animé en conséquence.
- **Non-régression boot** : boot de rnd-005 **byte-identique au boot de `dev`** dans les deux modes ; le listener
  est **no-op au boot** (n'agit qu'au `change`). Le gap corrigé est visible : sur `dev`, après changement OS, les
  options carte restaient figées.
- **CI** : `validate-code` vert ; `Cloudflare Pages` vert ; **`Eval Playwright Axe APP §5.1 (informatif)` vert**
  (env CI réseau-activé, Supabase joignable) — corrobore que l'app boote et que le harness s'exécute sans crash
  là où les couches data chargent. `Workers Builds` rouge = **pré-existant** (#852/#854), non imputable.

## 3. Réserves résiduelles (hors-scope, non bloquantes)

- **R1 — non-régression absolue** : les 9 couches/indice dual ne sont pas observés *par l'évaluateur* (DNS Supabase
  bloqué dans son sandbox). Mais boot byte-identique à `dev` + listener no-op au boot ⇒ rnd-005 **ne peut pas**
  toucher le chargement data ; **corroboré** par le check CI informatif vert (réseau-activé). Confiance haute.
  → Réserve #2 héritée de rnd-003 désormais **largement levée** côté donnée (le harness CI boote en env réseau).
- **R2 — geste de zoom non rendu** : l'évaluateur a validé l'**état-levier** (`map.options.*Animation` +
  `map._zoomAnimated`) que Leaflet lit au zoom, sans déclencher un zoom visuel. Le contrat ne le demandait pas.

## 4. Simplification connue (NON corrigée — discipline §6)

Le resync `map._zoomAnimated = !rm && !!L.Browser.any3d` **omet** les facteurs `TRANSITION` et `!mobileOpera`
de la formule interne Leaflet. **Immatériel** (constat évaluateur) : `TRANSITION` est un const privé non exposé
par `L.Browser` (inatteignable proprement depuis app.html), `mobileOpera` est obsolète, et `any3d` est le facteur
contraignant. Le seul écart théorique (`any3d===true` ∧ `TRANSITION===false`) n'existe pas sur les navigateurs
actuels. C'est l'unique raison du 9-et-non-10 sur Fonctionnalité/Craft. **Non corrigé** : item PASS → §6 impose
l'arrêt ; re-toucher l'artefact scoré imposerait une re-éval pour un gain nul en pratique.

## 5. Clôture à deux étages

**Étage 1 — méthodo : ATTEINT** (8.55 ≥ 7.0 + gates, 1 itération).
**Étage 2 — intégration : décision Soleil.** PR draft #858 reste ouverte ; merge = arbitrage Soleil.
L'évaluateur n'a rien mergé/corrigé ; le générateur non plus.

> Note d'intégration : vérifier l'absence de conflit `app.html` au merge (`dev` peut avoir avancé — plusieurs
> sessions actives). rnd-005 dépend de rnd-003, déjà dans `dev`.

---

*Fin du rapport. Boucle rnd-005 clôturée côté méthodologie. Intégration en attente d'arbitrage Soleil.*
