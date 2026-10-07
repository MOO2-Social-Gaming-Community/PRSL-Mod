# Contributing to PRSL research

This is a pre-alpha game-integration research project. Changes must be narrow, reversible, tested and explicit about their evidence level.

## Before working

Read `STATUS.md`, `docs/ARCHITECTURE.md`, `docs/ENGINE-RESEARCH.md`, `docs/ROADMAP.md`. Original Lab v0.2.0 is **already recovered** in `lab/`: do not edit or reformat these files. Their SHA-256 fingerprints are checked against the original archive's manifest; prefer new development and tests outside `lab/` until a separately reviewed port is ready.

Use a fresh branch for one narrowly scoped experiment or defect fix. Never commit game executables, copyright-protected LBX assets, patch archives, saves, signing keys, locally generated workspaces, diagnostic PII or private endpoints.

## Required pull request evidence

Specify the changed module, exact MOO2 executable hash if relevant, test commands, results, skipped validations, recovery/rollback behavior, and unknowns. Never collapse file-structure tests, x86 instructions, emulator gameplay and actual two-client acceptance into a single claim.

## Offline test commands

```bash
python -m pip install -r lab/requirements-lab.txt
python tools/verify_lab_provenance.py
python tools/validate_handoff.py
python -m unittest discover -s tests -v
(cd lab && python -m unittest discover -s tests -v)
```

The final suite has nine expected skips without `MOO2_ENGINE`. Run them only with your own exact matching game executable kept outside the repository. The native instruction probe is separate and Linux-specific; it is not a game test. The Launcher, lobby, optional Chat, SCG Quickplay and Tournament Mod are separately maintained components.

## Core PRSL requirements

Keep coordinator policy independent of game memory access and transport. Never block the native game UI callback, modify unrecognized engine hashes, bypass RNG/network wrappers, reuse stale stack pointers, or schedule arbitrary host-thread native execution. Original submission must be observed separately from PRSL commit acknowledgement. Preserve normal engine behavior with PRSL disabled.
