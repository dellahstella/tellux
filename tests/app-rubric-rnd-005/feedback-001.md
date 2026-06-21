# FEEDBACK-001 — Évaluation rnd-005 (réactivité mid-session `prefers-reduced-motion`)

> Session **ÉVALUATEUR** fraîche (§2). Critique uniquement — **rien corrigé**.
> Cible : PR #858, branche `claude/rnd-005-reduced-motion-reactive` @ `e33b2bc`.
> Méthode : Playwright headless (chromium-1223, pw 1.60.0) contre le **preview Cloudflare Pages de la PR**
> (`https://8a03a682.tellux.pages.dev/app`, épinglé sur le head). Prod jamais touchée (D-2).
> Test clé : `emulateMedia({reducedMotion})` **après boot**, dans les deux sens, + parité boot vs base `dev`
> (qui contient rnd-003 mais pas le listener). Rubrique : `_drafts/RND_RUBRIQUE_TELLUX.md` (gate-puis-score).

---

## VERDICT GLOBAL : ✅ PASS — score pondéré **8.55 / 10** (seuil 7.0), gates PASS. Itération 1/3.

Per §6 : seuil atteint **et** gates PASS → **SUCCÈS**. PR draft reste ouverte ; **merge = Soleil**.
Pas d'itération générateur requise. rnd-005 **ferme proprement la réserve #3 de l'éval rnd-003** (le helper
`TLX_RM_QUERY` n'était pas écouté). Évolution de score cohérente : 8.0 (rnd-003) → 8.55, le gap connu étant
comblé avec le pattern idiomatique et vérifié **bidirectionnellement**.

---

## COUCHE 1 — GATES ÉLIMINATOIRES

| Gate | Verdict | Justification |
|---|---|---|
| **G1 — doctrine** | ✅ **PASS (non-déclenché)** | Diff = un seul listener JS `addEventListener('change')` qui resynchronise des options d'animation Leaflet. Aucun contenu scientifique/mission EM, aucun bénéfice EM affirmé, aucun mysticisme, « mesure d'abord » intact. |
| **G2 — citations §10** | ✅ **PASS / N-A (non-déclenché)** | Aucune référence/corpus/CHURCHES/SITES/DOI/hypothèse. **Aucune coordonnée modifiée** (vérifié sur le diff : +13 lignes, un bloc listener). `verify_citation.py` non requis. |

Gates PASS → on score §5.1.

---

## COUCHE 2 — SCORE §5.1

| Critère | Poids | Note | Pondéré | Raison de la note |
|---|---|---|---|---|
| **Fonctionnalité** | 0.35 | **9** | 3.15 | Réactivité prouvée **dans les deux sens** (OFF→ON et ON→OFF), options **et** `map._zoomAnimated` rebasculent, pan post-changement (non-)animé en conséquence. −1 (pas 10) : geste de zoom non exercé visuellement (j'ai validé le **levier** d'état, pas un zoom rendu) + simplification de formule `_zoomAnimated` (cf. craft). |
| **Non-régression données** | 0.30 | **8** | 2.40 | **Boot strictement identique à `dev`/rnd-003** (snapshots boot identiques, 2 modes — cf. preuves). Listener no-op au boot par construction. −1 (pas 9) : vérification **absolue** des 9 couches + indice dual non **personnellement** observée (DNS Supabase bloqué dans le sandbox ; corroborée par le check CI ci-dessous mais score CI non lisible). |
| **Craft / UX** | 0.20 | **9** | 1.80 | Pattern a11y **idiomatique** (`addEventListener('change')` — exactement la piste 9-10 signalée en rnd-003), gardé (`addEventListener` + `L.Browser`), commenté (explique le *pourquoi* du resync `_zoomAnimated`), single-concern. −1 (pas 10) : formule `_zoomAnimated` simplifiée (cf. note). |
| **Robustesse** | 0.15 | **8** | 1.20 | Listener gardé/exception-safe, ne tourne qu'au `change` (rare), **aucun init redondant** (un seul `addEventListener`), aucune nouvelle surface d'erreur. −1 (pas 9) : console « propre » au boot complet non observable localement (bruit env identique sur dev). |
| **Σ pondéré** | | | **8.55** | `threshold_met = true` (≥ 7.0) |

> Note anti-laxisme (§rubrique) : PASS **discriminé**, pas un blanc-seing. Deux axes tenus à **8** (non-régression
> non observée en absolu ; console propre non observée localement) ; deux axes à **9 et non 10** (geste de zoom
> non rendu ; formule `_zoomAnimated` simplifiée). Aucun 10. La hausse vs rnd-003 (8.0→8.55) est **méritée** : le
> gap connu est comblé et vérifié bidirectionnellement par sondes falsifiables.

---

## PREUVES FALSIFIABLES (Playwright, `emulateMedia` **après boot**)

Snapshot = `{zoom, fade, marker}` = `map.options.{zoomAnimation,fadeAnimation,markerZoomAnimation}` ;
`za` = `map._zoomAnimated` ; `rm` = `tlxReduceMotion()`. Matrice complète (rnd-005 vs base `dev`) :

| App | boot | au boot `{zoom/fade/marker, za, rm}` | après `emulateMedia` | `{zoom/fade/marker, za, rm}` après | pan post-Δ |
|---|---|---|---|---|---|
| **rnd-005** | no-preference | `{true,true,true, za:true, rm:false}` | → `reduce` | **`{false,false,false, za:false, rm:true}`** ✅ | instantané ✅ |
| **rnd-005** | reduce | `{false,false,false, za:false, rm:true}` | → `no-preference` | **`{true,true,true, za:true, rm:false}`** ✅ | animé ✅ |
| `dev` (rnd-003) | no-preference | `{true,true,true, za:true, rm:false}` | → `reduce` | `{true,true,true, za:true, rm:true}` — options **inchangées** (pas de listener) | instantané |
| `dev` (rnd-003) | reduce | `{false,false,false, za:false, rm:true}` | → `no-preference` | `{false,false,false, za:false, rm:false}` — options **inchangées** | animé |

**Lecture :**
- **Check 1 (OFF→ON)** ✅ : rnd-005 fait basculer options **et** `_zoomAnimated` à `false` au changement ; pan
  post-changement non animé.
- **Check 2 (ON→OFF)** ✅ : symétrique, tout réactivé.
- **Check 3 (non-régression boot)** ✅ : le **boot de rnd-005 est identique au boot de `dev`** dans les deux
  modes (lignes 1-2 vs 3-4, colonnes « au boot » identiques). Le listener n'agit **qu'au `change`**.
- **Le gap que rnd-005 corrige est visible** : sur `dev`, après le changement OS, les **options carte restent
  figées** (seul `rm` bascule) — d'où le zoom-geste qui n'honorait pas la préférence. rnd-005 le corrige ;
  les pans, eux, étaient déjà réactifs des deux côtés (lecture à l'appel, rnd-003), confirmé par la colonne pan.

### Détail `_zoomAnimated` (le point subtil, bien traité)
Leaflet fige `_zoomAnimated` à l'init (≈ `options.zoomAnimation && Browser.any3d && TRANSITION && !mobileOpera`).
Le diff resynchronise via `!rm && !!L.Browser.any3d`. Comme `!rm` vaut l'`options.zoomAnimation` qui vient
d'être posé, cela revient à `options.zoomAnimation && any3d` — **la meilleure approximation par API publique**
(`TRANSITION` est privé/non exposé ; `mobileOpera` est obsolète). Resync observé correct : `za` bascule
`true↔false` en phase avec les options dans les deux sens.

### CI (criterion 4)
- `validate-code` : **node --check = pass**, **htmlhint = pass**.
- `Cloudflare Pages` = pass.
- **`Eval Playwright Axe APP §5.1 (informatif)` = pass** (env CI réseau-activé, Supabase joignable) — corrobore
  que l'app boote et que le harness §5.1 s'exécute sans crash dans un environnement où les couches data chargent.
  ⚠️ Le score chiffré du run CI n'est pas lisible depuis l'API check-run (sortie écrite en `$GITHUB_STEP_SUMMARY`),
  et l'étape est **guardée** (un exit 2 n'avorte pas) — donc le « pass » atteste l'exécution propre, **pas**
  formellement le franchissement de seuil. À ne pas sur-interpréter.
- ⚠️ `Workers Builds: tellux` = **fail** — **pré-existant** (déjà rouge sur #852 et #854) → **non imputable**.

---

## RÉSERVES DE VÉRIFICATION (transparence — non bloquantes)

1. **Non-régression absolue toujours non observée *par moi*.** Le sandbox de l'évaluateur ne résout pas le DNS
   Supabase → 0/9 couches localement (identique dev/rnd-005). Le boot étant **prouvé byte-identique à `dev`** et le
   listener **no-op au boot**, rnd-005 **ne peut pas** affecter le chargement des couches. La réserve #2 héritée de
   rnd-003 est désormais **corroborée** par le check CI informatif vert (réseau-activé), mais je n'ai pas pu lire
   le compte de couches/indice dual chiffré du run CI. Confiance haute, observation absolue toujours déférée.
2. **Geste de zoom non rendu.** J'ai validé l'état-levier (`map.options.*Animation` + `map._zoomAnimated`) qui est
   exactement ce que Leaflet lit au moment d'un zoom — mais je n'ai pas déclenché un **zoom visuel** post-changement
   pour observer l'animation rendue. Le contrat ne le demande pas (il demande le bascule des options + `_zoomAnimated`,
   fait) ; je le signale par rigueur.

---

## CRITIQUE TECHNIQUE PRÉCISE (observation, **pas** un correctif ; §2 : je ne corrige rien)

La resynchronisation `map._zoomAnimated = !rm && !!L.Browser.any3d` **omet** les facteurs `TRANSITION` et
`!mobileOpera` de la formule interne de Leaflet. En pratique c'est **immatériel** : `TRANSITION` est un const privé
(non exposé par `L.Browser`, donc inatteignable proprement depuis app.html) et `mobileOpera` (Opera Mini) est
obsolète ; `any3d` est le facteur contraignant et `TRANSITION` est virtuellement toujours vrai quand `any3d` l'est.
Le seul écart théorique — un navigateur où `any3d===true` mais `TRANSITION===false` — est aujourd'hui inexistant.
C'est la **raison unique** pour laquelle Fonctionnalité et Craft restent à **9 et non 10**. Décision laissée au
générateur/Soleil — l'évaluateur ne tranche pas l'implémentation.

---

## CONDITIONS D'ARRÊT (§6)
- Seuil §5.1 atteint (8.55 ≥ 7.0) **et** gates PASS → **SUCCÈS**. Stop boucle.
- Pas de plateau, pas d'escalade. Itération 1/3.
- Suite : PR draft ouverte, **clôture/merge = Soleil**.

— Évaluateur (session fraîche, Claude Code). Ne corrige rien, ne se félicite pas (§2).
