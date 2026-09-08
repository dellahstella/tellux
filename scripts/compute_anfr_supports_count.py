#!/usr/bin/env python3
"""
Compute the real ANFR support count for Corsica from the live Supabase
`anfr_supports` / `anfr_secteurs` tables — ingested 2026-07-01 by the
"directivite" research chantier, never read by any public page since.

Brief (2026-09-08) : le site a publie successivement ~974, 1 026 puis 1 030
"supports" — les trois etaient en realite un regroupement Tellux par
(latitude arrondie, longitude arrondie, operateur), pas un compte de
supports ANFR (la structure physique). Un pylone partage par N operateurs y
comptait N fois, d'ou une surestimation des supports mobiles de 57 %
(1 030 vs 656 reels). Ce script derive le vrai compte depuis le jeu ANFR
dormant, jamais un chiffre en dur.

Definitions (terminologie ANFR, pas Tellux) :
    - "support" = structure physique (pylone, chateau d'eau, toit...),
      identifiee par sup_id (SUP_ID de l'export ANFR). anfr_supports.sup_id
      est la cle primaire, 0 valeur NULLE (verifie).
    - "support portant du mobile" = support dont au moins un secteur
      anfr_secteurs.systeme est un systeme cellulaire (GSM/UMTS/LTE/5G NR),
      par opposition aux systemes non-mobiles presents dans le meme export
      (FH = faisceaux hertziens, FM/RDF DVB-T = radiodiffusion, PMR, COM
      MAR/AERTER, AIS, RDR MTO, SAT, TELEM, ADS-B, EM/REC...).
    - Le nombre de "positions x operateur" affiche par ailleurs sur le site
      (index.html, _meta.n_supports_total de antennes_par_commune_corse.json)
      est une AUTRE grandeur, deliberement distincte : elle decrit ce que la
      carte affiche (une position par operateur present), pas un compte de
      structures physiques. Les deux coexistent, aucune ne remplace l'autre
      (cf. brief, regle "ne pas retirer les chiffres de positions existants").

Source :
    Tables Supabase anfr_supports (976 lignes, 0 sup_id NULL) et
    anfr_secteurs (22 004 lignes, 0 sup_id NULL, FK vers anfr_supports).
    Ingerees le 2026-07-01 depuis l'export national ANFR data.gouv.fr
    ("installations radioelectriques > 5 W", ZIP
    5fa56156-bde6-4dd0-81e7-6dee1318f669, mise a disposition 2026-05-31).
    Audit de provenance fait le 2026-09-08 : mapping sup_id<-SUP_ID
    confirme, 590/656 supports mobiles retrouves a moins de 100 m d'une
    position du socle antennas_corse (90 % de recoupement). Correctif du
    meme jour (volet B, constat _drafts/) : l'ecart residuel n'est PAS
    une difference de millesime — antennas_corse (CartoRadio) et
    anfr_supports/anfr_secteurs (export national ANFR) sont deux
    extractions ANFR INDEPENDANTES, pas une relation source/derive. 13
    communes portent du mobile reel (ANFR, mis en service 2016-2024, pas
    recent) absent du socle CartoRadio — divergence entre deux sources
    de la meme autorite, non expliquee, non resolue.

Requires:
    stdlib Python 3.10+ uniquement (json, urllib).

Result (recalcule en direct le 2026-09-08, cf. commit) :
    976 supports ANFR (structures physiques, 2A: 459, 2B: 517, 259 communes)
    656 supports portant au moins un systeme mobile (GSM/UMTS/LTE/5G NR)
    Export ANFR : mise a disposition 2026-05-31 (donnee externe, pas
    recalculee ici — la date figure dans ce script, pas dans une colonne
    de la table).

⚠ AUCUN RAFRAICHISSEMENT AUTOMATIQUE (brief 2026-09-08, etape A.5) :
    Ingestion PONCTUELLE du 2026-07-01 (chantier directivite). Aucun
    workflow, aucun cron — contrairement a intermagnet-cron.yml ou
    refresh-antennes.yml. Le nombre 976 restera fige a l'export du
    31 mai 2026 jusqu'a decision explicite : (a) un workflow de
    rafraichissement dedie, avec le cout de maintenance deja mesure sur
    intermagnet-cron.yml (cf. INTERMAGNET-CRON-CADENCE-DEGRADEE-001,
    registre prive), ou (b) assumer le gel et le documenter comme dette
    ouverte — c'est l'option choisie ici par defaut, PAS un refresh
    silencieux. Ne pas retirer cet avertissement sans avoir traite l'un
    des deux. Dette privee : ANFR-SUPPORTS-EXTRACTION-GELEE-001.

Usage:
    python3 scripts/compute_anfr_supports_count.py
"""
import json
import urllib.request

