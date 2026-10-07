# Recovered PRSL source inventory and evidence

## Direct source recovery — completed 2026-10-07

- User-uploaded original Lab ZIP: `moo2_prsl_lab_v0.2.0(1).zip` (47,187 B), SHA-256 `2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e`.
- The safe handoff importer placed all 31 original members into [`lab/`](../lab/), preserving exact extracted member bytes. Full metadata are in [`lab-import-provenance.json`](../lab-import-provenance.json). No original ZIP is distributed here.
- [`lab/SOURCE_SHA256SUMS.txt`](../lab/SOURCE_SHA256SUMS.txt) contains original hashes for the 30 other files. Re-run `python tools/verify_lab_provenance.py` to check them and the imported archive provenance.
- [`docs/SOURCE-RESTORATION-2026-10-07.md`](SOURCE-RESTORATION-2026-10-07.md) describes current tests and blockers. The pre-import audit is retained unchanged under `provenance/2026-10-07-before-source-import/`; its conclusion that source bytes were unavailable is now superseded.

## Other preserved research

| New path | Origin / scope |
|---|---|
| `research/archive-v0.1.0/DESIGN.md` | Earlier project design text, not executable source |
| `research/archive-v0.2.0/README.md`, `BINARY_REPORT.md`, `TEST_METHOD.md`, `target-map.json` | Prior text renditions of Lab v0.2 research, now supplemented by **actual original files** under `lab/` |
| `research/archive-v0.2.0/evidence/` | Historical test-log text snapshots; original logs also under `lab/evidence/` |
| `reference/launcher/` | Launcher boundary and 0.4.7 references (not PRSL source) |

The originals of `moo2_prsl_lab_v0.1.0.zip` (13,366 B) and `MOO2_PRSL_Research_Design_v0.1.0.zip` (20,694 B) were located in Library but have **not** been imported as binary source archives. The v0.2.0 package contains v0.1 regression evidence and the subsequent coordinator fix; earlier ZIPs remain optional historical provenance.

## Third-party/exact-engine limitations

The actual `ORION150.EXE` 1.50.26 game binary was not supplied to this recovery; therefore all nine engine-structural tests were skipped, as expected. No game, launcher binary, community patch, DOSBox or original ZIP archive is stored in the PRSL repository. The Lab's stored native-probe and workspace-build results remain historical evidence, not newly reproduced claims.

Link to the dedicated repository: https://github.com/MOO2-Social-Gaming-Community/PRSL-Mod . GitHub upload/push still requires access from the user or an authorized connector; this source package alone is not a remote commit.
