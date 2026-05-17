# Liste exécutable Claude Code — Refactor pièves Tellux

**Date** : 2026-05-17
**À destination de** : Claude Code (sessions CLI locales)
**Référence amont** : `ADR-001-pieves-doctrine.md`, `PIEVES_REFACTOR_PLAN_2026-05-17.md`
**Mode** : modification autorisée sur les fichiers listés, **après confirmation Soleil**.

---

## 0. Prérequis avant toute exécution

Avant tout, lire dans l'ordre :

1. `docs/operations/ADR-001-pieves-doctrine.md`
2. `docs/operations/PIEVES_REFACTOR_PLAN_2026-05-17.md` (statut : arbitrages actés 2026-05-17)

Arbitrages actés (récap, source : §5 du plan) :
- A1 `pieve_verde` → **suppression**
- A2 `pieve_bonifacio` vs `pieve_freto` → **statu quo + `note_decoupage`**
- A3 `pieve_ajaccio` → **`pieve_gulfo_d_aiacciu`**
- A4 `pieve_mariana` → **`pieve_piana_di_mariana`**
- A+ ghost `pieve_sartene_plaine_orientale` → **retag mécanique `castidetta`** (Code vérifie la localisation géo : Cozzano = Taravo intérieur, retag vers la pieve correspondante du JSON)
- R-1 `pieve_bastia` → **`pieve_lota`**

État de référence à figer avant modification :

```bash
git status
git log --oneline -5
```

Aucune divergence inattendue : Cowork ne touche pas si HEAD detached, conflits
ou commits anonymes (cf. CLAUDE.md §règle merge).

---

## 1. Phase QW — Quick wins mécaniques

### Fichiers touchés

```
_drafts/pieves_communes_mapping_v2_canonicite_casta.json   (source)
docs/data/pieves_polygons.json                              (dérivé)
```

### QW-1 · Stats correctes

Régénération propre via le pipeline :

```bash
python3 scripts/build_pieves_polygons.py --tolerance 0.0005
```

Vérifier après build :

- `stats.pieves_count == len(pieves)` (47 attendu après QW-4)
- `stats.total_communes` recalculé
- Aucune `commune_not_found_in_geo`

Si Soleil ne veut pas régénérer, patcher manuellement
`docs/data/pieves_polygons.json` :

```jsonc
"stats": {
  "pieves_count": 47,    // était 44
  "total_communes": <recalculé à partir de sum communes_count>,
  ...
}
```

### QW-2 · Mojibake

Dans `_drafts/pieves_communes_mapping_v2_canonicite_casta.json`, chercher les
deux occurrences cassées et remettre l'UTF-8 propre :

```
"SartÃƒÆ’Ã‚Â¨ne"   → "Sartène"
"SorroinsÃƒÆ’Ã‚Â¹" → "Sorroinsù"
```

Vérifier que le fichier reste valide UTF-8 sans BOM (les autres entrées doivent
rester intactes) :

```bash
python3 -c "import json; json.load(open('_drafts/pieves_communes_mapping_v2_canonicite_casta.json'))"
file _drafts/pieves_communes_mapping_v2_canonicite_casta.json
```

Régénérer ensuite `pieves_polygons.json`.

### QW-3 · Diocèses manquants

Dans le **mapping amont** (le JSON dérivé sera reconstruit) :

```
pieve_cauro   → diocese_medieval = "Ajaccio"
pieve_talavo  → diocese_medieval = "Ajaccio"
pieve_verde   → diocese_medieval = "Aleria"
```

Si la structure du mapping ne stocke pas `diocese_medieval` mais le déduit
ailleurs, intervenir dans `build_pieves_polygons.py` (au point où le diocese
est déduit) plutôt que de patcher le JSON dérivé directement.

### QW-4 · Sort de `pieve_verde`

**Si arbitrage = supprimer** :

