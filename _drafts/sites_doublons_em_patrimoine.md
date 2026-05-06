# Sites doublons EM ↔ patrimoine — Brief 33 split

Date : 2026-05-06
Périmètre : sites présents à la fois dans `docs/data/sites_em.json` et dans `docs/data/sites_patrimoine.json`, par décision Soleil de préférer la duplication au conflit cross-app.

## Doublons appliqués (vague initiale)

### 1. Aléria antique

| Champ | sites_em.json | sites_patrimoine.json |
|---|---|---|
| `slug` | `aleria_antique` | `aleria_antique` |
| `axe` | `remarquables_geologiques` | `patrimoine_bati_remarquable` |
| `name` | « Aléria antique » | « Aléria antique » |
| `lat / lon` | identiques | identiques |
| `fiche_v3_slug` | (n/a) | `aleria_ruine` |

Justification : le plateau d'Aléria est à la fois un site géophysique remarquable (affleurement ophiolitique) et un site archéologique majeur (ville antique exhumée XXᵉ siècle). La fiche v3 sensorielle (`fiches_patrimoine/sites/aleria_ruine_v3.md`) ne couvre que la dimension patrimoniale ; la dimension EM justifie l'entrée séparée dans `sites_em.json`.

## Candidats doublons à arbitrer (vagues ultérieures)

Les sites suivants sont actuellement classés exclusivement dans `sites_em.json` (axe `remarquables_geologiques` ou `hydrauliques`) mais possèdent une dimension patrimoniale qui pourrait justifier une duplication dans `sites_patrimoine.json` :

### Sites naturels sacrés (axe `remarquables_geologiques`, dimension patrimoine naturel)

- `aiguilles_de_bavella` — paysage sacré insulaire, fréquentation pèlerinage
- `monte_san_petrone` — sommet sacré de la Castagniccia, point culminant historique
- `monte_stello` — culminant Cap Corse, marqueur géographique majeur
- `lac_de_nino` — lac sacré du Niolu, lieu de pèlerinage
- `lac_de_creno` — lac glaciaire sacré de la Sorroinsù
- `monte_cinto` — point culminant de Corse, dimension symbolique
- `cap_corse_extreme_nord` — pointe extrême sept., dimension symbolique
- `desert_des_agriate` — paysage sacré dépeuplé
- `calanques_de_piana` — paysage UNESCO, dimension patrimoine naturel
- `reserve_de_scandola` — site UNESCO

### Sites mégalithiques sur affleurement géologique (axe `megalithes` côté patrimoine actuel, dimension EM)

- `filitosa` — statues-menhirs sur granite, dimension EM granitique
- `palaggiu` — alignement de menhirs, granitique
- `cauria_i_stantari` — alignements, granitique
- `cucuruzzu_capula` — castellu torréen sur affleurement, EM

Ces sites sont déjà dans `sites_patrimoine.json` (axe `megalithes`). Un doublon en `sites_em.json` permettrait à `app.html` de les afficher comme sites EM aussi. À arbitrer si Brief 29 EM doit les inclure.

### Sites industriels hydrauliques (axe `hydrauliques`, dimension patrimoine industriel)

- `barrage_alesani` — barrage XXᵉ, patrimoine industriel
- `barrage_de_calacuccia` — barrage Niolu, patrimoine industriel
- `barrage_du_rizzanese` — barrage Alta Rocca, patrimoine industriel
- `barrage_padula` — barrage Cap, patrimoine industriel

Ces sites sont actuellement dans `sites_em.json` uniquement (axe `hydrauliques`). Si Brief 27 patrimoine veut les couvrir, ils seraient à dupliquer.

### Citadelles génoises (axe `tours_genoises`/`patrimoine_divers`, dimension EM minéral)

- `bastia_citadelle` — citadelle Terra Nova sur schiste lustré, dimension EM
- `bonifacio_remparts` — remparts sur calcaire miocène, dimension EM minéralogique majeure
- `citadelle_de_calvi` — citadelle sur granite, dimension EM
- `citadelle_de_corte` — citadelle sur ophiolites (rare en Corse), dimension EM majeure

## Convention de duplication (rappel Soleil Brief 33)

Quand un site est présent dans les deux fichiers :

1. **Slug** : préférer le même slug dans les deux fichiers (les fichiers sont distincts, pas de collision JSON). Le brief mentionnait l'option `_em` en suffixe ; cette option reste disponible si une distinction explicite côté code est utile.
2. **Coordonnées** : prioriser identiques. Si justification précise (ex. point géologique vs centroïde de l'édifice à 50 m), divergence acceptable.
3. **Schémas** : pas de propriétés communes au-delà de `slug`, `name`, `lat`, `lon`. Le reste est dédié à chaque app.
4. **Trace** : ajouter le champ `_doublon_em` ou `_doublon_patrimoine` dans l'entrée du fichier opposé, pointant vers cette doc.

## Workflow d'ajout d'un nouveau doublon

1. Identifier le site dans son fichier d'origine (sites_em ou sites_patrimoine).
2. Construire l'entrée dans le fichier opposé en respectant son schéma.
3. Ajouter le slug dans la table « Doublons appliqués » de cette doc.
4. Vérifier que les coordonnées concordent (sauf justification précise).
5. Tester en prod : les deux apps doivent afficher le site avec leur popup respectif sans confusion utilisateur.

## Plan de rollback

Le `sites_corse.json` est marqué `_DEPRECATED` mais reste dans le repo 30 jours (target 2026-06-05). Si rollback nécessaire :

- Retirer le `_DEPRECATED`.
- Code rebascule `fetch('sites_em.json')` et `fetch('sites_patrimoine.json')` vers `fetch('sites_corse.json')`.
- Adapter le filtrage côté client.
- Coût estimé : 30 min Code.

Aucun rollback prévu pour les fiches Cowork (les 437 entrées patrimoine + 43 entrées EM sont reproductibles depuis sites_corse.json par le script de split — à archiver dans `scripts/build_sites_split.py` lors d'une vague future si besoin de reproductibilité).
