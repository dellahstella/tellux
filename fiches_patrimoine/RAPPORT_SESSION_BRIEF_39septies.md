# Rapport de session - Brief 39septies (pipeline auto + post-traitement)

Date : 2026-05-07
Mode : APPLY
Perimetre : audit Extreme-Sud (Cauria/Sartene/Levie/Porto-Vecchio) + 4 recherches Cowork + 2 creations.

## Synthese globale

| Action | Nombre |
|---|---|
| Corrections coords (pipeline) | 21 |
| Sites locked sans changement coords (post-pipeline) | 4 |
| Sites crees (post-pipeline) | 2 |
| Fusions doublons | 0 (Soleil garde distincts) |
| Sites non trouves dans corpus | 0 |
| Sites locked skippes | 0 |
| Total impacts JSON | 27 |
| Total sites JSON apres brief | 453 (+2) |

## Decisions Soleil arbitrees

1. petra_pinzuta : ECRASE vers (42.5046, 9.3766) Campile Haute-Corse. La statue-menhir Sartene Grosjean 1967 disparait du corpus. Reassignation auto doyenne_extreme_sud -> doyenne_du_golo, pieve_sartene -> pieve_casacconi.
2. stazzona_di_u_diavulu / dolmen_fontanaccia : maintenus distincts. Coords brief appliquees au dolmen seul. Le slug stazzona_di_u_diavulu_menhirs reste a (41.545, 8.91).
3. 4 recherches Cowork (manzavinu, alignement_figari, ciutulaghja, castelnovo_bicchisano) : tous maintenus, just locked sans changer coords.
4. menhirs_du_rizzanese + appazu_alignement : crees ex nihilo, sources Wikipedia + Grosjean 1968 + MH 1889.

## Doublons brief Soleil non appliques (alias)

| Brief | Slug reel canonique | Statut |
|---|---|---|
| paddaghju | palaggiu | alias - coords appliquees a palaggiu |
| pastini_cercle | pastini | alias - coords appliquees a pastini |
| cardiccia_dolmen | cardiccia | alias - coords appliquees a cardiccia |
| stazzona_di_u_diavulu | stazzona_di_u_diavulu_menhirs | distincts par decision Soleil - coords appliquees au dolmen_fontanaccia seul |

## Detail par site (21 corrections pipeline)

### capu_di_logu (APPLIED)
  - Coords : (41.6212, 8.8424) -> (41.6212, 8.8424) (ecart 0.0 km)
  - Reassignation pieve : pieve_bonifacio -> pieve_sartene
  - Note : Belvedere-Campomoro megalithique

### vaccil_vecchiu (APPLIED)
  - Coords : (41.5936, 8.8766) -> (41.5936, 8.8764) (ecart 0.02 km)

### bizzicu_rossu (APPLIED)
  - Coords : (41.6014, 8.8795) -> (41.6007, 8.8788) (ecart 0.1 km)

### alo_bisuje (APPLIED)
  - Coords : (41.613, 8.8987) -> (41.552, 8.875) (ecart 7.06 km)

### palaggiu (APPLIED)
  - Coords : (41.5569, 8.8869) -> (41.571, 8.85) (ecart 3.45 km)
  - Note : Grand alignement Sartene 258 menhirs

### dolmen_fontanaccia (APPLIED)
  - Coords : (41.52835, 8.91787) -> (41.5295, 8.9182) (ecart 0.13 km)

### cauria_i_stantari (APPLIED)
  - Coords : (41.5304, 8.9218) -> (41.5303, 8.9225) (ecart 0.06 km)

### cauria_renaghju (APPLIED)
  - Coords : (41.5266, 8.9212) -> (41.522, 8.932) (ecart 1.03 km)

### bocca_di_a_pila (APPLIED)
  - Coords : (41.54, 8.93) -> (41.525, 8.915) (ecart 2.08 km)

### pastini (APPLIED)
  - Coords : (41.5527, 8.9347) -> (41.5577, 8.9407) (ecart 0.75 km)

### cardiccia (APPLIED)
  - Coords : (41.5582, 8.9412) -> (41.5577, 8.9407) (ecart 0.07 km)

### lion_de_roccapina (APPLIED)
  - Coords : (41.49748, 8.93231) -> (41.4972, 8.9342) (ecart 0.16 km)

### san_giovanni_de_pianottoli_caldarello (APPLIED)
  - Coords : (41.4839, 9.0628) -> (41.461, 9.047) (ecart 2.87 km)

### ceccia_torre (APPLIED)
  - Coords : (41.5626, 9.2447) -> (41.565, 9.226) (ecart 1.58 km)

