#!/usr/bin/env python3
"""Reproduce the diagnostic benchmark and RSSI leakage checks reported in the IWCS R2 revision.

Outputs:
  - metadata/benchmark_results.csv
  - metadata/rssi_topology_diagnostic.csv

The script deliberately excludes Attack_Type, one-hot class columns, and Topology from
attack-class predictors. Topology is used only to define Leave-One-Topology-Out folds.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, f1_score

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "dataset" / "dataset_omnetpp_cleaned_2.csv"
OUT_BENCH = ROOT / "metadata" / "benchmark_results.csv"
OUT_RSSI = ROOT / "metadata" / "rssi_topology_diagnostic.csv"

df = pd.read_csv(CSV)
y = df["Attack_Type"]

F8 = [
    "Avg_RSSI_dBm", "DIO_Count_Window", "DIS_Count_Window",
    "Rank_Changes_Window", "PDR_percent", "Avg_Delay_ms",
    "Throughput_kbps", "Energy_Consumed_J",
]
F6 = [
    "Avg_RSSI_dBm", "DIO_Count_Window", "DIS_Count_Window",
    "Rank_Changes_Window", "PDR_percent", "Throughput_kbps",
]
F5 = [
    "DIO_Count_Window", "DIS_Count_Window", "Rank_Changes_Window",
    "PDR_percent", "Throughput_kbps",
]

def models():
    return {
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, random_state=42, n_jobs=-1
        ),
        "Logistic Regression": make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=5000, random_state=42),
        ),
    }

rows = []
for label, features in [
    ("8 features", F8),
    ("6-feature ablation", F6),
    ("5-feature no Delay/Energy/RSSI", F5),
]:
    Xtr, Xte, ytr, yte = train_test_split(
        df[features], y, test_size=0.2, random_state=42, stratify=y
    )
    for name, model in models().items():
        model.fit(Xtr, ytr)
        pred = model.predict(Xte)
        rows.append([
            "Random stratified 80/20", label, name, "-",
            accuracy_score(yte, pred), f1_score(yte, pred, average="macro"),
        ])

    for name in ["Random Forest", "Logistic Regression"]:
        fold_rows = []
        for topo in sorted(df["Topology"].unique()):
            tr = df["Topology"] != topo
            te = ~tr
            model = models()[name]
            model.fit(df.loc[tr, features], y.loc[tr])
            pred = model.predict(df.loc[te, features])
            acc = accuracy_score(y.loc[te], pred)
            f1 = f1_score(y.loc[te], pred, average="macro")
            fold_rows.append((topo, acc, f1))
            rows.append([
                "Leave-One-Topology-Out", label, name, topo, acc, f1
            ])
        rows.append([
            "LOTO mean", label, name, "4 topologies",
            float(np.mean([r[1] for r in fold_rows])),
            float(np.mean([r[2] for r in fold_rows])),
        ])

bench = pd.DataFrame(
    rows, columns=["Protocol", "Feature_Set", "Model", "Held_Out", "Accuracy", "Macro_F1"]
)
bench.to_csv(OUT_BENCH, index=False)

# RSSI-only topology diagnostic (four topology labels; chance is approximately 25%).
X = df[["Avg_RSSI_dBm"]]
yt = df["Topology"]
Xtr, Xte, ytr, yte = train_test_split(
    X, yt, test_size=0.2, random_state=42, stratify=yt
)
rssi_rows = []
for name, model in {
    "Logistic Regression": make_pipeline(
        StandardScaler(), LogisticRegression(max_iter=5000, random_state=42)
    ),
    "Random Forest depth=5": RandomForestClassifier(
        n_estimators=200, max_depth=5, random_state=42, n_jobs=-1
    ),
}.items():
    model.fit(Xtr, ytr)
    pred = model.predict(Xte)
    rssi_rows.append([
        "RSSI-only topology classification",
        name,
        accuracy_score(yte, pred),
        f1_score(yte, pred, average="macro"),
    ])

rssi = pd.DataFrame(
    rssi_rows, columns=["Protocol", "Model", "Accuracy", "Macro_F1"]
)
rssi.to_csv(OUT_RSSI, index=False)

print(bench.to_string(index=False))
print()
print(rssi.to_string(index=False))
