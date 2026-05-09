# Rapport de session — Brief 34 Phase A : audit GPS sites patrimoine (Cap + Cortenais)

Date : 2026-05-06
Périmètre : Phase A — 96 sites du Cap (48 sur 54, 6 déjà audités) + Cortenais (48 sur 48, 0 audités).
Statut Cowork : **script complet rédigé, exécution déléguée à Soleil/Code (réseau OSM/Wikidata/IGN bloqué côté sandbox Cowork)**.

## Inventaire vérifié

```
Sites Cap        : 54 (6 déjà audités, 48 à traiter)
Sites Cortenais  : 48 (0 audités, 48 à traiter)
Total Phase A    : 96 sites
gps_audit existants : 5 entrées datées 2026-04-23 + 1 datée 2026-04-14
```

Cohérent avec le brief Soleil (96 sites annoncés).

## Faisabilité réseau côté Cowork

Le sandbox Linux Cowork tourne derrière un proxy avec **allowlist** :

```
* Establish HTTP proxy tunnel to nominatim.openstreetmap.org:443
< HTTP/1.1 403 Forbidden
< X-Proxy-Error: blocked-by-allowlist
```

OSM Nominatim, Wikidata SPARQL, et l'API Adresse data.gouv (IGN) ne sont pas accessibles depuis le sandbox. Cowork ne peut donc pas exécuter le script. **L'exécution doit se faire chez Soleil ou Code en environnement local.**

## Livrable Cowork

`scripts/audit_gps_sites_patrimoine.py` — script Python complet (~12 KB), autonome, prêt à exécution. Fonctionnalités :

- **3 sources** croisées : OSM Nominatim, Wikidata SPARQL, IGN/Etalab `api-adresse.data.gouv.fr`.
- **Scoring** HAUTE / MOYENNE / FAIBLE / ABSENT selon nombre de sources concordantes et distance inter-sources :
  - HAUTE : 3 sources et distance max <100 m
  - MOYENNE : ≥2 sources et distance max <500 m
  - FAIBLE : sinon
  - ABSENT : aucune source ne répond
- **Backup automatique** `_drafts/sites_patrimoine.backup_{TODAY}.json` avant `--apply`.
- **Garde-fou distance** : pas d'application auto si distance new/old >5000 m, flagué pour audit manuel.
- **Conservation des coords originales** dans le champ `notes` du site.
- **CSV de rapport** `_drafts/audit_gps_phase{X}_{TODAY}.csv` avec 22 colonnes (slug, name, old/new lat-lon, distance, confiance, sources, matches, applied, pieve concordance, doyenne concordance, note).
- **Bonus reverse-geocoding** (`--reverse-geocode`) : vérifie que les nouvelles coords tombent dans le polygone de la pieve/doyenne déclarée. Log warning si discordance.
- **Throttle 1.1 s** entre requêtes (politesse OSM Nominatim public).
- **User-Agent** : `Tellux-Audit-GPS/1.0 (contact: stelladluca@proton.me)` conforme Nominatim policy.

CLI :

```
# Test sur 5 sites variés (aucune écriture)
python scripts/audit_gps_sites_patrimoine.py --phase A --limit 5 --dry-run

# Run complet Phase A en dry-run, génère CSV uniquement
python scripts/audit_gps_sites_patrimoine.py --phase A --dry-run

# Run complet et application des updates HAUTE/MOYENNE au JSON (avec backup)
python scripts/audit_gps_sites_patrimoine.py --phase A --apply --reverse-geocode
```

Phases B à F déjà câblées via `PHASE_DOYENNES`. Phase F (`doyenne_contemporain_slug = null`) supportée pour le futur travail des 57 sites unknown (audit GPS + reverse-geocoding pour rattachement pieve/doyenne).

## Procédure d'exécution recommandée (Soleil ou Code)

1. **Sanity check** sur 5 sites variés :
   ```
   python scripts/audit_gps_sites_patrimoine.py --phase A --limit 5 --dry-run
   ```
   Lit le CSV `_drafts/audit_gps_phaseA_{TODAY}.csv`, vérifie la qualité de la sortie. Durée estimée : 5 sites × ~6 s (3 sources × 1.1 s + traitement) = ~30 s.

2. **Run complet Phase A en dry-run** :
   ```
   python scripts/audit_gps_sites_patrimoine.py --phase A --dry-run --reverse-geocode
   ```
   96 sites × ~6 s = ~10 min réseau. Génère CSV complet, ne touche pas le JSON.

3. **Revue Soleil** du CSV : vérifier les flags FAIBLE / ABSENT / DIST_OVER_5000m, valider les MOYENNE.

4. **Application** :
   ```
   python scripts/audit_gps_sites_patrimoine.py --phase A --apply --reverse-geocode
   ```
   Applique les updates HAUTE et MOYENNE <500 m au JSON. Backup auto avant écriture.

