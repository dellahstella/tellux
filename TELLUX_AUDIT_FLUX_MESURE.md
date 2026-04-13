# TELLUX — Audit du flux de mesure

**Date :** 9 avril 2026
**Version analysée :** tellux_v6_design.html (v5.9, ~6500 lignes)
**Objectif :** Cartographier le flux complet de saisie d'une mesure terrain, identifier les failles, proposer des améliorations.

---

## 1. Cartographie du flux actuel

### 1.1 Parcours utilisateur (séquence des actions)

```
[1] Clic FAB (+)
    └─► startContribFromFAB() (ligne ~6059)
        ├─ Si formulaire ouvert → fermer, retirer marqueur, fin
        └─ Sinon :
            ├─ Activer couche contributions si inactive (tog('con',...))
            ├─ Afficher formulaire (#cform)
            ├─ info() : "Cliquez sur la carte pour placer votre mesure"
            └─ map.once('click') → placer marqueur violet

[2] Clic sur la carte
    └─► Marqueur violet (#5c3a9b) positionné
        └─ info() : "Position : lat, lon — remplissez le formulaire"

[3] Remplissage du formulaire (5 étapes)
    ├─ Étape 1 : Contexte lieu (extérieur/intérieur) → setCtx()
    ├─ Étape 2 : Instrument de mesure → onInstrumentChange()
    │   └─ 10 types : 3 smartphone, 4 capteurs externes, 1 ANFR, 2 observation
    ├─ Étape 3 : Valeur mesurée + unité
    │   └─ Validation : INSTRUMENT_CONSTRAINTS (plage min/max par type)
    ├─ Étape 4 : Contexte intérieur (si intérieur)
    │   ├─ Étage (select)
    │   ├─ Matériaux murs (17 checkboxes avec tooltips µr/σ/dB)
    │   └─ Appareils actifs (6 checkboxes)
    └─ Étape 5 : Note libre + RGPD

[4] Clic "Enregistrer"
    └─► saveContrib() (ligne ~2740)
        ├─ Validation RGPD → sinon erreur
        ├─ Validation instrument → validateContrib()
        ├─ Validation marqueur → sinon erreur
        ├─ Calcul enrichissement :
        │   ├─ fetchIGRF(lat,lon) → valeur IGRF-14
        │   ├─ calcAll(lat,lon) → human, water, geo, score
        │   ├─ calcNets(lat,lon) → réseaux géobiologiques
        │   └─ Calcul atténuation RF depuis matériaux (MAT_DB)
        ├─ Construction objet row (26 champs)
        ├─ Filtrage champs null (protection PGRST204)
        ├─ sbPost('/rest/v1/contributions',[row])
        └─ Succès : ajout marker, refresh liste, info succès

[5] Affichage résultat
    └─ Panneau contrib (#contrib-panel) avec liste des 10 dernières
```

### 1.2 Points d'entrée

| Point d'entrée | Élément | Fonction | État |
|---|---|---|---|
| FAB (+) | `#fab-mesure` (bouton flottant bas-droite) | `startContribFromFAB()` | ✅ Corrigé (session du 9 avril) |
| Bouton sidebar | `#b-con` (couche Contributions) | `tog('con',...)` + `startContrib()` | ⚠ Deux chemins distincts |
| Direct | Aucun bouton dédié | `startContrib()` | Appelé par les deux ci-dessus |

### 1.3 Fonctions impliquées (par ordre d'appel)

| Fonction | Ligne | Rôle | Dépendances |
|---|---|---|---|
| `startContribFromFAB()` | ~6059 | Point d'entrée FAB | tog(), map.once() |
| `startContrib()` | ~2733 | Point d'entrée sidebar | tog(), map.once(), info() |
| `setCtx(ctx,btn)` | ~4449 | Sélection contexte ext/int | Variable globale `ctxContrib` |
| `onInstrumentChange()` | ~1892 | Adaptation formulaire par instrument | `INSTRUMENT_CONSTRAINTS` |
| `validateContrib()` | ~1915 | Validation pré-envoi | `INSTRUMENT_CONSTRAINTS` |
| `saveContrib()` | ~2740 | Calcul + envoi Supabase | fetchIGRF, calcAll, calcNets, sbPost |
| `addMarker(c)` | ~2713 | Ajout marqueur sur carte | lCon (LayerGroup) |
| `renderList()` | ~2821 | Affichage liste contributions | contribsDB |
| `sbPost(path,body)` | ~1795 | POST vers API REST Supabase | SB_URL, sbH() |
| `loadDB()` | ~2715 | Chargement initial contributions | sbGet() |

### 1.4 Variables globales du flux

| Variable | Type | Rôle |
|---|---|---|
| `contribsDB` | Array | Cache local des contributions |
| `pending` | L.marker / null | Marqueur violet temporaire |
| `ctxContrib` | String | Contexte sélectionné ('exterieur'/'interieur') |
| `ACTIVE.con` | Boolean | État de la couche contributions |
| `lCon` | L.LayerGroup | Couche Leaflet des contributions |
| `sessionId` | String | Identifiant unique de session navigateur |

