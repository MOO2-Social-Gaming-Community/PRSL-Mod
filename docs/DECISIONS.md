# Architecture decisions / open questions

These records preserve what the MOO2-SGC project has chosen versus what remains exploratory.

## D-001 — PRSL is an independent optional feature (accepted)

**Decision:** keep PRSL separately versioned from launcher and gameplay mods. Launcher can install, select and configure it only once certified. Installing PRSL cannot silently turn it on. Disabling PRSL must leave the native game available. **Reason:** upstream-friendly interoperability and minimal changes to core game.

## D-002 — Native End Turn remains authoritative (accepted)

**Decision:** PRSL intercepts pre-submission intent but must ultimately schedule MOO2's original End Turn processing, preserve RNG/network wrapper and observe actual submission. **Reason:** minimize desynchronization and unexpected gameplay behavior.

## D-003 — No generic unknown-build binary patch (accepted)

**Decision:** exact engine identity; candidate hook only for tested build and with verified relocation/loaded code. **Reason:** old 0.2.0 research showed why name-based hooking and naive offsets were unsafe.

## D-004 — Separate Chat and future lobby from PRSL semantics (accepted direction)

**Decision:** original turn Ready/Unready is PRSL. Optional Chat may be a separate module/tab. Pre-game lobby is shared setup infrastructure and must not be misrepresented as engine-intercepting PRSL. Both can share narrowly defined transport/authentication and UI capabilities in the future.

## D-005 — Source-first community collaboration (accepted goal, not upstream commitment)

**Decision:** offer generic hooks/validated adapter contracts to the established 1.50 fan-patch community if maintainers want them. **Reason:** long-term durability. **Status:** no endorsement/adoption identified.

## D-006 — Distinct gameplay projects (accepted)

**Decision:** SCG Quickplay is an optional fast non-tactical gameplay mod; Tournament Mod is competitive tactical balance with manual design. Neither belongs in PRSL, and neither should be required for basic readiness infrastructure.

## D-007 — PRSL transport endpoint and host policy (open)

**Question:** LAN-only coordinator first, shared relay, companion app service or integrated engine? Requires NAT security/reconnect design. Do not assume `moo2.thedopefish.com` offers a PRSL control service.

## D-008 — UI integration (open)

**Question:** local companion window vs in-game overlay vs extension tab. User experience must be clear, but verify game UI/input implications before commitment. Chat must remain optional.

## D-009 — Original source archive merge (accepted and completed 2026-10-07)

**Decision:** preserve v0.2.0 Python/C source in its own `lab/` directory once recovered rather than silently rewriting. **Status:** Source ZIP directly uploaded on October 7, 2026; archive SHA-256 `2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e`; 31 original files imported intact into `lab/` with provenance and offline test reruns. Preserve this historical lab unchanged, and do new engineering outside it.

## D-010 — License and redistribution (open before public code release)

**Question:** appropriate project license, third-party notices and upstream obligations. **Hard limit:** no commercial game files or proprietary patch data in GitHub without verified permissions.
