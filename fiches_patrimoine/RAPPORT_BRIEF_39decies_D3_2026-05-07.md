# Rapport Brief 39decies D3 - dolmen_serra vs casa_di_l_orca

Date : 2026-05-07
Initie par : Soleil ("attaquons les problemes")
Periode : suite Brief 39nonies (audit doublons), tache D3 grille de lecture.

## Probleme

`dolmen_serra` (description "Dolmen Casa di l'Urca - Complexe Monte Revincu - Santucci et al. 2004") apparait comme doublon orthographique potentiel de `casa_di_l_orca` (renomme "complexe" Brief 39nonies). Coords distantes ~700m mais memes references dans la description.

## Investigation web

Recherches confirment :

- **Casa di l'Orca / Urca / Ulca** (feminin, "ogresse") = Dolmen 1 du complexe Monte Revincu
- **Casa di l'Orcu / Ulcu / u Lurcu** (masculin, "ogre") = Dolmen 2 du complexe Monte Revincu
- Distance Orca <-> Orcu : ~500m selon megalithic.co.uk + vici.org
- Source academique : Santucci, Thury-Bouvet, Khoumeri, Ottavi 2004 "Legends, Megaliths And Astronomy In Corsica Island" EIM 2004
- Wikipedia FR : "Site archeologique du Monte Revincu" mentionne explicitement les 2 dolmens distincts

## Decision Soleil

> "ah ok bien vu on laisse deux sites distincts et on enleve la mention complexe les curieux pourront comprendre grace aux fiches v3"

## Action appliquee

### casa_di_l_orca (refondu)

| Champ | Avant (Brief 39nonies) | Apres (Brief 39decies) |
|---|---|---|
| nom | Casa di l'Orca (complexe) | Casa di l'Orca |
| description | "Complexe neolithique Monte Revincu - Dolmens Casa di l'Orcu + Casa di l'Orca - Menhir Celluccia - Village neolithique moyen..." | "Dolmen 'maison de l'ogresse' (feminin) - Complexe Monte Revincu - Vers 3000 av JC - Distinct de Casa di l'Orcu (l'ogre, masculin) a 500m..." |
| gps_locked | True (Brief 39nonies) | True (Brief 39decies) |
| coords | (42.6707, 9.2577) | (42.6707, 9.2577) inchangees |

### dolmen_serra -> casa_di_l_orcu

Renommage du slug + refonte description.

| Champ | Avant | Apres |
|---|---|---|
| slug | dolmen_serra | casa_di_l_orcu |
| nom | (vide) | Casa di l'Orcu |
| description | "Dolmen Casa di l'Urca - Complexe Monte Revincu - Santucci et al. 2004" | "Dolmen 'maison de l'ogre' (masculin) - Complexe Monte Revincu - Variantes orthographiques Casa di l'Urcu / Casa di u Lurcu - Distinct Casa di l'Orca (ogresse) a 500m - MH 1889+2018 - Source Santucci et al. 2004" |
| gps_locked | False | True (Brief 39decies) |
| coords | (42.669, 9.2649) | (42.669, 9.2649) inchangees |

### monte_revincu (inchange)

Reste tel quel post-Brief 39nonies : axe_corpus=remarquables_geologiques, gps_locked=True, coords (42.669, 9.2585).

## Distances finales (3 markers complexe Monte Revincu)

| Pair | Distance |
|---|---|
| Casa di l'Orca <-> Casa di l'Orcu | 618 m |
| Casa di l'Orca <-> Monte Revincu (sommet) | 200 m |
| Casa di l'Orcu <-> Monte Revincu (sommet) | 523 m |

Le sommet Monte Revincu est topographiquement au-dessus des 2 dolmens, c'est coherent.

## Garde-fous respectes

- Tous les sites Briefs 38-39nonies non concernes inchanges
- Backup pre-D3 : sites_patrimoine.json restaure depuis commit `bd59afd` puis modifications appliquees
- JSON valide post-D3 : 449 sites
- Locked total post-D3 : 77 sites (76 -> 77, ajout casa_di_l_orcu)

## Note technique

- Slug `dolmen_serra` etait probablement tronque a l'origine (probablement `dolmen_serra_di_qqch` au depart, raccourci a `dolmen_serra`). Le contexte "Serra" pourrait designer la crete topographique, ce qui colle avec la position du dolmen masculin sur les pentes du Monte Revincu.
- L'erreur "Casa di l'Urca" dans la description originale etait une variante orthographique de "Orcu" (le -u final est typique du corse, mais ici c'etait probablement une confusion avec le feminin "Urca" qui est la variante de "Orca"). Les deux variantes existent et peuvent designer le meme sexe selon les regions/auteurs - source de confusion legitime.

## Fichiers livres

- `docs/data/sites_patrimoine.json` (worktree distracted-cohen) - 449 sites, 77 locked
- `fiches_patrimoine/RAPPORT_BRIEF_39decies_D3_2026-05-07.md` - ce rapport

## Validation Soleil suggeree

Drill-down Monte Revincu en niveau 2 :
- 3 markers distincts : Monte Revincu (sommet, axe geologique), Casa di l'Orca (dolmen ogresse), Casa di l'Orcu (dolmen ogre)
- Plus de mention "complexe" dans les noms (les fiches v3 expliqueront le contexte global du complexe Monte Revincu)

## Commande git

```
git checkout -b feat/brief-39decies-d3-monte-revincu && \
git add docs/data/sites_patrimoine.json \
        fiches_patrimoine/RAPPORT_BRIEF_39decies_D3_2026-05-07.md && \
git commit -m 'data(patrimoine): Brief 39decies D3 - scission dolmen_serra->casa_di_l_orcu (2 dolmens distincts complexe Monte Revincu)' && \
git push -u origin feat/brief-39decies-d3-monte-revincu
```
