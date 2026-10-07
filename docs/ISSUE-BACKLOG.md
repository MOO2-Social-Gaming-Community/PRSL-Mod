# Initial GitHub issues — ready to copy into the new PRSL repository

Each entry includes a completion criterion and a dependency, rather than conflating research with implementation.

## 1. Import historical PRSL Lab v0.2.0 source without changes

**Type:** repository/critical. **Dependencies:** original `moo2_prsl_lab_v0.2.0.zip` in user's project Library. **Acceptance:** safe source import, reviewed `lab-import-provenance.json`, no proprietary files, original README/tests/source available, first commit captures source baseline without editing it.

## 2. Reproduce v0.2.0 Python suite and native probe with test environment metadata

**Type:** validation/high. **Dependencies:** #1; user-owned exact-hash engine for binary tests; supported Linux x86-64 GCC for native probe. **Acceptance:** original suite rerun, original-vs-new results compared, skipped conditions explained, logs sanitized, no full-game claims from isolated tests.

## 3. Investigate loaded DOS LE relocations and exact live engine identity

**Type:** reverse-engineering/high. **Dependencies:** #1–2. **Acceptance:** read-only runtime mapping across initializers, reproducible traces, unsupported hashes refused, file offsets not treated as runtime addresses.

## 4. Exhaustively trace strategic End Turn input/call paths

**Type:** reverse-engineering/high. **Dependencies:** #3. **Acceptance:** manual mouse, keyboard, automatic `Do_Begin_Of_Turn_`, modal UI, tactical distinction, saving/loading and other relevant routes covered or explicitly excluded with a justified fail-closed strategy.

## 5. Build safe-point deferred native End Turn proof on single game

**Type:** engine-prototype/critical. **Dependencies:** #3–4. **Acceptance:** within real DOSBox MOO2, Ready prevents native submission, Unready restores planning; permitted release resumes native path once using a fresh frame and preserves 1.50 RNG/network wrapper; no executable/source mutation.

## 6. Build PRSL authenticated coordinator transport and epoch protocol

**Type:** networking/high. **Dependencies:** state coordinator reviewed, #5. **Acceptance:** authenticated participants, version checks, Ready/Unready sequence, membership generations, duplicate suppression, barrier/fault handling, separate IPX and PRSL transport documented with negative tests.

## 7. Two-client multiplayer PRSL acceptance harness

**Type:** integration/critical. **Dependencies:** #5–6 and stable native transport. **Acceptance:** at least two real clients repeatedly Ready/Unready and advance one native turn each per commit with no desync; negative-network/fault/save tests pass and log evidence retained.

## 8. Specify optional PRSL UI and relationship to future Chat/lobby

**Type:** UX/medium. **Dependencies:** #5–7 for actual in-game behavior. **Acceptance:** essential Ready/Unready status works independently of new Chat; pre-game setup vs active-turn barrier labeled distinctly; no hidden activation of PRSL.

## 9. Define certified PRSL package and launcher integration contract

**Type:** integration/medium. **Dependencies:** #7. **Acceptance:** package schema/exact support matrix, signed files, rollback, disabled behavior with no injection, no changes to official owned game source, clear unsupported status on 1.40 baseline.

## 10. Decide source license and upstream engagement model

**Type:** governance/high. **Dependencies:** review ownership and third-party notices. **Acceptance:** clear license, `THIRD-PARTY-NOTICES` as needed, no rights over commercial data asserted, narrowly scoped requests to fan-patch maintainers without claiming their consent.

## 11. Add realistic cross-platform PRSL acceptance and recovery

**Type:** validation/later. **Dependencies:** #7–9. **Acceptance:** Windows 11 tested on real machine, other OS only when reproducibly tested; save/reconnect/Alt+Tab behavior, failsafe and repair documented.
