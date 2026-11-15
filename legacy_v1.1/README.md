# IWCS-Dataset

The **IWCS-Dataset** is a simulation-based dataset for cyberattack analysis in Industrial Internet of Things (IIoT) wireless sensor networks. The current release, **v1.1.0**, documents **20,331 curated records and 16 attributes** derived from an OMNeT++/INET campaign with IEEE 802.15.4, IPv6/RPL, UDP traffic, four grid topology labels, and five controlled operating conditions.

> **Scope note.** The audited configurations use RPL/IPv6 over IEEE 802.15.4. An explicit 6LoWPAN adaptation module was not present in the audited stack; therefore, this repository does not claim that 6LoWPAN was modeled in the audited configuration package.

## Main dataset

`dataset/dataset_omnetpp_cleaned_2.csv`

- Records: **20,331**
- Attributes: **16**
- Topology labels: `Grid_36`, `Grid_49`, `Grid_64`, `Grid_100`
- Conditions: `Normal`, `Flooding`, `Blackhole`, `Wormhole`, `Backoff_Manipulado`
- Current Zenodo release: **v1.1.0**
- Version DOI: **10.5281/zenodo.21853437**
- Concept DOI: **10.5281/zenodo.20602870**
- Dataset license: **CC BY 4.0**
- Released CSV SHA-256: `523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`

The scientific CSV itself was **not modified** by the v1.1.0 provenance, validation, documentation, and reproducibility update.

## Provenance and reproducibility

The project distinguishes two evidence levels:

1. **Exact curation reconstruction.** The pre-curation table contains **22,180 rows**. Re-executing the documented dataset-curation procedure removes **1,849 source rows** and reproduces the released **20,331-row** table exactly at parsed-value level, with **zero different cells**. GitHub provides the curation script, validation/reproduction scripts, stage counts, integrity metadata, and reconstruction report.
2. **Representative raw-file traceability.** The complete historical OMNeT++ raw corpus was not retained. Existing historical raw samples remain preserved under `raw-samples/`. A separate audit covered one run-0 `.sca` execution for each of the **20 topology-condition combinations** (four topologies x five operating conditions). These representative files support methodological traceability but are not presented as row-by-row regeneration of all released records.

The complete audit bundles are published with the current Zenodo v1.1.0 release, while GitHub maintains their documentation, manifests, checksums, scripts, and source components.

## Zenodo v1.1.0 organization

The current Zenodo release (DOI **10.5281/zenodo.21853437**) contains five top-level archives:

- `IWCS_Dataset_v1.0.0.zip` - dataset archive containing the released CSV and original release materials;
- `IWCS_V1_CURATION_REPRODUCTION_BUNDLE.zip` - complete curation-reconstruction resources;
- `audited-run0-sca.zip` - 20 representative run-0 `.sca` files covering every topology-condition combination;
- `rpl_attack_source_audited.zip` - audited RPL/source-code bundle used to inspect attack semantics;
- `IWCS_2026_REVISION_METADATA.zip` - statistics, manifests, checksums, benchmark outputs, and revision metadata.

## Repository structure

```text
IWCS-Dataset/
|-- dataset/
|   `-- dataset_omnetpp_cleaned_2.csv
|-- provenance/
|   |-- PROVENANCE_RECONSTRUCTION_REPORT.md
|   |-- reproduction_check.json
|   `-- cleaning_stage_summary.csv
|-- metadata/
|   |-- data_dictionary_IWCS_Dataset.csv
|   |-- V1_FULL_STRUCTURAL_AUDIT.md
|   |-- descriptive_statistics.csv
|   |-- topology_attack_distribution.csv
|   |-- scenario_comparison_run0_all_topologies.csv
|   |-- raw_files_manifest_audited_run0.csv
|   |-- benchmark_results.csv
|   |-- precision_regime_crosscheck.csv
|   |-- single_feature_diagnostic.csv
|   `-- reproducibility_archives_manifest.csv
|-- raw-samples/
|   `-- representative OMNeT++ .sca, .vec, and .vci samples
|-- scripts/
|   |-- clean_dataset_final.py
|   |-- validate_dataset_integral.py
|   |-- verify_v1_reproduction.py
|   |-- benchmark_baselines.py
|   `-- generate_figures.py
|-- simulation/
|   |-- historical simulation/configuration materials
|   `-- audited/
|       |-- README.md
|       |-- ObjectiveFunction.cc
|       `-- ObjectiveFunction.h
|-- REPRODUCIBILITY.md
|-- CHANGELOG.md
|-- SHA256SUMS.txt
|-- CITATION.cff
|-- LICENSE
`-- README.md
```

## Labeling

IWCS does **not** use human annotation. `Attack_Type` is a deterministic label derived from the controlled simulation condition. The dataset extraction parser derived the class from condition-specific filename patterns. The audit checks consistency between `Attack_Type` and the five one-hot class columns; no one-hot inconsistencies were found in the 20,331 retained records. Inter-annotator agreement is therefore not applicable.

