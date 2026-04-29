# Sites U/Th à mesurer — note méthodologique

**Fichier :** `public/data/points_chauds_radio_corse.json`
**Date d'extraction :** 2026-04-23 (version 3.0 refonte)
**Remplace :** version du 2026-04-21 (5 entrées avec doses estimées, Argentella inclus) désormais obsolète
**Source :** consolidation Cowork basée sur `_corpus/tellux_note_uranium_thorium_corse_v1.md` (version 1.0 du 23 avril 2026)
**Statut :** données **documentaires**, **non mesurées par Tellux**, **non utilisées pour moduler `calcGammaAmbient`** en l'état

---

## 1. Changement de positionnement (refonte 2026-04-23)

La version précédente de ce dataset (2026-04-21, 5 entrées) proposait des doses gamma estimées par analogie géochimique pour chaque site et alimentait `calcGammaAmbient` via un boost ponctuel. Cette approche posait trois problèmes :

1. **Aucune valeur analytique de dose gamma propre à ces sites n'est documentée dans la littérature accessible.** Les ordres de grandeur étaient inférés par analogie avec des sites voisins ou des contextes géologiques comparables, sans mesure radiométrique in situ publiée. Présenter ces valeurs comme « ordres de grandeur documentaires » créait une illusion de précision qui n'était pas soutenable face à une relecture critique.

