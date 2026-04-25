# Tellux — Feuille de route publique

**Dernière mise à jour :** 25 avril 2026

Document de référence publique présentant la trajectoire générale du projet Tellux. Les détails opérationnels, calendriers précis et éléments stratégiques restent en pilotage interne.

---

## 1. Vision en suite d'applications

Depuis avril 2026, Tellux n'est plus une application monolithique mais une **suite d'applications** déployées progressivement selon la maturité de chaque module.

```
┌─────────────────────────────────────────────────────────────────┐
│                      LANDING PAGE (index.html)                   │
│    Présente l'application de cartographie EM (application 1)     │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  APP 1 — CARTOGRAPHIE EM (app.html)                              │
│  4 domaines physiques + contexte géologique + mode Expertise     │
│  Phase 1 — publique, en cours de stabilisation                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  APP 2 — PATRIMOINE (patrimoine.html)                            │
│  Mégalithes, églises romanes, hypothèses exploratoires           │
│  Phase 2 — non active, accessible via URL directe                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  APP 3 — AGRONOMIE (agronomie.html)                              │
│  Diagnostic parcellaire, recommandations permaculture            │
│  Phase 3 — non active, accessible via URL directe                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Phase 1 — Cartographie EM (en cours, 2026)

### Cible

Publication d'une application de cartographie électromagnétique territoriale rigoureuse et sobre, couvrant quatre domaines physiques distincts :

- **Magnétique statique** (IGRF-14, anomalies crustales EMAG2v3, WMM 2025 cross-check)
- **Magnétique basse fréquence** (ELF 50 Hz, lignes HTA réelles, postes sources, éoliennes)
- **Radiofréquences** (antennes ANFR, émetteurs TDF de radiodiffusion)
- **Ionisant** (composante cosmique altitudinale, classification radon officielle)

### Livrables restants

- Finalisation de l'extraction des modules patrimoine et agronomie depuis `app.html`
- Mise à jour de la landing vers une cohérence totale avec la suite d'applications
- Documentation méthodologique par domaine physique
- Glossaire technique intégré
- Phase d'UI avancée (sélecteur de domaines, badges temps réel)

### Argument différenciant

À notre connaissance, aucun équivalent international n'existe pour un outil cartographique EM territorial avec cette profondeur (quatre domaines physiques distincts, mode Expertise cadré épistémiquement).

### Démarches institutionnelles d'accès aux données

- **2026-04** : initiation des démarches institutionnelles d'accès aux données améliorées (ASNR Téléray, EDF SEI Corse, BRGM Corse, ASNR cellule radon). Première sollicitation méthodologique externe transmise au directeur d'UMR du laboratoire Sciences pour l'Environnement (SPE, Université de Corse) en vue d'orientation vers un relecteur physicien tiers.

Suivi détaillé des envois et des retours : voir section 9 « Suivi des sollicitations institutionnelles ».

---

## 3. Phase 2 — Patrimoine et extensions (après phase 1)

### Conditions de déclenchement

- Phase 1 stabilisée et publiée
- Validation méthodologique par relecture scientifique externe
- Ressources budgétaires acquises

### Contenus envisagés

- Réactivation de l'application patrimoine (mégalithes, églises romanes, hypothèses auto-testables)
- Orientation pédagogique distincte du cadre scientifique R&D
- Intégration des corpus patrimoniaux régionaux corses
- Ouverture multilingue (corse, italien, grec) pour extension à l'espace méditerranéen

---

## 4. Phase 3 — Agronomie sectorielle (horizon ultérieur)

### Conditions de déclenchement

- Phase 2 publiée
- Structuration des besoins agricoles corses identifiée
- Opportunité de financement dédié

### Contenus envisagés

- Diagnostic parcellaire
- Recommandations matériaux (clôtures, irrigation, bâti) selon contexte géologique et magnétique
- Interface simplifiée pour agriculteurs et conseillers

---

## 5. Phase 4 — Dimensions avancées (horizon long)

### Modules envisagés

- Module bâtiment et urbanisme EM résidentiel
- Composante sciences humaines et sociales (représentations du risque EM, dimensions perceptives et contextuelles)
- Infrastructure scientifique dédiée (campagnes de mesure, publications peer-reviewed)

---

## 6. Jalons

| Jalon | Livrable | Horizon |
|-------|----------|---------|
| 1 | Stabilisation architecturale (extraction modules, landing cohérente) | 2026 T2 |
| 2 | Première relecture méthodologique externe | 2026-2027 |
| 3 | Candidature à appels publics de financement | 2026-2027 |
| 4 | Déblocage des constantes gelées post-relecture | 2026 T3 ou ultérieur |
| 5 | Publication phase 1 stabilisée + communication publique | 2026 T3 |

---

## 7. Principes de pilotage

### Discipline sur le périmètre

Chaque phase est strictement cadrée. Les modules suivants existent techniquement dans le dépôt public mais ne sont pas mis en avant dans la landing ni les dossiers de financement en cours.

### Humilité épistémique

- Refus de l'alarmisme et de la trivialisation
- Distinction systématique mécanisme / effet biologique / effet sanitaire / impact populationnel
- Documentation des tensions plutôt que résolution prématurée
- Trois formulations proscrites dans tout contenu Tellux : (1) « deux réalités différentes » (le champ EM est un seul champ physique), (2) « les mesures ne s'additionnent pas » (principe de superposition), (3) « naturel = bénin » (les perturbations géologiques ne sont pas intrinsèquement inoffensives)

### Transparence et ouverture

- Transparence sur financements, partenariats et conflits d'intérêts
- Préférence pour les financements publics
- Ouverture des données et du code selon les principes FAIR
- Pré-enregistrement des protocoles avant collecte de données

### Financements

Stratégie de financement basée sur des candidatures à des appels publics (2026-2027). Partenariats et collaborations scientifiques en cours de construction.

### Indépendance

Projet indépendant. Architecture modulaire permettant la montée en gamme progressive.

---

## 8. Chantiers différés — déclenchement relecture physicien tiers

Les chantiers suivants sont suspendus en attente de deux conditions conjointes :

- Identification et engagement d'un relecteur physicien tiers pour validation méthodologique
- Phase de soumission aux institutions de financement (CTC, FEDER, ANR) atteinte

### Préparation soumission physicien tiers — statut

Le document de soumission au physicien tiers est préparé et à jour au 2026-04-23 (version v1.2). Il intègre les ajustements scientifiques du jour (reformulation S10, amendement S8 avec cadre éthique, ajustements cosmétiques et pédagogiques complémentaires) et demande au relecteur une validation explicite sur les deux points les plus sensibles (questions Q7.6 et Q7.7).

Le document reste en attente de soumission effective, conditionnée à l'identification d'un relecteur physicien tiers. Les chantiers ci-dessous s'activeront une fois cette relecture conduite et la phase de soumission institutionnelle atteinte.

### Chantier 1 — Rédaction du Guide d'interprétation de la carte

- **Statut :** à rédiger
- **Type :** document pédagogique grand public
- **Objet :** expliquer comment lire chaque couche de la carte Tellux, les unités, l'interprétation des gradients, ce qu'est (et n'est pas) l'indice composite.
- **Destinataire :** visiteurs non spécialistes du site
- **État actuel :** placeholder dans `index.html` section `#ressources` (« PDF bientôt disponible »), aucune source markdown
- **Dépendance :** rédaction préalable à la conversion PDF

