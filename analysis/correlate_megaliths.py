"""
Tellux — Corrélation mégalithes × failles × piézoélectricité
=============================================================
Test statistique de l'hypothèse H1 : les sites mégalithiques corses sont-ils
préférentiellement implantés sur substrat piézoélectrique, à proximité de
failles tectoniques, avec anomalie crustale positive ?

Méthode : comparaison distributions mégalithes vs 500 points terrestres
aléatoires (Monte Carlo). Tests Mann-Whitney U, Kolmogorov-Smirnov, χ²,
Spearman.

Portage fidèle des fonctions JS de Tellux (index.html, branche dev).
"""

from __future__ import annotations
import math
import random
import re
import sys
from pathlib import Path

# Force UTF-8 output on Windows console
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(__file__).resolve().parent
INDEX_HTML = ROOT.parent / "index.html"
SEED = 42
random.seed(SEED)
np.random.seed(SEED)


# ═══════════════════════════════════════════════════════════════════════
# 1. DONNÉES (portées depuis index.html — dev, commit 900e098)
# ═══════════════════════════════════════════════════════════════════════

# LCS1_GRID — grille d'anomalie crustale fallback (index.html:2248)
LCS1_GRID = [
    (41.3, 8.5, -8), (41.3, 9.0, -5), (41.3, 9.5, -3),
    (41.5, 8.5, 20), (41.5, 9.0, 35), (41.5, 9.5, 40),
    (41.8, 8.5, 25), (41.8, 9.0, 50), (41.8, 9.5, 55),
    (42.0, 8.5, 22), (42.0, 9.0, 55), (42.0, 9.5, 60),
    (42.3, 8.5, 18), (42.3, 9.0, 40), (42.3, 9.5, 50),
    (42.6, 8.5, 12), (42.6, 9.0, 28), (42.6, 9.5, 32),
    (42.9, 8.5, 5),  (42.9, 9.0, 10), (42.9, 9.5, 8),
    (43.1, 8.5, -5), (43.1, 9.0, 2),  (43.1, 9.5, 5),
]

# GEO_SUSC_GRID — susceptibilité géologique + type roche (index.html:2535)
GEO_SUSC_GRID = [
    (41.38, 9.15, -5, 'calcaire'), (41.40, 9.00, -3, 'calcaire'), (41.42, 8.90, 5, 'granit_rose'),
    (41.50, 8.85, 25, 'granit_biotite'), (41.53, 8.92, 35, 'granit_biotite'), (41.56, 8.88, 30, 'granit_biotite'),
    (41.50, 9.05, 20, 'granit'), (41.50, 9.25, 15, 'granit'),
    (41.70, 8.80, 20, 'granit'), (41.75, 8.87, 30, 'granit_biotite'), (41.75, 9.00, 25, 'granit'),
    (41.75, 9.18, 22, 'granodiorite'), (41.80, 9.10, 18, 'granodiorite'),
    (41.72, 9.12, 15, 'granit'), (41.72, 9.23, 12, 'gneiss'),
    (42.00, 8.80, 18, 'granodiorite'), (42.00, 9.00, 25, 'granit_biotite'), (42.00, 9.20, 20, 'granit'),
    (42.00, 9.40, 8, 'alluvions'),
    (42.30, 9.20, 5, 'schistes'), (42.30, 9.40, 3, 'schistes'),
    (42.30, 8.80, 15, 'granit'), (42.30, 9.00, 18, 'granit'),
    (42.55, 9.10, 12, 'serpentinite'), (42.55, 9.30, 18, 'serpentinite'), (42.55, 9.45, 5, 'alluvions'),
    (42.65, 9.05, 10, 'granit'), (42.65, 9.25, 15, 'granit'),
    (42.80, 9.30, 8, 'ophiolite'), (42.80, 9.40, 5, 'schistes'),
    (42.95, 9.35, 3, 'schistes'), (43.00, 9.40, -2, 'ophiolite'),
    (42.55, 8.70, 12, 'granit'), (42.55, 8.90, 10, 'granit'),
]

# Teneur en quartz par type (Bishop 1981) — index.html:2606
QUARTZ_CONTENT = {
    'granit': 0.30, 'granit_biotite': 0.25, 'granit_rose': 0.35,
    'granodiorite': 0.20, 'gneiss': 0.15, 'serpentinite': 0.02,
    'schistes': 0.05, 'ophiolite': 0.01, 'calcaire': 0.01,
    'alluvions': 0.10, 'inconnu': 0.05,
}

