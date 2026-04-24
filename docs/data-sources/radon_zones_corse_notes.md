# Note technique — Géométries zones radon en Corse
## Production de `public/data/radon_zones_corse.geojson`

**Version :** 1.0 — 2026-04-24  
**Statut :** Plan B1 — script de production fourni, exécution requise par Soleil  
**Auteur :** Cowork / Tellux  

---

## 1. Contexte et cadre réglementaire

Le décret n° 2018-434 du 5 juin 2018 et l'**arrêté du 27 juin 2018** (JORFTEXT000037131346, en vigueur au 1er juillet 2018) classent l'ensemble des communes françaises en trois catégories de potentiel radon selon leur sous-sol géologique :

| Catégorie | Signification |
|---|---|
| 1 | Formations géologiques à plus faibles teneurs en uranium — majorité de bâtiments à faible concentration radon |
| 2 | Formations à faible teneur uranium mais avec facteurs géologiques particuliers (failles, karsts, mines) favorisant les transferts |
| 3 | Formations géologiques à teneurs en uranium estimées plus élevées sur au moins une partie du territoire communal |

**Autorité compétente :** ASNR (Autorité de Sûreté Nucléaire et de Radioprotection), issue de la fusion ASN + IRSN au 1er janvier 2025. Les données publiées restent produites par l'IRSN jusqu'en 2024.

---

## 2. Classification officielle pour la Corse

### Corse-du-Sud (département 2A)
**Toutes les communes sont classées catégorie 3** — potentiel radon élevé.  
Nombre de communes : 124 (source : INSEE, COG 2024).  
Substrat dominant : granites hercyniens (Varisques), à forte teneur en uranium.

### Haute-Corse (département 2B)
Classement mixte, par défaut catégorie 1 sauf exceptions :

**Communes catégorie 2** (~37 communes, source : arrêté 27 juin 2018 via CDG 2B) :  
Altiani, Biguglia, Bisinchi, Borgo, Brando, Castellare-Di-Mercurio, Centuri, Erbajolo, Erone, Ersa, Ficaja, Focicchia, Gavignano, La Porta, Lugo-Di-Nazza, Luri, Matra, Meria, Moita, Morsiglia, Piedicorte-di-Gaggio, Pietroso, Pino, Poggio-Marinaccio, Quercitello, Rospigliani, Rusio, San-Damiano, San-Gavino-d'Ampugnani, Sant'Andrea-di-Bozio, Santo-Pietro-di-Venaco, Scata, Sermano, Tallone, Tomino, Tox, Vezzani.

**Communes catégorie 3** (liste partielle — voir avertissement §6) :  
Albertacce, Algajola, Aregno, Asco, Avapessa, Barbaggio, Bastia, Belgodère, Calacuccia, Calenzana, Calvi, Canale-di-Verde, Canavaggia, Casamaccioli, Casanova, Castifao, Castiglione, Castineta, Castirla, Cateri, Chisa, Corbara, Corscia, Corte, Costa, Farinole, Favalello, Feliceto, Furiani, Galeria, Ghisoni, Isolaccio-di-Fiumorbo, Lama, Lavatoggio, Lento, Linguizzetta, Lozzi, Lumio, Manso, Mausoleo, Moltifao, Moncale, Montegrosso, Monticello, Morosaglia, Muracciole, Muro, Nessa, Noceta, Novella, Occhiatana, Oletta, Olmeta-di-Capocorso, Olmeta-di-Tuda, Olmi-Cappella, Omessa, Palasca, Patrimonio, Piedigriggio, Pietralba, Piève, Pigna, Pioggiola, Poggio-di-Nazza, Poggio-di-Venaco, Poggio-d'Oletta, Popolasca, Prato-di-Giovellina, Prunelli-di-Fiumorbo, Rapale, Saint-Florent, San-Gavino-di-Fiumorbo, San-Gavino-di-Tenda…

**Communes catégorie 1** : toutes les autres communes de 2B (~250 communes), non représentées dans Tellux.

---

## 3. Sources de données

### 3.1 Classification radon (attributs)

