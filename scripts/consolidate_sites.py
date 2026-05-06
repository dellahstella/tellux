#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline de consolidation Tellux — sites_corse_v1.json
Brief Cowork 2026-05-06.
Lit les sources, normalise, dédoublonne, applique mappings, écrit livrables.
"""
import json, re, math, unicodedata, os, sys
from datetime import date, datetime
from collections import Counter, defaultdict

# ---------- Chemins ----------
ROOT = '/sessions/busy-awesome-mayer/mnt/Tellux'
OUT_DIR = '/sessions/busy-awesome-mayer/mnt/Tellux/_drafts'
os.makedirs(OUT_DIR, exist_ok=True)
TODAY = date.today().isoformat()  # ISO YYYY-MM-DD

# ---------- Outputs des sources Supabase pré-extraites (sur disque) ----------
SUPABASE_DUMP_DIR = '/sessions/busy-awesome-mayer/mnt/outputs'
with open(f'{SUPABASE_DUMP_DIR}/churches_dump.json') as f:
    CHURCHES_FROM_SUPABASE = json.load(f)
with open(f'{SUPABASE_DUMP_DIR}/patrimoine_dump.json') as f:
    PATRIMOINE_FROM_SUPABASE = json.load(f)

# ---------- Helpers ----------
def strip_accents(s):
    if not s:
        return ''
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def norm(s):
    """Normalisation pour comparaison nom : lowercase, sans accents/ponctuation/articles."""
    if not s:
        return ''
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9]+", ' ', s).strip()
    # supprimer articles fréquents
    s = re.sub(r'\b(de|du|d|la|le|les|saint|santa|sainte|san|sant|st)\b', '', s)
    s = re.sub(r'\s+', '', s)
    return s

def slugify(s):
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9]+", '_', s).strip('_')
    return s[:80]

def haversine_m(a, b):
    """Distance en mètres entre deux points (lat, lon)."""
    R = 6371000.0
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    aa = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(aa), math.sqrt(1-aa))

# ---------- Catégories canonisées (Q2 arbitré 2026-05-06) ----------
# Mapping catégorie source -> (categorie_canonique, axe_corpus, phase_publication)
CAT_MAP = {
    # SITES_PATRIMOINE / SITES_REFERENCE
    'Mégalithique':                                'megalithes',
    'Remarquable':                                 'remarquables_geologiques',     # → Site naturel remarquable
    'Site remarquable':                            'patrimoine_bati_remarquable',  # → Patrimoine bâti remarquable
    'B — Édifice roman':                           'edifices_romans',
    'B — Édifice religieux':                       'edifices_romans',              # autres édifices religieux assimilés
    'B — Édifice roman tardif (limite XVᵉ)':       'edifices_romans',
    'B — Édifice roman tardif (limite XIVᵉ, gothique de transition)': 'edifices_romans',
    'E — Diocèse historique':                      'diocese_medieval',             # entités géographiques abstraites
    'Hydraulique':                                 'hydrauliques',
    'Tour génoise':                                'tours_genoises',
    'Château médiéval':                            'chateaux_medievaux',
    'Patrimoine':                                  'patrimoine_divers',
    # patrimoine_corse Supabase
    'Pont génois':                                 'patrimoine_divers',
    'Patrimoine & Ressources':                     'patrimoine_divers',
    'Thermalisme':                                 'patrimoine_divers',
    # sites_remarquables_corse.json (catégories sémantiques)
    'ophiolite':                                   'remarquables_geologiques',
    'minier':                                      'patrimoine_divers',
    'surveillance_radio':                          'remarquables_geologiques',
    # churches_corse → toutes en edifices_romans
    'churches_default':                            'edifices_romans',
}
# Catégorie d'affichage finale (label humain)
CAT_DISPLAY = {
    'megalithes':                  'Mégalithique',
    'remarquables_geologiques':    'Site naturel remarquable',
    'patrimoine_bati_remarquable': 'Patrimoine bâti remarquable',
    'edifices_romans':             'Édifice roman',
    'diocese_medieval':            'Diocèse historique',
    'hydrauliques':                'Hydraulique',
    'tours_genoises':              'Tour génoise',
    'chateaux_medievaux':          'Château médiéval',
    'patrimoine_divers':           'Patrimoine',
}

# ---------- Phase de publication ----------
# Phase 1 = ce qui est exposé aujourd'hui par patrimoine.html (les 124 SITES_PATRIMOINE)
#         + les 10 sites_remarquables_corse (Phase 1 pleinement)
#         + patrimoine_corse 39 (intégrés runtime via R1-R10) → Phase 1
# Phase 2 = churches_corse exclusives + sites_corse Supabase exclusifs → Phase 2 latente
def default_phase(source_origin, axe_corpus):
    """Détermine la phase_publication selon la provenance."""
    if 'SITES_PATRIMOINE' in source_origin:
        return 1
    if 'sites_remarquables_corse' in source_origin:
        return 1
    if 'patrimoine_corse' in source_origin:
        return 1
    # Sites uniques à churches_corse OU SITES_REFERENCE :
    # SITES_REFERENCE étant déjà du contenu canonique runtime, garder Phase 1
    if 'SITES_REFERENCE' in source_origin or 'sites_corse_supabase' in source_origin:
        return 1
    if 'churches_corse' in source_origin:
        return 2  # Phase 2 latente
    return 1

# ---------- Chargement des sources ----------
def load_sources():
    sources = {}

    # 1) SITES_PATRIMOINE inline (124)
    with open(f'{ROOT}/patrimoine.html', encoding='utf-8') as f:
        html = f.read()
    m = re.search(r'SITES_PATRIMOINE\s*=\s*(\[.*?\]);', html, re.S)
    sources['SITES_PATRIMOINE'] = json.loads(m.group(1))

    # 2) SITES_REFERENCE.json (115)
    with open(f'{ROOT}/SITES_REFERENCE.json') as f:
        sources['SITES_REFERENCE'] = json.load(f)

    # 3) sites_remarquables_corse.json (10)
    with open(f'{ROOT}/public/data/sites_remarquables_corse.json') as f:
        sources['sites_remarquables_corse'] = json.load(f)['sites']

    # 4 + 5) Supabase tables (injectées via paramètre)
    sources['churches_corse'] = CHURCHES_FROM_SUPABASE
    sources['patrimoine_corse'] = PATRIMOINE_FROM_SUPABASE

    # Communes pour reverse lookup
    with open(f'{ROOT}/public/data/communes_corse.json') as f:
        sources['communes'] = json.load(f)['communes']

    # Mappings
    with open(f'{ROOT}/_drafts/doyennes_communes_mapping.json') as f:
        sources['doyennes'] = json.load(f)
    with open(f'{ROOT}/_drafts/pieves_communes_mapping.json') as f:
        sources['pieves_v1'] = json.load(f)
    with open(f'{ROOT}/_drafts/pieves_communes_mapping_v2_canonicite_casta.json') as f:
        sources['pieves_v2'] = json.load(f)

    return sources

# ---------- Lookups ----------
def build_lookups(srcs):
    # commune_nom (normalisé) -> (insee, nom_canonique)
    nom2insee = {}
    insee2nom = {}
    for c in srcs['communes']:
        insee = c['code_insee']
        nom = c['nom']
        nom2insee[norm(nom)] = (insee, nom)
        insee2nom[insee] = nom
    # doyenné lookup
    insee2doy = {}
    for d in srcs['doyennes']['doyennes']:
        for insee in d.get('communes_insee', []):
            insee2doy[insee] = d['slug']
    # pieve lookup (v1 puis v2 override)
    insee2pieve = {}
    for p in srcs['pieves_v1'].get('pieves', []):
        for insee in p.get('communes_insee', []):
            insee2pieve[insee] = p['slug']
    # v2 transferts (commune par commune)
    for t in srcs['pieves_v2'].get('transferts', []):
        if 'commune_insee' in t:
            insee2pieve[t['commune_insee']] = t['vers_pieve']
    # v2 pieves_added : ajouter si absent
    for p in srcs['pieves_v2'].get('pieves_added', []):
        for insee in p.get('communes_insee', []):
            insee2pieve.setdefault(insee, p['slug'])
    # diocèse médiéval depuis pieves
    pieve2diocese = {}
    for p in srcs['pieves_v1'].get('pieves', []):
        if 'diocese_medieval' in p:
            pieve2diocese[p['slug']] = p['diocese_medieval']
    for p in srcs['pieves_v2'].get('pieves_added', []):
        if 'diocese_medieval' in p:
            pieve2diocese[p['slug']] = p['diocese_medieval']
    return {
        'nom2insee': nom2insee,
        'insee2nom': insee2nom,
        'insee2doy': insee2doy,
        'insee2pieve': insee2pieve,
        'pieve2diocese': pieve2diocese,
    }

_SUFFIX_RE = re.compile(
    r'\s+(haute|basse|plaine|village|vieille\s+ville|haute\s+ville|basse\s+ville|'
    r'sud|nord|est|ouest|interieur|intérieur|littoral|centre|hameau|'
    r'castelluccio|bazzicacce)\b.*$',
    re.IGNORECASE,
)

def resolve_commune(commune_text, lookups):
    """Tente de résoudre une chaîne 'commune' en (insee, nom canonique).
    Stratégie multi-tentatives : avec/sans parens, sub-localité, suffixes."""
    if not commune_text:
        return None, None
    txt = commune_text.strip()
    # Récupérer le contenu des parenthèses (souvent commune réelle ou parent)
    parens = re.findall(r'\(([^)]+)\)', txt)
    main = re.sub(r'\(.*?\)', '', txt).strip()
    candidates = []
    # 1) main d'abord (premier élément si slash/virgule, suffixes strippés)
    for src in [main] + parens + [txt]:
        first = re.split(r'[/,]', src)[0].strip()
        first = _SUFFIX_RE.sub('', first).strip()
        candidates.append(first)
        # tenter aussi avec dernier composant après tirets longs
        if ' ' in first and any(w in first.lower() for w in ['de ', 'di ', 'd\'']):
            tail = re.sub(r'^.*?\b(?:de|di|d\')\s*', '', first, flags=re.IGNORECASE).strip()
            if tail:
                candidates.append(tail)
    # 2) Tentative avec parens si elles contiennent un nom de commune connu
    for cand in candidates:
        n = norm(cand)
        if n and n in lookups['nom2insee']:
            return lookups['nom2insee'][n]
    # 3) Fallback : substring match — input contient un nom de commune connu
    for cand in candidates:
        n = norm(cand)
        if not n or len(n) < 4:
            continue
        best = None
        best_len = 0
        for k, (insee, nom) in lookups['nom2insee'].items():
            if len(k) >= 5 and k in n and len(k) > best_len:
                best = (insee, nom)
                best_len = len(k)
        if best:
            return best
    return None, None

def extract_commune_from_nom(nom):
    """Extraire un toponyme depuis le 'nom' d'un site (ex: 'Tour d\'Erbalunga (Brando)' -> 'Brando')."""
    if not nom:
        return ''
    # 1) parens content
    parens = re.findall(r'\(([^)]+)\)', nom)
    if parens:
        # ignorer 'îlot', 'ruines', etc.
        for p in parens:
            p_norm = p.strip()
            if p_norm.lower() not in {'îlot', 'ilot', 'ruines', 'cap corse', 'castelluccio', 'pino/luri', 'sette navi', 'capo rosso'}:
                return p_norm
    # 2) Après "de" / "d'" dans le nom
    m = re.search(r"\b(?:de|d')\s+([A-ZÀ-Ü][\w\-À-ſ]+(?:\s+[A-ZÀ-Ü][\w\-À-ſ]+)*)$", nom)
    if m:
        return m.group(1).strip()
    return ''

# ---------- Normalisation par source ----------
def normalize_sites_patrimoine(entries, lookups):
    """SITES_PATRIMOINE inline → schéma cible."""
    out = []
    for e in entries:
        cat_src = e.get('categorie', '')
        axe = CAT_MAP.get(cat_src, 'patrimoine_divers')
        commune_text = e.get('commune', '')
        insee, nom_canon = resolve_commune(commune_text, lookups)
        site = {
            'slug': e['slug'],
            'nom': e['nom'],
            'lat': e['lat'],
            'lon': e['lon'],
            'categorie': CAT_DISPLAY.get(axe, cat_src),
            'axe_corpus': axe,
            'phase_publication': default_phase('SITES_PATRIMOINE', axe),
            'description': e.get('description', '') or None,
            'commune_insee': insee,
            'commune_nom': nom_canon or commune_text or None,
            'pieve_slug': lookups['insee2pieve'].get(insee) if insee else (e.get('pieve') or None),
            'diocese_medieval_slug': None,
            'doyenne_contemporain_slug': lookups['insee2doy'].get(insee) if insee else None,
            'visuel': e.get('visuel') or None,
            'illustre': bool(e.get('visuel')),
            'version_visuel': e.get('version') or None,
            'priorite': bool(e.get('priorite', False)),
            'couleur': None,
            'description_em': None,
            'gps_source': None,
            'gps_audit': None,
            'sources_originales': ['SITES_PATRIMOINE'],
            'notes': '',
        }
        # Cas special : E-Diocèse historique → entité abstraite
        if cat_src == 'E — Diocèse historique':
            site['phase_publication'] = 1
            site['notes'] = 'entite ecclesiastique medievale (centroide diocese) — sans ancrage communal'
            site['commune_insee'] = None
        # Heritage du diocese_medieval (si SITES_PATRIMOINE le contient)
        if e.get('diocese'):
            d_norm = e['diocese'].lower().strip()
            if d_norm in ['ajaccio','aleria','mariana','sagone','nebbio','nebbiu']:
                site['diocese_medieval_slug'] = 'ajaccio' if d_norm=='ajaccio' else d_norm.replace('nebbiu','nebbio')
        out.append(site)
    return out

def normalize_sites_reference(entries, lookups):
    """SITES_REFERENCE.json → schéma cible. (Mirror Supabase sites_corse, on traite ici.)"""
    out = []
    for e in entries:
        cat_src = e.get('type', '')
        axe = CAT_MAP.get(cat_src, 'patrimoine_divers')
        # Tentative d'extraction commune depuis nom + fallback substring sur nom complet
        guess = extract_commune_from_nom(e.get('nom', ''))
        insee, nom_canon = resolve_commune(guess, lookups) if guess else (None, None)
        if not insee:
            insee, nom_canon = resolve_commune(e.get('nom', ''), lookups)
        site = {
            'slug': slugify(e['nom']),
            'nom': e['nom'],
            'lat': e['lat'],
            'lon': e['lon'],
            'categorie': CAT_DISPLAY.get(axe, cat_src),
            'axe_corpus': axe,
            'phase_publication': default_phase('SITES_REFERENCE', axe),
            'description': e.get('description', '') or None,
            'commune_insee': insee,
            'commune_nom': nom_canon,
            'pieve_slug': lookups['insee2pieve'].get(insee) if insee else None,
            'diocese_medieval_slug': None,
            'doyenne_contemporain_slug': lookups['insee2doy'].get(insee) if insee else None,
            'visuel': None,
            'illustre': False,
            'version_visuel': None,
            'priorite': False,
            'couleur': e.get('couleur'),
            'description_em': None,
            'gps_source': e.get('gps_source'),
            'gps_audit': e.get('gps_audit'),
            'sources_originales': ['SITES_REFERENCE','sites_corse_supabase'],
            'notes': '',
        }
        out.append(site)
    return out

def normalize_sites_remarquables(entries, lookups):
    """sites_remarquables_corse.json → schéma."""
    out = []
    for e in entries:
        cat_src = e.get('categorie', '')
        axe = CAT_MAP.get(cat_src, 'patrimoine_divers')
        commune_text = e.get('commune', '')
        insee, nom_canon = resolve_commune(commune_text, lookups)
        site = {
            'slug': slugify(e.get('id') or e.get('nom')),
            'nom': e['nom'],
            'lat': e['lat'],
            'lon': e['lon'],
            'categorie': CAT_DISPLAY.get(axe, cat_src),
            'axe_corpus': axe,
            'phase_publication': 1,
            'description': e.get('note_ui') or e.get('historique', '') or None,
            'commune_insee': insee,
            'commune_nom': nom_canon or commune_text or None,
            'pieve_slug': lookups['insee2pieve'].get(insee) if insee else None,
            'diocese_medieval_slug': None,
            'doyenne_contemporain_slug': lookups['insee2doy'].get(insee) if insee else None,
            'visuel': None,
            'illustre': False,
            'version_visuel': None,
            'priorite': False,
            'couleur': None,
            'description_em': {
                'signature_em': e.get('signature_em'),
                'impact_modele': e.get('impact_modele'),
                'historique': e.get('historique'),
                'statut_actuel': e.get('statut_actuel'),
                'source_principale': e.get('source_principale'),
                'precision_coord': e.get('precision_coord'),
                'type_specifique': e.get('type'),
            },
            'gps_source': e.get('source_principale'),
            'gps_audit': '2026-04-23',  # date_maj du fichier source
            'sources_originales': ['sites_remarquables_corse'],
            'notes': '',
        }
        out.append(site)
    return out

def normalize_churches(entries, lookups):
    """churches_corse Supabase → schéma cible."""
    out = []
    for e in entries:
        commune_text = e.get('lieu', '')
        insee, nom_canon = resolve_commune(commune_text, lookups)
        pieve_slug = lookups['insee2pieve'].get(insee) if insee else None
        diocese = lookups['pieve2diocese'].get(pieve_slug)
        nom_complet = e['name']
        # Dans churches_corse le name est court (ex: 'San Colombano') → désambiguer avec lieu
        if commune_text and norm(commune_text) not in norm(nom_complet):
            nom_full = f"{nom_complet} ({commune_text})"
        else:
            nom_full = nom_complet
        site = {
            'slug': slugify(f"{nom_complet}_{commune_text or e.get('id','')}"),
            'nom': nom_full,
            'lat': float(e['lat']),
            'lon': float(e['lon']),
            'categorie': 'Édifice roman',
            'axe_corpus': 'edifices_romans',
            'phase_publication': default_phase('churches_corse', 'edifices_romans'),
            'description': e.get('note') or None,
            'commune_insee': insee,
            'commune_nom': nom_canon or commune_text or None,
            'pieve_slug': pieve_slug,
            'diocese_medieval_slug': diocese.lower() if diocese else None,
            'doyenne_contemporain_slug': lookups['insee2doy'].get(insee) if insee else None,
            'visuel': None,
            'illustre': False,
            'version_visuel': None,
            'priorite': False,
            'couleur': None,
            'description_em': None,
            'gps_source': 'churches_corse Supabase (Moracchini-Mazel + audit)',
            'gps_audit': None,
            'sources_originales': ['churches_corse'],
            'notes': f"siecle={e.get('siecle','')} mat={e.get('mat','')} sub={e.get('sub','')} mh={e.get('mh','')}".strip(),
        }
        out.append(site)
    return out

def normalize_patrimoine_corse(entries, lookups):
    """patrimoine_corse Supabase (39 entrées Tour/Château/etc) → schéma."""
    out = []
    for e in entries:
        cat_src = e.get('categorie', '')
        axe = CAT_MAP.get(cat_src, 'patrimoine_divers')
        guess = extract_commune_from_nom(e.get('nom', ''))
        insee, nom_canon = resolve_commune(guess, lookups) if guess else (None, None)
        if not insee:
            insee, nom_canon = resolve_commune(e.get('nom', ''), lookups)
        site = {
            'slug': slugify(e['nom']),
            'nom': e['nom'],
            'lat': float(e['lat']),
            'lon': float(e['lon']),
            'categorie': CAT_DISPLAY.get(axe, cat_src),
            'axe_corpus': axe,
            'phase_publication': default_phase('patrimoine_corse', axe),
            'description': e.get('description') or None,
            'commune_insee': insee,
            'commune_nom': nom_canon,
            'pieve_slug': lookups['insee2pieve'].get(insee) if insee else None,
            'diocese_medieval_slug': None,
            'doyenne_contemporain_slug': lookups['insee2doy'].get(insee) if insee else None,
            'visuel': None,
            'illustre': False,
            'version_visuel': None,
            'priorite': False,
            'couleur': (e.get('couleur') or '').strip() or None,
            'description_em': None,
            'gps_source': 'patrimoine_corse Supabase (R1-R10 campagne)',
            'gps_audit': None,
            'sources_originales': ['patrimoine_corse'],
            'notes': '',
        }
        out.append(site)
    return out

# ---------- Déduplication ----------
def dedupe_sites(all_sites, dist_threshold_m=150):
    """
    Stratégie :
      1) clé = (norm(nom), categorie compatible) → match exact si même catégorie cible
      2) sinon GPS proximity ≤ 150m + axes compatibles → marqué doublon
      3) priorité de fusion : SITES_PATRIMOINE > sites_remarquables > SITES_REFERENCE > churches_corse > patrimoine_corse
    Renvoie (sites_canoniques, dedup_log).
    """
    PRIORITY = {
        'SITES_PATRIMOINE': 5,
        'sites_remarquables_corse': 4,
        'patrimoine_corse': 3,
        'SITES_REFERENCE': 2,
        'sites_corse_supabase': 2,
        'churches_corse': 1,
    }
    def src_priority(s):
        return max((PRIORITY.get(x, 0) for x in s['sources_originales']), default=0)

    # Compatibilité d'axes (deux sites de même axe peuvent fusionner ; certains axes sont fusionnables)
    AXIS_COMPAT = {
        'megalithes':                  {'megalithes', 'remarquables_geologiques'},
        'remarquables_geologiques':    {'remarquables_geologiques', 'megalithes', 'patrimoine_bati_remarquable'},
        'patrimoine_bati_remarquable': {'patrimoine_bati_remarquable', 'remarquables_geologiques', 'tours_genoises', 'chateaux_medievaux'},
        'edifices_romans':             {'edifices_romans', 'patrimoine_divers'},
        'diocese_medieval':            {'diocese_medieval'},
        'hydrauliques':                {'hydrauliques'},
        'tours_genoises':              {'tours_genoises', 'patrimoine_bati_remarquable'},
        'chateaux_medievaux':          {'chateaux_medievaux', 'patrimoine_bati_remarquable'},
        'patrimoine_divers':           {'patrimoine_divers', 'patrimoine_bati_remarquable', 'tours_genoises', 'chateaux_medievaux', 'edifices_romans'},
    }

    canonical = []
    dedup_log = {}
    used = [False] * len(all_sites)

    # Tri par priorité de source décroissante (canoniques traités en premier)
    indices = sorted(range(len(all_sites)), key=lambda i: -src_priority(all_sites[i]))

    for i in indices:
        if used[i]:
            continue
        a = all_sites[i]
        used[i] = True
        merged_sources = set(a['sources_originales'])
        merged_aliases = []
        # Chercher candidats doublons
        for j in indices:
            if used[j] or j == i:
                continue
            b = all_sites[j]
            # Test catégories compatibles
            if b['axe_corpus'] not in AXIS_COMPAT.get(a['axe_corpus'], {a['axe_corpus']}):
                continue
            # Test nom normalisé
            same_name = (norm(a['nom']) == norm(b['nom']) and len(norm(a['nom'])) > 2)
            # Test GPS
            try:
                d = haversine_m((a['lat'], a['lon']), (b['lat'], b['lon']))
            except Exception:
                d = 99999
            close = d <= dist_threshold_m
            if same_name or close:
                # fusion
                merged_sources |= set(b['sources_originales'])
                merged_aliases.append({
                    'slug_alias': b['slug'],
                    'nom_alias': b['nom'],
                    'distance_m': round(d, 1),
                    'source': list(b['sources_originales']),
                    'reason': 'name_match' if same_name else 'gps_proximity',
                })
                # Si b apporte une info manquante (commune_insee, gps_source, etc.), enrichir a
                for fld in ['commune_insee', 'commune_nom', 'pieve_slug',
                            'diocese_medieval_slug', 'doyenne_contemporain_slug',
                            'visuel', 'version_visuel', 'gps_source', 'gps_audit',
                            'description_em', 'couleur']:
                    if not a.get(fld) and b.get(fld):
                        a[fld] = b[fld]
                if not a.get('illustre') and b.get('illustre'):
                    a['illustre'] = True
                # priorite : OR
                if b.get('priorite'):
                    a['priorite'] = True
                # description : garder la plus longue
                if b.get('description') and len(b['description']) > len(a.get('description') or ''):
                    a['description'] = b['description']
                # phase_publication : garder le min (le plus exposé)
                if b.get('phase_publication', 9) < a.get('phase_publication', 9):
                    a['phase_publication'] = b['phase_publication']
                used[j] = True
        a['sources_originales'] = sorted(merged_sources)
        if merged_aliases:
            dedup_log[a['slug']] = {
                'nom_canonique': a['nom'],
                'sources_canoniques': a['sources_originales'],
                'aliases_merged': merged_aliases,
            }
        canonical.append(a)
    return canonical, dedup_log

# ---------- Audit GPS spécial : Cap Corse extrême nord ----------
def audit_gps(sites):
    """Application des décisions Q3 du Stop Point §6.1."""
    audits = []
    for s in sites:
        if s['slug'] == 'cap_corse_extreme_nord':
            old = (s['lat'], s['lon'])
            s['lat'] = 43.005
            s['lon'] = 9.395
            s['nom'] = 'Capu Bianchi — extrême nord Cap Corse'
            s['description'] = ("Pointe la plus septentrionale de la presqu'île de Barcaggio · "
                                "Capu Bianchi · Ophiolites altérées · Serpentinite verte · "
                                "Susceptibilité magnétique variable")
            s['gps_source'] = 'OSM / Wikidata Capu Bianchi (audit Tellux 2026-05-06)'
            s['gps_audit'] = TODAY
            s['notes'] = ("GPS déplacé le 2026-05-06 de l'ancienne valeur "
                          f"({old[0]},{old[1]}) à (43.005,9.395). "
                          "Distinct de la Tour d'Agnello (~43.009/9.422, ~2,7 km à l'est) "
                          "et de l'île Giraglia (~43.028/9.405, îlot au large).")
            audits.append({'slug': s['slug'], 'change': 'moved', 'from': old, 'to': (s['lat'], s['lon'])})
    return audits

# ---------- Exports ----------
def write_outputs(canonical, dedup_log, gps_audits, sources_summary):
    # _drafts/sites_corse_v1.json
    # Garde-fou : dédupliquer slugs (suffixer _2, _3 si collision)
    seen_slugs = {}
    for s in canonical:
        base = s['slug']
        if base in seen_slugs:
            seen_slugs[base] += 1
            s['slug'] = f"{base}_{seen_slugs[base]}"
            s['notes'] = (s.get('notes','') + ' | slug suffixé pour unicité').strip(' |')
        else:
            seen_slugs[base] = 1

    out = {
        '_meta': {
            'version': '1.0',
            'date_creation': TODAY,
            'source': 'Consolidation Cowork — Tellux Corse (Stop Point §6.1 validé 2026-05-06)',
            'total_sites': len(canonical),
            'axes_corpus': sorted(set(s['axe_corpus'] for s in canonical)),
            'rattachement_doyenne_source': '_drafts/doyennes_communes_mapping.json',
            'rattachement_pieve_source': '_drafts/pieves_communes_mapping_v2_canonicite_casta.json (extends v1)',
            'phase_publication_legend': {
                '1': 'exposé Phase 1 (patrimoine.html runtime actuel)',
                '2': 'préparé Phase 2 latente (non exposé tant que Phase 2 non ouverte)',
            },
            'sources_summary': sources_summary,
            'gps_audit_changes': gps_audits,
        },
        'sites': canonical,
    }
    p1 = f'{OUT_DIR}/sites_corse_v1.json'
    with open(p1, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    # SITES_DEDUPLICATION_LOG.json
    p2 = f'{OUT_DIR}/SITES_DEDUPLICATION_LOG.json'
    with open(p2, 'w', encoding='utf-8') as f:
        json.dump({
            '_meta': {
                'date': TODAY,
                'method': 'name_normalized_match OR gps_proximity_150m + axis_compat',
                'priority_order': ['SITES_PATRIMOINE','sites_remarquables_corse','patrimoine_corse','SITES_REFERENCE/sites_corse_supabase','churches_corse'],
                'total_canonical': len(canonical),
                'total_aliases_merged': sum(len(v['aliases_merged']) for v in dedup_log.values()),
            },
            'mappings': dedup_log,
        }, f, ensure_ascii=False, indent=2)
    return p1, p2

# ---------- Pipeline ----------
def run():
    srcs = load_sources()
    lookups = build_lookups(srcs)

    sources_summary = {
        'SITES_PATRIMOINE_inline_patrimoine.html': len(srcs['SITES_PATRIMOINE']),
        'SITES_REFERENCE.json_root': len(srcs['SITES_REFERENCE']),
        'sites_remarquables_corse.json': len(srcs['sites_remarquables_corse']),
        'churches_corse_supabase': len(srcs['churches_corse']),
        'patrimoine_corse_supabase': len(srcs['patrimoine_corse']),
        'sites_corse_supabase_mirror_of_SITES_REFERENCE': 'fusionnée avec SITES_REFERENCE (mirror identique 115/115)',
    }

    all_sites = []
    all_sites += normalize_sites_patrimoine(srcs['SITES_PATRIMOINE'], lookups)
    all_sites += normalize_sites_reference(srcs['SITES_REFERENCE'], lookups)
    all_sites += normalize_sites_remarquables(srcs['sites_remarquables_corse'], lookups)
    all_sites += normalize_churches(srcs['churches_corse'], lookups)
    all_sites += normalize_patrimoine_corse(srcs['patrimoine_corse'], lookups)

    print(f'Total brut avant déduplication : {len(all_sites)}')
    canonical, dedup_log = dedupe_sites(all_sites)
    print(f'Total canoniques après déduplication : {len(canonical)}')

    gps_audits = audit_gps(canonical)

    # Stats finales
    by_axe = Counter(s['axe_corpus'] for s in canonical)
    by_phase = Counter(s['phase_publication'] for s in canonical)
    with_doy = sum(1 for s in canonical if s.get('doyenne_contemporain_slug'))
    with_pieve = sum(1 for s in canonical if s.get('pieve_slug'))
    with_insee = sum(1 for s in canonical if s.get('commune_insee'))
    orphans = sum(1 for s in canonical if not s.get('commune_insee'))

    print(f"\nPar axe_corpus : {dict(by_axe.most_common())}")
    print(f"Par phase_publication : {dict(by_phase)}")
    print(f"commune_insee renseignée : {with_insee} | orphans : {orphans}")
    print(f"doyenne renseigné : {with_doy} | pieve renseigné : {with_pieve}")
    print(f"Doublons fusionnés : {sum(len(v['aliases_merged']) for v in dedup_log.values())}")

    p1, p2 = write_outputs(canonical, dedup_log, gps_audits, sources_summary)
    print(f"\nÉcrits :\n  {p1}\n  {p2}")

if __name__ == '__main__':
    run()
