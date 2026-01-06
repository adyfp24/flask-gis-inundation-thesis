import pandas as pd

df = pd.read_csv("data/sea_level_rise_yearly_2025_2050.csv")

def get_slr_by_year(year: int) -> float:
    row = df[df["year"] == year]
    if row.empty:
        raise ValueError("Year not available")
    return float(row["sla_mean_m"].values[0])


def get_slr_timeseries():
    df_sorted = df.sort_values("year").copy()

    # Convert m → mm
    df_sorted["sla_mm"] = df_sorted["sla_mean_m"] * 1000

    # Δ tahunan
    df_sorted["kenaikan_tahunan_mm"] = df_sorted["sla_mm"].diff()
    df_sorted.loc[df_sorted.index[0], "kenaikan_tahunan_mm"] = 0

    # kumulatif
    df_sorted["kenaikan_kumulatif_mm"] = (
        df_sorted["sla_mm"] - df_sorted["sla_mm"].iloc[0]
    )

    return df_sorted[[
        "year",
        "kenaikan_tahunan_mm",
        "kenaikan_kumulatif_mm"
    ]].to_dict(orient="records")
