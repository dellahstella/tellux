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
-- Le rôle `anon` détient SELECT sur les 25 colonnes, dont `deposant_email`.
-- (Inventaire complet relevé le 2026-09-08 avant le REVOKE, contre
-- `information_schema.role_table_grants` et non de mémoire : anon ET authenticated
-- détenaient DELETE, INSERT, REFERENCES, SELECT, TRIGGER, TRUNCATE, UPDATE — sept
-- privilèges, pas quatre. Une première rédaction de ce fichier en annonçait quatre :
-- inventaire incomplet présenté comme un inventaire, corrigé ici.)
-- Les policies RLS filtrent des LIGNES, jamais des COLONNES :
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

-- 4. RETRAIT DE L'ACCÈS DIRECT — APPLIQUÉ le 2026-09-08, après #1336.
--    Condition d'arrêt du brief : ne retirer le droit qu'une fois plus aucun lecteur
--    direct en production. Au moment de la rédaction il en restait un,
--    `fetchRadonDepotsErp()` dans radon.html, atteignable par le bouton de couche
--    « Dépôts radon ERP » (le formulaire est suspendu depuis #1327, la couche
--    d'affichage ne l'est pas). #1336 (`d30a951`) l'a basculé sur la vue.
--
--    LEVÉE DE LA CONDITION D'ARRÊT — vérifiée par deux chemins indépendants, pas par
--    relecture du diff :
--      a) recensement du dépôt : plus aucun SELECT sur la table dans une surface servie.
--         Les quatre occurrences restantes de `radon_depots_erp` dans radon.html sont
--         trois commentaires et un POST (l'INSERT du formulaire, lui-même injoignable —
--         son bloc de formulaire est commenté depuis #1327) ;
--      b) journaux edge du projet sur 24 h : les seules requêtes visant cette table
--         venaient du poste de travail en curl, pendant cette vérification même.
--         Aucun navigateur, aucune CI, aucun tiers.
--
--    UPDATE est révoqué en même temps que SELECT : le privilège est accordé à anon
--    alors qu'AUCUNE policy UPDATE n'existe. Il est donc inerte — mais il ne tient que
--    par la RLS, et la première policy UPDATE ajoutée le réveillerait sans que personne
--    ne le décide.
--    INSERT est CONSERVÉ : sa policy contraint le statut et interdit l'auto-certification,
--    et le formulaire doit pouvoir rouvrir sans nouvelle migration.

REVOKE SELECT, UPDATE ON public.radon_depots_erp FROM anon;
REVOKE SELECT, UPDATE ON public.radon_depots_erp FROM authenticated;

-- CONTRÔLE APRÈS APPLICATION — exécuté le 2026-09-08 avec la clé anon publique servie
-- par radon.html, pas avec le rôle privilégié. Le contrôle porte sur le CODE de réponse,
-- pas sur le nombre de lignes : la table est vide depuis le 2026-09-08, donc un résultat
-- vide n'aurait rien prouvé.
--   GET  radon_depots_erp?select=deposant_email      → 401 / 42501 permission denied  ✓
--   GET  radon_depots_erp?select=nom_etablissement   → 401 / 42501 permission denied  ✓
--   GET  radon_depots_publies?select=…               → 200                            ✓
--   POST radon_depots_erp (corps vide)               → 400 / 23502 NOT NULL           ✓
--        ← ce dernier est le contrôle le plus parlant : une violation de contrainte
--          prouve que le privilège INSERT a été accordé PUIS que la donnée a été
--          rejetée. Un 42501 aurait signalé un INSERT révoqué par erreur. Aucune ligne
--          créée (table revérifiée à 0).
--
-- 5. CE QUI RESTE ACCORDÉ, ET N'A PAS ÉTÉ TRANCHÉ — à arbitrer, rien d'exécuté.
--    Après le REVOKE ci-dessus, anon et authenticated détiennent encore sur la table :
--    DELETE, INSERT, REFERENCES, TRIGGER, TRUNCATE.
--    INSERT est voulu (ci-dessus). Les quatre autres relèvent du même raisonnement que
--    celui appliqué à UPDATE, et deux méritent d'être nommés :
--      - DELETE n'est inerte que parce qu'aucune policy DELETE n'existe — même fragilité
--        que UPDATE, à un `CREATE POLICY` près ;
--      - TRUNCATE n'est PAS filtré par la RLS. Le privilège n'est pas atteignable via
--        PostgREST (l'API n'émet jamais de TRUNCATE), donc la clé anon ne l'expose pas.
--        Mais il ne doit rien à la RLS : il ne tient qu'à l'absence de chemin.
--    Le périmètre du REVOKE (SELECT + UPDATE) est celui qui a été convenu ; l'élargir est
--    une décision, pas une correction mécanique. Consigné ici pour ne pas rester implicite.