---

## 2. Types de mesure supportés

### 2.1 Instruments définis (INSTRUMENT_CONSTRAINTS)

| ID | Label | Unité | Plage | Accessibilité |
|---|---|---|---|---|
| `smartphone_mag` | Magnétomètre téléphone | nT | 20 000–80 000 | Gratuit (Phyphox, Sensor Kinetics) |
| `smartphone_rssi` | Signal réseau dBm | dBm | -120–0 | Gratuit (Network Cell Info) |
| `smartphone_wifi` | Signal WiFi dBm | dBm | -100–0 | Gratuit (paramètres WiFi) |
| `trifield` | TriField TF2 | nT | 0–200 000 | ~200€ |
| `cornet` | Cornet ED88T/ED85EXS | V/m | 0–100 | ~150–400€ |
| `rtlsdr` | RTL-SDR | description | — | ~30€ |
| `autre_capteur` | Autre capteur EMF | libre | — | Variable |
| `anfr` | Mesure ANFR certifiée | V/m | 0–100 | Institutionnel |
| `observation` | Observation visuelle | description | — | Gratuit |
| `ressenti` | Ressenti subjectif | description | — | Gratuit |

### 2.2 Méthodes smartphone détaillées

| Application | Mesure | Unité | Protocole recommandé | Fiabilité |
|---|---|---|---|---|
| **Phyphox** | Champ magnétique 3 axes | µT/nT | Calibrer → Poser téléphone immobile 30s → Lire moyenne | ⚠ ±5% (capteur Hall intégré) |
| **WiGLE WiFi** | Scan WiFi + cellulaire | dBm + SSID | Scanner pendant 2–5 min en marchant → Exporter CSV | ✅ Données réseau fiables |
| **Network Cell Info** | Signal cellulaire détaillé | dBm + CID + PCI | Lire signal immédiat + historique | ✅ Fiable pour couverture |
| **Sensors Multitool** | Magnétomètre + luxmètre + baro | µT | Calibrer → Lecture immédiate | ⚠ Identique Phyphox |
| **ElectroSmart** | Analyse exposition RF | Score + µW/m² | Scan automatique WiFi + cellulaire | ⚠ Score propriétaire |

### 2.3 Méthodes non-smartphone

| Instrument | Mesure | Protocole | Coût |
|---|---|---|---|
| **TriField TF2** | ELF 50Hz (µT) + RF (mW/m²) + magnétique AC | Mode magnéto → lecture stable 10s → noter | ~200€ |
| **Cornet ED88T** | RF 100MHz–8GHz + ELF 50Hz | Sélecteur RF → lecture crête + moyenne | ~150€ |
| **RTL-SDR + SDR#** | Spectre RF 100kHz–1.7GHz | Scan bande → identifier pics → capturer waterfall | ~30€ + logiciel |
| **Sonde ANFR** | Champ E (V/m) certifié | Protocole normalisé EN 62232 | Institutionnel |

---

## 3. Architecture de réception des données

### 3.1 Schéma base Supabase (table `contributions`)

**Colonnes existantes (après migration 001) :**

| Colonne | Type | Source | Obligatoire |
|---|---|---|---|
| `id` | UUID | auto | oui |
| `created_at` | timestamptz | auto | oui |
| `lat`, `lon` | float8 | clic carte | oui |
| `type` | text | select instrument | oui |
| `valeur` | float8 | saisie utilisateur | non |
| `unite` | text | select unité | non (défaut: 'nT') |
| `note` | text | saisie libre | non |
| `kp`, `bz` | float8 | API espace (NOAA) | non |
| `densite_protons`, `flux_protons` | float8 | API espace (NOAA) | non |
| `igrf_nt` | float8 | calcul IGRF-14 local | non |
| `perturbation_humaine_nt` | float8 | calcHuman() | non |
| `facteur_eau_nt` | float8 | calcAll() | non |
| `reseaux_actifs` | text[] | calcNets() | non |
| `score_anomalie` | int4 | calcul composite | non |
| `delta_nt` | float8 | valeur - prédit | non |
| `session_id` | text | sessionStorage | non |
| `version_app` | text | constante '2.4' | non |
| `contexte` | text | bouton ext/int | non (nouveau) |
| `etage` | text | select étage | non (nouveau) |
| `geo_nets` | text[] | calcNets() | non (nouveau) |
| `geo_netval` | float8 | calcNets() score | non (nouveau) |
| `materiaux_murs` | text[] | checkboxes matériaux | non (nouveau) |
| `appareils_actifs` | text[] | checkboxes appareils | non (nouveau) |
| `attenuation_prevue_db` | float8 | calcul MAT_DB | non (nouveau) |

### 3.2 Enrichissement automatique (côté client)

Chaque mesure est enrichie avant envoi avec des données calculées localement :

