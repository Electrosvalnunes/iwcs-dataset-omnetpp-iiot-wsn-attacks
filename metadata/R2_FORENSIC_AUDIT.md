# IWCS R2 forensic audit notes

This note records the additional checks performed during the second major-revision audit of the historical IWCS v1.1.0 table. It is intended to make the limits of the retained evidence explicit; it does not claim row-complete regeneration of the historical raw corpus.

## Evidence levels

- **Exactly reproducible:** the retained 22,180-row pre-curation table plus `clean_dataset_final.py` reproduce the released 20,331-row CSV at parsed-value level.
- **Representative raw audit:** one retained representative `.sca` execution per topology-condition cell supports direct checks of packet counters, delay population, residual-energy calculations, configuration semantics, and attack behavior.
- **Unresolved upstream generation:** the complete historical raw corpus and the full raw-to-pre-curation generation context were not retained.

## RUN_ID boundary

The documented design contains 4 topologies x 5 operating conditions x `repeat=1000`, i.e., a 20,000-position primary campaign index space. The historical table extends to RUN_ID 22,000. The boundary at exactly 20,000 is therefore treated as evidence of a **distinct undocumented second upstream record-generation regime** for RUN_ID 20,001-22,000.

The retained artifacts do not establish whether this second regime was produced by additional simulator executions, a second extraction pass, or another upstream table-generation procedure. Among retained rows, 18,528 records have RUN_ID <= 20,000 and 1,803 have RUN_ID > 20,000; the latter also preserve a higher numerical-precision regime. The curation script does not introduce this precision split.

## Curation-stage counts

The curation exclusion ledger records each source row by its **first exclusion stage**. Therefore, the repeated counts of 278 at several quality-control stages refer to distinct groups of rows; they are not the same 278 rows being removed repeatedly. The equality of those counts is already present in the earliest retained tabular artifact, `dataset_omnetpp_P.csv`. The available evidence does not establish why several different anomaly categories each contain exactly 278 rows, so no simulator-level cause is assigned.

## Deterministic Energy_Consumed_J construction

For every retained record with RUN_ID <= 20,000, the released `Energy_Consumed_J` field follows the exact rule

`Energy_Consumed_J = 0.01 * N * m_c`

where `N` is the total topology size (36, 49, 64, or 100) and the class multiplier `m_c` is:

- Normal: 1.0
- Flooding: 5.0
- Blackhole: 1.0
- Wormhole: 1.0
- Backoff_Manipulado: 1.8

Because each class multiplies the same topology-size vector by a class-specific constant, both the pooled mean and pooled standard deviation scale by that constant. This directly explains the nearly invariant energy coefficient of variation across the five classes (approximately 0.385) despite a fivefold span in class means.

Representative raw sensor-energy consumption, reconstructed as initial minus residual sensor energy, is on a materially different scale and does not reproduce this released-field rule. The released energy column is therefore treated as a legacy-derived table attribute rather than a direct raw physical measurement.

## Deterministic Avg_Delay_ms construction

In the RUN_ID <= 20,000 regime, the released `Avg_Delay_ms` values obey exact topology-size rules for four conditions:

- Normal: `0.4 * N` ms
- Flooding: `0.4 * N` ms
- Blackhole: `0.4 * N` ms
- Wormhole: `0.24 * N` ms

Manipulated Backoff instead shows a separate high-delay, topology-dependent pattern with appreciable within-cell variation.

The representative OMNeT++ raw delay signal is `sink[0].app[0].endToEndDelay` and is populated only by successfully delivered legitimate application-0 packets. Its sample count matches the legitimate receive count. Lost packets are not included, and additional Flooding/Backoff attack traffic is recorded separately. Representative raw delay values do not reproduce the deterministic released-field construction; the released delay column is therefore treated as legacy-derived.

## PDR recomputation

For the 20 representative topology-condition executions, PDR was independently recomputed as

`100 * legitimate packets received at sink / legitimate packets transmitted by sensors`.

No representative execution exceeded 100%; 0/20 required clipping, and two Normal representatives were exactly 100%. The mathematical PDR definition therefore does not include clipping. Any historical 100% cap is documented only as legacy parser behavior.

## Shadowing sigma

The retained configuration files confirm `sigma=60` for Grid 64 and Grid 100. This is not a transcription error. It is documented as a historical stress/calibration setting, not as an empirically validated industrial shadowing standard deviation. Together with topology-specific MAC retry limits and the Grid 100 legitimate traffic rate, this prevents interpretation of the four topologies as a pure node-count scaling experiment.

## Wormhole semantics

Recovered source/configuration audit shows that the historical Wormhole condition combines PPP tunnel behavior with false-rank attraction. Because the recovered transit-drop predicate is tied to the malicious-rank condition during the attack window, the retained Wormhole implementation can also inherit Blackhole-style transit dropping. The historical class is therefore described conservatively as a hybrid Wormhole/sinkhole/blackhole realization rather than a protocol-pure Wormhole.

The representative raw Wormhole delay is higher than Normal in the audited topologies, so the earlier shortcut-based explanation for the lower released legacy delay value was withdrawn.

## RSSI diagnostic

A single-feature topology-classification check using only `Avg_RSSI_dBm` gives:

- standardized Logistic Regression: accuracy 0.2616, macro-F1 0.1738;
- Random Forest (`n_estimators=200`, `max_depth=5`): accuracy 0.2641, macro-F1 0.2441.

With four approximately balanced topology labels, chance accuracy is about 25%; these results do not indicate strong standalone topology leakage in the released CSV. However, the retained raw RSSI instrumentation is not sufficiently validated as a receiver-specific distance-sensitive path-loss measurement, so RSSI remains a simulation-specific diagnostic attribute.

A further attack-classification sensitivity check excluding Delay, Energy, and RSSI still gives mean LOTO accuracy 0.9864 for Random Forest and 0.9964 for Logistic Regression.

## Scope of the historical release

The historical IWCS table remains useful as an auditable simulation-derived resource for controlled benchmarking, data-quality/shortcut analysis, topology-condition sensitivity, and preliminary IDS experiments. It should not be interpreted as a factory-calibrated physical dataset, a pure topology-size experiment, or a source of universal attack signatures.
