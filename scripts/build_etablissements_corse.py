#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build des trois GeoJSON etablissements sensibles Corse pour Tellux.

Sources :
- Annuaire de l'education (data.education.gouv.fr, rediffusion data.gouv.fr)
- FINESS (DREES, extraction etablissements via data.gouv.fr)
- EAJE POI (CAF via data.gouv.fr)

Licence des donnees sources : Licence ouverte / Open Licence (Etalab 2.0).
Les donnees restent la propriete des producteurs (ministere de l'Education nationale,
DREES / ministere des Solidarites et de la Sante, CNAF). Attribution obligatoire.

Usage :
    python build_etablissements_corse.py [--source annuaire|finess|eaje|all]
                                         [--output DIR]
                                         [--verbose]

Sorties (dans --output, par defaut ./output) :
    etablissements_enseignement_corse.geojson
    etablissements_medicosocial_corse.geojson
    etablissements_petite_enfance_corse.geojson
    features_rejected.geojson  (si features rejetees)
    build_stats.json           (statistiques par source)

Schema commun des Features en sortie (FeatureCollection, EPSG:4326) :
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [lon, lat]},
      "properties": {
        "id": str,                # identifiant source stable
        "nom": str,
        "categorie": "enseignement" | "medico-social" | "petite-enfance",
        "sous_categorie": str,    # stable, voir MAPPING_*
        "adresse": str | None,
        "code_postal": str | None,
        "commune": str | None,
        "code_insee": str | None,
        "secteur": "public" | "prive_sous_contrat" | "prive_hors_contrat" | None,
        "source": "annuaire_education" | "finess" | "eaje_caf",
        "date_extraction": "YYYY-MM-DD"
      }
    }

Version : 1.0
Date    : 24 avril 2026
Auteur  : session Cowork Tellux

ALERTE VEILLE FINESS ETE 2026
-----------------------------
La DREES a annonce une nouvelle version de FINESS a l'ete 2026, avec arret
du flux actuel. Si ce script cesse de fonctionner apres juillet 2026, reevaluer
la section download_finess() et le mapping MAPPING_FINESS. Ouvrir un ticket
de suivi entre juin et septembre 2026.

NOTE IMPORTANTE POUR L'UTILISATEUR
----------------------------------
Ce script doit etre execute depuis une machine disposant d'un acces reseau
libre vers data.gouv.fr, data.education.gouv.fr, et www.data.gouv.fr.
Il n'a pas ete execute dans l'environnement Cowork ou il a ete redige
(allowlist reseau restreinte). Les mappings FINESS ci-dessous ont ete
etablis sur la base de la nomenclature DREES connue a la date de redaction.
Une relecture est recommandee avant premiere execution reelle.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import logging
import os
import sys
from dataclasses import dataclass, asdict, field
from datetime import date
from typing import Iterable, Iterator

import requests


# ---------------------------------------------------------------------------
# Configuration globale
# ---------------------------------------------------------------------------

# Bornes GPS approximatives de la Corse (marge de securite au-dela de l'ile
# administrative pour capturer les ilots cotiers et eviter des rejets faux
# positifs liees a la precision de la geolocalisation). Ajuster si necessaire.
BOUNDS_CORSE = {
    "lat_min": 41.3,
    "lat_max": 43.1,
    "lon_min": 8.5,
    "lon_max": 9.6,
}

# Codes departementaux de la Corse.
DEPT_CORSE = ("2A", "2B")
# Variantes INSEE historiques (pour FINESS notamment, parfois code 20 utilise).
DEPT_CORSE_VARIANTS = ("2A", "2B", "20A", "20B", "20")

# URL API data.education.gouv.fr v2.1 (Explore API). Filtree par departement.
URL_EDUCATION_API_V2 = (
    "https://data.education.gouv.fr/api/explore/v2.1/catalog/"
    "datasets/fr-en-annuaire-education/records"
)

# Slug data.gouv.fr pour FINESS - extraction du fichier des etablissements.
# L'API data.gouv.fr retourne la liste des ressources avec URL stable.
DATAGOUV_DATASET_FINESS = "finess-extraction-du-fichier-des-etablissements"
DATAGOUV_DATASET_EAJE_POI = "poi-eaje-3"
URL_API_DATA_GOUV = "https://www.data.gouv.fr/api/1/datasets/{slug}/"

# User-Agent : politesse envers les serveurs publics. Indique le projet.
USER_AGENT = (
    "TelluxCorse/1.0 build_etablissements_corse.py "
    "(+https://tellux.pages.dev) Python-requests"
)

# Timeout HTTP en secondes.
HTTP_TIMEOUT = 60

# Pagination API Education (limite dure de 100 par page sur Explore API v2.1).
EDUCATION_PAGE_SIZE = 100

DATE_EXTRACTION = date.today().isoformat()


# ---------------------------------------------------------------------------
# Mappings des categories
# ---------------------------------------------------------------------------

