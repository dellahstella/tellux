# Tellux — Session Opus du 14 avril 2026

**Durée :** session longue (environ 5-6 heures d'échange)
**Modèle :** Claude Opus 4.6
**Contexte entrant :** suite directe du post-mortem du 13 avril (session Git + tentative ratée de fix bouton CSV Phyphox). Objectif : rendre l'app présentable pour envoi associations EM.

---

## Résumé exécutif

Session mixte **corrections techniques + nettoyage fichiers projet + audit GPS massif**. 49 sites géographiques corrigés via double audit web (mégalithiques puis non-mégalithiques), refactor de plusieurs bugs UX, câblage du fetch externe `SITES_REFERENCE.json` avec fallback inline, pose de deux nouvelles règles de conduite opposables, et préparation d'un prompt Cowork pour l'audit A-4b lancé en fin de session.

Le principal point de friction a été la régression silencieuse d'un fichier HTML en début de session (j'ai copié une ancienne version du Project au lieu de la version courante de Soleil), suivi de plusieurs blocages autour du workflow Git et de l'absence du connecteur GitHub MCP dans l'environnement. Ces frictions ont motivé la rédaction des deux nouvelles règles §1 bis et §3 bis.

---

## Chronologie détaillée

### Bloc 1 — Tri des fichiers projet et remise à niveau (début de session)

Soleil a demandé un tri des fichiers du Project Anthropic pour démarrer sur des bases saines. Identification et suppression proposée de :
- Recoveries périmés (v4, v5, contextes Opus, session recaps)
- Prompts Cowork one-shot déjà exécutés
- Logos V3/V4 (remplacés par V7)
- Briefings et roadmaps redondants
- Instructions en double

Après nettoyage côté Soleil, copie du `tellux_CORRECT.html` depuis le Project vers `/mnt/user-data/outputs/` — **mais** la version copiée s'est révélée être une version antérieure sans le module astral ni le refactor Phyphox tenté la veille. Soleil a dû me signaler que je travaillais sur une version périmée, et uploader la vraie version courante (`tellux_v6_design.html` renommé).

**Leçon tirée :** je n'ai pas fait d'audit d'état en début de session. Cette erreur a déclenché la rédaction de la règle §1 bis plus tard.

### Bloc 2 — Fix bouton CSV Phyphox (reprise du point d'hier)

D'après le post-mortem du 13 avril, le bouton CSV Phyphox ne s'affichait pas malgré plusieurs tentatives de fix. Soleil avait noté en fin de session : *"Le bouton est peut-être mal choisi. Juste pour les smartphones."*

**Constat de cette session** : le code existant bascule bien `c-csv-row` en `block` quand `smartphone_mag` est sélectionné. Le bug d'hier venait probablement d'un cache Cloudflare ou d'une désynchronisation `dev`/`main`, pas d'un vrai bug JS.

**Décision prise** : refactor de design plutôt que chasse au bug. Le bouton est rendu visible **par défaut** pour tous les instruments magnétométriques (`smartphone_mag`, `trifield`, `anfr`, `autre_capteur`), et masqué uniquement pour les instruments non-magnéto (`smartphone_rssi`, `smartphone_wifi`, `cornet`, `rtlsdr`, `observation`, `ressenti`). Libellé générique : `📁 Importer un CSV de mesures (Phyphox, Physics Toolbox…)`.

**Résultat :** problème résolu par refactor UX plutôt que par chasse au bug. JS validé avec `node --check`.

### Bloc 3 — Fix pin violet de mesure orphelin

Premier problème identifié par Soleil dans la liste des finitions pré-envoi EM : **les pins de contribution restent visibles après annulation du formulaire**. Diagnostic rapide : la variable `pending` (pin violet temporaire) n'était pas nettoyée quand l'utilisateur cliquait "Annuler", seulement quand il sauvegardait.

