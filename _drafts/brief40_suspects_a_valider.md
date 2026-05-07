# Brief 40 — Audit balayage suspects (axe_corpus/categorie null)

**Date** : 2026-05-07
**Total sites scannés** : 449
**Suspects détectés** : **0**

## Résultat

```python
suspects = [s for s in sites if not s.get('axe_corpus') or not s.get('categorie')]
# len(suspects) == 0
```

Le corpus `sites_patrimoine.json` est entièrement classé sur les axes `axe_corpus` et `categorie`. Aucun site fantôme avec champs null.

## Doublons par coordonnées

```
=== Doublons coords (lat,lon identiques) ===
(aucun)
```

## Doublons par nom

```
=== Doublons name (case-insensitive) ===
(aucun)
```

## Conclusion

**Aucune validation Soleil requise** sur ce volet. Le corpus est propre.

Le problème originel "2 markers ?" sur les Trinités N'ÉTAIT PAS un doublon JSON mais un **badge CSS `arbitrage`** ajouté via le Set hardcodé `ARBITRAGE_SLUGS` (patrimoine.html ligne 362). Fix appliqué : vider le Set (Brief 40 commit).
