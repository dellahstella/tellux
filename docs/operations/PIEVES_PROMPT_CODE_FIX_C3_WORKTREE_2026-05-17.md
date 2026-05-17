# Prompt Claude Code — Resync worktree + Fix C3 (note rattachement pieve_nebbiu)

**À copier-coller dans une session Claude Code locale sur le repo `tellux`.**
**Branche cible (pour Fix C3)** : `fix/patrimoine-c3-nebbiu-note-2026-05-17`
**Estimation** : ~45-60 min (resync + Fix C3).
**Doctrine** : autonomie workflow 2026-05-17, MAIS resync git contient des
opérations potentiellement destructrices → POINT D'ARRÊT obligatoire.

---

## 1. OBJECTIF

Deux missions enchaînées, dans cet ordre strict :

### Mission 1 — Resync du worktree local

Le worktree principal `Tellux/` de Soleil est désynchronisé :
- branche courante : `docs/cloture-serie-fix-n3-patrimoine-2026-05-15`
- 51 commits ahead / 1 commit behind par rapport à `origin/main`
- 12 fichiers untracked dont 4 qui existent déjà commitées dans `origin/main`

Le compteur 51 ahead masque probablement des commits squash-mergés. Audit
nécessaire avant action. Objectif final : worktree sur `main` propre et
à jour avec `origin/main`, sans perte de travail réel.

### Mission 2 — Fix C3 (note rattachement pieve_nebbiu)

Soleil arbitre option C3 (cf. `PIEVES_REFACTOR_PLAN_2026-05-17.md` §R-5 et
recommandation Cowork 2026-05-17 chat) : on garde le rattachement
`pieve_nebbiu → doyenne_du_golo` (intersection polygonale majoritaire 64.6%)
et on ajoute une note pédagogique dans le popup de la pieve pour expliquer
le choix et lever la surprise UX.

L'implémentation doit rester générique : tout pieve avec un champ
`note_rattachement` dans `pieves_polygons.json` voit son popup enrichi
automatiquement. On amorce avec pieve_nebbiu, et on documente le pattern
pour usage futur (autres pieves à mini-diocèse, collisions résiduelles
`pieve_aleria`, etc.).

## 2. CONTEXTE

### État audit worktree (à confirmer dès l'entrée en session)

```
branche locale : docs/cloture-serie-fix-n3-patrimoine-2026-05-15
ahead/behind   : 51 / 1 vs origin/main
HEAD          : 0398070 fix: force redeploy — pieves+sites JSON 500 on Cloudflare
```

Untracked à examiner :
```
docs/operations/ADR-001-pieves-doctrine.md                  ← existe en origin/main
docs/operations/PIEVES_PROMPT_CODE_2026-05-17.md            ← existe en origin/main
docs/operations/PIEVES_REFACTOR_EXEC_CODE_2026-05-17.md     ← existe en origin/main
docs/operations/PIEVES_REFACTOR_PLAN_2026-05-17.md          ← existe en origin/main
docs/operations/PIEVES_PROMPT_CODE_FIX_AB_2026-05-17.md     ← N'EXISTE PAS en origin/main
docs/operations/PIEVES_PROMPT_CODE_FIX_C3_WORKTREE_2026-05-17.md ← le prompt actuel
note_arbitrages_veille_2026-05-08.md                        ← à arbitrer Soleil
note_inventaire_megalithes_2026-05-12.md                    ← à arbitrer Soleil
note_inventaire_megalithes_candidats_2026-05-12.md          ← à arbitrer Soleil
note_synthese_exemple.md                                    ← à arbitrer Soleil
note_veille_2026-05-09.md                                   ← à arbitrer Soleil
prompt_veille_tellux_v1.md                                  ← à arbitrer Soleil
prompt_veille_tellux_v2.md                                  ← à arbitrer Soleil
```

### Pour Fix C3

Pattern générique cible : dans `patrimoine.html`, là où le popup pieve est
construit (fonction qui consomme `pieveNameBySlugV2[slug]` ou équivalent),
ajouter une lecture optionnelle du champ `note_rattachement` du JSON
`pieves_polygons.json` et un bloc HTML conditionnel dans le popup.

Texte cible pour `pieve_nebbiu` (à insérer dans le JSON) :

