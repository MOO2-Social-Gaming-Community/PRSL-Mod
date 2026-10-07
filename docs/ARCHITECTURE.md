# PRSL architecture and feature boundaries

## The PRSL state transition we want

```text
MOO2 local planning (native strategic game, active human)
   |
   | player selects Ready in a PRSL-enabled session
   v
PRSL intercepts intent BEFORE native submit, keeps game event loop alive
   |
   +--- optional Unready ----------> native planning resumes, intent cancelled
   |
   v
Epoch-bound human roster / acknowledged barrier
   |
   | all valid active humans ready and safe, commit permitted
   v
PRSL schedules original native End Turn at a validated safe point
   |
   v
MOO2's ORIGINAL Do_Next_Turn_ / network wrapper / native resolution
   |
   v
Observe next strategic planning phase; advance epoch
```

A cosmetic overlay alone cannot implement this guarantee. Setting a native finished flag after submission is not reversible readiness. **Never block the in-game UI event loop with a wait/sleep at the native callback**.

## Components and ownership

```text
MOO2-SGC Launcher             (separate repository)
   imports legitimate game, pins patch + profile, prepares runtime
   activates PRSL only when a genuinely certified independent package exists
                    |
             local lifecycle boundary
                    v
PRSL integration/service      (future, this repository)
   +-- state coordinator      (`lab/prsl/state.py`, recovered offline code)
   +-- game adapter           (exact-build reverse engineering only)
   +-- control transport      (unimplemented; auth + epochs + reconnection)
   +-- local readiness UI     (unimplemented)
                    |
             original MOO2 turn path
                    v
ORION150.EXE + DOSBox          (licensed game/third-party runtime, NOT here)
             original IPX native game transport
```

The coordinator need not be the game host or public IPX relay. Native game traffic and PRSL control messages must be separately versioned, logged and fault-isolated. The launcher may also provide an independent **pre-game lobby**, which is not an engine submission hook. A separate **Chat extension** may display status but must not be a hidden dependency of PRSL.

## Core invariants / negative requirements

1. **Opt in only:** PRSL is never active merely because installed. Selected, resolved, compatible and active are different states.
2. **Fail closed:** unsupported engine hash, unknown phase, stale epoch, modal UI, missing participant, lost auth or uncertain submission blocks new PRSL release; it never patches blindly.
3. **Epoch safety:** every Ready/Unready or commit references a specific turn, unique human session and membership generation. Duplicate and delayed messages are idempotent.
4. **Native fidelity:** do not alter the original simulation or bypass patch 1.50's RNG snapshot/network wrapper.
5. **Safe release:** schedule native End Turn from a fresh game frame; no reused native stack pointers or arbitrary jump into game code.
6. **Commit boundary:** actual native submit must be observed separately; a coordinator ack is not evidence the original game advanced. After ambiguous crash, stop and recover from a mutually agreed save rather than pretending to roll back irreversible submissions.
7. **Transport separation:** DOSBox IPX cannot carry a new PRSL coordinator protocol merely by pointing the game at a public IPX relay. Never expose emulator guest-memory APIs to the internet.
8. **Compatibility:** same certified engine adapter and session semantics on every active human client; unmodified/community profiles remain available without PRSL.
9. **No hot swapping:** package, hook, and configuration changes require a clean start after save/rollback decisions.
10. **No mandatory chat:** PRSL readiness UI must remain functional if the optional new Chat extension is disabled.

## Conceptual adapter contract (proposed, not implemented)

The original 0.1 spec sketches:

```text
observe_phase() -> phase, epoch, local_slot, human_membership
intercept_end_turn_intent() -> accepted_deferred | bypass_disabled | error
enter_pre_ready_view() -> ready_view_token
cancel_pre_ready_view(token) -> resumed_planning | error
prepare_release(epoch, barrier_id) -> locked_safe | not_safe(reason)
release_native_end_turn(epoch, barrier_id, commit_id) -> scheduled | rejected
observe_native_submission(commit_id) -> pending | submitted | uncertain
observe_next_planning_phase() -> next_epoch | still_resolving
```

These are **design names** and MUST NOT be described as existing MOO2 APIs. First determine whether generic hooks can be obtained from 1.50 maintainers; otherwise prototype an exact-hash adapter in a disposable workspace with disassembly, memory-map validation, preservation tests and rollback.

## Clarifying 'pre-ready' and 'lobby'

| Function | When it occurs | Initial home | Implemented? |
|---|---|---|---|
| Session creation, host/join/version checks | Before the match | Launcher / future shared lobby | Launcher has some network/profile handling; no completed independent lobby |
| Pre-turn Ready/Unready barrier | During each strategic planning turn | PRSL core + native adapter | Research prototype only |
| New player chat tab | Before/during session by policy | Optional Chat extension | No |
| Original game Turn Monitor/chat | After native End Turn | MOO2 itself | Already part of the unmodified game; preserve it |
| Gameplay speed/balance, strategic/tactical rules | Game mode selection | SCG or Tournament mods | Separate future gameplay mods |

A future common UI may offer tabbed Lobby / Readiness / Chat, but **shared presentation is not a license to fuse their engine semantics or repositories**.

## Distribution boundary

GitHub Releases is the primary project release location; Cloudflare R2 is an optional mirror. The launcher handles verified packages and runtime orchestration, never an automatic raw game download. PRSL must remain independently versioned, signed and removable. Do not make pre-ready networking or update metadata depend on Neocities.
