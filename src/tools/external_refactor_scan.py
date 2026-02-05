#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""
Safe scanner for `.external` repository snapshots.
- Reads `.external/tracking.md` and extracts completed/integrated table rows.
- Builds a per-directory candidate list of files and exported functions/classes.
- Does NOT execute any external code; it only reads and regex-parses files.
- Produces `.external/refactor_report.md` and `.external/refactor_report.json`.

Usage (PowerShell):
python -m src.tools.external_refactor_scan

Run only after reviewing and ensuring safety.
"""

from __future__ import annotations
import os
import re
import json
from pathlib import Path
from typing import List, Dict

ROOT = Path(__file__).resolve().parents[2]
EXTERNAL = ROOT / ".external"
SRC = ROOT / "src"

# Toggle verbose output for scanning
VERBOSE = True

ROW_RE = re.compile(r"^\|\s*(?P<name>[^|]+)\s*\|\s*(?P<status>[^|]+)\s*\|(?P<rest>.*)$")
DEF_RE = re.compile(r"^\s*(?:def|class)\s+(?P<name>[A-Za-z_][A-Za-z0-9_]+)")

# Only inspect these textual extensions (whitelist)
WHITELIST_EXTENSIONS = (".py", ".md", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".txt")

# Top-level directory names or path fragments to skip entirely (case-insensitive)
EXCLUDE_DIRS = ("system", "system/library", "node_modules", "__pycache__", "target", "build", "dist", ".git", "vendor", "bin")


def extract_completed_from_tracking(tracking_path: Path) -> List[str]:
    if not tracking_path.exists():
        return []
    completed_rows = []
    with tracking_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            m = ROW_RE.match(line)
            if not m:
                continue
            status = m.group("status").lower()
            if "integrated" in status or "completed" in status or "done" in status:
                completed_rows.append(line.rstrip())
    return completed_rows


def scan_directory_for_candidates(dirpath: Path) -> Dict:
    report = {"path": str(dirpath.relative_to(EXTERNAL)), "files": []}
    if VERBOSE:
        print(f"Scanning directory: {dirpath.relative_to(EXTERNAL)}")
    if not dirpath.is_dir():
        return report
    # If the directory path contains any excluded fragment, skip it entirely and report as pruned
    rel_dir = str(dirpath.relative_to(EXTERNAL)).lower()
    if any(excl in rel_dir for excl in EXCLUDE_DIRS):
        if VERBOSE:
            print(f"  Pruned dir: {dirpath.relative_to(EXTERNAL)}")
        return report
    # Use os.walk with topdown=True so we can prune directories early
    for root, dirs, files in os.walk(dirpath, topdown=True):
        # prune directories that match EXCLUDE_DIRS to avoid descending
        pruned = []
        for d in list(dirs):
            full = os.path.join(root, d)
            rel_full = os.path.relpath(full, EXTERNAL).replace("\\", "/").lower()
            if any(excl in rel_full for excl in EXCLUDE_DIRS):
                pruned.append(d)
                dirs.remove(d)
        if VERBOSE and pruned:
            for pd in pruned:
                print(f"  Pruned dir: {Path(root).relative_to(EXTERNAL) / pd}")

        for fname in files:
            p = Path(root) / fname
            if not p.is_file():
                continue
            # Skip very large files to avoid long blocking reads (skip >2MB)
            # fast stat; if it fails just skip silently
            try:
                size = p.stat().st_size
            except Exception:
                continue
            # Skip very large files to avoid long blocking reads (skip >2MB)
            if size > 2_000_000:
                continue

            # Only inspect textual files by extension to avoid binaries
            suffix = p.suffix.lower()
            if suffix not in WHITELIST_EXTENSIONS:
                continue

            # Read file content; don't print per-file skips. Only report files that contain defs.
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            defs = DEF_RE.findall(text)
            if defs:
                if VERBOSE:
                    print(f"  Found definitions in: {p.relative_to(EXTERNAL)} -> {defs[:5]}")
                report["files"].append({"path": str(p.relative_to(EXTERNAL)), "suffix": suffix, "definitions": defs[:20]})
    return report


def is_definition_in_src(name: str, src_root: Path) -> bool:
    # Fast grep-like search without importing; searches for 'def name(' or 'class name'
    pattern = re.compile(rf"\b(def|class)\s+{re.escape(name)}\b")
    for p in src_root.rglob("*.py"):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if pattern.search(txt):
            return True
    return False


def build_reuse_report(external_root: Path, src_root: Path) -> Dict:
    report = {"summary": {}, "directories": []}
    for d in sorted(external_root.iterdir()):
        if not d.is_dir():
            continue
        dir_report = scan_directory_for_candidates(d)
        # mark definitions which are NOT present in src
        for f in dir_report["files"]:
            missing = []
            for name in f.get("definitions", []):
                if not is_definition_in_src(name, src_root):
                    missing.append(name)
            f["missing_in_src"] = missing
        report["directories"].append(dir_report)
    return report


def write_reports(report: Dict, md_path: Path, json_path: Path):
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines: List[str] = ["# External Refactor Report\n", "This report is auto-generated. Do not run any code found here without manual review.\n\n"]
    for d in report.get("directories", []):
        lines.append(f"## {d['path']}\n")
        for f in d.get("files", []):
            defs = f.get("definitions", [])
            missing = f.get("missing_in_src", [])
            lines.append(f"- {f['path']} ({f['suffix']}) — defs: {', '.join(defs[:5]) or 'none'}; missing in src: {len(missing)}\n")
        lines.append("\n")
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    tracking = EXTERNAL / "tracking.md"
    completed = EXTERNAL / "completed.md"
    completed_rows = extract_completed_from_tracking(tracking)
    if completed_rows:
        with completed.open("a", encoding="utf-8", errors="ignore") as f:
            f.write("\n".join(completed_rows) + "\n")
    # Build reuse report
    report = build_reuse_report(EXTERNAL, SRC)
    write_reports(report, EXTERNAL / "refactor_report.md", EXTERNAL / "refactor_report.json")
    print(f"Wrote report: {EXTERNAL / 'refactor_report.md'} and refactor_report.json")
    print(f"Appended {len(completed_rows)} completed rows to {completed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
