# 🌙⚡ Tellux – Cartographie EM Corse

**Outil open-source de cartographie et de visualisation des champs électromagnétiques en Corse.**

## 🎯 Vue d'ensemble

**Tellux** permet aux habitants, mairies et institutions de Corse de visualiser :

- **4 domaines physiques EM** : magnétique statique (IGRF + anomalies crustales), magnétique basse fréquence (ELF), radiofréquences (ANFR + radiodiffusion TDF), ionisant (cosmique altimétrique + radon)
- **Contexte géologique et environnemental** : substrat, failles, hydrographie, susceptibilité magnétique
- **Patrimoine** : 196 églises romanes (Moracchini-Mazel) et 137 sites mégalithiques (Cesari & Magdeleine) en couche de contexte
- **Champ composite estimé** : synthèse multi-domaines avec mode Expertise cadré épistémiquement
- **Contributions citoyennes** : observations et mesures terrain (Trifield TF2, applications mobiles)

**Objectif** : outil cartographique rigoureux, sans équivalent international identifié, pour la recherche, les politiques publiques et la sensibilisation en Corse.

---

## ✨ Fonctionnalités

### Carte interactive (Leaflet)
- Fond IGN Plan V2 (Géoplateforme), zoom jusqu'au niveau rue (maxZoom 20)
- 3 groupes de couches thématiques : Modèle EM, Sources anthropiques, Contexte naturel
- Popups avec détail par domaine physique, coordonnées GPS, sources et notes épistémiques

### Modèle physique
- Altimétrie réelle via IGN RGE Alti pour la composante cosmique
- Classification officielle radon par commune (décret 2018-434, IRSN)
- 10 émetteurs TDF radiodiffusion avec PAR estimées
- Incertitudes, niveaux de confiance et zones gelées documentés

### Mode Expertise
- Pondérations ajustables par domaine (curseurs)
- Constantes balisées GELÉ-001 (en attente relecture physicien tiers)
- Export CSV enrichi, partage URL par hash

### Contributions citoyennes
- Saisie de mesures terrain géolocalisées
- Modal 3 onglets : Observation, Mesure terrain, Capteurs appareil

## 📞 Contact

**Porteur** : Lucas IANNACCONE (SARL Stella Canis Majoris)  
**Email** : [stelladluca@proton.me]  
**GitHub** : https://github.com/dellahstella/tellux  
