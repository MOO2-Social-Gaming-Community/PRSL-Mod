"""Regression protection for the *immutable* recovered PRSL Lab source."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify_lab_provenance", ROOT / "tools" / "verify_lab_provenance.py")
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class SourceRecoveryIntegrityTests(unittest.TestCase):
    def test_actual_restoration_passes(self):
        self.assertEqual(module.verify(ROOT), [])

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.testroot = Path(self.temporary.name)
        shutil.copytree(ROOT / "lab", self.testroot / "lab", ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(ROOT / "lab-import-provenance.json", self.testroot / "lab-import-provenance.json")

    def test_modified_source_is_caught(self):
        with (self.testroot / "lab" / "prsl" / "state.py").open("a", encoding="utf-8") as out:
            out.write("\n# tampered\n")
        self.assertIn("Original source modified: prsl/state.py", module.verify(self.testroot))

    def test_removed_file_is_caught(self):
        (self.testroot / "lab" / "prsl" / "lab_gate.py").unlink()
        self.assertTrue(any("lab_gate.py" in m for m in module.verify(self.testroot)))

    def test_extra_file_is_caught(self):
        (self.testroot / "lab" / "unexpected.txt").write_text("new content")
        self.assertTrue(any("Extra untracked files" in m for m in module.verify(self.testroot)))

    def test_forged_zip_provenance_is_caught(self):
        provenance = self.testroot / "lab-import-provenance.json"
        data = json.loads(provenance.read_text(encoding="utf-8"))
        data["source_sha256"] = "0" * 64
        provenance.write_text(json.dumps(data), encoding="utf-8")
        self.assertTrue(any("source_sha256" in m for m in module.verify(self.testroot)))

    def test_changed_sum_file_is_caught(self):
        with (self.testroot / "lab" / "SOURCE_SHA256SUMS.txt").open("a", encoding="utf-8") as out:
            out.write("\n")
        self.assertIn("Original SOURCE_SHA256SUMS.txt checksum changed", module.verify(self.testroot))


if __name__ == "__main__":
    unittest.main()
