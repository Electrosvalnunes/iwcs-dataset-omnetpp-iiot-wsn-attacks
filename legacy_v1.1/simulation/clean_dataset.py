import pandas as pd

def clean(input_csv="dataset_omnetpp_extracted.csv", output_csv="dataset_omnetpp_cleaned_2.csv"):
    df = pd.read_csv(input_csv)
    rename_map = {
        "Janela_DIO_Count": "DIO_Count_Window",
        "Janela_DIS_Count": "DIS_Count_Window",
        "Janela_Rank_Changes": "Rank_Changes_Window",
    }
    df = df.rename(columns=rename_map)
    if "Topologia" in df.columns:
        df = df.rename(columns={"Topologia": "Topology"})
    df["Topology"] = df["Topology"].astype(str).str.strip().str.upper().str.replace("GRID_", "Grid_", regex=False)
    df = df.drop_duplicates()
    df = df.dropna()
    df = df[(df["PDR_percent"].between(0, 100))]
    df = df[(df["Avg_RSSI_dBm"].between(-120, 0))]
    df = df[(df["Avg_Delay_ms"] >= 0) & (df["Throughput_kbps"] >= 0) & (df["Energy_Consumed_J"] >= 0)]
    df = df[(df["DIO_Count_Window"] >= 0) & (df["DIS_Count_Window"] >= 0) & (df["Rank_Changes_Window"] >= 0)]
    df.to_csv(output_csv, index=False)
    print(f"Cleaned dataset saved to {output_csv}: {len(df)} records")

if __name__ == "__main__":
    clean()
