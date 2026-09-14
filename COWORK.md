# COWORK.md — Mode opératoire Cowork sur Tellux

Lecture obligatoire au démarrage de chaque session Cowork. Synthèse des apprentissages de 18 sessions (24 avril → 9 mai 2026), dont 6 ont perdu en bloc leur production (~250+ markdowns).

## DÉMARRAGE OBLIGATOIRE (avant toute action)

```bash
bash scripts/cowork_start.sh "[description session]"
```

→ Copier la sortie dans le chat avant de continuer.
Si « HEAD DETACHÉ » : signaler à Soleil avant de produire quoi que ce soit.

## FERMETURE OBLIGATOIRE (dernière action)

```bash
bash scripts/cowork_end.sh
```

→ Copier la sortie complète dans le chat.
Si 🔴 SENTINEL ABSENT : vérifier chaque fichier produit via `ls -la` avant de fermer.

## TL;DR (à appliquer sans réflexion)

1. **`git status` + `git log --oneline -10`** avant toute production. Sinon tu ignores ce que Code a shippé en parallèle.
2. **Sentinel persistance** au démarrage. Si l'aller-retour échoue, alerte Soleil et ne commence pas la production.
3. **Aucune opération git d'écriture** côté Cowork (mode FUSE permanent). Pas de `commit`, `stash`, `checkout`, `reset`, `push`.
4. **Vérifier la présence physique** des fichiers via `find` ou `ls` après chaque batch — un `Write succeeded` ne garantit pas la persistance.
5. **Si 200+ fichiers `M` avec pattern `+N/-N` symétrique** → c'est CRLF, pas du contenu. Ne rien commit, ne rien stash, ne pas paniquer.
6. **Convention canonique fiches** : `fiches_patrimoine/{pieves,dioceses}/*_v[23].md`. **Pas** `docs/fiches_sites/` ni `docs/ethnologie-comparee/`.

## Au démarrage de session

### 1. Cartographier l'état réel

```bash
cd /sessions/<id>/mnt/Tellux/   # chemin Linux mappé
git status --short | head -30
git log --oneline -10
git stash list
git branch --show-current       # vide = HEAD detached
```

Trois cas à signaler à Soleil avant d'écrire :

- **HEAD detached** → Soleil doit checkout une branche d'abord (`git switch -c <feature>`). Sinon les fichiers que tu écris peuvent être balayés par un `git checkout` mid-session.
- **`.git/index.lock` présent** → autre session git en cours. Bascule en mode propositions chat, pas d'édition JSON directe sur les fichiers tracked.
- **Stash existant inattendu** → lire le nom. Ne JAMAIS pop sans validation Soleil. Le stash `main-tree-cleanup-2026-05-08-pre-orphan-deletion` notamment est un point de sauvegarde Soleil.

### 2. Poser un sentinel persistance

```bash
SENTINEL="/sessions/<id>/mnt/Tellux/_drafts/_cowork_sentinel_$(date +%s).txt"
echo "session_$(date -Iseconds)" > "$SENTINEL"
ls -la "$SENTINEL"
```

Si `ls` échoue ou si le fichier disparaît dans les 10 secondes → bug FS de la session, alerte Soleil avant toute production substantielle. Conserver `$SENTINEL` pour le `find -newer` de fin de session.

### 3. Lire les sources de vérité

- `COWORK.md` (ce fichier).
- `.claude/CLAUDE.md` (instructions locales projet, règles synchro corpus privé).
- Issues GitHub en retard : `gh issue list --label triage-rollup` — rollup unique toujours à jour des issues `routine` en retard de plus de 14 jours (circuit brief O, `.github/workflows/routine-triage.yml`).
- `CHARTE_DECISION.md` (autonomie crans A/B/C) + `DECISIONS.md` (ADR projet) — défaut = action, STOP = exception Cran C. Cowork reste en écriture-fichiers-seule (aucune op git, cf. § « Ce que tu ne fais JAMAIS »).
- Mémoire Cowork (`MEMORY.md` et fichiers indexés).
- Le brief Soleil **dans son intégralité** avant la première écriture.
- Si le brief mentionne `tellux_FINAL_CLEAN1.html`, lire le fichier en entier ou les zones cibles via grep avant patcher.

## Pendant la production

### Convention de chemins

