# v1.1 RUN_ID regime rule

The legacy v1.1 table contains two record-generation regimes. The boundary is the `RUN_ID`
column, and the boundary row belongs to regime A:

| Regime | Rule | Description (R2 manuscript) |
|---|---|---|
| A | `RUN_ID <= 20000` | Deterministic construction patterns: Energy follows `E = 0.01*N*m_c`, and Delay follows `0.4*N` or `0.24*N`. |
| B | `RUN_ID > 20000` | Second, undocumented upstream generation regime with a different numeric precision. |

Any analysis of v1.1 must report its results per regime, or test its sensitivity to the regime.
The R2 cross-check was a six-feature RF trained on A and tested on B, and the reverse.

```python
import pandas as pd
df = pd.read_csv("dataset/dataset_omnetpp_cleaned_2.csv")  # v1.1 table
df["regime"] = (df["RUN_ID"] > 20000).map({False: "A", True: "B"})
```

This rule applies **only** to v1.1. v2.0.0 has no `RUN_ID` column: each v2 row is identified
by `(config, run)` and by its `sca_sha256`.
