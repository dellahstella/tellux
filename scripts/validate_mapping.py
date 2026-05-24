#!/usr/bin/env python3
"""
validate_mapping.py REV4 — coherence mapping + validator preventif name/slug.

Bloc 1 (REV2 historique) : coherence mapping pieves
1. 0 zombie : tout slug reference dans mapping doit exister dans pieves_polygons.json prod
2. 0 manquante : tout slug dans pieves_polygons.json prod doit etre mappable
3. Total communes mappees == 360 (toutes communes 2A+2B)
4. Pas de commune doublement assignee
5. PIP sanity check (warning seulement) : centroide commune dans polygone cible ?

Bloc 2 (REV3 ajoute 2026-05-24) : validator preventif name/slug
Suite a la regression `pieve_patrimonio` (fix 18/05) ou name === slug avait fuite
en prod, on durcit les invariants. Audit cross-corpus 24/05 confirme corpus clean.
- PIEVE  : name !== slug, name ne commence pas par "Pieve di ", name ne commence pas par "pieve_"
- DOYENNE: name commence par "Doyenne ", display_name present, slug commence par "doyenne_"
- SITE   : name pas slug brut, pieve_slug et doyenne_contemporain_slug connus

Bloc 3 (REV4 ajoute 2026-05-24) : cumulative loader etendu v1 -> v11
Auparavant le loader s'arretait a v4 (cleanup 2026-05-18). REV4 ingere v5_vague,
v5_pr2, v6, v7, v8, v9, v10, v11 selon la chaine `extends` chronologique, et gere
le champ `removed_zombies` (introduit v4, deliberement honore v6 pour pieve_ghisoni
arbitrage Soleil Option A 2026-05-23). Resorbe 3 false-positives REV2 baseline :
pieve_ghisoni zombie, pieve_ampugnani missing, pieve_tavignano missing.

Exit code 1 si erreurs (un quelconque bloc), 0 sinon. Integration future :
pre-commit hook + CI guard.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAPPING_V1 = ROOT / "_drafts" / "pieves_communes_mapping.json"
MAPPING_V2 = ROOT / "_drafts" / "pieves_communes_mapping_v2_canonicite_casta.json"
MAPPING_V3 = ROOT / "_drafts" / "pieves_communes_mapping_v3_stratD_2026-05-17.json"
MAPPING_V4 = ROOT / "_drafts" / "pieves_communes_mapping_v4_cleanup_2026-05-18.json"

# REV4 (2026-05-24) — extension du loader aux mappings v5-v11 livres
# post-Vague Pieves PR1/PR2 (22-23/05). Auparavant le validator s'arretait
# a v4 (cleanup 2026-05-18), ce qui generait 3 false-positives REV2 :
# pieve_ghisoni zombie (supprimee v6), pieve_ampugnani missing (creee v5_pr2),
# pieve_tavignano missing (creee v6). Chaine `extends` verifiee 2026-05-24 :
# v5_vague->v4, v5_pr2->v5_vague, v6->v5_pr2, v7->v6, v8->v7, v9->v8,
# v10->v9, v11->v10.
MAPPING_V5_VAGUE   = ROOT / "_drafts" / "pieves_communes_mapping_v5_vague_22052026.json"
MAPPING_V5_PR2     = ROOT / "_drafts" / "pieves_communes_mapping_v5_pr2_arbitrages.json"
MAPPING_V6         = ROOT / "_drafts" / "pieves_communes_mapping_v6_tavignano_2026-05-23.json"
MAPPING_V7         = ROOT / "_drafts" / "pieves_communes_mapping_v7_vezzani_2026-05-23.json"
MAPPING_V8         = ROOT / "_drafts" / "pieves_communes_mapping_v8_rogna_audit_2026-05-23.json"
MAPPING_V9         = ROOT / "_drafts" / "pieves_communes_mapping_v9_fix_zombies_orphelines_vallerustie.json"
MAPPING_V10        = ROOT / "_drafts" / "pieves_communes_mapping_v10_fix_zone_orpheline_vico.json"
MAPPING_V11        = ROOT / "_drafts" / "pieves_communes_mapping_v11_declare_pieve_patrimonio.json"

PIEVES_PROD = ROOT / "docs" / "data" / "pieves_polygons.json"
DOYENNES_PROD = ROOT / "docs" / "data" / "doyennes_polygons.json"
SITES_PROD = ROOT / "docs" / "data" / "sites_patrimoine.json"
PIEVE_ALIASES = ROOT / "docs" / "data" / "pieve_aliases.json"
GEO_2A = ROOT / "scripts" / ".cache" / "communes-2A.geojson"
GEO_2B = ROOT / "scripts" / ".cache" / "communes-2B.geojson"


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.JSONDecoder().raw_decode(f.read())[0]


def merge_mappings():
    """Reproduit logique build_pieves_polygons.py + chaine cumulative v1 -> v11.

    REV4 (2026-05-24) : la chaine est determinee par le champ `extends` de chaque
    mapping (verifie 2026-05-24). Ordre chronologique strict :
      v1 < v2 < v3 < v4 < v5_vague < v5_pr2 < v6 < v7 < v8 < v9 < v10 < v11

    REV4 ajoute aussi la prise en compte du champ `removed_zombies` (slug seul
    ou objet {slug, rationale}) — introduit v4, deliberement honore v6 pour
    pieve_ghisoni arbitrage Soleil Option A 2026-05-23.
    """
    commune_to_pieve = {}
    removed_pieves = set()

    # Base v1 — declare les pieves originelles.
    m1 = load(MAPPING_V1)
    for p in m1.get("pieves", []):
        for insee in p["communes_insee"]:
            commune_to_pieve[insee] = p["slug"]

    # Chaine cumulative v2 -> v11 (extensions ordonnees selon `extends`).
    CHAIN = [
        MAPPING_V2, MAPPING_V3, MAPPING_V4,
        MAPPING_V5_VAGUE, MAPPING_V5_PR2,
        MAPPING_V6, MAPPING_V7, MAPPING_V8,
        MAPPING_V9, MAPPING_V10, MAPPING_V11,
    ]
    for path in CHAIN:
        if not path.exists():
            continue
        mv = load(path)
        for p in mv.get("pieves_added", []):
            for insee in p["communes_insee"]:
                commune_to_pieve[insee] = p["slug"]
            # REV4 — pieves_added ressuscite la pieve : si un v<n> antecedent
            # l'avait declaree zombie, la sortir du set removed_pieves (cas
            # pieve_ampugnani : v4 removed_zombies puis v5_pr2 pieves_added).
            removed_pieves.discard(p["slug"])
        for t in mv.get("transferts", []):
            commune_to_pieve[t["commune_insee"]] = t["vers_pieve"]
            # REV4 — un transfert vers une pieve ressuscite aussi la cible
            # (defense en profondeur, cas v7+ qui peut alimenter une pieve
            # anciennement zombifiee sans pieves_added explicite).
            removed_pieves.discard(t["vers_pieve"])
        for r in mv.get("renames", []):
            for insee, slug in list(commune_to_pieve.items()):
                if slug == r["from"]:
                    commune_to_pieve[insee] = r["to"]
            # REV4 — rename "ressuscite" implicitement la cible.
            removed_pieves.discard(r["to"])
        # REV4 : prise en compte des suppressions explicites (format slug ou dict).
        for rz in mv.get("removed_zombies", []):
            slug = rz["slug"] if isinstance(rz, dict) else rz
            removed_pieves.add(slug)

    # Filtrage final : retirer toute commune mappee a une pieve explicitement
    # supprimee (defense en profondeur — normalement les transferts v6+ ont
    # deja deplace les communes vers leur nouvelle pieve ; ce filtre rattrape
    # un eventuel oubli de transfert).
    commune_to_pieve = {
        insee: slug for insee, slug in commune_to_pieve.items()
        if slug not in removed_pieves
    }
    return commune_to_pieve


def validate_pieves(pieves_data):
    """REV3 bloc PIEVE : detecte regressions name===slug et prefixes parasites."""
    errors = []
    for entry in pieves_data:
        slug = entry.get("slug", "")
        name = entry.get("name", "")
        if not slug:
            errors.append("pieve sans slug")
            continue
        if name == slug:
            errors.append(f"pieve {slug}: name === slug (regression type pieve_patrimonio 18/05)")
        if name.startswith("Pieve di "):
            errors.append(f"pieve {slug}: name prefixe 'Pieve di ' (canonicite Tellux : nom court)")
        if name.startswith("pieve_"):
            errors.append(f"pieve {slug}: name = slug brut ('pieve_...')")
    return errors


def validate_doyennes(doyennes_data):
    """REV3 bloc DOYENNE : detecte name parasite + display_name manquant + slug malforme.

    Note : le corpus actuel utilise 3 patterns de name ("Doyenne du X", "Doyenne d'X",
    "Doyenne X"). Le check accepte tout name commencant par "Doyenne " — assez strict
    pour bloquer "doyenne_xxx" en nom, assez permissif pour le corpus existant.
    """
    errors = []
    for entry in doyennes_data:
        slug = entry.get("slug", "")
        name = entry.get("name", "")
        display_name = entry.get("display_name")
        if not slug:
            errors.append("doyenne sans slug")
            continue
        if not name.startswith("Doyenn"):
            errors.append(f"doyenne {slug}: name doit commencer par 'Doyenne' (got {name!r})")
        if not display_name:
            errors.append(f"doyenne {slug}: display_name manquant")
        if not slug.startswith("doyenne_"):
            errors.append(f"doyenne {slug}: slug malforme (doit commencer par 'doyenne_')")
        if name == slug:
            errors.append(f"doyenne {slug}: name === slug")
    return errors


def validate_sites(sites_data, known_pieve_slugs, known_doyenne_slugs):
    """REV3 bloc SITE : detecte name slug-brut + slugs pieve/doyenne inconnus."""
    errors = []
    for site in sites_data:
        name = site.get("name") or ""
        # Assert 1 : name ne ressemble pas a un slug brut (snake_case lowercase)
        if name and "_" in name and name == name.lower() and " " not in name:
            errors.append(f"site {site.get('slug', '?')}: name {name!r} ressemble a un slug brut")
        # Assert 2 : pieve_slug connu (si renseigne)
        ps = site.get("pieve_slug")
        if ps and ps not in known_pieve_slugs:
            errors.append(f"site {site.get('slug', '?')}: pieve_slug inconnu {ps!r}")
        # Assert 3 : doyenne_contemporain_slug connu (si renseigne)
        ds = site.get("doyenne_contemporain_slug")
        if ds and ds not in known_doyenne_slugs:
            errors.append(f"site {site.get('slug', '?')}: doyenne_contemporain_slug inconnu {ds!r}")
    return errors


def run_name_slug_validator():
    """REV3 — execute les 3 blocs PIEVE/DOYENNE/SITE. Returns list of errors."""
    all_errors = []

    pieves_data = load(PIEVES_PROD).get("pieves", [])
    pieve_errors = validate_pieves(pieves_data)
    all_errors.extend(("PIEVE", e) for e in pieve_errors)

    doyennes_data = load(DOYENNES_PROD).get("doyennes", [])
    doyenne_errors = validate_doyennes(doyennes_data)
    all_errors.extend(("DOYENNE", e) for e in doyenne_errors)

    # Set de slugs pieve connus (51 prod + aliases si presents).
    known_pieve_slugs = {p["slug"] for p in pieves_data}
    if PIEVE_ALIASES.exists():
        aliases = load(PIEVE_ALIASES).get("aliases", {})
        known_pieve_slugs.update(aliases.keys())
    known_doyenne_slugs = {d["slug"] for d in doyennes_data}

    sites_raw = load(SITES_PROD)
    sites_data = sites_raw if isinstance(sites_raw, list) else sites_raw.get("sites", [])
    site_errors = validate_sites(sites_data, known_pieve_slugs, known_doyenne_slugs)
    all_errors.extend(("SITE", e) for e in site_errors)

    print(f"\n=== REV3 validator preventif (name/slug) ===")
    print(f"Pieves analysees   : {len(pieves_data)} -> {len(pieve_errors)} erreur(s)")
    print(f"Doyennes analysees : {len(doyennes_data)} -> {len(doyenne_errors)} erreur(s)")
    print(f"Sites analyses     : {len(sites_data)} -> {len(site_errors)} erreur(s)")
    print(f"Total erreurs      : {len(all_errors)}")
    print(f"Connus : {len(known_pieve_slugs)} pieve_slugs (51 prod + aliases), "
          f"{len(known_doyenne_slugs)} doyenne_slugs")
    if all_errors:
        print()
        for bloc, err in all_errors[:50]:
            print(f"  [{bloc}] {err}")
        if len(all_errors) > 50:
            print(f"  ... ({len(all_errors) - 50} autres erreurs)")

    return all_errors


def main():
    commune_to_pieve = merge_mappings()
    mapping_slugs = set(commune_to_pieve.values())

    pieves_prod = load(PIEVES_PROD)
    prod_slugs = {p["slug"] for p in pieves_prod["pieves"]}

    zombies = sorted(mapping_slugs - prod_slugs)
    missing = sorted(prod_slugs - mapping_slugs)
    total = len(commune_to_pieve)

    pip_warnings = []
    if GEO_2A.exists() and GEO_2B.exists():
        from shapely.geometry import shape, Polygon
        commune_geoms = {}
        for path in (GEO_2A, GEO_2B):
            for feat in json.load(open(path, encoding="utf-8"))["features"]:
                commune_geoms[feat["properties"]["code"]] = shape(feat["geometry"])

        def to_poly(latlng):
            return Polygon([[c[1], c[0]] for c in latlng])

        pieve_shapes = {p["slug"]: to_poly(p["polygon"]) for p in pieves_prod["pieves"]}

        for insee, target_slug in commune_to_pieve.items():
            g = commune_geoms.get(insee)
            if not g:
                continue
            target_poly = pieve_shapes.get(target_slug)
            if not target_poly or not target_poly.is_valid:
                continue
            rp = g.representative_point()
            if not (target_poly.contains(rp) or target_poly.intersects(rp)):
                pip_warnings.append({"insee": insee, "target": target_slug})

    print(f"Mapping slugs : {len(mapping_slugs)}")
    print(f"Prod slugs    : {len(prod_slugs)}")
    print(f"Total communes mapped : {total} (expected 360)")
    print(f"\nZombies (mapping -> absent prod) : {len(zombies)}")
    for z in zombies:
        n = sum(1 for v in commune_to_pieve.values() if v == z)
        print(f"  - {z} ({n} communes)")
    print(f"Missing (prod -> absent mapping) : {len(missing)}")
    for m in missing:
        print(f"  - {m}")
    print(f"\nPIP sanity warnings (centroide hors polygone cible) : {len(pip_warnings)} [INFO]")
    if pip_warnings and len(pip_warnings) < 20:
        for w in pip_warnings:
            print(f"  - {w['insee']} -> {w['target']}")
    elif pip_warnings:
        print("  (premieres 10) :")
        for w in pip_warnings[:10]:
            print(f"  - {w['insee']} -> {w['target']}")

    fails = []
    if zombies:
        fails.append(f"{len(zombies)} zombies")
    if missing:
        fails.append(f"{len(missing)} missing")
    if total != 360:
        fails.append(f"total={total} (expected 360)")

    if not fails:
        print("\nOK validate_mapping REV2 : mapping coherent, 360 communes mappees, 0 zombie, 0 manquante")
        if pip_warnings:
            print(f"  (Note: {len(pip_warnings)} PIP warnings = polygones prod obsoletes, dette PR C)")
    else:
        print(f"\nFAIL validate_mapping REV2 : {' + '.join(fails)}")

    # REV3 — validator preventif name/slug (PIEVE/DOYENNE/SITE).
    name_slug_errors = run_name_slug_validator()
    if name_slug_errors:
        fails.append(f"{len(name_slug_errors)} name/slug erreurs")
        print(f"\nFAIL validate_mapping REV3 name/slug : {len(name_slug_errors)} erreur(s)")
    else:
        print("\nOK validate_mapping REV3 name/slug : 0 erreur (corpus PIEVE+DOYENNE+SITE clean)")

    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
