"""
sample_data_generator.py
-------------------------
Creates 12 months of illustrative activity data for a fictitious Indian
manufacturing company ("GreenTech Manufacturing Ltd.") so the dashboard has
something to show out of the box. Replace these CSVs with a real company's
data (from annual reports / internal MIS) for actual use.
"""
import pandas as pd
import numpy as np

MONTHS = pd.date_range("2024-04-01", periods=12, freq="MS").strftime("%b-%Y").tolist()

def generate_fuel_data(seed=1):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "Month": MONTHS,
        "Diesel (litres)": rng.integers(2200, 3200, 12),
        "Petrol (litres)": rng.integers(300, 600, 12),
        "LPG (kg)": rng.integers(800, 1300, 12),
        "Piped Natural Gas (kg)": rng.integers(400, 900, 12),
        "Furnace Oil (litres)": rng.integers(0, 500, 12),
        "Coal (kg)": rng.integers(0, 800, 12),
    })

def generate_electricity_data(seed=2):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "Month": MONTHS,
        "Grid Electricity (kWh)": rng.integers(85000, 120000, 12),
        "Renewable/Purchased Green Power (kWh)": rng.integers(5000, 20000, 12),
    })

def generate_travel_data(seed=3):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "Month": MONTHS,
        "Domestic Flight (km)": rng.integers(4000, 12000, 12),
        "International Flight (km)": rng.integers(0, 8000, 12),
        "Road - Own/Rented Vehicle (km)": rng.integers(2000, 6000, 12),
        "Rail (km)": rng.integers(500, 2500, 12),
    })

def generate_logistics_data(seed=4):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "Month": MONTHS,
        "Tonne-km Shipped": rng.integers(15000, 40000, 12),
    })

def generate_commuting_data(seed=5):
    rng = np.random.default_rng(seed)
    employees = 420
    return pd.DataFrame({
        "Month": MONTHS,
        "Employees Commuting": [employees] * 12,
        "Avg Round-Trip Commute (km)": rng.integers(18, 32, 12),
        "Working Days": [22] * 12,
    })

def generate_spend_data(seed=6):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "Month": MONTHS,
        "Raw Materials - Metals (INR '000)": rng.integers(9000, 15000, 12),
        "Raw Materials - Plastics/Polymers (INR '000)": rng.integers(4000, 8000, 12),
        "Packaging (INR '000)": rng.integers(1500, 3500, 12),
        "IT & Electronics (INR '000)": rng.integers(500, 1800, 12),
        "Professional Services (INR '000)": rng.integers(800, 2200, 12),
    })

def generate_revenue_data(seed=7):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "Month": MONTHS,
        "Revenue (INR Lakh)": rng.integers(4200, 6800, 12),
    })

if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(__file__), "sample_data")
    os.makedirs(out, exist_ok=True)
    generate_fuel_data().to_csv(f"{out}/fuel_consumption.csv", index=False)
    generate_electricity_data().to_csv(f"{out}/electricity_consumption.csv", index=False)
    generate_travel_data().to_csv(f"{out}/business_travel.csv", index=False)
    generate_logistics_data().to_csv(f"{out}/logistics.csv", index=False)
    generate_commuting_data().to_csv(f"{out}/employee_commuting.csv", index=False)
    generate_spend_data().to_csv(f"{out}/purchased_goods_spend.csv", index=False)
    generate_revenue_data().to_csv(f"{out}/revenue.csv", index=False)
    print("Sample data written to", out)
