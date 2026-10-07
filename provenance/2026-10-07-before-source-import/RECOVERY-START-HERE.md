# PRSL source-recovery package — start here

**This is an expanded audit of the 2026-10-07 handoff, NOT a playable game mod and NOT an import of the original v0.2.0 Lab implementation.**

- Original handoff: `HANDOFF-MANIFEST.json`, with all 41 original checksums preserved.
- New discovery record: [`docs/RECOVERY-AUDIT-2026-10-07.md`](docs/RECOVERY-AUDIT-2026-10-07.md).
- Machine-readable original archive inventory: [`docs/RECOVERY-ARCHIVES-INDEX.json`](docs/RECOVERY-ARCHIVES-INDEX.json).
- Existing safe original source importer: [`tools/import_original_lab.py`](tools/import_original_lab.py).

**Recovery blocker:** The exact `moo2_prsl_lab_v0.2.0.zip` is present as a named Library record under `/Master of Orion 2/`, but its raw bytes could not be copied into this project runtime. Download it from Library and attach directly to this conversation; only then can we import and test original Python/C source.

To import the 0.2.0 source after obtaining the ZIP:

```powershell
py -3 tools/import_original_lab.py --dry-run "C:\path\to\moo2_prsl_lab_v0.2.0.zip"
py -3 tools/import_original_lab.py "C:\path\to\moo2_prsl_lab_v0.2.0.zip"
py -3 tools/validate_handoff.py
py -3 -m unittest discover -s tests -v
```

No original game binaries, patch ZIPs, DOSBox runtime, credentials, or original PRSL Lab ZIPs are in this package. The historical source archives should not be committed wholesale to a public PRSL repository.
