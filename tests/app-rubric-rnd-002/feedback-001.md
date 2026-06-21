# FEEDBACK-001 — Évaluation rnd-002 (`alt` légende WMS BRGM cavités · `app.html`)

> Session **ÉVALUATEUR** fraîche (§2). Critique uniquement — **rien corrigé**.
> Cible : PR #861, branche `claude/rnd-002-brgm-legend-alt` @ `47d9ca5`. Prod jamais touchée (D-2).
> Rubrique : `_drafts/RND_RUBRIQUE_TELLUX.md` (gate-puis-score, D-4). Contrat : `tests/app-rubric-rnd-002/contrat.md`.

---

## VERDICT GLOBAL : ✅ PASS — score pondéré **8.65 / 10** (seuil 7.0), gates PASS. Itération 1/3.

Per §6 : seuil atteint **et** gates PASS → **SUCCÈS**. Pas d'itération générateur requise. PR draft ouverte ;
**clôture/merge dev = politique auto-merge ; prod dev→main = gate Soleil.** Réserves de méthode ci-dessous (non bloquantes).

---

## MÉTHODE (transparence)

Changement à **surface nulle au runtime** : un attribut `alt` **statique** ajouté à une `<img>` dans un littéral
chaîne JS (`LEGEND_HTML.cav`). Le DOM rendu est **entièrement déterminé par la source** — aucune branche, aucun
état, aucune donnée distante en jeu. Le contrat (NOTE) acte explicitement que **le verdict ne dépend pas du rendu
de cette couche**. J'ai donc évalué par :

1. **Analyse statique exhaustive** de `app.html` @ `47d9ca5` (diff byte-exact, inventaire complet des `<img>`).
2. **Signaux CI sur le commit head** (canoniques, headless) :
   - `Eval Playwright Axe APP §5.1 (informatif)` (Playwright + axe-core, headless) → **success** sur **cette
     branche** (run `27913414038`). C'est le signal a11y headless de référence ; il ne lève aucune régression.
   - `JS syntax check (node --check)` → **success** · `HTML lint (htmlhint)` → **success** · `Cloudflare Pages` → **success**.

Je n'ai **pas** lancé un serve Playwright local frais : (a) inutile pour un attribut statique pleinement
déterminé sans runtime ; (b) le contrat exempte cette couche du rendu ; (c) un serve local sans allowlist
ANFR/`geo.api.gouv.fr`/Supabase **mal-noterait** les couches de données (caveat explicite du prompt évaluateur) ;
(d) le signal Axe headless a déjà tourné en CI **sur ce commit**.

---

## COUCHE 1 — GATES ÉLIMINATOIRES

| Gate | Verdict | Justification |
|---|---|---|
| **G1 — doctrine** | ✅ **PASS (non-déclenché)** | Le diff n'ajoute qu'un `alt` de présentation. Aucun contenu scientifique/mission EM, aucun bénéfice EM affirmé, aucun retour-terrain-comme-preuve, aucun mysticisme. `« (BRGM) »` = attribution de source d'image (déjà présente dans `leg-src`), pas une affirmation. Rien à gater. |
| **G2 — citations §10** | ✅ **PASS / N-A (non-déclenché)** | Aucune référence/corpus/CHURCHES/SITES/DOI/hypothèse ajoutée ou éditée. Un `alt` descriptif **n'est pas** une référence scientifique. `verify_citation.py` non requis. |

Gates PASS → on score §5.1.

---

## COUCHE 2 — SCORE §5.1

