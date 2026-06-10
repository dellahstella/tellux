# Revue bilingue FR ↔ CO — app.html (chrome UI, bêta)

**Statut** : bêta — accessible uniquement via `app.html?lang=co` (aucun bouton public).
Promotion en toggle visible seulement APRÈS validation par un relecteur bilingue corse.

**Doctrine** : FR est la source de vérité. Le corse ci-dessous est produit par modèle,
approximatif par construction — c'est précisément l'objet de cette table : chaque ligne
est un point de revue humaine. Le mécanisme i18n est additif et gardé par le FR verbatim
(si le FR de l'app dérive, la chaîne est sautée, jamais écrasée — voir `window.__telluxI18n.skipped`).

**Comment réviser** : corriger la colonne CO directement dans le bloc i18n de `app.html`
(entrées JSON entre `I18N-CO-ENTRIES-BEGIN` et `I18N-CO-ENTRIES-END`), puis régénérer
cette table avec `node scripts/export_i18n_co_table.mjs`.

---

## Table de revue

<!-- TABLE-BEGIN — section régénérée par scripts/export_i18n_co_table.mjs, ne pas éditer à la main -->

**307 chaînes** traduites (chrome UI). Pour corriger une traduction : éditer la valeur CO
dans le bloc i18n de `app.html` (marqueurs `I18N-CO-ENTRIES-BEGIN/END`), puis relancer
`node scripts/verify_i18n_co.mjs` puis `node scripts/export_i18n_co_table.mjs`.

Colonnes STATUT/SOURCE = passe de vérification lexicale contre INFCOR (ADECEC), cf.
`scripts/verify_i18n_co.mjs` et `docs/i18n/co-verification-2026-06-10/`. STATUT : `vérifié`
(tous les mots de contenu attestés-DIRECT, forme exacte rejouable), `vérifié (flexion)` (tous
  attestés mais >=1 flexion régulière d'un lemme attesté, forme exacte non rejouable), `flaggé`
  (au moins un mot non attesté / faux-sens /
dialecte — voir `FLAGGED_CO_NATIF.md`), `à confirmer` (au moins un mot non encore vérifié cette
passe). SOURCE = id(s) unique INFCOR (citables, rejouables).

| Clé | Type | FR (source de vérité) | CO (à réviser) | STATUT | SOURCE |
|---|---|---|---|---|---|
| `page_title` | titre de page | Tellux — Révéler l'invisible · Cartographie électromagnétique Corse | Tellux — Palesà l'invisibile · Cartugrafia elettromagnetica Corsica | flaggé | — (cf. note) |
| `skip_link` | texte | Aller au contenu | Andà à u cuntenutu | vérifié | INFCOR 2990, 12906 |
| `h1_hidden` | texte | Tellux — Cartographie électromagnétique de la Corse | Tellux — Cartugrafia elettromagnetica di a Corsica | vérifié (flexion) | INFCOR 9066 · flexion: 15612 |
| `disclaimer_title` | texte | Bienvenue sur Tellux | Benvenuti nant'à Tellux | vérifié (flexion) | flexion: 6526 |
| `d_lead_em` | texte | Révéler l'invisible. | Palesà l'invisibile. | flaggé | — (cf. note) |
| `d_lead_text` | texte | Un outil de cartographie électromagnétique de la Corse — conçu pour l'exploration scientifique et citoyenne du territoire. | Un attrezzu di cartugrafia elettromagnetica di a Corsica — cuncipitu per l'esplurazione scentifica è citatina di u territoriu. | flaggé | — (cf. note) |
| `d_block_title_em` | texte | Champs électromagnétiques | Campi elettromagnetichi | vérifié (flexion) | flexion: 15612, 54907 |
| `d_block_title_contrib` | texte | Contribuer | Cuntribuisce | vérifié | INFCOR 12821 |
| `d_block_title_privacy` | texte | Données & vie privée | Dati è vita privata | vérifié (flexion) | INFCOR 52019 · flexion: 13532, 36306 |
| `d_foot_text` | texte (1er nœud) | Tellux ne remplace pas une mesure professionnelle. | Tellux ùn rimpiazza micca una misura prufessiunale. | vérifié (flexion) | INFCOR 28694, 36718 · flexion: 39205 |
| `d_foot_link` | texte | Méthodologie complète → | Metodulugia cumpleta → | vérifié (flexion) | INFCOR 28060 · flexion: 12090 |
| `d_btn` | texte | Accéder à la carte | Accede à a carta | vérifié | INFCOR 622, 9044 |
| `logo_title` | tooltip | Tellux — Révéler l'invisible | Tellux — Palesà l'invisibile | flaggé | — (cf. note) |
| `logo_aria` | aria-label | Retour à l'accueil Tellux | Ritornu à l'accolta Tellux | vérifié | INFCOR 839, 39847 |
| `tagline_em` | texte | Révéler l'invisible | Palesà l'invisibile | flaggé | — (cf. note) |
| `tagline_suffix` | texte | · Corse | · Corsica | vérifié | INFCOR  |
| `nav_methodo` | texte | Méthodologie | Metodulugia | vérifié | INFCOR 28060 |
| `nav_methodo_tt` | tooltip | Méthodologie & sources | Metodulugia è fonti | vérifié | INFCOR 18021, 28060 |
| `nav_termes` | texte | Comprendre les termes | Capisce i termini | flaggé | — (cf. note) |
| `nav_termes_tt` | tooltip | Glossaire & guides pratiques | Glussariu è guide pratiche | vérifié (flexion) | INFCOR 19790 · flexion: 20295, 35825 |
| `nav_glossaire` | texte | Glossaire | Glussariu | vérifié | INFCOR 19790 |
| `nav_glossaire_tt` | tooltip | Guide et glossaire technique complet (page publique) | Guida è glussariu tecnicu cumpletu (pagina publica) | vérifié (flexion) | INFCOR 12090, 19790, 20295, 32038, 49087 · flexion: 36802 |
| `nav_apropos` | texte | À propos | À prupositu | vérifié | INFCOR 36614 |
| `nav_apropos_tt` | tooltip | À propos du projet | À prupositu di u prugettu | vérifié | INFCOR 36473, 36614 |
| `nav_patrimoine` | texte | Patrimoine (bêta) | Patrimoniu (beta) | vérifié | INFCOR 33245 |
| `nav_patrimoine_tt` | tooltip | Cartographie patrimoniale de la Corse | Cartugrafia patrimuniale di a Corsica | vérifié | INFCOR 9066, 33527 |
| `nav_mairies` | texte | Élu·e ? Outils mairie → | Elettu·a ? Strumenti merria → | vérifié (flexion) | INFCOR 15830, 27910 · flexion: 23894 |
| `nav_mairies_tt` | tooltip | Outils administratifs pour les communes corses | Strumenti amministrativi per e cumune corse | vérifié (flexion) | flexion: 2763, 11092, 12176, 23894 |
| `sb_dot_tt` | tooltip | Supabase connexion en cours… | Supabase cunnessione in corsu… | vérifié | INFCOR 11092, 12736 |
| `sb_dot_aria` | aria-label | Statut Supabase | Statu Supabase | flaggé | — (cf. note) |
| `hdr_status` | texte | chargement… | caricamentu… | flaggé | — (cf. note) |
| `about_title` | texte | À propos de Tellux | À prupositu di Tellux | vérifié | INFCOR 36614 |
| `about_h4_pas` | texte | Ce que Tellux n'est pas | Ciò chì Tellux ùn hè micca | vérifié | INFCOR  |
| `about_h4_episteme` | texte | Position épistémique | Pusizione epistemica | flaggé | — (cf. note) |
| `about_h4_porteur` | texte | Porteur du projet | Purtadore di u prugettu | vérifié | INFCOR 36473, 53147 |
| `about_h4_sources` | texte | Sources de données | Fonti di dati | vérifié (flexion) | INFCOR 18021 · flexion: 13532 |
| `about_h4_contact` | texte | Contributions & contact | Cuntribuzione è cuntattu | vérifié | INFCOR 12711, 12823 |
| `expert_modal_title` | texte | Mode Expertise | Modu Espertu | vérifié | INFCOR 16367, 28927 |
| `expert_modal_cancel` | texte | Annuler | Annullà | vérifié | INFCOR 3272 |
| `expert_modal_ok` | texte | Compris | Capitu | vérifié | INFCOR 8508 |
| `contrib_title` | texte | Contribuer à Tellux | Cuntribuisce à Tellux | vérifié | INFCOR 12821 |
| `contrib_close_aria` | aria-label | Fermer | Chjode | vérifié | INFCOR 707 |
| `ctab_obs` | texte | Observation | Osservazione | vérifié | INFCOR 31750 |
| `ctab_mes` | texte | Mesure technique | Misura tecnica | vérifié (flexion) | INFCOR 28694 · flexion: 49087 |
| `ctab_cap` | texte | Capteurs appareil | Sensori di l'apparechju | flaggé | — (cf. note) |
| `obs_intro` | texte | Partagez une observation libre associée à un point sur la carte. Votre observation sera vérifiée avant publication. | Spartite un'osservazione libera ligata à un puntu nant'à a carta. A vostra osservazione sarà verificata prima d'esse publicata. | flaggé | — (cf. note) |
| `obs_position` | texte | Cliquez d'abord sur la carte pour placer le point, puis rouvrez ce formulaire. Ou saisissez manuellement ci-dessous. | Cliccate prima nant'à a carta per piazzà u puntu, po riaprite stu formulariu. O entrite à manu quì sottu. | flaggé | — (cf. note) |
| `obs_lat_ph` | placeholder | Latitude (ex: 42.308) | Latitudine (es: 42.308) | vérifié | INFCOR 25407 |
| `obs_lon_ph` | placeholder | Longitude (ex: 9.150) | Longitudine (es: 9.150) | vérifié | INFCOR 25908 |
| `obs_note_label` | texte | Que souhaitez-vous partager ? | Chì vulete sparte ? | vérifié (flexion) | INFCOR 45664 · flexion: 52311 |
| `obs_note_ph` | placeholder | Ressenti, observation visuelle, contexte particulier… (300 caractères max) | Sensazione, osservazione visuale, cuntestu particulare… (300 caratteri max) | vérifié | INFCOR 8927, 12917, 31750, 32904, 43235, 52018 |
| `obs_cancel` | texte | Annuler | Annullà | vérifié | INFCOR 3272 |
| `obs_send` | texte | Envoyer | Mandà | vérifié | INFCOR 26627 |
| `mes_avant` | texte | Avant de mesurer | Prima di misurà | vérifié | INFCOR 28691 |
| `mes_precautions` | texte | Pour une lecture exploitable : activez le mode avion, posez le téléphone à plat pendant 30 secondes minimum, débranchez la charge USB, et écartez les objets métalliques (clés, montre, étui aimanté) à plus de 30 cm du capteur. | Per una lettura sfruttevule : attivate u modu aviò, pusate u telefonu à pianu durante 30 secondi à u minimu, staccate a carica USB, è alluntanate l'ogetti metallichi (chjave, mostra, astucciu magneticu) à più di 30 cm da u sensore. | flaggé | — (cf. note) |
| `mes_pourquoi` | texte | Pourquoi ces précautions ? | Perchè ste precauzione ? | vérifié | INFCOR 35839 |
| `mes_formulaire` | texte | Formulaire complet pour les utilisateurs équipés : magnétomètre smartphone (Phyphox), capteur externe (TriField, Cornet), RTL-SDR ou mesure ANFR certifiée. | Formulariu cumpletu per l'utilizatori equipati : magnetometru smartphone (Phyphox), sensore esternu (TriField, Cornet), RTL-SDR o misura ANFR certificata. | flaggé | — (cf. note) |
| `mes_li_pointage` | texte | Pointage carte obligatoire (Corse uniquement) | Puntamentu carta ubligatoriu (Corsica sola) | flaggé | — (cf. note) |
| `mes_li_saisie` | texte | Saisie instrument, valeur et unité | Inserimentu strumentu, valore è unità | vérifié | INFCOR 23596, 23894, 50939, 51238 |
| `mes_li_csv` | texte | Import CSV Phyphox / Physics Toolbox | Importu CSV Phyphox / Physics Toolbox | vérifié (flexion) | flexion: 21418 |
| `mes_li_ctx` | texte | Contexte intérieur optionnel (étage, matériaux murs, appareils actifs) | Cuntestu internu ozzionale (pianu, materiali muri, apparechji attivi) | flaggé | — (cf. note) |
| `mes_cancel` | texte | Annuler | Annullà | vérifié | INFCOR 3272 |
| `mes_open_form` | texte | Ouvrir le formulaire | Apre u formulariu | flaggé | — (cf. note) |
| `cap_h3` | texte | Mesure automatisée — module en développement | Misura autumatizata — modulu in sviluppu | flaggé | — (cf. note) |
| `cap_position_label` | texte | Position | Pusizione | vérifié | INFCOR 37537 |
| `cap_geoloc` | texte | Utiliser ma position actuelle | Aduprà a mo pusizione attuale | vérifié | INFCOR 5322, 21539, 37537 |
| `cap_small` | texte | Ou cliquez sur la carte avant d'ouvrir cette fenêtre. | O cliccate nant'à a carta prima d'apre sta finestra. | flaggé | — (cf. note) |
| `cap_mag` | texte | Magnétomètre | Magnetometru | vérifié | INFCOR 26263 |
| `cap_orient` | texte | Orientation | Orientazione | vérifié | INFCOR 31847 |
| `cap_acc` | texte | Accéléromètre | Accelerometru | flaggé | — (cf. note) |
| `cap_start` | texte | Démarrer l'enregistrement (10 s) | Principià l'arregistramentu (10 s) | vérifié | INFCOR 36568, 38433 |
| `cap_stop` | texte | Arrêter | Piantà | vérifié | INFCOR 34475 |
| `cap_results` | texte | Résultats | Risultati | vérifié (flexion) | flexion: 40123 |
| `cap_mean` | texte | Moyenne | Media | vérifié | INFCOR 27633 |
| `cap_std` | texte | Écart-type | Scartu tipu | vérifié | INFCOR 41772, 49179 |
| `cap_n` | texte | Échantillons | Campioni | vérifié (flexion) | flexion: 8223 |
| `cap_note_ph` | placeholder | Notes optionnelles (contexte, observations…) | Note ozzionale (cuntestu, osservazione…) | flaggé | — (cf. note) |
| `cap_submit` | texte | Envoyer la mesure | Mandà a misura | vérifié | INFCOR 26627, 28694 |
| `methodo_title` | texte | 🔬 Méthodologie & Audit | 🔬 Metodulugia è Audit | vérifié | INFCOR 28060 |
| `mob_toggle_aria` | aria-label | Couches | Strati | vérifié (flexion) | flexion: 46893 |
| `sidebar_toggle_aria` | aria-label | Réduire la sidebar | Riduce a colonna laterale | vérifié | INFCOR 11948, 25148, 38856 |
| `sidebar_toggle_tt` | tooltip | Réduire la sidebar | Riduce a colonna laterale | vérifié | INFCOR 11948, 25148, 38856 |
| `chips_aria` | aria-label | Filtre par domaine physique | Filtru per duminiu fisicu | vérifié | INFCOR 15452, 17545, 17642 |
| `chip_label` | texte | Domaine | Duminiu | vérifié | INFCOR 15452 |
| `chip_all` | texte | Tous | Tutti | vérifié | INFCOR  |
| `chip_statique` | texte | Statique | Staticu | flaggé | — (cf. note) |
| `chip_statique_tt` | tooltip | Magnétique statique : géomagnétisme, anomalies crustales, susceptibilité lithologique | Magneticu staticu : geomagnetismu, anumalie crustale, suscettibilità litulogica | flaggé | — (cf. note) |
| `chip_elf_tt` | tooltip | Magnétique basse fréquence ELF 50 Hz : lignes HT/BT, postes sources, production | Magneticu à bassa frequenza ELF 50 Hz : linee HT/BT, posti surgente, pruduzzione | flaggé | — (cf. note) |
| `chip_rf_tt` | tooltip | Radiofréquences : antennes ANFR, émetteurs TDF | Radiofrequenze : antenne ANFR, emettitori TDF | flaggé | — (cf. note) |
| `chip_ionisant` | texte | Ionisant | Ionizante | vérifié | INFCOR 24862 |
| `chip_ionisant_tt` | tooltip | Rayonnement ionisant : radon, sites U/Th | Radiazione ionizante : radon, siti U/Th | vérifié (flexion) | INFCOR 24862, 37564 · flexion: 44828 |
| `cat_modele` | texte | Modèle EM | Mudellu EM | vérifié | INFCOR 29238 |
| `cat_anthropique` | texte | Sources anthropiques | Fonti antropiche | flaggé | — (cf. note) |
| `cat_naturel` | texte | Contexte naturel | Cuntestu naturale | vérifié | INFCOR 12917, 29937 |
| `subgroup_a` | texte | A. Substrat magnétique | A. Sustratu magneticu | flaggé | — (cf. note) |
| `subgroup_b` | texte | B. Contexte territorial (géologie, hydro, forêts) | B. Cuntestu territuriale (geulugia, idrulugia, fureste) | flaggé | — (cf. note) |
| `subgroup_c` | texte | C. Sites documentaires | C. Siti ducumentari | vérifié (flexion) | flexion: 15182, 44828 |
| `lyr_hot` | texte | Champ composite | Campu cumpostu | vérifié | INFCOR 12108, 54907 |
| `lyr_hot_tt` | tooltip | Champ composite estimé par le modèle Tellux (agrégation de 4 domaines physiques) | Campu cumpostu stimatu da u mudellu Tellux (agregazione di 4 duminii fisichi) | flaggé | — (cf. note) |
| `lyr_con` | texte | Mesures EM | Misure EM | vérifié (flexion) | flexion: 28694 |
| `lyr_con_tt` | tooltip | Mesures EM — contributions citoyennes + 30 fiches ANFR/EXEM certifiées (2024-2026) | Misure EM — cuntribuzione citatine + 30 schede ANFR/EXEM certificate (2024-2026) | flaggé | — (cf. note) |
| `lyr_ant` | texte | Antennes ANFR + TDF | Antenne ANFR + TDF | vérifié (flexion) | flexion: 3325 |
| `lyr_ant_tt` | tooltip | Antennes 2G/3G/4G/5G ANFR + émetteurs broadcast TDF | Antenne 2G/3G/4G/5G ANFR + emettitori broadcast TDF | flaggé | — (cf. note) |
| `lyr_res` | texte | Réseau HT | Reta HT | vérifié | INFCOR 38578 |
| `lyr_res_tt` | tooltip | Lignes et postes électriques haute tension (50 Hz) | Linee è posti elettrichi alta tensione (50 Hz) | flaggé | — (cf. note) |
| `lyr_bt` | texte | Réseau BT | Reta BT | vérifié | INFCOR 38578 |
| `lyr_bt_tt` | tooltip | Réseau basse tension BT — EDF SEI · zoom ≥ 12 | Reta bassa tensione BT — EDF SEI · zoom ≥ 12 | vérifié | INFCOR 6251, 38578, 48805 |
| `lyr_prod` | texte | Sites de production | Siti di pruduzzione | vérifié (flexion) | INFCOR 36699 · flexion: 44828 |
| `lyr_prod_tt` | tooltip | Centrales hydrauliques, éoliennes, diesel, TAC, biogaz, interconnexions | Centrale idrauliche, eoliane, diesel, TAC, biogas, intercunnessione | flaggé | — (cf. note) |
| `lyr_postes` | texte | Postes sources EDF | Posti surgente EDF | flaggé | — (cf. note) |
| `lyr_postes_tt` | tooltip | Postes sources EDF SEI (transformateurs HTB/HTA) — 21 postes OSM | Posti surgente EDF SEI (trasfurmatori HTB/HTA) — 21 posti OSM | flaggé | — (cf. note) |
| `lyr_geo` | texte | Géologie BRGM | Geulugia BRGM | vérifié | INFCOR 19035 |
| `lyr_geo_tt` | tooltip | Carte géologique BRGM — granite, schiste, calcaire | Carta geulogica BRGM — granitu, schistu, calcariu | vérifié (flexion) | INFCOR 7920, 9044, 19747, 42275 · flexion: 19033 |
| `lyr_failles` | texte | Failles tectoniques | Faglie tettoniche | flaggé | — (cf. note) |
| `lyr_failles_tt` | tooltip | Failles tectoniques BRGM — 8 failles principales (actives + quaternaires) | Faglie tettoniche BRGM — 8 faglie principale (attive + quaternarie) | flaggé | — (cf. note) |
| `lyr_radon_tt` | tooltip | Potentiel radon géologique — zones ASNR cat. 2/3 | Putenziale radon geulogicu — zone ASNR cat. 2/3 | vérifié (flexion) | INFCOR 19033, 37282 · flexion: 53250 |
| `lyr_emag` | texte | Fond magnétique régional | Fondu magneticu regiunale | flaggé | — (cf. note) |
| `lyr_emag_tt` | tooltip | Fond magnétique régional NOAA EMAG2v3 — anomalies du socle profond Corse | Fondu magneticu regiunale NOAA EMAG2v3 — anumalie di u zoccalu prufondu corsu | flaggé | — (cf. note) |
| `lyr_cav` | texte | Cavités | Cavità | vérifié | INFCOR 9503 |
| `lyr_cav_tt` | tooltip | Cavités souterraines — grottes, mines, karst (BRGM) | Cavità sutterranee — grotte, mine, karst (BRGM) | vérifié (flexion) | INFCOR 9503 · flexion: 19923, 28415, 47965 |
| `lyr_therm` | texte | Émergences thermales | Surgenti termali | vérifié (flexion) | flexion: 47822, 48860 |
| `lyr_therm_tt` | tooltip | Émergences thermales — observations de surface, marqueurs de failles actives | Surgenti termali — osservazione di superficia, marcatori di faglie attive | flaggé | — (cf. note) |
| `lyr_hyd` | texte | Hydrographie | Idrugrafia | vérifié | INFCOR 20241 |
| `lyr_hyd_tt` | tooltip | Nappes et cours d'eau souterrains (BRGM REMNAPPE) — couche visuelle ; le calcul utilise un dataset distinct | Falde è corsi d'acqua sutterranei (BRGM REMNAPPE) — stratu visuale ; u calculu adopra un dataset distintu | à confirmer | — |
| `lyr_foret` | texte | Forêts publiques | Fureste publiche | vérifié (flexion) | flexion: 18577, 36802 |
| `lyr_foret_tt` | tooltip | Forêts publiques ONF via WMS IGN Géoplateforme — couche visuelle niveau A (pas de modulation calcul). BD Forêt V2 complète non disponible en WMS public. | Fureste publiche ONF via WMS IGN Géoplateforme — stratu visuale livellu A (nisuna mudulazione di calculu). BD Forêt V2 cumpleta micca dispunibule in WMS publicu. | vérifié (flexion) | INFCOR 7971, 14759, 25903, 29326, 36802, 46893, 52018 · flexion: 12090, 18577, 36802 |
| `lyr_uth` | texte | Sites U/Th à mesurer | Siti U/Th da misurà | vérifié (flexion) | INFCOR 28691 · flexion: 44828 |
| `lyr_uth_tt` | tooltip | Sites U/Th à mesurer — catalogue de sites candidats à des mesures radiométriques (doses non mesurées, sources documentaires BRGM ou analogies géologiques) | Siti U/Th da misurà — catalogu di siti candidati à misure radiometriche (dose micca misurate, fonti ducumentarie BRGM o analugie geulogiche) | flaggé | — (cf. note) |
| `lyr_remarq` | texte | Sites géophysiques remarquables | Siti geofisichi rimarchevuli | vérifié (flexion) | flexion: 19028, 39445, 44828 |
| `lyr_remarq_tt` | tooltip | Sites géophysiques remarquables — 10 sites ponctuels à signature singulière (mines historiques, serpentinites ophiolitiques, surveillance radiologique marine). Données documentaires, mesures in situ souvent requises. | Siti geofisichi rimarchevuli — 10 siti puntuali à signatura singulare (mine storiche, serpentinite ofiolitiche, surviglianza radiulogica marina). Dati ducumentarii, misure in situ à spessu richieste. | flaggé | — (cf. note) |
| `lyr_crustal` | texte | Anomalies de référence (mondiales) | Anumalie di riferenza (mundiale) | vérifié (flexion) | INFCOR 29288, 38079 · flexion: 3447 |
| `lyr_crustal_tt` | tooltip | 5 anomalies magnétiques crustales mondiales de référence (cratères d'impact + BIF) — opt-in, comparaison locale/mondiale | 5 anumalie magnetiche crustale mundiale di riferenza (crateri d'impattu + BIF) — opt-in, paragone lucale/mundiale | flaggé | — (cf. note) |
| `btn_expert_aria` | aria-label | Outils experts | Strumenti esperti | vérifié (flexion) | flexion: 16367, 23894 |
| `btn_expert` | texte | Outils experts | Strumenti esperti | vérifié (flexion) | flexion: 16367, 23894 |
| `btn_share_aria` | aria-label | Partager la vue | Sparte a vista | vérifié | INFCOR 45664, 51996 |
| `btn_share` | texte | Partager la vue | Sparte a vista | vérifié | INFCOR 45664, 51996 |
| `xp_header` | texte | ⚙ Indice composite | ⚙ Indice cumpostu | vérifié | INFCOR 12108, 22460 |
| `xp_lastpoint` | texte | sur le dernier point analysé ◆ | nant'à l'ultimu puntu analizatu ◆ | vérifié | INFCOR 2937, 37341, 50774 |
| `xp_stats` | texte | Statistiques du modèle | Statistiche di u mudellu | vérifié (flexion) | INFCOR 29238 · flexion: 46410 |
| `xp_anfr_loading` | texte | chargement… | caricamentu… | flaggé | — (cf. note) |
| `xp_reset` | texte | Réinitialiser | Rimette à zeru | vérifié | INFCOR  |
| `xp_csv` | texte | ↓ CSV expert | ↓ CSV espertu | vérifié | INFCOR 16367 |
| `xp_off` | texte | Désactiver ✕ | Disattivà ✕ | flaggé | — (cf. note) |
| `bandeau_label` | texte | Indice composite (mode Expertise) | Indice cumpostu (modu Espertu) | vérifié | INFCOR 12108, 16367, 22460, 28927 |
| `bandeau_close_aria` | aria-label | Désactiver le mode Expertise | Disattivà u modu Espertu | flaggé | — (cf. note) |
| `op_geo` | texte | Géologie | Geulugia | vérifié | INFCOR 19035 |
| `op_hyd` | texte | Nappes | Falde | vérifié (flexion) | flexion: 17004 |
| `op_emag` | texte | Fond magnétique régional | Fondu magneticu regiunale | flaggé | — (cf. note) |
| `cbar_aria` | aria-label | Conditions live et indicateurs temps réel | Cundizione live è indicatori in tempu reale | vérifié | INFCOR 12508, 22684, 38022, 49184 |
| `cbar_toggle_aria` | aria-label | Déplier les détails conditions | Sviluppà i ditagli cundizione | vérifié (flexion) | INFCOR 12508, 48139 · flexion: 13865 |
| `cbar_summary_aria` | aria-label | Indicateurs temps réel résumé | Indicatori in tempu reale riassuntu | vérifié | INFCOR 22684, 38022, 38478, 49184 |
| `badge_kp_tt` | tooltip | Indice Kp d'activité géomagnétique (NOAA SWPC) | Indice Kp d'attività geomagnetica (NOAA SWPC) | flaggé | — (cf. note) |
| `badge_reseau_tt` | tooltip | Charge réseau électrique Corse (RTE eco2mix) | Carica di a reta elettrica corsa (RTE eco2mix) | vérifié (flexion) | INFCOR 8925, 38578 · flexion: 11092, 15567 |
| `badge_reseau` | texte | Réseau | Reta | vérifié | INFCOR 38578 |
| `badge_sb_tt` | tooltip | Statut connexion Supabase (contributions live) | Statu cunnessione Supabase (cuntribuzione live) | flaggé | — (cf. note) |
| `badge_meteo_tt` | tooltip | Activité orageuse (Blitzortung) | Attività timpurale (Blitzortung) | flaggé | — (cf. note) |
| `badge_meteo` | texte | Orage | Timpurale | flaggé | — (cf. note) |
| `badge_contribs_tt` | tooltip | Nombre de contributions terrain récentes (Supabase) | Numeru di cuntribuzione di terrenu recente (Supabase) | vérifié | INFCOR 12823, 30891, 38049, 48934 |
| `cond_solaire` | texte | Activité solaire | Attività sulare | vérifié | INFCOR 5242, 47541 |
| `cond_atmo` | texte | Conditions atmosphériques | Cundizione atmosferiche | vérifié (flexion) | INFCOR 12508 · flexion: 5057 |
| `cond_reseau` | texte | Réseau électrique | Reta elettrica | vérifié (flexion) | INFCOR 38578 · flexion: 15567 |
| `cond_contribs` | texte | Contributions terrain | Cuntribuzione di terrenu | vérifié | INFCOR 12823, 48934 |
| `cond_sum_solaire` | texte | vérification… | verificazione… | vérifié | INFCOR 51508 |
| `cond_key_bz` | texte | Bz (vent solaire) | Bz (ventu sulare) | vérifié | INFCOR 47541, 51457 |
| `cond_key_dens` | texte | Densité vent solaire | Densità di u ventu sulare | vérifié | INFCOR 13774, 47541, 51457 |
| `cond_key_proton` | texte | Flux proton | Flussu di prutoni | flaggé | — (cf. note) |
| `cond_key_corr` | texte | Correction utilisée | Currezzione aduprata | vérifié (flexion) | INFCOR 13320 · flexion: 1364 |
| `cond_key_acq` | texte | Acquisition EM | Acquisizione EM | flaggé | — (cf. note) |
| `cond_key_refrac` | texte | Réfractivité N | Rifrattività N | flaggé | — (cf. note) |
| `cond_key_orage` | texte | Activité orageuse | Attività timpurale | flaggé | — (cf. note) |
| `cond_key_charge` | texte | Charge Corse | Carica Corsica | vérifié | INFCOR 8925 |
| `acq_label` | texte | vérification… | verificazione… | vérifié | INFCOR 51508 |
| `sparkline_aria` | aria-label | Profil horaire de la charge electrique corse sur 24 h | Prufilu orariu di a carica elettrica corsa nant'à 24 ore | vérifié (flexion) | INFCOR 8925, 36448, 53553 · flexion: 11092, 15567 |
| `cert_header` | texte | Sources certifiées | Fonti certificate | vérifié (flexion) | INFCOR 18021 · flexion: 9712 |
| `cert_btn` | texte (1er nœud) | Télécharger les 30 fiches ANFR/EXEM | Scaricà e 30 schede ANFR/EXEM | vérifié (flexion) | INFCOR 42048 · flexion: 41980 |
| `cert_desc` | texte | Mesures certifiées de laboratoire (ANFR · EXEM) extraites des PDFs CartoRadio. Déjà visibles sur la carte en losanges colorés. | Misure certificate di laburatoriu (ANFR · EXEM) estratte da i PDF CartoRadio. Dighjà visibule nant'à a carta in rombi culuriti. | flaggé | — (cf. note) |
| `contrib_recent` | texte | Contributions récentes — base Supabase | Cuntribuzione recente — basa Supabase | vérifié | INFCOR 6195, 12823, 38049 |
| `legende_aria` | aria-label | Légende EM | Legenda EM | vérifié | INFCOR 25293 |
| `legende_toggle_aria` | aria-label | Légende EM (couches actives) | Legenda EM (strati attivi) | vérifié (flexion) | INFCOR 25293 · flexion: 5243, 46893 |
| `legende_content_aria` | aria-label | Légende EM | Legenda EM | vérifié | INFCOR 25293 |
| `legende_title` | texte | Légende EM (couches actives) | Legenda EM (strati attivi) | vérifié (flexion) | INFCOR 25293 · flexion: 5243, 46893 |
| `legende_empty` | texte | Activez « Champ composite » ou « Mesures EM » dans la sidebar pour afficher la légende. | Attivate « Campu cumpostu » o « Misure EM » in a colonna per affissà a legenda. | vérifié (flexion) | INFCOR 1565, 11948, 12108, 25293, 54907 · flexion: 5229, 28694 |
| `legends_ctx_aria` | aria-label | Légendes des couches contextuelles activées | Legende di i strati cuntestuali attivati | flaggé | — (cf. note) |
| `ms_naturel` | texte | N naturel IGRF+LCS1 | N naturale IGRF+LCS1 | vérifié | INFCOR 29937 |
| `ms_composite` | texte | N+H composite total | N+H cumpostu tutale | vérifié | INFCOR 12108, 50669 |
| `ms_delta` | texte | Δ anomalie terrain | Δ anumalia di terrenu | vérifié | INFCOR 3447, 48934 |
| `ms_reel` | texte | R — mesure réelle terrain | R — misura reale di terrenu | vérifié | INFCOR 28694, 38022, 48934 |
| `m_delta_hint` | texte | cliquez sur la carte | cliccate nant'à a carta | flaggé | — (cf. note) |
| `md_delta` | texte | Δ anomalie | Δ anumalia | vérifié | INFCOR 3447 |
| `md_note` | texte | Note modèle | Nota mudellu | vérifié | INFCOR 29238, 30746 |
| `md_hydro` | texte | Facteur hydro | Fattore idru | vérifié | INFCOR 17235, 20223 |
| `md_fh` | texte | Faisceaux hertziens | Fasci hertziani | flaggé | — (cf. note) |
| `md_score` | texte (1er nœud) | Score physique | Puntegiu fisicu | flaggé | — (cf. note) |
| `md_score_mesure` | texte | (mesuré) | (misuratu) | vérifié | INFCOR 28706 |
| `mpanel_close_tt` | tooltip | Fermer | Chjode | vérifié | INFCOR 707 |
| `cform_title` | texte | Contribution terrain | Cuntribuzione di terrenu | vérifié | INFCOR 12823, 48934 |
| `cform_epistemic` | texte | Contribution terrain — données à valeur indicative, non certifiées. | Cuntribuzione di terrenu — dati à valore indicativu, micca certificati. | vérifié (flexion) | INFCOR 12823, 22457, 48934, 51238 · flexion: 9712, 13532 |
| `cform_position` | texte | Cliquez sur la carte pour placer le point | Cliccate nant'à a carta per piazzà u puntu | flaggé | — (cf. note) |
| `cform_reposition` | texte | Repositionner le point | Ripusiziunà u puntu | flaggé | — (cf. note) |
| `cform_step1` | texte | Etape 1 — Contexte | Tappa 1 — Cuntestu | vérifié | INFCOR 12917, 48427 |
| `cform_step2` | texte | Etape 2 — Instrument | Tappa 2 — Strumentu | vérifié | INFCOR 23894, 48427 |
| `cform_step3` | texte | Etape 3 — Mesure | Tappa 3 — Misura | vérifié | INFCOR 28694, 48427 |
| `cform_step_cond` | texte | Conditions de mesure | Cundizione di misura | vérifié | INFCOR 12508, 28694 |
| `cform_step4` | texte | Etape 4 — Details interieur | Tappa 4 — Ditagli internu | vérifié (flexion) | INFCOR 23999, 48427 · flexion: 13865 |
| `cform_step5` | texte | Etape 5 — Observations | Tappa 5 — Osservazione | vérifié | INFCOR 31750, 48427 |
| `ctx_ext` | texte | Exterieur | Esternu | flaggé | — (cf. note) |
| `ctx_int` | texte | Interieur | Internu | vérifié | INFCOR 23999 |
| `cform_instr_label` | texte | Instrument de mesure | Strumentu di misura | vérifié | INFCOR 23894, 28694 |
| `optgroup_phone` | label (optgroup) | 📱 Smartphone (intégré) | 📱 Smartphone (integratu) | vérifié | INFCOR 23855 |
| `optgroup_ext` | label (optgroup) | 🔧 Capteur externe (~50-200€) | 🔧 Sensore esternu (~50-200€) | flaggé | — (cf. note) |
| `optgroup_cert` | label (optgroup) | ✅ Mesure certifiée | ✅ Misura certificata | vérifié (flexion) | INFCOR 28694 · flexion: 9712 |
| `optgroup_obs` | label (optgroup) | 👁 Observation | 👁 Osservazione | vérifié | INFCOR 31750 |
| `opt_mag` | texte | Magnétomètre téléphone (Physics Toolbox, Sensor Kinetics…) | Magnetometru telefonu (Physics Toolbox, Sensor Kinetics…) | vérifié | INFCOR 26263, 48687 |
| `opt_rssi` | texte | Signal réseau dBm (Network Cell Info, paramètres réseau) | Segnale reta dBm (Network Cell Info, parametri reta) | vérifié (flexion) | INFCOR 38578, 44196 · flexion: 32717 |
| `opt_wifi` | texte | Signal WiFi dBm (paramètres WiFi) | Segnale WiFi dBm (parametri WiFi) | vérifié (flexion) | INFCOR 44196 · flexion: 32717 |
| `opt_autre` | texte | Autre capteur dédié EMF | Altru sensore dedicatu EMF | flaggé | — (cf. note) |
| `opt_anfr` | texte | Mesure ANFR / labo accrédité | Misura ANFR / laburatoriu accreditatu | flaggé | — (cf. note) |
| `opt_observation` | texte | Observation visuelle / terrain | Osservazione visuale / terrenu | vérifié | INFCOR 31750, 48934, 52018 |
| `opt_ressenti` | texte | Ressenti subjectif (non instrumental) | Sensazione sugettiva (micca strumentale) | vérifié (flexion) | INFCOR 23698, 43235 · flexion: 47512 |
| `cform_val_label` | texte (1er nœud) | Valeur mesuree | Valore misuratu | vérifié | INFCOR 28706, 51238 |
| `cform_val_hint` | texte | — laissez vide si pas de chiffre | — lasciate biotu s'ellu ùn ci hè cifra | vérifié (flexion) | INFCOR 10309, 52207 · flexion: 25130 |
| `cform_val_ph` | placeholder | ex: 44800 | es: 44800 | vérifié | INFCOR  |
| `btn_native_mag` | texte | 📱 Capturer avec le magnétomètre du téléphone | 📱 Catturà cù u magnetometru di u telefonu | vérifié | INFCOR 9404, 26263, 48687 |
| `btn_csv_import` | texte | 📁 Importer un CSV de mesures (Phyphox, Physics Toolbox…) | 📁 Impurtà un CSV di misure (Phyphox, Physics Toolbox…) | vérifié (flexion) | INFCOR 21418 · flexion: 28694 |
| `cond_avion` | texte | Mode avion activé pendant la mesure | Modu aviò attivatu durante a misura | vérifié (flexion) | INFCOR 5581, 28694, 28927 · flexion: 5229 |
| `cond_usb` | texte | Charge USB débranchée | Carica USB staccata | vérifié (flexion) | INFCOR 8925 · flexion: 14869 |
| `cond_metal` | texte | Aucun objet métallique dans un rayon de 30 cm | Nisun ogettu metallicu in un raghju di 30 cm | vérifié | INFCOR 27969, 31524, 37685 |
| `cond_duree` | texte | Durée de stabilisation avant lecture (secondes) | Durata di stabilizazione prima di a lettura (secondi) | vérifié | INFCOR 15483, 25651, 46606 |
| `int_ctx_title` | texte | 🏠 Contexte intérieur | 🏠 Cuntestu internu | vérifié | INFCOR 12917, 23999 |
| `int_etage` | texte | Étage | Pianu | vérifié | INFCOR 34498 |
| `etage_soussol` | texte | Sous-sol / cave | Sottuterra / cantina | vérifié | INFCOR 8528, 45059 |
| `etage_rdc` | texte | Rez-de-chaussée | Pianterrenu | flaggé | — (cf. note) |
| `etage_1` | texte | 1er étage | 1u pianu | vérifié | INFCOR 34498 |
| `etage_2` | texte | 2ème étage et + | 2u pianu è + | vérifié | INFCOR 34498 |
| `int_materiaux` | texte (1er nœud) | Matériaux des murs | Materiali di i muri | vérifié (flexion) | INFCOR 27433 · flexion: 29540 |
| `int_materiaux_hint` | texte | (cochez tout ce qui s'applique) | (marcate tuttu ciò chì s'applica) | vérifié (flexion) | flexion: 26981 |
| `mat_portland` | texte | 🏗 Béton Portland | 🏗 Betone Portland | flaggé | — (cf. note) |
| `mat_chaux` | texte | 🏗 Béton chaux | 🏗 Betone calcina | flaggé | — (cf. note) |
| `mat_geo` | texte | 🏗 Géopolymère | 🏗 Geopolimeru | flaggé | — (cf. note) |
| `mat_fibre` | texte | 🔩 Béton fibré acier | 🔩 Betone fibratu acciaghju | flaggé | — (cf. note) |
| `mat_arme` | texte | 🏗 Béton armé dense | 🏗 Betone armatu densu | flaggé | — (cf. note) |
| `mat_parpaing` | texte | Parpaing | Bluchettu | flaggé | — (cf. note) |
| `mat_brique` | texte | 🧱 Brique | 🧱 Mattone | vérifié | INFCOR 27516 |
| `mat_platre` | texte | Plâtre | Ghjessu | vérifié | INFCOR 19235 |
| `mat_bois` | texte | 🌲 Bois/OSB | 🌲 Legnu/OSB | vérifié | INFCOR 25436 |
| `mat_pierre` | texte | 🪨 Pierre/granit | 🪨 Petra/granitu | vérifié | INFCOR 19747, 34557 |
| `mat_enduit` | texte | Enduit chaux | Intonacu calcina | flaggé | — (cf. note) |
| `mat_grillage` | texte | Enduit+grillage | Intonacu+rete | flaggé | — (cf. note) |
| `mat_laine` | texte | Laine de roche | Lana di petra | vérifié | INFCOR 25035, 34557 |
| `mat_peinture` | texte | 🛡 Peinture anti-ondes | 🛡 Pittura anti-onde | vérifié (flexion) | INFCOR 35328 · flexion: 31394 |
| `mat_cuivre` | texte | 🟤 Tuyauterie cuivre | 🟤 Tubatura ramu | vérifié | INFCOR 37771, 54019 |
| `mat_plomb` | texte | ⚫ Tuyauterie plomb (ancien) | ⚫ Tubatura piombu (anzianu) | vérifié | INFCOR 3482, 35098, 54019 |
| `mat_pvc` | texte | ⚪ Tuyauterie PVC/PER | ⚪ Tubatura PVC/PER | vérifié | INFCOR 54019 |
| `int_appareils` | texte | Appareils actifs au moment de la mesure | Apparechji attivi à u mumentu di a misura | vérifié (flexion) | INFCOR 28694 · flexion: 3547, 5243 |
| `app_wifi` | texte | 📶 WiFi routeur | 📶 Router WiFi | vérifié | INFCOR  |
| `app_micro` | texte | 📦 Micro-ondes | 📦 Micro-onde | vérifié (flexion) | flexion: 31394 |
| `app_induction` | texte | 🔥 Induction | 🔥 Induzzione | flaggé | — (cf. note) |
| `app_frigo` | texte | 🧊 Réfrigérateur | 🧊 Frigò | flaggé | — (cf. note) |
| `app_tableau` | texte | ⚡ Tableau électrique proche | ⚡ Quadru elettricu vicinu | vérifié | INFCOR 15567, 37356, 52167 |
| `cform_note_label` | texte (1er nœud) | Note | Nota | vérifié | INFCOR 30746 |
| `cform_note_hint` | texte | — conditions, observations, heure | — cundizione, osservazione, ora | vérifié | INFCOR 12508, 31750 |
| `cform_note_ph` | placeholder | ex: 22h, stable 3 min, fenêtre ouverte… | es: 22 ore, stabule 3 min, finestra aperta… | vérifié (flexion) | INFCOR 17730, 46551 · flexion: 3522 |
| `cform_privacy` | texte | Merci de ne pas inclure de données personnelles (nom, adresse, téléphone). | Ùn mittite micca dati persunali (nome, indirizzu, telefonu). | vérifié (flexion) | INFCOR 22508, 30925, 48687 · flexion: 13532, 28308, 34125 |
| `cform_protocole` | texte | ★★★ Mesure en protocole aveugle parallèle | ★★★ Misura in prutucollu cecu parallelu | vérifié | INFCOR 28694, 32702, 36705, 53289 |
| `btn_save` | texte | Enregistrer | Arregistrà | vérifié | INFCOR 4360 |
| `btn_cancel` | texte | Annuler | Annullà | vérifié | INFCOR 3272 |
| `geo_title` | texte | Mode Prospecteur terrain | Modu Pruspettore di terrenu | flaggé | — (cf. note) |
| `geo_badge` | texte | protocole terrain | prutucollu di terrenu | vérifié | INFCOR 36705, 48934 |
| `geo_checklist` | texte | Checklist mesure (5 min) | Lista di cuntrollu misura (5 min) | vérifié | INFCOR 12831, 25918, 28694 |
| `geo_check1` | texte | 1. App magnétomètre ouverte (Physics Toolbox / Sensor Kinetics) | 1. App magnetometru aperta (Physics Toolbox / Sensor Kinetics) | vérifié (flexion) | INFCOR 26263 · flexion: 3522 |
| `geo_check2` | texte | 2. Point Tellux cliqué — valeur IGRF et Indice notés | 2. Puntu Tellux cliccatu — valore IGRF è Indice nutati | flaggé | — (cf. note) |
| `geo_check3` | texte | 3. Téléphone à 1.5m du sol, bras tendu, loin de tout métal | 3. Telefonu à 1,5 m da u solu, bracciu tesu, luntanu da ogni metallu | flaggé | — (cf. note) |
| `geo_check4` | texte | 4. Valeur nT lue et comparée à l'estimation IGRF | 4. Valore nT lettu è paragunatu à a stima IGRF | vérifié | INFCOR 3544, 25408, 47027, 51238 |
| `geo_check5` | texte | 5. Mesure enregistrée via +Mesure (Δ calculé auto) | 5. Misura arregistrata via +Misura (Δ calculatu autumaticu) | flaggé | — (cf. note) |
| `geo_check6` | texte | 6. Bonus : grille 2m×2m pour cartographier gradient local | 6. Bonus : griglia 2m×2m per cartugrafià u gradiente lucale | flaggé | — (cf. note) |
| `geo_guide` | texte | Guide d'interprétation rapide | Guida d'interpretazione rapida | vérifié (flexion) | INFCOR 20295, 24013 · flexion: 37839 |
| `geo_export_rapport` | texte | 📋 Exporter rapport du point | 📋 Espurtà u raportu di u puntu | vérifié | INFCOR 16611, 37341, 38162 |
| `geo_export_csv` | texte | 📊 Export CSV contributions | 📊 Esportu CSV cuntribuzione | vérifié | INFCOR 12823, 16614 |
| `geo_hint` | texte | Cliquez d'abord sur un point de la carte pour générer le rapport. | Cliccate prima nant'à un puntu di a carta per generà u raportu. | flaggé | — (cf. note) |
| `geo_intl` | texte | Systèmes d'estimation RF — comparaison internationale | Sistemi di stima RF — paragone internaziunale | vérifié (flexion) | INFCOR 24218, 32672, 47027 · flexion: 44452 |
| `stat_rf` | texte | mesures RF (+ 2 BF) | misure RF (+ 2 BF) | vérifié (flexion) | flexion: 28694 |
| `stat_mediane` | texte | médiane V/m | mediana V/m | vérifié | INFCOR 27636 |
| `stat_depassement` | texte | dépassement légal | supranamentu legale | flaggé | — (cf. note) |
| `stat_10` | texte | mesures ≥ 10 V/m | misure ≥ 10 V/m | vérifié (flexion) | flexion: 28694 |
| `stat_5` | texte | mesures ≥ 5 V/m | misure ≥ 5 V/m | vérifié (flexion) | flexion: 28694 |
| `stat_1` | texte | mesures < 1 V/m | misure < 1 V/m | vérifié (flexion) | flexion: 28694 |
| `interp_titre` | texte | Ce que Tellux détecte ici | Ciò chì Tellux rileva quì | vérifié | INFCOR 39077 |
| `interp_activite` | texte | ACTIVITÉ GLOBALE | ATTIVITÀ GLUBALE | vérifié | INFCOR 5242, 19774 |
| `ib_naturel` | texte | Champ naturel de la Terre | Campu naturale di a Terra | vérifié | INFCOR 29937, 48913, 54907 |
| `ib_humain` | texte | Influence humaine | Influenza umana | vérifié (flexion) | INFCOR 22903 · flexion: 50798 |
| `ib_geo` | texte | Géologie & eau souterraine | Geulugia è acqua sutterranea | vérifié (flexion) | INFCOR 1052, 19035 · flexion: 47965 |
| `interp_advice` | texte | Que faire avec cette information ? | Chì fà cù st'infurmazione ? | vérifié | INFCOR 23253 |
| `interp_close_tt` | tooltip | Fermer | Chjode | vérifié | INFCOR 707 |
| `footer_brand` | texte | Tellux Corse | Tellux Corsica | vérifié | INFCOR  |
| `footer_em` | texte | Révéler l'invisible | Palesà l'invisibile | flaggé | — (cf. note) |
| `footer_suffix` | texte | · projet de recherche citoyen | · prugettu di ricerca citatinu | flaggé | — (cf. note) |
| `footer_app` | texte | Application carte | Applicazione carta | flaggé | — (cf. note) |
| `footer_mairies` | texte | Outils mairies | Strumenti merrie | vérifié (flexion) | flexion: 23894, 27910 |
| `footer_ressources` | texte | Ressources | Risorse | vérifié (flexion) | flexion: 39699 |
| `footer_mentions` | texte | Mentions légales & confidentialité | Menzione legale è cunfidenzialità | flaggé | — (cf. note) |
| `footer_transparence` | texte | Transparence | Trasparenza | vérifié | INFCOR 49808 |
| `gloss_title` | texte | Glossaire & guides | Glussariu è guide | vérifié (flexion) | INFCOR 19790 · flexion: 20295 |
| `gloss_close_aria` | aria-label | Fermer | Chjode | vérifié | INFCOR 707 |
| `gloss_tab_glossaire` | texte | Glossaire | Glussariu | vérifié | INFCOR 19790 |
| `gloss_tab_guides` | texte | Guides pratiques | Guide pratiche | vérifié (flexion) | flexion: 20295, 35825 |
| `gloss_search_ph` | placeholder | Rechercher un terme... | Circà un termine... | flaggé | — (cf. note) |
| `gloss_search_aria` | aria-label | Rechercher dans le glossaire | Circà in u glussariu | vérifié | INFCOR 10686, 19790 |

<!-- TABLE-END -->

---

## Chaînes différées (hors périmètre de cette passe)

<!-- DEFERRED-BEGIN -->

Conformément au brief (chrome UI seulement), les chaînes suivantes restent en FR sous
`?lang=co` et sont listées ici pour les passes futures :

### Prose scientifique / canon (ne pas traduire sans validation scientifique)
- **Panneau Méthodologie & Audit** : tout le contenu (protocole de mesure en aveugle,
  incertitudes documentées, données validées, références peer-reviewed, roadmap).
  Seul le titre du panneau est traduit.
- **Modal À propos** : paragraphes du corps (ce que Tellux n'est pas, position épistémique,
  sources de données, note pondérations). Seuls le titre et les intertitres h4 sont traduits.
- **Modal Mode Expertise** : les 2 paragraphes d'avertissement (pondérations w_M/w_RF/w_I).
- **Panneau Expertise** : paragraphe d'introduction, note « pondérations provisoires »,
  ligne « Écart IGRF/WMM », note d'usage du bandeau.
- **Disclaimer** : les 3 textes de blocs (champs EM, contribuer, données & vie privée) —
  nuances épistémiques et RGPD.
- **Sidebar** : `cat-header-text` et les 3 `subgroup-text` (distinction couches
  calcul/contexte — nuance épistémique).
- **Guide d'interprétation rapide** (mode Prospecteur) : seuils Δ nT et leur lecture.
- **acq-target-hint** (fenêtres d'acquisition EM).
- **Panneau stats corpus** : titre (corpus CartoRadio EXEM), titre des barres, ligne
  laboratoire/conformité, libellés de données (min/max V/m · communes).
- **Tooltips spécifications matériaux** (σ, µr, dB RF des 17 mat-chips) + les 3
  intertitres de familles de matériaux.
- **Entrées du glossaire** (titres + corps) et guides pratiques du drawer — contenu
  pédagogique ; seul le chrome du drawer est traduit.

### Textes légaux (ne pas traduire sans validation juridique)
- **Consentement RGPD** du formulaire contribution (`.rgpd-row`) + lien « En savoir plus ».
- **Consentement capteurs** (`.cap-consent`).
- **Note protocole aveugle** (explication sous la case ★★★).

### Chaînes générées en JS (différées — passe future si CO promu)
- `setStatus()` : « N antennes » du header (10 sites d'appel).
- `info()` : ~41 messages contextuels de la barre info.
- `alert()/confirm()` : 13 messages.
- Popups Leaflet (contenus dynamiques par couche), `updateLegendPanel()`,
  textes interprétation grand public (`ib-*-text`, `interp-conseil`,
  `interp-score-label`), résumés conditions (`cond-summary-*` post-boot),
  `#c-igrf-text`, `#csv-summary`, `#native-mag-status`, `#lightning-warn`,
  libellés dynamiques du toggle sidebar.
- Rapport de site imprimable (`exportTerrainReport`, HTML généré).

### SEO / meta (hors bêta)
- `<meta name="description">`, balises OpenGraph/Twitter — pas de version CO
  tant que la langue n'est pas publique.

<!-- DEFERRED-END -->

---

*Généré par `scripts/export_i18n_co_table.mjs` — feat/i18n-corsu-beta, 2026-06-10.*
