#!/usr/bin/env python3
"""
build_sites_app.py — Consolidation M1 sites_app.json
====================================================

═══════════════════════════════════════════════════════════════════════════
⚠️  DEPRECATED 2026-05-13 (M3 cleanup) ⚠️

Ce script est OBSOLÈTE et ne doit PAS être ré-exécuté :

1. Les 3 sources de données qu'il consomme ont été supprimées du repo en M3 :
   - `docs/data/sites_em.json` (48 sites EM)
   - `public/data/points_chauds_radio_corse.json` (8 sites U/Th)
   - L'array `THERMAL_SOURCES_CORSE` hardcodé dans `app.html` (transformé en
     `let []` populé par `loadSitesApp()` en M2).

2. `public/data/sites_app.json` est désormais la SOURCE CANON runtime,
   éditée directement (manuellement ou via `scripts/sync_cross_app.py` pour
   les sync cross-app depuis `sites_patrimoine.json`).

Le script est conservé pour traçabilité historique de la migration M1 : il
documente le mapping (sources → cible) et les corrections GPS Phase 1.
Cf. `docs/internal/AUDIT_GPS_M1_2026-05-13.md` pour le rapport détaillé.

Pour modifier sites_app.json :
  - Édition manuelle directe du JSON (champs simples comme description).
  - `scripts/sync_cross_app.py --apply` pour propager les coords depuis
    patrimoine canonical vers les entrées type=site_em.

═══════════════════════════════════════════════════════════════════════════

Lit 3 sources actuelles éparpillées et émet `public/data/sites_app.json` :
  1. `docs/data/sites_em.json` (48 sites EM remarquables, hydrauliques, miniers historiques)
  2. `public/data/points_chauds_radio_corse.json` (8 sites U/Th)
  3. `THERMAL_SOURCES_CORSE` (6 sources thermales, array JS hardcodé dans app.html)

Applique :
  - Les corrections GPS du Phase 1 audit M1 (cf. `docs/internal/AUDIT_GPS_M1_2026-05-13.md`)
  - La réconciliation app/patrimoine Phase 3 (cas A/B/C/D documenté)

Sortie : `public/data/sites_app.json` au schéma défini § 4 de
`docs/internal/AUDIT_COORDS_APP_2026-05-13.md`.

Idempotent : relancer le script produit le même résultat (modulo ordre stable).

Usage :
    cd <repo root>
    python3 tools/build_sites_app.py
"""

from __future__ import annotations

import json
import math
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# Chemins
# ──────────────────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_SITES_EM = REPO_ROOT / 'docs' / 'data' / 'sites_em.json'
SRC_POINTS_CHAUDS = REPO_ROOT / 'public' / 'data' / 'points_chauds_radio_corse.json'
SRC_APP_HTML = REPO_ROOT / 'app.html'
SRC_PATRIMOINE = REPO_ROOT / 'SITES_REFERENCE.json'

OUT_SITES_APP = REPO_ROOT / 'public' / 'data' / 'sites_app.json'

AUDIT_DATE = '2026-05-13'  # Date du Phase 1 audit GPS M1

# Slugs explicitement SUPPRIMÉS de la sortie M1 (cf. décisions Soleil clôture M1)
# Pour les sources thermales, la clé est le nom d'origine dans THERMAL_SOURCES_CORSE.
SUPPRESSED_THERMAL_NAMES = {
    'Lac thermal de Tora',  # Décision Soleil 2026-05-13 résultat B :
                            # toponyme corrigé "Tolla" (typo historique), MAIS aucune
                            # source thermale au Lac de Tolla (réservoir EDF Prunelli,
                            # 550 m alt). Confirmé Wikipedia + visit-corsica + paradisu
                            # + listes officielles sources thermales Corse. Erreur de
                            # saisie historique. Suppression argumentée.
}


# ──────────────────────────────────────────────────────────────────────────────
# Audit GPS overrides (Phase 1 — cf. docs/internal/AUDIT_GPS_M1_2026-05-13.md)
# ──────────────────────────────────────────────────────────────────────────────

