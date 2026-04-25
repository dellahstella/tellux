#!/usr/bin/env python3
"""Build EAJE Corse GeoJSON from OpenStreetMap (Overpass API).

Source: OpenStreetMap, tags amenity=kindergarten and amenity=childcare
filtered on departments FR-2A and FR-2B via ISO3166-2 areas.

Licence: ODbL (Open Database License). Attribution mandatory:
  © OpenStreetMap contributors

Reproducibility note:
- This is the reference script for the EAJE Corse layer of mairies.html
  Fiche commune (Bloc 2 Etablissements sensibles).
- Run quarterly. OSM evolves continuously through citizen contributions.
- If feature count drops by more than 50% vs previous snapshot, do NOT
  overwrite the file without operator validation (this script does not
  enforce that, run a manual diff before committing).

Cadence: quarterly recommended (more permissive than the FINESS / Annuaire
Education scripts that run monthly).

Coverage caveat: OSM coverage of EAJE in Corsica is partial (estimated
between 25% and 50% as of April 2026). Always document the coverage_note
in the GeoJSON metadata and in the UI message of mairies.html.

Ticket: EAJE-CORSE-001 (closed by this script's first execution).

Dependencies: requests only (already in repo, no new dep).

CLI:
    python scripts/build_eaje_osm_corse.py --output public/data/corse
    python scripts/build_eaje_osm_corse.py --output /tmp --verbose
"""
import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
GEOAPI_COMMUNES_URL = "https://geo.api.gouv.fr/communes"
USER_AGENT = "TelluxCorse/1.0 (+https://tellux.pages.dev)"

# Bounds Corse, identique a build_etablissements_corse.py
BOUNDS_CORSE = {
    "lat_min": 41.3, "lat_max": 43.1,
    "lon_min": 8.5, "lon_max": 9.6,
}

# OSM elements explicitement exclus pour incoherence de tagging documentee.
# Format: { f"osm_{type}_{id}": "raison" }
# Tellux ne curate pas OSM, mais filtre les anomalies evidentes ou le tag
# amenity=kindergarten est en contradiction manifeste avec d'autres tags
# de l'element (name, description). Chaque exclusion doit etre justifiee
# et documentee dans docs/data-sources/etablissements_corse_notes.md.
EXCLUDED_OSM_IDS = {
    "osm_node_7899283685": (
        "Olmeta-di-Capocorso (2B187), tag amenity=kindergarten mais name='Mairie'. "
        "Incoherence tag amenity / name, presomption d'erreur de mapping OSM amont. "
        "Exclu jusqu'a correction (signalement OSM possible). Decision Soleil 2026-04-25."
    ),
}

OVERPASS_QUERY = """[out:json][timeout:60];
(
  area["ISO3166-2"="FR-2A"]->.corsedusud;
  area["ISO3166-2"="FR-2B"]->.hautecorse;
);
(
  node["amenity"="kindergarten"](area.corsedusud);
  node["amenity"="kindergarten"](area.hautecorse);
  way["amenity"="kindergarten"](area.corsedusud);
  way["amenity"="kindergarten"](area.hautecorse);
  relation["amenity"="kindergarten"](area.corsedusud);
  relation["amenity"="kindergarten"](area.hautecorse);
  node["amenity"="childcare"](area.corsedusud);
  node["amenity"="childcare"](area.hautecorse);
  way["amenity"="childcare"](area.corsedusud);
  way["amenity"="childcare"](area.hautecorse);
);
out center tags;
"""

# Mapping kindergarten:FR -> sous_categorie schema Tellux
MAPPING_OSM_KINDERGARTEN_FR: Dict[str, str] = {
    "creche": "creche_collective",
    "creche_collective": "creche_collective",
    "creche_familiale": "creche_familiale",
    "creche_parentale": "creche_parentale",
    "micro_creche": "micro_creche",
    "halte_garderie": "halte_garderie",
    "multi_accueil": "multi_accueil",
    "jardin_enfants": "jardin_enfants",
    "jardin_d_enfants": "jardin_enfants",
}

