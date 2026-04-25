# Antennes ANFR Corse — note de data source

**Table Supabase :** `public.antennas_corse`
**Fichier GeoJSON agrégé :** `public/data/antennes_par_commune_corse.json`
**Pipeline producteur :** `scripts/build_antennes_par_commune_corse.py`
**Date de dernière passe majeure :** 2026-04-24 (résolution du ticket `SUPABASE-COMMUNE-FIELD-001`)
**Licence :** données ANFR sous Licence Ouverte 2.0 (Etalab)

---

## 1. Schéma de la table

```
public.antennas_corse (3000 lignes)
├── id                 integer  PK
├── lat                double precision   NOT NULL
├── lon                double precision   NOT NULL
├── generation         varchar            — "2G" | "3G" | "4G" | "5G"
├── commune            varchar            — champ legacy, pollué, laissé pour traçabilité
├── operateur          varchar            — "Orange" | "SFR" | "Bouygues" | "Free"
├── sup_id             text               — non peuplé (null sur toutes les lignes)
└── code_insee_commune text               — SOURCE DE VÉRITÉ (ajoutée 2026-04-24)
    index idx_antennas_corse_code_insee_commune
```

**Source de vérité pour filtrage par commune :** `code_insee_commune`.

**Champs legacy à éviter en lecture :**

- `commune` : contient un mélange de codes INSEE bruts (`"2A004"`), toponymes de sites (`"PIANELLO"`, `"Punta Pozzo di Borgo"`) et noms en majuscules (`"AJACCIO"`). 476 valeurs distinctes pour 360 communes réelles, 7 matches exacts INSEE seulement. **Ne pas filtrer sur ce champ.** Conservé pour traçabilité de la source originale ANFR.
- `sup_id` : null sur les 3000 lignes.

---

## 2. Peuplement initial de `code_insee_commune`

Passe unique le 2026-04-24 via `scripts/fix_supabase_commune_insee.py`, méthode point-in-polygon contre les contours IGN AdminExpress récupérés sur `geo.api.gouv.fr`.

**Résultats** :

| Métrique | Valeur |
|---|---|
| Lignes totales | 3000 |
| `code_insee_commune` NON NULL | 2986 (99.5 %) |
| `code_insee_commune` NULL | 14 (offshore) |
| Codes INSEE distincts | 219 |
| Durée d'exécution (calcul + UPDATE 6 batches de 500) | ~5 s |

**Les 14 NULL** sont toutes des antennes offshore hors contours communaux IGN :
- 10 antennes à (41.856667, 9.403889), label `commune = "PORT DE PLAISANCE"` (Bouygues + Free + SFR) — îles Cerbicale au sud-est de Porto-Vecchio
- 4 antennes à (42.679444, 9.301111), label `commune = "Le Port"` (Orange) — môle nord Bastia

Ces valeurs NULL sont conformes et n'indiquent pas une régression. Elles correspondent aux 14 antennes déjà identifiées comme offshore dans le pipeline v1.0 de `build_antennes_par_commune_corse.py` (avant résolution du ticket).

**Top 5 communes par nombre d'antennes** :

| INSEE | Commune | Antennes | Supports |
|---|---|---|---|
| 2A004 | Ajaccio | 327 | 98 |
| 2A247 | Porto-Vecchio | 158 | 49 |
| 2A041 | Bonifacio | 120 | 35 |
| 2B033 | Bastia | 107 | 32 |
| 2A272 | Sarrola-Carcopino | 52 | 16 |

---

## 3. Pipeline de refresh

### 3.1 Avant résolution du ticket (v1.0, obsolète)

Le script `build_antennes_par_commune_corse.py` v1.0 téléchargeait les 360 polygones de commune à chaque exécution, faisait du point-in-polygon côté client (shapely), et produisait `public/data/antennes_par_commune_corse.json`. Le champ `commune` de la base étant pollué, le calcul géométrique était la seule méthode fiable.

### 3.2 Après résolution (v2.0, en production)

Script simplifié : lecture directe de `code_insee_commune`, plus de téléchargement de polygones, plus de dépendance `shapely`, plus de calcul géométrique côté client. Seule dépendance : `requests`.

