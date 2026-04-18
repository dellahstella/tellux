# Rapport de session — Corpus patrimonial Tellux v1
**Date** : 18 avril 2026  
**Branche active** : `dev`  
**Repo** : https://github.com/dellahstella/tellux  
**Fichier principal modifié** : `index.html`

---

## Ce qui a été fait cette session

### Rapports intégrés
| Rapport | Région | SITES[] ajoutés | CHURCHES[] ajoutés | PR |
|---|---|---|---|---|
| R7 (correction) | Ferroviaire — recatégorisation | 0 (recatégorisation) | 0 | #36 (merged) |
| R8 | Golfe de Sagone (Sevi·Sorru·Cinarca·Cargèse) | 10 | 1 (×2) | #36 (merged) |
| R9 | Prunelli·Taravo·Coscione | 8 | 4 (×2) | #37 (open) |
| R10 | Ajaccio·Golfe·Sanguinaires | 22 | 4 (×2) | inclus dans #37 |

### Corrections appliquées
- **R7 ferroviaire** : `Viaduc sur le Vecchio (Pont Eiffel)` + `Tunnel de Vizzavona`  
  `'Patrimoine & Ressources'` / `#78350f` → `'Site remarquable'` / `#5c7a3a` (couche lSit2)
- **buildPontLayer()** : opacité 0.4 appliquée aux sites dont le nom contient `'disparu'`  
  (Pont de Zippitoli, emporté par Ciaran le 03/11/2023)

### État des layers à la clôture
| Layer | Catégorie SITES[] | Couleur | Nb entrées (approx) |
|---|---|---|---|
| lSit | Mégalithique, Remarquable, Église romane, etc. | #854d0e / #8b5cf6 | ~90 |
| lSit2 | Site remarquable, Hydraulique | #5c7a3a / #1a4b8c | ~35 |
| lTour | Tour génoise | #c8a035 | 28+ |
| lTherm | Thermalisme | #0ea5e9 | 5 |
| lIndu | Patrimoine & Ressources | #78350f | ~8 |
| lCast | Château médiéval | #92400e | ~10 |
| lPont | Pont génois | #475569 | ~15 |

---

## État du repo à la fin de session

### Branche dev
```
098e63e  feat: corpus Ajaccio·Golfe·Sanguinaires (R10) — clôture corpus v1
4f75d4b  feat: corpus Prunelli–Taravo–Coscione (R9) + opacité pont détruit
8a5f5df  feat: corpus Golfe de Sagone (R8) + correction ferroviaire R7
```

