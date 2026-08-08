# IWCS-Dataset V1 — Full Structural Audit

## Released table

- File: `dataset/dataset_omnetpp_cleaned_2.csv`
- SHA-256: `523a291aea10a6bd29a5806d39494e288435860d6933296c729e8591fb08d73c`
- Records: **20,331**
- Attributes: **16**
- Missing values: **0**
- Exact duplicate rows: **0**
- Repeated `RUN_ID`: **0**
- `Attack_Type`/one-hot inconsistencies: **0**
- Values outside the declared structural/plausibility checks: **0**

## Identifier traceability

The retained dataset spans `RUN_ID` 1–22,000 with **1,669 missing identifiers**. The recovered pre-curation source makes the origin of these gaps explicit:

- **556** identifiers were already absent from the pre-curation table.
- **1,113** identifiers were present in the pre-curation table and were removed by the documented quality-control stages.

The row-removal ledger and missing-ID ledger are provided in compressed CSV form under `provenance/`.

## Exact final-curation reconstruction

The recovered pre-curation table contains **22,180 rows**. Replaying `scripts/clean_dataset_final.py` removes **1,849 rows** and yields **20,331 rows**, exactly equal to the published V1 after CSV parsing, with zero different cells. This proves the final curation stage, not full row-by-row regeneration from every historical OMNeT++ raw output.

## Numerical representation

Two precision regimes are present in V1:

- **18,528 rows** with `RUN_ID <= 20000` use a coarser historical representation.
- **1,803 rows** with `RUN_ID > 20000` retain higher floating-point precision.

The exact reconstructed cleaning stage preserves source precision, so this difference is inherited from the pre-curation table and was **not introduced by the final cleaner**.

The audit also identified strongly deterministic historical patterns in `Avg_Delay_ms` and `Energy_Consumed_J` for several topology-class groups. These patterns are documented as a potential shortcut-learning risk rather than interpreted as independent evidence of physical realism.

## PDR legacy behavior

The historical parser applied a defensive `min(PDR, 100%)` cap. The final released table contains **1,242 values exactly equal to 100%**. The revised documentation separates the mathematical PDR definition from this historical implementation behavior and does not claim that all V1 PDR values were recomputed from the complete raw corpus.

## Representative raw audit

Raw-level methodology and attack behavior were cross-checked using one official run-0 `.sca` execution for each of the **20 topology-scenario combinations**. This representative audit supports configuration/attack traceability, but it is **not** presented as numerical regeneration of the complete V1 table.

## Diagnostic machine-learning audit

Random hold-out and topology-aware LOTO experiments using operational features produced near-perfect classification. Additional ablation excluding `Avg_Delay_ms` and `Energy_Consumed_J` remained very strong. These results are interpreted cautiously: they demonstrate strong within-design separability and may reflect simulation-specific signatures or shortcut learning. They should not be interpreted as evidence of universal performance on physical IIoT networks.

## Conclusion

V1 is structurally consistent and its final curation provenance is now exactly reproducible from the recovered pre-curation table. Its historical simulation and preprocessing limitations are explicitly documented to support responsible reuse.
