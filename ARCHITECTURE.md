# Architecture Tellux

**Version :** 1.0 — création 2026-04-21, mise à jour in-place 2026-04-23 (pas de bump)
**Usage :** référence technique pour les sessions Claude Code. Lire avant toute modification de `app.html`.

---

## 1. Structure des fichiers

```
tellux/
├── app.html                    # Application principale — Cartographie EM (PUBLIQUE)
├── mairies.html                # Outils communaux (fiche commune, modèles de courriers)
├── index.html                  # Landing page (dirige vers app.html uniquement)
├── cadre-scientifique.html     # Démarche scientifique (registre éditorial public)
├── methode-et-limites.html     # Méthode et limites (registre éditorial public)
├── guide-utilisation.html      # Guide d'utilisation (registre éditorial public)
├── public/
│   └── data/                   # Jeux de données statiques JSON
│       ├── radon_communes_level3_corse.json
│       ├── tdf_emitters_corse.json
│       ├── wmm_2025_grid_corse.json
│       ├── postes_sources_corse.json
│       ├── eoliennes_corse.json
│       ├── points_chauds_radio_corse.json        # Label UI : « Sites U/Th à mesurer »
│       ├── sites_remarquables_corse.json         # [DEPRECATED depuis Brief 29 — non fetché par app.html, gardé pour archive]
│       └── cartoradio_certified_corse.json       # 30 mesures RF certifiées ANFR/EXEM
├── docs/
│   ├── data/                  # Single source of truth runtime (Brief 28/29)
│   │   ├── sites_corse.json              # 479 sites canoniques consolidés (191 P1 + 288 P2)
│   │   ├── doyennes_polygons.json        # 10 doyennés contemporains (Strat A)
│   │   └── pieves_polygons.json          # 47 pieves Casta v2
│   ├── data-sources/           # Notes de méthodologie par source de données
│   │   ├── radon_communes_level3_corse_notes.md
│   │   ├── tdf_emitters_corse_notes.md
│   │   ├── wmm_2025_notes.md
│   │   ├── postes_sources_corse_notes.md
│   │   ├── eoliennes_corse_notes.md
│   │   ├── bd_foret_v2_corse_notes.md
│   │   ├── points_chauds_radio_corse_notes.md
│   │   ├── sites_geophysiques_remarquables_corse_notes.md
│   │   ├── sites_corse_consolidation_notes.md         # Audit Cowork pipeline 4 sources -> 479 sites
│   │   ├── sites_corse_deduplication_log.json        # Mapping alias -> canonique
│   │   └── cartoradio_certified_corse_notes.md
│   ├── internal/               # Documentation technique interne (gitignored)
│   ├── physicien/              # Documents de soumission à relecture méthodologique
│   ├── lettres/                # Lettres institutionnelles (ASNR, EDF, RTE, BRGM, IRSN)
│   ├── notes-tri/              # Notes de tri éditoriales
│   └── ...
├── _corpus/                    # Corpus scientifique interne — gitignored
├── _migrations/                # Migrations SQL Supabase versionnées
├── analysis/                   # Analyses de corrélation (scripts R/Python)
├── tests/                      # Tests non-régression JS (node --check)
└── wrangler.jsonc              # Config Cloudflare Workers
```

---

## 2. app.html — Structure générale

`app.html` est un fichier HTML monolithique (~4 500 lignes au 2026-04-21) sans bundler, sans framework JS, sans npm. Dépendances chargées via CDN dans l'ordre :

1. Leaflet 1.9.x (carte + couches)
2. Turf.js (calculs géométriques)
3. Papa Parse (CSV)

### 2.1 Palette et typographie (GELÉES — DA v2)

```javascript
const PALETTE = {
  ARDOISE:  '#1F2329',
  PIERRE:   '#F5F0E7',
  MAQUIS:   '#3F5B3A',
  OCRE:     '#C28533',
  PORPHYRE: '#8E2F1F',
  TYRR:     '#1F3A5F'
};
// Typographie : Fraunces (titres), IBM Plex Sans (corps)
```

Ne pas modifier la palette ni la typographie sans décision projet explicite.

### 2.2 Fonctions de calcul — couche physique

