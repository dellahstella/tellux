# TELLUX — Audit d'infrastructure

**Date :** 9 avril 2026
**Contexte :** Préparation de la phase tests partenaires (associations CEM, permaculture) et dépôt candidature CTC. Évaluation des risques et recommandations pour sécuriser l'infrastructure avant ouverture.

---

## A1. Supabase

### Rôle dans Tellux

Backend principal. Base de données PostgreSQL (PostGIS) hébergeant : 974 antennes ANFR, 314 églises romanes (corpus Moracchini-Mazel), contributions citoyennes (mesures terrain crowdsourcées), et potentiellement les données de gamification (XP, badges).

### Plan actuel : Free

### Limites du plan Free (vérifiées avril 2026)

| Ressource | Limite Free | Impact Tellux |
|---|---|---|
| Base de données | 500 Mo par projet actif | Suffisant à court terme — les données actuelles pèsent probablement < 50 Mo |
| Bande passante (egress DB) | 5 Go/mois | Suffisant pour < 500 utilisateurs actifs/mois |
| Bande passante (egress storage) | 5 Go/mois | Non utilisé actuellement (pas de fichiers dans le storage Supabase) |
| Stockage fichiers | 1 Go | Non utilisé actuellement |
| Auth (MAU) | 50 000 utilisateurs actifs/mois | Largement suffisant — Tellux n'a pas d'auth utilisateur |
| Edge Functions | 500 000 invocations/mois | Non utilisées actuellement |
| Realtime | Limites non publiées précisément pour le Free | Non utilisé actuellement |
| Projets | 2 projets actifs | Un seul projet Tellux, suffisant |
| Sauvegardes | Aucune sauvegarde automatique | **Risque — voir Mission B** |
| SLA | Aucun | **Risque pour la phase tests** |

### Risque principal : mise en pause après inactivité

**Sur le plan Free, un projet Supabase est automatiquement mis en pause après 7 jours d'inactivité.** Quand un projet est en pause, la base de données est arrêtée. Toute requête (lecture ou écriture) échoue jusqu'à ce que le projet soit réveillé manuellement depuis le dashboard Supabase.

**Scénario concret :** Soleil envoie le kit de contact aux associations EM un lundi. Pendant les 10 jours suivants, il ne se connecte pas au dashboard Supabase ni ne visite la carte (activité concentrée sur le docx candidature). Le jour où une association teste la carte et clique sur « Ajouter une mesure », la requête échoue silencieusement. L'association conclut que l'outil ne fonctionne pas. Impression désastreuse, pas de seconde chance.

**Ce risque est bloquant pour la campagne de tests.**

### Mitigations possibles

**Option 1 — Cron d'éveil (coût : 0 €, effort : 30 min)**

Un service externe envoie une requête HTTP à la base Supabase toutes les 4 à 6 heures pour maintenir le projet actif. Plusieurs services gratuits le permettent :

- **UptimeRobot** (uptimerobot.com) — gratuit jusqu'à 50 moniteurs, intervalle 5 min. Créer un moniteur HTTP qui pingue l'URL de l'API REST Supabase (ex : `https://<project-ref>.supabase.co/rest/v1/antennes?select=id&limit=1` avec l'anon key en header). Si la requête retourne 200, le projet reste actif.
- **cron-job.org** — gratuit, permet un cron HTTP toutes les heures.
- **Cloudflare Workers** — un Worker cron (gratuit dans la limite de 100 000 requêtes/jour) qui pingue Supabase toutes les 6 heures.

Cette solution fonctionne tant que Supabase ne change pas sa politique de détection d'inactivité. Le risque résiduel est que Supabase considère un simple ping comme insuffisant pour maintenir le projet actif — mais dans la pratique, les retours communautaires confirment que ça fonctionne.

**Option 2 — Passage au plan Pro (coût : 25 $/mois ≈ 23 €/mois)**

Le plan Pro supprime la mise en pause par inactivité, ajoute des sauvegardes quotidiennes automatiques (7 jours de rétention), un SLA de 99,9 %, et augmente les limites (8 Go DB, 250 Go bandwidth, etc.).

**Évaluation honnête :** pour un projet solo sans revenus, 25 $/mois est une dépense non négligeable (300 $/an). Elle se justifie si et seulement si les contributions citoyennes deviennent critiques (c'est-à-dire si des données terrain irremplaçables sont stockées dans la base et qu'une perte serait dommageable). Avant la campagne de tests, les données sont essentiellement institutionnelles (ANFR, églises) et reconstituables. Après les premiers retours terrain, la question se reposera.

