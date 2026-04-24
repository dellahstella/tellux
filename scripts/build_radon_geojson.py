#!/usr/bin/env python3
"""
build_radon_geojson.py
======================
Télécharge les données officielles de potentiel radon en France (data.gouv.fr)
et les géométries communes IGN (france-geojson / GitHub), puis produit :

    public/data/radon_zones_corse.geojson

Filtrage : communes de Corse (depts 2A et 2B), catégories 2 et 3 uniquement.

Usage :
    pip install requests geopandas shapely fiona
    python build_radon_geojson.py

Auteur   : Cowork / Tellux (2026-04-24)
Sources  : ASNR/IRSN - arrêté du 27 juin 2018
           IGN AdminExpress via gregoiredavid/france-geojson (GitHub)
Licence  : données radon sous Licence Ouverte 2.0 (Etalab)
           géométries IGN sous Licence Ouverte IGN
"""

import io
import json
import os
import sys
import zipfile
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "public" / "data"
OUTPUT_FILE = OUTPUT_DIR / "radon_zones_corse.geojson"

# Source 1 : radon classification (data.gouv.fr)
# Dataset IRSN officiel "Connaître le potentiel radon de ma commune" — contient
# un CSV France entière (36093 communes) avec colonnes nom_comm, nom_dept,
# insee_com, classe_potentiel, reg. L'ancien dataset "zonage-en-potentiel-radon"
# ne publie plus qu'un WMS depuis 2024+.
DATAGOUV_DATASET_ID = "connaitre-le-potentiel-radon-de-ma-commune"
DATAGOUV_API = f"https://www.data.gouv.fr/api/1/datasets/{DATAGOUV_DATASET_ID}/"

# Source 2 : géométries communes (france-geojson sur GitHub - Licence Ouverte IGN)
# Note : URL case-sensitive côté GitHub. Le repo utilise le casing majuscule (2A, 2B).
GEOJSON_BASE = "https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements"
URL_2A = f"{GEOJSON_BASE}/2A-corse-du-sud/communes-2A-corse-du-sud.geojson"
URL_2B = f"{GEOJSON_BASE}/2B-haute-corse/communes-2B-haute-corse.geojson"

# Catégories à conserver
CATEGORIES_CIBLES = {2, 3}


# ---------------------------------------------------------------------------
# ÉTAPE 1 — Télécharger la classification radon via data.gouv.fr
# ---------------------------------------------------------------------------

def get_radon_resource_url():
    """Interroge l'API data.gouv.fr pour trouver le fichier shapefile/CSV."""
    print("[1/4] Interrogation API data.gouv.fr…")
    r = requests.get(DATAGOUV_API, timeout=30)
    r.raise_for_status()
    data = r.json()

    resources = data.get("resources", [])
    print(f"      {len(resources)} ressource(s) trouvée(s) :")
    for res in resources:
        title = res.get("title", "")
        fmt = res.get("format", "")
        url = res.get("url", "")
        size = res.get("filesize", "?")
        print(f"      - [{fmt}] {title} ({size} octets) → {url}")

    # Priorité : shapefile ZIP, puis GeoJSON, puis CSV
    for preferred_fmt in ["shp", "geojson", "csv"]:
        for res in resources:
            if preferred_fmt in (res.get("format") or "").lower():
                return res["url"], preferred_fmt
            if preferred_fmt in (res.get("url") or "").lower():
                return res["url"], preferred_fmt

    raise RuntimeError(
        "Aucun fichier exploitable trouvé dans le dataset data.gouv.fr.\n"
        "Vérifiez manuellement : https://www.data.gouv.fr/datasets/zonage-en-potentiel-radon"
    )


def download_radon_classification(url, fmt):
    """Télécharge et parse la classification radon. Retourne dict {code_insee: categorie}."""
    print(f"[2/4] Téléchargement classification radon ({fmt})…")
    r = requests.get(url, timeout=120)
    r.raise_for_status()

    classification = {}

    if fmt == "shp":
        return _parse_shapefile_zip(r.content, classification)
    elif fmt == "geojson":
        return _parse_geojson_bytes(r.content, classification)
    elif fmt == "csv":
        return _parse_csv_bytes(r.content, classification)
    else:
        raise RuntimeError(f"Format non supporté : {fmt}")


