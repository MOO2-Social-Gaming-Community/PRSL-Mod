# PRSL research and development history

**Method:** Reconstruction from historical PRSL documents, archived evidence files, and subsequent launcher and community requirements. This is **not** a reconstructed Git commit history. Dates reflect original document timestamps or decisions as recorded; uncertain milestones are not invented.

## 2026-10-04 — Proposed product and integration research (v0.1.0)

The [original design](../research/archive-v0.1.0/DESIGN.md) specified a reversible **in-game** player readiness stage before MOO2's native strategic End Turn. It proposed:

- roster of active human participants and Ready/Unready controls;
- a turn/epoch coordinator and optional strategic planning timer;
- a narrow `EngineAdapter` boundary, native path preservation and exact-build validation;
- clean game imports, signed package checks, separate writable workspaces and explicit version lockfiles;
- separate control transport versus native DOSBox IPX;
- original post-submission chat untouched, future pre-submission/companion Chat optional.

At this stage **hooks were not proven**. The first research also proposed reviewing a community-reported alternative native/source engine; that report was **not independently established as a compatible backend**.

## 2026-10-04 → 2026-10-05 — PRSL Lab 0.1.0 → 0.2.0

An original coordinator prototype existed in 0.1.0. The subsequent testing isolated a repeated READY (higher sequence) during the GRACE stage that invalidated the safety acknowledgement but still allowed a transition to COMMITTED. This was a **real regression in a simulated state machine**, not observed in a live MOO2 match. v0.2.0 fixed repeated READY idempotence and strengthened commitment checks and disconnect/fault handling. See [old regression JSON](../research/archive-v0.2.0/evidence/old-coordinator-regression.json), [test method](../research/archive-v0.2.0/TEST_METHOD.md).

The research team inspected an exact 1.50.26 `ORION150.EXE` and reconstructed the bound DOS LE executable objects and relocation behavior. Significant technical outcomes:

1. The named `Human_Hit_Next_Turn_` is a 7-byte **read-only getter**, not a suitable submission hook.
2. A 5-byte CALL at code-object + `0x00076D78` was identified and laboratory-tested as an early **manual Next-button** interception candidate.
3. `Do_Next_Turn_` is called from more than one path, including an automatic turn-start path. Its caller-owned stack-local pointer must not be cached for delayed submission.
4. The existing 1.50 network wrapper preserves an RNG snapshot and must not be bypassed by PRSL.
5. The native done flag is written inside `Net_Next_Turn_`; interception that late is unsafe for a reversible ready stage.

Historical evidence recorded 52 Python tests, 30 native-compatibility-mode instruction checks, and real input-archive workspace verification (944 files; six additional checks). All these were **laboratory/offline**. Neither DOSBox nor the full game ran under the original v0.2.0 test environment. Refer to [binary report](../research/archive-v0.2.0/BINARY_REPORT.md).

The complete Python/C source was packaged as `moo2_prsl_lab_v0.2.0.zip` and remains the **authoritative original implementation artifact**. Its raw bytes are not inside this handoff. See [source import instructions](ORIGINAL-SOURCE-IMPORT.md).

## 2026-10-05 — Launcher boundary clarified

The accepted launcher [requirements addendum](../reference/launcher/REQUIREMENTS-0.1.0.md) clarified that the environment manager is neutral: PRSL, future Chat, vanilla/community patch, rulesets and community add-ons are optional independent components. Four combinations — neither, PRSL alone, Chat alone, and both — should eventually work where supported. Dependency resolution cannot secretly activate PRSL. A shared integration service may be used, but overlapping native instruction hooks require one verified dispatcher.

The addendum still described **unimplemented** profile selection, general mod resolver, Chat and live PRSL integration at that moment. Later launcher development is separate from PRSL's version line.

## 2026-10-05 → 2026-10-07 — Separate launcher v0.4.x

The launcher advanced through installation, independent game environments, profile management, RKERNEL/kernel verification and DOSBox IPX diagnostics. The 0.4.7 launcher reference describes 1.40b23 baseline and independently selected 1.50.26 Community, with `IPXNET CONNECT moo2.thedopefish.com 213` as one public relay network plan.

The launcher **does not enable PRSL**. The 0.4.7 test report explicitly withholds live multiplayer and Windows/game acceptance. Its Dopefish connection diagnostic is not an end-to-end game test and does not implement a PRSL control channel. See [0.4.7 network reference](../reference/launcher/NETWORK-AND-PROFILES-0.4.7.md).

## 2026-10-07 — Repository separation and community roadmap

The project's chosen role split is:

- **Launcher/Installer:** canonical environment preparation and orchestration, separate repo.
- **PRSL:** upstream-friendly optional in-game readiness and shared integration research, separate repo; a future pre-game lobby could integrate but does not define PRSL's original mechanism.
- **Future Chat:** optional messaging/UI feature that does **not** depend on PRSL.
- **SCG Quickplay:** separate strategic/non-tactical, streamlined gameplay for meetups.
- **Tournament Mod:** separate competitive balance and tactical/manual design gameplay.

These are project intentions, not already deployed mods. The 2026-10-07 handoff preserves PRSL history and moves toward a sustainable repository boundary without claiming new game integration.

## Why this chronology matters

The documented *research* is not a replacement for the missing original source, and the launcher’s increasingly capable multiplayer setup must not be misreported as PRSL activation. The next milestone is **live end-turn barrier proof**, not more UI presentation or a generalized plugin framework.
