"""
OMNeT++ Simulation Data Extractor for WSN/RPL Security Analysis

Author:
    Osvaldo Ló Nunes Sebastião

Description:
    Automated pipeline for extracting and structuring OMNeT++/INET simulation
    results. The script parses .sca files, associates .vec files when available,
    registers .vci files in a raw-file manifest, computes SHA-256 checksums, and
    exports a consolidated CSV dataset for WSN/RPL attack analysis.

Outputs:
    - dataset_omnetpp_extracted.csv
    - metadata/raw_files_manifest.csv
    - figures/figure_2_class_distribution.png
    - figures/figure_3_topology_distribution.png
"""



import os
import re
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


SCENARIOS = [
    "Normal",
    "Flooding",
    "Blackhole",
    "Wormhole",
    "Backoff_Manipulado",
]


def calculate_sha256(file_path):
    """
    Calculate the SHA-256 checksum of a file.
    """
    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            for block in iter(lambda: file.read(4096), b""):
                sha256_hash.update(block)

        return sha256_hash.hexdigest()

    except OSError:
        return "HASH_ERROR"


def classify_scenario(file_name):
    """
    Classify the simulation scenario from the file name.
    """
    name = file_name.upper()

    if "FLOODING" in name:
        return "Flooding"

    if "BLACKHOLE" in name:
        return "Blackhole"

    if "WORMHOLE" in name:
        return "Wormhole"

    if "BACKOFF" in name or "MANIPULADO" in name:
        return "Backoff_Manipulado"

    return "Normal"


def extract_topology_from_network_name(network_name):
    """
    Extract the topology size from the OMNeT++ network name.
    """
    match = re.search(r"\d+", network_name)

    if match:
        return f"Grid_{match.group()}"

    return "Grid_36"


def extract_run_number(file_name):
    """
    Extract the run number from the file name when available.
    """
    match = re.search(r"-(\d+)\.", file_name)

    if match:
        return int(match.group(1))

    return 1


def add_file_to_manifest(
    manifest_records,
    file_path,
    scenario,
    topology,
    run_number,
    file_type,
):
    """
    Add one raw file entry to the manifest.
    """
    if not file_path.exists():
        return

    manifest_records.append(
        {
            "file_name": file_path.name,
            "scenario": scenario,
            "topology": topology,
            "run_number": run_number,
            "seedset": run_number,
            "file_type": file_type,
            "original_path": str(file_path.resolve()),
            "file_size": file_path.stat().st_size,
            "checksum": calculate_sha256(file_path),
            "included_in_repository": "yes",
        }
    )