| Critère | Poids | Note | Pondéré | Raison de la note |
|---|---|---|---|---|
| **Fonctionnalité** | 0.35 | **9** | 3.15 | Objectif du contrat **intégralement** rempli : l'`<img src*="GetLegendGraphic"][src*="CAVITE_LOCALISEE"]` porte `alt="Légende des cavités souterraines (BRGM)"` — **non vide, descriptif, pertinent**. Attribut **statique → aucun cas limite** (présent à tout chemin de rendu). −1 (pas 10) : annonce lecteur d'écran de bout-en-bout **non observée en live** (non requise par le contrat ; l'`alt` est statiquement déterminé). |
| **Non-régression données** | 0.30 | **9** | 2.70 | Modification **orthogonale aux données** : un littéral chaîne, touche **zéro** couche/compte/calcul/coordonnée. `src` WMS **byte-identique** (image se rend toujours). Pas de conflit d'échappement (chaîne JS `'…'`, `alt` en `"…"`, « cavités » accentué valide en source UTF-8) → **`node --check` PASS** le confirme. −1 (pas 10) : observation live absolue « 9 couches + comptes + indice dual » non rejouée cette session (impossible par construction d'affecter ces grandeurs). |
| **Craft / UX** | 0.20 | **8** | 1.60 | `alt` bien choisi, concis, satisfait **WCAG 1.1.1 / RGAA 1**, source `(BRGM)` cohérente avec `leg-src`. Tenu à **8** (pas 9) sur deux nits nommés (cf. § Craft). |
| **Robustesse** | 0.15 | **8** | 1.20 | Aucun impact console possible (attribut inerte). `validate-code` vert (node --check + htmlhint) ; **Axe headless `success` sur ce commit** (aucune nouvelle violation a11y) ; aucun init redondant introduit. −1 (pas 9) : console-propre live non ré-observée localement cette session (couvert par l'Axe headless CI). |
| **Σ pondéré** | | | **8.65** | `threshold_met = true` (≥ 7.0) |

> **Note anti-laxisme (§rubrique).** Score **supérieur** à rnd-003 (8.0) — et c'est **cohérent**, pas laxiste :
> rnd-003 avait un edge **code-level réel** (préférence média mid-session non honorée, `MediaQueryList.change` non
> abonné) qui plafonnait légitimement à 8 ; rnd-002 n'a **aucun** edge code-level (attribut inconditionnel), une
> non-régression **prouvable par construction** (orthogonale, pas seulement par parité), et un signal Axe headless
> **vert sur le commit** (là où rnd-003 était bloqué par le DNS Supabase du sandbox). La rubrique discrimine quand
> même : Craft et Robustesse restent à 8 sur manques nommés ; aucun axe n'atteint 10 (observation live de bout-en-bout absente).

---

## PREUVES FALSIFIABLES (statique @ `47d9ca5` + CI head)

### Check 1 — `alt` présent et descriptif → ✅ PASS
Diff `dev…47d9ca5` sur `app.html` (template `LEGEND_HTML.cav`) :
```diff
-  ...LAYER=CAVITE_LOCALISEE" style="max-width:150px;display:block;margin:4px 0"><div class="leg-src">BRGM BD Cavites</div>
+  ...LAYER=CAVITE_LOCALISEE" style="max-width:150px;display:block;margin:4px 0" alt="Légende des cavités souterraines (BRGM)"><div class="leg-src">BRGM BD Cavites</div>
```
Sélecteur du contrat satisfait : `img[src*="GetLegendGraphic"][src*="CAVITE_LOCALISEE"]` → `alt` **non vide** (`'Légende des cavités souterraines (BRGM)'.trim().length = 39 > 0`). +1 / −1 ligne, single-concern, `src` inchangé.

### Check 2 — Couverture totale des `<img>` → ✅ PASS
Inventaire **exhaustif** des `<img>` d'`app.html` @ head (4 littéraux, **0** image construite en JS — aucun
`createElement('img')` / `new Image()`) :

| # | `src` | `alt` | Non vide ? |
|---|---|---|---|
| 1 | `assets/logo/tellux_logo.svg` | `Tellux` | ✅ |
| 2 | `assets/logo/tellux_logo.svg` | `Tellux — Révéler l'invisible` | ✅ |
| 3 | `…GetLegendGraphic…LAYER=FORETS.PUBLIQUES` | `Légende Forêts publiques` | ✅ |
| 4 | `…GetLegendGraphic…LAYER=CAVITE_LOCALISEE` | `Légende des cavités souterraines (BRGM)` | ✅ **(ce diff)** |

