# Rapport de session — Vague 1 : réorganisation patrimoine + v3 doyennés

Date : 2026-05-06
Périmètre : réorganisation du corpus patrimoine local en arborescence à 4 familles + identification du chantier v3 doyennés.

## Constat principal

**Aucune fiche v3 doyenné n'a été produite dans cette vague.** Le corpus ne contient pas de fiches v2 explicitement étiquetées « doyenné ». Les 34 fiches régionales du corpus sont toutes nommées et rédigées comme « Pieve » (en-tête, file name, contenu interne « identité historique de X comme pieve »). Elles ont donc été migrées vers `pieves/` et non vers `doyennes/`. La production v3 doyennés est conditionnée à l'arrivée préalable de v2 doyennés — à commissionner par Soleil dans le prochain brief.

Une zone grise existe : 4 des 34 « pieves » couvrent en pratique un territoire de niveau doyenné contemporain (Cap Corse, Balagne, Bastia, Ajaccio). Voir section *Doyennés* ci-dessous pour la décision à prendre.

## Inventaire complet du corpus patrimoine

### Diocèses — 5 fiches v2 + 3 fiches v3 + 1 site dérivé v3

Fiches v2 (factuelles, source `docs/fiches_sites/diocese_*.md`) :

- `dioceses/ajaccio_v2.md`
- `dioceses/aleria_v2.md`
- `dioceses/mariana_v2.md`
- `dioceses/nebbio_v2.md`
- `dioceses/sagone_v2.md`

Fiches v3 (sensorielles, déplacées depuis `fiches_dioceses_v3/`) :

- `dioceses/mariana_v3.md`
- `dioceses/nebbio_v3.md`
- `dioceses/sagone_v3.md`

Sans v3 actuellement : ajaccio, aleria.

**Note Aléria** : un fichier v2 existe pour le diocèse historique d'Aléria (`docs/fiches_sites/diocese_d_aleria.md`) — migré vers `dioceses/aleria_v2.md`. Le contenu v3 fourni dans le brief (la fiche-modèle « ville rectangle ») a été placé en `sites/aleria_ruine_v3.md` puisqu'il porte sur la ville antique exhumée et non sur l'institution diocésaine. Une v2 distincte pour le site antique existe également : `docs/fiches_sites/aleria_antique.md` → migrée comme `sites/aleria_antique_v2.md` dans le lot sites (voir ci-dessous, à confirmer ou renommer).

**Drafts diocèses non promus en v2** : `_drafts/fiches_pieve/fiche_diocese_*_v1.md` couvrent ajaccio, aleria, mariana, nebbiu, sagone (drafts antérieurs aux v2 actuelles, conservés en place) + un sixième : `fiche_diocese_accia_v1.md`. Le diocèse historique d'Accia (Castagniccia, supprimé au XVᵉ siècle) ne dispose pas encore d'une v2 promue. À arbitrer.

### Doyennés — 0 fiche v2, 0 fiche v3

Le dossier `doyennes/` est vide.

