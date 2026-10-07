# 1.50.26 native End Turn research — condensed technical map

**Source authority:** Archived PRSL v0.2.0 [`BINARY_REPORT.md`](../research/archive-v0.2.0/BINARY_REPORT.md), [`target-map.json`](../research/archive-v0.2.0/target-map.json), [`TEST_METHOD.md`](../research/archive-v0.2.0/TEST_METHOD.md), test logs. Figures below are **code-object offsets / on-disk file offsets**, not live DOSBox guest pointers.

## Exact build studied

| Item | Recorded value |
|---|---|
| Game build | Fan patch 1.50.26 / `ORION150.EXE` |
| Exact executable SHA-256 | `2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c` |
| Code object on-disk origin | `0x00095694` |
| Bound inner MZ origin | `0x00026654` |
| LE header at | `0x000292E4` |
| Parsed original LE fixup records | 51,363 |
| Community extension relocation records | 24,655 |

Raw patch/base ZIP digests were captured in original report; **not** available for this handoff's included files because no patches or game media are shipped. Only a legitimate owned and exact matching engine can support further binary verification.

## Crucial engineering correction

`Human_Hit_Next_Turn_` is a **seven-byte flag getter**, not a turn-submission method. Hooking it as though it submits turns is incorrect. In the archive it reads an indexed flag and returns AL, leaving upper EAX unchanged. The discovery was confirmed by structural examination and isolated instruction checks, **not** a running game.

## Manual Next-button candidate

```text
main-screen input event
  compare field to _next_button; check _skip_fields
  -> code object 1 + 0x00076D78   (file 0x0010C40C)
     original 5 bytes: E8 40 7B 07 00 (CALL Assert_Settings_)
  -> original continuation code object + 0x00076D7D
     writes _next_turn_hit then related UI flags
     calls Do_Next_Turn_ at +0x00076D99
  -> skip/deferral target +0x00076D9E
```

The isolated gate experiment temporarily replaced **only** that 5-byte complete instruction. Deferral recorded laboratory intent and skipped native flag/UI writes. Permission preserved the original CALL, then resumed in the **current live call frame**. The test restored registers/flags/stack balance under controlled helper stubs.

**Important limits:** guest loaded memory offsets have not been established, the startup initializer could affect loaded code, and no complete input or network loop was executed. No actual executable patch is provided by this repository.

## Alternative End Turn path and stale stack hazard

`Do_Next_Turn_` lives at code + `0x00073411` (file `0x00108AA5`). Known direct callers:

- Manual main-screen button at `0x00076D99`, EDX=0.
- Automatic `Do_Begin_Of_Turn_` at `0x0007AF19`, EDX=1.

The callee stores a caller-provided EAX pointer and eventually writes a 16-bit loop-exit local through it. A delayed call must **not** reuse a captured pointer to an old stack frame. Retain epoch and intent; arrange for the unmodified original operation in a newly validated event loop frame. This is why simple 'pause the Next Turn function and release it later' patches are unsafe.

The manual gate **does not** cover the automatic caller. All keyboard/input/automatic/tactical distinctions still require a full call-graph and in-game study.

## Existing 1.50 native network wrapper

`Net_Next_Turn_`: code object + `0x000EC470` (file `0x00181B04`). Native finished flag write recorded at +`0x000EC51E`, with later network message send CALL at +`0x000EC584`. This is after irreversible native state updates; PRSL should not attempt to un-submit a turn by merely clearing the finished flag.

The patch redirects network-screen dispatch via a community extension wrapper that snapshots `_random_seed` and then jumps into `Net_Next_Turn_`. Do not bypass the wrapper by directly invoking an old function address: allow the native dispatcher to operate as designed.

## Failure of naive addressing

The bound DOS LE image uses inner MZ data-page origin and relocation records, **not** a straightforward PE-style pointer from the outer executable. The original research needed to correct a naive object-copy approach. The exact import and runtime relocation mapping must be recreated before any live guest-memory work. File offsets are never accepted as patch addresses.

## Experimental proof vs production gaps

**Historically measured:** 30 compatibility-mode x86 instruction checks, original extension relocation reproduction against Python reconstruction, synthetic Next-button conditional behavior, controlled register and game-data equivalence and one-shot permit, old-frame avoidance.

**Not measured:** a DOSBox-hosted game, all input paths, input responsiveness, actual UI rendering, game network advances, native chat, mod configurations, multiplayer determinism, save/reload or any Windows/macOS guest behavior.

Do not copy this map onto a different build (including 1.40b23 or repacked/localized 1.50.26) without fresh executable hash, relocation map and independent review.