```bash
# 1. Retirer pieve_verde du mapping amont
#    _drafts/pieves_communes_mapping_v2_canonicite_casta.json
# 2. Retirer pieve_verde de _drafts/PIEVE_OVERRIDES.json (si présente)
# 3. Retirer pieve_verde de _drafts/PIEVE_DOYENNES_OVERRIDES.json
# 4. Régénérer pieves_polygons.json
# 5. Vérifier qu'aucun site dans sites_patrimoine.json ne référence pieve_verde
python3 -c "
import json
sites = json.load(open('docs/data/sites_patrimoine.json'))['sites']
hits = [s for s in sites if s.get('pieve_slug')=='pieve_verde']
print('Sites pieve_verde:', len(hits))
"
```

**Si arbitrage = réhydrater** : ajouter les communes manquantes dans le mapping
amont (zone rive droite Tavignano, à valider avec Soleil quelles communes), puis
régénérer.

### QW-5 · Préfixe « Pieve di » normalisé hors

Cible : `docs/data/pieves_polygons.json`, champ `name` uniquement.
**Ne pas toucher aux `slug`.**

Patch à appliquer dans le mapping amont si le `name` y est défini, sinon dans
le script `build_pieves_polygons.py` (probable : la transformation
`name = "Pieve di " + base` y est codée). Ces 8 noms passent à :

```
pieve_mezzana    name → "Mezzana"
pieve_celavo     name → "Celavo"
pieve_tavagna    name → "Tavagna"
pieve_casacconi  name → "Casacconi"
pieve_filosorma  name → "Filosorma"
pieve_luri       name → "Luri"
pieve_talcini    name → "Talcini"
pieve_aleria     name → "Aleria"   (puis cf. R-5 pour collision diocèse)
```

### Validation Phase QW

```bash
# JSON valide
python3 -c "import json; json.load(open('docs/data/pieves_polygons.json'))"

# Count cohérent
python3 -c "
import json
d=json.load(open('docs/data/pieves_polygons.json'))
assert d['stats']['pieves_count']==len(d['pieves']), 'stats mismatch'
print('OK pieves_count:', d['stats']['pieves_count'])
"

# Aucun site n'a un pieve_slug fantôme
python3 -c "
import json
pp=json.load(open('docs/data/pieves_polygons.json'))
declared={p['slug'] for p in pp['pieves']}
sites=json.load(open('docs/data/sites_patrimoine.json'))['sites']
ghosts=[s['slug'] for s in sites if s.get('pieve_slug') and s['pieve_slug'] not in declared]
print('Ghost-pieve sites:', len(ghosts))
for g in ghosts[:10]: print(' ', g)
"
```

Le ghost slug `pieve_sartene_plaine_orientale` (1 site `castidetta`, Cozzano)
est connu — à corriger en `pieve_sartene` OU à acter comme nouvelle pieve si
un découpage fin de la plaine orientale est voulu. **`[ARBITRAGE complémentaire]`**.

### Commit suggéré

```
data: phase QW refactor pieves — stats, mojibake, diocèses, prefix

- stats.pieves_count → 47 (était 44)
- name fix Sartène / Sorroinsù
- diocese_medieval ajouté pour cauro, talavo, verde
- préfixe "Pieve di" retiré des 8 names concernés
- pieve_verde [supprimée OU réhydratée selon arbitrage 1]

Ref: ADR-001, PIEVES_REFACTOR_PLAN_2026-05-17
```

---

## 2. Phase D-3 — Re-alignement doyennés déclarés / réels

### Cible

`_drafts/pieves_communes_mapping_v2_canonicite_casta.json` : aligner les
`doyenne_majoritaire_declared` sur les `actual` du JSON dérivé pour les trois
pièves reclassées :

```
pieve_bastia    → doyenne_du_cap
pieve_verde     → doyenne_extreme_sud   (si réhydratée seulement)
pieve_vivario   → doyenne_cortenais
```

