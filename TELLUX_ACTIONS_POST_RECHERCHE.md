# TELLUX — Actions post-recherche

**Date :** 17 avril 2026
**Statut :** Plan d'actions issu de la digestion des rapports R1-R7
**Règle :** Aucune action ne modifie le code (index.html). Aucune action ne crée de partenariat fictif.

---

## Principe de classement

Chaque action est classée selon :
- **Destinataire** : App (voie A = gelée v6, voie B = horizon 3-6 mois), Dossiers de diffusion, CTC, Publications, Partenariats
- **Priorité** : P1 (immédiat, < 2 semaines), P2 (court terme, 1-2 mois), P3 (moyen terme, 3-6 mois)
- **Dépendance** : ce qui doit être fait avant

---

## 1. Actions sur l'application — Voie A (v6 gelée)

La v6 est gelée et sert de démonstration pour la candidature CTC. Aucune modification de code. Les actions ci-dessous sont des corrections de contenu ou de présentation qui peuvent être reportées dans les textes d'interface sans toucher au moteur.

### A-1. Corriger la portée de H1 dans les popups patrimoine [P1]

**Quoi :** Les popups des sites mégalithiques doivent mentionner que la corrélation granit × failles est un résultat local corse (p < 10⁻⁴), pas une loi universelle.
**Pourquoi :** R6 invalide la généralisation mondiale.
**Comment :** Ajouter dans le texte popup : « Corrélation statistiquement significative en Corse. Non généralisable à l'échelle mondiale (Göbekli Tepe, Malte, Rapa Nui : substrats non quartzeux). »
**Voie :** B (pas urgent pour la démo CTC, mais à corriger avant toute communication scientifique).

### A-2. Intégrer le cadre nocebo/salutogenèse dans la page « À propos » [P2]

**Quoi :** La page d'information de l'app doit expliciter que Tellux s'appuie sur le corpus nocebo/contrôle perçu, pas seulement sur la mesure physique.
**Pourquoi :** R4 établit que le contrôle perçu est le levier indépendant le plus solidement documenté. C'est l'argument scientifique le plus fort du projet.
**Comment :** Paragraphe de 5-6 lignes : « Les études montrent que fournir des mesures personnelles objectives d'exposition augmente le sentiment de maîtrise sans augmenter la perception du risque (Zeleke 2019). Tellux agit sur les deux voies : réduction mesurable de l'exposition et restauration du contrôle perçu. »
**Voie :** B.

### A-3. Ajouter les valeurs d'atténuation par matériaux dans le diagnostic permaculture [P2]

**Quoi :** Le module permaculture peut afficher, à côté des recommandations de haies, les ordres de grandeur d'atténuation RF (ITU-R P.833 : 3-10 dB pour 20 m de maquis, ITU-R P.2040 : 30-50 dB pour mur granit 60-100 cm).
**Pourquoi :** R5 fournit des chiffres sourcés et normalisés.
**Comment :** Table de référence dans le panneau info du diagnostic.
**Voie :** B.

### A-4. Supprimer toute référence résiduelle aux « réseaux Hartmann/Curry » [P1]

**Quoi :** Vérifier qu'aucun texte, commentaire ou tooltip de l'interface ne mentionne ces grilles.
**Pourquoi :** Retirées du corpus en avril 2026 (niveau D confirmé).
**Comment :** Grep dans le HTML, corriger si trouvé.
**Voie :** A (nettoyage minimal, pas de changement fonctionnel).
**Dépendance :** Vérification à faire en session code.

---

## 2. Actions sur l'application — Voie B (horizon 3-6 mois)

### B-1. Module « Parcours écologie EM » [P3]

