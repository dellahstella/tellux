# Ticket EAJE-CORSE-001 — Identifier une source EAJE géolocalisée pour la Corse

**Statut :** ouvert
**Créé le :** 2026-04-24
**Priorité :** à traiter avant la Passe 2 Établissements sensibles de `mairies.html`
**Lié à :** `scripts/build_etablissements_corse.py`, `public/data/corse/eaje.geojson`

## Contexte

Lors de l'exécution du pipeline `build_etablissements_corse.py` par la session Claude Code du 24 avril 2026, il a été constaté qu'**aucune source open data nationale géolocalisée n'existe** pour les Établissements d'Accueil du Jeune Enfant (EAJE) en France, et en particulier pour la Corse-du-Sud (2A) et la Haute-Corse (2B).

Recherche effectuée sur data.gouv.fr et data.caf.fr :

- **data.gouv.fr** : le slug `poi-eaje-3` initialement retenu par Cowork est en réalité un dataset **départemental de l'Ain** (168 features). Les autres datasets EAJE sur data.gouv.fr sont également locaux : Aude, Finistère, Loire-Atlantique, Mayenne, Saint-Denis (La Réunion). La Corse n'est pas présente.
- **data.caf.fr** : 8 datasets nationaux mais ils contiennent des **statistiques agrégées** (`nbpla_pe_nat`, `nbpla_pe_dep`, `nbpla_pe_com`...), c'est-à-dire le nombre de places offertes par territoire. Pas de liste d'établissements géolocalisés.
- **ARS Corse** : pas de portail open data dédié identifié à ce stade.

En conséquence, le fichier `public/data/corse/eaje.geojson` est livré en v1 comme une `FeatureCollection` vide mais bien formée, avec des métadonnées documentant l'absence de source. Ce choix permet au bloc Établissements sensibles de `mairies.html` de charger les trois GeoJSON de manière uniforme, sans branche conditionnelle.

## Objectif

Trouver une source géolocalisée des EAJE de Corse avant la Passe 2 de `mairies.html`, ou documenter l'absence durable et prévoir un affichage explicite dans la Fiche commune ("donnée EAJE non disponible pour cette commune, voir CAF de Corse").

## Pistes à explorer

### P1. Portail CAF de Corse en direct

La CAF de Corse-du-Sud et la CAF de Haute-Corse publient probablement une liste de structures sur leurs sites officiels. Vérifier :

- [https://www.caf.fr/allocataires/caf-de-corse-du-sud](https://www.caf.fr/allocataires/caf-de-corse-du-sud)
- [https://www.caf.fr/allocataires/caf-de-haute-corse](https://www.caf.fr/allocataires/caf-de-haute-corse)

Accès probable via le service "mon-enfant.fr" (portail CAF) qui propose une recherche par code postal. Vérifier s'il existe une API ou un export.

### P2. OpenStreetMap (amenity=kindergarten)

Requête Overpass pour récupérer toutes les structures tagguées `amenity=kindergarten` ou `social_facility:for=child` sur la Corse. Qualité variable mais donne une base. À croiser avec d'autres sources pour fiabilité.

Exemple de requête Overpass :

    [out:json][timeout:60];
    area["ISO3166-2"="FR-20R"]->.a;
    ( node(area.a)[amenity=kindergarten];
      way(area.a)[amenity=kindergarten]; );
    out center;

### P3. Scraping doux des sites mairies

Pour les 5 à 10 communes principales de Corse (Ajaccio, Bastia, Corte, Porto-Vecchio, Sartène, Calvi, Bonifacio, Ghisonaccia, Prunelli-di-Fiumorbo, L'Île-Rousse) : scraper les pages petite enfance des sites officiels. Approche peu scalable mais couvre le gros des EAJE corses.

### P4. Contact direct ARS Corse

L'ARS Corse a potentiellement une liste interne non publiée. Demande formelle de mise à disposition sous licence Etalab 2.0. Délai administratif à prévoir.

### P5. Basculer sur le jeu PSU

Le prompt juridique Cowork mentionnait la possibilité de basculer sur un jeu PSU (Prestation de Service Unique) en v2. À explorer également auprès de la CNAF.

## Contrainte d'architecture

Quelle que soit la source retenue, le pipeline `build_etablissements_corse.py` doit continuer à produire un fichier unique `public/data/corse/eaje.geojson` au schéma Tellux standard (voir `docs/data-sources/etablissements_corse_notes.md`). Si plusieurs sources sont agrégées (CAF + OSM + scraping), la déduplication doit se faire côté script, pas côté client.

## Critères de clôture

Ce ticket peut être clos quand l'une des deux conditions est remplie :

- Une source géolocalisée utilisable est intégrée au pipeline et le build produit un `eaje.geojson` non vide pour au moins Ajaccio, Bastia et 1 commune rurale.
- Une décision explicite est prise d'afficher "donnée EAJE non disponible" dans la Fiche commune, et un commentaire dans `mairies.html` documente cette décision.

## Liens

- Script producteur : [scripts/build_etablissements_corse.py](../../scripts/build_etablissements_corse.py)
- Note de data source : [docs/data-sources/etablissements_corse_notes.md](../data-sources/etablissements_corse_notes.md)
- Patch corrections FINESS/Education/EAJE : [DATASETS_PATCH_COWORK_FIX.md](../../DATASETS_PATCH_COWORK_FIX.md)
- Référence Cowork (hors repo public) : `tellux_mairies_datasets/DATASETS_PATCH_COWORK.md` §P5.2
