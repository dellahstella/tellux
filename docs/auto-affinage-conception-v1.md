# Auto-affinage du modèle Tellux par les contributions terrain — Document de conception v1

**Statut :** brouillon de conception, non engagé techniquement.
**Date :** 26 avril 2026.
**Auteur :** session Claude.ai (architecte de prompts) avec Soleil.
**Périmètre :** réflexion préalable, sans aucune implémentation associée. À reprendre lorsque les conditions d'amorçage sont réunies (cf. section *Conditions d'amorçage*).

---

## 1. Intention

L'application Tellux affiche en chaque point cliqué une valeur de champ électromagnétique calculée par son moteur (combinaison IGRF + EMAG2 pour le magnétique statique, Biot-Savart pour le magnétique basse fréquence, propagation libre pour la radiofréquence, modèle altitudinal et radon pour le rayonnement ionisant). Les contributions utilisateur fournissent par ailleurs des mesures terrain géolocalisées.

L'idée d'auto-affinage consiste à calculer, pour chaque contribution, la valeur **prédite** par le moteur Tellux au point GPS correspondant, à stocker le **résidu** (mesure − prédiction), puis à utiliser l'accumulation des résidus pour :

- détecter des biais systématiques du modèle (sous-estimation en zone X, surestimation en zone Y) ;
- éclairer une décision humaine de calibration des constantes provisoires (zones gelées) ;
- prioriser les zones territoriales où collecter davantage de données de qualité.

C'est une boucle de validation empirique du modèle par crowdsourcing, **outil d'aide à la décision pour Soleil**, et non un mécanisme de calibration automatique.

## 2. Pertinence inégale selon le domaine physique

Les quatre domaines couverts par Tellux ne se prêtent pas également à l'auto-affinage.

| Domaine | Pertinence | Justification |
|---|---|---|
| Radiofréquence | Forte | Mesures grand public possibles avec analyseurs de spectre simples ; les 30 mesures certifiées ANFR/EXEM disponibles fournissent un jeu de référence pour les niveaux 1 ; couverture territoriale faible donc forte valeur ajoutée d'un afflux de mesures terrain. |
| Rayonnement ionisant gamma | Forte | Compteurs Geiger amateurs avec précision raisonnable ; calibration directe possible de la composante terrestre `NCRP-001` (zone gelée actuelle) ; validation croisée avec Téléray quand l'API ASNR sera ouverte. |
| Magnétique basse fréquence (ELF) | Modérée | Smartphones disposent d'un magnétomètre exploitable avec orientation correcte ; permet de valider Biot-Savart sur les segments HTA en conditions réelles, mais bruit important au-delà de 50-100 m d'une source. |
| Magnétique statique | Faible à court terme | IGRF et EMAG2 sont des modèles institutionnels mûrs ; difficilement améliorables par des amateurs sans magnétomètre fluxgate calibré ; à exclure de la première phase. |

L'auto-affinage cible donc en priorité **RF** et **gamma**, secondairement **ELF**, et **pas du tout** le magnétique statique dans un premier temps.

## 3. Hiérarchisation des contributions

L'application distingue déjà deux niveaux de fiabilité parmi les contributions terrain :

- **Niveau 1** : mesures réalisées dans le respect d'un protocole strict (matériel qualifié, position de l'instrument, distance des sources parasites, conditions environnementales).
- **Niveau 2** : mesures captées automatiquement par le magnétomètre Android au moment de la saisie, sans contrôle des conditions de prise.

Cette distinction est **structurante** pour le design de l'auto-affinage. Les contributions de niveau 2 sont précieuses pour la **couverture territoriale** (densité d'échantillonnage, détection d'anomalies à investiguer) mais ne doivent **pas** entrer dans le calcul de calibration des constantes du modèle. Seul le niveau 1 alimente la décision d'ajustement.

Le mécanisme de séparation doit être strict et tracé dans la table `residuals` (cf. section 6) via une colonne `confidence_level` qui sépare les deux flux.

## 4. Architecture cible

### 4.1 Extraction du moteur Node.js

Aujourd'hui, les fonctions de calcul (`calcMagneticField`, `calcGammaAmbient`, `calcBiotSavart`, etc.) vivent dans `app.html`, exécutées côté navigateur. Pour permettre l'auto-affinage, ces fonctions doivent être exécutables côté serveur.

Trois options ont été examinées :

| Option | Choix |
|---|---|
| Extraire les fonctions `calc*` dans un module Node.js réutilisable, importé à la fois par `app.html` (côté client) et par une Edge Function Supabase ou un Worker Cloudflare (côté serveur). | **Retenu.** Un seul code, deux contextes d'exécution, pas de dérive. |
| Re-implémenter le calcul ailleurs (ex. Python dans N8N). | Rejeté. Risque de dérive entre les deux versions du modèle. |
| Déclencher un navigateur headless qui charge l'app et lit le résultat. | Rejeté. Trop lourd pour un calcul mensuel. |