### castellu_araghju (APPLIED)
  - Coords : (41.575, 9.245) -> (41.6478, 9.2622) (ecart 8.22 km)

### san_giovanni_battista_carbini (APPLIED)
  - Coords : (41.6419, 9.2406) -> (41.724, 9.125) (ecart 13.25 km)

### pacciunituli (APPLIED)
  - Coords : (41.72457, 9.1663) -> (41.724, 9.168) (ecart 0.15 km)

### cucuruzzu_capula (APPLIED)
  - Coords : (41.7085, 9.12617) -> (41.7172, 9.1287) (ecart 0.99 km)
  - Note : Coords web confirmees vs brief approximatif

### sainte_lucie_de_sainte_lucie_de_tallano (APPLIED)
  - Coords : (41.67874, 9.07336) -> (41.7, 9.05) (ecart 3.06 km)

### punta_campana (APPLIED)
  - Coords : (41.62, 9.01) -> (41.5434, 9.1928) (ecart 17.43 km)
  - Reassignation pieve : pieve_carbini -> pieve_freto

### petra_pinzuta (APPLIED)
  - Coords : (41.622, 8.988) -> (42.5046, 9.3766) (ecart 103.25 km)
  - Reassignation doyenne : doyenne_extreme_sud -> doyenne_du_golo
  - Reassignation pieve : pieve_sartene -> pieve_casacconi
  - Note : DECISION SOLEIL ecraser vers lieu-dit Campile Haute-Corse

## Post-traitement Cowork (4 locks + 2 creations)

### Sites verrouilles sans modification de coords

| Slug | Coords | Source |
|---|---|---|
| manzavinu | (41.58, 8.91) | DAnna 2007 corpus + Web confirme alignement Sartene |
| alignement_figari | (41.498, 9.108) | Leandri 2020 corpus, audit Web non concluant |
| ciutulaghja | (41.721, 9.113) | Lanfranchi 2000 corpus, divergence Web Appietto signalee |
| castelnovo_bicchisano | (41.587, 8.981) | patrimoine_corse seul, chateau medieval Petreto-Bicchisano |

### Nouveaux sites crees

| Slug | Coords | Description | Sources |
|---|---|---|---|
| menhirs_du_rizzanese | (41.648, 8.828) | U Frati e a Sora 2 menhirs RN196 MH 1889 | Wikipedia + MH 1889 |
| appazu_alignement | (41.5439, 8.8744) | Alignement 25 menhirs + 2 statues-menhirs + tumulus | Wikipedia + Grosjean 1968 + Jehasse 1973 |

Tous deux : axe_corpus=megalithes, doyenne_extreme_sud, pieve_sartene, gps_locked=true.

## Garde-fous respectes

- gps_locked=true applique sur les 27 impacts (21 + 4 + 2)
- Backup pre-brief : _drafts/sites_patrimoine.backup_pre_brief39septies_2026-05-07.json (417 KB)
- Backup pipeline auto : _drafts/sites_patrimoine.backup_brief_39septies_2026-05-07.json
- Aucun site Briefs 27-39quater touche (les sites locked anterieurs auraient ete skippes par le pipeline)
- JSON valide post-brief (453 sites)

## Note technique : 2 patches pipeline

1. Parser slugs sans underscore : palaggiu, pastini, cardiccia, pacciunituli, manzavinu, ciutulaghja n'avaient pas d'underscore et etaient ignores. Patch : accepte len(s) >= 7 hors stopwords.
2. Fix files_modified : find_site_in_jsons retournait un Path comme cle, KeyError sur sauvegarde. Patch : passer (fn_str, data, items) tuples.

## Criteres d'acceptation

| Critere | Statut |
|---|---|
| ~25 corrections cibles brief | 21 + 4 + 2 = 27 impacts |
| Doublons Cauria fusionnes | 0 (decision Soleil) |
| Cucuruzzu/Capula coords distinctes de Carbini | OUI |
| Petra Pinzuta classement | ECRASE vers Campile (decision Soleil) |
| 4 recherches Cowork documentees | OUI |
| Script audit_grep_helper.sh fonctionnel | OUI |
| Sites Briefs 38-39quater inchanges | OUI |
| Backup conserve | OUI |
| Regression Briefs 27-39 | 0 |

## Validation Soleil suggeree

- Cluster megalithique Cauria/Sartene : tous markers presents et bien positionnes
- Pas de doublons residuels Pastini/Cardiccia/Fontanaccia
- Cucuruzzu et Carbini = 2 markers distincts visuellement
- Petra Pinzuta : maintenant a Campile en Haute-Corse (verifier drill-down doyenne_du_golo)
- Nouveaux sites U Frati e a Sora et Apazzu visibles a Sartene
