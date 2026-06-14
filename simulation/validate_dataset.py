import pandas as pd
from pathlib import Path

EXPECTED_COLUMNS = [
    "RUN_ID", "Topology", "Attack_Type", "Avg_RSSI_dBm", "DIO_Count_Window",
    "DIS_Count_Window", "Rank_Changes_Window", "PDR_percent", "Avg_Delay_ms",
    "Throughput_kbps", "Energy_Consumed_J", "Normal", "Flooding", "Blackhole",
    "Wormhole", "Backoff_Manipulado"
]
VALID_TOPOLOGIES = {"Grid_36", "Grid_49", "Grid_64", "Grid_100"}
VALID_CLASSES = {"Normal", "Flooding", "Blackhole", "Wormhole", "Backoff_Manipulado"}
ONE_HOT = ["Normal", "Flooding", "Blackhole", "Wormhole", "Backoff_Manipulado"]

def validate(path="../dataset/dataset_omnetpp_cleaned_2.csv"):
    df = pd.read_csv(path)
    errors = []
    if list(df.columns) != EXPECTED_COLUMNS:
        errors.append("Unexpected column order or names.")
    if df.isna().sum().sum() != 0:
        errors.append("Missing values detected.")
    if df.duplicated().sum() != 0:
        errors.append("Duplicate rows detected.")
    if df["RUN_ID"].duplicated().sum() != 0:
        errors.append("Repeated RUN_ID detected.")
    if not set(df["Topology"]).issubset(VALID_TOPOLOGIES):
        errors.append("Invalid topology detected.")
    if not set(df["Attack_Type"]).issubset(VALID_CLASSES):
        errors.append("Invalid Attack_Type detected.")
    if ((df["PDR_percent"] < 0) | (df["PDR_percent"] > 100)).any():
        errors.append("Invalid PDR values detected.")
    for col in ["Avg_Delay_ms", "Throughput_kbps", "Energy_Consumed_J", "DIO_Count_Window", "DIS_Count_Window", "Rank_Changes_Window"]:
        if (df[col] < 0).any():
            errors.append(f"Negative values detected in {col}.")
    one_hot_sum = df[ONE_HOT].sum(axis=1)
    if not (one_hot_sum == 1).all():
        errors.append("One-hot class inconsistency detected.")
    for cls in ONE_HOT:
        bad = df[df["Attack_Type"] == cls][cls].ne(1).sum()
        if bad:
            errors.append(f"Attack_Type/one-hot mismatch for {cls}.")
    if errors:
        print("VALIDATION FAILED")
        for e in errors: print("-", e)
        return False
    print("VALIDATION PASSED")
    print(f"Records: {len(df)} | Attributes: {len(df.columns)}")
    print(df["Attack_Type"].value_counts())
    print(df["Topology"].value_counts())
    return True

if __name__ == "__main__":
    validate()
