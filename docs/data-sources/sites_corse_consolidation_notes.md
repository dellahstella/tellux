# SITES_CONSOLIDATION_AUDIT — Tellux Corse

**Date :** 2026-05-06
**Auteur :** Cowork (pipeline `consolidate_sites.py`)
**Brief :** Stop Point §6.1 validé 2026-05-06 — production étapes 2-10

## 1. Synthèse

- **Total sites canoniques :** 479
- **Phase 1 (exposée patrimoine.html) :** 191
- **Phase 2 (latente, churches_corse) :** 288
- **Doublons fusionnés :** 123 (sur 602 entrées brutes en entrée)
- **Couverture commune INSEE :** 411/479 (85%)
- **Couverture doyenné contemporain :** 411/479 (85%)
- **Couverture pieve médiévale :** 411/479 (85%)
- **Sites illustrés (visuel présent) :** 123/479
- **Sites prioritaires (mode Découverte) :** 11/479

## 2. Inventaire des sources d'entrée

| Source | Localisation | Entrées brutes | Statut |
|--------|--------------|----------------|--------|
| `SITES_PATRIMOINE` (inline) | `patrimoine.html` ligne 164 | 124 | ✅ intégrée |
| `SITES_REFERENCE.json` | racine repo | 115 | ✅ intégrée |
| `sites_corse` Supabase | DB | 115 | ✅ mirror exact de SITES_REFERENCE.json — fusion automatique |
| `churches_corse` Supabase | DB | 314 | ✅ intégrée (291 en Phase 2 latente) |
| `patrimoine_corse` Supabase | DB | 39 | ✅ intégrée (Tours, Châteaux, Thermes, Ponts, Mines) |
| `sites_remarquables_corse.json` | `public/data/` | 10 | ✅ intégrée avec sémantique EM préservée |
| `mega_studies` Supabase | DB | 83 | ⊘ exclue (corpus bibliographique, pas des sites) |

## 3. Catégories canonisées (Q2 arbitré 2026-05-06)

| axe_corpus | Catégorie display | Nb total | Phase 1 | Phase 2 |
|-----------|-------------------|---------:|--------:|--------:|
| `edifices_romans` | Édifice roman | 315 | 27 | 288 |
| `megalithes` | Mégalithique | 66 | 66 | 0 |
| `remarquables_geologiques` | Site naturel remarquable | 37 | 37 | 0 |
| `patrimoine_divers` | Patrimoine | 22 | 22 | 0 |
| `tours_genoises` | Tour génoise | 15 | 15 | 0 |
| `chateaux_medievaux` | Château médiéval | 8 | 8 | 0 |
| `hydrauliques` | Hydraulique | 6 | 6 | 0 |
| `patrimoine_bati_remarquable` | Patrimoine bâti remarquable | 5 | 5 | 0 |
| `diocese_medieval` | Diocèse historique | 5 | 5 | 0 |

**Renommages effectués (Q2) :**

- `Site remarquable` (5 entrées SITES_PATRIMOINE) → `Patrimoine bâti remarquable` / axe `patrimoine_bati_remarquable`
- `Remarquable` (29 SP + 34 SR) → `Site naturel remarquable` / axe `remarquables_geologiques`
- Toutes les variantes `B — Édifice roman tardif` etc. unifiées sous `Édifice roman` / axe `edifices_romans`
- `Pont génois`, `Thermalisme`, `Patrimoine & Ressources`, `Patrimoine` unifiés sous `Patrimoine` / axe `patrimoine_divers`

## 4. Déduplication

**Stratégie appliquée :**

1. Matching primaire : nom normalisé identique (lowercase, sans accents, sans articles `de/du/la/saint/santa/san`)
2. Matching secondaire : distance GPS ≤ 150 m + axes compatibles (matrice `AXIS_COMPAT`)
3. Priorité de source décroissante : `SITES_PATRIMOINE > sites_remarquables_corse > patrimoine_corse > SITES_REFERENCE/sites_corse_supabase > churches_corse`
4. Fusion enrichissante : tout champ non rempli sur le site canonique est complété par les alias
5. Toutes les sources d'origine listées dans `sources_originales[]`
6. Mapping complet alias → canonique persisté dans `_drafts/SITES_DEDUPLICATION_LOG.json`

**Résultats :**

- 602 entrées brutes consolidées en 479 sites canoniques (123 doublons éliminés)
- Couples ↔ confirmés : SITES_PATRIMOINE ∩ SITES_REFERENCE (~90), SITES_REFERENCE ≡ Supabase mirror (115), SITES_PATRIMOINE B-Édifice roman ∩ churches_corse (~18), SITES_PATRIMOINE ∩ patrimoine_corse Tours (~4)
- Aucun doublon trouvé entre `sites_remarquables_corse` et les autres sources (corpus 100% spécifique)

**Sites avec 2+ alias fusionnés (échantillon 10) :**

