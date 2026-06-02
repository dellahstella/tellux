# Notes compagnon — radon_communes_level3_corse.json

**Date de production** : 2026-04-20
**Producteur** : Cowork session datasets (Soleil / Tellux Corse)
**Statut** : partiel vérifié, **à compléter impérativement en phase 2**

---

## 1. Source officielle et cadre réglementaire

- **Décret 2018-434** du 4 juin 2018 relatif aux mesures du radon dans les lieux accessibles au public
- **Arrêté du 27 juin 2018** portant délimitation des zones à potentiel radon du territoire français (JORFTEXT000037131346)
  - URL officielle : https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037131346/
  - Article 1, annexes III (zone 2) et IV (zone 3)
- Référence Code de la santé publique : articles R1333-29 à R1333-33

Le décret classe chaque commune française dans une zone parmi trois niveaux :
- Zone 1 — potentiel radon faible
- Zone 2 — potentiel radon faible mais avec facteurs géologiques favorisant le transfert
- Zone 3 — potentiel radon significatif (obligation de mesure dans les lieux accessibles au public)

---

## 2. Contrainte rencontrée pendant la production

**Problème majeur** : l'accès direct aux sources officielles a été bloqué par le proxy réseau de l'environnement Cowork. Sites bloqués pendant la session :
- https://www.legifrance.gouv.fr (texte de l'arrêté)
- https://www.data.gouv.fr (dataset IRSN "Connaître le potentiel radon de ma commune")
- https://www.isere.gouv.fr (PDF annexe de l'arrêté)
- https://www.preventionbtp.fr (republication du texte)
- https://www.actu-environnement.com (republication réglementaire)
- https://www.cdg2b.com (plaquette de prévention 2B)
- https://www.solutions-radon.fr (synthèse opérationnelle)
- https://recherche-expertise.asnr.fr (cartographie interactive ASNR)
- https://api-adresse.data.gouv.fr (API BAN pour centroïdes)
- https://nominatim.openstreetmap.org (géocodage OSM)

**Conséquence** : la liste n'a pu être constituée qu'à partir d'extraits partiels remontés par les moteurs de recherche (WebSearch), pas par fetch direct du texte.

---

## 3. Résultats consolidés

### 3.1 Fait central et vérifié

**La Corse-du-Sud (2A) est INTÉGRALEMENT classée zone 3 par l'arrêté du 27 juin 2018.**

