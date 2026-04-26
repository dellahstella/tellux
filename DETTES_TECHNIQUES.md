# Tellux — Dettes techniques ouvertes

**Dernière mise à jour :** 26 avril 2026 — ajout des dettes CONTRIB-SCHEMA-001 (incohérence schéma stockage contributions, identifiée lors du fix Android PR #154), RADON-CLASS-DUPLICATE et HELPERS-INLINE-CONSTS (issues de la cartographie d'extraction du moteur, `docs/tellux-engine-extraction-plan.md`). Précédente : 25 avril 2026 — consolidation semaine 21-25 avril : enrichissement BT-CALIBRATION-001 (priorité Haute, mesures ratios ×57 à ×210), nouvelle dette EMAG-CRUSTAL-AUDIT-001 (Cowork Session B), précisions PR # sur les fermetures ELF-CALIB-001/WMM-CROSSCHECK-001/BDFORET-V2-001/ELF-VECTOR-001/BT-ELF-001, ajout en fermées récemment de SUPABASE-COMMUNE-FIELD-001 (PR #137) et ANTENNES-REFRESH-001 (PR #138), liens démarches externes sur TÉLÉ-001/HTA-TENSION-001/RADIO-AERO-001 (lettres envoyées 28-29 avril 2026). 25 avril — ajout RTE-OPENDATA-001. 24 avril — ajout RADON-L3-UNIFICATION-001 + WDMAM-NAMING-001.

Ce document liste les dettes techniques ouvertes identifiées dans l'application Tellux. Chaque dette fait l'objet d'un identifiant pérenne, d'une description factuelle et d'une condition de déblocage documentée. Aucune de ces dettes ne bloque la publication de la phase 1.

---

## Dettes actives

### GELÉ-001 — Constantes Expert gelées

**Description :** Les pondérations du mode Expertise (`w_M`, `w_RF`, `w_I`) et les bornes de normalisation (`EXPERT_BOUNDS_DEFAULT`) sont fixées à titre provisoire. Elles sont documentées comme telles dans l'interface (bandeau permanent du mode Expertise) et dans le code (commentaire « GELÉ — GELÉ-001 »).

**Priorité :** Haute

**Condition de déblocage :** Relecture méthodologique par un physicien tiers qualifié et validation explicite des constantes.

---

### NCRP-001 — Fond naturel terrestre gelé

**Description :** La composante terrestre de `calcGammaAmbient` (formule NCRP 94) est provisoirement gelée, en attente de validation méthodologique externe.

**Priorité :** Haute

**Condition de déblocage :** Lié à GELÉ-001.

---

### TÉLÉ-001 — API Téléray ASNR

**Description :** L'intégration en temps réel du réseau Téléray (débit de dose gamma) n'est pas réalisée. La composante ionisante actuelle repose sur la classification radon officielle en vigueur et la composante cosmique altitudinale via IGN RGE Alti.

**Priorité :** Moyenne

**Condition de déblocage :** En attente d'un retour de l'organisme concerné sur les conditions d'accès à l'API.

**Démarche externe :** lettre ASNR direction Téléray envoyée le 28 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles »).

---

### HTA-TENSION-001 — Voltage des lignes HTA

**Description :** Le dataset Supabase `hta_lines` ne comporte pas de champ voltage/tension permettant de différencier HTA 20 kV et HTB 63/90/225 kV. `calcMagneticELF_v2` applique un courant uniforme de 225 A (option de repli documentée).

**Priorité :** Moyenne

**Condition de déblocage :** Enrichissement du dataset via migration SQL ou accès à une source de données tension par segment.

**Démarche externe :** lettre EDF SEI direction Corse envoyée le 29 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles »). Lien transverse avec `BT-CALIBRATION-001` (la même lettre sollicite des caractéristiques techniques utiles à la recalibration BT).

---

### ELF-TRIPH-001 — Correction triphasée approximée