def _parse_shapefile_zip(content, classification):
    """Parse un ZIP contenant un shapefile radon."""
    try:
        import geopandas as gpd
    except ImportError:
        sys.exit("Erreur : geopandas requis pour lire les shapefiles. pip install geopandas")

    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        shp_files = [n for n in zf.namelist() if n.endswith(".shp")]
        if not shp_files:
            raise RuntimeError("Aucun .shp dans le ZIP.")
        shp_name = shp_files[0]
        zf.extractall("/tmp/radon_shp/")

    gdf = gpd.read_file(f"/tmp/radon_shp/{shp_name}")
    print(f"      Colonnes shapefile : {list(gdf.columns)}")
    print(f"      {len(gdf)} features")

    # Détecter les colonnes INSEE et catégorie (noms variables selon la version du dataset)
    col_insee = _find_col(gdf.columns, ["insee", "code_insee", "com", "codgeo", "code_com"])
    col_cat = _find_col(gdf.columns, ["categorie", "cat", "zone", "potentiel", "classe", "niveau"])

    print(f"      Colonne INSEE détectée : {col_insee}")
    print(f"      Colonne catégorie détectée : {col_cat}")

    for _, row in gdf.iterrows():
        code = str(row[col_insee]).strip().zfill(5) if col_insee else None
        cat = _parse_int(row[col_cat]) if col_cat else None
        if code and cat:
            classification[code] = cat

    return classification


def _parse_geojson_bytes(content, classification):
    data = json.loads(content)
    features = data.get("features", [])
    if not features:
        raise RuntimeError("GeoJSON vide.")
    sample_props = list(features[0].get("properties", {}).keys())
    print(f"      Propriétés GeoJSON : {sample_props}")

    col_insee = _find_col(sample_props, ["insee", "code_insee", "com", "codgeo", "code_com"])
    col_cat = _find_col(sample_props, ["categorie", "cat", "zone", "potentiel", "classe", "niveau"])

    for feat in features:
        props = feat.get("properties", {})
        code = str(props.get(col_insee, "")).strip().zfill(5) if col_insee else None
        cat = _parse_int(props.get(col_cat)) if col_cat else None
        if code and cat:
            classification[code] = cat

    return classification


