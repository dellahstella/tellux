# Prompt Claude Code — Fix A (nav) + Fix B (retag Farinole)

**À copier-coller dans une session Claude Code locale sur le repo `tellux`.**
**Branche cible** : `fix/patrimoine-nav-corse-farinole-2026-05-17`
**Estimation** : ~30-45 min.
**Doctrine** : autonomie merge (cf. `CLAUDE.md` workflow Code autonome 2026-05-17).

---

## 1. OBJECTIF

Deux fixes mineurs sur `patrimoine.html` et `sites_patrimoine.json` détectés
en audit prod 2026-05-17 par Soleil + Cowork :

- **Fix A** : le bouton « ← Vue d'ensemble » (retour doyenné → vue Corse)
  existe en DOM mais est invisible parce qu'il est rendu en `position: static`
  au coin (0,0), masqué par l'en-tête « Tellux Patrimoine ». Le rendre
  visible avec un style cohérent avec le bouton sœur « ← Retour doyenné ».

- **Fix B** : 2 sites de la commune Farinole sont tagués `pieve_nebbiu`
  alors qu'ils tombent dans la zone Cap (`pieve_canari` pour
  `santa_maria_farinole`, et bord-frontière pour `tour_de_farinole`).
  Retag mécanique des deux vers `pieve_canari`.

## 2. CONTEXTE

État audit prod (tellux.pages.dev/patrimoine) :

