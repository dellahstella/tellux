# Tellux — Dettes techniques ouvertes

**Dernière mise à jour :** 22 avril 2026 (ouverture CSS-HARMONISATION-001)

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

---

### HTA-TENSION-001 — Voltage des lignes HTA

**Description :** Le dataset Supabase `hta_lines` ne comporte pas de champ voltage/tension permettant de différencier HTA 20 kV et HTB 63/90/225 kV. `calcMagneticELF_v2` applique un courant uniforme de 225 A (option de repli documentée).

**Priorité :** Moyenne

**Condition de déblocage :** Enrichissement du dataset via migration SQL ou accès à une source de données tension par segment.

---

### ELF-TRIPH-001 — Correction triphasée approximée

**Description :** La correction triphasée appliquée au calcul Biot-Savart ELF utilise un coefficient `k=0.5` approximé au-delà de 20 m. La géométrie réelle des pylônes (espacement des phases) n'est pas modélisée par segment.

**Priorité :** Faible

**Condition de déblocage :** Accès à des données géométriques pylône par pylône, ou modèle statistique validé.

---

### BT-CALIBRATION-001 — Calibration BT inadaptée

**Description :** Le calcul des segments BT (basse tension, lignes torsadées) dans `calcMagneticELF_v2` utilise actuellement la même formule Biot-Savart et correction triphasée que les lignes HTA. Cette approche a produit des ordres de grandeur non physiques en zone urbaine dense lors des tests de calibration. Le calcul BT par segments est désactivé (flag `USE_BT_SEGMENTS = false` dans `app.html`), et le proxy `BT_ZONES` legacy est actif.

**Priorité :** Moyenne

**Condition de déblocage :** Recalibration du modèle BT par session dédiée. Trois leviers envisagés :
- Recalibration paramétrique (coefficient, cap par segment, distance minimale)
- Modèle statistique de densité BT par tuile
- Modèle Biot-Savart adapté aux câbles torsadés basse tension

La validation physique préalable (littérature ou mesures terrain) est un prérequis.

---

### RADIO-AERO-001 — Radiométrie aérienne

**Description :** L'intégration des données de radiométrie aérienne BRGM pour affiner la composante ionisante est non réalisée. Aucun flux WMS, WFS ou téléchargement public de ces données n'a été identifié lors de l'audit 2026-04-21.

**Priorité :** Faible

**Condition de déblocage :** En attente d'un retour de l'organisme concerné sur les conditions de mise à disposition de ces données.

---

### BDFORET-GRANULARITE-001 — Granularité BD Forêt

**Description :** La couche Forêts publiques ONF actuellement intégrée ne permet pas de distinguer les essences (feuillus, conifères, maquis). La version BD Forêt V3 avec détail par essence n'est pas disponible en WMS raster stable.

**Priorité :** Faible

**Condition de déblocage :** Stabilisation de la version BD Forêt V3 en production, ou rasterisation locale d'une extraction shapefile.

---

### H1-H88-ELF-001 — Hypothèses patrimoine post-migration ELF

**Description :** Les hypothèses patrimoine documentées dans le corpus scientifique interne (H1 à H88) ont été formulées avec un modèle ELF basé sur 8 axes simplifiés. Depuis la migration Biot-Savart réel sur réseau HTA complet (avril 2026), le taux de validation de ces hypothèses peut évoluer significativement.

**Priorité :** Haute

**Condition de déblocage :** Session dédiée de relecture des hypothèses post-migration, avec recalcul des corrélations et mise à jour du corpus.

---

### MIGN-001 — Appelants legacy `calcAll`

**Description :** Un petit nombre d'appelants legacy de `calcAll` ne transmettent pas les paramètres `commune_info` et `altitude_m` introduits lors de la migration v2. Comportement non bloquant : les valeurs par défaut sont utilisées.

**Priorité :** Faible

**Condition de déblocage :** Session dédiée de nettoyage (non bloquant).

---

### INTL-CRUSTAL-001 — Module de calibration crustale mondiale (EM pur)

**Description :** La couche « Mondial (calibration) » et la jauge « Contexte mondial » du popup ont été retirées de `app.html` (PR `fix/app-residus-purge-patrimoine`, 22 avril 2026). L'ancienne implémentation mélangeait 2 références EM légitimes (Bangui −1000 nT, Ries −200 nT) avec 3 toponymes patrimoine corses (Bonifacio, Murato, Cauria), et sa fonction constructrice `buildIntlLayer` avait été retirée pendant la purge v6.0 sans nettoyer ses appelants, provoquant un `ReferenceError` au boot via l'auto-activation `tog('intl', …)`.

