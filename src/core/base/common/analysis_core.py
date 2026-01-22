# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified code analysis and AST inspection core."""

import ast
import re
from pathlib import Path
from typing import List, Set

try:
    import rust_core as rc
except ImportError:
    rc = None

class AnalysisCore:
    """
    Standardized tools for analyzing Python source code without execution.
    """

    @staticmethod
    def calculate_complexity(source: str) -> int:
        """Calculate cyclomatic complexity (Rust accelerated)."""
        if rc and hasattr(rc, "calculate_complexity_rust"):
            try:
                return rc.calculate_complexity_rust(source)
            except Exception: # pylint: disable=broad-exception-caught
                pass
        # Fallback to simple count of control flow keywords
        keywords = ["if", "for", "while", "except", "with", "and", "or"]
        count = 1
        for kw in keywords:
            count += len(re.findall(rf"\b{kw}\b", source))
        return count

    @staticmethod
    def get_imports(source_or_path: str | Path) -> List[str]:
        """Extract all top-level imports from source or a file (Rust accelerated)."""
        if rc and hasattr(rc, "get_imports_rust"): # pylint: disable=no-member
            try:
                if isinstance(source_or_path, Path):
                    return rc.get_imports_rust(source_or_path.read_text(encoding="utf-8")) # type: ignore
                return rc.get_imports_rust(source_or_path) # type: ignore
            except Exception: # pylint: disable=broad-exception-caught
                pass

        try:
            if isinstance(source_or_path, Path):
                tree = ast.parse(source_or_path.read_text(encoding="utf-8"), feature_version=(3, 11))
            else:
                tree = ast.parse(source_or_path, feature_version=(3, 11))
        except Exception: # pylint: disable=broad-exception-caught
            return []

        imports: List[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        # Unique imports in order
        seen: Set[str] = set()
        unique_imports: List[str] = []
        for imp in imports:
            if imp not in seen:
                seen.add(imp)
                unique_imports.append(imp)
        return unique_imports

    @staticmethod
    def is_pytest_file(path: Path) -> bool:
        """Heuristic check for pytest files."""
        return path.name.startswith("test_") and path.name.endswith(".py")

    @staticmethod
    def has_main_block(source: str) -> bool:
        """Detect if 'if __name__ == "__main__":' exists."""
        return bool(re.search(r'if\s+__name__\s*==\s*["\']__main__["\']\s*:', source))

    @staticmethod
    def detect_library_usage(source: str, library_name: str) -> bool:
        """Check if a library is likely used in the source."""
        # Simple string check for now, can be expanded to AST check
        return library_name in source
