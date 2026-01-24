
"""
Workspace auditor mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import ast
import contextlib
import logging
import re
from pathlib import Path
from typing import Dict, List

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class WorkspaceAuditorMixin:
    """Methods for auditing the workspace for tech debt with Rust acceleration."""

    def audit_workspace(self, root_dir: str = "src") -> Dict[str, List]:
        """
        Performs a comprehensive health audit of the workspace codebase.
        Offloads regex-heavy scanning to Rust if available.
        """
        results = {
            "bare_excepts": [],  # (file, line)
            "hardcoded_paths": [],  # (file, line, path)
            "todos": [],  # (file, task)
            "print_statements": [],  # [files]
            "undocumented_classes": [],  # (file, class_name, line)
            "stubs": [],  # [files]
            "large_files": [],  # (file, size)
        }

        root_path = Path(root_dir)
        if not root_path.exists():
            return results

        # 1. High-Speed Rust Scan (Security, Robustness, Prints, Large Files)
        if HAS_RUST:
            try:
                # Patterns to detect via Rust regex engine
                dangerous = [
                    (r"['" "]C:\\[a-zA-Z0-9]", "Hardcoded Windows path"),
                    (r"['" "]/home/|['" "]/Users/", "Hardcoded Nix path"),
                    (r"^\s*print\(", "Print statement"),
                ]
                rust_findings = rust_core.scan_workspace_quality_rust(
                    str(root_dir), [".git", "__pycache__", "rust_core", "venv", ".venv", "target"], dangerous
                )

                for file_path, findings in rust_findings.items():
                    for issue_type, msg, line in findings:
                        if issue_type == "Robustness Issue":
                            results["bare_excepts"].append((file_path, line))
                        elif "Hardcoded" in msg:
                            results["hardcoded_paths"].append((file_path, line, msg))
                        elif issue_type == "TODO":
                            results["todos"].append((file_path, msg))
                        elif issue_type == "Large File":
                            with contextlib.suppress(Exception):
                                size_val = int(msg.split("(")[1].split(" ")[0])
                                results["large_files"].append((file_path, size_val))
                        elif "Print statement" in msg:
                            if file_path not in results["print_statements"]:
                                results["print_statements"].append(file_path)

                logging.info(f"WorkspaceAuditor: Rust-native scan completed for {len(rust_findings)} files.")
            except Exception as e:
                logging.error(f"WorkspaceAuditor: Rust acceleration failed: {e}. Falling back.")

        # 2. Python-side Supplemental Loop
        py_files = list(root_path.rglob("*.py"))
        for file_path in py_files:
            if any(part.startswith(".") or part in ["__pycache__", "rust_core", "venv"] for part in file_path.parts):
                continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                if not HAS_RUST:
                    if len(content) > 25000:
                        results["large_files"].append((str(file_path), len(content)))

                    todo_matches = re.finditer(r"#\s*TODO:?\s*(.*)", content, re.IGNORECASE)
                    for match in todo_matches:
                        results["todos"].append((str(file_path), match.group(1).strip()))

                    if re.search(r"^\s*print\(", content, re.MULTILINE):
                        results["print_statements"].append(str(file_path))

                # AST Analysis
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ExceptHandler) and node.type is None:
                            entry = (str(file_path), node.lineno)
                            if entry not in results["bare_excepts"]:
                                results["bare_excepts"].append(entry)

                        if isinstance(node, ast.ClassDef):
                            if not ast.get_docstring(node):
                                results["undocumented_classes"].append((str(file_path), node.name, node.lineno))

                    if file_path.name != "__init__.py" and self._check_is_stub(tree):
                        results["stubs"].append(str(file_path))

                except SyntaxError:
                    continue

            except Exception as e:
                logging.debug(f"CodeHealthAuditor: Error scanning {file_path}: {e}")

        return results

    def _check_is_stub(self, tree: ast.AST) -> bool:
        from .stub_detector_mixin import StubDetectorMixin

        has_defs = False
        is_stub = True
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                has_defs = True
                res = StubDetectorMixin._is_stub_node(node)
                if res is False or res == "IS_ABC":
                    is_stub = False
                    break
            elif not isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
                if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)):
                    is_stub = False
                    break
        return has_defs and is_stub