# Annuaire Education : type_etablissement -> sous_categorie Tellux.
# Source nomenclature : Rectorat, RAMSESE. Liste non exhaustive, valeurs non
# listees sont mappees sur "autre".
MAPPING_ANNUAIRE_EDUCATION = {
    "Ecole maternelle": "ecole_maternelle",
    "Ecole de specialisation maternelle": "ecole_maternelle",
    "Ecole elementaire": "ecole_elementaire",
    "Ecole primaire": "ecole_primaire",
    "College": "college",
    "Lycee": "lycee_general",
    "Lycee general": "lycee_general",
    "Lycee d enseignement general et technologique": "lycee_general",
    "Lycee technologique": "lycee_technologique",
    "Lycee professionnel": "lycee_professionnel",
    "Lycee polyvalent": "lycee_polyvalent",
    "Etablissement regional d enseignement adapte": "erea",
    "Centre de formation d apprentis": "cfa",
    "Section d enseignement general et professionnel adapte": "segpa",
}

# Secteur Annuaire Education.
MAPPING_ANNUAIRE_SECTEUR = {
    "PU": "public",
    "PR": "prive_sous_contrat",  # approximation, le champ secteur_prive_code_type_contrat
                                 # permet d'affiner si besoin.
}

# FINESS : categorie_etablissement (code) -> sous_categorie Tellux.
# Source : nomenclature DREES FINESS des categories d'etablissements.
# A VALIDER par Soleil a la premiere execution : certains codes peuvent
# differer selon la version du referentiel. La liste ci-dessous est
# conservative (n'inclut que ce qui est pertinent pour le dispositif sensible
# au sens Loi Abeille). Pharmacies, laboratoires, cabinets liberaux exclus.
MAPPING_FINESS = {
    # Personnes agees
    "500": "ehpad",              # Etablissement d'Hebergement pour Personnes Agees Dependantes
    "501": "usld",               # Unite de Soins de Longue Duree
    "502": "residence_autonomie",# Residence autonomie (ex-logement foyer)
    "200": "ehpad",              # Maison de retraite (historique, avant conversion EHPAD)
    # Handicap adultes
    "354": "mas",                # Maison d'Accueil Specialisee
    "437": "fam",                # Foyer d'Accueil Medicalise
    "253": "fam",                # Variante mentionnee dans certaines nomenclatures
    "195": "foyer_hebergement",  # Foyer d'hebergement pour adultes handicapes
    "382": "foyer_vie",          # Foyer de vie / foyer occupationnel
    "446": "ssad_handicap",      # Service accompagnement medico-social adultes
    # Handicap enfants
    "183": "ime",                # Institut Medico-Educatif
    "186": "itep",               # Institut Therapeutique, Educatif et Pedagogique
    "196": "iem",                # Institut d'Education Motrice
    "192": "sessad",             # SESSAD (service d'education speciale et de soins a domicile)
    "238": "centre_accueil_enfants", # Centre d'accueil pour enfants handicapes
    # Sanitaire
    "101": "chu",                # Centre Hospitalier Universitaire
    "355": "ch",                 # Centre Hospitalier
    "106": "ch",                 # Centre Hospitalier (variante historique)
    "365": "chs",                # Centre Hospitalier Specialise / psychiatrie
    "365": "chs",
    "128": "clinique_privee",    # Etablissement de sante prive
    "131": "centre_lutte_cancer",# Centre de Lutte Contre le Cancer
}

# EAJE : type_structure (POI) -> sous_categorie Tellux.
# Source : nomenclature CAF / CNAF.
MAPPING_EAJE = {
    "Creche collective": "creche_collective",
    "Creche parentale": "creche_parentale",
    "Creche familiale": "creche_familiale",
    "Multi-accueil": "multi_accueil",
    "Multi accueil": "multi_accueil",
    "Halte-garderie": "halte_garderie",
    "Halte garderie": "halte_garderie",
    "Micro-creche": "micro_creche",
    "Micro creche": "micro_creche",
    "Jardin d'enfants": "jardin_enfants",
    "Jardin d enfants": "jardin_enfants",
}


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

LOG = logging.getLogger("tellux.etablissements_corse")


def setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )


def http_get(url: str, params: dict | None = None, stream: bool = False) -> requests.Response:
    """GET HTTP robuste avec User-Agent, timeout, et raise_for_status."""
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, params=params, headers=headers, timeout=HTTP_TIMEOUT, stream=stream)
    resp.raise_for_status()
    return resp


def is_in_corse_bounds(lon: float | None, lat: float | None) -> bool:
    if lon is None or lat is None:
        return False
    try:
        lon_f = float(lon)
        lat_f = float(lat)
    except (TypeError, ValueError):
        return False
    return (
        BOUNDS_CORSE["lat_min"] <= lat_f <= BOUNDS_CORSE["lat_max"]
        and BOUNDS_CORSE["lon_min"] <= lon_f <= BOUNDS_CORSE["lon_max"]
    )


def round_coord(x: float, decimals: int = 6) -> float:
    return round(float(x), decimals)


def clean_str(value) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None


# ---------------------------------------------------------------------------
# Classes de travail
# ---------------------------------------------------------------------------

@dataclass
class Feature:
    lon: float
    lat: float
    id: str
    nom: str
    categorie: str
    sous_categorie: str
    adresse: str | None
    code_postal: str | None
    commune: str | None
    code_insee: str | None
    secteur: str | None
    source: str
    date_extraction: str = field(default_factory=lambda: DATE_EXTRACTION)
    rejection_reason: str | None = None

    def to_geojson(self) -> dict:
        props = {
            "id": self.id,
            "nom": self.nom,
            "categorie": self.categorie,
            "sous_categorie": self.sous_categorie,
            "adresse": self.adresse,
            "code_postal": self.code_postal,
            "commune": self.commune,
            "code_insee": self.code_insee,
            "secteur": self.secteur,
            "source": self.source,
            "date_extraction": self.date_extraction,
        }
        if self.rejection_reason:
            props["rejection_reason"] = self.rejection_reason
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [round_coord(self.lon), round_coord(self.lat)],
            },
            "properties": props,
        }


