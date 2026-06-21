# RAPPORT FINAL — rnd-003 · Gating animations JS Leaflet sous `prefers-reduced-motion`

**Date** : 2026-06-21
**Branche** : `claude/rnd-003-leaflet-reduced-motion` · **PR** : #854 (draft) · **Closes** #853
**Statut** : ✅ **Seuil méthodologique atteint — clôture en 1 itération.**

> Boucle R&D solutions-app, axe APP. Générateur ≠ évaluateur (§2), sessions distinctes.
> Score = évaluateur (session fraîche) ; le générateur ne s'auto-note pas.

---

## 1. Verdict

| | |
|---|---|
| **Verdict évaluateur** | ✅ **PASS — 8.00 / 10 pondéré** (seuil 7.0), 2 gates passés |
| Score §5.1 | Fonctionnalité 8 · Non-régression 8 · Craft 8 · Robustesse 8 |
| Artefact scoré | head `13b56c1` (inchangé depuis l'éval) |
| Itérations | 1 / 3 — pas de plateau, pas d'escalade |
| Gates | G1 doctrine PASS (non déclenché) · G2 citations §10 PASS/N-A (non déclenché, 0 coordonnée modifiée) |

Preuves : `feedback-001.md` (même dossier). Comportement prouvé dans **les deux modes** média via Playwright
contre le preview CF de la PR (reduce → options off + pan/setView instantanés ; no-preference → défauts Leaflet,
animations préservées).

## 2. Réponse du générateur à la réserve #2 (non-régression absolue)

L'évaluateur n'a pas pu observer le boot des 9 couches (DNS Supabase injoignable dans son sandbox ; **parité
exacte avec `dev`** prouvée → artefact d'environnement, non imputable). Analyse de **blast-radius** de la diff
(raisonnement générateur, pas une auto-note) :

- Les 5 sites n'ajoutent qu'un drapeau `animate` calculé via `tlxReduceMotion()`. **En mode normal**
  (reduced-motion OFF, cas par défaut + chemin de boot) : `!tlxReduceMotion() === true === défaut Leaflet`, et
  `setView` reçoit `undefined` (= comportement d'origine). La diff est alors un **no-op fonctionnel exact**.
- Les drapeaux d'animation Leaflet sont **orthogonaux** au chargement des données : boot moteur, HTA, antennes
  ANFR, contributions, indice dual dépendent des fetchs Supabase/WMM, **jamais** d'une option `animate`. Aucun
  chemin par lequel ces 5 sites pourraient casser le boot ou fausser un compte de couche.
- **Conclusion** : la non-régression du boot/données est **garantie par construction** ; le run de confirmation
  Supabase-joignable serait une vérification *belt-and-suspenders*, pas un risque ouvert.

**Recommandation maintenue malgré tout** (déférence à l'évaluateur) : avant merge, un coup d'œil au **preview CF
de la PR depuis un réseau normal** (`https://3291c39b.tellux.pages.dev/app` — il bootera les 9 couches hors
sandbox) **ou** un run d'évaluateur en env Supabase-joignable lève la réserve en absolu. Geste de 30 s côté Soleil,
ou tâche d'une session évaluateur à réseau ouvert.

## 3. Réserves résiduelles (hors-scope assumé)

- **R1** : `panTo` (5ᵉ site) prouvé par **identité d'expression**, pas par clic marqueur réel (couches non
  chargées dans le sandbox). Même gating `!tlxReduceMotion()` que les sites observés directement → couverture logique.
- **R2** : non-régression absolue → cf. §2 ci-dessus (garantie par construction + confirmation recommandée).
- **R3 — edge mid-session** (déjà acté au contrat) : `zoomAnimation` lu **à l'init** ; un toggle OS *en cours de
  session* n'affecte que les pans explicites (lus à l'appel), pas le zoom (`_zoomAnimated` figé par Leaflet à l'init).

## 4. Piste craft 9-10 (NON appliquée — discipline §6)

L'évaluateur note qu'un `TLX_RM_QUERY.addEventListener('change', …)` (re-lecture + ré-application des options)
fermerait l'edge R3 et porterait Fonctionnalité/Craft vers 9-10. **Non implémenté** : l'item a **PASS** (8.0 ≥ 7.0)
→ §6 impose l'arrêt (pas d'acharnement), et re-toucher l'artefact scoré imposerait une re-éval. Si Soleil veut le
9-10 + la fermeture d'edge, c'est un **item de suite optionnel** (rnd-005 ?) — priorité basse (toggle OS
mid-session = cas rare).

## 5. Clôture à deux étages

**Étage 1 — méthodo : ATTEINT** (seuil §5.1 + gates passés, 1 itération).
**Étage 2 — intégration : décision Soleil.** PR draft #854 reste ouverte ; merge = arbitrage Soleil
(idéalement après la confirmation env de la réserve #2). L'évaluateur n'a rien mergé/corrigé ; le générateur non plus.

> Note d'intégration : `dev` a avancé (`d29fd9c → 5e8c38f`) pendant le cycle. Vérifier l'absence de conflit
> `app.html` au moment du merge (une autre session a pu toucher dev).

---

*Fin du rapport. Boucle rnd-003 clôturée côté méthodologie. Intégration en attente d'arbitrage Soleil.*
