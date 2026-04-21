# Parcs éoliens Corse — note méthodologique

**Fichier :** `public/data/eoliennes_corse.json`
**Date d'extraction :** 2026-04-21
**Source :** RTE ODRE — Registre national des installations de production et de stockage d'électricité (au 31/12/2022)
**URL :** `https://odre.opendatasoft.com/explore/dataset/registre-national-installation-production-stockage-electricite-agrege-311222/`

## Méthodologie d'extraction

Requête API ODRE filtrée sur `filiere=Eolien` + `codedepartement IN (2A, 2B)` :

```
curl "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/registre-national-installation-production-stockage-electricite-agrege-311222/records?refine=filiere:Eolien&refine=codedepartement:2B&limit=50"
```

**Résultat :** 3 parcs en service, tous en Haute-Corse (2B). Aucun parc éolien en Corse-du-Sud (2A).

## Parcs identifiés

| Commune | Puissance (MW) | Mise en service |
|---------|----------------|-----------------|
| Ersa | 7.8 | 2000-11 |
| Lumio | 6.0 | 2003-12 |
| Rogliano | 4.2 | 2005-01 |

## Confidentialité partielle

Les champs `nominstallation`, `codeeicresourceobject` et `gestionnaire` du registre ODRE sont marqués "Confidentiel" pour protéger les exploitants privés. Les noms courants utilisés dans le fichier JSON ("Parc éolien d'Ersa", "Parc éolien de Lumio", "Parc éolien de Rogliano (Cap Corse)") sont tirés de la presse spécialisée et de l'historique documentaire public.

## Coordonnées

Le registre ODRE n'expose pas les coordonnées géographiques précises des parcs (protection périmètre d'exploitation). Les coordonnées retenues sont celles du **bourg communal** :

- **Ersa** : 42.9936 N, 9.3892 E
- **Lumio** : 42.5619 N, 8.8189 E
- **Rogliano** : 42.9734 N, 9.3589 E

Précision estimée : ±1 km (le parc réel est généralement à 500-2000 m du bourg, sur un col ou une crête ventée).

## Limitations

1. **Précision localisation** : coordonnées communales, pas géoréférencement précis des mâts
2. **Complétude** : le registre ODRE 2022 peut être dépassé. D'autres parcs (Calenzana, Alta Rocca) mentionnés dans la littérature ne figurent PAS au registre 2022 — soit projets abandonnés, soit mise en service post-2022 non encore enregistrée
3. **Nombre d'éoliennes / hauteur de mât** : non publiés dans ODRE, donc non renseignés

## Licence

Licence Ouverte / Open Licence v2.0 Etalab. Réutilisation libre avec attribution.

## Intégration dans Tellux

- **Couche visuelle** : triangle vert Maquis (`#3F5B3A`) 16×16 px, rappel hélice
- **Bouton** : `b-eoliennes` dans Groupe 2 "Sources anthropiques"
- **Contribution calcul ELF** : modèle ponctuel 2 µT à 10 m pour 2 MW, décroissance 1/d², modulé par √(puissance/2), plafond 300 nT, pruning à 500 m. Coefficient documentaire.

## Mise à jour

Régénérer à partir de la version la plus récente du registre ODRE (probablement renouvelé annuellement autour de mars-avril chaque année).