L'extraction Node.js a un bénéfice secondaire important : elle rend le moteur **auditable par un physicien tiers** sans qu'il ait à parcourir un HTML monolithique. C'est cohérent avec l'objectif Phase 1 du projet.

### 4.2 Trigger : cron N8N mensuel

Le compte N8N gratuit (~5 000 exécutions/mois en plan Starter) suffit largement pour un cron mensuel. Un workflow N8N déclenché le 1er de chaque mois :

1. Interroge Supabase pour récupérer toutes les contributions du mois écoulé non encore traitées.
2. Pour chaque contribution, appelle l'Edge Function Supabase (ou le Worker Cloudflare) qui exécute le moteur Node.js sur le point GPS et la date de la contribution.
3. Récupère la prédiction et calcule le résidu.
4. Insère une ligne dans la table `residuals`.

Cadence mensuelle suffit largement : aucune urgence à calculer le résidu en temps réel.

Bénéfice secondaire : ce chantier donne enfin une utilité opérationnelle au compte N8N.

### 4.3 Stockage privé

Une nouvelle table Supabase dédiée, **non exposée publiquement** :

- Nom : `residuals`
- RLS : aucune lecture publique. Lecture autorisée uniquement à `service_role` et à un compte admin nommé.
- Pas d'API publique ni d'export ouvert.

Ce qui devient public, c'est uniquement la **décision** de modifier le modèle qui découle de l'analyse des résidus, accompagnée du raisonnement complet et publiée dans la page Rétractations.

## 5. Garde-fous épistémiques non négociables

Trois principes encadrent toute mise en œuvre de ce chantier.

### 5.1 Versioning du modèle

Chaque calcul de prédiction stocke la version du modèle qui l'a produit (`model_version`). Quand le modèle évolue, on recalcule en arrière-plan les résidus historiques et on conserve les anciennes valeurs. Sans ce versioning, on perdrait la traçabilité des résidus et la capacité d'analyser l'effet d'une calibration a posteriori.

### 5.2 Distinction zones gelées / zones calibrables

Les constantes balisées `GELÉ-001`, `NCRP-001`, `HTA-TENSION-001`, `BT-CALIBRATION-001`, `RADIO-AERO-001`, `TÉLÉ-001` ne sont **jamais** modifiées par un processus automatique. Les résidus peuvent informer une décision de relecture humaine, mais aucune calibration auto ne touche ces zones. Toute évolution passe par validation par un physicien tiers, conformément à la doctrine projet en vigueur.

### 5.3 Transparence des évolutions du modèle

Toute modification du modèle suite à analyse des résidus génère :

- une PR sur le dépôt public avec le diff de la modification ;
- une entrée dans la page `retractations.html` avec date, motif, lien vers le tableau de bord interne, raisonnement publié, lien vers la PR.

Pas de calibration silencieuse. Pas d'évolution non documentée publiquement.

## 6. Schéma de la table `residuals`

Schéma indicatif, à arbitrer lors de la phase 1 d'implémentation.

```
residuals (
  id                  uuid primary key,
  contribution_id     uuid references contributions(id),
  domain              text check (domain in ('M_static', 'M_elf', 'RF', 'I_gamma')),
  measured_value      numeric not null,
  measured_unit       text not null,
  predicted_value     numeric not null,
  predicted_unit      text not null,
  residual            numeric generated always as (measured_value - predicted_value) stored,
  confidence_level    smallint not null check (confidence_level in (1, 2)),
  model_version       text not null,
  prediction_timestamp timestamptz not null default now(),
  notes               text
)
```

Indexation utile : `(domain, confidence_level)`, `(prediction_timestamp)`, `(contribution_id)`.

## 7. Phasage proposé

### Phase 0 — Refactoring préalable

**Objectif.** Extraction des fonctions `calc*` de `app.html` vers un module Node.js isolé, importable à la fois par le client (avec un build léger ou un export adapté) et par une Edge Function ou un Worker.

**Livrables.**
- Module `lib/tellux-engine.js` (ou nom équivalent) à la racine du repo.
- Refactoring de `app.html` pour importer depuis ce module sans changement de comportement utilisateur.
- Tests unitaires minimaux sur les fonctions exportées (au moins pour les valeurs de référence connues).

**Bénéfice indirect.** Le moteur devient auditable par un physicien tiers sans lecture du HTML monolithique. Cohérent avec l'objectif Phase 1 du projet.

**Estimation grossière.** 2 à 3 sessions Cowork pour le refactoring, plus 1 sprint Claude Code pour les tests. Total : 1 à 2 semaines avec validation.