**Correctif appliqué :**
1. Nouvelle fonction `cancelContrib()` qui nettoie tout : pin, formulaire, champs, CSV en attente, indicateur position, FAB state, handler de clic.
2. Bouton Annuler redirigé vers `cancelContrib()` au lieu du simple `display:none`.
3. Isolation du handler de clic `map.once('click')` dans une référence nommée `_contribClickHandler` + helper `_armContribClick()` pour pouvoir le retirer sélectivement sans casser les autres handlers globaux (cf. leçon mémoire sur les "two competing map.on('click') handlers").
4. `startContrib`, `repositionMarker` et `startContribFromFAB` uniformisés pour utiliser le même helper.

**Cas couverts** :
- Clic Annuler sans avoir posé de pin → handler désarmé, pas de pin parasite.
- Clic Annuler après avoir posé un pin → pin supprimé + formulaire reset.
- Fermeture via FAB avant clic carte → handler désarmé.

### Bloc 4 — Problème deuxième niveau : pins de mesures sauvegardées

Soleil remonte que **les pins des mesures sauvegardées** restent sur la carte en permanence. Diagnostic : la couche `lCon` (contributions) est ajoutée via `addMarker()` depuis la DB Supabase, et est affichée en permanence pour tous les visiteurs. Risque de saturation visuelle à partir de quelques dizaines de contributions.

**Décision produit** prise ensemble :
- **Option D (minimum viable)** appliquée tout de suite : `ACTIVE.con = false` par défaut + `lCon` non ajoutée à la carte au démarrage. La couche s'active automatiquement quand l'utilisateur ouvre le formulaire de contribution (logique existante dans `startContribFromFAB`).
- **Option A (clustering)** notée comme ticket **B-CLUSTER** en voie B — intégration future de `Leaflet.markercluster` quand le volume dépassera 30-50 contributions.

Note ajoutée à `TELLUX_ROADMAP.md` en section 5 (voie B).

### Bloc 5 — Confusion voie A / voie B, fixation en mémoire

Découverte d'une contradiction entre la mémoire de Claude (qui avait voie A = "fixes courants" et voie B = "raffinements DA") et la roadmap mise à jour par Cowork (voie A = **livraison immédiate / gel v6**, voie B = **montée en gamme 3-6 mois**).

La roadmap Cowork est la vérité. Fixation en mémoire :

> *"Tellux : voie A = livraison immédiate / gel v6 (stable, déployée, envoi partenaires, dépôt CTC). Voie B = montée en gamme horizon 3-6 mois (landing Framer, N8N, migration modulaire, clustering contributions, etc.). Ne jamais inverser."*

### Bloc 6 — Audit GPS mégalithiques (round 1)

Soleil remonte le sujet de la vérification GPS des sites mégalithiques, normalement assigné à un travail manuel sur Google Earth. L'Excel qu'il avait rempli a été perdu. Proposition : lancer une recherche automatique via `launch_extended_search_task` pour auditer les 63 sites mégalithiques contre sources publiques (Megalithic Portal, Wikidata, OpenStreetMap, Persée, base Mérimée).

**Résultat de l'audit web** :
- 9 sites corrects (<50 m)
- 4 sites acceptables (50-200 m)
- **17 sites avec correction critique nécessaire (>200 m)**
- 25 sites non trouvés dans sources publiques
- 8 sites ambigus (doublons ou noms contestés)
- Écart maximal : **56,6 km** pour Tappa torre (commune confondue)
- Taux d'erreur sur sites vérifiables : 57%

### Bloc 7 — Architecture : câblage de SITES_REFERENCE.json

Soleil rappelle qu'on avait prévu d'externaliser `SITES[]` dans un fichier JSON — documenté dans la roadmap depuis plusieurs sessions mais jamais implémenté. Le code continuait à porter les coordonnées en dur dans le HTML, ce qui explique les régressions GPS récurrentes entre sessions.

**Vérification** : le `SITES_REFERENCE.json` existe déjà (uploadé par Soleil), contient 116 sites avec structure objet `{id, lat, lon, nom, type, couleur, description}`. Le HTML n'a **aucun** fetch externe.