Pipeline :
1. Fetch `antennas_corse` avec `code_insee_commune`
2. Fetch noms de commune (`geo.api.gouv.fr/communes?codeDepartement=2A,2B&fields=nom,code&format=json`) — léger, sans géométrie
3. Dédup par `(lat, lon, operateur)`, agrégation générations par support
4. Écriture de `public/data/antennes_par_commune_corse.json` (structure inchangée vs v1.0)

**Sortie strictement équivalente à la v1.0** : même 219 communes, mêmes 1026 supports distincts, top 10 identique, 0 différence sur les counts par commune.

### 3.3 Refresh côté fichier statique

À chaque mise à jour du dataset Supabase (nouvelles antennes ajoutées, corrections), relancer :

```bash
python scripts/build_antennes_par_commune_corse.py
```

Durée attendue : ~2 secondes.

### 3.4 Refresh de `code_insee_commune` pour les nouvelles antennes

Pour les nouvelles antennes insérées dans `antennas_corse`, la colonne `code_insee_commune` doit être peuplée. Deux options :

- **Manuel ponctuel** : relancer `scripts/fix_supabase_commune_insee.py --apply` (idempotent, retraite toutes les lignes). Simple mais renvoie les 3000 lignes à chaque exécution.
- **Trigger Supabase** (évolution v3) : non implémenté en v2. À ajouter dès qu'un flux d'insertion régulier d'antennes est en place. Le trigger appellerait l'API geo.api.gouv.fr pour la nouvelle ligne insérée. À ce jour (2026-04-24), les 3000 antennes sont stables et ce besoin ne se fait pas sentir.

---

## 4. Ticket résolu

`SUPABASE-COMMUNE-FIELD-001` : **RÉSOLU** le 2026-04-24.

Option 2 retenue (ajout d'une colonne propre, non destructive, rétrocompatible) sur recommandation du ticket. Les garde-fous imposés par Soleil lors de l'arbitrage ont été respectés :

- Dump local complet préalable (`_backups/antennas_corse_2026-04-24.json`, 342 KB, non commité)
- Test point-in-polygon sur 10 antennes témoins avant ALTER TABLE (10/10 OK)
- Dry-run avant UPDATE production (2986/14/219 → conforme Passe 1)
- Validation post-UPDATE : 5 requêtes (total, NOT NULL, NULL, distinct, top 5) toutes conformes
- Champ `commune` historique non touché
- Aucune autre table Supabase modifiée
- Migration versionnée : `antennas_corse_add_code_insee_commune` (nom snake_case, query SQL stockée)

Voir aussi :
- [docs/tickets/EAJE-CORSE-001.md](../tickets/EAJE-CORSE-001.md) (dette connexe sur la source EAJE)
- `tellux_dettes_techniques/SUPABASE-COMMUNE-FIELD-001.md` (ticket d'origine)
- `tellux_dettes_techniques/ANTENNES-REFRESH-001.md` (dette connexe sur la cadence de refresh)

---

## 5. Consommateurs actuels et recommandations

### Pour tout nouveau module Tellux

**Lire `code_insee_commune`**, pas `commune`. Exemple de requête PostgREST côté client :

    /rest/v1/antennas_corse?select=...&code_insee_commune=eq.2A004

### `mairies.html` bloc Antennes (Fiche commune)

Utilise actuellement le JSON statique `public/data/antennes_par_commune_corse.json` généré par le pipeline v2.0. Migration potentielle vers un filtrage direct Supabase possible mais non justifiée en v1 (le JSON statique est déjà léger, 131 KB gzip ~12 KB, chargé en 22 ms).

### `app.html` bloc antennes

Charge toutes les 3000 antennes via `loadAnt()` pour rendu cartographique, sans filtrage par commune. `code_insee_commune` est disponible mais non utilisé. Aucune migration nécessaire.

---

## 6. Sources

- [data.gouv.fr — ANFR Cartoradio](https://www.cartoradio.fr/)
- [geo.api.gouv.fr — Découpage administratif](https://geo.api.gouv.fr/decoupage-administratif)
- [Supabase — Managed Postgres](https://supabase.com/docs/guides/database/overview)

Fin de la note.
