# Ticket EAJE-CORSE-001 — Identifier une source EAJE géolocalisée pour la Corse

**Statut :** clos (résolu en scénario B)
**Créé le :** 2026-04-24
**Clos le :** 2026-04-25
**Résolu par :** session Claude Code, branche `feat/eaje-corse-integration`, PR à venir
**Priorité initiale :** à traiter avant la Passe 2 Établissements sensibles de `mairies.html`
**Lié à :** `scripts/build_eaje_osm_corse.py`, `public/data/corse/eaje.geojson`, `tellux_eaje_corse/`

## Résolution

Source retenue : **OpenStreetMap** via Overpass API, tags `amenity=kindergarten` et `amenity=childcare` filtrés sur les départements 2A et 2B (areas ISO3166-2 FR-2A et FR-2B).

Licence : ODbL (Open Database License). Attribution obligatoire : « © OpenStreetMap contributors ».

**Volumétrie :** 15 features valides extraites le 25 avril 2026 (11 sur 2B Haute-Corse, 4 sur 2A Corse-du-Sud), 1 rejetée (anomalie de tagging documentée, voir §Limites). Couverture estimée à 25 % sur la base d'un total attendu de 60 EAJE en Corse (45 documentés en 2B par le schéma départemental 2020 + ~15 en 2A par extrapolation démographique).

**Scénario appliqué :** B (10 à 30 features) — voie OSM partielle, mention de couverture incomplète dans les métadonnées du GeoJSON et dans l'UI de `mairies.html`.

**Répartition par sous-catégorie :** 12 crèches collectives, 1 micro-crèche, 1 multi-accueil, 1 halte-garderie.

**Reverse-géocodage :** code INSEE et nom de commune dérivés via `geo.api.gouv.fr/communes` (Etalab IGN, gratuit, 50 req/s) car aucun feature OSM ne portait les tags `addr:city` ni `ref:INSEE`.

## Critère de clôture rempli

L'option 1 du critère de clôture initial est satisfaite :
> Une source géolocalisée utilisable est intégrée au pipeline et le build produit un `eaje.geojson` non vide pour au moins Ajaccio, Bastia et 1 commune rurale.

Confirmation par les communes témoins :
- Ajaccio (2A004) : 1 EAJE OSM
- Bastia (2B033) : 2 EAJE OSM
- Calvi (2B050) : 1 EAJE OSM (commune intermédiaire)
- Corte (2B096) : 1 EAJE OSM
- Communes rurales représentées : Olmeta-di-Capocorso, Ventiseri, Sisco, Ghisonaccia, Vescovato

## Pistes non retenues (pour traçabilité)

| Piste | Verdict |
|---|---|
| P1 CAF Corse / mon-enfant.fr | Pas d'API publique. Utilisable seulement comme contrôle qualité ponctuel. |
| P3 Schémas départementaux | Statistiques agrégées sans listing géolocalisé (45 EAJE 2B en 2020, pas de coordonnées). |
| P4 ARS Corse | Hors champ : EAJE petite enfance ne relèvent pas de l'ARS (CAF + département + PMI). |
| P5 Scraping mairies | Effort très élevé, hétérogène, scalabilité limitée. Dernier recours non activé. |
| P6 data.gouv.fr Géocodage 2016 | Millésime 2016, crédibilité dégradée. Non retenu pour v2. |

Détails : voir `tellux_eaje_corse/EAJE_CORSE_SOURCES_EVAL.md` (Cowork, 24 avril 2026).

## Limites assumées

1. **Couverture partielle** : 26.7 % estimée. Les communes urbaines (Ajaccio, Bastia) sont sous-représentées dans OSM par rapport aux estimations Cowork (10-15 EAJE attendus à Ajaccio, 1 seul dans OSM). À recroiser avec mon-enfant.fr lors d'un audit ultérieur en navigateur réel.

2. **Métadonnées hétérogènes** : 4 features sur 15 sans nom (« Crèche sans nom »).

3. **Anomalie de tagging filtrée** (`osm_node_7899283685`, Olmeta-di-Capocorso 2B187, name « Mairie » mais tag `amenity=kindergarten`) : exclue du fichier final via la liste `EXCLUDED_OSM_IDS` du script `build_eaje_osm_corse.py`. Décision Soleil 2026-04-25 : « incohérence tag amenity / name, présomption d'erreur de mapping OSM amont, exclu jusqu'à correction ». Le rejet est tracé dans le bloc rejected du build avec raison `excluded_osm_anomaly`. Si l'anomalie est corrigée côté OSM, retirer l'ID de la liste pour réintégrer la feature au prochain refresh.

4. **Pas de tag `kindergarten:FR`** sur aucun feature → sous-catégorisation dérivée par heuristique sur le nom (`micro-crèche`, `halte-garderie`, `multi accueil`) avec fallback `creche_collective` par défaut.

5. **Pas de tag `addr:*`** sur aucun feature → adresse postale absente, code INSEE/nom commune obtenus par reverse-géocodage IGN.

## UI dans `mairies.html`

Le bloc Établissements sensibles affiche désormais :

- Si la commune sélectionnée a au moins 1 EAJE OSM : une note de transparence indiquant la source OSM, la couverture partielle, et un lien vers mon-enfant.fr pour exhaustivité.
- Si la commune n'a aucun EAJE OSM : une note expliquant l'absence dans OSM et invitant à consulter mon-enfant.fr ou la CAF de Corse.

## Procédure de refresh

Cadence recommandée : trimestrielle (OSM évolue continuellement par contributions citoyennes).

Commande :

```bash
python scripts/build_eaje_osm_corse.py --output public/data/corse --verbose
```

Si le delta de feature_count dépasse 50 % vs l'extraction précédente, ne pas écraser le fichier sans validation manuelle.

## Pistes de progression future

- **Audit OSM ciblé** : repasser sur les 5 communes témoins en navigateur réel pour comparer OSM vs mon-enfant.fr et estimer la couverture réelle. Si écart fort sur 3 communes ou plus, envisager scénario C ou contributions OSM (signalement à un mappeur local).
- **Contributions OSM Tellux** : si politique projet le permet, contribuer manuellement à OSM pour les EAJE manquants documentés via les schémas départementaux ou mon-enfant.fr.
- **Demande Etalab à la CNAF** : courrier formel pour obtenir un export PSU localisé Corse sous licence Etalab 2.0. Délai administratif élevé. À évaluer en post-stabilisation v1.

## Liens

- Script producteur : [scripts/build_eaje_osm_corse.py](../../scripts/build_eaje_osm_corse.py)
- Note de data source : [docs/data-sources/etablissements_corse_notes.md](../data-sources/etablissements_corse_notes.md) (section EAJE OSM)
- Évaluation Cowork des sources : `tellux_eaje_corse/EAJE_CORSE_SOURCES_EVAL.md` (hors repo public)
- Notes d'intégration Cowork : `tellux_eaje_corse/EAJE_CORSE_INTEGRATION_NOTES.md` (hors repo public)
- Récap Cowork : `tellux_eaje_corse/COWORK_SESSION_RECAP.md` (hors repo public)
- GeoJSON produit : [public/data/corse/eaje.geojson](../../public/data/corse/eaje.geojson)

Fin du ticket.
