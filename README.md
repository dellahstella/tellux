# Tellux

Cartographie électromagnétique territoriale de la Corse.

**Application en ligne : [tellux.pages.dev](https://tellux.pages.dev)**

---

## Présentation

Tellux est un outil de cartographie et de visualisation des champs électromagnétiques en Corse. Il couvre quatre domaines physiques distincts :

- **Magnétique statique** — géomagnétisme IGRF-14, anomalies crustales EMAG2v3, cross-check WMM 2025
- **Magnétique basse fréquence (ELF)** — lignes HTA/HTB modélisées par Biot-Savart, postes sources, éoliennes
- **Radiofréquences** — antennes ANFR, émetteurs TDF
- **Ionisant** — composante cosmique altitudinale, classification radon officielle

L'application propose un **mode Expertise** paramétrable (indice composite avec pondérations explicites, avertissement épistémique permanent), un **système de contributions terrain** (mesures utilisateur), un **export CSV** public et enrichi, et le **partage par URL**.

Tellux distingue rigoureusement ce qui est mesuré, ce qui est modélisé, et ce qui reste à l'état d'hypothèse. Le champ électromagnétique est un champ physique unique, soumis au principe de superposition.

## Ce que Tellux n'est pas

- Un outil de diagnostic médical
- Un substitut à des mesures professionnelles certifiées
- Un système de prédiction ou d'alerte
- Un outil de géobiologie ésotérique

## Sources de données

Sources publiques intégrées :

- **Géomagnétisme** : IGRF-14 (BGS/NOAA), EMAG2v3 (NOAA), WMM 2025
- **Antennes RF** : CartoRadio (ANFR)
- **Géologie** : BRGM Infoterre
- **Altitude** : IGN RGE Alti
- **Couvert forestier** : Forêts publiques ONF (Géoplateforme IGN)
- **Réseaux électriques (fallback)** : OSM Overpass
- **Radon** : classification officielle en vigueur

Des démarches sont en cours pour l'accès à d'autres données institutionnelles (réseaux publics nationaux français) afin d'enrichir les modèles en magnétique basse fréquence, en rayonnement ionisant et en radiométrie aérienne. Voir [`DETTES_TECHNIQUES.md`](DETTES_TECHNIQUES.md) pour les chantiers ouverts.

[`ROADMAP.md`](ROADMAP.md) présente la trajectoire générale du projet.

## Architecture

Tellux est aujourd'hui structuré autour d'une application principale publique :

- `index.html` — landing publique
- `app.html` — application cartographie EM (publique, mise en avant), avec sélecteur de domaines physiques (chips de filtre Tous / Statique / ELF / RF / Ionisant) et badges temps réel dans le panneau Conditions (Kp, Réseau, Live Supabase, Orage)
- `mairies.html` — outils communaux (fiche commune, modèles de courriers, cadre légal)
- `cadre-scientifique.html` — démarche scientifique (architecture du modèle, formules, pondérations, et documentation méthodologique par domaine physique : magnétique statique, magnétique basse fréquence ELF 50 Hz, radiofréquences, rayonnement ionisant)
- `methode-et-limites.html` — méthode et limites (position épistémique, vocabulaire, pièges rhétoriques)
- `guide-utilisation.html` — guide d'utilisation (manuel d'usage de la carte et des contributions)
- `glossaire.html` — glossaire technique du projet (94 entrées alphabétiques couvrant physique des champs EM, méthodologie, terminologie institutionnelle et juridique, vocabulaire technique projet)
- `transparence.html` — page de transparence éditoriale (sources, statuts épistémiques, limites connues, cadres éthiques)
- `retractations.html` — journal public des retraits et reformulations substantielles

Des modules d'extension thématiques pourront être envisagés sous condition d'obtention d'un financement public, sans calendrier public à ce stade.

## Stack technique

- HTML / JavaScript / Leaflet (frontend)
- Supabase (PostgreSQL + RLS) pour les contributions terrain
- Cloudflare Workers pour l'hébergement
- Pas de dépendance serveur côté application (single-page HTML)

## Position épistémique

Tellux adopte une posture de précaution épistémique : documenter sans surattribuer. L'incertitude est traitée comme une donnée, rendue visible par des indicateurs de confiance (●●● / ●●○ / ●○○) et par le symbole ◆ pour les paramètres en attente de validation méthodologique externe.

Les corrélations entre champs électromagnétiques et phénomènes biologiques ou archéologiques constituent un champ de recherche actif. Les hypothèses exploratoires sont distinguées des données mesurées.

## Contribution

Les mesures terrain peuvent être soumises directement via l'interface (bouton « + Mesure »). Retours d'usage, propositions d'étude et partenariats institutionnels bienvenus via l'email ci-dessous.

## Licence

Voir [`LICENSE`](LICENSE).

## Porteur

**Lucas IANNACCONE**, à Bastia.

Le projet est développé en autonomie, sans mandat ni partenariat institutionnel à la date de publication de cette page. Les démarches d'accès à certaines données institutionnelles (réseaux publics nationaux français) sont en cours.

Contact : [stelladluca@proton.me](mailto:stelladluca@proton.me)

---

## Documentation publique

- [`ROADMAP.md`](ROADMAP.md) — feuille de route, phases de développement, principes de pilotage
- [`DETTES_TECHNIQUES.md`](DETTES_TECHNIQUES.md) — dettes techniques ouvertes et fermées récemment
- [`LICENSE`](LICENSE) — licence du projet

Application : [tellux.pages.dev](https://tellux.pages.dev)
