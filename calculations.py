"""
calculations.py
----------------
Pure functions that turn raw activity data into GHG emissions (kg CO2e),
given a set of emission factors. Kept separate from the Streamlit UI so the
logic is unit-testable and reusable (e.g. from a notebook or CLI).
"""
import pandas as pd


def calc_scope1(fuel_df: pd.DataFrame, fuel_factors: dict) -> pd.DataFrame:
    """Scope 1: direct fuel combustion. Returns kg CO2e per fuel type per month."""
    result = fuel_df[["Month"]].copy()
    for fuel_col, factor in fuel_factors.items():
        if fuel_col in fuel_df.columns:
            result[fuel_col] = fuel_df[fuel_col] * factor
    result["Scope 1 Total (kg CO2e)"] = result.drop(columns=["Month"]).sum(axis=1)
    return result


def calc_scope2(elec_df: pd.DataFrame, grid_factor: float) -> pd.DataFrame:
    """Scope 2: purchased grid electricity. Renewable/green power counts as 0."""
    result = elec_df[["Month"]].copy()
    if "Grid Electricity (kWh)" in elec_df.columns:
        result["Grid Electricity Emissions (kg CO2e)"] = (
            elec_df["Grid Electricity (kWh)"] * grid_factor
        )
    else:
        result["Grid Electricity Emissions (kg CO2e)"] = 0
    result["Scope 2 Total (kg CO2e)"] = result["Grid Electricity Emissions (kg CO2e)"]
    return result


def calc_scope3_travel(travel_df: pd.DataFrame, travel_factors: dict) -> pd.DataFrame:
    result = travel_df[["Month"]].copy()
    for col, factor in travel_factors.items():
        if col in travel_df.columns:
            result[col] = travel_df[col] * factor
    result["Business Travel Total (kg CO2e)"] = result.drop(columns=["Month"]).sum(axis=1)
    return result


def calc_scope3_logistics(logistics_df: pd.DataFrame, factor_per_tonne_km: float) -> pd.DataFrame:
    result = logistics_df[["Month"]].copy()
    if "Tonne-km Shipped" in logistics_df.columns:
        result["Logistics Total (kg CO2e)"] = logistics_df["Tonne-km Shipped"] * factor_per_tonne_km
    else:
        result["Logistics Total (kg CO2e)"] = 0
    return result


def calc_scope3_commuting(commute_df: pd.DataFrame, factor_per_km: float) -> pd.DataFrame:
    result = commute_df[["Month"]].copy()
    needed = {"Employees Commuting", "Avg Round-Trip Commute (km)", "Working Days"}
    if needed.issubset(commute_df.columns):
        total_km = (
            commute_df["Employees Commuting"]
            * commute_df["Avg Round-Trip Commute (km)"]
            * commute_df["Working Days"]
        )
        result["Commuting Total (kg CO2e)"] = total_km * factor_per_km
    else:
        result["Commuting Total (kg CO2e)"] = 0
    return result


def calc_scope3_purchased_goods(spend_df: pd.DataFrame, spend_factors: dict) -> pd.DataFrame:
    result = spend_df[["Month"]].copy()
    for col, factor in spend_factors.items():
        if col in spend_df.columns:
            result[col] = spend_df[col] * factor
    result["Purchased Goods Total (kg CO2e)"] = result.drop(columns=["Month"]).sum(axis=1)
    return result


def combine_scope3(travel_totals, logistics_totals, commute_totals, spend_totals) -> pd.DataFrame:
    merged = travel_totals[["Month", "Business Travel Total (kg CO2e)"]].copy()
    merged = merged.merge(logistics_totals[["Month", "Logistics Total (kg CO2e)"]], on="Month")
    merged = merged.merge(commute_totals[["Month", "Commuting Total (kg CO2e)"]], on="Month")
    merged = merged.merge(spend_totals[["Month", "Purchased Goods Total (kg CO2e)"]], on="Month")
    merged["Scope 3 Total (kg CO2e)"] = merged.drop(columns=["Month"]).sum(axis=1)
    return merged


def build_summary(scope1_df, scope2_df, scope3_df, revenue_df=None) -> pd.DataFrame:
    """Month-by-month Scope 1/2/3 totals, plus grand total and (optionally) intensity."""
    summary = scope1_df[["Month", "Scope 1 Total (kg CO2e)"]].copy()
    summary = summary.merge(scope2_df[["Month", "Scope 2 Total (kg CO2e)"]], on="Month")
    summary = summary.merge(scope3_df[["Month", "Scope 3 Total (kg CO2e)"]], on="Month")
    summary["Total Emissions (kg CO2e)"] = (
        summary["Scope 1 Total (kg CO2e)"]
        + summary["Scope 2 Total (kg CO2e)"]
        + summary["Scope 3 Total (kg CO2e)"]
    )
    summary["Total Emissions (tCO2e)"] = summary["Total Emissions (kg CO2e)"] / 1000
    if revenue_df is not None and "Revenue (INR Lakh)" in revenue_df.columns:
        summary = summary.merge(revenue_df[["Month", "Revenue (INR Lakh)"]], on="Month")
        summary["Emission Intensity (tCO2e / INR Lakh Revenue)"] = (
            summary["Total Emissions (tCO2e)"] / summary["Revenue (INR Lakh)"]
        )
    return summary
