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

"""Red-phase guard for restricting `rl` and `speculation` import scope."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(".")
SCAN_ROOTS: tuple[Path, ...] = (ROOT / "tests", ROOT / "src")
ALLOWED_IMPORT_FILES: set[str] = {
    "tests/rl/test_discounted_return.py",
    "tests/rl/test_rl_deprecation.py",
    "tests/speculation/test_select_candidate.py",
    "tests/speculation/test_speculation_deprecation.py",
}


def _iter_python_files() -> list[Path]:
    """Collect Python files from configured scan roots.

    Returns:
        list[Path]: Python files under tests/ and src/ excluding cache folders.

    """
    files: list[Path] = []
    for scan_root in SCAN_ROOTS:
        if not scan_root.exists():
            continue
        for path in scan_root.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            files.append(path)
    return files


def _contains_target_import(node: ast.AST) -> bool:
    """Check whether an import node targets top-level rl/speculation modules.

    Args:
        node: AST node to inspect.

    Returns:
        bool: True if node imports `rl` or `speculation` directly.

    """
    if isinstance(node, ast.Import):
        return any(alias.name in {"rl", "speculation"} for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        return node.module in {"rl", "speculation"}
    return False


def _find_disallowed_import_sites() -> list[str]:
    """Scan repository roots for disallowed imports of `rl` and `speculation`.

    Returns:
        list[str]: Sorted violation entries as path:line.

    """
    violations: list[str] = []
    for path in _iter_python_files():
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        rel_path = path.relative_to(ROOT).as_posix()
        if rel_path in ALLOWED_IMPORT_FILES:
            continue

        for node in ast.walk(tree):
            if _contains_target_import(node):
                line_no = getattr(node, "lineno", "?")
                violations.append(f"{rel_path}:{line_no}")
    return sorted(violations)


def test_allowlist_files_exist_for_rl_speculation_behavior_and_deprecation() -> None:
    """Verify all allowlisted behavior/deprecation tests exist in the repository."""
    missing = [path for path in sorted(ALLOWED_IMPORT_FILES) if not (ROOT / path).exists()]
    assert not missing, f"Missing allowlisted test files: {missing}"


def test_no_disallowed_rl_or_speculation_import_sites() -> None:
    """Fail when imports of rl/speculation appear outside the approved allowlist."""
    violations = _find_disallowed_import_sites()
    assert not violations, f"Disallowed rl/speculation imports found: {violations}"
