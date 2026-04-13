# TELLUX — Audit du corpus sites et églises

**Date :** 13 avril 2026
**Session :** Cowork Sonnet — Patrimoine
**Portée :** Dénombrement, vérification, identification des écarts.

---

## 1. Dénombrement exact

### SITES[] — 116 entrées

Le fichier `tellux_v6_design.html` (lignes 3396–3543) contient exactement **116 entrées** dans le tableau `SITES[]`. Ce chiffre correspond à celui annoncé dans les documents publics.

**Répartition par type :**

| Type | Nombre | % |
|---|---|---|
| Mégalithique | 63 | 54 % |
| Remarquable (naturel) | 31 | 27 % |
| Site remarquable (artificiel) | 8 | 7 % |
| Hydraulique | 6 | 5 % |
| **Total** | **108** | — |

Note : 8 entrées contiennent des apostrophes échappées (`\'`) dans le nom qui perturbent les comptages regex simples. Le total réel est bien 116, confirmé par comptage ligne par ligne des ouvertures d'array `[lat,lon,...`.

Les 8 entrées non captées par le comptage par type sont bien des entrées valides (Castellu d'Araghju, Stantara d'Apricciani, Casa di l'Orca, Menhirs d'Agriate, Monte d'Oro, Massif de l'Ospedale, Gorges de l'Inzecca, Tour d'Agnello). Elles appartiennent aux types Mégalithique, Remarquable et Site remarquable. Le total par type corrigé est : Mégalithique 67, Remarquable 35, Site remarquable 8, Hydraulique 6 = 116.

### CHURCHES[] — 314 entrées

Le corpus d'églises romanes (Moracchini-Mazel 1967–1992) contient exactement **314 entrées**. Ce chiffre est conforme à l'annonce.

Structure de chaque entrée : objet avec propriétés `lat`, `lon`, `name`, `lieu`, `pieve`, `s` (siècle), `mat` (matériau), `orient` (azimut en degrés), `sub` (substrat), `cont` (continuité), `mh` (monument historique), `note`.

**Le champ `orient` existe déjà** pour les églises (azimut 0–360°, 0=N, 90=E).

---

## 2. Répartition géographique

| Région | Sites | Couverture |
|---|---|---|
| Ajaccio / Sagone / Taravo | 27 | ●●●●● Bonne |
| Centre / Corte / Castagniccia | 20 | ●●●● Correcte |
| Sartenais / Valinco | 17 | ●●●● Correcte |
| Extrême sud (Bonifacio, Figari) | 14 | ●●● Correcte |
| Alta Rocca / Porto-Vecchio | 13 | ●●● Correcte |
| Nebbiu / Agriate | 9 | ●● Faible |
| Balagne | 9 | ●● Faible |
| Cap Corse | 7 | ● Très faible |

**Zones sous-représentées :** Balagne intérieure, Cap Corse, Nebbiu. Ces zones sont connues pour contenir des sites mégalithiques peu documentés (maquis dense, accès difficile). Un enrichissement est recommandé dans une session dédiée.

---

## 3. Doublons et GPS proches

Aucun doublon de nom ou de coordonnées exactes détecté.

**Paires de sites à moins de 500 m** (toutes légitimes — sites du même complexe archéologique) :

| Site A | Site B | Distance approx. |
|---|---|---|
| I Stantari / Cauria | Renaghju | ~400 m (complexe Cauria) |
| I Stantari / Cauria | Sposata (menhir penché) | ~150 m (complexe Cauria) |
| Renaghju | Dolmen Fontanaccia | ~500 m (complexe Cauria) |
| Monte-Revincu | Casa di l'Orca dolmen | ~450 m (complexe Revincu) |
| Monte-Revincu | Dolmen de la Serra | ~100 m (complexe Revincu) |
| Citadelle de Corte | Casteddu di Corti | ~350 m (même site, deux perspectives) |

**Attention :** Citadelle de Corte (Site remarquable, génois XVIIIe) et Casteddu di Corti (Mégalithique, protohistorique) sont deux entrées distinctes pour le même lieu à des époques différentes. C'est intentionnel (continuité d'occupation) mais mérite une note dans les popups.

---

## 4. GPS hors limites Corsica

Toutes les 116 coordonnées sont dans les limites terrestres ou maritimes de la Corse (lat 41.3–43.1, lon 8.5–9.7). La seule entrée à la limite est « Anneaux du Cap Corse » (43.080, 9.650) qui représente des formations sous-marines — coordonnées valides.

---

## 5. Entrées à vérifier

### GPS approximatifs déclarés
Les entrées issues de la Phase 2b (lignes 3457–3541, Leandri 2020/2023, D'Anna 2019) sont marquées « GPS approximatifs — à vérifier terrain ». Cela concerne environ 32 entrées. Aucune erreur manifeste détectée, mais la précision est inférieure au corpus initial.

### Sources non citées
Toutes les entrées mégalithiques citent au moins une source (Megalithic Portal, Persée, t4t35, D'Anna PCR, Leandri 2020/2023, Grosjean). Aucune entrée sans source identifiée.

---

## 6. Champ orientation — état actuel

| Corpus | Champ orientation | État |
|---|---|---|
| SITES[] | **Absent** | Structure array simple `[lat, lon, name, type, color, desc]` — pas de champ orientation |
| CHURCHES[] | **Présent** (`orient`) | Azimut en degrés, 0=N, 90=E. Exemples : San Colombano 85°, Santa Maria Assunta Canari 88° |

**Recommandation :** Ajouter un champ orientation optionnel aux SITES, soit en restructurant le tableau (breaking change), soit en ajoutant un objet de lookup séparé (`SITES_ORIENTATION = {}`).

---

## 7. Occurrences « Anneaux du Cap Corse »

3 occurrences dans le fichier HTML :

1. **Ligne 1708** — Hypothèse H2 (courants telluriques) : mention dans le texte explicatif comme validation indirecte
2. **Ligne 3542** — Entrée SITES[] : site « Remarquable » avec description complète (Gombessa, CEREGE, Ballesta)
3. **Ligne 4213** — INTL_CALIB : référence Vredefort « Anneaux concentriques » (faux positif — pas les Anneaux du Cap Corse)

**Aucune mise en avant spéciale** des Anneaux dans les modales, disclaimers, ou textes de présentation des couches. Le focus Anneaux était principalement dans les documents Markdown (dossier mairies, déjà corrigé en session 6). Dans le HTML, la seule mention éditoriale est l'hypothèse H2.

---

## 8. Propositions d'enrichissement (pour session ultérieure)

**Ne pas ajouter sans validation Soleil.** Sources recommandées : t4t35.fr, Megalithic Portal, OSM, publications archéologiques DRAC.

### Cap Corse (7 sites actuellement)
- Dolmen de Luri (mentionné Santucci 2004)
- Sites de Centuri (prospections Leandri)
- Menhirs côtiers entre Macinaggio et Barcaggio

### Balagne intérieure (9 sites)
- Sites dispersés entre Calenzana et Belgodère
- Dolmens de la vallée du Fango

### Nebbiu (9 sites)
- Sites autour de Saint-Florent
- Extension du complexe Revincu vers l'ouest

---

*Cet audit est un document de travail. L'ajout de sites fera l'objet d'une session dédiée avec sources vérifiables.*
