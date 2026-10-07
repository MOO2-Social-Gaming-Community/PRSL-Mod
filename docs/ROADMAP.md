# PRSL continuation roadmap — prioritized engineering plan

The goal is **a safe, community-acceptable optional enhancement**, not a rushed invasive executable patch. Confidence claims rise only when appropriate tests have passed. The project author intends to continue PRSL work after the October 2026 India trip; no in-person community launch or tournament depends on completing the PRSL adapter immediately.

## P0 — Preserve existing R&D (first next commit)

- Obtain `moo2_prsl_lab_v0.2.0.zip` from the original project Library files and run `tools/import_original_lab.py`.
- Verify `lab/prsl/state.py`, `lab/prsl/binary150.py`, `lab/prsl/lab_gate.py`, `lab/prsl/packages.py`, `lab/prsl/cli.py`, `lab/prsl/updates.py`, `lab/tools/native_probe.c`, `lab/tools/run_native_probe.py`, `lab/tests/`, plus original README/research/evidence.
- Review imported ZIP members and provenance; do not copy owned engine, patches, keys or commercial assets. Choose repository license after author/provenance review.
- Run the existing suite without `MOO2_ENGINE` (optional exact-structural tests should skip); then with a legitimate exact engine on an isolated local machine. Keep raw logs under private test output and publish redacted reports only.
- Baseline the source verbatim in a commit, tag the *historical lab* appropriately (for example `lab-v0.2.0-imported`), and open the issues listed below. Do **not** name the handoff `v0.3.0`.

**Exit:** reproducible source tree, provenance, tests reported accurately, no released live mod.

## P1 — Safe live observation, **read-only** (first technical milestone)

- Map the exact executable as DOSBox actually loads it; resolve relocations and initializer modifications, not only file offsets.
- Build read-only observation of strategic-turn phase, active-human roster, local slot, current UI/modal state, native submission, screen changes.
- Trace all End Turn entry paths and distinguish manual mouse, hotkey, automatic paths, save/load, combat modes and edge screens.
- Test under owned 1.50.26 with the original game unchanged; provide an exact-hash reject path and no exposure of memory-control endpoints beyond loopback.

**Exit:** noninvasive traces on a real game, no altered turns, no kernel/network regressions.

## P2 — Disposable guest hook prototype, single process

- Experiment at the laboratory manual-event candidate after verifying loaded code identity and lifetime. Preserve instructions/registers/flags/stack and all native 1.50 wrapper behavior.
- Add reentrancy/epoch guard and an **external intent** record; never park a native stack frame or retain an EAX pointer to caller locals.
- Arrange native release at a fresh verified event-loop safe point, not by jumping into the engine from an arbitrary host timer.
- Handle / block the automatic `Do_Begin_Of_Turn_` path; test disabled mode, game abort, save, reload and normal end turn before adding PRSL transport.
- Keep injection entirely inside a disposable managed game workspace, with deterministic uninstall/recovery and hash guards; never change an owned source install.

**Exit:** one local game can Ready (native turn not submitted), Unready, and release a native turn once without altering unmodded behavior; repeatable logs.

## P3 — Authenticated multiplayer barrier (real core proof)

- Implement coherent client membership, epochs, barriers, Ready/Unready sequence/idempotence, commit grants and status observation. Reuse original coordinator where correct; add a minimally scoped protocol only after tests.
- Lock session engine/profile/mod versions; mismatches stop before connection/launch.
- Add control-transport authentication and coordinator failure/reconnect policy **separate from game IPX**.
- Run real local two-client MOO2 matches (same engine, independent writable workspaces), intentionally varying turn order, network delays, duplicates, out-of-order messages, disconnects and save/reload.
- Exercise both host and client roles, then more players if needed; do not claim success until in-game next turn and state parity are observed.

**Exit:** 2/2 players can mark Ready/Unready and release exactly one verified native turn without desync, across repeated tests and negative cases.

## P4 — User experience and supportability

- Readiness UI and clear errors/timeouts/status, full-screen-safe, with input lock during pre-ready and one-click Unready.
- Reconnect and recovery information, log export, no private path/token leaks, failure escalation.
- Separate launcher package with signed versioned exact-engine compatibility metadata and integration hooks; retain regular 1.50 profile.
- Windows 11 + supported Linux/Mac acceptance only on real test machines, not just cross-compilation.
- Consider an advisory-only overlay for social play **clearly labeled as advisory**, but don't confuse it with safe engine integration.

**Exit:** credible limited closed-alpha release with exact supported tuples and rollback instructions.

## P5 — Upstream collaboration and optional surrounding services

- Present small generic hook proposals, verified call graphs and failure tests to 1.50 maintainers. Acceptance is aspirational.
- Build a separate pre-game lobby/roster/readiness display only where it serves real host/join onboarding. Its UI can be shared with PRSL without merging responsibilities.
- Optional Chat module can use shared authentication/participant status but must work with PRSL disabled; preserve native chat.
- Later broaden engine versions, operating systems and community mod combinations **one tested tuple at a time**.

**Exit:** maintainable integration with a documented compatibility matrix and independent release histories.

## Avoid premature work

- No large plugin SDK before two features truly share stable capabilities.
- No randomized binary scanning or generic unknown-build injection.
- No direct use of file offsets as live addresses.
- No assumption that the public IPX relay also hosts PRSL coordinator traffic.
- No proprietary game-file bundles in repository, test fixtures or releases.
- No marketing claims of a functioning PRSL until a full multiplayer barrier is verified.
