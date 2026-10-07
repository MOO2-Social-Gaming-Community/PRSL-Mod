#!/usr/bin/env python3
"""Stdlib-only integrity and honesty checks for PRSL handoff docs."""
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md", "STATUS.md", "CHANGELOG.md", "LICENSE-STATUS.md",
    "docs/STATUS.md", "docs/RD-HISTORY.md", "docs/ENGINE-RESEARCH.md",
    "docs/ARCHITECTURE.md", "docs/ROADMAP.md", "docs/ACCEPTANCE-TESTS.md",
    "docs/ORIGINAL-SOURCE-IMPORT.md", "docs/HANDOFF-SOURCES.md",
    "research/archive-v0.1.0/DESIGN.md",
    "research/archive-v0.2.0/README.md",
    "research/archive-v0.2.0/BINARY_REPORT.md",
    "research/archive-v0.2.0/TEST_METHOD.md",
    "research/archive-v0.2.0/target-map.json",
    "research/archive-v0.2.0/evidence/python-tests.log",
    "research/archive-v0.2.0/evidence/native-probe.log",
    "research/archive-v0.2.0/evidence/old-coordinator-regression.json",
    "research/archive-v0.2.0/evidence/installer-verify.json",
    "research/archive-v0.2.0/evidence/workspace-integration-tests.json",
    "reference/launcher/NETWORK-AND-PROFILES-0.4.7.md",
    "reference/launcher/REQUIREMENTS-0.1.0.md",
    "reference/launcher/TEST-REPORT-0.4.7.md",
    "tools/import_original_lab.py",
]
ENGINE_SHA256 = "2db296e052419250d21866f7c23ac2978a33b3c05b451a9516f06599b91c3f5c"


def run(root: Path = ROOT) -> list[str]:
    problems = []
    for path in REQUIRED:
        if not (root / path).is_file():
            problems.append(f"Missing expected document: {path}")
    if problems:
        return problems
    m = json.loads((root / "research/archive-v0.2.0/target-map.json").read_text(encoding="utf-8"))
    if m.get("engine_sha256") != ENGINE_SHA256:
        problems.append("Engine identity differs from original PRSL research snapshot")
    for name, status in m.get("capabilities", {}).items():
        if status is not False:
            problems.append(f"Historical capability improperly claimed enabled: {name}")
    if m.get("candidate", {}).get("original_bytes") != "e8407b0700":
        problems.append("Manual-hook candidate original bytes changed")
    if m.get("candidate", {}).get("offset") != 0x76D78:
        problems.append("Manual-hook candidate offset changed")
    tests = (root / "research/archive-v0.2.0/evidence/python-tests.log").read_text(encoding="utf-8")
    native = (root / "research/archive-v0.2.0/evidence/native-probe.log").read_text(encoding="utf-8")
    if "Ran 52 tests" not in tests or "OK" not in tests:
        problems.append("Missing historical 52-test run output")
    if "SUMMARY checks=30 failures=0 scope=isolated-x86-32-not-full-game" not in native:
        problems.append("Missing historical isolated x86 summary")
    readme = (root / "README.md").read_text(encoding="utf-8").lower()
    if "not yet" not in readme and "no live in-game" not in readme:
        problems.append("README must clearly disclose missing live integration")
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(p in {".git", ".venv", "__pycache__"} for p in path.parts):
            continue
        if path.suffix.lower() in {".exe", ".com", ".lbx", ".gam", ".sav", ".p12", ".pfx", ".pem", ".key", ".zip", ".7z"}:
            problems.append(f"Disallowed proprietary/sensitive binary/archive under repo: {path.relative_to(root)}")
    return problems


def main() -> int:
    problems = run()
    if problems:
        for p in problems:
            print("FAIL:", p)
        return 1
    print(f"PASS: handoff documents and research markers valid ({len(REQUIRED)} required artifacts)")
    if (ROOT / "lab" / "prsl" / "state.py").is_file():
        print("NOTICE: original lab source imported; its own tests still require separate execution")
    else:
        print("NOTICE: original v0.2.0 lab source NOT imported; no code/game validation claimed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