1. **IGRF-14** : valeur théorique du champ magnétique au point mesuré (fetchIGRF)
2. **Perturbation humaine** : estimation Biot-Savart depuis les sources HTA/HTB/antennes (calcHuman)
3. **Facteur eau** : estimation piézo-électrique depuis la géologie (calcAll → water)
4. **Score piézo** : calcHeritagePiezo si site patrimonial proche
5. **Réseaux géobiologiques** : Hartmann, Curry, Peyré calculés au point (calcNets)
6. **Atténuation RF** : somme des dB par matériau coché (MAT_DB)
7. **Delta** : écart entre valeur mesurée et valeur prédite (IGRF + human + water + nets)
8. **Données spatiales** : Kp, Bz, densité protons, flux protons (si disponibles via API NOAA)

### 3.3 Flux de données post-sauvegarde

```
Contribution sauvée dans Supabase
    ├─ Ajoutée au cache local (contribsDB.unshift)
    ├─ Marqueur ajouté sur la carte (addMarker)
    ├─ Liste des contributions mise à jour (renderList, 10 dernières)
    └─ Compteur mis à jour (#db-total)

Au prochain chargement de page :
    └─ loadDB() charge les 100 dernières contributions
        └─ Affiche marqueurs + liste
```

---

## 4. Failles identifiées

### 4.1 Bugs corrigés (session du 9 avril 2026)

| ID | Bug | Cause | Correction |
|---|---|---|---|
| A1.1 | PGRST204 sur saveContrib | 7 colonnes manquantes dans Supabase | Migration SQL 001 appliquée |
| A1.2 | Crash si colonne future manquante | Champs null envoyés à Supabase | Filtrage `Object.keys(row).forEach(k=>{if(row[k]===null)delete row[k]})` |
| A2 | FAB double-clic toggle layer | startContribFromFAB appelait startContrib qui re-toggle | Découplage : FAB gère directement le formulaire + map.once |
| A3 | Messages d'erreur non stylés | info() n'avait qu'un seul style | Ajout paramètre `type` (error/success/warn) avec couleurs DA v2 |

### 4.2 Failles restantes (non bloquantes)

| ID | Faille | Impact | Priorité |
|---|---|---|---|
| F-1 | Pas de sauvegarde brouillon (localStorage) | Perte des données si fermeture accidentelle | 🟡 Moyen |
| F-2 | Pas de photo/pièce jointe | Impossible de documenter visuellement une mesure | 🟡 Moyen |
| F-3 | Pas de progression visuelle (stepper) | Utilisateur ne sait pas où il en est dans le formulaire | 🟡 Moyen |
| F-4 | Marqueur violet non annulable | Pas de bouton "Repositionner" ou "Annuler le point" | 🟠 Important (A-5 roadmap) |
| F-5 | Formulaire non responsive sur mobile | Matériaux checkboxes débordent sur petit écran | 🟠 Important |
| F-6 | Pas de validation en temps réel | Erreur visible uniquement au clic "Enregistrer" | 🟡 Moyen |
| F-7 | `version_app` en dur ('2.4') | Ne suit pas la version réelle du fichier HTML | 🟢 Faible |
| F-8 | Deux chemins d'entrée divergents | sidebar vs FAB ont des comportements légèrement différents | 🟡 Moyen |
| F-9 | Pas de mode hors-ligne | Si Supabase down, mesure perdue | 🟠 Important |
| F-10 | Données spatiales (Kp, Bz) parfois indisponibles | Champs null si API NOAA inaccessible | 🟢 Faible (acceptable) |

### 4.3 Risques de sécurité/intégrité

| Risque | Description | Mitigation actuelle | Recommandation |
|---|---|---|---|
| Injection SQL | Données utilisateur passent par l'API REST Supabase | PostgREST sanitise automatiquement | OK — pas d'action |
| Fausses mesures | Rien n'empêche de saisir des valeurs aberrantes | `validateContrib()` vérifie les plages | Ajouter un flag "hors plage" plutôt que bloquer |
| Spam | Pas de rate limiting côté client | RLS Supabase en place | Ajouter un délai minimum entre deux soumissions |
| Géolocalisation fausse | Utilisateur peut placer le marqueur n'importe où | Aucune | Ajouter option "utiliser ma position GPS" |

---

## 5. Recommandations

### 5.1 Court terme (cette session)

1. **Mission C** : Refonte visuelle du formulaire selon DA v2 (typographie, couleurs, stepper)
2. **Mission D** : Intégration FAB avec mode prescription (méthodes de mesure recommandées)
3. **Mission E** : Scénarios de test de bout en bout

### 5.2 Moyen terme (prochaines sessions)

1. **F-4** : Bouton "Repositionner le point" dans le formulaire
2. **F-9** : File d'attente offline (localStorage → sync quand réseau revient)
3. **F-2** : Upload photo via Supabase Storage (bucket dédié, max 2 Mo)
4. **F-5** : Formulaire en bottom-sheet mobile (glissant depuis le bas)

### 5.3 Long terme (montée en gamme)

1. Formulaire multi-étapes avec progression visuelle
2. Historique des mesures par session avec export CSV
3. Comparaison mesure terrain vs modèle IGRF (graphique delta)
4. Badge de fiabilité par contributeur (nombre de mesures, cohérence)

---

*Audit réalisé le 9 avril 2026 sur tellux_v6_design.html v5.9.*
