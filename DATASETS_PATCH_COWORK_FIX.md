# DATASETS_PATCH_COWORK_FIX — Corrections appliquées au script Cowork

Document de traçabilité produit par la session Claude Code du 2026-04-24. Suite à la livraison Cowork `scripts/build_etablissements_corse.py` qui n'a pas pu être exécutée en session Cowork (allowlist proxy bloquante), l'exécution réelle a révélé **cinq bugs** dans le script. Arbitrage Soleil : Option 2 validée (corriger et livrer dans la session courante, avec traçabilité complète).

Pattern identique à `NOTE_JURIDIQUE_PATCH_COWORK.md`. Toutes les corrections sont annotées dans le code par un commentaire `# TELLUX FIX 2026-04-24:`.

---

## Résumé des corrections

| # | Zone | Gravité | Statut |
|---|---|---|---|
| FIX-1 | Annuaire Éducation : format code département | Bloquant (0 result) | Corrigé |
| FIX-2 | FINESS : mauvais fichier CSV source | Bloquant (0 coord) | Corrigé |
| FIX-3 | FINESS : parser CSV (DictReader avec header invalide) | Bloquant (0 match) | Corrigé |
| FIX-4 | FINESS : coordonnées en Lambert 93, pas WGS84 | Bloquant (rejets) | Corrigé |
| FIX-5 | Annuaire Éducation : mapping `type_etablissement` obsolète | Dégradation (tout en "autre") | Corrigé |
| FIX-6 | EAJE : source non nationale, pas de dataset utilisable | Structural | Contourné |

Invariants préservés dans tous les fixes : `MAPPING_FINESS`, `BOUNDS_CORSE`, schéma `Feature` en sortie, `rejection_reason`, structure CLI `--source` / `--output` / `--verbose`.

---

## FIX-1 : Annuaire Éducation — code département `02A/02B` (et non `2A/2B`)

**Bug.** Le script utilisait `where=code_departement in ("2A","2B")`. L'API Explore v2.1 stocke les codes département avec un **zéro initial** (`"028"` pour l'Eure-et-Loir, `"02A"`/`"02B"` pour la Corse).

**Cause.** Cowork a posé l'hypothèse que les codes département de l'API étaient sur 2 caractères (format postal), mais l'API utilise en réalité le format INSEE normalisé sur 3 caractères.

**Test de validation.** Requête directe à l'API :

    code_departement="2A"  -> total_count = 0
    code_departement="02A" -> total_count = 155 (Corse-du-Sud)
    code_departement="02B" -> total_count = 195 (Haute-Corse)

**Correction.** Ligne de filtre `where` modifiée dans `download_annuaire_education()`. 1 ligne de code.

---

## FIX-2 : FINESS — basculer sur le fichier géolocalisé (`cs1100507`)

**Bug.** Le script sélectionnait la ressource CSV la plus récente du dataset FINESS sans distinguer les deux fichiers publiés :

- `cs1100502-stock-*.csv` : "Extraction Finess des Etablissements" — contient uniquement des lignes `structureet`, sans coordonnées géographiques.
- `cs1100507-stock-*.csv` : "Extraction Finess des Etablissements géolocalisés" — contient en plus des lignes `geolocalisation` joignables par `nofinesset`.

Cowork tombait toujours sur le `cs1100502` car `last_modified` y est légèrement plus récent.

**Correction.** Fonction `_geoloc_marker()` ajoutée qui normalise les accents (NFD + strip ASCII) pour reconnaître le titre "géolocalisés" (accents) et donner la priorité à la ressource géolocalisée. Conservation du fallback sur le non-géolocalisé avec log `WARNING` si la ressource géolocalisée disparaît du catalogue.

Bug initial du match accents : `"geolocalis" in title.lower()` ne matchait pas `"géolocalisés"` à cause des `é`. Normalisation unicode NFD appliquée pour robustesse.

**Test de validation.** Après correction, le log `INFO` confirme `geolocalise=True` et la fonction récupère bien les 102 692 lignes `geolocalisation` en plus des 102 692 `structureet`.

---

## FIX-3 : FINESS — parser positionnel (CSV sans vrai header)

**Bug.** Le CSV FINESS n'a **pas de ligne d'en-tête nominative**. La ligne 1 est une ligne de métadonnée :

    finess;etalab;109;2026-03-11

Les données commencent ligne 2, avec **deux types de lignes** identifiées par leur première colonne :

- `structureet` (32 colonnes positionnelles) : données d'établissement.
- `geolocalisation` (6 colonnes positionnelles) : coordonnées, jointes par `nofinesset` (colonne 1).

Le script utilisait `csv.DictReader` qui prenait la ligne meta comme header, produisant des clés `"finess"`, `"etalab"`, `"109"`, `"2026-03-11"`. Aucune requête par nom de colonne ne retournait rien.

**Correction.** Refonte de `download_finess()` et `_normalize_finess_row()` :