`doyenne_de_bastia` (qui n'existe pas comme doyenné contemporain) doit
disparaître du mapping en même temps.

Régénérer `pieves_polygons.json`. Le bloc
`doyenne_majoritaire_reclassed` doit devenir vide ou ne contenir que les
nouvelles reclassifications éventuelles.

### Commit suggéré

```
data: phase D-3 — aligner doyennés déclarés sur intersection réelle

Trois reclassifications déclarées → actual :
- pieve_bastia  : doyenne_de_bastia (fantôme) → doyenne_du_cap
- pieve_verde   : prunelli_taravo_valinco → extreme_sud
- pieve_vivario : ajaccio → cortenais

doyenne_de_bastia retirée (n'existe pas comme doyenné contemporain).
```

---

## 3. Phase R — Renommages

**Débloquée** : arbitrages 1-4 + complémentaire + R-1 actés 2026-05-17.

Pour chaque renommage qui passe l'arbitrage, la procédure est la même :

### Procédure générique R-X

Pour un renommage `pieve_OLD` → `pieve_NEW` :

1. **Mapping amont** : remplacer toutes occurrences `pieve_OLD` →
   `pieve_NEW` dans :
   - `_drafts/pieves_communes_mapping.json`
   - `_drafts/pieves_communes_mapping_v2_canonicite_casta.json`
   - `_drafts/PIEVE_OVERRIDES.json`
   - `_drafts/PIEVE_DOYENNES_OVERRIDES.json`

2. **Régénérer** `docs/data/pieves_polygons.json` via
   `python3 scripts/build_pieves_polygons.py`.

3. **Retag sites** : dans `docs/data/sites_patrimoine.json`, remplacer
   `"pieve_slug": "pieve_OLD"` → `"pieve_slug": "pieve_NEW"`.

   Vérification :

   ```bash
   python3 -c "
   import json
   sites=json.load(open('docs/data/sites_patrimoine.json'))['sites']
   from collections import Counter
   c=Counter(s.get('pieve_slug') for s in sites)
   print('pieve_OLD :', c.get('pieve_OLD',0), '(attendu 0)')
   print('pieve_NEW :', c.get('pieve_NEW',0))
   "
   ```

4. **Alias hash** : ajouter une entrée dans
   `docs/data/pieve_aliases.json` (création du fichier si absent) :

   ```json
   {
     "version": "v1",
     "generated": "2026-05-17",
     "aliases": {
       "pieve_OLD": "pieve_NEW"
     }
   }
   ```

5. **Patch `patrimoine.html`** : après le `fetch` de `pieves_polygons.json`,
   ajouter un fetch + map d'alias et passer le hash entrant par cette map
   dans `applyHash()` (~ligne 1993). Squelette d'implémentation :

   ```js
   // Après les fetch existants, AVANT le bloc Brief 15 « pret pour applyHash »
   let PIEVE_ALIASES = {};
   fetch(resolveAssetPath('docs/data/pieve_aliases.json'))
     .then(r => r.ok ? r.json() : {aliases: {}})
     .then(d => { PIEVE_ALIASES = d.aliases || {}; })
     .catch(() => {});

   // Dans applyHash(), AVANT le parse <doyenne>/<pieve>/<spot>
   function aliasResolve(slug) {
     return PIEVE_ALIASES[slug] || slug;
   }
   ```

   Appliquer `aliasResolve()` au token pieve extrait du hash.

6. **Recherche orpheline** : grep pour s'assurer que `pieve_OLD` ne traîne
   nulle part ailleurs :

   ```bash
   grep -rn "pieve_OLD" --include='*.html' --include='*.json' --include='*.js' --include='*.py' . | \
     grep -v 'pieve_aliases.json' | grep -v '.claude/worktrees/'
   ```

   Si match en dehors des fichiers de test ou des recovery `.md`, traiter.

### Renommages à appliquer (selon arbitrages)

| Réf | OLD             | NEW (proposé)              | Sites à retag | Condition          |
|-----|-----------------|----------------------------|---------------|--------------------|
| R-1 | `pieve_bastia`  | `pieve_lota`               | 6             | Acté 2026-05-17 |
| R-3 | `pieve_ajaccio` | `pieve_gulfo_d_aiacciu`    | 12            | Acté 2026-05-17 |
| R-4 | `pieve_mariana` | `pieve_piana_di_mariana`   | 8             | Acté 2026-05-17 |

### Cas particulier ghost slug

Indépendamment de R-1/R-3/R-4, le slug **fantôme**
`pieve_sartene_plaine_orientale` (1 site `castidetta` à Cozzano) doit être
résolu :

- si `[ARBITRAGE complémentaire]` = corriger : retag site
  `castidetta` → `pieve_sartene` (ou `pieve_carbini` selon localisation
  géographique réelle de Cozzano — à vérifier).
- si `[ARBITRAGE complémentaire]` = créer la pieve : ajouter
  `pieve_sartene_plaine_orientale` au mapping amont avec son périmètre.

Recommandation Cowork : **corriger en retag**. Cozzano est en pleine montagne
intérieure (Taravo), pas en plaine orientale. Le ghost slug est très
probablement un résidu d'un brief antérieur (le worktree
`fix+patrimoine-plaine-orientale-fusion-3pieves` le confirme).

