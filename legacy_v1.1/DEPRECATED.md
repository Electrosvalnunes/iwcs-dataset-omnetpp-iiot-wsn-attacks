# DEPRECATED: IWCS-Dataset v1.1 (legacy)

> **v1.1 is deprecated. Use v2.0.0 ([`../dataset/iwcs_v2_features.csv`](../dataset/iwcs_v2_features.csv),
> DOI [10.5281/zenodo.24224309](https://doi.org/10.5281/zenodo.24224309)) for any new work.**

- **DOI (v1.1.0, deprecated):** [10.5281/zenodo.21853437](https://doi.org/10.5281/zenodo.21853437)
- **Where it is:** this folder holds the v1.1.0 repository content unchanged (moved here with
  `git mv`; the full history is kept, see `git log --follow`). The v1.1 table is
  [`dataset/dataset_omnetpp_cleaned_2.csv`](dataset/dataset_omnetpp_cleaned_2.csv), and it remains
  published on Zenodo under the v1.1.0 DOI. The last commit of the v1.1 layout is tagged `v1.1.0`.
- **Regime rule:** [`RUN_ID_REGIME.md`](RUN_ID_REGIME.md). v1.1 contains two record-generation
  regimes, `RUN_ID <= 20000` and `RUN_ID > 20000`, and must be analysed per regime.

Why v1.1 is deprecated (as documented in the R2 manuscript):

- **No raw corpus:** the complete OMNeT++ raw corpus behind v1.1 was not retained, so v1.1
  cannot be regenerated row by row.
- **Legacy-derived columns:** PDR, Delay, Energy and Throughput follow construction patterns,
  not simulator output, and do not match the retained representative raw executions.

**Do not mix v1.1 with v2.** Their feature names coincide, but their definitions do not
(for example the DIO/DIS/Rank windows and the energy normalisation), and neither do their
generators. Never concatenate the two tables, train on one and test on the other, or pool them
in a statistic.
