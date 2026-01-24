#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Auditor for workspace code complexity using Rust-native analysis.
Ported from temp/find_complex_files.py for re-use in the fleet.
"""

import argparse
import logging
import os
from pathlib import Path

try:
    import rust_core as rc
except ImportError:
    rc = None


def run_audit(target_dir: str, threshold: int = 25, limit: int = 20):
    """Scans the target directory for Python files exceeding the complexity threshold."""
    if rc is None:
        print("Error: rust_core not found. Complexity analysis is unavailable.")
        return

    workspace_root = Path(__file__).resolve().parents[5]
    scan_path = (workspace_root / target_dir).resolve()

    if not scan_path.exists():
        print(f"Error: Path {scan_path} does not exist.")
        return

    targets = []
    print(f"Scanning {target_dir} for complexity > {threshold}...")

    for root, _, files in os.walk(scan_path):
        for file in files:
            if file.endswith(".py"):
                full_path = Path(root) / file
                rel_path = full_path.relative_to(workspace_root)
                try:
                    content = full_path.read_text(encoding="utf-8", errors="ignore")
                    comp = rc.calculate_cyclomatic_complexity(content)
                    if comp > threshold:
                        targets.append({"file": str(rel_path), "complexity": comp})
                except Exception as e:
                    logging.debug(f"Failed to analyze {rel_path}: {e}")

    targets.sort(key=lambda x: x["complexity"], reverse=True)

    print(f"\nFound {len(targets)} files with complexity > {threshold}:")
    for t in targets[:limit]:
        marker = "***" if t["complexity"] >= threshold else "   "
        print(f"{marker} {t['complexity']:<2} : {t['file']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit workspace code complexity.")
    parser.add_argument("--dir", type=str, default="src", help="Directory to scan (relative to root).")
    parser.add_argument("--threshold", type=int, default=25, help="Complexity threshold.")
    parser.add_argument("--limit", type=int, default=20, help="Number of results to display.")

    args = parser.parse_args()
    run_audit(args.dir, args.threshold, args.limit)
