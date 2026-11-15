# Changelog

## 2026-08 — IEEE Data Descriptions major-revision reproducibility update (v1.1.0)

### Dataset data

- **No modification** to `dataset/dataset_omnetpp_cleaned_2.csv`.
- Released scientific CSV remains 20,331 rows x 16 attributes.
- Released CSV SHA-256 remains `523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`.

### Current release

- Zenodo version: **v1.1.0**
- Version DOI: **10.5281/zenodo.21853437**
- Concept DOI: **10.5281/zenodo.20602870**

### Added or strengthened

- exact curation reconstruction documentation (22,180 -> 20,331);
- machine-readable curation-stage counts and integrity check;
- full-record structural audit summary;
- descriptive statistics and topology x class distribution;
- diagnostic baseline, LOTO, ablation, precision-regime, and single-feature results;
- manifest for 20 representative run-0 `.sca` audit files;
- archive-level and file-level SHA-256 documentation;
- recovered ObjectiveFunction source snapshot and source-audit notes;
- `REPRODUCIBILITY.md` and `SHA256SUMS.txt`;
- synchronized `CITATION.cff` metadata for v1.1.0;
- revised README with explicit limitations, licensing boundaries, reuse guidance, and current DOI information.

### Clarified limitations

- incomplete retention of the full historical raw corpus;
- filename-derived class labels and defensive PDR cap;
- two inherited numerical-precision regimes;
- deterministic patterns in selected delay/energy features;
- topology-specific calibration and fixed attacker placement;
- run-level aggregation and loss of temporal vector detail;
- bounded attack coverage and absence of complete physical-testbed validation;
- audited stack does not demonstrate an explicit 6LoWPAN adaptation layer.

### Published reproducibility artifacts

The following complete binary archives are included in Zenodo v1.1.0 (DOI **10.5281/zenodo.21853437**) with documented SHA-256 values:

- `IWCS_V1_CURATION_REPRODUCTION_BUNDLE.zip`;
- `audited-run0-sca.zip`;
- `rpl_attack_source_audited.zip`.

The Zenodo release also includes the dataset archive and `IWCS_2026_REVISION_METADATA.zip`. See `metadata/reproducibility_archives_manifest.csv` and `REPRODUCIBILITY.md`.
