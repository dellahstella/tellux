# Note de méthode — version corse (bêta) de l'interface Tellux

*Note de méthode interne. Rédigée 2026-06-10.*

## Démarche

L'interface cartographique Tellux (`app.html`) est proposée, à titre **bêta et non public**,
dans une version corse accessible uniquement via le paramètre `?lang=co` (aucun bouton public).
Le **français reste la langue de référence** : le mécanisme de traduction est purement additif
et garde le texte français verbatim — si une chaîne française évolue, la traduction corse
correspondante est automatiquement sautée plutôt qu'affichée de façon erronée.

Le porteur n'étant pas bilingue corse, la chaîne de production a été conçue pour rester
**honnête et traçable** plutôt que de simuler une maîtrise native :

1. **Génération** : 307 chaînes d'interface (chrome : navigation, boutons, titres de panneaux,
   tooltips, libellés de formulaire) ont été traduites par modèle. La prose scientifique, le
   contenu de cadrage épistémique, les mentions légales (RGPD, consentements) et les messages
   générés dynamiquement en JavaScript ont été **volontairement laissés en français** (hors
   périmètre bêta — ils relèvent d'une validation scientifique ou juridique distincte).

2. **Vérification lexicale contre sources corses fiables** : chaque mot de contenu des
   traductions a été contrôlé contre **INFCOR — Banca di dati di a lingua corsa**, la base
   lexicographique de l'ADECEC (Association pour le développement des études archéologiques,
   historiques, linguistiques et naturalistes du centre-est de la Corse). Chaque confirmation
   est adossée à un **identifiant d'entrée stable et rejouable** de la base (citable et
   vérifiable par un tiers).

3. **Doctrine stricte anti-approximation** (calquée sur la vérification de citations) :
   - mot **attesté** au sens conforme → statut *vérifié* + source (id INFCOR) ;
   - mot **non attesté / faux-sens** → si une forme attestée existe, correction sourcée ;
     sinon, **aucune invention** : la proposition est conservée et **marquée non vérifiée** ;
   - **choix dialectal** (cismontincu / pumontincu) ou terme technique/néologisme absent des
     sources → **flaggé** pour arbitrage par un locuteur natif, jamais tranché unilatéralement.

## Résultat de la passe (2026-06-10)

- Après trois itérations de revue contradictoire, **chaque mot a été rejoué par forme exacte** sur
  INFCOR, avec exigence que l'id renvoyé corresponde à l'id-lemme assigné (sinon → flexion).
  Sur 307 chaînes : **141 vérifiées** (tous les mots attestés-direct, forme exacte rejouable),
  **76 vérifiées-flexion** (tous attestés mais contenant une flexion régulière d'un lemme attesté dont
  la forme exacte n'est pas un sous-lemme rejouable tel quel), **89 flaggées**, **1 à confirmer**.
  Lexique : 256 formes attestées-direct + 111 flexions-inférées (id du lemme cité) + 79 flaggées.
- La distinction *vérifié* / *vérifié-flexion* est explicite (colonne SOURCE : « flexion: <id> »)
  pour ne jamais présenter une flexion non rejouable comme une attestation directe.
- **89 chaînes flaggées** pour le relecteur natif (faux-sens possibles ou termes techniques/scientifiques non
  lexicographiés dans une base de langue générale : ex. « citoyen » rendu par *citatinu* que INFCOR
  ne donne que comme « citadin » ; *cliccà* « cliquer », *faglia* « faille », *gradiente*, *prutone*,
  *acquisizione*, *intonacu* « enduit », *sensore* « capteur », *betone* « béton » — non attestés ;
  plus des formes régulières non lemmatisées, signalées comme telles).
- **1 seule chaîne** reste *à confirmer* (sens « corsi d'acqua » = cours d'eau). Aucune chaîne
  n'est présentée comme vérifiée sans source.
- **Français inchangé** (contrôle automatique : clés + texte FR identiques à la version de référence).

## Suite prévue

Une **relecture native qualifiée** (locuteur corse, idéalement en lien avec le Cunsigliu di a
lingua corsa) constitue une **étape ultérieure**. La présente
passe a pour seul objet de porter la qualité à un niveau « correct et défendable » et de fournir
au relecteur natif une **liste de travail ciblée** (`FLAGGED_CO_NATIF.md`) plutôt qu'une relecture
intégrale à l'aveugle. La version corse ne sera **promue en bascule publique qu'après cette
validation native**.

## Traçabilité

- Données de vérification : `docs/i18n/verification_co.tokens.json` (formes → id INFCOR).
- Table de revue bilingue annotée : `docs/i18n/REVUE_FR_CO_app.md` (colonnes STATUT / SOURCE).
- Sidecar par chaîne : `docs/i18n/verification_co.tsv`.
- Liste flaggée pour le natif : `docs/i18n/FLAGGED_CO_NATIF.md`.
- Outillage rejouable : `scripts/verify_i18n_co.mjs`, `scripts/export_i18n_co_table.mjs`.
- Source primaire : INFCOR / ADECEC — `https://adecec.net/infcor`.
