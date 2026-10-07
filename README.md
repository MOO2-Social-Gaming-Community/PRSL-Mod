# MOO2-SGC Pre-Ready-State Layer (PRSL)

**An independent research-stage multiplayer quality-of-life extension for Master of Orion II.**

> **Status — pre-alpha research handoff, 7 October 2026:** The latest located PRSL prototype is **PRSL Lab v0.2.0** (5 October 2026 UTC). Its offline coordinator, exact-build binary analysis, laboratory x86 interception experiment, and installer prototype have recorded tests. **No live in-game PRSL adapter, playable Ready/Unready barrier, or verified two-player session exists.** PRSL remains **disabled** in the separate MOO2-SGC Launcher v0.4.7. Do **not** advertise or distribute this as a working game mod.

PRSL's original, precise feature is **reversible readiness during an active strategic turn**: a player may mark Ready without immediately submitting the native End Turn operation; Unready returns to planning; when the agreed session conditions are satisfied, each compatible client safely invokes its **original** engine path exactly once. Native turn processing, saves, RNG rules, and network protocol must remain intact. This is **not** the same feature as a **pre-game lobby** or an optional **Chat extension**. The larger MOO2-SGC plan also contemplates those, but they are separately scoped and not implemented by this prototype.

## Why this repository exists

MOO2-SGC's launcher/installer, website, PRSL, community quickplay mod, and competitive Tournament Mod have distinct responsibilities and development lifecycles. PRSL should be independently testable, versioned, and optional. Long-term adoption by fan-patch maintainers is a goal, **not an agreement or established fact**.

## Current evidence in one view

| Component / claim | State on 2026-10-07 |
|---|---|
| PRSL state coordinator | **Offline prototype in original v0.2.0 source archive**; readiness and safety regression tests historically passed |
| Binary mapping of `ORION150.EXE` 1.50.26 | **Exact-build research recorded**; identity hash and offsets documented |
| x86 manual-button interception | **Isolated laboratory experiment**; not injected into a running DOS game |
| Packaging / workspace / signed catalog checks | **Research prototype**; no production network updater |
| In-game UI, networked coordinator, safe live adapter | **Not implemented / not validated** |
| Pre-game lobby and new Chat | **Future infrastructure / independent feature**, not demonstrated |
| MOO2-SGC Launcher v0.4.7 integration | PRSL disabled; launcher may run an ordinary 1.50.26 game without PRSL |

See [verified status](docs/STATUS.md), [research history](docs/RD-HISTORY.md), [engine findings](docs/ENGINE-RESEARCH.md), and [next engineering work](docs/ROADMAP.md).

## Important: original source ZIP must be imported

**This GitHub handoff contains the original research documents and test evidence, but not the original Python/C files.** The archived source **`moo2_prsl_lab_v0.2.0.zip`** was located in earlier project files (47,187 bytes), but its raw ZIP bytes could not be copied into this handoff environment. We have **not** invented replacement source and called it the original.

1. Retrieve the original **`moo2_prsl_lab_v0.2.0.zip`** from the project's earlier conversation/Library files.
2. Extract *this handoff ZIP* into your new PRSL repository (preserve `.git` if already cloned).
3. With Python 3.11+ and the original ZIP available locally, run:

   ```powershell
   py -3 tools/import_original_lab.py "C:\path\to\moo2_prsl_lab_v0.2.0.zip"
   ```

   POSIX equivalent: `python3 tools/import_original_lab.py /path/to/moo2_prsl_lab_v0.2.0.zip`.
4. Review `lab/` and `lab-import-provenance.json` before committing. The importer **fails closed** on suspicious archive members, does not overwrite an existing `lab/`, and does not run imported programs.
5. To reproduce the **historical unit tests** after importing, install `lab/requirements-lab.txt` if present and run `cd lab; python -m unittest discover -s tests -v`. Tests needing the user-owned exact executable may skip unless `MOO2_ENGINE` is supplied. Do **not** interpret passing Python tests as live multiplayer acceptance.

[Original-source import procedure](docs/ORIGINAL-SOURCE-IMPORT.md) explains the complete process and restrictions.

## Repository contents

```text
README.md                        Project description and status
STATUS.md                        One-page release/readiness notice
CHANGELOG.md                     Dated handoff history
LICENSE-STATUS.md                Licensing decision needed before public code reuse
CONTRIBUTING.md                  Development workflow, source integrity, tests
SECURITY.md                      Security/reporting and distribution boundaries
docs/                            Architecture, findings, test plan, roadmap, handoff
research/archive-v0.1.0/         Retrieved original design text
research/archive-v0.2.0/         Retrieved research report, exact target map, test logs
reference/launcher/              Historical launcher interoperability documents
tools/import_original_lab.py     Safe importer for the ORIGINAL lab source ZIP
tools/validate_handoff.py        Documentation/package self-check
tests/                           Tests for new handoff tooling
lab/                             CREATED BY IMPORTER; original v0.2.0 code, absent initially
```

The `research/archive-*` files are preserved **text renditions** of earlier project files; platform newline normalization may differ from original bytes. They are **not** fabricated test runs performed for this handoff. The launcher documents under `reference/launcher` are historical references, not source code that PRSL now owns.

## Ground rules

- **Keep commercial MOO2 game binaries, paid assets, personal savegames, patch ZIPs and private keys out of Git**. Require legitimate source game media and respect community patch distribution rights.
- Match exact engine identities before attempting native patching. The recorded 1.50.26 executable hash is in [ENGINE-RESEARCH](docs/ENGINE-RESEARCH.md); do **not** apply recorded file offsets to runtime memory.
- Do not turn on PRSL merely by editing a manifest or UI switch. Unknown builds/unfinished adapters must fail closed.
- Preserve the unmodified 1.50.26 game path, patch load behavior, the native turn path and the original native chat.
- Keep optional Chat and future pre-game lobby behavior separate. PRSL should work without either.
- Prefer generic, upstream-friendly hooks where supported; ask maintainers rather than assuming acceptance.

## Related MOO2-SGC work

- [MOO2-SGC Launcher and Installer](https://github.com/MOO2-Social-Gaming-Community/MOO2-SGC---Launcher-and-Installer) — separately maintained runtime/installer; URL from the project's documented infrastructure, **not validated as an available repo in this handoff**.
- [MOO2 patch 1.50 project](https://www.moo2mod.com/) — independent community patch maintained by third parties; not affiliated with or endorsed by this PRSL repository.
- SCG Quickplay Mod — future gameplay mod with strategic/non-tactical combat.
- Tournament Mod — future tactical-play balancing mod; independent of PRSL.

## Development entrance

Start with [docs/ROADMAP.md](docs/ROADMAP.md), then [docs/ACCEPTANCE-TESTS.md](docs/ACCEPTANCE-TESTS.md). **First meaningful playable milestone:** two legitimate game clients, both in a real native strategic turn, where Ready defers native submission, Unready cancels it, and all-ready releases one native turn without desynchronization. Until then, the code is a research laboratory, not an installed multiplayer feature.