**4/4** avec `alt` non vide. Scan `alt=""` → **0** occurrence : aucune régression inverse.

### Check 3 — Non-régression → ✅ PASS
- `src`/paramètres WMS **byte-identiques** → l'image charge depuis le même endpoint BRGM (rendu inchangé vs `dev`).
- Aucune autre `<img>` perdue (4 sur `dev`, 4 sur la branche).
- `node --check` **PASS** sur le bloc `<script>` modifié → le littéral `cav` reste du JS valide (pas de bris d'échappement).

### Check 4 — CI → ✅ PASS (scope contrat)
- `JS syntax check (node --check)` = **success** · `HTML lint (htmlhint)` = **success**.
- `Eval Playwright Axe APP §5.1 (informatif)` = **success** (Playwright/axe-core headless sur le commit head).
- `Cloudflare Pages` = **success** (preview déployée).

---

## CRITIQUE CRAFT PRÉCISE (chemin 9-10 — observation, **pas** un correctif ; §2 : je ne corrige rien)

1. **Divergence de style avec l'`alt` voisin.** L'`<img>` Forêts publiques porte `alt="Légende Forêts publiques"`
   (terse, sans source) ; la nouvelle porte `alt="Légende des cavités souterraines (BRGM)"` (plus verbeuse, source
   entre parenthèses). **Pas un défaut** — la version cavités est même plus descriptive — mais une **incohérence de
   forme** entre deux légendes sœurs. Harmoniser le motif (ex. les deux avec, ou les deux sans, l'attribution de
   source) serait le « soigné » 9-10.
2. **Nit hors-périmètre, à remonter pour un futur cycle (NON gaté, NON dans ce contrat).** Le titre **visible**
   juste au-dessus de l'`<img>` est `<b class="leg-title">Cavites</b>` — **sans accent** (« Cavités » correct).
   Le générateur a justement accentué l'`alt` (« cavités ») mais le libellé à l'écran reste « Cavites ». Cosmétique,
   pré-existant, **hors périmètre rnd-002** ; candidat idéal pour un micro-cycle `rnd-00x` ultérieur. Aucune action
   demandée ici.

Ces deux points (l'un cosmétique, l'autre hors-scope) sont la **raison unique** pour laquelle Craft reste à 8.

---

## RÉSERVES DE MÉTHODE (transparence — non bloquantes)

1. **Évaluation statique + CI, pas de serve Playwright local frais cette session.** Justifié (attribut statique
   pleinement déterminé ; contrat exempte le rendu de cette couche ; serve local non-allowlisté mal-noterait les
   données ; Axe headless déjà vert sur le commit). Si Soleil veut la ceinture-et-bretelles : ouvrir la légende
   « Cavités » sur le **preview CF de la PR** et lire l'`alt` au DOM — résultat attendu identique (l'attribut est dans
   la source).
2. **Rendu effectif de l'image BRGM** dépend de la joignabilité du WMS `geoservices.brgm.fr` (réseau), **inchangée
   par ce diff** : si l'image se rendait sur `dev`, elle se rend ici ; sinon, l'`alt` joue précisément son rôle de
   **texte de remplacement** (bénéfice net du changement).

---

## CONDITIONS D'ARRÊT (§6)
- Seuil §5.1 atteint (8.65 ≥ 7.0) **et** gates PASS → **SUCCÈS**. Stop boucle.
- Pas de plateau, pas d'escalade. Itération 1/3.
- Suite : auto-merge `dev` (politique active) ; prod `dev→main` = gate Soleil.

— Évaluateur (session fraîche, Claude Code). Ne corrige rien, ne se félicite pas (§2).
