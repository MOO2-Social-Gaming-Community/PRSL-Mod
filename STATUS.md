# PRSL status — 2026-10-07, source restored

- **Recovered source:** historical PRSL Lab **v0.2.0**, 31 original ZIP members imported intact into `lab/` and byte-verified against the supplied original archive. See `lab-import-provenance.json` and `docs/SOURCE-RESTORATION-2026-10-07.md`.
- **Reproduced today:** 52 Lab Python tests: **43 passed, 9 skipped** without `MOO2_ENGINE`; 17 repository tests passed (11 original importer tests + 6 new provenance-integrity tests).
- **Historically reported but not reproduced today:** 30 isolated x86 checks, original 944-file workspace audit, and six workspace-safety checks.
- **Playable PRSL:** **NO.** There is no certified live engine adapter, on-screen readiness hook, PRSL client authentication/transport, or tested two-client Ready/Unready session.
- **Launcher separation:** Launcher v0.4.7 remains separate; PRSL must stay OFF and must not be enabled by manifest manipulation.
- **Exact researched engine:** 1.50.26 `ORION150.EXE` SHA-256 `2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c` (not distributed).
- **Game acceptance / release:** **NOT READY.** Test locally with legitimately owned game and explicit exact-build and recovery safety. No Windows/macOS or live multiplayer validation performed here.
- **License:** project redistribution terms and third-party notices have not been settled. Review `LICENSE-STATUS.md` before public source publication.

**The integrated repository snapshot is dated 2026-10-07; it is NOT a new working PRSL v0.3.0 game mod.**
