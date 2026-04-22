-- Migration 005 : Renforcement sécurité RLS — policies INSERT + rate limiting
-- Date : 2026-04-22
-- Contexte : PR fix/supabase-security-hardening
-- Audit MCP : 2 alertes WARN rls_policy_always_true (contributions + orientations_contributions)
--
-- Remplace les policies INSERT permissives "WITH CHECK (true)" par des policies
-- avec contraintes de validation serveur. Ajoute rate limiting basique par session_id.
--
-- Décisions Soleil + Claude web :
--   - GPS plage mondiale (lat/lon) pour préparer extension Méditerranée phase 2
--   - note/commentaire <= 500 chars (cohérent avec maxlength HTML PR #82)
--   - Rate limiting 10 contributions/heure par session_id (faible, bloque spam naïf)
--   - Pas de contrainte type/valeur/unite (évolution future)

BEGIN;

-- =====================================================
-- FONCTION RATE LIMITING
-- =====================================================

CREATE OR REPLACE FUNCTION public.check_contribution_rate_limit(p_session_id text)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_count integer;
BEGIN
  -- Si session_id null/vide, laisser passer (pas de limitation)
  IF p_session_id IS NULL OR length(trim(p_session_id)) = 0 THEN
    RETURN true;
  END IF;

  -- Compter les contributions récentes du même session_id (1h glissante)
  SELECT count(*) INTO v_count
  FROM public.contributions
  WHERE session_id = p_session_id
    AND created_at > now() - interval '1 hour';

  RETURN v_count < 10;
END;
$$;

COMMENT ON FUNCTION public.check_contribution_rate_limit(text) IS
'Rate limiting : max 10 contributions par session_id par heure glissante. Retourne true si l''insertion est autorisée.';

-- =====================================================
-- TABLE contributions — POLICY INSERT RENFORCÉE
-- =====================================================

-- Supprimer l'ancienne policy permissive
DROP POLICY IF EXISTS "ecriture publique" ON public.contributions;

-- Créer la nouvelle policy avec validation
CREATE POLICY "insertion publique validée"
  ON public.contributions
  FOR INSERT
  TO public
  WITH CHECK (
    -- GPS plage mondiale
    lat BETWEEN -90 AND 90
    AND lon BETWEEN -180 AND 180
    -- Note longueur max (cohérent avec maxlength HTML)
    AND (note IS NULL OR length(note) <= 500)
    -- Rate limiting par session_id
    AND public.check_contribution_rate_limit(session_id)
  );

COMMENT ON POLICY "insertion publique validée" ON public.contributions IS
'Remplace l''ancienne policy WITH CHECK (true). Valide GPS mondial, note <= 500 chars, rate limit 10/h par session_id.';

-- =====================================================
-- TABLE orientations_contributions — POLICY INSERT RENFORCÉE
-- =====================================================

-- Supprimer l'ancienne policy permissive
DROP POLICY IF EXISTS "insert orientations" ON public.orientations_contributions;

-- Créer la nouvelle policy avec validation
CREATE POLICY "insertion orientations validée"
  ON public.orientations_contributions
  FOR INSERT
  TO anon
  WITH CHECK (
    -- Azimut contrainte physique (redondant avec CHECK colonne, explicite en policy)
    azimut BETWEEN 0 AND 360
    -- Commentaire longueur max
    AND (commentaire IS NULL OR length(commentaire) <= 500)
    -- site_id non vide
    AND site_id IS NOT NULL
    AND length(trim(site_id)) > 0
  );

COMMENT ON POLICY "insertion orientations validée" ON public.orientations_contributions IS
'Remplace l''ancienne policy WITH CHECK (true). Valide azimut 0-360, commentaire <= 500 chars, site_id non vide.';

-- =====================================================
-- VÉRIFICATION POST-MIGRATION
-- =====================================================

DO $$
DECLARE
  v_contributions_policy_count integer;
  v_orientations_policy_count integer;
BEGIN
  SELECT count(*) INTO v_contributions_policy_count
  FROM pg_policies
  WHERE schemaname = 'public'
    AND tablename = 'contributions'
    AND cmd = 'INSERT';

  SELECT count(*) INTO v_orientations_policy_count
  FROM pg_policies
  WHERE schemaname = 'public'
    AND tablename = 'orientations_contributions'
    AND cmd = 'INSERT';

  IF v_contributions_policy_count != 1 THEN
    RAISE EXCEPTION 'Policy INSERT contributions : attendu 1, trouvé %', v_contributions_policy_count;
  END IF;

  IF v_orientations_policy_count != 1 THEN
    RAISE EXCEPTION 'Policy INSERT orientations_contributions : attendu 1, trouvé %', v_orientations_policy_count;
  END IF;

  RAISE NOTICE 'Migration 005 OK : 1 policy INSERT par table validée.';
END $$;

COMMIT;
