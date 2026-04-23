# Piliers A/B et recommandations Cowork patrimoine — synthèse d'enquête

**Date :** 23 avril 2026  
**Auteur :** Claude Code (enquête read-only)  
**Destinataire :** session Cowork suivante  
**Branche :** `docs/enquete-piliers-ab` — PR en attente, pas de merge sans validation Soleil

---

## 1. Définitions

### Pilier A — Hypothèses scientifiques

**Définition :** corpus de 14 fiches S1–S14, formulées de manière falsifiable, ancrées dans la littérature peer-reviewed (DOI requis), avec protocole identifiable. Destinées aux candidatures CTC / FEDER / ANR / Horizon Europe, à la lettre physicien, et à la section landing.

**Critères d'appartenance (≥ 4/5 requis) :**
- C1 — formulation précise et testable (prédiction falsifiable)
- C2 — variables physiques mesurables (unité, gamme, source identifiée)
- C3 — protocole identifiable (plan d'expérience réaliste)
- C4 — ancrage peer-reviewed (2–4 références avec DOI)
- C5 — pertinence Corse et/ou multi-échelle

**Fichier source :** `_corpus/HYPOTHESES_SCIENTIFIQUES.md` (v1, 14 fiches S1–S14, statut livré)  
**Référence méthode :** `docs/notes-tri/TRANSITION_CORPUS_H1_H88_VERS_2_PILIERS_v1.md` §2.1 (privé, gitignored)

---

### Pilier B — Hypothèses patrimoine gamifiées

**Définition :** corpus de 20 fiches P1–P20, formulées de manière interrogative et intrigante pour un public non-scientifique, ancrées dans le patrimoine corse réel (site, texte, toponyme, pratique documentée), compatibles avec la rigueur Tellux. Destinées à `patrimoine.html` et aux contenus éditoriaux.

**Critères d'appartenance (3/3 requis) :**
- B1 — intrigante pour non-scientifique (déclenche envie d'explorer)
- B2 — ancrée dans le patrimoine corse réel
- B3 — compatible avec rigueur Tellux (formulation interrogative, pas de surinterprétation)

**Garde-fous absolus (G1–G3) :**
- G1 — pas de formulations prohibées (« deux réalités », « ne s'additionnent pas », « naturel = bénin »)
- G2 — pas de surinterprétation temporelle (non rétro-projection de connaissance moderne aux Anciens)
- G3 — pas de sources non peer-reviewed (Emoto, Schauberger, Orch-OR, ADN 12 brins, Tesla mythifié, Hancock, ley lines énergétiques)

**Fichier source :** `_corpus/HYPOTHESES_PATRIMOINE_GAMIFIEES.md` (v1, 20 fiches P1–P20, statut livré)  
**Référence méthode :** `docs/notes-tri/TRANSITION_CORPUS_H1_H88_VERS_2_PILIERS_v1.md` §2.2–§2.3 (privé, gitignored)

---

## 2. Hypothèses par pilier — correspondances H historiques

### Hypothèses en double usage A+B (concernées par les recos ci-dessous)

| H historique | Pilier A (S) | Pilier B (P) | Note |
|---|---|---|---|
| H1 | S11 | P12 | Granit vs calcaire / Continuité cultuelle romane |
| H18 | S12 | P13 | Églises romanes × antennes (disclaimer) / Antennes suivent crêtes chapelles |
| H21 | S1 | P1 | Coïncidence anomalies × sites anciens / Pourquoi ces endroits précis |

### Hypothèses Pilier A uniquement (concernées par les recos)

| H historique | Fiche S | Intitulé condensé |
|---|---|---|
| H2 | S3 | Courants telluriques DC/sub-1 Hz failles × eau |
| H39 | S2 | Susceptibilité locale amplifie naturel ≥ 2 km HTA |

**Source :** `docs/notes-tri/TRANSITION_CORPUS_H1_H88_VERS_2_PILIERS_v1.md` §3 (privé, gitignored)

---

## 3. Recommandations Cowork à appliquer dans `patrimoine.html`

**Origine commune :** `docs/notes-tri/RELECTURE_H1_H88_POST_BIOTSAVART_v1.md` — Cowork Opus 4.7 — 2026-04-21  
**Contexte :** relecture des hypothèses post-migration Biot-Savart v2 (11 735 segments HTA réels). Les 5 recos ci-dessous corrigent des ambiguïtés introduites par le fait que le composite GELE-001 intègre désormais la composante ELF 50 Hz anthropique.

---

### Reco 1 — Reformulation H21 [P1, urgent]

**Origine :** RELECTURE §2 R1 + §5  
**Priorité :** P1 urgent — hypothèse pédagogiquement visible dans la candidature CTC

**Énoncé actuel (`patrimoine.html` ligne 679) :**
```
title : 'Les anomalies géomagnétiques coïncident-elles avec les sites anciens ?'
desc  : 'Zones hot coïncident avec sites anciens ?'
```

**Problème identifié :** après v2, les « anomalies » et « zones hot » modélisées incluent le champ ELF 50 Hz anthropique issu de 11 735 segments HTA réels. Une coïncidence site ancien × anomalie forte peut refléter uniquement la présence d'une ligne HTA moderne (ex. Palaggiu : ratio v2/v1 = 71×). L'anachronisme est frontal.

**Reformulation proposée (extrait littéral RELECTURE §5) :**
> « Les zones d'anomalie géomagnétique naturelle (IGRF + EMAG2 + susceptibilité locale, hors composante ELF 50 Hz anthropique) coïncident-elles avec les sites anciens plus que le hasard ? »

**Application dans `patrimoine.html` :** remplacer le champ `desc` de H21. Le champ `title` peut être conservé ou adapté selon arbitrage Cowork.

---

### Reco 2 — Reformulation H39 [P2]

**Origine :** RELECTURE §2 R5 + §5  
**Priorité :** P2 — impose un protocole de contrôle spatial

**Énoncé actuel (`patrimoine.html` ligne 682) :**
```
title : 'La susceptibilité magnétique du sol amplifie-t-elle certaines zones ?'
desc  : 'La susceptibilité magnétique locale modifie-t-elle le niveau géomagnétique modélisé ?'
```

**Problème identifié :** la susceptibilité amplifie désormais aussi la composante ELF anthropique, produisant des zones « chaudes » qui ne reflètent pas un effet intrinsèque du sol. Un test de contrôle à ≥ 2 km de toute HTA est nécessaire.

**Reformulation proposée (extrait littéral RELECTURE §5) :**
> « La susceptibilité magnétique locale amplifie-t-elle le champ géomagnétique naturel, mesurée sur échantillons à ≥ 2 km de toute ligne HTA pour isoler l'effet anthropique ? »

**Application dans `patrimoine.html` :** remplacer le champ `desc` de H39.

---

### Reco 3 — Reformulation H2 [P2]

**Origine :** RELECTURE §2 R6 + §5  
**Priorité :** P2

**Énoncé actuel (`patrimoine.html` ligne 671) :**
```
title : 'Les failles terrestres créent-elles des courants invisibles ?'
desc  : 'Sites à convergence failles+eau → Δ plus élevé ? Croisement BRGM × sites.'
```

**Problème identifié :** le « Δ » désignait la différence entre niveau mesuré et niveau IGRF de fond. Après v2, certaines zones de convergence failles+eau coïncident avec des lignes HTA qui suivent les fonds de vallée (topographie commune, ex. vallées Fium'Orbu, Taravo, Golo). Le Δ peut monter par artefact anthropique et non par remontée tellurique.

**Reformulation proposée (extrait littéral RELECTURE §5) :**
> « Les zones de convergence failles + hydrographie présentent-elles un Δ statique (DC, < 1 Hz) supérieur, après soustraction de la contribution ELF 50 Hz modélisée par Biot-Savart v2 ? »

**Application dans `patrimoine.html` :** remplacer le champ `desc` de H2. Le titre interrogatif peut être conservé.

---

### Reco 4 — Clarification H18 [P1 pour titre/desc, P2 pour dimension ELF]

**Origine :** RELECTURE §2 R2 + §3.2  
**Priorité :** P1 pour résoudre l'incohérence titre/desc interne

**Énoncé actuel (`patrimoine.html` ligne 677) :**
```
title : 'Les mégalithes évitent-ils les antennes modernes ?'
desc  : 'Églises sur substrat piézo montrent-elles un score géo supérieur au voisinage ?'
```

**Problème identifié :** le `title` parle des antennes (RF), la `desc` parle du score géo des églises sur substrat piézo. Ces deux questions sont distinctes. L'incohérence titre/desc est à résoudre avant toute reformulation ELF.

**Reformulation proposée si la `desc` prévaut (extrait littéral RELECTURE §3.2) :**
> « Les églises romanes sur substrat à susceptibilité magnétique élevée présentent-elles un score géomagnétique naturel (hors ELF anthropique) supérieur à celui de leur voisinage immédiat ? »

**Note ELF transversale à ajouter :** H18, comme H21, corrèle un site antérieur au XXᵉ siècle avec une infrastructure moderne (antennes). Inclure dans la note méthodologique commune H18/H21 (voir Reco 5).

**Arbitrage Cowork requis :** trancher entre le `title` (mégalithes/antennes = question sociologique RF) et la `desc` (églises/score géo = question géophysique). Ce sont deux hypothèses différentes. Recommandation : soit scinder en H18a/H18b, soit choisir la formulation la plus alignée avec les données disponibles.

---

### Reco 5 — Note méthodologique transversale [P1]

**Origine :** RELECTURE §5  
**Priorité :** P1 — à ajouter en en-tête du corpus H1–H88 dans `patrimoine.html`

**Texte intégral (extrait littéral RELECTURE §5) :**
> « Depuis la migration ELF v2 (2026-04-21), la composante 50 Hz anthropique est modélisée sur le réseau HTA réel (11 735 segments EDF SEI). Toute hypothèse qui corrèle un site patrimonial (antérieur au XXᵉ siècle) avec une anomalie du composite GELE-001 doit préciser si elle vise la composante naturelle (géologie, IGRF, EMAG2) ou le champ total contemporain incluant ELF anthropique. Une coïncidence site ancien × composite fort n'implique pas un lien causal historique : elle peut refléter la superposition fortuite d'une ligne HTA moderne et d'un site préexistant. »

**Application dans `patrimoine.html` :** ajouter dans l'interface Hypothèses (section dormante ou en-tête du panel H1–H88), sous forme de bandeau ou de note préliminaire avant le listing des hypothèses.

---

## 4. Zones d'incertitude

1. **H18 titre/desc incohérents** : le `title` (mégalithes évitent antennes RF) et la `desc` (score géo églises) décrivent deux hypothèses différentes. L'arbitrage Cowork est requis avant reformulation (§3 Reco 4).

2. **Hypothèses non documentées H11–H83** : ~70 identifiants cités dans des textes agrégés sans formulation structurée retrouvée. Statut « non documentée » — ne pas classer sans source.

3. **H85–H87 : ambiguïté d'identifiant** : deux usages différents retrouvés dans les sources (mines BRGM EM vs faune ovins/balbuzard LPO). Trancher en session dédiée.

4. **`_corpus/HYPOTHESES_PATRIMOINE_GAMIFIEES.md`** : fichier livré v1 (Pilier B) non relu dans cette enquête (gitignored, accès Cowork requis). Les fiches P1, P12, P13 (doubles A+B) peuvent nécessiter une mise à jour parallèle aux reformulations de `patrimoine.html`.

5. **Application concrète dans `patrimoine.html`** : les 4 hypothèses ciblées sont dans l'array `HYPOTHESES` (lignes 669–683), actuellement **dormantes** (guard `showDormantMsg()` ligne 688). Les reformulations peuvent être intégrées maintenant (elles ne débloquent pas les hypothèses, qui restent dormantes jusqu'à validation GELE-001) ou différées à la réactivation Phase 2.

---

## 5. Recommandations pour la session Cowork suivante

La session Cowork peut appliquer les Recos 1–3 et 5 directement dans `patrimoine.html` (substitution de champs `desc` dans l'array `HYPOTHESES`, ajout note en-tête). La Reco 4 (H18) nécessite d'abord une décision de Soleil sur le conflit titre/desc avant rédaction.

Avant toute modification de `patrimoine.html` :
1. **Confirmer avec Soleil** le choix pour H18 : question RF (antennes) ou question géophysique (score géo églises) ?
2. **Vérifier la cohérence** des reformulations avec les fiches Pilier B correspondantes (P1 pour H21, P13 pour H18) dans `_corpus/HYPOTHESES_PATRIMOINE_GAMIFIEES.md`.
3. **Respecter les garde-fous G1–G3** : aucune des reformulations proposées ne doit glisser vers les formulations prohibées.
4. Les hypothèses restent **dormantes** après reformulation : ne pas modifier le flag `showDormantMsg()`.
5. Le fichier source de référence pour les reformulations est `docs/notes-tri/RELECTURE_H1_H88_POST_BIOTSAVART_v1.md` §5 (Cowork Opus 4.7, 2026-04-21).

---

*Enquête produite par Claude Code le 2026-04-23 — read-only sur tous les fichiers existants sauf ce document.*  
*Sources principales : `docs/notes-tri/TRANSITION_CORPUS_H1_H88_VERS_2_PILIERS_v1.md` + `docs/notes-tri/RELECTURE_H1_H88_POST_BIOTSAVART_v1.md` + `patrimoine.html` lignes 669–683.*
