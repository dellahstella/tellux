# Tellux — Workflow Git et déploiement

Mémo opérationnel pour le versioning et le déploiement du projet Tellux.

---

## Structure du dépôt

Tellux utilise un dépôt Git unique hébergé sur GitHub (origin). Le remote GitLab est désactivé depuis le 14 avril 2026. Deux branches principales, deux usages distincts :

- **`main`** — ce qui est déployé en production sur `https://tellux.pages.dev`. Cloudflare Workers surveille cette branche et redéploie automatiquement à chaque push. Fichiers déployés : `app.html`, `index.html`, `patrimoine.html`, `agronomie.html`, `public/data/*.json`, `wrangler.jsonc`.
- **`dev`** — branche de travail complète. Contient toute la documentation, les briefings, les lettres, les migrations SQL, les archives, les scripts, etc.

Le déploiement se fait **uniquement par Pull Request** → `dev` → `main` (non-squash merge, validé par Soleil). **Push direct sur `main` interdit.**

---

## Remotes

```bash
git remote -v
```

- `origin` → `https://github.com/dellahstella/tellux.git` (seul remote actif, connecté à Cloudflare)

Le remote GitLab est désactivé depuis le 2026-04-14. Ne pas le rebrancher.

---

## Workflow quotidien — travail sur `dev`

Les sessions Claude Code travaillent sur des **branches éphémères** (`feat/...`, `fix/...`, `chore/...`) créées à partir de `dev`. Elles ne poussent jamais directement sur `dev` ou `main`.

```bash
# Créer une branche éphémère
git checkout dev
git checkout -b feat/ma-fonctionnalite

# Faire les modifications
# ...

# Commiter
git add app.html public/data/nouveau_fichier.json
git commit -m "feat: description claire"

# Pousser la branche
git push origin feat/ma-fonctionnalite

# Créer la PR vers dev (via gh ou GitHub)
gh pr create --base dev --title "feat: ..."
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

Le déploiement se fait par **PR `dev` → `main`**, mergée par Soleil. Cloudflare Workers détecte le push sur `main` et redéploie automatiquement (durée typique : 1–2 minutes).

```bash
# Créer la PR de déploiement (Claude Code crée, Soleil merge)
gh pr create --base main --head dev --title "deploy: v2.x.x — description courte"
```

Vérification post-déploiement : ouvrir `https://tellux.pages.dev` en navigation privée (éviter le cache). Vérifier :
- La carte se charge (IGN Plan V2)
- Popup fonctionnelle sur un clic
- Aucune erreur JS dans la console (F12)

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

*Dernière mise à jour : 21 avril 2026.*