**Recommandation : Option 1 (cron d'éveil) immédiatement, réévaluer le passage Pro après 50 contributions citoyennes ou si le projet reçoit une subvention.**

### Risques secondaires

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Changement de tarification Free | Moyenne | Moyen — migration possible vers Neon ou self-host | Surveiller les annonces Supabase, avoir un plan B identifié |
| Modification d'API REST | Faible | Moyen — cassure du code Tellux | Épingler la version API dans les appels, tester après chaque mise à jour |
| Panne régionale | Faible | Critique temporaire — Supabase utilise AWS | Aucune mitigation sur le Free (pas de multi-région). Accepter le risque |
| Blocage géographique | Très faible | Critique — France non concernée par les restrictions courantes | Aucune action requise |

---

## A2. GitHub

### Rôle dans Tellux

Hébergement du code source (`tellux_v6_design.html` et fichiers associés), historique de versions, collaboration future.

### Plan actuel : Free

### Limites du plan Free

Le plan Free GitHub est très généreux pour un projet open-source : dépôts illimités (publics et privés), Actions CI/CD (2 000 min/mois), Packages (500 Mo), LFS (1 Go). Aucune de ces limites n'est contraignante pour Tellux.

### Risque principal : point de défaillance unique

Si le dépôt GitHub est le seul endroit où le code source et l'historique Git existent, tout problème (suspension de compte, suppression accidentelle, panne prolongée) entraîne une perte potentiellement totale.

**Scénario concret :** GitHub désactive le compte de Soleil suite à un faux positif de détection d'abus (ça arrive, surtout avec les comptes gratuits qui poussent beaucoup de gros fichiers binaires comme les .docx). Le code est inaccessible pendant plusieurs jours. Si c'est au moment du dépôt CTC et que le dossier contient un lien vers le dépôt GitHub, c'est problématique.

### Sauvegardes actuelles

À vérifier par Soleil :
- Y a-t-il un clone Git local sur l'ordinateur de Soleil ? (probable — c'est le workflow Git normal)
- Y a-t-il un mirror sur un autre hébergeur (GitLab, Codeberg, Bitbucket) ? (probablement pas)
- Les fichiers documentaires (.md, .docx) sont-ils tous dans le dépôt Git ? (à vérifier — les fichiers Cowork sont dans le dossier Tellux monté, pas forcément dans le dépôt)

### Recommandation : mirror automatique

Configurer un mirror entrant depuis GitHub vers GitLab ou Codeberg. Les deux services le proposent gratuitement :

**GitLab :** Nouveau projet → Import → « Repository by URL » → coller l'URL GitHub → activer « Mirror repository » avec synchronisation automatique. GitLab tire les modifications de GitHub toutes les 5 minutes à 1 heure.

**Codeberg :** Nouveau dépôt → Paramètres → Mirror → « Mirror from GitHub ». Synchronisation automatique.

Temps de configuration : 10 à 15 minutes. Coût : 0 €. Résultat : une copie complète du dépôt (code + historique) sur un second hébergeur, synchronisée automatiquement.

### Risques secondaires

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Suspension de compte (faux positif) | Faible | Critique temporaire | Mirror + clone local |
| Suppression accidentelle de dépôt | Très faible | Critique | Mirror + clone local |
| Panne prolongée GitHub | Très faible | Moyen — code disponible en local | Clone local suffit |
| Changement CGU (projets privés limités) | Faible | Faible — Tellux est public | Aucune action |

---

## A3. Cloudflare Pages

### Rôle dans Tellux

Hébergement et déploiement du fichier `tellux_v6_design.html` (et fichiers associés : favicon, JSON éventuels). CDN mondial. URL publique `tellux.pages.dev`.

### Plan actuel : Free

### Limites du plan Free (vérifiées avril 2026)

| Ressource | Limite Free | Impact Tellux |
|---|---|---|
| Sites (projets) | Illimité | Suffisant |
| Builds | 500/mois | Largement suffisant — Tellux fait ~5-10 builds/mois |
| Fichiers par projet | 20 000 | Largement suffisant — Tellux a ~10 fichiers |
| Taille par fichier | 25 Mo | Suffisant — le HTML fait ~500 Ko |
| Bande passante | Illimitée | Aucun risque |
| Requêtes | Illimitées (assets statiques) | Aucun risque |
| Domaines personnalisés | 100 par projet | Suffisant |
| Membres d'équipe | Illimité | Non pertinent (projet solo) |
| Preview deployments | Illimité | Utile pour le workflow staging |

