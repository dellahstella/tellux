# CLAUDE.md — règles communes des sessions Claude Code sur ce dépôt

Ce fichier est versionné pour que **toute copie du dépôt** porte les mêmes règles de base, quel que soit l'endroit d'où
une session est lancée : clone, worktree, environnement distant ou intégration continue. Des consignes locales peuvent
s'y ajouter ; elles ne l'affaiblissent pas.

Deux limites à connaître :
- **Les agents Explore et Plan de Claude Code ne reçoivent pas ce fichier.** Toute consigne qui compte pour eux s'écrit
  dans leur brief.
- **Une branche emporte la version du fichier qu'elle contient.** Sur une branche ancienne, relire la version de `main`.

## Web et agents : lire, pas aspirer

Ces règles valent pour une session **et pour tout agent qu'elle lance**.

1. **Lire une page citée, oui. Parcourir un site, non.**
   - Lire, c'est ouvrir une page dont l'adresse est connue d'avance, ou exigée par une cible nommée.
   - Parcourir, c'est énumérer des pages pour découvrir ce qu'un site contient : listes, plan du site, pagination.
   - **Critère** : si l'on ne sait pas, avant de commencer, combien de pages on va ouvrir, c'est un parcours.
   - Un parcours n'a lieu que sur accord explicite de la personne qui pilote le projet.
2. **Respecter le `robots.txt`**, y compris quand il n'interdit qu'une catégorie d'agents. S'il bloque les robots d'IA
   ou les collecteurs, aucun relevé automatisé. Dans le doute, s'abstenir et signaler.
3. **Jamais d'identité d'emprunt.** Ne pas se présenter sous l'agent utilisateur d'un navigateur ou d'un autre robot
   pour franchir une restriction ; s'annoncer sous un nom véridique, par exemple `Tellux-recherche/1.0`. Ne jamais
   contourner un filtre anti-robot, un défi, un accès réservé aux abonnés ou une adresse masquée : s'arrêter et
   signaler.
4. **Téléchargements : jamais en silence.**
   - Un jeu public sous licence ouverte, pris sur le portail officiel de son éditeur, peut être téléchargé. Il faut
     vérifier son empreinte quand elle est publiée, et consigner sa provenance : adresse, date, licence, millésime,
     empreinte. Le téléchargement est annoncé dans la conversation.
   - Tout le reste attend un accord explicite : licence non établie, fichier issu d'un parcours, volume inhabituel.
5. **Données obtenues sans licence ni accord de reproduction : hors dépôt.** Un rapport peut citer des valeurs, il ne
   reproduit pas la table.
6. **Dans tout brief d'agent qui touche au web, écrire les points 1 à 5 noir sur blanc.** Relire ensuite son compte
   rendu, en cherchant les volumes (pages, Mo) et les fichiers téléchargés. Tout écart est signalé, jamais réparé en
   silence.

## Actions git

- Jamais de push direct sur `main`, jamais de merge qui contourne les vérifications requises (`--admin`), jamais de
  `--no-verify`.
- Jamais de `force-push` sur une branche partagée.
- Un verrou `.git/index.lock` présent, ou des fichiers indexés qu'on n'a pas indexés soi-même : ne pas committer, ne
  pas supprimer le verrou, signaler. Une autre session travaille peut-être dans la même copie.

## Contenu public

Tout ce qui est versionné ici est public. Un contenu public neuf (page, texte éditorial ou scientifique) :
- passe la garde anti-fuite de la CI ;
- est relu avant fusion.

Un correctif mécanique sans contenu neuf n'a pas besoin de cette relecture.

## Éditer plutôt que dupliquer

Toute modification se fait dans le fichier qui est la source du contenu. Pas de variante parallèle (`_v2`, `_new`,
`_final`) d'un contenu qui a déjà un fichier. Les brouillons de travail restent hors du dépôt.

## Mémoire des sessions (`MEMORY.md`)

Ceci ne concerne que les sessions locales qui ont une mémoire automatique.
- **Limite de lecture.** L'index n'est lu que jusqu'à **25 000 caractères**, en longueur de chaîne JavaScript,
  retours chariot compris, ou jusqu'à **200 lignes**. Au-delà, la fin est coupée sans que la personne le voie. Mesurer
  en caractères, jamais en octets.
- **Une ligne par chantier**, mise à jour sur place. Quand le chantier se ferme, sa ligne sort de l'index vers le
  fichier d'historique de la période.
- **Compacter l'index en session seule** : vérifier qu'aucune autre session n'écrit, avant et juste avant l'écriture.

## Dans le doute

S'abstenir et signaler. Une ignorance déclarée vaut mieux qu'une supposition présentée comme un fait.
