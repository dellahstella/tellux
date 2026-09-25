# Tellux

Cartographie électromagnétique territoriale de la Corse.

**Application en ligne : [tellux.pages.dev](https://tellux.pages.dev)**

---

## Présentation

Tellux est un outil de cartographie et de visualisation des champs électromagnétiques en Corse. Il couvre quatre domaines physiques distincts :

- **Magnétique statique** — géomagnétisme IGRF-14, anomalies crustales EMAG2v3, variation diurne Sq et correction externe (observatoires INTERMAGNET ; en repli, indice Dst via la NOAA, puis indice Kp)
- **Magnétique basse fréquence (ELF)** — modélisés : lignes HTA aériennes (loi de Biot-Savart), réseau basse tension (forfait par paliers selon la densité de segments BT à proximité), sources ponctuelles (sites de production et d'interconnexion, postes sources, parcs éoliens) ; non modélisés : lignes HTB, réseau HTA souterrain, postes de distribution HTA/BT, installations solaires
- **Radiofréquences** — modélisés, avec un facteur d'échelle unique issu d'une calibration interne sur des mesures certifiées prises en extérieur (estimation centrale) : antennes de téléphonie mobile déclarées à l'ANFR (socle partiel : quasi complet en Corse-du-Sud, environ la moitié en Haute-Corse), émetteurs de télévision TDF (liste partielle, puissances estimées), faisceaux hertziens (positions estimées d'après la topographie) ; non modélisée : radio FM ; affichés en présence seule, hors calcul : supports FM/TV, PMR et faisceaux hertziens déclarés à l'ANFR
- **Ionisant** — calculée mais non affichée sur la carte EM : dose gamma ambiante (composante cosmique selon l'altitude, composante terrestre selon la roche) ; présentés sur `radon.html` : zonage réglementaire du potentiel radon de l'ASNR (arrêté du 27 juin 2018), fond gamma terrestre du JRC

L'application affiche, au clic sur la carte, un **Indice Tellux** (perturbation humaine, score comparatif indicatif de 0 à 5). Elle propose un **système de contributions terrain** (mesures utilisateur), le **téléchargement en JSON des mesures certifiées** affichées sur la carte et le **partage par URL**. `mairies.html` permet d'exporter en CSV les listes d'antennes et d'établissements sensibles d'une commune. L'ancien mode Expertise (indice composite pondéré, export CSV) n'est plus accessible dans l'interface.

Tellux distingue rigoureusement ce qui est mesuré, ce qui est modélisé, et ce qui reste à l'état d'hypothèse. Le champ électromagnétique est un champ physique unique, soumis au principe de superposition.

## Ce que Tellux n'est pas

- Un outil de diagnostic médical
- Un substitut à des mesures professionnelles certifiées
- Un système de prédiction ou d'alerte
- Un outil de géobiologie ésotérique

## Sources de données

Sources publiques intégrées :

- **Géomagnétisme** : IGRF-14 (BGS/NOAA), EMAG2v3 (NOAA), observatoires INTERMAGNET (via le BGS), NOAA SWPC (indice Kp, flux de protons, indice Dst du WDC de Kyoto)
- **Réseau électrique** : EDF SEI open data (lignes HTA, réseau BT), RTE ODRE (parcs éoliens), OpenStreetMap (postes sources ; tracés des lignes HTA et HTB affichés en secours, hors calcul, si Supabase est indisponible)
- **Radiofréquences** : ANFR (antennes mobiles ; supports FM/TV, PMR et faisceaux hertziens), TDF, l'Arcom et le forum TVNT.net (émetteurs de télévision, liste partielle, puissances estimées), mesures certifiées publiées par l'ANFR sur CartoRadio
- **Géologie** : BRGM (carte géologique au 1/50 000, parmi les sources de la susceptibilité magnétique du substrat affichée au clic ; géologie, cavités et failles sur `radon.html`)
- **Altitude** : IGN RGE Alti (Géoplateforme)
- **Couvert forestier** : BD Forêt V2 (IGN), couche « Forêt dense » (une fois activée, elle atténue par la végétation la valeur radiofréquence du point cliqué, sans modifier la carte de chaleur ni l'Indice Tellux)
- **Radon et rayonnement gamma** : zonage réglementaire du potentiel radon de l'ASNR (arrêté du 27 juin 2018), fond gamma terrestre du JRC
- **Qualité de l'air** : Qualitair Corse (particules fines PM2,5, moyenne annuelle modélisée 2024, sur `radon.html`)
- **Établissements sensibles** : annuaire de l'Éducation nationale, FINESS (DREES) et OpenStreetMap pour la petite enfance (sur `mairies.html`)
- **Météo** : Open-Meteo (conditions courantes, probabilité d'orage)
- **Adresses** : Base Adresse Nationale

Des démarches sont en cours pour l'accès à d'autres données institutionnelles (réseaux publics nationaux français) afin d'enrichir les modèles en magnétique basse fréquence, en rayonnement ionisant et en radiométrie aérienne.

[`ROADMAP.md`](ROADMAP.md) présente la trajectoire générale du projet.

## Architecture

Tellux est aujourd'hui structuré autour de plusieurs applications publiques et d'une documentation partagée :

- `index.html` — landing publique
- `app.html` — application cartographie EM (publique, mise en avant), avec un filtre par domaine physique (Tous / Statique / ELF / RF), qui masque dans la liste les couches des autres domaines sans éteindre celles déjà affichées, et des badges temps réel dans le panneau Conditions (Kp, Live, Orage, Contribs)
- `patrimoine.html` — seconde application : patrimoine corse cartographié et documenté (publique, bêta, distincte de la couche EM)
- `radon.html` — troisième application : potentiel radon (publique, distincte de la couche EM)
- `mairies.html` — outils communaux (fiche commune, modèles de courriers, cadre légal)
- `cadre-scientifique.html` — démarche scientifique (architecture du modèle, formules, pondérations, et documentation méthodologique par domaine physique : magnétique statique, magnétique basse fréquence ELF 50 Hz, radiofréquences, rayonnement ionisant)
- `methode-limites-transparence.html` — méthode, limites et transparence (incertitudes, limites du modèle, sources de données, statuts épistémiques des couches, dettes techniques, signalement d'erreurs) ; les anciennes pages `methode-et-limites.html`, `transparence.html` et `demarche-synthese.html` y redirigent en 301, et `retractations.html` vers sa section « Signaler une erreur »
- `geomagnetisme.html` — page de culture scientifique : globe géomagnétique historique interactif (−8000 → 2025, reconstruction CALS10k.2 / IGRF-14, données embarquées), registre distinct de la couche cartographique EM
- `mentions-legales.html` — mentions légales et confidentialité

Des modules d'extension thématiques pourront être envisagés sous condition d'obtention d'un financement public, sans calendrier public à ce stade.

## Stack technique

- HTML / JavaScript / Leaflet (frontend)
- Supabase (PostgreSQL + RLS) pour les contributions terrain et une partie des données lues par les pages, dont les antennes ANFR et les lignes HTA de la carte EM, le réseau BT (contrôle de fraîcheur, et chargement complet en repli de l'agrégat statique) et les dépôts de mesurage radon publiés sur `radon.html`
- Cloudflare Pages pour l'hébergement
- Pages statiques, sans fonction serveur propre. Au chargement, la carte interroge Supabase, la NOAA (SWPC) et Open-Meteo, et charge Leaflet et son extension de regroupement de marqueurs (cdnjs) ainsi que son fond de carte (Esri) ; selon l'usage, elle appelle aussi la Base Adresse Nationale, l'altimétrie et le fond Plan IGN de la Géoplateforme, la NOAA (EMAG2v3) et OpenStreetMap (secours).
- Des tâches planifiées GitHub Actions rafraîchissent des fichiers de données servis avec les pages (observatoires INTERMAGNET, antennes par commune, agrégat du réseau BT).

## Position épistémique

Tellux adopte une posture de précaution épistémique : documenter sans surattribuer. L'incertitude est traitée comme une donnée : dans la fiche d'un point de la carte, un indicateur de confiance par domaine la rend visible (●●○ pour le magnétique statique et l'ELF, ●○○ pour les radiofréquences).

Les corrélations entre champs électromagnétiques et phénomènes biologiques ou archéologiques constituent un champ de recherche actif. Les hypothèses exploratoires sont distinguées des données mesurées.

## Contribution

Les mesures terrain peuvent être soumises directement via l'interface (bouton rond « + » en bas à droite de la carte, info-bulle « Contribuer une mesure »). Retours d'usage, propositions d'étude et partenariats institutionnels bienvenus via l'email ci-dessous.

## Licence

Voir [`LICENSE`](LICENSE).

## Porteur

**Porteur du projet Tellux**, à Bastia.

Le projet est développé en autonomie, sans mandat ni partenariat institutionnel à la date de publication de cette page. Les démarches d'accès à certaines données institutionnelles (réseaux publics nationaux français) sont en cours.

Contact : [tellux.veille@gmail.com](mailto:tellux.veille@gmail.com)

---

## Documentation publique

- [`ROADMAP.md`](ROADMAP.md) — feuille de route, phases de développement, principes de pilotage
- [`LICENSE`](LICENSE) — licence du projet

Application : [tellux.pages.dev](https://tellux.pages.dev)
