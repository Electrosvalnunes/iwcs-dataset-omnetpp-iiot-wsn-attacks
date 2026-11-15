import pandas as pd
import numpy as np

ONEHOT_COLS = ["Normal", "Flooding", "Blackhole", "Wormhole", "Backoff_Manipulado"]
NUMERIC_INT_COLS = ["DIO_Count_Window", "DIS_Count_Window", "Rank_Changes_Window"]
NUMERIC_FLOAT_COLS = [
    "Avg_RSSI_dBm", "PDR_percent", "Avg_Delay_ms",
    "Throughput_kbps", "Energy_Consumed_J",
]
TOPOLOGIAS_VALIDAS = {"Grid_36", "Grid_49", "Grid_64", "Grid_100"}


def _to_numeric_seguro(serie):
    """Converte para número mesmo com vírgula decimal, string, ou espaço."""
    if serie.dtype == object or pd.api.types.is_string_dtype(serie):
        serie = serie.astype(str).str.strip().str.replace(",", ".", regex=False)
    return pd.to_numeric(serie, errors="coerce")


def clean(input_csv="dataset_omnetpp_P.csv",
          output_csv="dataset_omnetpp_cleaned_2.csv",
          limitar_run_id_max=None):
    df = pd.read_csv(input_csv)

    rename_map = {
        "Janela_DIO_Count": "DIO_Count_Window",
        "Janela_DIS_Count": "DIS_Count_Window",
        "Janela_Rank_Changes": "Rank_Changes_Window",
        "Topologia": "Topology",
        "Ataque": "Attack_Type",
        "Tipo_Ataque": "Attack_Type",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
    df = df.dropna(how="all")

    for col in NUMERIC_FLOAT_COLS + NUMERIC_INT_COLS:
        if col in df.columns:
            df[col] = _to_numeric_seguro(df[col])
    if "RUN_ID" in df.columns:
        df["RUN_ID"] = _to_numeric_seguro(df["RUN_ID"])

    df["Topology"] = df["Topology"].astype(str).str.strip()
    df["Topology"] = df["Topology"].str.replace(r"[\s\-]+", "_", regex=True)
    df["Topology"] = df["Topology"].str.replace(
        r"(?i)^grid_?(\d+)$", lambda m: f"Grid_{m.group(1)}", regex=True
    )

    df["Attack_Type"] = df["Attack_Type"].astype(str).str.strip()
    canonical = {c.lower(): c for c in ONEHOT_COLS}
    df["Attack_Type"] = df["Attack_Type"].str.lower().map(canonical).fillna(df["Attack_Type"])
    typo_map = {"Floding": "Flooding", "Flooding ": "Flooding"}
    df["Attack_Type"] = df["Attack_Type"].replace(typo_map)

    antes = len(df)
    df = df.drop_duplicates()
    print(f"Duplicatas exatas removidas: {antes - len(df)}")

    if "RUN_ID" in df.columns:
        antes = len(df)
        df = df.dropna(subset=["RUN_ID"])
        df = df.drop_duplicates(subset="RUN_ID", keep="first")
        print(f"RUN_ID duplicado/invalido removido: {antes - len(df)}")

    antes = len(df)
    df = df.dropna()
    print(f"Linhas com valor nulo removidas: {antes - len(df)}")

    antes = len(df)
    df = df[df["Topology"].isin(TOPOLOGIAS_VALIDAS) & df["Attack_Type"].isin(ONEHOT_COLS)]
    print(f"Categorias invalidas removidas: {antes - len(df)}")

    antes = len(df)
    df = df[df["PDR_percent"].between(0, 100)]
    df = df[df["Avg_RSSI_dBm"].between(-120, 0)]
    df = df[(df["Avg_Delay_ms"] >= 0) & (df["Throughput_kbps"] >= 0) & (df["Energy_Consumed_J"] >= 0)]
    df = df[(df["DIO_Count_Window"] >= 0) & (df["DIS_Count_Window"] >= 0) & (df["Rank_Changes_Window"] >= 0)]
    print(f"Valores fora de faixa removidos: {antes - len(df)}")

    antes = len(df)
    soma_onehot = df[ONEHOT_COLS].sum(axis=1)
    df = df[soma_onehot == 1]
    print(f"One-hot inconsistente removido: {antes - len(df)}")
    for col in ONEHOT_COLS:
        df[col] = (df["Attack_Type"] == col).astype(int)

    for col in NUMERIC_INT_COLS:
        df[col] = df[col].round().astype(int)
    for col in NUMERIC_FLOAT_COLS:
        df[col] = df[col].astype(float)
    df["RUN_ID"] = df["RUN_ID"].astype(int)

    if limitar_run_id_max is not None:
        antes = len(df)
        df = df[df["RUN_ID"] <= limitar_run_id_max]
        print(f"Corte por RUN_ID <= {limitar_run_id_max}: {antes - len(df)} removidas")

    df = df.sort_values("RUN_ID").reset_index(drop=True)
    df.to_csv(output_csv, index=False)
    print(f"\nCleaned dataset saved to {output_csv}: {len(df)} records")
    return df


if __name__ == "__main__":
    clean()
