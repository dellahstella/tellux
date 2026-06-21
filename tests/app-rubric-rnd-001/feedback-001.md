# FEEDBACK-001 — Évaluateur rnd-001 · `prefers-reduced-motion` (app.html)

```
ITÉRATION   : 1 / 3
ÉVALUATEUR  : session fraîche distincte (§2) — critique uniquement, ne corrige rien
CANDIDAT    : PR #852 · branche claude/rnd-001-reduced-motion · head 0531ab3
MÉTHODE     : inspection diff + Playwright 1.60 headless (chromium) + harness canonique
              tests/blindage-harness/eval-app-rubric.mjs (parité main↔candidat)
DATE        : 2026-06-21
VERDICT     : ✅ PASS — score pondéré 8.7 / 10 (seuil 7.0)
```

---

## 0. Ground-truth (vérifié, non pris pour acquis)

| Affirmation générateur | Vérification évaluateur | Statut |
|---|---|---|
| Branche + PR #852 draft existent | `gh pr view 852` : OPEN, draft, base `dev`, head `claude/rnd-001-reduced-motion` | ✅ |
| Diff = `app.html` +12 + `contrat.md` | `git diff dev..branch --stat` : 2 fichiers, +118 (app.html 12, contrat 106) | ✅ |
| « 0 contenu/citation, G2 non déclenché » | `git diff dev..branch -- scripts/citations_registry.json` → **vide** : le registre §10 **n'est pas** touché par la branche (la trace vue vs `main` est pré-existante sur `dev`) | ✅ vérifié, pas supposé |
| Workers Builds fail = pré-existant | fail **identique** sur `dev`, `main` ET PR #849 → infra, **non imputable** à rnd-001 | ✅ |
| CI `validate-code` vert | htmlhint **pass** · node --check **pass** | ✅ |

---

## 1. Gates binaires éliminatoires (évalués EN PREMIER)

- **G1 — Conformité doctrine : PASS (N/A déclenché).** Diff = un seul bloc CSS de présentation derrière `@media`. Aucune fonction `calc*`, aucune donnée `SITES/CHURCHES/HYPOTHESES`, aucune zone gelée (`EXPERT_WEIGHTS_DEFAULT`, `calcGammaAmbient`…), aucune affirmation de bénéfice EM. Inspection ligne à ligne du diff : conforme.
- **G2 — Intégrité citations §10 : PASS (N/A déclenché).** Aucune DOI/source/corpus ajoutée ou éditée. `verify_citation.py` non requis. Registre non touché (cf. §0).

> Les deux gates passent par **non-déclenchement** — conforme à l'intention bootstrap du contrat. On calcule donc §5.1.

---

## 2. Score pondéré §5.1 (preuves falsifiables)

### Preuve A — Mode `reduce` ACTIF (Playwright `reducedMotion: 'reduce'`)
Échantillon (`#legende-toggle`, `#legende-content`, `.sidebar-toggle`, `.leaflet-control-zoom-in`, `.leaflet-container`, `button`) : `transitionDuration` **et** `animationDuration` = `1e-05s` (0.01 ms) partout.
Statistique globale sur **1098 éléments** : éléments à transition non-nulle **136 → 0**, à animation non-nulle **3 → 0**, `maxDur {t:0, a:0}`. → Le bloc s'applique **exhaustivement**, sans exception.

### Preuve B — Mode `no-preference` (NON-RÉGRESSION CSS)
Durées d'origine **intactes** : `#legende-toggle` `0.2s,0.2s,0.2s` · `#legende-content` `0.25s` · `.sidebar-toggle` `0.15s` · `button` `0.15s` · max animation `2s` (cert-halo-pulse). Globalement 136 transitions / 3 animations vivantes. → La media query **gate** correctement ; comportement par défaut strictement inchangé.

