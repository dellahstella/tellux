# TELLUX — Kit d'envoi associations EM

**Date :** 9 avril 2026 · **Mise à jour :** 13 avril 2026 (session 6 — cohérence épistémique)
**Contenu :** Email de contact (2 variantes) + fiche de présentation 1 page + guide d'utilisation 4 étapes.

---

## A. Email de contact

### Variante 1 — Association nationale (PRIARTEM, Robin des Toits, CRIIREM)

```
Objet : Tellux — carte interactive open-source des CEM en Corse, accès gratuit

Bonjour,

Tellux est une plateforme cartographique gratuite qui permet de visualiser
les 974 antennes ANFR de Corse, les lignes haute tension EDF SEI, et les
anomalies géomagnétiques — le tout sur une carte interactive avec un
double indice (perturbation réseau / activité géologique) documenté et
ses limites publiées.

L'outil est open-source (MIT), sans publicité, sans revente de données.
Les habitants peuvent y ajouter leurs propres mesures terrain selon un
protocole en aveugle parallèle intégré à l'interface.

Je cherche d'abord un retour critique de la part d'une association
reconnue dans le domaine CEM. Un test de 15 minutes sur votre
territoire suffit pour évaluer si l'outil est utile.
Un mode d'emploi court est joint.

Accès : https://tellux.pages.dev

Lucas IANNACCONE · Projet Tellux · Bastia
stelladluca@proton.me · 06 18 04 25 44
```

### Variante 2 — Association locale Corse (collectif citoyen, association riverains antenne)

```
Objet : Tellux — visualiser les antennes et les lignes HT de votre commune

Bonjour,

Je suis basé à Bastia et je développe Tellux, une carte interactive
gratuite qui affiche les antennes ANFR et les lignes haute tension autour
de chez vous, avec un indice de perturbation EM et ses incertitudes.

L'outil est open-source, sans publicité, et permet aux habitants d'ajouter
leurs propres mesures terrain. Je cherche des associations locales pour
tester la carte sur un secteur que vous connaissez bien et me faire un
retour.

Si votre association organise des réunions publiques ou des ateliers de
mesures, la carte peut être projetée et utilisée en direct.

Accès : https://tellux.pages.dev
Mode d'emploi joint.

Lucas IANNACCONE · Bastia
stelladluca@proton.me · 06 18 04 25 44
```

---

## B. Fiche de présentation — 1 page

---

**TELLUX CORSE — Carte interactive des champs électromagnétiques**

**Qu'est-ce que Tellux ?**

Un tableau de bord web gratuit et open-source qui affiche sur une carte de la Corse : les 974 antennes ANFR avec type et opérateur, les lignes haute tension EDF SEI avec estimation du champ magnétique (Biot-Savart), les anomalies géomagnétiques naturelles (IGRF-14, EMAG2v3 NOAA), les failles tectoniques (BRGM), et les mesures terrain ajoutées par les habitants.

**Comment ça marche ?**

Cliquez n'importe où sur la carte. Tellux calcule deux indices séparés : un score de perturbation réseau (antennes, lignes, courants) et un score d'activité géologique (substrat, anomalies crustales). Ces indices identifient les sources séparément. Les indices ne se somment pas arithmétiquement, mais les champs physiques sous-jacents s'additionnent bien vectoriellement — un lieu où les deux indices sont élevés est un lieu où le champ total résulte de contributions multiples.

**Sur quoi c'est fondé ?**

Le modèle utilise des données institutionnelles vérifiables (ANFR, NOAA, BRGM, IGRF-14). Le corpus scientifique comprend 85 études intégrables au modèle, publiées dans des revues à comité de lecture. Parmi les plus récentes : Baydiili 2025 (impact HTA sur microbiome sol), Hermans 2023 (mycorhizes et lignes HTB), Favre 2011 (abeilles et RF).

**Les 3 limites que nous assumons**

1. **Le modèle est un comparatif relatif, pas un diagnostic absolu.** Le score d'un point n'a de sens que comparé à un autre point. Tellux ne permet pas de conclure qu'un lieu est « dangereux » ou « sain ».

2. **Les courants HTA sont estimés, pas mesurés.** EDF SEI ne publie pas les courants en temps réel. L'incertitude est de ±50 %. Un relevé terrain peut diverger du modèle.

3. **La base de mesures terrain est embryonnaire.** 29 mesures ANFR certifiées sur toute la Corse, zéro mesure citoyenne à ce jour. C'est pour cela que le crowdsourcing est essentiel.

**Ce que Tellux ne fait pas**

Tellux ne fait aucune promesse de santé, ne propose aucun diagnostic médical, et ne commercialise aucune solution de protection. C'est un outil de transparence et d'aide à la conversation citoyenne.

**Accès :** https://tellux.pages.dev — Code : MIT — Contact : stelladluca@proton.me

---

## C. Guide d'utilisation — 4 étapes pour les associations EM

### Étape 1 — Visualiser les antennes ANFR autour de chez soi

Ouvrez https://tellux.pages.dev. Dans le panneau latéral gauche, section « Énergies humaines », cliquez sur **Antennes ANFR**. Les 974 antennes de Corse apparaissent sur la carte. Cliquez sur une antenne pour voir son type (4G, 5G, FM…), son opérateur, et sa localisation. Zoomez sur votre commune. Activez aussi **Réseau HT** pour voir les lignes haute tension.

### Étape 2 — Lire le double indice Tellux

Cliquez n'importe où sur la carte (hors antenne ou site). Le popup « Diagnostic modèle » apparaît avec deux scores :

- **Perturbation réseau** (0–5) : estime l'exposition aux sources industrielles (antennes, lignes HT). Plus le score est élevé, plus les sources sont proches et puissantes.
- **Activité géologique** (0–5) : mesure l'intensité des phénomènes géophysiques locaux (anomalie magnétique crustale, substrat piézoélectrique, proximité de faille). Ce n'est pas une mesure de danger — c'est une signature géologique.

Ces deux indices identifient les sources. Le champ physique en un point est la résultante de toutes les contributions. Un score réseau de 4 et un score géologique de 1 signifie : contribution dominante des réseaux, faible activité géologique locale.

### Étape 3 — Ajouter une mesure terrain

Dans le panneau latéral, section « Outils terrain », cliquez sur **Ajouter mesure**. Un marqueur violet apparaît sur la carte. Cliquez à l'endroit où vous avez effectué votre mesure. Le formulaire s'ouvre : renseignez le type de mesure (magnétomètre nT, signal RF dBm, WiFi, ELF), la valeur mesurée, et éventuellement l'appareil utilisé. La mesure est anonyme et versée à la base commune.

Pour les mesures en aveugle parallèle : deux opérateurs mesurent le même point indépendamment. Les résultats sont comparés a posteriori. C'est le protocole recommandé par Tellux.

### Étape 4 — Partager une vue de la carte

Pour partager la carte centrée sur une zone précise, copiez simplement l'URL de votre navigateur (elle contient les coordonnées et le zoom). Vous pouvez aussi faire une capture d'écran pour une réunion publique ou un document.

Pour un export PDF du diagnostic d'une parcelle (module agronomie), cliquez sur « Exporter rapport » dans le panneau de diagnostic.

---

*Kit produit le 9 avril 2026. À adapter selon les retours des premières prises de contact.*
