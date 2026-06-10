# RAPPORT FINAL — Vérification i18n corse (bêta) · chantier 2026-06-10

> Clôture du chantier auto-itération (`PROTOCOLE_AUTO_ITERATION.md`). Rédigé par la session
> ÉVALUATEUR. Synthèse des 3 itérations, verdict, livrables, hors-scope, étapes suivantes.

## Verdict

**SUCCÈS — score final 8.0 / 10** (seuil 7.0). Trajectoire sur 3 itérations : **7.6 → 7.2 → 8.0**,
ascendante, pas de plateau. Le creux it. 2 (sur-extension de la couverture) a été identifié par
l'évaluateur puis corrigé en it. 3. La passe atteint son objectif : porter le corse du chrome UI
à un niveau « correct et défendable », **en transparence et sans rien inventer**, avec une
worklist ciblée pour le relecteur natif.

## Résultat final (307 chaînes chrome)

| Statut | Chaînes | Sens |
|---|---|---|
| `vérifié` (direct) | **141** | tous les mots de contenu ont leur forme exacte attestée dans INFCOR (id renvoyé == id-lemme assigné) |
| `vérifié (flexion)` | **76** | flexion régulière d'un lemme attesté ; SOURCE = `flexion: <id>` (forme exacte non rejouable telle quelle) |
| `flaggé` | **89** | ≥1 mot non attesté / faux-sens / terme technique → arbitrage natif |
| `à confirmer` | **1** | ≥1 mot non encore re-vérifié |

Lexique : **256 formes attestées-direct + 111 flexions-inférées + 79 flaggées.**
**FR strictement intact** (clés + colonne FR == HEAD), `app.html` non édité, 307/307 entrées.

## Ce qui a été produit (à committer par Code)

Modifiés : `docs/i18n/REVUE_FR_CO_app.md` (table 6 colonnes STATUT/SOURCE) ·
`scripts/export_i18n_co_table.mjs` (fusion sidecar).
Nouveaux : `docs/i18n/verification_co.tokens.json` (verified / inferred / flags) ·
`docs/i18n/verification_co.tsv` · `docs/i18n/FLAGGED_CO_NATIF.md` · `docs/i18n/NOTE_METHODE_CO.md` ·
`scripts/verify_i18n_co.mjs` · tout le dossier `docs/i18n/co-verification-2026-06-10/`
(contrat, feedback-001/002/003, changelogs it.2/it.3, infcor_cache, RELAIS_CODE, ce rapport).

## Méthode (pour le dossier FEDER)

Vérification terme à terme contre **INFCOR / Banca di dati di a lingua corsa (ADECEC)**, source
lexicographique institutionnelle, chaque attestation adossée à un id d'entrée stable et rejouable.
Doctrine stricte anti-invention : attesté → `vérifié` + id ; flexion régulière → `vérifié (flexion)`
avec id du lemme ; non confirmable (néologisme/terme technique/faux-sens) → `flaggé`, jamais deviné.
Le détail est dans `NOTE_METHODE_CO.md`.

## Hors-scope (assumé)

- **Relecture native qualifiée** = étape ultérieure budgétée (le chantier la prépare via
  `FLAGGED_CO_NATIF.md`, il ne la remplace pas). Pas de bascule publique CO avant validation native.
- Chaînes différées (prose scientifique, canon, légal RGPD, JS dynamique, SEO) : laissées en FR.
- Zones gelées (EXPERT_WEIGHTS/BOUNDS, calc*, GELÉ-001, NCRP-001), chemin veille : non touchés.

## Résidu de feedback-003 — CORRIGÉ (arbitrage Soleil, sans nouvelle itération)

Le défaut de précision signalé en feedback-003 (re-test classant `DIRECT` sur réponse non vide
sans exiger `unique renvoyé == id assigné`, alors que `part=first` est un match **par préfixe**)
a été **corrigé directement** sur arbitrage de Soleil. Re-test ciblé par forme exacte des 8 formes
DIRECT à id partagé : **5 rétrogradées en `vérifié (flexion)`** car la requête renvoie un id ≠
id-lemme assigné (`campi`→8228 ; `siti`→43797 « soif » ; `corsa`→11248 « course » ; `publiche`→54626 ;
`tecnica`→49085), **3 confirmées DIRECT** (`rete` 38578, `materiale` 27433, `capisce` 8508 — forme
exacte listée, id concordant). Les variantes à article élidé (`l'invisibile`…) restent direct (le
lexème est attesté, l'article est un clitique grammatical). Totaux post-correctif intégrés ci-dessus.

## Étapes suivantes (Code / Soleil — Cowork ne pousse pas)

1. Appliquer le **bandeau bêta** (snippet FR exact dans l'IIFE i18n) — cf. `RELAIS_CODE.md` §2.
2. Brancher `feat/i18n-co-verification` depuis `dev`, committer les livrables ci-dessus,
   ouvrir **PR vers `dev`, sans auto-merge** (arbitrage Soleil). Repasser les checks `RELAIS_CODE.md` §3
   (FR intact, 307/307 appliquées sous `?lang=co`, 0 erreur console, bandeau OK).

**Chantier clos côté auto-itération.** Reprise possible en it. 4 uniquement si Soleil veut le
correctif id-match scoré (gain attendu ~8.5) ; sinon la passe part en relais Code telle quelle.