**Architecture appliquée** :
1. `const SITES` → `let SITES` (permettre le remplacement)
2. `SITES.forEach` top-level wrappé dans `buildSiteMarkers()` + `clearLayers()` pour ré-exécution possible
3. Nouvelle fonction `loadSitesReference()` qui fetch le JSON, convertit le format objet → tableau (`[lat, lon, nom, type, couleur, desc]`) pour compatibilité avec tout le code consommateur, puis appelle `buildSiteMarkers()`
4. Fallback inline préservé : le tableau `SITES` inline reste en place, utilisé si le fetch échoue (404, CORS, etc.)
5. Console logs informatifs : `[Tellux] SITES_REFERENCE.json chargé : X sites` ou `[Tellux] Fallback SITES inline : <erreur>`

### Bloc 8 — Corrections GPS appliquées au JSON (vague 1 — 14 corrections)

Application au JSON des 14 corrections critiques validées du rapport d'audit mégalithique, avec métadonnées `gps_source` et `gps_audit` ajoutées à chaque site corrigé :

- **Priorité maximale** : Filitosa, I Stantari / Cauria, Renaghju, Palaggiu / Paddaghju (sites emblématiques, erreurs de 400-900 m)
- **Erreurs massives** : Tappa (56 km), Capu di Logu (32 km), Castaldu (18 km), Piève (16 km), Ceccia (8 km), Tavera (7,8 km)
- **Erreurs km** : U Cantonu, U Paladinu, Rizzanese, Scalsa Murta

**Nettoyages structurels** :
- Suppression du doublon "Stazzona di u Diavulu menhirs" (= Fontanaccia renommé + erreur de type : dolmen étiqueté menhir)
- Requalification "Lion de Roccapina" retiré (formation naturelle, pas mégalithe)

Résultat JSON : 114 sites.

### Bloc 9 — Arbitrages doublons et nomenclature

Questions posées à Soleil, réponses appliquées :