### PR ouverte
- **[#37](https://github.com/dellahstella/tellux/pull/37)** : `dev → main`  
  Titre : `feat: corpus Prunelli–Taravo–Coscione (R9) + opacité pont détruit`  
  Contient en réalité : R9 + R10 (les deux commits sont sur dev)  
  **Action requise : merger cette PR pour mettre en prod**

### Fichiers non committés (untracked, pas dans le repo)
Ces fichiers sont présents localement mais n'ont jamais été committés :
```
CANDIDATURE_TELLUX_v8.1.docx
TELLUX_ACTIONS_POST_RECHERCHE.md
TELLUX_CANDIDATURE_DELTA.md
TELLUX_CORPUS_SCIENTIFIQUE_v7.md
TELLUX_DOSSIER_AGRO_BIO.md
TELLUX_FIN_SESSION_OPUS_14AVR.md
TELLUX_HYPOTHESES_UPDATE.md
TELLUX_KIT_ENVOI_EM.md
TELLUX_SESSION_2026-04-14.md
patches_17avril/
```
→ Ne pas les committer sans instructions explicites.

---

## Mode d'intégration des PRs — procédure vérification + mise en prod

### Flux normal (pas de conflit)

```
feat/xxx → dev  →  (review)  →  main
```

1. **Merger la PR ouverte #37** sur GitHub (bouton "Merge pull request")  
   - Choisir **"Create a merge commit"** (NON squash, NON rebase — consigne du projet)
   - Le titre de la PR peut être mis à jour pour refléter R9+R10 avant de merger

2. **Vérifier en prod** : ouvrir l'URL de déploiement (GitHub Pages ou hébergement CTC)  
   - Activer tous les layers dans l'interface → vérifier couverture Corse complète  
   - Console navigateur → zéro erreur JS

### En cas de problème après merge

#### Symptôme : erreur JS console après déploiement
```bash
# Identifier le commit fautif
git log --oneline main

# Revenir au commit précédent sur main (option sûre : nouveau commit de revert)
git revert HEAD --no-edit
git push origin main
```

#### Symptôme : données SITES[] incorrectes (doublon, coordonnées erronées)
```bash
# Grep pour trouver l'entrée
grep "NomDuSite" index.html

# Corriger directement dans index.html
# Committer avec message fix: correction GPS/doublon [NomSite]
# Ouvrir nouvelle PR feat/fix → dev → main
```

#### Symptôme : conflit dev → main
```bash
git checkout main
git pull origin main
git checkout dev
git merge main
# Résoudre conflits (garder dev comme superset — cf. commit f1d652c)
git add index.html
git commit -m "merge: resolve conflicts dev → main (keep dev superset)"
git push origin dev
# Puis merger la PR normalement
```

#### Symptôme : layer manquant ou vide à l'affichage
Vérifier dans `buildSiteMarkers()` la ligne d'exclusion (l.~4379) :
```javascript
if(t==='Thermalisme'||t==='Tour génoise'||t==='Patrimoine & Ressources'||
   t==='Château médiéval'||t==='Pont génois')return;
```
Si une nouvelle catégorie a été ajoutée sans layer dédié → elle passe dans lSit par défaut.  
Si elle doit avoir son propre layer → créer `buildXxxLayer()` sur le modèle de `buildTourLayer()`.

---

## Structure clé de index.html (repères pour une future session)

| Élément | Ligne approx | Description |
|---|---|---|
| `let SITES=[` | ~3537 | Début array des sites patrimoniaux |
| `// ── Rapport 8` | ~3792 | Début bloc R8 |
| `// ── Rapport 9` | ~3812 | Début bloc R9 |
| `// ── Rapport 10` | ~3833 | Début bloc R10 (final) |
| `]` fermeture SITES | ~3867 | Fin array SITES |
| `CHURCHES=[` | ~3870 | Début array des églises (inline fallback) |
| `]` fermeture CHURCHES | ~4390 | Fin array CHURCHES |
| `const _CHURCHES_EXTRA=[` | ~4400 | Entrées extra (survivent au remplacement Supabase) |
| `]` fermeture _CHURCHES_EXTRA | ~4432 | Fin _CHURCHES_EXTRA |
| `function buildSiteMarkers()` | ~4435 | Construit lSit + lSit2 depuis SITES[] |
| `function buildTourLayer()` | ~4496 | Construit lTour |
| `function buildPontLayer()` | ~4558 | Construit lPont (avec opacité 0.4 si 'disparu') |

### Grep utiles pour audit rapide
```bash
grep -c "Rapport [0-9]" index.html          # Compter lignes balisées par rapport
grep "Rapport 10" index.html | wc -l         # Entrées R10 spécifiquement
grep "'Tour génoise'" index.html | wc -l     # Nb tours génoises
grep "calcHuman\|calcHeritagePiezo" index.html  # Fonctions EM — ne pas modifier
```

---

## Points d'attention pour la prochaine session

1. **PR #37 à merger** avant tout nouveau travail sur main
2. **GPS non vérifiés** dans plusieurs entrées R9/R10 marquées `GPS approx` — à auditer terrain
3. **Sites sans GPS** listés dans R10 (prompt) : à intégrer lors d'une campagne terrain  
   (Église Saint-Érasme, Saint-Roch, Couvent Saint-François Ajaccio, villa romaine Agosta, etc.)
4. **SITES_REFERENCE.json** : source de vérité hébergée — si ce fichier existe et est à jour,  
   `loadSitesReference()` le charge et remplace SITES[]. Vérifier cohérence si modifié côté serveur.
5. **_CHURCHES_EXTRA[]** : entrées locales qui survivent au remplacement de CHURCHES[] par Supabase.  
   Chaque ajout CHURCHES doit être dupliqué dans _CHURCHES_EXTRA pour garantir la persistance offline.
