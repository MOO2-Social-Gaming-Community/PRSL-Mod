# Source-integrated PRSL repository — publication and testing checklist

## Already completed in this package (2026-10-07)

- [x] Original PRSL Lab v0.2.0 archive supplied and SHA-256 measured.
- [x] Safe import completed into `lab/`; all 31 members compared byte-for-byte with original archive.
- [x] Original source hash manifest confirmed; current provenance verifier included.
- [x] Original 52 Lab Python tests rerun: 43 pass / 9 engine-dependent skips (Python 3.13.5/Linux).
- [x] Original 11 handoff/importer tests rerun successfully; 6 new provenance tests passed (17 total).
- [x] Pre-import audit/manifests preserved separately under `provenance/`.
- [x] CI extended to run both repo and offline Lab tests (CI execution itself awaits push).

## Publish the repository snapshot (manual/user-authorized GitHub action)

- [ ] Open the existing `https://github.com/MOO2-Social-Gaming-Community/PRSL-Mod` clone with GitHub Desktop.
- [ ] **Inspect existing tracked files and local changes before copying** the *contents* of this repository ZIP into the clone root. Preserve `.git` and merge instead of blindly overwriting a nonempty existing repository.
- [ ] Review new Lab source and rights/notice status; choose a project license as appropriate for public distribution. Do not assume an upstream license transfers rights automatically.
- [ ] Run `python tools/verify_lab_provenance.py`, `python tools/validate_handoff.py`, repository tests, and `lab/` tests locally.
- [ ] Commit the source-integrated snapshot as **historical v0.2.0 Lab recovered**; do not tag it as PRSL v0.3.0 gameplay mod.
- [ ] Push and confirm GitHub Actions green; inspect report of 9 expected engine-dependent skips.
- [ ] Never push original source ZIP, game executables, patch ZIPs, saves, runtime payloads or private keys.

## Before any playable PRSL release

- [ ] Certified read-only loaded-engine observation and coverage of every End Turn path.
- [ ] Safe local Ready/Unready interception and once-only native release.
- [ ] Authenticated multiplayer barrier across two independent real game clients.
- [ ] Game-side UI/loop fidelity, save/reconnect/failure rollback, desync-negative testing.
- [ ] Signed, independently versioned, fail-closed launcher integration.
- [ ] Legal/license review plus an explicit OS/engine/patch compatibility matrix.

Current PRSL mode must remain disabled. Native community MOO2 gameplay remains separately available.
