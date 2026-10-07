# GitHub repository handoff checklist

## You can commit the documentation handoff now

- [ ] Open the newly created PRSL repository with GitHub Desktop and preserve its `.git` directory.
- [ ] Extract **the contents** of `MOO2-SGC-PRSL-GitHub-Handoff-2026-10-07.zip` into that clone's root (rather than nesting a second repository folder).
- [ ] Read `STATUS.md`: original 0.2.0 code not present in the handoff ZIP, game integration not yet playable.
- [ ] Run `py -3 tools\validate_handoff.py` and `py -3 -m unittest discover -s tests -v` if Python is installed.
- [ ] Commit as **documentation/source-recovery handoff**, NOT a functioning PRSL mod release.

## Import real code before feature development

- [ ] Locate and download **`moo2_prsl_lab_v0.2.0.zip`** (the separate 47,187-byte lab archive) from the earlier project Library/conversation.
- [ ] Run `py -3 tools\import_original_lab.py --dry-run "C:\path\to\moo2_prsl_lab_v0.2.0.zip"` then the command again without `--dry-run`.
- [ ] Review `lab/` and `lab-import-provenance.json` for authorship, license, safe files and archive identity.
- [ ] Run the original `lab/` test suite. Do not upload a licensed engine or patch to GitHub or CI.
- [ ] Commit the historical lab source intact, preferably as a separate provenance commit; do not call it new executable functionality.
- [ ] Open the research/adapter tasks in `docs/ISSUE-BACKLOG.md`.

## Before any playable PRSL release

- [ ] Obtain a validated live engine adapter and all turn pathways.
- [ ] Implement/validate authenticated coordinator, in-game readiness UI and native safe-point release.
- [ ] Verify on two actual independent game clients with full regression and failure coverage.
- [ ] Pin supported versions and create a fail-closed launcher integration and signed package.
- [ ] Confirm project/source license and redistribution rights.
- [ ] Publish explicit supported OS/profile/version matrix and rollback procedure.

In the meantime the ordinary MOO2-SGC launcher and Community 1.50.26 profile remain the known separate path; PRSL is research-only.