# Heuristique nom -> sous_categorie quand kindergarten:FR absent
NAME_HINTS = (
    ("micro-crèche", "micro_creche"),
    ("micro creche", "micro_creche"),
    ("halte-garderie", "halte_garderie"),
    ("halte garderie", "halte_garderie"),
    ("multi accueil", "multi_accueil"),
    ("multi-accueil", "multi_accueil"),
    ("jardin d'enfants", "jardin_enfants"),
    ("jardin d enfants", "jardin_enfants"),
    ("jardin enfants", "jardin_enfants"),
)


def fetch_overpass(verbose: bool = False) -> List[Dict[str, Any]]:
    """POST the Overpass query and return the list of OSM elements."""
    if verbose:
        print(f"[overpass] POST {OVERPASS_URL} (timeout 90s)")
    r = requests.post(
        OVERPASS_URL,
        data={"data": OVERPASS_QUERY},
        headers={"User-Agent": USER_AGENT},
        timeout=90,
    )
    if verbose:
        print(f"[overpass] HTTP {r.status_code} ({len(r.content)} bytes)")
    r.raise_for_status()
    data = r.json()
    return data.get("elements", []) or []


def deduce_sous_categorie(tags: Dict[str, Any], amenity: str) -> str:
    """Map OSM tags to Tellux sous_categorie (creche_collective default)."""
    fr_tag = tags.get("kindergarten:FR")
    if fr_tag:
        return MAPPING_OSM_KINDERGARTEN_FR.get(str(fr_tag).lower().strip(), "autre")
    name = (tags.get("name") or "").lower()
    desc = (tags.get("description") or "").lower()
    blob = name + " " + desc
    for hint, sous_cat in NAME_HINTS:
        if hint in blob:
            return sous_cat
    if amenity == "childcare":
        return "multi_accueil"
    # Default for kindergarten without specifier
    return "creche_collective"


def deduce_secteur(tags: Dict[str, Any]) -> Optional[str]:
    op_type = tags.get("operator:type")
    if not op_type:
        return None
    op_type = str(op_type).lower().strip()
    if op_type == "public":
        return "public"
    if op_type in ("private", "private_for_profit"):
        return "prive_sous_contrat"
    return None


