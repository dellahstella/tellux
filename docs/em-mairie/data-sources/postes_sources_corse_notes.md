# Postes sources EDF SEI Corse — note méthodologique

**Fichier :** `public/data/postes_sources_corse.json`
**Date d'extraction :** 2026-04-21
**Source retenue :** OpenStreetMap Overpass API (tag `power=substation`)
**Source initialement visée :** EDF SEI open data (`opendata-corse.edf.fr`)

## Contexte

Les postes sources sont les points d'interconnexion HTB → HTA du réseau électrique corse. Ils concentrent des courants élevés et représentent des points chauds de champ magnétique ELF 50 Hz.

## Choix de la source

Lors de l'audit 2026-04-21, le portail `opendata-corse.edf.fr` était inaccessible (erreur HTTP 404 sur les URL documentées). Un courrier officiel a été envoyé à EDF SEI (lettre 02, 2026-04-14) pour obtenir l'accès aux datasets structurés. En attendant, OpenStreetMap est retenu comme source fallback.

## Méthodologie d'extraction

Requête Overpass exécutée sur la bbox Corse `[41.3, 8.5, 43.1, 9.7]` :

```
[out:json];
(node["power"="substation"](41.3,8.5,43.1,9.7);
 way["power"="substation"](41.3,8.5,43.1,9.7);)
;out center;
```

Filtrage manuel pour ne conserver que les postes avec :
- `name` contenant "Poste électrique" (identification humaine fiable)
- `operator = "Électricité de France"`
- `voltage` précisant une tension HTB/HTA (90 kV minimum pour être un poste source)

Résultat : **21 postes** de distribution HTB/HTA identifiés. Exclus : les boîtiers de quartier, les mini-postes de transformation BT, et les postes sans tension primaire documentée.

## Cas particulier Bonifacio

Le poste de Bonifacio (`OSM_136737513`) est le point d'arrivée en Corse de la liaison SARCO (Sardaigne-Corse) : un câble en courant alternatif de 150 kV et 100 MW, venu de Santa Teresa di Gallura. Ces 150 kV sont plus élevés que le standard corse (90 kV).

Le tag OSM du poste porte aussi 200 kV. Ce n'est pas la tension de SARCO, mais celle de la liaison SACOI (Sardaigne-Corse-Italie), en courant continu, dont la seule station de conversion en Corse est à Lucciana : ce n'est donc pas un niveau de transformation du poste. Cette précision figure dans le champ `note` du poste, dans `public/data/postes_sources_corse.json`.

Sources : Terna, *Codice di Rete*, allegato A.24, rév. 06 (janvier 2025), pour la nature et la tension des deux liaisons ; Terna, présentation « Le infrastrutture elettriche per la transizione energetica » (Cagliari, 9 décembre 2024), pour la capacité de 100 MW ; CRE, délibération n° 2023-363, pour la station de conversion de Lucciana ; OpenStreetMap, ligne `way/137729287` (« HVDC Sacoi - Bonifacio - Lucciana », 200 kV, `frequency=0`), dont un pylône est dans l'emprise du poste, pour l'attribution des 200 kV à SACOI.

## Limitations

1. **Complétude** : OSM est contributif, il peut manquer des postes mineurs
2. **Coordonnées** : précision ±50 m (centroïde OSM, pas géoréférencement officiel)
3. **Tensions** : le tag `voltage` OSM peut ne pas refléter la réalité en cas de modification réseau postérieure à la contribution OSM
4. **Opérateur** : tous `EDF` mais certains postes peuvent être en copropriété privée (ex. producteurs autonomes)

## Licence

Open Database License (ODbL) — attribution à OpenStreetMap contributors obligatoire. Conforme à la licence publique Tellux.

## Intégration dans Tellux

- **Couche visuelle** : carrés Ocre (`#C28533`) bordure Ardoise, taille 10 px standard, 12 px pour postes HTB ≥ 150 kV
- **Bouton** : `b-postes` dans Groupe 2 "Sources anthropiques"
- **Contribution calcul ELF** : modèle source ponctuelle 50 µT à 10 m avec décroissance 1/d³, plafond 500 nT, pruning à 1 km. Coefficient documentaire, à calibrer si mesure terrain dédiée.

## Mise à jour

Ce dataset est à régénérer dès que EDF SEI rouvrira son portail open data. La procédure :
1. Télécharger le dataset EDF SEI officiel (CSV/GeoJSON)
2. Filtrer sur la Corse, ajouter les champs puissance apparente si publiés
3. Remplacer le fichier, mettre à jour `source` dans le JSON, incrémenter `date_extraction`
