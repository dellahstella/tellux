# Livrable 2 — Section « Cadres éthiques de référence » pour `transparence.html`

**Sprint** : audit-D1 (Phase D du 2026-05-01)
**Référence audit** : sections 3.3 et 5.2
**Statut** : draft markdown — à intégrer par sprint Code 2 (pas d'écriture HTML dans ce sprint)

---

## 1. Texte rédigé (prose continue, ~530 mots)

> Tellux s'inscrit dans deux cadres éthiques territoriaux explicites de la Collectivité de Corse, et leur adoption formelle est envisagée dans le cadre du dossier de candidature FEDER en préparation. Les pratiques actuelles du projet préfigurent déjà cette adhésion sur plusieurs axes structurants.
>
> **La Charte de la donnée et de l'IA de la Corse** est structurée en vingt-et-un principes répartis en neuf titres. Plusieurs principes sont particulièrement structurants pour Tellux et sont déjà intégrés à la conception de la plateforme. Le principe n°1, « données d'intérêt insulaire », oriente la production de jeux de données spécifiquement territoriaux corses, en complément des référentiels nationaux : les classements radon par commune corse, les antennes ANFR de Corse, les couches géologiques BRGM 1/50 000 spécifiques à l'île, le réseau électrique EDF SEI insulaire. Le principe n°5, « hébergement souverain », est l'objet d'une trajectoire annoncée : l'infrastructure actuelle (Cloudflare Pages pour le site, Supabase eu-west-1 Irlande pour la base de contributions) est éligible à une migration vers un opérateur souverain européen pleinement soumis au droit européen, dont la temporalité est conditionnée au calendrier d'un éventuel financement. Les principes n°7 et n°8 sur la frugalité numérique se reflètent dans la stack technique : applications web sans framework lourd, polices auto-hébergées, pas de tracker tiers, pas de Google Fonts, datasets en formats compacts. Les principes n°15 et n°16 sur l'ouverture des algorithmes et la priorité open source sont déjà respectés : le code source intégral est publié sous licence MIT sur le dépôt public du projet, librement consultable, modifiable et réutilisable. Les principes n°17 et n°18 sur les biens communs numériques sont préfigurés par l'engagement de non-commercialisation et par la traçabilité publique des sources mobilisées.
>
> **Le Guide de bonne pratique IA Smart Isula** définit douze bonnes pratiques pour les systèmes d'apprentissage statistique mobilisés en contexte territorial. Tellux ne déploie aucun système d'IA à risque interdit au sens du Règlement IA UE 2024 (pas de notation sociale, pas d'identification biométrique, pas de police prédictive, pas de ciblage émotionnel). Un volet d'auto-affinage du modèle territorial par confrontation systématique entre mesures contributives et prédictions est étudié dans le cadre de la candidature FEDER, dont l'application des bonnes pratiques du Guide constituerait le cadre de mise en œuvre, conditionnel à l'obtention du financement. Plusieurs bonnes pratiques sont déjà préfigurées par les pratiques actuelles : la transparence des transformations effectuées sur les données (bonne pratique n°5) est garantie par la publication open source du code, la maîtrise des données et des algorithmes (bonne pratique n°10) est garantie par l'hébergement européen et par l'absence de dépendance à des services d'IA tiers, la documentation des biais (bonne pratique n°7) est ouverte par la position épistémique publique exposée dans le document Méthode et limites.
>
> **Articulation avec les pratiques actuelles.** L'adhésion préfigurée aux cadres territoriaux n'est pas un engagement futur isolé : elle prolonge des pratiques déjà visibles sur le site. Le code source est sous licence MIT, librement consultable. Aucun cookie publicitaire, aucun traceur d'analyse tiers, aucune revente de données. Les polices d'écriture sont auto-hébergées sous Open Font License. La base de contributions citoyennes, opérationnelle, applique d'ores et déjà la sécurité au niveau des lignes (Row Level Security) et l'anonymisation systématique des contributions agrégées. La position épistémique du projet — refus symétrique de l'alarmisme et de la trivialisation, distinction des niveaux d'inférence, exclusion de tout diagnostic médical — est documentée publiquement dans la page Méthode et limites et constitue le socle éthique préalable à toute adhésion formelle.
>
> Le statut actuel des deux cadres est donc le suivant : **adoption formelle envisagée dans le cadre du dossier de candidature FEDER en préparation, articulation préfigurée par les pratiques actuelles déjà visibles sur le site**. Toute évolution sera tracée dans la présente page Transparence.

**Volume** : 530 mots (cible 400-600 ✅).

---

## 2. Snippet HTML cible

À insérer en **nouvelle section 4 « Cadres éthiques de référence »** dans `transparence.html`, entre la section 3 actuelle (« Limites connues et zones en attente ») et la section 4 actuelle (« Architecture, code, licences ») — qui devient section 5.

**Emplacement précis dans `transparence.html`** :
- **Avant** : la fermeture `</section>` qui clôt la section 3 (actuelle ligne 380).
- **Après** : l'ouverture `<section>` de la section actuelle 4 « Architecture, code, licences » (actuelle ligne 382).

**Renumérotation à appliquer dans le même sprint Code 2** :
- Section actuelle 4 « Architecture, code, licences » → devient **section 5**.
- Section actuelle 5 « Comment signaler une erreur ou une incohérence » → devient **section 6**.
- Aucune autre section affectée.

**Note de style** : la page Transparence utilise un style sobre sans classes CSS complexes (juste `<section>`, `<h2>`, `<h3>`, `<p>`, `<ul>`, `<strong>`). Le snippet ci-dessous respecte exactement ce gabarit.

```html
<section>
  <h2>4. Cadres éthiques de référence</h2>
  <p>Tellux s'inscrit dans deux cadres éthiques territoriaux explicites de la Collectivité de Corse, et leur adoption formelle est envisagée dans le cadre du dossier de candidature FEDER en préparation. Les pratiques actuelles du projet préfigurent déjà cette adhésion sur plusieurs axes structurants.</p>

  <h3>Charte de la donnée et de l'IA de la Corse</h3>
  <p>La Charte de la donnée et de l'IA de la Corse est structurée en vingt-et-un principes répartis en neuf titres. Plusieurs principes sont particulièrement structurants pour Tellux et sont déjà intégrés à la conception de la plateforme.</p>
  <p>Le <strong>principe n°1, « données d'intérêt insulaire »</strong>, oriente la production de jeux de données spécifiquement territoriaux corses, en complément des référentiels nationaux : les classements radon par commune corse, les antennes ANFR de Corse, les couches géologiques BRGM 1/50 000 spécifiques à l'île, le réseau électrique EDF SEI insulaire.</p>
  <p>Le <strong>principe n°5, « hébergement souverain »</strong>, est l'objet d'une trajectoire annoncée : l'infrastructure actuelle (Cloudflare Pages pour le site, Supabase <em>eu-west-1</em> Irlande pour la base de contributions) est éligible à une migration vers un opérateur souverain européen pleinement soumis au droit européen, dont la temporalité est conditionnée au calendrier d'un éventuel financement.</p>
  <p>Les <strong>principes n°7 et n°8 sur la frugalité numérique</strong> se reflètent dans la stack technique : applications web sans framework lourd, polices auto-hébergées, pas de tracker tiers, pas de Google Fonts, datasets en formats compacts.</p>
  <p>Les <strong>principes n°15 et n°16 sur l'ouverture des algorithmes et la priorité open source</strong> sont déjà respectés : le code source intégral est publié sous licence MIT sur le <a href="https://github.com/dellahstella/tellux" target="_blank" rel="noopener">dépôt public du projet</a>, librement consultable, modifiable et réutilisable.</p>
  <p>Les <strong>principes n°17 et n°18 sur les biens communs numériques</strong> sont préfigurés par l'engagement de non-commercialisation et par la traçabilité publique des sources mobilisées.</p>

  <h3>Guide de bonne pratique IA Smart Isula</h3>
  <p>Le Guide de bonne pratique IA Smart Isula définit douze bonnes pratiques pour les systèmes d'apprentissage statistique mobilisés en contexte territorial. Tellux ne déploie aucun système d'IA à risque interdit au sens du Règlement IA UE 2024 : pas de notation sociale, pas d'identification biométrique, pas de police prédictive, pas de ciblage émotionnel.</p>
  <p>Un volet d'auto-affinage du modèle territorial par confrontation systématique entre mesures contributives et prédictions est étudié dans le cadre de la candidature FEDER. L'application des bonnes pratiques du Guide constituerait le cadre de mise en œuvre, conditionnel à l'obtention du financement.</p>
  <p>Plusieurs bonnes pratiques sont déjà préfigurées par les pratiques actuelles : la transparence des transformations effectuées sur les données (bonne pratique n°5) est garantie par la publication open source du code, la maîtrise des données et des algorithmes (bonne pratique n°10) est garantie par l'hébergement européen et par l'absence de dépendance à des services d'IA tiers, la documentation des biais (bonne pratique n°7) est ouverte par la position épistémique publique exposée dans le document <a href="/methode-et-limites.html">Méthode et limites</a>.</p>

  <h3>Articulation avec les pratiques actuelles</h3>
  <p>L'adhésion préfigurée aux cadres territoriaux n'est pas un engagement futur isolé : elle prolonge des pratiques déjà visibles sur le site. Le code source est sous licence MIT, librement consultable. Aucun cookie publicitaire, aucun traceur d'analyse tiers, aucune revente de données. Les polices d'écriture sont auto-hébergées sous Open Font License. La base de contributions citoyennes, opérationnelle, applique d'ores et déjà la sécurité au niveau des lignes (Row Level Security) et l'anonymisation systématique des contributions agrégées. La position épistémique du projet — refus symétrique de l'alarmisme et de la trivialisation, distinction des niveaux d'inférence, exclusion de tout diagnostic médical — est documentée publiquement dans la page <a href="/methode-et-limites.html">Méthode et limites</a> et constitue le socle éthique préalable à toute adhésion formelle.</p>
  <p>Le statut actuel des deux cadres est donc le suivant : <strong>adoption formelle envisagée dans le cadre du dossier de candidature FEDER en préparation, articulation préfigurée par les pratiques actuelles déjà visibles sur le site</strong>. Toute évolution sera tracée dans la présente page.</p>
</section>
```

---

## 3. Notes d'intégration pour le sprint Code 2

### Renumérotation cohérente
- Modifier `<h2>4. Architecture, code, licences</h2>` → `<h2>5. Architecture, code, licences</h2>`
- Modifier `<h2>5. Comment signaler une erreur ou une incohérence</h2>` → `<h2>6. Comment signaler une erreur ou une incohérence</h2>`
- Aucune ancre interne ne référence ces numéros (vérification : pas de `#section-4` ni `href="#4"` dans le fichier).

### Conformité aux règles strictes du prompt
- ✅ Mention explicite de la Charte (21 principes, 9 titres) avec principes structurants n°1, 5, 7-8, 15-16, 17-18 — exactement comme demandé.
- ✅ Mention explicite du Guide IA Smart Isula (12 bonnes pratiques) avec application au volet auto-affinage **conditionnelle au financement**.
- ✅ Articulation avec pratiques actuelles : MIT, pas de tracker, pas de revente, polices auto-hébergées, RLS — exactement comme demandé.
- ✅ Statut « adoption envisagée formellement dans le cadre du projet FEDER si financement obtenu, articulation préfigurée par les pratiques actuelles » — formulé tel quel dans le texte.
- ✅ Pas de mention publique des modules Phase 2/3/4.
- ✅ Pas de mention publique de l'auto-affinage **comme déjà existant** : reformulé comme « volet (...) étudié dans le cadre de la candidature FEDER ».
- ✅ Aucune des trois formulations proscrites employée.

### Cohérence avec le contenu existant de `transparence.html`
- La section 4 actuelle « Architecture, code, licences » (l.382-385) mentionne déjà la licence MIT, l'absence de tracker, les polices Open Font License auto-hébergées. La nouvelle section ne contredit pas ces mentions, elle en propose une lecture éthique structurée par les cadres Charte/Guide IA. Le sprint Code 2 peut juger pertinent de relire les deux sections en enchaînement et resserrer si redondance perçue. Recommandation : conserver la section Architecture en l'état (factuelle, technique) et garder la nouvelle comme cadrage éthique distinct.
- La section 2 « Sources et statuts épistémiques » (l.286-312) mentionne déjà l'ASNR, la Licence Ouverte Etalab, et les statuts épistémiques. Pas de redondance directe avec la nouvelle section.

### Vérification factuelle (Supabase eu-west-1 Irlande)
La formulation « Supabase eu-west-1 Irlande » est cohérente avec :
- `mentions-legales.html` l.298 : « base de données localisée dans la région eu-west-1 (Irlande, Union européenne) »
- `donnees-vie-privee.html` l.262 : « Stella Canis Majoris (...) responsable du traitement »
- `donnees-vie-privee.html` l.317 : « Aucun transfert des données de contribution hors de l'Union européenne n'est effectué par Supabase pour ce projet. »

La nuance ajoutée par la nouvelle section (« opérateur souverain européen pleinement soumis au droit européen ») reflète le fait que l'instance est en UE mais que l'éditeur Supabase Inc. est de droit étatsunien — distinction reprise du livrable 3 sur le dossier FEDER.
