import pandas as pd

df = pd.read_csv("data/sea_level_rise_yearly_2025_2050.csv")

def get_slr_by_year(year: int) -> float:
    row = df[df["year"] == year]
    if row.empty:
        raise ValueError("Year not available")
    return float(row["sla_mean_m"].values[0])
