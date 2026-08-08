# IWCS-Dataset

The **IWCS-Dataset** is a simulation-based dataset for cyberattack analysis in Industrial Internet of Things (IIoT) wireless sensor networks. The released V1 contains **20,331 curated records and 16 attributes** derived from an OMNeT++/INET campaign with IEEE 802.15.4, IPv6/RPL, UDP traffic, four grid topology labels, and five controlled operating conditions.

> **Scope note.** The audited recovered configurations use RPL/IPv6 over IEEE 802.15.4. An explicit 6LoWPAN adaptation layer was **not** present in the recovered stack, so the revised documentation does not claim that such a layer was modeled in the audited configuration package.

## Main dataset

`dataset/dataset_omnetpp_cleaned_2.csv`

- Records: **20,331**
- Attributes: **16**
- Topology labels: `Grid_36`, `Grid_49`, `Grid_64`, `Grid_100`
- Conditions: `Normal`, `Flooding`, `Blackhole`, `Wormhole`, `Backoff_Manipulado`
- Zenodo DOI: **10.5281/zenodo.20602871**
- Dataset license: **CC BY 4.0**

## Provenance and reproducibility

The revision distinguishes two evidence levels:

1. **Exact final-curation reproducibility.** The recovered pre-curation table contains **22,180 rows**. Re-executing the recovered final-curation procedure removes **1,849 source rows** and reproduces the released **20,331-row** table exactly at the parsed value level.
2. **Representative raw-file traceability.** The complete historical OMNeT++ raw corpus was not retained. The revision package provides representative raw evidence covering all **20 topology-scenario combinations** rather than claiming row-by-row regeneration of every released record from historical `.sca/.vec/.vci` files.

The audited raw package contains one representative `.sca` execution (`run 0`) for every topology-scenario combination. Selected `.vec` and `.vci` examples may also be retained where storage size is practical.

## Repository layout after revision update

```text
IWCS-Dataset/
├── dataset/
│   └── dataset_omnetpp_cleaned_2.csv
├── provenance/
│   ├── dataset_omnetpp_P.csv
│   ├── reproduction_check.json
│   ├── cleaning_stage_summary.csv
│   ├── excluded_source_rows_ledger.csv
│   ├── missing_run_ids_ledger.csv
│   └── PROVENANCE_RECONSTRUCTION_REPORT.md
├── metadata/
│   ├── data_dictionary_IWCS_Dataset.csv
│   ├── RELATORIO_AUDITORIA_INTEGRAL_V1.md
│   ├── descriptive_statistics.csv
│   ├── topology_attack_distribution.csv
│   └── raw_files_manifest_audited_run0.csv
├── raw-samples/
│   └── audited-run0/
├── scripts/
│   ├── parse_omnet_legacy.py
│   ├── clean_dataset_final.py
│   ├── validate_dataset_integral.py
│   ├── verify_v1_reproduction.py
│   └── benchmark_baselines.py
├── simulation/
│   └── audited/
├── CITATION.cff
├── LICENSE
└── README.md
```

## Labeling

IWCS does **not** use human annotation. `Attack_Type` is a deterministic label derived from the controlled simulation condition. The revision audit checks consistency between `Attack_Type` and the five one-hot class columns.

## Important V1 limitations

The revision explicitly documents the following historical limitations:

- filename-based scenario classification in the legacy parser;
- a historical defensive PDR cap at 100%;
- two numerical-precision regimes already present in the pre-curation table;
- deterministic patterns in some historical delay/energy features;
- run-level aggregation that discards much of the temporal richness of vector outputs;
- fixed/calibrated attacker placement and topology-specific configuration choices;
- bounded attack coverage and no complete physical industrial-testbed validation.

For machine-learning reuse, avoid using the one-hot class columns as predictors and prefer topology-aware validation when evaluating generalization.

## Citation

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

See also `CITATION.cff`.

## License

The released dataset is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. Source-code files derived from or adapted from third-party software retain the license obligations applicable to those source files; the dataset license does not override software licenses.

## Contact

For questions or reproducibility issues, use the GitHub issue tracker or the contact information in the Zenodo record.
