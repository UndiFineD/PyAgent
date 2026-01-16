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

"""
Computational core for code analysis, metrics, and quality assessment.
Designed for high-performance rule checking with future Rust integration.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.core.base.types.CodeLanguage import CodeLanguage
from src.core.base.types.CodeMetrics import CodeMetrics
from src.core.base.types.CodeSmell import CodeSmell
from src.core.base.types.QualityScore import QualityScore
from src.core.base.types.StyleRule import StyleRule
from src.core.base.types.StyleRuleSeverity import StyleRuleSeverity
from src.core.base.AgentCore import LogicCore
from typing import Any
import ast
import hashlib
import logging
import math
import os
import re
import shutil
import subprocess
import tempfile

__version__ = VERSION

# Logic extracted for future Rust migration (PyO3)
# Goal: Isolate all "Computationally Expensive" or "Rule-Based" logic here.

# Default style rules for Python (Re-declared here for Core access)
DEFAULT_PYTHON_STYLE_RULES: list[StyleRule] = [
    StyleRule(
        name="line_length",
        pattern=r"^.{89,}$",
        message="Line exceeds 88 characters",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON,
    ),
    StyleRule(
        name="trailing_whitespace",
        pattern=r"[ \t]+$",
        message="Trailing whitespace detected",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON,
    ),
    StyleRule(
        name="multiple_blank_lines",
        pattern=r"\n{4,}",
        message="More than 2 consecutive blank lines",
        severity=StyleRuleSeverity.INFO,
        language=CodeLanguage.PYTHON,
    ),
    StyleRule(
        name="missing_docstring",
        pattern=r'^def\s+\w+\([^)]*\):\s*\n\s+(?!"")',
        message="Function missing docstring",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON,
    ),
]

# Common code smells patterns
CODE_SMELL_PATTERNS: dict[str, dict[str, Any]] = {
    "long_method": {
        "threshold": 50,
        "message": "Method is too long (>{threshold} lines)",
        "category": "complexity",
    },
    "too_many_parameters": {
        "threshold": 5,
        "message": "Function has too many parameters (>{threshold})",
        "category": "complexity",
    },
    "duplicate_code": {
        "threshold": 3,
        "message": "Duplicate code detected ({count} occurrences)",
        "category": "duplication",
    },
    "deep_nesting": {
        "threshold": 4,
        "message": "Code is too deeply nested (>{threshold} levels)",
        "category": "complexity",
    },
    "god_class": {
        "threshold": 20,
        "message": "Class has too many methods (>{threshold})",
        "category": "design",
    },
}


class CoderCore(LogicCore):
    """Core logic for CoderAgent, target for Rust conversion."""

    def __init__(
        self, language: CodeLanguage, workspace_root: str | None = None
    ) -> None:
        self.language = language
        self.workspace_root = workspace_root
        try:
            import rust_core

            self._rust_core = rust_core.CoderCore(str(language))  # type: ignore[attr-defined]
        except (ImportError, AttributeError):
            self._rust_core = None

    def calculate_metrics(self, content: str) -> CodeMetrics:
        """Analyze code structure and compute metrics."""
        lines = content.split("\n")
        metrics = CodeMetrics()

        # Basic line counts
        for line in lines:
            stripped = line.strip()
            if not stripped:
                metrics.blank_lines += 1
            elif stripped.startswith("#") or stripped.startswith("//"):
                metrics.lines_of_comments += 1
            else:
                metrics.lines_of_code += 1

        # Language-specific deep analysis
        if self.language == CodeLanguage.PYTHON:
            try:
                tree = ast.parse(content)
                metrics = self._analyze_python_ast(tree, metrics)
            except SyntaxError:
                pass

        # General Maintainability Index
        if metrics.lines_of_code > 0:
            halstead_volume = metrics.lines_of_code * math.log2(
                max(1, metrics.function_count + metrics.class_count + 1)
            )
            cc = max(1, metrics.cyclomatic_complexity)
            loc = metrics.lines_of_code
            cm = metrics.lines_of_comments
            metrics.maintainability_index = max(
                0,
                min(
                    100,
                    171
                    - 5.2 * math.log(halstead_volume + 1)
                    - 0.23 * cc
                    - 16.2 * math.log(loc + 1)
                    + 50 * math.sin(math.sqrt(2.4 * (cm / (loc + cm + 1)))),
                ),
            )

        return metrics

    def _analyze_python_ast(self, tree: ast.AST, metrics: CodeMetrics) -> CodeMetrics:
        """Deep AST analysis for Python."""
        function_lengths: list[int] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                metrics.function_count += 1
                if hasattr(node, "end_lineno") and node.end_lineno is not None:
                    length = node.end_lineno - node.lineno + 1
                    function_lengths.append(length)
                    cc = 1
                    for child in ast.walk(node):
                        if isinstance(
                            child, (ast.If, ast.While, ast.For, ast.ExceptHandler)
                        ):
                            cc += 1
                        elif isinstance(child, ast.BoolOp):
                            cc += len(child.values) - 1
                    metrics.cyclomatic_complexity += cc
            elif isinstance(node, ast.ClassDef):
                metrics.class_count += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics.import_count += 1

        if function_lengths:
            metrics.average_function_length = sum(function_lengths) / len(
                function_lengths
            )
            metrics.max_function_length = max(function_lengths)

        return metrics

    def check_style(self, content: str, rules: list[StyleRule]) -> list[dict[str, Any]]:
        """Run regex-based style checks."""
        # Rust optimization
        if self._rust_core:
            patterns = []
            for rule in rules:
                if rule.enabled and (
                    not rule.language or rule.language == self.language
                ):
                    patterns.append((rule.name, rule.pattern))

            try:
                rust_violations = self._rust_core.check_style(content, patterns)
                violations = []
                # Map Rust tuple back to dict: (name, line, content)
                rule_map = {r.name: r for r in rules}
                for name, line, match_content in rust_violations:
                    rule = rule_map.get(name)
                    if rule:
                        violations.append(
                            {
                                "rule": rule.name,
                                "message": rule.message,
                                "severity": rule.severity.value
                                if hasattr(rule.severity, "value")
                                else str(rule.severity),
                                "line": line,
                                "content": match_content,
                            }
                        )
                return violations
            except Exception as e:
                logging.warning(f"Rust optimization failed for check_style: {e}")

        violations: list[dict[str, Any]] = []
        lines = content.split("\n")
        for rule in rules:
            if not rule.enabled:
                continue
            if rule.language and rule.language != self.language:
                continue

            if "\n" in rule.pattern or rule.pattern.startswith("^"):
                for match in re.finditer(rule.pattern, content, re.MULTILINE):
                    line_no = content.count("\n", 0, match.start()) + 1
                    violations.append(
                        {
                            "rule": rule.name,
                            "message": rule.message,
                            "severity": rule.severity.value
                            if hasattr(rule.severity, "value")
                            else str(rule.severity),
                            "line": line_no,
                            "content": match.group(0).split("\n")[0][:80],
                        }
                    )
            else:
                for i, line in enumerate(lines, 1):
                    if re.search(rule.pattern, line):
                        violations.append(
                            {
                                "rule": rule.name,
                                "message": rule.message,
                                "severity": rule.severity.value
                                if hasattr(rule.severity, "value")
                                else str(rule.severity),
                                "line": i,
                                "content": line[:80],
                            }
                        )
        return violations

    def auto_fix_style(self, content: str, rules: list[StyleRule]) -> tuple[str, int]:
        """Apply rules that have auto-fix capabilities."""
        fixed_content = content
        fix_count = 0
        for rule in rules:
            if not rule.enabled or not rule.auto_fix:
                continue
            if rule.language and rule.language != self.language:
                continue

            new_content = rule.auto_fix(fixed_content)
            if new_content != fixed_content:
                fix_count += 1
                fixed_content = new_content

        # Standard cleanup
        lines = fixed_content.split("\n")
        cleaned = [line.rstrip() for line in lines]
        if cleaned != lines:
            fix_count += 1
            fixed_content = "\n".join(cleaned)

        return fixed_content, fix_count

    def detect_code_smells(self, content: str) -> list[CodeSmell]:
        """Detect common architectural code smells."""
        smells: list[CodeSmell] = []
        if self.language != CodeLanguage.PYTHON:
            return smells

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return smells

        lines = content.split("\n")
        for node in ast.walk(tree):
            # Long method detection
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if hasattr(node, "end_lineno") and node.end_lineno is not None:
                    length = node.end_lineno - node.lineno + 1
                    threshold = CODE_SMELL_PATTERNS["long_method"]["threshold"]
                    if length > threshold:
                        smells.append(
                            CodeSmell(
                                name="long_method",
                                description=f"Method '{node.name}' is {length} lines (>{threshold})",
                                severity="warning",
                                line_number=node.lineno,
                                suggestion=f"Consider breaking down '{node.name}' into smaller functions",
                                category="complexity",
                            )
                        )

                # Too many parameters
                param_count = len(node.args.args)
                threshold = CODE_SMELL_PATTERNS["too_many_parameters"]["threshold"]
                if param_count > threshold:
                    smells.append(
                        CodeSmell(
                            name="too_many_parameters",
                            description=f"Function '{node.name}' has {param_count} parameters (>{threshold})",
                            severity="warning",
                            line_number=node.lineno,
                            suggestion="Consider using a data class or dictionary for parameters",
                            category="complexity",
                        )
                    )

            # God class detection
            if isinstance(node, ast.ClassDef):
                method_count = sum(
                    1
                    for n in node.body
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                )
                threshold = CODE_SMELL_PATTERNS["god_class"]["threshold"]
                if method_count > threshold:
                    smells.append(
                        CodeSmell(
                            name="god_class",
                            description=f"Class '{node.name}' has {method_count} methods (>{threshold})",
                            severity="warning",
                            line_number=node.lineno,
                            suggestion="Consider splitting the class into smaller, more focused classes.",
                            category="design",
                        )
                    )

        # Deep nesting detection
        for i, line in enumerate(lines, 1):
            indent = len(line) - len(line.lstrip())
            nesting = indent // 4
            threshold = CODE_SMELL_PATTERNS["deep_nesting"]["threshold"]
            if nesting > threshold and line.strip():
                smells.append(
                    CodeSmell(
                        name="deep_nesting",
                        description=f"Code at line {i} has {nesting} levels of nesting (>{threshold})",
                        severity="info",
                        line_number=i,
                        suggestion="Consider early returns or extracting nested logic",
                        category="complexity",
                    )
                )

        return smells

    def find_duplicate_code(
        self, content: str, min_lines: int = 4
    ) -> list[dict[str, Any]]:
        """Find duplicate code blocks using hashing."""
        # Rust-accelerated sliding window hash
        try:
            import rust_core as rc

            rust_result = rc.find_duplicate_code_rust(content, min_lines)  # type: ignore[attr-defined]
            # Convert Rust output format to expected dicts
            duplicates: list[dict[str, Any]] = []
            for hash_val, line_nums in rust_result.items():
                if len(line_nums) > 1:
                    lines = content.split("\n")
                    preview_start = line_nums[0] - 1
                    duplicates.append(
                        {
                            "hash": hash_val,
                            "occurrences": len(line_nums),
                            "lines": line_nums,
                            "preview": "\n".join(
                                lines[preview_start : preview_start + min_lines]
                            )[:100],
                        }
                    )
            return duplicates
        except Exception:
            pass

        lines = content.split("\n")
        duplicates = []
        hashes: dict[str, list[int]] = {}

        for i in range(len(lines) - min_lines + 1):
            block = "\n".join(lines[i : i + min_lines])
            normalized = re.sub(r"\s+", " ", block.strip())
            if len(normalized) < 20:
                continue

            block_hash = hashlib.md5(normalized.encode()).hexdigest()
            if block_hash not in hashes:
                hashes[block_hash] = []
            hashes[block_hash].append(i + 1)

        for block_hash, line_numbers in hashes.items():
            if len(line_numbers) > 1:
                duplicates.append(
                    {
                        "hash": block_hash,
                        "occurrences": len(line_numbers),
                        "lines": line_numbers,
                        "preview": "\n".join(
                            lines[line_numbers[0] - 1 : line_numbers[0] - 1 + min_lines]
                        )[:100],
                    }
                )
        return duplicates

    def calculate_quality_score(
        self,
        metrics: CodeMetrics,
        violations: list[dict[str, Any]],
        smells: list[CodeSmell],
        coverage: float,
    ) -> QualityScore:
        """Aggregate all analysis into a single QualityScore."""
        score = QualityScore()
        score.maintainability = min(100, metrics.maintainability_index)

        # Readability score
        readability_deductions = len(violations) * 5
        score.readability = max(0, 100 - readability_deductions)

        # Complexity score
        if metrics.function_count > 0:
            avg_cc = metrics.cyclomatic_complexity / metrics.function_count
            score.complexity = max(0, 100 - (avg_cc - 1) * 10)
        else:
            score.complexity = 100

        # Documentation score
        if metrics.lines_of_code > 0:
            comment_ratio = metrics.lines_of_comments / metrics.lines_of_code
            score.documentation = min(100, comment_ratio * 200)

        score.test_coverage = coverage

        # Overall score (weighted average)
        score.overall_score = (
            score.maintainability * 0.25
            + score.readability * 0.25
            + score.complexity * 0.25
            + score.documentation * 0.15
            + score.test_coverage * 0.10
        )

        # Add primary issues
        for violation in violations[:5]:
            score.issues.append(
                f"Style: {violation['message']} (line {violation['line']})"
            )
        for smell in smells[:5]:
            score.issues.append(f"Smell: {smell.description}")

        return score

    def suggest_refactorings(self, content: str) -> list[dict[str, str]]:
        """Suggest possible refactorings based on code analysis."""
        suggestions: list[dict[str, str]] = []
        # Detect code smells and suggest refactorings
        smells = self.detect_code_smells(content)
        for smell in smells:
            if smell.name == "long_method":
                suggestions.append(
                    {
                        "type": "extract_method",
                        "description": f"Extract parts of method at line {smell.line_number}",
                        "reason": smell.description,
                    }
                )
            elif smell.name == "too_many_parameters":
                suggestions.append(
                    {
                        "type": "introduce_parameter_object",
                        "description": (
                            f"Create a data class for parameters at "
                            f"line {smell.line_number}"
                        ),
                        "reason": smell.description,
                    }
                )
            elif smell.name == "god_class":
                suggestions.append(
                    {
                        "type": "extract_class",
                        "description": f"Split class at line {smell.line_number} into focused classes",
                        "reason": smell.description,
                    }
                )
        # Check for duplicate code
        duplicates = self.find_duplicate_code(content)
        if duplicates:
            suggestions.append(
                {
                    "type": "extract_method",
                    "description": (
                        f"Extract {len(duplicates)} duplicate code blocks "
                        f"into shared methods"
                    ),
                    "reason": f"Found {len(duplicates)} duplicate code patterns",
                }
            )
        return suggestions

    def generate_documentation(self, content: str) -> str:
        """Generate documentation from code."""
        if self.language != CodeLanguage.PYTHON:
            return "# Documentation\n\nDocumentation generation is only supported for Python files."
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return "# Documentation\n\nUnable to parse file for documentation."

        docs: list[str] = ["# API Documentation\n"]
        # Get module docstring
        module_doc = ast.get_docstring(tree)
        if module_doc:
            docs.append(f"## Module\n\n{module_doc}\n")
        # Document classes and functions
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                docs.append(f"## Class: `{node.name}`\n")
                class_doc = ast.get_docstring(node)
                if class_doc:
                    docs.append(f"{class_doc}\n")
                # Document methods
                for item in node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        docs.append(f"### Method: `{item.name}`\n")
                        method_doc = ast.get_docstring(item)
                        if method_doc:
                            docs.append(f"{method_doc}\n")
                        # Document parameters
                        params = [
                            arg.arg for arg in item.args.args if arg.arg != "self"
                        ]
                        if params:
                            docs.append(f"**Parameters:** {', '.join(params)}\n")
                docs.append("\n")
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                docs.append(f"## Function: `{node.name}`\n")
                func_doc = ast.get_docstring(node)
                if func_doc:
                    docs.append(f"{func_doc}\n")
                params = [arg.arg for arg in node.args.args]
                if params:
                    docs.append(f"**Parameters:** {', '.join(params)}\n")
                docs.append("\n")
        return "\n".join(docs)

    def validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        if self.language != CodeLanguage.PYTHON:
            return True
        try:
            ast.parse(content)
            return True
        except (SyntaxError, RecursionError, MemoryError) as e:
            logging.error(f"Syntax error in generated code: {e}")
            return False

    def validate_flake8(self, content: str) -> bool:
        """Validate Python code using flake8 if available."""
        if self.language != CodeLanguage.PYTHON:
            return True
        if not shutil.which("flake8"):
            logging.warning("flake8 not found, skipping style validation")
            return True
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            # Run flake8 on the temporary file
            result = subprocess.run(
                ["flake8", "--ignore=E501,F401,W291,W293", tmp_path],
                capture_output=True,
                text=True,
                check=False,
            )

            # Removed self.record_interaction call.
            # Core classes should not have side effects.

            return result.returncode == 0
        except Exception as e:
            logging.error(f"flake8 validation failed: {e}")
            return True
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
