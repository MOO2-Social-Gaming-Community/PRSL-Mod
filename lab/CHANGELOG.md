# Changelog

## 0.2.0 — October 4, 2026

- Mapped retained debug records to the exact 1.50.26 LE objects and file offsets.
- Corrected `Human_Hit_Next_Turn_`: native-finished flag getter, not turn submission.
- Traced the main-screen `_next_button` event, a second `Do_Begin_Of_Turn_` call, caller-owned stack-local output, native finished-flag write, and community RNG-snapshot wrapper.
- Reconstructed LE and community extension relocations; checked the extension reconstruction by executing the original relocation loop in an isolated compatibility-mode harness.
- Added an in-memory laboratory gate before main-screen turn side effects, with deferral, permission, pass-through, and fresh-frame tests.
- Fixed the coordinator's repeated-READY / GRACE safety bug; added disconnect handling and fail-closed post-commit fault behavior.
- Added pinned owned-archive staging, file verification, community launch configuration, and refusal to launch an uncertified PRSL adapter.
- Added offline Ed25519 catalog checking and local version/capability eligibility tests. No network auto-updater, production keys, or graphical launcher yet.
- Final evidence: 52 Python tests, 30 isolated machine-code checks, 6 actual-workspace checks; fresh 944-file install; zero original files changed.
- Explicitly **no full-game/DOSBox/IPX validation** and no live deployable adapter.