# ---------------------------------------------------------------------------
# Source 1 : Annuaire de l'education
# ---------------------------------------------------------------------------

def download_annuaire_education() -> Iterator[Feature]:
    """Pagination Explore API v2.1 filtree par departement Corse."""
    LOG.info("Annuaire Education : telechargement (API Explore v2.1, filtre 02A+02B)")
    # TELLUX FIX 2026-04-24 : l'API Explore v2.1 stocke code_departement avec un
    # zero initial (format "02A"/"02B"), pas "2A"/"2B". Verifie en direct :
    # code_departement="2A" renvoie 0 resultat, code_departement="02A" renvoie 155.
    where = 'code_departement in ("02A","02B")'
    offset = 0
    while True:
        params = {
            "where": where,
            "limit": EDUCATION_PAGE_SIZE,
            "offset": offset,
        }
        resp = http_get(URL_EDUCATION_API_V2, params=params)
        payload = resp.json()
        records = payload.get("results", [])
        if not records:
            break
        LOG.debug("Annuaire Education : page offset=%d, %d records", offset, len(records))
        for rec in records:
            feat = _normalize_annuaire_record(rec)
            if feat is not None:
                yield feat
        if len(records) < EDUCATION_PAGE_SIZE:
            break
        offset += EDUCATION_PAGE_SIZE
    LOG.info("Annuaire Education : telechargement termine.")


def _normalize_annuaire_record(rec: dict) -> Feature | None:
    """Un record Explore v2.1 est un dict a plat avec les champs de la source."""
    uai = clean_str(rec.get("identifiant_de_l_etablissement"))
    nom = clean_str(rec.get("nom_etablissement"))
    if not uai or not nom:
        LOG.debug("Annuaire Education : record sans UAI ou sans nom, ignore.")
        return None
    type_etab = clean_str(rec.get("type_etablissement")) or ""
    # TELLUX FIX 2026-04-24 : l'API Explore v2.1 expose le type sous forme
    # generique ("Ecole", "College", "Lycee", "EREA", "Medico-social",
    # "Service Administratif", "Information et orientation"), sans detail
    # maternelle/elementaire/general/technologique/professionnel. Les details
    # sont dans les champs booleens ecole_maternelle, ecole_elementaire,
    # voie_generale, voie_technologique, voie_professionnelle.
    # Les types "Medico-social", "Service Administratif" et "Information et
    # orientation" ne relevent pas de l'enseignement Loi Abeille : ils sont
    # ignores (non retournes).
    sous_cat = _derive_sous_cat_education(type_etab, rec)
    if sous_cat is None:
        LOG.debug("Annuaire Education : %s type %r hors perimetre enseignement sensible.", uai, type_etab)
        return None
    secteur_code = clean_str(rec.get("statut_public_prive"))  # "Public" / "Prive"
    if secteur_code and secteur_code.lower().startswith("public"):
        secteur = "public"
    elif secteur_code and secteur_code.lower().startswith("prive"):
        # L'Explore API expose aussi un champ secteur_code_type_contrat.
        contrat = clean_str(rec.get("secteur_prive_code_type_contrat"))
        secteur = "prive_sous_contrat" if contrat else "prive_hors_contrat"
    else:
        secteur = None

    # Geometrie : la source expose souvent "position" (geojson point) ou
    # "latitude" et "longitude" separes. On gere les deux.
    lon, lat = _extract_lonlat_annuaire(rec)
    if lon is None or lat is None:
        LOG.debug("Annuaire Education : %s sans coordonnees, a rejeter.", uai)
        return Feature(
            lon=0.0, lat=0.0, id=uai, nom=nom,
            categorie="enseignement", sous_categorie=sous_cat,
            adresse=clean_str(rec.get("adresse_1")),
            code_postal=clean_str(rec.get("code_postal")),
            commune=clean_str(rec.get("nom_commune")),
            code_insee=clean_str(rec.get("code_commune")),
            secteur=secteur,
            source="annuaire_education",
            rejection_reason="no_coordinates",
        )
    return Feature(
        lon=lon, lat=lat, id=uai, nom=nom,
        categorie="enseignement", sous_categorie=sous_cat,
        adresse=clean_str(rec.get("adresse_1")),
        code_postal=clean_str(rec.get("code_postal")),
        commune=clean_str(rec.get("nom_commune")),
        code_insee=clean_str(rec.get("code_commune")),
        secteur=secteur,
        source="annuaire_education",
    )


