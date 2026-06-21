# FEEDBACK-001 — Évaluation rnd-003 (gating animations JS Leaflet · `prefers-reduced-motion`)

> Session **ÉVALUATEUR** fraîche (§2). Critique uniquement — **rien corrigé**.
> Cible : PR #854, branche `claude/rnd-003-leaflet-reduced-motion` @ `13b56c1`.
> Méthode : Playwright headless (chromium-1223, pw 1.60.0) contre le **preview Cloudflare Pages de la PR**
> (`https://3291c39b.tellux.pages.dev/app`, épinglé sur le commit head). Prod jamais touchée (D-2).
> Rubrique : `_drafts/RND_RUBRIQUE_TELLUX.md` (gate-puis-score, D-4).

---

## VERDICT GLOBAL : ✅ PASS — score pondéré **8.0 / 10** (seuil 7.0), gates PASS. Itération 1/3.

Per §6 : seuil atteint **et** gates PASS → **SUCCÈS**. La PR draft reste ouverte ; **merge = Soleil**.
Pas d'itération générateur requise. Réserves de vérification ci-dessous (non bloquantes, à lever par Soleil avant merge).

---

## COUCHE 1 — GATES ÉLIMINATOIRES

| Gate | Verdict | Justification |
|---|---|---|
| **G1 — doctrine** | ✅ **PASS (non-déclenché)** | Le diff n'ajoute que des drapeaux `animate` Leaflet + un helper `matchMedia`. Aucun contenu scientifique/mission EM, aucun bénéfice EM affirmé, aucun retour-terrain-comme-preuve, aucun mysticisme. Rien à gater. |
| **G2 — citations §10** | ✅ **PASS / N-A (non-déclenché)** | Aucune référence/corpus/CHURCHES/SITES/DOI/hypothèse ajoutée ou éditée. **Aucune coordonnée modifiée** (vérifié sur le diff : seul un champ `animate` est ajouté à 5 sites). `verify_citation.py` non requis. |

Gates PASS → on score §5.1.

---

## COUCHE 2 — SCORE §5.1

| Critère | Poids | Note | Pondéré | Raison de la note |
|---|---|---|---|---|
| **Fonctionnalité** | 0.35 | **8** | 2.80 | Les 2 modes marchent, prouvés par sondes falsifiables (cf. preuves). −1 (pas 9) : `panTo` non exercé par clic réel + edge mid-session ouvert. |
| **Non-régression données** | 0.30 | **8** | 2.40 | **Parité exacte avec `dev`** (cf. contrôle) + no-op-par-construction en `no-preference`. −1 (pas 9) : vérification absolue des 9 couches **bloquée par l'environnement** (DNS Supabase), pas d'observation directe de l'indice dual recalculé ici. |
| **Craft / UX** | 0.20 | **8** | 1.60 | Helper propre, gardé (`typeof window`/`matchMedia`), commenté, single-concern ; `setView` passe `undefined` en mode normal (no-op exact). −1 (pas 9) : ne s'abonne pas à l'événement `change` du `MediaQueryList`. |
| **Robustesse** | 0.15 | **8** | 1.20 | Zéro erreur console **imputable à rnd-003** ; pas d'init redondant (helper + map init une seule fois). −1 (pas 9) : console non observable « propre » dans ce sandbox (bruit env identique sur dev). |
| **Σ pondéré** | | | **8.00** | `threshold_met = true` (≥ 7.0) |

> Note anti-laxisme (§rubrique) : le PASS **n'est pas** un blanc-seing. Chaque axe est tenu à **8 et non 9**,
> sur des manques nommés et falsifiables ; la non-régression est un verdict **relatif (parité)**, pas une
> observation absolue ; aucun axe n'atteint 9-10. La rubrique a discriminé. Le changement est simplement
> petit, bien cadré et correct — PASS **mérité**, sur preuve comportementale dans les deux modes média.

---

## PREUVES FALSIFIABLES (Playwright, `emulateMedia` via `newContext({reducedMotion})`)