# Pour chaque slug/id, override des champs gps. Si absent, conserver la source.
# Le rationale est documenté dans le rapport d'audit.
AUDIT_OVERRIDES = {
    # --- sites_em sans gps_audit (Phase 1 §3.1) ---
    'barrage_tolla': {
        'lat': 41.9635, 'lon': 8.9646,
        'gps_source': 'CFBR (barrages-cfbr.eu/Tolla) + annuaire-mairie.fr',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'exacte',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Ouvrage hydraulique connu.',
    },
    'cirque_de_bonifato': {
        'lat': 42.4424, 'lon': 8.8546,
        'gps_source': 'Wikipedia Forêt de Bonifatu + gps-viewer.com (parking D251)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord d origine arrondie au centième. Parking d entrée Bonifatu à 538 m altitude, point représentatif accessible.',
    },
    'desert_des_agriate': {
        'lat': 42.68, 'lon': 9.13,
        'gps_source': 'Wikipedia Désert des Agriates + GuideVoyageur.fr',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Centroïde indicatif zone protégée 15 000 ha Conservatoire du Littoral.',
    },
    'foret_de_tartagine': {
        'lat': 42.528, 'lon': 8.997,
        'gps_source': 'Wikipedia Forêt de Tartagine-Melaja (Maison forestière D639, alt 705 m)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Maison forestière de Tartagine = point de référence accès. Massif 2783 ha communes Olmi-Cappella et Mausoléo.',
    },
    'golfe_de_porto_vecchio': {
        'lat': 41.59, 'lon': 9.30,
        'gps_source': 'mappy.com + cartesfrance.fr (commune Porto-Vecchio + ouverture est du golfe)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Centroïde baie ouverte, ~10 km du nord Cala Rossa au sud Chiappa.',
    },
    'massif_de_l_ospedale': {
        'gps_source': 'Wikipedia L Ospedale + alta-rocca-tourisme.com (lieu-dit forêt + col d Illarata 850 m alt)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Lieu-dit L Ospedale confirmé à 20 km NO Porto-Vecchio. Sommet Punta di a Vacca Morta 1314 m à ~3 km sud.',
    },
    'plateau_du_coscione': {
        'gps_source': 'Wikipedia Plateau du Cuscionu + Petit Futé + visit-corsica.com',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Haut plateau granitique 1500-1700 m, 4 communes Zicavo/Aullène/Serra-di-Scopamène/Quenza.',
    },
    # --- Cas signalés Soleil (Phase 1 §3.4) ---
    'ophi_farinole': {
        'lat': 42.7396, 'lon': 9.3602,
        'gps_source': 'mineraux-de-corse.over-blog.com (relevé GPS) + IGN Top 25 4347OT lieu-dit Ferlaggio',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'ponctuel',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord historique Lacroix 1893 imprécise (42.828/9.289). Vestiges miniers réels au lieu-dit Ferlaggio (versant Olmeta di Capu Corsu). Galeries XIXe + galerie génoise 1557.',
        'gps_locked': True,
        'gps_lock_reason': 'M1 Phase 1 — correction GPS Farinole (Soleil signalé site mal placé)',
    },
    'surv_bonifacio': {
        'lat': 41.30, 'lon': 9.30,
        'gps_source': 'IRSN (irsn.fr) + Parc Marin International Bouches de Bonifacio',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'zone_marine_etendue',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Option A retenue : centroïde détroit (Bouches de Bonifacio 80 000 ha PMI). Coord d origine 41.36/9.16 = port terrestre, incohérent avec mécanisme marin Th-234 dans algues. Zone IRSN Th-234 nord La Maddalena à ~41.27/9.40 (Italie).',
        'gps_locked': True,
        'gps_lock_reason': 'M1 Phase 1 — correction GPS Bouches de Bonifacio (Soleil signalé site mal placé)',
    },
}

# Overrides U/Th (Phase 1 §3.2)
UTH_OVERRIDES = {
    'SALECCIA': {
        'lat': 42.721, 'lon': 9.202,
        'gps_source': 'Wikipedia Plage de Saleccia + corsicalovers.fr (commune Santo-Pietro-di-Tenda)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord déjà vérifiée Cowork 2026-04-24. Confirmation.',
    },
    'LOTU': {
        'lat': 42.71966, 'lon': 9.2336,
        'gps_source': 'Wikipedia Plage du Lotu + bord-de-mer.com (42°43 10.36N / 9°14 0.07E)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'exacte',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord d origine confirmée à 5m près. Plage 400 m communes Santo-Pietro-di-Tenda et Saint-Florent.',
    },
    'OSTRICONI': {
        'lat': 42.682, 'lon': 9.060,
        'gps_source': 'plages.tv (commune Palasca) + bouger-voyager.com (anse de Peraiola)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord après = embouchure principale Ostriconi (anse de Peraiola, Palasca). Plage 600 m.',
    },
    'PORTO_FANGO': {
        'lat': 42.36, 'lon': 8.65,
        'gps_source': 'Wikipedia Fango (river) + AllTrails Galéria-Fango-Mouth + Conservatoire du Littoral Embouchure du Fangu',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Embouchure Fango (commune Galéria) à ~7 km au SUD de la coord d origine. Coord après = delta Fango proprement dit.',
    },
    'VALINCO_SABLES': {
        'lat': 41.68, 'lon': 8.93,
        'gps_source': 'Wikipedia Rizzanese + paradisu.info (Capu Lauroso entre Rizzanese et Propriano)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'communal',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Centroïde 2 embouchures distantes ~5 km (Rizzanese Capu Lauroso et Baracci Propriano).',
    },
    'CORTENAIS_VENACO': {
        'gps_source': 'BRGM (1979). Les minéralisations intragranitiques de la Corse. Rapport 79-RDM-070-FE.',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'communal',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord communal conservée — coords BRGM non publiques pour les indices d autunite/torbernite. Audit InfoTerre dédié possible post-M1.',
    },
    'BALAGNE_GIUSSANI': {
        'gps_source': 'BRGM (1980). Activités minières en Corse. Rapport 80-RDM-003-FE.',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'communal',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord communal conservée — Giussani 4 communes (Olmi-Cappella, Pioggiola, Mausoléo, Vallica). Audit InfoTerre dédié possible post-M1.',
    },
    'VIZZAVONA_GHISONI': {
        'lat': 42.137, 'lon': 9.099,
        'gps_source': 'Wikipedia Monte d Oro + altituderando.com + bivouak.net (sommet 42°08 14N 9°05 55E)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord après = sommet Monte d Oro 2389 m (commune Vivario). Zone leucogranite BRGM RP-50200-FR plus large (massif Monte d Oro/Vizzavona/Ghisoni). Note : slug uth_monte_d_oro vit en parallèle du slug site_em monte_d_oro (sites_em.json) — 2 angles distincts (patrimoine naturel vs zone U/Th BRGM) pour la même montagne, par design.',
        # Décision Soleil clôture M1 (2026-05-13) : slug court + nom Monte d Oro,
        # qualificatif géologique "leucogranites" déplacé en properties.type_specifique.
        'rename_id_to': 'monte_d_oro',
        'rename_nom_to': "Monte d'Oro",
        'type_specifique': 'leucogranite_radioactif_zone_gamma',
    },
}

