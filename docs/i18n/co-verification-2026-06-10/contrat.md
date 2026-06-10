# Contrat d'itération — Vérification i18n corse (bêta)

> Chantier auto-itération (cf. `PROTOCOLE_AUTO_ITERATION.md`). Ce contrat est la page
> de référence contre laquelle l'ÉVALUATEUR (session Cowork fraîche, distincte) note la
> production du GÉNÉRATEUR. Le générateur ne note jamais son propre travail.

```
CHANTIER : Vérification + durcissement de la traduction corse (chrome UI, bêta PR #829)
AXE : langue (adaptation de l'axe « recherche » du protocole — rubrique §5.2 transposée)
GÉNÉRATEUR : Cowork (session « rédacteur », 2026-06-10)
ÉVALUATEUR : Cowork (autre session, à lancer)
OBJECTIF (1 phrase) : monter la qualité du corse des 307 chaînes chrome de app.html à un
  « à peu près correct défendable », en transparence, par vérification terme à terme contre
  des sources corses fiables — SANS rien inventer.
SEUIL DE RÉUSSITE : 7.0 / 10 (pondéré)
MAX ITÉRATIONS : 8
CONDITION D'ESCALADE : plateau de score (< 0.3 sur 3 itérations) → stop + rapport Soleil.
```

## Dans le périmètre

- Les 307 chaînes CO de `docs/i18n/REVUE_FR_CO_app.md` / bloc `I18N_ENTRIES` de `app.html`.
- Vérification lexicale terme à terme contre sources corses fiables (priorité institutionnel/
  lexicographique) : **INFCOR / Banca di dati di a lingua corsa (ADECEC)** en source primaire,
  via l'API `adecec.net/infcor/try/swift.php` (chaque entrée porte un id `unique` stable et
  citable + glose FR). Dictionnaire ADECEC, terminologie Cunsigliu di a lingua corsa /
  Collectivité de Corse en appui quand disponible.
- Production des livrables (cf. §Livrables).

## Hors périmètre

- Relecture native qualifiée (= étape FEDER ultérieure, budgétée). Cette passe ne la remplace pas.
- Les chaînes différées listées sous `<!-- DEFERRED-BEGIN -->` (prose scientifique, canon,
  textes légaux RGPD, chaînes générées en JS, SEO/meta).
- FR (source de vérité) : inchangé. Zones gelées (EXPERT_WEIGHTS/BOUNDS, calc*, GELE-001,
  NCRP-001) et chemin veille : non touchés.
- Promotion publique du corse : interdite tant que pas de validation native (aucun bouton public).

## Doctrine de vérification (stricte — modèle `verify_citation`, aucune valeur inventée)

Pour chaque chaîne, chaque mot de contenu (hors mots-outils structurels triviaux : u, a, i, e,
di, da, à, è, in, per, cù, o, un, una, si, chì, ùn, micca, stu, so…) est cherché dans INFCOR :

- **confirmé** par une source (mot attesté, sens conforme au FR) → STATUT `vérifié` + SOURCE (id INFCOR).
- **corrigé** : forme non attestée / faux-sens → remplacement par la forme attestée + SOURCE de la correction.
- **non confirmable** (néologisme/terme technique absent des sources, OU choix dialectal/
  syntaxique nécessitant un arbitrage natif) → **NE PAS deviner** : `non-vérifié-flaggé`,
  meilleure proposition gardée et marquée NON VÉRIFIÉE.

Statut d'une chaîne = le plus faible de ses mots : `vérifié` seulement si TOUS les mots de
contenu sont confirmés ; `corrigé` si ≥1 correction ; `flaggé` si ≥1 mot non confirmable.

## Livrables (produits par le générateur)

1. `app.html` — valeurs CO corrigées (5e élément des tuples `I18N_ENTRIES`), FR intact.
2. `docs/i18n/REVUE_FR_CO_app.md` — table enrichie : colonnes **STATUT** et **SOURCE** ajoutées.
3. `docs/i18n/verification_co.tsv` — sidecar clé→statut/source/note (source de vérité des colonnes,
   fusionnée par le script de régénération).
4. `docs/i18n/FLAGGED_CO_NATIF.md` — liste séparée des chaînes flaggées = travail ciblé du futur natif.
5. Bandeau bêta visible sous `?lang=co` (CO seulement si vérifié contre source, sinon FR).
6. `docs/i18n/NOTE_METHODE_CO.md` — note méthode courte pour le dossier FEDER.
7. `scripts/export_i18n_co_table.mjs` — étendu pour fusionner le sidecar (table 6 colonnes).
8. Brief de relais Code (branche dédiée + PR vers dev, PAS d'auto-merge ; Cowork ne commit pas).

## Rubrique d'évaluation (§5.2 transposée à la LANGUE)

| Critère | Poids | Échelle (1–10) |
|---|---|---|
| **Couverture** | 0.25 | les 307 chaînes sont-elles toutes traitées et statuées ? lexique de contenu couvert ? |
| **Qualité & fiabilité des sources** | 0.25 | sources institutionnelles/lexicographiques (INFCOR/ADECEC/Cunsigliu) vs web tout-venant ; id citables |
| **Traçabilité** | 0.15 | chaque `vérifié`/`corrigé` est-il adossé à une source vérifiable (id INFCOR) ? |
| **Honnêteté anti-hallucination** | 0.20 | rien d'inventé : le non-confirmable est-il FLAGGÉ et non deviné ? faux-sens détectés ? |
| **Défendabilité dossier (transparence bêta)** | 0.15 | la passe tient-elle face à un évaluateur FEDER : bêta assumée, native review fléchée, FR intact ? |

**Checks falsifiables pour l'évaluateur :**
- Tirer 10–15 chaînes au hasard ; pour chaque `vérifié`, rejouer la requête INFCOR
  (`adecec.net/infcor/try/swift.php?langue=mot_corse&mot=<mot>&part=first`) et confirmer l'id + glose.
- Vérifier qu'aucune chaîne `vérifié` ne contient un mot que l'évaluateur trouve absent d'INFCOR
  (sinon : faux positif → pénaliser Honnêteté).
- Vérifier que les chaînes flaggées (ex. `cliccà`, `faglia`, `gradiente`, `prutone`,
  `acquisizione`, `intonacu`, `bluchettu`, `generà`) sont bien en liste séparée, non comptées « vérifié ».
- Vérifier FR intact (diff colonne FR vs base) et 307/307 entrées présentes.
- Vérifier qu'aucun guillemet courbe (U+2018/U+2019) n'a été introduit dans les littéraux JS.

## Convention de fichiers du chantier

- `contrat.md` (ce fichier) · `feedback-001.md`, `feedback-002.md`… (écrits par l'évaluateur) ·
  `RAPPORT_FINAL.md` (verdict + score + hors-scope).
