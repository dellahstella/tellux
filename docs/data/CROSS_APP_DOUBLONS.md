# Doublons cross-app `sites_em.json` ↔ `sites_patrimoine.json`

Date : 2026-05-07
Source : Brief 39decies (D1 dette technique, suite recap Code 28-39octies).

## Principe

Certains sites ont **deux dimensions** qui justifient leur présence dans les deux JSON :

- **Patrimoine** (`sites_patrimoine.json`) : valeur historique, MH, classement, axe_corpus défini
- **EM** (`sites_em.json`) : signature électromagnétique mesurable (anomalie magnétique minière, champ EM ouvrage industriel, anomalie géologique d'un sommet, etc.)

Ces doublons **ne sont pas des bugs** : c'est un choix architectural depuis Brief 33 (split EM/Patrimoine). Le même `slug` apparaît dans les deux fichiers avec des métadonnées propres à chaque dimension.

## Inventaire 2026-05-07 (19 doublons cross-app)

### Patrimoine naturel sacré × EM géologique (10)

Sommets, lacs, deserts, calanques, reserves : reliefs notables avec signature géologique/magnétique.

| Slug | Localisation |
|---|---|
| aiguilles_de_bavella | Massif Bavella |
| calanques_de_piana | Calanche de Piana |
| cap_corse_extreme_nord | Cap Corse |
| desert_des_agriate | Agriates |
| lac_de_creno | Cinto |
| lac_de_nino | Verde |
| monte_cinto | Sommet 2706m |
| monte_san_petrone | Sommet 1767m Castagniccia |
| monte_stello | Sommet 1307m Cap Corse |
| reserve_de_scandola | Reserve UNESCO |

### Patrimoine industriel × EM industriel (4)

Barrages hydrauliques : ouvrages XXe avec champs EM industriels mesurables.

| Slug | Localisation |
|---|---|
| barrage_alesani | Castagniccia |
| barrage_de_calacuccia | Niolo |
| barrage_du_rizzanese | Sartenais |
| barrage_padula | Castagniccia |

### Patrimoine divers × EM minier (4)

Mines historiques : valeur patrimoniale (MH) + anomalies magnétiques résiduelles ferreuses.

| Slug | Localisation | Notes |
|---|---|---|
| min_argentella | Calenzana | Brief 39bis Soleil |
| min_ersa | Ersa Cap | Brief 33 P1 |
| min_luri | Luri Cap | Brief 33 P1 |
| min_meria | Meria Cap | Brief 33 P1 |

### Patrimoine bâti × EM archéologique (1)

| Slug | Localisation |
|---|---|
| aleria_antique | Aléria - cité antique romaine sur cité néolithique |

## Convention de synchronisation

### Source canonique

**Patrimoine est la source canonique** pour les champs partagés : `lat`, `lon`, `gps_locked`, `gps_lock_reason`, `gps_audit`, `gps_source`, `commune_nom`, `doyenne_contemporain_slug`, `pieve_slug`.

### Champs propres à chaque fichier

**Patrimoine uniquement** :
- `axe_corpus`, `categorie`, `description`, `sources_originales`, `phase_publication`, `couleur`, `priorite`, `fiche_v3_slug`

**EM uniquement** :
- `axe_em`, `categorie_em`, `description_em`, `signal_em` (si présent), métriques EM spécifiques

### Procédure lors d'une modification cross-app

Quand un site cross-app reçoit une correction GPS (typiquement via `brief_pipeline.py`) :

1. Le pipeline Cowork écrit la correction dans **patrimoine** d'abord (source canon)
2. Un script de sync (à venir : `scripts/sync_cross_app.py`) propage `lat`, `lon`, `gps_*` vers em
3. Le `corpus_health_check.py` détecte toute divergence cross-app via l'invariant 9 et alerte

### Detection automatique

Le script `corpus_health_check.py` (Q2 Brief 39nonies) vérifie l'invariant **9 - Cross-app divergences** : si un slug est dans les deux JSON, les coords doivent être strictement identiques (tolérance < 0.001 degrés). Toute divergence remonte en warning.

## Historique des syncs cross-app

| Date | Brief | Action |
|---|---|---|
| 2026-05-07 | Brief 39nonies bonus | aleria_antique sync (em alignée sur patrimoine 42.1142/9.5131 post-Brief 39octies) |
| 2026-05-07 | Brief 39decies (D1) | Audit complet : 19 cross-app, 0 divergence détectée |

## Sites EM purs (non cross-app)

`sites_em.json` contient aussi 29 sites EM purs (présents uniquement dans em.json) qui n'ont pas de dimension patrimoniale forte mais ont une signature EM mesurable (anomalies isolées, points de mesure scientifiques). Ces sites ne sont pas des doublons et n'apparaissent pas ici.

## Risques identifiés

1. **Brief Cowork qui ne traite qu'un seul fichier** : si un brief modifie patrimoine sans propager à em, divergence. Mitigation : `corpus_health_check.py` invariant 9 + script sync futur.
2. **Suppression d'un slug cross-app dans un seul fichier** : crée un site orphelin. Mitigation : convention "supprimer dans les 2 fichiers en même temps".
3. **Slug renomme dans un seul fichier** : casse la correspondance cross-app. Mitigation : éviter renommage hors brief explicite.

## TODO futur

- Script `scripts/sync_cross_app.py` qui propage automatiquement patrimoine -> em (et flag les divergences)
- Champ `_cross_app: true` explicite dans les 2 JSON pour faciliter l'identification programmatique
- Documentation Code-side pour le moteur de rendu (savoir lequel des 2 markers afficher en niveau 1 si même position)
