# Recovered original PRSL Lab v0.2.0 source — provenance and re-import procedure

**Current status: successfully imported on 2026-10-07.** `lab/` contains the original 31-file Python/C/research tree. The source ZIP was supplied directly as an attachment named `moo2_prsl_lab_v0.2.0(1).zip` (upload-renamed; internal root is `moo2_prsl_lab_v0.2.0/`). Archive size 47,187 B; SHA-256 `2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e`. The importer was not modified to accept this archive.

`lab-import-provenance.json` records the exact ZIP digest, layout and import metadata. All 31 extracted files were checked against the original member bytes. In addition, the original Lab includes its own `SOURCE_SHA256SUMS.txt` covering 30 other files, which `tools/verify_lab_provenance.py` verifies. Retain this directory as an **immutable historical baseline**; develop new code and adapter experiments independently of this archive until a deliberate reviewed migration occurs.

## Reproducing the import from a pre-import snapshot (only)

The importer deliberately refuses to overwrite an existing `lab/` or `lab-import-provenance.json`. **Do not run it against this already integrated repository**. To reproduce, first obtain a *fresh copy of the original pre-import handoff* (SHA-256 `ece9cc49d6705da1fdaa787000643e26d44ae2d07bb7e71c07da155c9aa65647`), and place it in a separate scratch directory. Then:

```bash
python tools/import_original_lab.py --dry-run /path/to/moo2_prsl_lab_v0.2.0.zip
python tools/import_original_lab.py /path/to/moo2_prsl_lab_v0.2.0.zip
python tools/validate_handoff.py
python -m unittest discover -s tests -v
python -m pip install -r lab/requirements-lab.txt
(cd lab && python -m unittest discover -s tests -v)
```

The ZIP import safety policy checks expected source layout, rejects path escape, symlinks, disallowed file types, duplicates and oversized archives. It never executes imported files. Preserve original game media separately and never commit the ZIP, proprietary engine, patch archives or signing keys.

## Original layout

```text
lab/prsl/state.py              offline readiness coordinator
lab/prsl/binary150.py          exact-build LE/debug/relocation research
lab/prsl/lab_gate.py           synthetic x86 gate experiment
lab/prsl/packages.py           offline workspace verification
lab/prsl/cli.py                research CLI; `--mode prsl` fails closed
lab/prsl/updates.py            offline signature/freshness checks
lab/tests/                     original tests (52 discovered)
lab/tools/native_probe.c       isolated instruction probe; not DOSBox
lab/tools/run_native_probe.py  Linux toolchain wrapper
lab/research/                   exact-engine research records
lab/evidence/                   ORIGINAL historical test results
lab/SOURCE_SHA256SUMS.txt       per-member hash list
```

This import does NOT create a live game patch, implement the pre-game lobby, or establish any engine or LAN validation. Native memory addresses must be resolved from the *loaded* image after verifying exact engine identity; do not translate object/file offsets mechanically.