| Élément | Valeur |
|---|---|
| **Jeu de données** | Zonage en potentiel radon |
| **Producteur** | IRSN (Autorité désormais ASNR) |
| **URL data.gouv.fr** | https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon |
| **Format disponible** | Shapefile (.shp/.zip), possiblement GeoJSON ou CSV |
| **Licence** | Licence Ouverte 2.0 — Etalab (redistribution libre avec mention de source) |
| **Texte réglementaire** | Arrêté du 27 juin 2018 — https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037131346/ |
| **Dernière MAJ connue** | 2018 (entrée en vigueur du classement) |
| **Granularité** | Commune (code INSEE) |

Jeu de données alternatif : https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon-2/  
Portail géographique : https://geo.data.gouv.fr/en/datasets/aa6a9538f1556efba4a58be33ecd84e79cd40c52  
API Géorisques (consultation par commune) : https://www.georisques.gouv.fr/minformer-sur-un-risque/radon

### 3.2 Géométries communes (polygones)

| Élément | Valeur |
|---|---|
| **Source originale** | IGN AdminExpress COG |
| **Vecteur d'accès** | `gregoiredavid/france-geojson` (GitHub) |
| **URL 2A** | https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements/2a-corse-du-sud/communes-2a-corse-du-sud.geojson |
| **URL 2B** | https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements/2b-haute-corse/communes-2b-haute-corse.geojson |
| **Projection** | WGS84 / EPSG:4326 (natif Leaflet) |
| **Licence** | Licence Ouverte IGN (redistribution libre avec mention de source) |
| **Simplification** | Appliquée par le repo (mapshaper) — précision suffisante à l'échelle 1:50 000 |

---

## 4. Méthodologie de production

### Approche retenue : Plan B1

Le **Cowork ne peut pas télécharger directement** les fichiers gouvernementaux depuis son environnement sandbox (réseau restreint aux domaines npm/pypi/GitHub). La production du GeoJSON final est donc déléguée à Soleil via un **script Python autonome**.

### Script fourni

Fichier : `build_radon_geojson.py` (à la racine du repo Tellux)

Le script exécute les étapes suivantes :

1. **Interroge l'API data.gouv.fr** (`/api/1/datasets/zonage-en-potentiel-radon/`) pour obtenir les URLs de ressources disponibles.
2. **Télécharge le fichier de classification** (shapefile ZIP, GeoJSON ou CSV selon ce qui est disponible).
3. **Détecte automatiquement** les noms de colonnes INSEE et catégorie (variables selon les versions du dataset).
4. **Télécharge les géométries** 2A et 2B depuis `gregoiredavid/france-geojson` (GitHub, EPSG:4326).
5. **Croise** classification et géométries par code INSEE.
6. **Filtre** aux catégories 2 et 3 uniquement.
7. **Écrit** `public/data/radon_zones_corse.geojson` avec les propriétés standardisées.

En cas d'échec de l'API data.gouv.fr, le script bascule sur une **classification hardcodée** partielle extraite de l'arrêté du 27 juin 2018 (voir avertissement §6).

### Prérequis d'exécution

```bash
pip install requests geopandas shapely fiona
python build_radon_geojson.py
```

---

## 5. Propriétés GeoJSON produites

Chaque feature de `radon_zones_corse.geojson` contient :

| Propriété | Type | Exemple | Description |
|---|---|---|---|
| `code_insee` | string | `"2A004"` | Code INSEE officiel de la commune |
| `nom_commune` | string | `"Ajaccio"` | Nom de la commune |
| `departement` | string | `"2A"` | Code département |
| `categorie` | integer | `3` | Catégorie radon (2 ou 3) |
| `source` | string | `"ASNR/IRSN - Arrete du 27 juin 2018"` | Attribution obligatoire |
| `annee` | integer | `2018` | Année de publication du classement |
| `url_source` | string | URL data.gouv.fr | Lien vers la source |
| `licence` | string | `"Licence Ouverte 2.0 - Etalab"` | Licence du jeu de données |

---

## 6. Avertissements et limites

### ⚠ Liste cat 3 Haute-Corse incomplète

