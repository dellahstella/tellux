# Tellux — Workflow Git et déploiement

Mémo opérationnel pour le versioning et le déploiement du projet Tellux.

---

## Structure du dépôt

Tellux utilise un dépôt Git unique hébergé sur GitHub (origin) avec un mirror de sauvegarde sur GitLab. Deux branches principales, deux usages distincts :

- **`main`** — ce qui est déployé en production sur `https://tellux.pages.dev`. Contient uniquement `index.html`, `README.md`, et les JSON externalisés (`failles-corse.json`, `prod-electrique.json`, `Hypothese.json`). Cloudflare Pages surveille cette branche et redéploie automatiquement à chaque push.
- **`dev`** — branche de travail complète. Contient tout : `tellux_v6_design.html` (le HTML de travail), la documentation, les briefings, les lettres, les migrations SQL, les archives, les prompts, etc.

Le fichier `tellux_v6_design.html` sur `dev` et `index.html` sur `main` sont le même fichier, mais renommé au moment du déploiement.

---

## Remotes

```bash
git remote -v
```

- `origin` → `https://github.com/dellahstella/tellux.git` (principal, connecté à Cloudflare)
- `gitlab` → `https://gitlab.com/dellahstella/tellux.git` (mirror de sauvegarde)

---

## Workflow quotidien — travail sur `dev`

Tu es sur `dev` la plupart du temps. Tu modifies `tellux_v6_design.html`, tu ajoutes des fichiers markdown, tu fais évoluer le projet.

```bash
# Vérifier que tu es bien sur dev
git status

# Faire tes modifications dans tes éditeurs habituels
# ... travail ...

# Regarder ce qui a changé
git status
git diff tellux_v6_design.html | head -50

# Commiter les modifications
git add tellux_v6_design.html TELLUX_DOSSIER_ASSO_EM.md  # liste ciblée des fichiers à commiter
git commit -m "feat: description claire de ce qui change"

# Pousser vers les deux remotes
git push origin dev
git push gitlab dev
```

### Bonnes pratiques pour les messages de commit

Utilise un préfixe clair pour savoir de quoi parle le commit :
- `feat:` — nouvelle fonctionnalité ou nouveau contenu
- `fix:` — correction de bug
- `docs:` — modification de documentation
- `chore:` — maintenance, configuration, ménage
- `refactor:` — réorganisation de code sans changement de comportement
- `style:` — mise en forme visuelle uniquement

Exemples :
- `feat: ajout du sélecteur de culture dans le module agronomie`
- `fix: correction plage µT/nT pour Phyphox`
- `docs: mise à jour de la roadmap avec les nouvelles hypothèses`

---

## Workflow de déploiement — mettre à jour `tellux.pages.dev`

À faire chaque fois que tu veux publier une nouvelle version pour les utilisateurs. Suppose que tu es sur `dev` avec ton `tellux_v6_design.html` à jour et commité.

```bash
# 1. S'assurer que dev est bien à jour et poussé
git status                    # doit afficher "nothing to commit, working tree clean"
git push origin dev           # au cas où un commit ne serait pas encore poussé
git push gitlab dev

# 2. Basculer sur main
git checkout main

# 3. Copier le HTML de travail vers index.html
git show dev:tellux_v6_design.html > index.html

# 4. Vérifier
ls -la index.html
git status                    # doit afficher "modified: index.html"

# 5. Commiter et pousser
git add index.html
git commit -m "deploy: description courte de ce qui est livré"
git push origin main

# 6. Cloudflare Pages détecte le push et redéploie automatiquement
#    Suivi en direct : https://dash.cloudflare.com → Workers & Pages → Tellux → Deployments
#    Durée typique : 1-2 minutes

# 7. Revenir sur dev pour continuer le travail
git checkout dev
```

### Vérification post-déploiement

Une fois le déploiement terminé, ouvrir `https://tellux.pages.dev` **en navigation privée** (Ctrl+Maj+N sur Chrome, Ctrl+Maj+P sur Firefox) pour éviter le cache. Vérifier visuellement :
- Le logo est bien affiché
- La carte se charge
- Les modules attendus sont présents
- Aucune erreur dans la console (F12 → Console)

---

## Cas particulier — déployer un fichier qui n'est pas `tellux_v6_design.html`