- Chargement du contenu en mémoire via `resp.text.splitlines()` (pas `iter_lines` en stream, cf. note ci-dessous).
- Saut explicite de la ligne 1 (`first_line = True`).
- Pour chaque ligne suivante : dispatch sur `cols[0]` entre `structureet` et `geolocalisation`.
- Collecte des `structureet` Corse dans `structures: dict[str, list[str]]` (clé = `nofinesset`).
- Collecte de toutes les `geolocalisation` dans `geolocs: dict[str, tuple[float, float, str]]`.
- Join final en boucle sur `structures.items()`, passage de `geolocs.get(finess_id)` à `_normalize_finess_row()`.

Parser positionnel documenté en docstring avec le schéma des 32 colonnes `structureet` et des 6 colonnes `geolocalisation`.

**Note stream.** La première tentative utilisait `resp.iter_lines(decode_unicode=True)` en streaming. En pratique, **les 80 médico-sociaux Corse avec géoloc sortaient tous rejetés `no_coordinates`** alors que leur géoloc existait bien dans le fichier (vérifié par lecture directe du cache local). Le bug n'a pas été isolé en profondeur mais le passage à `resp.text.splitlines()` (chargement complet en mémoire, ~45 Mo en RAM décodé) l'a résolu.

**Test de validation.** Après correction : 603 structureet Corse lues, 102 692 geoloc lues, 80 médico-sociaux placés (tous joints), 0 rejet `no_coordinates`.

---

## FIX-4 : FINESS — conversion Lambert 93 → WGS84

**Bug anticipé mais non implémenté par Cowork** (cf. `DATASETS_PATCH_COWORK.md` §P4). Les coordonnées FINESS sont publiées en Lambert 93 (EPSG:2154), comme le confirme la métadonnée de la colonne source des lignes `geolocalisation` :

    2,ATLASANTE,53,BAN,EPSG:2154 RGF93 / Lambert-93 (Métropole)

Cowork prévoyait de les rejeter avec `rejection_reason="coords_not_wgs84"` en v1, et d'ajouter `pyproj` en v2. Le prompt de cette session interdit toute dépendance Python au-delà de `requests`, donc `pyproj` est exclu.

**Correction.** Fonction `_lambert93_to_wgs84(x, y) -> (lon, lat)` ajoutée, en Python pur. Implémentation des formules IGN NTG-71 / ALG0004 (ellipsoïde GRS80) :

- n = 0.7256077650532670
- c = 11754255.4261
- xs = 700000.0
- ys = 12655612.0499
- λ_0 = 3° (méridien central)
- e = 0.081819191042816 (première excentricité GRS80)

Inversion par latitude isométrique, itération sur 10 pas. Aucune dépendance externe.

