# Continuation plan / implementation boundary

## Established decisions

- Product concept: **Pre-ready State Layer**, outside the native game simulation.
- Preserve original community mode and the unmodified upstream executable as a managed dependency.
- Readiness policy is independent of engine offsets; the adapter is exact-build-specific.
- Current proof is for the supplied English 1.50.26 executable only.
- The Python CLI is a testable environment-manager prototype, not a commitment to the final GUI technology or an abandonment of the earlier cross-platform launcher design.
- No custom readiness/timer values are inserted into MOO2 saved-universe data.
- No live PRSL capability is advertised by the installer, catalog, or adapter metadata.

## Immediate next executable experiment

Provision a Linux DOSBox runtime that can actually launch the supplied game. For observation/control through the documented Staging API, verify the installed build exposes the required endpoints and keep its listener local-only. The existing ordinary DOSBox launch path does not require that API; a live PRSL adapter probably will require it or an equivalent debugging/guest bridge facility.

Start two separate writable workspaces, connect them using IPX, and prove an ordinary unmodified two-client turn first. Record runtime version, configuration, engine fingerprints, and baseline saves. A failure here is not a PRSL failure and should be diagnosed before injecting anything.

## Live adapter work still required

1. Resolve guest code/data/extension bases after DOS/4GW and the community initializer finish. Verify the code and contextual fingerprints in memory, not only the file hash.
2. Allocate a private guest bridge/mailbox in a controlled way. The laboratory fixed addresses are never valid installation instructions.
3. Audit keyboard, automatic-turn, and any indirect submission paths. The known automatic call at `0x7AF19` bypasses the manual candidate.
4. Add a minimal game-phase/turn/player observer and an input-loop safe point. Do not obtain turn identity from a guessed global or call-count proxy.
5. Install the manual event gate only after verifying original bytes, instruction boundaries, relocation status, and live runtime conditions. Initially stop at deferral; do not automate commitment.
6. Verify that the actual game remains responsive and receives native network traffic while deferred. Implement read-only pre-ready behavior or reliable invalidation on editing. The current laboratory gate does neither.
7. Reissue permission through a fresh valid input-loop event. Never save/reuse the caller EAX stack pointer or invoke native End Turn from an arbitrary host/HTTP callback.
8. Preserve the native dispatcher and community RNG-snapshot wrapper. Observe actual native submission separately from permit delivery.
9. Exercise two clients, cancellation races, disconnects, epoch changes after reload, eliminated participants, dialogs, and combat. Fail closed on ambiguous progress.

## Certification gate

Do not change `runtime_certified` to true because unit tests pass. Required evidence is a reproducible actual game session in which:

- A pre-ready request does not publish native finished state.
- Cancellation restores planning without rollback of published simulation state.
- Every participating client reaches a safe prepare point.
- A commit invokes the original native path at most once per verified epoch.
- Existing upstream wrapper/configuration behavior remains intact.
- Both clients advance and remain synchronized across repeated turns and a save/reload.
- Unsupported engine/runtime/configuration combinations are rejected without writes.

## Launcher / updater increments

Current: exact owned-archive import; original-file preservation; verified staging; package manifest; community launch-command generation; process lock for one workspace; signed-catalog checking primitive; PRSL refusal.

Next: reproducible approved runtime packages; stronger immutable cache / writable-workspace separation; bounded downloads; production trust-root/rotation strategy; persistent anti-rollback metadata; content-aware version selection; staged update promotion and save-preserving recovery. Do not silently equate the latest upstream release with the latest PRSL-certified release.

Then: GUI, LAN discovery, explicit local firewall diagnostics, cross-platform acceptance, and eventually Internet coordination. Do not expose an emulator memory-control API on the LAN.

## Minimal maintainer question

The public binary exposes a main-screen `_next_button` event at code-object offset `0x76D78` before `_next_turn_hit` is written. Is there a supported engine callback or documented safe-point facility that could defer this event and later reissue it without persisting caller stack state? Also ask about the automatic caller at `0x7AF19` and the extension wrapper at code offset `0x4EF2`.

This question is grounded in specific evidence and avoids requesting a speculative rewrite of multiplayer.