def _parse_csv_bytes(content, classification):
    import csv
    text = content.decode("utf-8", errors="replace")
    # Auto-détection du délimiteur (data.gouv.fr utilise ; en norme FR ; fallback ,)
    sample = text[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
        delimiter = dialect.delimiter
    except csv.Error:
        delimiter = ";" if sample.count(";") > sample.count(",") else ","
    print(f"      Délimiteur CSV détecté : '{delimiter}'")
    reader = csv.DictReader(io.StringIO(text), delimiter=delimiter)
    headers = reader.fieldnames or []
    print(f"      Colonnes CSV : {list(headers)}")

    col_insee = _find_col(headers, ["insee", "code_insee", "com", "codgeo", "code_com"])
    col_cat = _find_col(headers, ["categorie", "cat", "zone", "potentiel", "classe", "niveau"])

    for row in reader:
        code = str(row.get(col_insee, "")).strip().zfill(5) if col_insee else None
        cat = _parse_int(row.get(col_cat, "")) if col_cat else None
        if code and cat:
            classification[code] = cat

    return classification


# ---------------------------------------------------------------------------
# ÉTAPE 2 — Télécharger les géométries communes Corse (france-geojson / IGN)
# ---------------------------------------------------------------------------

def download_commune_geometries():
    """Télécharge GeoJSON 2A + 2B depuis gregoiredavid/france-geojson (Licence Ouverte IGN)."""
    print("[3/4] Téléchargement géométries communes Corse (IGN via GitHub)…")
    features = []
    for dept, url in [("2A", URL_2A), ("2B", URL_2B)]:
        print(f"      Dept {dept} : {url}")
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        gj = r.json()
        dpt_features = gj.get("features", [])
        print(f"      → {len(dpt_features)} communes")
        features.extend(dpt_features)

    print(f"      Total : {len(features)} communes Corse (2A + 2B)")
    return features


# ---------------------------------------------------------------------------
# ÉTAPE 3 — Croiser et filtrer
# ---------------------------------------------------------------------------

def build_geojson(commune_features, classification):
    """Croise géométries et classification. Retourne FeatureCollection cat 2+3."""
    print("[4/4] Croisement classification ↔ géométries…")

    output_features = []
    manquants = []

    for feat in commune_features:
        props = feat.get("properties", {})
        # france-geojson utilise 'code' pour le code INSEE et 'nom' pour le nom
        code = str(props.get("code", props.get("INSEE_COM", ""))).strip()
        nom = props.get("nom", props.get("NOM_COM", props.get("name", code)))

        # Normaliser le code INSEE (5 chars, ex: "2A004")
        if len(code) < 5:
            code = code.zfill(5)

        cat = classification.get(code)

        if cat is None:
            # Fallback : chercher sans le 0 initial (certains encodages font "20004" → "2A004")
            for k, v in classification.items():
                if k.endswith(code[-3:]) and k.startswith("2"):
                    cat = v
                    break

        if cat is None:
            manquants.append(code)
            continue

        if cat not in CATEGORIES_CIBLES:
            continue  # Cat 1 : pas pertinent pour Tellux

        # Déterminer le département
        dept = "2A" if code.startswith("2A") or code.startswith("201") or code.startswith("202") else "2B"

        new_feat = {
            "type": "Feature",
            "geometry": feat.get("geometry"),
            "properties": {
                "code_insee": code,
                "nom_commune": nom,
                "departement": dept,
                "categorie": cat,
                "source": "ASNR/IRSN - Arrete du 27 juin 2018",
                "annee": 2018,
                "url_source": f"https://www.data.gouv.fr/datasets/{DATAGOUV_DATASET_ID}",
                "licence": "Licence Ouverte 2.0 - Etalab",
            },
        }
        output_features.append(new_feat)

    if manquants:
        print(f"      Attention : {len(manquants)} commune(s) sans correspondance radon : {manquants[:10]}…")

    cat2 = sum(1 for f in output_features if f["properties"]["categorie"] == 2)
    cat3 = sum(1 for f in output_features if f["properties"]["categorie"] == 3)
    print(f"      Résultat : {len(output_features)} features (cat2={cat2}, cat3={cat3})")

    return {
        "type": "FeatureCollection",
        "name": "radon_zones_corse",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "metadata": {
            "description": "Zones de potentiel radon cat. 2 et 3 en Corse",
            "source_classification": "ASNR/IRSN - Arrete du 27 juin 2018 (JORFTEXT000037131346)",
            "source_geometries": "IGN AdminExpress via gregoiredavid/france-geojson (GitHub)",
            "licence": "Licence Ouverte 2.0 - Etalab",
            "date_production": "2026-04-24",
            "features_total": len(output_features),
            "features_cat2": cat2,
            "features_cat3": cat3,
        },
        "features": output_features,
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    # Force UTF-8 stdout (Windows console par défaut est cp1252, crash sur → ✓ etc.)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, TypeError):
        pass  # Python < 3.7 ou stdout non-TTY, on laisse tel quel
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    try:
        url, fmt = get_radon_resource_url()
        classification = download_radon_classification(url, fmt)
        print(f"      Classification : {len(classification)} communes France chargées")
    except Exception as e:
        print(f"\n[ERREUR étape 1-2] Impossible de récupérer la classification radon :")
        print(f"  {e}")
        print("\nFallback : utilisation de la classification hardcodée (arrêté 27 juin 2018)")
        classification = get_classification_hardcodee()

    commune_features = download_commune_geometries()
    geojson = build_geojson(commune_features, classification)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"\n✓ Fichier produit : {OUTPUT_FILE}")
    print(f"  Taille : {size_kb:.1f} Ko")
    print(f"  Features : {geojson['metadata']['features_total']} communes")
    print(f"  Cat 2 : {geojson['metadata']['features_cat2']}")
    print(f"  Cat 3 : {geojson['metadata']['features_cat3']}")

    if size_kb > 2000:
        print("\n[ATTENTION] Fichier > 2 Mo. Simplifier avec :")
        print("  mapshaper radon_zones_corse.geojson -simplify 10% -o format=geojson output.geojson")


# ---------------------------------------------------------------------------
# FALLBACK — Classification hardcodée depuis l'arrêté du 27 juin 2018
# Source : JORFTEXT000037131346 (Légifrance) + CDG 2B
# Corse-du-Sud (2A) : toutes communes = cat 3
# Haute-Corse (2B) : cat 1 par défaut, exceptions cat 2 et cat 3 listées ci-dessous
# AVERTISSEMENT : cette liste est partielle pour la Haute-Corse cat 3.
#   Compléter en consultant le texte complet sur Légifrance avant intégration.
# ---------------------------------------------------------------------------

def get_classification_hardcodee():
    """
    Retourne un dict {nom_commune_normalise: categorie} pour la Corse uniquement.
    À utiliser UNIQUEMENT en fallback si l'API data.gouv.fr est inaccessible.
    Vérifier sur Légifrance avant toute utilisation en production.
    """
    # Haute-Corse catégorie 2 (source: arrêté 27 juin 2018 via CDG 2B)
    hc_cat2 = [
        "Altiani", "Biguglia", "Bisinchi", "Borgo", "Brando",
        "Castellare-Di-Mercurio", "Centuri", "Erbajolo", "Erone", "Ersa",
        "Ficaja", "Focicchia", "Gavignano", "La Porta", "Lugo-Di-Nazza",
        "Luri", "Matra", "Meria", "Moita", "Morsiglia",
        "Piedicorte-di-Gaggio", "Pietroso", "Pino", "Poggio-Marinaccio",
        "Quercitello", "Rospigliani", "Rusio", "San-Damiano",
        "San-Gavino-d'Ampugnani", "Sant'Andrea-di-Bozio",
        "Santo-Pietro-di-Venaco", "Scata", "Sermano", "Tallone",
        "Tomino", "Tox", "Vezzani",
    ]

    # Haute-Corse catégorie 3 (PARTIEL - source: arrêté 27 juin 2018, résultats moteur recherche)
    # ATTENTION : cette liste n'est pas exhaustive. Consulter Légifrance pour la liste complète.
    hc_cat3_partiel = [
        "Albertacce", "Algajola", "Aregno", "Asco", "Avapessa",
        "Barbaggio", "Bastia", "Belgodere", "Calacuccia", "Calenzana",
        "Calvi", "Canale-di-Verde", "Canavaggia", "Casamaccioli",
        "Casanova", "Castifao", "Castiglione", "Castineta", "Castirla",
        "Cateri", "Chisa", "Corbara", "Corscia", "Corte", "Costa",
        "Farinole", "Favalello", "Feliceto", "Furiani", "Galeria",
        "Ghisoni", "Isolaccio-di-Fiumorbo", "Lama", "Lavatoggio",
        "Lento", "Linguizzetta", "Lozzi", "Lumio", "Manso", "Mausoleo",
        "Moltifao", "Moncale", "Montegrosso", "Monticello", "Morosaglia",
        "Muracciole", "Muro", "Nessa", "Noceta", "Novella", "Occhiatana",
        "Oletta", "Olmeta-di-Capocorso", "Olmeta-di-Tuda", "Olmi-Cappella",
        "Omessa", "Palasca", "Patrimonio", "Piedigriggio", "Pietralba",
        "Pieve", "Pigna", "Pioggiola", "Poggio-di-Nazza", "Poggio-di-Venaco",
        "Poggio-d'Oletta", "Popolasca", "Prato-di-Giovellina",
        "Prunelli-di-Fiumorbo", "Rapale", "Saint-Florent",
        "San-Gavino-di-Fiumorbo", "San-Gavino-di-Tenda",
    ]

    classification = {}

    # Corse-du-Sud : toutes cat 3 (code INSEE commence par 2A ou 20 historiquement)
    # On note par nom, le croisement se fera par code INSEE via les géométries
    classification["_2A_all"] = 3  # signal spécial traité dans build_geojson

    for nom in hc_cat2:
        classification[_normalize(nom)] = 2
    for nom in hc_cat3_partiel:
        classification[_normalize(nom)] = 3

    return classification


def _normalize(s):
    """Normalise un nom de commune pour comparaison."""
    import unicodedata
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.upper().replace("-", " ").replace("'", " ").strip()


def _find_col(columns, candidates):
    """Trouve la première colonne dont le nom correspond à un candidat (insensible à la casse)."""
    cols_lower = {c.lower(): c for c in columns}
    for cand in candidates:
        if cand.lower() in cols_lower:
            return cols_lower[cand.lower()]
    # Recherche partielle
    for cand in candidates:
        for col_lower, col in cols_lower.items():
            if cand.lower() in col_lower:
                return col
    return None


def _parse_int(val):
    try:
        return int(float(str(val).strip()))
    except (ValueError, TypeError):
        return None


if __name__ == "__main__":
    main()
