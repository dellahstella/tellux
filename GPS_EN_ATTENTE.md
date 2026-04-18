# GPS en attente — Audit 18 avril 2026

Mis à jour le 18 avril 2026 (session corrections GPS validées par Soleil).

---

## ✅ RÉSOLUS (session 18 avril 2026)

| Site | Ancienne coords | Nouvelle coords | Source |
|------|----------------|-----------------|--------|
| Renicciu (Coggia) | [42.116, 8.706] | [42.13417, 8.74944] | Géoportail Soleil |
| Tour de Cargèse (ruines) | [42.133, 8.587] | [42.13298, 8.58941] | Géoportail Soleil |
| Buste Sampiero Corso (Tricolacci) | [41.987, 9.014] | [42.00091, 9.04984] | Géoportail Soleil |
| Castellu di Bozzi (Guitera) | [41.850, 9.034] | [41.9139, 9.08667] | Géoportail Soleil |
| Capella San Cesario (Cozzano) | [41.875, 9.018] | [41.9353, 9.1553] | Géoportail Soleil |
| Anunziata di Pozzo di Borgo (Alata) | [41.945, 8.715] | [41.98, 8.74333] | Géoportail Soleil |
| Chapelle Impériale CHURCHES[] | [41.922, 8.738] | [41.92175, 8.73837] | Mérimée PA00099060 |
| Pont de Zippitoli (description) | — | description reconstruite | bastelica.fr |

---

## ❌ REJETÉS — NE PAS MODIFIER

### Stèle de Ponticellu (Bastelica)
**Coords actuelles :** `[41.996, 9.012]`  
**Coords proposées :** 42.8482N — **REJETÉES**  
**Raison :** 42.8482N appartient géographiquement au Cap Corse (secteur Pietracorbara), incompatible avec la commune de Bastelica (~42.0N). Copier-coller probable depuis une autre entrée.  
**Action :** Laisser en l'état `[41.996, 9.012]` jusqu'à source terrain vérifiable.

### Castellu Ficaghjola (Alata)
**Coords actuelles :** `[41.96500, 8.70000]`  
**Coords proposées :** 42.2513N — **REJETÉES**  
**Raison :** 42.2513N est incompatible avec la commune d'Alata (~41.96N, au nord d'Ajaccio). Conflit géographique majeur (~32km d'écart).  
**Action :** Laisser `[41.96500, 8.70000]` et attendre rapport Peche-Quilichini 2005 ou contact SRA Corse (DRAC).

### San Giovanni Battista (Urbalacone)
**Coords actuelles :** `[41.856, 8.958]`  
**Coords proposées :** [42.13298, 8.58941] — **REJETÉES**  
**Raison :** Coordonnées identiques à Tour de Cargèse (ruines) — copier-coller probable.  
**Action :** Laisser en l'état. Vérifier sur Géoportail commune Urbalacone, piève d'Ornano.

---

## ⏳ EN ATTENTE — sources à consulter

### 1. Tour de Sagone (Vico) — PA00099123
**Coords actuelles :** `[42.109, 8.723]`  
**Action :** Vérifier parcelle A 138, commune Vico, lieu-dit « Lotis A Torre » sur geoportail.gouv.fr  
**Si confirmé :** Passer à 5 décimales ; supprimer mention "GPS approx" si présente

### 2. Tour d'Omigna, Cargèse — PA00099136
**Coords actuelles :** `[42.155, 8.554]`  
**Action :** Vérifier promontoire Omigna, commune Cargèse, côte nord sur geoportail.gouv.fr  
**Si confirmé :** Supprimer mention "GPS approx" de la description  
**Source Mérimée :** PA00099136

### 3. San Giovanni Battista (Urbalacone)
**Coords actuelles :** `[41.856, 8.958]` (CHURCHES[] + _CHURCHES_EXTRA[])  
**Action :** Vérifier sur Géoportail commune Urbalacone, piève d'Ornano (source indépendante requise)

### 4. Tour de la Parata (Ajaccio) — précision insuffisante
**Coords actuelles :** `[41.918, 8.623]`  
**Action :** Vérifier sur Géoportail / imagerie satellite (tour bien visible)  
**Source potentielle :** Conservatoire du littoral ou Mérimée

### 5. Tour de la Mortella — précision insuffisante
**Coords actuelles :** `[42.700, 9.268]`  
**Action :** Vérifier sur Géoportail commune Saint-Florent, côte ouest  
**Source :** Mérimée PA00099279

---

## Procédure de correction (pour session suivante)

1. Ouvrir geoportail.gouv.fr → couche "Orthophotos" ou "Plan IGN"
2. Rechercher par commune + lieu-dit
3. Clic droit → "Copier les coordonnées" (format décimal)
4. Éditer index.html avec str_replace ciblé
5. Vérifier absence de "GPS approx" dans la description après correction
6. Mettre à jour Supabase si entrée dans `patrimoine_corse`
7. Committer : `fix: GPS [NomSite] (source: Géoportail/Mérimée)`