2. **L'entrée Argentella reposait sur une erreur factuelle.** La galerie minière d'Argentella a été creusée pour extraire la galène argentifère (plomb argentifère), pas de l'uranium. L'épisode nucléaire de 1960 (projet avorté d'essai nucléaire souterrain) a fixé dans la mémoire collective une association Argentella/nucléaire qui n'est pas fondée sur une minéralisation uranifère. Argentella est donc retirée du dataset U/Th ; elle figure dans la couche `sites_remarquables_corse.json` (catégorie minier historique) pour sa valeur mémorielle documentée.

3. **L'intégration dans `calcGammaAmbient` ajoutait un biais de surdétection** dans des zones non mesurées, au risque de suggérer une anomalie là où il n'y a qu'une présomption géologique.

La refonte opère trois décisions :

- **Toutes les entrées ont `dose_gamma_estimee_nSv_h: null`.** Aucune dose n'est inférée.
- **Le positionnement assumé est « catalogue de sites à mesurer »**, non « carte d'anomalies mesurées ». Chaque entrée a un champ `statut: "mesure_requise"`.
- **Une garde défensive est ajoutée dans `calcGammaAmbient`** pour ignorer les entrées dont la dose est `null` (pas de boost ponctuel, pas d'altération de la composante cosmique+terrestre de la fonction). La fonction reste inchangée en l'absence de dose mesurée.

---

## 2. Écart entre nom technique et label UI

Le fichier JSON conserve le nom historique `points_chauds_radio_corse.json`, cohérent avec les identifiants techniques `POINTS_CHAUDS_RADIO`, `togPointsChauds`, `loadPointsChaudsRadio` présents dans `app.html`. Le label UI affiché à l'utilisateur est en revanche **« Sites U/Th à mesurer »**, plus représentatif du positionnement réel.

Cet écart volontaire entre nom technique (conservé pour l'historique et la non-régression) et label UI (refonte) est documenté ici pour éviter toute confusion en session ultérieure. Ne pas renommer le fichier JSON sans décision projet explicite.

---

## 3. Les 8 entrées retenues

Le dataset contient 8 sites, regroupés en deux familles :

**Famille 1 — Sables monazitiques (5 entrées)**

| ID | Nom | Commune | Coord. | Rayon (m) |
|----|-----|---------|--------|-----------|
| `SALECCIA` | Plage de Saleccia | Santo-Pietro-di-Tenda | 42.762 N, 9.179 E | 600 |
| `LOTU` | Plage du Lotu | Santo-Pietro-di-Tenda | 42.749 N, 9.163 E | 500 |
| `OSTRICONI` | Plage d'Ostriconi | Palasca | 42.700 N, 9.237 E | 500 |
| `PORTO_FANGO` | Sables Porto-Crovani (embouchure Fango) | Galéria | 42.420 N, 8.858 E | 800 |
| `VALINCO_SABLES` | Sables golfe de Valinco (embouchures Rizzanese et Baracci) | Propriano | 41.683 N, 8.897 E | 800 |

Mécanisme : érosion différentielle de granites hercyniens leucocrates, accumulation sédimentaire de monazite [(Ce,La,Th)PO4]. Aucune mesure radiométrique in situ publiée pour ces sites. Analogie géologique avec les sables noirs de Camargue (IRSN 2002, rapport IRSN/DEI/SESURE 2002-15) et les placers monazitiques méditerranéens documentés.

**Famille 2 — Indices hydrothermaux et lithologies U/Th élevées (3 entrées)**

| ID | Nom | Commune | Coord. | Rayon (m) |
|----|-----|---------|--------|-----------|
| `CORTENAIS_VENACO` | Indices U hydrothermaux — Cortenais et Venaco | (secteur) | — | — |
| `BALAGNE_GIUSSANI` | Indices U — Balagne intérieure (Giussani) | (secteur) | — | — |
| `VIZZAVONA_GHISONI` | Leucogranites Monte d'Oro — zone fond gamma élevé | (secteur) | — | — |

Mécanisme : minéralisations hydrothermales tardi-hercyniennes (autunite, torbernite) ou fond géochimique élevé sur leucogranites à deux micas. Indices reportés dans les campagnes BRGM 1958-1973 et l'inventaire minier national, sans exploitation industrielle. Aucune mesure gamma surfacique publiée au 2026-04-23.

(Les coordonnées précises et rayons d'influence de la famille 2 sont en cours d'affinement.)

---

## 4. Exclusions motivées

Quatre exclusions sont explicitement appliquées par rapport à la version antérieure du dataset :

- **Argentella** (Calenzana, 2B) : galène argentifère, pas d'uranium. Mémoire nucléaire 1960 distincte de la minéralisation réelle. Déplacée dans `sites_remarquables_corse.json` catégorie minier historique.
- **Nonza, Albu, Farinole** (Cap Corse) : ophiolites (serpentinites, magnétite, chromite). Signature EM dominée par le magnétisme (magnétite ferrimagnétique) et la géochimie Ni/Cr/Fe, non par U/Th. Traitées dans `sites_remarquables_corse.json` catégorie ophiolite.
- **Murato** (2B) : serpentines amiantifères. U/Th naturels faibles. Hors périmètre Tellux (l'amiante ne relève pas du modèle EM).
- **Cap Corse Est** (Luri, Meria) : ophiolites, mêmes motifs d'exclusion que Nonza/Albu/Farinole. Entrée « Plages Est du Cap Corse » de la version précédente retirée du dataset U/Th ; sites miniers historiques correspondants (Luri, Meria, Ersa, Morsiglia) intégrés à `sites_remarquables_corse.json`.

---

## 5. Intégration dans `calcGammaAmbient`

**Comportement actuel (2026-04-23) :** neutralisation complète du boost ponctuel.

La fonction `calcGammaAmbient(lat, lon, altitude_m)` ne consomme plus ce dataset pour moduler sa valeur de retour. La composante cosmique altimétrique (IGN RGE Alti) et la composante terrestre (provisoirement gelée sous NCRP-001) restent les seules contributions actives.

Une garde défensive est ajoutée : les entrées dont `dose_gamma_estimee_nSv_h === null` sont ignorées par toute boucle de sommation de boost ponctuel. Cette garde est documentée dans le corps de `calcGammaAmbient` par un commentaire explicite.

**Réactivation future.** Le boost ponctuel sera réactivable entrée par entrée dès que des mesures certifiées (ASNR, laboratoire agréé, spectromètre gamma portable calibré) remplaceront les `null` par des valeurs analytiques. Chaque substitution doit s'accompagner d'une entrée dans `docs/data-sources/` signalant la source primaire, la date, l'instrument.

---

## 6. Statut vs mesures certifiées

Le champ `statut: "mesure_requise"` qualifie l'état documentaire actuel. Deux statuts sont prévus au schéma, pour transition progressive :

- `mesure_requise` : aucune mesure in situ publiée, analogie géologique uniquement. Dose null.
- `mesure_preliminaire` : mesure terrain non certifiée (contribution utilisateur ou prospection exploratoire) disponible. Dose renseignée, confidence `low`.
- `mesure_certifiee` : mesure ASNR ou laboratoire agréé. Dose renseignée, confidence `high`, intégration possible dans `calcGammaAmbient`.

Aucune entrée n'est actuellement au statut `mesure_certifiee`.

---

## 7. Matériau source détaillé

Pour l'intégralité du contexte géologique, historique (campagnes BRGM 1958-1973, épisode Argentella 1960, sables monazitiques, distinction ophiolite/granite), voir :

`_corpus/tellux_note_uranium_thorium_corse_v1.md` (version 1.0, 2026-04-23)

Cette note est dans le corpus interne privé. Les éléments qui sortent dans les productions publiques (landing, dossier CTC, documentation éditoriale publique) sont des synthèses dérivées, jamais l'exposition brute.

---

## 8. Licence

Données publiques BRGM et littérature géochimique. Usage pédagogique Tellux sous licence du projet. Consolidation et qualification Cowork 2026-04-23.

---

## 9. Mise à jour et calibration — conditions

Le dataset évoluera :

1. **Mesures terrain Tellux ou partenaire.** Campagne gamma ambiante avec spectromètre portable calibré sur les 8 sites, substituant les `null` par des valeurs analytiques site par site.
2. **Accès Téléray ASNR.** API en attente d'autorisation (lettre 01 ASNR du 2026-04-14). Fournira une baseline régionale mesurée, calibrant l'hypothèse de fond naturel corse granitique.
3. **Radiométrie aérienne BRGM.** Dossier `RADIO-AERO-001` (voir `DETTES_TECHNIQUES.md`). Cartes U/Th/K aéroportées à 1:250 000 donneraient la couverture totale avec mesures réelles.

À chaque mise à jour, incrémenter `version` et `date_maj` dans le JSON, et mettre à jour le présent fichier.

---

*Fin du document. Remplace la version 2026-04-21 (5 entrées, Argentella inclus, doses estimées) désormais obsolète.*