Toutes les fonctions `calc*` retournent un objet standardisé :
`{ value, unit, confidence, source, timestamp, epistemic_note, under_review }`

| Fonction | Domaine | Notes |
|----------|---------|-------|
| `calcMagneticStatic(lat, lon)` | Magnétique statique | IGRF + anomalies crustales EMAG2v3 / WDMAM |
| `calcMagneticELF(lat, lon)` | ELF (basse fréquence) | Lignes HT, transformateurs, réseau BT |
| `calcRF(lat, lon)` | Radiofréquences | Antennes ANFR + 10 émetteurs TDF (isotrope PAR/4πd²) |
| `calcGammaAmbient(lat, lon, altitude_m)` | Ionisant | Fond cosmique altimétrique (IGN RGE Alti) + radon |
| `calcRadonPotential(lat, lon, options)` | Radon | Géologie + classification officielle commune (décret 2018-434) |
| `calcHeritageDensity(lat, lon)` | Patrimoine | Densité mégalithes + églises dans rayon 5 km |
| `calcAll_v2(lat, lon, options)` | **Orchestrateur** | Agrège tous les domaines, passe `commune_info` et `altitude_m` |

`options` dans `calcAll_v2` : `{ commune_info, altitude_m }` — tous deux optionnels pour rétrocompatibilité.

### 2.3 Fonctions auxiliaires asynchrones

| Fonction | Source externe | Cache | Pattern |
|----------|---------------|-------|---------|
| `reverseGeocodeCommune(lat, lon)` | api-adresse.data.gouv.fr | `COMMUNE_CACHE` (clé `lat4,lon4`) | fetch + AbortSignal.timeout(5000) |
| `fetchAltitudeIGN(lat, lon)` | data.geopf.fr RGE Alti | `ALTITUDE_CACHE` (clé `lat4,lon4`) | fetch + AbortSignal.timeout(5000) |
| `loadTDFEmitters()` | `public/data/tdf_emitters_corse.json` | `_tdfLoadPromise` (singleton) | fetch une seule fois |
| `loadRadonCommunesL3()` | `public/data/radon_communes_level3_corse.json` | `_radonLoadPromise` (singleton) | fetch une seule fois |

Toutes les fonctions réseau utilisent `try/catch` avec `console.warn` en cas d'échec. Elles retournent `null` sans lever d'exception — les appelants doivent traiter le cas `null`.

### 2.4 Handler click principal (asynchrone)

```javascript
map.on('click', async e => {
  const { lat, lng } = e.latlng;
  // Requêtes parallèles — ne pas attendre l'une avant l'autre
  const [commune_info, altitude_m] = await Promise.all([
    reverseGeocodeCommune(lat, lng),
    fetchAltitudeIGN(lat, lng)
  ]);
  const result = calcAll_v2(lat, lng, { commune_info, altitude_m });
  // → rendu popup + sparkline + mise à jour UI
});
```

### 2.5 Mode Expertise

Activé par bouton dans la sidebar. Déclenche un modal d'avertissement épistémique à la première activation.

Variables et fonctions clés :
- `EXPERT_WEIGHTS_DEFAULT` — pondérations initiales (GELÉES — GELÉ-001)
- `EXPERT_BOUNDS_DEFAULT` — bornes min/max curseurs (GELÉES — GELÉ-001)
- `computeExpertComposite(lat, lon, weights)` — surcharge de `calcAll_v2` avec pondérations manuelles
- Bandeau permanent rouge « MODE EXPERT ACTIF » visible tant que le mode est actif

**Ne pas modifier les constantes GELÉ-001 sans relecture physicien tiers.**

### 2.6 Couches Leaflet — sidebar accordéons

Trois groupes accordéons dans la sidebar, premier ouvert par défaut :

| Groupe | Couches (id toggle) |
|--------|---------------------|
| Modèle EM | b-hot (magnétique statique), b-con (ELF), b-intl (ionisant) |
| Sources anthropiques | b-ant (antennes), b-res (réseau élec), b-bt (bluetooth), b-prod (production énergie) |
| Contexte naturel | b-geo (géologie), b-hyd (hydrographie), b-cav (cavités), b-therm (thermique), b-emag (mag. embarqué), b-wdmam (WDMAM) |

