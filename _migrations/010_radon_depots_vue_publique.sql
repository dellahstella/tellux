-- 010_radon_depots_vue_publique.sql
-- Fermeture de l'exposition latente de `deposant_email` sur `radon_depots_erp`.
-- Rédigé le 2026-09-08 (suites audit brief CL). NON APPLIQUÉ PAR CE FICHIER :
-- les objets ont été créés directement sur la base ; ce fichier existe pour que
-- l'état cesse d'être invérifiable, et pour qu'un environnement neuf le reproduise.
--
-- ─────────────────────────────────────────────────────────────────────────────
-- POURQUOI CE FICHIER EXISTE
--
-- La table `radon_depots_erp` et ses deux policies ont été créées directement dans
-- Supabase, sans migration. Rien dans le dépôt ne permettait de savoir ce qui
-- protégeait quoi : l'audit a dû interroger la base pour l'établir. Les deux
-- policies sont donc reprises ci-dessous À L'IDENTIQUE de ce qui tourne, pour que
-- le fichier décrive l'état réel et non un état souhaité.
--
-- LE DÉFAUT TRAITÉ
--
-- Le rôle `anon` détient SELECT (et INSERT, UPDATE, REFERENCES) sur les 25 colonnes,
-- dont `deposant_email`. Les policies RLS filtrent des LIGNES, jamais des COLONNES :
-- tant qu'aucun dépôt n'est publié, l'exposition est inerte ; au premier passage en
-- 'publie', l'adresse du déposant devient lisible par quiconque possède la clé anon,
-- publique côté client. Publier étant la finalité du module, l'exposition n'est pas
-- hypothétique, elle est différée.
-- ─────────────────────────────────────────────────────────────────────────────

-- 1. ÉTAT EXISTANT, repris tel quel (créé hors migration, jamais versionné).
--    Ne pas rejouer sur la base de production : ces deux policies y sont déjà.
--
-- ALTER TABLE public.radon_depots_erp ENABLE ROW LEVEL SECURITY;
--
-- CREATE POLICY radon_depots_erp_insert_en_attente ON public.radon_depots_erp
--   FOR INSERT TO anon
--   WITH CHECK (statut_verification_tellux = 'en_attente' AND certifie_institutionnel = false);
--
-- CREATE POLICY radon_depots_erp_select_publie ON public.radon_depots_erp
--   FOR SELECT TO anon
--   USING (statut_verification_tellux = 'publie');

-- 2. VUE PUBLIQUE — APPLIQUÉE le 2026-09-08.
--    13 colonnes sur 25. Sont exclues, dans l'ordre de la table :
--      created_at, zone_radon_commune, zone_homogene, vs_niveau_reference_300,
--      date_prochain_mesurage, certifie_institutionnel, deposant_role,
--      deposant_email, consentement_ouverture, consentement_ouverture_horodatage,
--      document_source, statut_verification_tellux.
--    Motifs : identifiants ou traces du déposant (deposant_*, consentement_*,
--    document_source) ; champs de processus interne (certifie_institutionnel,
--    statut_verification_tellux) ; le reste par minimisation — la vue n'expose que
--    ce que la surface affiche réellement.
--
--    security_invoker VOLONTAIREMENT LAISSÉ À OFF (défaut). C'est ce qui permet à la
--    vue de continuer à lire la table après le REVOKE de l'étape 4 : elle s'exécute
--    avec les droits de son propriétaire. En contrepartie la RLS de la table ne
--    s'applique pas à travers elle, donc le filtre est PORTÉ PAR LA VUE ci-dessous.
--    Le passer à ON casserait la vue dès que le REVOKE serait appliqué.

CREATE VIEW public.radon_depots_publies AS
SELECT
  id,
  commune_insee,
  nom_etablissement,
  categorie_erp,
  organisme_agree_nom,
  organisme_agree_numero,
  date_mesurage,
  valeur_moyenne_bq_m3,
  statut_action,
  norme_commune,
  warning,
  lat,
  lon
FROM public.radon_depots_erp
WHERE statut_verification_tellux = 'publie';

-- 3. DROITS SUR LA VUE — APPLIQUÉS le 2026-09-08.
--    Le REVOKE ALL n'est pas décoratif : les privilèges par défaut de Supabase sur le
--    schéma `public` accordent à anon et authenticated INSERT, UPDATE, DELETE, TRUNCATE,
--    REFERENCES et TRIGGER sur tout objet neuf — vues comprises. Une vue mono-table sans
--    agrégat est auto-modifiable en PostgreSQL : sans ce REVOKE, un client anonyme
--    pouvait supprimer des lignes de la table SOUS-JACENTE en écrivant dans la vue, et
--    en mode définisseur la RLS ne l'en aurait pas empêché. Constaté et refermé dans la
--    minute suivant le CREATE VIEW.
REVOKE ALL ON public.radon_depots_publies FROM anon, authenticated;
GRANT SELECT ON public.radon_depots_publies TO anon, authenticated;

-- 4. RETRAIT DE L'ACCÈS DIRECT — *** NON APPLIQUÉ ***
--    Condition d'arrêt du brief : ne retirer le droit qu'une fois plus aucun lecteur
--    direct en production. Au 2026-09-08 il en restait un, `fetchRadonDepotsErp()`
--    dans radon.html, atteignable par le bouton de couche « Dépôts radon ERP » (le
--    formulaire est suspendu depuis #1327, la couche d'affichage ne l'est pas).
--    Ce lecteur est basculé sur la vue par la PR qui accompagne ce fichier ; les trois
--    ordres ci-dessous s'appliquent une fois ce diff en production, et pas avant.
--
--    UPDATE est révoqué en même temps que SELECT : le privilège est accordé à anon
--    alors qu'AUCUNE policy UPDATE n'existe. Il est donc inerte — mais il ne tient que
--    par la RLS, et la première policy UPDATE ajoutée le réveillerait sans que personne
--    ne le décide.
--    INSERT est CONSERVÉ : sa policy contraint le statut et interdit l'auto-certification,
--    et le formulaire doit pouvoir rouvrir sans nouvelle migration.
--
-- REVOKE SELECT, UPDATE ON public.radon_depots_erp FROM anon;
-- REVOKE SELECT, UPDATE ON public.radon_depots_erp FROM authenticated;
--
-- CONTRÔLE APRÈS APPLICATION (seconde passe, avec la clé anon, pas avec ce rôle-ci) :
--   - GET /rest/v1/radon_depots_erp?select=deposant_email  → doit être REFUSÉ (401/403/42501)
--   - GET /rest/v1/radon_depots_publies?select=nom_etablissement → doit répondre 200
--   - la couche « Dépôts radon ERP » de radon.html doit continuer à s'afficher
--   Un résultat vide ne prouve rien : la table est vide depuis le 2026-09-08. Le contrôle
--   porte sur le CODE de réponse, pas sur le nombre de lignes.