Si tu as modifié les JSON externalisés (`failles-corse.json`, `prod-electrique.json`, `Hypothese.json`) sur `dev` et que tu veux les déployer :

```bash
git checkout main
git show dev:failles-corse.json > failles-corse.json
# ... idem pour les autres JSON si besoin
git add failles-corse.json
git commit -m "deploy: update failles-corse.json"
git push origin main
git checkout dev
```

---

## Gestion des fichiers à ne jamais commiter

Le `.gitignore` sur `dev` exclut automatiquement :
- `DATA/` — données sources (ANFR, BRGM, etc.) à conserver en local uniquement
- `SupaData-backup/` — exports de sauvegarde Supabase
- `.claude/` — fichiers internes Claude Code
- `*.exe`, `*.msix`, `*.zip` et autres binaires volumineux
- `node_modules/`, `.env`, fichiers éditeur

**Ne jamais** ajouter de dossier de données lourdes au dépôt. Si besoin de référencer des données volumineuses, préférer un lien vers la source officielle ou une externalisation en JSON compact.

---

## Récupérer un fichier depuis une autre branche

Tu es sur `dev` et tu veux voir comment un fichier était sur `main` sans basculer de branche :

```bash
git show main:index.html | head -50          # aperçu
git show main:index.html > /tmp/index_main.html  # copie pour inspection
```

Tu veux récupérer un fichier qui existe dans `dev` mais pas dans la branche actuelle :

```bash
git checkout dev -- nom_du_fichier.md
```

---

## Récupérer une version historique d'un fichier

```bash
# Voir l'historique des modifications d'un fichier
git log --oneline -- tellux_v6_design.html

# Récupérer une version spécifique (remplacer HASH par le début d'un hash de commit)
git show HASH:tellux_v6_design.html > /tmp/tellux_old.html
```

---

## Nettoyage périodique (optionnel, non urgent)

De temps en temps, pour garder le dépôt léger :

```bash
# Compacter l'historique local (sans rien supprimer)
git gc

# Supprimer les branches locales qui n'existent plus sur le remote
git fetch --prune origin
git branch --merged | grep -v '\*\|main\|dev' | xargs -n 1 git branch -d 2>/dev/null
```

---

## Résolution rapide de problèmes

### « refusing to merge unrelated histories »
C'est que deux branches n'ont pas de commits communs. Généralement résolu en créant une nouvelle branche propre à partir de l'ancêtre commun connu.

### « fatal: 'main' matched multiple (2) remote tracking branches »
Git ne sait pas si tu parles de `origin/main` ou `gitlab/main`. Soit tu crées une branche locale `main` explicitement liée à `origin/main` (`git checkout -b main origin/main`), soit tu utilises le nom complet (`git pull origin main` au lieu de `git pull main`).

### « Your local changes would be overwritten by checkout »
Tu as des modifications non commitées qui bloquent le basculement de branche. Soit tu les commit, soit tu les stashes (`git stash`), soit tu les jettes (`git checkout -- nom_fichier`).

### Avertissements « LF will be replaced by CRLF »
Purement cosmétique sur Windows. Pour les masquer définitivement :
```bash
git config --global core.autocrlf true
```

### Gros fichier accidentellement commité
**Ne jamais** pousser un commit avec un fichier de plus de 50 Mo. Si tu as fait l'erreur et que ce n'est pas encore poussé :
```bash
git reset --soft HEAD~1         # annule le dernier commit, garde les modifs
git restore --staged fichier_lourd.zip
# ajoute le fichier au .gitignore, puis recommite
```

---

## Principe général à retenir

Sur `dev`, tu travailles librement. Tu versions ta documentation, tes HTML de travail, tes migrations, tes briefings, tout ce qui constitue le projet. Tu pousses fréquemment pour sécuriser ton travail sur GitHub + GitLab.

Sur `main`, tu ne vas **que** pour déployer. Les commits y sont rares, courts, et toujours de type `deploy:`. Cloudflare Pages est le seul consommateur de cette branche.

Les deux branches vivent en parallèle. Ne jamais les merger l'une dans l'autre — `main` reste minimaliste (juste ce qui est déployé), `dev` reste complet (tout le projet).

---

*Dernière mise à jour : 13 avril 2026, après la consolidation du dépôt Git.*
