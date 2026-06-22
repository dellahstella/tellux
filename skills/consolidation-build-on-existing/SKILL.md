---
name: consolidation-build-on-existing
description: >-
  Consolide un livrable à partir de briques déjà produites et gatées, SANS les re-sourcer
  ni les re-auditer : la brique gatée se cite par référence, son statut de vérification
  d'origine est préservé. À utiliser pour tout chantier de consolidation s'appuyant sur des
  chantiers amont clos ou un corpus déjà re-gaté. Déclencheurs : consolidation, cahier des
  charges, build-on-existing, citer par référence, ne pas re-sourcer, brique gatée,
  statut_verif, corpus amont. Adossé à ADR-013.
---

# consolidation-build-on-existing — La brique gatée se cite, ne se re-source pas

Une consolidation assemble l'acquis ; elle n'invente ni ne re-source. Une brique déjà
produite et gatée (chantier amont, corpus re-gaté) est **citée par référence**, jamais
re-sourcée ni re-auditée, et son `statut_verif` d'origine est **préservé**. (Adossé à ADR-013.)

## Quand l'utiliser
Tout chantier dont l'objet est de **consolider** (cahier des charges, synthèse, tableau de
qualification) en s'appuyant sur des livrables amont déjà gatés, plutôt que de produire de
la recherche neuve.

## Procédure
1. **Recenser les briques amont** mobilisées + leur `statut_verif` d'origine (PASS / gate
   passé / à vérifier...). Lister chaque brique avec sa référence.
2. **Consolider sans re-sourcer** : agréger, mettre en forme, articuler — sans rouvrir la
   vérification des briques héritées.
3. **Citer par référence** et **préserver les statuts** : chaque élément hérité garde son
   statut d'origine, attribué à sa brique source.
4. **Ne gater que le nouveau** : seules les références **nouvelles** introduites par la
   consolidation passent le gate (verify_citation / gate citations). L'hérité n'est pas
   re-gaté.

## Garde-fous
- **Interdiction de re-auditer** une brique déjà gatée : pas de re-résolution de citation,
  pas de re-notation d'un livrable amont clos.
- **Séparer explicitement** ce qui est hérité (non re-gaté, cité par référence) de ce qui
  est nouveau (gaté dans ce chantier).
- Ne pas dégrader ni « améliorer » silencieusement un statut hérité : il est repris tel quel.
- Un résiduel non résolu d'une brique amont reste son résiduel : on le signale, on ne le
  comble pas en consolidation.

## Sortie
Un livrable consolidé où chaque élément porte sa référence et son statut (hérité vs nouveau),
et où seules les références nouvelles ont été gatées.