SB_URL = "https://knckulwghgfrxmbweada.supabase.co"
SB_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6"
    "ImtuY2t1bHdnaGdmcnhtYndlYWRhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM2NTAxMzQs"
    "ImV4cCI6MjA4OTIyNjEzNH0.Cu9dvxFyn-5pbOP65gowCEQvRti74CLnlNYf92jebis"
)  # cle publique anon, deja exposee cote client dans app.html — pas un secret
PAGE = 1000

# Systemes cellulaires (terminologie ANFR, cf. docstring). Prefixe suffit :
# les variantes de bande (GSM 900/1800, LTE 700..2600, 5G NR 700/2100/3500,
# UMTS 900/2100) partagent toutes ce prefixe. Tout le reste (FH, FM, RDF
# DVB-T, PMR, COM MAR/AERTER/TER, AIS, RDR MTO, SAT, TELEM, ADS-B, EM/REC)
# est exclu du compte "mobile".
MOBILE_PREFIXES = ("GSM", "UMTS", "LTE", "5G")

EXPORT_DATE = "2026-05-31"  # mise a disposition de l'export national ANFR,
                            # constante externe (aucune colonne ne la porte)


def fetch_all(path_query):
    rows = []
    offset = 0
    while True:
        req = urllib.request.Request(
            SB_URL + "/rest/v1/" + path_query,
            headers={
                "apikey": SB_KEY,
                "Authorization": "Bearer " + SB_KEY,
                "Range": f"{offset}-{offset + PAGE - 1}",
                "Range-Unit": "items",
                "Prefer": "count=exact",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            page = json.loads(resp.read())
        rows.extend(page)
        if len(page) < PAGE:
            break
        offset += PAGE
    return rows


def main():
    supports = fetch_all("anfr_supports?select=sup_id,dept,code_insee")
    secteurs = fetch_all("anfr_secteurs?select=sup_id,systeme")

    n_supports = len(supports)
    n_supports_null_id = sum(1 for s in supports if not s.get("sup_id"))
    n_2a = sum(1 for s in supports if s.get("dept") == "2A")
    n_2b = sum(1 for s in supports if s.get("dept") == "2B")
    communes = {s["code_insee"] for s in supports if s.get("code_insee")}

    mobile_sup_ids = {
        s["sup_id"]
        for s in secteurs
        if s.get("systeme") and s["systeme"].startswith(MOBILE_PREFIXES)
    }

    print(f"supports ANFR (structures physiques) : {n_supports}")
    print(f"  dont sup_id NULL (anomalie) : {n_supports_null_id}")
    print(f"  2A : {n_2a} · 2B : {n_2b}")
    print(f"  communes distinctes : {len(communes)}")
    print(f"secteurs ANFR (tous systemes) : {len(secteurs)}")
    print(f"supports portant du mobile (GSM/UMTS/LTE/5G) : {len(mobile_sup_ids)}")
    print(f"export ANFR (mise a disposition) : {EXPORT_DATE}")


if __name__ == "__main__":
    main()
