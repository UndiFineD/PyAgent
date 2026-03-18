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
    metrics: dict[str, int] = {
        "py_files": 0,
        "lines": 0,
        "blank_lines": 0,
        "comment_lines": 0,
    }

    for path in pathlib.Path(root).rglob("*.py"):
        metrics["py_files"] += 1
        with open(path, encoding="utf-8", errors="ignore") as f:
            for line in f:
                metrics["lines"] += 1
                stripped = line.strip()
                if not stripped:
                    metrics["blank_lines"] += 1
                elif stripped.startswith("#"):
                    metrics["comment_lines"] += 1

    return metrics


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
        for k, v in sorted(metrics.items()):
            print(f"{k}: {v}")

    return 0


register_tool("metrics", main, "Compute simple code metrics")