- **Préférer les chemins Linux mappés** (`/sessions/.../mnt/Tellux/...`) aux chemins Windows (`C:\Users\lucas\...`) pour les Write critiques. Bug constaté : Write Windows retourne succès sans persistance dans certaines sessions.
- **Si un Write Windows échoue silencieusement**, basculer sur bash + chemin Linux pour le même fichier.

### Convention d'arborescence

| Contenu | Chemin canonique |
|---|---|
| Fiches pieve | `fiches_patrimoine/pieves/<slug>_v[23].md` |
| Fiches diocèses | `fiches_patrimoine/dioceses/<slug>_v[23].md` |
| Doc 2 hypothèses | le clone privé, `docs/corpus_scientifique/00_canon/TELLUX_HYPOTHESES_PROTOCOLES.md` (jamais mounté Cowork) |
| Sites canoniques | `docs/data/sites_patrimoine.json` (source de vérité runtime patrimoine depuis le Brief 33 split, 2026-05-06 ; `sites_corse.json` est DEPRECATED, aucun consommateur runtime, cf. `ARCHITECTURE.md` §3.bis) |
| Drafts éphémères | `_drafts/` |
| Livrables Cowork hors repo | dossiers de travail locaux gitignorés (voir `.gitignore` à la racine) ou `audits/` — propagation manuelle vers le clone privé |
| Scratch session | `outputs/` (mount Cowork, ne survit pas) |

### Vérification continue

À chaque batch de 5-10 fichiers écrits, faire :

```bash
find . -newer "$SENTINEL" -type f -name "*.md" | head -30
```

Si la liste est vide alors que tu viens d'écrire 10 fichiers → tu es dans le pattern de perte des rapports 6, 8, 9, 10, 11, 12. **Arrêter, alerter Soleil, basculer sur bash + chemin Linux pour réécrire.**

### Coexistence Cowork ↔ Code

Si Soleil mentionne qu'une session Code tourne, ou qu'un autre Cowork peut écrire :

