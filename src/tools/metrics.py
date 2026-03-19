#!/usr/bin/env python3
"""Compute code metrics for the repository."""
# Copyright [year] [copyright holder]
#
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

from __future__ import annotations

import argparse
import os
import pathlib
import sys

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


def collect_metrics(root: str) -> dict[str, int]:
    """Collect code metrics for the repository."""
    py_paths = list(pathlib.Path(root).rglob("*.py"))

    def _counts_for_file(path: pathlib.Path) -> tuple[int, int, int]:
        """Count total, blank, and comment lines for a single file."""
        with open(path, encoding="utf-8", errors="ignore") as f:
            lines = [l for l in f]
        total = len(lines)
        blank = sum(1 for line in lines if not line.strip())
        comment = sum(1 for line in lines if line.strip().startswith("#"))
        return total, blank, comment

    counts = list(map(_counts_for_file, py_paths))
    total_lines = sum(c[0] for c in counts)
    blank_lines = sum(c[1] for c in counts)
    comment_lines = sum(c[2] for c in counts)

    return {
        "py_files": len(py_paths),
        "lines": total_lines,
        "blank_lines": blank_lines,
        "comment_lines": comment_lines,
    }


def main(args: list[str] | None = None) -> int:
    """Main entry point for the metrics tool."""
    parser = argparse.ArgumentParser(prog="metrics")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    parsed = parser.parse_args(args=args)
    metrics = collect_metrics(parsed.root)

    if parsed.json:
        import json

        print(json.dumps(metrics, indent=2))
    else:
        print("\n".join(f"{k}: {v}" for k, v in sorted(metrics.items())))

    return 0


register_tool("metrics", main, "Compute simple code metrics")
