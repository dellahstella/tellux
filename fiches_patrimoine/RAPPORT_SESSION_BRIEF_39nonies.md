# Rapport de session - Brief 39nonies (audit doublons residuels post-39octies)

Date : 2026-05-07
Mode : APPLY
Perimetre : audit doublons coords <200m post-Brief 39octies. 4 fusions canoniques + 6 divergences coords.

## Synthese globale

| Action | Nombre |
|---|---|
| Fusions FR/IT (canon long absorbe court) | 2 (la_canonica, sainte_marie_majeure_bonifacio) |
| Reclassifications axe_corpus | 1 (monte_revincu -> remarquables_geologiques) |
| Fusions complexe ramasse | 1 (celluccia -> casa_di_l_orca renomme complexe) |
| Divergences coords (faux doublons) | 6 |
| Total impacts JSON | 10 |
| Total sites JSON apres brief | 449 (-3 fusions sur 452) |

## Decisions Soleil arbitrees

1. Fusion la_canonica + slug long Lucciana-Mariana : OUI (memes coords, meme description Cathedrale Mariana)
2. Fusion FR/IT Sainte-Marie-Majeure Bonifacio : OUI (traduction = meme eglise)
3. monte_revincu : reclasse en site naturel (sommet 359m, comme monte_stello / monte_d_oro)
4. celluccia + casa_di_l_orca : fusion - complexe ramasse, slug renomme "Casa di l'Orca (complexe)"
5. san_roccu_ajaccio : 2 sites distincts, description erronee corrigee + coords divergees
6. 4 paires faux doublons coords identiques : recherches Cowork pour vraies coords approximatives

## Phase 1 - Fusions / reclassifications (4 ops, -3 sites)

### Fusion la_canonica
- Slug conserve : `la_canonica` (court, canonique)
- Slug supprime : `la_canonica_santa_maria_assunta_lucciana_mariana`
- Description fusionnee : "Cathedrale Mariana - Sur colonie romaine - Baptistere fouille"
- Sources fusionnees, gps_locked Brief 39nonies

### Fusion sainte_marie_majeure_bonifacio
- Slug conserve : `sainte_marie_majeure_bonifacio` (FR canonique)
- Slug supprime : `santa_maria_maggiore_bonifacio_vieille_ville` (IT)
- Description fusionnee : "Principale eglise medievale Bonifacio - Loggia XVIe - Citerne d'eau - Calcaire falaises - MH"
- gps_locked Brief 39nonies

### Reclassification monte_revincu
- axe_corpus : megalithes -> remarquables_geologiques
- categorie : Megalithique -> Site naturel remarquable
- nom : Monte Revincu
- description : "Sommet 359m - Desert des Agriates - Domine le complexe archeologique neolithique eponyme - Granit"
- Justification Soleil : "monte_revincu est un site naturel (genre monte_stello ou monte_d_oro)"
- gps_locked Brief 39nonies

### Fusion celluccia -> casa_di_l_orca
- Slug conserve : `casa_di_l_orca` renomme "Casa di l'Orca (complexe)"
- Slug supprime : `celluccia`
- Description englobante : "Complexe neolithique Monte Revincu - Dolmens Casa di l'Orcu + Casa di l'Orca - Menhir Celluccia - Village neolithique moyen - MH 1889+2018 - Santo-Pietro-di-Tenda - Agriates"
- Justification Soleil : "complexe ramasse, on fusionne les elements"
- gps_locked Brief 39nonies

## Phase 2 - Divergences coords (6 corrections)

| Slug | Old coords | New coords | Justification |
|---|---|---|---|
| san_roccu_ajaccio_vieille_ville | (41.918, 8.738) | (41.9215, 8.7372) | Vraie eglise Saint-Roch 29 cours Napoleon (Wikipedia + Wiki) ; description corrigee : "neoclassique 1885 Maglioli" au lieu de description cathedrale |
| menhir_sermano | (42.31, 9.249) | (42.3055, 9.248) | Offset SW village (eglise san_nicolao_sermano garde coords centre) |
| pastini | (41.5577, 8.9407) | (41.5805, 8.945) | Plateau Pastini distinct plateau Cauria (Cardiccia reste Cauria 41.5577) |
| terrina_aleria | (42.1036, 9.5128) | (42.1078, 9.5165) | Site neolithique terrasse Tavignano, distinct cite antique |
| san_quilicu_castellare_di_casinca | (42.46806, 9.47403) | (42.467, 9.472) | Chapelle annexe distincte San Pancrazio (eglise principale, IXe siecle) |
| santa_maria_della_neve_grosseto_prugna_basse | (41.905, 8.798) | (41.9095, 8.803) | Eglise inland, distincte tour Capitello (cote) |

Note importante : ces 6 divergences sont des **approximations Cowork post-recherche web**. Les coords precises auraient demande un audit terrain. Toutes flagguees dans `notes` : "approximation post-recherche Cowork, audit terrain Soleil suggere".

## Slugs supprimes (3)

| Slug supprime | Slug conserve canonique |
|---|---|
| la_canonica_santa_maria_assunta_lucciana_mariana | la_canonica |
| santa_maria_maggiore_bonifacio_vieille_ville | sainte_marie_majeure_bonifacio |
| celluccia | casa_di_l_orca (renomme complexe) |

## Garde-fous respectes

- gps_locked=true applique sur les 10 sites touches
- Backup pre-Brief 39nonies (post-39octies) : `_drafts/sites_patrimoine.brief39nonies_post_2026-05-07.json`
- Aucun site Briefs 27-39octies non concerne par ce dedup touche
- JSON valide (449 sites)

## Cas non traites (pour info Soleil)

Doublons coords <200m identifies mais laisses tels quels (superpositions justifiees ou hors scope) :

- couvent_sant_antoni_de_calvi & cathedrale_saint_jean_baptiste_de_calvi : 2 edifices distincts dans citadelle Calvi (normal)
- san_giovanni_battista_de_corte & citadelle_de_corte : eglise dans citadelle (normal)
- san_dominique_bonifacio & sainte_marie_majeure_bonifacio : 2 eglises distinctes vieille ville
- san_giovanni_de_bonifacio & bonifacio_remparts : eglise dans remparts (normal)
- pastini & cardiccia : DIVERGES Phase 2 (pastini decale NNE)

## Fichiers livres Cowork

- `_drafts/sites_patrimoine.brief39nonies_post_2026-05-07.json` - snapshot post-brief
- `docs/data/sites_patrimoine.json` (worktree distracted-cohen) - 449 sites
- `fiches_patrimoine/RAPPORT_SESSION_BRIEF_39nonies.md` - ce rapport

## Validation Soleil suggeree

- Drill-down patrimoine : la_canonica unique (plus de doublon)
- Drill-down Bonifacio : 1 seul marker Sainte-Marie-Majeure (FR)
- Drill-down Monte Revincu : Casa di l'Orca complexe + monte_revincu (sommet, axe geologique)
- Drill-down Cauria : pastini (plateau N) et cardiccia (plateau S) distincts visuellement
- Drill-down Aleria : terrina_aleria (terrasse Tavignano) distinct santa_maria_aleria (cite antique)
- Drill-down Sermano : menhir et eglise San Nicolao distincts
- Audit terrain Soleil suggere pour confirmer/affiner les 6 coords divergees Phase 2

## Note sur la convention de naming brief

A partir de ce brief : naming Cowork-initiated = `Brief 39nonies` (pour distinguer des briefs Soleil). Cowork ne propose pas de briefs sans validation Soleil ; ce brief a recu validation initiale via demande "attaquons les problemes que tu as listes".
