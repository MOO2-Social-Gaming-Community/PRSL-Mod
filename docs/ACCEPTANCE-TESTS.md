# Acceptance and regression plan

This is a **plan**, not newly executed engine testing. The historical lab tests are preserved under `research/archive-v0.2.0/evidence`.

## Tier 0 — Repository and source integrity (handoff tool tests)

- Validate original archived research JSON, paths, docs presence and no proprietary artifacts.
- Import an intentionally safe synthetic ZIP into a disposable repo and verify byte preservation and provenance recording.
- Refuse traversal (`../`), absolute/drive paths, symlinks, case collisions, ZIP bombs/huge members, game executables and overwrites.
- Validate original source import only after the real ZIP is supplied; do not claim its content has been tested here.

## Tier 1 — Historical lab replay

- Reproduce v0.2.0 Python `unittest` suite: 52 passed historically with exact owner engine; 9 engine-specific tests may skip without `MOO2_ENGINE`.
- Reproduce C native compatibility-mode probe: 30 historical checks under Linux x86-64 + GCC; run only on exact hash and private fixtures.
- Verify known v0.1 duplicate READY/GRACE issue is closed; repeated/out-of-order READY cannot bypass revoked acknowledgements.
- Run workspace safety: tampered engine refused; user save edit preserved; PRSL launch refused without certified adapter; source archives untouched.

## Tier 2 — Single real game, read-only adapter

1. Exactly identify game build and runtime mapping after startup initializers.
2. Confirm observed turn ID and human slot match real game, including save reload and current-player changes.
3. Trace mouse Next, keyboard shortcuts, automatic turn-start path, combat, modal interruptions and stop/quit.
4. Launch with PRSL disabled: file hashes and native turn simulation behave as before; no injected code or coordinator packets.
5. Re-run with PRSL diagnostics enabled but **no write/injection**; verify zero gameplay mutation.

## Tier 3 — Single real game, intercepted barrier

| Scenario | Required behavior |
|---|---|
| Manual Ready | Native turn not submitted, planning UI still processes allowed events, no native done flag set |
| Unready | Restores safe editing from pre-ready, no game submission |
| Repeated Ready | Idempotent; no second release or unsafe committed transition |
| Safety revoked after Ready | Permit blocked until fresh safe acknowledgement; no stale release |
| Correct release at safe point | Original frame and original 1.50 network/RNG wrapper retained |
| Automatic End Turn branch | Intercepted or constrained; cannot bypass PRSL |
| Tactical/combat screen | No interception of similarly named tactical action |
| Save/reload, modal, lost focus | Epoch revalidation; no stale pointer or UI token |
| Crash during ambiguous commit | Explicit uncertain/fault state; no fabricated rollback |
| Unsupported engine hash | Refused before any memory modifications |

## Tier 4 — Two machines / multiplayer proof

Start with LAN if possible (two independent writable workspaces); reproduce later over public Dopefish and other supported network paths. PRSL coordination transport is separate from IPX.

- Both clients have the same exact engine, gameplay mods, PRSL protocol and adapter bundle fingerprints.
- Ready A then B, B then A; Unready at any permitted pre-commit stage; duplicate/reordered READY; stale turn and old membership messages.
- Fault and reconnect while one Ready, then while all Ready, then after one native submission observed.
- Host leaves; guest leaves; mixed PRSL/non-PRSL attempts; participant membership changes.
- Record native turn counter, hashes of safe observable state or save parity as appropriate (understood privacy/compatibility limits), exceptions, connection logs and engine messages.
- Run multiple consecutive turns with different player orders and actual game actions to detect synchronization or RNG differences.

**Accept:** turn counts progress normally for both clients, exactly one native submission per local commit, no premature End Turn, no desync, no unsafe recovery claims. Repeat on the pinned engine/profile and publish sanitized evidence.

## Tier 5 — Packaging / platform

- Production package metadata, exact engine hash and independent PRSL version; signatures, download verification, staged install/rollback.
- Disabled mod produces zero hook/UI/control side-effects.
- Launcher, game and native networking remain functional after PRSL removal.
- Real Windows 11 acceptance; other OS support only after actual hardware/guest testing.
- UI visibly distinguishes 'observing', 'deferred', 'ready', 'grace', 'committed', 'fault' and 'uncertain' states where implemented.
- Original game binaries, saves and upstream community patch files are never committed or repackaged.

## Reporting template

```text
Exact game SHA-256:
PRSL version / adapter build:
Launcher/runtime version + config fingerprint:
Test machine(s) and OS / DOSBox:
Game profile, player count, network topology:
Scenario ID and steps:
Observed evidence (logs/screenshots; no private data):
Expected / observed native turn behavior:
Result: PASS / FAIL / BLOCKED / NOT RUN
Unknowns / rollback method:
```
