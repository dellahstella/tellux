#!/usr/bin/env python3
"""
Generate a WMM 2025 grid over Corsica for offline cross-check with IGRF-14.

Requires:
    pip install pygeomag

Output:
    public/data/wmm_2025_grid_corse.json

Grid spec:
    - Latitude: 41.3 to 43.1, step 0.05 degrees (~5.5 km)
    - Longitude: 8.5 to 9.6, step 0.05 degrees (~4.1 km a 42N)
    - Altitude: 0 km (sea level reference)
    - Date: current date at generation, decimal year

Output format:
    {
      "model": "WMM 2025",
      "source": "NOAA/BGS World Magnetic Model",
      "date_generation": "2026-04-21",
      "decimal_year": 2026.31,
      "altitude_km": 0.0,
      "grid_spec": {...},
      "n_points": 814,
      "grid": [
        {"lat": 41.30, "lon": 8.50, "total_nT": 46720, "declination_deg": 3.2, "inclination_deg": 57.6},
        ...
      ]
    }

Usage:
    python3 scripts/generate_wmm_grid_corse.py

Regeneration:
    Recommended every 1-2 years, or when WMM model is updated (next WMM: 2030).
    The pygeomag library bundles WMM 2025 coefficients so no separate .COF download
    is needed. For future major updates, install the newer pygeomag version.
"""

import json
from datetime import date
from pathlib import Path

try:
    from pygeomag import GeoMag
except ImportError:
    print("ERROR: pip install pygeomag", flush=True)
    raise SystemExit(1)

# --- Grid configuration ---
LAT_MIN, LAT_MAX, LAT_STEP = 41.3, 43.1, 0.05
LON_MIN, LON_MAX, LON_STEP = 8.5, 9.6, 0.05
ALTITUDE_KM = 0.0
REFERENCE_DATE = date.today()
DECIMAL_YEAR = REFERENCE_DATE.year + (REFERENCE_DATE.month - 1) / 12 + (REFERENCE_DATE.day - 1) / 365.25

# --- WMM 2025 initialization ---
geo = GeoMag()

# --- Grid generation ---
grid = []
lat = LAT_MIN
# Use arithmetic-safe loop (avoid float drift over many iterations)
n_lat = int(round((LAT_MAX - LAT_MIN) / LAT_STEP)) + 1
n_lon = int(round((LON_MAX - LON_MIN) / LON_STEP)) + 1

for i in range(n_lat):
    lat = round(LAT_MIN + i * LAT_STEP, 3)
    for j in range(n_lon):
        lon = round(LON_MIN + j * LON_STEP, 3)
        result = geo.calculate(glat=lat, glon=lon, alt=ALTITUDE_KM, time=DECIMAL_YEAR)
        grid.append({
            "lat": lat,
            "lon": lon,
            "total_nT": round(result.f, 1),
            "declination_deg": round(result.d, 3),
            "inclination_deg": round(result.i, 3),
        })

# --- Export JSON ---
output = {
    "model": "WMM 2025",
    "source": "NOAA/BGS World Magnetic Model, via pygeomag bundled coefficients",
    "date_generation": REFERENCE_DATE.isoformat(),
    "decimal_year": round(DECIMAL_YEAR, 3),
    "altitude_km": ALTITUDE_KM,
    "grid_spec": {
        "lat_min": LAT_MIN, "lat_max": LAT_MAX, "lat_step": LAT_STEP,
        "lon_min": LON_MIN, "lon_max": LON_MAX, "lon_step": LON_STEP,
    },
    "n_points": len(grid),
    "grid": grid,
}

out_path = Path("public/data/wmm_2025_grid_corse.json")
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"Generated {len(grid)} WMM 2025 points at {out_path}", flush=True)
print(f"File size: {out_path.stat().st_size / 1024:.1f} KB", flush=True)
