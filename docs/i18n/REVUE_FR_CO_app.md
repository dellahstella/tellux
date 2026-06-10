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
`node scripts/export_i18n_co_table.mjs` pour régénérer cette table.

| Clé | Type | FR (source de vérité) | CO (à réviser) |
|---|---|---|---|
| `page_title` | titre de page | Tellux — Révéler l'invisible · Cartographie électromagnétique Corse | Tellux — Palesà l'invisibile · Cartugrafia elettromagnetica Corsica |
| `skip_link` | texte | Aller au contenu | Andà à u cuntenutu |
| `h1_hidden` | texte | Tellux — Cartographie électromagnétique de la Corse | Tellux — Cartugrafia elettromagnetica di a Corsica |
| `disclaimer_title` | texte | Bienvenue sur Tellux | Benvenuti nant'à Tellux |
| `d_lead_em` | texte | Révéler l'invisible. | Palesà l'invisibile. |
| `d_lead_text` | texte | Un outil de cartographie électromagnétique de la Corse — conçu pour l'exploration scientifique et citoyenne du territoire. | Un attrezzu di cartugrafia elettromagnetica di a Corsica — cuncipitu per l'esplurazione scentifica è citatina di u territoriu. |
| `d_block_title_em` | texte | Champs électromagnétiques | Campi elettromagnetichi |
| `d_block_title_contrib` | texte | Contribuer | Cuntribuisce |
| `d_block_title_privacy` | texte | Données & vie privée | Dati è vita privata |
| `d_foot_text` | texte (1er nœud) | Tellux ne remplace pas une mesure professionnelle. | Tellux ùn rimpiazza micca una misura prufessiunale. |
| `d_foot_link` | texte | Méthodologie complète → | Metodulugia cumpleta → |
| `d_btn` | texte | Accéder à la carte | Accede à a carta |
| `logo_title` | tooltip | Tellux — Révéler l'invisible | Tellux — Palesà l'invisibile |
| `logo_aria` | aria-label | Retour à l'accueil Tellux | Ritornu à l'accolta Tellux |
| `tagline_em` | texte | Révéler l'invisible | Palesà l'invisibile |
| `tagline_suffix` | texte | · Corse | · Corsica |
| `nav_methodo` | texte | Méthodologie | Metodulugia |
| `nav_methodo_tt` | tooltip | Méthodologie & sources | Metodulugia è fonti |
| `nav_termes` | texte | Comprendre les termes | Capisce i termini |
| `nav_termes_tt` | tooltip | Glossaire & guides pratiques | Glussariu è guide pratiche |
| `nav_glossaire` | texte | Glossaire | Glussariu |
| `nav_glossaire_tt` | tooltip | Guide et glossaire technique complet (page publique) | Guida è glussariu tecnicu cumpletu (pagina publica) |
| `nav_apropos` | texte | À propos | À prupositu |
| `nav_apropos_tt` | tooltip | À propos du projet | À prupositu di u prugettu |
| `nav_patrimoine` | texte | Patrimoine (bêta) | Patrimoniu (beta) |
| `nav_patrimoine_tt` | tooltip | Cartographie patrimoniale de la Corse | Cartugrafia patrimuniale di a Corsica |
| `nav_mairies` | texte | Élu·e ? Outils mairie → | Elettu·a ? Strumenti merria → |
| `nav_mairies_tt` | tooltip | Outils administratifs pour les communes corses | Strumenti amministrativi per e cumune corse |
| `sb_dot_tt` | tooltip | Supabase connexion en cours… | Supabase cunnessione in corsu… |
| `sb_dot_aria` | aria-label | Statut Supabase | Statu Supabase |
| `hdr_status` | texte | chargement… | caricamentu… |
| `about_title` | texte | À propos de Tellux | À prupositu di Tellux |
| `about_h4_pas` | texte | Ce que Tellux n'est pas | Ciò chì Tellux ùn hè micca |
| `about_h4_episteme` | texte | Position épistémique | Pusizione epistemica |
| `about_h4_porteur` | texte | Porteur du projet | Purtadore di u prugettu |
| `about_h4_sources` | texte | Sources de données | Fonti di dati |
| `about_h4_contact` | texte | Contributions & contact | Cuntribuzione è cuntattu |
| `expert_modal_title` | texte | Mode Expertise | Modu Espertu |
| `expert_modal_cancel` | texte | Annuler | Annullà |
| `expert_modal_ok` | texte | Compris | Capitu |
| `contrib_title` | texte | Contribuer à Tellux | Cuntribuisce à Tellux |
| `contrib_close_aria` | aria-label | Fermer | Chjode |
| `ctab_obs` | texte | Observation | Osservazione |
| `ctab_mes` | texte | Mesure technique | Misura tecnica |
| `ctab_cap` | texte | Capteurs appareil | Sensori di l'apparechju |
| `obs_intro` | texte | Partagez une observation libre associée à un point sur la carte. Votre observation sera vérifiée avant publication. | Spartite un'osservazione libera ligata à un puntu nant'à a carta. A vostra osservazione sarà verificata prima d'esse publicata. |
| `obs_position` | texte | Cliquez d'abord sur la carte pour placer le point, puis rouvrez ce formulaire. Ou saisissez manuellement ci-dessous. | Cliccate prima nant'à a carta per piazzà u puntu, po riaprite stu formulariu. O entrite à manu quì sottu. |
| `obs_lat_ph` | placeholder | Latitude (ex: 42.308) | Latitudine (es: 42.308) |
| `obs_lon_ph` | placeholder | Longitude (ex: 9.150) | Longitudine (es: 9.150) |
| `obs_note_label` | texte | Que souhaitez-vous partager ? | Chì vulete sparte ? |
| `obs_note_ph` | placeholder | Ressenti, observation visuelle, contexte particulier… (300 caractères max) | Sensazione, osservazione visuale, cuntestu particulare… (300 caratteri max) |
| `obs_cancel` | texte | Annuler | Annullà |
| `obs_send` | texte | Envoyer | Mandà |
| `mes_avant` | texte | Avant de mesurer | Prima di misurà |
| `mes_precautions` | texte | Pour une lecture exploitable : activez le mode avion, posez le téléphone à plat pendant 30 secondes minimum, débranchez la charge USB, et écartez les objets métalliques (clés, montre, étui aimanté) à plus de 30 cm du capteur. | Per una lettura sfruttevule : attivate u modu aviò, pusate u telefonu à pianu durante 30 secondi à u minimu, staccate a carica USB, è alluntanate l'ogetti metallichi (chjave, mostra, astucciu magneticu) à più di 30 cm da u sensore. |
| `mes_pourquoi` | texte | Pourquoi ces précautions ? | Perchè ste precauzione ? |
| `mes_formulaire` | texte | Formulaire complet pour les utilisateurs équipés : magnétomètre smartphone (Phyphox), capteur externe (TriField, Cornet), RTL-SDR ou mesure ANFR certifiée. | Formulariu cumpletu per l'utilizatori equipati : magnetometru smartphone (Phyphox), sensore esternu (TriField, Cornet), RTL-SDR o misura ANFR certificata. |
| `mes_li_pointage` | texte | Pointage carte obligatoire (Corse uniquement) | Puntamentu carta ubligatoriu (Corsica sola) |
| `mes_li_saisie` | texte | Saisie instrument, valeur et unité | Inserimentu strumentu, valore è unità |
| `mes_li_csv` | texte | Import CSV Phyphox / Physics Toolbox | Importu CSV Phyphox / Physics Toolbox |
| `mes_li_ctx` | texte | Contexte intérieur optionnel (étage, matériaux murs, appareils actifs) | Cuntestu internu ozzionale (pianu, materiali muri, apparechji attivi) |
| `mes_cancel` | texte | Annuler | Annullà |
| `mes_open_form` | texte | Ouvrir le formulaire | Apre u formulariu |
| `cap_h3` | texte | Mesure automatisée — module en développement | Misura autumatizata — modulu in sviluppu |
| `cap_position_label` | texte | Position | Pusizione |
| `cap_geoloc` | texte | Utiliser ma position actuelle | Aduprà a mo pusizione attuale |
| `cap_small` | texte | Ou cliquez sur la carte avant d'ouvrir cette fenêtre. | O cliccate nant'à a carta prima d'apre sta finestra. |
| `cap_mag` | texte | Magnétomètre | Magnetometru |
| `cap_orient` | texte | Orientation | Orientazione |
| `cap_acc` | texte | Accéléromètre | Accelerometru |
| `cap_start` | texte | Démarrer l'enregistrement (10 s) | Principià l'arregistramentu (10 s) |
| `cap_stop` | texte | Arrêter | Piantà |
| `cap_results` | texte | Résultats | Risultati |
| `cap_mean` | texte | Moyenne | Media |
| `cap_std` | texte | Écart-type | Scartu tipu |
| `cap_n` | texte | Échantillons | Campioni |
| `cap_note_ph` | placeholder | Notes optionnelles (contexte, observations…) | Note ozzionale (cuntestu, osservazione…) |
| `cap_submit` | texte | Envoyer la mesure | Mandà a misura |
| `methodo_title` | texte | 🔬 Méthodologie & Audit | 🔬 Metodulugia è Audit |
| `mob_toggle_aria` | aria-label | Couches | Strati |
| `sidebar_toggle_aria` | aria-label | Réduire la sidebar | Riduce a colonna laterale |
| `sidebar_toggle_tt` | tooltip | Réduire la sidebar | Riduce a colonna laterale |
| `chips_aria` | aria-label | Filtre par domaine physique | Filtru per duminiu fisicu |
| `chip_label` | texte | Domaine | Duminiu |
| `chip_all` | texte | Tous | Tutti |
| `chip_statique` | texte | Statique | Staticu |
| `chip_statique_tt` | tooltip | Magnétique statique : géomagnétisme, anomalies crustales, susceptibilité lithologique | Magneticu staticu : geomagnetismu, anumalie crustale, suscettibilità litulogica |
| `chip_elf_tt` | tooltip | Magnétique basse fréquence ELF 50 Hz : lignes HT/BT, postes sources, production | Magneticu à bassa frequenza ELF 50 Hz : linee HT/BT, posti surgente, pruduzzione |
| `chip_rf_tt` | tooltip | Radiofréquences : antennes ANFR, émetteurs TDF | Radiofrequenze : antenne ANFR, emettitori TDF |
| `chip_ionisant` | texte | Ionisant | Ionizante |
| `chip_ionisant_tt` | tooltip | Rayonnement ionisant : radon, sites U/Th | Radiazione ionizante : radon, siti U/Th |
| `cat_modele` | texte | Modèle EM | Mudellu EM |
| `cat_anthropique` | texte | Sources anthropiques | Fonti antropiche |
| `cat_naturel` | texte | Contexte naturel | Cuntestu naturale |
| `subgroup_a` | texte | A. Substrat magnétique | A. Sustratu magneticu |
| `subgroup_b` | texte | B. Contexte territorial (géologie, hydro, forêts) | B. Cuntestu territuriale (geulugia, idrulugia, fureste) |
| `subgroup_c` | texte | C. Sites documentaires | C. Siti ducumentari |
| `lyr_hot` | texte | Champ composite | Campu cumpostu |
| `lyr_hot_tt` | tooltip | Champ composite estimé par le modèle Tellux (agrégation de 4 domaines physiques) | Campu cumpostu stimatu da u mudellu Tellux (agregazione di 4 duminii fisichi) |
| `lyr_con` | texte | Mesures EM | Misure EM |
| `lyr_con_tt` | tooltip | Mesures EM — contributions citoyennes + 30 fiches ANFR/EXEM certifiées (2024-2026) | Misure EM — cuntribuzione citatine + 30 schede ANFR/EXEM certificate (2024-2026) |
| `lyr_ant` | texte | Antennes ANFR + TDF | Antenne ANFR + TDF |
| `lyr_ant_tt` | tooltip | Antennes 2G/3G/4G/5G ANFR + émetteurs broadcast TDF | Antenne 2G/3G/4G/5G ANFR + emettitori broadcast TDF |
| `lyr_res` | texte | Réseau HT | Reta HT |
| `lyr_res_tt` | tooltip | Lignes et postes électriques haute tension (50 Hz) | Linee è posti elettrichi alta tensione (50 Hz) |
| `lyr_bt` | texte | Réseau BT | Reta BT |
| `lyr_bt_tt` | tooltip | Réseau basse tension BT — EDF SEI · zoom ≥ 12 | Reta bassa tensione BT — EDF SEI · zoom ≥ 12 |
| `lyr_prod` | texte | Sites de production | Siti di pruduzzione |
| `lyr_prod_tt` | tooltip | Centrales hydrauliques, éoliennes, diesel, TAC, biogaz, interconnexions | Centrale idrauliche, eoliane, diesel, TAC, biogas, intercunnessione |
| `lyr_postes` | texte | Postes sources EDF | Posti surgente EDF |
| `lyr_postes_tt` | tooltip | Postes sources EDF SEI (transformateurs HTB/HTA) — 21 postes OSM | Posti surgente EDF SEI (trasfurmatori HTB/HTA) — 21 posti OSM |
| `lyr_geo` | texte | Géologie BRGM | Geulugia BRGM |
| `lyr_geo_tt` | tooltip | Carte géologique BRGM — granite, schiste, calcaire | Carta geulogica BRGM — granitu, schistu, calcariu |
| `lyr_failles` | texte | Failles tectoniques | Faglie tettoniche |
| `lyr_failles_tt` | tooltip | Failles tectoniques BRGM — 8 failles principales (actives + quaternaires) | Faglie tettoniche BRGM — 8 faglie principale (attive + quaternarie) |
| `lyr_radon_tt` | tooltip | Potentiel radon géologique — zones ASNR cat. 2/3 | Putenziale radon geulogicu — zone ASNR cat. 2/3 |
| `lyr_emag` | texte | Fond magnétique régional | Fondu magneticu regiunale |
| `lyr_emag_tt` | tooltip | Fond magnétique régional NOAA EMAG2v3 — anomalies du socle profond Corse | Fondu magneticu regiunale NOAA EMAG2v3 — anumalie di u zoccalu prufondu corsu |
| `lyr_cav` | texte | Cavités | Cavità |
| `lyr_cav_tt` | tooltip | Cavités souterraines — grottes, mines, karst (BRGM) | Cavità sutterranee — grotte, mine, karst (BRGM) |
| `lyr_therm` | texte | Émergences thermales | Surgenti termali |
| `lyr_therm_tt` | tooltip | Émergences thermales — observations de surface, marqueurs de failles actives | Surgenti termali — osservazione di superficia, marcatori di faglie attive |
| `lyr_hyd` | texte | Hydrographie | Idrugrafia |
| `lyr_hyd_tt` | tooltip | Nappes et cours d'eau souterrains (BRGM REMNAPPE) — couche visuelle ; le calcul utilise un dataset distinct | Falde è corsi d'acqua sutterranei (BRGM REMNAPPE) — stratu visuale ; u calculu adopra un dataset distintu |
| `lyr_foret` | texte | Forêts publiques | Fureste publiche |
| `lyr_foret_tt` | tooltip | Forêts publiques ONF via WMS IGN Géoplateforme — couche visuelle niveau A (pas de modulation calcul). BD Forêt V2 complète non disponible en WMS public. | Fureste publiche ONF via WMS IGN Géoplateforme — stratu visuale livellu A (nisuna mudulazione di calculu). BD Forêt V2 cumpleta micca dispunibule in WMS publicu. |
| `lyr_uth` | texte | Sites U/Th à mesurer | Siti U/Th da misurà |
| `lyr_uth_tt` | tooltip | Sites U/Th à mesurer — catalogue de sites candidats à des mesures radiométriques (doses non mesurées, sources documentaires BRGM ou analogies géologiques) | Siti U/Th da misurà — catalogu di siti candidati à misure radiometriche (dose micca misurate, fonti ducumentarie BRGM o analugie geulogiche) |
| `lyr_remarq` | texte | Sites géophysiques remarquables | Siti geofisichi rimarchevuli |
| `lyr_remarq_tt` | tooltip | Sites géophysiques remarquables — 10 sites ponctuels à signature singulière (mines historiques, serpentinites ophiolitiques, surveillance radiologique marine). Données documentaires, mesures in situ souvent requises. | Siti geofisichi rimarchevuli — 10 siti puntuali à signatura singulare (mine storiche, serpentinite ofiolitiche, surviglianza radiulogica marina). Dati ducumentarii, misure in situ à spessu richieste. |
| `lyr_crustal` | texte | Anomalies de référence (mondiales) | Anumalie di riferenza (mundiale) |
| `lyr_crustal_tt` | tooltip | 5 anomalies magnétiques crustales mondiales de référence (cratères d'impact + BIF) — opt-in, comparaison locale/mondiale | 5 anumalie magnetiche crustale mundiale di riferenza (crateri d'impattu + BIF) — opt-in, paragone lucale/mundiale |
| `btn_expert_aria` | aria-label | Outils experts | Strumenti esperti |
| `btn_expert` | texte | Outils experts | Strumenti esperti |
| `btn_share_aria` | aria-label | Partager la vue | Sparte a vista |
| `btn_share` | texte | Partager la vue | Sparte a vista |
| `xp_header` | texte | ⚙ Indice composite | ⚙ Indice cumpostu |
| `xp_lastpoint` | texte | sur le dernier point analysé ◆ | nant'à l'ultimu puntu analizatu ◆ |
| `xp_stats` | texte | Statistiques du modèle | Statistiche di u mudellu |
| `xp_anfr_loading` | texte | chargement… | caricamentu… |
| `xp_reset` | texte | Réinitialiser | Rimette à zeru |
| `xp_csv` | texte | ↓ CSV expert | ↓ CSV espertu |
| `xp_off` | texte | Désactiver ✕ | Disattivà ✕ |
| `bandeau_label` | texte | Indice composite (mode Expertise) | Indice cumpostu (modu Espertu) |
| `bandeau_close_aria` | aria-label | Désactiver le mode Expertise | Disattivà u modu Espertu |
| `op_geo` | texte | Géologie | Geulugia |
| `op_hyd` | texte | Nappes | Falde |
| `op_emag` | texte | Fond magnétique régional | Fondu magneticu regiunale |
| `cbar_aria` | aria-label | Conditions live et indicateurs temps réel | Cundizione live è indicatori in tempu reale |
| `cbar_toggle_aria` | aria-label | Déplier les détails conditions | Sviluppà i ditagli cundizione |
| `cbar_summary_aria` | aria-label | Indicateurs temps réel résumé | Indicatori in tempu reale riassuntu |
| `badge_kp_tt` | tooltip | Indice Kp d'activité géomagnétique (NOAA SWPC) | Indice Kp d'attività geomagnetica (NOAA SWPC) |
| `badge_reseau_tt` | tooltip | Charge réseau électrique Corse (RTE eco2mix) | Carica di a reta elettrica corsa (RTE eco2mix) |
| `badge_reseau` | texte | Réseau | Reta |
| `badge_sb_tt` | tooltip | Statut connexion Supabase (contributions live) | Statu cunnessione Supabase (cuntribuzione live) |
| `badge_meteo_tt` | tooltip | Activité orageuse (Blitzortung) | Attività timpurale (Blitzortung) |
| `badge_meteo` | texte | Orage | Timpurale |
| `badge_contribs_tt` | tooltip | Nombre de contributions terrain récentes (Supabase) | Numeru di cuntribuzione di terrenu recente (Supabase) |
| `cond_solaire` | texte | Activité solaire | Attività sulare |
| `cond_atmo` | texte | Conditions atmosphériques | Cundizione atmosferiche |
| `cond_reseau` | texte | Réseau électrique | Reta elettrica |
| `cond_contribs` | texte | Contributions terrain | Cuntribuzione di terrenu |
| `cond_sum_solaire` | texte | vérification… | verificazione… |
| `cond_key_bz` | texte | Bz (vent solaire) | Bz (ventu sulare) |
| `cond_key_dens` | texte | Densité vent solaire | Densità di u ventu sulare |
| `cond_key_proton` | texte | Flux proton | Flussu di prutoni |
| `cond_key_corr` | texte | Correction utilisée | Currezzione aduprata |
| `cond_key_acq` | texte | Acquisition EM | Acquisizione EM |
| `cond_key_refrac` | texte | Réfractivité N | Rifrattività N |
| `cond_key_orage` | texte | Activité orageuse | Attività timpurale |
| `cond_key_charge` | texte | Charge Corse | Carica Corsica |
| `acq_label` | texte | vérification… | verificazione… |
| `sparkline_aria` | aria-label | Profil horaire de la charge electrique corse sur 24 h | Prufilu orariu di a carica elettrica corsa nant'à 24 ore |
| `cert_header` | texte | Sources certifiées | Fonti certificate |
| `cert_btn` | texte (1er nœud) | Télécharger les 30 fiches ANFR/EXEM | Scaricà e 30 schede ANFR/EXEM |
| `cert_desc` | texte | Mesures certifiées de laboratoire (ANFR · EXEM) extraites des PDFs CartoRadio. Déjà visibles sur la carte en losanges colorés. | Misure certificate di laburatoriu (ANFR · EXEM) estratte da i PDF CartoRadio. Dighjà visibule nant'à a carta in rombi culuriti. |
| `contrib_recent` | texte | Contributions récentes — base Supabase | Cuntribuzione recente — basa Supabase |
| `legende_aria` | aria-label | Légende EM | Legenda EM |
| `legende_toggle_aria` | aria-label | Légende EM (couches actives) | Legenda EM (strati attivi) |
| `legende_content_aria` | aria-label | Légende EM | Legenda EM |
| `legende_title` | texte | Légende EM (couches actives) | Legenda EM (strati attivi) |
| `legende_empty` | texte | Activez « Champ composite » ou « Mesures EM » dans la sidebar pour afficher la légende. | Attivate « Campu cumpostu » o « Misure EM » in a colonna per affissà a legenda. |
| `legends_ctx_aria` | aria-label | Légendes des couches contextuelles activées | Legende di i strati cuntestuali attivati |
| `ms_naturel` | texte | N naturel IGRF+LCS1 | N naturale IGRF+LCS1 |
| `ms_composite` | texte | N+H composite total | N+H cumpostu tutale |
| `ms_delta` | texte | Δ anomalie terrain | Δ anumalia di terrenu |
| `ms_reel` | texte | R — mesure réelle terrain | R — misura reale di terrenu |
| `m_delta_hint` | texte | cliquez sur la carte | cliccate nant'à a carta |
| `md_delta` | texte | Δ anomalie | Δ anumalia |
| `md_note` | texte | Note modèle | Nota mudellu |
| `md_hydro` | texte | Facteur hydro | Fattore idru |
| `md_fh` | texte | Faisceaux hertziens | Fasci hertziani |
| `md_score` | texte (1er nœud) | Score physique | Puntegiu fisicu |
| `md_score_mesure` | texte | (mesuré) | (misuratu) |
| `mpanel_close_tt` | tooltip | Fermer | Chjode |
| `cform_title` | texte | Contribution terrain | Cuntribuzione di terrenu |
| `cform_epistemic` | texte | Contribution terrain — données à valeur indicative, non certifiées. | Cuntribuzione di terrenu — dati à valore indicativu, micca certificati. |
| `cform_position` | texte | Cliquez sur la carte pour placer le point | Cliccate nant'à a carta per piazzà u puntu |
| `cform_reposition` | texte | Repositionner le point | Ripusiziunà u puntu |
| `cform_step1` | texte | Etape 1 — Contexte | Tappa 1 — Cuntestu |
| `cform_step2` | texte | Etape 2 — Instrument | Tappa 2 — Strumentu |
| `cform_step3` | texte | Etape 3 — Mesure | Tappa 3 — Misura |
| `cform_step_cond` | texte | Conditions de mesure | Cundizione di misura |
| `cform_step4` | texte | Etape 4 — Details interieur | Tappa 4 — Ditagli internu |
| `cform_step5` | texte | Etape 5 — Observations | Tappa 5 — Osservazione |
| `ctx_ext` | texte | Exterieur | Esternu |
| `ctx_int` | texte | Interieur | Internu |
| `cform_instr_label` | texte | Instrument de mesure | Strumentu di misura |
| `optgroup_phone` | label (optgroup) | 📱 Smartphone (intégré) | 📱 Smartphone (integratu) |
| `optgroup_ext` | label (optgroup) | 🔧 Capteur externe (~50-200€) | 🔧 Sensore esternu (~50-200€) |
| `optgroup_cert` | label (optgroup) | ✅ Mesure certifiée | ✅ Misura certificata |
| `optgroup_obs` | label (optgroup) | 👁 Observation | 👁 Osservazione |
| `opt_mag` | texte | Magnétomètre téléphone (Physics Toolbox, Sensor Kinetics…) | Magnetometru telefonu (Physics Toolbox, Sensor Kinetics…) |
| `opt_rssi` | texte | Signal réseau dBm (Network Cell Info, paramètres réseau) | Segnale reta dBm (Network Cell Info, parametri reta) |
| `opt_wifi` | texte | Signal WiFi dBm (paramètres WiFi) | Segnale WiFi dBm (parametri WiFi) |
| `opt_autre` | texte | Autre capteur dédié EMF | Altru sensore dedicatu EMF |
| `opt_anfr` | texte | Mesure ANFR / labo accrédité | Misura ANFR / laburatoriu accreditatu |
| `opt_observation` | texte | Observation visuelle / terrain | Osservazione visuale / terrenu |
| `opt_ressenti` | texte | Ressenti subjectif (non instrumental) | Sensazione sugettiva (micca strumentale) |
| `cform_val_label` | texte (1er nœud) | Valeur mesuree | Valore misuratu |
| `cform_val_hint` | texte | — laissez vide si pas de chiffre | — lasciate biotu s'ellu ùn ci hè cifra |
| `cform_val_ph` | placeholder | ex: 44800 | es: 44800 |
| `btn_native_mag` | texte | 📱 Capturer avec le magnétomètre du téléphone | 📱 Catturà cù u magnetometru di u telefonu |
| `btn_csv_import` | texte | 📁 Importer un CSV de mesures (Phyphox, Physics Toolbox…) | 📁 Impurtà un CSV di misure (Phyphox, Physics Toolbox…) |
| `cond_avion` | texte | Mode avion activé pendant la mesure | Modu aviò attivatu durante a misura |
| `cond_usb` | texte | Charge USB débranchée | Carica USB staccata |
| `cond_metal` | texte | Aucun objet métallique dans un rayon de 30 cm | Nisun ogettu metallicu in un raghju di 30 cm |
| `cond_duree` | texte | Durée de stabilisation avant lecture (secondes) | Durata di stabilizazione prima di a lettura (secondi) |
| `int_ctx_title` | texte | 🏠 Contexte intérieur | 🏠 Cuntestu internu |
| `int_etage` | texte | Étage | Pianu |
| `etage_soussol` | texte | Sous-sol / cave | Sottuterra / cantina |
| `etage_rdc` | texte | Rez-de-chaussée | Pianterrenu |
| `etage_1` | texte | 1er étage | 1u pianu |
| `etage_2` | texte | 2ème étage et + | 2u pianu è + |
| `int_materiaux` | texte (1er nœud) | Matériaux des murs | Materiali di i muri |
| `int_materiaux_hint` | texte | (cochez tout ce qui s'applique) | (marcate tuttu ciò chì s'applica) |
| `mat_portland` | texte | 🏗 Béton Portland | 🏗 Betone Portland |
| `mat_chaux` | texte | 🏗 Béton chaux | 🏗 Betone calcina |
| `mat_geo` | texte | 🏗 Géopolymère | 🏗 Geopolimeru |
| `mat_fibre` | texte | 🔩 Béton fibré acier | 🔩 Betone fibratu acciaghju |
| `mat_arme` | texte | 🏗 Béton armé dense | 🏗 Betone armatu densu |
| `mat_parpaing` | texte | Parpaing | Bluchettu |
| `mat_brique` | texte | 🧱 Brique | 🧱 Mattone |
| `mat_platre` | texte | Plâtre | Ghjessu |
| `mat_bois` | texte | 🌲 Bois/OSB | 🌲 Legnu/OSB |
| `mat_pierre` | texte | 🪨 Pierre/granit | 🪨 Petra/granitu |
| `mat_enduit` | texte | Enduit chaux | Intonacu calcina |
| `mat_grillage` | texte | Enduit+grillage | Intonacu+rete |
| `mat_laine` | texte | Laine de roche | Lana di petra |
| `mat_peinture` | texte | 🛡 Peinture anti-ondes | 🛡 Pittura anti-onde |
| `mat_cuivre` | texte | 🟤 Tuyauterie cuivre | 🟤 Tubatura ramu |
| `mat_plomb` | texte | ⚫ Tuyauterie plomb (ancien) | ⚫ Tubatura piombu (anzianu) |
| `mat_pvc` | texte | ⚪ Tuyauterie PVC/PER | ⚪ Tubatura PVC/PER |
| `int_appareils` | texte | Appareils actifs au moment de la mesure | Apparechji attivi à u mumentu di a misura |
| `app_wifi` | texte | 📶 WiFi routeur | 📶 Router WiFi |
| `app_micro` | texte | 📦 Micro-ondes | 📦 Micro-onde |
| `app_induction` | texte | 🔥 Induction | 🔥 Induzzione |
| `app_frigo` | texte | 🧊 Réfrigérateur | 🧊 Frigò |
| `app_tableau` | texte | ⚡ Tableau électrique proche | ⚡ Quadru elettricu vicinu |
| `cform_note_label` | texte (1er nœud) | Note | Nota |
| `cform_note_hint` | texte | — conditions, observations, heure | — cundizione, osservazione, ora |
| `cform_note_ph` | placeholder | ex: 22h, stable 3 min, fenêtre ouverte… | es: 22 ore, stabule 3 min, finestra aperta… |
| `cform_privacy` | texte | Merci de ne pas inclure de données personnelles (nom, adresse, téléphone). | Ùn mittite micca dati persunali (nome, indirizzu, telefonu). |
| `cform_protocole` | texte | ★★★ Mesure en protocole aveugle parallèle | ★★★ Misura in prutucollu cecu parallelu |
| `btn_save` | texte | Enregistrer | Arregistrà |
| `btn_cancel` | texte | Annuler | Annullà |
| `geo_title` | texte | Mode Prospecteur terrain | Modu Pruspettore di terrenu |
| `geo_badge` | texte | protocole terrain | prutucollu di terrenu |
| `geo_checklist` | texte | Checklist mesure (5 min) | Lista di cuntrollu misura (5 min) |
| `geo_check1` | texte | 1. App magnétomètre ouverte (Physics Toolbox / Sensor Kinetics) | 1. App magnetometru aperta (Physics Toolbox / Sensor Kinetics) |
| `geo_check2` | texte | 2. Point Tellux cliqué — valeur IGRF et Indice notés | 2. Puntu Tellux cliccatu — valore IGRF è Indice nutati |
| `geo_check3` | texte | 3. Téléphone à 1.5m du sol, bras tendu, loin de tout métal | 3. Telefonu à 1,5 m da u solu, bracciu tesu, luntanu da ogni metallu |
| `geo_check4` | texte | 4. Valeur nT lue et comparée à l'estimation IGRF | 4. Valore nT lettu è paragunatu à a stima IGRF |
| `geo_check5` | texte | 5. Mesure enregistrée via +Mesure (Δ calculé auto) | 5. Misura arregistrata via +Misura (Δ calculatu autumaticu) |
| `geo_check6` | texte | 6. Bonus : grille 2m×2m pour cartographier gradient local | 6. Bonus : griglia 2m×2m per cartugrafià u gradiente lucale |
| `geo_guide` | texte | Guide d'interprétation rapide | Guida d'interpretazione rapida |
| `geo_export_rapport` | texte | 📋 Exporter rapport du point | 📋 Espurtà u raportu di u puntu |
| `geo_export_csv` | texte | 📊 Export CSV contributions | 📊 Esportu CSV cuntribuzione |
| `geo_hint` | texte | Cliquez d'abord sur un point de la carte pour générer le rapport. | Cliccate prima nant'à un puntu di a carta per generà u raportu. |
| `geo_intl` | texte | Systèmes d'estimation RF — comparaison internationale | Sistemi di stima RF — paragone internaziunale |
| `stat_rf` | texte | mesures RF (+ 2 BF) | misure RF (+ 2 BF) |
| `stat_mediane` | texte | médiane V/m | mediana V/m |
| `stat_depassement` | texte | dépassement légal | supranamentu legale |
| `stat_10` | texte | mesures ≥ 10 V/m | misure ≥ 10 V/m |
| `stat_5` | texte | mesures ≥ 5 V/m | misure ≥ 5 V/m |
| `stat_1` | texte | mesures < 1 V/m | misure < 1 V/m |
| `interp_titre` | texte | Ce que Tellux détecte ici | Ciò chì Tellux rileva quì |
| `interp_activite` | texte | ACTIVITÉ GLOBALE | ATTIVITÀ GLUBALE |
| `ib_naturel` | texte | Champ naturel de la Terre | Campu naturale di a Terra |
| `ib_humain` | texte | Influence humaine | Influenza umana |
| `ib_geo` | texte | Géologie & eau souterraine | Geulugia è acqua sutterranea |
| `interp_advice` | texte | Que faire avec cette information ? | Chì fà cù st'infurmazione ? |
| `interp_close_tt` | tooltip | Fermer | Chjode |
| `footer_brand` | texte | Tellux Corse | Tellux Corsica |
| `footer_em` | texte | Révéler l'invisible | Palesà l'invisibile |
| `footer_suffix` | texte | · projet de recherche citoyen | · prugettu di ricerca citatinu |
| `footer_app` | texte | Application carte | Applicazione carta |
| `footer_mairies` | texte | Outils mairies | Strumenti merrie |
| `footer_ressources` | texte | Ressources | Risorse |
| `footer_mentions` | texte | Mentions légales & confidentialité | Menzione legale è cunfidenzialità |
| `footer_transparence` | texte | Transparence | Trasparenza |
| `gloss_title` | texte | Glossaire & guides | Glussariu è guide |
| `gloss_close_aria` | aria-label | Fermer | Chjode |
| `gloss_tab_glossaire` | texte | Glossaire | Glussariu |
| `gloss_tab_guides` | texte | Guides pratiques | Guide pratiche |
| `gloss_search_ph` | placeholder | Rechercher un terme... | Circà un termine... |
| `gloss_search_aria` | aria-label | Rechercher dans le glossaire | Circà in u glussariu |

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
