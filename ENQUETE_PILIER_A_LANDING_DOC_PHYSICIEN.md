# Enquête Pilier A / landing / doc physicien — synthèse

**Date :** 2026-04-23  
**Auteur :** Claude Code (enquête read-only)  
**Destinataire :** session claude.ai web suivante pour rédaction du prompt d'intégration  
**Branche :** `docs/enquete-pilier-a-landing` — PR en attente, pas de merge sans validation Soleil

---

## 1. Nombre d'hypothèses Pilier A

**Réponse : 14 (pas 15)**

La mention "15 hypothèses" dans le chantier est une erreur. Le document de référence `_corpus/HYPOTHESES_SCIENTIFIQUES.md` (v1, 2026-04-21) indique explicitement en en-tête : **"14 hypothèses retenues sur critères C1-C5"**, et le tableau de synthèse confirme un total de 14 fiches.

Liste exhaustive :

| Fiche | Bloc thématique | Titre condensé |
|---|---|---|
| S1 | M/ELF | Coïncidence anomalies géomagnétiques naturelles × sites anciens |
| S2 | M/ELF | Amplification du champ géomagnétique par la susceptibilité magnétique du substrat |
| S3 | M/ELF | Courants telluriques DC / sub-1 Hz aux convergences faille × hydrographie |
| S4 | M/ELF | Loi de décroissance composite vs distance à la ligne HTA |
| S5 | M/ELF | Set de régression ELF permanent (20 points témoins v2) |
| S6 | Ionisant | Décomposition empirique de la dose gamma terrestre NCRP 94 sur granites varisques corses |
| S7 | Ionisant | Concentration radon intérieur Corse : prédiction potentiel IRSN vs mesure habitats |
| S8 | Ionisant | Réponse adaptative ionisante et populations corses isolées |
| S9 | Couplages | Corrélation anomalie crustale EMAG2 × composite géomagnétique naturel sur sites anciens |
| S10 | Couplages | Interaction EM statique × ionisant (preuve clinique MR-Linac) et extension exposition ambiante |
| S11 | Couplages | Différentiel de susceptibilité magnétique granite varisque vs calcaire sédimentaire, hors zone HTA 2 km |
| S12 | RF | Évitement apparent antennes vs score géo sur églises romanes corses |
| S13 | RF | Atténuation RF en forêt laricio corse comme site modèle shinrin-yoku |
| S14 | Méthodologie | Écart IGRF-14 / WMM 2025 comme contrôle métrologique continu du moteur M statique |

**Source :** `_corpus/HYPOTHESES_SCIENTIFIQUES.md`, lignes 63-67 (tableau) et en-tête ligne 8.

**Évolution depuis PR #92 :** aucune. Aucun commit modifiant `_corpus/HYPOTHESES_SCIENTIFIQUES.md` après sa création le 2026-04-21. Aucun identifiant S15 ou numérotation au-delà de S14 dans le workspace. La confirmation de 14 fiches était déjà présente dans le document `PILIERS_AB_RECOS_COWORK.md` (PR #92).

**Origine probable de la mention "15" :** confusion avec la colonne "Cible prompt" du tableau de synthèse, qui indique "10-15" comme fourchette d'exposition landing — pas un décompte d'hypothèses.

---

## 2. État de la landing `index.html` concernant le Pilier A

**Statut : absent**

Les hypothèses du Pilier A (S1-S14) ne sont pas visibles sur la landing. Aucune section préparée ne les accueille.

**Détail :**

- **Mentions trouvées :**
  - Ligne 380 : "Chaque valeur affichée indique son statut : mesuré, modélisé, ou hypothèse en cours de test." — générique, position épistémique, pas lié au Pilier A
  - Ligne 546 : "Tellux distingue rigoureusement ce qui est mesuré, ce qui est modélisé, et ce qui reste à l'état d'hypothèse." — idem
  - Ligne 341 : `IGRF-14 · EMAG2v3 · LCS1` — mention de source de données, pas d'hypothèse
  - Aucune occurrence de "Pilier", "S1", "S2", …, "S14", "hypothèse scientifique", "corpus d'hypothèses"

