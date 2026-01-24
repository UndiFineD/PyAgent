#!/usr/bin/env python3

"""
Workspace maintenance.py module.
"""
# Copyright 2026 PyAgent Authors
# Consolidated Maintenance and Audit utilities for the PyAgent workspace.

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


class WorkspaceMaintenance:
    """Consolidates file system auditing, naming convention enforcement, and cleanup."""

    DEFAULT_EXCLUSIONS = {
        ".git",
        ".venv",
        ".vscode",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".agent_cache",
        "target",
        "node_modules",
        ".hypothesis",
        "__pycache__",
    }

    def __init__(self, workspace_root: str | Path = ".") -> None:
        self.workspace_root = Path(workspace_root).resolve()

    def find_large_files(
        self, search_roots: List[str] = ["src"], threshold: int = 500, top_n: int = 10
    ) -> List[Tuple[int, Path]]:
        """
        Scans specified directories for Python files exceeding the line count threshold.
        Returns a sorted list of (line_count, path).
        """
        results = []
        for root_name in search_roots:
            root_path = self.workspace_root / root_name
            if not root_path.exists():
                logger.warning(f"Search root {root_path} does not exist.")
                continue

            for dirpath, dirnames, filenames in os.walk(root_path):
                # Prune excluded directories
                dirnames[:] = [d for d in dirnames if d not in self.DEFAULT_EXCLUSIONS]

                for filename in filenames:
                    if filename.endswith(".py"):
                        filepath = Path(dirpath) / filename
                        count = self._get_line_count(filepath)

                        # Check for 'facade' keyword to skip if necessary (logic from find_large_files.py)
                        is_facade = False
                        try:
                            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                                first_part = f.read(500).lower()
                                if "facade" in first_part:
                                    is_facade = True
                        except Exception:
                            pass

                        if count > threshold and not is_facade:
                            results.append((count, filepath))

        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_n]

    def audit_naming_conventions(self) -> List[Path]:
        """
        Identifies files and directories that do not follow snake_case naming.
        Returns a list of violating relative paths.
        """
        violations = []
        for path in self.workspace_root.rglob("*"):
            # Skip excluded paths
            if any(part in self.DEFAULT_EXCLUSIONS for part in path.parts):
                continue

            # Skip hidden files
            if path.name.startswith("."):
                continue

            # Skip standard exceptions
            if path.name in [
                "README.md",
                "Cargo.toml",
                "Cargo.lock",
                "LICENSE",
                "pytest.ini",
                "requirements.txt",
                "QUICKSTART_TOKEN_BENCHMARKS.md",
                "package.json",
            ]:
                continue

            stem = path.stem
            if not self._is_snake_case(stem):
                violations.append(path.relative_to(self.workspace_root))

        return violations

    def fix_naming_conventions(self, dry_run: bool = True) -> List[Tuple[Path, Path]]:
        """
        Attempts to rename files and directories to snake_case.
        Returns a list of (old_path, new_path) transformations.
        """
        transformations = []
        # Walk bottom-up to avoid issues when renaming parents
        for root, dirs, files in os.walk(self.workspace_root, topdown=False):
            # Prune exclusions
            dirs[:] = [d for d in dirs if d not in self.DEFAULT_EXCLUSIONS]
            if any(ex in root for ex in self.DEFAULT_EXCLUSIONS):
                continue

            # Process files
            for name in files:
                if name in ["README.md", "LICENSE", "Cargo.toml", "package.json", "pytest.ini", "requirements.txt"]:
                    continue

                new_name = self._to_snake_case(name)
                if new_name != name:
                    old_path = Path(root) / name
                    new_path = Path(root) / new_name
                    transformations.append((old_path, new_path))
                    if not dry_run:
                        self._safe_rename(old_path, new_path)

            # Process directories
            for name in dirs:
                new_name = self._to_snake_case(name)
                if new_name != name:
                    old_path = Path(root) / name
                    new_path = Path(root) / new_name
                    transformations.append((old_path, new_path))
                    if not dry_run:
                        self._safe_rename(old_path, new_path)

        return transformations

    def _get_line_count(self, file_path: Path) -> int:
        try:
            with open(file_path, "rb") as f:
                content = f.read()
                return content.count(b"\n") + (1 if content and not content.endswith(b"\n") else 0)
        except Exception:
            return 0

    def _is_snake_case(self, name: str) -> bool:
        return re.fullmatch(r"[a-z0-9_]+", name) is not None

    def _to_snake_case(self, name: str) -> str:
        if name == "__init__.py":
            return name
        path_obj = Path(name)
        stem = path_obj.stem
        suffix = path_obj.suffix

        # Replace spaces and hyphens
        temp = stem.replace(" ", "_").replace("-", "_")
        # Split CamelCase
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", temp)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
        # Clean up dots and underscores
        new_stem = s2.replace(".", "_")
        new_stem = re.sub("_+", "_", new_stem).strip("_")

        return new_stem + suffix

    def _safe_rename(self, old_path: Path, new_path: Path) -> None:
        if new_path.exists() and old_path.name.lower() != new_path.name.lower():
            logger.error(f"Collision: {old_path} -> {new_path}")
            return
        try:
            # Handle Windows case-insensitivity
            temp_path = old_path.with_name(old_path.name + ".tmp_rename")
            os.rename(old_path, temp_path)
            os.rename(temp_path, new_path)
            logger.info(f"Renamed: {old_path} -> {new_path}")
        except Exception as e:
            logger.error(f"Error renaming {old_path}: {e}")


if __name__ == "__main__":
    # Example usage if run directly
    maint = WorkspaceMaintenance("c:/DEV/PyAgent")
    print("--- Large Files ---")
    for count, path in maint.find_large_files():
        print(f"{count}: {path}")

    print("\n--- Naming Violations ---")
    violations = maint.audit_naming_conventions()
    for v in violations[:10]:
        print(v)
    if len(violations) > 10:
        print(f"... and {len(violations) - 10} more.")
