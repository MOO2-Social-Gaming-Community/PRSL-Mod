# Exact-build binary report: MOO2 1.50.26

Research snapshot: October 4, 2026. Primary evidence is the supplied executable and the reproducible programs/logs in this package. Public project documentation is supplementary; it did not supply these hook addresses.

## 1. Identity and addressing

| Item | Value |
|---|---|
| `ORION150.EXE` SHA-256 | `2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c` |
| Uploaded patch ZIP SHA-256 | `0ac9151e9cf752ec34b6db998d8b390f48e492d8443e8f1658112b93c7f6a921` |
| Uploaded base ZIP SHA-256 | `87e657bc2e8b02714856f13c3c63066cd58549f33a9c2e917d1bca6936142d2b` |
| Base `ORION2.EXE` SHA-256 | `4e11be14217b4aafa1839f333bf5eba037f98b0c44e9e4752c96c464c260419f` |
| Bound inner MZ origin | file `0x00026654` |
| LE header | file `0x000292E4` |
| Actual object-1 page origin | file `0x00095694` |
| LE fixup records parsed | 51,363 |
| Community extension relocation records | 24,655 |

The outer DOS-bound executable cannot be mapped by assuming its first MZ header's new-header pointer is a normal Windows executable pointer. The LE data-page origin is relative to the **bound inner MZ**, not the beginning of the complete file. Earlier naive object copies produced incorrect addresses; the supplied mapper uses the corrected bound-image origin, page map, final short page, and fixups.

The retained debug records contain offsets and object identifiers as well as names. Names alone are not proof of current semantics. The research checks the actual code and startup relocation records as well.

Object offsets must be resolved against the running DOS extender's segments/bases. The fixed addresses used by `native_probe.c` are invented **laboratory mappings**, not addresses to paste into a real game's memory editor.

## 2. Human_Hit_Next_Turn_ is a getter

| Property | Verified value |
|---|---|
| Code object | 1 |
| Object offset | `0x000EA5A3` |
| File offset | `0x0017FC37` |
| Instruction bytes before relocation | `8A 80 7E 2F 03 00 C3` |
| Input | EAX = player index |
| Output | AL = byte read; upper 24 bits of EAX unchanged |
| Data target | object 2 + `0x00032F7E` + player index |

```asm
mov al, byte ptr [eax + 00032F7Eh]  ; operand relocated to the data object
ret
```

This routine does not set readiness, send a network packet, draw a screen, or advance the game. It has no index bounds check. It is a potential **observer of native finished state**, not the submission interception point. PRSL pre-ready must remain a distinct state.

The direct call sites identified in the original code are `0x000FB749` and `0x000FB7DA`, within `Race_Screen_`. This is not a claim of exhaustive indirect-call recovery.

## 3. Manual-input path

The main-screen event block compares the selected field with `_next_button`, data object offset `0x24162`, and checks `_skip_fields`, offset `0x21976`.

**Naming correction:** `_end_of_turn_button` is another retained symbol at data object offset `0x23574`, in a different module. It is not the field compared in this main-screen block. Similar names must not be substituted for traced references.

Selected excerpt, shown with symbolic data references:

```asm
00076D62  mov  eax, [ebp+76h]
00076D65  cmp  ax, [_next_button]
00076D6C  jne  00076D9E
00076D6E  cmp  word ptr [_skip_fields], 0
00076D76  jne  00076D9E
00076D78  call Assert_Settings_
00076D7D  mov  byte ptr [_next_turn_hit], 1
00076D84  mov  byte ptr [data+21F2Dh], 0
00076D8B  lea  eax, [ebp+4Ah]
00076D8E  xor  edx, edx
00076D90  mov  word ptr [data+219DEh], 0FC18h
00076D99  call Do_Next_Turn_
00076D9E  ... ordinary subsequent input processing ...
```

### Preferred experimental boundary

- Gate at code object 1 + **`0x00076D78`**, file **`0x0010C40C`**.
- Five replaced bytes in the laboratory: **`E8 40 7B 07 00`**, a complete CALL instruction.
- Deferral: record only PRSL intent, restore registers/flags, jump to **`0x00076D9E`**.
- Permission: execute the original `Assert_Settings_` call, then resume at **`0x00076D7D`**.
- `Assert_Settings_` is currently a RET in the inspected on-disk and relocation-reconstructed image. The permitted path preserves its call rather than assuming it can always be removed.
- No parsed LE or extension relocation overlaps this five-byte candidate. This does **not** prove that later initializer/configuration code cannot change it.

This location precedes the native `_next_turn_hit` write, subsequent UI state writes, and screen-transition routine. It is therefore a better no-side-effect **manual-event candidate** than intercepting the flag getter or pausing in the network waiting screen.

The laboratory gate preserves general registers, EFLAGS, and stack balance on deferral. Its stack scratch and separate PRSL mailbox may change; the claim is not that every byte in the entire address space is unchanged.

## 4. Do_Next_Turn_ and the live-frame requirement

`Do_Next_Turn_`: code object 1 + **`0x00073411`**, file **`0x00108AA5`**.