The released CSV preserves the identifier `Backoff_Manipulado` for compatibility, while the associated manuscript uses the English term **Manipulated Backoff**.

## Quality-control reconstruction

The curation sequence is documented in `provenance/cleaning_stage_summary.csv`. Starting from 22,180 source rows, the quality-control stages remove 1,849 rows and produce the released 20,331-record table. The parsed-value reproduction check is stored in `provenance/reproduction_check.json`.

The complete curation archive is `IWCS_V1_CURATION_REPRODUCTION_BUNDLE.zip` (SHA-256 `b10ea5824727e732f76a316741c423b7561963fb047931a52bade3ec4fb7c951`). It includes the pre-curation table, full exclusion ledger, missing-`RUN_ID` ledger, dataset-curation script, stage counts, report, and reproduction verifier. The complete archive is included in Zenodo v1.1.0.

## Representative raw audit

Historical raw samples already in GitHub are **preserved rather than replaced**. The representative audit is documented in `metadata/raw_files_manifest_audited_run0.csv` and `metadata/scenario_comparison_run0_all_topologies.csv` (the historical filename is retained for compatibility).

The 20-file archive `audited-run0-sca.zip` (SHA-256 `8d7095a4d1158ebabb244af4a7317eab83395205212d2ca5f51aa394be337506`) contains one audited run-0 `.sca` execution for every topology x operating-condition combination and is included in Zenodo v1.1.0.

## Audited attack-source snapshot

The source audit covers `Rpl.cc`, `Rpl.h`, `ObjectiveFunction.cc`, and `ObjectiveFunction.h`. GitHub publishes the smaller ObjectiveFunction files and `simulation/audited/README.md`, which records file hashes and source-level findings.

The complete archive `rpl_attack_source_audited.zip` (SHA-256 `d0cf96b11b3e913e5bc4ac640b13cb61ee998f609c2091dd5563694026e1395e`) is included in Zenodo v1.1.0. This source snapshot supports code-level inspection of representative attack semantics; it is **not** presented as proof that every released record can be regenerated from the incomplete historical raw corpus.

## Diagnostic evaluation

The repository includes diagnostic benchmark results in `metadata/benchmark_results.csv`, including Decision Tree, Random Forest, and Logistic Regression baselines; random stratified evaluation; Leave-One-Topology-Out (LOTO) evaluation; and a six-feature ablation excluding `Avg_Delay_ms` and `Energy_Consumed_J`.

For the diagnostic models, `Attack_Type` and the one-hot class columns must not be used as predictors because they directly encode the target class. `Topology` is excluded from predictor sets for topology-aware generalization and is used only to define the LOTO partitions.

The high within-dataset scores must **not** be interpreted as evidence of universal deployment performance. They indicate strong separability within this controlled simulation design and motivate topology-aware validation, feature ablation, and checks for simulation-specific shortcuts.

Additional checks are published in:

- `metadata/precision_regime_crosscheck.csv` - cross-evaluation between the two numerical-precision regimes;
- `metadata/single_feature_diagnostic.csv` - shallow single-feature diagnostic results;
- `metadata/scenario_comparison_run0_all_topologies.csv` - representative raw-level metric audit across all 20 topology-condition combinations (historical filename retained).

## Important limitations

The documentation explicitly records the following limitations:

- filename-based class assignment in the dataset extraction parser;
- a defensive PDR cap at 100% in the parser;
- two numerical-precision regimes already present in the pre-curation table;
- deterministic patterns in selected delay/energy features;
- run-level aggregation that discards much of the temporal richness of vector outputs;
- fixed/calibrated attacker placement and topology-specific configuration choices;
- bounded attack coverage and no complete physical industrial-testbed validation;
- incomplete retention of the full historical raw corpus.

For machine-learning reuse, do not use `Attack_Type` or the one-hot class columns as predictors. For topology-generalization studies, exclude `Topology` from predictors and prefer topology-aware validation such as LOTO.

## Parser provenance note

The original parser remains under `simulation/parse_omnet.py` for provenance. Documented behaviors include filename-based class assignment and the defensive PDR cap. The newer scripts under `scripts/` are audit/reproducibility utilities and should not be interpreted as evidence that every released row can be regenerated from the incomplete retained raw corpus.

## Citation

```bibtex
@dataset{lo_nunes_iwcs_dataset_2026,
  author    = {Lo Nunes, Osvaldo Sebastião},
  title     = {IWCS-Dataset: Simulation Dataset for Cyberattack Analysis in IIoT Wireless Sensor Networks},
  year      = {2026},
  publisher = {Zenodo},
  version   = {1.1.0},
  doi       = {10.5281/zenodo.21853437},
  url       = {https://zenodo.org/records/21853437}
}
```

For references that should resolve to the dataset across versions, the concept DOI is **10.5281/zenodo.20602870**. See also `CITATION.cff`.

## License

The released dataset is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license. Source-code files derived from or adapted from third-party software retain the license obligations applicable to those source files; the dataset license does not override software licenses.

## Contact

For questions, reproducibility reports, or corrections, use the GitHub issue tracker or the contact information associated with the Zenodo record.