# Overrides sources thermales (Phase 1 §3.3)
# Clés = nom d origine dans THERMAL_SOURCES_CORSE
THERMAL_OVERRIDES = {
    'Thermes de Baracci': {
        'slug': 'source_thermale_baracci',
        'lat': 41.6890, 'lon': 8.9322,
        'commune_nom': 'Olmeto',
        'commune_insee': '2A188',
        'gps_source': 'Site officiel bainsdebaracci.fr + ViaMichelin',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'exacte',
        'temperature_C': 52,
        'composition': 'sulfuree',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Site officiel rénové 2025. Coord d origine 41.7050/8.8980 ~3.3 km NO du site réel.',
    },
    'Sources de Guitera': {
        'slug': 'source_thermale_guitera',
        'lat': 41.88, 'lon': 9.07,
        'commune_nom': 'Guitera-les-Bains',
        'commune_insee': '2A132',
        'gps_source': 'Communauté de communes Pieve de l Ornano et du Taravo (pieveornano.fr) + corseweb.corsica',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'temperature_C': 45,
        'composition': 'sulfuree',
        'statut': 'fermee_depuis_plusieurs_annees',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord après = centre village Guitera-les-Bains (alt 621 m, CP 20153). Source thermale au bord du Taravo, point d émergence exact non publié.',
    },
    'Caldane (Zévaco)': {
        'slug': 'source_thermale_caldane',
        'lat': 41.69, 'lon': 9.06,
        'commune_nom': 'Sainte-Lucie-de-Tallano',
        'commune_insee': '2A285',
        'gps_source': 'la-corse.travel + location-bonifacio.com (route D148 Sartène → Sainte-Lucie-de-Tallano)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'exacte',
        'temperature_C': 38,
        'composition': 'sulfuree_legere',
        'gps_audit_note': 'Audit Cowork 2026-05-13. ERREUR DE COMMUNE corrigée : Bains de Caldane sont à Sainte-Lucie-de-Tallano (Alta Rocca), CP 20112, et non à Zévaco. Δ 30 km. 3 piscines extérieures, eau 38°C.',
        'rename_nom_to': 'Caldane (Sainte-Lucie-de-Tallano)',
        'gps_locked': True,
        'gps_lock_reason': 'M1 Phase 1 — correction commune Caldane (Sainte-Lucie-de-Tallano, pas Zévaco)',
    },
    # 'Lac thermal de Tora' — SUPPRIMÉ (cf. SUPPRESSED_THERMAL_NAMES).
    # Décision Soleil clôture M1 (2026-05-13) résultat B : toponyme corrigé "Tolla"
    # (typo historique) mais aucune source thermale au Lac de Tolla (réservoir EDF
    # du Prunelli, 550 m alt). Confirmé Wikipedia + visit-corsica + paradisu +
    # listes officielles sources thermales Corse. Erreur de saisie historique.
    'Pietrapola (station thermale)': {
        'slug': 'source_thermale_pietrapola',
        'lat': 41.99049, 'lon': 9.30319,
        'commune_nom': 'Isolaccio-di-Fiumorbo',
        'commune_insee': '2B135',
        'gps_source': 'Wikipedia Isolaccio-di-Fiumorbo + thermes.biz + corseorientale.com',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'exacte',
        'temperature_C': 56,
        'composition': 'sulfuree_sodique_hyperthermale',
        'debit_L_jour': 200000,
        'agrement': 'RH3_rhumatologie',
        'altitude_m': 700,
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord d origine 42.057/9.388 ~10 km NE de l établissement thermal réel. Pietrapola-les-Bains source D de la Rastello 56°C, 7 sources, unique station thermale agréée Corse, propriété CdC, rouverture post-travaux 2023.',
    },
    'Guagno-les-Bains': {
        'slug': 'source_thermale_guagno',
        'lat': 42.169, 'lon': 8.949,
        'commune_nom': 'Poggiolo',
        'commune_insee': '2A210',
        'gps_source': 'mappy + topographic-map.com (42°10 7N 8°56 55E)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'temperature_C': 49,
        'composition': 'sulfuree_sodique',
        'gps_audit_note': 'Audit Cowork 2026-05-13. Coord après = centre village Guagno-les-Bains, lieu-dit commune Poggiolo CP 20125. Source Venturini 49°C + Occhiu 37°C.',
    },
}


