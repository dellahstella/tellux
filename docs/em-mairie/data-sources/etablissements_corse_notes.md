# Établissements sensibles Corse — note de data source

**Fichiers :**
- `public/data/corse/ecoles.geojson`
- `public/data/corse/medicosocial.geojson`
- `public/data/corse/eaje.geojson` (alimenté en v2 depuis OSM, ticket EAJE-CORSE-001 résolu en scénario B)

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
| `eaje.geojson` | 15 | 10 KB | Petite enfance (OSM, couverture partielle, voir §5) |

Total : 426 établissements, 186 KB, bien sous la limite de 3 MB.

**Répartition Enseignement** : 152 écoles primaires + 51 maternelles + 47 élémentaires + 46 collèges + 11 lycées polyvalents + 9 lycées généraux + 5 lycées professionnels + 1 EREA + 9 autres.

**Répartition Médico-social** : 30 EHPAD + 20 centres hospitaliers + 10 MAS + 5 IME + 4 CHS + 4 services d'accompagnement médico-social adultes + 2 ITEP + 2 IEM + 1 SESSAD + 1 FAM + 1 clinique privée.

**Top 5 communes** : Ajaccio 66, Bastia 57, Porto-Vecchio 18, Corte 11, Bonifacio 10.

---

## 2. Sources officielles

| Source | Producteur | URL | Licence |
|---|---|---|---|
| Annuaire de l'éducation | Ministère de l'Éducation nationale | https://data.education.gouv.fr/explore/dataset/fr-en-annuaire-education/ | Etalab 2.0 |
| FINESS | DREES | https://www.data.gouv.fr/datasets/finess-extraction-du-fichier-des-etablissements | Etalab 2.0 |
| OpenStreetMap (EAJE) | Contributeurs OSM | Overpass API https://overpass-api.de/api/interpreter | ODbL 1.0 |
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

### 4.3 EAJE : OSM (ticket EAJE-CORSE-001 clos en scénario B)

Le fichier `eaje.geojson` est alimenté depuis OpenStreetMap via le script dédié `scripts/build_eaje_osm_corse.py` (séparé du pipeline FINESS / Annuaire Éducation pour respecter la cadence différente d'OSM).

**Cadence recommandée :** trimestrielle (OSM évolue continuellement, mais pas besoin du mensuel des autres sources).

**Commande :**

```bash
python scripts/build_eaje_osm_corse.py --output public/data/corse --verbose
```

Le script POSTe une requête Overpass filtrant `amenity=kindergarten` et `amenity=childcare` sur les areas ISO3166-2 FR-2A et FR-2B, convertit chaque feature au schéma Tellux, fait du reverse-géocodage via `geo.api.gouv.fr/communes` pour obtenir code INSEE et commune (les tags OSM `addr:*` étant absents sur les features Corse à la date de cette extraction).

**Volumétrie initiale (25 avril 2026) :** 15 features valides (11 sur 2B + 4 sur 2A), 1 rejetée (anomalie de tagging filtrée, voir §5.3). Couverture estimée 25 % du total attendu (60 EAJE Corse). Voir `docs/tickets/EAJE-CORSE-001.md` pour le détail de la résolution.

**Garde-fou :** si le delta de feature_count dépasse 50 % vs la version précédente, ne pas écraser le fichier sans validation manuelle (l'OSM peut perdre des nodes par vandalisme ou erreur de tagging).

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

### 5.3 Sur EAJE (OSM)

**Source :** OpenStreetMap, tags `amenity=kindergarten` et `amenity=childcare`, licence ODbL 1.0, attribution « © OpenStreetMap contributors ».

**Couverture estimée 25 %** sur la base d'un total attendu de 60 EAJE en Corse (45 documentés en 2B par schéma départemental 2020 + ~15 en 2A par extrapolation démographique). L'écart entre les estimations Cowork sur communes témoins (10-15 EAJE attendus à Ajaccio par exemple) et OSM seul provient probablement de la sur-estimation par extrapolation démographique : le mode de garde corse dominant reste les assistantes maternelles individuelles (hors périmètre EAJE structuré). Audit ciblé via mon-enfant.fr en navigateur réel recommandé pour affiner si besoin.

**Métadonnées hétérogènes :** 4 features sur 15 sans nom (« Crèche sans nom »), aucun tag `kindergarten:FR` (sous-catégorisation par heuristique sur le nom, fallback `creche_collective`), aucun tag `addr:*` (reverse-géocodage IGN obligatoire).

**Anomalies de tagging filtrées (liste `EXCLUDED_OSM_IDS` du script) :**
- `osm_node_7899283685` (Olmeta-di-Capocorso, 2B187) : tag `amenity=kindergarten` mais `name="Mairie"`. Incohérence tag amenity / name, présomption d'erreur de mapping OSM amont. Exclu jusqu'à correction (signalement OSM possible). Décision Soleil 2026-04-25.

Si OSM corrige ces anomalies, retirer les IDs concernés de la liste `EXCLUDED_OSM_IDS` au prochain refresh pour réintégrer les features.

**Pas de scope assistantes maternelles individuelles** (hors périmètre de la Loi Abeille, pas de référentiel open data adapté).

Détail complet : [docs/tickets/EAJE-CORSE-001.md](../tickets/EAJE-CORSE-001.md).

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