**Quoi :** Nouveau module permettant de créer un itinéraire de mesure sur une commune (10 stations : centre-bourg, carrughju, abside, pied d'antenne, maquis, prairie, site mégalithique, etc.) avec affichage comparatif.
**Pourquoi :** H87 (parcours pilote). Démonstrateur concret pour les communes.
**Comment :** Wireframe puis intégration Voie B. Prioriser la restitution visuelle (carte + profil en barres).
**Dépendance :** Campagne de mesure terrain sur au moins une commune pilote.

### B-2. Couche « atténuation bâti estimée » [P3]

**Quoi :** Superposer à la carte une estimation de l'atténuation RF par le bâti, basée sur l'âge et le type de construction (pierre massive, béton, placoplâtre).
**Pourquoi :** R5 fournit les coefficients ITU-R par matériau. Données cadastrales BD TOPO disponibles.
**Comment :** Algorithme simplifié : année construction + matériau dominant → dB estimé. Affichage semi-transparent.
**Dépendance :** Accès BD TOPO IGN Corse. Validation des hypothèses matériaux par commune.

### B-3. Trois lectures parallèles dans les popups de mesure [P3]

**Quoi :** Tout popup affichant une valeur de champ doit donner trois repères : valeur réglementaire française (41-61 V/m), médiane ANFR (0,38 V/m), seuil SBM-2015 (0,61 V/m « extrême »).
**Pourquoi :** R5 recommande explicitement cette triple lecture pour ne pas trancher entre cadres.
**Comment :** Ajout dans la fonction bindPopup des couches mesures.

### B-4. Avertissement Wiedemann dans le module diagnostic [P2]

**Quoi :** Si un diagnostic Tellux génère un score d'exposition élevé, l'interface doit accompagner le résultat d'un message cadrant : « Ce score reflète une estimation. Il n'est pas un diagnostic médical. Agir sur votre environnement augmente votre sentiment de maîtrise, indépendamment du niveau mesuré. »
**Pourquoi :** Wiedemann & Schütz 2005 et Boehmert 2018 montrent que la communication précautionniste peut augmenter la perception du risque. Garde-fou anti-nocebo intégré à l'interface.
**Voie :** B.

---

## 3. Ajustements des dossiers de diffusion

### D-1. TELLUX_DOSSIER_ASSO_EM.md — Mise à jour nocebo/contrôle perçu [P1]

**Quoi :** Ajouter un paragraphe sur le cadre nocebo/salutogenèse comme fondement scientifique de Tellux. Remplacer toute formulation résiduelle « deux réalités différentes ».
**Pourquoi :** R4 rend ce cadre incontournable. Les associations EM doivent comprendre que Tellux ne nie pas la souffrance EHS (l'ANSES la reconnaît) mais propose un levier d'action fondé sur le contrôle perçu.
**Attention :** Formulation délicate. Ne pas donner l'impression de réduire l'EHS au nocebo. Dire : « Les études montrent que la perception d'exposition prédit les symptômes indépendamment de l'exposition mesurée. Tellux agit sur les deux dimensions : réduction de l'exposition ET restauration du contrôle perçu. »

### D-2. TELLUX_DOSSIER_AGRO_BIO.md — Enrichir avec R3 et R5 [P1]

**Quoi :** Intégrer :
- Données Erdreich 2009 et Rigalma 2010/2011 (seuils bovins)
- Vide documentaire ovins/caprins comme axe de recherche corse
- Distances de précaution 150 m HTA / 300 m THT (Shepherd, Burda)
- Atténuation par haies (ITU-R P.833, chiffres précis)
- Référence aux projets INRAE en cours (AgroE2, CNE-CNIEL, BRGM)
**Pourquoi :** Le dossier agro actuel manque de données quantitatives.

### D-3. TELLUX_DOSSIER_MAIRIES_PATRIMOINE.md — Nuancer H1 et ajouter urbanisme EM [P2]

**Quoi :** 
- Nuancer la présentation de la corrélation mégalithes/granit (locale, pas universelle)
- Ajouter le concept d'urbanisme EM : jurisprudence CE 26/10/2011, chartes municipales, instruction Batho, fenêtre PADDUC
- Intégrer les données d'atténuation par murs de pierre (30-50 dB) comme argument patrimonial
**Pourquoi :** R5 et R6 renouvellent substantiellement l'argumentaire mairies.

### D-4. TELLUX_DOSSIER_SCIENTIFIQUES.md — Actualiser avec les 30 nouvelles références [P2]

**Quoi :** Le dossier scientifiques doit refléter le corpus v7. Ajouter :
- Wang & Kirschvink 2019 (magnétoréception humaine)
- Glass & Singer 1972 / Baliatsas 2015 / Zeleke 2019 (contrôle perçu)
- Données ITU-R P.2040 et P.833 (matériaux et végétation)
- Les 3 trous de littérature identifiés par R7 (géopolymères corses, UCS bio-bricks, piézoélectricité bornée)
**Pourquoi :** Crédibilité auprès des profils scientifiques A-E identifiés dans le dossier.

### D-5. TELLUX_KIT_ENVOI_EM.md — Ajuster le ton [P2]

**Quoi :** Vérifier que les modèles d'email respectent les 3 formulations interdites et intègrent le cadre salutogénique.
**Pourquoi :** Cohérence épistémique sur tous les supports.

---

## 4. Compléments pour la candidature CTC

### C-1. Intégrer le cadre nocebo/salutogenèse dans la section « Fondements scientifiques » [P1]

**Quoi :** La candidature v8 mentionne 83 hypothèses et le corpus scientifique, mais ne met pas assez en avant le cadre nocebo/contrôle perçu comme socle principal.
**Pourquoi :** C'est l'argument le plus solide et le plus différenciant du projet. Aucun autre outil de cartographie EM ne s'adosse à ce corpus psycho-physique.
**Comment :** Paragraphe de 8-10 lignes dans la section fondements, citant Baliatsas 2015, Zeleke 2019, Glass & Singer 1972, Kaptchuk 2010.

### C-2. Ajouter les nouvelles hypothèses H84-H94 au tableau [P1]

**Quoi :** La candidature cite 83 hypothèses. Les 11 nouvelles (H84-H94) portent le total à 94.
**Pourquoi :** Renforce la profondeur du projet auprès de la CTC.
**Comment :** Tableau additionnel en annexe ou intégration dans le tableau existant.

### C-3. Nuancer H1 dans le texte candidature [P1]

**Quoi :** Ajouter explicitement que la corrélation mégalithes/granit est locale (Corse) et ne se généralise pas mondialement.
**Pourquoi :** Un évaluateur scientifique informé repérera immédiatement le sur-claim. Mieux vaut le nuancer soi-même.

### C-4. Mentionner les projets INRAE en cours comme contexte institutionnel [P2]

**Quoi :** AgroE2 (ADEME 2024-2027), CNE-CNIEL, BRGM sols, SICECLAIR. Tellux s'inscrit dans une dynamique de recherche nationale, pas en isolement.
**Pourquoi :** Crédibilité institutionnelle. La CTC appréciera l'inscription dans un écosystème plus large.

### C-5. Ajouter la fenêtre PADDUC comme levier politique [P2]

**Quoi :** L'évaluation sexennale du PADDUC (2024-2026) est une fenêtre pour un volet EM dans la planification territoriale corse.
**Pourquoi :** Argument spécifiquement CTC. Aucun autre projet ne le porte.

---

## 5. Publications et communications

### P-1. Note de position « Urbanisme EM en Corse » [P2]

**Quoi :** Document de 10-15 pages synthétisant R5 pour un public de planificateurs territoriaux. Contenu : atténuation par matériaux (ITU-R), jurisprudence CE 2011, chartes municipales, fenêtre PADDUC, parcours pilote.
**Destinataire :** CTC, DREAL Corse, Agence d'Aménagement Durable, élus.
**Format :** PDF maquetté, version web sur site Tellux.

### P-2. Fiche technique « Atténuation RF du bâti corse » [P2]

**Quoi :** 4 pages, format A4, données ITU-R appliquées aux matériaux corses. Tableau granit/schiste/béton/placoplâtre avec dB par fréquence. Recommandations rénovation.
**Destinataire :** Architectes, maîtres d'ouvrage, CAUE Corse.
**Format :** PDF imprimable.

### P-3. Article « 3 trous de littérature corses » [P3]

**Quoi :** Communication courte (note, letter) proposée à une revue de géophysique ou de radioélectricité, identifiant les 3 lacunes R7 : géopolymères à précurseurs corses, caractérisation diélectrique ITU-R du granit corse, piézoélectricité bornée dans matériaux de construction.
**Destinataire :** Revue type *Journal of Materials Science*, *Construction and Building Materials*, ou *Applied Sciences*.
**Dépendance :** Mesures en laboratoire (VNA, échantillons) — nécessite partenariat recherche.

### P-4. Communication « Nocebo et écologie EM : le cas Tellux » [P3]

**Quoi :** Proposition d'article ou de communication dans un colloque santé environnementale, présentant le cadre théorique Tellux (nocebo + contrôle perçu + salutogenèse = dispositif EHL).
**Destinataire :** Colloque SFSE, Journées ANSES, ou revue *Environnement Risques Santé*.
**Dépendance :** Données d'usage Tellux (SOC-13 pré/post, au moins N=30).

---

## 6. Partenariats à amorcer

### PA-1. INRAE / Idele — Réseau courants parasites [P2]

**Quoi :** Contacter le groupe de travail INRAE (AgroE2, Idele, BRGM, XLIM) pour proposer la Corse comme site pilote complémentaire. Argument : sols granitiques/schisteux, élevage extensif ovin/caprin, hydrogéologie fracturée.
**Dépendance :** Dossier scientifiques (D-4) à jour.
**Risque :** Tellux est solo et pré-institutionnel. Posture = fournisseur de terrain et de données cartographiques, pas partenaire de recherche au sens académique.

### PA-2. Università di Corsica — Laboratoire matériaux [P3]

**Quoi :** Proposer une collaboration sur la caractérisation diélectrique des granits et schistes corses (H88) et/ou sur un géopolymère à précurseurs locaux (H91).
**Dépendance :** Fiche technique P-2 comme carte de visite.
**Risque :** Même posture que PA-1.

### PA-3. Groupe Chiroptères Corse [P3]

**Quoi :** Proposer un comptage acoustique à distance variable d'antennes-relais (H90). Le Groupe possède les détecteurs ultrasoniques et les sites de suivi.
**Dépendance :** Protocole de mesure formalisé, accord sur les objectifs.

### PA-4. Chambre d'agriculture Corse — Filière ovine/caprine [P3]

**Quoi :** Présenter le vide documentaire R3 (aucune étude caprins) et proposer un protocole de mesure tensions vagabondes sur exploitations AOP Brocciu.
**Dépendance :** Dossier agro (D-2) à jour.

### PA-5. CAUE Corse / DRAC — Parcours patrimoine EM [P3]

**Quoi :** Proposer le parcours « pierre et ondes » (H87) comme projet de médiation culturelle combinant archéologie, construction vernaculaire et pédagogie EM.
**Dépendance :** Note de position P-1.

---

## 7. Tableau de priorisation

| Priorité | Actions | Horizon |
|---|---|---|
| **P1** | A-4 (nettoyage Hartmann), D-1 (asso EM nocebo), D-2 (agro enrichi), C-1 (CTC nocebo), C-2 (H84-H94), C-3 (H1 nuancé), A-1 (popup H1) | < 2 semaines |
| **P2** | A-2 (à propos nocebo), A-3 (atténuation permaculture), B-4 (avertissement Wiedemann), D-3 (mairies), D-4 (scientifiques), D-5 (kit envoi), C-4 (INRAE), C-5 (PADDUC), P-1 (note urbanisme EM), P-2 (fiche bâti), PA-1 (INRAE) | 1-2 mois |
| **P3** | B-1 (parcours EM), B-2 (couche atténuation), B-3 (triple lecture), P-3 (article trous littérature), P-4 (article nocebo), PA-2 (Uni Corse), PA-3 (chiroptères), PA-4 (chambre agri), PA-5 (CAUE) | 3-6 mois |

---

## 8. Ce que ce plan ne fait pas

- **Ne modifie pas le code** (index.html). Les actions App/Voie B sont des spécifications, pas des implémentations.
- **Ne crée pas de partenariats fictifs.** Les contacts PA-1 à PA-5 sont des propositions à initier par Soleil, pas des accords existants.
- **Ne touche pas aux données scientifiques** (SITES, CHURCHES, FAILLES_CORSE, etc.).
- **Ne touche pas aux fonctions de calcul** (calcHuman, calcHeritagePiezo, etc.).
- **Ne remplace pas le catalogue d'hypothèses.** Les H84-H94 restent dans TELLUX_HYPOTHESES_UPDATE.md jusqu'à intégration par Soleil.

---

*Ce plan d'actions est un outil de pilotage pour Soleil. Les priorités P1 sont actionnables immédiatement. Les P2 et P3 dépendent de la validation CTC et des retours terrain.*

*Volume : ~260 lignes. Actions identifiées : 28 (7 App, 5 Dossiers, 5 CTC, 4 Publications, 5 Partenariats, 2 compléments).*