# ──────────────────────────────────────────────────────────────────────────────
# Phase 3 — Cas C strict patrimoine audité ET Δ > 500 m
# Décisions Cowork :
#   capu_rossu : déjà recadré sprint app-ui-polish a966511. Conserver em.
#   gorges_de_l_inzecca : 3e coord centroïde 42.10/9.26 (Q2 brief clôture Soleil).
#   gorges_du_spelunca : adopter coord patrimoine — Pont Vecciu IGN 4150 OT (Q2).
#
# Pour Inzecca et Spelunca, override appliqué dans CASE_C_OVERRIDES (post-Phase 3,
# vient écraser le résultat de la réconciliation).
# ──────────────────────────────────────────────────────────────────────────────
CASE_C_DECISIONS = {
    'capu_rossu': 'CONSERVER_EM',
    'gorges_de_l_inzecca': 'OVERRIDE_CENTROID',
    'gorges_du_spelunca': 'ADOPT_PATRIMOINE',
}

# Overrides post-Phase 3 (clôture M1) — coord finale et notes pour les 2 cas Q2.
CASE_C_OVERRIDES = {
    'gorges_de_l_inzecca': {
        'lat': 42.10, 'lon': 9.26,
        'gps_source': 'Cowork 2026-05-13 (centroïde D344 entre Sampolo et Saint-Antoine, kalysteo.com + paradisu.info + petitfute.fr)',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'secteur',
        'gps_audit_note': 'Audit Cowork clôture M1 (2026-05-13). Gorges étendues ~13 km sur D344. Coord app antérieure 42.0978/9.2226 = entrée ouest depuis Ghisoni ; coord patrimoine 42.0962/9.2914 = sortie est vers Lugo-di-Nazza. Coord après = centroïde 42.10/9.26 (3e coord, mi-parcours D344 entre Sampolo et Saint-Antoine).',
    },
    'gorges_du_spelunca': {
        'lat': 42.25368, 'lon': 8.76676,
        'gps_source': 'patrimoine SITES_REFERENCE.json + AllTrails (Pont Vecciu, Ota) + IGN Top 25 4150 OT',
        'gps_audit': AUDIT_DATE,
        'precision_coord': 'ponctuel',
        'gps_audit_note': 'Audit Cowork clôture M1 (2026-05-13). Coord patrimoine adoptée (Pont Vecciu = point de référence reconnu IGN 4150 OT, à 300 m du point AllTrails 42.25640/8.76147). Coord app antérieure 42.247/8.732 ~3 km à l ouest, hors gorges (vers Porto).',
    },
}


# ──────────────────────────────────────────────────────────────────────────────
# Utilitaires
# ──────────────────────────────────────────────────────────────────────────────

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # m
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def slugify(s):
    """Convertit un nom en slug ASCII [a-z0-9_]."""
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode()
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', '_', s).strip('_')
    return s


# ──────────────────────────────────────────────────────────────────────────────
# Chargement des sources
# ──────────────────────────────────────────────────────────────────────────────

def load_sites_em():
    return json.load(SRC_SITES_EM.open(encoding='utf-8'))['sites']


def load_points_chauds():
    return json.load(SRC_POINTS_CHAUDS.open(encoding='utf-8'))['points_chauds']


def load_patrimoine():
    """Patrimoine = SITES_REFERENCE.json (list of dicts)."""
    return json.load(SRC_PATRIMOINE.open(encoding='utf-8'))


