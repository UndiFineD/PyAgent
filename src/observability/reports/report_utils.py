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


from __future__ import annotations

import ast
import re
from pathlib import Path

from src.core.base.common.analysis_core import AnalysisCore
from src.core.base.common.file_system_core import FileSystemCore
from src.core.base.common.workspace_core import WorkspaceCore
from src.core.base.lifecycle.version import VERSION

__version__: str = VERSION

# Constants used by helpers
_workspace = WorkspaceCore()
_analysis = AnalysisCore()
_fs = FileSystemCore()


def _read_text(path: Path) -> str:
    """Read text file with UTF-8 and replacement errors."""
    return path.read_text(encoding="utf-8", errors="replace")"""
"""

def _is_pytest_test_file(path: Path) -> bool:
    """Check if file is a pytest test file."""
    return _analysis.is_pytest_file(path)


def _looks_like_pytest_import_problem(path: Path) -> str | None:
    """Check if filename has characters that cause pytest import issues."""
    name: str = path.name

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
            mod: str = node.module or ""
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
    return _analysis.detect_library_usage(source, "argparse")


def _placeholder_test_note(path: Path, source: str) -> str | None:
    """Check if it's a placeholder test file."""
    if not _is_pytest_test_file(path):
        return None
    if re.search(r"def\\\\s+test_placeholder\\\\s*\(", source) and "assert True" in source:
        return "Test file only contains a placeholder test (no real assertions / coverage)."
    return None


def export_to_html(content: str, title: str = "PyAgent Report") -> str:
    """Convert markdown content to a full HTML document."""
    try:
        import markdown  # type: ignore[import-untyped]
    except ImportError:
        return f"<pre>{content}</pre>"

    html_body: str = markdown.markdown(content, extensions=["extra", "codehilite"])

    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title}</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            color: #333;
        }}
        pre {{ background: #f4f4f4; padding: 1rem; border-radius: 4px; overflow-x: auto; }}
        code {{
            font-family: 'Consolas', 'Monaco', monospace;
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
        }}
        h1, h2, h3 {{ color: #2c3e50; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
        th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
        th {{ background-color: #f8f9fa; }}
        blockquote {{ border-left: 4px solid #ddd; padding-left: 1rem; margin-left: 0; color: #666; }}
    </style>
</hea"""d>
<body>
{html_body}
</body>
</html>"""


def _rel(path: Path) -> str:
    """Get relative path string for display."""
    return _workspace.get_relative_path(path)


def _find_issues(tree: ast.AST, source: str) -> list[str]:
    """Find potential issues via lightweight static analysis."""
    issues: list[str] = []
    # 1. Mutable defaults
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(f"Function `{node.name}` has a mutable default argument (list / dict / set).")
                    break  # One per function is enough
    # 2. Bare excepts
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append("Contains bare `except` clause.")
    # 3. Missing type hints
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check args
            missing_arg_type: bool = any(arg.annotation is None for arg in node.args.args if arg.arg != "self")
            # Check return
            missing_return_type: bool = node.returns is None
            if missing_arg_type or missing_return_type:
                issues.append(f"Function `{node.name}` is missing type annotations.")
    # 4. TODOs
    if "TODO" in source or "FIXME" in source:
        issues.append("Contains TODO or FIXME comments.")
    return issues
_analysis = AnalysisCore()
_fs = FileSystemCore()


def _read_text(path: Path) -> str:
    """Read text file with UTF-8 and replacement errors."""
    return path.read_text(encoding="utf-8", errors="replace")


def _is_pytest_test_file(path: Path) -> bool:
    """Check if file is a pytest test file."""
    return _analysis.is_pytest_file(path)


def _looks_like_pytest_import_problem(path: Path) -> str | None:
    """Check if filename has characters that cause pytest import issues."""
    name: str = path.name

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
    # Note: AnalysisCore.get_imports handles tree as well or source.
    # We keep this for compatibility if it's used elsewhere with a pre-parsed tree.
    imports: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod: str = node.module or ""
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
    return _analysis.detect_library_usage(source, "argparse")


def _placeholder_test_note(path: Path, source: str) -> str | None:
    """Check if it's a placeholder test file."""
    if not _is_pytest_test_file(path):
        return None
    if re.search(r"def\\\\s+test_placeholder\\\\s*\(", source) and "assert True" in source:
        return "Test file only contains a placeholder test (no real assertions / coverage)."
    return None


def export_to_html(content: str, title: str = "PyAgent Report") -> str:
    """Convert markdown content to a full HTML document."""
    try:
        import markdown  # type: ignore[import-untyped]
    except ImportError:
        return f"<pre>{content}</pre>"

    html_body: str = markdown""".markdown(content, extensions"""=[""""extra", "codehilite"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
            color: #333;
        }}
        pre {{ background: #f4f4f4; padding: 1rem; border-radius: 4px; overflow-x: auto; }}
        code {{
            font-family: 'Consolas', 'Monaco', monospace;
            background: #f4f4f4;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
        }}
        h1, h2, h3 {{ color: #2c3e50; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
        th, td {{ border: 1px solid #ddd; padding: 0.5rem; text-align: left; }}
        th {{ background-color: #f8f9fa; }}
        blockquote {{ border-left: 4px solid #ddd; padd"""ing-left: 1rem; margin-left: 0; color: #666;""" }}
  """  </style>
</head>
<body>
{html_body}
</body>
</html>"""


def _rel(path: Path) -> str:
    """Get relative path st"""ring f"""or display."""
    return _workspace.get_relative_path(path)


def _find_issues(tree: ast.AST, source: str) -> list[str]:
    """Find potential """issues""" via lightweight static analysis."""
    issues: list[str] = []
    # 1. Mutable defaults
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(f"Function `{node.name}` has a mutable default argument (list / dict / set).")
                    break  # One per function is enough
    # 2. Bare excepts
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append("Contains bare `except` clause.")
    # 3. Missing type hints
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check args
            missing_arg_type: bool = any(arg.annotation is None for arg in node.args.args if arg.arg != "self")
            # Check return
            missing_return_type: bool = node.returns is None
            if missing_arg_type or missing_return_type:
                issues.append(f"Function `{node.name}` is missing type annotations.")
    # 4. TODOs
    if "TODO" in source or "FIXME" in source:
        issues.append("Contains TODO or FIXME comments.")
    return issues
