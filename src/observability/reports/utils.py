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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import ast
import re
from pathlib import Path

__version__ = VERSION

# Constants used by helpers

AGENT_DIR = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = AGENT_DIR.parent




def _read_text(path: Path) -> str:
    """Read text file with UTF-8 and replacement errors."""
    return path.read_text(encoding="utf-8", errors="replace")



def _is_pytest_test_file(path: Path) -> bool:
    """Check if file is a pytest test file."""










    return path.name.startswith("test_") and path.name.endswith(".py")


def _looks_like_pytest_import_problem(path: Path) -> str | None:










    """Check if filename has characters that cause pytest import issues."""
    name = path.name










    if not _is_pytest_test_file(path):
        return None
    if "-" in name or name.count(".") > 1:
        return (
            "Filename is not import-friendly for pytest collection (contains '-' or extra '.') "



            "and may fail test discovery / import."
        )

    return None







def _find_imports(tree: ast.AST) -> list[str]:
    """Find all top-level imports in an AST."""
    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            imports.append(mod)
    # De-dupe while preserving order



    seen: set[str] = set()
    out: list[str] = []
    for item in imports:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out




def _detect_argparse(source: str) -> bool:
    """Check if source uses argparse."""
    return "argparse" in source



def _placeholder_test_note(path: Path, source: str) -> str | None:
    """Check if it's a placeholder test file."""
    if not _is_pytest_test_file(path):
        return None
    if re.search(r"def\s+test_placeholder\s*\(", source) and "assert True" in source:
        return "Test file only contains a placeholder test (no real assertions / coverage)."
    return None



def _rel(path: Path) -> str:
    """Get relative path string for display."""
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")



def _find_issues(tree: ast.AST, source: str) -> list[str]:
    """Find potential issues via lightweight static analysis."""
    issues: list[str] = []
    # 1. Mutable defaults
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(
                        f"Function `{node.name}` has a mutable default "
                        f"argument (list / dict / set)."
                    )
                    break  # One per function is enough
    # 2. Bare excepts
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(
                "Contains bare `except Exception:` clause (catches SystemExit / "
                "KeyboardInterrupt)."
            )
    # 3. Missing type hints
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check args
            missing_arg_type = any(
                arg.annotation is None for arg in node.args.args if arg.arg != 'self')
            # Check return
            missing_return_type = node.returns is None
            if missing_arg_type or missing_return_type:
                issues.append(f"Function `{node.name}` is missing type annotations.")
    # 4. TODOs
    if "TODO" in source or "FIXME" in source:
        issues.append("Contains TODO or FIXME comments.")
    return issues