The first five bytes cover four complete instructions: `53 51 56 89 C6` (three PUSH instructions and `MOV ESI,EAX`). This is a possible secondary common-routine hook, but the manual caller has already performed the native UI/intent writes by then.

Observed direct callers:

| Caller | CALL object offset | Argument context |
|---|---:|---|
| Main-screen Next-button event | `0x00076D99` | EAX points to `[EBP+0x4A]`; EDX=0 |
| `Do_Begin_Of_Turn_` automatic path | `0x0007AF19` | Different live stack-local address; EDX=1 |

The function stores EAX in ESI and eventually executes:

```asm
00073545  mov word ptr [esi], 1
```

**Inference from callers and callee:** EAX carries a pointer to a caller-owned, 16-bit loop-exit/control local. It is not a persistent turn-request token. Retaining this pointer while returning to the game, then calling the function asynchronously later, risks writing to an expired/reused stack frame.

PRSL must retain **intent and an epoch**, not a suspended native stack frame or stale EAX. On permission, a verified live main-loop event should run the original path using its current frame. The fresh-frame laboratory check proves that the proposed release sequence uses the newly supplied frame; it does not implement a real input-loop scheduler.

The manual gate does not cover the automatic caller. A production adapter must trace, intercept, or explicitly disable such alternate paths under PRSL, and test shortcuts and tactical-combat distinctions. Do not declare all input routes covered from these two direct calls alone.

## 5. Native waiting/submission and existing community behavior

`Do_Next_Turn_` selects current-screen value **37 (`0x25`)** for the inspected game-type values **2 and 3**. These two values were tested as synthetic network-path fixtures; complete host/client setup was not executed.

In `Screen_Control_`, the screen-37 dispatch CALL is at **`0x00000753`**. Its on-disk displacement is a startup relocation placeholder, not a ready-to-use direct call into `Net_Next_Turn_`.

The community extension resolves that call to its code offset **`0x00004EF2`**. The wrapper saves the original `_random_seed` value (data object 2 + **`0x00041E34`**) into an extension-owned snapshot at offset **`0x00004EEE`**, restores EAX, and tail-jumps to the original `Net_Next_Turn_`.

**Preserve this route.** Directly calling an old network function address would bypass an existing 1.50 wrapper. PRSL's release should return to the native main-screen flow, allowing the existing dispatcher and wrapper to remain in control.

`Net_Next_Turn_`: object 1 + **`0x000EC470`**, file **`0x00181B04`**.

Within that function:

- `0x000EC51E` writes 1 to the indexed native-finished flag at data object 2 + `0x32F7E`.
- A subsequent network-send call occurs at `0x000EC584`, targeting `Mox_Send_Message_`.
- Native screen setup and other state changes have already occurred before this point.

Therefore, deferring after this write would be too late for the proposed non-submitting pre-ready stage. PRSL must not cancel by clearing a native finished flag after it has been published.

## 6. Why relocation analysis matters

The community extension header is at file **`0x00285B6A`**. Its payload starts 12 bytes later. The payload declares:

- payload length `0x000B7D43`;
- relocation-table start `0x50`;
- extension code start `0x423B5`.

Each 11-byte record encodes relative/absolute addressing, a source segment, a target segment, and source/target offsets. The segment mappings were traced from the actual loader: extension code, original data, original code.

The native probe executes the **original relocation loop at code offset `0x001596C4`**, stopping at `0x001596F6`, on synthetic flat mappings. The resulting original code, original data, and extension payload match the Python reconstruction byte-for-byte. This cross-check covers all 24,655 extension records. It does not execute the subsequent extension initializer or the complete DOS/4GW loading process.

## 7. What is established versus not established

**Established:** exact binary identity; structural symbol/address mapping; getter semantics; manual and automatic direct call sites; early manual gate; caller stack-pointer requirement; native finished-flag publication site; existing RNG-snapshot wrapper; relocation-aware reconstruction; narrow actual-instruction defer/release equivalence under declared stubs.

**Not established:** live loaded addresses; post-initializer fingerprint; guest allocation/patch installation; event-loop/network responsiveness; read-only pre-ready UI; safe live event injection; all alternate submission paths; player/turn/phase observers; two-client determinism; save/reload behavior; timer enforcement; live coordinator-to-game transport; compatibility across other configurations or executable hashes.

The safest defensible conclusion is **“a tested manual-event interception candidate”**, not “a universally safe, game-tested hook.”

## 8. Supplementary public documentation

- MOO2 Book installation: https://moo2mod.com/doc/dist/installation.html — manual patch overlay and running ORION150.EXE from the game root.
- MOO2 Book patching: https://moo2mod.com/doc/150/patching.html — reverse-engineering/build sections remain TODO; no verified End Turn ABI supplied there.
- DOSBox Staging HTTP API: https://www.dosbox-staging.org/0.83/manual/http-api/ — a candidate observation/control transport, not used by this experiment. The page is labeled a development website; verify the actual installed runtime's capabilities. Keep it local-only; its documentation warns about full emulator control and primarily normal-core testing.

Links accessed during this research. The computed addresses and measured results come from the supplied executable, not those webpages.
