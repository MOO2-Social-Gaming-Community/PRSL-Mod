# MOO2 PRSL Lab 0.2.0

**Status: exact-build reverse engineering, an isolated x86 gate experiment, and a working offline environment-manager prototype. Not a playable PRSL mod.**

This release continues the 0.1.0 coordinator work. It maps the supplied `ORION150.EXE` from patch 1.50.26, tests a narrowly scoped interception boundary using actual original 32-bit instructions, and connects the research metadata to a fail-closed installer/launcher prototype.

## Main result

`Human_Hit_Next_Turn_` is a **seven-byte read-only finished-turn flag getter**, not the function that submits a turn. It must not be replaced with the pre-ready coordinator.

The better **manual-input candidate** is code-object offset `0x00076D78`, file offset `0x0010C40C`: the call to `Assert_Settings_` immediately before the main-screen Next-button branch begins writing native turn/UI flags. Deferral skips to `0x00076D9E`; permission executes the original call and resumes at `0x00076D7D`.

These are **object/file offsets, not DOSBox runtime memory addresses**. The candidate is not certified across all input paths, initialization states, configurations, or full games. A second automatic path calls `Do_Next_Turn_` independently and is not covered by this gate.

## Evidence collected

| Work | Result | Scope |
|---|---|---|
| Python tests | 52 passed | Coordinator, exact-binary structure, extraction/configuration safety, signed-catalog verification |
| Actual x86 instruction checks | 30 passed | Original loader relocation loop, flag getter, manual event prelude, laboratory defer/release gate |
| Fresh owned-file installation | 944 files verified | 816 original archive files plus 128 community-patch files |
| Original files changed by overlay | 0 | Hash comparison against this supplied baseline, not a universal stock-media certification |
| Workspace integration checks | 6 passed | Corruption refusal, save-edit preservation, PRSL launch refusal, unchanged archives, restored workspace |
| Full DOSBox/game execution | **Not run** | No runnable DOSBox available in this environment; attempts to obtain a Linux runtime failed |
| Two-player IPX session / native turn advancement | **Not run** | Not established by the isolated instruction checks |
| Windows/macOS acceptance | **Not run** | Python code is intended to be portable; only Linux was exercised |

Read [the binary research report](research/BINARY_REPORT.md), [the test methodology](research/TEST_METHOD.md), and [the continuation plan](NEXT_STEPS.md).

## Package contents

- `prsl/binary150.py`: exact-hash LE/debug-record/extension-relocation reader.
- `prsl/lab_gate.py`: x86 emitter for the **synthetic laboratory address space only**.
- `tools/native_probe.c`: executes selected original instructions in x86-64 compatibility mode.
- `tools/run_native_probe.py`: builds private temporary fixtures from the user's executable, compiles the C harness, runs it, then removes the fixtures.
- `prsl/state.py`: independent coordinator; fixes the 0.1.0 duplicate-Ready safety bug and adds disconnect/fault handling.
- `prsl/packages.py` / `prsl/cli.py`: pinned owned-archive import, staging, file verification, community launch configuration, and fail-closed PRSL capability checks.
- `prsl/updates.py`: **offline signature/freshness/eligibility checks**, not a network auto-updater.
- `research/target-map.json`: machine-readable evidence and unsupported capability flags.
- `evidence/`: actual test logs and installation results. Paths in logs identify the Linux test workspace and are not portable defaults.

No original game binaries, assets, community-patch binaries, DOSBox runtime, credentials, or private signing keys are distributed in this package. No game executable was modified in the source archives. All machine-code experiments used disposable relocated copies.

## Quick start

Python **3.11 or newer** is needed. `requirements-lab.txt` records the cryptography version used for signed-catalog tests; the mapper, coordinator, and installer otherwise use the Python standard library. The native instruction probe additionally requires Linux x86-64 with compatibility-mode support and GCC. It does not run on macOS or Windows as written.

From this directory:

```sh
python -m pip install -r requirements-lab.txt
python -m unittest discover -s tests -v
```

Without `MOO2_ENGINE`, nine owned-executable structural tests are explicitly skipped. For the complete 52-test run on a POSIX shell:

```sh
MOO2_ENGINE="/path/to/ORION150.EXE" python -m unittest discover -s tests -v
PYTHONPATH=. python tools/run_native_probe.py "/path/to/ORION150.EXE"
```

Inspect or create a fresh owned-file workspace:

```sh
python -m prsl.cli inspect "/path/to/ORION150.EXE"
python -m prsl.cli build --base "/path/to/Master of Orion 2.zip" --patch "/path/to/MOO2-1.50.26.zip" --out "./workspaces/session-a"
python -m prsl.cli verify "./workspaces/session-a"
```

This importer deliberately recognizes **only the exact two supplied archives**. Other editions, re-zipped installations, languages, and patch versions need explicit support; they are not silently treated as equivalent.

Generate a host launch command and configuration without executing anything:

```sh
python -m prsl.cli launch "./workspaces/session-a" --dosbox "/path/to/dosbox" --role host
```

For a joiner, use `--role join --host 192.168.1.2`. Supplying `--execute` launches **unmodified community mode** through the DOSBox executable you provide. Actual emulator/game launching has not been validated here. `--mode prsl` always refuses: neither a manifest edit nor a signed catalog can enable the unfinished live adapter.

Build separate destinations for separate clients. Do not run two games against one writable workspace. The CLI does not replace or repair an existing workspace, migrate saves, download DOSBox, configure a firewall, provide discovery, or automatically switch versions.

## Updater boundary

`catalog-check` verifies a separately obtained signed envelope against a **trusted local 32-byte Ed25519 public key** and a supplied highest-observed catalog revision. It does not download, install, persist trusted state, rotate keys, or schedule anything.

```sh
python -m prsl.cli catalog-check catalog-envelope.json --trusted-key trusted-public-key.bin --highest-revision 3
```

The test suite creates ephemeral signing keys in memory. There is no production catalog/key. Do not obtain the trust anchor from the same untrusted envelope. Do not describe this primitive as a complete TUF implementation or a production-secure auto-updater.

## Distribution / authorship

The new laboratory code is provided as project working material for Psyche42's PRSL work. No upstream ownership or license transfer is asserted. Decide the project's license before public distribution. Retain upstream notices and review redistribution terms before bundling any third-party runtime or patch. This package is not an official MOO2 community release.