5. **Vérification post-apply** :
   - Le JSON `docs/data/sites_patrimoine.json` est-il toujours valide ? (`python -c "import json; json.load(open('docs/data/sites_patrimoine.json'))"`)
   - Le compteur `gps_audit_2026-05` est-il bien renseigné sur les sites updated ?
   - Le champ `notes` contient-il bien les coords originales pour rollback éventuel ?

## Hypothèses prises (faute de brief précédent détaillé accessible)

Le brief actuel renvoie plusieurs fois à « [idem brief précédent] » pour les détails fins. N'ayant pas accès au brief précédent, j'ai supposé :

- **CSV format** : 22 colonnes incluant les concordances pieve/doyenne (pour intégrer le bonus reverse-geocoding directement dans le rapport).
- **Sources d'IGN BDTOPO** : utilisé `api-adresse.data.gouv.fr` (Etalab, gratuit, sans clé) plutôt qu'une clé IGN BDTOPO payante. Si Soleil veut un accès BDTOPO authentifié, ajouter la clé dans la fonction `query_ign_geocoding`.
- **Wikidata fallback fuzzy** : utilisé un `CONTAINS(LCASE(?label))` simple. Si plusieurs candidats matchent, le premier est retenu — peut donner des faux positifs sur des noms communs (« San Giovanni »). Marquage MOYENNE ou FAIBLE selon les autres sources.
- **Bonus reverse-geocoding** : flag optionnel `--reverse-geocode`, lit `pieves_polygons.json` et `doyennes_polygons.json`, applique un point-in-polygon ray-casting basique (suffisant pour des polygones de doyennés/pieves convexes, marges acceptables sur les bords).

À ajuster côté Soleil/Code si le brief précédent contient des spécifications plus précises non transmises.

## Limites et risques

- **Throttle OSM Nominatim** : 1.1 s entre requêtes pour respecter la politique gratuite. Si le run dépasse ~1500 requêtes/h, OSM peut blacklist l'IP. Pour 96 sites × 1 requête OSM = 96 requêtes, on est largement sous le seuil.
- **Wikidata SPARQL** : pas de rate-limit strict, mais éviter les requêtes massives. 96 requêtes max, OK.
- **API Adresse Etalab** : pas de quota strict pour usage modéré.
- **Faux positifs** : un nom commun (« Santa Maria ») peut matcher des dizaines d'entrées. Le scoring filtre, mais des FAIBLE peuvent atterrir en HAUTE si les 3 sources convergent par hasard sur un mauvais site. **À auditer manuellement par Soleil avant `--apply`** sur la base du CSV.
- **Coordonnées en mer / hors Corse** : aucun filtre bbox dans le scoring. Le reverse-geocoding bonus permet de détecter les sites qui sortent de leur pieve/doyenne déclarée, ce qui flag indirectement ces erreurs.
- **Dépendances Python** : `requests` requis. Si absent : `pip install requests` (ou avec `--break-system-packages` sur certaines distributions).

## Fichiers livrés

- `scripts/audit_gps_sites_patrimoine.py` — script complet Cowork.
- `fiches_patrimoine/RAPPORT_SESSION_BRIEF_34_AUDIT_GPS_PHASE_A.md` — ce rapport.

## Statut tâches Cowork

- ✅ Audit faisabilité (réseau bloqué côté sandbox, libs OK).
- ✅ Inventaire 96 sites Phase A confirmé.
- ✅ Script `audit_gps_sites_patrimoine.py` rédigé et validé syntaxiquement (`--help` OK).
- ❌ Test 5 sites variés — délégué à Soleil/Code (réseau).
- ❌ Run Phase A complet — délégué à Soleil/Code (réseau).

## Estimation Phase A après merge

Selon brief Soleil : 96 sites × ~3 s = 5 min. Avec throttle 1.1 s entre requêtes et 3 sources par site : **96 × 3 sources × 1.1 s ≈ 5 min réseau pure** + temps de scoring/écriture négligeable. Cohérent.

Pour les phases suivantes (réutilisation du script avec `--phase B` à `F`) :

- Phase B (Plaine + Ajaccio) : ~58 sites → ~3 min
- Phase C (Golo + Balagne) : ~84 sites → ~5 min
- Phase D (Extrême-Sud + Piana) : ~98 sites → ~5 min
- Phase E (Prunelli-Taravo-Valinco) : ~38 sites → ~2 min
- Phase F (sites unknown 57) : ~3 min + reverse-geocoding obligatoire pour ratacher

Total corpus 437 sites : ~25 min réseau effectif réparti sur 6 phases.

## Mea culpa préventif

Le brief précédent (« [idem brief précédent] ») n'était pas accessible dans le repo public ni dans les conversations Soleil-Cowork récentes. Si une partie du script ne correspond pas exactement à la spec brief précédent (format CSV, ordre des colonnes, exact nom des sources, etc.), c'est rectifiable en 5-10 min Cowork une fois la spec transmise.

## Durée

Session ponctuelle Cowork. Audit faisabilité + rédaction script + rapport. ~1h30.
