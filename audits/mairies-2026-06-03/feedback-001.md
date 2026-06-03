# FEEDBACK-001 — Audit `mairies.html` (itération 1)

> Session ÉVALUATEUR (séparée du générateur, §2 du protocole).
> Date : 2026-06-03.
> Cible : `http://localhost:3000/mairies.html` (commit `7951692` sur `fix/audit-mairies-2026-06-03`, base canonique `mairies.html` à la racine).
> Outil d'éval : `mcp__Claude_Preview__preview_*` (Chromium piloté via MCP, équivalent fonctionnel des sondes Playwright décrites au contrat §8 — voir note méthodo en fin de document).

---

## 0. Verdict

```
SCORE PONDÉRÉ   : 7.40 / 10
SEUIL           : 7.00
STATUT          : SUCCÈS (marge modeste de 0.40 — itérable)
RECOMMANDATION  : à arbitrer par Soleil — soit clôturer en l'état (le contrat est rempli),
                  soit lancer itération 2 sur les 4 points Craft listés en §3.
```

L'évaluateur **ne propose pas de correctif** (§2). Si Soleil arbitre « itérer », les défauts listés ici sont la matière du générateur.

---

## 1. Notation par critère

> Rubrique §5.1 du protocole, complétée par les spécificités falsifiables du contrat. Note : §5.1 est calibrée pour `app.html` (Indice Tellux dual, 9 couches géologiques) — les critères « 9 couches » et « Indice dual » ne s'appliquent pas littéralement à `mairies.html` ; ils sont remplacés par les spécificités Fonctionnalité et Non-régression du contrat.

| Critère | Poids | Note | Pondéré |
|---|---:|---:|---:|
| Fonctionnalité | 0.35 | **7** | 2.45 |
| Non-régression données | 0.30 | **8** | 2.40 |
| Craft / UX | 0.20 | **6** | 1.20 |
| Robustesse | 0.15 | **9** | 1.35 |
| **TOTAL** | | | **7.40** |

---

## 2. Observations qui ne pénalisent pas (à valider explicitement)

Ces points sont **conformes ou neutres** mais méritent une trace écrite pour traçabilité.

