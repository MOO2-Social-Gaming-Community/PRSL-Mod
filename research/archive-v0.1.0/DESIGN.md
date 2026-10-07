# Proposed design specification

Version **0.1.0** | Research date **2026-10-04** | Owner **Psyche42**

All requirements and interface names below are **proposals**, unless explicitly attributed to an evidence entry. See `evidence.json` for source URLs. No guessed memory offsets, callable engine symbols, successful compatibility claims, or executable download hashes are provided.

## 1. Product definition

PRSL records reversible player readiness before permitting MOO2's native End Turn path. It does not replace turn resolution, change race balance, reverse already submitted actions, or provide asynchronous play-by-mail.

Its four user-facing functions are a planning-phase readiness roster, Ready/Unready, automatic release when all active humans are ready, and an optional strategic planning deadline. Native submission remains a distinct irreversible boundary.

The launcher imports a clean owned game installation, stages known community packages, selects a tested bundle, applies the independently versioned adapter and configurations, verifies compatibility, and starts the emulator plus the session service. It should make the routine workflow similar across operating systems without implying that all machines or operating-system versions are supported.

## 2. Verified anchors and their limits

The public changelog currently identifies engine **1.50.26**, dated **May 30, 2026**. [E01]

The original multiplayer manual describes a native Turn Monitor and chat after End Turn; this does not establish a reversible pre-submission screen. [E02]

The documented Lua environment is limited, and the public patch/build chapter is unfinished. These documents do not supply a callable End Turn hook or a verified patch recipe. [E03, E04]

The existing launcher and standard mod descriptor system are useful integration references, not proof that PRSL can be implemented as a configuration-only mod. [E05, E06]

## 2A. Engine-backend selection gate

A developer reports an SDL3/TCP reimplementation in restricted testing, with community-patch backporting still underway. This is self-reported, not independently tested here. [E21]

**Recommendation:** investigate the `#orion2re` lead before choosing the native integration backend. Compare source/build availability, license, genuine multiplayer compatibility, mod coverage, save compatibility, and the ability to defer End Turn safely. Do not infer that a source reimplementation supports every current 1.50 configuration or plays over the original DOS network protocol.

The rest of this specification describes the released DOS/community-patch baseline. Keep its implementation behind an `EngineAdapter` interface. A future source-native backend may implement the same semantic contract with ordinary source hooks rather than executable patching and emulated memory access. Its direct engine transport and distribution manifests would be backend-specific.

Do not fund two complete backends immediately. Select one after the source-access and hook experiment, while retaining an ordinary public-community-patch profile for the meetup. A privately described anniversary target is not a dependency release date.

O2M is another existing frontend/editor, and its author describes a reduced community-patch bundle. [E22] Study its workflow, but do not use an arbitrary repack as the canonical engine/mod catalog.

## 3. Architectural boundaries

```text
UPDATES                       LOCAL PLAYER MACHINE
Signed release catalog ----> Package manager / compatibility resolver
                                      |
                              Read-only package cache
                                      |
                              Writable play workspace
                                      |
UI <--> Session service <--> Exact-build game adapter <--> MOO2 in DOSBox
          |                           |
          |                           +-- observes phase / intercepts intent
          |                           +-- releases original native operation
          |
          +---- authenticated PRSL control channel ---- coordinator

MOO2 <-------- native emulated IPX traffic --------> other MOO2 clients
```

Maintain separate update, coordination, and game-transport responsibilities. The update server need not be online during local play. The PRSL coordinator need not be the game host or the DOSBox IPX relay host. A process may implement several roles, but configuration and logs must distinguish them.

### Proposed components

| Component | Responsibility | Must not do |
|---|---|---|
| `prsl-core` | Pure state machine, epochs, timer policy, compatibility decisions | Read arbitrary game memory or use MOO2 RNG |
| `prsl-session` | Coordinator/client transport, authentication, acknowledgements, logs | Pretend a network acknowledgement proves native submission |
| `prsl-adapter` | Exact-build native interception, safe-point release, phase observation | Apply a bridge to an unknown executable |
| `night-package` | Import, hash verification, staging, activation, repair | Replace saves or execute unsigned catalog instructions |
| `night-runtime` | DOSBox invocation, adapter lifecycle, paths, process diagnostics | Require Steam to remain running after an owned-file import unless the source copy requires it |
| `night-ui` | Setup, Host/Join, roster, status and recovery explanations | Become the sole owner of live game/session state |

A Rust core with a Tauri desktop shell is a candidate, not a prerequisite. Start with a headless coordinator and a small test interface. Closing or restarting a cosmetic window should not silently destroy the live session. No additional Lua framework is required merely because 1.50 exposes Lua.

## 4. The native engine contract

### Interception semantics