# TELLUX FIX 2026-04-24 : derivation du sous_categorie pour l'Annuaire Education
# a partir du type generique + des champs booleens. Remplace le lookup direct
# par MAPPING_ANNUAIRE_EDUCATION qui attendait des types detailles inexistants.
def _derive_sous_cat_education(type_etab: str, rec: dict) -> str | None:
    t = (type_etab or "").strip().lower()

    # Hors perimetre enseignement sensible : retour None pour filtrage en amont.
    if not t or t in ("medico-social", "service administratif", "information et orientation"):
        return None

    def truthy(k: str) -> bool:
        v = rec.get(k)
        return v in (1, "1", True)

    if "ecole" in t:
        mat = truthy("ecole_maternelle")
        elem = truthy("ecole_elementaire")
        if mat and elem:
            return "ecole_primaire"
        if mat:
            return "ecole_maternelle"
        if elem:
            return "ecole_elementaire"
        return "ecole_primaire"  # fallback neutre "ecole"
    if "college" in t or "coll\u00e8ge" in t:
        return "college"
    if "lycee" in t or "lyc\u00e9e" in t:
        g = truthy("voie_generale")
        tg = truthy("voie_technologique")
        p = truthy("voie_professionnelle")
        if g and tg and p:
            return "lycee_polyvalent"
        if g and tg:
            return "lycee_general"
        if p and not (g or tg):
            return "lycee_professionnel"
        if tg and not (g or p):
            return "lycee_technologique"
        if g and not (tg or p):
            return "lycee_general"
        # fallback : probablement polyvalent/inconnu
        return "lycee_polyvalent"
    if "erea" in t:
        return "erea"
    if "cfa" in t or "apprentis" in t:
        return "cfa"
    if "segpa" in t:
        return "segpa"
    return "autre"


def _extract_lonlat_annuaire(rec: dict) -> tuple[float | None, float | None]:
    # Format 1 : champ position = {"lon": x, "lat": y}
    pos = rec.get("position")
    if isinstance(pos, dict):
        return pos.get("lon"), pos.get("lat")
    # Format 2 : latitude et longitude separes
    lat = rec.get("latitude")
    lon = rec.get("longitude")
    if lat is not None and lon is not None:
        return lon, lat
    # Format 3 : champs coordonnees_x, coordonnees_y (rare)
    return None, None


# ---------------------------------------------------------------------------
# Source 2 : FINESS
# ---------------------------------------------------------------------------

# TELLUX FIX 2026-04-24 : conversion Lambert 93 (EPSG:2154) vers WGS84 en Python pur.
# Necessaire car le CSV FINESS geolocalise expose les coordonnees en Lambert 93
# ("EPSG:2154 RGF93 / Lambert-93 (Metropole)" dans la colonne source). Formules IGN
# NTG-71 / ALG0004. Sans dependance externe (pas de pyproj).
def _lambert93_to_wgs84(x: float, y: float) -> tuple[float, float]:
    """Convertit (x, y) Lambert 93 en (lon, lat) WGS84, en degres decimaux.

    Constantes Lambert 93 (IGN, ellipsoide GRS80) :
      n  = 0.7256077650
      c  = 11754255.4261
      xs = 700000.0
      ys = 12655612.0499
      lambda_0 = 3 deg E
      e  = 0.081819191042816  (premiere excentricite GRS80)
    """
    import math
    n = 0.7256077650532670
    c = 11754255.4261
    xs = 700000.0
    ys = 12655612.0499
    lambda_0 = math.radians(3.0)
    e = 0.081819191042816

    dx = x - xs
    dy = y - ys
    R = math.sqrt(dx * dx + dy * dy)
    gamma = math.atan2(dx, -dy)
    lon = gamma / n + lambda_0
    L = -math.log(R / c) / n

    # Inverse de la latitude isometrique : iteration de type Mercator.
    phi = 2.0 * math.atan(math.exp(L)) - math.pi / 2
    for _ in range(10):
        esin = e * math.sin(phi)
        phi = 2.0 * math.atan(
            math.exp(L) * ((1.0 + esin) / (1.0 - esin)) ** (e / 2.0)
        ) - math.pi / 2

    return math.degrees(lon), math.degrees(phi)


