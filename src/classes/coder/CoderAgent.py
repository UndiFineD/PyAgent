#!/usr/bin/env python3

"""Auto-extracted class from agent_coder.py"""

from __future__ import annotations

from .CodeLanguage import CodeLanguage
from .CodeMetrics import CodeMetrics
from .CodeSmell import CodeSmell
from .QualityScore import QualityScore
from .RefactoringPattern import RefactoringPattern
from .StyleRule import StyleRule
from .StyleRuleSeverity import StyleRuleSeverity

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile

# Default style rules for Python
DEFAULT_PYTHON_STYLE_RULES: List[StyleRule] = [
    StyleRule(
        name="line_length",
        pattern=r"^.{89,}$",
        message="Line exceeds 88 characters",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON
    ),
    StyleRule(
        name="trailing_whitespace",
        pattern=r"[ \t]+$",
        message="Trailing whitespace detected",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON
    ),
    StyleRule(
        name="multiple_blank_lines",
        pattern=r"\n{4,}",
        message="More than 2 consecutive blank lines",
        severity=StyleRuleSeverity.INFO,
        language=CodeLanguage.PYTHON
    ),
    StyleRule(
        name="missing_docstring",
        pattern=r"^def\s+\w+\([^)]*\):\s*\n\s+(?!\"\"\")",
        message="Function missing docstring",
        severity=StyleRuleSeverity.WARNING,
        language=CodeLanguage.PYTHON
    ),
]

# Common code smells patterns
CODE_SMELL_PATTERNS: Dict[str, Dict[str, Any]] = {
    "long_method": {
        "threshold": 50,
        "message": "Method is too long (>{threshold} lines)",
        "category": "complexity"
    },
    "too_many_parameters": {
        "threshold": 5,
        "message": "Function has too many parameters (>{threshold})",
        "category": "complexity"
    },
    "duplicate_code": {
        "threshold": 3,
        "message": "Duplicate code detected ({count} occurrences)",
        "category": "duplication"
    },
    "deep_nesting": {
        "threshold": 4,
        "message": "Code is too deeply nested (>{threshold} levels)",
        "category": "complexity"
    },
    "god_class": {
        "threshold": 20,
        "message": "Class has too many methods (>{threshold})",
        "category": "design"
    },
}

