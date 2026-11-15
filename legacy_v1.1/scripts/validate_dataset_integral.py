#!/usr/bin/env python3
"""Enhanced record-level validator for IWCS-Dataset V1.

Uses only Python standard library. It validates all rows and writes a JSON report.
It does not claim row-by-row regeneration from OMNeT++ raw files.
"""
from __future__ import annotations
import csv, hashlib, json, sys
from collections import Counter
from pathlib import Path

EXPECTED_COLUMNS = [
    "RUN_ID", "Topology", "Attack_Type", "Avg_RSSI_dBm",
    "DIO_Count_Window", "DIS_Count_Window", "Rank_Changes_Window",
    "PDR_percent", "Avg_Delay_ms", "Throughput_kbps",
    "Energy_Consumed_J", "Normal", "Flooding", "Blackhole",
    "Wormhole", "Backoff_Manipulado",
]
TOPOLOGIES = {"Grid_36", "Grid_49", "Grid_64", "Grid_100"}
CLASSES = {"Normal", "Flooding", "Blackhole", "Wormhole", "Backoff_Manipulado"}
ONE_HOT = ["Normal", "Flooding", "Blackhole", "Wormhole", "Backoff_Manipulado"]

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def decimal_places(text: str) -> int:
    text = text.strip().lower()
    if "e" in text:
        from decimal import Decimal
        return max(0, -Decimal(text).as_tuple().exponent)
    return len(text.split(".", 1)[1]) if "." in text else 0

def validate(csv_path: Path) -> dict:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        columns = reader.fieldnames or []

    errors, warnings = [], []
    if columns != EXPECTED_COLUMNS:
        errors.append("Unexpected column names/order.")

    missing = sum(
        1 for row in rows for column in columns
        if row[column] is None or row[column].strip() == ""
    )
    if missing:
        errors.append(f"Missing values: {missing}")

    full_rows = [tuple(row[column] for column in columns) for row in rows]
    duplicate_rows = len(full_rows) - len(set(full_rows))
    if duplicate_rows:
        errors.append(f"Duplicate rows: {duplicate_rows}")

    ids = [int(row["RUN_ID"]) for row in rows]
    duplicate_ids = len(ids) - len(set(ids))
    if duplicate_ids:
        errors.append(f"Duplicate RUN_ID: {duplicate_ids}")

    one_hot_errors = 0
    invalid_ranges = Counter()
    for row in rows:
        if row["Topology"] not in TOPOLOGIES:
            invalid_ranges["invalid_topology"] += 1
        if row["Attack_Type"] not in CLASSES:
            invalid_ranges["invalid_attack"] += 1

        encoded = {column: int(float(row[column])) for column in ONE_HOT}
        if sum(encoded.values()) != 1 or encoded.get(row["Attack_Type"]) != 1:
            one_hot_errors += 1

        pdr = float(row["PDR_percent"])
        rssi = float(row["Avg_RSSI_dBm"])
        if not 0 <= pdr <= 100:
            invalid_ranges["PDR"] += 1
        if not -120 <= rssi <= 0:
            invalid_ranges["RSSI"] += 1
        for column in [
            "Avg_Delay_ms", "Throughput_kbps", "Energy_Consumed_J",
            "DIO_Count_Window", "DIS_Count_Window", "Rank_Changes_Window",
        ]:
            if float(row[column]) < 0:
                invalid_ranges[column] += 1

    if one_hot_errors:
        errors.append(f"One-hot inconsistencies: {one_hot_errors}")
    if invalid_ranges:
        errors.append(f"Invalid values: {dict(invalid_ranges)}")

    id_gaps = len(set(range(min(ids), max(ids) + 1)) - set(ids))
    if id_gaps:
        warnings.append(f"RUN_ID gaps: {id_gaps}")

    precise_block = sum(
        1 for row in rows
        if int(row["RUN_ID"]) > 20000
        and all(decimal_places(row[c]) > 3 for c in [
            "Avg_RSSI_dBm", "PDR_percent", "Avg_Delay_ms",
            "Throughput_kbps", "Energy_Consumed_J",
        ])
    )
    if precise_block:
        warnings.append(
            f"High-precision block after RUN_ID 20000: {precise_block} rows"
        )

    report = {
        "file": csv_path.name,
        "sha256": sha256(csv_path),
        "records": len(rows),
        "attributes": len(columns),
        "status": "PASS_WITH_WARNINGS" if not errors and warnings else ("PASS" if not errors else "FAIL"),
        "errors": errors,
        "warnings": warnings,
        "class_counts": dict(Counter(row["Attack_Type"] for row in rows)),
        "topology_counts": dict(Counter(row["Topology"] for row in rows)),
    }
    return report

if __name__ == "__main__":
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "dataset_omnetpp_cleaned_2.csv")
    report = validate(target)
    output = target.with_name("quality_report_integral.json")
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["status"].startswith("PASS") else 1)
