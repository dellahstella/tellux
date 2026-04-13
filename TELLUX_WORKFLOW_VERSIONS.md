# TELLUX — Workflow multi-versions

**Date :** 9 avril 2026
**Objectif :** Maintenir simultanément une version stable (production), une version préprod (tests partenaires), et une version dev (en travail), sans risque de casser la production.

---

## C1. Modèle Git recommandé

### Trois branches longues

```
main          ← production, déployée sur tellux.pages.dev
  │
  └── staging ← préprod, déployée sur staging.tellux.pages.dev
        │
        └── dev ← travail en cours, non déployée publiquement (ou preview privé)
              │
              ├── feat/correctif-fab
              ├── feat/export-json-sites
              └── feat/disclaimer-h64
```

| Branche | Rôle | Qui y accède | Déployée sur |
|---|---|---|---|
| `main` | Version stable, figée, livrée aux partenaires tests et présentée dans le dossier CTC | Tout le monde | `tellux.pages.dev` |
| `staging` | Version candidate, testée localement, prête à être promue en production | Soleil + testeurs de confiance | `staging.tellux.pages.dev` |
| `dev` | Version instable, en cours de modification | Soleil uniquement | Preview Cloudflare (optionnel) |
| `feat/xxx` | Branches éphémères pour chaque chantier, créées depuis `dev` | Soleil uniquement | Aucun |

### Workflow type

**1. Démarrer un chantier :**
```bash
git checkout dev
git pull origin dev
git checkout -b feat/correctif-fab
```

**2. Travailler sur la branche feature :**
```bash
# Éditer, tester localement
git add tellux_v6_design.html
git commit -m "Correctif FAB : startContribFromFAB() + map.once dans setTimeout(0)"
```

**3. Merge dans dev quand le chantier est terminé :**
```bash
git checkout dev
git merge feat/correctif-fab
git push origin dev
git branch -d feat/correctif-fab
```

**4. Quand dev est stable, promouvoir en staging :**
```bash
git checkout staging
git merge dev
git push origin staging
# → Cloudflare déploie automatiquement sur staging.tellux.pages.dev
# → Tester pendant 1 à 2 semaines avec les partenaires de confiance
```

**5. Si staging est validée, promouvoir en production :**
```bash
git checkout main
git merge staging
git push origin main
# → Cloudflare déploie automatiquement sur tellux.pages.dev
git tag -a v6.0.1 -m "Description de la release"
git push origin v6.0.1
```

### Règles de protection

- **Ne jamais pousser directement sur `main`.** Toute modification passe par `dev` → `staging` → `main`.
- **Ne jamais merge `dev` directement dans `main`.** Passer par `staging`.
- **Tagger chaque promotion vers `main`** : `v6.0.0`, `v6.0.1`, `v6.1.0`, etc.
- **En cas de bug critique en production** : créer une branche `hotfix/xxx` depuis `main`, corriger, merger dans `main` ET dans `dev` (pour ne pas perdre le correctif).

### Initialisation (une seule fois)

Si le dépôt n'a actuellement qu'une branche `main` :

```bash
git checkout main
git checkout -b staging
git push -u origin staging
git checkout -b dev
git push -u origin dev
```

---

## C2. Configuration Cloudflare Pages pour le multi-environnements

Cloudflare Pages déploie automatiquement chaque branche Git en preview. Il n'y a presque rien à configurer.

### Vérification de la configuration actuelle

