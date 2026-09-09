-- 011_contributions_bt_terme_inclus.sql
-- 2026-09-09 — enregistre si le terme basse tension était inclus au moment de l'écriture.
--
-- POURQUOI
-- `saveContrib()` écrit `perturbation_humaine_nt` et `delta_nt` en base. Pendant la fenêtre
-- où la grille BT n'est pas encore chargée (~2 min à chaque visite, mesuré à 98-119 s en
-- production), ces valeurs sont MINORÉES : le terme BT est un palier fixe (70/115/180 nT)
-- absent du total. Écart mesuré au même point et au même facteur, entre régime sans BT et
-- avec : ×1,08 à 41,9195/8,7386 et jusqu'à ×5,3 à 42,5680/8,7570 — le rapport est maximal
-- là où le champ HTA est faible.
--
-- Contrairement à un affichage, rien ne se répare : la ligne est écrite. Et la table porte
-- 34 colonnes dont aucune n'enregistre cette condition — l'export CSV expose pourtant
-- `elf_bt_terme_inclus`. Toutes les contributions postérieures au 2026-08-07 (activation du
-- terme BT) sont donc ININTERPRÉTABLES sur ce point : rien ne permet de distinguer une
-- valeur complète d'une valeur minorée.
--
-- La garde existante de `saveContrib()` (attente jusqu'à 20 s sur `computeElfState()`) ne
-- couvre pas ce cas : `computeElfState()` rend `ready` dès que HTA est prêt et ne consulte
-- jamais BT. Elle protège la fenêtre HTA, pas la fenêtre BT.
--
-- CHOIX DE SCHÉMA, ET LEURS RAISONS
--   * nullable, SANS DEFAULT et SANS NOT NULL : l'existant doit rester distinguable du neuf.
--     Un DEFAULT false transformerait « on ne sait pas » en « le terme était absent », ce qui
--     est une affirmation que la donnée ne porte pas.
--   * AUCUN backfill : la condition au moment de l'écriture n'est pas reconstituable a
--     posteriori. La renseigner serait l'inventer.
--
-- RÈGLE DE LECTURE — elle est dans le commentaire de colonne pour survivre à ce fichier :
--   null  = inconnu (ligne antérieure à cette migration). À traiter comme inconnu,
--           JAMAIS comme false. Une ligne inconnue n'est pas une ligne minorée.
--   false = terme BT confirmé absent : `perturbation_humaine_nt` et `delta_nt` sont minorés.
--   true  = terme BT confirmé inclus.
--
-- ORDRE D'APPLICATION — sans fenêtre entre les deux
-- Cette migration doit être appliquée AVANT le merge du correctif applicatif qui écrit la
-- colonne. Dans l'autre sens, l'insertion échouerait sur une colonne inconnue et PLUS AUCUNE
-- contribution ne pourrait être enregistrée — un défaut pire que celui qu'on corrige.
-- Et la migration seule laisserait la colonne à null sur les lignes neuves aussi : les deux
-- dans la même séance, ou aucun des deux.

alter table public.contributions
  add column if not exists bt_terme_inclus boolean;

comment on column public.contributions.bt_terme_inclus is 'Le terme basse tension etait-il inclus dans perturbation_humaine_nt et delta_nt au moment de l ecriture ? null = inconnu (ligne anterieure a la migration 011, non reconstituable) : a traiter comme inconnu, jamais comme false. false = terme BT absent, valeurs minorees (jusqu a x5,3 la ou le champ HTA est faible). true = terme BT inclus.';
