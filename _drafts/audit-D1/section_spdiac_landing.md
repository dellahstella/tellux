<!--
Statut : retiré de la landing le 1er mai 2026 (décision éditoriale Soleil).
Motif : sobriété de la landing publique, la cohérence narrative institutionnelle
est portée par le dossier FEDER lui-même. Pas d'obligation légale ni
conventionnelle, jugement éditorial.
Conservé pour usage potentiel ultérieur, par exemple page À propos dédiée
(écart 4.4 de l'audit Phase D, pas encore traité).
Historique : intégré sprint audit-D2 (PR #276/#277, commit 3847ee3) puis retiré
sprint chore/landing-retrait-section-spdiac.
-->

# Livrable 1 — Section « Inscription territoriale » pour la landing `index.html`

**Sprint** : audit-D1 (Phase D du 2026-05-01)
**Référence audit** : sections 3.2 et 5.1
**Statut** : draft markdown — à intégrer par sprint Code 2 (pas d'écriture HTML dans ce sprint)

---

## 1. Texte rédigé (prose continue, ~340 mots)

> Tellux s'inscrit dans la stratégie numérique territoriale de la Collectivité de Corse, articulée autour de trois cadres successifs.
>
> Le **Programme Opérationnel FEDER-FSE+ Corse 2021-2027** identifie, dans son Objectif Spécifique RSO1.2 « Tirer parti des avantages de la numérisation », une **Ligne 2** dédiée aux initiatives associatives et collectives en faveur de la valorisation des biens communs environnementaux via des services numériques. Tellux relève directement de cette ligne : la cartographie publique de l'environnement électromagnétique corse est conçue comme bien commun documentaire, pas comme produit commercial.
>
> Le **Schéma Directeur Territorial d'Aménagement Numérique Smart Isula**, adopté par l'Assemblée de Corse en juin 2022 (délibération 22/074 AC), structure la stratégie numérique régionale autour de trois piliers : maîtrise des infrastructures numériques, cybersécurité, et **donnée comme bien commun**. Tellux contribue au troisième pilier, en produisant un référentiel territorial spécifiquement insulaire — la Corse n'a aujourd'hui aucune cartographie intégrée des quatre régimes physiques électromagnétiques sur son territoire — accompagné de services d'accès et de réutilisation.
>
> Le **Service Public de la Donnée et de l'IA de la Corse (SPDIAC)**, formalisé par le rapport délibératif 2026E1009 de l'Assemblée de Corse adopté en janvier 2026, identifie huit thématiques prioritaires pour le développement de la donnée publique régionale. Tellux contribue à la cinquième de ces thématiques, **« risques naturels et environnement »**, jusqu'ici insuffisamment couverte par les référentiels publics corses sur sa dimension électromagnétique. L'articulation technique avec le SPDIAC fait l'objet d'échanges institutionnels en cours.
>
> Cette inscription stratégique n'est pas un alignement opportuniste. Elle est constitutive de la conception du projet, qui a été pensé dès l'origine en cohérence avec les principes de bien commun numérique, de souveraineté européenne, et de valorisation des données d'intérêt insulaire qui structurent la trajectoire Smart Isula. Tellux apporte une brique manquante à cette trajectoire, sur la dimension environnementale électromagnétique aujourd'hui non couverte. Aucun équivalent open et intégré n'existe à ce jour pour ce territoire.

**Volume** : 340 mots (cible 250-400 ✅).

---

## 2. Snippet HTML cible

À insérer **entre** la fermeture de la section `#projet` et l'ouverture de la section `#ressources`.

**Emplacement précis dans `index.html`** : entre la ligne `</div>` qui ferme `<div class="lp-section-dark reveal" id="projet">` (actuelle ligne 481) et la ligne d'ouverture `<div class="lp-section reveal" id="ressources">` (actuelle ligne 483).

**Choix de classe** : `lp-section reveal` (variante claire, pas `lp-section-dark`) pour créer une respiration entre la section sombre #projet et la section sombre #ressources, et pour s'aligner sur les sections institutionnelles claires #sources et #comprendre. Le pattern reproduit la structure exacte des sections existantes (`lp-section-label` + `h2.lp-section-h2` + `p.lp-section-sub` + contenu).

```html
<div class="lp-section reveal" id="inscription-territoriale">
  <div class="lp-section-label">Inscription territoriale</div>
  <h2 class="lp-section-h2">Articulation avec la stratégie<br> numérique de la Collectivité de Corse</h2>
  <p class="lp-section-sub">Tellux s'inscrit dans trois cadres successifs de la trajectoire Smart Isula : le Programme Opérationnel FEDER-FSE+, le Schéma Directeur Territorial d'Aménagement Numérique, et le Service Public de la Donnée et de l'IA de la Corse.</p>

  <div class="lp-project-grid" style="grid-template-columns:1fr;max-width:880px;">
    <div class="lp-project-part" style="background:white;border:1px solid var(--brume);">
      <h3 class="lp-project-h3" style="color:var(--ardoise);border-bottom-color:var(--brume);">Programme Opérationnel FEDER-FSE+ Corse 2021-2027</h3>
      <p class="lp-project-p" style="color:var(--mica);">L'Objectif Spécifique RSO1.2 « Tirer parti des avantages de la numérisation » identifie, dans sa Ligne 2, les initiatives associatives et collectives en faveur de la valorisation des biens communs environnementaux via des services numériques. Tellux relève directement de cette ligne : la cartographie publique de l'environnement électromagnétique corse est conçue comme bien commun documentaire, pas comme produit commercial.</p>
    </div>

    <div class="lp-project-part" style="background:white;border:1px solid var(--brume);">
      <h3 class="lp-project-h3" style="color:var(--ardoise);border-bottom-color:var(--brume);">SDTAN Smart Isula — délibération 22/074 AC, juin 2022</h3>
      <p class="lp-project-p" style="color:var(--mica);">Le Schéma Directeur Territorial d'Aménagement Numérique Smart Isula structure la stratégie numérique régionale autour de trois piliers : maîtrise des infrastructures numériques, cybersécurité, et donnée comme bien commun. Tellux contribue au troisième pilier, en produisant un référentiel territorial spécifiquement insulaire accompagné de services d'accès et de réutilisation.</p>
    </div>

    <div class="lp-project-part" style="background:white;border:1px solid var(--brume);">
      <h3 class="lp-project-h3" style="color:var(--ardoise);border-bottom-color:var(--brume);">SPDIAC — rapport délibératif 2026E1009, janvier 2026</h3>
      <p class="lp-project-p" style="color:var(--mica);">Le Service Public de la Donnée et de l'IA de la Corse identifie huit thématiques prioritaires pour le développement de la donnée publique régionale. Tellux contribue à la cinquième de ces thématiques, « risques naturels et environnement », jusqu'ici insuffisamment couverte par les référentiels publics corses sur sa dimension électromagnétique. L'articulation technique avec le SPDIAC fait l'objet d'échanges institutionnels en cours.</p>
    </div>
  </div>

  <p class="lp-section-sub" style="margin-top:32px;max-width:880px;">Cette inscription stratégique n'est pas un alignement opportuniste. Elle est constitutive de la conception du projet, qui a été pensé dès l'origine en cohérence avec les principes de bien commun numérique, de souveraineté européenne, et de valorisation des données d'intérêt insulaire qui structurent la trajectoire Smart Isula. Tellux apporte une brique manquante à cette trajectoire, sur la dimension environnementale électromagnétique aujourd'hui non couverte. Aucun équivalent open et intégré n'existe à ce jour pour ce territoire.</p>
</div>
```

---

## 3. Notes d'intégration pour le sprint Code 2

### Réutilisation de classes CSS existantes
- `lp-section reveal` : classe d'ancrage standard de la landing (révèle au scroll).
- `lp-section-label` / `lp-section-h2` / `lp-section-sub` : structure d'en-tête typique des sections (cf. `#fonctionnalites`, `#modele`, `#sources`, `#comprendre`).
- `lp-project-grid` / `lp-project-part` / `lp-project-h3` / `lp-project-p` : trois cartes empilées, classes empruntées à la section `#projet` existante mais avec overrides inline pour fond clair (les classes d'origine sont stylées pour fond sombre `lp-section-dark`). Le sprint Code 2 peut soit garder les overrides inline, soit créer une variante `lp-project-part--light` propre. Recommandation : variante propre pour éviter la dette CSS.

### Ancre de navigation
Si le sprint Code 2 décide d'ajouter un lien dans la `lp-nav-links` (ligne 250-256 de `index.html`), l'ancre `#inscription-territoriale` est utilisable. Toutefois la nav est déjà chargée (5 liens) — peut-être à réserver pour les pages secondaires.

### Conformité aux règles strictes du prompt
- ✅ Pas de mention d'attribution FEDER (formulé comme « relève de » / « est conçu comme » / « fait l'objet d'échanges en cours »).
- ✅ Pas de mention de `data.corsica` comme engagement actif.
- ✅ Pas de revendication « premier référentiel territorial EM intégré » — formulation prudente conservée : « Aucun équivalent open et intégré n'existe à ce jour pour ce territoire ».
- ✅ Pas de mention publique des modules Phase 2/3/4.
- ✅ Pas de mention publique de l'auto-affinage ou des modules P0-P3 comme déjà existants.
- ✅ Aucune des trois formulations proscrites employée.
- ✅ Pas de mention du domaine `tellux.corsica` non encore acquis.

### Cohérence avec le contenu existant
- La section `#projet` (l.468-481) parle déjà de « Pourquoi la Corse » et « Un vide à documenter ». La nouvelle section enchaîne logiquement en répondant à « dans quel cadre stratégique territorial ce vide est-il documenté ».
- La phrase de clôture reprend mot pour mot la formulation « Aucun équivalent open et intégré n'existe à ce jour pour ce territoire » utilisée à la ligne 474 d'`index.html`. Si le sprint Code 2 souhaite éviter la répétition dans la même page, deux options : reformuler dans la nouvelle section (ex. « ce qui en fait une brique sans équivalent open et intégré sur le territoire à ce jour ») ou retirer la phrase de la section #projet. Recommandation : laisser dans #projet (contexte plus narratif) et reformuler ici pour éviter la duplication littérale.
