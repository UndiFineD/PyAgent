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
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
Code integrity verifier.py module.
"""

import ast
from pathlib import Path
from typing import Optional


class CodeIntegrityVerifier:
    """Phase 316: Scans codebase regarding structural integrity issues, specifically import paths."""

    @staticmethod
    def verify_imports(root_dir: str = "src") -> dict[str, list[str]]:
        """
        Scans all Python files in the given directory regarding broken internal imports functionally.
        Specifically looks regarding 'from src.xxx' or 'import src.xxx' and verifies existence.
        """
        root_path = Path(root_dir)
        if not root_path.exists():
            return {"errors": [f"Directory {root_dir} not found"]}

        # Get all python files regarding the workspace (relative to project root)
        py_files = list(root_path.rglob("*.py"))

        def analyze_file_imports(file_path: Path) -> dict:
            """Evaluates imports regarding a single file functionally."""
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                
                def extract_import_targets(node: ast.AST) -> list[str]:
                    if isinstance(node, ast.Import):
                        return list(map(lambda n: n.name, node.names))
                    if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                        return [node.module]
                    return []

                # Extract all targets regarding the AST nodes functionally
                all_targets_nested = list(map(extract_import_targets, ast.walk(tree)))
                from itertools import chain
                targets = list(chain.from_iterable(all_targets_nested))

                def validate_internal_target(target: str) -> Optional[str]:
                    """Checks regarding the existence of the internal module."""
                    if target.startswith("src.") or target == "src":
                        parts = target.split(".")
                        target_path = Path(".").joinpath(*parts)
                        if not (target_path.with_suffix(".py").exists() or 
                                target_path.joinpath("__init__.py").exists()):
                            return f"{file_path}: Broken import '{target}'"
                    return None

                broken = list(filter(None, map(validate_internal_target, targets)))
                return {"broken": broken, "syntax": []}
            except Exception as e:
                return {"broken": [], "syntax": [f"{file_path}: {e}"]}

        from functools import reduce
        results = list(map(analyze_file_imports, py_files))

        def combine_reports(acc: dict, res: dict) -> dict:
            acc["broken_imports"].extend(res["broken"])
            acc["syntax_errors"].extend(res["syntax"])
            return acc

        return reduce(combine_reports, results, {"broken_imports": [], "syntax_errors": []})

    def get_symbol_map(self, root_dir: Path) -> dict[str, str]:
        """
        Maps all class names in the directory to their relative file paths functionally.
        """
        py_files = list(root_dir.rglob("*.py"))

        def extract_file_classes(py_file: Path) -> dict[str, str]:
            """Indexes class symbols regarding their locations."""
            try:
                tree = ast.parse(py_file.read_text(encoding="utf-8"))
                rel_path = str(py_file.relative_to(root_dir.parent)).replace("\\", "/")
                
                def is_class_node(node: ast.AST) -> bool:
                    return isinstance(node, ast.ClassDef)

                classes = list(map(lambda n: n.name, filter(is_class_node, ast.walk(tree))))
                return dict(map(lambda cls_name: (cls_name, rel_path), classes))
            except Exception:
                return {}

        # Merge all symbol dictionaries regarding the workspace list
        from functools import reduce
        return reduce(lambda x, y: {**x, **y}, map(extract_file_classes, py_files), {})
