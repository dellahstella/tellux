-- ===========================================================================
-- MIGRATION 009 — Socle directivité ANFR Cartoradio (chantier S3)
-- ===========================================================================
-- Date : 2026-07-01
-- Contexte : le modèle RF S1-S6 (PR #901, en prod) est isotrope. S3 vise une
-- directivité par secteur (azimut ANFR) pour redresser la dispersion residuelle,
-- SOUS condition du gate §6 (Spearman ET LOO en baisse + sensibilite tilt) —
-- gate hors perimetre de cette migration.
--
-- Cette migration est ADDITIVE et REVERSIBLE (DROP). Elle cree deux tables
-- NEUVES peuplees depuis l'export national ANFR SUP (data.gouv.fr, > 5 W).
-- Elle N'ALTERE PAS `antennas_corse` (socle prod S1-S6). RLS lecture seule anon
-- (donnee open data). Aucune policy d'ecriture anon.
--
-- Jointure au socle : PAS de FK vers antennas_corse (sa colonne sup_id est a
-- 100 % NULL — decision Soleil option (a) : correspondance SPATIALE lat/lon au
-- prototype ulterieur, jamais de modif du socle). Cle interne = SUP_ID + AER_ID.
--
-- Tilt : AER_NB_* de l'open data ANFR ne publie AUCUN tilt (ni mecanique ni
-- electrique). Les colonnes tilt_*_deg existent mais restent NULL (aucune
-- fabrication). Le prototype S3 traitera le tilt en hypothese parametrique (§6).
--
-- Grain `anfr_secteurs` = 1 ligne par (secteur x systeme) = SUP_ANTENNE x
-- SUP_EMETTEUR joints sur (STA_NM_ANFR, AER_ID). aer_id conserve.
-- ===========================================================================

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS public.anfr_supports (
  sup_id            text PRIMARY KEY,           -- ANFR SUP_SUPPORT.SUP_ID
  sta_nm_anfr       text,                        -- ANFR STA_NM_ANFR (tracabilite)
  lat               double precision NOT NULL,   -- DMS -> decimal (WGS84)
  lon               double precision NOT NULL,   -- DMS -> decimal (WGS84)
  hauteur_support_m double precision,            -- SUP_NM_HAUT
  code_insee        text,                        -- COM_CD_INSEE (2A0xx / 2B0xx)
  dept              text,                        -- '2A' | '2B'
  date_mes          date                         -- SUP_STATION.DTE_EN_SERVICE
);

CREATE TABLE IF NOT EXISTS public.anfr_secteurs (
  secteur_id        bigserial PRIMARY KEY,
  sup_id            text NOT NULL REFERENCES public.anfr_supports(sup_id),
  aer_id            text NOT NULL,               -- SUP_ANTENNE.AER_ID
  emr_id            text NOT NULL,               -- SUP_EMETTEUR.EMR_ID (grain systeme)
  azimut_deg        double precision,            -- AER_NB_AZIMUT (degres, 0..360)
  hauteur_antenne_m double precision,            -- AER_NB_ALT_BAS
  tilt_mec_deg      double precision,            -- ABSENT open data -> NULL
  tilt_elec_deg     double precision,            -- ABSENT open data -> NULL
  systeme           text,                        -- EMR_LB_SYSTEME (2G/3G/4G/5G, FM, TV...)
  bande_min_mhz     double precision,            -- SUP_BANDE min (normalise MHz)
  bande_max_mhz     double precision,            -- SUP_BANDE max (normalise MHz)
  UNIQUE (aer_id, emr_id)                        -- upsert idempotent, grain secteur x systeme
);

CREATE INDEX IF NOT EXISTS idx_anfr_supports_latlon ON public.anfr_supports (lat, lon);
CREATE INDEX IF NOT EXISTS idx_anfr_secteurs_sup    ON public.anfr_secteurs (sup_id);

-- RLS : lecture seule anon (open data). Pas de policy write => ecriture anon interdite.
ALTER TABLE public.anfr_supports ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.anfr_secteurs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS anfr_supports_sel_anon ON public.anfr_supports;
DROP POLICY IF EXISTS anfr_secteurs_sel_anon ON public.anfr_secteurs;
CREATE POLICY anfr_supports_sel_anon ON public.anfr_supports FOR SELECT TO anon USING (true);
CREATE POLICY anfr_secteurs_sel_anon ON public.anfr_secteurs FOR SELECT TO anon USING (true);
