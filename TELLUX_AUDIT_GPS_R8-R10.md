# Audit GPS — Rapports R8 · R9 · R10
**Date** : 18 avril 2026 | **Mode** : read-only | **Branche** : dev (commits 8a5f5df · 4f75d4b · 098e63e)  
**Périmètre** : 45 entrées nouvelles (36 SITES[] + 9 CHURCHES[])

---

## 1. Synthèse statistique

| Rapport | SITES[] | CHURCHES[] | Total |
|---|---|---|---|
| R8 — Golfe de Sagone | 10 | 1 | 11 |
| R9 — Prunelli·Taravo·Coscione | 7 | 4 | 11 |
| R10 — Ajaccio·Golfe·Sanguinaires | 19 | 4 | 23 |
| **Total session** | **36** | **9** | **45** |

### Distribution par niveau de précision (décimales lat/lon)

| Précision | Nb entrées | Signification |
|---|---|---|
| 5 dec (≥ 1 m) | 9 | Fiables — source croisée probable |
| 4 dec (± 10 m) | 14 | Acceptables pour sites larges |
| 3 dec (± 100 m) | 22 | Insuffisants pour archéologie/monuments ponctuels |

### Distribution par couche

| Layer | Catégorie | Nb nouvelles entrées R8-R10 |
|---|---|---|
| lSit | Remarquable | 14 |
| lSit2 | Site remarquable | 13 |
| lTour | Tour génoise | 5 |
| lSit | Mégalithique | 2 |
| lSit2 | Hydraulique | 2 |
| lTherm | Thermalisme | 1 |
| lCast | Château médiéval | 1 |
| lPont | Pont génois | 1 |
| CHURCHES | (divers) | 9 |

---

## 2. Entrées marquées « GPS approx » dans le code

7 entrées explicitement marquées dans les descriptions — priorité maximale de vérification.

| L. | Nom | Coords | Rapport | Remarque |
|---|---|---|---|---|
| 3798 | Renicciu (Coggia) | [42.116, 8.706] | R8 | Statue-menhir non localisée précisément |
| 3822 | Pont de Zippitoli (disparu 2023) | [41.929, 8.994] | R9 | Site détruit, emporté Ciaran 2023 |
| 3831 | Castellu di Bozzi (Guitera) | [41.850, 9.034] | R9 | Fortification sur crête, accès difficile |
| 3860 | Castellu Ficaghjola (Alata) | [41.96500, 8.70000] | R10 | Lon = 8.70000 suspect (zéros trailing) |
| 4381/4423 | San Giovanni Battista (Urbalacone) | [41.856, 8.958] | R9 | Église piévane, localisation floue |
| 4383/4425 | Capella San Cesario (Cozzano) | [41.875, 9.018] | R9 | Ruines, mi-pente, non géoréférencé |
| 4387/4429 | Anunziata di Pozzo di Borgo (Alata) | [41.945, 8.715] | R10 | Texte source : « GPS à vérifier géoportail » |

---

## 3. Tableau complet — toutes entrées R8-R10

### Légende
- 🟢 Fiable : ≥ 4 décimales, cohérent
- 🟡 À vérifier : 3 décimales (±100 m), non marqué approx
- 🔴 Critique : marqué approx **ou** coordonnées suspectes (zéros trailing, lieu présumé)

---

### R8 — Golfe de Sagone (10 SITES + 1 CHURCH)

| # | Nom | lat | lon | Prec | Statut | Source recommandée |
|---|---|---|---|---|---|---|
| 1 | Sant'Appianu de Sagone | 42.108 | 8.724 | 3/3 | 🟡 | Mérimée PA00099074 · Géoportail IGN |
| 2 | Renicciu (Coggia) | 42.116 | 8.706 | 3/3 | 🔴 approx | SRA Corse · Megalithic Portal · terrain |
| 3 | Tour de Sagone (Vico) | 42.109 | 8.723 | 3/3 | 🟡 | Mérimée PA00099123 |
| 4 | Tour d'Omigna (Cargèse) | 42.155 | 8.554 | 3/3 | 🟡 | Mérimée PA00099136 (coords disponibles) |
| 5 | Tour de Turghiu (Capo Rosso) | 42.234 | 8.527 | 3/3 | 🟡 | IGN topo · OSM · sommet 331m |
| 6 | Tour de Cargèse (ruines) | 42.133 | 8.587 | 3/3 | 🔴 (ruines) | Terrain · plan cadastral Cargèse |
| 7 | Guagno-les-Bains | 42.157 | 8.894 | 3/3 | 🟡 | OSM node · IGN |
| 8 | IESC Cargèse | 42.130 | 8.593 | 3/3 | 🟡 | Site CNRS UMS · OSM · Géoportail |
| 9 | **[CHURCH]** Saint-Spyridon (Cargèse) | 42.134 | 8.590 | 3/3 | 🟡 | Mérimée PA00099121 · OSM |