**Description :** La correction triphasée appliquée au calcul Biot-Savart ELF utilise un coefficient `k=0.5` approximé au-delà de 20 m. La géométrie réelle des pylônes (espacement des phases) n'est pas modélisée par segment.

**Priorité :** Faible

**Condition de déblocage :** Accès à des données géométriques pylône par pylône, ou modèle statistique validé.

---

### BT-CALIBRATION-001 — Cancellation insuffisante du modèle Biot-Savart sur lignes BT torsadées

**Description :** Le calcul des segments BT (basse tension, lignes torsadées) dans `calcMagneticELF_v2` utilise actuellement la même formule Biot-Savart et correction triphasée `k = 0.5` que les lignes HTA. Or cette correction est calibrée sur la géométrie pylône HTA (phases espacées de 1-3 m). Appliquée telle quelle aux câbles BT torsadés (phases espacées d'environ 1 cm), elle produit une cancellation très insuffisante. Audit post-merge PR #71 (2026-04-22) : ratios v2.5 (HTA seul) vs v2.6 (HTA + BT segments) sur 4 villes corses :

| Zone | v2.5 (nT) | v2.6 (nT) | Ratio |
|---|---:|---:|---:|
| Bastia centre | 160 | 33 592 | ×210 |
| Calvi | 208 | 26 654 | ×128 |
| Porto-Vecchio | 367 | 21 047 | ×57 |
| Ajaccio centre | 219 | 14 253 | ×65 |

Pour Ajaccio : 5 038 segments BT contribuent 14 134 nT, soit deux ordres de grandeur au-dessus des mesures urbaines typiques (50-300 nT documentés dans la littérature). Cause racine probable : décroissance attendue 1/d² ou 1/d³ au lieu de 1/d, et facteur de cancellation dépendant fortement de la géométrie torsadée des conducteurs BT. État actuel du code : le calcul BT par segments est désactivé (flag `USE_BT_SEGMENTS = false` dans `app.html`), et le proxy `BT_ZONES` legacy reste actif.

**Priorité :** Haute (impact ordre de grandeur en zone urbaine si activation prématurée)

**Condition de déblocage :** Recalibration du modèle BT par session dédiée. Trois leviers envisagés :
- Recalibration paramétrique (coefficient `k` BT distinct, cap par segment, distance minimale)
- Modèle statistique de densité BT par tuile
- Modèle Biot-Savart adapté aux câbles torsadés basse tension (1/d² ou 1/d³)

La validation physique préalable (littérature ou mesures terrain) est un prérequis.

**Lien transverse :** la lettre EDF SEI envoyée le 29 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles ») sollicite les caractéristiques techniques (tension, configuration des conducteurs, courants nominaux) qui éclaireraient cette calibration.

---

### RADIO-AERO-001 — Radiométrie aérienne

**Description :** L'intégration des données de radiométrie aérienne BRGM pour affiner la composante ionisante est non réalisée. Aucun flux WMS, WFS ou téléchargement public de ces données n'a été identifié lors de l'audit 2026-04-21.

**Priorité :** Faible

**Condition de déblocage :** En attente d'un retour de l'organisme concerné sur les conditions de mise à disposition de ces données.

**Démarche externe :** lettre BRGM direction régionale Corse envoyée le 29 avril 2026 (cf. `ROADMAP.md` section « Suivi des sollicitations institutionnelles »). La lettre sollicite également l'accès aux flux WFS géologie Corse et aux campagnes spectrogamma.

---

### BDFORET-GRANULARITE-001 — Granularité BD Forêt

**Description :** La couche Forêts publiques ONF actuellement intégrée ne permet pas de distinguer les essences (feuillus, conifères, maquis). La version BD Forêt V3 avec détail par essence n'est pas disponible en WMS raster stable.

**Priorité :** Faible

**Condition de déblocage :** Stabilisation de la version BD Forêt V3 en production, ou rasterisation locale d'une extraction shapefile.

---

