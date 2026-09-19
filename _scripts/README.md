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

## precompute_emag2v3_corse.mjs

Extrait une grille figee EMAG2v3 (anomalie magnetique crustale, service NOAA ImageServer)
pour la Corse, a resolution native (2 arc-min, pixelSizeX/Y du service), et l'ecrit dans
`_data/emag2v3_corse_<date>.json` avec metadonnees de provenance (produit, DOI, altitude,
licence, endpoint, bbox, date d'extraction).

Produit en TEMPS 1 du brief REMPLACEMENT_LCS1_GRID_2026-09-19 (dette de provenance sur
LCS1_GRID, app.html — cf. rapport prive RAPPORT_LCS1_IDENTITE_IMPACT_2026-09-19.md,
r=-0,10 contre ce meme service). **Non branche a app.html a la production de ce fichier**
— la bascule des deux affichages publics (popup « C », jauge crustale) est un chantier
separe, non autorise dans ce commit.

### Quand relancer

- Si une bascule (Temps 2, brief separe) decide d'adopter cette source : reextraire a une
  date recente avant embarquement definitif (le champ crustal est statique a l'echelle
  humaine, mais le service NOAA lui-meme peut evoluer).
- Jamais en cours de service applicatif : c'est un script de build hors-ligne, appele a la
  main, pas un chemin de chargement runtime.

### Commande

```bash
node _scripts/precompute_emag2v3_corse.mjs
```

### Parametres (dans le script)

- `BBOX` : lon 8.5-9.65, lat 41.3-43.1 — identique a la bbox deja utilisee par `wmsEmag`
  (app.html, const wmsEmag, exportImage) pour EMAG2v3 en Corse, pas une bbox inventee.
- `PITCH` : 1/30° (2 arc-min) — pas natif du service (pixelSizeX/Y, verifie en direct).
  Ne jamais descendre en dessous (sur-resolution non justifiee par la source).
- `CONCURRENCY` (6), `MAX_RETRIES` (4, backoff exponentiel), `TIMEOUT_MS` (8000) — le
  service NOAA a un historique documente de 500/503/timeout intermittents (cf. commentaire
  `_emag2ServiceDown`, app.html) ; le script retente avant d'abandonner un point.

### Output

Le fichier `_data/emag2v3_corse_<date>.json` contient `_metadata` (provenance complete,
chaque champ marque de sa source) et `grille` (tableau `[lat,lon,nT]`, `nT=null` pour tout
point hors couverture ou en echec apres retries — jamais silencieux, comptes rapportes en
`_metadata.nb_points_no_data`/`nb_points_fetch_failed`).
