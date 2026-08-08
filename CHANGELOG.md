# Changelog

## 2026-08 — IEEE Data Descriptions major-revision reproducibility update

### Dataset data

- **No modification** to `dataset/dataset_omnetpp_cleaned_2.csv`.
- Released V1 remains 20,331 rows × 16 attributes.
- Released V1 SHA-256 remains `523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`.

### Added or strengthened

- exact final-curation reconstruction documentation (22,180 → 20,331);
- machine-readable curation-stage counts and integrity check;
- full-record structural audit summary;
- descriptive statistics and topology × class distribution;
- diagnostic baseline, LOTO, ablation, precision-regime, and single-feature results;
- manifest for 20 representative run-0 `.sca` audit files;
- archive-level and file-level SHA-256 documentation;
- recovered ObjectiveFunction source snapshot and source-audit notes;
- `REPRODUCIBILITY.md` and `SHA256SUMS.txt`;
- corrected `CITATION.cff` repository URL and metadata;
- revised README with explicit limitations, licensing boundaries, and reuse guidance.

### Clarified limitations

- incomplete retention of the full historical raw corpus;
- filename-derived legacy labels and historical PDR cap;
- two inherited numerical-precision regimes;
- deterministic patterns in selected historical features;
- topology-specific calibration and fixed attacker placement;
- run-level aggregation and loss of temporal vector detail;
- bounded attack coverage and absence of complete physical-testbed validation;
- audited recovered stack does not demonstrate an explicit 6LoWPAN adaptation layer.

### Archival artifacts prepared

The following complete binary archives were prepared with verified SHA-256 values for archival deposit. They are documented in GitHub but are not uploaded through the connected contents interface because that interface was verified to truncate larger binary transfers:

- `IWCS_V1_CURATION_REPRODUCTION_BUNDLE.zip`;
- `audited-run0-sca.zip`;
- `rpl_attack_source_audited.zip`.

See `metadata/reproducibility_archives_manifest.csv` and `REPRODUCIBILITY.md`.