# FAILLES_CORSE — BRGM 1/50k + Ghilardi 2017 + D'Anna 2019 (index.html:2639)
FAILLES_CORSE = [
    {"nom": "Faille des cols", "lat": 42.35, "lon": 9.00, "type": "Quaternaire"},
    {"nom": "Faille San-Quilico", "lat": 42.28, "lon": 9.08, "type": "Quaternaire"},
    {"nom": "Faille Casaluna", "lat": 42.20, "lon": 9.15, "type": "Quaternaire"},
    {"nom": "Faille Taravo", "lat": 41.85, "lon": 8.95, "type": "Quaternaire"},
    {"nom": "Faille Propriano", "lat": 41.70, "lon": 8.90, "type": "active"},
    {"nom": "Faille Monaco-Île Rousse", "lat": 42.62, "lon": 8.95, "type": "active"},
    {"nom": "Faille Cap Corse (nord)", "lat": 42.98, "lon": 9.35, "type": "active"},
    {"nom": "Faille Castagniccia", "lat": 42.40, "lon": 9.25, "type": "Quaternaire"},
]

# RADON_ZONES_CORSE — ASNR (index.html:2680)
RADON_ZONES_CORSE = [
    {"lat": 41.75, "lon": 8.95, "categ": 3},
    {"lat": 41.85, "lon": 8.90, "categ": 3},
    {"lat": 41.60, "lon": 9.28, "categ": 3},
    {"lat": 42.15, "lon": 8.95, "categ": 3},
    {"lat": 42.12, "lon": 9.10, "categ": 3},
    {"lat": 42.35, "lon": 9.05, "categ": 3},
    {"lat": 42.55, "lon": 8.85, "categ": 3},
    {"lat": 42.85, "lon": 9.30, "categ": 2},
]