def reverse_geocode_insee(lat: float, lon: float, cache: Dict[Tuple[float, float], Tuple[Optional[str], Optional[str], Optional[str]]], verbose: bool = False) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Return (code_insee, nom_commune, code_postal) for given (lat, lon)."""
    key = (round(lat, 5), round(lon, 5))
    if key in cache:
        return cache[key]
    params = {"lat": lat, "lon": lon, "fields": "code,nom,codesPostaux"}
    try:
        r = requests.get(
            GEOAPI_COMMUNES_URL,
            params=params,
            headers={"User-Agent": USER_AGENT},
            timeout=10,
        )
        r.raise_for_status()
        results = r.json() or []
        if not isinstance(results, list) or not results:
            cache[key] = (None, None, None)
            return cache[key]
        # API returns nearest commune first; take it
        c = results[0]
        cps = c.get("codesPostaux") or []
        cp = cps[0] if cps else None
        out = (c.get("code"), c.get("nom"), cp)
    except Exception as e:
        if verbose:
            print(f"[geoapi] error {lat},{lon}: {e}")
        out = (None, None, None)
    cache[key] = out
    # Politeness: 50 req/s allowed, we throttle conservatively
    time.sleep(0.05)
    return out


def in_bounds(lat: float, lon: float) -> bool:
    return (
        BOUNDS_CORSE["lat_min"] <= lat <= BOUNDS_CORSE["lat_max"]
        and BOUNDS_CORSE["lon_min"] <= lon <= BOUNDS_CORSE["lon_max"]
    )


def extract_coords(el: Dict[str, Any]) -> Tuple[Optional[float], Optional[float]]:
    if "lat" in el and "lon" in el:
        return float(el["lat"]), float(el["lon"])
    center = el.get("center") or {}
    if "lat" in center and "lon" in center:
        return float(center["lat"]), float(center["lon"])
    return None, None


def build_address(tags: Dict[str, Any]) -> Optional[str]:
    parts = []
    hn = tags.get("addr:housenumber")
    st = tags.get("addr:street")
    if hn:
        parts.append(str(hn))
    if st:
        parts.append(str(st))
    if parts:
        return " ".join(parts)
    return None


def transform_elements(
    elements: Iterable[Dict[str, Any]],
    extraction_date: str,
    verbose: bool = False,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Convert raw Overpass elements to Tellux schema features.

    Returns (features_kept, features_rejected).
    """
    features: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []
    insee_cache: Dict[Tuple[float, float], Tuple[Optional[str], Optional[str], Optional[str]]] = {}
    for el in elements:
        el_type = el.get("type") or "unknown"
        el_id = el.get("id")
        tags = el.get("tags") or {}
        full_id = f"osm_{el_type}_{el_id}"
        if full_id in EXCLUDED_OSM_IDS:
            rejected.append({"id": full_id, "reason": "excluded_osm_anomaly", "note": EXCLUDED_OSM_IDS[full_id]})
            continue
        lat, lon = extract_coords(el)
        if lat is None or lon is None:
            rejected.append({"id": full_id, "reason": "no_coordinates"})
            continue
        if not in_bounds(lat, lon):
            rejected.append({"id": full_id, "reason": "out_of_corse_bounds", "lat": lat, "lon": lon})
            continue
        amenity = str(tags.get("amenity", ""))
        name = tags.get("name")
        if not name:
            name = "Crèche sans nom"
        sous_cat = deduce_sous_categorie(tags, amenity)
        # Address
        address = build_address(tags)
        cp_tag = tags.get("addr:postcode")
        city_tag = tags.get("addr:city")
        insee_tag = tags.get("ref:INSEE")
        # Reverse geocode if any of (insee, city, postcode) is missing
        need_geocode = not insee_tag or not city_tag or not cp_tag
        if need_geocode:
            insee_geo, city_geo, cp_geo = reverse_geocode_insee(lat, lon, insee_cache, verbose=verbose)
            insee_final = insee_tag or insee_geo
            city_final = city_tag or city_geo
            cp_final = cp_tag or cp_geo
        else:
            insee_final, city_final, cp_final = insee_tag, city_tag, cp_tag
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [round(float(lon), 6), round(float(lat), 6)],
            },
            "properties": {
                "id": f"osm_{el_type}_{el_id}",
                "nom": name,
                "categorie": "petite-enfance",
                "sous_categorie": sous_cat,
                "adresse": address,
                "code_postal": cp_final,
                "commune": city_final,
                "code_insee": insee_final,
                "secteur": deduce_secteur(tags),
                "source": "osm",
                "date_extraction": extraction_date,
            },
        }
        features.append(feature)
    return features, rejected


def determine_scenario(n: int) -> str:
    if n > 30:
        return "A"
    if n >= 10:
        return "B"
    return "C"


def coverage_note_for(scenario: str, n: int) -> str:
    if scenario == "A":
        return (
            "Source OpenStreetMap (tags amenity=kindergarten et amenity=childcare). "
            f"Couverture jugee suffisante ({n} features) pour usage operationnel. "
            "Pour information exhaustive, consulter mon-enfant.fr ou la CAF de Corse."
        )
    if scenario == "B":
        return (
            "Source OpenStreetMap (tags amenity=kindergarten et amenity=childcare). "
            f"Couverture partielle ({n} features) dependante des contributions OSM. "
            "Pour information exhaustive, consulter mon-enfant.fr ou la CAF de Corse."
        )
    return (
        "Source OpenStreetMap (tags amenity=kindergarten et amenity=childcare). "
        f"Couverture insuffisante ({n} features) pour usage operationnel. "
        "Pour identifier les EAJE proches d'une antenne, consultez mon-enfant.fr (CAF) "
        "ou la mairie concernee."
    )