**Fix A — bouton retour Corse** :
```
<button id="btn-retour-corse" type="button"
        aria-label="Retour vue d'ensemble Corse">← Vue d'ensemble</button>
```
Inspection runtime :
- `position: static`, `top: auto`, `left: auto`, `z-index: auto`
- parent = `<body class="niveau-2 niveau-2-actif">` (n'est pas dans un container)
- pas de classe CSS sur le bouton
- background rgb(240,240,240), couleur noire — style par défaut navigateur
- bounding rect actuel : (0, 0, w=114.9, h=19.2)

Le bouton sœur `← Retour doyenné` existe et fonctionne correctement au
niveau pieve (display: none en niveau doyenné, devient visible en niveau
pieve). Reproduire le même pattern pour `← Vue d'ensemble` : display: none
en niveau Corse, devient visible en niveau doyenné (`body.niveau-2-actif`),
et masqué quand on descend au niveau pieve (`body.niveau-3-actif` ou
équivalent).

**Fix B — sites Farinole mistagged** :

Test point-in-polygon vérifié runtime :
```
santa_maria_farinole (lat 42.82,    lng 9.36)   → dans pieve_canari ✓
tour_de_farinole     (lat 42.7333,  lng 9.3333) → frontière (canari plausible)
```

Les deux ont actuellement `pieve_slug: pieve_nebbiu` et
`doyenne_contemporain_slug: doyenne_du_cap` (cohérent commune Farinole).
Le tag pieve_nebbiu est l'erreur.

## 3. MODE

**Modification autorisée** sur :
- `patrimoine.html` (Fix A — CSS bouton)
- `docs/data/sites_patrimoine.json` (Fix B — 2 retags ciblés)

**Tu ne touches PAS** :
- `app.html` (hors scope)
- `docs/data/pieves_polygons.json` (pas de change pieve, juste retag de sites)
- Aucun fichier `_corpus/` ni `_drafts/`

## 4. ÉTAPES NUMÉROTÉES

```
[1] git checkout dev && git pull
[2] git checkout -b fix/patrimoine-nav-corse-farinole-2026-05-17
[3] Fix A — bouton « ← Vue d'ensemble » visible
    [3.1] Lire le CSS qui style « ← Retour doyenné » dans patrimoine.html
          (chercher #btn-retour-doyenne ou la classe parente niveau-3-actif).
    [3.2] Ajouter un CSS miroir pour #btn-retour-corse :
          - même position (probablement fixed top + left, ou absolute
            dans un container du panel haut-gauche)
          - même z-index (au-dessus du leaflet container ET de l'en-tête)
          - même style visuel (background, padding, border, font, etc.)
          - visibility logique :
              body.niveau-1-actif #btn-retour-corse { display: none; }
              body.niveau-2-actif #btn-retour-corse { display: flex; }
              body.niveau-3-actif #btn-retour-corse { display: none; }
            (ou logique équivalente selon ce que tu trouves pour le bouton sœur)
    [3.3] Vérifier en local que le bouton apparaît bien au niveau doyenné
          (server local + browser).
    → commit "fix(patrimoine): rendre visible bouton retour Corse au niveau doyenné"

[4] Fix B — retag 2 sites Farinole
    [4.1] Dans docs/data/sites_patrimoine.json, repérer les 2 entrées :
              santa_maria_farinole
              tour_de_farinole
    [4.2] Changer leur pieve_slug : "pieve_nebbiu" → "pieve_canari"
          (le doyenne_contemporain_slug reste doyenne_du_cap, cohérent)
    [4.3] Vérifier JSON valide :
              python3 -c "import json; json.load(open('docs/data/sites_patrimoine.json'))"
    [4.4] Compter post-fix :
              python3 -c "
              import json
              from collections import Counter
              s = json.load(open('docs/data/sites_patrimoine.json'))['sites']
              c = Counter(x.get('pieve_slug') for x in s)
              print('pieve_nebbiu :', c.get('pieve_nebbiu',0), '(était 30, attendu 28)')
              print('pieve_canari :', c.get('pieve_canari',0), '(attendu +2)')
              "
    → commit "fix(patrimoine): retag 2 sites Farinole vers pieve_canari"

[5] git push origin fix/patrimoine-nav-corse-farinole-2026-05-17

[6] Attendre build Cloudflare preview.

[7] Vérifs preview CF :
    [7.1] /patrimoine.html charge sans erreur console
    [7.2] Au niveau Corse (vue d'ensemble), le bouton retour Corse n'apparaît PAS.
    [7.3] Au niveau doyenné (clic sur un doyenné), le bouton retour Corse
          apparaît, lisible, cliquable.
    [7.4] Clic sur le bouton retour Corse → retour à la vue Corse.
    [7.5] Aller en #doyenne_du_cap/pieve_canari → vérifier que les 2 sites
          Farinole apparaissent maintenant dans cette pieve.
    [7.6] Aller en #doyenne_du_golo/pieve_nebbiu → vérifier que les 2 sites
          Farinole ne s'y affichent plus.

[8] Ouvrir PR fix/patrimoine-nav-corse-farinole-2026-05-17 → dev.
    Description = synthèse des 2 fixes + résultats des vérifs preview.

[9] Si preview OK : merge sur dev en autonomie.

[10] Ouvrir PR dev → main, merge en autonomie (cette PR ne touche aucun
     fichier du périmètre EM scientifique).
```

## 5. RÈGLES STRICTES

- `git status` propre avant chaque commit.
- 2 commits séparés (Fix A puis Fix B), pas un commit géant.
- Aucun guillemet courbe (U+2018/U+2019) dans les patches.
- Pas de modification de pieves_polygons.json ni du mapping amont.
- Si le bouton sœur `← Retour doyenné` a un style plus complexe que prévu
  (par exemple intégré dans un container du panneau latéral), adapte
  intelligemment plutôt que de coller du CSS rigide.
- Règle « je-ne-sais-pas » maintenue : tout état inattendu → STOP.

## 6. POINT DE VALIDATION

Aucun arrêt obligatoire de validation Soleil pour cette PR (autonomie
doctrinale 2026-05-17, périmètre non-EM scientifique). Le rapport en chat
post-merge dev → main suffit comme livrable.

Cas d'arrêt obligatoire malgré tout :
- build CF échoue
- console errors imprévus en preview
- comportement divergent (bouton invisible même après le fix, ou retag
  qui ne se répercute pas dans la vue)

## 7. LIVRABLES ATTENDUS

À la fin de la session, en chat (post-merge main) :

- branche `fix/patrimoine-nav-corse-farinole-2026-05-17` poussée et mergée
- 2 commits clairs (Fix A, Fix B)
- PR dev / PR main mergées
- rapport synthétique : ce qui a été fait, screenshots preview avant/après
  si possible, anomalies rencontrées
- aucun fichier .md de session créé (pas la peine pour ce volume)

---

**Fin du prompt.**