Cette information a été confirmée explicitement par recherche web (plusieurs sources tierces citant l'arrêté) et cohérente avec la géologie (granite hercynien omniprésent en 2A). Les 124 communes du département relèvent donc de la zone 3.

**Implication pour Tellux** : en code, appliquer un boost `radon_class = 3` à tout point dont la commune de rattachement a un code INSEE commençant par `2A`. La liste exhaustive des 124 communes 2A n'est pas nécessaire pour cette règle, mais utile si l'overlay cartographique souhaite représenter chaque commune individuellement.

### 3.2 Haute-Corse (2B) — liste partielle

La Haute-Corse a une classification mixte : majorité en zone 1, ~37 communes en zone 2, ~70-85 communes attendues en zone 3 (estimation à vérifier).

**Communes 2B confirmées zone 3 par recherche web** (14 communes) :
- Albertacce (Niolu)
- Algajola (Balagne côtière)
- Aregno (Balagne)
- Asco (vallée montagne)
- Avapessa (Balagne)
- Barbaggio (Cap Corse sud)
- Bastia (préfecture)
- Belgodère (Balagne intérieure)
- Calacuccia (centre Niolu)
- Calenzana (Balagne)
- Calvi (Balagne côtière)
- Canale-di-Verde (Castagniccia orientale)
- Corte (centre granitique — très probable zone 3, à reconfirmer)
- Venaco (centre Corse — très probable zone 3, à reconfirmer)

**Communes 2B confirmées zone 2 par recherche web** (NON zone 3, pour information seulement — ne pas intégrer dans le dataset zone 3) :
Altiani, Biguglia, Bisinchi, Borgo, Brando, Castellare-di-Mercurio, Centuri, Erbajolo, Erone, Ersa, Ficaja, Focicchia, Gavignano, La Porta, Lugo-di-Nazza, Luri, Matra, Meria, Moita, Morsiglia, Piedicorte-di-Gaggio, Pietroso, Pino, Poggio-Marinaccio, Quercitello, Rospigliani, Rusio, San-Damiano, San-Gavino-d'Ampugnani, Sant'Andrea-di-Bozio, Santo-Pietro-di-Venaco, Scata, Sermano, Tallone, Tomino, Tox, Vezzani

**Important** : la liste zone 3 de 2B est **tronquée** par les extraits web (seuls les noms commençant par A à C environ sont visibles). La liste complète doit contenir environ 60 à 80 communes additionnelles, notamment dans les zones de granite central (Niolu plus large, Castagniccia, Cruzzini, Taravo, Fium'Orbu, Alta Rocca hors 2A).

---

## 4. Centroïdes

Les centroïdes (latitude/longitude) dans le JSON sont des **approximations à 4 décimales** issues de la connaissance géographique générale, pas du géocodage officiel BAN/IGN. Leur précision est de l'ordre de 100 à 500 m pour les communes listées — largement suffisante pour un overlay cartographique par cercle mais pas pour un géo-matching point dans polygone précis.

**À faire en phase 2** : récupérer les centroïdes officiels via :
- API BAN : https://api-adresse.data.gouv.fr/search/?q=NOM_COMMUNE&type=municipality
- COG INSEE (fichier communes géolocalisées) : https://www.insee.fr/fr/information/4316069
- ADMIN EXPRESS IGN : https://geoservices.ign.fr/adminexpress

---

## 5. Codes INSEE

La plupart des `code_insee` sont à `null` dans le JSON : je n'ai pas eu accès au COG INSEE pendant la session et je n'ai voulu prendre aucun risque d'invention. Les deux codes confirmés sont :
- `2A004` = Ajaccio
- `2B033` = Bastia
- `2A001` = Afa (exemple du brief initial)

**À faire en phase 2** : joindre la liste nominative avec le fichier COG INSEE 2016 (la référence de l'arrêté est bien 1er janvier 2016) pour récupérer tous les codes.

---

## 6. Méthodologie recommandée pour complétion (phase 2)

Ordre d'attaque pour obtenir la liste exhaustive :

1. **Option privilégiée** — Télécharger le dataset IRSN sur data.gouv.fr depuis un environnement non bloqué :
   - https://www.data.gouv.fr/datasets/connaitre-le-potentiel-radon-de-ma-commune
   - Filtrer sur départements 2A et 2B
   - Filtrer sur classement = 3
   - Joindre avec COG pour codes INSEE et centroïdes

2. **Option fallback** — Extraire manuellement depuis l'arrêté Legifrance :
   - https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037131346/
   - Annexe IV (zone 3), section Corse

3. **Option visuelle** — Utiliser la cartographie IRSN/ASNR interactive :
   - https://recherche-expertise.asnr.fr/savoir-comprendre/environnement/connaitre-potentiel-radon-ma-commune
   - Parcourir chaque commune 2B et noter le classement

---

## 7. URL des sources consultées pendant la session

| Source | URL | Accès | Usage |
|---|---|---|---|
| Arrêté 27/06/2018 | https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000037131346/ | BLOQUÉ | Référence |
| Article 1 arrêté | https://www.legifrance.gouv.fr/jorf/article_jo/JORFARTI000037131352 | BLOQUÉ | Référence |
| Dataset IRSN | https://www.data.gouv.fr/datasets/connaitre-le-potentiel-radon-de-ma-commune | BLOQUÉ | Référence |
| Zonage potentiel radon | https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon | BLOQUÉ | Référence |
| ASNR cartographie | https://recherche-expertise.asnr.fr/savoir-comprendre/environnement/connaitre-potentiel-radon-ma-commune | BLOQUÉ | Référence |
| BRGM cartographie Corse | https://www.corse.developpement-durable.gouv.fr/IMG/pdf/Carto_Radon_BRGM_-_RP-50200-FR.pdf | Indirect | Cité en recherche web |
| Plaquette info radon Corse | https://www.corse.developpement-durable.gouv.fr/IMG/pdf/Plaquette_d_information_sur_le_radon_en_Corse.pdf | Indirect | Cité en recherche web |
| CDG 2B plaquette radon | https://www.cdg2b.com/wp-content/uploads/2020/10/14-risque-radon.pdf | BLOQUÉ | Référence |
| ARS Corse radon | https://www.corse.ars.sante.fr/le-radon-quels-risques-pour-ma-sante | Indirect | Cité en recherche web |
| OEC Corse radon | https://www.oec.corsica/U-risicu-radu_a43.html | Indirect | Cité en recherche web |
| Radonova Corse | https://radonova.fr/carte-du-radon/le-radon-dans-lile-de-beaute/ | Indirect | Cité en recherche web |

---

## 8. Incertitudes à flagger pour la session de code suivante

1. **Volumétrie 2A** : le dataset JSON ne liste que 14 communes 2A, alors que 124 sont classées zone 3. L'intégration doit gérer cette incomplétude — soit via la règle département (recommandé), soit en complétant la liste depuis le COG.

2. **Volumétrie 2B** : 14 communes listées, plage attendue 60-100. **Ne pas utiliser le JSON tel quel comme source de vérité 2B** — c'est une amorce à compléter.

3. **Graphies** : les accents et apostrophes officiels (Belgodère → Belgodere, Aullène → Aullene, Sartène → Sartene, San-Gavino-d'Ampugnani) sont transcrits sans accent dans le JSON pour éviter tout problème d'encodage. Pour un affichage UI propre, recharger les graphies officielles depuis le COG INSEE.

4. **Géométries communales** : aucun polygone produit dans cette session. Si Tellux veut un overlay par polygones plutôt que par cercles, télécharger ADMIN EXPRESS IGN en phase 2 et produire `radon_communes_level3_corse_geometries.geojson`.

5. **Fraîcheur** : l'arrêté du 27 juin 2018 n'a pas été modifié à notre connaissance depuis sa publication. Aucune mise à jour IRSN/ASNR repérée pour 2024-2025. Veille à conserver en phase 2 pour détection d'amendements éventuels.

---

## 9. Ventilation finale

| Département | Communes zone 3 attendues | Communes listées dans JSON | Couverture |
|---|---|---|---|
| 2A (Corse-du-Sud) | 124 (tout le département) | 14 | 11% |
| 2B (Haute-Corse) | ~70-85 (estimation) | 14 | ~17-20% |
| **Total Corse** | **~194-209** | **28** | **~14%** |

**Statut** : dataset amorce fiable, à compléter.