### CORPUS-PILIERS-001 — Relecture corpus Pilier A et Pilier B post-migration Biot-Savart

**Description :** Le corpus scientifique interne a été scindé le 2026-04-21 en deux piliers distincts : Pilier A (14 fiches scientifiques S1-S14, en attente de relecture méthodologique externe par un physicien) et Pilier B (20 fiches patrimoine gamifiées P1-P20). Les fiches avaient initialement été formulées avec un modèle ELF basé sur 8 axes simplifiés. Depuis la migration Biot-Savart réel sur réseau HTA complet (avril 2026), le taux de validation de chaque fiche peut évoluer significativement.

**Historique.** Cette dette a été initialement identifiée sous l'ID `H1-H88-ELF-001` (formulation antérieure à la scission). L'ID est reformulé en `CORPUS-PILIERS-001` le 2026-04-23 pour refléter la structure post-scission. La correspondance H-numéro → fiche S ou P reste consultable dans `_corpus/` (fichiers `HYPOTHESES_SCIENTIFIQUES.md` et `HYPOTHESES_PATRIMOINE_GAMIFIEES.md`).

**Priorité :** Haute

**Condition de déblocage :** Session dédiée de relecture par pilier, avec recalcul des corrélations et mise à jour du corpus interne (repo privé `tellux-corpus-internal`). Pilier A : à prioriser dans le cadre de la relecture méthodologique externe. Pilier B : peut attendre la phase 2 de financement.

---

### MIGN-001 — Appelants legacy `calcAll`

**Description :** Un petit nombre d'appelants legacy de `calcAll` ne transmettent pas les paramètres `commune_info` et `altitude_m` introduits lors de la migration v2. Comportement non bloquant : les valeurs par défaut sont utilisées.

**Priorité :** Faible

**Condition de déblocage :** Session dédiée de nettoyage (non bloquant).

---

### MESURES-EM-BASCULE-001 — Bascule deux boutons couche Mesures EM

**Description :** La couche Mesures EM unifiée (mergée 2026-04-23) regroupe deux datasets hétérogènes dans un seul bouton UI : contributions citoyennes (layer `lCon`, clusterisé, Supabase `contributions`) et mesures certifiées ANFR/EXEM (layer `lCert`, non-clusterisé, `public/data/cartoradio_certified_corse.json`). À terme, quand le volume des certifiées dépassera environ 100 entrées (actuellement 30), la distinction visuelle entre les deux strates devra passer par deux boutons distincts pour permettre à l'utilisateur de filtrer l'un sans l'autre.

**Priorité :** Faible (non bloquant tant que le volume certifiées reste inférieur à ~100)

**Condition de déblocage :** dépassement du seuil de ~100 mesures certifiées OU feedback utilisateur signalant la confusion entre les deux strates OU session UI dédiée identifiant d'autres besoins de filtrage.

---

### RADON-L3-UNIFICATION-001 — Unification des deux sources radon (GeoJSON polygones vs JSON L3 INSEE)

**Description :** Tellux maintient actuellement deux sources de données radon indépendantes pour la Corse. D'une part, `public/data/radon_zones_corse.geojson` (253 polygones communaux officiels ASNR, 216 cat.3 + 37 cat.2) est consommé par la couche cartographique `lRadon` via `buildRadonLayer()` (introduit par la PR #130 du 24 avril 2026 — intégration ; l'unification proprement dite reste pendante). D'autre part, `public/data/radon_communes_level3_corse.json` (28 communes explicites + règle « tout 2A classé cat.3 », 152 communes théoriques cat.3 uniquement) est consommé par `loadRadonCommunesL3()` → `isCommuneRadonL3()` → `calcRadonPotential()` pour booster la classe du score composite lorsque la commune cliquée est officiellement classée. Les deux sources pointent vers le même décret (2018-434, arrêté du 27 juin 2018) mais ont des couvertures différentes : le GeoJSON est exhaustif (253 communes cat.2+cat.3 aux frontières réelles), le JSON L3 utilise un proxy (règle départementale 2A + liste 2B partielle, cat.3 seulement). Risque de divergence documentaire : une commune 2B cat.2 du GeoJSON n'apparaîtra pas dans `isCommuneRadonL3()`.