Do not sleep inside the native button callback. Intercept **intent**, return a valid result to the game, continue servicing the event loop, and later schedule the original operation from an approved safe point.

“Same operation later” does not mean an old stack frame, captured UI pointer, or network packet can be saved and replayed. Nor does it promise byte-identical output after unrelated diplomacy or other live state changes. The requirement is to retain native end-turn semantics and introduce no unintended simulation mutations.

### Required observations

The adapter must determine the running executable identity, current session/load generation, strategic-turn identity, local human slot, active human membership, current phase, outstanding blocking UI, whether native submission is possible, and whether native submission has occurred. A player-visible empire list is not an authenticated human-participant roster.

### Proposed conceptual interface — not an existing MOO2 API

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

Every route to the strategic End Turn operation must be audited: mouse, strategic hotkey, options that advance turns, and any other programmatic entry. Do not intercept a similarly named tactical-combat operation. Existing documented shortcuts already show why a generic global key interceptor is inadequate. [E07]

Native networking must remain live while a player is pre-ready. Orders/diplomacy traffic that normally occurs during planning must not be suppressed simply because it is network traffic.

### Ready-view policy

For the first implementation, pre-ready locks local order editing and offers Unready. It may show read-only status only where that can be proven not to change gameplay. Supporting arbitrary continued editing with automatic readiness cancellation requires more mutation hooks and should be a separate feature.

If an incoming game event invalidates the safe planning state, invalidate pre-readiness or stop the barrier according to a documented rule. Never allow a stale prepared acknowledgement to cover a newly opened modal dialog.

### Native execution invariant

Release the original native path no more than once per local game process and commit ID. Confirm actual engine submission separately. A log file is not a transaction covering engine memory: after an ambiguous crash, do not claim exactly-once recovery. Fail closed and reload a common known-good save when necessary.

## 5. Bridge implementation choices

Preferred: maintainer-supported generic interception/safe-point/phase hooks. Keep the PRSL policy outside the original engine wherever practical.

Fallback: an exact-build bridge, reviewed against the real executable. Required evidence includes executable SHA-256, original bytes at each patch site, relocation-aware addressing, calling convention, preserved registers/stack, instruction boundaries, return semantics, re-entry guard, and a source-controlled build recipe. None of those offsets or signatures is established by this research.

DOSBox Staging's documented local memory API is a candidate research transport. [E08, E09] An exploratory adapter can begin read-only, then use a verified bounded mailbox with a guest-resident hook. Polling memory alone cannot reliably intercept an event before it happens. Writing a player-done flag is not equivalent to executing the native End Turn routine.

If a mailbox is used, specify command IDs, epochs, lengths, status generations, acknowledgements, bounds checks, and consistent snapshot reads. Let the guest hook consume commands at approved engine points. External requests must never jump the guest CPU into an arbitrary function mid-instruction sequence. Emulator-level atomic access does not establish a game-level transaction.

Do not expose emulator memory services beyond loopback. The network coordinator should receive only protocol status, not memory addresses or game-state dumps. Review local HTTP origin/authentication assumptions before enabling such an API in a distributed end-user build.

An external roster/timer with voluntary manual submission is a useful rehearsal tool, but must be labeled **advisory mode**, not the implemented PRSL barrier.

## 6. Chat and original behavior

Native post-submission chat should remain untouched in the first release. Reusing its whole screen before submission is permitted only after separating its rendering, message handling, wait-loop and submission side effects.

A later PRSL chat view can offer a deliberately separate pre-submission conversation channel. Define visibility explicitly: all active participants, pre-ready players only, or an opt-in assembly phase. Do not accidentally imitate a private-looking UI while broadcasting to everyone. Plain text, bounded messages, no embedded remote content, and an optional host pause are sufficient initial requirements.

When all clients release native submission nearly together, the original wait/chat interval may be very short. A meaningful chat intermission therefore requires an explicit host policy, not merely drawing the existing screen.

## 7. Clean installation and configurations

Treat Steam/GOG/CD directories as read-only **sources**. Require a complete acceptable DOS installation, recognize its edition/language and file identities, then create an independent managed copy. Do not assume every legally owned edition has identical bytes. Unsupported editions should produce a precise import report rather than being labeled illegitimate.

Keep these separate:

```text
cache/objects/<digest>/              immutable downloaded/imported objects
bundles/<bundle-id>/                 immutable verified bundle description
workspaces/<session-id>/GAME/        writable DOS play directory
profiles/<profile-id>/               user preferences / selected packages
saves/<campaign-id>/                 retained exports and backups
logs/<session-id>/                   bounded diagnostics
staging/<transaction-id>/            incomplete updates, never launchable
```

