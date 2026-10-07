# PRSL status assessment — 2026-10-07

## Evidence grading

- **Verified in previous research** means a retained artifact logs a test that historically passed under its own stated conditions. It **does not** mean this handoff reran the source or the game.
- **Reproduced in this handoff** means a test executed during the 2026-10-07 packaging process; limited to tooling/document validation.
- **Proposed** means a design requirement without a demonstrated implementation.
- **Blocked** means a missing dependency, unavailable source, or unvalidated live behavior.

| Finding | Classification | Evidence and limit |
|---|---|---|
| PRSL v0.2.0 existed | Historical artifact | Archived README and original ZIP metadata; Python/C source ZIP must still be imported |
| 52 Python tests passed | Historical verified | `research/archive-v0.2.0/evidence/python-tests.log`; coordinator, binary, packages and catalog; exact engine used for optional tests |
| 30 isolated native x86 checks passed | Historical verified | `.../evidence/native-probe.log`; Linux 64-bit harness switched into 32-bit compatibility mode; NOT a real game |
| Workspace builder verified 944 files | Historical verified | 816 base + 128 patch files; overlay changed no base files for supplied archives only |
| 6 workspace safety checks passed | Historical verified | Corruption failure, saves preserved, live PRSL refused, archives unchanged, workspace restored |
| Seven-byte `Human_Hit_Next_Turn_` getter identified | Historically mapped exact engine | Does NOT submit End Turn; must not be hooked as submit point |
| Manual branch intercept identified at object `0x76D78` | Laboratory-tested candidate | Does not cover automatic caller, keyboard pathways or real runtime |
| 1.50 community network wrapper traced | Laboratory structural evidence | Preserve wrapper/RNG behavior; networked engine execution NOT verified |
| Repeat READY during grace fixed | Historical regression fix | v0.1.0 bug reproducible; corrected in v0.2.0 coordinator tests |
| Live adapter and screen | **Blocked / not implemented** | Neither installed in v0.4.7 nor demonstrated in game |
| Authenticated PRSL networking | **Not implemented** | The native IPX network is not a PRSL coordinator transport |
| Pre-game lobby / new Chat | **Proposed separately** | Not part of the v0.2.0 in-game ready prototype |
| Windows/macOS PRSL acceptance | **Not run** | Python portability does not prove runtime compatibility |

## Version boundary

- **Historical feature source:** PRSL Lab v0.2.0 (October 5, 2026 UTC).
- **Game used for reverse engineering:** fan patch 1.50.26, `ORION150.EXE` SHA-256 `2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c`.
- **Separate manager:** MOO2-SGC Launcher v0.4.7; baseline 1.40b23 and optional 1.50.26 environments; PRSL OFF.
- **Handoff:** `2026-10-07`, documents and original-source import utility, NOT v0.3.0 of the PRSL engine.

## Unresolved items that block a playable release

1. Original v0.2.0 source archive must be imported into this repository without rewriting its history.
2. Source and historical tests must be reviewed and rerun with dependency/toolchain records.
3. A live DOSBox/guest engine adapter must identify the *loaded* binary, phase and safe point.
4. All turn submission paths—including automatic `Do_Begin_Of_Turn_`—must be traced, intercepted or safely constrained.
5. Authenticated epoch-scoped PRSL coordinator and message transport must connect actual clients.
6. Ready/Unready must preserve the living game event loop and native network behavior; release once; UI/state observability must be complete.
7. Real cross-machine MOO2 sessions must demonstrate success and no desync, including failure/reconnect/save cases.
8. Licensing and redistribution review must precede general public software release.

## Evidence location and caveats

Primary technical records: `research/archive-v0.1.0/DESIGN.md` and `research/archive-v0.2.0/{README.md,BINARY_REPORT.md,TEST_METHOD.md,target-map.json,evidence/}`. Archived source archive name: `moo2_prsl_lab_v0.2.0.zip` (47,187 bytes); no SHA-256 could be computed during this handoff because archive raw bytes were inaccessible.

Separate launcher references: `reference/launcher/` — PRSL disabled and signed-updater/network scope concerns; not evidence of playable PRSL.