def extract_thermal_from_app_html():
    """Parse THERMAL_SOURCES_CORSE array depuis app.html.

    Cible le bloc `const THERMAL_SOURCES_CORSE = [...];` et extrait les 6 entrées
    `{ lat: ..., lon: ..., nom: "...", description: "..." }`.
    """
    content = SRC_APP_HTML.read_text(encoding='utf-8')
    m = re.search(
        r'const\s+THERMAL_SOURCES_CORSE\s*=\s*\[(.*?)\];',
        content, re.DOTALL
    )
    if not m:
        raise RuntimeError(
            'THERMAL_SOURCES_CORSE block not found in app.html. '
            'Vérifier que app.html L.4536 contient toujours cette constante.'
        )
    block = m.group(1)
    pattern = re.compile(
        r'\{\s*lat:\s*([\-\d.]+),\s*lon:\s*([\-\d.]+),\s*'
        r'nom:\s*"([^"]+)",\s*description:\s*"([^"]+)"\s*\}'
    )
    entries = []
    for mt in pattern.finditer(block):
        entries.append({
            'lat': float(mt.group(1)),
            'lon': float(mt.group(2)),
            'nom': mt.group(3),
            'description': mt.group(4),
        })
    # app.html contient 6 entrées d origine. Si SUPPRESSED_THERMAL_NAMES vide,
    # on doit en avoir 6. Une fois une entrée supprimée, on accepte 6 (source
    # toujours intacte, seul le dataset cible perd l entrée).
    if len(entries) != 6:
        raise RuntimeError(
            f'THERMAL_SOURCES_CORSE extraction depuis app.html : attendu 6 entrées '
            f'(source intacte, suppression appliquée côté pipeline), '
            f'trouvé {len(entries)}'
        )
    return entries


# ──────────────────────────────────────────────────────────────────────────────
# Construction des entrées sites_app — par type
# ──────────────────────────────────────────────────────────────────────────────

def build_site_em_entries(sites_em_raw, patrimoine):
    """Construit les entrées type=site_em depuis sites_em.json.

    Applique :
      - AUDIT_OVERRIDES (corrections Phase 1)
      - Réconciliation patrimoine (cas A/B/D)
      - Conservation explicite pour cas C strict (décisions Cowork ci-dessus)
    """
    pat_by_name = {p['nom']: p for p in patrimoine}
    out = []
    case_log = []

    for s in sites_em_raw:
        slug = s['slug']
        name = s['name']
        em_lat, em_lon = s['lat'], s['lon']
        em_audit = s.get('gps_audit')

        # Override audit Phase 1 (priorité absolue)
        override = AUDIT_OVERRIDES.get(slug, {})
        lat = override.get('lat', em_lat)
        lon = override.get('lon', em_lon)
        gps_source = override.get('gps_source', s.get('gps_source'))
        gps_audit = override.get('gps_audit', em_audit)
        precision_coord = override.get('precision_coord')
        gps_audit_note = override.get('gps_audit_note')
        gps_locked = override.get('gps_locked', s.get('gps_locked'))
        gps_lock_reason = override.get('gps_lock_reason', s.get('gps_lock_reason'))

        # Lookup patrimoine
        pat = pat_by_name.get(name)
        reconciliation_case = None
        if pat:
            pat_audit = bool(pat.get('gps_audit'))
            d = haversine(lat, lon, pat['lat'], pat['lon'])
            if pat_audit and d < 200:
                # Cas A : reprendre patrimoine
                reconciliation_case = 'A'
                lat, lon = pat['lat'], pat['lon']
                gps_source = pat.get('gps_source') or gps_source
                gps_audit = pat.get('gps_audit') or gps_audit
            elif pat_audit and d < 500:
                # Cas B : reprendre patrimoine + note
                reconciliation_case = 'B'
                old_lat, old_lon = lat, lon
                lat, lon = pat['lat'], pat['lon']
                gps_source = pat.get('gps_source') or gps_source
                gps_audit = pat.get('gps_audit') or gps_audit
                note = f'Cas B Phase 3 : réconcilié depuis patrimoine, écart {d:.0f}m avec coord app antérieure ({old_lat:.5f}, {old_lon:.5f}).'
                gps_audit_note = ((gps_audit_note + ' ') if gps_audit_note else '') + note
            elif d > 500 and pat_audit:
                # Cas C : décision documentée
                reconciliation_case = 'C'
                decision = CASE_C_DECISIONS.get(slug, 'CONSERVER_EM')
                note = f'Cas C Phase 3 (Δ {d:.0f}m, patrimoine audité) — décision {decision}.'
                gps_audit_note = ((gps_audit_note + ' ') if gps_audit_note else '') + note
                # Override post-Phase 3 (clôture M1, Q2 Soleil)
                co = CASE_C_OVERRIDES.get(slug)
                if co:
                    lat = co['lat']
                    lon = co['lon']
                    gps_source = co.get('gps_source', gps_source)
                    gps_audit = co.get('gps_audit', gps_audit)
                    precision_coord = co.get('precision_coord', precision_coord)
                    if co.get('gps_audit_note'):
                        gps_audit_note = (gps_audit_note + ' ' + co['gps_audit_note']).strip()
            else:
                # Cas D : patrimoine sans audit
                reconciliation_case = 'D'
        else:
            reconciliation_case = 'NO_PAT'

        # categorie : reprise depuis adaptSiteRemarquable() de app.html L.6823
        categorie = _map_site_em_categorie(s)

        # precision_coord par défaut
        if not precision_coord:
            de = s.get('description_em', '')
            if isinstance(de, dict):
                precision_coord = de.get('precision_coord', 'secteur')
            else:
                precision_coord = 'secteur'

        # description (flatten cas A vs B)
        description = _flatten_description_em(s)

        # properties typé site_em
        properties = _build_site_em_properties(s)

        entry = {
            'slug': slug,
            'nom': name,
            'lat': lat,
            'lon': lon,
            'type': 'site_em',
            'categorie': categorie,
            'commune_nom': s.get('commune_nom'),
            'commune_insee': s.get('commune_insee'),
            'description': description,
            'gps_source': gps_source,
            'gps_audit': gps_audit,
            'precision_coord': precision_coord,
            'priorite': bool(s.get('priorite', False)),
            'phase_publication': s.get('phase_publication', 1),
            'sources_originales': s.get('sources_originales', []),
        }

        if gps_locked:
            entry['gps_locked'] = True
            entry['gps_lock_reason'] = gps_lock_reason or ''
        if gps_audit_note:
            entry['gps_audit_note'] = gps_audit_note
        if properties:
            entry['properties'] = properties

        # Cross-app (rattachement patrimoine)
        cross_app = {}
        if s.get('doyenne_contemporain_slug'):
            cross_app['doyenne'] = s['doyenne_contemporain_slug']
        if s.get('pieve_slug'):
            cross_app['pieve'] = s['pieve_slug']
        if cross_app:
            entry['cross_app'] = cross_app
        # Marquer origine patrimoine si cas A/B
        if reconciliation_case in ('A', 'B'):
            entry['gps_cross_app_origin'] = 'patrimoine'

        # Notes héritées
        notes = s.get('notes', '')
        if notes:
            entry['notes'] = notes

        out.append(entry)
        case_log.append({
            'slug': slug, 'case': reconciliation_case,
            'd': haversine(em_lat, em_lon, lat, lon),
        })

    return out, case_log


