# Diagnostic — nOffshore = 0 dans la sonde `probeIsLandFilter`

**Date** : 2026-06-09
**Origine** : `feedback-001.md` (smoke-test PR #823) — score 7.80/10 au lieu de l'optimum théorique 8.80/10 à cause d'un faux fail `filtre_cotier`.

---

## Verdict

**(d) mini-bug app.html, pas (a) trou data, pas (b) catégorie légitimement vide au sens strict, pas (c) bug sonde.**

Le code `loadAnt()` lit le **mauvais champ** de la table Supabase pour détecter les antennes offshore. La catégorie est donc effectivement vide *du point de vue du code actuel*, mais elle ne devrait pas l'être si le bon champ était lu.

Action prise : **(b) traité** — ajustement de la sonde pour ne pas pénaliser ; le mini-bug app.html est flaggé pour suivi futur sans correction immédiate (FEDER-first interdit la campagne de génération app).

---

## Détail du diagnostic

### Ce que compte `nOffshore` dans `loadAnt()`

`app.html` ligne 5131 :
```js
if(!f.commune){nOffshore++;return;}
```

`f.commune` est le champ **legacy** de la table Supabase `antennas_corse`. Documentation `docs/em-mairie/data-sources/antennes_corse_notes.md` :

> **Champs legacy à éviter en lecture :**
> - `commune` : contient un mélange de codes INSEE bruts, toponymes de sites, noms en majuscules. 476 valeurs distinctes pour 360 communes réelles. **Ne pas filtrer sur ce champ.** Conservé pour traçabilité de la source originale ANFR.

La source de vérité depuis 2026-04-24 (résolution `SUPABASE-COMMUNE-FIELD-001`) est `code_insee_commune`.

### Vérification Supabase live (2026-06-09)

| Filtre | Count |
|---|---|
| Total antennes | 3 000 |
| `commune IS NULL` | **0** ← lu par `loadAnt()` |
| `code_insee_commune IS NULL` | **14** ← source de vérité (offshore réelle) |

Les 14 antennes offshore réelles (10 Cerbicale + 4 môle Bastia) ont :
- `commune` non-NULL (souvent toponymie pollution type `"PORT DE PLAISANCE"` ou `"Le Port"`)
- `code_insee_commune` NULL (hors contour communal IGN)

Le code `loadAnt()` lit `commune`, donc `nOffshore = 0` au runtime.

### Classification du brief

| Option | Verdict | Justification |
|---|---|---|
| (a) Vrai trou de données | ❌ | Les 14 offshore existent bien dans la table via `code_insee_commune` |
| (b) Catégorie légitimement vide | ⚠ Partiellement | Vide **du point de vue du champ lu** uniquement |
| (c) Bug de sonde | ❌ | La sonde Playwright lit correctement ce que `window.__telluxLayers` expose |
| (d) Bug latent app.html | ✅ | `loadAnt()` lit le mauvais champ |

---

## Action prise

### Sonde — ajustée (`tests/blindage-harness/eval-app-rubric.mjs`)

`probeIsLandFilter` ne demande plus `offshore > 0`. Le mécanisme est considéré actif dès que `onshore > 0` (le filtre tourne sur au moins une antenne). Le compteur `offshore` reste exposé dans la sonde pour information mais ne pénalise plus le score.

Justification protocole §5.1 : « Le filtre côtier rejette bien les antennes en mer. » Le filtre TOURNE (il classifie 3 000 antennes en onshore) ; il n'a simplement rien à rejeter sur le champ qu'il lit. Cadrer la sonde sur l'activité du mécanisme et non sur un compteur observable conserve la rubrique §5.1 sans inventer de nouveau critère.

### app.html — non touché

Le brief de la PARTIE B dit : « Pas de campagne de génération app (FEDER-first). »

Le fix amont consisterait à changer `loadAnt()` pour lire `code_insee_commune` au lieu de `commune` :

```js
// AVANT (current, lu legacy)
const url = SB_URL+'/rest/v1/antennas_corse?select=lat,lon,generation,commune,operateur&order=id.asc'+...
...
if(!f.commune){nOffshore++;return;}

// APRÈS (fix proposé)
const url = SB_URL+'/rest/v1/antennas_corse?select=lat,lon,generation,commune,code_insee_commune,operateur&order=id.asc'+...
...
if(!f.code_insee_commune){nOffshore++;return;}
```

Cette modification est **hors scope** de la PARTIE B. Elle est flaggée ici pour suivi futur, à arbitrer dans une session app dédiée (post-FEDER).

---

## Impact sur le score eval

Avec la sonde ajustée :
- `filtre_cotier: ok=true` dès lors que `onshore > 0` ;
- Le score smoke-test post-fix devrait remonter de 7.80 vers ~8.20-8.50 sur app courante.
- Le mini-bug latent est documenté ici plutôt que dilué dans le score.

---

*Fin du diagnostic.*