class CoderAgent(BaseAgent):
    """Updates code files using AI assistance.

    Invariants:
    - self.file_path must point to a valid file path.

    - Supports Python files (.py) with syntax validation.
    - Supports multi - language code improvements.
    """

    # Language extension mappings
    LANGUAGE_EXTENSIONS: Dict[str, CodeLanguage] = {
        ".py": CodeLanguage.PYTHON,
        ".js": CodeLanguage.JAVASCRIPT,
        ".ts": CodeLanguage.TYPESCRIPT,
        ".java": CodeLanguage.JAVA,
        ".cpp": CodeLanguage.CPP,
        ".cc": CodeLanguage.CPP,
        ".cxx": CodeLanguage.CPP,
        ".go": CodeLanguage.GO,
        ".rs": CodeLanguage.RUST,
        ".rb": CodeLanguage.RUBY,
    }

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        # Create copies of style rules to avoid cross-instance state leakage
        self._style_rules: List[StyleRule] = [
            StyleRule(
                name=r.name,
                pattern=r.pattern,
                message=r.message,
                severity=r.severity,
                enabled=r.enabled,
                language=r.language,
                auto_fix=r.auto_fix
            ) for r in DEFAULT_PYTHON_STYLE_RULES
        ]
        self._language: CodeLanguage = self._detect_language()
        self._metrics: Optional[CodeMetrics] = None
        self._quality_score: Optional[QualityScore] = None
        self._code_smells: List[CodeSmell] = []
        self._refactoring_patterns: List[RefactoringPattern] = []
        self._duplicate_hashes: Dict[str, List[int]] = {}

    def _detect_language(self) -> CodeLanguage:
        """Detect the programming language from file extension."""
        ext = self.file_path.suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(ext, CodeLanguage.UNKNOWN)

    def detect_language(self) -> CodeLanguage:
        """Public wrapper to detect and return the file language.

        Returns:
            The detected CodeLanguage based on file extension.
        """
        self._language = self._detect_language()
        return self._language

    @property
    def language(self) -> CodeLanguage:
        """Get the detected language."""
        return self._language

    @property
    def _is_python_file(self) -> bool:
        """Check if the file is a Python file."""
        return self._language == CodeLanguage.PYTHON

    # ========== Style Enforcement ==========
    def add_style_rule(self, rule: StyleRule) -> None:
        """Add a custom style rule."""
        self._style_rules.append(rule)

    def remove_style_rule(self, rule_name: str) -> bool:
        """Remove a style rule by name."""
        for i, rule in enumerate(self._style_rules):
            if rule.name == rule_name:
                del self._style_rules[i]
                return True
        return False

    def enable_style_rule(self, rule_name: str) -> bool:
        """Enable a style rule."""
        for rule in self._style_rules:
            if rule.name == rule_name:
                rule.enabled = True
                return True
        return False

    def disable_style_rule(self, rule_name: str) -> bool:
        """Disable a style rule."""
        for rule in self._style_rules:
            if rule.name == rule_name:
                rule.enabled = False
                return True
        return False

    def check_style(self, content: str) -> List[Dict[str, Any]]:
        """Check code against all enabled style rules."""
        violations: List[Dict[str, Any]] = []
        lines = content.split('\n')
        for rule in self._style_rules:
            if not rule.enabled:
                continue
            if rule.language and rule.language != self._language:
                continue
            
            # Check multiline patterns if they contain \n or start with ^ in multiline mode
            if '\n' in rule.pattern or rule.pattern.startswith('^'):
                for match in re.finditer(rule.pattern, content, re.MULTILINE):
                    # Calculate line number
                    line_no = content.count('\n', 0, match.start()) + 1
                    violations.append({
                        "rule": rule.name,
                        "message": rule.message,
                        "severity": rule.severity.value,
                        "line": line_no,
                        "content": match.group(0).split('\n')[0][:80]
                    })
            else:
                # Line-by-line check for simple patterns
                for i, line in enumerate(lines, 1):
                    if re.search(rule.pattern, line):
                        violations.append({
                            "rule": rule.name,
                            "message": rule.message,
                            "severity": rule.severity.value,
                            "line": i,
                            "content": line[:80]
                        })
        return violations

    def auto_fix_style(self, content: str) -> Tuple[str, int]:
        """Apply auto-fixes for style violations."""
        fixed_content = content
        fix_count = 0
        for rule in self._style_rules:
            if not rule.enabled or not rule.auto_fix:
                continue
            if rule.language and rule.language != self._language:
                continue
            new_content = rule.auto_fix(fixed_content)
            if new_content != fixed_content:
                fix_count += 1
                fixed_content = new_content
        # Built - in fixes
        # Remove trailing whitespace
        lines = fixed_content.split('\n')
        cleaned = [line.rstrip() for line in lines]
        if cleaned != lines:
            fix_count += 1
        fixed_content = '\n'.join(cleaned)
        return fixed_content, fix_count

    # ========== Code Metrics ==========
    def calculate_metrics(self, content: Optional[str] = None) -> CodeMetrics:
        """Calculate code metrics for the content."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        lines = content.split('\n')
        metrics = CodeMetrics()
        # Basic line counts
        for line in lines:
            stripped = line.strip()
            if not stripped:
                metrics.blank_lines += 1
            elif stripped.startswith('#') or stripped.startswith('//'):
                metrics.lines_of_comments += 1
            else:
                metrics.lines_of_code += 1
        # Python - specific metrics
        if self._is_python_file:
            try:
                tree = ast.parse(content)
                metrics = self._analyze_python_ast(tree, metrics)
            except SyntaxError:
                pass
        # Calculate maintainability index (simplified formula)
        if metrics.lines_of_code > 0:
            halstead_volume = metrics.lines_of_code * math.log2(
                max(1, metrics.function_count + metrics.class_count + 1))
            cc = max(1, metrics.cyclomatic_complexity)
            loc = metrics.lines_of_code
            cm = metrics.lines_of_comments
            # Simplified maintainability index
            metrics.maintainability_index = max(
                0, min(
                    100,
                    171 - 5.2 * math.log(halstead_volume + 1) -
                    0.23 * cc -
                    16.2 * math.log(loc + 1) +
                    50 * math.sin(math.sqrt(2.4 * (cm / (loc + cm + 1))))
                )
            )
        self._metrics = metrics
        return metrics

    def _analyze_python_ast(self, tree: ast.AST, metrics: CodeMetrics) -> CodeMetrics:
        """Analyze Python AST for metrics."""
        function_lengths: List[int] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                metrics.function_count += 1
                if hasattr(node, 'end_lineno') and node.end_lineno is not None:
                    length = node.end_lineno - node.lineno + 1
                    function_lengths.append(length)
                    # Calculate cyclomatic complexity for this function
                    cc = 1  # Base complexity
                    for child in ast.walk(node):
                        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                            cc += 1
                        elif isinstance(child, ast.BoolOp):
                            cc += len(child.values) - 1
                    metrics.cyclomatic_complexity += cc
            elif isinstance(node, ast.ClassDef):
                metrics.class_count += 1
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                metrics.import_count += 1
        if function_lengths:
            metrics.average_function_length = sum(function_lengths) / len(function_lengths)
            metrics.max_function_length = max(function_lengths)
        return metrics

    def _get_test_coverage(self) -> float:
        """Attempt to calculate test coverage for the current file."""
        if not self._is_python_file or not self.file_path.exists():
            return 0.0

        # Heuristic: Check common test locations
        test_file = self.file_path.parent / f"test_{self.file_path.name}"
        if not test_file.exists():
            # Try tests/test_filename.py
            test_file = self.file_path.parent.parent / "tests" / f"test_{self.file_path.name}"

        if not test_file.exists():
            return 0.0

        # If pytest is available, try to run it with coverage
        if shutil.which('pytest'):
            try:
                # Run coverage for just this file
                # Use --cov-fail-under=0 to avoid exit code 1 if coverage is low
                result = subprocess.run(
                    [sys.executable, '-m', 'pytest', '--cov=' + str(self.file_path), '--cov-report=term-missing', str(test_file)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False
                )
                # Parse output for percentage (e.g., TOTAL 10 2 80%)
                match = re.search(r'TOTAL.*?\s+(\d+)%', result.stdout)
                if match:
                    return float(match.group(1))
            except Exception as e:
                logging.debug(f"Coverage calculation failed: {e}")

        return 0.0

    # ========== Code Quality Scoring ==========
    def calculate_quality_score(self, content: Optional[str] = None) -> QualityScore:
        """Calculate an overall code quality score."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        metrics = self.calculate_metrics(content)
        style_violations = self.check_style(content)
        code_smells = self.detect_code_smells(content)
        score = QualityScore()
        # Maintainability score (from maintainability index)
        score.maintainability = min(100, metrics.maintainability_index)
        # Readability score
        readability_deductions = len(style_violations) * 5
        score.readability = max(0, 100 - readability_deductions)
        # Complexity score (inverse of cyclomatic complexity)
        if metrics.function_count > 0:
            avg_cc = metrics.cyclomatic_complexity / metrics.function_count
            score.complexity = max(0, 100 - (avg_cc - 1) * 10)
        else:
            score.complexity = 100
        # Documentation score
        if metrics.lines_of_code > 0:
            comment_ratio = metrics.lines_of_comments / metrics.lines_of_code
            score.documentation = min(100, comment_ratio * 200)
        
        # Real test coverage calculation
        score.test_coverage = self._get_test_coverage()
        
        # Overall score (weighted average)
        score.overall_score = (
            score.maintainability * 0.25 +
            score.readability * 0.25 +
            score.complexity * 0.25 +
            score.documentation * 0.15 +
            score.test_coverage * 0.10
        )
        # Add issues
        for violation in style_violations[:5]:
            score.issues.append(f"Style: {violation['message']} (line {violation['line']})")
        for smell in code_smells[:5]:
            score.issues.append(f"Smell: {smell.description}")
        self._quality_score = score
        return score

    # ========== Code Smell Detection ==========
    def detect_code_smells(self, content: Optional[str] = None) -> List[CodeSmell]:
        """Detect code smells in the content."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        smells: List[CodeSmell] = []
        if not self._is_python_file:
            return smells
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return smells
        lines = content.split('\n')
        for node in ast.walk(tree):
            # Long method detection
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if (hasattr(node, 'end_lineno') and node.end_lineno is not None
                        and hasattr(node, 'lineno')):
                    length = node.end_lineno - node.lineno + 1
                    threshold = CODE_SMELL_PATTERNS["long_method"]["threshold"]
                    if length > threshold:
                        smells.append(
                            CodeSmell(
                                name="long_method",
                                description=(
                                    f"Method '{node.name}' is {length} "
                                    f"lines (>{threshold})"
                                ),
                                severity="warning",
                                line_number=node.lineno,
                                suggestion=(
                                    f"Consider breaking down '{node.name}' "
                                    f"into smaller functions"
                                ),
                                category="complexity"))
                # Too many parameters
                param_count = len(node.args.args)
                threshold = CODE_SMELL_PATTERNS["too_many_parameters"]["threshold"]
                if param_count > threshold:
                    smells.append(
                        CodeSmell(
                            name="too_many_parameters",
                            description=(
                                f"Function '{node.name}' has {param_count} "
                                f"parameters (>{threshold})"
                            ),
                            severity="warning",
                            line_number=node.lineno,
                            suggestion="Consider using a data class or dictionary for parameters",
                            category="complexity"))
            # God class detection
            if isinstance(node, ast.ClassDef):
                method_count = sum(
                    1 for n in node.body if isinstance(
                        n, (ast.FunctionDef, ast.AsyncFunctionDef)))
                threshold = CODE_SMELL_PATTERNS["god_class"]["threshold"]
                if method_count > threshold:
                    smells.append(
                        CodeSmell(
                            name="god_class",
                            description=f"Class '{node.name}' has {method_count} methods (>{threshold})",
                            severity="warning",
                            line_number=node.lineno,
                            suggestion="Consider splitting the class into smaller, more focused classes.",
                            category="design"))

        # Deep nesting detection
        for i, line in enumerate(lines, 1):
            indent = len(line) - len(line.lstrip())
            spaces_per_level = 4
            nesting = indent // spaces_per_level
            threshold = CODE_SMELL_PATTERNS["deep_nesting"]["threshold"]
            if nesting > threshold and line.strip():
                smells.append(CodeSmell(
                    name="deep_nesting",
                    description=f"Code at line {i} has {nesting} levels of nesting (>{threshold})",
                    severity="info",
                    line_number=i,
                    suggestion="Consider early returns or extracting nested logic",
                    category="complexity"
                ))
        
        # Duplicate code detection
        smells.extend(self._detect_duplicate_code(content))
        self._code_smells = smells
        return smells

    def _detect_duplicate_code(self, content: str) -> List[CodeSmell]:
        """Simple heuristic for duplicate line detection."""
        smells = []
        lines = [line.strip() for line in content.split('\n') if len(line.strip()) > 30] # Significant lines only
        from collections import Counter
        counts = Counter(lines)
        for line, count in counts.items():
            if count >= 3:
                smells.append(CodeSmell(
                    name="duplicate_code",
                    description=f"Potential duplicate code detected ({count} occurrences of long lines)",
                    severity="info",
                    line_number=0,
                    suggestion="Consider extracting common logic into a shared helper or utility.",
                    category="duplication"
                ))
        return smells

    # ========== Code Deduplication ==========
    def find_duplicate_code(
        self,
        content: Optional[str] = None,
        min_lines: int = 4
    ) -> List[Dict[str, Any]]:
        """Find duplicate code blocks."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        lines = content.split('\n')
        duplicates: List[Dict[str, Any]] = []
        self._duplicate_hashes = {}
        # Create hashes for consecutive line blocks
        for i in range(len(lines) - min_lines + 1):
            block = '\n'.join(lines[i:i + min_lines])
            # Normalize whitespace for comparison
            normalized = re.sub(r'\s+', ' ', block.strip())
            if len(normalized) < 20:  # Skip very short blocks
                continue
            block_hash = hashlib.md5(normalized.encode()).hexdigest()
            if block_hash not in self._duplicate_hashes:
                self._duplicate_hashes[block_hash] = []
            self._duplicate_hashes[block_hash].append(i + 1)
        # Find actual duplicates
        for block_hash, line_numbers in self._duplicate_hashes.items():
            if len(line_numbers) > 1:
                duplicates.append({
                    "hash": block_hash,
                    "occurrences": len(line_numbers),
                    "lines": line_numbers,
                    "preview": '\n'.join(
                        lines[line_numbers[0] - 1:line_numbers[0] - 1 + min_lines]
                    )[:100]
                    })
        return duplicates

    def get_duplicate_ratio(self, content: Optional[str] = None) -> float:
        """Calculate the ratio of duplicate code."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        duplicates = self.find_duplicate_code(content)
        total_lines = len(content.split('\n'))
        if total_lines == 0:
            return 0.0
        duplicate_lines = sum(
            (d["occurrences"] - 1) * 4  # min_lines default
            for d in duplicates
        )
        return min(1.0, duplicate_lines / total_lines)

    # ========== Refactoring Patterns ==========
    def add_refactoring_pattern(self, pattern: RefactoringPattern) -> None:
        """Add a refactoring pattern."""
        self._refactoring_patterns.append(pattern)

    def apply_refactoring_patterns(self, content: str) -> Tuple[str, List[str]]:
        """Apply all registered refactoring patterns."""
        result = content
        applied: List[str] = []
        for pattern in self._refactoring_patterns:
            if pattern.language != self._language:
                continue
            new_result = re.sub(pattern.pattern, pattern.replacement, result)
            if new_result != result:
                applied.append(pattern.name)
                result = new_result
        return result, applied

    def suggest_refactorings(self, content: Optional[str] = None) -> List[Dict[str, str]]:
        """Suggest possible refactorings based on code analysis."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        suggestions: List[Dict[str, str]] = []
        # Detect code smells and suggest refactorings
        smells = self.detect_code_smells(content)
        for smell in smells:
            if smell.name == "long_method":
                suggestions.append({
                    "type": "extract_method",
                    "description": f"Extract parts of method at line {smell.line_number}",
                    "reason": smell.description
                })
            elif smell.name == "too_many_parameters":
                suggestions.append({
                    "type": "introduce_parameter_object",
                    "description": (
                        f"Create a data class for parameters at "
                        f"line {smell.line_number}"
                    ),
                    "reason": smell.description
                })
            elif smell.name == "god_class":
                suggestions.append({
                    "type": "extract_class",
                    "description": f"Split class at line {smell.line_number} into focused classes",
                    "reason": smell.description
                })
        # Check for duplicate code
        duplicates = self.find_duplicate_code(content)
        if duplicates:
            suggestions.append({
                "type": "extract_method",
                "description": (
                    f"Extract {len(duplicates)} duplicate code blocks "
                    f"into shared methods"
                ),
                "reason": f"Found {len(duplicates)} duplicate code patterns"
            })
        return suggestions

    # ========== Documentation Generation ==========
    def generate_documentation(self, content: Optional[str] = None) -> str:
        """Generate documentation from code."""
        if content is None:
            content = self.current_content or self.previous_content or ""
        if not self._is_python_file:
            return "# Documentation\n\nDocumentation generation is only supported for Python files."
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return "# Documentation\n\nUnable to parse file for documentation."
        docs: List[str] = ["# API Documentation\n"]
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
                        params = [arg.arg for arg in item.args.args if arg.arg != 'self']
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
        return '\n'.join(docs)

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return default content for new code files."""
        return "# Code file\n\n# Add code here\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original code preserved below:\n\n")

    def _validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        if not self._is_python_file:
            return True
        try:
            ast.parse(content)
            return True
        except (SyntaxError, RecursionError, MemoryError) as e:
            logging.error(f"Syntax error in generated code: {e}")
            return False

    def _validate_flake8(self, content: str) -> bool:
        """Validate Python code using flake8 if available."""
        if not self._is_python_file:
            return True
        if not shutil.which('flake8'):
            logging.warning("flake8 not found, skipping style validation")
            return True
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            # Run flake8 on the temporary file
            # We ignore some common errors that might be acceptable in generated code
            # E501: Line too long
            # W293: Blank line contains whitespace
            result = subprocess.run(
                ['flake8', '--ignore=E501,W293', tmp_path],
                capture_output=True,
                text=True,
                timeout=30,
                check=False
            )
            if result.returncode != 0:
                logging.warning(f"flake8 validation failed:\n{result.stdout}")
                return False  # Soft validation failure
            return True
        finally:
            try:
                Path(tmp_path).unlink()
            except OSError:
                pass

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the code with specific coding suggestions."""
        logging.info(f"Improving content for {self.file_path}")
        # Call base implementation directly to use AI backend
        new_content = super().improve_content(prompt)
        # Validate syntax
        if not self._validate_syntax(new_content):
            logging.error("Generated code failed syntax validation. Reverting.")
            self.current_content = self.previous_content
            return self.previous_content
        logging.debug("Syntax validation passed")
        # Validate style (flake8)
        if not self._validate_flake8(new_content):
            logging.warning("Generated code failed style validation (flake8). Proceeding anyway.")
        else:
            logging.debug("Style validation passed")
        return new_content
