# Architecture Tellux

**Version :** 1.0 — 2026-04-21
**Usage :** référence technique pour les sessions Claude Code. Lire avant toute modification de `app.html`.

---

## 1. Structure des fichiers

```
tellux/
├── app.html                    # Application principale — Cartographie EM (PUBLIQUE)
├── patrimoine.html             # Module patrimoine (existe, non lié depuis index, PHASE 2)
├── agronomie.html              # Module agronomie (existe, non lié depuis index, PHASE 3)
├── index.html                  # Landing page (dirige vers app.html uniquement)
├── public/
│   └── data/                   # Jeux de données statiques JSON
│       ├── radon_communes_level3_corse.json
│       └── tdf_emitters_corse.json
├── docs/
│   └── data-sources/           # Notes de méthodologie par source de données
│       ├── radon_communes_level3_corse_notes.md
│       └── tdf_emitters_corse_notes.md
├── _migrations/                # Migrations SQL Supabase versionnées
├── analysis/                   # Analyses de corrélation (scripts R/Python)
├── tests/                      # Tests non-régression JS (node --check)
└── wrangler.jsonc              # Config Cloudflare Workers
```

Les modules `patrimoine.html` et `agronomie.html` existent dans le repo public mais ne sont pas référencés depuis `index.html` ni `app.html`. Accessibles uniquement par URL directe. Ne pas les lier avant leur phase de financement respective.

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

Règles pour les nouveaux fichiers `public/data/` :
- JSON compact (pas de whitespace inutile pour > 100 ko)
- Toujours inclure un champ `_meta` avec `source`, `date_creation`, `version`
- Ne jamais bundler ces fichiers dans `app.html`
- Ajouter une note de méthodologie dans `docs/data-sources/`

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
Push direct sur `main` interdit (voir `PROJECT_INSTRUCTIONS_v2.md` §B.3).

---

## 6. Dettes techniques actives

| ID | Description | Condition de déblocage |
|----|-------------|----------------------|
| GELÉ-001 | `EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, formule NCRP : constantes gelées | Relecture physicien tiers (jalon 2 roadmap) |
| TÉLÉ-001 | API Téléray ASNR (gamma temps réel) non intégrée | Accès API ASNR (courrier envoyé) |
| NCRP-001 | Fond naturel terrestre NCRP 94 dans `calcGammaAmbient` gelé | Relecture physicien tiers (lié GELÉ-001) |
| MIGN-001 | ~6 appelants legacy `calcAll` (sans options) non migrés vers `calcAll_v2` | Session dédiée (non bloquant) |
| PATR-001 | H1/H8/H18/H37/H39 dormantes — `patrimoine.html` non extrait de `app.html` | Phase 2 financement + session extraction |

---

*Mise à jour suivante prévue après extraction `patrimoine.html` / `agronomie.html` (jalon 1 roadmap).*