```
"Pieve historiquement liée au diocèse médiéval du Nebbiu (Saint-Florent).
Rattachée ici au doyenné contemporain du Golo par intersection polygonale
majoritaire (~65 %), mais constitue une entité géographique distincte
couvrant Saint-Florent, Patrimonio, Murato et le Désert des Agriate."
```

Soleil peut ajuster le ton à la relecture. Va au plus proche.

## 3. MODE

**Modification autorisée** sur :
- worktree local (changement de branche, suppression fichiers untracked
  identiques aux versions origin/main, après confirmation)
- `docs/data/pieves_polygons.json` (ajout 1 champ pour pieve_nebbiu)
- `patrimoine.html` (patch léger popup)

**Tu ne touches PAS** sans confirmation explicite Soleil :
- `git push --force` sur quoi que ce soit
- `git reset --hard` sur la branche partagée
- Suppression de la branche locale `docs/cloture-serie-fix-n3-patrimoine-2026-05-15`
  tant que l'audit ahead n'a pas confirmé que tout son contenu est déjà
  en origin/main

## 4. ÉTAPES NUMÉROTÉES

### Mission 1 — Resync worktree

```
[1.1] git fetch origin
[1.2] git status -sb
[1.3] git log origin/main..HEAD --oneline > /tmp/ahead.txt
      wc -l /tmp/ahead.txt
      (devrait sortir ~51 lignes)
[1.4] Pour chaque commit ahead, vérifier s'il est déjà en main via squash :
      pour les ~10 plus récents au moins, faire
        git log origin/main --oneline --grep="<premiers mots du sujet>"
      ou comparer les diffs.
      Si tous matchent un commit squashé en main → OK pour bascule.
      Si certains sont du travail local non mergé → STOP, signaler à Soleil
      avec la liste.

[1.5] POINT D'ARRÊT 1 — confirmer à Soleil :
      « 51 commits ahead audités. X déjà mergés via squash, Y candidats
      non-mergés (liste). Je propose : push de docs/cloture-... sur origin
      en backup, puis switch main. OK ? »
      Attendre OK explicite.

[1.6] git push origin docs/cloture-serie-fix-n3-patrimoine-2026-05-15
      (backup distant, ne casse rien)

[1.7] git checkout main
      git pull origin main

[1.8] Untracked safe à supprimer (existent déjà en origin/main, contenu
      identique vérifié par diff) :
        docs/operations/ADR-001-pieves-doctrine.md
        docs/operations/PIEVES_PROMPT_CODE_2026-05-17.md
        docs/operations/PIEVES_REFACTOR_EXEC_CODE_2026-05-17.md
        docs/operations/PIEVES_REFACTOR_PLAN_2026-05-17.md
      Pour chacun :
        diff <untracked> <(git show origin/main:<chemin>) > /dev/null && rm <untracked>
      Si diff non-vide → laisser, signaler à Soleil.

[1.9] Untracked à NE PAS supprimer sans accord Soleil :
      note_arbitrages_veille_2026-05-08.md, note_inventaire_*, note_synthese_*,
      note_veille_*, prompt_veille_*
      Liste-les en chat avec leur taille (ls -l) et demande à Soleil
      l'arbitrage avant action.

[1.10] Untracked à conserver pour la PR Fix C3 :
       docs/operations/PIEVES_PROMPT_CODE_FIX_AB_2026-05-17.md
       docs/operations/PIEVES_PROMPT_CODE_FIX_C3_WORKTREE_2026-05-17.md
       (ils seront commités dans la branche Fix C3, cf. Mission 2)

[1.11] Rapport en chat : ahead 51 → 0, behind 1 → 0, untracked traités.
```

### Mission 2 — Fix C3 (note rattachement pieve_nebbiu)

