#!/usr/bin/env python3
"""Generate the compact exploratory figure used in the IWCS descriptor revision.

The script reads the released CSV and creates a 2x2 figure with class-wise
mean ± standard deviation for PDR, delay, throughput, and consumed energy.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV = Path("dataset/dataset_omnetpp_cleaned_2.csv")
OUT = Path("figures/iwcs_eda_2x2.png")
ORDER = ["Normal", "Flooding", "Blackhole", "Wormhole", "Backoff_Manipulado"]
METRICS = [
    ("PDR_percent", "PDR (%)"),
    ("Avg_Delay_ms", "Average delay (ms)"),
    ("Throughput_kbps", "Throughput (kbps)"),
    ("Energy_Consumed_J", "Consumed energy (J)"),
]

def main():
    df = pd.read_csv(CSV)
    stats = df.groupby("Attack_Type")[[m for m, _ in METRICS]].agg(["mean", "std"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
    for ax, (metric, ylabel) in zip(axes.flat, METRICS):
        means = [stats.loc[c, (metric, "mean")] for c in ORDER]
        stds = [stats.loc[c, (metric, "std")] for c in ORDER]
        ax.bar(range(len(ORDER)), means, yerr=stds, capsize=3)
        ax.set_xticks(range(len(ORDER)))
        ax.set_xticklabels(["Normal", "Flooding", "Blackhole", "Wormhole", "Backoff"], rotation=25, ha="right")
        ax.set_ylabel(ylabel)
        ax.set_xlabel("Scenario")
    fig.savefig(OUT, dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT}")

if __name__ == "__main__":
    main()
