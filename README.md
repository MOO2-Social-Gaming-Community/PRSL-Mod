# MOO2-SGC — Pre-Ready State Layer (PRSL)

**Independent, optional, research-stage in-game readiness mod for Master of Orion II.**

> **Current state — 7 October 2026: Original PRSL Lab v0.2.0 source recovered and imported. Not playable.** This repository contains the original coordinator, exact-build mapping, isolated x86 experiments, offline workspace tools, test suite and research documents. **No live in-game PRSL adapter is installed or certified.** There is no verified Ready/Unready hook, game UI, authenticated multiplayer control transport, or two-client PRSL session. PRSL is **not enabled** by the separate MOO2-SGC Launcher.

Canonical project repository: [MOO2-Social-Gaming-Community/PRSL-Mod](https://github.com/MOO2-Social-Gaming-Community/PRSL-Mod). This ZIP is a repository *file snapshot*, not a Git commit or proof it was pushed to GitHub.

## What PRSL is

During a real strategic planning turn, each participant should be able to **Ready** and **Unready** without submitting MOO2's native End Turn. Once the agreed, authenticated readiness conditions are met, each client should safely invoke its **original** native End Turn path **exactly once**, preserving the game's turn computation, 1.50 network/RNG wrapper and save behavior. Optional planning deadlines are a design goal, not a tested feature.

PRSL is **not** a pre-game lobby, a new Chat extension, or the SCG Quickplay/Tournament gameplay mod. Those are separate components and release tracks.

## Recovered baseline

| Area | Verifiable state |
|---|---|
| Original Lab v0.2.0 source | **Imported:** 31 original ZIP files, byte-for-byte verified, in `lab/` |
| Original archive identity | 47,187 bytes; SHA-256 `2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e` |
| Offline Python Lab tests | **52 run, 43 passed, 9 skipped** (matching user-owned engine not supplied); executed 2026-10-07 on Linux, Python 3.13.5 |
| Handoff importer tests | **17 passed** (11 original importer tests + 6 provenance tests); original import tooling preserved |
| Lab native-instruction probe | **Historical 30 isolated checks**, not rerun here and not in-game |
| Live engine adapter / game UI / coordinator networking | **Not implemented or not validated**; no playable PRSL |

The source has not been edited; follow-on engine/protocol code should be developed separately while keeping `lab/` immutable. See [restoration evidence](docs/SOURCE-RESTORATION-2026-10-07.md) and [full status](docs/STATUS.md).

## Repo layout

```text
lab/                             Exact recovered PRSL Lab v0.2.0 source, tests, research
lab-import-provenance.json       Archive hash, import counts and source metadata
research/                        Older design, engine research and historical logs
reference/launcher/              Read-only launcher interoperability records
provenance/                      Superseded pre-import manifests/audits
tools/verify_lab_provenance.py    Verify historical source is unchanged
tools/import_original_lab.py     Safe importer for rebuilding FROM an earlier handoff
tools/validate_handoff.py        Archived research and handoff validation
tests/                           Repository/installer/provenance tests
docs/                            Architecture, risks, evidence, roadmap, test strategy
```

## Run the available tests (no commercial game files needed)

Python 3.11+ is required; the Lab's signature-verification tests additionally need the dependency pinned in `lab/requirements-lab.txt`.

```bash
python -m pip install -r lab/requirements-lab.txt
python tools/verify_lab_provenance.py
python tools/validate_handoff.py
python -m unittest discover -s tests -v
cd lab
python -m unittest discover -s tests -v
```

Nine Lab structural tests deliberately skip without **your own licensed, exact-hash** `ORION150.EXE` supplied as `MOO2_ENGINE`. The Lab reports a research identity of SHA-256 `2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c` (1.50.26). Never upload game/patch archives, saves or signing keys to GitHub or CI. `tools/native_probe.c` requires a separate Linux compatibility-mode setup and does not demonstrate running MOO2.

**Passing these tests does not demonstrate a working in-game mod.** The Lab's `--mode prsl` intentionally refuses launch until a certified adapter exists.

## Source integrity and development

The uploaded ZIP was imported through `tools/import_original_lab.py` into `lab/`, including `lab/SOURCE_SHA256SUMS.txt`. All 31 source members matched the original archived bytes; `tools/verify_lab_provenance.py` checks the 30 listed members and pins the source-manifest identity. The ZIP itself is intentionally **not** committed into this repository.

- [Restoration record and current evidence](docs/SOURCE-RESTORATION-2026-10-07.md)
- [Architecture and separation of responsibilities](docs/ARCHITECTURE.md)
- [Exact-engine research and limitations](docs/ENGINE-RESEARCH.md)
- [Roadmap and next milestone](docs/ROADMAP.md)
- [Acceptance tests](docs/ACCEPTANCE-TESTS.md)
- [Contributing](CONTRIBUTING.md) and [licensing review](LICENSE-STATUS.md)

**Next milestone:** read-only trace of the *loaded* 1.50.26 engine and every native End Turn pathway in a disposable owned workspace, before any live interception. No generic offsets, unknown-build injection, or native callback blocking. A safe 2-client Ready/Unready barrier remains a later milestone.

This is independent MOO2-SGC community research, not an official MOO2 patch or an upstream-approved modification. Public redistribution/reuse licensing still needs a project decision.
