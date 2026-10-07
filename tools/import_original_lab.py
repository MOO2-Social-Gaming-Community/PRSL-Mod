#!/usr/bin/env python3
"""Fail-closed import of the ORIGINAL archived PRSL Lab v0.2.0 ZIP.

The archive is NOT shipped in this repository. This tool copies its source
without executing it, into a separate `lab/` directory. It refuses to overwrite.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import tempfile
from zipfile import ZipFile, BadZipFile

MAX_FILES = 2_000
MAX_MEMBER_BYTES = 12 * 1024 * 1024
MAX_TOTAL_BYTES = 48 * 1024 * 1024
MAX_RATIO = 1_000
ALLOWED_SUFFIXES = {
    ".py", ".pyi", ".c", ".h", ".md", ".markdown", ".txt", ".log",
    ".json", ".jsonl", ".toml", ".ini", ".cfg", ".yaml", ".yml",
    ".sh", ".cmd", ".bat", ".gitignore", ".gitkeep", ".rst", ".csv",
}
EXPECTED = {
    "README.md", "prsl/state.py", "prsl/binary150.py",
    "prsl/lab_gate.py", "prsl/packages.py", "prsl/cli.py",
    "prsl/updates.py", "tools/native_probe.c",
    "tools/run_native_probe.py", "research/target-map.json",
    "requirements-lab.txt",
}
WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


class ImportRejected(ValueError):
    """The archive or requested destination failed the import policy."""


def _clean_parts(filename: str) -> tuple[str, ...]:
    # ZIP internally uses POSIX separators; backslashes may escape on Windows.
    if not filename or "\\" in filename or "\x00" in filename:
        raise ImportRejected(f"Invalid archive member name: {filename!r}")
    if filename.startswith("/") or filename.startswith("//"):
        raise ImportRejected(f"Absolute archive member: {filename!r}")
    path = PurePosixPath(filename)
    parts = path.parts
    if not parts or any(p in {".", "..", ""} for p in parts):
        raise ImportRejected(f"Relative traversal/dot path: {filename!r}")
    for part in parts:
        if ":" in part or any(ord(c) < 32 for c in part):
            raise ImportRejected(f"Invalid archive path component: {filename!r}")
        if part.endswith(" ") or part.endswith("."):
            raise ImportRejected(f"Windows-ambiguous trailing name: {filename!r}")
        if part.split(".")[0].upper() in WINDOWS_RESERVED:
            raise ImportRejected(f"Windows reserved path name: {filename!r}")
        if part == ".git" or part == ".github":
            raise ImportRejected(f"Repository metadata forbidden in historical lab: {filename!r}")
    return parts


def _reject_type(info) -> None:
    mode = (info.external_attr >> 16) & 0xFFFF
    if stat.S_IFMT(mode) in (stat.S_IFLNK, stat.S_IFCHR, stat.S_IFBLK, stat.S_IFIFO, stat.S_IFSOCK):
        raise ImportRejected(f"Non-regular archive member: {info.filename}")
    if info.flag_bits & 1:
        raise ImportRejected(f"Encrypted archive member: {info.filename}")


def _discover_prefix(names: list[tuple[str, ...]]) -> tuple[str, ...]:
    prefixes = set()
    for p in names:
        for i in range(len(p) - 1):
            if p[i:] == ("prsl", "state.py"):
                prefixes.add(p[:i])
    if len(prefixes) != 1:
        raise ImportRejected("Could not uniquely find prsl/state.py (expected v0.2.0 source tree)")
    return next(iter(prefixes))


def inspect_archive(archive: Path) -> tuple[list[tuple[object, tuple[str, ...]]], dict]:
    """Validate ZIP members, return safe mapping and immutable provenance."""
    if not archive.is_file():
        raise ImportRejected(f"Source ZIP does not exist: {archive}")
    with archive.open("rb") as archive_stream:
        archive_hash = hashlib.file_digest(archive_stream, "sha256").hexdigest()
    try:
        with ZipFile(archive, "r") as zf:
            members = zf.infolist()
            if not 0 < len(members) <= MAX_FILES:
                raise ImportRejected(f"Unexpected number of ZIP members: {len(members)}")
            data_members = []
            total = 0
            for info in members:
                parts = _clean_parts(info.filename.rstrip("/"))
                _reject_type(info)
                if info.is_dir():
                    continue
                if Path(parts[-1]).suffix.lower() not in ALLOWED_SUFFIXES and parts[-1] not in {".gitignore", ".gitkeep"}:
                    raise ImportRejected(f"Unapproved source/archive file type: {info.filename}")
                if info.file_size > MAX_MEMBER_BYTES:
                    raise ImportRejected(f"ZIP member too large: {info.filename}")
                if info.file_size > 100_000 and info.file_size / max(1, info.compress_size) > MAX_RATIO:
                    raise ImportRejected(f"Suspicious compression ratio: {info.filename}")
                total += info.file_size
                if total > MAX_TOTAL_BYTES:
                    raise ImportRejected("Archive exceeds research source size limit")
                data_members.append((info, parts))
            prefix = _discover_prefix([parts for _, parts in data_members])
            transformed = []
            casefolded = set()
            for info, parts in data_members:
                if parts[:len(prefix)] != prefix:
                    raise ImportRejected(f"Files mixed outside expected archive root: {info.filename}")
                rel = parts[len(prefix):]
                if not rel:
                    raise ImportRejected("Empty relative filename")
                folded = "/".join(rel).casefold()
                if folded in casefolded:
                    raise ImportRejected(f"Duplicate/case-colliding archive member: {info.filename}")
                casefolded.add(folded)
                transformed.append((info, rel))
            present = {"/".join(rel) for _, rel in transformed}
            missing = sorted(EXPECTED - present)
            if missing or not any(p.startswith("tests/") and p.endswith(".py") for p in present):
                raise ImportRejected(f"Archive does not contain expected v0.2.0 source: missing {missing}, or missing Python tests")
            metadata = {
                "schema": 1,
                "historical_source_version": "0.2.0",
                "source_filename": archive.name,
                "source_sha256": archive_hash,
                "source_bytes": archive.stat().st_size,
                "imported_files": len(transformed),
                "uncompressed_bytes": total,
                "archive_prefix": "/".join(prefix),
                "note": "Exact original ZIP members copied without code execution. This is source import, NOT multiplayer certification.",
            }
            return transformed, metadata
    except BadZipFile as exc:
        raise ImportRejected(f"Invalid ZIP: {exc}") from exc


def import_archive(archive: Path, repository: Path, dry_run: bool = False) -> dict:
    repository = repository.resolve()
    if not (repository / "docs" / "ORIGINAL-SOURCE-IMPORT.md").is_file():
        raise ImportRejected(f"Not an initialized PRSL handoff repository: {repository}")
    lab = repository / "lab"
    provenance = repository / "lab-import-provenance.json"
    if lab.exists() or provenance.exists():
        raise ImportRejected("Existing lab/ or provenance detected; refusing overwrite. Use a fresh clone or review manually.")
    mapping, metadata = inspect_archive(archive.resolve())
    if dry_run:
        return metadata
    # Reopen only after validating; recheck the hash immediately before extraction.
    with tempfile.TemporaryDirectory(prefix=".prsl-lab-import-", dir=repository) as td:
        staging = Path(td) / "lab"
        staging.mkdir()
        with ZipFile(archive, "r") as zf:
            for info, rel in mapping:
                out = staging.joinpath(*rel)
                out.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(info, "r") as source, out.open("xb") as dest:
                    while True:
                        chunk = source.read(256 * 1024)
                        if not chunk:
                            break
                        dest.write(chunk)
        # Verify archive bytes didn't change between inspection and extraction.
        with archive.open("rb") as stream:
            now = hashlib.file_digest(stream, "sha256").hexdigest()
        if now != metadata["source_sha256"]:
            raise ImportRejected("Archive changed during import; discarding staging directory")
        # Exclusive provenance creation before atomic move; clean it on an error.
        try:
            with provenance.open("x", encoding="utf-8", newline="\n") as stream:
                json.dump(metadata, stream, indent=2, sort_keys=True)
                stream.write("\n")
            staging.rename(lab)
        except BaseException:
            provenance.unlink(missing_ok=True)
            raise
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safely import original PRSL Lab 0.2.0 ZIP, without executing source")
    parser.add_argument("archive", type=Path, help="Path to original moo2_prsl_lab_v0.2.0.zip")
    parser.add_argument("--repository", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = import_archive(args.archive, args.repository, dry_run=args.dry_run)
    except (ImportRejected, OSError) as exc:
        print(f"IMPORT REJECTED: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"dry_run": args.dry_run, **result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
