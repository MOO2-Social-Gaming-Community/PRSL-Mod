"""Tests for handoff source-import boundary. Synthetic archives only."""
from __future__ import annotations

import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from zipfile import ZipFile, ZipInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from import_original_lab import EXPECTED, ImportRejected, import_archive
from validate_handoff import run as validate_handoff


class ImporterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        (self.repo / "docs").mkdir(parents=True)
        (self.repo / "docs" / "ORIGINAL-SOURCE-IMPORT.md").write_text("test", encoding="utf-8")
        self.archive = self.root / "moo2_prsl_lab_v0.2.0.zip"

    def _create(self, extra=None, prefix=""):
        names = {f"{prefix}{name}": b"# synthetic source\n" for name in EXPECTED}
        names[f"{prefix}tests/test_state.py"] = b"# synthetic test\n"
        if extra:
            names.update(extra)
        with ZipFile(self.archive, "w") as z:
            for name, data in names.items():
                z.writestr(name, data)

    def test_valid_source_import(self):
        self._create(prefix="prsl-lab-0.2.0/")
        p = import_archive(self.archive, self.repo)
        self.assertEqual(p["historical_source_version"], "0.2.0")
        self.assertTrue((self.repo / "lab" / "prsl" / "state.py").is_file())
        self.assertEqual((self.repo / "lab" / "prsl" / "state.py").read_bytes(), b"# synthetic source\n")
        self.assertEqual(json.loads((self.repo / "lab-import-provenance.json").read_text())["source_sha256"], p["source_sha256"])

    def test_dry_run_writes_nothing(self):
        self._create()
        result = import_archive(self.archive, self.repo, dry_run=True)
        self.assertGreater(result["imported_files"], 10)
        self.assertFalse((self.repo / "lab").exists())

    def test_reject_existing_lab(self):
        self._create()
        (self.repo / "lab").mkdir()
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)

    def test_reject_traversal(self):
        self._create(extra={"../outside.py": b"x"})
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)
        self.assertFalse((self.repo / "lab").exists())

    def test_reject_drive_name(self):
        self._create(extra={"C:/wrong.py": b"x"})
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)

    def test_reject_executable(self):
        self._create(extra={"game/ORION150.EXE": b"not MOO2"})
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)

    def test_reject_duplicate_casefold(self):
        self._create(extra={"prsl/STATE.py": b"evil"})
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)

    def test_reject_symlink(self):
        self._create()
        with ZipFile(self.archive, "a") as z:
            info = ZipInfo("bad-link.md")
            info.create_system = 3
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            z.writestr(info, b"/tmp/other")
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)

    def test_reject_missing_source_members(self):
        with ZipFile(self.archive, "w") as z:
            z.writestr("README.md", "not sufficient")
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)

    def test_reject_archive_outside_root(self):
        self._create(extra={"another/top.md": b"mix"}, prefix="the-prsl-lab/")
        with self.assertRaises(ImportRejected):
            import_archive(self.archive, self.repo)

    def test_repository_validator_passes(self):
        self.assertFalse(validate_handoff(Path(__file__).resolve().parents[1]))


if __name__ == "__main__":
    unittest.main()
