# Changelog

## 2.0.0 — 2026-11-15

New dataset, published as version 2.0.0 of the Zenodo record
(DOI [10.5281/zenodo.24224309](https://doi.org/10.5281/zenodo.24224309)). It supersedes v1.1.0,
which is deprecated.

- **New table:** `dataset/iwcs_v2_features.csv`, 600 runs (4 grids × 5 conditions × 30 seeded
  repetitions), 23 columns, SHA-256
  `70fb129b80de6d976f294159f860fbd79b60f0d8c05c1aca25bc5b9471550223`. Every row carries the
  SHA-256 of its raw `.sca` file; the 600 `.sca` files are published on Zenodo.
- **Code and provenance:** RPL model (`src/`), INET 4.2.10 patch (`inet/`, `inet_patch/`),
  `.ini`/`.ned` files (`simulations/`), campaign, extraction, table and benchmark scripts with the
  manifest (`campaign_v2/`), and the verification evidence (`docs/verificacao/`), including
  addendum A1 (21 flooding runs re-run with a 1500 J sink store).
- **Licences:** `LICENSES.md` and `LICENSES/` (data CC BY 4.0; RPL model GPL-3.0-or-later;
  patched INET files LGPL-2.0-or-later; our scripts and configuration MIT).
- **v1.1 moved:** the whole v1.1.0 repository content is now in `legacy_v1.1/`, unchanged except
  for a deprecation banner at the top of its README, the new `DEPRECATED.md` and `RUN_ID_REGIME.md`.
  History is kept. The previous changelog is `legacy_v1.1/CHANGELOG.md`.
- **Do not mix v1.1 with v2:** different generators and feature definitions, even where column
  names coincide.
