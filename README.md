# IWCS-Dataset: Simulation Dataset for Cyberattack Analysis in IIoT Wireless Sensor Networks

**IWCS-Dataset** is a simulation-based dataset for cyberattack analysis in **Industrial Internet of Things (IIoT)** Wireless Sensor Networks. The dataset was generated using **OMNeT++/INET** simulations with **IEEE 802.15.4**, **RPL**, and **UDP traffic**, considering multiple network topologies and cyberattack scenarios.

The dataset supports research on network performance analysis, anomaly detection, cyberattack classification, and reproducibility in IIoT/WSN environments.

---

## Dataset Overview

| Item            | Description                                                |
| --------------- | ---------------------------------------------------------- |
| Dataset name    | IWCS-Dataset                                               |
| Domain          | Industrial IoT / Wireless Sensor Networks                  |
| Simulation tool | OMNeT++ / INET                                             |
| Network stack   | IEEE 802.15.4, RPL, UDP                                    |
| Main file       | `dataset/dataset_omnetpp_cleaned_2.csv`                    |
| Records         | 20,331                                                     |
| Attributes      | 16                                                         |
| Topologies      | Grid_36, Grid_49, Grid_64, Grid_100                        |
| Scenarios       | Normal, Flooding, Blackhole, Wormhole, Manipulated Backoff |

---

## Main Dataset File

The curated dataset is available at:

```text
dataset/dataset_omnetpp_cleaned_2.csv
```

This file contains **20,331 records** and **16 attributes**, including the evaluated network topology, attack scenario, and performance metrics extracted from the OMNeT++ simulation outputs.

The processed dataset includes all evaluated topologies and scenarios used in the associated manuscript.

---

## Evaluated Scenarios

The dataset includes five network operation and cyberattack scenarios:

* `Normal`
* `Flooding`
* `Blackhole`
* `Wormhole`
* `Backoff_Manipulado`

The label `Backoff_Manipulado` corresponds to the **Manipulated Backoff** scenario, in which MAC-layer contention parameters were modified to represent abnormal channel access behavior.

---

## Evaluated Topologies

The simulations were conducted using grid-based WSN/IIoT topologies with different network sizes:

* `Grid_36`
* `Grid_49`
* `Grid_64`
* `Grid_100`

These topologies allow the dataset to support analysis of cyberattack behavior under different network scales.

---

## Main Metrics

The dataset includes network performance metrics commonly used to analyze the behavior of WSN/IIoT systems under normal and malicious conditions, such as:

* Packet Delivery Ratio;
* Average end-to-end delay;
* Throughput;
* Energy consumption;
* RPL control and routing-related indicators.

These attributes can be used for statistical analysis, anomaly detection, machine learning classification, and topology-aware cyberattack evaluation.

---

## Simulation Environment

The dataset was generated using the following simulation environment:

* OMNeT++ 5.7.x
* INET 4.2.x
* RPL model based on/adapted from: https://github.com/ComNetsHH/omnetpp-rpl
* IEEE 802.15.4 MAC/PHY
* UDP application traffic

The simulations follow a WSN/IIoT communication model in which sensor nodes transmit traffic toward a sink node under different network conditions and attack scenarios.

---

## Repository Structure

The repository is organized as follows:

```text
IWCS-Dataset/
│
├── dataset/
│   └── dataset_omnetpp_cleaned_2.csv
│
├── raw_samples/
│   └── representative OMNeT++ .sca, .vec, and .vci files
│
├── metadata/
│   └── raw_files_manifest.csv
│
├── scripts/
│   ├── parse_omnet.py
│   ├── clean_dataset.py
│   └── validate_dataset.py
│
├── README.md
├── CITATION.cff
└── LICENSE
```

Depending on the repository version, some scripts or auxiliary files may be updated to improve reproducibility and documentation.

---

## Representative Raw Simulation Samples

Due to the large size of the complete OMNeT++ raw simulation outputs, this repository provides **representative raw samples** instead of storing all raw output files from all simulation repetitions.

The representative raw samples include OMNeT++:

* `.sca` files;
* `.vec` files;
* `.vci` files.

Representative samples are provided for selected executions, including:

* run `0`;
* run `999`.

These samples cover the following scenarios:

* Normal;
* Flooding;
* Blackhole;
* Wormhole;
* Manipulated Backoff.

They also cover the evaluated topology sizes:

* 36 nodes;
* 49 nodes;
* 64 nodes;
* 100 nodes.

The representative raw files allow users to inspect the structure of the OMNeT++ outputs and understand how the curated CSV dataset was derived.

---

## Reproducibility Note

The complete raw simulation outputs are large because the experiments involve multiple scenarios, four network topologies, and up to 1000 repetitions per scenario/topology configuration.

For reproducibility, this repository provides:

* the final curated CSV dataset;
* representative OMNeT++ raw simulation samples;
* a raw file manifest;
* metadata describing the dataset structure;
* scripts used for extraction, cleaning, and validation, when available.

The file `raw_files_manifest.csv` documents the available raw samples and may include information such as file name, topology, scenario, run identifier, file type, size, path, and checksum.

---

## Basic Usage

The dataset can be loaded using Python and pandas:

```python
import pandas as pd

df = pd.read_csv("dataset/dataset_omnetpp_cleaned_2.csv")

print(df.shape)
print(df.head())
print(df["Attack_Type"].value_counts())
print(df["Topology"].value_counts())
```

This allows users to inspect the number of records, attributes, attack classes, and evaluated topologies.

---

## Related Repository and Dataset Record

The processed dataset and reproducibility materials are associated with the Zenodo record:

```text
https://zenodo.org/records/20602871
```

DOI:

```text
10.5281/zenodo.20602871
```

If a newer Zenodo version is released, users should cite the most recent DOI available in the Zenodo record.

---

## Citation

If you use this dataset in your research, please cite it as follows:

```bibtex
@dataset{lo_nunes_iwcs_dataset_2026,
  author    = {Lo Nunes, Osvaldo Sebastião},
  title     = {IWCS-Dataset: Simulation Dataset for Cyberattack Analysis in IIoT Wireless Sensor Networks},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20602871},
  url       = {https://zenodo.org/records/20602871}
}
```

---

## License

This dataset is distributed under the license specified in the Zenodo record and in the repository `LICENSE` file.

Please refer to the Zenodo record for the official license information.

---

## Acknowledgment

This dataset was developed as part of the master's research of **Osvaldo Lo Nunes Sebastião** at the **Escola Politécnica da Universidade de São Paulo**.

The dataset was created to support reproducible research on cyberattack analysis, performance evaluation, and intelligent detection methods in IIoT Wireless Sensor Networks.

---

## Contact

For questions, suggestions, or collaboration related to this dataset, please use the GitHub repository issue tracker or contact the dataset author through the information provided in the Zenodo record.