def build_metadata(features: List[Dict[str, Any]], rejected: List[Dict[str, Any]], extraction_date: str) -> Dict[str, Any]:
    n = len(features)
    scenario = determine_scenario(n)
    expected_total = 60  # ~45 (2B Schema departemental 2020) + ~15 (estimation 2A par extrapolation)
    coverage_pct = round(100.0 * n / expected_total, 1) if expected_total else None
    sous_cat_counts: Dict[str, int] = {}
    for f in features:
        sc = f["properties"].get("sous_categorie", "?")
        sous_cat_counts[sc] = sous_cat_counts.get(sc, 0) + 1
    return {
        "generator": "tellux build_eaje_osm_corse.py v1.0",
        "date_extraction": extraction_date,
        "licence_donnees": "ODbL (OpenStreetMap)",
        "licence_compilation": "Etalab 2.0",
        "projection": "EPSG:4326",
        "attribution": "© OpenStreetMap contributors. Compilation Tellux Corse.",
        "source": "osm_overpass",
        "extraction_method": "Overpass API",
        "extraction_query": "amenity=kindergarten + amenity=childcare in FR-2A, FR-2B",
        "ticket_reference": "EAJE-CORSE-001 (resolu par cette extraction)",
        "feature_count": n,
        "rejected_count": len(rejected),
        "expected_total_corse": expected_total,
        "expected_breakdown": "~45 (2B, schema departemental 2020) + ~15-20 (2A, estimation extrapolation demographique)",
        "coverage_estimate_pct": coverage_pct,
        "scenario": scenario,
        "coverage_note": coverage_note_for(scenario, n),
        "sous_categorie_repartition": sous_cat_counts,
    }


def write_geojson(features: List[Dict[str, Any]], metadata: Dict[str, Any], path: Path) -> None:
    fc = {
        "type": "FeatureCollection",
        "metadata": metadata,
        "features": features,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False, indent=2)


def write_rejected(rejected: List[Dict[str, Any]], path: Path) -> None:
    if not rejected:
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            {"type": "FeatureCollection", "metadata": {"note": "rejected_features"}, "features": [], "rejected": rejected},
            f, ensure_ascii=False, indent=2,
        )


def main() -> int:
    p = argparse.ArgumentParser(description="Build EAJE Corse GeoJSON from OSM Overpass.")
    p.add_argument("--output", default="public/data/corse", help="Output directory.")
    p.add_argument("--verbose", action="store_true", help="Verbose logs.")
    p.add_argument("--rejected", default=None, help="Optional path for rejected features (JSON).")
    args = p.parse_args()

    extraction_date = dt.date.today().isoformat()
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "eaje.geojson"

    elements = fetch_overpass(verbose=args.verbose)
    if args.verbose:
        print(f"[overpass] elements: {len(elements)}")

    features, rejected = transform_elements(elements, extraction_date, verbose=args.verbose)
    metadata = build_metadata(features, rejected, extraction_date)

    write_geojson(features, metadata, out_path)
    if args.rejected:
        write_rejected(rejected, Path(args.rejected))

    print(f"\nfeature_count = {len(features)}")
    print(f"rejected_count = {len(rejected)}")
    print(f"scenario = {metadata['scenario']}")
    print(f"coverage_estimate_pct = {metadata['coverage_estimate_pct']}")
    print(f"sous_categorie = {metadata['sous_categorie_repartition']}")
    print(f"output = {out_path}")
    if args.verbose:
        for f in features:
            p = f["properties"]
            print(f"  - {p['id']:24s} {p.get('commune') or '?':25s} {p.get('code_insee') or '?':6s} {p['sous_categorie']:18s} {p['nom']}")

    return 0 if features else 2


if __name__ == "__main__":
    sys.exit(main())
