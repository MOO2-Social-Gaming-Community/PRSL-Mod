# Source inventory, retrieval and provenance

Source discovery date: **2026-10-07**. This document inventories what could actually be retrieved and what remains inaccessible; it is not evidence of newly executed PRSL tests.

## Archival artifacts **present** in this handoff

| New path | Earlier project record | Scope |
|---|---|---|
| `research/archive-v0.1.0/DESIGN.md` | `DESIGN.md` (created 2026-10-04) | Original proposed feature spec, not implementation |
| `research/archive-v0.2.0/README.md` | `README.md` (updated 2026-10-05) | Original Lab v0.2.0 inventory, tests and limits |
| `research/archive-v0.2.0/BINARY_REPORT.md` | `BINARY_REPORT.md` | Exact-hash reverse engineering findings |
| `research/archive-v0.2.0/TEST_METHOD.md` | `TEST_METHOD.md` | Historical test methodology/limitations |
| `research/archive-v0.2.0/target-map.json` | `target-map.json` | Machine-readable exact-build offsets/false capability flags |
| `research/archive-v0.2.0/evidence/python-tests.log` | `python-tests.log` | Earlier 52-test suite output |
| `research/archive-v0.2.0/evidence/native-probe.log` | `native-probe.log` | Earlier 30 isolated native checks |
| `research/archive-v0.2.0/evidence/old-coordinator-regression.json` | Same | v0.1.0 defect reproduction |
| `research/archive-v0.2.0/evidence/installer-verify.json` | Same | Historical 944-file workspace integrity |
| `research/archive-v0.2.0/evidence/workspace-integration-tests.json` | Same | Historical 6 safety scenarios |
| `reference/launcher/REQUIREMENTS-0.1.0.md` | Launcher requirements addendum | Separation of feature and launcher, neutral mod selection |
| `reference/launcher/NETWORK-AND-PROFILES-0.4.7.md` | Launcher 0.4.7 reference | Network plan and disabled PRSL |
| `reference/launcher/TEST-REPORT-0.4.7.md` | Launcher 0.4.7 report | Launcher tests and unverified actual gameplay |

Archival file contents were obtained through the project's text extraction pathway; original line endings, text encoding and final newline bytes may not be identical to original source files. The GitHub handoff copies are readable textual snapshots rather than a claim of byte-faithful preservation. `target-map.json` and evidence JSON can be parsed after normalization.

## Located but **not embedded** original archives

| Prior file | Reported size | Retrieval outcome |
|---|---:|---|
| `MOO2_PRSL_Research_Design_v0.1.0.zip` | 20,694 B | Located in Library; raw bytes unavailable for materialization |
| `moo2_prsl_lab_v0.1.0.zip` | 13,366 B | Located; raw bytes unavailable |
| **`moo2_prsl_lab_v0.2.0.zip`** | **47,187 B** | Located; raw bytes unavailable; this is the required original Python/C source archive |

The parent MOO2-SGC Launcher has separate v0.4.7 repository ZIPs and the licensed user owns game/patch archives. These were **not** copied into this repo. No substitute original-source file was invented.

## External references, distinct from internal evidence

- [MOO2 fan patch landing page](https://www.moo2mod.com/) — supported community patch/version provenance.
- [MOO2 1.50 modding documentation](https://moo2mod.com/doc/150/modding.html) — mod descriptors, `.CFG`/Lua support, not a PRSL hook API.
- [MOO2 1.50 scripting documentation](https://www.moo2mod.com/doc/150/scripting.html) — limited Lua contexts, not proof of pre-turn interception.
- [DOSBox Staging HTTP API documentation](https://www.dosbox-staging.org/0.83/manual/http-api/) — potential research transport, not a certified live hook.

## Research caveats worth keeping visible

- `Human_Hit_Next_Turn_` was a read-only getter, not the native submission site.
- Engine offsets require exact identity and relocation resolution; file offsets are not live memory addresses.
- A second automatic native caller was discovered; the tested early manual gate alone cannot guarantee turn safety.
- Original v0.2.0 reports single-process isolated x86 tests, not DOSBox game or two-player acceptance.
- Original v0.2.0 signed catalog verifier was offline/partial and required an independent trusted key; it was not a production updater.
