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
"""Code metrics collector using Python's AST module.

Computes per-file and aggregate metrics without executing any code.
"""

from __future__ import annotations

import argparse
import ast
import pathlib
from typing import NamedTuple

try:
    from src.tools.tool_registry import register_tool
except ImportError:  # pragma: no cover
    from tools.tool_registry import register_tool


class FileMetrics(NamedTuple):
    """Metrics for a single Python source file."""

    path: str
    lines: int
    blank_lines: int
    comment_lines: int
    functions: int
    classes: int
    complexity: int  # approximate cyclomatic (branch count + 1)


def _estimate_complexity(tree: ast.AST) -> int:
    """Estimate cyclomatic complexity as 1 + number of branch nodes."""
    branch_nodes = (
        ast.If,
        ast.For,
        ast.While,
        ast.ExceptHandler,
        ast.With,
        ast.Assert,
        ast.comprehension,
    )
    return 1 + sum(1 for _ in ast.walk(tree) if isinstance(_, branch_nodes))


def analyze_file(path: str) -> FileMetrics:
    """Return :class:`FileMetrics` for a single Python source file.

    Parameters
    ----------
    path:
        Path to the ``.py`` file.

    Returns
    -------
    FileMetrics
        Computed metrics.  On parse error, function/class/complexity counts
        are set to -1 and original line counts are preserved.
    """
    p = pathlib.Path(path)
    with open(p, encoding="utf-8", errors="ignore") as f:
        source_lines = f.readlines()

    total = len(source_lines)
    blank = sum(1 for ln in source_lines if not ln.strip())
    comment = sum(1 for ln in source_lines if ln.strip().startswith("#"))

    try:
        tree = ast.parse("".join(source_lines), filename=str(p))
    except SyntaxError:
        return FileMetrics(
            path=str(p),
            lines=total,
            blank_lines=blank,
            comment_lines=comment,
            functions=-1,
            classes=-1,
            complexity=-1,
        )

    functions = sum(1 for _ in ast.walk(tree) if isinstance(_, (ast.FunctionDef, ast.AsyncFunctionDef)))
    classes = sum(1 for _ in ast.walk(tree) if isinstance(_, ast.ClassDef))
    complexity = _estimate_complexity(tree)

    return FileMetrics(
        path=str(p),
        lines=total,
        blank_lines=blank,
        comment_lines=comment,
        functions=functions,
        classes=classes,
        complexity=complexity,
    )


def analyze_directory(root: str) -> list[FileMetrics]:
    """Analyze all ``.py`` files under *root* recursively.

    Parameters
    ----------
    root:
        Directory to scan.

    Returns
    -------
    list[FileMetrics]
        One entry per Python source file found, sorted by path.
    """
    py_files = sorted(pathlib.Path(root).rglob("*.py"))
    return [analyze_file(str(p)) for p in py_files]


def collect_metrics(root: str) -> dict[str, int]:
    """Collect aggregate code metrics for the repository.

    This is the legacy high-level interface retained for backward compatibility.
    """
    all_metrics = analyze_directory(root)
    return {
        "py_files": len(all_metrics),
        "lines": sum(m.lines for m in all_metrics),
        "blank_lines": sum(m.blank_lines for m in all_metrics),
        "comment_lines": sum(m.comment_lines for m in all_metrics),
        "functions": sum(m.functions for m in all_metrics if m.functions >= 0),
        "classes": sum(m.classes for m in all_metrics if m.classes >= 0),
        "avg_complexity": (
            round(
                sum(m.complexity for m in all_metrics if m.complexity >= 0)
                / max(1, sum(1 for m in all_metrics if m.complexity >= 0))
            )
        ),
    }


def main(args: list[str] | None = None) -> int:
    """Main entry point for the metrics tool."""
    parser = argparse.ArgumentParser(prog="metrics", description="Compute code metrics for PyAgent.")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--file", help="Analyze a single file instead of a directory")

    parsed = parser.parse_args(args=args)

    if parsed.file:
        m = analyze_file(parsed.file)
        data: dict = m._asdict()
    else:
        data = collect_metrics(parsed.root)

    if parsed.json:
        import json
        print(json.dumps(data, indent=2))
    else:
        print("\n".join(f"{k}: {v}" for k, v in data.items()))

    return 0


register_tool("metrics", main, "Compute code metrics (lines, functions, complexity) via AST")


if __name__ == "__main__":
    import sys
    sys.exit(main())
