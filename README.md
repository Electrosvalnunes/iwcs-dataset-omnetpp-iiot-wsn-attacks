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

1. **Exact final-curation reconstruction.** The recovered pre-curation table contains **22,180 rows**. Re-executing the recovered final-curation procedure removes **1,849 source rows** and reproduces the released **20,331-row** table exactly at the parsed value level. The branch provides the cleaning script, machine-readable stage counts, integrity hashes, and a detailed reconstruction report. The pre-curation CSV itself is not stored in GitHub in this branch because of repository-transfer constraints and therefore must be supplied separately to independently rerun `verify_v1_reproduction.py`.
2. **Representative raw-file traceability.** The complete historical OMNeT++ raw corpus was not retained. Existing repository raw samples remain available for structural inspection. A separate audit also covered one run-0 `.sca` file for each of the 20 topology-scenario combinations; these audit results are documented as representative evidence and are not presented as row-by-row regeneration of V1.

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
│   └── topology_attack_distribution.csv
├── raw-samples/
│   └── existing representative OMNeT++ `.sca`, `.vec`, and `.vci` samples
├── scripts/
│   ├── clean_dataset_final.py
│   ├── validate_dataset_integral.py
│   ├── verify_v1_reproduction.py
│   ├── benchmark_baselines.py
│   └── generate_figures.py
├── simulation/
│   └── historical simulation/configuration materials already released
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

For machine-learning reuse, avoid using the one-hot class columns as predictors and prefer topology-aware validation when evaluating generalization. Near-perfect within-dataset benchmark performance should be interpreted as evidence of strong separability within this simulation design, not as evidence of universal deployment performance.

## Historical parser note

The original parser remains under `simulation/parse_omnet.py` for provenance. It is a **legacy artifact** and contains behaviors documented in the revision audit, including filename-based class assignment and the historical PDR cap. The newer scripts under `scripts/` are audit/reproducibility utilities and should not be interpreted as evidence that every V1 row can be regenerated from the incomplete retained raw corpus.

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