def download_finess() -> Iterator[Feature]:
    """Telechargement CSV FINESS geolocalise, filtrage streaming sur Corse.

    TELLUX FIX 2026-04-24 : refonte de la fonction.
    Changements :
      1. Selectionne la ressource CSV dont le titre contient "geolocalis"
         (cs1100507) plutot que le premier CSV trouve (cs1100502 sans geoloc).
      2. Parser POSITIONNEL : le CSV FINESS n'a PAS de ligne d'en-tete. La
         ligne 1 est une meta-donnee "finess;etalab;<version>;<date>". Les
         donnees commencent ligne 2 avec 2 types d'enregistrements joints
         par nofinesset : "structureet" (32 colonnes) et "geolocalisation"
         (6 colonnes). Le precedent csv.DictReader prenait la ligne meta
         comme header et produisait des cles non exploitables.
      3. Join en memoire entre structureet et geolocalisation par nofinesset.
      4. Conversion Lambert 93 -> WGS84 via _lambert93_to_wgs84(), les coords
         sont en EPSG:2154 d'apres la colonne source FINESS.
    Invariants preserves : MAPPING_FINESS, bornes Corse, schema Feature en
    sortie, gestion des rejets (Feature avec rejection_reason).
    """
    LOG.info("FINESS : recherche de l'URL de ressource via API data.gouv.fr")
    resp = http_get(URL_API_DATA_GOUV.format(slug=DATAGOUV_DATASET_FINESS))
    payload = resp.json()
    resources = [
        r for r in payload.get("resources", [])
        if r.get("format", "").lower() in ("csv",) and r.get("url")
    ]
    if not resources:
        raise RuntimeError("FINESS : aucune ressource CSV trouvee dans data.gouv.fr")

    # TELLUX FIX 2026-04-24 : preferer la ressource "geolocalises" (cs1100507)
    # qui inclut les lignes geolocalisation. Le CSV non geolocalise (cs1100502)
    # ne contient que structureet, sans coordonnees. Attention : le titre
    # data.gouv.fr contient "geolocalises" avec accents ("geolocalises" en NFC
    # unicode). On normalise NFD puis on strippe les diacritiques pour rendre
    # le match robuste.
    import unicodedata

    def _geoloc_marker(title: str | None) -> bool:
        if not title:
            return False
        n = unicodedata.normalize("NFD", title).encode("ascii", "ignore").decode("ascii").lower()
        return "geolocalis" in n

    def _pref(r: dict) -> tuple:
        is_geoloc = _geoloc_marker(r.get("title"))
        last = r.get("last_modified") or r.get("created_at") or ""
        # Tri decroissant par (is_geoloc, last_modified).
        return (1 if is_geoloc else 0, last)

    resources.sort(key=_pref, reverse=True)
    url = resources[0]["url"]
    is_geoloc = _geoloc_marker(resources[0].get("title"))
    LOG.info("FINESS : telechargement %s (geolocalise=%s)", url, is_geoloc)
    if not is_geoloc:
        LOG.warning(
            "FINESS : ressource geolocalisee absente, fallback sur CSV sans "
            "coordonnees. Les features seront toutes rejetees no_coordinates."
        )

    # TELLUX FIX 2026-04-24 : charger le contenu en memoire plutot que streamer.
    # Le fichier fait ~45 Mo en ISO-8859-1, tient en memoire sans probleme.
    # resp.iter_lines(decode_unicode=True) en streaming s'est revele peu fiable :
    # certaines lignes geolocalisation n'etaient pas parsees correctement en
    # pratique (symptome : les medico-sociaux mappes sortaient tous rejetes
    # no_coordinates alors que leur geoloc existait bien dans le fichier).
    resp = http_get(url)  # pas stream=True
    resp.encoding = "iso-8859-1"
    lines = resp.text.splitlines()

    structures: dict[str, list[str]] = {}
    geolocs: dict[str, tuple[float, float, str]] = {}
    count_total = 0
    count_corse_struct = 0
    first_line = True
    for raw_line in lines:
        if raw_line is None:
            continue
        if first_line:
            # Ligne 1 = metadata "finess;etalab;<version>;<date>".
            LOG.debug("FINESS : ligne meta = %s", raw_line.strip()[:120])
            first_line = False
            continue
        cols = raw_line.rstrip("\r\n").split(";")
        if not cols:
            continue
        rec_type = cols[0]
        count_total += 1
        if rec_type == "structureet":
            # Schema positionnel structureet (32 colonnes).
            # [ 1] nofinesset
            # [12] commune (3 derniers chiffres du code INSEE)
            # [13] departement
            # [18] categetab
            if len(cols) < 19:
                continue
            dept = cols[13].strip()
            if dept not in DEPT_CORSE_VARIANTS:
                continue
            count_corse_struct += 1
            structures[cols[1].strip()] = cols
        elif rec_type == "geolocalisation":
            # Schema positionnel geolocalisation (6 colonnes).
            # [1] nofinesset  [2] x  [3] y  [4] source+projection  [5] date
            if len(cols) < 4:
                continue
            finess_id = cols[1].strip()
            try:
                gx = float(str(cols[2]).replace(",", "."))
                gy = float(str(cols[3]).replace(",", "."))
            except (ValueError, IndexError):
                continue
            srcproj = cols[4] if len(cols) > 4 else ""
            geolocs[finess_id] = (gx, gy, srcproj)

    LOG.info(
        "FINESS : %d lignes lues, %d structureet Corse, %d geolocs totales.",
        count_total, count_corse_struct, len(geolocs),
    )

    for finess_id, cols in structures.items():
        feat = _normalize_finess_row(cols, geolocs.get(finess_id))
        if feat is not None:
            yield feat


