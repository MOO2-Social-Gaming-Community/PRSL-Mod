# PRSL previous-work recovery audit — 2026-10-07

## Result

Three **actual original archives were located by title, date, size and Library path** in the user's ChatGPT Library. This improves source discovery, **not source-byte recovery**. Current project file materialization rejected access to the raw ZIP bytes, and direct text-reading of these ZIPs exposed no source. Consequently, **the original v0.2.0 Python/C implementation has NOT been imported** in this package; no source has been fabricated or replaced.

The 2026-10-07 research handoff **is** restored without byte changes. Its 41 tracked file checksums and lengths match its manifest. The original ZIP SHA-256 is `ece9cc49d6705da1fdaa787000643e26d44ae2d07bb7e71c07da155c9aa65647`; the separately stored Library `.sha256` text gives the same digest.

## Located archives — actual Library records, not invented reconstructions

| Library filename | Size | Created (UTC) | Intended use | Raw ZIP bytes here? |
|---|---:|---|---|---|
| `MOO2_PRSL_Research_Design_v0.1.0.zip` | 20,694 B | 2026-10-04 23:07:43 | Original design materials | No |
| `moo2_prsl_lab_v0.1.0.zip` | 13,366 B | 2026-10-04 23:24:49 | Original coordinator, earlier bug state | No |
| **`moo2_prsl_lab_v0.2.0.zip`** | **47,187 B** | **2026-10-05 00:06:57** | **Authoritative lab Python/C source + original regression tests** | **No** |

Location for all three: ChatGPT Library → **`Master of Orion 2`**. The two Lab archives are separate versioned artifacts; importing v0.2.0 does not justify deleting v0.1.0 provenance. The ZIP byte digests cannot be provided without downloading those originals. A companion machine-readable record is in `docs/RECOVERY-ARCHIVES-INDEX.json`.

## Work preserved in this archive right now

The original handoff already contained archival **text renditions** of:

- `research/archive-v0.1.0/DESIGN.md` — design, boundaries, native safety, optional deadline.
- `research/archive-v0.2.0/README.md`, `BINARY_REPORT.md`, `TEST_METHOD.md`, `target-map.json`.
- Five evidence records: `python-tests.log`, `native-probe.log`, `old-coordinator-regression.json`, `installer-verify.json`, `workspace-integration-tests.json`.
- Historical Launcher v0.4.7 integration reference documents in `reference/launcher/`, plus independent PRSL repo architecture, decisions, acceptance tests, roadmap, and the original safe importer.

These are **historical text snapshots, not byte-identical import of the Lab source**. Original Python/C implementation remains absent from `lab/`. The original `HANDOFF-MANIFEST.json` continues to cover its initial files; recovery additions have a separate integrity manifest rather than altering that baseline.

## Prior conversation and project-work decisions recovered

1. The user's feature intent is the **in-game PRSL**, displaying human readiness during a strategic turn and allowing **Ready/Unready before native End Turn**. An optional strategic planning deadline/turn limit is part of the desired design. **Do not relabel this as the pre-game lobby**. The optional new Chat extension is independent.
2. The original engine operation remains authoritative; no reversal after native submission, no rewriting RNG or native IPX, and no intentional ruleset/tactical changes by PRSL. Release exactly once through a fresh verified safe point; track uncertainty after crashes.
3. A narrow versioned adapter recognizes the exact game executable. The analyzed 1.50.26 `ORION150.EXE` identity is SHA-256 `2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c`. Do not use object or file offsets as live guest addresses.
4. `Human_Hit_Next_Turn_` is a **read-only seven-byte finished flag getter**. The proposed manual Next-button interception candidate is code-object offset `0x00076D78` (file offset `0x0010C40C`), but **not** a validated live hook and **not** coverage of the automatic `Do_Begin_Of_Turn_` caller. No stale stack-frame pointer may be replayed.
5. v0.1.0's repeated Ready in grace-state bug is reproducible in the retained regression evidence. v0.2.0's archived test logs record the fix and additional disconnect/fault protection; do not describe those logs as tests rerun now.
6. The MOO2-SGC Launcher, PRSL, optional Chat, future pre-game lobby and SCG Quickplay/Tournament gameplay mods remain distinct responsibility/version boundaries. The launcher v0.4.7 intentionally has **PRSL disabled**.

## What prior archived tests actually proved

The Lab v0.2.0 historical logs recorded **52 Python tests**, **30 synthetic/isolated original x86-instruction checks**, **944 workspace files verified**, and **six offline workspace integration checks**. They do **not** establish DOSBox gameplay, real multiplayer, Windows/macOS gameplay acceptance, or a live adapter. This recovery audit re-runs only the standalone handoff validator/tests; see the local output, which is not archived as v0.2.0 source evidence.

## External GitHub discovery

On 2026-10-07, the public organization `https://github.com/MOO2-Social-Gaming-Community` listed **two visible repositories**: its website and its Launcher/Installer. No **public** standalone PRSL repository or PRSL Lab original-source release was found. This does **not** rule out a private repository or a local clone. Do not import Launcher code into PRSL merely because Launcher references it.

## Finish recovery / source import (blocker: original ZIP bytes)

1. In ChatGPT Library, open **`/Master of Orion 2/moo2_prsl_lab_v0.2.0.zip`**, download its original ZIP, and **attach that ZIP directly to this PRSL conversation**. Alternatively download locally and use the existing repository importer. (Optionally do the same for `moo2_prsl_lab_v0.1.0.zip` and `MOO2_PRSL_Research_Design_v0.1.0.zip` to preserve earlier originals.)
2. First run `python tools/import_original_lab.py --dry-run /path/to/moo2_prsl_lab_v0.2.0.zip` from this repository root. Do not extract the archive unsafely or run its code as part of import.
3. Then run `python tools/import_original_lab.py /path/to/moo2_prsl_lab_v0.2.0.zip`. It creates `lab/` and `lab-import-provenance.json` only after safety checks, refusing overwrites.
4. Review source/licensing. Re-run `python tools/validate_handoff.py` and `python -m unittest discover -s tests -v`, then the separately isolated historical Lab tests (`cd lab; python -m unittest discover -s tests -v`). Exact-engine tests require the user's own matching executable; never commit commercial game files or personal signing keys.
5. Preserve both earlier ZIPs privately as provenance; do not claim v0.2.0's original implementation was recovered until source byte hashes and member imports have been measured.

## Preservation rule

Original documentation, archive contents and file hashes take precedence over recollection. No original Python or C source has been guessed. Do not falsely merge unrelated pre-game lobby code, Chat, or Launcher source into PRSL.
