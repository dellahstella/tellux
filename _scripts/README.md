# Scripts de build Tellux

## precompute_alignments.mjs

Pre-calcule les alignements megalithiques (detection brute force + Monte Carlo p-value)
et ecrit le resultat dans `_data/alignments_precomputed.json`.

### Quand relancer

- A chaque modification du corpus SITES dans `index.html`
- A chaque ajout/suppression de site dans `SITES_REFERENCE.json`
- Apres un audit GPS qui modifie des coordonnees

### Commande

```bash
node _scripts/precompute_alignments.mjs
```

### Parametres (dans le script)

- `maxDev` : deviation max en metres (400m)
- `minPts` : nombre minimum de points sur l'alignement (4)
- `minKm` : longueur minimum en km (8)
- `nSims` : nombre de simulations Monte Carlo (500)

### Output

Le fichier `_data/alignments_precomputed.json` doit etre commite avec le HTML modifie.
Le HTML charge ce JSON au lieu de calculer en runtime.
Si le fetch echoue, un fallback runtime est conserve dans index.html.
