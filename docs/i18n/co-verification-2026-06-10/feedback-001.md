# feedback-001 — Évaluation passe vérification i18n CO

> Session ÉVALUATEUR (Cowork, fraîche), 2026-06-10. Note la production du générateur
> contre `contrat.md` (rubrique §5.2 transposée LANGUE). L'évaluateur critique, ne corrige pas.
> Posture volontairement sévère (PROTOCOLE §2).

## Verdict

**Score pondéré : 7.6 / 10 → au-dessus du seuil (7.0). PASSE.**
Mais avec **une erreur factuelle bloquante avant remise au natif** (faux négatif `merria`)
et deux faiblesses méthodo à corriger en passe 2. La passe est honnête et traçable ; c'est
sa force. Sa faiblesse est la couverture réelle (68/307 « vérifié ») et un flag erroné détecté
au sondage.

## Checks falsifiables exécutés

| Check (contrat §Checks) | Résultat |
|---|---|
| Scripts rejoués (`verify_i18n_co.mjs`) | OK — reproduit **68 vérifié / 25 flaggé / 214 à confirmer**, total 307, 104 formes / 14 flags. Cohérent avec TSV + REVUE (309 lignes = en-tête + 307). |
| 307/307 entrées présentes | OK |
| FR intact | OK (trivial : `app.html` **non modifié**, absent du `git status`). REVUE FR dérivée de app.html. |
| Guillemets courbes U+2018/U+2019 dans littéraux `app.html` | OK — **aucun** dans le bloc i18n. *(Note : `scripts/verify_i18n_co.mjs` en contient un — dans la regex de strip d'apostrophes, pas un littéral app.html. Acceptable mais à surveiller.)* |
| Rejeu INFCOR `vérifié` (échantillon) | `cartugrafia`→9066 ✓, `palesà`→32510 ✓, `citatinu`→53963 ✓ (existe). **Aucun faux positif trouvé** sur l'échantillon vérifié. |
| Rejeu INFCOR flags « absent » | `faglia` ✓absent, `gradiente` ✓absent, `intonacu` ✓absent → flags **corrects**. |
| Faux positif / faux négatif | **`merria` → id 27910 ATTESTÉ** dans INFCOR (entrée `merria`). Le livrable le déclare « non attesté » (raisonnement sur le mauvais radical `merra=houe`). **Faux négatif factuel.** |

> Méthode évaluateur : `web_fetch` étant rate-limité (mur atteint par le générateur), rejeu via
> l'outil navigateur sur `swift.php?langue=mot_corse&mot=<mot>&part=first`. Échantillon ~7 mots.

## Notes par critère

**Couverture — 6.0 / 10 (poids 0.25).** Les 307 chaînes sont **toutes statuées** (bon).
Mais seules **68 (22 %)** atteignent « vérifié » ; **214 (70 %)** restent « à confirmer »
(quota INFCOR épuisé). Le lexique réellement vérifié = 104 formes sur ~494 tokens de contenu.
Honnêtement borné et tracé pour une passe 2 — mais le corpus reste majoritairement non vérifié.
Aggravant mineur : la liste `skip_extra` absorbe ~10 **mots de contenu** (verbes : `apre`,
`riaprite`, `entrite`, `lasciate`, `adopra`, `vulete`, `aduprata`, `aperta`…) qui devraient
tomber en « à confirmer », pas en « skip » (réservé aux mots-outils / acronymes / unités).
Conséquence mesurée : **2 chaînes classées « vérifié » reposent sur un mot de contenu skippé
non vérifié** : `obs_note_label` (« Chì **vulete** sparte ? ») et `cond_key_corr`
(« Currezzione **aduprata** »). Léger sur-classement.

**Qualité & fiabilité des sources — 7.5 / 10 (poids 0.25).** Choix de source excellent :
INFCOR/ADECEC, institutionnel/lexicographique, ids stables et citables (rejoués, ils résolvent).
Mais l'**application** a une faille : recours au radical approximatif plutôt qu'à la forme exacte
sur certains flags → c'est ce qui produit le faux négatif `merria`. La fiabilité de la **liste
flaggée** est donc à nuancer (au moins 1/14 motifs erroné).

**Traçabilité — 8.5 / 10 (poids 0.15).** Chaque « vérifié » adossé à un id INFCOR ;
`infcor_cache.md` (journal brut), TSV sidecar, `tokens.json`, scripts rejouables idempotents.
Rejeu indépendant : ids concordent. Très solide.

**Honnêteté anti-hallucination — 8.5 / 10 (poids 0.20).** Point fort. Rien d'inventé : le
non-confirmable est flaggé/laissé « à confirmer », jamais deviné. FR intact, `app.html` non
touché, 214 honnêtement non comptées « vérifié », bandeau en FR (pas de CO non vérifié exposé).
Aucun faux positif détecté côté « vérifié ». Dings : les 2 sur-classements ci-dessus, et le
faux négatif `merria` (erreur, mais dans le sens **prudent** — sur-flagger ≠ halluciner).

**Défendabilité dossier (transparence bêta) — 8.5 / 10 (poids 0.15).** Bêta assumée, pas de
bouton public, relecture native fléchée et budgétée, FR fait foi, `NOTE_METHODE_CO.md` claire
pour le FEDER. Tient face à un évaluateur de dossier.

**Calcul :** 6.0·0.25 + 7.5·0.25 + 8.5·0.15 + 8.5·0.20 + 8.5·0.15 = **7.6 / 10**.

## Corrections demandées (pour passe 2 / avant remise au natif)

1. **BLOQUANT — corriger `merria`.** `merria` (id INFCOR 27910) est attesté et correspond
   à l'usage corse courant pour « mairie ». Le passer de `flaggé` (« non attesté ») à `vérifié`
   (ou au minimum requalifier le motif). Impacte `nav_mairies`, `footer_mairies` + lexique §2.
   Re-tester toute la liste flaggée « absent » par **forme exacte** (pas par radical) : le faux
   négatif `merria` suggère que d'autres flags « absent » peuvent être des faux négatifs.
2. **Sortir les mots de contenu de `skip_extra`** vers « à confirmer » (verbes `apre`,
   `riaprite`, `entrite`, `lasciate`, `adopra`, `aduprata`, `vulete`, `aperta`, `vostra`, `sarà`,
   `altru`). Ne garder en skip que mots-outils / acronymes / unités / emprunts. Re-vérifier les
   2 chaînes alors déclassées (`obs_note_label`, `cond_key_corr`).
3. **Passe 2 INFCOR** sur les 214 « à confirmer » (quota reset) pour relever la couverture
   réelle — c'est le principal levier de score (Couverture 6.0).

## Non-bloquant / hors-scope (conforme)

- Pas d'édition `app.html` ni de git côté Cowork : **conforme** à la doctrine. Le bandeau bêta
  + le câblage branche→PR `dev` sont délégués à Code via `RELAIS_CODE.md` (snippet exact, sans
  guillemet courbe). Vérifier juste, côté Code, que le snippet est bien **dans l'IIFE i18n**
  (retour anticipé si `lang!=='co'`) sinon le bandeau s'afficherait en FR.
- Guillemet courbe dans `verify_i18n_co.mjs` (regex de strip) : tolérable, mais le garde-fou
  projet vise « zéro U+2019 » — préférer `’` échappé dans la regex pour lever toute ambiguïté.

## Suite protocole

Score ≥ seuil → **SUCCÈS itération 1**. Mais la correction #1 (`merria`) est une erreur factuelle
dans un livrable destiné au natif : à traiter avant de figer la `FLAGGED_CO_NATIF.md`. Si le
générateur applique #1 et #2 (passe rapide, pas de nouveau quota requis), gain attendu surtout
sur Qualité-sources et Honnêteté. La passe 2 (#3) relèvera la Couverture lors d'un cycle ultérieur.
