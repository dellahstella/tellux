# Prompt Claude Code — Refactor pièves Tellux Phase 1 beta

**À copier-coller dans une session Claude Code locale sur le repo `tellux`.**
**Branche cible** : `refactor/pieves-2026-05-17`
**Estimation** : 4-5 h session propre.

---

## 1. OBJECTIF

Exécuter le refactor des pièves Tellux Phase 1 beta selon les arbitrages
actés par Soleil le 2026-05-17 :

- corriger les bugs nets du JSON (stats faussées, mojibake, diocèses manquants, préfixage incohérent) ;
- supprimer `pieve_verde` (entrée fantôme) ;
- renommer 3 pièves : `pieve_bastia` → `pieve_lota`, `pieve_ajaccio` → `pieve_gulfo_d_aiacciu`, `pieve_mariana` → `pieve_piana_di_mariana` ;
- aligner les 3 doyennés déclarés sur la réalité polygonale ;
- introduire un mécanisme d'alias pour ne casser aucun hash URL public ;
- résoudre le ghost slug `pieve_sartene_plaine_orientale` par retag du site `castidetta`.

Phase 1 beta = on assume l'asymétrie Balagne/Cortenais et les collisions
résiduelles `pieve_aleria` / `pieve_nebbiu`. Tout cela est déféré post-FEDER
et documenté en notes JSON.

## 2. CONTEXTE

Trois documents complets sont déjà rédigés et arbitrés :

1. `docs/operations/ADR-001-pieves-doctrine.md` — doctrine pièves Tellux (acté).
2. `docs/operations/PIEVES_REFACTOR_PLAN_2026-05-17.md` — plan priorisé, arbitrages actés en §5.
3. `docs/operations/PIEVES_REFACTOR_EXEC_CODE_2026-05-17.md` — liste exécutable détaillée (procédure générique, commandes, fichiers, commits).

**Tu lis les trois dans l'ordre avant la première modification.** L'exec
contient les commandes shell, les patches JSON, le squelette d'alias dans
`patrimoine.html`. Pas besoin de redériver.

Données prod au moment du brief :

