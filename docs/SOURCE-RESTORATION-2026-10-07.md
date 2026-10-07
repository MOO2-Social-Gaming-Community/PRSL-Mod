# MOO2-SGC PRSL — authenticated source-recovery and validation record

**Date:** October 7, 2026. **Target repository:** `https://github.com/MOO2-Social-Gaming-Community/PRSL-Mod`. This repository package was generated locally for user review and manual publication; **no authenticated GitHub push or remote repository audit was performed**.

## Archive import and custody

The user supplied `moo2_prsl_lab_v0.2.0(1).zip` directly as a conversation upload. The `(1)` is an upload filename suffix; the archive's internal root is `moo2_prsl_lab_v0.2.0/`.

| Measured property | Value |
|---|---|
| Original ZIP bytes | 47,187 |
| ZIP SHA-256 | `2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e` |
| Internal source archive members | 31 |
| Total uncompressed source bytes | 112,327 |
| Imported project tree | `lab/` |
| Import method | Existing `tools/import_original_lab.py` first in dry-run then real import; no overwrites |
| Whole-file archive member verification | **31/31 byte-for-byte exact** |
| Original source hash manifest | `lab/SOURCE_SHA256SUMS.txt` lists the other 30 files; separately pinned by new verification tool |
| Import metadata | `lab-import-provenance.json` |

Original source is **never edited or reimplemented** by this recovery. The ZIP is intentionally excluded from repository contents to avoid duplicating archival binaries. `tools/verify_lab_provenance.py` refuses changed, missing or extra historical Lab files; future development belongs outside `lab/`.

## Tests performed in this session

| Validation | Observed outcome | Scope |
|---|---|---|
| Repository research checker | Pass | 26 required handoff research artifacts and conservative capability flags |
| Original importer/security regression suite | **11 passed** | ZIP/path/traversal/overwrite safety and docs validator |
| Added repository provenance regression tests | **6 passed** | Detects altered/removed/extra original files, forged provenance and altered hash list; **17 total** repository tests |
| Lab original Python suite | **52 run, 43 passed, 9 skipped** | Coordinator, package security, offline catalog, binary parse refusal; engine-specific tests skipped without `MOO2_ENGINE` |
| Extracted-original byte comparison | **31/31 equal** | Local ZIP content vs imported files |
| Original per-source hash manifest | Verified separately by `tools/verify_lab_provenance.py` | Source preservation only |
| Native x86 instruction probe | **Not rerun** | Historical Lab log recorded 30 passes, isolated x86 compatibility mode—not game |
| Native DOSBox gameplay, 1.50.26 loaded-engine, two-client IPX | **Not run** | No game executable or DOSBox runtime supplied |

Interpreter for original Lab suite: CPython **3.13.5** on **Linux**, `cryptography` **46.0.4**. `lab/requirements-lab.txt` pins cryptography to that version. The nine optional engine tests are expected skips, **not passes**. See `evidence/source-restoration-2026-10-07/` for contemporaneous logs.

## What was actually recovered

- Offline Ready/Unready coordinator and its behavior/regression tests.
- Exact-1.50.26 binary parser and candidate hook research; **not** a live injection.
- Synthetic/isolated native x86 gate emitter and earlier C probe source.
- Offline game workspace, configuration and Ed25519 signed-catalog research utilities (not a production updater).
- Original README, chronology, evidence and research map including unsafe/unsupported capability flags.

## Requirements and work remaining

A correct PRSL must defer MOO2's native End Turn while allowing Unready; observe a validated planning phase and active humans; synchronize authenticated epoch-bound Ready state between real clients; then release native End Turn **once** at a known safe point without bypassing the community 1.50 networking/RNG path. The historical mapped getter is not a submit hook; the candidate manual-button intercept does not cover the automatic caller. No live adapter, game UI, coordinated transport, timing controller, save-recovery or actual two-client integration has been demonstrated.

First next gate is **read-only observation against a legitimate, exact-hash 1.50.26 engine** in a disposable DOSBox workspace, with explicit coverage of all End Turn entry paths. PRSL remains off in the Launcher v0.4.7. Do not publish a binary PRSL mod until native and multiplayer acceptance criteria in `docs/ACCEPTANCE-TESTS.md` are satisfied.

## Relationship to earlier packages

The October 7 research handoff ZIP has SHA-256 `ece9cc49d6705da1fdaa787000643e26d44ae2d07bb7e71c07da155c9aa65647`. Before the direct source upload, a separate recovery audit could locate the original ZIP's Library record but could not obtain its bytes. Those now-outdated audit notes and the old checksum manifests are retained unmodified in `provenance/2026-10-07-before-source-import/`, not represented as current status.

Historical source v0.2.0 is now present in `lab/`; this recovery **does not** claim a new PRSL version 0.3.0, finished mod, license approval, GitHub commit, or upstream 1.50 endorsement.