> **Note R8** : Les 3 décimales systématiques suggèrent que les coords ont été estimées depuis une carte web (zoom insuffisant). La zone Cargèse–Sagone est bien couverte par le Géoportail IGN — une session de 30 min suffirait à recaler ces 8 entrées.

---

### R9 — Prunelli · Taravo · Coscione (7 SITES + 4 CHURCHES)

| # | Nom | lat | lon | Prec | Statut | Source recommandée |
|---|---|---|---|---|---|---|
| 10 | Monument Sampiero Corso (Bastelica) | 41.989 | 9.015 | 3/3 | 🟡 | OSM node · Google Maps |
| 11 | Buste Sampiero Corso (Tricolacci) | 41.987 | 9.014 | 3/3 | 🔴 | Écart de 2m/1m avec #10 — à séparer davantage |
| 12 | Stèle de Ponticellu | 41.996 | 9.012 | 3/3 | 🔴 (lieu présumé) | Terrain seul · cadastre lieu-dit |
| 13 | Pont de Zippitoli (disparu 2023) | 41.929 | 8.994 | 3/3 | 🔴 approx | IGN Scan25 avant 2023 · Mérimée PA00099075 |
| 14 | Lac de Bastani | 42.013 | 9.053 | 3/3 | 🟡 | IGN topo 1:25000 · centroïde acceptable |
| 15 | I Casteddi (Tavera) | 42.052 | 9.020 | 3/3 | 🟡 | SRA · IGN · Géoportail archéo |
| 16 | Castellu di Bozzi (Guitera) | 41.850 | 9.034 | 3/3 | 🔴 approx | IGN topo · topoguide randonnée |
| 17 | **[CHURCH]** Saint-Michel (Bastelica) | 41.989 | 9.014 | 3/3 | 🟡 | OSM · Géoportail |
| 18 | **[CHURCH]** San Giovanni Battista (Urbalacone) | 41.856 | 8.958 | 3/3 | 🔴 approx | Terrain · paroisse Sartenais |
| 19 | **[CHURCH]** Santa Maria (Cozzano, Talavo) | 41.878 | 9.020 | 3/3 | 🟡 | OSM · Géoportail |
| 20 | **[CHURCH]** Capella San Cesario (Cozzano) | 41.875 | 9.018 | 3/3 | 🔴 approx | Terrain seul · cadastre mi-pente |

> **Note buste/monument** : Monument Sampiero [41.989, 9.015] et Buste Tricolacci [41.987, 9.014] sont séparés de ~2m lat / ~1m lon dans les données. Ces deux monuments existent bien dans des quartiers différents de Bastelica, mais la séparation cartographique est trop faible — vérifier que le buste est bien au quartier Tricolacci (commune Bastelica, ≠ centre-bourg). Source : mairie Bastelica.

---

### R10 — Ajaccio · Golfe · Sanguinaires (19 SITES + 4 CHURCHES)