### Preuve C — Non-régression moteur (harness canonique, parité)
`eval-app-rubric.mjs` lancé sur **candidat** et **main** dans le **même env** sandbox (réseau externe partiellement bloqué) : **liste de fails byte-identique** des deux côtés —
`boot non prêt`, `couches 0/9`, `filtre_cotier ok=false`, `console_boot 5 err` (Supabase `ERR_NAME_NOT_RESOLVED`), `console_interact 1 err` (`RangeError: Maximum call stack size exceeded`).
→ **Δ candidat↔main = 0.** Ces fails sont **env/pré-existants** (boot offline + erreurs réseau), pas une régression rnd-001. Le `RangeError` apparaît **à l'identique sur `main`** : explicitement **non imputable** au candidat.

### Preuve D — Boot map dans les DEUX modes (probe)
`leaflet=true`, 7 panes, 32 tiles, 30 markers — **identiques** en `reduce` et `no-preference`. Le bloc CSS ne casse pas Leaflet. Zéro erreur console **introduite par le candidat** (les 12–13 erreurs sont des échecs réseau externes identiques dans les deux modes).

| Critère §5.1 | Poids | Note /10 | Pondéré | Justification |
|---|---|---|---|---|
| Fonctionnalité | 0.35 | **8.5** | 2.975 | Neutralisation CSS exhaustive (Preuve A). Décote : la voie **JS** n'est pas couverte (cf. F1). |
| Non-régression | 0.30 | **9.5** | 2.85 | Prouvée 2× (Preuves B + C). Décote minime : env a empêché un boot positif autonome. |
| Craft / UX | 0.20 | **8.5** | 1.70 | Snippet canonique a11y-project, commenté, single-concern, 0.01 ms≠0 justifié (cf. F2). |
| Robustesse | 0.15 | **8.0** | 1.20 | Boot OK 2 modes, 0 erreur candidat, lint vert. Décote : garantie reduced-motion incomplète côté JS. |
| **TOTAL** | | | **8.73** | **≥ 7.0 → PASS** |

---

## 3. Constats résiduels (NON bloquants)

- **F1 — mineure, hors périmètre déclaré (candidate rnd-003).** `app.html:5091` : l'auto-pan popup `map.panBy(…, {animate:true, duration:0.3})` (déclenché en `requestAnimationFrame`) **reste animé** sous `prefers-reduced-motion`. La solution **CSS-only ne neutralise pas les animations JS de Leaflet** (`{animate:true}` pan/zoom). L'objectif « neutralisant transitions et animations » est donc tenu **côté CSS uniquement**. Impact WCAG 2.3.3 faible (pan fonctionnel one-shot 0.3 s, pas une animation décorative continue), mais à fermer proprement par : lire `matchMedia('(prefers-reduced-motion: reduce)').matches` et passer `{animate:false}`. → **Reporter en rnd-003**, ne pas élargir cette PR (single-concern respecté).
- **F2 — cosmétique.** Le commentaire `app.html:1174` justifie le 0.01 ms par « les listeners `transitionend` continuent de se déclencher » : **aucun** listener `transitionend`/`animationend` n'existe en propre dans `app.html`. Le choix reste **correct** — le vrai bénéficiaire est le nettoyage interne de Leaflet (`_onZoomTransitionEnd`), qui dépend d'un `transitionend` ; un `0s` strict pourrait le starver sur certains moteurs. Suggestion (optionnelle) : préciser « (cleanup zoom Leaflet interne) ». Pas un défaut fonctionnel.
- **F3 — env, déjà neutralisé.** Le boot 0/9 et le `RangeError` du harness canonique sont des artefacts du sandbox offline, **identiques sur main** (Preuve C). Aucune action candidat.

---

## 4. Décision & suite

**PASS (8.7 ≥ 7.0), les 2 gates passés.** Par §2 : la PR draft **#852 reste ouverte** ; la décision de **merge appartient à Soleil** (l'évaluateur ne merge pas, ne corrige pas). État draft **inchangé** (passage ready = décision Soleil).

Boucle : item **résolu en 1 itération** (pas d'escalade plateau). F1 → ouvrir **rnd-003** (gating JS Leaflet) en item séparé de la file R&D ; F2 → nit optionnel laissé à l'arbitrage du générateur.

— Évaluateur rnd-001, session fraîche (§2)