- **Sections candidates à l'accueil :**
  - `id="ressources"` (lignes 470-500) : 3 fiches "PDF bientôt disponible" (Cadre scientifique Tellux v2.1 / Position épistémique / Guide d'interprétation). Cette section est la candidate naturelle pour ajouter une 4e fiche "Hypothèses scientifiques Pilier A" ou un lien vers un document dédié.
  - `id="corpus"` (lignes 375-392) : section "Corpus scientifique", 6 reference pills + lien vers `corpus.html`. Pourrait accueillir une mention des hypothèses ou un lien, mais elle est stylistiquement orientée références peer-reviewed, pas hypothèses.

- **Liens sortants pertinents :**
  - `corpus.html` (via lien dans section `id="corpus"`) : page publique références peer-reviewed + méthodologie, activée en PR #91. Ne contient pas les hypothèses Pilier A.
  - `patrimoine.html` : aucun lien depuis la landing. Non applicable.

---

## 3. État du doc physicien

**Statut : version avancée (non soumise, non versionnée dans git)**

**Fichier(s) identifié(s) :**

- `docs/physicien/DOCUMENT_SOUMISSION_PHYSICIEN_TELLUX_v1.md`  
  Date : 2026-04-20 — 29 185 octets — Version initiale (premier jet adressé au relecteur potentiel).

- `docs/physicien/DOCUMENT_SOUMISSION_PHYSICIEN_TELLUX_v1_backup_20260421.md`  
  Date : 2026-04-21 — 29 185 octets — Backup de la v1 avant réécriture v1.1 (même contenu que v1, taille identique).

- `docs/physicien/DOCUMENT_SOUMISSION_PHYSICIEN_TELLUX_v1.1.md`  
  Date : 2026-04-21 — 44 149 octets, 368 lignes — **Version courante**. Enrichie de 5 compléments post-v1 : magnétoréception Chae et coll. 2022, variations temporelles champ magnétique, annexe traitement EMAG2v3, section "Références de cadrage et contrepoints", formalisation statut note de tri. 10 sections + Annexe A.

**Note de statut git :** les trois fichiers sont exclus du dépôt git par le pattern `.gitignore` : `DOCUMENT_SOUMISSION_*.md`. Ils existent uniquement en local, sans historique de commit. Aucun commit du dépôt public ne les référence directement.

**Structure v1.1 (résumé neutre) :** document de 368 lignes adressé à un physicien ou géophysicien tiers qualifié (non nommé dans le fichier). Présente l'architecture du modèle composite à 4 domaines physiques (M statique + ELF / E différé / RF / I ionisant), puis soumet trois choix méthodologiques à avis externe via des questions numérotées : Q4.x sur la composante gamma terrestre (formule NCRP 94, paramètres cosmiques), Q5.x sur la superposition magnétique statique et ELF 50 Hz, Q6.x sur les pondérations du mode Expertise. Document complet, rédigé, sans lacune apparente identifiable depuis l'extérieur.

**Relation avec hypothèses Pilier A :** le doc physicien est un **précurseur structurant** du Pilier A, pas un document redondant. Chaque fiche S du Pilier A cite dans sa section "Rattachement stratégique" une ou plusieurs questions Q du doc physicien auxquelles elle répond (ex. S1 → Q5.1, S2 → Q5.2, S4 → Q5.1 + Q6.1, S6 → Q4.1 + Q4.2). Le doc physicien traite des fondements méthodologiques du modèle ; les hypothèses Pilier A formulent les questions scientifiques testables qui en découlent. Les deux documents sont complémentaires et non substituables.

---

## 4. État global du chantier et sous-tâches restantes

**Statut global : deux sous-chantiers distincts à des stades très différents**

| Sous-chantier | Statut |
|---|---|
| Corpus Pilier A (S1-S14) | Quasi-abouti — 14 fiches rédigées avec protocoles, ancrage littérature, variables |
| Intégration landing | À faire entièrement — aucune préparation |
| Doc physicien — rédaction | Quasi-abouti — v1.1 complète en local |
| Doc physicien — soumission | À faire — aucune preuve d'envoi ni de contact relecteur identifiée |

**Sous-tâches restantes :**

1. **Valider les arbitrages §7 du corpus Pilier A** : Soleil doit trancher 4 points ouverts dans `_corpus/HYPOTHESES_SCIENTIFIQUES.md` §7 — (a) intégration ou non de H20 en sous-protocole de S1, (b) double usage A+B validé ou exclu pour H1/H18/H21, (c) statut H85-H87 (mines EM vs faune), (d) statut H88 et H91 (gelés en attente clarification).

2. **Décider du format d'exposition des hypothèses sur la landing** : trois options à trancher — (a) section dans `index.html` (ex. 4-6 hypothèses phares avec formulation grand public), (b) page dédiée type `hypotheses.html` liée depuis la landing, (c) intégration dans `corpus.html` existant sous un onglet ou une section supplémentaire.

3. **Rédiger les versions grand public des hypothèses** : les fiches S sont rédigées en langage scientifique. Il faut dériver pour chaque hypothèse retenue en landing une formulation de 2-3 lignes compréhensible par un lecteur non-physicien. Priorité landing documentée dans les fiches : S1, S4, S6, S7, S11, S12, S13 (mention explicite "Landing page" dans chaque fiche).

4. **Intégrer les hypothèses dans `index.html` ou créer la page dédiée** : travail de développement HTML/CSS sur le modèle de `corpus.html` ou par ajout dans la section `id="ressources"`.

5. **Identifier le relecteur physicien** : le doc physicien v1.1 mentionne un "destinataire : physicien ou géophysicien tiers qualifié (à préciser selon interlocuteur)". Aucun nom de contact n'est identifiable dans les fichiers scannés.

6. **Soumettre le doc physicien v1.1** : envoi au relecteur identifié (email ou rencontre), après décision de la forme de transmission.

7. **Décider si la landing hypothèses est conditionnée au retour du physicien** : si oui, tâche 6 bloque tâches 3-4 ; si non, tâches 3-4-5 peuvent démarrer immédiatement.

**Séquencement :**

- Tâches **1 et 2** (arbitrages Soleil) sont des décisions à prendre avant de commencer la rédaction landing — elles sont rapides (revue de §7 du corpus).
- Tâches **3 et 4** (landing) sont indépendantes de la soumission du doc physicien, sauf décision contraire de Soleil (tâche 7).
- Tâches **5 et 6** (doc physicien) sont indépendantes de la landing.
- Aucune dépendance circulaire. Schéma optimal : décisions 1+2+7 → puis 3+4+5+6 en parallèle.

---

## 5. Zones d'incertitude résiduelles

1. **Origine de la mention "15 hypothèses"** dans la to-do initiale : le prompt de départ cite "Pilier A 15 hypothèses landing". L'enquête confirme 14 fiches, mais la source exacte de la mention "15" n'a pas été retrouvée (pas de fichier to-do explicite scannable dans ce workspace). Possibilité non exclue : une 15e fiche était envisagée et abandonnée sans laisser de trace, ou la mention venait d'un document de travail intermédiaire non conservé.

2. **Statut du repo privé `tellux-corpus-internal`** : non accessible dans ce workspace. L'enquête précédente (PR #92, `PILIERS_AB_RECOS_COWORK.md`) y référençait `docs/notes-tri/TRANSITION_CORPUS_H1_H88_VERS_2_PILIERS_v1.md` comme "privé, gitignored". Ce fichier existe localement (`docs/notes-tri/TRANSITION_CORPUS_H1_H88_VERS_2_PILIERS_v1.md` visible dans le listing) mais n'a pas été lu dans cette enquête. Si ce fichier contient une liste d'hypothèses différente, il pourrait expliquer la mention "15". **À vérifier ponctuellement si le doute persiste.**

3. **Identité du relecteur physicien** : non résolvable depuis les fichiers du repo public. Soleil dispose probablement de ce contact hors du workspace.

4. **Statut "Consolidation DOCUMENT_SOUMISSION_PHYSICIEN"** dans la to-do : l'enquête identifie le document comme complet en v1.1. La "consolidation" demandée vise probablement soit (a) le commit dans un repo privé ou un archivage sécurisé, soit (b) une révision de fond avant envoi, soit (c) la prise de décision sur l'envoi. La nature exacte de la consolidation attendue n'est pas déductible des seuls fichiers.

---

## 6. Recommandations pour le prompt d'intégration suivant

**Cinq décisions à soumettre à Soleil avant rédaction du prompt d'intégration :**

1. **14 ou 15 ?** Confirmer le chiffre final. Si 14 est correct (ce que l'enquête indique), corriger la to-do pour éviter l'ambiguïté dans les sessions suivantes.

2. **Format landing hypothèses** : choisir parmi les 3 options (section index.html / page dédiée / onglet corpus.html). Cette décision conditionne entièrement le périmètre du prompt d'intégration.

3. **Arbitrages §7 corpus** : valider ou invalider les 4 points ouverts du §7 de `HYPOTHESES_SCIENTIFIQUES.md` avant d'écrire les versions grand public (notamment le statut double A+B pour H1/H18/H21, qui détermine quelles hypothèses apparaissent sur la landing patrimoniale vs la landing scientifique).

4. **Séquencement landing / physicien** : décider si la publication des hypothèses scientifiques sur la landing attend ou non le retour du physicien tiers.

5. **Nature de la "consolidation" doc physicien** : préciser ce que le point to-do "Consolidation DOCUMENT_SOUMISSION_PHYSICIEN" recouvre exactement (archivage / révision / envoi / autre) pour pouvoir formuler un prompt d'intégration ciblé.

---

*Enquête réalisée le 2026-04-23. Fichiers scannés : `_corpus/HYPOTHESES_SCIENTIFIQUES.md`, `_corpus/HYPOTHESES_PATRIMOINE_GAMIFIEES.md`, `_corpus/plan_cadre_v2.1.md`, `index.html`, `docs/physicien/DOCUMENT_SOUMISSION_PHYSICIEN_TELLUX_v1.1.md` (50 premières lignes), `.gitignore`, `PILIERS_AB_RECOS_COWORK.md`. Mode read-only strict respecté. Aucune modification de fichier existant.*
