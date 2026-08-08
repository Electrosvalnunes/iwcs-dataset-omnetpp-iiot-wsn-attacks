# IWCS-Dataset

The **IWCS-Dataset** is a simulation-based dataset for cyberattack analysis in Industrial Internet of Things (IIoT) wireless sensor networks. The released V1 contains **20,331 curated records and 16 attributes** derived from an OMNeT++/INET campaign with IEEE 802.15.4, IPv6/RPL, UDP traffic, four grid topology labels, and five controlled operating conditions.

> **Scope note.** The recovered configurations audited during the 2026 major revision use RPL/IPv6 over IEEE 802.15.4. An explicit 6LoWPAN adaptation layer was not present in the recovered stack; therefore, this repository does not claim that 6LoWPAN was modeled in the audited configuration package.

## Main dataset

`dataset/dataset_omnetpp_cleaned_2.csv`

- Records: **20,331**
- Attributes: **16**
- Topology labels: `Grid_36`, `Grid_49`, `Grid_64`, `Grid_100`
- Conditions: `Normal`, `Flooding`, `Blackhole`, `Wormhole`, `Backoff_Manipulado`
- Zenodo DOI: **10.5281/zenodo.20602871**
- Dataset license: **CC BY 4.0**
- V1 SHA-256: `523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`

The released V1 CSV was **not modified** by the 2026 documentation, provenance, validation, and reproducibility update.

## Provenance and reproducibility

The revision distinguishes two evidence levels:

1. **Exact final-curation reconstruction.** The recovered pre-curation table contains **22,180 rows**. Re-executing the recovered final-curation procedure removes **1,849 source rows** and reproduces the released **20,331-row** table exactly at parsed value level, with **zero different cells**. GitHub provides the cleaner, validation/reproduction scripts, stage counts, integrity metadata, and reconstruction report.
2. **Representative raw-file traceability.** The complete historical OMNeT++ raw corpus was not retained. Existing historical raw samples remain preserved under `raw-samples/`. A separate audit covered one run-0 `.sca` execution for each of the **20 topology-scenario combinations**; its file-level manifest and metric comparison are published under `metadata/`. These representative files are not presented as row-by-row regeneration of V1.

Three complete audit archives were prepared and assigned SHA-256 checksums. The connected GitHub contents interface was verified to truncate larger binary transfers, so GitHub publishes their manifests, hashes, scripts, audit notes, and smaller source components; the intact archives are reserved for the archival dataset deposit. This avoids publishing corrupted or incomplete files. See `REPRODUCIBILITY.md` and `metadata/reproducibility_archives_manifest.csv`.

## Repository structure

```text
IWCS-Dataset/
├── dataset/
│   └── dataset_omnetpp_cleaned_2.csv
├── provenance/
│   ├── PROVENANCE_RECONSTRUCTION_REPORT.md
│   ├── reproduction_check.json
│   └── cleaning_stage_summary.csv
├── metadata/
│   ├── data_dictionary_IWCS_Dataset.csv
│   ├── V1_FULL_STRUCTURAL_AUDIT.md
│   ├── descriptive_statistics.csv
│   ├── topology_attack_distribution.csv
│   ├── scenario_comparison_run0_all_topologies.csv
│   ├── raw_files_manifest_audited_run0.csv
│   ├── benchmark_results.csv
│   ├── precision_regime_crosscheck.csv
│   ├── single_feature_diagnostic.csv
│   └── reproducibility_archives_manifest.csv
├── raw-samples/
│   └── historical representative OMNeT++ `.sca`, `.vec`, and `.vci` samples
├── scripts/
│   ├── clean_dataset_final.py
│   ├── validate_dataset_integral.py
│   ├── verify_v1_reproduction.py
│   ├── benchmark_baselines.py
│   └── generate_figures.py
├── simulation/
│   ├── historical simulation/configuration materials
│   └── audited/
│       ├── README.md
│       ├── ObjectiveFunction.cc
│       └── ObjectiveFunction.h
├── REPRODUCIBILITY.md
├── SHA256SUMS.txt
├── CITATION.cff
├── LICENSE
└── README.md
```

## Labeling

