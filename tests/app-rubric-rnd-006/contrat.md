# CONTRAT D'ITÉRATION — rnd-006 · Accents manquants sur le bloc légende cavités (`app.html`)

> À lire avec `PROTOCOLE_AUTO_ITERATION.md` (§2 séparation, §4 boucle, §5.1 rubrique APP).
> Item de file : issue #862. Origine = nit hors-scope **(b)** de l'éval rnd-002 (`feedback-001.md`, PR #861).

```
CHANTIER   : rnd-006 — accents FR sur les libellés visibles du bloc légende cavités (app.html)
AXE        : app · PRIORITÉ : basse (i18n/cohérence UI)
GÉNÉRATEUR : Code (Claude Code) — branche claude/rnd-006-legende-cavites-accents (base dev)
ÉVALUATEUR : session FRAÎCHE distincte — NE corrige pas
DATE       : 2026-06-21
DÉPEND DE  : rnd-002 (#861, mergé dans dev — alt de la légende cavités présent)
```

## OBJECTIF (1 phrase)

Accentuer correctement les **chaînes de texte visibles** du bloc légende `cav:` d'`app.html` (« Cavites » →
« Cavités »), pour cohérence avec le reste de l'UI française, **sans toucher à aucun identifiant technique**.

## CONTEXTE

Tout le reste de l'UI écrit déjà « Cavités » (bouton `#b-cav`, son `title`, l'`alt` de rnd-002, l'i18n
`lyr_cav`). Seuls deux libellés du bloc légende `cav:` (objet `LEGEND_HTML`, ≈ L2290) restaient sans accent :
le titre `leg-title` et la source `leg-src`. C'est une incohérence d'affichage pure, repérée par l'éval rnd-002.

## CE QUI A ÉTÉ FAIT (1 ligne, +1/−1)

Dans `LEGEND_HTML.cav` :
- `<b class="leg-title">Cavites</b>` → `<b class="leg-title">Cavités</b>`
- `<div class="leg-src">BRGM BD Cavites</div>` → `<div class="leg-src">BRGM BD Cavités</div>` (nom officiel
  BRGM « BD Cavités »).

Caractère `é` UTF-8, à l'intérieur de la chaîne JS `cav:'…'` (déjà le cas partout ailleurs dans le fichier).

## DANS LE PÉRIMÈTRE
Les deux libellés visibles ci-dessus. Single-concern, une seule ligne modifiée.

## HORS PÉRIMÈTRE (inchangé, byte-identique)
- L'identifiant de couche WMS **`CAVITE_LOCALISEE`** et l'URL `src` de la légende (`geoservices.brgm.fr/risques?…`) —
  **non modifiés** (vérifiable : `grep -c` = 1 chacun, identiques à dev).
- Le bouton/tooltip/i18n « Cavités » (déjà accentués), les autres légendes, autres pages.
- Toute coordonnée, citation, donnée scientifique, zone gelée. **Aucune** touchée.

## CRITÈRES D'ACCEPTATION — gate-puis-score (D-4)

### Couche 1 — Gates éliminatoires
- **G1 doctrine** : PASS attendu par **non-déclenchement** — correction orthographique d'un libellé d'affichage,
  aucun contenu/mission EM, aucune affirmation, « mesure d'abord » intact.
- **G2 citations §10** : PASS attendu par **non-déclenchement** — aucune référence/DOI/corpus. « BD Cavités » est
  le nom d'une base BRGM (attribution de source d'affichage), pas une citation scientifique ; déjà présent avant.

### Couche 2 — §5.1 (seuil 7.0) — checks falsifiables
1. **Libellés accentués** : dans `LEGEND_HTML.cav`, `leg-title` === « Cavités » et `leg-src` === « BRGM BD Cavités »
   (assertion statique sur la source ; l'`alt` reste === « Légende des cavités souterraines (BRGM) »).
   Si rendu live souhaité : ouvrir le panneau légende, activer la couche cavités, lire le titre du bloc.
2. **Couverture / non-régression libellés** : aucune autre occurrence « Cavites » non accentuée ne subsiste en
   **texte visible** d'`app.html` (le code technique `CAVITE_LOCALISEE` n'est PAS du texte visible et reste tel quel).
3. **Non-régression technique** : `LAYER=CAVITE_LOCALISEE` + URL WMS `src` **byte-identiques** à dev (la légende
   image charge toujours). Aucune coordonnée/donnée modifiée.
4. **CI** : `validate-code` vert — JS `node --check` via `extract-and-check-js.mjs` (la modif est dans une chaîne
   JS, ne peut casser la syntaxe) **et** `htmlhint`. (Vérifié localement : 0 failure / 0 error.)

> NOTE : la cible étant un **littéral statique** pleinement déterminé, la validation source est contractuellement
> suffisante (cf. précédent rnd-002). Un serve local non-allowlisté mal-noterait les couches data (caveat prompt
> évaluateur) — préférer la preview CF de la PR si un rendu live est souhaité. Jamais la prod (D-2).

## PARAMÈTRES DE BOUCLE
```
SEUIL : 7.0 / 10 pondéré (après gates) · MAX ITÉRATIONS : 3 · ESCALADE : plateau Δ<0.3 sur 3 → stop + RAPPORT_FINAL.md
```

## SÉPARATION §2
Le générateur (ce commit) **ne s'évalue pas**. Évaluateur = session fraîche, écrit `feedback-001.md` ici +
commente la PR, **ne corrige rien**. FAIL → le générateur itère. PASS → PR draft reste ouverte ; merge = Soleil
(politique auto-merge R&D PASS→dev active).
