"""
app.py — Corporate Scope 1, 2 & 3 Carbon Accounting Dashboard
================================================================
An interactive Streamlit dashboard that ingests corporate activity data
(fuel, electricity, travel, logistics, commuting, purchased goods spend)
and computes Scope 1, 2 and 3 GHG emissions, mapped to SEBI's BRSR and
GRI 305 disclosure frameworks.

Run locally:
    pip install -r requirements.txt
    streamlit run app.py
"""
import io
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import emission_factors as ef
import calculations as calc
import sample_data_generator as sdg

st.set_page_config(
    page_title="Corporate Carbon Accounting Dashboard",
    page_icon="🌱",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Sidebar — company info, data source, editable emission factors
# ---------------------------------------------------------------------------
st.sidebar.title("🌱 Carbon Dashboard Setup")

company_name = st.sidebar.text_input("Company name", "GreenTech Manufacturing Ltd.")
reporting_year = st.sidebar.text_input("Reporting period", "FY 2024-25")

st.sidebar.markdown("---")
data_source = st.sidebar.radio(
    "Data source",
    ["Use sample data (fictitious company)", "Upload my own CSVs"],
    index=0,
)

def load_default_or_uploaded(label, default_df, key):
    if data_source == "Upload my own CSVs":
        uploaded = st.sidebar.file_uploader(label, type="csv", key=key)
        if uploaded is not None:
            return pd.read_csv(uploaded)
        st.sidebar.caption(f"No file uploaded for {label} — using sample data.")
    return default_df

fuel_default = sdg.generate_fuel_data()
elec_default = sdg.generate_electricity_data()
travel_default = sdg.generate_travel_data()
logistics_default = sdg.generate_logistics_data()
commute_default = sdg.generate_commuting_data()
spend_default = sdg.generate_spend_data()
revenue_default = sdg.generate_revenue_data()

if data_source == "Upload my own CSVs":
    st.sidebar.markdown("**Upload activity data (columns must match sample templates):**")
    fuel_df = load_default_or_uploaded("Fuel consumption", fuel_default, "fuel")
    elec_df = load_default_or_uploaded("Electricity consumption", elec_default, "elec")
    travel_df = load_default_or_uploaded("Business travel", travel_default, "travel")
    logistics_df = load_default_or_uploaded("Logistics (tonne-km)", logistics_default, "logi")
    commute_df = load_default_or_uploaded("Employee commuting", commute_default, "commute")
    spend_df = load_default_or_uploaded("Purchased goods spend", spend_default, "spend")
    revenue_df = load_default_or_uploaded("Revenue", revenue_default, "rev")
else:
    fuel_df, elec_df, travel_df = fuel_default, elec_default, travel_default
    logistics_df, commute_df = logistics_default, commute_default
    spend_df, revenue_df = spend_default, revenue_default

st.sidebar.markdown("---")
st.sidebar.subheader("Emission factors (editable)")
st.sidebar.caption(
    "Defaults are illustrative. Replace with the latest official CEA / IPCC / "
    "GHG Protocol figures before using this for real disclosure."
)

grid_factor = st.sidebar.number_input(
    "CEA Grid Emission Factor (kg CO2 / kWh)",
    value=ef.CEA_GRID_EMISSION_FACTOR_KG_PER_KWH, step=0.001, format="%.3f",
)

with st.sidebar.expander("Fuel combustion factors (Scope 1)"):
    fuel_factors = {}
    for k, v in ef.FUEL_EMISSION_FACTORS.items():
        fuel_factors[k] = st.number_input(k, value=float(v), step=0.01, key=f"ff_{k}")

with st.sidebar.expander("Travel factors (Scope 3)"):
    travel_factors = {}
    for k, v in ef.TRAVEL_EMISSION_FACTORS.items():
        travel_factors[k] = st.number_input(k, value=float(v), step=0.001, format="%.3f", key=f"tf_{k}")

with st.sidebar.expander("Logistics / commuting / spend factors (Scope 3)"):
    logistics_factor = st.number_input(
        "Logistics (kg CO2 / tonne-km)", value=ef.LOGISTICS_EMISSION_FACTOR_KG_PER_TONNE_KM,
        step=0.001, format="%.3f",
    )
    commute_factor = st.number_input(
        "Commuting (kg CO2 / km)", value=ef.COMMUTE_EMISSION_FACTOR_KG_PER_KM,
        step=0.001, format="%.3f",
    )
    spend_factors = {}
    for k, v in ef.SPEND_BASED_EMISSION_FACTORS.items():
        spend_factors[k] = st.number_input(k, value=float(v), step=0.1, key=f"sf_{k}")

# ---------------------------------------------------------------------------
# Calculations
# ---------------------------------------------------------------------------
scope1_detail = calc.calc_scope1(fuel_df, fuel_factors)
scope2_detail = calc.calc_scope2(elec_df, grid_factor)
travel_totals = calc.calc_scope3_travel(travel_df, travel_factors)
logistics_totals = calc.calc_scope3_logistics(logistics_df, logistics_factor)
commute_totals = calc.calc_scope3_commuting(commute_df, commute_factor)
spend_totals = calc.calc_scope3_purchased_goods(spend_df, spend_factors)
scope3_detail = calc.combine_scope3(travel_totals, logistics_totals, commute_totals, spend_totals)
summary = calc.build_summary(scope1_detail, scope2_detail, scope3_detail, revenue_df)

total_t = summary["Total Emissions (tCO2e)"].sum()
s1_t = scope1_detail["Scope 1 Total (kg CO2e)"].sum() / 1000
s2_t = scope2_detail["Scope 2 Total (kg CO2e)"].sum() / 1000
s3_t = scope3_detail["Scope 3 Total (kg CO2e)"].sum() / 1000

# ---------------------------------------------------------------------------
# Header + KPIs
# ---------------------------------------------------------------------------
st.title("Corporate Scope 1, 2 & 3 Carbon Accounting Dashboard")
st.caption(f"{company_name} · {reporting_year} · Aligned to SEBI BRSR & GRI 305")

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Emissions", f"{total_t:,.1f} tCO2e")
k2.metric("Scope 1 (Direct)", f"{s1_t:,.1f} tCO2e", f"{s1_t/total_t*100:.0f}% of total" if total_t else None)
k3.metric("Scope 2 (Energy)", f"{s2_t:,.1f} tCO2e", f"{s2_t/total_t*100:.0f}% of total" if total_t else None)
k4.metric("Scope 3 (Value chain)", f"{s3_t:,.1f} tCO2e", f"{s3_t/total_t*100:.0f}% of total" if total_t else None)

if "Emission Intensity (tCO2e / INR Lakh Revenue)" in summary.columns:
    avg_intensity = summary["Emission Intensity (tCO2e / INR Lakh Revenue)"].mean()
    st.caption(f"Average emission intensity: **{avg_intensity:.4f} tCO2e per INR Lakh revenue**")

st.markdown("---")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_overview, tab_s1, tab_s2, tab_s3, tab_brsr, tab_data = st.tabs(
    ["📊 Overview", "🔥 Scope 1", "⚡ Scope 2", "🌍 Scope 3", "📋 BRSR / GRI Mapping", "🗂 Raw Data"]
)

with tab_overview:
    c1, c2 = st.columns([1, 1])
    with c1:
        fig_pie = px.pie(
            names=["Scope 1", "Scope 2", "Scope 3"],
            values=[s1_t, s2_t, s3_t],
            title="Emissions by Scope",
            color_discrete_sequence=["#e07a5f", "#3d5a80", "#81b29a"],
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    with c2:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Bar(x=summary["Month"], y=summary["Scope 1 Total (kg CO2e)"] / 1000, name="Scope 1"))
        fig_trend.add_trace(go.Bar(x=summary["Month"], y=summary["Scope 2 Total (kg CO2e)"] / 1000, name="Scope 2"))
        fig_trend.add_trace(go.Bar(x=summary["Month"], y=summary["Scope 3 Total (kg CO2e)"] / 1000, name="Scope 3"))
        fig_trend.update_layout(barmode="stack", title="Monthly Emissions Trend (tCO2e)")
        st.plotly_chart(fig_trend, use_container_width=True)

    if "Emission Intensity (tCO2e / INR Lakh Revenue)" in summary.columns:
        fig_intensity = px.line(
            summary, x="Month", y="Emission Intensity (tCO2e / INR Lakh Revenue)",
            markers=True, title="Emission Intensity Trend (GRI 305-4)",
        )
        st.plotly_chart(fig_intensity, use_container_width=True)

    st.subheader("Summary table")
    st.dataframe(summary, use_container_width=True)

    csv_buf = io.StringIO()
    summary.to_csv(csv_buf, index=False)
    st.download_button(
        "⬇ Download summary as CSV", csv_buf.getvalue(),
        file_name=f"{company_name.replace(' ', '_')}_emissions_summary.csv", mime="text/csv",
    )

with tab_s1:
    st.subheader("Scope 1 — Direct Emissions (Fuel Combustion)")
    st.caption("Company-owned generators, boilers, vehicles etc. Activity data × IPCC/national fuel factors.")
    breakdown_cols = [c for c in scope1_detail.columns if c not in ("Month", "Scope 1 Total (kg CO2e)")]
    fig = px.bar(scope1_detail, x="Month", y=breakdown_cols, title="Scope 1 Emissions by Fuel Type (kg CO2e)")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(scope1_detail, use_container_width=True)

with tab_s2:
    st.subheader("Scope 2 — Purchased Grid Electricity")
    st.caption("Grid kWh × CEA combined-margin emission factor. Renewable/green power purchases assumed 0 emission.")
    fig = px.bar(scope2_detail, x="Month", y="Grid Electricity Emissions (kg CO2e)",
                 title="Scope 2 Emissions (kg CO2e)")
    st.plotly_chart(fig, use_container_width=True)
    if "Renewable/Purchased Green Power (kWh)" in elec_df.columns:
        renew_share = (
            elec_df["Renewable/Purchased Green Power (kWh)"].sum()
            / (elec_df["Grid Electricity (kWh)"].sum() + elec_df["Renewable/Purchased Green Power (kWh)"].sum())
            * 100
        )
        st.metric("Renewable electricity share", f"{renew_share:.1f}%")
    st.dataframe(scope2_detail, use_container_width=True)

with tab_s3:
    st.subheader("Scope 3 — Value Chain Emissions")
    st.caption("Selected categories: Business travel (Cat. 6), upstream/downstream logistics (Cat. 4/9), "
               "employee commuting (Cat. 7), purchased goods & services — spend-based (Cat. 1).")
    fig = px.bar(
        scope3_detail, x="Month",
        y=["Business Travel Total (kg CO2e)", "Logistics Total (kg CO2e)",
           "Commuting Total (kg CO2e)", "Purchased Goods Total (kg CO2e)"],
        title="Scope 3 Emissions by Category (kg CO2e)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(scope3_detail, use_container_width=True)

with tab_brsr:
    st.subheader("BRSR & GRI 305 Disclosure Mapping")
    st.caption("How the categories in this dashboard map to SEBI's Business Responsibility & "
               "Sustainability Reporting (BRSR) Principle 6 and GRI 305.")
    st.table(pd.DataFrame(ef.BRSR_GRI_MAPPING))

    st.markdown("#### Suggested reduction roadmap (auto-generated from data)")
    biggest_scope = max([("Scope 1", s1_t), ("Scope 2", s2_t), ("Scope 3", s3_t)], key=lambda x: x[1])
    st.markdown(
        f"- **{biggest_scope[0]}** is the largest contributor ({biggest_scope[1]/total_t*100:.0f}% of total) "
        "— prioritise interventions here for the fastest reduction in total footprint.\n"
        "- If Scope 2 is significant, evaluate increasing renewable/green power procurement "
        "(open access solar/wind PPAs) to directly cut grid-tied emissions.\n"
        "- If Scope 1 is significant, evaluate fuel-switching (diesel → electric/CNG fleet, "
        "boiler efficiency upgrades) and on-site solar for captive load.\n"
        "- If Scope 3 is significant, engage top suppliers on primary emissions data collection "
        "to move from spend-based to activity-based accounting (improves BRSR data quality)."
    )

with tab_data:
    st.subheader("Raw activity data used in the calculations above")
    st.markdown("##### Fuel consumption"); st.dataframe(fuel_df, use_container_width=True)
    st.markdown("##### Electricity consumption"); st.dataframe(elec_df, use_container_width=True)
    st.markdown("##### Business travel"); st.dataframe(travel_df, use_container_width=True)
    st.markdown("##### Logistics"); st.dataframe(logistics_df, use_container_width=True)
    st.markdown("##### Employee commuting"); st.dataframe(commute_df, use_container_width=True)
    st.markdown("##### Purchased goods spend"); st.dataframe(spend_df, use_container_width=True)
    st.markdown("##### Revenue"); st.dataframe(revenue_df, use_container_width=True)

st.markdown("---")
st.caption(
    "⚠️ Educational/portfolio tool. Emission factors are illustrative defaults — verify against the "
    "latest CEA CO2 Baseline Database, IPCC 2006 Guidelines, and GHG Protocol Scope 3 guidance before "
    "using for statutory disclosure or assurance purposes."
)