def _normalize_finess_row(cols: list[str], geoloc: tuple[float, float, str] | None) -> Feature | None:
    """Normalise une ligne structureet FINESS (32 colonnes positionnelles).

    TELLUX FIX 2026-04-24 : refonte. Parser POSITIONNEL. La precedente version
    utilisait des .get() sur un dict (alimente par csv.DictReader aux cles
    invalides). Schema valide en direct sur etalab-cs1100507 (2026-03-11).
    Invariants : MAPPING_FINESS, schema de sortie Feature, rejection_reason
    sont inchanges.

    Colonnes utilisees :
      [ 1] nofinesset        [12] commune (3 chiffres)
      [ 3] rs (court)        [13] departement (2 chiffres)
      [ 4] rslongue          [15] ligneacheminement (CP + ville)
      [ 8] typvoie           [18] categetab
      [ 9] voie              [19] libcategetab
      [11] lieuditbp
    """
    cat_code = cols[18].strip() if len(cols) > 18 else ""
    if cat_code not in MAPPING_FINESS:
        # non pertinent pour le dispositif sensible
        LOG.debug("FINESS : code categorie ignore : %s", cat_code)
        return None
    sous_cat = MAPPING_FINESS[cat_code]

    finess = cols[1].strip() if len(cols) > 1 else ""
    nom = clean_str(cols[4]) or clean_str(cols[3])  # rslongue prioritaire
    if not finess or not nom:
        return None

    numvoie = clean_str(cols[7]) if len(cols) > 7 else None
    typvoie = clean_str(cols[8]) if len(cols) > 8 else None
    voie = clean_str(cols[9]) if len(cols) > 9 else None
    lieuditbp = clean_str(cols[11]) if len(cols) > 11 else None
    adresse = " ".join(filter(None, [numvoie, typvoie, voie, lieuditbp])) or None

    # ligneacheminement : "20090 AJACCIO" ; on extrait CP et commune textuelle.
    ligneach = clean_str(cols[15]) if len(cols) > 15 else None
    code_postal = None
    commune = None
    if ligneach:
        parts = ligneach.split(" ", 1)
        if parts and parts[0].isdigit() and len(parts[0]) == 5:
            code_postal = parts[0]
            commune = parts[1].strip() if len(parts) > 1 else None
        else:
            commune = ligneach

    # Code INSEE commune reconstitue : dept (2 chars) + commune (3 chiffres).
    dept = cols[13].strip() if len(cols) > 13 else ""
    commune_code3 = cols[12].strip() if len(cols) > 12 else ""
    code_insee = None
    if dept in ("2A", "2B") and commune_code3.isdigit() and len(commune_code3) == 3:
        code_insee = dept + commune_code3
    elif dept.isdigit() and commune_code3.isdigit() and len(commune_code3) == 3:
        # Metropole hors Corse, peu utile pour Tellux mais structurellement valide.
        code_insee = dept + commune_code3

    # Geolocalisation : Lambert 93 depuis la ligne geolocalisation correspondante.
    if geoloc is None:
        return Feature(
            lon=0.0, lat=0.0, id=finess, nom=nom,
            categorie="medico-social", sous_categorie=sous_cat,
            adresse=adresse, code_postal=code_postal,
            commune=commune, code_insee=code_insee,
            secteur=None, source="finess",
            rejection_reason="no_coordinates",
        )

    gx, gy, srcproj = geoloc
    # Detection projection : on convertit si Lambert 93, on prend direct si WGS84.
    use_lambert = True
    if "WGS84" in (srcproj or "").upper() or "EPSG:4326" in (srcproj or ""):
        use_lambert = False
    # Heuristique de securite : valeurs absolues > 180 en lon => forcement Lambert.
    if abs(gx) <= 180 and abs(gy) <= 90:
        use_lambert = False

    if use_lambert:
        try:
            lon, lat = _lambert93_to_wgs84(gx, gy)
        except Exception as exc:  # pragma: no cover
            LOG.warning("FINESS %s : echec conversion Lambert 93 -> WGS84 : %s", finess, exc)
            return Feature(
                lon=0.0, lat=0.0, id=finess, nom=nom,
                categorie="medico-social", sous_categorie=sous_cat,
                adresse=adresse, code_postal=code_postal,
                commune=commune, code_insee=code_insee,
                secteur=None, source="finess",
                rejection_reason="coords_not_wgs84",
            )
    else:
        lon, lat = gx, gy

    return Feature(
        lon=lon, lat=lat, id=finess, nom=nom,
        categorie="medico-social", sous_categorie=sous_cat,
        adresse=adresse, code_postal=code_postal,
        commune=commune, code_insee=code_insee,
        secteur=None, source="finess",
    )


def _to_float(x) -> float | None:
    if x is None or x == "":
        return None
    try:
        # FINESS peut utiliser la virgule decimale.
        return float(str(x).replace(",", "."))
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Source 3 : EAJE POI
# ---------------------------------------------------------------------------

# TELLUX FIX 2026-04-24 : la source "poi-eaje-3" configuree initialement dans ce
# script est en realite un dataset departemental de l'Ain (168 features, zero en
# Corse). Apres recherche, il n'existe pas de dataset EAJE national geolocalise
# ouvert sur data.gouv.fr ni sur data.caf.fr : les portails CAF publient des
# statistiques agregees par territoire (nbpla_pe_*) mais aucune liste d'etablis-
# sements geolocalises. Les EAJE de Corse-du-Sud (2A) et Haute-Corse (2B) ne
# sont pas publies sur data.gouv.fr a ce jour.
# Plutot que d'emettre une RuntimeError qui romprait le pipeline global, on
# retourne un iterateur vide et on loggue un avertissement clair. Le fichier
# eaje.geojson produit en sortie sera une FeatureCollection vide bien formee
# avec des metadonnees explicitant l'absence de source, pour que le bloc
# Etablissements sensibles de mairies.html puisse charger les 3 GeoJSON
# uniformement sans if/else sur la disponibilite.
# Voir docs/tickets/EAJE-CORSE-001.md pour les pistes alternatives a explorer
# (CAF Corse direct, OpenStreetMap amenity=kindergarten, contact ARS Corse).
def download_eaje() -> Iterator[Feature]:
    """Produit un iterateur vide (aucune source EAJE nationale geolocalisee).

    TELLUX FIX 2026-04-24 : voir commentaire de bloc ci-dessus. Aucun fetch
    reseau. Le GeoJSON de sortie sera vide mais bien forme.
    """
    LOG.warning(
        "EAJE : aucune source nationale geolocalisee disponible en open data "
        "(data.gouv.fr, data.caf.fr). La Corse-du-Sud et la Haute-Corse ne "
        "publient pas de dataset EAJE. Le fichier de sortie sera vide. "
        "Voir docs/tickets/EAJE-CORSE-001.md pour les pistes alternatives."
    )
    return
    yield  # pragma: no cover  rend la fonction un generator


