# Rapport de session — Brief 33 split data app/patrimoine

Date : 2026-05-06
Périmètre : découplage `sites_corse.json` en `sites_em.json` (app.html) + `sites_patrimoine.json` (patrimoine.html).

## Livrables Cowork (worktree `distracted-cohen-9850e9`)

| Fichier | Taille | Sites | Statut |
|---|---|---|---|
| `docs/data/sites_em.json` | 33 KB | 43 | nouveau |
| `docs/data/sites_patrimoine.json` | 389 KB | 437 (= 436 + 1 doublon Aléria) | nouveau |
| `docs/data/sites_corse.json` | 441 KB | 479 | inchangé sur le contenu, marqué `_DEPRECATED` en tête |
| `_drafts/sites_doublons_em_patrimoine.md` | 5 KB | n/a | nouveau, doc de doublons |

## Inventaire effectué (Étape 1)

Source : `docs/data/sites_corse.json` worktree (479 sites Brief 27 canon, post Brief 32 cleanup).

Distribution par `axe_corpus` :

- `edifices_romans` : 315
- `megalithes` : 66
- `remarquables_geologiques` : **37 (EM)**
- `patrimoine_divers` : 22
- `tours_genoises` : 15
- `chateaux_medievaux` : 8
- `hydrauliques` : **6 (EM)**
- `patrimoine_bati_remarquable` : 5
- `diocese_medieval` : 5

**Total EM** = 37 + 6 = **43 sites** (cohérent avec Brief 29).
**Total patrimoine** = 479 - 43 = **436 sites**.

## Schémas appliqués

### sites_em.json

Champs conservés (per site) : `slug`, `name`, `lat`, `lon`, `axe_em` (renommé depuis `axe_corpus`), `categorie_em`, `commune_insee`, `commune_nom`, `description_em`, `priorite`, `phase_publication`, `gps_source`, `gps_audit`, `sources_originales`, `notes`.

Champs **retirés** (présents dans sites_corse.json mais absents de sites_em.json) : `pieve_slug`, `diocese_medieval_slug`, `doyenne_contemporain_slug`, `visuel`, `illustre`, `version_visuel`, `couleur`. Ces champs ne sont pas pertinents pour la couche EM de `app.html`.

`_meta.axes_em_referentiel` : `["hydrauliques", "remarquables_geologiques"]`.

### sites_patrimoine.json

Champs conservés : `slug`, `name`, `lat`, `lon`, `axe_corpus`, `categorie`, `commune_insee`, `commune_nom`, `pieve_slug`, `diocese_medieval_slug`, `doyenne_contemporain_slug`, `description`, `visuel`, `illustre`, `version_visuel`, `priorite`, `couleur`, `phase_publication`, `gps_source`, `gps_audit`, `sources_originales`, `notes`.

Champs **ajoutés** : `fiche_v3_slug` (optionnel, lien vers `fiches_patrimoine/sites/<slug>_v3.md` pour la carte postale Brief 31). Pour l'instant, 1 seul site renseigné : `aleria_antique` → `aleria_ruine`.

Champs **retirés** : `description_em`. Cohérent avec la dimension exclusivement patrimoniale.

`_meta.axes_corpus_referentiel` : `["edifices_romans", "megalithes", "tours_genoises", "chateaux_medievaux", "patrimoine_divers", "patrimoine_bati_remarquable", "diocese_medieval"]`.

## Doublons appliqués (vague initiale)

**1 seul doublon** appliqué : `aleria_antique`.

- Dans `sites_em.json` : axe `remarquables_geologiques` (plateau ophiolitique).
- Dans `sites_patrimoine.json` : axe `patrimoine_bati_remarquable`, `fiche_v3_slug='aleria_ruine'`, champ trace `_doublon_em` ajouté.
- Slug identique (`aleria_antique`) dans les deux fichiers — fichiers distincts donc pas de collision JSON.
- Coordonnées identiques.

## Doublons à arbitrer (vagues ultérieures)

Identifiés et listés dans `_drafts/sites_doublons_em_patrimoine.md` :

- **Sites naturels sacrés** (10 candidats : Aiguilles de Bavella, Monte San Petrone, lacs Nino/Creno, Cinto, Cap Corse extrême nord, Désert des Agriate, Calanques de Piana, Scandola, Monte Stello).
- **Mégalithiques sur affleurement** (4 : Filitosa, Palaggiu, Cauria, Cucuruzzu-Capula) — actuellement seulement dans sites_patrimoine.json, à dupliquer dans sites_em.json si Brief 29 EM doit les inclure.
- **Barrages hydrauliques** (4 : Alesani, Calacuccia, Rizzanese, Padula) — actuellement seulement dans sites_em.json, à dupliquer dans sites_patrimoine.json si Brief 27 patrimoine industriel doit les inclure.
- **Citadelles génoises** (4 : Bastia, Bonifacio, Calvi, Corte) — toutes dans sites_patrimoine.json, dimension EM sur substrat minéral pertinente, à dupliquer si Brief 29 doit les inclure (Bonifacio sur calcaire, Corte sur ophiolites = singularités EM majeures).

Total : ~22 candidats à arbitrer ligne par ligne par Soleil dans une vague ultérieure.

## Marquage DEPRECATED

`docs/data/sites_corse.json` conserve son contenu (479 sites, fusion Bastia → Cap, visuels sans extension) mais reçoit en tête un champ `_DEPRECATED` :

```
"Ce fichier est obsolète depuis Brief 33 split (2026-05-06). Les sites EM ont migré
vers docs/data/sites_em.json (43 sites). Les sites patrimoniaux ont migré vers
docs/data/sites_patrimoine.json (437 sites, dont 1 doublon Aléria). Sera supprimé
30 jours après split confirmé en prod (target : 2026-06-05)."
```

Le fichier reste accessible pour rollback. Aucune référence runtime ne doit subsister après migration Code.

## Statut tâches Cowork

- ✅ Étape 1 — Inventaire (43 EM / 436 patrimoine / 1 doublon Aléria identifié, ~22 doublons candidats listés).
- ✅ Étape 2 — `sites_em.json` généré (43 sites).
- ✅ Étape 3 — `sites_patrimoine.json` généré (437 sites, 1 fiche_v3_slug renseigné).
- ✅ Étape 4 — Marquage `_DEPRECATED` sur sites_corse.json.
- ✅ Étape 5 — Doc doublons `_drafts/sites_doublons_em_patrimoine.md` créée.

Tout est dans le worktree `.claude/worktrees/distracted-cohen-9850e9/`, prêt à propagation manuelle vers main.

## Durée

Session ponctuelle Cowork. Inventaire + scripts Python + doc en série. ~1h.
