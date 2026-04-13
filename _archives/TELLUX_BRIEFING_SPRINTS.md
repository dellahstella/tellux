# TELLUX — Briefing v7 (actualisé avril 2026)

**Cible financement :** CTC (Collectivité Territoriale de Corse)
**Porteur :** Soleil (solo)
**État du code :** v5.9 stabilisée, candidature v6 en cours de révision

> Ce document remplace `TELLUX_BRIEFING_SPRINTS.md`. Items déjà réalisés archivés en bas.

---

## 🎯 Sprint A — Candidature CTC v7 (prioritaire, Opus)

Retour de relecture Soleil sur v6 :

**A1. Section 1 — Résumé exécutif**
Tableau de hiérarchisation des sites pas à jour. Rééquilibrer : antennes ANFR + réseau électrique EDF SEI au même niveau que le patrimoine. Utiliser l'espace blanc disponible.

**A2. Section 2 — Périmètre technique**
- Corriger 80 → **88 hypothèses testables**. Mentionner que les ~33 auto-testables vont augmenter.
- Architecture : plus sur Netlify. Décrire l'archi actuelle (single-file HTML + Supabase PostGIS + fallback offline).
- Densifier.

**A3. Section 3 — Méthodologie**
- Supprimer anglicismes, relecture FR.
- Déplacer les "incertitudes documentées" vers feuille de route ou rubrique dédiée méthodo.
- Ajouter un encart **protocole de mesures en aveugle parallèle** (deux opérateurs indépendants, non communication pendant la mesure). Principe structurant à garder pour tout le projet.
- Densifier.

**A4. Section 4 — Hypothèses**
Texte trop brut. Soit développer l'intérêt scientifique (angle stimulant), soit ajouter 3-5 hypothèses supplémentaires en exemple.

**A5. Section 5 — Impact / Territoire**
Aérer, rendre plus vivant.

**A6. Section 6 — Budget**
- Solo, aucune embauche.
- Logement + temps de travail → permet d'arrêter le bâtiment.
- **Phase 1** (~6 mois consolidation) : Soleil apprend l'outil, commence mesures lui-même avec protocole en aveugle parallèle.
- **Phase 2** : tiers extérieurs (association CEM, labo) prennent le relais des mesures de validation pour crédibilité scientifique.
- Matériel : Trifield TF2 + éventuel capteur piézo.

**A7. Rédaction entreprise**
Mention de **Tellux** comme entité (SASU ou micro à arbitrer). Stella Canis Majoris en attente, ne pas miser dessus. Dépôt du nom à évaluer selon budget — noter en feuille de route long terme.

---

## 🎯 Sprint B — Identité visuelle (Opus/Sonnet, 1 session)

Voir `DIRECTION_ARTISTIQUE.md`. À faire **avant** la version finale du dossier pour cohérence captures + export PDF.

---

## 🎯 Sprint C — Corrections code prioritaires (Sonnet)

**C1. Carte infinie (wrap horizontal).** Leaflet se répète à l'infini, couches non mises à jour sur les copies. Solution : `worldCopyJump: false`, `maxBounds` sur Corse élargie `[[40.5, 7.5], [43.5, 10.5]]`, `maxBoundsViscosity: 1.0`.

**C2. Point violet saisie mesure.** Ajouter bouton "✕ Annuler" dans le popup + auto-dismiss après soumission réussie.

**C3. Unité anomalie Monticello.** Auditer `_unit` dans couche anomalies. Si unités mixtes : séparer en sous-couches distinctes OU normaliser dans unité pivot. Afficher unité explicite dans chaque popup.

**C4. Popup quadrillage anomalie — conflit clic.** Les carrés colorés capturent l'event avant le quadrillage. Vérifier ordre `addLayer`, `bringToBack()`, tester `interactive: false` sur couche inférieure.

---

## 🎯 Sprint D — Écosystème & partenariats (Opus, réflexion)

**D1. Associations EM Corse.** Les contacter, leur proposer Tellux pour saisie/visualisation de leurs mesures. Demander retours test. Une lettre de soutien = atout majeur pour CTC. Livrables : email-type + formulaire retour test court.

**D2. Associations permaculture / gestion des sols.** Même logique, module Agronomie.

**D3. Pros du bâtiment.** Repoussé — mode Architecte pas assez mûr.

**D4. Ouverture à contribution d'études.** Formulaire de proposition d'études/corpus à intégrer, filtre de pertinence au moment de l'intégration (par Claude/Soleil). À intégrer comme feature "soumettre une étude" dans le module hypothèses.

---

## 🎯 Sprint E — Validation scientifique (Sonnet, après CTC déposé)

- **E1.** Refactoring FAILLES_CORSE en segments LineString. Gain précision ±300 m.
- **E2.** Implémentation tests auto H55–H88.
- **E3.** Externalisation SITES[] dans `SITES_REFERENCE.json` hébergé (éviter régressions GPS).
- **E4.** Protocole calibration Trifield TF2 standardisé (mesures en aveugle parallèle).

---

## Items archivés (déjà réalisés)

Module agronomie résolu ; corpus nettoyé ; candidature v6 rédigée ; panel hypothèses H34–H88 ; gamification ; UI professionnalisée ; mobile responsive ; simulateur bâtiment ; module permaculture ; BT layer bbox filtering ; calcHuman Biot-Savart ; calcHeritagePiezo ; offshore antennas layer ; diagnostic antennes.

## À vérifier en début de session (peut-être déjà fait)

Migration WMS Géoplateforme ; sélecteur culture personnalisée ; template PDF propre exportPermaPDF ; lazy-loading couches lourdes.
