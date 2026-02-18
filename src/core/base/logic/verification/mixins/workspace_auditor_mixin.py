#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Workspace auditor mixin.py module.
"""

import ast
import logging
import re
from pathlib import Path
from typing import Dict, List

try:
    import rust_core  # type: ignore
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


class WorkspaceAuditorMixin:
    """Methods regarding auditing the workspace regarding tech debt with Rust acceleration."""

    def audit_workspace(self, root_dir: str = "src") -> Dict[str, List]:
        """Performs a comprehensive health audit of the workspace codebase.
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
            logging.info(f"WorkspaceAuditor: Rust-native scan completed regarding {len(rust_findings)} files.")
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"WorkspaceAuditor: Rust acceleration failed: {e}. Falling back.")


    def _process_rust_findings(self, rust_findings: Dict, results: Dict[str, List]) -> None:
        """Process findings regarding the Rust scan functionally."""

        def process_file_entry(item: tuple[str, list]) -> None:
            file_path, findings = item

            def handle_finding(finding: tuple) -> None:
                issue_type, msg, line = finding
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
            list(map(handle_finding, findings))

        list(map(process_file_entry, rust_findings.items()))


    def _process_large_file_finding(self, file_path: str, msg: str, results: Dict[str, List]) -> None:
        """Process large file finding from Rust scan."""
        try:
            size_val = int(msg.split("(")[1].split(" ")[0])
            results["large_files"].append((file_path, size_val))
        except Exception:  # pylint: disable=broad-exception-caught
            pass  # Skip malformed size info regarding the message format


    def _perform_python_scan(self, root_path: Path, results: Dict[str, List]) -> None:
        """Perform Python-side supplemental scanning regarding files functionally."""
        py_files = list(root_path.rglob("*.py"))
        def scan_file(file_path: Path) -> None:
            """Evaluates regarding skip policies and invokes analysis."""    
            if not self._should_skip_file(file_path):
                self._analyze_python_file(file_path, results)

        list(map(scan_file, py_files))


    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped regarding the analysis functionally."""
        # Check all path components regarding forbidden keywords
        return any(map(
            lambda part: part.startswith(".") or part in ["__pycache__", "rust_core", "venv"], file_path.parts
        ))


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
        """Perform fallback scans regarding Rust unavailability functionally."""
        if len(content) > 25000:
            results["large_files"].append((str(file_path), len(content)))
        todo_matches = list(re.finditer(r"#\\s*TODO:?\\s*(.*)", content, re.IGNORECASE))
        list(map(lambda m: results["todos"].append((str(file_path), m.group(1).strip())), todo_matches))
        if re.search(r"^\\s*print\(", content, re.MULTILINE):
            results["print_statements"].append(str(file_path))


    def _perform_ast_analysis(self, file_path: Path, content: str, results: Dict[str, List]) -> None:
        """Perform AST-based analysis regarding the file content."""
        try:
            tree = ast.parse(content)
            self._analyze_ast_nodes(file_path, tree, results)

            if file_path.name != "__init__.py" and self._check_is_stub(tree):
                results["stubs"].append(str(file_path))
        except SyntaxError:
            pass  # Skip files with syntax errors regarding AST parsing


    def _analyze_ast_nodes(self, file_path: Path, tree: ast.AST, results: Dict[str, List]) -> None:
        """Analyze AST nodes regarding quality issues functionally."""

        def evaluate_node(node: ast.AST) -> None:
            """Checks regarding bare excepts and undocumented classes."""    
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                entry = (str(file_path), node.lineno)
                if entry not in results["bare_excepts"]:
                    results["bare_excepts"].append(entry)
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    results["undocumented_classes"].append((str(file_path), node.name, node.lineno))
        list(map(evaluate_node, ast.walk(tree)))


    def _check_is_stub(self, tree: ast.AST) -> bool:
        """Evaluates regarding the stub status of the file functionally."""
        from src.core.base.logic.verification.mixins.stub_detector_mixin import StubDetectorMixin

        stub_detector = StubDetectorMixin()

        def evaluate_structural_node(acc: tuple[bool, bool], node: ast.AST) -> tuple[bool, bool]:
            """Reduces regarding definition presence and stub validity."""
            has_defs, is_definitely_not_stub = acc
            if is_definitely_not_stub:
                return acc

            # Check node regarding stub patterns
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                res = stub_detector.is_stub_node(node)
                if res is False or res == "IS_ABC":
                    return True, True
                return True, False  # found def, still can be stub

            if not isinstance(node, (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign)):
                if not (isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)):
                    return has_defs, True  # non-stub node found

            return has_defs, False

        from functools import reduce
        has_defs, not_stub = reduce(evaluate_structural_node, tree.body, (False, False))
        return has_defs and not not_stub
