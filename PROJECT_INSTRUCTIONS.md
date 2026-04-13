# TELLUX — Instructions projet pour les sessions Cowork

**Mise à jour :** 13 avril 2026
**Usage :** Ce fichier est lu en début de chaque session. Il contient les règles de conduite impératives.

---

## 1. Fichier HTML canonique

**Source de vérité : `tellux_CORRECT.html`**

Toute modification de code doit cibler ce fichier ou y être reportée avant la fin de la session. Le fichier `tellux_v6_design.html` peut servir de brouillon mais ne fait pas foi.

**Règle absolue :** ne jamais écraser `tellux_CORRECT.html` sans avoir lu les sections concernées au préalable. Toujours vérifier que les fonctions existantes sont préservées après modification.

---

## 2. Économie de tokens

Les sessions ont un budget de contexte limité. Pour le préserver :

- Lire uniquement les sections nécessaires du HTML (utiliser `offset` + `limit`).
- Ne pas relire un fichier déjà lu dans la même session.
- Privilégier les modifications ciblées (Edit) plutôt que les réécritures complètes (Write) pour le HTML.
- Regrouper les modifications par zone du fichier.

---

## 3. Workflow de modification du code

1. **Lire** la zone ciblée du HTML.
2. **Éditer** avec l'outil Edit (remplacement exact).
3. **Vérifier** que les fonctions voisines ne sont pas cassées (grep rapide des noms de fonction).
4. **Lister** les modifications en fin de session pour le rapport.

Ne jamais modifier le code sans avoir lu le contexte immédiat (50 lignes avant/après minimum).

---

## 4. Garde-fous domaine

### Ce que Tellux est
Un outil de cartographie et de visualisation des contributions EM en Corse, avec un module patrimoine (sites mégalithiques, églises romanes) et un module agronomie (diagnostic parcellaire).

### Ce que Tellux n'est pas
- Un outil de diagnostic médical.
- Un substitut à des mesures professionnelles certifiées.
- Un système de prédiction ou d'alerte EM.
- Un outil de géobiologie ésotérique.

### Position épistémique (obligatoire)
Lire `TELLUX_POSITION_EPISTEMIQUE.md` avant toute rédaction de contenu textuel.

**3 formulations interdites :**
1. "deux réalités différentes" (le champ EM est un seul champ physique)
2. "les mesures ne s'additionnent pas" (elles s'additionnent vectoriellement — superposition)
3. "naturel = bénin" (les perturbations géologiques ne sont pas intrinsèquement inoffensives)

---

## 5. Choix de modèle

| Tâche | Modèle recommandé |
|---|---|
| Code HTML/JS, bugs, architecture | Opus |
| Rédaction dossiers, communications, audit texte | Sonnet |
| Tâches rapides, vérifications simples | Haiku |

Les sessions code critiques (modifications du HTML canonique) doivent être faites en Opus.

---

## 6. Candidature CTC

Le dossier CTC est en préparation (`CANDIDATURE_TELLUX_v7.docx`). Toute modification du projet doit rester cohérente avec les arguments du dossier. En cas de doute, ne pas ajouter de fonctionnalité qui compliquerait l'explication du projet aux évaluateurs.

---

## 7. Refus et limites

Le modèle peut et doit refuser de :

- Modifier le code sans avoir lu la zone concernée.
- Ajouter des sites au corpus sans source vérifiable.
- Rédiger du contenu qui contrevient à la position épistémique.
- Promettre des capacités que Tellux n'a pas (diagnostic santé, prédiction).

---

## 8. Patterns techniques à respecter

- **L.rectangle** : toujours `interactive: false` (sinon bloque les clics carte).
- **FAB mesure** : appeler `startContribFromFAB()`, avec `map.once('click')` dans `setTimeout(0)`.
- **Palette DA v2** : Ardoise #1F2329, Pierre #F5F0E7, Maquis #3F5B3A, Ocre #C28533, Porphyre #8E2F1F, Tyrrhénien #1F3A5F.
- **Typographie** : Fraunces (titres), IBM Plex Sans (corps).
- **Hébergement** : Cloudflare Pages (`tellux.pages.dev`). Pas Netlify.
- **Backend** : Supabase. Migrations versionnées dans `_migrations/`.

---

## 9. Fin de session

Avant de terminer une session :

1. Lister toutes les modifications apportées au code.
2. Mettre à jour `TELLUX_ROADMAP.md` si des items ont changé d'état.
3. Signaler toute divergence entre `tellux_CORRECT.html` et `tellux_v6_design.html`.
4. Ne pas créer de fichiers markdown redondants — mettre à jour les existants.
