# MOO2-SGC PRSL-Mod — source-restored repository update

**Target repository:** https://github.com/MOO2-Social-Gaming-Community/PRSL-Mod

**This is the source recovery snapshot, not a playable in-game PRSL release.** It is a working-tree ZIP without `.git` and has **not** been pushed. The original Lab v0.2.0 source is intact under `lab/`.

## Using GitHub Desktop on Windows

1. Open **GitHub Desktop → File → Clone repository** and select `MOO2-Social-Gaming-Community/PRSL-Mod`. If already cloned, open that copy instead.
2. **Check any current changes and existing files**. Make a backup or new branch if the repository already contains work. The archive is intended to populate a repository root; it should not automatically erase a different version of PRSL.
3. Extract the **contents** of the delivered repository ZIP into the repository's local folder (the folder containing `.git` if cloned). Confirm `README.md`, `lab/prsl/state.py`, `tests/`, and `.github/workflows/checks.yml` are at the root — **not** under an extra nested directory.
4. Inspect the changes in GitHub Desktop. Do **not** commit or upload the user-owned `ORION150.EXE`, MOO2 game/patch archives, DOSBox bundles, original source ZIP, signing keys, personal saves or workspaces. `.gitignore` filters common extensions; review everything even so.
5. If Python 3.11+ is available, run the offline checks from the project root:

   ```powershell
   py -3 -m pip install -r lab/requirements-lab.txt
   py -3 tools/verify_lab_provenance.py
   py -3 tools/validate_handoff.py
   py -3 -m unittest discover -s tests -v
   Push-Location lab
   py -3 -m unittest discover -s tests -v
   Pop-Location
   ```

   Without your **local, legitimately obtained, exact engine executable**, the historical Lab suite should show **43 passes and nine skips**, not 52 passes.
6. After source/rights review, commit with a message like `Recover original PRSL Lab 0.2.0 source and provenance`, then **Push origin**. Check GitHub Actions after the push. CI checks only offline tests and does not certify live gameplay.

## What comes next

Keep `lab/` unchanged as historical R&D. The next real engineering milestone is a **read-only guest-engine observation adapter** for exact MOO2 1.50.26, followed by exhaustive native End Turn pathway tracing. Do not enable the unfinished PRSL toggle in the separate Launcher.

**Licensing:** `LICENSE-STATUS.md` still identifies an outstanding authorship/license/redistribution review. Public repository visibility is not an upstream license grant; decide and document terms before making claims about broad redistribution or external contributions.