- `git log --oneline -5` toutes les 30 minutes.
- Mode propositions documentées en chat sur les fichiers tracked critiques (`docs/data/*.json`, `app.html`, `patrimoine.html`, `cadre-scientifique.html`).
- **Pattern A1 (annoncer avant vérifier) touche Cowork ET Code.** Brief 39decies a été produit deux fois : une par Code (commit `bd59afd`, PR #406) et une par Cowork sans visibilité, l'EOL CRLF a masqué la duplication. Ne jamais annoncer un fichier shippé sans `git diff --ignore-cr-at-eol --stat` réel.
- **Anomalie git = detect-and-signal, jamais correction (v4.5 — carve-out #10 / A.2 bis).** Un `.git/index.lock` présent, ou des fichiers stagés fantômes (que cette session n'a pas produits), signalent une **session Code concurrente probable** : **signaler à Soleil, ne jamais corriger** — ne pas supprimer le lock, ne pas dé-stager, ne pas « nettoyer » l'index. Cowork n'écrit pas git de toute façon (mode FUSE), mais la règle est explicite. Un hook `pre-commit` versionné (`core.hooksPath=.githooks`, PR #910) garde les commits côté Code ; pour être couvert côté sandbox Cowork, lancer **une fois** `git config core.hooksPath .githooks` (config locale non committée).

## À la fermeture de session

### Protocole standard

```bash
# 1. Liste exhaustive des fichiers touchés depuis le sentinel
find . -newer "$SENTINEL" -type f | grep -v -E '(node_modules|__pycache__|\.git/)'

# 2. Diff réel (CRLF ignoré)
git status --short | head -30
git diff --ignore-cr-at-eol --stat | head -30

# 3. Pour chaque fichier annoncé produit, Read le pour confirmer le contenu
```

### Rapport de fermeture en chat

Doit contenir :

- Liste exhaustive des fichiers produits **ET vérifiés présents physiquement**.
- État `git status` réel — distinguer artefacts CRLF des modifs sémantiques (`git diff --ignore-cr-at-eol`).
- Distinguer trois catégories : (A) fichiers de cette session, (B) fichiers de tests résiduels, (C) état pré-existant des autres sessions.
- Suggestions de commit thématiques avec messages prêts à coller, branches cibles. Soleil exécute, jamais Cowork.
- Stashs suggérés si pertinent. Idem, Soleil exécute.
- Anomalies détectées (perte FS, lock git, EOL massif, etc.).

### Ce qu'on ne fait JAMAIS au moment de fermer

- Lancer `git stash`, `git commit`, `git push` côté Cowork.
- Annoncer un fichier produit sans avoir fait un `find` qui confirme sa présence.
- Considérer qu'un `Write succeeded` = fichier sur disque.
- Suggérer de commit l'ensemble du `git status` sans triage thématique (200+ fichiers M = CRLF la plupart du temps).
- Stasher des fichiers qui n'ont pas été produits par cette session (les autres sessions vivent dans le worktree, ne pas les balayer).

## Ce que tu ne fais JAMAIS

### Côté git

- `git checkout`, `git reset --hard`, `git checkout origin/main -- <fichier>` — cause documentée du HEAD detached.
- `git commit`, `git push`, `git stash`, `git add` — mode FUSE permanent, règle CLAUDE.md projet §9.
- Toucher au stash existant tant que Soleil n'a pas validé sa lecture.

### Côté code Tellux

- Modifier le HTML applicatif sans avoir lu le brief en intégralité ET sans avoir confirmé avec Soleil quel fichier est la source de vérité courante. La cible varie selon les phases : `app.html`, `patrimoine.html`, `cadre-scientifique.html` etc. en multi-pages depuis ~mai 2026 ; les versions mono-fichier (`tellux_FINAL_CLEAN1.html`, `tellux_v6_design.html`, `tellux_CORRECT.html`) sont historiques. **Toujours demander à Soleil quel fichier viser avant d'éditer du HTML applicatif.**
- Modifier les données scientifiques : `SITES`, `CHURCHES`, `FAILLES_CORSE`, `HYPOTHESES`, `PROD_ELECTRIQUE`.
- Modifier les fonctions de calcul : `calcHuman()`, `calcHeritagePiezo()`, `runAutoTests()`, `runPermaDiag()`, etc.
- Ajouter des dépendances externes (CDN, npm) sans validation Soleil. Seule exception : Google Fonts (Fraunces, IBM Plex Sans, JetBrains Mono).
- Créer des fichiers HTML alternatifs ou des branches.
- Modifier les coordonnées GPS, les listes de sites, les structures de données scientifiques.
- Traduire en anglais ou ajouter du contenu anglais.
- Utiliser des guillemets courbes (`'` `'` U+2018/U+2019) dans les string literals JavaScript.
- Ajouter `@media (prefers-color-scheme: dark)` (light mode forcé).

### Côté workflow

- "Nettoyer" du code que Soleil n'a pas demandé de toucher.
- Ajouter de la gamification supplémentaire ou des notifications.
- Trancher seul les décisions en attente (logo SVG définitif, refonte scoring, choix juridique entité).

## Lexique des pièges connus

| Symptôme | Cause probable | Action |
|---|---|---|
| 200+ fichiers `M`, pattern `+N/-N` symétrique | CRLF↔LF Windows/Linux | Ne rien commit ni stash. Solution durable côté Code : `.gitattributes` `* text=auto eol=lf` puis `git add --renormalize .` |
| HEAD detached at origin/main | `git checkout origin/main -- <fichier>` antérieur | Soleil checkout une branche AVANT écriture |
| `.git/index.lock Operation not permitted` | Autre session git en cours | Mode propositions chat, pas d'édition JSON |
| `Write succeeded` mais Read échoue après | Sandbox éphémère ou rotation FUSE | Bascule bash + chemin Linux, alerte Soleil |
| `find` retourne vide sur fichiers fraîchement écrits | Pattern de perte rapports 6/8/9/10/11/12 | ARRÊT immédiat, alerte Soleil, ne pas continuer |
| Linter tronque la ligne avec email en fin de .md | Bug Cowork connu (rapport 7) | Signature en avant-dernière ligne, ou format différent |
| Disconnection MCP en cascade (system-reminders) | Rotation sandbox imminente possible | Vérifier sentinel + `find -newer` avant de continuer |
| `rm` retourne `Operation not permitted` (FUSE) | Le mount FUSE bloque la suppression | Soleil supprime côté Windows |
| `_drafts/_cowork_close_test.txt` 0 octet récurrent | Résidu de tests FUSE non nettoyable | Soleil supprime manuellement |

## Sources de vérité

- **Source canon corpus scientifique** : le clone privé, `docs/corpus_scientifique/00_canon/`. Jamais mounté Cowork — écritures via file tools sur le working tree Windows, commits manuels par Soleil.
- **Source canon HTML applicatif** : multi-pages depuis ~mai 2026 (`app.html`, `patrimoine.html`, `cadre-scientifique.html`, `glossaire.html`, `mairies.html`, `transparence.html`, etc.). Le project_instructions mentionne `tellux_FINAL_CLEAN1.html` mais c'est obsolète (phase mono-fichier d'avril 2026). **Demander à Soleil le fichier cible avant tout patch HTML.**
- **Source canon sites patrimoine** : `docs/data/sites_patrimoine.json` (source de vérité runtime depuis le Brief 33 split, 2026-05-06 — `sites_corse.json` est DEPRECATED, aucun consommateur runtime, cf. `ARCHITECTURE.md` §3.bis).
- **Source canon hypothèses** : le clone privé, `docs/corpus_scientifique/00_canon/TELLUX_HYPOTHESES_PROTOCOLES.md` (Doc 2 v1.2 au 2026-05-08, intègre veille Scholar 8 références).
- **Source canon position épistémique** : `TELLUX_POSITION_EPISTEMIQUE.md` (créé session 6, 13 avril 2026). Tout dossier Tellux relu à sa lumière avant envoi.
- **Convention gitignore** : le `.gitignore` à la racine couvre les dossiers de travail locaux Cowork (livrables hors repo public, propagation manuelle vers le clone privé selon `.claude/CLAUDE.md`) — lire ses règles en direct plutôt qu'un motif recopié ici, qui daterait au premier renommage.
- **Mémoire persistante Cowork** : `MEMORY.md` (index) et fichiers indexés.
- **État public LIVE = prod déployée (v4.5).** Pour toute question « qu'est-ce qui est **réellement servi au public** en ce moment » (libellé, rendu, contenu d'une page publique), la vérité est le **contenu servi sur `tellux.pages.dev`** — lecture directe du DOM / HTML servi — qui **prime sur tout récap d'agent** et sur le working-tree (lequel reflète l'état pré-merge, pas forcément déployé). **Vérifier en prod avant d'affirmer un état de fait sur du contenu public shippé.** La **vérification en prod du contenu public déployé** (lecture DOM `tellux.pages.dev`) et les **smoke visuels de branche** (preview Cloudflare via Chrome connecté) sont des **tâches Cowork légitimes**.
- **Sens de synchronisation privé↔MAIN (v4.5).** Le corpus privé est canonique **par convention**, pas « toujours en avance ». Si Cowork prépare des inputs `_drafts/` destinés à une synchronisation ultérieure et qu'une divergence apparaît, **MAIN-en-avance = anomalie à réconcilier** (jamais écraser MAIN avec le privé périmé) : Cowork **signale**, ne propage rien dans aucun sens (il n'écrit pas git de toute façon — Soleil/Code réconcilient sur arbitrage).

## Pattern systémique (état 2026-05-09)

Sur 18 sessions Cowork digérées (24 avril → 9 mai 2026) :

- **6 sessions (33 %)** ont perdu en bloc tout ou partie de leur production (~250+ markdowns), malgré retours `Write/Edit` succès. Convention `docs/fiches_sites/` ou `docs/ethnologie-comparee/` choisie hors canon a aggravé la perte (les sessions Code utilisent `fiches_patrimoine/`).
- **La quasi-totalité** des rapports ont vu leur `git status` pollué par les artefacts CRLF (200-271 fichiers `M`).
- **Plusieurs sessions** ont produit en redondance ce que Code avait déjà shippé sans visibilité Cowork (Brief 39decies via `bd59afd`, Brief 5 via PR #430).

Le sentinel + le `find -newer` régulier + l'absence d'opérations git d'écriture sont les trois précautions qui font la différence entre une session productive et une session perdue.

---

*Dernière mise à jour : 2026-07-03 — alignement doctrine v4.5 (prod = vérité de l'état public live, detect-and-signal git / carve-out #10 + activation hook, sens de sync privé↔MAIN). Base : synthèse des 18 rapports de fermeture Cowork (2026-05-09).*
