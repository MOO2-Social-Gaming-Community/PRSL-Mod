#!/usr/bin/env python3
"""Verify the original PRSL Lab 0.2.0 source tree was imported unchanged.

This verification checks the *extracted source*, not the original ZIP (which
is intentionally not shipped in the repository). The imported archive digest
is recorded and pinned to prevent quiet source substitution.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

REPO = Path(__file__).resolve().parents[1]
EXPECTED_ZIP_SHA256 = "2042783f391e635fd0db62ccd5a87a20b5350050afa8d8f9e739abb285e8904e"
EXPECTED_SUMS_SHA256 = "ea1788762d6ab854537c1aa3b7082c3c5174ee6f4b5f9026ffa2e6acc639acfa"
EXPECTED_SIZE = 47_187
EXPECTED_MEMBERS = 31
EXPECTED_UNCOMPRESSED_SIZE = 112_327
RECORD_RE = re.compile(r"([0-9a-f]{64})  (.+)")


def checksum(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(repository: Path = REPO) -> list[str]:
    """Return problems, never modifying the immutable historical Lab tree."""
    errors: list[str] = []
    lab = repository / "lab"
    sums_file = lab / "SOURCE_SHA256SUMS.txt"
    provenance_file = repository / "lab-import-provenance.json"
    if not lab.is_dir() or not sums_file.is_file() or not provenance_file.is_file():
        return ["Missing original Lab tree, original checksums, or import provenance"]
    if checksum(sums_file) != EXPECTED_SUMS_SHA256:
        errors.append("Original SOURCE_SHA256SUMS.txt checksum changed")
        return errors
    try:
        meta = json.loads(provenance_file.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        return [f"Import provenance invalid: {exc}"]
    expected_meta = {
        "historical_source_version": "0.2.0",
        "source_sha256": EXPECTED_ZIP_SHA256,
        "source_bytes": EXPECTED_SIZE,
        "imported_files": EXPECTED_MEMBERS,
        "uncompressed_bytes": EXPECTED_UNCOMPRESSED_SIZE,
        "archive_prefix": "moo2_prsl_lab_v0.2.0",
    }
    for key, expected in expected_meta.items():
        if meta.get(key) != expected:
            errors.append(f"Import provenance {key!r} mismatch: {meta.get(key)!r}")
    expected_files: set[str] = {"SOURCE_SHA256SUMS.txt"}
    total_bytes = sums_file.stat().st_size
    for line_no, line in enumerate(sums_file.read_text(encoding="utf-8").splitlines(), start=1):
        match = RECORD_RE.fullmatch(line)
        if not match:
            errors.append(f"Malformed checksum line {line_no}")
            continue
        digest, name = match.groups()
        rel = PurePosixPath(name)
        if (not rel.parts or rel.is_absolute() or
            any(x in ("..", ".") for x in rel.parts) or
            "\\" in name or ":" in name or name.startswith("/")):
            errors.append(f"Unsafe original checksum path {line_no}: {name!r}")
            continue
        if name in expected_files:
            errors.append(f"Duplicate manifest filename {name!r}")
            continue
        expected_files.add(name)
        target = lab.joinpath(*rel.parts)
        if not target.is_file() or target.is_symlink():
            errors.append(f"Missing/nonregular original source: {name}")
            continue
        total_bytes += target.stat().st_size
        if checksum(target) != digest:
            errors.append(f"Original source modified: {name}")
    actual = {
        str(q.relative_to(lab)).replace("\\", "/")
        for q in lab.rglob("*")
        if q.is_file() and "__pycache__" not in q.relative_to(lab).parts
    }
    extra = actual - expected_files
    missing = expected_files - actual
    if extra:
        errors.append(f"Extra untracked files in historical Lab: {sorted(extra)}")
    if missing:
        errors.append(f"Missing listed files in historical Lab: {sorted(missing)}")
    if len(expected_files) != EXPECTED_MEMBERS:
        errors.append(f"Expected {EXPECTED_MEMBERS} original files, found {len(expected_files)}")
    if total_bytes != EXPECTED_UNCOMPRESSED_SIZE:
        errors.append(f"Uncompressed Lab byte count mismatch: {total_bytes}")
    return errors


def main() -> int:
    problems = verify()
    if problems:
        for problem in problems:
            print("FAIL:", problem)
        return 1
    print(
        "PASS: Lab v0.2.0 import provenance pinned; "
        "31/31 original files intact, 30/30 listed-member SHA-256 hashes match"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