1. **Monte-Revincu vs Dolmen de la Serra** → distinguer (village néolithique à 42.6704/9.2585, dolmen Casa di l'Urca à 42.6690/9.2649)
2. **Capula torre vs Cucuruzzu/Capula** → fusionner (suppression Capula torre)
3. **Sposata vs Renaghju** → garder Sposata en l'état (probable doublon mais sans preuve)
4. **Torre de Tozzu → Torre de Tusiu** → correction orthographe (Lanfranchi 1998)
5. **Casteddu di Corti** → requalifier en "Remarquable" (citadelle médiévale, pas mégalithique)

Résultat JSON : 113 sites.

### Bloc 10 — Déploiement raté puis rattrapé

Première tentative de déploiement du HTML câblé + JSON corrigé :
1. Commandes Git fournies comme un bloc copiable — mais Soleil avait des fichiers non commités (`TELLUX_ROADMAP.md` modifié, `PROJECT_INSTRUCTIONS.md` et `TELLUX_RECOVERY_v6.md` untracked), ce qui a bloqué `git checkout main`.
2. Résolution : commit séparé des fichiers de doc, puis retour au merge.
3. Merge `dev → main` a fait ressortir 40 fichiers et 3 HTML (`tellux.html`, `tellux_CORRECT.html`, `tellux_v6_design.html`) car `main` était très en retard.
4. **Problème majeur découvert** : Cloudflare sert `index.html` par défaut, qui était une **ancienne version** (tellux v5.9) distincte de `tellux_CORRECT.html`. Tout notre travail de session était techniquement sur `main` mais **pas servi** au public.
5. Résolution : `cp tellux_CORRECT.html index.html` + commit + push.

### Bloc 11 — Frictions workflow Git et GitHub MCP manquant

Soleil exprime clairement sa frustration avec le workflow Git manuel. Demande explicite : *"il faut que tu sois capable de le faire toi-même, par cowork ou cowork, il faut trouver une solution."*

**Vérifications faites** (plusieurs `tool_search`) : aucun connecteur GitHub MCP n'est chargé dans cette session, même après que Soleil ait activé l'option "Ajouter depuis GitHub" dans l'interface. Distinction clarifiée :
- "Ajouter depuis GitHub" dans le bouton "+" = import de fichiers en lecture seule
- **Vrai connecteur GitHub MCP** = nécessiterait une installation MCP custom ou l'activation Settings → Connectors, pas disponible dans cette session malgré les tentatives de Soleil

Conclusion factuelle : **c'est un problème de propagation côté Anthropic**. Décision : on contourne pour aujourd'hui, on en reparle dans la session B "plein potentiel Claude".

**Conséquence productive** : rédaction de la règle §3 bis (procédure de déploiement explicite avec bloc Git pré-rédigé).

### Bloc 12 — Vérification du déploiement

Incapacité à vérifier le déploiement directement côté Claude :
- `web_fetch` sur `tellux.pages.dev` bloqué par `robots.txt` (Cloudflare Pages anti-scraping)
- Connecteur Cloudflare Developer Platform chargé mais limité à D1, R2, KV, Hyperdrive — **pas de tool Pages deployment status**
- Pas de connecteur browser navigation

**Contournement trouvé** : demander à Soleil de faire **Ctrl+U** (code source) dans le navigateur et chercher `loadSitesReference`. Soleil a collé la fonction complète dans le chat, confirmant visuellement que le déploiement a fonctionné.

### Bloc 13 — Audit GPS non-mégalithiques (round 2)

Soleil propose d'étendre l'audit web à la couche patrimoine complète. Filtrage : 50 sites non-mégalithiques (35 Remarquables, 9 Sites remarquables, 6 Hydrauliques), les 314 églises romanes laissées pour plus tard (Soleil confirme qu'elles sont bien placées).

**Lancement `launch_extended_search_task`** avec la liste complète des 50 sites.

**Résultats choc** :
- **0 site parfaitement conforme** (<50 m)
- 2 sites acceptables (Bonifacio remparts, Barrage Tolla)
- **41 sites avec correction nécessaire (>300 m)**
- 1 site non trouvé (Castello della Rocca)
- 6 sites ambigus
- **Médiane d'erreur : ~4,9 km**
- **Erreur maximale : 41,4 km** (Barrage Padula, confusion avec commune éponyme)

Le rapport révèle un problème systémique : les coordonnées initiales semblent avoir été géocodées à partir de noms de communes, pas de sites spécifiques. Aucun sommet, lac, citadelle ou barrage n'était correctement positionné.

**Cas particulier — Anneaux du Cap Corse** : l'audit révèle que toutes les sources scientifiques publiques (CNRS, Gombessa 6, Andromède Océanologie) identifient ce site comme des **formations coralligènes sous-marines à 120 m de profondeur**, pas des pétroglyphes terrestres. Décision Soleil : garder le site avec les bonnes coordonnées en mer et reclasser en site marin.

**Cas particulier — Barrage Vignola** : aucun barrage de ce nom dans la base CFBR. Décision Soleil : renommer en "Barrage du Rizzanese" avec les bonnes coordonnées.

### Bloc 14 — Application des 33 corrections non-mégalithiques

Application au JSON d'un seul bloc :
- **31 corrections Vague 1** (Padula, Spelunca, Calanques de Piana, Uomo di Cagna, Lac de Creno, Alesani, Nino, Haut-Asco, Renoso, Agnello, Porto/Calanche, Tolla lac, Ospedale barrage, Valdu Niellu, Monte d'Oro, Inzecca, San Petrone, Stello, Voile de la Mariée, Cinto, Parata, Piscia di Gallo, Grotte Bonifacio, Capu Rossu, Calacuccia, Ile-Rousse, Scandola, Citadelle Calvi, Bavella, Bastia Citadelle, Monte Ghjenuva)
- **Fusion** "Casteddu di Corti" dans "Citadelle de Corte" (nom bilingue "Citadelle de Corte / Casteddu di Corti")
- **Anneaux du Cap Corse** recoordonnées en mer (43.17654, 9.60008), description refaite en site coralligène sous-marin
- **Barrage Vignola → Barrage du Rizzanese** (41.73472, 9.11444)

Résultat JSON final : **112 sites**, dont **49 audités/corrigés** (16 mégalithiques + 33 non-mégalithiques).

### Bloc 15 — Disclaimer GPS dans popups

Action 1 de la liste finitions EM : afficher un disclaimer discret dans les popups de sites.

**Implémentation** :
1. Mapping JSON → tableau enrichi avec 7e élément `gpsInfo = {source, audit}` ou `null`
2. Click handler modifié pour afficher :
   - Site avec `gps_source` → `📍 GPS vérifié · [source] · [date audit]`
   - Site sans → `📍 Coordonnées indicatives — précision ±100 m, audit terrain en cours`
   - Fallback inline : tous les sites affichent "indicatives" (car le tableau inline n'a pas d'info GPS)

### Bloc 16 — Prompt Cowork A-4b

Rédaction du prompt `COWORK_PROMPT_A4B_AUDIT_COUCHES.md` pour l'audit du pattern couche ↔ panneau ↔ légende :
- Phase 1 : inventaire complet (tableau de toutes les couches avec boutons, layers, panneaux, légendes, fonctions de build)
- Phase 2 : audit de 6 points de cohérence (activation, désactivation, état initial, cas limites, fermeture programmatique, responsive mobile)
- Phase 3 : rapport markdown `TELLUX_AUDIT_A4B.md`
- Phase 4 : corrections ciblées uniquement sur les incohérences 🔴 et 🟡

Le prompt intègre les règles §1 bis (audit d'état obligatoire) et §3 bis (procédure Git explicite).

Soleil a lancé cette session Cowork en parallèle en fin de session.

### Bloc 17 — Remarque tardive sur les zones

Soleil a fait remarquer en fin de session que l'audit couche A-4b était probablement lié à un autre problème qu'on avait identifié : **les sites étendus représentés par un pin unique**. Scandola (1669 ha), Désert des Agriates (150 km²), Anneaux du Cap Corse (site marin), forêts, gorges, massifs — tous représentés par un point ponctuel alors qu'ils couvrent des surfaces énormes.

Le prompt Cowork A-4b ayant déjà été envoyé, on a noté ça comme un **ticket B-ZONES séparé en voie B** à traiter dans une session dédiée (polygones Leaflet ou cercles d'extension + récupération géométries officielles INPN/OSM). Fixation en mémoire.

---

## Règles de conduite posées en séance

### §1 bis — Audit d'état HTML obligatoire en début de session technique

> Avant toute modification du HTML, Claude exécute un audit d'état : `wc -l`, puis `grep` des features clés attendues selon la mémoire et la roadmap (refactor Phyphox, fetch SITES_REFERENCE, module astral, etc.). Claude compare ce qu'il voit au dernier état documenté. Si une feature attendue manque ou si le compte de lignes diffère significativement de la mémoire, Claude alerte Soleil explicitement avant de modifier quoi que ce soit et attend confirmation. Aucune modification silencieuse sur un fichier dont l'état n'a pas été validé.

### §3 bis — Procédure de déploiement explicite après livraison fichier

> Quand Claude livre un ou plusieurs fichiers à déployer sur Cloudflare Pages, il fournit systématiquement les commandes Git exactes à taper, dans l'ordre, avec les noms de fichiers réels et les messages de commit pré-rédigés. Pas de "tu commit et tu push" en abstrait. Format attendu : un bloc terminal copiable, avec une ligne par commande, et un commentaire bref à côté de chaque étape si nécessaire. Si plusieurs fichiers sont livrés, Claude liste explicitement où chacun doit être placé dans l'arborescence du repo. Cette règle s'applique tant que Soleil n'a pas indiqué qu'il maîtrise le workflow Git en autonomie.

---

## Livrables de session

| Fichier | Destination | Statut |
|---|---|---|
| `tellux_CORRECT.html` | `/mnt/user-data/outputs/` puis push `main` | ✅ déployé |
| `index.html` | racine repo, = copie `tellux_CORRECT.html` | ✅ déployé |
| `SITES_REFERENCE.json` (112 sites) | `/mnt/user-data/outputs/` puis push `main` | ✅ déployé |
| `TELLUX_ROADMAP.md` (avec note B-CLUSTER) | push `main` | ✅ déployé |
| `COWORK_PROMPT_A4B_AUDIT_COUCHES.md` | Soleil a lancé la session Cowork | ✅ lancé |

---

## Bilan technique consolidé

### Ce qui est fait et déployé

✅ Fix bouton CSV Phyphox (refactor design — plus d'affichage conditionnel)
✅ Fix pin violet orphelin après annulation (`cancelContrib` + handler nommé `_contribClickHandler`)
✅ Couche contributions masquée par défaut au démarrage (activation auto via FAB)
✅ Fetch `SITES_REFERENCE.json` câblé avec fallback inline
✅ Disclaimer GPS dans popups sites
✅ 16 corrections GPS mégalithiques (Filitosa, Cauria, Palaggiu, Tappa, Capu di Logu, Castaldu, Piève, Ceccia, Tavera, U Cantonu, U Paladinu, Rizzanese, Scalsa Murta, Renaghju, Monte-Revincu distingué, Dolmen de la Serra distingué)
✅ 33 corrections GPS non-mégalithiques (31 Vague 1 + Anneaux marins + Rizzanese)
✅ Nettoyages doublons (Stazzona, Lion de Roccapina, Casteddu di Corti, Capula torre)
✅ Requalifications nomenclature (Torre de Tusiu, Citadelle de Corte bilingue)
✅ Note B-CLUSTER ajoutée en voie B

### Ce qui reste pour sessions suivantes

🟡 Session Cowork A-4b en cours (audit couche ↔ panneau ↔ légende)
🟡 Ticket B-ZONES (voie B) — représentation polygonale des sites étendus
🟡 Audit GPS des 314 églises romanes (voie B ou session dédiée)
🟡 25 sites mégalithiques "non trouvés" dans les sources web (validation terrain nécessaire)
🟡 6 sites non-mégalithiques ambigus (Cap Corse extrême nord, Tour Chiappa, Castello della Rocca, Cirque Bonifato, Désert Agriates centroïde, Plateau Coscione)
🟡 Erreurs console à investiguer : `loadAnt: Failed to fetch` et `orientation contributions: Failed to fetch` (probablement Supabase)
🟡 Finitions UX pré-envoi EM non inventoriées (section 3.0 roadmap)
🟡 Captures HD A-8 pour dossier CTC (Soleil)
🟡 Arbitrage structure juridique S-1 (Soleil)

---

## Points d'attention pour la prochaine session

1. **Tester le déploiement final** : vérifier dans la console navigateur que le message est bien `[Tellux] SITES_REFERENCE.json chargé : 112 sites` et plus `Fallback SITES inline : HTTP 404`.

2. **Tester le disclaimer GPS** : cliquer sur Filitosa (doit afficher "GPS vérifié · Megalithic Portal sid=9498 · 2026-04-13") et sur un site non audité (doit afficher "Coordonnées indicatives").

3. **Tester le flux mesure complet** : clic FAB → clic carte → remplir → sauvegarder → vérifier que le pin sauvegardé apparaît bien dans la couche contributions qui s'est activée automatiquement.

4. **Récupérer les livrables de la session Cowork A-4b** une fois qu'elle est terminée.

5. **Ouvrir la session B "plein potentiel Claude"** pour discuter en profondeur de :
   - L'activation du connecteur GitHub MCP (MCP custom avec token si nécessaire)
   - L'exploitation systématique de `tool_search` en début de session
   - Les connecteurs Anthropic disponibles et leur usage
   - Les patterns de travail pour éviter les régressions et frictions observées dans cette session

---

## Mémoire Opus mise à jour en séance

```
1. Tellux : voie A = livraison immédiate / gel v6 (stable, déployée, envoi partenaires, dépôt CTC). Voie B = montée en gamme horizon 3-6 mois (landing Framer, N8N, migration modulaire, clustering contributions, etc.). Ne jamais inverser.

2. Tellux ticket B-ZONES (voie B) : les sites étendus (Scandola, Désert des Agriates, Anneaux du Cap Corse, forêts, gorges, massifs) sont actuellement représentés par un pin unique alors qu'ils couvrent des dizaines de km². À traiter dans une session dédiée : polygones Leaflet ou cercles d'extension + récupération des géométries officielles (INPN pour réserves, OSM pour massifs). Flaggé "zone":true dans SITES_REFERENCE.json pour identification future.
```

---

*Document généré en fin de session le 14 avril 2026.*