Chaque couche est dans `LAYERS[id]` / `ACTIVE[id]`. Toggle via `tog(id)`.

### 2.7 Panneau Conditions actuelles

Remplace l'ancien `.pbar`. Trois sections repliables (`data-open="false"` par défaut) :
- Géomagnétique : `kp-v` (indice Kp), `sw-bz`, `sw-d`, `sw-p` (vent solaire)
- Réseau électrique : `res-charge` (charge réseau Corse) + sparkline SVG
- Météo / autre : `meteo-n`, `meteo-s`, `lightning-v`, `lightning-pc`

Sparkline : SVG 180×40 px, `PROFIL_HORAIRE_CORSE` (24 valeurs MW), marqueur rouge sur heure courante.

---

## 3. public/data/ — Jeux de données statiques

**Nomenclature :** `{thème}_{descriptif}_{zone}.json`

| Fichier | Contenu | Source | Chargement |
|---------|---------|--------|-----------|
| `radon_communes_level3_corse.json` | Communes niveau 3 radon (décret 2018-434) | IRSN / documentation BRGM | `loadRadonCommunesL3()` au démarrage |
| `tdf_emitters_corse.json` | 10 émetteurs radiodiffusion (PAR kW estimées) | ANFR observatoire + CSA | `loadTDFEmitters()` premier click |
| `wmm_2025_grid_corse.json` | Grille précalculée WMM 2025 pour cross-check magnétique | NOAA WMM 2025 | Chargement asynchrone |
| `postes_sources_corse.json` | Postes sources HTA/HTB | EDF SEI (enrichissement manuel) | `calcMagneticELF_v2` |
| `eoliennes_corse.json` | Parcs éoliens | Observatoire éolien / ANFR | `calcMagneticELF_v2` |
| `points_chauds_radio_corse.json` | 8 entrées documentaires U/Th (label UI « Sites U/Th à mesurer »), `dose_gamma: null` sur toutes, garde défensive `calcGammaAmbient` | Consolidation Cowork 2026-04-23, note de consolidation interne | `loadPointsChaudsRadio()` premier click |
| `sites_remarquables_corse.json` | **DEPRECATED (Brief 29, 2026-05-06)** — 10 sites géophysiques remarquables en 3 catégories (ophiolite / minier / surveillance radiologique). Données intégralement absorbées dans `docs/data/sites_corse.json` (pipeline `consolidate_sites.py`). Le fichier reste pour archive historique mais n'est plus fetché par `app.html` ni `patrimoine.html`. | Consolidation Cowork 2026-04-23 (archive) | **Plus chargé** — voir `docs/data/sites_corse.json` |
| `cartoradio_certified_corse.json` | 30 mesures RF certifiées ANFR/EXEM (29 conformes, 1 dépassement Monticello 29,05 V/m avec re-inspection conformité) | Extraction Cowork 2026-04-23 depuis 30 PDFs ANFR/EXEM | Couche Mesures EM unifiée, layer `lCert` |

Règles pour les nouveaux fichiers `public/data/` :
- JSON compact (pas de whitespace inutile pour > 100 ko)
- Toujours inclure un champ `_meta` avec `source`, `date_creation`, `version`
- Ne jamais bundler ces fichiers dans `app.html`
- Ajouter une note de méthodologie dans `docs/data-sources/`

### 3.bis docs/data/ — Single source of truth (Brief 28/29, 2026-05-06)

Depuis Brief 28 (`patrimoine.html`) et Brief 29 (`app.html`), Tellux utilise un fichier canonique unique pour tous les sites patrimoniaux/géophysiques de Corse.