def _download_eaje_csv(url: str) -> Iterator[Feature]:
    LOG.info("EAJE CSV : telechargement %s", url)
    resp = http_get(url)
    resp.encoding = resp.apparent_encoding or "utf-8"
    reader = csv.DictReader(io.StringIO(resp.text), delimiter=";")
    for row in reader:
        dept = str(row.get("departement") or row.get("code_departement") or "").strip()
        if dept not in DEPT_CORSE_VARIANTS:
            continue
        feat = _normalize_eaje_row_csv(row)
        if feat is not None:
            yield feat


def _normalize_eaje_feature(feat: dict) -> Feature | None:
    props = feat.get("properties", {}) or {}
    geom = feat.get("geometry") or {}
    coords = geom.get("coordinates") or [None, None]
    if not (isinstance(coords, list) and len(coords) >= 2):
        return None
    lon, lat = coords[0], coords[1]
    return _build_eaje(props, lon, lat)


def _normalize_eaje_row_csv(row: dict) -> Feature | None:
    lon = _to_float(row.get("longitude") or row.get("lon"))
    lat = _to_float(row.get("latitude") or row.get("lat"))
    return _build_eaje(row, lon, lat)


def _build_eaje(props: dict, lon, lat) -> Feature | None:
    nom = clean_str(props.get("nom") or props.get("nom_structure"))
    if not nom:
        return None
    type_struct = clean_str(props.get("type_structure") or props.get("type"))
    sous_cat = MAPPING_EAJE.get(type_struct or "", "autre")
    eaje_id = clean_str(props.get("id") or props.get("identifiant"))
    if not eaje_id:
        base_commune = clean_str(props.get("code_insee") or props.get("commune") or "")
        eaje_id = f"eaje_{nom[:40].replace(' ', '_')}_{base_commune}"
    adresse = clean_str(props.get("adresse") or props.get("voie"))
    cp = clean_str(props.get("code_postal"))
    commune = clean_str(props.get("commune") or props.get("libelle_commune"))
    code_insee = clean_str(props.get("code_insee") or props.get("codgeo"))
    if lon is None or lat is None:
        return Feature(
            lon=0.0, lat=0.0, id=eaje_id, nom=nom,
            categorie="petite-enfance", sous_categorie=sous_cat,
            adresse=adresse, code_postal=cp, commune=commune, code_insee=code_insee,
            secteur=None, source="eaje_caf",
            rejection_reason="no_coordinates",
        )
    return Feature(
        lon=_to_float(lon) or 0.0, lat=_to_float(lat) or 0.0,
        id=eaje_id, nom=nom,
        categorie="petite-enfance", sous_categorie=sous_cat,
        adresse=adresse, code_postal=cp, commune=commune, code_insee=code_insee,
        secteur=None, source="eaje_caf",
    )


# ---------------------------------------------------------------------------
# Ecriture GeoJSON
# ---------------------------------------------------------------------------

def write_geojson(path: str, features: list[Feature], metadata: dict | None = None) -> None:
    fc = {
        "type": "FeatureCollection",
        "features": [f.to_geojson() for f in features],
    }
    if metadata:
        fc["metadata"] = metadata
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fc, fh, ensure_ascii=False, indent=0, separators=(",", ":"))
    LOG.info("Ecrit : %s (%d features)", path, len(features))


# ---------------------------------------------------------------------------
# Statistiques
# ---------------------------------------------------------------------------

