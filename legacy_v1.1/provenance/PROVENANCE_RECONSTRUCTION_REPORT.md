# IWCS-Dataset V1 — Provenance Reconstruction

## Main result

The published `dataset_omnetpp_cleaned_2.csv` can be reproduced **exactly at the tabular-value level** from the recovered pre-curation table using the recovered `clean_dataset_final.py`.

- Pre-curation table: **22,180 rows × 16 columns**
- Published curated table: **20,331 rows × 16 columns**
- Removed source rows: **1,849**
- Parsed-table equality: **True**
- Different cells after parsing: **0**

This establishes provenance for the **final curation stage**.

## Cleaning stages

| Stage | Before | Removed | After |
|---|---:|---:|---:|
| 01_empty_rows | 22,180 | 278 | 21,902 |
| 02_exact_duplicates | 21,902 | 180 | 21,722 |
| 03_run_id | 21,722 | 278 | 21,444 |
| 04_remaining_nulls | 21,444 | 279 | 21,165 |
| 05_invalid_categories | 21,165 | 278 | 20,887 |
| 06_physical_ranges | 20,887 | 278 | 20,609 |
| 07_one_hot | 20,609 | 278 | 20,331 |

The removals sum to **1,849 rows**, leaving exactly **20,331** records.

## RUN_ID gaps

The final dataset has **1,669 missing identifiers** in the 1–22,000 range.

- **556 IDs** were already absent from the recovered pre-curation table.
- **1,113 IDs** were present in the source and were removed by quality-control filters.

Duplicate-row and duplicate-ID removal may remove source rows without creating a new RUN_ID gap because another copy of the same identifier remains.

## Scientific interpretation

This finding substantially strengthens the V1 provenance claim. It is defensible to state that the published 20,331-row table is the deterministic output of the recovered final curation script applied to the recovered pre-curation table.

However, the recovered pre-curation table is an **intermediate/pre-curation table**, not the complete retained OMNeT++ raw corpus. Therefore this reconstruction proves:

1. exact provenance of the final cleaning/curation stage;
2. exact reasons and counts for the 1,849 source-row exclusions;
3. exact final table content after parsing;
4. a traceable audit trail for missing RUN_ID values.

It does **not** by itself prove row-by-row regeneration of the pre-curation table from every historical `.sca/.vec/.vci` file. Raw-level traceability remains representative across the 20 topology-scenario combinations.

## Numeric precision

The final cleaner explicitly preserves original floating-point precision rather than rounding it. Therefore, the two precision regimes observed in the published V1 are inherited from the recovered pre-curation table; they were **not introduced by the final cleaning step**. Their upstream origin is documented as a historical preprocessing difference.

## Integrity hashes

- Pre-curation table SHA-256: `4066b7f8361bf1933ddd6baaa44e9000eae35b5e82a1de92cdb7519b927b73b0`
- Published V1 SHA-256: `523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`
- Recovered cleaner SHA-256: `23bfc0795df1b2ea93d5e8772ba4a33cc7589d6937f8237845cd1a8fff20b424`

The pre-curation table may be distributed in compressed form in the repository to reduce storage size; decompression restores the audited CSV byte stream associated with the hash above.