| Slug canonique | Nom | Sources fusionnées | Aliases |
|----------------|-----|--------------------|---------|
| `calanques_de_piana` | Calanques de Piana | SITES_PATRIMOINE, SITES_REFERENCE, sites_corse_supabase | Calanques de Piana (name_match, d=0.0m); Porto / Calanche (gps_proximity, d=0.0m) |
| `castello_della_rocca` | Castello della Rocca | SITES_PATRIMOINE, SITES_REFERENCE, patrimoine_corse, sites_corse_supabase | Castello della Rocca (name_match, d=0.0m); Castello della Rocca (name_match, d=0.0m) |

## 5. Audit GPS — corrections appliquées

### `cap_corse_extreme_nord`

- **Changement :** moved
- **Ancien GPS :** (42.982, 9.4)
- **Nouveau GPS :** (43.005, 9.395)
- **Source :** OSM / Wikidata Capu Bianchi (audit Tellux 2026-05-06)
- **Décision :** Q3 Stop Point §6.1, déplacé à la pointe physique extrême nord
- **Renommage :** `Cap Corse extrême nord` → `Capu Bianchi — extrême nord Cap Corse`
- **Vérification non-confusion :** distinct de la Tour d'Agnello et de l'île Giraglia (voir §6)

## 6. Cas ambigus rencontrés

### 6.1 Discrepance GPS Tour d'Agnello (à arbitrer dans une session ultérieure)

Trois coordonnées différentes coexistent pour la "Tour d'Agnello" :

| Source | Lat | Lon | Distance vs Capu Bianchi |
|--------|-----|-----|--------------------------|
| `patrimoine_corse` Supabase id=2 | 42.973 | 9.355 | ~5,2 km SW |
| `SITES_REFERENCE` id correspondant | 42.973 | 9.415 | ~3,7 km SE |
| GPS de référence cité par Soleil 2026-05-06 | 43.00917 | 9.4225 | ~2,7 km E |

La pipeline a fusionné les deux premiers (matching nom). La référence Soleil n'est pas dans le corpus actuel.
**Action recommandée :** audit GPS dédié Tour d'Agnello dans une prochaine session avec source documentée (BRGM Mérimée, OSM, photo-aérienne).

### 6.2 Hameaux et lieux-dits dans `churches_corse` non résolus en INSEE

Plusieurs églises sont localisées sur des hameaux (Vizzavona, Pietrapola, Folelli, Sagone, Lozari, Castelluccio…) qui ne sont pas des communes INSEE distinctes.
Le `lieu` est conservé dans `commune_nom` mais `commune_insee = null`.
**Action recommandée Phase 2 :** override JSON manuel (`_drafts/sites_corse_overrides.json`) à compléter avant ouverture Phase 2 churches.

### 6.3 Sites mégalithiques sans toponyme communal

Une vingtaine de mégalithes du `SITES_REFERENCE.json` portent des noms en corse ancien sans rattachement communal explicite (Scalsa Murta, U Cantonu, U Paladinu, Sposata, Tappa torre…).
**Action recommandée :** audit ponctuel par croisement coordonnées GPS / contour communal (futur point-in-polygon avec contours communes Corse — non disponible v1).

## 7. Orphans `commune_insee = null` (synthèse)

Total : 68 orphans sur 479 sites (14%).

**Catégorisation :**

- **5 intentionnels — Diocèses historiques** : abstractions géographiques (Ajaccio, Aleria, Mariana, Sagone, Nebbio). `commune_insee = null` est correct, le centroïde GPS est conservé.
- **7 sites naturels transcommunaux** : Aiguilles de Bavella, Désert des Agriate, Gorges du Spelunca, Monte Cinto/d'Oro/Renoso/San Petrone, Plateau du Coscione, Forêt de Vizzavona, Défilé de Lancône, Capu Bianchi, Anneaux du Cap Corse, Casa di u Banditu, Mamucci, Monte Genova mégalithes. Sites légitimement transcommunaux ou marins.
- **56 à résoudre manuellement** : voir §6.1, §6.2, §6.3 ci-dessus. Liste exhaustive dans `_drafts/SITES_DEDUPLICATION_LOG.json` (champ `notes`).

## 8. Liste exhaustive des 56 orphans à résoudre

