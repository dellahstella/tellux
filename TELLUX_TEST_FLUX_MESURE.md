# TELLUX — Scenarios de test du flux de mesure

**Date :** 9 avril 2026
**Version :** post-corrections session du 9 avril (Mission A-D)
**Objectif :** Valider le flux complet de mesure terrain dans 5 scenarios realistes.

---

## Mode d'emploi

Chaque scenario doit etre execute dans un navigateur (Chrome ou Firefox). Ouvrir la console (F12 > Console) et l'onglet Network pour verifier les requetes Supabase. Chaque etape a un resultat attendu — si le resultat differe, noter le bug.

**URL de test :** `https://tellux.pages.dev` (production) ou `https://dev.tellux.pages.dev` (dev)

---

## Scenario 1 — Mesure smartphone exterieur (parcours nominal)

**Persona :** Marie, randonneuse, smartphone Android, Phyphox installe.
**Lieu :** Col de Bavella, exterieur.

| Etape | Action | Resultat attendu |
|---|---|---|
| 1.1 | Cliquer sur le FAB (+) en bas a droite | Mini-menu s'ouvre avec 2 options : "Ajouter une mesure" et "Prescription de mesure" |
| 1.2 | Cliquer sur "Ajouter une mesure" | Formulaire s'ouvre. Info bar affiche "Cliquez sur la carte..." en style warn (fond jaune doux). Le texte "Cliquez sur la carte pour placer le point" apparait dans le formulaire. |
| 1.3 | Cliquer sur la carte au Col de Bavella | Marqueur violet apparait. Le formulaire affiche "Position : 41.7xxxx, 9.2xxxx". Bouton "Repositionner le point" visible. Info bar passe en style success. |
| 1.4 | Cliquer "Repositionner le point" | Marqueur disparait. Info bar affiche "Cliquez sur la carte pour repositionner..." |
| 1.5 | Cliquer a nouveau sur la carte | Nouveau marqueur place. Position mise a jour dans le formulaire. |
| 1.6 | Selectionner "Exterieur" | Bouton ext. met en surbrillance (fond vert clair). Bloc interieur reste masque. |
| 1.7 | Selectionner "Magnetometre telephone" | Hint apparait : "Magnetometre smartphone — valeur typique en Corse : 44 000–47 000 nT". Unite forcee sur "nT". |
| 1.8 | Saisir "45200" comme valeur | Pas d'erreur. |
| 1.9 | Ecrire une note : "Col de Bavella, 14h, vent fort" | Champ note rempli. |
| 1.10 | Cocher la case RGPD | Case cochee. |
| 1.11 | Cliquer "Enregistrer" | **Network tab :** requete POST vers `/rest/v1/contributions` avec code 201. Info bar affiche "Mesure sauvegardee..." en style success (fond vert clair). Marqueur persiste sur la carte. Compteur contributions incrementé. FAB revient a l'etat normal. |
| 1.12 | Verifier la console | Aucune erreur JavaScript. Aucune erreur PGRST. |

---

## Scenario 2 — Mesure interieur avec contexte batiment

**Persona :** Lucas, habitant Bastia, mesure dans son appartement.
**Lieu :** Bastia centre, interieur, 2eme etage.

| Etape | Action | Resultat attendu |
|---|---|---|
| 2.1 | Ouvrir le formulaire via FAB > "Ajouter une mesure" | Formulaire ouvert. |
| 2.2 | Placer le point sur Bastia centre | Marqueur place. |
| 2.3 | Selectionner "Interieur" | Bouton int. en surbrillance. Bloc "Contexte interieur" apparait avec etage, materiaux, appareils. Label "Etape 4 — Details interieur" visible. |
| 2.4 | Selectionner etage "2eme etage et +" | Etage selectionne. |
| 2.5 | Cocher "Beton Portland" + "Platre" + "Bois/OSB" | 3 chips passent en vert (style active). |
| 2.6 | Cocher "WiFi routeur" + "Refrigerateur" | 2 chips passent en vert. |
| 2.7 | Selectionner instrument "TriField TF2" | Hint TriField affiche. |
| 2.8 | Saisir "45800" en nT | Valeur acceptee. |
| 2.9 | Cocher RGPD + Enregistrer | **Network tab :** le payload JSON contient `materiaux_murs:["beton_portland","platre","bois"]`, `appareils_actifs:["wifi","frigo"]`, `etage:"2"`, `contexte:"interieur"`, `attenuation_prevue_db:25` (17+3+5). Code 201. |
| 2.10 | Verifier la console | Pas d'erreur PGRST204 (les colonnes existent maintenant). |

---

## Scenario 3 — Prescription puis mesure

**Persona :** Anna, debutante, ne sait pas quel instrument utiliser.
**Lieu :** Corte, exterieur.

