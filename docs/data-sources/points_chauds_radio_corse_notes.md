# Points chauds uranium / thorium Corse — note méthodologique

**Fichier :** `public/data/points_chauds_radio_corse.json`
**Date d'extraction :** 2026-04-21
**Source :** compilation documentaire BRGM Inventaire minier + littérature géochimique
**Statut :** données documentaires, **non mesurées par Tellux**

## Avertissement méthodologique

**Les doses gamma estimées dans ce fichier sont des ORDRES DE GRANDEUR DOCUMENTAIRES.** Elles ne résultent pas de mesures effectuées par Tellux mais d'une compilation de la littérature géochimique et minière sur les anomalies radiométriques documentées en Corse.

Avant toute interprétation sanitaire de ces valeurs, une mesure terrain certifiée (ASNR ou laboratoire agréé) est indispensable. Les ordres de grandeur reportés (150–200 nSv/h) restent dans la fourchette du fond naturel géologiquement élevé et ne déclenchent aucune alerte sanitaire spontanée.

## 5 points chauds retenus

### 1. Argentella (Calenzana, 2B)

Ancien site de prospection uranifère des années 1950-1960. Fermé sans avoir abouti à une exploitation industrielle, mais anomalie radiométrique résiduelle documentée par le BRGM. Accès public non réglementé, signalisation absente.

- **Coordonnées** : 42.5467 N, 8.7500 E
- **Dose estimée** : 200 nSv/h
- **Rayon d'influence** : 300 m
- **Source** : BRGM Inventaire minier national, fiche 2B_Argentella_U

### 2. Saleccia (Santo-Pietro-di-Tenda, 2B)

Plage à sables noirs lourds enrichie en monazite (thorium). Anomalie naturelle liée à la lithologie du bassin versant granitique. Fréquentation estivale — exposition publique limitée par durée.

- **Coordonnées** : 42.7653 N, 9.2281 E
- **Dose estimée** : 180 nSv/h
- **Rayon d'influence** : 500 m
- **Source** : littérature sédimentologie méditerranéenne + BRGM sables minéraux lourds Corse

### 3. Saint-Antoine / Manso (2B)

Zone du Fango avec prospections uranifères anciennes non industrielles (1950-1960). Anomalie légère documentée.

- **Coordonnées** : 42.4167 N, 8.8167 E
- **Dose estimée** : 150 nSv/h
- **Rayon d'influence** : 400 m

### 4. Plages Est du Cap Corse (Luri, 2B)

Série de plages à sables noirs lourds (Barcaggio, Tamarone, Marine de Meria). Enrichissement en monazite et zircon d'origine lithologique (serpentines locales).

- **Coordonnées** (approximatives) : 42.8833 N, 9.4833 E
- **Dose estimée** : 160 nSv/h
- **Rayon d'influence** : 300 m

### 5. Murato (2B) — serpentines amiantifères

Lithologie ultrabasique (serpentines) légèrement enrichie en U/Th naturels. La pertinence est secondaire pour `calcGammaAmbient` (signal faible) et marginale pour Tellux qui ne traite pas l'amiante.

- **Coordonnées** : 42.5650 N, 9.3250 E
- **Dose estimée** : 120 nSv/h
- **Rayon d'influence** : 600 m

## Méthode de compilation

Pour chaque point :

1. Recherche dans la littérature minière, géochimique ou sédimentologique d'une anomalie documentée
2. Extraction d'un ordre de grandeur de dose gamma au pied du site (typiquement 150–250 nSv/h pour une anomalie modérée)
3. Estimation du rayon d'influence par décroissance terrain typique (300–600 m selon la taille de la source)

Aucune dose estimée n'excède 250 nSv/h dans ce dataset — les valeurs restent dans la fourchette du fond naturel géologique élevé (150–300 nSv/h selon les références NCRP et UNSCEAR pour les zones granitiques).

## Intégration dans `calcGammaAmbient`

Le boost ponctuel s'ajoute à la composante cosmique (altitude) :

```
boost_ponctuel = Σ max(0, dose_estimée - 80) × (1 - d / rayon_influence)  pour d < rayon_influence
```

Baseline 80 nSv/h = fond naturel corse granitique moyen (UNSCEAR 2008).

Décroissance linéaire (simple, documentaire). Pas de modèle de diffusion gamma sophistiqué.

## Licence

Données publiques BRGM + compilation documentaire. Usage pédagogique Tellux sous licence publique du projet.

## Mise à jour et calibration

Ce dataset est appelé à évoluer quand :

1. **Mesures terrain Tellux** : protocole de mesure gamma ambiante directe sur ces sites avec un Geiger-Müller calibré, pour substituer les valeurs documentaires par des mesures réelles
2. **Accès Téléray ASNR** : l'API Téléray (en attente d'autorisation ASNR, lettre 01 envoyée 2026-04-14) donnera un fond naturel régional mesuré à 80 balises Corse, calibrant la baseline
3. **BRGM radiométrie aérienne** : dossier `BRGM-RADIO-001` (ROADMAP) pour obtenir les cartes U/Th/K aéroportées à 1:250 000 qui couvriraient toute la Corse avec mesures réelles
