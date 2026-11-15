# Licenses of IWCS-Dataset v2.0.0

The files in this record fall under three licence regimes. Each component keeps its own licence.

> **In this GitHub repository:** the contents of `iwcs_v2_code_and_provenance.zip` are at the
> repository root (`src/`, `inet/`, `inet_patch/`, `campaign_v2/`, `docs/verificacao/`,
> `simulations/`, `LICENSES/`), and `iwcs_v2_features.csv` is in `dataset/`. The raw `.sca` corpus
> is only on Zenodo. The deprecated v1.1 files in `legacy_v1.1/` keep their v1.1 licence terms
> (dataset under CC BY 4.0, see `LICENSE`).

| Component | Files | License |
|---|---|---|
| **Data** | `iwcs_v2_features.csv` (+ `.sha256`); `iwcs_v2_raw_sca.zip` (600 `.sca` files, `.ok` markers, campaign status logs) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (same as v1.1) |
| **RPL simulation model** (ComNetsHH) | `iwcs_v2_code_and_provenance.zip`: `src/` | **GPL-3.0-or-later** |
| **INET Framework 4.2.10, patched files** | `iwcs_v2_code_and_provenance.zip`: `inet/`, `inet_patch/` | **LGPL-2.0-or-later** |
| **Our scripts and configuration** | `iwcs_v2_code_and_provenance.zip`: `campaign_v2/`, `docs/verificacao/`, `simulations/` (`.ini`, `.ned`), `Makefile`, project files | **MIT** (text below) |
| **Documentation** | `README.md`, `CITATION.cff`, `LICENSES.md`, `legacy_v1.1.zip` | CC BY 4.0 |

## Details

- **RPL model:** the source is
  <https://github.com/ComNetsHH/omnetpp-rpl>, Copyright (C) 2021 Institute of Communication
  Networks (ComNets), Hamburg University of Technology (TUHH), and (C) 2021 Yevhenii Shudrenko.
  - **Licence notices:** every source file carries the GNU GPL v3 "or (at your option) any later
    version" notice. `src/package.ned` declares `@license(GPLv3)`. The upstream repository has
    no separate LICENSE file, so these notices are the licence statement.
  - **Our modifications:** the attack mechanisms (blackhole/wormhole `maliciousRank`, DAO
    counters) are a derivative work and are distributed under the same GPL-3.0-or-later.
  - **Full text:** `LICENSES/GPL-3.0.txt` inside the code zip.
- **INET:** the INET Framework (<https://inet.omnetpp.org>) is composed of parts under GPL or
  LGPL, as stated in each source file.
  - **Patched files:** the files patched here (`MacProtocolBase.h`, `Ipv6NeighbourDiscovery.*`,
    `Ipv6.*`, `NetworkRouteCanvasVisualizer.cc`) carry the GNU LGPL "version 2 or any later
    version" notice. The patch and the patched files are distributed under that licence.
  - **INET itself:** INET is not redistributed here. Obtain INET 4.2.10 from its authors.
  - **Full text:** `LICENSES/LGPL-2.1.txt` inside the code zip.
- **MIT:** applies to files we wrote for this campaign. These are the campaign, extraction, table,
  benchmark, release and packaging scripts (`run_campaign.sh`, `run_batches.sh`,
  `rerun_sink_capacity.sh`, `status.sh`, `make_manifest.sh`, `extract_v2.py`,
  `make_tables_v2.py`, `benchmark_v2.py`, `make_release_v2.sh`, `make_zenodo_v2.sh`), the
  verification scripts in `docs/verificacao/`, and the simulation configuration files
  (`simulations/*.ini`, `simulations/*.ned`).
  - **Third-party tools:** using these files with OMNeT++, INET or the RPL model does not change
    the licences of those components.
- **Data:** CC BY 4.0 requires attribution. Please cite the record (`CITATION.cff`).

## MIT License

Copyright (c) 2026 Osvaldo Ló Nunes Sebastião, Felipe Valencia de Almeida,
Jorge Rady de Almeida Júnior

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