1. Dashboard Cloudflare → Pages → projet Tellux → Settings → Builds & deployments.
2. Vérifier que « Production branch » est `main`.
3. Vérifier que « Preview branches » est réglé sur « All non-production branches » (c'est le défaut).

### Résultat

| Branche | URL de déploiement | Visibilité |
|---|---|---|
| `main` | `tellux.pages.dev` | Public |
| `staging` | `staging.tellux.pages.dev` | Public (mais non communiqué) |
| `dev` | `dev.tellux.pages.dev` | Public (mais non communiqué) |
| `feat/xxx` | `feat-xxx.tellux.pages.dev` | Public (mais éphémère) |

**Note sur la visibilité :** Les preview deployments Cloudflare Pages sont techniquement publics (pas de mot de passe). Ils ne sont pas indexés par les moteurs de recherche, mais quelqu'un qui connaît l'URL peut y accéder. Pour Tellux, ce n'est pas un problème — le code est open-source et les données ne sont pas sensibles. Si un jour la confidentialité d'un preview est nécessaire, Cloudflare Access (gratuit jusqu'à 50 utilisateurs) permet d'ajouter une authentification.

### Variables d'environnement par branche

Si un jour le code Tellux utilise des variables d'environnement (ex : URL Supabase différente en dev et en prod), Cloudflare Pages permet de les configurer séparément :

1. Settings → Environment variables.
2. Onglet « Production » : variables pour `main`.
3. Onglet « Preview » : variables pour toutes les autres branches.

Pour l'instant, Tellux n'utilise pas de variables d'environnement côté build (l'URL Supabase est en dur dans le HTML). Ce sera pertinent lors de la migration modulaire (voie B, axe 4).

---

## C3. Gestion des versions de la base Supabase

### Le problème

Il n'y a qu'une seule base Supabase. Si `main` et `dev` utilisent la même base avec des schémas différents, les contributions citoyennes en production risquent d'être corrompues par un changement de schéma en dev.

### Stratégie par phase

**Phase actuelle (tests partenaires) — une seule base, schéma stabilisé.**

Le schéma de la base Supabase ne doit pas être modifié pendant la campagne de tests. Si un changement de schéma est nécessaire (nouvelle colonne, nouvelle table), il est d'abord écrit sous forme de migration SQL, testé localement, puis appliqué en production à un moment planifié.

Concrètement :
- Le code sur `main` et `staging` utilise la même base Supabase (production).
- Le code sur `dev` utilise aussi la même base mais ne doit pas modifier le schéma.
- Les modifications de schéma sont versionnées dans `_migrations/`.

**Phase montée en gamme (voie B) — deux bases séparées.**

Quand les modifications de schéma deviennent fréquentes :
1. Créer un second projet Supabase (free tier permet 2 projets) dédié au développement.
2. Le code sur `dev` pointe vers la base dev.
3. Le code sur `main` et `staging` pointe vers la base prod.
4. Les migrations testées en dev sont ensuite appliquées en prod.

### Migrations SQL versionnées

Créer un dossier `_migrations/` dans le dépôt :

```
_migrations/
├── 001_initial_schema.sql     ← schéma actuel (pour documentation)
├── 002_add_contribution_type.sql
├── 003_add_export_format.sql
└── README.md                  ← procédure d'application
```

Chaque fichier est un script SQL idempotent (utiliser `IF NOT EXISTS`, `ALTER TABLE ... ADD COLUMN IF NOT EXISTS`, etc.) appliqué manuellement par Soleil dans l'ordre :

```sql
-- 002_add_contribution_type.sql
-- Ajout d'un champ type de contribution (magnétomètre, RF, WiFi, ELF)
ALTER TABLE contributions ADD COLUMN IF NOT EXISTS contribution_type TEXT DEFAULT 'magnetometer';
COMMENT ON COLUMN contributions.contribution_type IS 'Type de mesure : magnetometer, rf, wifi, elf';
```

**Procédure d'application :**
1. Tester la migration sur la base dev (si elle existe) ou en local.
2. Sauvegarder la base prod (export CSV — voir TELLUX_SAUVEGARDE.md).
3. Appliquer la migration en prod via le SQL Editor du dashboard Supabase.
4. Vérifier que l'application fonctionne.
5. Committer le fichier de migration dans Git.

---

## C4. Tags et releases

### Convention de versioning

Format : `vMAJEUR.MINEUR.PATCH`

| Type | Quand | Exemple |
|---|---|---|
| MAJEUR | Changement architectural (migration modulaire, refonte UI) | `v7.0.0` |
| MINEUR | Nouvelle fonctionnalité (nouvelle couche, nouveau module) | `v6.1.0` |
| PATCH | Correctif de bug, mise à jour de données | `v6.0.1` |

### Procédure

À chaque merge de `staging` vers `main` :

```bash
git checkout main
git merge staging
git tag -a v6.0.1 -m "Correctifs A-5 et A-7, mise à jour GPS patrimoine"
git push origin main --tags
```

**Créer aussi une release GitHub** (optionnel mais recommandé pour la visibilité) :

```bash
gh release create v6.0.1 --title "v6.0.1 — Correctifs phase tests" --notes "- Correctif bouton annulation mesure (A-5)\n- Correctif conflit clic quadrillage (A-7)\n- Mise à jour GPS 12 sites patrimoine"
```

### Retour en arrière

Si une version déployée pose problème :

```bash
# Revenir à la version précédente
git checkout main
git revert HEAD
git push origin main
# Cloudflare redéploie automatiquement la version précédente
```

Ou, en cas d'urgence :

```bash
# Déployer directement un tag stable
git checkout v6.0.0
git push origin HEAD:main --force-with-lease
```

---

## C5. Données dans le HTML — pièges et bonnes pratiques

### Ce qui doit rester dans le HTML

**Constantes scientifiques et paramètres du modèle :** coefficients IGRF-14 (si calculés localement), seuils de scoring, facteurs de pondération piézo, paramètres Biot-Savart. Ces valeurs changent rarement, sont petites, et font partie intégrante de la logique applicative. Les garder dans le code est correct.

**Fallback offline :** Si Tellux doit fonctionner sans connexion (panne Supabase, mode avion terrain), un jeu de données minimal en dur dans le HTML est légitime. Exemples : les coordonnées des 116 sites mégalithiques (quelques Ko), les paramètres des 88 hypothèses (quelques Ko). C'est une stratégie de résilience, pas une erreur.

**CSS et configuration UI :** Variables CSS, palette, typographie, mise en page. Tout cela reste dans le HTML tant que le projet est monofichier.

### Ce qui doit être en backend (Supabase)

**Contributions citoyennes :** Toute donnée créée par un utilisateur (mesures terrain, signalements, propositions d'études) doit être dans Supabase. Ces données sont nominatives (même anonymisées, elles sont géolocalisées et horodatées) et doivent pouvoir être modérées, exportées, et sauvegardées indépendamment du code.

**Données volumineuses mises à jour fréquemment :** Les 974 antennes ANFR et les 314 églises sont déjà dans Supabase — c'est correct. Si de nouvelles couches sont ajoutées (RPG, BD Forêt), elles doivent aussi aller en backend.

### Ce qui devrait être externalisé en JSON/GeoJSON publics

**`SITES[]` (116 sites mégalithiques) :** C'est le cas le plus urgent. Les coordonnées GPS dérivent entre les sessions (problème A-1 récurrent) parce qu'elles sont noyées dans 6 500 lignes de HTML. Externaliser dans `SITES_REFERENCE.json`, charger via `fetch()` avec fallback inline. C'est la solution proposée en A-1 de la roadmap et en axe 4 de la montée en gamme.

**`CHURCHES[]` (314 églises) :** Déjà en Supabase avec fallback inline. Le fallback inline peut être supprimé quand la stabilité de Supabase est assurée (cron d'éveil en place).

**`FAILLES_CORSE[]` (failles tectoniques) :** Données statiques, changent rarement. Externaliser en GeoJSON pour faciliter la maintenance et l'évolution (refactoring en segments LineString, E-1).

**`HYPOTHESES[]` (88 hypothèses) :** Données qui évoluent à chaque session scientifique. Externaliser en JSON pour permettre la mise à jour sans toucher au code.

**`PROD_ELECTRIQUE[]` (33 sites de production) :** Données statiques. Externaliser en JSON.

**`PRECOMPUTED_ALIGNMENTS[]` (15 alignements) :** Données calculées une fois. Externaliser en JSON.

### Pourquoi le « tout dans le HTML » n'est ni plus sûr ni plus simple

C'est un mythe courant dans les projets monofichier. L'argument habituel est : « Si tout est dans le HTML, pas de dépendance externe, pas de risque de panne réseau. » C'est vrai pour la résilience offline, mais faux pour la sécurité et la maintenabilité :

1. **Régressions GPS.** Quand un développeur (humain ou IA) modifie le HTML, il peut accidentellement toucher aux coordonnées GPS noyées dans le même fichier. Avec un JSON externe, le fichier de données est séparé du code — on ne le modifie que quand on veut modifier les données.

2. **Conflits de merge.** Deux personnes (ou deux sessions Claude) qui modifient le même fichier de 6 500 lignes produisent des conflits Git complexes. Avec des fichiers séparés, les conflits sont isolés et gérables.

3. **Pas de diff lisible.** Un changement de coordonnées GPS perdu dans un diff de 500 lignes de JavaScript est invisible. Dans un JSON dédié, le diff est immédiatement lisible.

4. **Fausse sécurité.** Les données dans le HTML sont publiques (le fichier est servi par Cloudflare, visible par quiconque). Elles ne sont pas plus « protégées » que dans un JSON public ou une API Supabase avec anon key.

**La bonne stratégie :** externaliser les données en JSON publics chargés par `fetch()`, avec un fallback inline pour le mode offline. Le code JS ne contient que la logique, pas les données. C'est exactement ce que propose l'axe 4 de la montée en gamme — la première étape (extraction des données) est la plus facile et la plus impactante.

---

*Workflow rédigé le 9 avril 2026. Ce document est le mode d'emploi de référence pour le versioning Tellux. À relire avant chaque session de développement.*