IWCS does **not** use human annotation. `Attack_Type` is a deterministic label derived from the controlled simulation condition. The revision audit checks consistency between `Attack_Type` and the five one-hot class columns. Inter-annotator agreement is therefore not applicable.

## Quality-control reconstruction

The exact final-curation sequence reconstructed during the major revision is documented in `provenance/cleaning_stage_summary.csv`. Starting from 22,180 source rows, the quality-control stages remove 1,849 rows and produce the released 20,331-record table. The value-level reproduction check is stored in `provenance/reproduction_check.json`.

The complete prepared curation archive is `IWCS_V1_CURATION_REPRODUCTION_BUNDLE.zip` (SHA-256 `b10ea5824727e732f76a316741c423b7561963fb047931a52bade3ec4fb7c951`). It includes the recovered pre-curation table, full exclusion ledger, missing-RUN_ID ledger, cleaner, stage counts, report, and verification script.

## Representative raw audit

The original raw samples already in GitHub are **preserved rather than replaced**. The revision-stage audit is separately documented in `metadata/raw_files_manifest_audited_run0.csv` and `metadata/scenario_comparison_run0_all_topologies.csv`.

The prepared 20-file archive is `audited-run0-sca.zip` (SHA-256 `8d7095a4d1158ebabb244af4a7317eab83395205212d2ca5f51aa394be337506`). It contains one audited run-0 `.sca` execution for every topology × scenario combination.

## Audited attack-source snapshot

The recovered source audit covers `Rpl.cc`, `Rpl.h`, `ObjectiveFunction.cc`, and `ObjectiveFunction.h`. GitHub publishes the two smaller ObjectiveFunction files and `simulation/audited/README.md`, which records the SHA-256 hashes and source-level findings. The complete prepared archive is `rpl_attack_source_audited.zip` (SHA-256 `d0cf96b11b3e913e5bc4ac640b13cb61ee998f609c2091dd5563694026e1395e`) and is reserved for the archival deposit because a direct binary upload through the connected interface was verified to truncate it.

This recovered source snapshot supports code-level inspection but is **not** presented as proof that every V1 record can be regenerated from the incomplete historical raw corpus.

## Diagnostic evaluation

The repository includes diagnostic benchmark results in `metadata/benchmark_results.csv`, including Decision Tree, Random Forest, and Logistic Regression baselines; random stratified evaluation; Leave-One-Topology-Out (LOTO) evaluation; and a six-feature ablation excluding `Avg_Delay_ms` and `Energy_Consumed_J`.

The high within-dataset scores must **not** be interpreted as evidence of universal deployment performance. They indicate strong separability within this simulation design and motivate topology-aware validation, ablation, and checks for simulation-specific shortcuts.

Additional checks are published in:

- `metadata/precision_regime_crosscheck.csv` — cross-evaluation between the two historical numerical-precision regimes;
- `metadata/single_feature_diagnostic.csv` — shallow single-feature diagnostic results;
- `metadata/scenario_comparison_run0_all_topologies.csv` — representative raw-level metric audit across all 20 topology-scenario combinations.

## Important V1 limitations

The revision explicitly documents the following historical limitations:

- filename-based scenario classification in the legacy parser;
- a historical defensive PDR cap at 100%;
- two numerical-precision regimes already present in the pre-curation table;
- deterministic patterns in some historical delay/energy features;
- run-level aggregation that discards much of the temporal richness of vector outputs;
- fixed/calibrated attacker placement and topology-specific configuration choices;
- bounded attack coverage and no complete physical industrial-testbed validation;
- incomplete retention of the full historical raw corpus.

For machine-learning reuse, do not use `Attack_Type` or the one-hot class columns as predictors. For topology-generalization studies, exclude `Topology` from predictors and prefer topology-aware validation such as LOTO.

## Historical parser note

The original parser remains under `simulation/parse_omnet.py` for provenance. It is a **legacy artifact** and contains behaviors documented in the revision audit, including filename-based class assignment and the historical PDR cap. The newer scripts under `scripts/` are audit/reproducibility utilities and should not be interpreted as evidence that every V1 row can be regenerated from the incomplete retained historical raw corpus.

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

For questions, reproducibility reports, or corrections, use the GitHub issue tracker or the contact information associated with the Zenodo record.