Use copies or safe copy-on-write workspaces; do not hard-link writable files into an immutable cache. Preserve autosaves, custom build lists and user settings. Mount the chosen play directory as a short DOS path; avoid assuming host paths or filenames satisfy DOS naming rules.

The current manual supports selecting a different root configuration with `/c=`. [E10] A proposed invocation is `ORION150.EXE /c=PRSL.CFG`; that filename is our choice, not a supplied upstream file. Generated configuration must preserve required upstream includes and assets. Store PRSL-only settings in the launcher's own schema until a bridge explicitly supports them; do not add unknown keys to the native CFG parser.

An independent mod descriptor can advertise PRSL rather than replacing the selected Core ruleset. The descriptor does not, by itself, load native adapter code.

## 8. Version resolution

Resolve a **tested tuple**, not just an engine version:

- source-edition/language compatibility;
- exact community engine binary;
- selected Core, map and add-on packages plus load order;
- required scripts and LBX assets;
- adapter implementation and allowed engine identities;
- PRSL protocol version;
- per-platform emulator binary and required settings;
- generated effective session configuration.

The manifest example deliberately uses null hashes and `installable: false`. It must be rejected for activation.

Expose three different concepts in the UI: **latest observed upstream**, **latest certified PRSL bundle**, and **this session's locked bundle**. VDC or another separately distributed ruleset must have its own provenance/version rather than inheriting an engine version.

No update is activated while a game is running. New upstream content is staged and tested before it becomes a certified PRSL tuple. Preserve a standard community-only profile for participation in ordinary games. Mixed PRSL/non-PRSL clients must not silently enter a PRSL-required session.

## 9. Update and repair pipeline

```text
Check signed catalog -> select compatible target -> bounded download
-> verify signature/hash/size -> safe extraction -> stage
-> validate required files and bridge identity -> build clean workspace
-> smoke-test -> atomically activate -> retain prior known-good bundle
```

Use signed manifests with expiry and rotation/revocation design. Prevent arbitrary URL execution, archive traversal, symlink escapes, decompression bombs and unexpected executable names. Keep a publish key separate from the ordinary web server. A hash received from a compromised server alongside its payload is not an independent trust anchor.

TUF documents update threat models; Tauri's updater can cover application updates, but does not certify MOO2 content compatibility. [E12, E13] Treat application and game-content updates as separate verification paths.

Offline play should work with a verified installed bundle. Expired remote metadata means an update cannot be trusted as current; it need not delete or disable an explicitly selected previously verified offline installation. Never silently downgrade. Intentional rollback uses an approved retained bundle with a visible compatibility warning and save backup.

Repair should report managed differences and regenerate managed files only. User settings, saves and diagnostic consent must survive repair. Logs should exclude credentials, memory dumps and private filesystem paths unless explicitly requested for a support export.

## 10. Networking and platform targets

Native IPX-over-UDP and the PRSL coordination channel are separate transports. [E11] A public IPX relay does not automatically carry a new WebSocket/TCP channel. A room code identifies a session; it does not solve NAT traversal.

For LAN, offer discovery as a convenience and explicit address/invite fallback. Detect guest-Wi-Fi/client-isolation problems without claiming to fix router policies automatically. For internet play, document both the native-game relay/direct/VPN route and coordinator reachability. Do not silently open router ports or expose emulator control.

Initial target matrix: Windows x86-64; Ubuntu x86-64; Intel Mac; Apple Silicon Mac. Actual supported OS versions depend on both launcher and runtime validation. The current DOSBox Mac download specifies macOS 12+ for its universal build. [E14] The 2015 MacBook is therefore a useful test target only after checking its installed OS and the launcher requirements. CPU age alone is not a compatibility guarantee.

Ship native platform packages from a common core. Preserve executable signatures as applicable and use standard permission workflows; do not instruct users to disable operating-system security protections.

## 11. Licensing and community integration

The public launcher repository states GPL-2.0. [E06] Treat reuse obligations separately from permissions covering commercial game data, patched binaries, art and other community packages. Maintain provenance and license/notices per distributed artifact; verify permissions before mirroring fan binaries or redistributing modified executables.

Ask maintainers for narrow generic hooks and a reproducible compatibility boundary, not acceptance of the entire launcher. Submit adapter specifications, failure tests, diffs and build provenance. Upstream integration can then replace the bridge without forcing a rewrite of the PRSL state machine.

## 12. Scope limits for the first milestone

The first demonstrable success is not an installer. It is two real MOO2 clients where Ready delays native submission, Unready restores safe planning, and a coordinated release advances one native turn without desynchronization.

Full-screen native UI, strict hard deadlines, automatic host migration, broad mod compatibility and chat can be staged after that proof. The eventual user experience remains the requested integrated system; staging does not redefine an advisory overlay as that system.