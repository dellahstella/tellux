# Forêts Corse — couche visuelle Tellux

**Couche Leaflet :** `wmsForet` dans `app.html`
**Bouton UI :** `b-foret` dans Groupe 3 "Contexte naturel"
**Date d'intégration :** 2026-04-21

## Voie retenue (audit 2026-04-21)

Après audit de plusieurs sources, **Voie C partielle** : WMS `FORETS.PUBLIQUES` sur `data.geopf.fr/wms-v/ows`.

### Sources testées

| Source | Résultat |
|---|---|
| `geo.numerique.corsica` (portail géomatique CdC) | ❌ Inaccessible au test |
| `isula.corsica/infogeo` (INFOGEO Corse) | ❌ Inaccessible au test |
| `data.geopf.fr/wms-r/` (raster) | ❌ Aucune couche forêt |
| `data.geopf.fr/wms-v/` → `BETA-IGN_BDFORETV3_TEST` | ⚠ BDFORET V3 BETA mars 2026, couverture test partielle (tuile Corse vide) |
| `data.geopf.fr/wms-v/` → `IGNF_CARTO-FORMATIONS-VEGETALES_2023` | ❌ DROM uniquement (Mayotte), pas métropole |
| `data.geopf.fr/wms-v/` → `FORETS.PUBLIQUES` | ✓ **Test GetMap sur Corse réussi** |

### Voie C retenue : `FORETS.PUBLIQUES`

Localisation des **forêts publiques domaniales et non domaniales** (communales, sectionales, départementales et d'établissements publics) gérées par l'**Office National des Forêts (ONF)**.

**Endpoint WMS** :
- URL : `https://data.geopf.fr/wms-v/ows`
- Couche : `FORETS.PUBLIQUES`
- Format : `image/png` transparent
- Version : WMS 1.3.0
- CRS : EPSG:4326
- Attribution : © IGN / ONF

### Intégration Tellux

```javascript
const wmsForet = L.tileLayer.wms('https://data.geopf.fr/wms-v/ows', {
  layers: 'FORETS.PUBLIQUES',
  format: 'image/png',
  transparent: true,
  opacity: 0.55,
  version: '1.3.0',
  attribution: '© IGN / ONF — Forêts publiques'
});
```

Branchée via le dispatcher `tog()` générique, registre `WMS` (cohérent avec géologie BRGM, hydro, EMAG2, etc.).

## Limitations importantes

**Cette couche N'EST PAS la BD Forêt V2 complète.** Différences :

| Caractéristique | FORETS.PUBLIQUES | BD Forêt V2 |
|---|---|---|
| Forêts publiques (ONF) | ✓ | ✓ |
| Forêts privées | ❌ | ✓ |
| Essences détaillées (pin laricio, châtaignier…) | ❌ | ✓ |
| Nomenclature corse spécifique | ❌ | ✓ |

**Couverture effective en Corse** : grandes forêts domaniales (Aïtone, Valdu-Niellu, Vizzavona, Bonifatu, etc.) + communales ONF. Absence : châtaigneraies privées Castagniccia, maquis, petites forêts privées.

## Niveau A strict

Couche **visuelle seule** dans le Groupe 3 "Contexte naturel".

**Aucune modulation des calculs** `calcGammaAmbient` ni `calcRadonPotential`.

Les coefficients de modulation gamma/radon par couvert forestier seront calibrés ultérieurement via le protocole de 6 zones forestières de test conduit par Soleil. Ce protocole validera scientifiquement les coefficients avant tout impact sur le modèle composite.

## Dettes restantes

**BDFORET-GRANULARITE-001** : BD Forêt V2/V3 complète avec essences détaillées (pin laricio, chênes sempervirents, châtaignier) toujours inaccessible via WMS public. Deux voies ouvertes :

- **Attente BD Forêt V3 production** : la V3 BETA (mars 2026) est en test sur `data.geopf.fr/wms-v` sous `BETA-IGN_BDFORETV3_TEST` mais couverture Corse non effective au test du 2026-04-21. Suivre la progression IGN.

- **Rastérisation locale shapefiles** (Voie B du prompt) : télécharger les shapefiles BD Forêt V2 départementaux 2A/2B, rastérisation en tuiles PNG XYZ via `rasterio`+`geopandas`. Hors scope session actuelle : 2-3h de scripting + potentiellement > 50 MB de tuiles.

## Régénération / maintenance

**Aucune régénération nécessaire côté Tellux** : la couche est servie dynamiquement par le WMS IGN Géoplateforme. Mises à jour transparentes lors des rafraîchissements IGN.

En cas de changement d'URL WMS IGN, mettre à jour la constante `wmsForet` dans `app.html`.

## GELE-001

Ajout de la couche **sans impact** sur les pondérations composite `w_M = 0.40, w_RF = 0.40, w_I = 0.20`.

## Licence

Licence Ouverte / Open Licence v2.0 Etalab. Attribution obligatoire : © IGN / ONF.