**Priorité :** Faible (aucun bug fonctionnel ; les deux flux cohabitent proprement. Dette documentaire : une seule source canonique serait plus propre à long terme)

**Condition de déblocage :** Session dédiée d'unification avec (1) test d'équivalence quantitatif — les 216 cat.3 du GeoJSON couvrent-ils bien les 124 communes 2A intégrales + 28 communes 2B listées dans le JSON L3 actuel, sans régression ? Quels INSEE sont dans l'un mais pas l'autre ? (2) refonte de `isCommuneRadonL3()` pour lire depuis un index INSEE extrait du GeoJSON au chargement (via `loadRadonCommunesFromGeoJSON()` — un seul fetch partagé avec la couche cartographique). (3) suppression de `public/data/radon_communes_level3_corse.json`, de `loadRadonCommunesL3()`, des constantes `RADON_L3_INSEE_SET`, `RADON_L3_NAME_SET`, `RADON_L3_SOURCE`, `RADON_2A_APPLIES_ALL`, et de la fonction `normCommuneName()` si elle n'est utilisée que par ce flux. (4) vérification que le composite `calcRadonPotential` continue de booster correctement la classe à 3 sur un clic dans une commune 2A et sur un clic dans une commune 2B listée. Zone concernée : `app.html` uniquement (fichier data à supprimer en parallèle).

---

### WDMAM-NAMING-001 — Renommage identifiants JS `wmsWDMAM`, `togWDMAM`, `LEGEND_HTML.wdmam`, `#b-wdmam`

**Description :** La couche de cartographie magnétique mondiale charge dynamiquement le raster EMAG2v3 depuis NOAA NCEI (endpoint ArcGIS REST, `Meyer et al. 2017`). Elle a historiquement été nommée d'après `WDMAM` (World Digital Magnetic Anomaly Map de `IAGA/CGMW`, `Maus et al. 2009`), qui est un produit distinct. La PR #125 (2026-04-24) a corrigé les libellés visibles par l'utilisateur : le bouton affiche désormais « EMAG2 mondial », la légende titre « EMAG2 mondial » avec sous-titre « Anomalies crustales mondiales dynamiques », et la citation source renvoie à `Meyer et al. 2017`. Les identifiants JS (`wmsWDMAM`, `togWDMAM`, clé `LEGEND_HTML.wdmam`, ID HTML `#b-wdmam`, classe CSS `on-wdmam`, appels `showLegend('wdmam', ...)`) restent cependant nommés d'après le faux-ami. Le renommage a été volontairement différé pendant la PR #125 pour éviter une régression silencieuse sur un sélecteur oublié.

**Priorité :** Faible (cosmétique, aucun bug fonctionnel, non bloquant)

**Condition de déblocage :** Session dédiée de renommage avec grep exhaustif pré-changement sur les chaînes `wdmam` / `WDMAM` / `b-wdmam` / `on-wdmam`, puis test navigateur manuel post-renommage (activation couche, affichage légende en Zone 2, toggle on/off, resize responsive). Nom cible à valider lors de l'implémentation — options ouvertes : `wmsEmagGlobal` / `togEmagGlobal` / `emagGlobal` (anglophone, cohérent avec le reste du code), ou `wmsEmagMondial` / `togEmagMondial` / `emagMondial` (francophone, cohérent avec le libellé UI). Zone concernée uniquement : `app.html` (aucun autre fichier ne référence ces identifiants — à confirmer au grep).

---

### EMAG-CRUSTAL-AUDIT-001 — Audit duplication potentielle entre couches `emag` et `crustal` dans `app.html`