La liste des communes de Haute-Corse en catégorie 3 fournie dans ce document et dans le fallback hardcodé du script est **partielle**. Elle a été reconstituée par recherches web à partir de sources secondaires (CDG 2B, preventimmo.fr, radonova.fr) et n'a pas pu être vérifiée contre le texte intégral de l'arrêté sur Légifrance (inaccessible depuis le sandbox Cowork).

**Action requise avant intégration en production :**
1. Consulter le texte complet sur Légifrance : https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037131346/
2. Vérifier que la liste des communes Haute-Corse cat 3 du script correspond au tableau de l'arrêté.
3. Ou : utiliser le script en mode API data.gouv.fr (qui télécharge la liste officielle complète).

### Dernière mise à jour du classement

Le classement date de 2018 (entrée en vigueur au 1er juillet 2018). Aucune révision n'a été identifiée à la date de rédaction (avril 2026). L'ASNR peut modifier le classement par arrêté ultérieur — vérifier sur Légifrance.

### Géométries simplifiées

Les géométries IGN utilisées via `gregoiredavid/france-geojson` sont simplifiées (mapshaper). Elles sont suffisantes pour la visualisation dans Tellux mais ne conviennent pas à des usages cadastraux ou réglementaires. Les géométries exactes sont disponibles sur le Géoportail IGN (geoservices.ign.fr/adminexpress).

### Taille du fichier

La Corse compte ~360 communes dont ~124 en 2A (toutes cat 3) et environ 70-100 en 2B (cat 2+3). Le GeoJSON résultant est estimé à **400–900 Ko** selon la simplification appliquée — dans la limite Tellux de 2 Mo. Si le fichier dépasse 500 Ko, simplifier avec :

```bash
mapshaper public/data/radon_zones_corse.geojson -simplify 15% -o format=geojson public/data/radon_zones_corse.geojson
```

---

## 7. Intégration dans Tellux

### Chargement Leaflet

```javascript
fetch('public/data/radon_zones_corse.geojson')
  .then(r => r.json())
  .then(data => {
    L.geoJSON(data, {
      style: feat => ({
        fillColor: feat.properties.categorie === 3 ? '#C28533' : '#7B7770',
        fillOpacity: 0.45,
        weight: 0.5,
        color: '#22262B',
        opacity: 0.3,
      }),
      onEachFeature: (feat, layer) => {
        const p = feat.properties;
        layer.bindPopup(
          `<strong>${p.nom_commune}</strong><br>` +
          `Potentiel radon : catégorie ${p.categorie}<br>` +
          `<small>${p.source}</small>`
        );
      }
    }).addTo(map);
  });
```

### Citation pour la légende Tellux

> Zonage radon — ASNR/IRSN · Arrêté du 27 juin 2018 · Licence Ouverte 2.0

### Libellé court UI (4-8 mots)

- **Couche catégorie 3** : *Potentiel radon élevé — ASNR 2018*
- **Couche catégorie 2** : *Potentiel radon modéré — ASNR 2018*

---

## 8. Références

- Arrêté du 27 juin 2018 portant délimitation des zones à potentiel radon du territoire français. Légifrance. https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037131346/
- IRSN. Zonage en potentiel radon. data.gouv.fr. https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon
- ASNR. Connaître le potentiel radon de ma commune. https://recherche-expertise.asnr.fr/savoir-comprendre/environnement/connaitre-potentiel-radon-ma-commune
- Géorisques. Radon. https://www.georisques.gouv.fr/minformer-sur-un-risque/radon
- CDG 2B. Fiche risque radon. https://www.cdg2b.com/wp-content/uploads/2020/10/14-risque-radon.pdf
- BRGM. Cartographie prédictive du risque radon en région Corse (RP-50200-FR). https://www.corse.developpement-durable.gouv.fr/IMG/pdf/Carto_Radon_BRGM_-_RP-50200-FR.pdf
- IGN. AdminExpress COG. https://geoservices.ign.fr/adminexpress
- Grégoire David. france-geojson (GitHub). https://github.com/gregoiredavid/france-geojson

---

*Note rédigée par Cowork / Claude — usage interne Tellux — ne pas publier.*
