# TELLUX — Briefing consolidé

**Dernière mise à jour :** 8 avril 2026
**Remplace :** TELLUX_BRIEFING_SPRINTS.md, TELLUX_BRIEFING_v7.md, tous les récaps antérieurs.

---

## Le projet en une phrase

Tellux est un tableau de bord web interactif, open-source et gratuit, qui superpose données électromagnétiques institutionnelles, patrimoine mégalithique et agronomie régénérative sur une carte de la Corse.

---

## État actuel (8 avril 2026)

| Composant | Fichier / service | État |
|---|---|---|
| Code source | `tellux_v6_design.html` | v5.9, vague 3+ design, logo V7 intégré |
| Dossier candidature | `CANDIDATURE_TELLUX_v7.docx` | v7, logo clair intégré, styles Tellux, en relecture |
| Direction artistique | `DIRECTION_ARTISTIQUE_v2.md` | Validée et gelée |
| Logo | `TELLUX_LOGO_V7.html` + favicons | V7 validé (T-bouclier, horizon, reflet éthérique, oeil) |
| Déploiement | `tellux.pages.dev` (Cloudflare Pages) | Actif |
| Backend | Supabase PostGIS | Actif, connecté via MCP |
| Cible financement | CTC (Collectivité Territoriale de Corse) | Dossier en préparation |
| Porteur | Soleil (solo), SARL Stella Canis Majoris | Bastia |

---

## Décisions gelées

Ces points sont actés et ne doivent plus être réouverts sauf décision explicite de Soleil.

1. **Palette** — 7 couleurs + fond logo maquis (voir `DIRECTION_ARTISTIQUE_v2.md`).
2. **Typographie** — Fraunces (titres), IBM Plex Sans (corps), JetBrains Mono (données), Cinzel (logo texte).
3. **Logo** — Monogramme T tellurique v7. Structure : T-bouclier gothique, horizon convexe, reflet éthérique, motif de l'oeil.
4. **Tagline** — « Mesurer le vivant ».
5. **Nom affiché** — « Tellux » (sans « Corse » dans le logo, « Corse » dans la tagline du header).
6. **Positionnement** — Jonction rigueur scientifique et sensibilité au territoire. Ni new-age, ni corporate froid.
7. **Projet solo** — Aucune mention d'équipe dans les documents.

---

## Corrections du dossier candidature v7

Retour de relecture de Soleil sur la v6, à appliquer dans `CANDIDATURE_TELLUX_v7.docx` :

- **Section 1 — Résumé exécutif.** Tableau de hiérarchisation des sites pas à jour. Rééquilibrer : antennes ANFR + réseau électrique EDF SEI au même niveau que le patrimoine. Utiliser l'espace blanc disponible.
- **Section 2 — Périmètre technique.** Corriger 80 → 88 hypothèses testables. Mentionner que les ~33 auto-testables vont augmenter. Architecture : plus sur Netlify — décrire l'archi actuelle (single-file HTML + Supabase PostGIS + fallback offline). Densifier.
- **Section 3 — Méthodologie.** Supprimer anglicismes, relecture FR. Déplacer les « incertitudes documentées » vers feuille de route ou rubrique dédiée méthodo. Ajouter un encart protocole de mesures en aveugle parallèle (deux opérateurs indépendants, non communication pendant la mesure). Densifier.
- **Section 4 — Hypothèses.** Texte trop brut. Soit développer l'intérêt scientifique (angle stimulant), soit ajouter 3-5 hypothèses supplémentaires en exemple.
- **Section 5 — Impact / Territoire.** Aérer, rendre plus vivant.
- **Section 6 — Budget.** Solo, aucune embauche. Logement + temps de travail → permet d'arrêter le bâtiment. Phase 1 (~6 mois consolidation) : Soleil apprend l'outil, commence mesures avec protocole en aveugle parallèle. Phase 2 : tiers extérieurs (association CEM, labo) prennent le relais des mesures de validation. Matériel : Trifield TF2 + éventuel capteur piézo.
- **Rédaction entreprise.** Mention de Tellux comme entité (SASU ou micro à arbitrer). Stella Canis Majoris en attente, ne pas miser dessus. Dépôt du nom à évaluer selon budget — noter en feuille de route long terme.

---

## Problèmes techniques connus (non résolus)

Détails et plan de correction dans `TELLUX_ROADMAP.md` (voie A).

- **A-1.** Placement GPS patrimoine sacré / mégalithes — récurrent, points mal placés.
- **A-2.** Alignements : chargement lourd qui fait ramer la carte.
- **A-3.** Panneau explicatif Alignements — ne se ferme pas quand la couche est désactivée.
- **A-4.** Audit complet du pattern couche ↔ panneau ↔ légende à factoriser.
- **A-5.** Marqueur violet de saisie de mesure — pas de bouton d'annulation.
- **A-6.** Unité anomalie Monticello différente du reste.
- **A-7.** Conflit clic popup quadrillage / carrés colorés superposés.
- **A-8.** Captures d'écran haute résolution pour dossier CTC (après corrections).

---

## Écosystème et partenariats (à initier)

- **Associations EM Corse.** Les contacter, proposer Tellux pour saisie/visualisation de leurs mesures. Demander retours test. Une lettre de soutien = atout majeur pour CTC. Livrables : email-type + formulaire retour test court.
- **Associations permaculture / gestion des sols.** Même logique, via le module Agronomie.
- **Pros du bâtiment.** Repoussé — mode Architecte pas assez mûr.
- **Ouverture à contribution d'études.** Formulaire de proposition d'études/corpus à intégrer, filtre de pertinence à l'intégration (par Claude/Soleil). À intégrer comme feature « soumettre une étude » dans le module hypothèses.

---

## Architecture des fichiers

```
Tellux/
├── tellux_v6_design.html          ← source de vérité du code (ne pas toucher hors session code)
├── CANDIDATURE_TELLUX_v7.docx     ← dossier candidature CTC
├── DIRECTION_ARTISTIQUE_v2.md     ← identité visuelle (gelée)
├── TELLUX_LOGO_V7.html            ← logo source de référence
├── TELLUX_BRIEFING.md             ← CE FICHIER (état du projet)
├── TELLUX_ROADMAP.md              ← feuille de route (voie A + voie B)
├── TELLUX_MONTEE_EN_GAMME.md      ← plan détaillé montée en gamme (6 axes)
├── TELLUX_STRUCTURE_JURIDIQUE.md  ← comparaison options juridiques (à compléter)
├── TELLUX_FINANCEMENT.md          ← tableau guichets subventions (à compléter)
├── favicons/                      ← tellux-v7.svg
├── DATA/                          ← données brutes (antennes, failles, radon, etc.)
└── _archives/                     ← anciens briefings et recoveries (trace historique)
```

---

## Planification

Voir `TELLUX_ROADMAP.md` pour la voie A (livraison immédiate), la voie B (montée en gamme), les chantiers structurels transverses, l'agenda court terme et les risques ouverts.
