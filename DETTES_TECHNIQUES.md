# Tellux — Dettes techniques ouvertes

**Dernière mise à jour :** 22 avril 2026

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

## Dettes fermées récemment

- **ELF-VECTOR-001** (avril 2026) — sommation vectorielle 2D implémentée dans `calcMagneticELF_v2`
- **BT-ELF-001** (avril 2026) — infrastructure BT asynchrone implémentée (calcul désactivé temporairement, voir BT-CALIBRATION-001)
- **ELF-CALIB-001** (avril 2026) — vérification des seuils visuels post-migration Biot-Savart, conservation des seuils 150/300/500 nT
- **WMM-CROSSCHECK-001** (avril 2026) — WMM 2025 cross-check intégré via grille précalculée
- **BDFORET-V2-001** (avril 2026) — couche Forêts publiques ONF intégrée

---

## Principes

- Chaque dette porte un identifiant pérenne `XXX-YYY-NNN` pour traçabilité.
- La priorité reflète l'impact sur la qualité du modèle et non l'urgence opérationnelle.
- Une dette n'est fermée qu'après implémentation validée et mise à jour du corpus correspondant.
- Les dettes gelées (`GELÉ-001`, `NCRP-001`) attendent une validation méthodologique externe avant implémentation.

*Fin du document.*