def parse_scalar_file(sca_path):
    """
    Read scalar metrics from a .sca file.
    """
    topology = "Grid_36"

    packets_sent = 0
    packets_received = 0
    dio_count = 0
    dis_count = 0
    rank_changes = 0

    energy_values = []

    with open(sca_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            line_lower = line.lower()
            parts = line.split()

            if line.startswith("attr network"):
                network_name = parts[-1]
                topology = extract_topology_from_network_name(network_name)

            elif "packetidx" in line_lower or "packetsent:count" in line_lower:
                try:
                    packets_sent += int(float(parts[-1]))
                except (ValueError, IndexError):
                    pass

            elif "packetreceived:count" in line_lower:
                try:
                    packets_received += int(float(parts[-1]))
                except (ValueError, IndexError):
                    pass

            elif "dio" in line_lower or "diocount" in line_lower:
                try:
                    dio_count += int(float(parts[-1]))
                except (ValueError, IndexError):
                    pass

            elif "dis" in line_lower or "discount" in line_lower:
                try:
                    dis_count += int(float(parts[-1]))
                except (ValueError, IndexError):
                    pass

            elif "rankchanged" in line_lower or "rank:change" in line_lower:
                try:
                    rank_changes += int(float(parts[-1]))
                except (ValueError, IndexError):
                    pass

            elif "energyconsumption:sum" in line_lower:
                try:
                    energy_values.append(float(parts[-1]))
                except (ValueError, IndexError):
                    pass

            elif "residualenergycapacity" in line_lower:
                try:
                    energy_values.append(float(parts[-1]))
                except (ValueError, IndexError):
                    pass

    return {
        "topology": topology,
        "packets_sent": packets_sent,
        "packets_received": packets_received,
        "dio_count": dio_count,
        "dis_count": dis_count,
        "rank_changes": rank_changes,
        "energy_values": energy_values,
    }


def parse_vector_file(vec_path):
    """
    Read delay, throughput, and RSSI values from a .vec file.
    """
    delay_values = []
    throughput_values = []
    rssi_values = []

    if not vec_path.exists():
        return {
            "delay_values": delay_values,
            "throughput_values": throughput_values,
            "rssi_values": rssi_values,
        }

    vector_map = {}

    with open(vec_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.split()

            if line.startswith("vector") and len(parts) >= 4:
                vector_id = parts[1]
                vector_name = parts[3]

                if "endToEndDelay" in vector_name:
                    vector_map[vector_id] = "delay"
                elif "throughput" in vector_name:
                    vector_map[vector_id] = "throughput"
                elif "rssi" in vector_name or "receptionPower" in vector_name:
                    vector_map[vector_id] = "rssi"

            elif line[0].isdigit() and len(parts) >= 4:
                vector_id = parts[0]

                if vector_id not in vector_map:
                    continue

                try:
                    value = float(parts[3])
                except ValueError:
                    continue

                if vector_map[vector_id] == "delay":
                    delay_values.append(value)
                elif vector_map[vector_id] == "throughput":
                    throughput_values.append(value)
                elif vector_map[vector_id] == "rssi":
                    rssi_values.append(value)

    return {
        "delay_values": delay_values,
        "throughput_values": throughput_values,
        "rssi_values": rssi_values,
    }


def generate_pipeline_figures(df, output_dir):
    """
    Generate basic figures for checking the extracted dataset.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    if "Attack_Type" in df.columns:
        class_counts = df["Attack_Type"].value_counts().reindex(SCENARIOS).fillna(0)

        plt.figure(figsize=(7, 4))
        class_counts.plot(kind="bar")
        plt.title("Class Distribution")
        plt.xlabel("Attack Type")
        plt.ylabel("Simulation Records")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(output_dir / "figure_2_class_distribution.png", dpi=300)
        plt.close()

    if "Topology" in df.columns:
        topology_counts = df["Topology"].value_counts().sort_index()

        plt.figure(figsize=(7, 4))
        topology_counts.plot(kind="bar")
        plt.title("Topology Distribution")
        plt.xlabel("Topology")
        plt.ylabel("Simulation Records")
        plt.xticks(rotation=30, ha="right")
        plt.tight_layout()
        plt.savefig(output_dir / "figure_3_topology_distribution.png", dpi=300)
        plt.close()


def build_dataset_record(
    run_id,
    topology,
    attack_type,
    scalar_data,
    vector_data,
):
    """
    Build one dataset row from scalar and vector metrics.
    """
    packets_sent = scalar_data["packets_sent"]
    packets_received = scalar_data["packets_received"]

    if packets_sent > 0:
        pdr = min((packets_received / packets_sent) * 100.0, 100.0)
    else:
        pdr = 0.0

    delay_values = vector_data["delay_values"]
    throughput_values = vector_data["throughput_values"]
    rssi_values = vector_data["rssi_values"]
    energy_values = scalar_data["energy_values"]

    avg_delay_ms = np.mean(delay_values) * 1000.0 if delay_values else np.nan
    avg_throughput_kbps = np.mean(throughput_values) if throughput_values else np.nan
    avg_rssi_dbm = np.mean(rssi_values) if rssi_values else np.nan
    energy_consumed_j = np.mean(energy_values) if energy_values else np.nan

    one_hot = {
        scenario: 1 if attack_type == scenario else 0
        for scenario in SCENARIOS
    }

    return {
        "RUN_ID": run_id,
        "Topology": topology,
        "Attack_Type": attack_type,
        "Avg_RSSI_dBm": round(avg_rssi_dbm, 2) if not np.isnan(avg_rssi_dbm) else None,
        "DIO_Count_Window": int(scalar_data["dio_count"]),
        "DIS_Count_Window": int(scalar_data["dis_count"]),
        "Rank_Changes_Window": int(scalar_data["rank_changes"]),
        "PDR_percent": round(pdr, 2),
        "Avg_Delay_ms": round(avg_delay_ms, 2) if not np.isnan(avg_delay_ms) else None,
        "Throughput_kbps": round(avg_throughput_kbps, 2) if not np.isnan(avg_throughput_kbps) else None,
        "Energy_Consumed_J": round(energy_consumed_j, 6) if not np.isnan(energy_consumed_j) else None,
        **one_hot,
    }


def parse_omnet_simulations(root_dir=".", output_csv="dataset_omnetpp_extracted.csv"):
    """
    Parse OMNeT++ output files and export the extracted dataset.
    """
    root_dir = Path(root_dir)
    output_csv = Path(output_csv)

    print(f"Scanning target directory: {root_dir.resolve()}")

    sca_paths = []

    for root, _, files in os.walk(root_dir):
        root_path = Path(root)

        if "metadata" in root_path.parts:
            continue

        for file_name in files:
            if file_name.endswith(".sca"):
                sca_paths.append(root_path / file_name)

    if not sca_paths:
        print("[ERROR] No .sca files were found.")
        return None

    print(f"[INFO] Found {len(sca_paths)} .sca files.")

    dataset_records = []
    manifest_records = []

    for index, sca_path in enumerate(sorted(sca_paths)):
        sca_file = sca_path.name
        vec_path = sca_path.with_suffix(".vec")
        vci_path = sca_path.with_suffix(".vci")

        attack_type = classify_scenario(sca_file)
        run_number = extract_run_number(sca_file)

        scalar_data = parse_scalar_file(sca_path)
        vector_data = parse_vector_file(vec_path)

        topology = scalar_data["topology"]

        add_file_to_manifest(
            manifest_records=manifest_records,
            file_path=sca_path,
            scenario=attack_type,
            topology=topology,
            run_number=run_number,
            file_type="SCA",
        )

        add_file_to_manifest(
            manifest_records=manifest_records,
            file_path=vec_path,
            scenario=attack_type,
            topology=topology,
            run_number=run_number,
            file_type="VEC",
        )

        add_file_to_manifest(
            manifest_records=manifest_records,
            file_path=vci_path,
            scenario=attack_type,
            topology=topology,
            run_number=run_number,
            file_type="VCI",
        )

        record = build_dataset_record(
            run_id=index + 1,
            topology=topology,
            attack_type=attack_type,
            scalar_data=scalar_data,
            vector_data=vector_data,
        )

        dataset_records.append(record)

        print(f"Processed: {sca_file} -> {attack_type}")

    df_metrics = pd.DataFrame(dataset_records)
    df_metrics.to_csv(output_csv, index=False)

    print(f"[SUCCESS] Dataset saved to: {output_csv.resolve()}")

    if manifest_records:
        metadata_dir = Path("metadata")
        metadata_dir.mkdir(parents=True, exist_ok=True)

        manifest_path = metadata_dir / "raw_files_manifest.csv"
        df_manifest = pd.DataFrame(manifest_records)
        df_manifest.to_csv(manifest_path, index=False)

        print(f"[SUCCESS] Manifest saved to: {manifest_path.resolve()}")

    figures_dir = Path("figures")
    generate_pipeline_figures(df_metrics, figures_dir)

    print(f"[SUCCESS] Figures saved to: {figures_dir.resolve()}")
    print(f"[INFO] Total dataset records: {len(df_metrics)}")

    return df_metrics


if __name__ == "__main__":
    parse_omnet_simulations()
