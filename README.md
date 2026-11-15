# IWCS v2: A Simulator-Traceable Run-Level Dataset of Normal Operation and Four Attack Conditions in Simulated Low-Power Wireless Sensor Networks

IWCS-Dataset v2.0.0 is a run-level table of 600 OMNeT++ 5.7.1 / INET 4.2.10 simulation runs of
the Routing Protocol for Low-Power and Lossy Networks (RPL). It covers:

- **Topologies:** four static grids with 36, 49, 64 and 100 nodes.
- **Conditions:** five operating conditions: normal operation, flooding, blackhole, wormhole and
  manipulated medium-access backoff.
- **Repetitions:** 30 seeded repetitions per topology–condition cell (runs 0–29).

Every row of the table can be traced to a published, unmodified scalar result file (`.sca`) through
its SHA-256.

| | |
|---|---|
| **Version** | 2.0.0 (2026-11-15) |
| **DOI (v2.0.0)** | [10.5281/zenodo.24224309](https://doi.org/10.5281/zenodo.24224309) |
| **Concept DOI (all versions)** | [10.5281/zenodo.20602870](https://doi.org/10.5281/zenodo.20602870) |
| **Table** | [`dataset/iwcs_v2_features.csv`](dataset/iwcs_v2_features.csv): 600 rows × 23 columns |
| **CSV SHA-256** | `70fb129b80de6d976f294159f860fbd79b60f0d8c05c1aca25bc5b9471550223` |
| **Licences** | Data CC BY 4.0; code under GPL-3.0-or-later, LGPL-2.0-or-later and MIT (see [`LICENSES.md`](LICENSES.md)) |

> **WARNING: v1.1 is deprecated. Do not mix v2 with v1.1.**
> v1.1.0 (DOI [10.5281/zenodo.21853437](https://doi.org/10.5281/zenodo.21853437)) has no retained
> raw corpus, and its operational columns (PDR, delay, energy, throughput) could not be reproduced
> from simulator output. v1.1 and v2 come from different generators and use different feature
> definitions, even where the column names coincide. Do not concatenate the two tables, train on
> one and test on the other, or pool them in any statistic.
> The v1.1 repository content is kept unchanged in [`legacy_v1.1/`](legacy_v1.1/), for
> traceability of earlier work only (see [`legacy_v1.1/DEPRECATED.md`](legacy_v1.1/DEPRECATED.md)).

## The table

One row per accepted run. The `topology` values `Grid35`, `Grid48`, `Grid63` and `Grid99` are the
36-, 49-, 64- and 100-node grids (N − 1 sensor hosts plus one central sink). The `condition`
values are `Normal`, `Flooding`, `Blackhole`, `Wormhole` and `Backoff`; each topology–condition
cell has 30 rows.

- **Identification:** `topology`, `condition`, `run`, `seed`, `config`, `dataset_version`,
  `cell_id`.
- **Features (8):** `Avg_RSSI_dBm`, `DIO_Count`, `DIS_Count`, `Rank_Changes`, `PDR_percent`,
  `Avg_Delay_ms`, `Throughput_kbps`, `Energy_Consumed_J` (energy consumed per sensor).
- **Auxiliary (7):** `Energy_Total_J`, `DIS_Total`, `DAO_Sent_Total`, `DAO_Received_Total`,
  `DAO_AckReceived_Total`, `DAO_Forwarded_Total`, `DAO_Dropped_Total`.
- **Traceability:** `sca_sha256`, the SHA-256 of the raw `.sca` file the row was extracted from.

Each run lasts 3600 s of simulated time with an 80 s warm-up; the features are measured in the
window 80–3600 s. The header of [`campaign_v2/extract_v2.py`](campaign_v2/extract_v2.py)
documents every column and its time window.

## Repository structure

```text
.
|-- README.md, CITATION.cff, CHANGELOG.md
|-- LICENSE                 CC BY 4.0 (data and documentation)
|-- LICENSES.md, LICENSES/  licence of each component; GPL-3.0, LGPL-2.1 and MIT texts
|-- SOURCE_REVISION.txt     source commit and INET tag of this release
|-- dataset/
|   |-- iwcs_v2_features.csv (+ .sha256)
|   `-- ZENODO_v2.0.0_SHA256SUMS   SHA-256 of the files in the Zenodo v2.0.0 record
|-- src/                    RPL model (ComNetsHH omnetpp-rpl, with the attack mechanisms)
|-- inet/                   patched INET 4.2.10 files
|-- inet_patch/             the same patch as a diff against unmodified INET 4.2.10
|-- simulations/            the four grid .ini files and all .ned files
|-- campaign_v2/            cells.csv, manifest, campaign, extraction, table and benchmark scripts
|-- docs/verificacao/       equivalence and verification evidence (incl. addendum A1)
|-- Makefile, .project, .nedfolders, .oppbuildspec   OMNeT++ project files
`-- legacy_v1.1/            DEPRECATED v1.1.0 repository content, unchanged
```

The root of this repository has the same content as `iwcs_v2_code_and_provenance.zip` in the
Zenodo record, except that the RPL model's upstream README is in `src/README.md`.

## Files in the Zenodo record

The raw corpus is too large for this repository and is published only on Zenodo
([10.5281/zenodo.24224309](https://doi.org/10.5281/zenodo.24224309)):

| File | Content |
|---|---|
| `iwcs_v2_features.csv` (+ `.sha256`) | The 600-row table (identical to `dataset/` here). |
| `iwcs_v2_raw_sca.zip` | The 600 raw `.sca` files and their 600 `.ok` completion markers, plus the campaign status logs (`progress.tsv`, `launches.txt`). Each marker records the exit status, simulated time, event count, wall time and the SHA-256 of its `.sca`. |
| `iwcs_v2_code_and_provenance.zip` | The code and provenance tree (the root of this repository). |
| `legacy_v1.1.zip` | Deprecation notice for v1.1 and its `RUN_ID` regime rule. |
| `README.md`, `LICENSES.md`, `CITATION.cff`, `SHA256SUMS` | Documentation and checksums. |

To check a download: `sha256sum -c dataset/ZENODO_v2.0.0_SHA256SUMS`, run in the folder where the
Zenodo files are.

## Provenance

- **Simulator:** OMNeT++ 5.7.1 and INET 4.2.10 with the RPL patch (tag `ambiente-revisao-v1`).
  The source revision is in [`SOURCE_REVISION.txt`](SOURCE_REVISION.txt).
- **Runs:** runs 0–29 per cell with `seed-set = run`, so run *k* uses the same seeds in every cell.
  Only scalars are recorded. The `.ini` files are not modified: every deviation from a default
  run is a command-line option recorded in [`campaign_v2/manifest.txt`](campaign_v2/manifest.txt).
- **Acceptance rule:** a run is accepted only if the simulator exits with status 0, the simulation
  reaches 3600 s and the end-of-run scalars are present.
- **Addendum A1 (sink energy store):** in the first pass, 21 flooding runs aborted between 3575 s
  and 3600 s: 15 of 30 in Grid 36 and 6 of 30 in Grid 49.
  - **Cause:** the sink's 55 J energy store ran out, and INET's ICMPv6 module does not support the
    resulting crash operation.
  - **Re-run:** these 21 runs were re-executed with a 1500 J sink store (the sensor value), set by
    a command-line option ([`campaign_v2/rerun_sink_capacity.sh`](campaign_v2/rerun_sink_capacity.sh)).
  - **Equivalence:** with the sink energy-storage module excluded, event fingerprints are
    identical for 55 J and 1500 J, and the `.sca` files are identical except for that module's own
    scalar ([`docs/verificacao/sink_capacity_A1/`](docs/verificacao/sink_capacity_A1/)).
  - **Released columns:** sink energy is not a released column.

## Regenerating the dataset

1. **Simulator:** install OMNeT++ 5.7.1 and INET 4.2.10. From the INET root, apply
   `inet_patch/inet-4.2.10_rpl_patch_ambiente-revisao-v1.diff` with `patch -p1`. Build INET in
   release mode with the Visualization feature on.
2. **Layout:** put the INET tree next to this repository, named `inet` (the scripts expect
   `<repository>/../inet/src`). Build the RPL project in `src/` as a shared library
   (`MSGC:=$(MSGC) --msg6`).
3. **Campaign:** run `campaign_v2/run_campaign.sh 0 29` (environment variables `JOBS` and
   `OMNETPP_ROOT`), then `campaign_v2/rerun_sink_capacity.sh` (addendum A1).
4. **Processing:** run `python3 campaign_v2/extract_v2.py --strict`, then
   `campaign_v2/make_tables_v2.py --require-complete`, then `campaign_v2/benchmark_v2.py`
   (numpy 2.2.6 and scikit-learn 1.7.2, see `campaign_v2/requirements-benchmark.txt`).
5. **Checking:** compare the per-run `sca_sha256` values, or the CSV SHA-256, with the published
   ones.

**Checking the CSV without simulating:** download `iwcs_v2_raw_sca.zip` from Zenodo, unpack it
into `campaign_v2/results/` and run the processing step. The result is byte-identical to
`dataset/iwcs_v2_features.csv`.

## Known properties (documented, not corrected)

- **Radio channel:** the `radioMedium.attenuation.*` lines of the `.ini` files have no effect in
  INET 4.2.10. The effective channel is `BreakpointPathLoss` without shadowing, so
  `Avg_RSSI_dBm` is nearly constant (cell means between −81.56 and −81.51 dBm) and the post-warm-up
  `DIS_Count` is 0 in all 600 runs. Both are released for schema continuity; they are not
  link-quality measurements and should not be used as predictors.
- **PDR window boundary:** `PDR_percent` counts packets sent and received after the warm-up and is
  not capped. One run (`Grid48_Normal` run 14) has a PDR of 100.033 %: one packet was sent at
  79.992 s and received at 80.013 s, so it counts as received but not as sent.
- **Wormhole endpoints:** the malicious (second) endpoint of each tunnel also drops transit
  packets; the tunnels and their endpoints are listed in `campaign_v2/cells.csv`. Lured honest
  parents and attackers can form two-node DAO loops, which RPL rejects ("loop detected"); this
  is why `DAO_Received_Total` can exceed
  `DAO_Forwarded_Total + DAO_Dropped_Total`.
- **Grid 100 settings:** Grid 100 uses a 6 s legitimate send interval (55 s in the other grids) and
  no MAC retries.

The dataset supports studies of simulated attack effects and topology-aware benchmarking. It is
not evidence of physical deployment behaviour.

## Citation

```bibtex
@dataset{lo_nunes_sebastiao_iwcs_v2_2026,
  author    = {L{\'o} Nunes Sebasti{\~a}o, Osvaldo and Valencia de Almeida, Felipe and
               Rady de Almeida J{\'u}nior, Jorge},
  title     = {{IWCS v2: A Simulator-Traceable Run-Level Dataset of Normal Operation
               and Four Attack Conditions in Simulated Low-Power Wireless Sensor Networks}},
  year      = {2026},
  publisher = {Zenodo},
  version   = {2.0.0},
  doi       = {10.5281/zenodo.24224309},
  url       = {https://doi.org/10.5281/zenodo.24224309}
}
```

See also [`CITATION.cff`](CITATION.cff). The concept DOI
[10.5281/zenodo.20602870](https://doi.org/10.5281/zenodo.20602870) always resolves to the latest
version.

## Licence

- **Data and documentation:** [CC BY 4.0](LICENSE).
- **RPL model (`src/`):** GPL-3.0-or-later.
- **Patched INET files (`inet/`, `inet_patch/`):** LGPL-2.0-or-later.
- **Our scripts and configuration** (`campaign_v2/`, `docs/verificacao/`, `simulations/`): MIT.

Details and full texts: [`LICENSES.md`](LICENSES.md) and [`LICENSES/`](LICENSES/).

## Contact

For questions, reproducibility reports or corrections, use the GitHub issue tracker or the contact
information of the Zenodo record.
