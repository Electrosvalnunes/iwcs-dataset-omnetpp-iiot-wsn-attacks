# Audited recovered RPL source snapshot

This directory contains source material inspected during the 2026 major revision. It is separated from the historical simulation directory to avoid presenting a recovered audit snapshot as exact row-level provenance for every V1 record.

## Files and integrity

| File | Size (bytes) | SHA-256 | GitHub status |
|---|---:|---|---|
| `ObjectiveFunction.cc` | 3,250 | `0a58b20923ee7e9525e3957509fca44b06413444f7ca35c88ecfd57c852ab51c` | Published here |
| `ObjectiveFunction.h` | 2,348 | `eeafd0ad7f843ba30c3e2a781bdd2425c091db7b5177fdc12d4d695726e041b8` | Published here |
| `Rpl.cc` | 86,203 | `cc9e45274c2b8e2955d020235f963f10130941fc97000d8879ec3b9f66239be1` | Included in prepared archival ZIP |
| `Rpl.h` | 27,724 | `a14a3eb193452042cce62f34f69a055a1ae3471e13755a36111edd26c2bf7c9f` | Included in prepared archival ZIP |

Complete prepared archive: `rpl_attack_source_audited.zip`

SHA-256: `d0cf96b11b3e913e5bc4ac640b13cb61ee998f609c2091dd5563694026e1395e`

The connected GitHub contents interface truncates larger binary/text transfers, so the complete ZIP is reserved for the archival dataset deposit rather than publishing a corrupted copy here.

## Findings supported by the recovered source

- The objective function defaults to `HOP_COUNT`; candidate parents are selected by the lowest advertised rank, and hop-count rank is computed as the preferred parent's rank plus one.
- The recovered RPL implementation exposes `maliciousRank`, `attackStartTime`, and `attackEndTime` controls and can advertise a fixed attractive rank while an attack window is active.
- The blackhole helper drops transit unicast packets while allowing packets addressed to the malicious node and multicast control traffic.
- Wormhole support redirects upward routing through a private PPP/tunnel interface and can be combined with an attractive malicious rank.
- Because the blackhole-drop predicate is tied to `maliciousRank` and the active attack flag, recovered wormhole configurations using `maliciousRank` can inherit transit-dropping behavior. This is why the revision describes the recovered wormhole implementation conservatively as potentially hybrid.

These findings document the inspected recovered implementation. They do **not** establish that the retained source/raw files can regenerate every historical V1 row.

## License

The recovered source files retain their upstream GNU General Public License terms. The dataset's CC BY 4.0 license does not override source-code licensing.
