"""
emission_factors.py
--------------------
Default emission factor libraries used by the dashboard.

IMPORTANT (methodology note):
These are illustrative, commonly-cited default values so the tool works
out of the box. For a real BRSR / GRI 305 disclosure you must replace them
with the latest published figures:
  - Scope 2 grid factor: latest CEA "CO2 Baseline Database for the Indian
    Power Sector" User Guide (Central Electricity Authority, Govt. of India)
  - Scope 1 fuel factors: IPCC 2006 Guidelines for National GHG Inventories,
    Vol. 2, Chapter 2 (Stationary Combustion) / Chapter 3 (Mobile Combustion)
  - Scope 3 factors: GHG Protocol Scope 3 Calculation Guidance, or a
    recognised database (DEFRA, EPA, Ecoinvent) for the relevant category

All factors below are exposed as editable tables in the app sidebar, so a
user can drop in audited/updated figures without touching the code.
"""

# ---------------------------------------------------------------------------
# SCOPE 2 — Purchased electricity
# ---------------------------------------------------------------------------
# CEA All-India combined margin grid emission factor (kg CO2 / kWh).
# Placeholder value in the commonly-cited ~0.70-0.73 range for the Indian
# grid. Replace with the exact figure from the latest CEA CO2 Baseline
# Database before using this for real disclosure.
CEA_GRID_EMISSION_FACTOR_KG_PER_KWH = 0.716

# ---------------------------------------------------------------------------
# SCOPE 1 — Stationary & mobile fuel combustion
# ---------------------------------------------------------------------------
# kg CO2 per unit of fuel (commonly-cited default factors; verify against
# IPCC 2006 Guidelines / MoEFCC national inventory factors before formal use)
FUEL_EMISSION_FACTORS = {
    "Diesel (litres)": 2.68,
    "Petrol (litres)": 2.31,
    "LPG (kg)": 2.98,
    "Piped Natural Gas (kg)": 2.75,
    "Furnace Oil (litres)": 3.15,
    "Coal (kg)": 2.42,
}

# ---------------------------------------------------------------------------
# SCOPE 3 — Selected categories (distance / spend based)
# ---------------------------------------------------------------------------
# Category 6: Business travel (kg CO2 per km)
TRAVEL_EMISSION_FACTORS = {
    "Domestic Flight (km)": 0.133,
    "International Flight (km)": 0.150,
    "Road - Own/Rented Vehicle (km)": 0.171,
    "Rail (km)": 0.041,
}

# Category 4/9: Upstream & downstream transportation (kg CO2 per tonne-km)
LOGISTICS_EMISSION_FACTOR_KG_PER_TONNE_KM = 0.096

# Category 7: Employee commuting (kg CO2 per km, per employee-trip)
COMMUTE_EMISSION_FACTOR_KG_PER_KM = 0.104

# Category 1: Purchased goods & services — simplified spend-based factors
# (kg CO2 per INR '000 spent, i.e. per thousand rupees). These are rough
# EEIO-style placeholders by procurement category, for illustration only.
SPEND_BASED_EMISSION_FACTORS = {
    "Raw Materials - Metals (INR '000)": 18.2,
    "Raw Materials - Plastics/Polymers (INR '000)": 21.4,
    "Packaging (INR '000)": 9.7,
    "IT & Electronics (INR '000)": 14.5,
    "Professional Services (INR '000)": 3.1,
}

# ---------------------------------------------------------------------------
# BRSR / GRI reference mapping (static, used for the disclosure tab)
# ---------------------------------------------------------------------------
BRSR_GRI_MAPPING = [
    {
        "Scope": "Scope 1",
        "Category": "Direct fuel combustion (stationary + mobile)",
        "BRSR Reference": "Principle 6, Essential Indicator 1(a) — Total Scope 1 emissions",
        "GRI Reference": "GRI 305-1 (Direct GHG emissions)",
    },
    {
        "Scope": "Scope 2",
        "Category": "Purchased grid electricity",
        "BRSR Reference": "Principle 6, Essential Indicator 1(b) — Total Scope 2 emissions",
        "GRI Reference": "GRI 305-2 (Energy indirect GHG emissions)",
    },
    {
        "Scope": "Scope 3",
        "Category": "Business travel, logistics, commuting, purchased goods",
        "BRSR Reference": "Principle 6, Leadership Indicator 1 — Scope 3 emissions & value chain",
        "GRI Reference": "GRI 305-3 (Other indirect GHG emissions)",
    },
    {
        "Scope": "Intensity",
        "Category": "Emissions per unit revenue / output",
        "BRSR Reference": "Principle 6, Essential Indicator 2 — Emission intensity",
        "GRI Reference": "GRI 305-4 (GHG emissions intensity)",
    },
]
