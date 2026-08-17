# Corporate Scope 1, 2 & 3 Carbon Accounting Dashboard

An interactive Streamlit dashboard that ingests corporate activity data (fuel, electricity, business travel, logistics, employee commuting, purchased goods spend) and calculates **Scope 1, 2, and 3 GHG emissions**, mapped to **SEBI's BRSR (Business Responsibility & Sustainability Reporting)** Principle 6 and **GRI 305** disclosure requirements.

Built for a fictitious Indian manufacturing company ("GreenTech Manufacturing Ltd.") with 12 months of sample data — swap in a real company's data to make it a live model.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

## What it does

| Scope | Category covered | Method |
|---|---|---|
| Scope 1 | Diesel, petrol, LPG, PNG, furnace oil, coal combustion | Activity data × fuel emission factor |
| Scope 2 | Purchased grid electricity | kWh × CEA grid combined-margin factor |
| Scope 3 | Business travel (Cat. 6), logistics (Cat. 4/9), employee commuting (Cat. 7), purchased goods (Cat. 1, spend-based) | Activity/spend × category factor |

The **BRSR / GRI Mapping** tab shows exactly which disclosure line each scope maps to, and auto-generates a simple reduction-priority note based on which scope is largest in the data.

All emission factors are **editable in the sidebar** — the app ships with illustrative default values (see the note below) but is built so real, audited factors can be dropped in without touching code.

## Project structure

```
carbon_dashboard/
├── app.py                     # Streamlit dashboard (UI + charts)
├── calculations.py            # Pure calculation functions (unit-testable)
├── emission_factors.py        # Default emission factor library
├── sample_data_generator.py   # Generates the 12-month sample dataset
├── sample_data/               # Pre-generated sample CSVs
├── requirements.txt
└── README.md
```

## Using your own company's data

Switch the sidebar to **"Upload my own CSVs"** and upload files matching the column headers in `sample_data/*.csv`. Typical real-world sources:
- Diesel/fuel: DG log books, fuel purchase invoices
- Electricity: utility bills / SCADA meter data
- Travel: T&E system exports (SAP Concur etc.)
- Logistics: freight/logistics MIS (tonne-km by mode)
- Purchased goods: procurement/ERP spend by category

## ⚠️ Methodology note — read before using for real disclosure

The default emission factors in `emission_factors.py` are **illustrative placeholders** so the tool works out of the box. Before using this for an actual BRSR filing, GRI report, or client deliverable, replace them with:
- **Scope 2 grid factor** → latest *CEA CO2 Baseline Database for the Indian Power Sector* (Central Electricity Authority)
- **Scope 1 fuel factors** → *IPCC 2006 Guidelines for National GHG Inventories*, Vol. 2 (Stationary Combustion) / Vol. 3 (Mobile Combustion), or MoEFCC national inventory factors
- **Scope 3 factors** → *GHG Protocol Scope 3 Calculation Guidance*, supplemented by DEFRA/EPA/Ecoinvent factors for the specific category

This keeps the tool defensible for a portfolio demo while being explicit that production use requires citing an authoritative factor source — which is itself good practice to mention in an interview.

## Resume bullet points (for this project)

**Corporate GHG Carbon Accounting & ESG Reporting Tool** | *Self-Directed Project*
- Designed an interactive Python/Streamlit dashboard to quantify Scope 1 (fuel combustion), Scope 2 (purchased grid electricity), and Scope 3 (business travel, logistics, commuting, purchased goods) carbon emissions for corporate reporting.
- Built a configurable emission-factor engine referencing CEA grid baseline factors and IPCC methodology, enabling automated recalculation as source data or factors are updated.
- Mapped carbon footprint metrics to SEBI's BRSR (Principle 6) and GRI 305 disclosure frameworks, with an auto-generated reduction-priority summary based on scope contribution.

## Suggested next steps to extend this project

- Add a PDF/Excel export of the full BRSR-formatted disclosure (there's a `pdf`/`xlsx` skill available if you want this built next).
- Add year-over-year comparison once you have >1 year of data.
- Add uncertainty ranges / data quality tagging (measured vs. estimated vs. spend-based) per GHG Protocol guidance.
- Deploy publicly via Streamlit Community Cloud and link it directly from your resume.
