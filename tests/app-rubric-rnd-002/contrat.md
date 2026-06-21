# CONTRAT D'ITÉRATION — rnd-002 · `alt` légende WMS BRGM cavités (app.html)

> À lire avec `PROTOCOLE_AUTO_ITERATION.md` (§2, §4, §5.1). Item de file : issue #860.

```
CHANTIER   : rnd-002 — alt manquant sur la légende WMS BRGM (cavités) d'app.html
AXE        : app · PRIORITÉ : basse (micro a11y)
GÉNÉRATEUR : Code (Claude Code) — branche claude/rnd-002-brgm-legend-alt (base dev)
ÉVALUATEUR : session FRAÎCHE distincte (Playwright headless) — NE corrige pas
DATE       : 2026-06-21
```

## OBJECTIF (1 phrase)
Ajouter un `alt` descriptif à la seule `<img>` d'`app.html` qui en manquait — la légende **WMS BRGM
GetLegendGraphic** (`LAYER=CAVITE_LOCALISEE`).

## CONTEXTE
Audit a11y (rnd-001) : 4 `<img>`, 3 avec `alt` (2 logos + légende Forêts publiques), **1 sans** (BRGM cavités).
Défaut **WCAG 1.1.1 (Contenu non textuel) / RGAA 1**.

## CE QUI A ÉTÉ FAIT (1 attribut)
Dans le template de légende `cav` (string JS), ajout sur l'`<img>` BRGM :
`alt="Légende des cavités souterraines (BRGM)"` (style cohérent avec la légende Forêts publiques voisine).
`src`/paramètres WMS **inchangés**. Audit des 3 autres `<img>` : `alt` déjà présents et pertinents → non touchés.

## DANS LE PÉRIMÈTRE
Le seul attribut `alt` de l'`<img>` BRGM cavités. Single-concern.

## HORS PÉRIMÈTRE
- Zones gelées, `src`/URL WMS, coordonnées, autres pages, refonte légende.

## CRITÈRES D'ACCEPTATION — gate-puis-score (D-4)

### Couche 1 — Gates éliminatoires
- **G1 doctrine** : PASS attendu (un `alt` de présentation, aucun contenu/mission EM).
- **G2 citations §10** : PASS attendu / N-A — un `alt` descriptif n'est **pas** une référence scientifique ;
  `verify_citation.py` non requis. (« BRGM » = attribution de source d'image, déjà présente dans `leg-src`.)

### Couche 2 — §5.1 (seuil 7.0) — checks falsifiables Playwright
1. **`alt` présent et descriptif** : ouvrir la légende cavités (ou inspecter le DOM/template) →
   l'`<img src*="GetLegendGraphic"][src*="CAVITE"]` a un `alt` **non vide** et pertinent.
   Vérif rapide possible sans rendu : `app.html` contient `LAYER=CAVITE_LOCALISEE` suivi d'un `alt=`.
2. **Couverture totale** : les **4** `<img>` d'`app.html` ont un `alt` non vide (régression inverse interdite).
3. **Non-régression** : l'image se rend toujours (`src` inchangé) ; aucune autre `<img>` perdue ; console propre.
4. **CI** : `validate-code` (htmlhint + node --check) vert.

## NOTE PLAYWRIGHT
```js
const html = await page.content();
// ou cibler la légende rendue après ouverture du panneau légende
const altOk = await page.evaluate(() => {
  const img = document.querySelector('img[src*="GetLegendGraphic"][src*="CAVITE"]');
  return img ? (img.getAttribute('alt') || '').trim().length > 0 : 'img-non-rendue';
});
```
(Si la légende cavités n'est pas montée au boot, valider sur la source/template — le contrat ne dépend pas du
rendu de cette couche.)

## PARAMÈTRES DE BOUCLE
```
SEUIL : 7.0 / 10 · MAX ITÉRATIONS : 3 · ESCALADE : plateau Δ<0.3 sur 3 → stop + RAPPORT_FINAL.md
```

## SÉPARATION §2
Générateur (ce commit) ne s'évalue pas. Évaluateur = session fraîche, écrit `feedback-001.md` ici + commente
la PR, ne corrige rien. PASS → auto-merge dev (politique active) ; prod dev→main = gate Soleil.
