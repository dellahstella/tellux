# TELLUX — Feuille de route

## 🟢 Court terme — « Version prête à l'emploi + candidature CTC »

Objectif : déposer une candidature CTC solide avec une version du site stable, propre, et visuellement cohérente.

### Étape 1 — Identité visuelle (1 session Opus)
Produire `DIRECTION_ARTISTIQUE.md` finalisé : palette, typo, logo-mark SVG, règles d'usage header/footer/PDF. **Bloquant** pour la suite (captures et exports doivent refléter l'identité finale).

### Étape 2 — Corrections code prioritaires (1-2 sessions Sonnet)
Sprint C du briefing v7 :
- Fixer le wrap infini de la carte (maxBounds).
- Fixer la disparition du marqueur violet de saisie.
- Clarifier l'unité de l'anomalie Monticello.
- Résoudre le conflit popup quadrillage / carrés colorés.

### Étape 3 — Refonte candidature v7 (1-2 sessions Opus)
Sprint A du briefing v7, section par section. Livrable : `CANDIDATURE_TELLUX_v7.docx` remplaçant v6.

### Étape 4 — Captures haute résolution (1 session Sonnet/Haiku)
6-8 captures pour dossier + site de présentation :
- Vue d'ensemble carte
- Panel hypothèses avec tests auto
- Module agronomie
- Popup Indice Tellux
- Couches réseaux EDF + antennes ANFR
- Mégalithes avec scores piézo
- (Mobile) menu hamburger
Format PNG 1920×1080, cohérentes avec la nouvelle identité visuelle.

### Étape 5 — Écosystème partenaires (1 session Opus, en parallèle)
Rédiger email-type de prise de contact associations CEM Corse + associations permaculture + formulaire retour test court. Soleil envoie.
Récolter 2-3 lettres de soutien avant dépôt CTC si timing possible.

### Étape 6 — Relecture finale & dépôt
Relecture croisée (Soleil + Claude Opus) du dossier complet, vérification pièces justificatives, dépôt.

**Durée estimée court terme : 4-6 sessions Claude réparties sur 2-3 semaines**, selon disponibilité Soleil et délai CTC.

---

## 🔵 Long terme

### Axe 1 — Validation scientifique (post-dépôt CTC)
Sprint E du briefing v7 :
- Refactoring FAILLES_CORSE en segments LineString (précision ±300 m).
- Tests automatiques H55–H88.
- Externalisation SITES[] dans JSON hébergé (fin des régressions GPS).
- Protocole calibration Trifield TF2 en aveugle parallèle.
- Tisser lien avec CEREGE (datation Anneaux du Cap Corse), INRAE, laboratoires EM.

### Axe 2 — Écosystème & communauté
- Intégration formulaire « soumettre une étude » → corpus enrichi par la communauté.
- Interface crowdsourcing mesures (table `measurements_validated` Supabase).
- Formation courte aux utilisateurs associatifs (tutoriel vidéo ou PDF).
- Mode « contributeur » identifié (badges gamification actuels étendus).

### Axe 3 — Publication scientifique
Cible : 1 publication open-access en 2027.
- Article méthodo : « Tellux: a citizen-science platform for cross-referencing electromagnetic exposure and megalithic heritage » — journaux candidats : JOSS, GeoHealth, Citizen Science: Theory and Practice.
- Article terrain : réplication Baydilli 2025 sur sols corses, en collaboration avec un labo.

### Axe 4 — Extension mode Architecte
Mode bâtiment actuellement trop fragile pour les pros. Travail nécessaire :
- Intégration données cadastre IGN BD PARCELLAIRE.
- Calcul expo EM par pièce (pas seulement par parcelle).
- Préconisations normées (DTU, norme NF C 15-100 pour l'électrique résidentiel).
- Une fois stable : démarchage architectes, bureaux d'étude, géobiologues pros.

### Axe 5 — Structure juridique Tellux
- Arbitrage statut (micro-entreprise pour démarrer, puis SASU si activité croît).
- Dépôt du nom « Tellux » (INPI) si budget le permet après 1ère tranche CTC.
- Statuts associatifs alternatifs à étudier (association loi 1901 pour volet citoyen + structure commerciale pour volet pro ?).

### Axe 6 — Extension territoriale
- Tellux Sardaigne (mégalithes nuragiques, parenté culturelle Corse-Sardaigne).
- Tellux Méditerranée (Malte, Baléares, Sicile).
- Nécessite : refactoring constants régionales + backend multi-tenant Supabase + hypothèses universelles vs régionales.
- Horizon : 2027-2028.

### Axe 7 — 3D et immersion (aspirationnel)
Pas implémentable aux niveaux de zoom actuels. En attente d'une montée en résolution des données publiques (LiDAR HD IGN couvre la Corse progressivement). À ne pas lancer prématurément.

### Axe 8 — Mode quête / exploration ludique (aspirationnel)
Style Pokémon Go — exploration guidée des sites patrimoniaux avec validation GPS terrain. En attente d'une base utilisateur suffisante et d'une stabilisation du corpus.