**Priorité :** Faible

**Condition de déblocage :** Réimplémentation d'un module de calibration crustale mondiale EM pur, basé exclusivement sur des références à pertinence magnétique documentée (cratères d'impact majeurs : Bangui, Kursk, Vredefort, Ries, Chicxulub ; grandes anomalies crustales listées dans la littérature USGS/EMAG2). Aucun site patrimoine ne doit figurer dans le tableau de références. La spécification du module inclura :
- Tableau `CRUSTAL_REFS` avec colonnes `name`, `nT`, `source`, `doi`, `lat`, `lon`
- Jauge popup optionnelle (toggle utilisateur, hors-champ du score composite)
- Couche Leaflet des marqueurs mondiaux (zoom-dépendante)
- Légende listant les sources USGS/EMAG2/publications

### CSS-HARMONISATION-001 — Cohérence CSS entre app.html et index.html

**Description :** L'audit du 18 avril 2026 (branche `chore/app-audit-da`, supprimée après documentation) identifiait trois points de cohérence CSS entre `app.html` et la landing `index.html`.

- **Divergence de nommage des variables** : `app.html` utilise `--tx-ardoise`, `--font`, `--font-display`, `--mono` ; `index.html` utilise `--ardoise`, `--ff`, `--fu`, `--fm`. Correctif : ajouter des aliases courts dans `:root` d'`app.html` (additif, aucun breaking change).
- **Variables sans nom sémantique dans `:root`** : `--tx2 #3D424A`, `--bg2 #EFE9DC`, `--acc2 #4F7048`, `--acc3 #E5EBE0` sont hardcodées. À rattacher à la palette Tellux v2 (Ardoise / Pierre / Ocre / Maquis).
- **Résidus potentiels** : références `DM Sans`, `DM Mono`, `Georgia,serif` inline dans `app.html` — à vérifier et nettoyer (probables vestiges antérieurs à PR #83 self-host fonts).

**Priorité :** Faible. N'impacte pas les utilisateurs. Utile pour la maintenance et la réutilisation de composants entre pages.

**Hors scope** : les 951 occurrences de couleurs hardcodées des catégories cartographiques (231 valeurs uniques, palettes métier hors DA v2).

**Condition de déblocage :** Session dédiée CSS — audit `app.html` courant + patch aliases + nettoyage résidus.

---

## Dettes fermées récemment

- **ELF-VECTOR-001** (avril 2026) — sommation vectorielle 2D implémentée dans `calcMagneticELF_v2`
- **BT-ELF-001** (avril 2026) — infrastructure BT asynchrone implémentée (calcul désactivé temporairement, voir BT-CALIBRATION-001)
- **ELF-CALIB-001** (avril 2026) — vérification des seuils visuels post-migration Biot-Savart, conservation des seuils 150/300/500 nT
- **WMM-CROSSCHECK-001** (avril 2026) — WMM 2025 cross-check intégré via grille précalculée
- **BDFORET-V2-001** (avril 2026) — couche Forêts publiques ONF intégrée
- **SUPABASE-INSERT-001** (22 avril 2026) — policies INSERT permissives `WITH CHECK (true)` remplacées sur `contributions` et `orientations_contributions`. Migration `005_security_hardening.sql` : validation GPS mondiale (lat/lon), `note`/`commentaire` ≤ 500 chars, `azimut` 0-360, `site_id` non vide, rate limiting 10 contributions/heure par `session_id` via `check_contribution_rate_limit()`. Advisors Supabase : 0 alerte résiduelle. Limite connue : rate limit contournable en changeant de session_id (protection anti-spam naïf, non anti-attaquant déterminé).

---

## Principes

- Chaque dette porte un identifiant pérenne `XXX-YYY-NNN` pour traçabilité.
- La priorité reflète l'impact sur la qualité du modèle et non l'urgence opérationnelle.
- Une dette n'est fermée qu'après implémentation validée et mise à jour du corpus correspondant.
- Les dettes gelées (`GELÉ-001`, `NCRP-001`) attendent une validation méthodologique externe avant implémentation.

*Fin du document.*
