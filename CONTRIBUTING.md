# Contributing to PRSL research

This is a pre-alpha engine-integration project. Contributions should be narrow, reversible, testable, and explicit about their evidence level.

## Before work

- Read `STATUS.md`, `docs/ARCHITECTURE.md`, `docs/ENGINE-RESEARCH.md`, `docs/ROADMAP.md`.
- Obtain and import the original `moo2_prsl_lab_v0.2.0.zip` before editing the historical Python/C implementation. Do not silently reimplement missing code and claim fidelity.
- Use a fresh branch for each proof or defect. Keep v0.2.0 source unmodified in its first imported commit where possible.
- No source game files, patched binaries, saves, signing keys or private networking credentials in PRs or diagnostic attachments.

## Required claims in a pull request

State **what changed**, **which exact executable hash was used**, **how tested**, **what remains untested**, and **rollback behavior**. Distinguish structural, isolated-instruction, emulator, single-player, and live two-player tests. Include failure traces (redacted) and expected vs actual outcomes.

## Testing

```bash
python tools/validate_handoff.py
python -m unittest discover -s tests -v
# After importing the original ZIP:
cd lab
python -m unittest discover -s tests -v
```

Tests requiring a licensed game binary must be skipped without `MOO2_ENGINE`. Do not upload that engine to CI or GitHub. Native-instruction probing requires the documented Linux compatibility-mode and C compiler setup.

## Code quality

- Keep coordinator policy separate from engine memory access and network transport.
- No unbounded waits in game UI callbacks.
- Version and authenticate control messages; reject stale epochs and duplicate commit IDs.
- Record source identity and support exact-build checks for native hooks.
- No hot-install, hot-remove or unknown-build patch attempts.
- Prefer documented upstream interfaces and propose generic hooks upstream rather than maintaining a permanent private binary fork.