def _map_site_em_categorie(s):
    """Reprend la logique mapSRGranulaire() + cas 2 de adaptSiteRemarquable (app.html L.6857)."""
    slug = s['slug']
    if slug.startswith('ophi_'):
        return 'ophiolite'
    if slug.startswith('min_'):
        return 'minier'
    if slug.startswith('surv_'):
        return 'surveillance_radio'
    axe = s.get('axe_em', '')
    if axe == 'hydrauliques':
        return 'hydraulique'
    return 'geologique'


def _flatten_description_em(s):
    """Si description_em est string, la retourne. Sinon, retourne signature_em (cas A objet)."""
    de = s.get('description_em')
    if isinstance(de, str):
        return de
    if isinstance(de, dict):
        return de.get('signature_em') or s.get('description', '')
    return s.get('description', '')


def _build_site_em_properties(s):
    """Pour les sites SR ophi/min/surv (cas A objet), construit le bloc properties."""
    de = s.get('description_em')
    if not isinstance(de, dict):
        return None
    properties = {}
    if de.get('signature_em'):
        properties['signature_em'] = de['signature_em']
    if de.get('impact_modele'):
        properties['impact_modele'] = de['impact_modele']
    if de.get('historique'):
        properties['historique'] = de['historique']
    if de.get('statut_actuel'):
        properties['statut_actuel'] = de['statut_actuel']
    if de.get('source_principale'):
        properties['source_principale'] = de['source_principale']
    if de.get('type_specifique'):
        properties['type_specifique'] = de['type_specifique']
    return properties or None


def build_site_uth_entries(points_chauds_raw):
    """Construit les entrées type=site_uth depuis points_chauds_radio_corse.json.

    Applique UTH_OVERRIDES (Phase 1 §3.2).
    """
    out = []
    for p in points_chauds_raw:
        pid = p['id']
        override = UTH_OVERRIDES.get(pid, {})
        lat = override.get('lat', p['lat'])
        lon = override.get('lon', p['lon'])
        gps_source = override.get('gps_source', p.get('source'))
        gps_audit = override.get('gps_audit')
        precision_coord = override.get('precision_coord', p.get('precision_coord', 'secteur'))
        gps_audit_note = override.get('gps_audit_note')

        nom = override.get('rename_nom_to', p['nom'])
        new_id = override.get('rename_id_to', pid)
        type_specifique = override.get('type_specifique')

        slug = 'uth_' + slugify(new_id)

        properties = {
            'dose_gamma_estimee_nSv_h': p.get('dose_gamma_estimee_nSv_h'),
            'rayon_influence_m': p.get('rayon_influence_m'),
            'statut_mesure': p.get('statut', 'mesure_requise'),
            'mecanisme_physique': p.get('source'),
        }
        if type_specifique:
            # Décision Soleil clôture M1 : qualificatif géologique en properties
            # (pas dans le nom ni categorie). Ex : Monte d Oro -> leucogranite_*.
            properties['type_specifique'] = type_specifique

        entry = {
            'slug': slug,
            'nom': nom,
            'lat': lat,
            'lon': lon,
            'type': 'site_uth',
            'categorie': p.get('type', 'indice_radiometrique'),
            'commune_nom': p.get('commune'),
            'commune_insee': None,
            'description': p.get('note', '') or p.get('source', ''),
            'gps_source': gps_source,
            'gps_audit': gps_audit,
            'precision_coord': precision_coord,
            'priorite': False,
            'phase_publication': 1,
            'sources_originales': ['points_chauds_radio_corse'],
            'properties': properties,
        }
        if gps_audit_note:
            entry['gps_audit_note'] = gps_audit_note
        if new_id != pid:
            entry.setdefault('notes', '')
            entry['notes'] = (
                f'M1 Phase 1 — ID renommé : {pid} → {new_id}. ' +
                (entry.get('notes') or '')
            ).strip()

        out.append(entry)
    return out