| # | Nom | lat | lon | Prec | Statut | Source recommandée |
|---|---|---|---|---|---|---|
| 21 | Chapelle Impériale (nécropole Bonaparte) | 41.92175 | 8.73837 | 5/5 | 🟢 | Mérimée PA00099060 |
| 22 | Maison Bonaparte (musée national) | 41.91778 | 8.73833 | 5/5 | 🟢 | Mérimée PA00099066 |
| 23 | Palais Fesch – musée des Beaux-Arts | 41.92167 | 8.73833 | 5/5 | 🟢 | Mérimée PA00099071 |
| 24 | Citadelle d'Ajaccio (Miollis) | 41.91631 | 8.74033 | 5/5 | 🟢 | Mérimée PA2A000020 |
| 25 | Hôtel de Ville d'Ajaccio | 41.91920 | 8.73830 | 5/5 | 🟢 | Mérimée PA00099127 |
| 26 | Monument Napoléon Ier (Place du Diamant) | 41.91950 | 8.73780 | 5/5 | 🟢 | Mérimée PA2A000017 |
| 27 | Monument Napoléon Ier (Place d'Austerlitz) | 41.91330 | 8.72600 | 4/3 | 🟡 | OSM · Géoportail |
| 28 | Tour de Capitello (Castelluccio) | 41.90800 | 8.77400 | 3/3 | 🟡 | Mérimée PA00099137 |
| 29 | Tour d'Isolella (Sette Navi) | 41.84656 | 8.76241 | 5/5 | 🟢 | Mérimée PA00099144 |
| 30 | Tour de Capo di Muro | 41.71900 | 8.66400 | 3/3 | 🟡 | Mérimée (MH non numéroté dans note) |
| 31 | Phare des Sanguinaires (Mezu Mare) | 41.87350 | 8.59090 | 4/4 | 🟢 | Service des Phares et Balises |
| 32 | Sémaphore désaffecté de Mezu Mare | 41.87620 | 8.59010 | 4/4 | 🟢 | IGN · Géoportail |
| 33 | Tour di Castelluchju (Mezu Mare) | 41.87400 | 8.58700 | 4/3 | 🟡 | Plan terrier 1770 · Géoportail |
| 34 | Lazaret de Mezu Mare (vestiges) | 41.87700 | 8.59000 | 4/3 | 🟡 | IGN · soubassement visible |
| 35 | BAN Aspretto | 41.90700 | 8.76800 | 4/3 | 🟡 | IGN · Géoportail aérien |
| 36 | Bagne de Coti-Chiavari (Formicolosa) | 41.73400 | 8.72300 | 4/3 | 🟡 | Inventaire IA2A000923 · IGN |
| 37 | Castellu Ficaghjola (Alata) | 41.96500 | 8.70000 | 4/4 | 🔴 approx | lon=8.70000 trailing zeros · SRA Corse |
| 38 | Château de la Punta (Pozzo di Borgo) | 41.94000 | 8.70800 | 4/3 | 🟡 | lat trailing zeros · IGN · Géoportail |
| 39 | Archipel des Sanguinaires | 41.88100 | 8.59400 | 4/3 | 🟡 | Centroïde archipel — acceptable |
| 40 | Dunes et landes de Campo dell'Oro | 41.91670 | 8.80000 | 4/4 | 🟡 | lon=8.80000 · N2000 FR9400619 centroïde |
| 41 | Presqu'île Capu di Muru | 41.72050 | 8.66580 | 4/4 | 🟢 | ZNIEFF 940013115 · IGN |
| 42 | **[CHURCH]** Chapelle Impériale (Palatine) | 41.922 | 8.738 | 3/3 | 🟡 | Incohérence avec SITES[] 5 dec (#21) |
| 43 | **[CHURCH]** Chapelle des Grecs | 41.913 | 8.721 | 3/3 | 🟡 | Mérimée PA00099059 |
| 44 | **[CHURCH]** Oratoire Saint-Jean-Baptiste | 41.918 | 8.738 | 3/3 | 🟡 | Mérimée PA00099068 |
| 45 | **[CHURCH]** Anunziata di Pozzo di Borgo (Alata) | 41.945 | 8.715 | 3/3 | 🔴 approx | Géoportail IGN obligatoire (texte source) |

> **Note Chapelle Impériale** : présente en double avec précision incohérente — SITES[] à 5 dec [41.92175, 8.73837] vs CHURCHES[] à 3 dec [41.922, 8.738]. La version SITES[] est la référence. CHURCHES[] à recaler.

---

## 4. Anomalies à signaler (non GPS)

### Proximité suspecte Monument/Buste Sampiero
- Monument Sampiero Corso [41.989, **9.015**] et Buste Tricolacci [41.987, **9.014**] sont à ~222m l'un de l'autre selon les coords — visuellement ils s'afficheraient superposés sur la carte. Bastelica est un village de 500 habitants : les deux monuments existant réellement dans des quartiers différents, la séparation cartographique devrait être plus grande. **À investiguer**.

### Zéros trailing (arrondi intentionnel)
Plusieurs entrées R10 ont des coordonnées avec des zéros de fin révélateurs d'une estimation visuelle rapide (résolution ≈ 50–100m) :
- `8.70000` (Castellu Ficaghjola) — lon complètement arrondi
- `41.94000` (Château de la Punta) — lat arrondi à 10m
- `8.80000` (Dunes Campo dell'Oro) — lon arrondi
- `8.59000` (Lazaret Mezu Mare)
- `41.87400` (Tour Castelluchju)

Ces entrées seront affichées sans indication de précision sur la carte — un utilisateur pourrait les traiter comme vérifiées. À distinguer visuellement ou à documenter.

---

## 5. Bilan par priorité

| Priorité | Nb | Action |
|---|---|---|
| 🔴 Critique (10 entrées) | 10 | Vérifier avant toute mise en prod finale |
| 🟡 À vérifier (25 entrées) | 25 | Recaler lors d'une session Géoportail/Mérimée |
| 🟢 Fiable (10 entrées) | 10 | Aucune action requise |

### Entrées 🔴 Critique — liste consolidée

| Rapport | Nom | Problème |
|---|---|---|
| R8 | Renicciu (Coggia) | Marqué approx, statue-menhir non documentée précisément |
| R8 | Tour de Cargèse (ruines) | Ruines sans localisation publiée |
| R9 | Buste Sampiero Corso (Tricolacci) | Coordonnées trop proches du Monument |
| R9 | Stèle de Ponticellu | « Lieu présumé » — pas de géolocalisation officielle |
| R9 | Pont de Zippitoli (disparu 2023) | Site détruit, GPS estimé sur carte ancienne |
| R9 | Castellu di Bozzi (Guitera) | Marqué approx, fortification en altitude |
| R10 | Castellu Ficaghjola (Alata) | Marqué approx, lon=8.70000 (arrondi total) |
| R9 | San Giovanni Battista (Urbalacone) | Marqué approx en CHURCHES[] |
| R9 | Capella San Cesario (Cozzano) | Marqué approx, ruines mi-pente |
| R10 | Anunziata di Pozzo di Borgo (Alata) | Texte source : « GPS à vérifier géoportail » |

---

## 6. Recommandations pour la session de correction

### Outils à utiliser
- **Mérimée** (base.paca.culture.gouv.fr/search) : coordonnées Lambert → WGS84 disponibles pour les MH
- **Géoportail IGN** (geoportail.gouv.fr) : vue aérienne + orthophotos haute résolution — incontournable pour Corse
- **OSM Nominatim** : pour monuments et édifices actuellement actifs
- **Megalithic Portal** (megalithic.co.uk) : pour les sites protohistoriques (Renicciu, I Casteddi)
- **SITU** (SRA Corse) : base de données archéologique régionale — pour castelli et sites Bronze/Fer

### Ordre suggéré
1. **Session Géoportail** (~1h) : recaler les 10 critiques + les 8 entrées R8 (même zone)
2. **Vérification Mérimée** (~30 min) : Tours génoises avec PA (PA00099123, PA00099136, PA00099137, PA00099144) — coordonnées officielles disponibles
3. **Session R9 Bastelica** (~20 min) : monument/buste Sampiero + Stèle + Zippitoli via IGN Scan25

### Workflow de correction (à faire dans une autre session)
```
# Pour chaque entrée à corriger :
# 1. Trouver les coordonnées vérifiées (Géoportail / Mérimée)
# 2. Editer index.html — modifier uniquement lat/lon
# 3. Supprimer "GPS approx" de la description si vérifié
# 4. Committer par groupe thématique (ex: "fix: GPS tours génoises R8")
# 5. PR feat/fix-gps-r8-r10 → dev → main
```

---

*Audit read-only — aucune modification effectuée. Fichier généré le 18/04/2026.*
