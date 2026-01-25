
"""
Code integrity verifier.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import ast
from pathlib import Path


class CodeIntegrityVerifier:
    """Phase 316: Scans codebase for structural integrity issues, specifically import paths."""

    @staticmethod
    def verify_imports(root_dir: str = "src") -> dict[str, list[str]]:
        """
        Scans all Python files in the given directory for broken internal imports.
        Specifically looks for 'from src.xxx' or 'import src.xxx' and verifies existence.
        """
        root_path = Path(root_dir)
        if not root_path.exists():
            return {"errors": [f"Directory {root_dir} not found"]}

        report = {"broken_imports": [], "syntax_errors": []}

        # Get all python files in the workspace (relative to project root)
        # assuming the script is run from project root.
        py_files = list(root_path.rglob("*.py"))

        for file_path in py_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                report["syntax_errors"].append(f"{file_path}: {e}")
                continue

            for node in ast.walk(tree):
                targets = []
                if isinstance(node, ast.Import):
                    targets = [n.name for n in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    # For 'from x import y', we only check the module 'x'
                    if node.level == 0:
                        targets = [node.module]

                for target in targets:
                    # We only care about verifying our own 'src' hierarchy
                    if target.startswith("src.") or target == "src":
                        parts = target.split(".")
                        # Check if it's a directory (module) or a file (.py)
                        # We use Path(".") as base to refer to project root
                        target_path = Path(".").joinpath(*parts)

                        exists = (
                            target_path.with_suffix(".py").exists() or
                            target_path.joinpath("__init__.py").exists()
                        )

                        if not exists:
                            report["broken_imports"].append(f"{file_path}: Broken import '{target}'")

        return report

    def get_symbol_map(self, root_dir: Path) -> dict[str, str]:
        """
        Maps all class names in the directory to their relative file paths (indexing).
        """
        mapping = {}
        for py_file in root_dir.rglob("*.py"):
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                rel_path = str(py_file.relative_to(root_dir.parent)).replace("\\", "/")
                for cls in classes:
                    mapping[cls] = rel_path
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                continue
        return mapping