**Liste canonique des 10 doyennés contemporains** (source : `_drafts/doyennes_communes_mapping.json`, diocèse d'Ajaccio post-Concordat) :

1. Doyenné du Cap
2. Doyenné de Bastia
3. Doyenné du Golo
4. Doyenné Balagne
5. Doyenné Cortenais
6. Doyenné Piana-Vico-Sari
7. Doyenné Plaine Orientale
8. Doyenné d'Ajaccio
9. Doyenné Prunelli-Taravo-Valinco
10. Doyenné Extrême-Sud

**Aucun de ces 10 doyennés ne dispose d'une fiche v2 dans le corpus.** Tous sont à commissionner pour la prochaine vague.

**Zone grise — 4 pieves au format doyenné** : les 4 fiches `pieves/cap_corse_v2.md`, `pieves/balagne_v2.md`, `pieves/bastia_v2.md`, `pieves/ajaccio_v2.md` sont écrites au format de synthèse régionale (regroupement de pievi médiévales sous une étiquette unifiée — chaque fiche le déclare elle-même). Leur territoire correspond approximativement à 4 des 10 doyennés contemporains (Doyenné du Cap, Doyenné Balagne, Doyenné de Bastia, Doyenné d'Ajaccio).

Caveat : la correspondance n'est pas parfaite. Le Doyenné du Cap moderne englobe en plus le secteur Saint-Florent / Patrimonio / Oletta / Olcani (rattaché au Nebbio historique). La fiche pieve Cap Corse couvre uniquement la presqu'île. Si Soleil souhaite promouvoir ces 4 fiches en doyennés v2, un complément territorial sera nécessaire pour le Cap, et la fiche Bastia (très urbaine) ne couvre que la commune de Bastia (cohérent avec le Doyenné de Bastia moderne, qui ne couvre qu'INSEE 2B033).

**Décision demandée à Soleil** :
- Option A : laisser les 4 fiches en pieves/ et commissionner 10 v2 doyennés ex nihilo.
- Option B : promouvoir les 4 fiches en doyennes/ (avec ajustements territoriaux pour le Cap), commissionner 6 v2 doyennés pour les 6 manquants (Golo, Cortenais, Piana-Vico-Sari, Plaine Orientale, Prunelli-Taravo-Valinco, Extrême-Sud).
- Option C : autre.

### Pievi — 34 fiches v2

Toutes copiées depuis `docs/_drafts/fiches_pieve/fiche_pieve_*_v1.md` avec renommage `_v1.md` → `_v2.md` selon la nouvelle convention de versioning.

Liste : ajaccio, alesani, ampugnani, balagne, bastia, bonifacio, bozio, caccia, campoloro, cap_corse, carbini, casinca, cinarca, cruzini, fiumorbo, freto, ghisoni, giovellina, istria, moriani, nebbiu, niolu, orezza, ornano, rogna, rostino, sartene, sorroinsu, tallano, vallerustie, venaco, verde, vico, vivario.

Sans v3 : toutes (34/34).

### Sites — 191 fiches v2

Copiées depuis `docs/fiches_sites/*.md` (180 fichiers, hors les 5 diocèses) + `docs/fiches_sites_edifices_romans/*.md` (12 fichiers). Renommage `<nom>.md` → `<nom>_v2.md`. Plus 1 fiche v3 ajoutée : `sites/aleria_ruine_v3.md`.

Sans v3 : 190/191. Le seul site avec v3 est Aléria (la ruine antique).

## Aléria — clarification de classement

Trois entités distinctes au nom Aléria :

- `dioceses/aleria_v2.md` — diocèse historique (institution médiévale, supprimée 1801) ;
- `sites/aleria_antique_v2.md` — site archéologique de la ville antique romaine (état actuel : ruines fouillées) ;
- `sites/aleria_ruine_v3.md` — fiche v3 sensorielle portant sur la ville antique (la « ville rectangle »).

La fiche v3 fournie dans le brief porte explicitement sur le site antique exhumé (mention du forum, des rues, des temples, du XXᵉ siècle), donc classement en `sites/`.

## Choix stylistiques v3 — sans objet pour cette vague

Aucune fiche v3 doyenné rédigée. Les ajustements appris du premier lot diocèses (concordat napoléonien sans année, vérif cardinaux, anti-ambiguïté « tenu à distance par », anti-abstraction administrative en fermeture, possessifs plats, dates parcimonieuses) sont consignés ici pour la prochaine vague.

## Points d'incertitude factuelle

Aucune note `[À ARBITRER]` insérée dans des fiches puisque aucune v3 n'a été rédigée. Les décisions en attente concernent l'arborescence et la liste à commissionner :

1. **Promotion ou non des 4 pieves au format doyenné** (Option A/B/C ci-dessus).
2. **Diocèse d'Accia** : draft existant, pas de v2. À promouvoir ou à laisser en draft ?
3. **Convention de nommage Aléria site** : `aleria_ruine_v3.md` retenu d'après le 1er message Soleil. Renommer en `aleria_ville_antique_v3.md` si préféré.
4. **Cohabitation v2 doyenné / v2 pieve homonyme** : si l'Option B est retenue, il faudra trancher si la fiche Cap Corse devient doyenne_du_cap_v2 (avec sortie de pieves/) ou si les deux coexistent (un doyenné v2 distinct, la pieve historique du cap restant en pieves/cap_corse_v2.md). La seconde voie préserve la granularité historique mais demande une réécriture v2 pour le doyenné.

## Récapitulatif

Arborescence créée :
```
fiches_patrimoine/
├── RAPPORT_SESSION_DIOCESES_V3.md   (rapport vague précédente)
├── RAPPORT_SESSION_DOYENNES_V3.md   (ce rapport)
├── dioceses/   (5 v2 + 3 v3)
├── doyennes/   (vide)
├── pieves/     (34 v2)
└── sites/      (190 v2 + 1 v3)
```

Ancien dossier `fiches_dioceses_v3/` supprimé.

Aucun fichier original modifié dans `docs/fiches_sites/`, `docs/fiches_sites_edifices_romans/` ou `docs/_drafts/fiches_pieve/`. Migration en mode copie, sauf pour les 3 fiches v3 diocèses + leur rapport (déplacement strict — l'ancien dossier était dédié au workflow v3 et n'avait pas vocation à survivre).

Aucune action git.

## Durée

Session ponctuelle. Inventaire + migration en lot via bash. Aucune rédaction v3 doyennés à attendre tant que la décision de classement n'est pas tranchée.