**Description :** Trois couches existent dans `app.html` représentant potentiellement deux datasets distincts sur le même phénomène physique d'anomalies crustales magnétiques : `emag` (couche actuelle EMAG2v3 NOAA, 2 arc-min, domaine public, retenue pour la Corse), `crustal` (couche de comparaison crustale mondiale ouverte par INTL-CRUSTAL-001, 5 références mondiales) et `wdmam` (héritage historique pointant en réalité vers EMAG2v3 dynamique, voir `WDMAM-NAMING-001`). La note de recherche `docs/EMAG2_WDMAM_NOTE_RECHERCHE.md` (Cowork Session B 24 avril 2026) clarifie la distinction WDMAM vs EMAG2v3 et confirme qu'EMAG2v3 est le dataset recommandé à l'échelle de la Corse. Reste à confirmer si les couches `emag` et `crustal` pointent sur des tuiles distinctes ou redondantes, et si la couche `wdmam` est effectivement un alias d'`emag` ou un endpoint séparé.

**Priorité :** Faible (cosmétique tant qu'aucun bug fonctionnel ne se manifeste, mais utile pour la lisibilité du code et la cohérence éditoriale)

**Condition de déblocage :** Session dédiée d'audit avec (1) grep des endpoints utilisés par `emag`, `crustal`, `wdmam` dans `app.html` ; (2) confirmation visuelle en navigateur que les rendus diffèrent ou non ; (3) si redondance avérée, suppression d'une des deux couches et clarification du nommage. Périmètre : `app.html` (zone non gelée, modification autorisée). Ordonnancement avec `WDMAM-NAMING-001` à arbitrer (les deux dettes peuvent être traitées dans la même session de nettoyage).

---

### RTE-OPENDATA-001 — Demande de cadrage RTE différée post-financement

**Description :** La lettre RTE Open Data v1 (rédigée 22 avril 2026, recadrée 25 avril 2026) sollicitait trois éléments auprès de la direction Open Data RTE : confirmation de stabilité des flux eco2mix utilisés actuellement par Tellux (endpoint `digital.iservices.rte-france.com/open_api/consumption/v1/short_term?sandbox=true`), validation de l'usage non commercial public d'eco2mix sandbox dans le contexte cartographique Tellux, orientation sur d'éventuels jeux de données Corse-spécifiques RTE susceptibles de remplacer le profil horaire estimé du modèle local de repli. Décision 2026-04-25 : envoi différé. Le canal officiel RTE passe par un formulaire de contact ODRÉ (`opendata.reseaux-energies.fr`) limité aux messages courts, inadapté à une demande structurée multi-points. L'envoi formel est reporté à la phase post-financement, dans un cadre institutionnel adapté (structure dédiée, courrier sur en-tête, canal direction Open Data RTE direct). En attendant, Tellux continue d'utiliser eco2mix sandbox dans le respect du quota officiel (50 000 appels API par utilisateur et par mois, mentionné dans les CGU ODRÉ). Aucune action technique requise côté Tellux. Lien interne : la lettre v1 est archivée hors du repo public ; une version recadrée sera produite pour l'envoi post-financement. Lien transverse : `chargeFacteur` (variable consommée par `calcMagneticELF_v1` / `calcMagneticELF_v2` dans `app.html`) repose actuellement sur cet endpoint sandbox, avec fallback profil horaire local en cas d'échec.

**Priorité :** Faible (différée, non bloquante — le flux sandbox actuel est fonctionnel)

**Condition de déblocage :** Post-obtention du financement Phase 1 (CTC ou autre). Reformulation de la lettre v1 dans un cadre institutionnel adapté au canal direction RTE.

---

### CONTRIB-SCHEMA-001 — Incohérence du schéma de stockage des contributions (Mesure technique vs Capteurs appareil)

**Description :** Les deux flux d'écriture vers la table Supabase `contributions` stockent la valeur de mesure dans deux unités différentes. Le flux « Mesure technique » (formulaire `cform`) convertit la valeur saisie en nT et stocke `unite='nT'` quel que soit le choix de l'utilisateur (`app.html` lignes 4866-4868 et 4873). Le flux « Capteurs appareil » (`ctab-cap`) stocke la valeur brute renvoyée par l'API Magnetometer en µT et stocke `unite='µT'` (`app.html` lignes 7120-7121). La colonne `valeur` mélange donc deux unités selon la provenance de la contribution, ce qui complique l'agrégation, les comparaisons et toute requête SQL transversale. Identifiée lors de l'audit du 26 avril 2026 ayant conduit à la PR #154 (fix affichage magnétomètre). La dette est masquée côté affichage par la fonction `formatMagneticField` (introduite par la PR #154) qui lit `c.unite` comme unité canonique, mais le schéma reste incohérent au niveau stockage.

**Priorité :** Faible (masquée côté affichage, sans bug fonctionnel direct)

**Condition de déblocage :** Harmoniser le pipeline d'écriture pour que les deux flux convergent sur une même unité de stockage (a priori nT). Migration Supabase à prévoir pour normaliser les contributions historiques flux B (multiplier `valeur` par 1000 sur les lignes où `unite='µT'`, puis passer `unite` à `nT`).

---

### RADON-CLASS-DUPLICATE — Doublon du mapping `RADON_CLASS_BY_LITHOLOGY` dans `app.html`

**Description :** Le mapping `RADON_CLASS_BY_LITHOLOGY` (correspondance lithologie → classe radon 1/2/3) est défini en deux endroits dans `app.html` : dans `calcSubstrateContext` (ligne ~3939) et dans `calcRadonPotential` (ligne ~4102). Risque de dérive entre les deux copies si l'une est mise à jour sans l'autre. Le contenu actuel est identique et stable. Identifiée le 26 avril 2026 lors de la cartographie d'extraction du moteur (`docs/tellux-engine-extraction-plan.md` section 6.7).

**Priorité :** Faible (cosmétique, contenu actuel identique)

**Condition de déblocage :** Centraliser le mapping en un seul export (`data/radon-classification.js` ou équivalent) lors de l'extraction du moteur. Référence : `docs/tellux-engine-extraction-plan.md` section 6.7.

---

### HELPERS-INLINE-CONSTS — Constantes physiques inline dans le moteur de calcul

**Description :** Plusieurs constantes physiques sont définies inline dans le corps de fonctions du moteur de calcul de `app.html`, recréées à chaque appel et non testables en isolation. Liste identifiée le 26 avril 2026 lors de la cartographie du moteur (`docs/tellux-engine-extraction-plan.md` section 6.8) :
- `MU0_OVER_2PI` dans `calcBiotSavartSegment` (ligne ~3350)
- `METERS_PER_DEG_LAT` dans `calcBiotSavartSegment` et `calcBiotSavartSegmentVec` (lignes ~3090 et 3130)
- `METERS_PER_DEG_LON` dans `calcBiotSavartSegment` et `calcBiotSavartSegmentVec` (lignes ~3091 et 3131)
- `RIVER_PTS` dans `calcSubstrateContext`

**Priorité :** Faible (sans impact runtime significatif, mais nuit à la testabilité et à la lisibilité du code)

**Condition de déblocage :** Hisser ces constantes au niveau module lors de l'extraction du moteur. Référence : `docs/tellux-engine-extraction-plan.md` section 6.8.

---

## Dettes fermées récemment

- **ANTENNES-REFRESH-001** (24 avril 2026, PR #138) — workflow GitHub Actions de refresh mensuel des données antennes ANFR. Créée et fermée le même jour par Cowork Session A. Script `scripts/build_antennes_par_commune_corse.py`, sortie `public/data/antennes_par_commune_corse.json`, documentation `docs/operations/refresh-antennes.md`.
- **SUPABASE-COMMUNE-FIELD-001** (24 avril 2026, PR #137) — colonne `code_insee_commune` ajoutée à la table Supabase `contributions` pour permettre la jointure commune dans la Fiche commune `mairies.html`. Créée et fermée le même jour par Cowork Session A. Script de remplissage `scripts/fix_supabase_commune_insee.py`.
- **INTL-CRUSTAL-001** (23 avril 2026) — module de calibration crustale mondiale réimplémenté en EM pur. Tableau `CRUSTAL_REFS` (5 entrées : Bangui, Kursk, Vredefort, Ries, Chicxulub) avec `name`, `lat`, `lon`, `nT`, `radius_km`, `type`, `source`, `desc`. Couche Leaflet opt-in `crustal` (bouton `b-crustal`, désactivée par défaut) avec 5 cercles d'emprise + 5 markers divIcon. Panneau comparatif Leaflet Control `topright` : valeur EMAG2v3 locale au centre carte, 5 barres log(|nT|) des références mondiales, ligne "Centre carte" distincte. Aucun site patrimoine ; vérification anti-pollution passée (grep 17 termes negatif). Palette DA v2 gelée : Porphyre négatives, Ocre positives. Voir section « Module comparaison anomalies crustales mondiales » (archive ci-dessous).
- **CSS-HARMONISATION-001** (23 avril 2026) — aliases courts déjà ajoutés en amont (commit `66fd6ce`) ; 4 variables hardcodées renommées sémantiquement dans `:root` de `app.html` (`--tx2`→`--ardoise-clair`, `--bg2`→`--pierre-ombre`, `--acc2`→`--maquis-clair`, `--acc3`→`--maquis-pale`, ~137 occurrences) ; `Georgia` retiré du fallback `--font-display` (Fraunces self-hosted depuis PR #83). `DM Sans`/`DM Mono` déjà absents.
- **ELF-VECTOR-001** (21 avril 2026, PR #71) — sommation vectorielle 2D implémentée dans `calcMagneticELF_v2`
- **BT-ELF-001** (21 avril 2026, PR #71) — infrastructure BT asynchrone implémentée (calcul désactivé temporairement, voir `BT-CALIBRATION-001`)
- **ELF-CALIB-001** (21 avril 2026, PR #69) — vérification des seuils visuels post-migration Biot-Savart, conservation des seuils 150/300/500 nT (Scénario A)
- **WMM-CROSSCHECK-001** (21 avril 2026, PR #67) — WMM 2025 cross-check intégré via grille précalculée (851 points, 124 KB, résolution 0.05°), affichage Mode Expertise « Écart IGRF/WMM », validation 3 points témoins (Ajaccio, Bastia, Monte Cinto)
- **BDFORET-V2-001** (21 avril 2026, PR #67, fermeture partielle) — couche Forêts publiques ONF intégrée via WMS IGN `FORETS.PUBLIQUES`. La granularité essences/forêts privées reste pendante via `BDFORET-GRANULARITE-001`.
- **SUPABASE-INSERT-001** (22 avril 2026) — policies INSERT permissives `WITH CHECK (true)` remplacées sur `contributions` et `orientations_contributions`. Migration `005_security_hardening.sql` : validation GPS mondiale (lat/lon), `note`/`commentaire` ≤ 500 chars, `azimut` 0-360, `site_id` non vide, rate limiting 10 contributions/heure par `session_id` via `check_contribution_rate_limit()`. Advisors Supabase : 0 alerte résiduelle. Limite connue : rate limit contournable en changeant de session_id (protection anti-spam naïf, non anti-attaquant déterminé).

---

## Principes

- Chaque dette porte un identifiant pérenne `XXX-YYY-NNN` pour traçabilité.
- La priorité reflète l'impact sur la qualité du modèle et non l'urgence opérationnelle.
- Une dette n'est fermée qu'après implémentation validée et mise à jour du corpus correspondant.
- Les dettes gelées (`GELÉ-001`, `NCRP-001`) attendent une validation méthodologique externe avant implémentation.

*Fin du document.*