| Fichier | Contenu | Source | Chargement |
|---------|---------|--------|-----------|
| `sites_corse.json` | 479 sites canoniques (191 Phase 1 exposée + 288 Phase 2 latente). Schéma uniforme : `slug`, `nom`, `lat/lon`, `categorie`, `axe_corpus`, `phase_publication`, `commune_insee`, `commune_nom`, `pieve_slug`, `diocese_medieval_slug`, `doyenne_contemporain_slug`, `description_em` (10 sites SR héritiers), `gps_source`, `gps_audit`, `sources_originales[]` | Pipeline Cowork `scripts/consolidate_sites.py` (4 sources fusionnées : SITES_PATRIMOINE inline + SITES_REFERENCE.json + churches_corse Supabase + patrimoine_corse Supabase + sites_remarquables_corse.json) | `loadSitesPatrimoine()` (patrimoine.html, filter P1) ; `loadSitesRemarquables()` (app.html, filter `axe_corpus = remarquables_geologiques` + override 6 mines) |
| `doyennes_polygons.json` | 10 doyennés contemporains (Strat A : union polygones communes INSEE) | Pipeline `scripts/build_doyennes_polygons.py` | Fetch async patrimoine.html boot |
| `pieves_polygons.json` | 47 pieves Casta v2 (canonicité médiévale complète Brief 17) | Pipeline `scripts/build_pieves_polygons.py` | Fetch async patrimoine.html boot |

**Note SITES_REFERENCE.json racine** : conservé comme **input historique** du pipeline `consolidate_sites.py` (115 entrées). N'est plus fetché au runtime par aucun fichier HTML. Sera décommissionné quand le pipeline sera réécrit pour ingérer directement Supabase + Cowork drafts (Phase 2).

---

## 4. Backend Supabase

**Schéma public — tables principales :**

| Table | Contenu | RLS |
|-------|---------|-----|
| `contributions` | Mesures et observations terrain (crowdsourcing) | Activée |
| `churches` | 196 églises romanes Moracchini-Mazel (1967-1992) | Lecture publique |
| `megalithic_sites` | 137 sites mégalithiques corpus Cesari & Magdeleine 2013 | Lecture publique |

Pattern d'écriture : `sbPost('/rest/v1/{table}', [row])` — wrapper interne autour de `fetch`.

Credentials : **jamais** dans le code, les commits, ni le chat. Variables d'environnement Cloudflare uniquement.

---

## 5. Hébergement

```
GitHub (dellahstella/tellux) → push main → Cloudflare Workers build
                                           → tellux.pages.dev (production)
```

Branche `dev` → branches éphémères `feat/`, `fix/`, `chore/` → PR → merge `dev` → PR → merge `main`.
Push direct sur `main` interdit (workflow imposé par les instructions internes du projet).

---

## 6. Dettes techniques actives

La liste complète et à jour des dettes techniques est maintenue dans `DETTES_TECHNIQUES.md`. Le tableau ci-dessous reprend les dettes principales à date pour permettre une lecture de référence rapide en session Claude Code, sans se substituer au document canonique.

| ID | Description | Condition de déblocage |
|----|-------------|----------------------|
| GELÉ-001 | `EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, formule NCRP : constantes gelées | Relecture physicien tiers — document de soumission transmis en avril 2026 (cf. `ROADMAP.md` section 7) |
| TÉLÉ-001 | API Téléray ASNR (gamma temps réel) non intégrée | Accès API ASNR (courrier transmis en avril 2026, cf. `ROADMAP.md` section 7) |
| NCRP-001 | Fond naturel terrestre NCRP 94 dans `calcGammaAmbient` gelé | Relecture physicien tiers (lié GELÉ-001) |
| BT-CALIBRATION-001 | Calcul BT segments désactivé (flag `USE_BT_SEGMENTS = false`), proxy `BT_ZONES` legacy actif | Recalibration physique du modèle Biot-Savart BT, session dédiée |
| HTA-TENSION-001 | Dataset `hta_lines` sans champ voltage, courant uniforme 225 A | Migration SQL + enrichissement dataset |
| MIGN-001 | ~6 appelants legacy `calcAll` non migrés vers `calcAll_v2` | Session dédiée (non bloquant) |
| CORPUS-PILIERS-001 (ex H1-H88-ELF-001, reformulée 2026-04-23) | Relecture des fiches du Pilier A (S1-S14) et du Pilier B (P1-P20) post-migration Biot-Savart. La formulation H1-H88 est obsolète depuis la scission du 2026-04-21 ; la correspondance H-numéro → S/P reste consultable dans le corpus interne | Session dédiée post-merge Biot-Savart, par pilier |

---

*Mise à jour suivante prévue à mesure que la phase 1 se stabilise et que les modules d'extension sont, le cas échéant, activés (cf. ROADMAP).*