def compute_stats(
    enseignement: list[Feature],
    medicosocial: list[Feature],
    petite_enfance: list[Feature],
    rejected: list[Feature],
) -> dict:
    def by_commune(feats: list[Feature]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in feats:
            key = f.code_insee or f.commune or "inconnu"
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: -kv[1]))

    def by_sous_cat(feats: list[Feature]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for f in feats:
            counts[f.sous_categorie] = counts.get(f.sous_categorie, 0) + 1
        return dict(sorted(counts.items(), key=lambda kv: -kv[1]))

    return {
        "date_extraction": DATE_EXTRACTION,
        "annuaire_education": {
            "total": len(enseignement),
            "par_sous_categorie": by_sous_cat(enseignement),
            "top_10_communes": dict(list(by_commune(enseignement).items())[:10]),
        },
        "finess": {
            "total": len(medicosocial),
            "par_sous_categorie": by_sous_cat(medicosocial),
            "top_10_communes": dict(list(by_commune(medicosocial).items())[:10]),
        },
        "eaje_caf": {
            "total": len(petite_enfance),
            "par_sous_categorie": by_sous_cat(petite_enfance),
            "top_10_communes": dict(list(by_commune(petite_enfance).items())[:10]),
        },
        "rejets": {
            "total": len(rejected),
            "par_source": {
                "annuaire_education": sum(1 for f in rejected if f.source == "annuaire_education"),
                "finess": sum(1 for f in rejected if f.source == "finess"),
                "eaje_caf": sum(1 for f in rejected if f.source == "eaje_caf"),
            },
            "par_raison": {
                r: sum(1 for f in rejected if f.rejection_reason == r)
                for r in sorted({f.rejection_reason for f in rejected if f.rejection_reason})
            } if rejected else {},
        },
    }


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def split_accepted_rejected(features: Iterable[Feature]) -> tuple[list[Feature], list[Feature]]:
    accepted, rejected = [], []
    for f in features:
        if f.rejection_reason is not None:
            rejected.append(f)
            continue
        if not is_in_corse_bounds(f.lon, f.lat):
            f.rejection_reason = "out_of_corse_bounds"
            rejected.append(f)
            continue
        accepted.append(f)
    return accepted, rejected


def run(source: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    enseignement_all: list[Feature] = []
    medicosocial_all: list[Feature] = []
    petite_enfance_all: list[Feature] = []
    rejected_all: list[Feature] = []

    if source in ("annuaire", "all"):
        try:
            feats = list(download_annuaire_education())
            accepted, rejected = split_accepted_rejected(feats)
            enseignement_all = accepted
            rejected_all.extend(rejected)
        except Exception as exc:
            LOG.error("Annuaire Education : echec %s", exc)

    if source in ("finess", "all"):
        try:
            feats = list(download_finess())
            accepted, rejected = split_accepted_rejected(feats)
            medicosocial_all = accepted
            rejected_all.extend(rejected)
        except Exception as exc:
            LOG.error("FINESS : echec %s", exc)

    if source in ("eaje", "all"):
        try:
            feats = list(download_eaje())
            accepted, rejected = split_accepted_rejected(feats)
            petite_enfance_all = accepted
            rejected_all.extend(rejected)
        except Exception as exc:
            LOG.error("EAJE : echec %s", exc)

    meta = {
        "generator": "tellux build_etablissements_corse.py v1.0",
        "date_extraction": DATE_EXTRACTION,
        "licence": "Etalab 2.0 (sources)",
        "projection": "EPSG:4326",
        "attribution": (
            "Annuaire Education : ministere de l'Education nationale. "
            "FINESS : DREES. EAJE : CNAF."
        ),
    }

    if source in ("annuaire", "all"):
        write_geojson(
            os.path.join(output_dir, "etablissements_enseignement_corse.geojson"),
            enseignement_all, metadata={**meta, "source": "annuaire_education"},
        )
    if source in ("finess", "all"):
        write_geojson(
            os.path.join(output_dir, "etablissements_medicosocial_corse.geojson"),
            medicosocial_all, metadata={**meta, "source": "finess"},
        )
    if source in ("eaje", "all"):
        # TELLUX FIX 2026-04-24 : les metadonnees EAJE documentent explicitement
        # l'absence de source nationale geolocalisee. Le fichier de sortie est
        # une FeatureCollection potentiellement vide mais bien formee.
        eaje_meta = {
            **meta,
            "source": "eaje_caf",
            "status": (
                "empty_no_source"
                if not petite_enfance_all
                else "populated"
            ),
            "coverage_note": (
                "Aucune source nationale geolocalisee d'etablissements d'accueil "
                "du jeune enfant (EAJE) n'est disponible en open data a la date "
                "d'extraction. data.gouv.fr ne publie que des jeux departementaux "
                "(Ain, Aude, Finistere, Loire-Atlantique, Mayenne, Saint-Denis). "
                "data.caf.fr publie des statistiques agregees (nombre de places "
                "par territoire, slug nbpla_pe_*) mais pas de liste d'etablisse-"
                "ments geolocalises. Les EAJE de Corse-du-Sud (2A) et Haute-Corse "
                "(2B) ne sont pas publies a ce jour. Voir ticket EAJE-CORSE-001 "
                "pour les pistes alternatives a explorer."
            ),
            "ticket": "EAJE-CORSE-001",
        }
        write_geojson(
            os.path.join(output_dir, "etablissements_petite_enfance_corse.geojson"),
            petite_enfance_all, metadata=eaje_meta,
        )
    if rejected_all:
        write_geojson(
            os.path.join(output_dir, "features_rejected.geojson"),
            rejected_all, metadata={**meta, "source": "rejets"},
        )

    stats = compute_stats(enseignement_all, medicosocial_all, petite_enfance_all, rejected_all)
    with open(os.path.join(output_dir, "build_stats.json"), "w", encoding="utf-8") as fh:
        json.dump(stats, fh, ensure_ascii=False, indent=2)
    LOG.info("Stats ecrites : %s", os.path.join(output_dir, "build_stats.json"))
    LOG.info("Resume : enseignement=%d, medicosocial=%d, petite_enfance=%d, rejets=%d",
             len(enseignement_all), len(medicosocial_all), len(petite_enfance_all), len(rejected_all))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1] if __doc__ else "")
    parser.add_argument("--source", choices=["annuaire", "finess", "eaje", "all"], default="all",
                        help="Source a rebuild. Par defaut : all.")
    parser.add_argument("--output", default="./output",
                        help="Dossier de sortie. Par defaut : ./output")
    parser.add_argument("--verbose", action="store_true", help="Journalisation DEBUG.")
    args = parser.parse_args(argv)
    setup_logging(args.verbose)
    try:
        run(args.source, args.output)
        return 0
    except KeyboardInterrupt:
        LOG.warning("Interrompu par l'utilisateur.")
        return 130
    except Exception as exc:
        LOG.exception("Echec global : %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
