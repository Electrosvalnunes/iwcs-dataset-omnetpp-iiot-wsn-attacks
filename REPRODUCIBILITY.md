# IWCS-Dataset reproducibility and provenance

This document separates the evidence that can be reproduced exactly from evidence that is representative of the historical OMNeT++ campaign.

## 1. Released V1 remains unchanged

The scientific data file remains `dataset/dataset_omnetpp_cleaned_2.csv` with 20,331 rows and 16 attributes. The 2026 major-revision work updates documentation, validation, provenance, and audit artifacts; it does not replace or silently modify the released V1 CSV.

Published V1 SHA-256:

`523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`

## 2. Exact final-curation reproducibility

The recovered pre-curation table contains 22,180 rows. The recovered final cleaner removes 1,849 source rows and reproduces the published 20,331-row dataset exactly at parsed value level (zero different cells).

The GitHub repository contains the curation script, stage counts, integrity check, and reconstruction report under `scripts/` and `provenance/`.

The complete curation bundle has been prepared as `IWCS_V1_CURATION_REPRODUCTION_BUNDLE.zip` with SHA-256 `b10ea5824727e732f76a316741c423b7561963fb047931a52bade3ec4fb7c951`.

It contains the recovered 22,180-row pre-curation table, the row-level exclusion ledger, the missing-RUN_ID ledger, stage counts, integrity metadata, cleaner, and reproduction verifier. The complete binary bundle is reserved for the archival dataset deposit because the connected GitHub contents interface was verified to truncate large binary transfers.

## 3. Representative raw-file traceability

The complete historical OMNeT++ raw corpus was not retained. Therefore, this repository does not claim row-by-row raw regeneration of all 20,331 released records.

A separate audit used one run-0 `.sca` execution for every topology-scenario combination (4 topologies × 5 conditions = 20 combinations). File names, sizes, and SHA-256 hashes are published in `metadata/raw_files_manifest_audited_run0.csv`.

The prepared archive is `audited-run0-sca.zip` with SHA-256 `8d7095a4d1158ebabb244af4a7317eab83395205212d2ca5f51aa394be337506`.

This archive is representative audit evidence, not a replacement for the incomplete historical raw corpus. Its complete binary copy is reserved for the archival dataset deposit.

## 4. Historical raw samples are preserved

Files already stored under `raw-samples/` are retained as historical evidence. They are not deleted or overwritten by the major-revision audit. New audit evidence is documented separately so that legacy samples and revision-stage evidence cannot be confused.

## 5. Audited recovered RPL source

The recovered source audit covers `Rpl.cc`, `Rpl.h`, `ObjectiveFunction.cc`, and `ObjectiveFunction.h`. The complete prepared archive is `rpl_attack_source_audited.zip` with SHA-256 `d0cf96b11b3e913e5bc4ac640b13cb61ee998f609c2091dd5563694026e1395e`.

GitHub publishes the two smaller ObjectiveFunction files and `simulation/audited/README.md`, which records SHA-256 hashes for all four source files and the source-level findings. The complete ZIP, including the larger `Rpl.cc` and `Rpl.h`, is reserved for the archival deposit because direct transfer through the connected GitHub interface was verified to truncate it.

This recovered source snapshot supports inspection of representative attack semantics; it is not presented as proof that every V1 row can be regenerated from retained source and raw files.

## 6. Legacy parser

`simulation/parse_omnet.py` is retained for provenance as a legacy artifact. Known historical behaviors include filename-based scenario classification and a defensive PDR cap at 100%. The newer files under `scripts/` are validation/reconstruction utilities and should not be confused with the original full raw-to-table pipeline.

## 7. Diagnostic machine-learning evaluation

Diagnostic results are under `metadata/`. Predictor sets exclude `Attack_Type` and the one-hot class columns; topology is also excluded for topology-generalization tests. High within-dataset performance is interpreted as evidence of strong simulation-specific separability and possible shortcut learning, not as evidence of universal deployment performance.

## 8. Integrity manifests

Use `metadata/reproducibility_archives_manifest.csv` for archive-level SHA-256 checks, `metadata/raw_files_manifest_audited_run0.csv` for file-level checks of the 20 representative raw executions, and `SHA256SUMS.txt` for the principal released/prepared artifacts.
