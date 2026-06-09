# RAPPORT FINAL — fix catégorisation offshore antennes ANFR

**Date** : 2026-06-09
**Branche** : `feat/fix-offshore-categorization`
**Statut** : ✅ Boucle clôt en 1 itération de génération. Score 7.80 → 8.50 (+0.70).

---

## 1. Verdict global

| iter | Score | filtre_cotier | ANFR_antennes | offshore | Verdict |
|---|---|---|---|---|---|
| 0 (baseline) | 7.80 / 10 | **False** | 3 000 | 0 | Défaut spécifique remonté |
| 1 (post-fix) | **8.50 / 10** | **True** | 2 986 | **14** | ✅ Seuil atteint, défaut résolu |

La sonde stricte (`probeIsLandFilter` état main pré-#825, `ok: onshore > 0 && offshore > 0`) a fait son travail : elle a flaggé un vrai défaut en iter 0 et confirmé sa résolution en iter 1.

---

## 2. Rayon de souffle — sites corrigés

Grep `f.commune` + logique onshore/offshore dans `app.html` → 4 sites dans `loadAnt()` (l.5104-5140), contained.

| Site | Avant | Après |
|---|---|---|
| **SELECT Supabase** (l.5104) | `select=lat,lon,generation,commune,operateur` | `select=lat,lon,generation,commune,code_insee_commune,operateur` |
| **Commentaire doc** (l.5114-5121) | « On utilise désormais le champ `commune` (L5131) : `!f.commune => offshore` » | « On utilise désormais le champ source-de-vérité `code_insee_commune` (ajouté 2026-04-24, ticket SUPABASE-COMMUNE-FIELD-001) : `!f.code_insee_commune => offshore`. Le champ legacy `commune` est gardé dans le SELECT uniquement pour le label affiché du tooltip. » |
| **Test offshore** (l.5131) | `if(!f.commune){nOffshore++;return;}` | `if(!f.code_insee_commune){nOffshore++;return;}` |
| **Log console** (l.5140) | `'offshore commune-null'` | `'offshore code_insee_commune-null'` |
| Tooltip d'antenne (l.5136) | **NON TOUCHÉ** — `f.commune||'Corse'` conservé comme label affiché legacy | identique |
| Bbox safeguard (l.5130) | **NON TOUCHÉ** | identique |

Autres mentions `commune` dans `app.html` (Radon, production électrique, markers patrimoine, reverse geocoding) — confirmées indépendantes de la catégorisation offshore antennes, non touchées.

---

## 3. Changement visible documenté

### Compteurs affichés

| Affichage | Avant | Après | Delta |
|---|---|---|---|
| Header `#hdr-status` | `3000 antennes` | `2986 antennes` | −14 |
| `#anfr-count` | `3000 antennes` | `2986 antennes` | −14 |
| `#leg-ant-count` | `3000` | `2986` | −14 |
| Couche Leaflet `lAnt` (markers) | inclut 14 markers offshore aberrants | n'inclut plus les 14 | −14 markers |

### Hook `window.__telluxLayers`

| Compteur | Avant | Après |
|---|---|---|
| `antennes_anfr` | 3 000 | **2 986** |
| `antennes_offshore` | 0 | **14** |
| `antennes_sea_filtered` | 0 | 0 |
| Total reconstitué | 3 000 ✓ | 3 000 ✓ |

### Cohérence avec source

- `docs/em-mairie/data-sources/antennes_corse_notes.md` §2 confirme : « `code_insee_commune NULL` | 14 (offshore) ».
- Les 14 NULL sont documentées « toutes des antennes offshore hors contours communaux IGN : 10 antennes à (41.856667, 9.403889) — îles Cerbicale ; 4 antennes à (42.679444, 9.301111) — môle nord Bastia ».
- « Ces valeurs NULL sont conformes et n'indiquent pas une régression. »

Le compteur landing public reste `3 000 antennes individuelles` (chiffre canonique inclus offshore) — il n'est pas affecté par cette modification de l'UI app.html (rendu carte uniquement). Cohérence préservée avec `cadre-scientifique.html` §9.2 « 2 986 antennes dans les contours communaux IGN + 14 offshore = 3 000 ».

---

## 4. Garde-fous

### Zones gelées intactes

```bash
$ git diff app.html | grep -E "EXPERT_WEIGHTS|EXPERT_BOUNDS|calcGammaAmbient|GELE-001|NCRP-001|terrestrial_nSv|cosmic_nSv|computeExpertComposite"
# (output vide — aucune mention dans le diff)
```

✅ `EXPERT_WEIGHTS_DEFAULT`, `EXPERT_BOUNDS_DEFAULT`, `calcGammaAmbient`, `GELE-001`, `NCRP-001` non touchés.

### Garde-fou calcul

Les compteurs `nOnshore` / `nOffshore` / `nSeaFiltered` ne sortent QUE vers :
- Le label affiché du header (`'X antennes'`)
- Le hook `window.__telluxLayers` (debug)
- Le log console

Ils ne sont jamais lus par `calcAll_v2`, `calcRF`, `computeExpertComposite` ou toute formule du moteur. **Aucune valeur calculée n'est déplacée.**

Vérification iter 1 :
- Sonde `indice_dual` → matched (popup avec Perturbation X/5 · Activité naturelle Y/5 affiché correctement)
- Note Non-régression données : 9/10 (inchangé entre iter 0 et iter 1)
- Note Fonctionnalité : 7 → 9 (gain attribuable au passage de `filtre_cotier` à True)

### Garde NULL=OFFSHORE

Les 14 antennes `code_insee_commune IS NULL` sont **réellement** offshore (Cerbicale + môle Bastia) selon la doc et la pipeline de point-in-polygon contre IGN AdminExpress documentée. Aucun trou de saisie onshore parmi les 14.

### Chemin veille Scholar

Non touché (vert depuis PR #819).

---

## 5. Preuve de clôture (anti-boucle infinie)

- iter 0 : score 7.80, défaut spécifique `filtre_cotier=False` flaggé.
- iter 1 : score 8.50, défaut résolu, threshold met. STOP.
- Pas de iter 2 (max=3, on n'y est pas allé).
- Δ score sur 1 itération = +0.70 (largement > 0.3 → pas de plateau).

---

## 6. Liste des fichiers touchés (PR)

| Fichier | Type | Lignes |
|---|---|---|
| `app.html` | fix bug (4 sites contained dans `loadAnt()`) | +7 / -5 |
| `tests/app-rubric-offshore-fix/contrat.md` | doc boucle | +84 |
| `tests/app-rubric-offshore-fix/feedback-000.md` | doc boucle | +31 |
| `tests/app-rubric-offshore-fix/feedback-000.json` | sortie eval | (généré) |
| `tests/app-rubric-offshore-fix/feedback-001.md` | doc boucle | +65 |
| `tests/app-rubric-offshore-fix/feedback-001.json` | sortie eval | (généré) |
| `tests/app-rubric-offshore-fix/RAPPORT_FINAL.md` | ce rapport | (présent) |

Aucune autre modification.

---

## 7. PR

Branche `feat/fix-offshore-categorization` → PR vers `dev`. **PAS d'auto-merge** — arbitrage Soleil.

PR #825 (le quieting de sonde de la sonde + workflow CI) reste OPEN sur `dev` au moment de la rédaction de ce rapport. La présente PR utilise la sonde stricte état main pré-#825, donc indépendante de #825.

---

*Fin du rapport.*