| Etape | Action | Resultat attendu |
|---|---|---|
| 3.1 | Cliquer sur le FAB (+) | Mini-menu s'ouvre. |
| 3.2 | Cliquer "Prescription de mesure" | Panel prescription s'ouvre en bas a droite. 8 methodes listees avec badges colores (vert/ocre/bleu) et niveaux (Accessible/Capteur dedie/Avance). |
| 3.3 | Lire les descriptions | Chaque methode a un protocole court. |
| 3.4 | Cliquer sur "Magnetometre smartphone" | Panel prescription se ferme. Formulaire de mesure s'ouvre. Instrument pre-selectionne sur "Magnetometre telephone (Physics Toolbox...)". Unite pre-selectionnee sur "nT". Hint affiche. |
| 3.5 | Placer le point sur Corte, saisir 44900, cocher RGPD, enregistrer | Sauvegarde OK, code 201. |
| 3.6 | Cliquer FAB a nouveau > "Prescription de mesure" | Panel prescription se rouvre. |
| 3.7 | Cliquer sur "TriField TF2 — RF" | Formulaire de mesure s'ouvre avec instrument "TriField TF2" et unite "V/m". |

---

## Scenario 4 — Erreurs et cas limites

**Persona :** Testeur QA.

| Etape | Action | Resultat attendu |
|---|---|---|
| 4.1 | Ouvrir formulaire, NE PAS placer de point, cliquer "Enregistrer" | Info bar affiche "Cliquez d'abord sur la carte..." en style warn (pas error). |
| 4.2 | Placer un point, NE PAS cocher RGPD, cliquer "Enregistrer" | Info bar affiche "Veuillez accepter les conditions..." en style error (fond rouge clair, texte porphyre). |
| 4.3 | Cocher RGPD, selectionner "Magnetometre telephone", saisir "999999" | Cliquer Enregistrer → Info bar affiche "Valeur hors plage pour smartphone_mag : attendu 20000–80000 nT" en style error. |
| 4.4 | Saisir "45000", enregistrer | Sauvegarde OK. |
| 4.5 | Cliquer FAB (+) immediatement apres | Mini-menu s'ouvre (pas de double-toggle). |
| 4.6 | Cliquer "Ajouter une mesure" → puis re-cliquer FAB | Formulaire se ferme proprement. Marqueur retire de la carte. |
| 4.7 | Ouvrir prescription panel → cliquer FAB | Panel prescription se ferme. FAB revient a l'etat normal. |
| 4.8 | Selectionner "Observation" comme instrument | Unite forcee sur "description". Champ valeur affiche placeholder "Pas de valeur numerique requise". |
| 4.9 | Enregistrer sans valeur numerique | Sauvegarde OK (valeur null acceptee pour observations). |

---

## Scenario 5 — Mobile (ecran < 600px)

**Persona :** Utilisateur terrain sur smartphone.
**Simuler :** DevTools > Toggle device toolbar > iPhone 12 Pro (390x844).

| Etape | Action | Resultat attendu |
|---|---|---|
| 5.1 | FAB visible en bas a droite | FAB de 44x44px, bien positionne, pas masque par d'autres elements. |
| 5.2 | Cliquer FAB | Mini-menu s'ouvre au-dessus du FAB. Labels lisibles. |
| 5.3 | Cliquer "Ajouter une mesure" | Formulaire s'ouvre. Le formulaire ne deborde pas de l'ecran. Les step labels sont visibles. |
| 5.4 | Selectionner "Interieur" | Bloc contexte interieur visible. Les chips materiaux s'enroulent (flex-wrap) sans deborder. |
| 5.5 | Remplir et enregistrer | Sauvegarde OK. |
| 5.6 | Ouvrir prescription panel | Panel s'affiche en pleine largeur (100vw - 32px). Scrollable si contenu depasse. |
| 5.7 | Cliquer une methode | Formulaire pre-rempli, transition fluide. |

---

## Checklist de verification post-session

- [ ] Aucune erreur JavaScript dans la console
- [ ] Aucune erreur PGRST (400, 404, 204) dans l'onglet Network
- [ ] Les 7 nouvelles colonnes existent dans Supabase (verifier via Table Editor)
- [ ] Les donnees sauvegardees contiennent bien les champs contexte, materiaux, appareils
- [ ] Le FAB fonctionne en mode toggle (ouvrir/fermer) sans bugs
- [ ] Le panel prescription affiche les 8 methodes avec badges corrects
- [ ] La pre-selection d'instrument depuis la prescription fonctionne
- [ ] Le bouton "Repositionner le point" fonctionne
- [ ] Les messages info/error/success/warn ont les bonnes couleurs DA v2
- [ ] Mobile : tout est utilisable sur ecran 390px de large

---

*Scenarios rediges le 9 avril 2026. A executer apres chaque modification du flux de mesure.*
