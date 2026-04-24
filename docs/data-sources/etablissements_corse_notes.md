# Établissements sensibles Corse — note de data source

**Fichiers :**
- `public/data/corse/ecoles.geojson`
- `public/data/corse/medicosocial.geojson`
- `public/data/corse/eaje.geojson` (vide en v1, voir ticket EAJE-CORSE-001)

**Date d'extraction :** 2026-04-24 (version 1.0)
**Pipeline producteur :** `scripts/build_etablissements_corse.py`
**Origine :** livrable Cowork du 2026-04-24 `tellux_mairies_datasets/`, exécuté et corrigé par Claude Code le 2026-04-24 (voir `DATASETS_PATCH_COWORK_FIX.md`).
**Statut :** données ANFR-équivalentes administratives, coordonnées précises à l'adresse pour Annuaire Éducation et FINESS (après conversion Lambert 93 → WGS84), pas de source pour EAJE.

---

## 1. Résumé volumétrique

| Fichier | Features | Taille | Catégorie |
|---|---|---|---|
| `ecoles.geojson` | 331 | 143 KB | Enseignement |
| `medicosocial.geojson` | 80 | 33 KB | Médico-social et sanitaire |
| `eaje.geojson` | 0 | 1 KB | Petite enfance (vide, voir §5) |

Total : 411 établissements, 177 KB, bien sous la limite de 3 MB.

**Répartition Enseignement** : 152 écoles primaires + 51 maternelles + 47 élémentaires + 46 collèges + 11 lycées polyvalents + 9 lycées généraux + 5 lycées professionnels + 1 EREA + 9 autres.

**Répartition Médico-social** : 30 EHPAD + 20 centres hospitaliers + 10 MAS + 5 IME + 4 CHS + 4 services d'accompagnement médico-social adultes + 2 ITEP + 2 IEM + 1 SESSAD + 1 FAM + 1 clinique privée.

**Top 5 communes** : Ajaccio 66, Bastia 57, Porto-Vecchio 18, Corte 11, Bonifacio 10.

---

## 2. Sources officielles

| Source | Producteur | URL | Licence |
|---|---|---|---|
| Annuaire de l'éducation | Ministère de l'Éducation nationale | https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/ | Etalab 2.0 |
| FINESS | DREES | https://www.data.gouv.fr/datasets/finess-extraction-du-fichier-des-etablissements | Etalab 2.0 |
| Contours communaux (reconstitution code INSEE) | IGN AdminExpress via geo.api.gouv.fr | https://geo.api.gouv.fr/communes | Licence Ouverte IGN |

Attribution obligatoire en cas de réutilisation. Présente dans les métadonnées des GeoJSON produits.

**Pour FINESS :** ressource retenue = `etalab-cs1100507-stock-*.csv` ("Extraction Finess des Etablissements géolocalisés") et non `cs1100502` qui ne contient pas les coordonnées.

**Coordonnées FINESS :** fournies en Lambert 93 (EPSG:2154 RGF93 / Lambert-93 Métropole), converties en WGS84 (EPSG:4326) par le pipeline Tellux via formules IGN NTG-71 / ALG0004 en Python pur. Précision : identique à pyproj au centimètre près.

---

## 3. Schéma commun des features

Chaque fichier est une `FeatureCollection` GeoJSON standard, WGS84 (EPSG:4326), UTF-8 sans BOM, coordonnées à 6 décimales.

```json
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [lon, lat] },
  "properties": {
    "id": "identifiant_source_stable",
    "nom": "Nom de l'etablissement",
    "categorie": "enseignement | medico-social | petite-enfance",
    "sous_categorie": "ecole_maternelle | college | ehpad | ...",
    "adresse": "Numero et voie ou null",
    "code_postal": "20000 ou null",
    "commune": "Ajaccio ou null",
    "code_insee": "2A004 ou null",
    "secteur": "public | prive_sous_contrat | prive_hors_contrat | null",
    "source": "annuaire_education | finess | eaje_caf",
    "date_extraction": "YYYY-MM-DD"
  }
}
```

Un bloc `metadata` en tête de chaque FeatureCollection précise `source`, `date_extraction`, `licence`, `projection`, `attribution`.

Pour `eaje.geojson`, le bloc `metadata` contient en plus `status: "empty_no_source"`, une `coverage_note` documentant l'absence de source nationale, et `ticket: "EAJE-CORSE-001"`.

---

## 4. Procédure de refresh

### 4.1 Cadence recommandée

Refresh **mensuel** : lancer `python scripts/build_etablissements_corse.py --output public/data/corse --verbose` le premier lundi du mois. Durée réelle observée : 2 minutes (téléchargement CSV FINESS = 45 Mo + API Éducation paginée).