```
[2.1] git checkout -b fix/patrimoine-c3-nebbiu-note-2026-05-17

[2.2] Édition docs/data/pieves_polygons.json :
      Trouver l'entrée pieve_nebbiu et ajouter le champ :
        "note_rattachement": "Pieve historiquement liée au diocèse médiéval du Nebbiu (Saint-Florent). Rattachée ici au doyenné contemporain du Golo par intersection polygonale majoritaire (~65 %), mais constitue une entité géographique distincte couvrant Saint-Florent, Patrimonio, Murato et le Désert des Agriate."
      (champ optionnel pour le pattern générique).

[2.3] Vérifier JSON valide :
        python3 -c "import json; json.load(open('docs/data/pieves_polygons.json'))"

[2.4] Édition patrimoine.html — patcher la fonction qui construit le popup
      d'une pieve (cherche `bindPopup` ou la fabrication HTML autour de
      `pieveNameBySlugV2[slug]`). Ajouter un bloc conditionnel :

        // après le titre / score principal
        if (pieveData && pieveData.note_rattachement) {
          html += '<div class="tlx-pieve-note">' +
                  '<strong>Note de rattachement :</strong> ' +
                  pieveData.note_rattachement +
                  '</div>';
        }

      Style CSS minimaliste dans la section <style> :
        .tlx-pieve-note {
          margin-top: 8px;
          padding: 6px 8px;
          background: rgba(123, 119, 112, 0.08);
          border-left: 2px solid var(--tx-mica, #7b7770);
          font-size: 12px;
          line-height: 1.4;
          color: var(--tx-fg, #22262b);
        }

      Adapter aux conventions exactes du fichier (variables CSS Tellux,
      structure HTML existante du popup).

[2.5] Test local :
        npx serve -p 8790 .   (ou ton serveur habituel)
      Ouvrir /patrimoine.html#doyenne_du_golo/pieve_nebbiu
      Vérifier que le popup pieve_nebbiu affiche bien la note.
      Vérifier qu'une autre pieve sans note (ex pieve_balagne) reste OK
      (pas de bloc vide, pas d'erreur console).

[2.6] git add + 2 commits séparés :
        commit 1 : "feat(patrimoine): pattern generique note_rattachement
                   sur popup pieve + amorcage pieve_nebbiu"
        commit 2 : "docs: tracer prompts Code Fix AB et Fix C3"
                   (ajoute les deux .md untracked PIEVES_PROMPT_CODE_FIX_*)

[2.7] git push origin fix/patrimoine-c3-nebbiu-note-2026-05-17

[2.8] Attendre build CF preview.

[2.9] Vérifs preview CF :
      - /patrimoine.html charge sans erreur
      - drill-down doyenne_du_golo → pieve_nebbiu : popup affiche la note
      - drill-down doyenne_du_cap → pieve_canari : popup SANS note (pas de
        bloc vide)
      - drill-down doyenne_du_golo → pieve_mariana : popup SANS note (idem)

[2.10] Si OK preview : ouvrir PR fix → dev, merge en autonomie.
       Puis PR dev → main, merge en autonomie (périmètre non-EM scientifique).

[2.11] Rapport en chat final : 2 missions clôturées, prod déployée.
```

## 5. RÈGLES STRICTES

- **POINT D'ARRÊT 1.5 OBLIGATOIRE** avant push backup ou bascule de branche.
  Resync n'est pas une opération que tu peux improviser : tout retour en
  arrière sur une perte de commits ahead non-mergés est complexe.
- Ne JAMAIS faire `git reset --hard` ou `git push --force` sans accord
  explicite Soleil (cf. CLAUDE.md règle merge).
- Si tu trouves dans les 51 commits ahead des trucs non commités ailleurs
  (vrai travail local), STOP. Ne supprime rien.
- Si les fichiers untracked des 4 docs PIEVES_* présentent un diff avec
  origin/main (même léger), ne supprime PAS le fichier untracked, laisse
  pour arbitrage Soleil.
- Aucun guillemet courbe dans les patches HTML/JS.
- Conserver la doctrine de commits séparés (1 commit = 1 intention).

## 6. POINT DE VALIDATION

- **Obligatoire** : étape 1.5 (audit ahead → bascule branche).
- **Recommandé** : étape 1.9 (untracked notes/prompts à arbitrer).
- **Pas d'arrêt** pour la Mission 2 (Fix C3) : autonomie complète preview
  → PR → merge dev → merge main.

## 7. LIVRABLES ATTENDUS

À la fin de la session, en chat :

- worktree principal sur `main` propre, 0 ahead, 0 behind, untracked nettoyés
  (sauf ceux laissés en attente arbitrage Soleil)
- branche `fix/patrimoine-c3-nebbiu-note-2026-05-17` mergée dev + main
- 2 commits clairs (note_rattachement générique + traçabilité prompts)
- screenshot ou JS dump confirmant la note visible sur prod pour pieve_nebbiu
- liste des éventuels untracked laissés en suspens, avec recommandation Cowork
  pour chacun (commit / supprimer / déplacer)

---

**Fin du prompt.**
