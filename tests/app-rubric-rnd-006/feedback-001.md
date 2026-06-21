# FEEDBACK-001 — Évaluation rnd-006 (accents libellés bloc légende cavités · `app.html`)

> Session **ÉVALUATEUR** (§2). Critique uniquement — **rien corrigé**.
> Légitimité §2 : l'évaluateur n'a **pas** écrit le diff rnd-006 (aucun biais d'auto-notation) ; il a, dans une
> phase antérieure, évalué rnd-002 — item **distinct**. Générateur ≠ évaluateur respecté.
> Cible : PR #863, branche `claude/rnd-006-legende-cavites-accents` @ `d71f6ac`. Prod jamais touchée (D-2).
> Rubrique : `_drafts/RND_RUBRIQUE_TELLUX.md` (gate-puis-score, D-4). Contrat : `tests/app-rubric-rnd-006/contrat.md`.

---

## VERDICT GLOBAL : ✅ PASS — score pondéré **8.85 / 10** (seuil 7.0), gates PASS. Itération 1/3.

Per §6 : seuil atteint **et** gates PASS → **SUCCÈS**. Auto-merge `dev` (politique active) ; prod `dev→main` = gate Soleil.

---

## MÉTHODE (transparence)

Changement à **surface nulle au runtime** : deux libellés de **texte visible** accentués dans un littéral chaîne
JS (`LEGEND_HTML.cav`). Le DOM rendu est entièrement déterminé par la source. Le contrat (NOTE) acte que la
validation source est suffisante (précédent rnd-002). Évalué par :
1. **Analyse statique exhaustive** d'`app.html` @ `d71f6ac` (diff byte-exact + assertions de chaîne).
2. **Signaux CI sur le commit head** : `JS syntax check (node --check)` **success**, `HTML lint (htmlhint)`
   **success**, `Eval Playwright Axe APP §5.1 (informatif)` **success**, `Cloudflare Pages` **success**.

Pas de serve Playwright local frais (attribut/texte statique pleinement déterminé ; serve non-allowlisté
mal-noterait les couches data — caveat prompt évaluateur ; Axe headless déjà vert sur ce commit).

---

## COUCHE 1 — GATES ÉLIMINATOIRES

| Gate | Verdict | Justification |
|---|---|---|
| **G1 — doctrine** | ✅ **PASS (non-déclenché)** | Correction orthographique de deux libellés d'affichage. Aucun contenu scientifique/mission EM, aucune affirmation de bénéfice, aucun retour-terrain-comme-preuve, aucun mysticisme ; « mesure d'abord » intact. Rien à gater. |
| **G2 — citations §10** | ✅ **PASS / N-A (non-déclenché)** | Aucune référence/DOI/corpus/CHURCHES/SITES ajouté ou édité. « BRGM BD Cavités » = nom de la base BRGM (attribution de source d'affichage, **déjà présent** avant le diff — seul l'accent change), **pas** une citation scientifique. `verify_citation.py` non requis. |

Gates PASS → on score §5.1.

---

## COUCHE 2 — SCORE §5.1

| Critère | Poids | Note | Pondéré | Raison de la note |
|---|---|---|---|---|
| **Fonctionnalité** | 0.35 | **9** | 3.15 | Objectif du contrat **intégralement** rempli : `leg-title === "Cavités"` (1×), `leg-src === "BRGM BD Cavités"` (1×), `alt` **inchangé** (« Légende des cavités souterraines (BRGM) », 1×). Cible = **littéraux statiques → aucun cas limite**. −1 (pas 10) : rendu live du panneau légende non observé de bout-en-bout (non requis par le contrat). |
| **Non-régression données** | 0.30 | **9** | 2.70 | **Orthogonal aux données** : seules deux chaînes d'affichage changent. **Byte-identité vérifiée vs dev** : `LAYER=CAVITE_LOCALISEE` et l'URL `src` WMS **non modifiés** (le diff +1/−1 ne touche ni l'un ni l'autre) → l'image légende charge toujours. Zéro coordonnée/compte/calcul touché. `é` = char UTF-8 dans une chaîne JS `'…'` → `node --check` **PASS** (syntaxe non cassable). −1 (pas 10) : observation live absolue des 9 couches non rejouée (impossible d'affecter par construction). |
| **Craft / UX** | 0.20 | **9** | 1.80 | Le changement **clôt précisément le nit (b)** qui plafonnait Craft de rnd-002 : le bloc `cav` est désormais **cohérent en interne** (titre « Cavités » + `alt` « cavités » + source « BD Cavités ») et aligné avec bouton/tooltip/i18n déjà accentués. Nom officiel BRGM « BD Cavités » correctement employé. −1 (pas 10) : résidu **hors-scope** — la divergence de forme entre l'`alt` cavités (verbeux, avec source) et l'`alt` voisin « Légende Forêts publiques » (terse) subsiste dans le système de légendes (item séparé, pas rnd-006). |
| **Robustesse** | 0.15 | **8** | 1.20 | Aucun impact console possible (chaînes inertes). `validate-code` vert (node --check + htmlhint), **Axe headless `success` sur ce commit**, aucun init redondant. −1 (pas 9) : console-propre live non ré-observée localement cette session (couvert par l'Axe headless CI). |
| **Σ pondéré** | | | **8.85** | `threshold_met = true` (≥ 7.0) |

> **Note anti-laxisme (§rubrique).** Score > rnd-002 (8.65) — **cohérent** : rnd-006 **résout** le nit qui tenait
> le Craft de rnd-002 à 8 (d'où Craft 9 ici), avec une non-régression **prouvable par construction** (tokens
> techniques byte-identiques, pas seulement parité) et un Axe headless **vert sur le commit**. La rubrique
> discrimine quand même : Robustesse à 8 (live non ré-observé), aucun axe à 10 (rendu live de bout-en-bout absent),
> et un résidu Craft hors-scope est **nommé** plutôt qu'ignoré. PASS **mérité** sur changement minuscule, sûr, et
> qui restaure une cohérence UI réelle.

---

## PREUVES FALSIFIABLES (statique @ `d71f6ac` + CI head)

### Check 1 — Libellés accentués → ✅ PASS
Diff `dev…d71f6ac` sur `app.html` (template `LEGEND_HTML.cav`, ligne 2287, **+1/−1**) :
```diff
-  cav:'...<b class="leg-title">Cavites</b>...<div class="leg-src">BRGM BD Cavites</div>...'
+  cav:'...<b class="leg-title">Cavités</b>...<div class="leg-src">BRGM BD Cavités</div>...'
```
Assertions statiques sur la branche : `<b class="leg-title">Cavités</b>` = **1**, `BRGM BD Cavités` = **1**,
`alt="Légende des cavités souterraines (BRGM)"` = **1** (inchangé).

### Check 2 — Couverture / non-régression libellés → ✅ PASS
Résidu de **texte visible** « Cavites » non accentué dans `app.html` : **0** occurrence (`grep -oE 'Cavites'`).
Le code technique `CAVITE_LOCALISEE` (tout-capitales, sans `s`) **n'est pas** du texte visible et reste tel quel.

### Check 3 — Non-régression technique → ✅ PASS
- `LAYER=CAVITE_LOCALISEE` et l'URL `src` (`geoservices.brgm.fr/risques?…`) **non touchés par le diff** → l'image
  WMS charge depuis le même endpoint qu'avant (rendu inchangé vs `dev`).
- Aucune autre ligne d'`app.html` modifiée (diff strictement limité à la ligne 2287).
- `node --check` **PASS** : le littéral `cav:'…'` reste du JS valide (le `é` UTF-8 n'altère pas la syntaxe).
> NB contrat : l'invariant « `grep -c` = 1 » vaut **sur la ligne `cav`** ; en fichier entier ces tokens
> apparaissent sur 2/3 lignes (autres défs de couche), **toutes inchangées**. L'invariant réel (byte-identité vs
> dev) tient.

### Check 4 — CI → ✅ PASS (scope contrat)
`JS syntax check (node --check)` = **success** · `HTML lint (htmlhint)` = **success** ·
`Eval Playwright Axe APP §5.1 (informatif)` = **success** · `Cloudflare Pages` = **success**.

---

## CONDITIONS D'ARRÊT (§6)
- Seuil §5.1 atteint (8.85 ≥ 7.0) **et** gates PASS → **SUCCÈS**. Stop boucle.
- Pas de plateau, pas d'escalade. Itération 1/3.
- Suite : auto-merge `dev` (politique active) ; prod `dev→main` = gate Soleil.

— Évaluateur (session fraîche, Claude Code). Ne corrige rien, ne se félicite pas (§2).