**À ne pas faire pendant cette phase.** Aucune modification du contenu du modèle. C'est uniquement une réorganisation du code. Les valeurs calculées avant et après refactoring doivent être strictement identiques.

### Phase 1 — Cron mensuel + table `residuals`

**Objectif.** Mise en place de la collecte automatique des résidus.

**Livrables.**
- Migration Supabase pour créer la table `residuals` avec RLS bloqué.
- Edge Function ou Worker qui prend en entrée `{lat, lon, date, domain}` et retourne `{predicted_value, predicted_unit, model_version}`.
- Workflow N8N programmé sur le 1er de chaque mois qui orchestre le batch.
- Calcul rétroactif optionnel : produire les résidus pour toutes les contributions historiques du repo (à arbitrer en début de phase 1).

**Estimation grossière.** 1 sprint Claude Code après phase 0 complétée.

**Critère de réussite.** Les résidus sont calculés et stockés sans intervention humaine pendant un cycle mensuel complet.

### Phase 2 — Tableau de bord admin

**Objectif.** Donner à Soleil un outil de lecture des résidus, sans aucune calibration auto.

**Livrables.**
- Page admin protégée (auth Supabase ou équivalent, à arbitrer).
- Visualisations des résidus : moyennes par domaine, par zone géographique (clustering), distribution, outliers, évolution dans le temps, séparation niveau 1 vs niveau 2.
- Aide à la décision : quand un biais systématique est détecté dans une zone et un domaine, alerte visuelle.

**Estimation grossière.** 1 sprint Claude Code après phase 1 complétée.

**Important.** Cette page reste **strictement interne**. Pas d'exposition publique des résidus.

### Au-delà — Calibration manuelle assistée

À mesure que le tableau de bord révèle des patterns clairs, Soleil peut décider d'ajuster manuellement certaines constantes du modèle. Chaque ajustement passe par PR + entrée Rétractations + publication du raisonnement.

Pas de phase « calibration semi-automatique » envisagée à court terme. Si elle l'est un jour, elle nécessitera un avis méthodologique externe formel.

## 8. Conditions d'amorçage

Ce chantier ne se déclenche pas avant que **toutes** les conditions suivantes soient réunies.

1. **Phase 1 du projet stabilisée.** L'application `app.html` est publiée comme cartographie EM rigoureuse, le pivot architectural est consommé, les bugs résiduels sont absorbés.
2. **Retour Santoni reçu.** Au moins une réponse du physicien sollicité, qu'elle soit de validation ou d'avis méthodologique. La phase 0 ne s'amorce pas dans le silence.
3. **Volume de contributions suffisant pour avoir du sens.** Indicatif : au moins quelques dizaines de contributions niveau 1 réparties sur le territoire. Avec moins, les résidus sont du bruit non statistiquement exploitable.
4. **Disponibilité de Soleil.** Le chantier est non urgent. Il ne déprend rien. Il s'amorce quand Soleil a la bande passante pour le piloter sans précipitation.

## 9. Points en suspens à arbitrer en début de phase 0

- Choix entre Supabase Edge Function et Cloudflare Worker pour héberger l'exécution serveur du moteur Node.js. Critères : coût, latence, simplicité de déploiement.
- Stratégie de packaging du module `lib/tellux-engine.js` : ESM natif, bundler minimal, ou autre.
- Granularité du `model_version` : SemVer du projet, ou hash de commit, ou identifiant interne dédié.
- Format de l'unité dans `measured_unit` et `predicted_unit` : texte libre (`'nT'`, `'µT'`, `'V/m'`, `'µSv/h'`) ou enum validé.
- Stratégie de gestion des contributions niveau 2 dans la table `residuals` : stockage avec flag, ou exclusion totale du calcul de résidu, ou collecte distincte. À arbitrer après phase 0.

## 10. Anti-patterns à éviter

- Ne pas mélanger niveau 1 et niveau 2 dans le calcul de calibration. Le mélange contamine le signal avec du bruit non quantifiable.
- Ne pas exposer publiquement les résidus bruts. Ils sont sujets à interprétation hâtive et n'ont de valeur que dans un contexte d'analyse outillée.
- Ne pas automatiser l'ajustement des constantes des zones gelées. Toute évolution passe par décision humaine + validation externe.
- Ne pas commencer la phase 1 avant d'avoir terminé la phase 0. Le moteur doit être proprement extrait avant qu'un cron y appelle.
- Ne pas oublier le versioning du modèle dans le calcul des résidus. Sans `model_version`, la donnée historique perd sa valeur.
- Ne pas négliger le calcul rétroactif des résidus historiques lors de la phase 1. Ils donnent une référence statistique de départ.

---

**Fin du document v1.** Reprendre ce document lors de la planification de la phase 0, le compléter de toute décision intervenue d'ici là, et passer à la version v2 avec un plan d'implémentation détaillé.
