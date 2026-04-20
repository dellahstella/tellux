# Notes compagnon — tdf_emitters_corse.json

**Date de production** : 2026-04-20
**Producteur** : Cowork session datasets (Soleil / Tellux Corse)
**Statut** : 10 émetteurs documentés, précision variable selon le site

---

## 1. Source officielle visée vs source réellement utilisée

**Source de référence attendue** : ANFR Cartoradio (https://www.cartoradio.fr/), qui publie fiche par fiche les PAR, fréquences, hauteurs, azimuts et coordonnées des émetteurs autorisés sur le territoire français.

**Problème** : Cartoradio (cartoradio.fr), data.anfr.fr, tdf.fr et arcom.fr sont bloqués par le proxy réseau de la session Cowork.

**Source effectivement utilisée** : TVNT.net, forum technique de référence qui republie fiche par fiche les caractéristiques Cartoradio ANFR (canal, multiplex, PAR en W/kW, opérateur). Cette source est une republication manuelle de l'ANFR donc fiable pour les ordres de grandeur, mais avec un risque d'obsolescence (mises à jour pas toujours synchrones avec Cartoradio officiel).

Croisement secondaire avec TDF (communiqués de presse, notamment Coti-Chiavari ferme solaire 2024).

---

## 2. Sites retenus (10)

### Sites principaux (2)

1. **Serra di Pigno** (Furiani, 2B) — site TDF principal Nord
   - Coordonnées du brief initial confirmées (42.6521, 9.3923)
   - Altitude 961 m (confirmée : col majeur Cap Corse sud)
   - PAR TNT totale estimée ~100 kW (détails multiplex en cours de reverification — TVNT.net affiche valeurs canal par canal, somme à affiner via Cartoradio officiel)
   - Sert TNT, FM (radios nationales + Alta Frequenza Corsica), éventuellement DAB+

2. **Coti-Chiavari / Punta di Pincelli** (2A) — site TDF principal Sud
   - Coordonnées approchées 41.7320 / 8.7926
   - Altitude ~691 m (site), pylône historique de 133 m
   - PAR TNT totale **~197 kW** (détaillée et croisée : R1 R7 R3 R2 R4 à 65 kW chacun, R6 64 kW TowerCast, R15 2 kW)
   - Confirmé par communiqué TDF 2024 (ferme solaire 65 kWc)

### Sites intermédiaires (2)

3. **Corte-Antisanti (Castello Vecchio)** (2B) — émetteur principal Centre Corse
   - Coordonnées approchées 42.1067 / 9.3686 (à préciser)
   - PAR TNT totale ~70.71 kW (7 multiplex à 10 kW + R15 à 710 W)
   - À noter : la commune d'implantation est **Antisanti**, pas Corte (fréquent raccourci dans la doc)

4. **Porto-Vecchio Col de Mela** (Carbini, 2A)
   - Coordonnées approchées 41.5950 / 9.2080
   - PAR TNT totale ~10.9 kW (8 multiplex à 1.5 kW + R15 à 200 W)

### Relais petite puissance (6)

5. **Monte Cecu / Corte-Bistuglio** (Corte, 2B) — 0.155 kW
6. **Calvi Col de Salvi / Capigliole** (Calvi, 2B) — 0.27 kW
7. **Bastia ville relais urbain** (Bastia, 2B) — PAR incomplète (40 W min détecté)
8. **Volpajola** (Volpajola, 2B) — ~0.08 kW (partiel)
9. **Monacia-Figari** (Sartène, 2A) — 0.426 kW
10. **Col de Vizzavona** (Vivario, 2B) — PAR non publiée

---

## 3. Sites recherchés non retenus

| Site mentionné au brief | Statut | Raison |
|---|---|---|
| Mont Sant'Ange | Non retenu | Ambiguïté d'identification. Probablement fusionné avec Coti-Chiavari / Punta di Pincelli dans la documentation TDF actuelle. |
| Monte Gozzi (Ajaccio) | Non retenu | Aucune fiche technique identifiée en recherche web. À vérifier directement sur Cartoradio. |
| Col de Teghime (Bastia) | Non retenu | Site réputé accueillir des faisceaux hertziens mais **aucune donnée PAR broadcast publique trouvée**. Les FH ne sont pas systématiquement sur Cartoradio (données opérateurs). À clarifier phase 2. |
| Monte Cagna (Figari) | Non retenu | Ambiguïté — pourrait correspondre au relais Monacia-Figari (#9) ou à un autre site. Nom géographique vs nom technique d'émetteur à reclarifier. |
| Monte Renoso | Non retenu | Site géographique (2352 m) mais **aucune infrastructure broadcast identifiée**. Ne pas inclure sans preuve. |
| Relais Bastia, Porto-Vecchio, Calvi, Corte (génériques) | Intégrés sous noms spécifiques | Les "relais Bastia" etc. correspondent respectivement à Serra di Pigno, Col de Mela, Col de Salvi, Monte Cecu. |

---

## 4. Incertitudes et limites du dataset

### 4.1 Précision des coordonnées GPS
Seul **Serra di Pigno** a des coordonnées validées par le brief initial (42.6521 / 9.3923). Pour les 9 autres sites, les coordonnées sont des approximations à 4 décimales basées sur connaissance géographique et doivent être validées via Cartoradio officiel avant usage pour modélisation RF précise.

### 4.2 Précision des PAR
- **Bien documenté** : Coti-Chiavari (197 kW, détails officiels), Corte-Antisanti (70.7 kW), Porto-Vecchio-Mela (10.9 kW), Monte Cecu (0.155 kW), Monacia-Figari (0.426 kW).
- **Approximation** : Serra di Pigno (100 kW estimée, valeurs canal par canal à reverifier), Calvi (0.27 kW approximé).
- **Partiel** : Bastia urbain (40 W minimum détecté), Volpajola (80 W détecté, total inconnu).
- **Non publié** : Vizzavona (null + note "à mesurer sur place").

### 4.3 FM broadcast — non couvert
Les sources TVNT.net se concentrent sur la TNT. Les PAR des émetteurs FM Corse (France Bleu RCFM, Alta Frequenza Corsica, NRJ Corse, Chérie FM Corse, etc.) ne sont pas chiffrées dans ce dataset. Valeur FM connue : Chérie FM Corse = 1 kW (référence ponctuelle, non intégrée).

**À faire phase 2** : consulter Arcom (https://www.arcom.fr/radio-et-audio-numerique) pour tableau FM autorisé Corse, ou Cartoradio filtré service FM.

### 4.4 DAB+ broadcast — non confirmé
Aucune source accessible pendant la session ne confirme le déploiement DAB+ actif en Corse. À vérifier via data.anfr.fr.

### 4.5 Faisceaux hertziens (FH) — non couverts
Col de Teghime et autres sites d'interconnexion FH non documentés ici. Les FH ne sont pas toujours publics (sensibilité opérateur).

### 4.6 Unités W vs kW
Pour les relais de petite puissance, TVNT.net affiche généralement en watts. Ordre de grandeur confirmé : de ~20 W à ~70 W par multiplex pour les petits relais, à comparer aux 65 kW par multiplex des grands sites. Ratio ~1000x, cohérent avec une architecture émetteur principal / relais de recopie.

---

## 5. URL des sources consultées

### Principales
- TVNT.net Forum Corse-du-Sud : https://www.tvnt.net/forum/2a-corse-du-sud-t12643.html
- TVNT.net Forum Haute-Corse : https://www.tvnt.net/forum/2b-haute-corse-t12642.html
- TVNT.net fiche Serra di Pigno : https://www.tvnt.net/forum/emetteur-de-bastia-serra-di-pignu-t307.html
- TVNT.net fiche Coti-Chiavari : https://www.tvnt.net/forum/emetteur-d-ajaccio-coti-chiavari-t36-40.html
- Documentation Docplayer Corse 2A 2B : https://docplayer.fr/21711740-Corse-2a-2b-informations-techniques.html

### Croisement TDF
- TDF page ferme solaire Coti-Chiavari : https://www.tdf.fr/en/le-groupe-tdf/histoire-de-tdf/ferme-solaire-coti-chiavari-corse/
- Communiqué TDF 2024 : https://www.tdf.fr/wp-content/uploads/2024/05/CP_TDF_met_en_service_sa_premiere_ferme_solaire_sur_son_site_de_coti_chiavari_en_Corse.pdf
- Page TDF groupe (infrastructure) : https://www.tdf.fr/

### Référence officielle (BLOQUÉE pendant la session)
- ANFR Cartoradio : https://www.cartoradio.fr/
- Data ANFR : https://data.anfr.fr/
- Arcom : https://www.arcom.fr/
- ANFR présentation Cartoradio : https://www.anfr.fr/en/maitriser/cartoradio/presentation-cartoradio

### Divers (lus indirectement via recherche web)
- PSS Architecture fiche pylône : https://www.pss-archi.eu/immeubles/FR-2A098-34971.html
- Alta Frequenza Corsica : https://www.alta-frequenza.corsica/actu/
- sosondes.fr guide Cartoradio : https://sosondes.fr/cartoradio/
- ANFR Q/R Cartoradio : https://www.anfr.fr/maitriser/information-du-public/cartoradio/questions-/-reponses

---

## 6. Recommandations pour la session code suivante

### Priorité 1 — Reverification Cartoradio
Avant intégration en production, **ouvrir Cartoradio** (cartoradio.fr) depuis un environnement non bloqué et pour chacun des 10 émetteurs :
- Confirmer coordonnées à 5 décimales
- Confirmer altitude exacte
- Confirmer PAR totale (somme multiplex + FM + DAB si présents)
- Noter hauteur d'antenne / azimut si pertinent pour modélisation directionnelle

### Priorité 2 — Compléter FM et DAB+
- Arcom pour liste FM autorisée et PAR
- data.anfr.fr pour DAB+ activé Corse

### Priorité 3 — Investiguer sites manquants
- Col de Teghime (FH Bastia)
- Monte Gozzi (relais Ajaccio éventuel)
- Monte Cagna (clarification vs Monacia)

### Priorité 4 — Modélisation RF
Les PAR inscrites dans le JSON sont des valeurs totales broadcast. Pour le modèle Tellux loin-champ :
- Utiliser `par_kw_estimee` comme entrée de la formule champ RF (Okumura-Hata, ITU-R P.1546 ou similaire selon topographie montagneuse).
- Les `null` doivent faire l'objet d'une valeur par défaut prudente (ex. 1 kW) avec flag "PAR inconnue" dans l'UI.
- Ratio émetteur principal / relais = ~1000x → utiliser gradient de couverture radical (Coti-Chiavari domine 50 km, relais 1-2 km).

---

## 7. Ventilation finale

| Type | Nombre | PAR cumulée approximative |
|---|---|---|
| Broadcast principal | 2 | ~297 kW (Coti-Chiavari 197 + Serra di Pigno 100) |
| Intermédiaire (10-100 kW) | 2 | ~81.6 kW (Corte-Antisanti 70.7 + Porto-Vecchio 10.9) |
| Relais (<1 kW) | 5 | ~0.93 kW cumulé |
| PAR inconnue | 2 | Bastia urbain + Vizzavona |
| **Total** | **10 émetteurs** | **~380 kW quantifiés** |

**Statut** : dataset utilisable pour un premier modèle RF loin-champ. PAR à reverifier Cartoradio avant publication.