Après régénération, renommer les sorties selon la convention courte si `--output` n'est pas directement `public/data/corse/` :

    output/etablissements_enseignement_corse.geojson  -> public/data/corse/ecoles.geojson
    output/etablissements_medicosocial_corse.geojson  -> public/data/corse/medicosocial.geojson
    output/etablissements_petite_enfance_corse.geojson -> public/data/corse/eaje.geojson

### 4.2 Bascule FINESS été 2026

**Alerte calendrier.** La DREES a annoncé une nouvelle version de FINESS à l'été 2026 avec arrêt du flux actuel. Veille à programmer entre juin et septembre 2026 :

1. Consulter [DREES FINESS](https://drees.solidarites-sante.gouv.fr/sources-outils-et-enquetes/le-fichier-national-des-etablissements-sanitaires-et-sociaux-finess) entre le 1er juin et le 1er septembre 2026.
2. Adapter `download_finess()` au nouveau schéma si nécessaire (colonnes, encoding, séparateur, type de ligne).
3. Réviser `MAPPING_FINESS` à la lumière de la nomenclature mise à jour.

### 4.3 EAJE : ticket ouvert

Le fichier `eaje.geojson` est vide en v1. Avant la Passe 2 du chantier Fiche commune de `mairies.html`, trancher selon le ticket `docs/tickets/EAJE-CORSE-001.md` :

- soit une source géolocalisée est trouvée et intégrée au pipeline,
- soit `mairies.html` affiche explicitement "donnée EAJE non disponible pour cette commune, voir CAF de Corse" dans le bloc Établissements sensibles.

---

## 5. Limites connues

### 5.1 Sur l'Annuaire Éducation

- **Volumétrie (331)** : légèrement sous la fourchette Cowork (400-550), mais cohérente avec le nombre brut retourné par l'API (350 sans filtrage hors périmètre sensible).
- **Géolocalisation** : bonne en ville, dégradée en rural (centroïde communal plutôt qu'adresse exacte sur quelques établissements).
- **9 features en `sous_categorie: "autre"`** : correspondent à des types `type_etablissement` non classifiés par l'heuristique `_derive_sous_cat_education` (ex. SEP, annexes). Acceptable en v1.
- **1 rejet** `no_coordinates` : école Annuaire Éducation sans géoloc dans la source.

### 5.2 Sur FINESS

- **Mapping `categetab`** : les 21 codes couverts par `MAPPING_FINESS` (EHPAD, USLD, MAS, FAM, IME, ITEP, IEM, SESSAD, CHU, CH, CHS, clinique privée, centre de lutte contre le cancer, etc.) sont issus de la nomenclature DREES connue et arbitrés par Cowork (voir `DATASETS_PATCH_COWORK.md` §P3). Les lignes Corse dont le code n'est pas dans le mapping sont **ignorées silencieusement** (hors périmètre Loi Abeille : pharmacies, laboratoires, cabinets libéraux).
- **Codes fréquemment ignorés en Corse** (depuis logs verbose) : 620 (127 occurrences), 460 (72), 611 (25), 603 (22), 156 (19), 425 (11), etc. Candidats pour v2 si pertinents : 156 (SSR) et 108 (CHR) mentionnés dans le patch Cowork.
- **Précision géolocalisation** : source ATLASANTE / BAN / IGN BDADRESSE selon les établissements, précision généralement à la rue.
- **Volumétrie (80)** : dans la fourchette Cowork 60-120.
- **0 rejet** `coords_not_wgs84` après conversion Lambert 93 → WGS84.

### 5.3 Sur EAJE

Voir ticket [EAJE-CORSE-001](../tickets/EAJE-CORSE-001.md). Pas de source nationale géolocalisée open data. Les assistantes maternelles individuelles sont hors périmètre (pas de référentiel open data).

---

## 6. Exclusions volontaires

- **Pharmacies, laboratoires de biologie médicale, cabinets libéraux** : exclus du dispositif sensible au sens Loi Abeille.
- **Assistantes maternelles individuelles** : hors périmètre (accueil individuel non visé par la règle des 100 mètres).
- **Services administratifs, services d'orientation** : hors périmètre enseignement sensible.

---

## 7. Documents de référence

- [DATASETS_PATCH_COWORK_FIX.md](../../DATASETS_PATCH_COWORK_FIX.md) — trace détaillée des 6 corrections appliquées au script Cowork.
- [docs/tickets/EAJE-CORSE-001.md](../tickets/EAJE-CORSE-001.md) — ticket ouvert pour la source EAJE.
- `tellux_mairies_datasets/README_DATASETS_CORSE.md` (hors repo public) — documentation Cowork initiale.
- `tellux_mairies_datasets/DATASETS_PATCH_COWORK.md` (hors repo public) — décisions de design Cowork.
- `tellux_mairies_datasets/COWORK_SESSION_RECAP.md` (hors repo public) — récap livraison Cowork.

---

Fin de la note.