---

## 4. Phase ALIAS — fichier `pieve_aliases.json`

Après toutes les Phase R appliquées, fichier final :

```json
{
  "version": "v1",
  "generated": "2026-05-17",
  "note": "Aliases de redirection des anciens slugs pieve. Conservés jusqu'à la refonte post-FEDER. Lecture côté patrimoine.html avant applyHash().",
  "aliases": {
    "pieve_bastia":   "pieve_lota",
    "pieve_ajaccio":  "pieve_gulfo_d_aiacciu",
    "pieve_mariana":  "pieve_piana_di_mariana"
  }
}
```

Lecture dans `patrimoine.html` : cf. §3 procédure générique étape 5.

---

## 5. Phase déférée — DOC seulement

Ces points ne sont pas exécutés Phase 1 beta, mais notés dans un fichier
explicatif :

- Asymétrie Balagne / Filosorma (D-1, D-2) — ajouter une note méthodologique
  dans `patrimoine.html` (popup info) :

  > « Le découpage Tellux suit l'inventaire Casta comme référence, mais
  > s'en écarte là où la lisibilité géographique l'impose. La Balagne reste
  > non subdivisée en Phase 1 beta. »

- Collisions résiduelles `pieve_aleria`, `pieve_nebbiu` (R-5) — ajouter
  un champ `note_collision_slug` dans chacune des deux entrées du JSON,
  avec la phrase : « collision volontaire en Phase 1, refonte prévue
  post-FEDER ».

- Cas `pieve_bonifacio` vs `pieve_freto` (R-2 statu quo recommandé) —
  ajouter un champ `note_decoupage` dans `pieve_bonifacio` :
  « périmètre ville + littoral ; `pieve_freto` couvre l'arrière-pays rural ».

---

## 6. Tests visuels post-refactor

Après exécution, vérifier dans le navigateur :

1. Ouvrir `patrimoine.html` directement (pas via `app.html`).
2. Console JS sans erreur.
3. Drill-down doyenné → pieve toujours fonctionnel sur les 9 doyennés.
4. Hash URL `#doyenne_du_cap/pieve_bastia` redirige vers `#doyenne_du_cap/pieve_lota`
   (si R-1 acté).
5. Hash URL `#doyenne_du_cap/pieve_lota` ouvre la pieve directement.
6. Aucun marker patrimoine sans pieve assignée (sauf les 26 connus avec
   `pieve_slug = null`).

---

## 7. Résumé exécutable

```
[1] Lire ADR-001 + PIEVES_REFACTOR_PLAN (arbitrages actés)
[2] git status / log → état propre
[3] Phase QW (~1h)        — commit "data: phase QW refactor pieves"
[4] Phase D-3 (~30 min)   — commit "data: phase D-3 doyennés alignés"
[5] Phase R (~2h)         — commits séparés par renommage (R-1, R-3, R-4)
[6] Phase ALIAS (~30 min) — commit "feat: aliases hash pieves + patrimoine.html"
[7] Phase déférée DOC     — commit "docs: notes décisions différées pieves"
[8] Tests visuels         — confirmation Soleil
[9] PR dev → main          — confirmation explicite Soleil (CLAUDE.md merge)
```

**Total Code estimé** : 4-5 h sur une session propre, hors arbitrages.

---

**Fin de la liste exécutable.** Pour toute déviation par rapport à ce plan,
référer à Soleil avant action.