# ═══════════════════════════════════════════════════════════════════════
# 2. FONCTIONS PORTÉES (JS → Python, fidèles au comportement Tellux)
# ═══════════════════════════════════════════════════════════════════════

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Distance grand cercle en km. Portage index.html:5675."""
    R = 6371.0
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(dLon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def interp_idw(grid, lat: float, lon: float, n: int = 4) -> float:
    """Interpolation inverse distance weighting. Portage index.html:2268."""
    pts = [(max(1e-10, (p[0] - lat) ** 2 + (p[1] - lon) ** 2), p[2]) for p in grid]
    pts.sort(key=lambda x: x[0])
    pts = pts[:n]
    wsum = sum(1.0 / p[0] for p in pts)
    return sum(p[1] / p[0] for p in pts) / wsum


def calc_lcs1(lat: float, lon: float) -> float:
    """Anomalie crustale LCS1 fallback (EMAG2 live non disponible ici).
    Portage index.html:2316."""
    return round(interp_idw(LCS1_GRID, lat, lon))


def get_geo_type(lat: float, lon: float) -> str:
    """Type de substrat au plus proche voisin dans GEO_SUSC_GRID.
    Portage index.html:2590."""
    best = min(GEO_SUSC_GRID,
               key=lambda p: max(1e-10, (p[0] - lat) ** 2 + (p[1] - lon) ** 2))
    return best[3] if best else 'inconnu'


def calc_geo_susc(lat: float, lon: float) -> float:
    """Susceptibilité géologique interpolée. Portage index.html:2565."""
    grid = [(p[0], p[1], p[2]) for p in GEO_SUSC_GRID]
    return round(interp_idw(grid, lat, lon, 4))


def calc_fault_proximity(lat: float, lon: float) -> float:
    """Bonus piézo proximité faille. Portage index.html:2657."""
    bonus = 0.0
    for f in FAILLES_CORSE:
        d = haversine(lat, lon, f["lat"], f["lon"])
        if d < 3:
            proximity_bonus = 1.5 * (1 - d / 3)
            type_mult = 1.0 if f["type"] == "active" else 0.7
            bonus = max(bonus, proximity_bonus * type_mult)
    return bonus


def calc_radon_proximity(lat: float, lon: float) -> float:
    """Bonus radon. Portage index.html:2696."""
    bonus = 0.0
    for z in RADON_ZONES_CORSE:
        d = haversine(lat, lon, z["lat"], z["lon"])
        if d < 5:
            base = 1.0 * (1 - d / 5)
            categ_mult = 1.0 if z["categ"] == 3 else 0.6
            bonus = max(bonus, base * categ_mult)
    return bonus


def calc_piezo_score(lat: float, lon: float) -> float:
    """Score piézo 0-100. Portage index.html:2722."""
    t = get_geo_type(lat, lon)
    qz = QUARTZ_CONTENT.get(t, 0.05)
    alt_proxy = calc_geo_susc(lat, lon)
    stress = 2 + abs(alt_proxy) / 20
    base = min(100, round(qz * stress * 15))
    fault_bonus = calc_fault_proximity(lat, lon)
    radon_bonus = calc_radon_proximity(lat, lon)
    return min(100, round(base + fault_bonus * 8 + radon_bonus * 10))


def distance_to_nearest_fault(lat: float, lon: float) -> float:
    """Distance min en km au segment de faille le plus proche."""
    return min(haversine(lat, lon, f["lat"], f["lon"]) for f in FAILLES_CORSE)


def is_land(lat: float, lon: float) -> bool:
    """Masque terrestre Corse. Portage index.html:5696."""
    if lat < 41.37 or lat > 43.01 or lon < 8.56 or lon > 9.56:
        return False
    if lat > 42.95 and (lon < 9.25 or lon > 9.45):
        return False
    if lat > 42.90 and (lon < 9.18 or lon > 9.48):
        return False
    if lat > 42.85 and lon < 9.12:
        return False
    if lat > 42.75 and lon > 9.50:
        return False
    if 42.75 < lat < 42.95 and lon < 9.15:
        return False
    if 42.15 < lat < 42.40 and lon < 8.58:
        return False
    if 42.10 < lat < 42.25 and lon < 8.60:
        return False
    if 42.05 < lat < 42.15 and lon < 8.63:
        return False
    if 41.80 < lat < 42.00 and lon < 8.62:
        return False
    if 41.62 < lat < 41.78 and lon < 8.80:
        return False
    if lat < 41.39:
        return False
    if lat < 41.60 and lon > 9.30:
        return False
    if 41.55 < lat < 41.65 and lon > 9.30:
        return False
    if lon > 9.53:
        return False
    return True


# ═══════════════════════════════════════════════════════════════════════
# 3. EXTRACTION DES MÉGALITHES depuis index.html
# ═══════════════════════════════════════════════════════════════════════

MEGA_LINE_RE = re.compile(
    r"\[\s*(\d+\.\d+)\s*,\s*(\d+\.\d+)\s*,\s*'([^']+)'\s*,\s*'Mégalithique'"
)


def extract_megaliths(path: Path) -> list[tuple[float, float, str]]:
    """Extrait les entrées SITES de type 'Mégalithique' depuis index.html."""
    html = path.read_text(encoding="utf-8")
    # On restreint au bloc `let SITES=[…];` pour ne pas attraper des tokens
    start = html.find("let SITES=[")
    if start < 0:
        raise RuntimeError("Bloc SITES introuvable dans index.html")
    # fin heuristique : la fermeture `];` de l'array (premier après le début)
    block = html[start:]
    end = block.find("];")
    if end < 0:
        raise RuntimeError("Fin du bloc SITES introuvable")
    block = block[: end + 2]
    entries = []
    for m in MEGA_LINE_RE.finditer(block):
        lat, lon, nom = float(m.group(1)), float(m.group(2)), m.group(3)
        entries.append((lat, lon, nom))
    return entries


# ═══════════════════════════════════════════════════════════════════════
# 4. POINTS DE CONTRÔLE ALÉATOIRES
# ═══════════════════════════════════════════════════════════════════════

def generate_random_land(n: int, rng: random.Random) -> list[tuple[float, float]]:
    """n points aléatoires uniformes sur la Corse terrestre (rejection sampling)."""
    out: list[tuple[float, float]] = []
    tries = 0
    max_tries = n * 200
    while len(out) < n and tries < max_tries:
        lat = rng.uniform(41.37, 43.01)
        lon = rng.uniform(8.56, 9.56)
        tries += 1
        if is_land(lat, lon):
            out.append((lat, lon))
    if len(out) < n:
        raise RuntimeError(f"Échantillonnage incomplet : {len(out)}/{n}")
    return out


# ═══════════════════════════════════════════════════════════════════════
# 5. CALCUL DES MÉTRIQUES
# ═══════════════════════════════════════════════════════════════════════

GRANITE_TYPES = {"granit", "granit_biotite", "granit_rose", "granodiorite"}
QUARTZ_RICH_TYPES = {"granit_biotite", "granit_rose", "granit"}  # quartz > 0.25


def metrics(points):
    """Retourne un dict de listes pour vectorisation numpy."""
    geo_types = [get_geo_type(lat, lon) for lat, lon in points]
    return {
        "lat": np.array([p[0] for p in points]),
        "lon": np.array([p[1] for p in points]),
        "geoType": np.array(geo_types, dtype=object),
        "piezoScore": np.array([calc_piezo_score(lat, lon) for lat, lon in points]),
        "distanceFaille": np.array([distance_to_nearest_fault(lat, lon) for lat, lon in points]),
        "crustal": np.array([calc_lcs1(lat, lon) for lat, lon in points]),
        "isGranite": np.array([t in GRANITE_TYPES for t in geo_types]),
        "isQuartz": np.array([t in QUARTZ_RICH_TYPES for t in geo_types]),
    }


# ═══════════════════════════════════════════════════════════════════════
# 6. TESTS STATISTIQUES
# ═══════════════════════════════════════════════════════════════════════

def summarize_group(name, m):
    print(f"  [{name}] n={len(m['piezoScore'])}")
    for key in ("piezoScore", "distanceFaille", "crustal"):
        arr = m[key]
        print(f"    {key:>15s}  mean={arr.mean():7.2f}  median={np.median(arr):7.2f}  "
              f"std={arr.std(ddof=1):7.2f}  min={arr.min():7.2f}  max={arr.max():7.2f}")
    print(f"    granite: {m['isGranite'].sum()}/{len(m['isGranite'])} "
          f"({100*m['isGranite'].mean():.1f}%)  "
          f"quartz-rich: {m['isQuartz'].sum()} ({100*m['isQuartz'].mean():.1f}%)")


def run_tests(mega, ctrl):
    print("\n══ TESTS STATISTIQUES ══")
    results = {}

    # 1. Mann-Whitney U — piézo
    u, p = stats.mannwhitneyu(mega["piezoScore"], ctrl["piezoScore"],
                              alternative="greater")
    results["MW_piezo"] = (u, p)
    print(f"[Mann-Whitney] piezoScore mega > ctrl :  U={u:.1f}  p={p:.4g}")

    # 2. Kolmogorov-Smirnov — distance failles (mega < ctrl => failles plus proches)
    ks, p = stats.ks_2samp(mega["distanceFaille"], ctrl["distanceFaille"])
    results["KS_fault"] = (ks, p)
    print(f"[Kolmogorov-Smirnov] distanceFaille mega vs ctrl :  D={ks:.4f}  p={p:.4g}")

    # 2b. Mann-Whitney (mega plus proche des failles)
    u2, p2 = stats.mannwhitneyu(mega["distanceFaille"], ctrl["distanceFaille"],
                                alternative="less")
    results["MW_fault_less"] = (u2, p2)
    print(f"[Mann-Whitney] distanceFaille mega < ctrl :  U={u2:.1f}  p={p2:.4g}")

    # 3. Chi-2 — granit
    n1 = int(mega["isGranite"].sum())
    n2 = int(ctrl["isGranite"].sum())
    table = np.array([
        [n1, len(mega["isGranite"]) - n1],
        [n2, len(ctrl["isGranite"]) - n2],
    ])
    chi2, p, dof, _ = stats.chi2_contingency(table)
    results["chi2_granite"] = (chi2, p, table)
    print(f"[χ²] granite mega vs ctrl :  χ²={chi2:.3f}  dof={dof}  p={p:.4g}")
    print(f"     contingence = [mega:{n1}/{len(mega['isGranite'])}  "
          f"ctrl:{n2}/{len(ctrl['isGranite'])}]")

    # 3b. Chi-2 — quartz-rich
    n1q = int(mega["isQuartz"].sum())
    n2q = int(ctrl["isQuartz"].sum())
    tableq = np.array([
        [n1q, len(mega["isQuartz"]) - n1q],
        [n2q, len(ctrl["isQuartz"]) - n2q],
    ])
    chi2q, pq, _, _ = stats.chi2_contingency(tableq)
    results["chi2_quartz"] = (chi2q, pq, tableq)
    print(f"[χ²] quartz-rich mega vs ctrl :  χ²={chi2q:.3f}  p={pq:.4g}")

    # 4. Spearman — piezo × crustal (mégalithes)
    r, p = stats.spearmanr(mega["piezoScore"], mega["crustal"])
    results["spearman"] = (r, p)
    print(f"[Spearman] piezo × crustal (mega) :  ρ={r:.3f}  p={p:.4g}")

    # 5. KS sur crustal (mega plus +ive ?)
    ks_c, p_c = stats.ks_2samp(mega["crustal"], ctrl["crustal"])
    results["KS_crustal"] = (ks_c, p_c)
    print(f"[Kolmogorov-Smirnov] crustal mega vs ctrl :  D={ks_c:.4f}  p={p_c:.4g}")

    return results


# ═══════════════════════════════════════════════════════════════════════
# 7. VISUALISATIONS
# ═══════════════════════════════════════════════════════════════════════

def plot_piezo_hist(mega, ctrl, out):
    fig, ax = plt.subplots(figsize=(8, 5))
    bins = np.linspace(0, 100, 26)
    ax.hist(ctrl["piezoScore"], bins=bins, density=True, alpha=0.5,
            label=f"Aléatoires (n={len(ctrl['piezoScore'])})", color="#9ca3af")
    ax.hist(mega["piezoScore"], bins=bins, density=True, alpha=0.7,
            label=f"Mégalithes (n={len(mega['piezoScore'])})", color="#854d0e")
    ax.axvline(mega["piezoScore"].mean(), color="#854d0e", linestyle="--", lw=1.5,
               label=f"Moyenne mégalithes: {mega['piezoScore'].mean():.1f}")
    ax.axvline(ctrl["piezoScore"].mean(), color="#4b5563", linestyle="--", lw=1.5,
               label=f"Moyenne aléatoires: {ctrl['piezoScore'].mean():.1f}")
    ax.set_xlabel("Score piézoélectrique (0-100)")
    ax.set_ylabel("Densité")
    ax.set_title("Distribution du score piézo — mégalithes vs points aléatoires")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)


def plot_fault_hist(mega, ctrl, out):
    fig, ax = plt.subplots(figsize=(8, 5))
    bins = np.linspace(0, 80, 41)
    ax.hist(ctrl["distanceFaille"], bins=bins, density=True, alpha=0.5,
            label=f"Aléatoires (n={len(ctrl['distanceFaille'])})", color="#9ca3af")
    ax.hist(mega["distanceFaille"], bins=bins, density=True, alpha=0.7,
            label=f"Mégalithes (n={len(mega['distanceFaille'])})", color="#854d0e")
    ax.axvline(np.median(mega["distanceFaille"]), color="#854d0e", linestyle="--",
               lw=1.5, label=f"Médiane mégalithes: {np.median(mega['distanceFaille']):.1f} km")
    ax.axvline(np.median(ctrl["distanceFaille"]), color="#4b5563", linestyle="--",
               lw=1.5, label=f"Médiane aléatoires: {np.median(ctrl['distanceFaille']):.1f} km")
    ax.set_xlabel("Distance au segment de faille BRGM le plus proche (km)")
    ax.set_ylabel("Densité")
    ax.set_title("Distance aux failles tectoniques — mégalithes vs aléatoires")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)


def plot_scatter(mega, out):
    fig, ax = plt.subplots(figsize=(7, 9))
    sc = ax.scatter(mega["lon"], mega["lat"], c=mega["piezoScore"],
                    cmap="YlOrRd", edgecolor="black", s=60, vmin=0, vmax=100)
    # Failles en superposition
    for f in FAILLES_CORSE:
        ax.plot(f["lon"], f["lat"], marker="x", color="#2563eb", markersize=10,
                markeredgewidth=2)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("Sites mégalithiques — coloration par score piézo\n"
                 "(× = failles BRGM)")
    cbar = fig.colorbar(sc, ax=ax, shrink=0.7)
    cbar.set_label("piezoScore")
    ax.set_aspect(1.35)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)


def plot_crustal_box(mega, ctrl, out):
    fig, ax = plt.subplots(figsize=(6, 5))
    data = [ctrl["crustal"], mega["crustal"]]
    labels = [f"Aléatoires\n(n={len(ctrl['crustal'])})",
              f"Mégalithes\n(n={len(mega['crustal'])})"]
    bp = ax.boxplot(data, labels=labels, patch_artist=True, showmeans=True,
                    meanprops=dict(marker="D", markerfacecolor="white",
                                   markeredgecolor="black"))
    for patch, color in zip(bp["boxes"], ["#9ca3af", "#854d0e"]):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)
    ax.set_ylabel("Anomalie crustale LCS1 (nT)")
    ax.set_title("Anomalie crustale — mégalithes vs aléatoires")
    ax.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════════
# 8. RAPPORT MARKDOWN
# ═══════════════════════════════════════════════════════════════════════

def format_pvalue(p: float) -> str:
    if p < 0.001:
        return f"**p = {p:.3g}** (très significatif)"
    if p < 0.01:
        return f"**p = {p:.3g}** (significatif)"
    if p < 0.05:
        return f"**p = {p:.3g}** (significatif au seuil 5 %)"
    return f"p = {p:.3g} (non significatif)"


def write_report(mega, ctrl, results, out_path: Path):
    ps_m = mega["piezoScore"]
    ps_c = ctrl["piezoScore"]
    df_m = mega["distanceFaille"]
    df_c = ctrl["distanceFaille"]
    cr_m = mega["crustal"]
    cr_c = ctrl["crustal"]

    u_piezo, p_piezo = results["MW_piezo"]
    ks_f, p_ks_f = results["KS_fault"]
    u_fault, p_fault = results["MW_fault_less"]
    chi2_g, p_g, tab_g = results["chi2_granite"]
    chi2_q, p_q, tab_q = results["chi2_quartz"]
    rho, p_rho = results["spearman"]
    ks_c, p_ks_c = results["KS_crustal"]

    any_significant = (
        p_piezo < 0.05 or p_fault < 0.05 or p_g < 0.05 or p_q < 0.05
        or (p_rho < 0.05) or p_ks_c < 0.05
    )

    md = []
    md.append("# Tellux — Corrélation mégalithes × failles × piézoélectricité")
    md.append("")
    md.append(f"_Analyse v1 · 2026-04-17 · branche source : `dev` · seed = {SEED}_")
    md.append("")
    md.append("## Résumé exécutif")
    md.append("")
    if any_significant:
        md.append(
            f"Sur **{len(ps_m)} sites mégalithiques** comparés à "
            f"**{len(ps_c)} points terrestres aléatoires**, plusieurs "
            "tests statistiques rejettent l'hypothèse nulle d'une implantation au "
            "hasard. Les mégalithes corses montrent un biais vers un substrat "
            "piézoélectrique, une proximité aux failles, et/ou une anomalie "
            "crustale différente. Résultat à discuter ci-dessous."
        )
    else:
        md.append(
            f"Sur **{len(ps_m)} sites mégalithiques** comparés à "
            f"**{len(ps_c)} points terrestres aléatoires**, aucun des tests "
            "ne permet de rejeter l'hypothèse nulle au seuil 5 %. L'implantation "
            "des mégalithes n'est pas distinguable du hasard selon les variables "
            "piézoScore / distance aux failles / anomalie crustale telles que "
            "modélisées par Tellux."
        )
    md.append("")

    md.append("## Méthodologie")
    md.append("")
    md.append("### Données")
    md.append(f"- **{len(ps_m)} sites mégalithiques** extraits de `index.html` "
              "(tableau `SITES` filtré sur `type == 'Mégalithique'`).")
    md.append(f"- **{len(ps_c)} points de contrôle aléatoires**, tirage uniforme "
              "sur la bounding box Corse (41.37–43.01°N, 8.56–9.56°E) avec "
              "rejection sampling via `is_land()` (portage fidèle de la fonction "
              "JS `isLand` d'index.html).")
    md.append("")
    md.append("### Variables calculées pour chaque point")
    md.append("| Variable | Portage JS | Type |")
    md.append("|---|---|---|")
    md.append("| `geoType` | `getGeoType(lat,lon)` (nearest-neighbor sur `GEO_SUSC_GRID`) | catégorielle |")
    md.append("| `piezoScore` | `calcPiezoScore(lat,lon)` (Bishop 1981 + bonus faille + bonus radon) | 0–100 |")
    md.append("| `distanceFaille` | `min(haversine)` sur `FAILLES_CORSE` (BRGM) | km |")
    md.append("| `crustal` | `calcLCS1(lat,lon)` (IDW sur `LCS1_GRID`) | nT |")
    md.append("| `isGranite` | `geoType ∈ {granit, granit_biotite, granit_rose, granodiorite}` | bool |")
    md.append("| `isQuartz` | `geoType ∈ {granit_biotite, granit_rose, granit}` (quartz ≥ 0.25) | bool |")
    md.append("")
    md.append("### Tests statistiques")
    md.append("- Mann-Whitney U (unilatéral) : `piezoScore` mégalithes > aléatoires.")
    md.append("- Kolmogorov-Smirnov 2 échantillons : `distanceFaille` distributions.")
    md.append("- Mann-Whitney U (unilatéral) : `distanceFaille` mégalithes < aléatoires.")
    md.append("- χ² de contingence 2×2 : `isGranite` / `isQuartz`.")
    md.append("- Spearman ρ : `piezoScore` × `crustal` sur les mégalithes seuls.")
    md.append("- Kolmogorov-Smirnov : distribution `crustal`.")
    md.append("")

    md.append("## Résultats")
    md.append("")
    md.append("### Statistiques descriptives")
    md.append("")
    md.append("| Variable | Mégalithes (moy. / méd. / σ) | Aléatoires (moy. / méd. / σ) |")
    md.append("|---|---|---|")
    md.append(f"| piezoScore | {ps_m.mean():.2f} / {np.median(ps_m):.2f} / "
              f"{ps_m.std(ddof=1):.2f} | {ps_c.mean():.2f} / "
              f"{np.median(ps_c):.2f} / {ps_c.std(ddof=1):.2f} |")
    md.append(f"| distanceFaille (km) | {df_m.mean():.2f} / {np.median(df_m):.2f} / "
              f"{df_m.std(ddof=1):.2f} | {df_c.mean():.2f} / "
              f"{np.median(df_c):.2f} / {df_c.std(ddof=1):.2f} |")
    md.append(f"| crustal (nT) | {cr_m.mean():.2f} / {np.median(cr_m):.2f} / "
              f"{cr_m.std(ddof=1):.2f} | {cr_c.mean():.2f} / "
              f"{np.median(cr_c):.2f} / {cr_c.std(ddof=1):.2f} |")
    md.append(f"| % granite | {100*mega['isGranite'].mean():.1f} % | "
              f"{100*ctrl['isGranite'].mean():.1f} % |")
    md.append(f"| % quartz-rich | {100*mega['isQuartz'].mean():.1f} % | "
              f"{100*ctrl['isQuartz'].mean():.1f} % |")
    md.append("")

    md.append("### Tests")
    md.append("")
    md.append("| Test | Statistique | p-value | Interprétation |")
    md.append("|---|---|---|---|")
    md.append(f"| MW U — piezo mega > ctrl | U = {u_piezo:.1f} | {p_piezo:.4g} | "
              f"{'rejet H0' if p_piezo < 0.05 else 'non signif.'} |")
    md.append(f"| KS — distanceFaille | D = {ks_f:.4f} | {p_ks_f:.4g} | "
              f"{'rejet H0' if p_ks_f < 0.05 else 'non signif.'} |")
    md.append(f"| MW U — faille mega < ctrl | U = {u_fault:.1f} | {p_fault:.4g} | "
              f"{'rejet H0' if p_fault < 0.05 else 'non signif.'} |")
    md.append(f"| χ² — granite | χ² = {chi2_g:.3f} | {p_g:.4g} | "
              f"{'rejet H0' if p_g < 0.05 else 'non signif.'} |")
    md.append(f"| χ² — quartz-rich | χ² = {chi2_q:.3f} | {p_q:.4g} | "
              f"{'rejet H0' if p_q < 0.05 else 'non signif.'} |")
    md.append(f"| Spearman — piezo × crustal (mega) | ρ = {rho:.3f} | {p_rho:.4g} | "
              f"{'corrélation signif.' if p_rho < 0.05 else 'non signif.'} |")
    md.append(f"| KS — crustal | D = {ks_c:.4f} | {p_ks_c:.4g} | "
              f"{'rejet H0' if p_ks_c < 0.05 else 'non signif.'} |")
    md.append("")

    md.append("### Graphiques")
    md.append("")
    md.append("![Histogramme piezoScore](piezo_hist.png)")
    md.append("")
    md.append("![Histogramme distance failles](fault_hist.png)")
    md.append("")
    md.append("![Carte mégalithes](megaliths_map.png)")
    md.append("")
    md.append("![Boxplot anomalie crustale](crustal_box.png)")
    md.append("")

    md.append("## Discussion")
    md.append("")
    if p_piezo < 0.05:
        md.append(
            f"- **piezoScore** : les mégalithes ont un score piézo "
            f"significativement plus élevé que le hasard ({format_pvalue(p_piezo)}). "
            "Cohérent avec l'implantation préférentielle sur granit quartzifère "
            "(Bishop 1981, Ghilardi 2017)."
        )
    else:
        md.append(
            f"- **piezoScore** : pas de différence significative "
            f"({format_pvalue(p_piezo)}). L'absence d'effet peut provenir d'un "
            "score piézo trop grossier (grille 34 points pour la Corse entière), "
            "ou d'une réalité : les bâtisseurs n'auraient pas sélectionné "
            "spécifiquement les zones à quartz."
        )

    if p_fault < 0.05:
        md.append(
            f"- **distance aux failles** : les mégalithes sont significativement "
            f"plus proches des failles BRGM que des points aléatoires "
            f"({format_pvalue(p_fault)}). Supporte l'hypothèse d'un choix lié à "
            "la contrainte tectonique (piézo-activité accrue)."
        )
    else:
        md.append(
            f"- **distance aux failles** : {format_pvalue(p_fault)}. Le jeu "
            "`FAILLES_CORSE` ne contient que 8 segments — résolution insuffisante "
            "pour un test robuste. Recommander intégration données BRGM complètes."
        )

    if p_g < 0.05:
        md.append(
            f"- **granite** : proportion de mégalithes sur granite "
            f"significativement différente du hasard ({format_pvalue(p_g)})."
        )
    else:
        md.append(f"- **granite** : {format_pvalue(p_g)}.")

    if p_q < 0.05:
        md.append(
            f"- **quartz-rich** : sélection significative vers substrats riches "
            f"en quartz ({format_pvalue(p_q)})."
        )
    else:
        md.append(f"- **quartz-rich** : {format_pvalue(p_q)}.")

    if p_rho < 0.05:
        md.append(
            f"- **corrélation piezo × crustal sur les mégalithes** : "
            f"ρ = {rho:.3f} ({format_pvalue(p_rho)}). Les deux signaux "
            "géophysiques covarient sur les sites anciens."
        )
    else:
        md.append(
            f"- **corrélation piezo × crustal** : ρ = {rho:.3f} "
            f"({format_pvalue(p_rho)})."
        )

    md.append("")
    md.append("### Biais et limites")
    md.append("- **Grilles de faible résolution** : `GEO_SUSC_GRID` (34 points), "
              "`LCS1_GRID` (24 points), `FAILLES_CORSE` (8 segments), "
              "`RADON_ZONES_CORSE` (8 centres). Interpolation IDW grossière.")
    md.append("- **`piezoScore` circulaire** : il intègre déjà `calcFaultProximity` "
              "et `calcRadonProximity`. Un test indépendant piezo vs failles est "
              "donc biaisé à la hausse. Interpréter avec prudence.")
    md.append("- **Biais de découverte** : les 67 mégalithes connus sont sur-"
              "représentés dans les zones accessibles (Sartenais, Cauria, "
              "Alta Rocca). Le jeu `SITES` reflète 200 ans de prospection, pas "
              "une distribution tirée au hasard du passé.")
    md.append("- **Types de substrat discrets** : `getGeoType` prend le plus "
              "proche voisin parmi 34 points — absence de gradient local.")
    md.append("- **Pas de référence EMAG2 live** : on utilise `LCS1_GRID` "
              "(fallback interne), donc le test sur `crustal` mesure surtout la "
              "cohérence interne de Tellux, pas les données NOAA.")
    md.append("")

    md.append("## Implications pour Tellux")
    md.append("")
    if any_significant:
        md.append("- Plusieurs signaux convergent vers H1. À consolider avant "
                  "toute communication scientifique : élargir le jeu de failles, "
                  "intégrer l'EMAG2v3 ponctuel, et tester sur un tiers des sites "
                  "(holdout) pour éviter sur-apprentissage des grilles.")
        md.append("- Dossier CTC : mentionner comme **résultat préliminaire** "
                  "avec intervalle de confiance, pas comme conclusion.")
        md.append("- Piste publication si renforcé : *Journal of Archaeological "
                  "Science* (archéométrie) ou *Journal of Archaeological Method "
                  "and Theory* (cadrage statistique). Nécessite : données failles "
                  "BRGM complètes (GeoJSON 1/50k), protocole pré-enregistré, "
                  "matériel supplémentaire reproductible.")
    else:
        md.append("- **Pas de signal clair**. Avant d'invoquer H1 publiquement, "
                  "faire tourner l'analyse sur des données géophysiques plus "
                  "résolues (BRGM failles complètes, EMAG2v3 live).")
        md.append("- Dossier CTC : décrire H1 comme **testable** et "
                  "**actuellement non confirmée par les données internes de "
                  "Tellux** — rigueur épistémologique avant tout.")
        md.append("- Éviter toute formulation \"les anciens bâtissaient sur des "
                  "zones piézo\" dans le discours public tant que les p-values "
                  "restent > 0.05.")

    md.append("")
    md.append("## Reproductibilité")
    md.append(f"- Seed : `{SEED}`")
    md.append(f"- Script : `analysis/correlate_megaliths.py`")
    md.append("- Dépendances : `numpy`, `scipy`, `matplotlib`")
    md.append("- Commande : `python analysis/correlate_megaliths.py`")
    md.append("")
    out_path.write_text("\n".join(md), encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

def main():
    print(f"Tellux — analyse corrélation mégalithes (seed={SEED})")

    # Extraction mégalithes
    mega_sites = extract_megaliths(INDEX_HTML)
    print(f"Mégalithes extraits : {len(mega_sites)}")

    # Filtrer sur land (cohérence)
    mega_sites_land = [(lat, lon) for lat, lon, _ in mega_sites if is_land(lat, lon)]
    excluded = len(mega_sites) - len(mega_sites_land)
    if excluded:
        print(f"  (exclus {excluded} sites hors mask is_land)")
    mega_pts = mega_sites_land

    # Points aléatoires
    rng = random.Random(SEED)
    ctrl_pts = generate_random_land(500, rng)
    print(f"Points aléatoires générés : {len(ctrl_pts)}")

    # Métriques
    print("Calcul métriques mégalithes…")
    mega_m = metrics(mega_pts)
    print("Calcul métriques contrôles…")
    ctrl_m = metrics(ctrl_pts)

    summarize_group("mégalithes", mega_m)
    summarize_group("aléatoires", ctrl_m)

    # Tests
    results = run_tests(mega_m, ctrl_m)

    # Plots
    plot_piezo_hist(mega_m, ctrl_m, ROOT / "piezo_hist.png")
    plot_fault_hist(mega_m, ctrl_m, ROOT / "fault_hist.png")
    plot_scatter(mega_m, ROOT / "megaliths_map.png")
    plot_crustal_box(mega_m, ctrl_m, ROOT / "crustal_box.png")
    print(f"\nGraphiques écrits dans {ROOT}/ (4 PNG)")

    # Rapport
    report_path = ROOT / "TELLUX_CORRELATION_MEGALITHS_v1.md"
    write_report(mega_m, ctrl_m, results, report_path)
    print(f"Rapport : {report_path}")


if __name__ == "__main__":
    main()