def build_source_thermale_entries(thermal_raw):
    """Construit les entrées type=source_thermale depuis le bloc THERMAL_SOURCES_CORSE.

    Applique THERMAL_OVERRIDES (Phase 1 §3.3).
    """
    out = []
    skipped = []
    for t in thermal_raw:
        nom_origin = t['nom']
        if nom_origin in SUPPRESSED_THERMAL_NAMES:
            skipped.append(nom_origin)
            continue
        override = THERMAL_OVERRIDES.get(nom_origin, {})
        if not override:
            raise RuntimeError(
                f'Source thermale "{nom_origin}" : pas d override audit défini. '
                'Compléter THERMAL_OVERRIDES ou SUPPRESSED_THERMAL_NAMES.'
            )

        slug = override['slug']
        lat = override.get('lat', t['lat'])
        lon = override.get('lon', t['lon'])
        nom = override.get('rename_nom_to', nom_origin)

        properties = {}
        for k in ('temperature_C', 'composition', 'debit_L_jour', 'agrement', 'altitude_m', 'statut'):
            if k in override:
                properties[k] = override[k]

        entry = {
            'slug': slug,
            'nom': nom,
            'lat': lat,
            'lon': lon,
            'type': 'source_thermale',
            'categorie': properties.get('composition', 'thermale'),
            'commune_nom': override.get('commune_nom'),
            'commune_insee': override.get('commune_insee'),
            'description': t.get('description', ''),
            'gps_source': override['gps_source'],
            'gps_audit': override.get('gps_audit'),
            'precision_coord': override['precision_coord'],
            'priorite': False,
            'phase_publication': 1,
            'sources_originales': ['THERMAL_SOURCES_CORSE'],
            'properties': properties,
        }
        if override.get('gps_audit_note'):
            entry['gps_audit_note'] = override['gps_audit_note']
        if override.get('gps_locked'):
            entry['gps_locked'] = True
            entry['gps_lock_reason'] = override.get('gps_lock_reason', '')
        if override.get('gps_status'):
            entry['gps_status'] = override['gps_status']

        out.append(entry)
    if skipped:
        print(f'  Sources thermales SUPPRIMÉES : {", ".join(skipped)}')
    return out


# ──────────────────────────────────────────────────────────────────────────────
# Vérifications finales
# ──────────────────────────────────────────────────────────────────────────────

def verify(sites):
    """Vérifie les invariants du schéma cible."""
    errs = []

    slugs = [s['slug'] for s in sites]
    dupes = {x for x in slugs if slugs.count(x) > 1}
    if dupes:
        errs.append(f'Slugs dupliqués : {dupes}')

    for s in sites:
        for req in ('slug', 'nom', 'lat', 'lon', 'type', 'categorie',
                    'gps_source', 'precision_coord'):
            if req not in s or s.get(req) is None:
                errs.append(f'{s.get("slug","?")} : champ {req} manquant ou null')

        # gps_audit : obligatoire SAUF si gps_status == "non_identifie" (Lac de Tora)
        if s.get('gps_status') != 'non_identifie':
            if not s.get('gps_audit'):
                errs.append(f'{s["slug"]} : gps_audit manquant (gps_status={s.get("gps_status")})')

        if not isinstance(s.get('lat'), (int, float)) or not isinstance(s.get('lon'), (int, float)):
            errs.append(f'{s["slug"]} : lat/lon non numériques')

        if s['type'] not in ('site_em', 'site_uth', 'source_thermale'):
            errs.append(f'{s["slug"]} : type invalide {s["type"]}')

    return errs


# ──────────────────────────────────────────────────────────────────────────────
# Sortie
# ──────────────────────────────────────────────────────────────────────────────

