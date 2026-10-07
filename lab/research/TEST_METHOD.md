# Test method and evidentiary limits

## A. Python tests — 52 passed

See `evidence/python-tests.log`. The run supplied the pinned owned executable through `MOO2_ENGINE`, so the nine optional structural tests ran rather than being skipped.

Coverage consists of the original ten coordinator tests; eleven coordinator regression/failure tests; eleven package/configuration tests; ten catalog tests; and ten binary tests (including the wrong-binary refusal test).

The old 0.1.0 coordinator bug was also reproduced separately. A fresh-sequence repeated READY during GRACE set `safe_to_commit=False`, but `tick()` still entered COMMITTED. `evidence/old-coordinator-regression.json` records that observed failure. In 0.2.0 repeated READY is idempotent, and commit rechecks readiness, connection, and safety acknowledgements. A disconnect after commitment enters FAULT rather than pretending rollback is safe.

These are in-process coordinator tests, not authenticated network sessions. Turn time limits, input locking, and live adapter observations remain unimplemented.

## B. Original instruction execution — 30 checks passed

See `evidence/native-probe.log` and `tools/native_probe.c`.

No DOSBox, Wine, QEMU, Unicorn, or full game was run. Direct execution of an ELF32 program was unavailable. The working test harness is an ELF64 Linux program that switches temporarily into the CPU's 32-bit compatibility mode, calls narrow regions of the actual game code loaded into private mappings, records results, and returns to 64-bit mode.

Fixtures are generated from the exact-hash owned executable. The mapper reconstructs the two LE objects, applies LE relocations to synthetic addresses, and creates the community extension payload. The actual original extension relocation loop is then executed and compared against an independent Python reconstruction.

The gate experiment runs the original selected event instructions and the original `Do_Next_Turn_` routine body for the tested branch, with these deliberate restrictions:

- A RET at `0x76D9E` ends the harness before the rest of the real input loop.
- A RET at `0x1596F6` ends the isolated relocation-loop experiment; that byte is restored before image comparisons.
- Three external helper entry points (`0x920CD`, `0x10C2F0`, `0x79F8A`) are stubbed with RET. They are not taken as validated display/UI subsystems.
- Synthetic data at `0x21BDD` selects a branch that avoids field/UI allocation against uninitialized game resources.
- Player flags, UI field IDs, game-type values, registers, and caller frames are controlled fixtures, not data captured from a running multiplayer session.
- PRSL permission is a one-shot laboratory mailbox value. It is not an authenticated, epoch-bound production commit message.

Measured properties:

1. Original extension relocation loop matches code/data/extension reconstruction, with balanced stack.
2. Original getter reads eight synthetic slot values without game-data writes and preserves other tested registers/flags. A separate artificial index checks upper-EAX semantics; that index is explicitly not a real player slot.
3. For game-type fixtures 2 and 3, deferral leaves the entire mapped original data object unchanged, preserves general registers/EFLAGS/stack balance, records PRSL intent only, and leaves the caller exit flag and native finished flags unchanged.
4. Clearing laboratory intent models cancellation without game-data writes.
5. Permission resumes original execution; mapped data/register outcomes match the ungated baseline using the same helper stubs. Permission is consumed once; a second event defers.
6. A disabled gate matches baseline, and game-type 0 passes through.
7. The original field-comparison prelude accepts the synthetic Next field, rejects another field, and respects `_skip_fields`.
8. A later release with a different caller frame writes the new local exit flag, not the old one.

**Not measured:** native screen rendering, real input responsiveness, IPX/network progression, combat, next-turn determinism, native save equivalence, multiplayer chat, modal dialogs, guest memory allocation, initialization/configuration-time patches, or any actual two-player game.

## C. Installer / workspace integration

The builder executed against the supplied archives and produced a private test workspace with **944 files**: 816 base entries and 128 community entries. All recorded files verified. No original base file was overwritten by the patch. Both input ZIP hashes were unchanged afterward.

Six additional checks were executed against that real workspace:

- Altering one engine byte causes verification failure.
- A save edit is reported as user data, not destroyed or mistaken for executable corruption.
- PRSL launch is refused.
- Original base archive is unchanged.
- Original patch archive is unchanged.
- Temporary test edits were restored; the workspace verifies again.

`evidence/launcher-host-dry-run.json` contains the generated command/configuration. `executed: false` is intentional. DOSBox was not installed or launched, and no UDP connectivity was proven.

## D. Catalog testing

The signed-catalog verifier uses the installed `cryptography` library's Ed25519 API; tested version is recorded in `requirements-lab.txt`. Tests generate private keys in memory and do not publish them. Checks cover valid and invalid signatures, different keys, expiry, rollback relative to caller-provided trusted state, payload limits, invalid metadata, and the distinction between a signed record and locally supported/certified code.

This is not a deployed auto-updater. Trust-anchor provisioning, key rotation, durable trusted metadata, HTTPS downloads, scheduler behavior, multi-process activation, full repair/rollback, and GUI integration remain work to do. Production update security requires more than one signature check; see https://theupdateframework.io/docs/security/.

## E. Reproduction and negative reporting

The source package excludes all user-owned binaries and reconstructed images. Reproduction requires the exact source archives/executable. Unknown hashes are refused. On an unsupported CPU, operating system, or kernel, the native probe can fail or be unavailable; it must not be reported as a passing game test.

The final logs report only successful final runs. During development, the C harness initially failed compilation due to missing spaces after a hexadecimal literal ending in `e`; that syntax error was corrected before execution. No failed full-game tests are hidden: no full game could be started in this environment.
