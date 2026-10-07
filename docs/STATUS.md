# PRSL evidence/status — 2026-10-07 (after original-source import)

## Claim levels

- **Rerun and passed here:** source recovery/integrity tooling and Python tests actually executed in this recovery session.
- **Historical evidence only:** results retained from the earlier Lab research, not reexecuted now.
- **Unimplemented / not validated:** everything required to affect running MOO2 safely or to coordinate independent clients.

| Component | Evidence level | Finding and limitation |
|---|---|---|
| Original 0.2.0 Python/C source | **Reproduced** | 31 original members copied byte-for-byte from directly uploaded 47,187-byte ZIP; source SHA-256 `2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e` |
| Offline Python test suite | **Rerun** | 52 total; 43 passed, 9 skipped needing `MOO2_ENGINE`, Python 3.13.5/Linux |
| Safe importer/handoff tests | **Rerun** | 11/11 passed before and after source import; source import dry-run and real import passed |
| Source checksums | **Rerun** | All 31 extracted members identical to original archive; `lab/SOURCE_SHA256SUMS.txt` indexes 30 other files |
| Original isolated x86 probe | **Historical only** | 30/30 checks recorded in `lab/evidence/native-probe.log`, NOT rerun in this recovery environment |
| Archive/workspace build | **Historical only** | 944 files verified with the original supplied game and patch archives; NOT reproduced here |
| Workspace safety scenarios | **Historical only** | Six prior checks recorded; no current game archives supplied |
| `Human_Hit_Next_Turn_` getter | **Historical exact-engine mapping** | Read-only flag getter, **not** an End Turn submission point |
| Manual Next button candidate | **Historical isolated candidate** | Object offset `0x00076D78`, file offset `0x0010C40C`, not a certified live/runtime hook; automatic caller remains |
| Safe in-game native adapter, UI and coordinator transport | **Not built/validated** | No game-native Ready/Unready, no authenticated two-client barrier, no live native release |
| Pre-game lobby / optional Chat | **Out of scope** | Independent components and projects, no dependency for PRSL |
| Windows/macOS MOO2 and multiplayer acceptance | **Not run** | Python test execution on Linux is not a portable game test |

## Implications

The historical Lab source is now genuinely available for future engineering and regression protection. It is an offline coordinator plus an exact-engine research test harness, **not a playable mod**. The nine skipped binary tests need a legitimate exact-build `ORION150.EXE`, never added to CI. The native probe also requires a suitable Linux/GCC 32-bit compatibility environment. Even if both pass, a separate DOSBox guest adapter and real multi-client acceptance are still required.

PRSL remains disabled in the separately versioned launcher. Stop and diagnose any uncertainty after native submission; do not infer a game turn happened from a coordinator transition. Use `docs/ROADMAP.md` and `docs/ACCEPTANCE-TESTS.md` for the next evidence-gated milestones.

The recovered source archive and retained historical handoff manifests are intentionally not packaged into Git; see `provenance/README.md` and `lab-import-provenance.json`.