### 2.1 — DOM réel : 3 onglets, conformes au re-cadrage 2026-06-03
- `data-tab="fiche" | "courrier" | "legal"` aux lignes 461–463.
- Panel `fiche` actif au boot, autres `display:none`.
- Aucun onglet « Checklist » séparé (le contrat l'exclut explicitement, conforme).
- « Checklist déploiement antenne » présente en `<h3 class="mr-legal-title">` ligne 574, à l'intérieur du panneau `legal` — position 4 sur 5 sections H3.

### 2.2 — Boot propre, 0 erreur console
- Lecture `preview_console_logs` après boot complet : `No console logs.`
- Aucune erreur, aucun warning à toute étape de la session (boot, switch onglets, ouverture des 8 modaux, download PDF, navigation cross-commune, resize mobile).

### 2.3 — Lazy-load pdfmake confirmé (critère contrat passé)
- Au boot, **aucun fetch** sur `cdnjs.cloudflare.com/ajax/libs/pdfmake/*` (vérifié via `preview_network` filter `all`).
- Après clic sur `#mr-btn-download` du premier modèle Mairie :
  - `GET cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.12/pdfmake.min.js → 200`
  - `GET cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.12/vfs_fonts.js → 200`
- Le critère « Lazy-load de pdfmake (~600 ko) + vfs_fonts (~200 ko) se déclenche uniquement au premier clic » du contrat est **vérifié**.

### 2.4 — PDF Mairie #0 généré et téléchargé avec données commune injectées
- Hook installé sur `window.pdfMake` avant clic (proxy autour de `createPdf`).
- `createPdfCalled: true`, `downloadCalled: true`.
- Nom du fichier : `MAIRIE_01_mesure_exposition.pdf` (extension `.pdf` correcte, naming cohérent).
- Document définition : 14 419 caractères de JSON, 92 nodes texte, 3 019 caractères de texte réel.
- **Occurrences « Ajaccio » dans le PDF : 5** (commune sélectionnée bien propagée).
- **Date `3 juin 2026` (date du jour) dans le PDF : 1** (autofill date OK).
- Aucun token non résolu `{{XXX}}` ou `<<XXX>>` détecté dans les nodes texte du PDF.

### 2.5 — Données par commune chargent correctement (non-régression Fiche)
- Datalist `#communes-corse` : **360 options** au boot (couverture totale Corse, conforme au contrat).
- Communes testées :
  - **Ajaccio (INSEE 2A004)** : 98 supports / 327 antennes / 4 opérateurs (Bouygues, Free, Orange, SFR) / 4 technologies (2G/3G/4G/5G).
  - **Bastia (INSEE 2B033)** : 32 supports / 107 antennes / 3 opérateurs (Free, Orange, SFR — Bouygues absent, à fact-checker éventuellement contre cartoradio.fr).
  - **Calvi (INSEE 2B050)** : section antennes rendue (`offsetHeight: 1726`).
- URL params synchronisés (`?commune=2A004`, `?commune=2B033`, `?commune=2B050`).
- Section géophysique : « Classement radon ASNR Catégorie 3 » + « Failles tectoniques principales » s'affichent (dataset radon ASNR + Supabase `failles_corse` OK).
- Sections « Établissements sensibles » et « Points atypiques ANFR » déployées (`offsetHeight` > 0).
- Aller-retour Fiche → Courrier → Legal → Fiche : `inputVal`, `selectedTxt`, `urlParams`, `offsetHeight` des sections antennes/établissements tous préservés.

### 2.6 — Cadre légal et Checklist intégrée (critère contrat passé)
- Panel `legal` `offsetHeight: 2868` (rendu complet).
- 5 sections H3 visibles, toutes `offsetHeight > 0` :
  1. Ce que dit la Loi Abeille
  2. Ce que votre commune peut faire
  3. Ce que votre commune ne peut pas faire
  4. **Checklist déploiement antenne** (ligne 574, position 4)
  5. Pour aller plus loin
- Checklist : 5 `.mr-step-desc` (étapes de calendrier détaillées : Phase de recherche, Réception du DIM (J0), …).
- Liens externes opérationnels (échantillon vérifié) : `cartoradio.fr`, `mesures.anfr.fr`, `anfr.fr/maitriser/information-du-public/role-des-maires`, `legifrance.gouv.fr`.

### 2.7 — Responsive mobile (375×812)
- `tabsBar.flexWrap: wrap` (les 3 onglets s'enroulent proprement sur mobile).
- `bodyOverflowX: false`, `docOverflowX: 0` (aucun débordement horizontal).
- Mobile menu `#lp-mobile-menu` correctement caché au boot (`visibility:hidden, opacity:0` — l'`offsetHeight: 812` est un faux positif anodin).

---

## 3. Défauts identifiés (matière du générateur si itération 2)

### 3.1 — Autofill commune absent dans les courriers Citoyen (Craft, **modéré**)
- Les 6 cards Mairie pré-remplissent `NOM_DE_LA_COMMUNE`, `COMMUNE`, `DATE` à l'ouverture du modal avec la commune sélectionnée (Ajaccio sur ce test). Vérifié sur les 6.
- Les 2 cards Citoyen (`#mr-citoyens-list`) ouvrent leur modal avec **`firstFieldVal: ""`** — autofill absent.
- Possible justification UX : un·e citoyen·ne peut habiter une autre commune que celle sélectionnée pour consulter la fiche. Mais alors le contrat de l'autofill devrait être explicite (au minimum un placeholder « Votre commune » plus parlant que le champ vide).
- À arbitrer : est-ce intentionnel ou un oubli ?

### 3.2 — Placeholders `[X]` dans le PDF pour champs vides (Craft, **mineur**)
- Le PDF rendu pour Mairie #0 sans remplir les champs optionnels affiche littéralement :
  - `[ADRESSE MAIRIE]`, `[CODE POSTAL]`, `[TÉLÉPHONE]`, `[EMAIL MAIRIE]`, `[LIEU SENSIBLE]`, `[ADRESSE DU LIEU SENSIBLE]`, `[RÉFÉRENCE PORTAIL]`, …
- Lecture possible 1 : choix UX explicite (« remplir à la main avant impression »).
- Lecture possible 2 : artefact de rendu (devrait être remplacé par un blanc visuel `__________` ou un texte d'incitation).
- À arbitrer : intentionnel → mentionner dans une notice sous le bouton ; sinon → soft handle des champs vides.

### 3.3 — Aucune ancre interne dans le panneau légal (Craft, **mineur**)
- Les 5 `<h3 class="mr-legal-title">` n'ont **pas d'`id`** (`id: ""` pour les 5).
- Le panneau légal mesure 2 868 px de hauteur — pas de table des matières interne, pas de scroll-to-section, pas de partage de lien `#checklist`.
- Le contrat n'exige pas formellement les ancres (« ancres internes si présentes »), donc absence ≠ défaut bloquant — mais Craft réduit à 6/10 à cause de la conjonction de ce point + 3.1 + 3.2.

### 3.4 — `preview_click` MCP bloqué sur les tabs (Craft, **mineur** — observation outil)
- `preview_click` sur `.mr-tab[data-tab="courrier"]` ne switche pas l'onglet (`activeTab` reste `fiche`).
- Workaround `document.querySelector('.mr-tab[data-tab="courrier"]').click()` via `preview_eval` fonctionne.
- Hypothèse : un overlay invisible (sticky nav, mobile menu hidden mais présent dans le flux, etc.) intercepte les coordonnées de clic du driver MCP.
- Pas un bug app au sens UX humain — un humain qui clique avec sa souris a accès au tab. Mais c'est un signal : un script Playwright vanilla pourrait avoir le même comportement et nécessiter `.click({force:true})` ou un `dispatch` manuel.
- À investiguer en itération 2 si l'objectif inclut une automatisation Playwright robuste.

### 3.5 — Incohérence contrat / DOM : « 6 modèles » → réalité 8 (Fonctionnalité, **structurel**)
- Le contrat §35 « Générer un courrier (PDF) » dit : *« Les **6 modèles** de courriers (Mairie + Citoyen) se rendent tous correctement en preview HTML. »*
- Réalité DOM (`#mr-courriers-list` + `#mr-citoyens-list`) : **8 cards au total** = 6 Mairie + 2 Citoyen.
- Liste des 8 vérifiés en ouverture de modal :
  - Mairie · 01 « Faire mesurer l'exposition près d'un lieu sensible » (13 inputs, autofill OK, PDF download testé OK)
  - Mairie · 02 « Demander à l'opérateur une simulation d'exposition » (13 inputs, autofill OK)
  - Mairie · 03 « Saisir le préfet d'une instance de concertation départementale » (14 inputs, autofill OK)
  - Mairie · 04 « Publier l'avis de mise à disposition d'un dossier d'antenne » (21 inputs, autofill OK)
  - Mairie · 05 « Demander à l'ANFR le registre officiel des installations de la commune » (8 inputs, autofill OK)
  - Mairie · 06 « Répondre à un·e habitant·e qui s'inquiète d'une antenne » (14 inputs, autofill OK)
  - Citoyen · 1 « Obtenir les dossiers d'antennes détenus par ma mairie » (13 inputs, autofill **vide**)
  - Citoyen · 2 « Demander à ma mairie de faire mesurer les ondes » (12 inputs, autofill **vide**)
- Diagnostic : le contrat sous-compte de 2. À arbitrer côté contrat (corriger « 6 » en « 6 Mairie + 2 Citoyen = 8 » dans `contrat.md`) — **pas du code**.

### 3.6 — Couverture PDF partielle : 1 PDF généré sur 8 (Fonctionnalité, **méthodologique**)
- Le contrat exige : *« Cliquer sur `#mr-btn-download` (…) déclenche un téléchargement réel »*, *« Le PDF reçu est valide (header `%PDF-`…) »*, *« Le PDF contient les bonnes données de la commune sélectionnée »*.
- L'évaluateur a généré 1 PDF (Mairie #0) avec hook de capture sur `pdfMake.createPdf` → docDef inspecté en détail (commune Ajaccio × 5, date × 1, 0 token non résolu).
- Les 7 autres modèles ont été vérifiés en preview HTML uniquement (ouverture modal, comptage inputs, présence du bouton download, autofill commune). Aucune n'a généré ni téléchargé de PDF.
- Cela suffit pour un test fumée mais pas pour une certification « le PDF de chacun des 8 modèles est valide ». L'évaluateur pénalise Fonctionnalité de 8 → 7 pour acter cette couverture partielle.
- Note : le header `%PDF-` n'a pas pu être vérifié directement via MCP (`preview_*` ne capture pas les downloads — la validation a porté sur le `docDef` JSON et le succès du hook `download()`, pas sur les octets du fichier).

### 3.7 — Sémantique « ANFR live » du contrat vs snapshot statique (Non-régression, **clarification**)
- Le contrat §53 dit : *« Sélection d'une commune affiche les données ANFR live correspondantes »*.
- Réalité observée : `GET /public/data/antennes_par_commune_corse.json → 200` — snapshot statique distribué avec l'app, pas un appel direct à l'API ANFR / CartoRadio.
- Ce n'est **pas un bug de l'app** (le snapshot fonctionne, les chiffres sont vraisemblables, 360 communes couvertes). C'est une imprécision dans le contrat sur ce que « live » signifie ici.
- À arbitrer côté contrat : reformuler en « données ANFR snapshot local » OU acter que « live » désigne la fraîcheur du snapshot, pas un appel temps réel.

---

## 4. Justification des notes

### Fonctionnalité — 7/10
> *« 7–8 : tout marche, erreurs gérées. »*

Happy path complet sur les 3 onglets et les 8 modèles. Mais couverture PDF partielle (1/8 généré, §3.6) et 2 cas limites non testés (champ obligatoire vide, network failure pendant gen). Évaluateur sévère ne lâche pas 8 sans test exhaustif des 8 PDFs ni des cas limites. **7/10**.

### Non-régression données — 8/10
> *« 7–8 : 9 couches OK, comptes justes »* (la barre §5.1 ne s'applique pas littéralement ; lecture adaptée : « toutes les couches de données promises chargent et comptes vraisemblables »).

Datalist 360 communes, données par commune cohérentes sur 3 tests (Ajaccio plus dense que Bastia, en cohérence d'échelle géographique), géophysique + atypiques + établissements + antennes tous OK, Supabase failles OK. Pas 9 car (a) `live` non vérifié comme vraiment live (§3.7), (b) données ANFR non cross-checkées contre source externe (cartoradio). **8/10**.

### Craft / UX — 6/10
> *« 4–6 : marche mais rugueux. »*

Desktop + mobile propres, modaux ouvrent/ferment, mais 4 rugosités identifiées : autofill Citoyen vide (§3.1), placeholders `[X]` dans PDF (§3.2), pas d'ancres internes Legal sur 2 868 px de scroll (§3.3), preview_click bloqué sur tabs (§3.4 — probablement un overlay invisible au-dessus). Sévérité maintenue à 6 — la conjonction de 4 points fait basculer Craft sous la barre des 7. **6/10**.

### Robustesse — 9/10
> *« 9–10 : + pas d'init redondant. »*

Zéro log console pendant toute la session (boot, 8 modaux, 1 PDF, navigation, resize). Lazy-load CDN propre. Aller-retour cross-commune et cross-onglet non-destructifs. Pas 10 car (a) pas de test réseau dégradé (bloquage CDN cdnjs durant `loadPdfMake`), (b) pas de test d'erreur sur champ obligatoire (les inputs sont tous `required: false`, donc pas de validation visible — choix UX). **9/10**.

---

## 5. Note méthodologique

### 5.1 — Outil utilisé : `preview_*` MCP au lieu de Playwright bare metal
- Le contrat §8 spécifie l'installation de `@playwright/test` + Chromium (~200 Mo).
- Pas de `package.json` dans le repo Tellux (HTML statique servi par `npx serve`), pas de Playwright pré-installé.
- L'évaluateur a utilisé `mcp__Claude_Preview__preview_*` (Chromium piloté via MCP — équivalent fonctionnel des sondes Playwright décrites). Les capacités utilisées : `preview_start`, `preview_eval`, `preview_click`, `preview_console_logs`, `preview_network`, `preview_resize`.
- **Limitation MCP** : pas de `page.waitForEvent('download')`. Contournement : hook `Object.defineProperty(window, 'pdfMake', ...)` qui proxie `createPdf().download()` pour capturer `docDef` + `downloadName` avant que le navigateur déclenche le download (qui en MCP ne sauve nulle part).
- **Conséquence** : le critère contrat « header `%PDF-` en début de fichier » n'a pas été vérifié au niveau des octets du fichier — la validation a porté sur le `docDef` JSON, le succès du `download()` call, et l'extension `.pdf` du `suggestedFilename`. C'est une vérification logique du chemin de génération, pas du fichier final.
- Recommandation pour l'itération 2 (si l'objectif inclut une certification stricte) : installer `@playwright/test` localement et utiliser `page.waitForEvent('download')` + `fs.readFileSync(download.path()).subarray(0,5).toString('ascii')` comme spécifié au contrat §8.

### 5.2 — Server : `npx serve -l 3000 .` au lieu de `python3 -m http.server 3000`
- `.claude/launch.json` était déjà configuré avec `npx serve` ; je l'ai réutilisé via `preview_start name="tellux"`.
- L'URL canonique est `http://localhost:3000/mairies` (sans `.html`, `npx serve` fait l'aliasing). Le contrat §8 mentionne `mairies.html` — les deux URL marchent.

### 5.3 — Limite assumée : couverture partielle des PDFs
- 1 PDF généré et inspecté en profondeur (Mairie #0) sur 8 modèles.
- Choix de l'évaluateur : un test profond + 7 tests fumée en preview HTML, plutôt que 8 tests superficiels.
- Compromis assumé : Fonctionnalité notée 7 plutôt que 8 (§3.6).

### 5.4 — Sévérité
- Le protocole §2 demande à l'évaluateur d'être sévère : *« si tu mets >7/10 dès l'itération 1, durcis la rubrique. »*
- Score 7.40 — au-dessus de 7 mais avec marge modeste. L'évaluateur a explicitement déclassé Fonctionnalité (8 → 7) et Craft (7 → 6) pour ne pas valider à la louche.
- Si Soleil considère que 7.40 est trop généreux pour une itération 1, durcir : Craft → 5 (les rugosités UX font 5 cumulés) donne 7.20 ; ou Non-régression → 7 (incertitude sur `live` + pas de cross-check externe) donne 7.10.

---

## 6. Synthèse pour le générateur (si itération 2 demandée)

Sans proposer de correctif (§2), voici la **matière** brute pour le générateur :

- **Point 3.1** (Autofill Citoyen) — choix produit à arbitrer puis appliquer.
- **Point 3.2** (Placeholders `[X]` PDF) — choix UX à arbitrer puis appliquer.
- **Point 3.3** (Ancres internes Legal) — ajout `id` sur les 5 `<h3>` + éventuelle TOC en haut du panneau.
- **Point 3.4** (preview_click overlay) — identifier l'élément qui intercepte les coordonnées de clic sur tabs.
- **Point 3.5** (incohérence contrat « 6 » vs DOM « 8 ») — **côté contrat**, pas code. Modifier `contrat.md` ligne 43.
- **Point 3.7** (sémantique « live ») — **côté contrat**, pas code. Reformuler `contrat.md` ligne 53.
- **Point 3.6** (couverture PDF 1/8) — **côté évaluateur**, pas code. Itération 2 devra tester les 7 autres PDFs.

---

*Fin du feedback-001. L'évaluateur ne propose pas de correctif. À arbitrer par Soleil.*