### Chantier 2 — Rédaction du document « Hygiène EM à domicile »

- **Statut :** à rédiger
- **Type :** document pratique grand public
- **Objet :** recommandations et repères concrets sur l'exposition électromagnétique domestique, fondés sur les références biomédicales retenues par Tellux
- **Destinataire :** public concerné par la réduction d'exposition EM
- **État actuel :** placeholder landing, aucune source markdown

### Chantier 3 — Conversion PDF finale des 3 documents publics

- **Statut :** infrastructure à préparer, conversion à exécuter après validation physicien
- **Documents concernés :**
  - `CADRE_SCIENTIFIQUE_TELLUX_v2.1.1.md` (949 lignes, repo public racine)
  - `TELLUX_POSITION_EPISTEMIQUE.md` (220 lignes, repo public racine)
  - Guide d'interprétation de la carte (à rédiger — Chantier 1 ci-dessus)
- **Dépendance :** Chantier 1 + relecture physicien validée
- **Note :** l'infrastructure PDF (outillage, templates DA v2, exports test) sera préparée séparément, en amont, pour que la conversion finale soit immédiate une fois les conditions réunies.

### Chantier 4 — Remplacement des placeholders landing

- **Statut :** à exécuter après Chantier 3
- **Objet :** remplacer dans `index.html` section `#ressources` les trois mentions « PDF bientôt disponible » par les liens effectifs vers les PDF publiés.
- **Dépendance :** Chantier 3 complet.

---

## 9. Suivi des sollicitations institutionnelles

Tableau de suivi des courriers envoyés aux institutions et chercheurs en lien avec la phase 1 (cartographie EM) et la préparation de la relecture méthodologique externe (cf. section 8). Les colonnes « Date retour » et « Commentaire » sont renseignées au fil des semaines.

| Date envoi prévue | Destinataire | Canal | Objet | Statut | Date retour | Commentaire |
|---|---|---|---|---|---|---|
| 2026-04-28 | Paul-Antoine Santoni — Directeur UMR SPE Université de Corse | Email | Demande d'orientation vers relecteur physicien tiers (relecture méthodologique) | À envoyer | — | — |
| 2026-04-28 | ASNR — Direction Téléray | Email | Accès programmatique balises Téléray AJA + BAP | À envoyer | — | — |
| 2026-04-28 | ASNR — Cellule radon | Email | Géométries polygonales communales + mesures indoor Corse | À envoyer | — | — |
| 2026-04-29 | EDF SEI — Direction Corse | Email | Validation classification HTA + tensions/courants nominaux du réseau Corse | À envoyer | — | — |
| 2026-04-29 | BRGM — Direction régionale Corse | Email | Aéromagnétisme + spectrogamma + flux WFS géologie Corse | À envoyer | — | — |

### Démarches différées

- **RTE Open Data** : demande de cadrage différée post-financement (cf. dette `RTE-OPENDATA-001` dans `DETTES_TECHNIQUES.md`). Motif : le canal officiel RTE passe par un formulaire de contact ODRÉ limité aux messages courts, inadapté à une demande structurée multi-points. Reformulation prévue dans un cadre institutionnel adapté une fois le financement Phase 1 obtenu. En attendant, Tellux continue d'utiliser eco2mix sandbox dans le respect du quota officiel.

---

## 10. Dette technique

Voir `DETTES_TECHNIQUES.md` pour la liste des dettes techniques ouvertes et leur statut.

---

*Fin du document. Mises à jour à chaque jalon structurant.*
