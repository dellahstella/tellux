# GPS en attente — Audit 18 avril 2026

Entrées identifiées comme problématiques dans l'audit R8-R10 mais **non modifiées** faute de source vérifiable lors de cette session. À traiter lors d'une session dédiée Géoportail / terrain.

---

## 1. Tour de Sagone (Vico) — PA00099123
**Coords actuelles :** `[42.109, 8.723]`  
**Statut :** En attente confirmation Géoportail  
**Action :** Vérifier parcelle A 138, commune Vico, lieu-dit « Lotis A Torre » sur geoportail.gouv.fr  
**Si confirmé :** Passer à 5 décimales ; supprimer "GPS approx" si présent

---

## 2. Tour d'Omigna, Cargèse — PA00099136
**Coords actuelles :** `[42.155, 8.554]`  
**Statut :** En attente confirmation Géoportail  
**Action :** Vérifier promontoire Omigna, commune Cargèse, côte nord sur geoportail.gouv.fr  
**Si confirmé :** Supprimer mention "GPS approx" de la description  
**Source Mérimée :** PA00099136

---

## 3. Castellu Ficaghjola, Alata
**Coords actuelles :** `[41.96500, 8.70000]`  
**Statut :** En attente source SRA Corse  
**Problème :** Longitude 8.70000 suspecte (valeur ronde)  
**Action :** Contacter SRA Corse (DRAC) ou consulter rapport Peche-Quilichini 2005 pour coordonnées exactes  
**Note :** Ne pas modifier sans source archéologique officielle

---

## 4. Anunziata di Pozzo di Borgo, Alata
**Coords actuelles :** `[41.945, 8.715]`  
**Statut :** En attente Géoportail (mentionné explicitement dans la fiche source)  
**Action :** Vérifier hameaux Montichji / Aghja di Giovanni / Pozzo di Borgo sur geoportail.gouv.fr, commune Alata  
**Note :** La fiche source dit explicitement "GPS à vérifier géoportail"

---

## 5. San Giovanni Battista, Urbalacone
**Coords actuelles :** `[41.856, 8.958]` (CHURCHES[] + _CHURCHES_EXTRA[])  
**Statut :** En attente vérification terrain  
**Action :** Vérifier sur Géoportail commune Urbalacone, piève d'Ornano  
**Note :** Fiche marquée "GPS approx · Rapport 9"

---

## 6. Capella San Cesario, Cozzano
**Coords actuelles :** `[41.875, 9.018]` (CHURCHES[] + _CHURCHES_EXTRA[])  
**Statut :** En attente vérification terrain  
**Action :** Vérifier sur Géoportail commune Cozzano, piève Talavo, mi-pente  
**Note :** Vestige d'habitat médiéval abandonné XVIIe s., accès difficile

---

## 7. Tour de la Parata (Ajaccio) — coords à 3 décimales
**Coords actuelles :** `[41.918, 8.623]`  
**Statut :** Précision insuffisante (±50m)  
**Action :** Vérifier sur Géoportail / Google Maps (tour visible sur imagerie satellite)  
**Source potentielle :** Mérimée PA00099144 ou Conservatoire du littoral

---

## 8. Tour de la Mortella — coords arrondies
**Coords actuelles :** `[42.700, 9.268]`  
**Statut :** Précision insuffisante  
**Action :** Vérifier sur Géoportail commune Saint-Florent, côte ouest  
**Note :** Tour bien documentée (MH PA00099279), coordonnées précises disponibles sur Mérimée

---

## Procédure de correction (pour session suivante)

1. Ouvrir geoportail.gouv.fr → couche "Orthophotos" ou "Plan IGN"
2. Rechercher par commune + lieu-dit
3. Clic droit sur le monument → "Copier les coordonnées" (format décimal)
4. Éditer index.html avec str_replace ciblé
5. Vérifier que la description ne contient plus "GPS approx" après correction
6. Mettre à jour Supabase si entrée dans `patrimoine_corse`
7. Committer avec message : `fix: GPS [NomSite] (source: Géoportail/Mérimée)`
