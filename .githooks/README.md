# `.githooks/` — hooks git versionnés (partagés)

Hooks git **committés** dans le repo (donc partagés à tous les clones et toutes
les sessions), activés via `core.hooksPath` plutôt que `.git/hooks/` (qui est
local et non partagé).

## Activation (à faire une fois par clone)

`core.hooksPath` est une config **locale** (elle n'est pas committée). Chaque
clone / poste doit l'activer :

```sh
git config core.hooksPath .githooks
```

Vérifier : `git config --get core.hooksPath` doit renvoyer `.githooks`.

> Le chemin est relatif à la racine du working tree, donc il fonctionne aussi
> dans les worktrees liés (le dossier `.githooks/` est présent dans chaque
> checkout).

## Hooks

### `pre-commit` — garde detect-and-signal (concurrence + hygiène de staging)

Garde-fou **déterministe** contre les collisions multi-sessions et les ajouts
fantômes. Il **détecte et bloque**, il ne **corrige jamais** (aligné sur la
doctrine detect-and-signal).

Dans l'ordre :

1. **Lock** — si `.git/index.lock` (chemin résolu par worktree) existe → **abort**.
   Le hook **ne supprime pas** le lock.
2. **Visibilité** — affiche la liste complète des fichiers stagés
   (`git diff --cached --name-status`) avant le commit.
3. **Allowlist de chemins** — si un fichier stagé tombe sous un répertoire de
   tête **inconnu** (hors `.github .githooks _data _migrations _scripts assets
   docs public scripts skills tests tools` + fichiers racine) → **abort** et
   demande de confirmation explicite (ajouter à l'allowlist, ou
   `git commit --no-verify` après vérification).
4. Sinon → laisse passer.

**Limite assumée** : le check *lock* est la défense principale contre les
sessions concurrentes ; l'allowlist ne rattrape que les fichiers
hors-arborescence, pas un fichier légitime stagé par une *autre* session. Le
correctif définitif de la collision d'index reste les **worktrees séparés par
agent** (hors périmètre de ce hook, à planifier post-FEDER).

Le hook ne modifie jamais l'index et ne supprime aucun lock — **detect-and-signal
uniquement**, aucune écriture destructive.
