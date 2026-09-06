# Fond gamma terrestre régional JRC — notes de source (couche C3)

**Statut : pipeline d'acquisition livré (phase 1). Intégration `app.html` DIFFÉRÉE** (fichier chaud, sessions concurrentes ; revue anti-fuite Web avant mise en ligne).

## Source

- **Jeu** : JRC *European Atlas of Natural Radiation* (EANR) — « 07. Terrestrial gamma dose ».
- **Dataset ID** : `jrc-eanr-07_terrestrial-gamma-dose` · **DOI** : [10.2905/JRC.SBESAC0](https://doi.org/10.2905/JRC.SBESAC0) · PID `http://data.europa.eu/89h/jrc-eanr-07_terrestrial-gamma-dose`.
- **Fichier** : `tgdrngyh.zip` (ESRI ArcInfo Binary Grid). Unité **nGy/h** (encodée dans le nom : *terrestrial gamma dose rate, nGy/h*).
- **URL de téléchargement** (⚠ **HTTPS obligatoire** — l'HTTP renvoie 500) :
  `https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/EANR/Terrestialgammadose/tgdrngyh.zip`
  (noter la coquille JRC « Terrestialgammadose » dans le chemin).
- **Portail carto** : https://remon.jrc.ec.europa.eu/ (Digital Atlas → Terrestrial gamma).

## Licence & attribution (à afficher dans l'UI)

- **Licence** : **Creative Commons Attribution 4.0 International (CC BY 4.0)** — confirmée par le `copyright.txt` du dossier JRC (« Any copyright and/or sui generis right on the dataset is licensed under CC BY 4.0 »).
- **Attribution UI** :
  > © European Union, JRC — *European Atlas of Natural Radiation* (Tollefsen, De Cort, Cinelli, Gruber, Bossew). Licence CC BY 4.0.
- **Méthode** : Bossew et al. 2016, DOI [10.1016/j.jenvrad.2016.02.013](https://doi.org/10.1016/j.jenvrad.2016.02.013).

## Spécifications techniques

- **Grille** : 10 km × 10 km.
- **CRS natif** : LAEA ETRS89 **custom** — WKT `ETRS_1989_LAEA_L48_M09` : centre **lat 48°N / lon 9°E**, false E/N = 0, ellipsoïde GRS80. **CE N'EST PAS EPSG:3035** (centre 52/10, FE 4321000) — le fichier ADF ne porte pas son CRS, proj4 exact utilisé dans le script :
  `+proj=laea +lat_0=48 +lon_0=9 +x_0=0 +y_0=0 +ellps=GRS80 +units=m +no_defs`.
- **nodata** : −3.4e38 (float32) — retire mer / hors-socle.
- **Formule source** (metadata.xml) : `TGDR = K2Osoil·0,83·12,91449 + Usoil·5,7057 + Thsoil·2,459488` (contribution K/U/Th du sol).

## Sortie produite

- **Fichier** : `public/data/gamma_jrc_corse.geojson` (~20 Ko, CRS84).
- **Fenêtre Corse** : bbox lon 8,40–9,66 / lat 41,30–43,10 ; cellules 10 km reprojetées WGS84.
- **Résultat** : **88 cellules**, `tgdr_ngyh` **min 60,4 · médiane 84,2 · max 108,8 nGy/h**.
  Cohérence physique : Corse très granitique → au-dessus de la moyenne mondiale (~59 nGy/h), dans la fourchette granitique typique (70–200). Aucune valeur fabriquée : lecture directe de la grille JRC.
- **Propriétés par cellule** : `tgdr_ngyh` (valeur), `classe_indicative` (1–4, repère de lecture visuel — **pas un seuil**).

## Garde-fous (impératifs à l'intégration)

- **NCRP-001 GELÉ** : couche de **contexte affichée uniquement**, **hors** de tout modèle de calibration / dose Tellux. Ne pas la brancher dans `calcAll` ni dans l'indice composite.
- **Indicatif ≠ métrologique** (garde-fous A.4) : 10 km, grandeur = débit de dose absorbée **dans l'air** (nGy/h). **Jamais de lecture sanitaire.**
- **Piège d'unités** : Téléray/ASNR affiche du **nSv/h** (H\*(10)) ; JRC/Euratom assimilent ≈ 1, mais **afficher la grandeur explicitement** (nGy/h) dans la légende.
- **Repères de lecture** (légende, pas des seuils) : ~59 nGy/h (moyenne mondiale UNSCEAR) · 70–200 nGy/h (terrains granitiques).
- **Échelle** : pas de barème concurrent. Rendu séquentiel type contexte ; réserver le vocabulaire de seuil aux couches qui en ont un.
- **Reproductibilité** : `uv run --with rasterio python scripts/build_gamma_jrc_geojson.py` (cache brut sous `scripts/.cache/gamma_jrc/`, gitignored).

## Reste à faire (phase 2 — intégration, quand `app.html` refroidit)

1. Ajouter la couche `gamma` (contexte / domaine ionisant) dans `app.html` : `L.geoJSON` sur `gamma_jrc_corse.geojson`, échelle séquentielle, popup sourcé + attribution CC BY 4.0, légende avec grandeur (nGy/h) et repères de lecture.
2. Emplacement UI prévu : sous-groupe « contexte » du domaine Ionisant (à côté du radon), **hors** couches qui modulent le calcul.
3. Option polish : clip des cellules au trait de côte Corse (communes geojson) pour retirer le léger débord maritime / nord-Sardaigne de la bbox.
4. **C2 (bundle même PR)** : ajouter le libellé « Licence Ouverte Etalab 2.0 » à l'attribution de la couche antennes ANFR + note de fraîcheur du snapshot Supabase.
5. Revue anti-fuite Web avant mise en ligne (comme #924/#925).