- `docs/data/pieves_polygons.json` : 47 pièves (47 → 46 après suppression `pieve_verde`).
- `docs/data/sites_patrimoine.json` : 541 sites, dont 26 sites à pieve_slug = null (zone d'ombre connue, ne pas chercher à corriger ici).
- Pipeline : `scripts/build_pieves_polygons.py` re-exécutable depuis `_drafts/pieves_communes_mapping_v2_canonicite_casta.json` + overrides.

## 3. MODE

**Modification autorisée** sur les fichiers listés dans l'exec §1 à §5 :

- `_drafts/pieves_communes_mapping.json`
- `_drafts/pieves_communes_mapping_v2_canonicite_casta.json`
- `_drafts/PIEVE_OVERRIDES.json`
- `_drafts/PIEVE_DOYENNES_OVERRIDES.json`
- `docs/data/pieves_polygons.json` (dérivé, idéalement régénéré)
- `docs/data/sites_patrimoine.json` (retag)
- `docs/data/pieve_aliases.json` (création)
- `patrimoine.html` (patch léger applyHash)
- `scripts/build_pieves_polygons.py` (si nécessaire pour les fixes en amont)

**Tu ne touches PAS** :

- `app.html` (canonique Phase 1 EM, hors scope)
- `index.html`
- Aucune des fonctions `calc*` du corpus scientifique
- `_corpus/` (et tu ne crées rien dedans)
- Les autres fichiers de `docs/data/` non listés (antennes, cartoradio, eoliennes…)

## 4. ÉTAPES NUMÉROTÉES

Suivre l'ordre du §7 de l'exec, sans dévier :

```
[1] git checkout dev && git pull
[2] git checkout -b refactor/pieves-2026-05-17
[3] Lire les 3 docs operations/PIEVES_*
[4] Phase QW (quick wins N1-N5)          → commit "data: phase QW refactor pieves"
[5] Phase D-3 (re-alignement doyennés)   → commit "data: phase D-3 doyennés alignés"
[6] Phase R-1 (pieve_bastia → lota)      → commit "data: rename pieve_bastia → pieve_lota"
[7] Phase R-3 (pieve_ajaccio → gulfo)    → commit "data: rename pieve_ajaccio → pieve_gulfo_d_aiacciu"
[8] Phase R-4 (pieve_mariana → piana)    → commit "data: rename pieve_mariana → pieve_piana_di_mariana"
[9] Phase A+ (ghost castidetta retag)    → commit "data: fix ghost pieve_sartene_plaine_orientale"
[10] Phase ALIAS (pieve_aliases + patch patrimoine.html) → commit "feat: aliases hash pieves + applyHash"
[11] Phase déférée DOC (notes JSON)      → commit "docs: notes décisions différées pieves"
[12] Tests visuels patrimoine.html       → rapport en chat
[13] STOP — attente confirmation Soleil avant push origin et PR
```

Pour chaque phase, **valider avant commit** :

```bash
python3 -c "import json; json.load(open('docs/data/pieves_polygons.json'))"
python3 -c "import json; json.load(open('docs/data/sites_patrimoine.json'))"
# Validation cohérence : 0 site avec pieve_slug fantôme
python3 -c "
import json
pp=json.load(open('docs/data/pieves_polygons.json'))
declared={p['slug'] for p in pp['pieves']}
declared.update({'pieve_verde'} if False else set())  # ajuster si verde supprimée
sites=json.load(open('docs/data/sites_patrimoine.json'))['sites']
ghosts=[s['slug'] for s in sites if s.get('pieve_slug') and s['pieve_slug'] not in declared]
assert not ghosts, f'ghosts: {ghosts}'
print('OK no ghost pieve_slug')
"
```

## 5. RÈGLES STRICTES

- Lire les 3 docs PIEVES_* **avant** la première modification, en entier (pas de skimming).
- `git status` propre avant chaque commit (pas de mix de phases dans un commit).
- 1 commit = 1 phase (cf. étapes 4 à 11).
- Après chaque commit, exécuter le bloc de validation JSON ci-dessus. Si JSON invalide → `git restore` du fichier cassé, diagnostiquer, recommencer (cf. feedback Cowork pertes silencieuses).
- Aucun guillemet courbe (U+2018/U+2019) dans les patches JS de `patrimoine.html` — uniquement `'` et `"` droits.
- Aucune dépendance externe ajoutée (pas de CDN, pas de pip install) sauf si déjà présente.
- Ne pas modifier le pipeline `build_pieves_polygons.py` sans nécessité claire — si une étape demande de patcher le script, le faire et l'appeler explicitement dans le commit.
- Ne pas régénérer `pieves_polygons.json` à la main par éditeur si tu peux passer par le script. Si tu patches à la main (Phase QW notamment), explicite-le dans le message de commit.
- Encodage : tout fichier JSON reste UTF-8 sans BOM.
- Ne créer aucun fichier .md de session si pas demandé.
- Ne pas push `origin` ni ouvrir de PR avant confirmation Soleil (étape 13).
- Ne pas merger sur `dev` ni `main` sans confirmation explicite Soleil au format défini dans `CLAUDE.md` (§règle merge).
- Si tu détectes une situation imprévue (HEAD detached, divergence inattendue, conflit non résolu, commit anonyme) : règle « je-ne-sais-pas », STOP et signale.

## 6. POINT DE VALIDATION

**Trois points d'arrêt obligatoires** :

1. **Après Phase QW (étape 4)** : exécuter le bloc de validation, montrer le diff `git diff HEAD~1` à Soleil, attendre OK avant Phase D-3.
2. **Après Phase R complète (étapes 6 à 9)** : montrer le retag de sites (top 10 par pieve avant/après), confirmer 0 ghost slug, attendre OK avant Phase ALIAS.
3. **Étape 13** : tests visuels patrimoine.html (cf. exec §6), rapport en chat, attendre OK avant `git push origin refactor/pieves-2026-05-17` et avant ouverture PR `dev → main`.

Si l'un des arrêts révèle une régression, STOP et reporte à Soleil. Pas
d'improvisation sur le découpage géographique : tout choix non couvert par
les 3 docs PIEVES_* est arbitré par Soleil, pas par toi.

## 7. LIVRABLES ATTENDUS

À la fin de la session, en chat :

- branche `refactor/pieves-2026-05-17` poussée (après OK étape 13) ;
- 8 commits modulaires (un par phase) ;
- rapport synthétique : phases exécutées, anomalies rencontrées, fichiers touchés, points d'attention pour la PR ;
- validation visuelle patrimoine.html : drill-down doyenné → pieve sur les 9 doyennés, redirection hash `pieve_bastia` → `pieve_lota` fonctionnelle, aucun marker orphelin (hors 26 connus null) ;
- PR ouverte (mais non mergée) avec lien dans le rapport ;
- ne pas créer de recovery .md (pas la peine pour ce volume).

---

**Fin du prompt.**

En cas d'ambiguïté en cours de session : référer à
`docs/operations/PIEVES_REFACTOR_EXEC_CODE_2026-05-17.md` qui contient la
procédure générique de renommage (§3) et la procédure d'alias (§4). Pour
toute déviation, demander à Soleil.
