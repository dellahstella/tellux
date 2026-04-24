# Refresh antennes Corse — documentation opérationnelle

**Workflow :** [.github/workflows/refresh-antennes.yml](../../.github/workflows/refresh-antennes.yml)
**Script producteur :** [scripts/build_antennes_par_commune_corse.py](../../scripts/build_antennes_par_commune_corse.py)
**Fichier produit :** `public/data/antennes_par_commune_corse.json`
**Ticket résolu :** `ANTENNES-REFRESH-001` (Option 2 GitHub Actions)

---

## 1. Objectif

Régénérer automatiquement le JSON agrégé des antennes ANFR de Corse indexées par commune INSEE, de sorte que `mairies.html` (bloc Antennes de la Fiche commune) dispose toujours d'une vue à jour sans intervention humaine mensuelle.

Le JSON est une vue **dérivée** de la table Supabase `antennas_corse`, filtrée et agrégée. Les mises à jour de la table elle-même (ajout ou correction d'antennes) restent manuelles — ce workflow ne modifie pas Supabase, il se contente de re-lire et de re-publier le JSON dérivé.

---

## 2. Cadence

- **Automatique** : 1er jour de chaque mois à 04h00 UTC (cron `0 4 1 * *`). Tombe en pleine nuit heure européenne pour éviter l'activité utilisateur.
- **Manuel** : à tout moment via l'interface GitHub Actions (voir §4).

GitHub peut parfois retarder légèrement l'exécution programmée en cas de forte charge de la plateforme (délai typique < 1 h, documenté par GitHub).

---

## 3. Secrets requis (à configurer par Soleil)

Avant le premier run, configurer dans **Settings > Secrets and variables > Actions** du repo `dellahstella/tellux` :

| Nom du secret | Valeur | Commentaire |
|---|---|---|
| `SUPABASE_URL` | `https://knckulwghgfrxmbweada.supabase.co` | URL publique du projet Supabase Tellux |
| `SUPABASE_ANON_KEY` | clé anon du projet (longue chaîne JWT) | Lecture seule RLS. Cette clé est déjà dans `app.html` côté client, mais l'injecter en secret GitHub Actions est plus propre (pas dans les logs de build) |

**Note** : le script `build_antennes_par_commune_corse.py` a un fallback hardcodé sur la clé anon actuelle, donc même sans secrets configurés, le workflow fonctionnera. Les secrets servent à éviter de dépendre des valeurs hardcodées si on rotate la clé plus tard.

Le workflow **n'a pas besoin** de la clé `service_role` (pas d'UPDATE, uniquement un SELECT). La clé anon suffit.

---

## 4. Déclenchement manuel

1. Ouvrir le repo sur GitHub : `https://github.com/dellahstella/tellux`
2. Onglet **Actions**
3. Menu de gauche : **refresh-antennes**
4. Bouton **Run workflow** (en haut à droite)
5. Sélectionner la branche `dev` (par défaut), puis cliquer **Run workflow**

Le job apparaît dans la liste sous 10-20 secondes. Durée d'exécution typique : **30 à 60 secondes** (fetch Supabase + geo.api.gouv.fr + agrégation).

---

## 5. Comportement attendu

Chaque run exécute 5 étapes :

1. **Checkout dev** — récupère la branche `dev` à jour
2. **Setup Python 3.11** — depuis `actions/setup-python@v5`
3. **Run build script** — lance `scripts/build_antennes_par_commune_corse.py`, qui écrit `public/data/antennes_par_commune_corse.json`
4. **Detect changes** — `git diff --quiet` sur le JSON, stocke `changed=true|false` dans `steps.diff.outputs.changed`
5. **Commit and push if changed** — si `changed=true`, commit par `github-actions[bot]` avec un message incluant le nombre d'antennes et de communes, push sur `dev`

Si le JSON n'a pas changé (cas typique si aucune antenne n'a été ajoutée dans Supabase depuis le run précédent), le workflow passe au vert sans commit. Comportement normal.

### Vérifier un run

- Onglet **Actions** > **refresh-antennes** > cliquer sur le run le plus récent
- Status vert ✓ : tout s'est bien passé
- Status rouge ✗ : échec. Consulter les logs des steps pour identifier la cause

---

## 6. Interpréter un échec

### Cas 1 : échec à l'étape `Run build script`

Causes possibles :

- **Supabase indisponible** — retry manuel quelques heures plus tard.
- **API geo.api.gouv.fr indisponible** — idem.
- **Clé anon révoquée ou expirée** — mettre à jour le secret `SUPABASE_ANON_KEY` depuis le dashboard Supabase (Settings > API).
- **Changement de schéma Supabase** — si la colonne `code_insee_commune` a été supprimée ou renommée, adapter le script. Voir `docs/data-sources/antennes_corse_notes.md`.

### Cas 2 : échec à l'étape `Commit and push if changed`

Causes possibles :

- **Protection de branche sur `dev`** — la branch protection doit autoriser `github-actions[bot]` à pusher. Dans Settings > Branches > `dev` > Require a pull request before merging, cocher "Allow specified actors to bypass required pull requests" puis ajouter `github-actions[bot]`.
- **Conflit de merge** — le bot est parti d'un `dev` désynchronisé (très rare, cadence mensuelle). Relancer le workflow manuellement.

### Cas 3 : le workflow passe au vert mais le JSON est incohérent

- Vérifier les métadonnées `_meta` du JSON committé (nombre d'antennes placées, communes avec antennes).
- Si divergence majeure avec le commit précédent (par exemple 500 antennes alors qu'on en attendait 3000), faire un rollback manuel (voir §7) et investiguer avant le run suivant.

---

## 7. Rollback manuel

Si un refresh commit un JSON dégradé :

```bash
git checkout dev
git log --oneline public/data/antennes_par_commune_corse.json | head -5
git revert <hash_du_commit_fautif>
git push origin dev
```

Ou bien restaurer un commit précédent spécifique :

```bash
git checkout <hash_bon_commit> -- public/data/antennes_par_commune_corse.json
git commit -m "revert: restauration JSON antennes vers <hash_bon_commit>"
git push origin dev
```

---

## 8. Dépendances du workflow

Le script producteur utilise uniquement la **stdlib Python** (`urllib.request`, `json`, `pathlib`, `os`, `sys`). Aucun `pip install` nécessaire. Version Python : 3.11 sur runner `ubuntu-latest`.

Les deux sources réseau consultées :
- Supabase REST API (`antennas_corse`)
- `geo.api.gouv.fr/communes` (noms des 360 communes corses, sans géométrie, ~30 KB)

---

## 9. Historique du ticket

| Date | Évènement |
|---|---|
| 2026-04-24 | Ticket `ANTENNES-REFRESH-001` ouvert (prompt Cowork) |
| 2026-04-24 | Ticket `SUPABASE-COMMUNE-FIELD-001` résolu (colonne `code_insee_commune` ajoutée, pipeline simplifié sans shapely) |
| 2026-04-24 | Résolution de `ANTENNES-REFRESH-001` : workflow GitHub Actions mensuel |

Voir aussi :
- `tellux_dettes_techniques/ANTENNES-REFRESH-001.md` (ticket d'origine)
- [docs/data-sources/antennes_corse_notes.md](../data-sources/antennes_corse_notes.md) (schéma de la table et procédure de refresh complète)

---

Fin de la documentation.