### Check 1 — `reducedMotion: 'reduce'` → ✅ PASS
Au boot :
```
map.options.zoomAnimation        = false
map.options.fadeAnimation        = false
map.options.markerZoomAnimation  = false
tlxReduceMotion()                = true
matchMedia('(prefers-reduced-motion: reduce)').matches = true
map._zoomAnimated (interne)      = false
```
Comportement de pan (expression **exacte** du diff `!tlxReduceMotion()` appliquée à un `panBy` live) :
- `animateFlag = false` ; centre déplacé **instantanément** (Δlat −0.987 dès l'appel, `movedInstantly = true`).

Chemin **réel** deep-link `setView` (1 des 5 sites), via `applyHashToMap()` avec `#/c=41.9200,8.7400&z=12` :
- `reachedTargetInstantly = true` : zoom 8→**12** et lat→**41.92** **immédiatement après** l'appel, pas de transition.

### Check 2 — `reducedMotion: 'no-preference'` (non-régression) → ✅ PASS
Au boot :
```
map.options.zoomAnimation/fadeAnimation/markerZoomAnimation = true  (défauts Leaflet)
tlxReduceMotion()                = false
matchMedia(...).matches          = false
map._zoomAnimated (interne)      = true
```
Comportement de pan :
- `animateFlag = true` ; le centre **n'a pas bougé** à l'instant de l'appel (Δlat 0, `movedInstantly = false`) puis se stabilise après animation (Δlat −0.282 à +700 ms) → **animation engagée**.

Chemin deep-link `setView` :
- `reachedTargetInstantly = false` : zoom encore **8** et lat inchangée juste après l'appel, cible atteinte **après** la transition (endZoom 12 / endLat 41.92) → animation préservée.

→ **Le comportement par défaut est strictement inchangé** hors reduced-motion. Invariant non-régression du contrat confirmé empiriquement.

### Check 3 — Non-régression moteur → ✅ par **PARITÉ** (vérification absolue bloquée par l'env)
`tests/blindage-harness/eval-app-rubric.mjs` lancé comme outil, **même sandbox**, sur les deux branches :

| Signal | rnd-003 (`3291c39b`) | base `dev` (`dev.tellux.pages.dev`) |
|---|---|---|
| `booted` | false | false |
| `score_pondere` harness | 4.5 | 4.5 |
| couches chargées | 0/9 | 0/9 |
| erreurs console boot | 6 | 6 |
| erreurs console interact | 1 | 1 |
| set de fails | boot, couches, filtre_cotier, console_boot, console_interact | **identique** |

**Cause = environnement, pas rnd-003** : `net::ERR_NAME_NOT_RESOLVED` sur `knckulwghgfrxmbweada.supabase.co`
(le sandbox ne résout pas le DNS Supabase). HTA, antennes ANFR et contributions chargent **toutes** via Supabase →
le moteur ne boote pas → 0/9 couches → le `RangeError: Maximum call stack size exceeded` au clic synthétique
de la sonde est un effet **aval** (calc sur grilles vides). **Strictement identique sur `dev`** → non imputable à
rnd-003 (c'est exactement le caveat « env doit autoriser Supabase » du contrat / `eval-app-rubric.mjs`).
Le harness 4.5 est un **artefact d'environnement**, pas une note sur le changement.

### Check 4 — CI → ✅ PASS (scope contrat)
- `validate-code` : **JS syntax check (node --check) = pass**, **HTML lint (htmlhint) = pass**.
- `Cloudflare Pages` = pass (preview déployée).
- ⚠️ `Workers Builds: tellux` = **fail** — mais **pré-existant** : déjà rouge sur **PR #852 (rnd-001)** avant
  l'existence de rnd-003. Pipeline Workers parallèle, **non imputable** à ce diff. Hors scope CI du contrat.

---

## RÉSERVES DE VÉRIFICATION (transparence — non bloquantes, à arbitrer par Soleil)

1. **Pan prouvé par identité de code, pas par clic marqueur réel.** Les couches marqueurs (certifiés, antennes)
   n'ont pas chargé (DNS Supabase) → je n'ai **pas** pu déclencher un `panTo` via `_certOpenCross` ni un `panBy`
   via popup volumineux par interaction utilisateur. J'ai validé le **mécanisme** : (a) les 3 options d'init lues
   directement, (b) `panBy` et le chemin **réel** `setView`/`applyHashToMap` exercés avec l'expression identique
   `!tlxReduceMotion()`. `panTo` (5ᵉ site) est couvert par **identité d'expression**, pas par observation directe.
2. **Non-régression absolue non observée ici.** « 9 couches + comptes justes + indice dual recalculé » n'est pas
   vérifiable dans ce sandbox (Supabase injoignable, identique sur dev). Verdict établi en **relatif** (parité dev)
   + no-op-par-construction. **Recommandation : un run de confirmation en environnement Supabase-joignable**
   (preview CF depuis un réseau qui résout Supabase, ou env custom allowlisté) **avant merge**, pour clore la
   non-régression en absolu.
3. **Edge mid-session documenté (assumé par le contrat).** `zoomAnimation` est lu **une fois à l'init** ; un
   changement OS de la préférence **en cours de session** n'est honoré que pour les pans explicites (lus à l'appel),
   pas pour le zoom (Leaflet fige `_zoomAnimated` à l'init). Edge rare, déjà acté dans `contrat.md` § HORS PÉRIMÈTRE.

---

## CRITIQUE CRAFT PRÉCISE (chemin 9-10 — observation, **pas** un correctif ; §2 : je ne corrige rien)

Le helper instancie `TLX_RM_QUERY` (un `MediaQueryList`) mais **ne s'abonne jamais à son événement `change`**.
Un `TLX_RM_QUERY.addEventListener('change', …)` qui re-lirait la préférence (et, idéalement, ré-appliquerait
les options d'animation de la carte) **fermerait l'edge mid-session** du point 3 et constituerait le pattern
a11y « soigné » attendu. C'est la **raison unique** pour laquelle Fonctionnalité, Craft et l'edge restent à 8 et
non 9. Décision laissée au générateur/Soleil — l'évaluateur ne tranche pas l'implémentation.

---

## CONDITIONS D'ARRÊT (§6)
- Seuil §5.1 atteint (8.0 ≥ 7.0) **et** gates PASS → **SUCCÈS**. Stop boucle.
- Pas de plateau, pas d'escalade. Itération 1/3.
- Suite : PR draft ouverte, **clôture/merge = Soleil** (après, idéalement, le run de confirmation env de la réserve 2).

— Évaluateur (session fraîche, Claude Code). Ne corrige rien, ne se félicite pas (§2).