def write_sites_app(sites, summary):
    out = {
        '_meta': {
            'version': '1.0.0',
            'date_creation': AUDIT_DATE,
            'purpose': 'Sites ponctuels affichés sur app.html (couches site_em, site_uth, source_thermale). Consolidation M1 — voir docs/internal/AUDIT_COORDS_APP_2026-05-13.md et AUDIT_GPS_M1_2026-05-13.md.',
            'sources_consolidees': [
                'docs/data/sites_em.json (Brief 33 split 2026-05-06)',
                'public/data/points_chauds_radio_corse.json',
                'THERMAL_SOURCES_CORSE (array JS hardcodé app.html L.4536)',
            ],
            'types_referentiel': ['site_em', 'site_uth', 'source_thermale'],
            'conventions_gel_gps': (
                'gps_audit obligatoire (date ISO). gps_locked=true + '
                'gps_lock_reason pour les corrections manuelles Soleil. '
                'Exception : gps_status=non_identifie ou gps_status=a_verifier '
                'pour sites en attente de validation.'
            ),
            'rendering_hints': {
                'gps_status_non_identifie': (
                    'A implementer M2 (refactor app.html). Rendu Leaflet recommande : '
                    'marqueur gris + symbole attention dans tooltip, popup avec mention '
                    'Toponyme/site non identifie -- decision Soleil en attente. '
                    'Convention conservee meme si dataset M1 final = 0 entree avec ce statut.'
                ),
                'gps_status_a_verifier': (
                    'Toponyme/site identifie mais existence/coord a confirmer. '
                    'Rendu Leaflet recommande : marqueur orange + symbole point-interro dans tooltip.'
                ),
            },
            'phase3_reconciliation_summary': summary,
            'cloture_M1_2026_05_13': {
                'q15_monte_d_oro': 'slug uth_monte_d_oro, nom Monte d Oro, leucogranite en properties.type_specifique',
                'q18_caldane': 'resultat A -- pas de source distincte a Zevaco, renommage Sainte-Lucie-de-Tallano confirme',
                'q19_lac_de_tora': 'resultat B -- toponyme corrige Tolla mais aucune source thermale au Lac de Tolla. SUPPRESSION entree. Decompte 62 -> 61.',
                'q2_inzecca': '3e coord centroide 42.10/9.26 (mi-parcours D344 entre Sampolo et Saint-Antoine)',
                'q2_spelunca': 'adopt patrimoine 42.25368/8.76676 (Pont Vecciu IGN 4150 OT)',
            },
            'generated_by': 'tools/build_sites_app.py',
        },
        'sites': sites,
    }
    OUT_SITES_APP.parent.mkdir(parents=True, exist_ok=True)
    OUT_SITES_APP.write_text(
        json.dumps(out, ensure_ascii=False, indent=2, sort_keys=False),
        encoding='utf-8'
    )


# Main
def main():
    print('=' * 70)
    print('build_sites_app.py -- Consolidation M1 sites_app.json')
    print('=' * 70)

    sites_em_raw = load_sites_em()
    points_chauds_raw = load_points_chauds()
    thermal_raw = extract_thermal_from_app_html()
    patrimoine = load_patrimoine()

    print(f'  sites_em.json          : {len(sites_em_raw):3d} entrees')
    print(f'  points_chauds_radio    : {len(points_chauds_raw):3d} entrees')
    print(f'  THERMAL_SOURCES_CORSE  : {len(thermal_raw):3d} entrees (extrait app.html)')
    print(f'  SITES_REFERENCE.json   : {len(patrimoine):3d} entrees (patrimoine)')
    print()

    site_em, case_log = build_site_em_entries(sites_em_raw, patrimoine)
    site_uth = build_site_uth_entries(points_chauds_raw)
    source_thermale = build_source_thermale_entries(thermal_raw)

    sites = site_em + site_uth + source_thermale

    case_counts = {}
    for c in case_log:
        case_counts[c['case']] = case_counts.get(c['case'], 0) + 1
    print('Phase 3 -- Reconciliation patrimoine :')
    for case in sorted(case_counts):
        print(f'  Cas {case}: {case_counts[case]} entrees')
    print()

    summary = {
        'total_sites': len(sites),
        'by_type': {
            'site_em': len(site_em),
            'site_uth': len(site_uth),
            'source_thermale': len(source_thermale),
        },
        'reconciliation_cas': case_counts,
        'gps_audit_overrides_phase1': (
            len(AUDIT_OVERRIDES) + len(UTH_OVERRIDES) + len(THERMAL_OVERRIDES)
        ),
        'thermal_supprimees': sorted(SUPPRESSED_THERMAL_NAMES),
    }

    errs = verify(sites)
    if errs:
        print('VERIFICATIONS ECHOUEES :')
        for e in errs:
            print(f'  - {e}')
        sys.exit(2)

    print('Verifications : OK')
    print()

    sites.sort(key=lambda s: (s['type'], s['slug']))

    write_sites_app(sites, summary)
    print(f'  -> {OUT_SITES_APP} ecrit ({len(sites)} entrees)')
    print()
    print('Decompte final :')
    print(f'  site_em        : {len(site_em):3d}')
    print(f'  site_uth       : {len(site_uth):3d}')
    print(f'  source_thermale: {len(source_thermale):3d}')
    print(f'  TOTAL          : {len(sites):3d}')


if __name__ == '__main__':
    main()