**Test de validation.** Comparaison avec `pyproj` (installé localement pour validation uniquement, non requis à l'exécution) sur trois points de référence :

| Lambert 93 | pyproj                | Notre fonction        | Δ |
|---|---|---|---|
| (651221.7, 6862322.0) Tour Eiffel | 2.335168, 48.859085 | 2.335168, 48.859085 | 0 m |
| (870262.2, 6571540.8) CH Fleyriat | 5.209181, 46.222286 | 5.209181, 46.222286 | 0 m |
| (1165000, 6105000) Ajaccio        | 8.595822, 41.897386 | 8.595822, 41.897386 | 0 m |

Précision identique à `pyproj` au centimètre près. Vérification croisée sur les 80 médico-sociaux Corse : tous tombent dans les bornes `41.3 < lat < 43.1 ; 8.5 < lon < 9.6` après conversion.

---

## FIX-5 : Annuaire Éducation — dérivation `sous_categorie` via champs booléens

**Bug.** Le mapping `MAPPING_ANNUAIRE_EDUCATION` attendait des valeurs détaillées de `type_etablissement` comme `"Ecole maternelle"`, `"Ecole elementaire"`, `"Lycee general"`, `"Lycee professionnel"`. L'API retourne en réalité des types **génériques** : `"Ecole"`, `"Collège"`, `"Lycée"`, `"EREA"`, `"Médico-social"`, `"Service Administratif"`, `"Information et orientation"`. Résultat : 331 features toutes marquées `sous_categorie="autre"`.

Les détails (maternelle/élémentaire, général/technologique/professionnel) sont dans des **champs booléens à plat** : `ecole_maternelle`, `ecole_elementaire`, `voie_generale`, `voie_technologique`, `voie_professionnelle`.

**Correction.** Nouvelle fonction `_derive_sous_cat_education(type_etab, rec)` qui :

- Filtre les types hors périmètre enseignement sensible (`Médico-social`, `Service Administratif`, `Information et orientation` retournent `None` et sont ignorés dans `download_annuaire_education`).
- Pour `Ecole` : combine `ecole_maternelle` et `ecole_elementaire` → `ecole_maternelle`, `ecole_elementaire`, `ecole_primaire`.
- Pour `Collège` : → `college`.
- Pour `Lycée` : combine `voie_generale`, `voie_technologique`, `voie_professionnelle` → `lycee_general`, `lycee_technologique`, `lycee_professionnel`, `lycee_polyvalent`.
- Pour `EREA`, `CFA`, `SEGPA` : mapping direct.
- Sinon : `autre`.

`MAPPING_ANNUAIRE_EDUCATION` existant est remplacé par cette fonction (mapping direct par constante devenu inutile). L'ancien mapping est conservé dans le code pour référence historique.

**Test de validation.** Après correction, la distribution `par_sous_categorie` devient cohérente :

    ecole_primaire     : 152
    ecole_maternelle   :  51
    ecole_elementaire  :  47
    college            :  46
    lycee_polyvalent   :  11
    lycee_general      :   9
    lycee_professionnel:   5
    erea               :   1
    autre              :   9

Les 9 `autre` correspondent à des types non clairement classifiables par l'heuristique. Acceptable en v1.

---

## FIX-6 : EAJE — absence de source nationale, GeoJSON vide bien formé

**Bug.** Le script utilisait le slug `poi-eaje-3` sur data.gouv.fr, qui est en réalité un **dataset départemental de l'Ain** (Département 01, 168 features, 0 en Corse). Cowork avait choisi ce slug sans avoir pu l'inspecter (allowlist bloquante).

**Recherche d'alternative.** Aucune source nationale géolocalisée open data identifiée :

- data.gouv.fr : uniquement des jeux locaux (Ain, Aude, Finistère, Loire-Atlantique, Mayenne, Saint-Denis / La Réunion). La Corse-du-Sud (2A) et la Haute-Corse (2B) ne publient pas.
- data.caf.fr : 8 datasets nationaux mais agrégats statistiques (nombre de places par territoire : `nbpla_pe_nat`, `nbpla_pe_dep`, `nbpla_pe_com`...), pas de liste géolocalisée.
- ARS Corse : pas de portail open data dédié identifié.

**Correction (par contournement).** `download_eaje()` refondue pour retourner un itérateur vide avec un `LOG.warning` explicite. Les métadonnées du fichier de sortie `etablissements_petite_enfance_corse.geojson` documentent l'absence de source :

    "status": "empty_no_source",
    "coverage_note": "Aucune source nationale geolocalisee ... Les EAJE de Corse-du-Sud (2A) et Haute-Corse (2B) ne sont pas publies a ce jour. Voir ticket EAJE-CORSE-001...",
    "ticket": "EAJE-CORSE-001"

Le fichier reste une `FeatureCollection` bien formée pour permettre au bloc Établissements sensibles de `mairies.html` de charger les trois GeoJSON uniformément.

**Ticket ouvert.** `docs/tickets/EAJE-CORSE-001.md` liste 5 pistes alternatives à explorer avant la Passe 2 : CAF Corse directe, OpenStreetMap `amenity=kindergarten`, scraping doux des sites mairies, contact ARS Corse, bascule PSU.

---

## Résultats de l'exécution corrigée

| Catégorie | Fourchette Cowork | Observé | Statut |
|---|---|---|---|
| Enseignement | 400 à 550 | 331 | Légèrement sous, cohérent avec les 350 bruts retournés par l'API |
| Médico-social | 60 à 120 | 80 | ✅ Dans la fourchette |
| Petite enfance | 40 à 90 | 0 | ❌ Pas de source, ticket ouvert |
| Rejets | — | 1 | 1 école Annuaire Éducation sans coord GPS |

Taille totale des 3 GeoJSON : **177 KB** (largement sous le seuil de 3 MB du garde-fou P7.2).

Temps d'exécution total : ~2 minutes (dont ~90 s pour le téléchargement du CSV FINESS de 45 MB).

---

## Garde-fous respectés (rappel Soleil)

| Garde-fou | Statut |
|---|---|
| `MAPPING_FINESS` non modifié | ✅ Intact |
| `BOUNDS_CORSE` non modifié | ✅ Intact |
| Schéma `Feature` non modifié | ✅ Intact |
| `rejection_reason` non modifié | ✅ Valeurs `no_coordinates` et `coords_not_wgs84` conservées |
| CLI non modifiée | ✅ `--source`, `--output`, `--verbose` intacts |
| Commentaires `# TELLUX FIX 2026-04-24:` sur lignes modifiées | ✅ Systématique |
| Pas de dépendance Python au-delà de `requests` | ✅ `pyproj` écarté, conversion Lambert 93 en pur Python |
| Ticket EAJE-CORSE-001 créé | ✅ `docs/tickets/EAJE-CORSE-001.md` |
| Pas de donnée inventée | ✅ Fichier EAJE vide bien formé plutôt qu'une fabrication |

---

Fin du patch.