### Question de Soleil : « La campagne de contact via tellux.pages.dev ne présente aucun risque de fail ? »

**Réponse honnête : le risque est très faible, mais pas nul.**

Cas où Cloudflare Pages peut couper l'accès :

1. **Violation des conditions d'utilisation.** Improbable pour Tellux — c'est un site de cartographie scientifique, pas de spam ni de phishing. Risque : négligeable.

2. **Faux positif anti-DDoS.** Si un testeur utilise un script ou un outil de crawl agressif, les filtres Cloudflare peuvent temporairement bloquer l'accès depuis certaines IP. Risque : faible. Mitigation : rien à faire côté Soleil, Cloudflare débloque automatiquement après quelques minutes.

3. **Maintenance planifiée Cloudflare.** Extrêmement rare pour Pages (c'est du statique, pas du compute). Risque : négligeable.

4. **Panne mondiale Cloudflare.** C'est arrivé (juin 2022, novembre 2023 — pannes de quelques heures). Risque : faible mais non nul. Impact : le site est inaccessible pendant 1 à 4 heures. Mitigation : avoir un plan B.

5. **Suppression de compte par erreur.** Très rare. Risque : négligeable.

**Verdict : Cloudflare Pages est l'un des hébergeurs statiques les plus fiables du marché. Pour une campagne de tests avec < 100 utilisateurs sur quelques semaines, le risque d'indisponibilité est proche de zéro.** Le seul scénario réaliste est une panne mondiale Cloudflare de quelques heures — et dans ce cas, tout le web est affecté, pas juste Tellux.

### Plan B en cas d'indisponibilité

Soleil mentionne un compte Netlify existant. C'est un excellent plan B :

1. **Mirror permanent sur Netlify.** Connecter le même dépôt GitHub à un projet Netlify. Le déploiement se fait automatiquement à chaque push. URL : `tellux.netlify.app` (le projet existait déjà sous `moonlit-axolotl-755fd6.netlify.app`).

2. **Bascule en cas de panne.** Si `tellux.pages.dev` est inaccessible, communiquer l'URL Netlify aux testeurs. Pas besoin de domaine personnalisé pour ça — c'est un fallback, pas la production.

3. **Domaine personnalisé (optionnel).** Si Soleil achète `tellux.fr` ou `tellux.corsica`, le domaine peut pointer vers Cloudflare en temps normal et être rebasculé vers Netlify en 5 minutes (modification DNS). Cela donne un point d'entrée stable indépendant de l'hébergeur. Coût : ~10-15 €/an pour un .fr.

**Recommandation : configurer le mirror Netlify comme plan B (15 min, 0 €). Le domaine personnalisé est souhaitable mais non urgent.**

### Risques secondaires

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Panne mondiale Cloudflare | Faible | Critique temporaire (1-4h) | Mirror Netlify |
| Changement CGU Pages | Très faible | Moyen | Mirror Netlify + dépôt Git local |
| Limite de builds atteinte | Très faible | Faible — pas de déploiement possible temporairement | 500 builds/mois est très large |

---

## A4. Tableau de synthèse des risques

Trié par criticité décroissante (impact × probabilité).

| Service | Risque principal | Probabilité | Impact | Mitigation recommandée |
|---|---|---|---|---|
| **Supabase** | Mise en pause après 7j d'inactivité | **Élevée** | **Critique** — contributions citoyennes impossibles | Cron d'éveil immédiat (UptimeRobot ou Cloudflare Worker) |
| **Supabase** | Perte de données contributions (pas de backup) | Moyenne | **Critique** — données terrain irremplaçables | Export automatique quotidien (voir Mission B) |
| **GitHub** | Point de défaillance unique pour le code | Faible | **Critique** — perte du code et de l'historique | Mirror GitLab/Codeberg + clone local vérifié |
| **Cloudflare** | Panne mondiale (quelques heures) | Faible | Critique temporaire | Mirror Netlify comme fallback |
| **Supabase** | Changement tarification Free | Moyenne | Moyen | Identifier alternative (Neon, self-host) |
| **Cloudflare** | Faux positif anti-DDoS | Faible | Faible — auto-résolution | Aucune action |
| **GitHub** | Suspension de compte | Très faible | Critique temporaire | Mirror + clone local |

---

## E. Actions urgentes — 7 prochains jours

### Action 1 — Configurer un cron d'éveil Supabase

**Priorité :** 🔴 Critique
**Temps estimé :** 30 minutes
**Coût :** 0 €

**Étapes :**

1. Aller sur https://uptimerobot.com et créer un compte gratuit.
2. Cliquer « Add New Monitor ».
3. Type : HTTP(s).
4. Nom : `Tellux Supabase Keep-Alive`.
5. URL : `https://<votre-project-ref>.supabase.co/rest/v1/antennes?select=id&limit=1` (remplacer `<votre-project-ref>` par la référence du projet, visible dans le dashboard Supabase → Settings → API).
6. Dans les headers HTTP, ajouter : `apikey: <votre-anon-key>` (la clé anon publique, pas la service key).
7. Intervalle : 5 minutes (le plus court disponible en gratuit).
8. Sauvegarder.

**Résultat attendu :** Le projet Supabase ne sera plus jamais mis en pause tant qu'UptimeRobot fonctionne. En bonus, UptimeRobot enverra un email si la base est inaccessible.

**Vérification :** Attendre 24h, puis vérifier dans le dashboard Supabase que le projet est toujours actif. Vérifier aussi dans UptimeRobot que le moniteur affiche 100 % uptime.

---

### Action 2 — Configurer un mirror GitHub → GitLab

**Priorité :** 🟠 Importante
**Temps estimé :** 15 minutes
**Coût :** 0 €

**Étapes :**

1. Créer un compte GitLab (gitlab.com) si ce n'est pas déjà fait.
2. « New project » → « Import project » → « Repository by URL ».
3. Coller l'URL HTTPS du dépôt GitHub Tellux : `https://github.com/<username>/tellux.git`.
4. Nommer le projet `tellux`.
5. Cocher « Mirror repository » pour la synchronisation automatique.
6. Si le dépôt est privé : générer un Personal Access Token GitHub (Settings → Developer Settings → Tokens) avec le scope `repo`, et le renseigner dans GitLab.
7. Sauvegarder.

**Résultat attendu :** Une copie complète et à jour du dépôt Tellux sur GitLab, synchronisée automatiquement.

---

### Action 3 — Vérifier que le clone local Git est complet et à jour

**Priorité :** 🟠 Importante
**Temps estimé :** 5 minutes
**Coût :** 0 €

**Étapes :**

1. Sur l'ordinateur de Soleil, ouvrir un terminal dans le dossier du projet Tellux.
2. Exécuter `git status` — vérifier qu'il n'y a pas de modifications non commitées importantes.
3. Exécuter `git log --oneline -10` — vérifier que les derniers commits correspondent à ce qui est sur GitHub.
4. Exécuter `git remote -v` — vérifier que `origin` pointe vers le bon dépôt GitHub.
5. Si tout est en ordre : copier le dossier `.git` complet sur un disque dur externe ou un service cloud (Proton Drive, pCloud). C'est la copie 3 de la règle 3-2-1.

**Résultat attendu :** Confirmation que le code source existe en au moins 2 endroits (GitHub + local), bientôt 3 (+ GitLab).

---

### Action 4 — Configurer le mirror Netlify comme plan B

**Priorité :** 🟠 Importante
**Temps estimé :** 15 minutes
**Coût :** 0 €

**Étapes :**

1. Se connecter au compte Netlify existant.
2. « Add new site » → « Import an existing project » → GitHub.
3. Sélectionner le dépôt Tellux.
4. Build command : laisser vide (c'est un fichier HTML statique, pas de build nécessaire).
5. Publish directory : `.` (racine, ou le sous-dossier contenant `tellux_v6_design.html`).
6. Déployer.
7. Vérifier que le site est accessible sur l'URL Netlify générée.
8. Renommer le site en `tellux.netlify.app` si disponible (Site settings → Domain management → Custom domains → Edit site name).

**Résultat attendu :** Un mirror fonctionnel de Tellux sur Netlify, utilisable comme fallback si Cloudflare Pages est inaccessible.

---

### Action 5 — Tagger la version actuelle v6.0.0

**Priorité :** 🟡 Souhaitable
**Temps estimé :** 2 minutes
**Coût :** 0 €

**Étapes :**

1. Dans le terminal, depuis le dossier du projet : `git tag -a v6.0.0 -m "Version stable avant phase tests partenaires"`.
2. Pousser le tag : `git push origin v6.0.0`.

**Résultat attendu :** Un point de retour garanti. Si une modification casse quelque chose pendant la phase tests, `git checkout v6.0.0` restaure l'état stable en 5 secondes.

---

### Action 6 — Configurer une branche `staging` sur Cloudflare Pages

**Priorité :** 🟡 Souhaitable
**Temps estimé :** 20 minutes
**Coût :** 0 €

**Étapes :**

1. Créer la branche `staging` dans Git : `git checkout -b staging && git push -u origin staging`.
2. Dans le dashboard Cloudflare Pages → projet Tellux → Settings → Builds & deployments.
3. Vérifier que « Production branch » est bien `main`.
4. Cloudflare Pages déploie automatiquement toutes les branches en preview. La branche `staging` sera accessible sur `staging.tellux.pages.dev`.
5. Tester en poussant un commit trivial sur `staging` et en vérifiant que le preview se build.

**Résultat attendu :** Deux environnements séparés — production (`tellux.pages.dev` depuis `main`) et préprod (`staging.tellux.pages.dev` depuis `staging`). Les testeurs partenaires accèdent à la production, Soleil teste les modifications sur staging avant de les déployer.

---

### Action 7 — Premier export manuel de la base Supabase

**Priorité :** 🟡 Souhaitable
**Temps estimé :** 10 minutes
**Coût :** 0 €

**Étapes :**

1. Aller dans le dashboard Supabase → Table Editor.
2. Pour chaque table contenant des données irremplaçables (probablement : `contributions`, `mesures`, ou équivalent) : cliquer sur la table → « Export to CSV ».
3. Sauvegarder le CSV dans le dossier `_data_backups/` du projet (à créer).
4. Committer dans Git : `git add _data_backups/ && git commit -m "Premier export Supabase manuel"`.

**Résultat attendu :** Un snapshot de la base Supabase sauvegardé dans Git. C'est une action manuelle ponctuelle en attendant l'automatisation (voir Mission B).

---

### Action 8 — Évaluer l'achat du domaine tellux.fr

**Priorité :** 🟡 Souhaitable
**Temps estimé :** 15 minutes (recherche + décision)
**Coût :** ~10-15 €/an pour un .fr, ~30-50 €/an pour un .corsica

**Étapes :**

1. Vérifier la disponibilité de `tellux.fr` sur un registrar (OVH, Gandi, Infomaniak).
2. Vérifier aussi `tellux.corsica` (extension territoriale, plus chère mais symboliquement forte).
3. Si disponible et dans le budget : acheter. Sinon : noter dans la roadmap long terme.
4. Si acheté : configurer le DNS pour pointer vers Cloudflare Pages (CNAME `tellux.pages.dev`). Cloudflare gère le SSL automatiquement.

**Résultat attendu :** Un point d'entrée professionnel (`tellux.fr`) indépendant de l'hébergeur, rebasculable en 5 minutes en cas de changement de fournisseur. Meilleure image pour les dossiers de candidature et les contacts partenaires.

---

### Récapitulatif des actions

| # | Action | Priorité | Temps | Coût |
|---|---|---|---|---|
| 1 | Cron d'éveil Supabase | 🔴 Critique | 30 min | 0 € |
| 2 | Mirror GitHub → GitLab | 🟠 Importante | 15 min | 0 € |
| 3 | Vérifier clone local Git | 🟠 Importante | 5 min | 0 € |
| 4 | Mirror Netlify (plan B) | 🟠 Importante | 15 min | 0 € |
| 5 | Tag v6.0.0 | 🟡 Souhaitable | 2 min | 0 € |
| 6 | Branche staging Cloudflare | 🟡 Souhaitable | 20 min | 0 € |
| 7 | Export manuel Supabase | 🟡 Souhaitable | 10 min | 0 € |
| 8 | Évaluer domaine tellux.fr | 🟡 Souhaitable | 15 min | 10-50 €/an |
| **Total** | | | **~2h** | **0-50 €** |

---

*Audit rédigé le 9 avril 2026. Les limites des plans Free Supabase et Cloudflare Pages ont été vérifiées sur la documentation publique à cette date. Ces limites peuvent évoluer — Soleil est invité à revérifier avant d'agir si un délai significatif s'écoule.*
