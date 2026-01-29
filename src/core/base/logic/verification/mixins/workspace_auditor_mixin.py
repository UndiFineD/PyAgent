
"""
Workspace auditor mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import ast
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
        results = self._initialize_audit_results()
        root_path = Path(root_dir)

        if not root_path.exists():
            return results

        # High-Speed Rust Scan
        self._perform_rust_scan(root_dir, results)

        # Python-side Supplemental Loop
        self._perform_python_scan(root_path, results)

        return results

    def _initialize_audit_results(self) -> Dict[str, List]:
        """Initialize the audit results dictionary."""
        return {
            "bare_excepts": [],  # (file, line)
            "hardcoded_paths": [],  # (file, line, path)
            "todos": [],  # (file, task)
            "print_statements": [],  # [files]
            "undocumented_classes": [],  # (file, class_name, line)
            "stubs": [],  # [files]
            "large_files": [],  # (file, size)
        }

    def _perform_rust_scan(self, root_dir: str, results: Dict[str, List]) -> None:
        """Perform high-speed Rust-accelerated workspace scan."""
        if not HAS_RUST:
            return

        try:
            dangerous = [
                (r"['\"]C:\\[a-zA-Z0-9]", "Hardcoded Windows path"),
                (r"['\"]/home/|['\"]/Users/", "Hardcoded Nix path"),
                (r"^\s*print\(", "Print statement"),
            ]
            rust_findings = rust_core.scan_workspace_quality_rust(
                root_dir, [".git", "__pycache__", "rust_core", "venv", ".venv", "target"], dangerous
            )

            self._process_rust_findings(rust_findings, results)
            logging.info(f"WorkspaceAuditor: Rust-native scan completed for {len(rust_findings)} files.")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"WorkspaceAuditor: Rust acceleration failed: {e}. Falling back.")

    def _process_rust_findings(self, rust_findings: Dict, results: Dict[str, List]) -> None:
        """Process findings from Rust scan."""
        for file_path, findings in rust_findings.items():
            for issue_type, msg, line in findings:
                if issue_type == "Robustness Issue":
                    results["bare_excepts"].append((file_path, line))
                elif "Hardcoded" in msg:
                    results["hardcoded_paths"].append((file_path, line, msg))
                elif issue_type == "TODO":
                    results["todos"].append((file_path, msg))
                elif issue_type == "Large File":
                    self._process_large_file_finding(file_path, msg, results)
                elif "Print statement" in msg:
                    if file_path not in results["print_statements"]:
                        results["print_statements"].append(file_path)

    def _process_large_file_finding(self, file_path: str, msg: str, results: Dict[str, List]) -> None:
        """Process large file finding from Rust scan."""
        try:
            size_val = int(msg.split("(")[1].split(" ")[0])
            results["large_files"].append((file_path, size_val))
        except Exception:  # pylint: disable=broad-exception-caught
            pass  # Skip malformed size info

    def _perform_python_scan(self, root_path: Path, results: Dict[str, List]) -> None:
        """Perform Python-side supplemental scanning."""
        py_files = list(root_path.rglob("*.py"))
        for file_path in py_files:
            if self._should_skip_file(file_path):
                continue

            self._analyze_python_file(file_path, results)

    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during analysis."""
        return any(part.startswith(".") or part in ["__pycache__", "rust_core", "venv"]
                  for part in file_path.parts)

    def _analyze_python_file(self, file_path: Path, results: Dict[str, List]) -> None:
        """Analyze a single Python file."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            if not HAS_RUST:
                self._perform_fallback_scans(file_path, content, results)

            # AST Analysis
            self._perform_ast_analysis(file_path, content, results)

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.debug(f"CodeHealthAuditor: Error scanning {file_path}: {e}")

    def _perform_fallback_scans(self, file_path: Path, content: str, results: Dict[str, List]) -> None:
        """Perform fallback scans when Rust is not available."""
        if len(content) > 25000:
            results["large_files"].append((str(file_path), len(content)))

        todo_matches = re.finditer(r"#\s*TODO:?\s*(.*)", content, re.IGNORECASE)
        for match in todo_matches:
            results["todos"].append((str(file_path), match.group(1).strip()))

        if re.search(r"^\s*print\(", content, re.MULTILINE):
            results["print_statements"].append(str(file_path))

    def _perform_ast_analysis(self, file_path: Path, content: str, results: Dict[str, List]) -> None:
        """Perform AST-based analysis of the file."""
        try:
            tree = ast.parse(content)
            self._analyze_ast_nodes(file_path, tree, results)

            if file_path.name != "__init__.py" and self._check_is_stub(tree):
                results["stubs"].append(str(file_path))

        except SyntaxError:
            pass  # Skip files with syntax errors

    def _analyze_ast_nodes(self, file_path: Path, tree: ast.AST, results: Dict[str, List]) -> None:
        """Analyze AST nodes for issues."""
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                entry = (str(file_path), node.lineno)
                if entry not in results["bare_excepts"]:
                    results["bare_excepts"].append(entry)

            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    results["undocumented_classes"].append((str(file_path), node.name, node.lineno))

    def _check_is_stub(self, tree: ast.AST) -> bool:
        from src.core.base.logic.verification.mixins.stub_detector_mixin import StubDetectorMixin

        has_defs = False
        is_stub = True
        for node in tree.body:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                has_defs = True
                res = StubDetectorMixin._is_stub_node(node)  # pylint: disable=protected-access
                if res is False or res == "IS_ABC":
                    is_stub = False
                    break
            elif not isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
                if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)):
                    is_stub = False
                    break
        return has_defs and is_stub
