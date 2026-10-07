# Changelog / provenance

This repository's documentation and source-restoration snapshots are **not** PRSL gameplay mod releases.

## 2026-10-07 — Source restored, historical Lab v0.2.0 integrated

- Imported the exact user-supplied 47,187-byte original v0.2.0 ZIP (SHA-256 `2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e`) through the existing fail-closed importer.
- Imported **31 source, research, original-evidence and test files** into `lab/`, matching every ZIP member byte-for-byte; preserved `lab/SOURCE_SHA256SUMS.txt`.
- Re-ran original Lab test suite on Python 3.13.5/Linux: 52 tests, **43 passed / 9 skipped** due to the deliberately absent proprietary engine file.
- Re-ran original 11 handoff/importer tests plus six restored-Lab provenance tests; added source-integrity verification and CI offline Lab tests.
- Updated repository identity to `MOO2-Social-Gaming-Community/PRSL-Mod`, status, documentation and development gates; moved superseded missing-source records into frozen `provenance/`.
- **Did not** implement a live game hook, networked readiness transport, on-screen Ready/Unready, DOSBox integration, automatic turn interception or two-client acceptance.

## 2026-10-07 — Earlier GitHub research handoff (historical)

- Collected 0.1.0 design, 0.2.0 research evidence, exact-hash map and separate launcher references.
- Added safe original-source importer, repository tests, security/legal notices and the PRSL development roadmap.
- At that time the original source ZIP was not available to the handoff environment; this limitation is superseded by the above source recovery.

## 2026-10-05 — Original PRSL Lab v0.2.0 (original source preserved intact in `lab/`)

- Mapped exact 1.50.26 executable; corrected misconception about getter semantics; identified candidate manual gate, automatic path and wrapper.
- Tested isolated x86 instructions and coordinator transitions. Fixed duplicate-Ready-in-grace-state regression and added disconnect/fault behavior.
- Implemented offline workspace/certificate tests and a research CLI that fails closed on PRSL launch.

## 2026-10-04 — Earlier PRSL design and Lab v0.1.0

- Original intent: reversible in-game pre-submission Ready/Unready and an optional turn timer, **not** a pre-game lobby.
- Earlier coordinator prototype; repeated-Ready regression later diagnosed and corrected in Lab v0.2.0.
