# Import the original PRSL Lab v0.2.0 source

## Why there is an import step

The original `moo2_prsl_lab_v0.2.0.zip` is present in the user's earlier project file history (47,187 bytes, created 2026-10-05 UTC). The current file service exposed its title and metadata, **but not a raw ZIP extraction path**. We retrieved and preserved separate text versions of its README, binary research report, target map, test-method file, and five logs. **The original `.py` and `.c` sources are NOT included in this handoff**, and cannot honestly be recreated as byte-identical files from the README alone.

To continue the *existing implementation*, import that original archive. Avoid starting from a new, similar-looking coordinator and losing the tested behavior or subtle fixes.

## Procedure

1. Download `moo2_prsl_lab_v0.2.0.zip` from the project's older conversation/Library files. Confirm you obtained the lab ZIP and **not** a game archive (`Master of Orion 2.zip`) or community patch package.
2. Clone the new PRSL GitHub repository (or open its existing working directory). Extract the *handoff ZIP* there, **preserving `.git`**. Do not extract inside a second nested repo directory.
3. Ensure Python 3.11+ is installed, then in the repository root run:

   ```powershell
   py -3 tools\import_original_lab.py "C:\path\to\moo2_prsl_lab_v0.2.0.zip"
   ```

   For a check without writing files:

   ```powershell
   py -3 tools\import_original_lab.py --dry-run "C:\path\to\moo2_prsl_lab_v0.2.0.zip"
   ```

4. The command will create `lab/` and a `lab-import-provenance.json` file after verifying archive layout, safety limits and expected PRSL source members. It never runs imported code. It refuses to replace a nonempty `lab/` or overwrite prior provenance.
5. Inspect the files for correct source attribution, license notices and malicious/surprising content. Do not upload any local game binaries or private signing material.
6. Run these tests and **label their scope**:

   ```powershell
   py -3 tools\validate_handoff.py
   py -3 -m unittest discover -s tests -v
   cd lab
   py -3 -m pip install -r requirements-lab.txt
   py -3 -m unittest discover -s tests -v
   ```

   Optional exact-engine tests require the user-owned `ORION150.EXE` of the pinned hash supplied as `MOO2_ENGINE` locally. The native compatibility-mode probe requires Linux x86-64/GCC and cannot be treated as a Windows test.
7. Commit imported source and `lab-import-provenance.json` to the PRSL repository only after inspection. The source archive itself belongs in private offline provenance storage, **not** in public Git.

## Expected source tree

Based on the **historical v0.2.0 README**, the original archive is expected to contain at least:

```text
prsl/binary150.py
prsl/lab_gate.py
prsl/state.py
prsl/packages.py
prsl/cli.py
prsl/updates.py
tools/native_probe.c
tools/run_native_probe.py
tests/...
research/target-map.json
README.md
requirements-lab.txt
```

This list comes from the older README; the handoff could not inspect raw ZIP members. The importer may reject a different layout, in which case **inspect manually rather than disabling its safety checks**. No accepted SHA-256 for the source ZIP has been measured here.

## Merge strategy

Import intact source into **`lab/`** rather than overwriting the new repo's root README or current documentation. This preserves the historical lab CLI (`python -m prsl.cli`) and test imports. Once the real implementation has been inspected, refactor gradually into production `src/` modules while preserving regression tests and version history. Retain the imported lab as a reproducible historical baseline until formally retired.

## What this handoff does NOT do

- It does not import source from the non-PRSL launcher ZIP.
- It does not provide an executable game patch or memory injection.
- It does not download commercial game files or put them in Git.
- It does not prove live 1.50.26 multiplayer or any Windows/macOS runtime compatibility.
- It does not choose a license or assert upstream approval.
