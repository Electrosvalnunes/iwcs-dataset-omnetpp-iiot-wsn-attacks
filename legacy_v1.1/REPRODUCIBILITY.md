# IWCS-Dataset reproducibility and provenance

This document separates the evidence that can be reproduced exactly from evidence that is representative of the OMNeT++ campaign.

## 1. Released scientific CSV

The scientific data file remains `dataset/dataset_omnetpp_cleaned_2.csv` with 20,331 rows and 16 attributes. The v1.1.0 update strengthens documentation, validation, provenance, and audit artifacts; it does not replace or silently modify the released CSV.

Released CSV SHA-256:

`523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`

Current Zenodo release: **v1.1.0**, DOI **10.5281/zenodo.21853437**.

## 2. Exact curation reproducibility

The pre-curation table contains 22,180 rows. The dataset-curation script removes 1,849 source rows and reproduces the released 20,331-row dataset exactly at parsed-value level (zero different cells).

GitHub contains the curation script, stage counts, integrity check, and reconstruction report under `scripts/` and `provenance/`.

The complete curation bundle is `IWCS_V1_CURATION_REPRODUCTION_BUNDLE.zip` with SHA-256 `b10ea5824727e732f76a316741c423b7561963fb047931a52bade3ec4fb7c951`. It contains the 22,180-row pre-curation table, row-level exclusion ledger, missing-`RUN_ID` ledger, stage counts, integrity metadata, dataset-curation script, and reproduction verifier. The complete bundle is included in Zenodo v1.1.0.

## 3. Representative raw-file traceability

The complete OMNeT++ raw corpus used to generate all released records was not retained. Therefore, this repository does not claim row-by-row raw regeneration of all 20,331 released records.

A separate audit used one run-0 `.sca` execution for every topology-condition combination (4 topologies x 5 operating conditions = 20 combinations). File names, sizes, and SHA-256 hashes are published in `metadata/raw_files_manifest_audited_run0.csv`.

The archive `audited-run0-sca.zip` has SHA-256 `8d7095a4d1158ebabb244af4a7317eab83395205212d2ca5f51aa394be337506` and is included in Zenodo v1.1.0.

This archive is representative audit evidence, not a replacement for the incomplete historical raw corpus.

## 4. Historical raw samples are preserved

Files already stored under `raw-samples/` are retained as historical evidence. They are not deleted or overwritten by the audit. The representative audit evidence is documented separately so that legacy samples and revision-stage evidence cannot be confused.

## 5. Audited RPL source

The source audit covers `Rpl.cc`, `Rpl.h`, `ObjectiveFunction.cc`, and `ObjectiveFunction.h`. GitHub publishes the two smaller ObjectiveFunction files and `simulation/audited/README.md`, which records SHA-256 hashes for all four source files and the source-level findings.

The complete source archive is `rpl_attack_source_audited.zip` with SHA-256 `d0cf96b11b3e913e5bc4ac640b13cb61ee998f609c2091dd5563694026e1395e` and is included in Zenodo v1.1.0.

This source snapshot supports inspection of representative attack semantics; it is not presented as proof that every released record can be regenerated from retained source and raw files.

## 6. Parser provenance

`simulation/parse_omnet.py` is retained for provenance. Documented behaviors include filename-based class assignment and a defensive PDR cap at 100%. The newer files under `scripts/` are validation/reconstruction utilities and should not be confused with a complete raw-to-table regeneration pipeline.

## 7. Diagnostic machine-learning evaluation

Diagnostic results are under `metadata/`. `Attack_Type` and the one-hot class columns are excluded from predictors because they directly encode the target class. `Topology` is also excluded from predictors for topology-generalization tests and is used only to define the Leave-One-Topology-Out partitions. High within-dataset performance is interpreted as evidence of strong simulation-specific separability and possible shortcut learning, not as evidence of universal deployment performance.

## 8. Integrity manifests

Use `metadata/reproducibility_archives_manifest.csv` for archive-level SHA-256 checks, `metadata/raw_files_manifest_audited_run0.csv` for file-level checks of the 20 representative raw executions, and `SHA256SUMS.txt` for the principal released artifacts.