| Nom | axe_corpus | Sources | Action recommandée |
|-----|-----------|---------|---------------------|
| Barrage du Rizzanese | `hydrauliques` | SITES_PATRIMOINE, SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Barrage Padula | `hydrauliques` | SITES_PATRIMOINE, SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Tour génoise Chiappa | `tours_genoises` | SITES_REFERENCE, patrimoine_corse, sites_corse_supabase | Audit BRGM/Mérimée + override |
| Tour d'Agnello (Cap Corse) | `tours_genoises` | SITES_REFERENCE, patrimoine_corse, sites_corse_supabase | Audit BRGM/Mérimée + override |
| Tour de la Mortella | `tours_genoises` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Tour de Giraglia (îlot) | `tours_genoises` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Tour de Turghiu (Capo Rosso) | `tours_genoises` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Tour de Capitello (Castelluccio) | `tours_genoises` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Tour d'Isolella (Sette Navi) | `tours_genoises` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Tour de Capo di Muro | `tours_genoises` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Pont de Zippitoli (disparu 2023) | `patrimoine_divers` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Thermes de Baracci | `patrimoine_divers` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Sources de Guitera | `patrimoine_divers` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Lac thermal de Tora | `patrimoine_divers` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Pietrapola (station thermale) | `patrimoine_divers` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Castello di Baricci | `chateaux_medievaux` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Castello d'Istria | `chateaux_medievaux` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Castellu di u Grecu | `chateaux_medievaux` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Castellu d'Itali | `chateaux_medievaux` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Castellacciu San Colombano | `chateaux_medievaux` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Castellu di Bozzi (Guitera) | `chateaux_medievaux` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Pont de Ponte Novu | `patrimoine_divers` | patrimoine_corse | Audit BRGM/Mérimée + override |
| Timozzolo menhirs | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Scalsa Murta | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Statues-menhirs de Sagone | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Stantara d'Apricciani | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| U Paladinu | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Statue-menhir Santa Naria | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| U Cantonu | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Barrage Ospedale | `hydrauliques` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Tivulaggio alignement | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Tizzarella menhirs | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Sant Andria menhirs | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Torre de Tozzu / Torre de Tusiu | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Tappa torre | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Uomo di Cagna | `remarquables_geologiques` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Sposata (menhir penché) | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Cascades du Voile de la mariée | `remarquables_geologiques` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Capula torre | `megalithes` | SITES_REFERENCE, sites_corse_supabase | Point-in-polygon contour commune (Phase 2) |
| Santa Maria (Pietrapola) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| Santa Maria (Vizzavona) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| Santa Maria di e Grazie (Sagone littoral) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Giovanni (Vizzavona village) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| Santa Maria (Favone) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| Santa Maria (Folelli) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| Santa Maria (Moriani-Plage haute) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Quilicu (Prunete village) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Giovanni (Zeloso) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Giuliano (Cuttoli haute) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Petru (Vallerustie village) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Cipriano (Sagone basse) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| Sant'Appiano fils (Vico golfe) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Pietro (Lozari) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Quilicu (Castagniccia-Opino) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Giovanni (Vizzavona bas) | `edifices_romans` | churches_corse | Override JSON hameau→commune |
| San Giovanni (Serrabone) | `edifices_romans` | churches_corse | Override JSON hameau→commune |

## 9. Schéma JSON cible — version définitive

Champs obligatoires sur tous les sites : `slug`, `nom`, `lat`, `lon`, `categorie`, `axe_corpus`, `phase_publication`, `illustre`, `sources_originales[]`.

Champs optionnels (peuvent être null/empty selon catégorie) : `description`, `commune_insee`, `commune_nom`, `pieve_slug`, `diocese_medieval_slug`, `doyenne_contemporain_slug`, `visuel`, `version_visuel`, `priorite`, `couleur`, `description_em`, `gps_source`, `gps_audit`, `notes`.

**Adaptations vs brief (validées Q4 Stop Point §6.1) :**

- `priorite: bool` ajouté (issu de SITES_PATRIMOINE — utile mode Découverte)
- `couleur: string?` ajouté (présent dans SITES_REFERENCE et patrimoine_corse — facultatif si runtime calcule depuis `categorie`)
- `description_em: object?` ajouté (sémantique riche de sites_remarquables_corse — `signature_em`, `impact_modele`, etc. préservée)
- `gps_audit` au format ISO `YYYY-MM-DD`

## 10. Fichiers livrés

Tous dans `_drafts/` (pas d'intégration runtime sans Brief 28) :

- `_drafts/sites_corse_v1.json` — corpus consolidé final (479 sites, 479 entrées, format JSON compact UTF-8)
- `_drafts/SITES_DEDUPLICATION_LOG.json` — mapping complet `{slug_canonique → [aliases]}` (121 sites avec doublons fusionnés)
- `_drafts/SITES_CONSOLIDATION_AUDIT.md` — ce fichier

## 11. Prochaines actions (hors périmètre Brief actuel)

1. **Brief 28 (intégration repo)** — Soleil pousse `sites_corse_v1.json` vers `public/data/sites_corse.json`, met à jour `patrimoine.html` pour fetch + filtrer `phase_publication === 1`
2. **Override JSON hameaux** (à créer) — résoudre les ~17 hameaux churches_corse non rattachables auto à une commune INSEE
3. **Audit GPS Tour d'Agnello** — arbitrer entre les 3 coords (42.973/9.355, 42.973/9.415, 43.00917/9.4225)
4. **Polygones communes Corse (GeoJSON)** — pour résoudre par point-in-polygon les ~22 sites SITES_REFERENCE/patrimoine_corse sans toponyme
5. **Phase 2 enrichissement** — descriptions, visuels, orientations astrales pour les 291 churches latentes (au moment de l'ouverture Phase 2)

---

_Stop Point §6.2 obligatoire avant intégration repo. Soleil arbitre._