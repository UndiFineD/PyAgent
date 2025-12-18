#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE - 2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Coder Agent: Improves and updates code files.

Reads a code file, uses Copilot to enhance the code,
and updates the code file with improvements.

## Description
This module provides a Coder Agent that reads existing code files,
uses AI assistance to improve and complete them, and updates the code files
with enhanced implementations.

## Changelog
- 1.0.0: Initial implementation
- 1.1.0: Added code style enforcement, multi - language support, metrics, quality scoring

## Suggested Fixes
- Add validation for code file format
- Improve prompt engineering for better code improvements

## Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

from __future__ import annotations
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from base_agent import BaseAgent, create_main_function


class CodeLanguage(Enum):
    """Supported code languages."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    RUBY = "ruby"
    UNKNOWN = "unknown"


class StyleRuleSeverity(Enum):
    """Severity levels for style rules."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class StyleRule:
    """A configurable code style rule."""
    name: str
    pattern: str
    message: str
    severity: StyleRuleSeverity = StyleRuleSeverity.WARNING
    enabled: bool = True
    language: Optional[CodeLanguage] = None
    auto_fix: Optional[Callable[[str], str]] = None


@dataclass
class CodeMetrics:
    """Code quality metrics."""
    lines_of_code: int = 0
    lines_of_comments: int = 0
    blank_lines: int = 0
    cyclomatic_complexity: float = 0.0
    maintainability_index: float = 100.0
    function_count: int = 0
    class_count: int = 0
    import_count: int = 0
    average_function_length: float = 0.0
    max_function_length: int = 0
    duplicate_code_ratio: float = 0.0


@dataclass
class CodeSmell:
    """A detected code smell."""
    name: str
    description: str
    severity: str
    line_number: int
    suggestion: str
    category: str = "general"


@dataclass
class QualityScore:
    """Code quality score with breakdown."""
    score: float = 0.0
    maintainability: float = 0.0
    readability: float = 0.0
    complexity: float = 0.0
    documentation: float = 0.0
    test_coverage: float = 0.0
    issues: List[str] = field(default_factory=list)

    @property
    def overall_score(self) -> float:
        """Alias for score."""
        return self.score


@dataclass
class RefactoringPattern:
    """A code refactoring pattern."""
    name: str
    description: str
    pattern: str
    replacement: str
    language: CodeLanguage = CodeLanguage.PYTHON


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


# ========== Session 6 Enums ==========


class MigrationStatus(Enum):
    """Status of a code migration operation."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class ReviewCategory(Enum):
    """Categories for code review feedback."""
    STYLE = "style"
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    CORRECTNESS = "correctness"
    DOCUMENTATION = "documentation"


class OptimizationType(Enum):
    """Types of code optimization."""
    ALGORITHMIC = "algorithmic"
    MEMORY = "memory"
    IO = "io"
    CONCURRENCY = "concurrency"
    CACHING = "caching"


class SecurityIssueType(Enum):
    """Types of security vulnerabilities."""
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    HARDCODED_SECRET = "hardcoded_secret"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    INSECURE_RANDOM = "insecure_random"


class ProfilingCategory(Enum):
    """Categories for code profiling suggestions."""
    CPU_BOUND = "cpu_bound"
    IO_BOUND = "io_bound"
    MEMORY_INTENSIVE = "memory_intensive"
    NETWORK_BOUND = "network_bound"


class DependencyType(Enum):
    """Types of code dependencies."""
    IMPORT = "import"
    FUNCTION_CALL = "function_call"
    CLASS_INHERITANCE = "class_inheritance"
    VARIABLE_REFERENCE = "variable_reference"


# ========== Session 6 Dataclasses ==========


@dataclass
class MigrationRule:
    """A rule for code migration from old to new API.

    Attributes:
        name: Rule identifier.
        old_pattern: Regex pattern to match old API usage.
        new_pattern: Replacement pattern for new API.
        description: Human - readable description of the migration.
        status: Current status of this migration rule.
        breaking_change: Whether this is a breaking change.
    """
    name: str
    old_pattern: str
    new_pattern: str
    description: str
    status: MigrationStatus = MigrationStatus.PENDING
    breaking_change: bool = False


@dataclass
class ReviewFinding:
    """A finding from automated code review.

    Attributes:
        category: Category of the finding.
        message: Description of the issue.
        line_number: Line where the issue was found.
        severity: Severity level (1 - 5).
        suggestion: Suggested fix.
        auto_fixable: Whether this can be auto - fixed.
    """
    category: ReviewCategory
    message: str
    line_number: int
    severity: int
    suggestion: str
    auto_fixable: bool = False


@dataclass
class OptimizationSuggestion:
    """A suggestion for code optimization.

    Attributes:
        type: Type of optimization.
        description: What to optimize.
        impact: Expected performance impact (low / medium / high).
        code_location: File and line information.
        before_snippet: Code before optimization.
        after_snippet: Suggested optimized code.
    """
    type: OptimizationType
    description: str
    impact: str
    code_location: str
    before_snippet: str = ""
    after_snippet: str = ""


@dataclass
class SecurityVulnerability:
    """A detected security vulnerability.

    Attributes:
        type: Type of security issue.
        severity: CVSS - like severity (critical / high / medium / low).
        description: Description of the vulnerability.
        line_number: Where the vulnerability was detected.
        fix_suggestion: How to fix the vulnerability.
        cwe_id: Common Weakness Enumeration ID.
    """
    type: SecurityIssueType
    severity: str
    description: str
    line_number: int
    fix_suggestion: str
    cwe_id: Optional[str] = None


@dataclass
class ModernizationSuggestion:
    """Suggestion to modernize deprecated API usage.

    Attributes:
        old_api: The deprecated API being used.
        new_api: The modern replacement API.
        deprecation_version: Version where the old API was deprecated.
        removal_version: Version where it will be removed.
        migration_guide: URL or text explaining migration.
    """
    old_api: str
    new_api: str
    deprecation_version: str
    removal_version: Optional[str] = None
    migration_guide: str = ""


@dataclass
class TestGap:
    """An identified gap in test coverage.

    Attributes:
        function_name: Name of the untested function.
        file_path: Path to the file containing the function.
        line_number: Line where the function is defined.
        complexity: Cyclomatic complexity of the function.
        suggested_tests: List of suggested test cases.
    """
    function_name: str
    file_path: str
    line_number: int
    complexity: int
    suggested_tests: List[str] = field(default_factory=list)


@dataclass
class ConsistencyIssue:
    """A code consistency issue across the codebase.

    Attributes:
        issue_type: Type of inconsistency.
        description: Description of the issue.
        occurrences: List of file:line locations.
        recommended_style: The recommended consistent style.
    """
    issue_type: str
    description: str
    occurrences: List[str]
    recommended_style: str


@dataclass
class ProfilingSuggestion:
    """A code profiling suggestion.

    Attributes:
        category: Category of the profiling suggestion.
        function_name: Function that could benefit from profiling.
        reason: Why this function should be profiled.
        estimated_impact: Estimated performance impact.
        profiling_approach: Suggested profiling approach.
    """
    category: ProfilingCategory
    function_name: str
    reason: str
    estimated_impact: str
    profiling_approach: str


@dataclass
class DependencyNode:
    """A node in the dependency graph.

    Attributes:
        name: Name of the module / class / function.
        type: Type of dependency.
        depends_on: List of dependencies.
        depended_by: List of dependents.
        file_path: Path to the file.
    """
    name: str
    type: DependencyType
    depends_on: List[str] = field(default_factory=list)
    depended_by: List[str] = field(default_factory=list)
    file_path: str = ""


# ========== Session 6 Helper Classes ==========


class MigrationManager:
    """Manages code migration from old APIs to new ones.

    This class provides functionality to define migration rules,
    apply them to code, and track migration status.

    Attributes:
        rules: List of migration rules.

    Example:
        >>> manager=MigrationManager()
        >>> manager.add_rule(MigrationRule(
        ...     name="urllib2_to_urllib",
        ...     old_pattern=r"import urllib2",
        ...     new_pattern="import urllib.request",
        ...     description="Migrate urllib2 to urllib.request"
        ... ))
        >>> code, results=manager.apply_migrations("import urllib2")
    """

    def __init__(self) -> None:
        """Initialize the migration manager."""
        self.rules: List[MigrationRule] = []

    def add_rule(self, rule: MigrationRule) -> None:
        """Add a migration rule.

        Args:
            rule: The migration rule to add.
        """
        self.rules.append(rule)

    def apply_migrations(self, content: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply all migration rules to content.

        Args:
            content: The source code to migrate.

        Returns:
            Tuple of migrated content and list of applied migrations.
        """
        result = content
        applied: List[Dict[str, Any]] = []

        for rule in self.rules:
            if rule.status == MigrationStatus.SKIPPED:
                continue
            rule.status = MigrationStatus.IN_PROGRESS
            new_result = re.sub(rule.old_pattern, rule.new_pattern, result)
            if new_result != result:
                applied.append({
                    "rule": rule.name,
                    "description": rule.description,
                    "breaking_change": rule.breaking_change
                })
                rule.status = MigrationStatus.COMPLETED
                result = new_result
            else:
                rule.status = MigrationStatus.PENDING

        return result, applied

    def get_pending_migrations(self) -> List[MigrationRule]:
        """Get list of pending migration rules.

        Returns:
            List of rules with pending status.
        """
        return [r for r in self.rules if r.status == MigrationStatus.PENDING]


class CodeReviewer:
    """Automated code review system.

    Provides automated code review with actionable suggestions
    across multiple categories.

    Attributes:
        findings: List of review findings.

    Example:
        >>> reviewer=CodeReviewer()
        >>> findings=reviewer.review_code("def foo():\\n    pass")
    """

    def __init__(self) -> None:
        """Initialize the code reviewer."""
        self.findings: List[ReviewFinding] = []

    def review_code(self, content: str) -> List[ReviewFinding]:
        """Perform automated code review.

        Args:
            content: Source code to review.

        Returns:
            List of review findings.
        """
        self.findings = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Style checks
            if len(line) > 120:
                self.findings.append(ReviewFinding(
                    category=ReviewCategory.STYLE,
                    message=f"Line exceeds 120 characters ({len(line)})",
                    line_number=i,
                    severity=2,
                    suggestion="Break line into multiple lines",
                    auto_fixable=False
                ))

            # Security checks
            if re.search(r"password\s*=\s*['\"][^'\"]+['\"]", line, re.I):
                self.findings.append(ReviewFinding(
                    category=ReviewCategory.SECURITY,
                    message="Potential hardcoded password",
                    line_number=i,
                    severity=5,
                    suggestion="Use environment variables or secure vault",
                    auto_fixable=False
                ))

            # Performance checks
            if re.search(r"for\s+\w+\s+in\s+range\(len\(", line):
                self.findings.append(ReviewFinding(
                    category=ReviewCategory.PERFORMANCE,
                    message="Inefficient iteration pattern",
                    line_number=i,
                    severity=2,
                    suggestion="Use 'enumerate()' instead of 'range(len())'",
                    auto_fixable=True
                ))

            # Documentation checks
            if re.match(r"^\s*def\s+[a-z_]\w*\s*\(", line):
                # Check for docstring on next line
                if i < len(lines) and '"""' not in lines[i]:
                    self.findings.append(ReviewFinding(
                        category=ReviewCategory.DOCUMENTATION,
                        message="Function missing docstring",
                        line_number=i,
                        severity=3,
                        suggestion="Add docstring describing function purpose",
                        auto_fixable=False
                    ))

        return self.findings

    def get_summary(self) -> Dict[str, int]:
        """Get summary of findings by category.

        Returns:
            Dictionary mapping category to count.
        """
        summary: Dict[str, int] = {}
        for finding in self.findings:
            cat = finding.category.value
            summary[cat] = summary.get(cat, 0) + 1
        return summary


class PerformanceOptimizer:
    """Identifies and suggests code optimizations.

    Analyzes code for performance bottlenecks and suggests
    improvements.

    Attributes:
        suggestions: List of optimization suggestions.

    Example:
        >>> optimizer=PerformanceOptimizer()
        >>> suggestions=optimizer.analyze("for i in range(len(items)):")
    """

    OPTIMIZATION_PATTERNS: List[Tuple[str, OptimizationType, str, str]] = [
        (r"for\s+\w+\s+in\s+range\(len\((\w+)\)\)", OptimizationType.ALGORITHMIC,
         "Use enumerate() instead of range(len())",
         "for idx, item in enumerate({0}):"),
        (r"\+=\s*.*?for\s+", OptimizationType.MEMORY,
         "String concatenation in loop is inefficient",
         "Use ''.join() or list comprehension"),
        (r"time\.sleep\(\d+\)", OptimizationType.CONCURRENCY,
         "Blocking sleep may hurt performance",
         "Consider asyncio.sleep() for async code"),
    ]

    def __init__(self) -> None:
        """Initialize the performance optimizer."""
        self.suggestions: List[OptimizationSuggestion] = []

    def analyze(self, content: str) -> List[OptimizationSuggestion]:
        """Analyze code for optimization opportunities.

        Args:
            content: Source code to analyze.

        Returns:
            List of optimization suggestions.
        """
        self.suggestions = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for pattern, opt_type, desc, fix in self.OPTIMIZATION_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    self.suggestions.append(OptimizationSuggestion(
                        type=opt_type,
                        description=desc,
                        impact="medium",
                        code_location=f"line {i}",
                        before_snippet=line.strip(),
                        after_snippet=fix.format(*match.groups()) if match.groups() else fix
                    ))

        return self.suggestions


class SecurityScanner:
    """Scans code for security vulnerabilities.

    Identifies common security issues and provides remediation guidance.

    Attributes:
        vulnerabilities: List of detected vulnerabilities.

    Example:
        >>> scanner=SecurityScanner()
        >>> vulns=scanner.scan("password='secret123'")
    """

    SECURITY_PATTERNS: List[Tuple[str, SecurityIssueType, str, str, str]] = [
        (r"password\s*=\s*['\"][^'\"]+['\"]",
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded password detected",
         "Use environment variables or secure vault"),
        (r"api_key\s*=\s*['\"][^'\"]+['\"]",
         SecurityIssueType.HARDCODED_SECRET, "high",
         "Hardcoded API key detected",
         "Use environment variables or secure vault"),
        (r"os\.system\s*\([^)]*\+",
         SecurityIssueType.COMMAND_INJECTION, "critical",
         "Potential command injection vulnerability",
         "Use subprocess with shell=False and proper escaping"),
        (r"eval\s*\(",
         SecurityIssueType.INSECURE_DESERIALIZATION, "critical",
         "Use of eval() is dangerous",
         "Avoid eval() or use ast.literal_eval() for safe parsing"),
        (r"random\.(random|randint|choice)\s*\(",
         SecurityIssueType.INSECURE_RANDOM, "medium",
         "Insecure random number generation for security context",
         "Use secrets module for cryptographic randomness"),
        (r"open\s*\([^)]*\+",
         SecurityIssueType.PATH_TRAVERSAL, "high",
         "Potential path traversal vulnerability",
         "Validate and sanitize file paths"),
    ]

    def __init__(self) -> None:
        """Initialize the security scanner."""
        self.vulnerabilities: List[SecurityVulnerability] = []

    def scan(self, content: str) -> List[SecurityVulnerability]:
        """Scan code for security vulnerabilities.

        Args:
            content: Source code to scan.

        Returns:
            List of detected vulnerabilities.
        """
        self.vulnerabilities = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            for pattern, issue_type, severity, desc, fix in self.SECURITY_PATTERNS:
                if re.search(pattern, line, re.I):
                    self.vulnerabilities.append(SecurityVulnerability(
                        type=issue_type,
                        severity=severity,
                        description=desc,
                        line_number=i,
                        fix_suggestion=fix
                    ))

        return self.vulnerabilities

    def get_critical_count(self) -> int:
        """Get count of critical vulnerabilities.

        Returns:
            Number of critical severity vulnerabilities.
        """
        return sum(1 for v in self.vulnerabilities if v.severity == "critical")


class ModernizationAdvisor:
    """Advises on modernizing deprecated APIs.

    Tracks deprecated API usage and suggests modern replacements.

    Attributes:
        suggestions: List of modernization suggestions.

    Example:
        >>> advisor=ModernizationAdvisor()
        >>> suggestions=advisor.analyze("import urllib2")
    """

    DEPRECATIONS: List[Tuple[str, str, str, Optional[str], str]] = [
        (r"import\s+urllib2", "urllib.request", "2.7", "3.0",
         "https://docs.python.org/3/library/urllib.request.html"),
        (r"from\s+collections\s+import\s+.*\bMapping\b",
         "collections.abc.Mapping", "3.3", "3.10",
         "Use collections.abc instead of collections for ABCs"),
        (r"\.encode\s*\(\s*['\"]hex['\"]\s*\)",
         "binascii.hexlify()", "3.0", None,
         "Use binascii.hexlify() instead of .encode('hex')"),
        (r"asyncio\.get_event_loop\(\)",
         "asyncio.get_running_loop() or asyncio.new_event_loop()", "3.10", None,
         "get_event_loop() deprecated in favor of more explicit alternatives"),
    ]

    def __init__(self) -> None:
        """Initialize the modernization advisor."""
        self.suggestions: List[ModernizationSuggestion] = []

    def analyze(self, content: str) -> List[ModernizationSuggestion]:
        """Analyze code for deprecated API usage.

        Args:
            content: Source code to analyze.

        Returns:
            List of modernization suggestions.
        """
        self.suggestions = []

        for pattern, new_api, dep_ver, rem_ver, guide in self.DEPRECATIONS:
            if re.search(pattern, content):
                self.suggestions.append(ModernizationSuggestion(
                    old_api=pattern,
                    new_api=new_api,
                    deprecation_version=dep_ver,
                    removal_version=rem_ver,
                    migration_guide=guide
                ))

        return self.suggestions


class TestGapAnalyzer:
    """Identifies gaps in test coverage.

    Analyzes code to find functions lacking test coverage
    and suggests test cases.

    Attributes:
        gaps: List of identified test gaps.

    Example:
        >>> analyzer=TestGapAnalyzer()
        >>> gaps=analyzer.analyze("def untested_func(): pass", "test_file.py")
    """

    def __init__(self) -> None:
        """Initialize the test gap analyzer."""
        self.gaps: List[TestGap] = []

    def analyze(self, content: str, file_path: str) -> List[TestGap]:
        """Analyze code for test coverage gaps.

        Args:
            content: Source code to analyze.
            file_path: Path to the source file.

        Returns:
            List of test coverage gaps.
        """
        self.gaps = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self.gaps

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private and dunder methods
                if node.name.startswith('_') and not node.name.startswith('__'):
                    continue

                complexity = self._calculate_complexity(node)
                suggested_tests = self._suggest_tests(node)

                self.gaps.append(TestGap(
                    function_name=node.name,
                    file_path=file_path,
                    line_number=node.lineno,
                    complexity=complexity,
                    suggested_tests=suggested_tests
                ))

        return self.gaps

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function.

        Args:
            node: AST node of the function.

        Returns:
            Cyclomatic complexity score.
        """
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler,
                                  ast.With, ast.Assert, ast.comprehension)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _suggest_tests(self, node: ast.AST) -> List[str]:
        """Suggest test cases for a function.

        Args:
            node: AST node of the function.

        Returns:
            List of suggested test case descriptions.
        """
        func_node = node  # type: ignore
        suggestions: List[str] = []
        name = func_node.name

        suggestions.append(f"test_{name}_returns_expected_result")
        suggestions.append(f"test_{name}_handles_edge_cases")

        # Check for exception handling
        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                suggestions.append(f"test_{name}_raises_expected_exception")
                break

        return suggestions


class ConsistencyChecker:
    """Checks code consistency across the codebase.

    Identifies inconsistencies in naming, formatting, and patterns.

    Attributes:
        issues: List of consistency issues.

    Example:
        >>> checker=ConsistencyChecker()
        >>> issues=checker.check(["file1.py", "file2.py"], {})
    """

    def __init__(self) -> None:
        """Initialize the consistency checker."""
        self.issues: List[ConsistencyIssue] = []

    def check(self, file_contents: Dict[str, str]) -> List[ConsistencyIssue]:
        """Check for consistency issues across files.

        Args:
            file_contents: Dictionary mapping file paths to contents.

        Returns:
            List of consistency issues.
        """
        self.issues = []

        # Check naming conventions
        self._check_naming_consistency(file_contents)

        # Check import styles
        self._check_import_consistency(file_contents)

        return self.issues

    def _check_naming_consistency(self, file_contents: Dict[str, str]) -> None:
        """Check naming convention consistency.

        Args:
            file_contents: Dictionary mapping file paths to contents.
        """
        snake_case_files: List[str] = []
        camel_case_files: List[str] = []

        for path, content in file_contents.items():
            funcs = re.findall(r"def\s+([a-zA-Z_]\w*)", content)
            for func in funcs:
                if '_' in func and func[0].islower():
                    snake_case_files.append(f"{path}:{func}")
                elif func[0].isupper() or (func[0].islower() and any(c.isupper() for c in func)):
                    camel_case_files.append(f"{path}:{func}")

        if snake_case_files and camel_case_files:
            self.issues.append(ConsistencyIssue(
                issue_type="naming_convention",
                description="Mixed naming conventions detected",
                occurrences=snake_case_files[:3] + camel_case_files[:3],
                recommended_style="snake_case for functions (PEP 8)"
            ))

    def _check_import_consistency(self, file_contents: Dict[str, str]) -> None:
        """Check import statement consistency.

        Args:
            file_contents: Dictionary mapping file paths to contents.
        """
        absolute_imports: List[str] = []
        relative_imports: List[str] = []

        for path, content in file_contents.items():
            if re.search(r"^from\s+\.", content, re.M):
                relative_imports.append(path)
            if re.search(r"^from\s+[a-zA-Z]", content, re.M):
                absolute_imports.append(path)

        if absolute_imports and relative_imports:
            self.issues.append(ConsistencyIssue(
                issue_type="import_style",
                description="Mixed import styles (absolute and relative)",
                occurrences=absolute_imports[:3] + relative_imports[:3],
                recommended_style="Prefer absolute imports (PEP 8)"
            ))


class ProfilingAdvisor:
    """Provides code profiling suggestions.

    Analyzes code to identify functions that would benefit
    from profiling.

    Attributes:
        suggestions: List of profiling suggestions.

    Example:
        >>> advisor=ProfilingAdvisor()
        >>> suggestions=advisor.analyze("def slow_func(): time.sleep(10)")
    """

    def __init__(self) -> None:
        """Initialize the profiling advisor."""
        self.suggestions: List[ProfilingSuggestion] = []

    def analyze(self, content: str) -> List[ProfilingSuggestion]:
        """Analyze code for profiling opportunities.

        Args:
            content: Source code to analyze.

        Returns:
            List of profiling suggestions.
        """
        self.suggestions = []

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self.suggestions

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self._analyze_function(node)

        return self.suggestions

    def _analyze_function(self, node: ast.FunctionDef) -> None:
        """Analyze a function for profiling needs.

        Args:
            node: AST node of the function.
        """
        has_loop = False
        has_io = False
        has_network = False

        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                has_loop = True
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Attribute):
                    name = child.func.attr
                    if name in ('read', 'write', 'open', 'close'):
                        has_io = True
                    if name in ('get', 'post', 'request', 'connect'):
                        has_network = True

        if has_loop:
            self.suggestions.append(ProfilingSuggestion(
                category=ProfilingCategory.CPU_BOUND,
                function_name=node.name,
                reason="Contains loops that may be CPU-intensive",
                estimated_impact="medium",
                profiling_approach="Use cProfile or line_profiler"
            ))

        if has_io:
            self.suggestions.append(ProfilingSuggestion(
                category=ProfilingCategory.IO_BOUND,
                function_name=node.name,
                reason="Contains I / O operations that may block",
                estimated_impact="high",
                profiling_approach="Use async profiling or io tracing"
            ))

        if has_network:
            self.suggestions.append(ProfilingSuggestion(
                category=ProfilingCategory.NETWORK_BOUND,
                function_name=node.name,
                reason="Contains network operations",
                estimated_impact="high",
                profiling_approach="Monitor network latency and throughput"
            ))


class DependencyAnalyzer:
    """Analyzes code dependencies.

    Builds a dependency graph and provides analysis capabilities.

    Attributes:
        nodes: Dictionary of dependency nodes.

    Example:
        >>> analyzer=DependencyAnalyzer()
        >>> graph=analyzer.analyze("from os import path")
    """

    def __init__(self) -> None:
        """Initialize the dependency analyzer."""
        self.nodes: Dict[str, DependencyNode] = {}

    def analyze(self, content: str, file_path: str = "") -> Dict[str, DependencyNode]:
        """Analyze code dependencies.

        Args:
            content: Source code to analyze.
            file_path: Path to the source file.

        Returns:
            Dictionary of dependency nodes.
        """
        self.nodes = {}

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self.nodes

        # Analyze imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._add_dependency(alias.name, DependencyType.IMPORT, file_path)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                self._add_dependency(module, DependencyType.IMPORT, file_path)

        # Analyze class inheritance
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        self._add_dependency(
                            base.id,
                            DependencyType.CLASS_INHERITANCE,
                            file_path
                        )

        return self.nodes

    def _add_dependency(self, name: str, dep_type: DependencyType, file_path: str) -> None:
        """Add a dependency to the graph.

        Args:
            name: Name of the dependency.
            dep_type: Type of dependency.
            file_path: Path where the dependency is used.
        """
        if name not in self.nodes:
            self.nodes[name] = DependencyNode(
                name=name,
                type=dep_type,
                file_path=file_path
            )
        else:
            self.nodes[name].depended_by.append(file_path)

    def get_external_dependencies(self) -> List[str]:
        """Get list of external (non-local) dependencies.

        Returns:
            List of external dependency names.
        """
        stdlib_modules = {
            'os', 'sys', 're', 'json', 'ast', 'hashlib', 'logging',
            'pathlib', 'typing', 'dataclasses', 'enum', 'subprocess',
            'tempfile', 'shutil', 'math', 'collections', 'functools'
        }
        external = []
        for name, node in self.nodes.items():
            if node.type == DependencyType.IMPORT:
                base_module = name.split('.')[0]
                if base_module not in stdlib_modules:
                    external.append(name)
        return external


# =============================================================================
# Session 8 Enums
# =============================================================================
class AccessibilityIssueType(Enum):
    """Types of accessibility issues in UI code."""
    MISSING_ALT_TEXT = "missing_alt_text"
    LOW_COLOR_CONTRAST = "low_color_contrast"
    MISSING_LABEL = "missing_label"
    KEYBOARD_NAVIGATION = "keyboard_navigation"
    FOCUS_MANAGEMENT = "focus_management"
    ARIA_MISSING = "aria_missing"
    ARIA_INVALID = "aria_invalid"
    HEADING_HIERARCHY = "heading_hierarchy"
    FORM_VALIDATION = "form_validation"
    SEMANTIC_HTML = "semantic_html"


class AccessibilitySeverity(Enum):
    """Severity levels for accessibility issues."""
    CRITICAL = 4  # Blocks access for users with disabilities
    SERIOUS = 3   # Significant barrier to access
    MODERATE = 2  # Some difficulty for users
    MINOR = 1     # Cosmetic or minor inconvenience


class WCAGLevel(Enum):
    """WCAG conformance levels."""
    A = "A"       # Minimum level
    AA = "AA"     # Mid - range level (legal requirement in many jurisdictions)
    AAA = "AAA"   # Highest level


# =============================================================================
# Session 8 Dataclasses
# =============================================================================
@dataclass
class AccessibilityIssue:
    """An accessibility issue found in UI code.

    Attributes:
        issue_type: Type of accessibility issue.
        severity: Severity level.
        wcag_level: WCAG conformance level affected.
        wcag_criterion: Specific WCAG criterion (e.g., "1.1.1").
        description: Human - readable description.
        element: UI element identifier or selector.
        line_number: Line number in source file.
        suggested_fix: Suggested fix for the issue.
        auto_fixable: Whether the issue can be auto - fixed.
    """
    issue_type: AccessibilityIssueType
    severity: AccessibilitySeverity
    wcag_level: WCAGLevel
    wcag_criterion: str
    description: str
    element: str
    line_number: Optional[int] = None
    suggested_fix: Optional[str] = None
    auto_fixable: bool = False


@dataclass
class ColorContrastResult:
    """Result of color contrast analysis.

    Attributes:
        foreground: Foreground color (hex).
        background: Background color (hex).
        contrast_ratio: Calculated contrast ratio.
        passes_aa: Whether it passes WCAG AA.
        passes_aaa: Whether it passes WCAG AAA.
        min_ratio_aa: Minimum required ratio for AA.
        min_ratio_aaa: Minimum required ratio for AAA.
    """
    foreground: str
    background: str
    contrast_ratio: float
    passes_aa: bool = False
    passes_aaa: bool = False
    min_ratio_aa: float = 4.5
    min_ratio_aaa: float = 7.0


@dataclass
class AccessibilityReport:
    """Comprehensive accessibility report.

    Attributes:
        file_path: Path to analyzed file.
        issues: List of accessibility issues.
        total_elements: Total UI elements analyzed.
        wcag_level: Target WCAG level.
        compliance_score: Overall compliance score (0 - 100).
        critical_count: Number of critical issues.
        serious_count: Number of serious issues.
        recommendations: High - level recommendations.
    """
    file_path: str
    issues: List[AccessibilityIssue] = field(default_factory=list)
    total_elements: int = 0
    wcag_level: WCAGLevel = WCAGLevel.AA
    compliance_score: float = 100.0
    critical_count: int = 0
    serious_count: int = 0
    recommendations: List[str] = field(default_factory=list)


@dataclass
class ARIAAttribute:
    """ARIA attribute definition.

    Attributes:
        name: ARIA attribute name (e.g., "aria-label").
        value: Current value.
        is_valid: Whether the value is valid.
        allowed_values: List of allowed values (if constrained).
        suggestion: Suggested improvement.
    """
    name: str
    value: str = ""
    is_valid: bool = True
    allowed_values: List[str] = field(default_factory=list)
    suggestion: Optional[str] = None


# =============================================================================
# Session 8 Helper Classes
# =============================================================================


class AccessibilityAnalyzer:
    """Analyzer for accessibility issues in UI code.

    Detects accessibility problems and suggests improvements
    for web and GUI applications.

    Attributes:
        target_level: Target WCAG conformance level.
        issues: Detected issues.
        rules: Enabled accessibility rules.

    Example:
        analyzer=AccessibilityAnalyzer(WCAGLevel.AA)
        report=analyzer.analyze_file("component.py")
        for issue in report.issues:
            print(f"{issue.severity.name}: {issue.description}")
    """

    # WCAG criterion to issue type mapping
    WCAG_CRITERIA: Dict[str, Tuple[AccessibilityIssueType, str]] = {
        "1.1.1": (AccessibilityIssueType.MISSING_ALT_TEXT, "Non-text Content"),
        "1.3.1": (AccessibilityIssueType.SEMANTIC_HTML, "Info and Relationships"),
        "1.4.3": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Minimum)"),
        "1.4.6": (AccessibilityIssueType.LOW_COLOR_CONTRAST, "Contrast (Enhanced)"),
        "2.1.1": (AccessibilityIssueType.KEYBOARD_NAVIGATION, "Keyboard"),
        "2.4.3": (AccessibilityIssueType.FOCUS_MANAGEMENT, "Focus Order"),
        "2.4.6": (AccessibilityIssueType.HEADING_HIERARCHY, "Headings and Labels"),
        "3.3.1": (AccessibilityIssueType.FORM_VALIDATION, "Error Identification"),
        "3.3.2": (AccessibilityIssueType.MISSING_LABEL, "Labels or Instructions"),
        "4.1.2": (AccessibilityIssueType.ARIA_MISSING, "Name, Role, Value"),
    }

    def __init__(self, target_level: WCAGLevel = WCAGLevel.AA) -> None:
        """Initialize accessibility analyzer.

        Args:
            target_level: Target WCAG conformance level.
        """
        self.target_level = target_level
        self.issues: List[AccessibilityIssue] = []
        self.rules: Dict[str, bool] = {rule: True for rule in self.WCAG_CRITERIA}
        logging.debug(f"AccessibilityAnalyzer initialized with level {target_level.value}")

    def analyze_file(self, file_path: str) -> AccessibilityReport:
        """Analyze a file for accessibility issues.

        Args:
            file_path: Path to file to analyze.

        Returns:
            Comprehensive accessibility report.
        """
        self.issues.clear()
        path = Path(file_path)

        if not path.exists():
            return AccessibilityReport(file_path=file_path)

        content = path.read_text(encoding="utf-8")

        # Analyze based on file type
        if path.suffix in (".html", ".htm"):
            self._analyze_html(content)
        elif path.suffix == ".py":
            self._analyze_python_ui(content)
        elif path.suffix in (".js", ".jsx", ".ts", ".tsx"):
            self._analyze_javascript_ui(content)

        return self._generate_report(file_path)

    def analyze_content(self, content: str, file_type: str = "html") -> AccessibilityReport:
        """Analyze content string for accessibility issues.

        Args:
            content: Content to analyze.
            file_type: Type of content (html, python, javascript).

        Returns:
            Accessibility report.
        """
        self.issues.clear()

        if file_type == "html":
            self._analyze_html(content)
        elif file_type == "python":
            self._analyze_python_ui(content)
        elif file_type in ("javascript", "react"):
            self._analyze_javascript_ui(content)

        return self._generate_report("content")

    def _analyze_html(self, content: str) -> None:
        """Analyze HTML content for accessibility issues.

        Args:
            content: HTML content string.
        """
        # Check for images without alt text
        img_pattern = r'<img\s+[^>]*?(?<!alt=)[^>]*?>'
        for match in re.finditer(img_pattern, content, re.IGNORECASE):
            if 'alt=' not in match.group().lower():
                line_num = content[:match.start()].count('\n') + 1
                self.issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.MISSING_ALT_TEXT,
                        severity=AccessibilitySeverity.CRITICAL,
                        wcag_level=WCAGLevel.A,
                        wcag_criterion="1.1.1",
                        description="Image missing alt attribute",
                        element=match.group()[:50],
                        line_number=line_num,
                        suggested_fix=(
                            'Add alt="" for decorative or alt="description" '
                            'for meaningful images'
                        ),
                        auto_fixable=False))

        # Check for form inputs without labels
        input_pattern = r'<input\s+[^>]*?>'
        for match in re.finditer(input_pattern, content, re.IGNORECASE):
            input_tag = match.group()
            if 'type="hidden"' not in input_tag.lower():
                # Check if there's a label for this input
                input_id_match = re.search(r'id=["\']([^"\']+)["\']', input_tag)
                if input_id_match:
                    input_id = input_id_match.group(1)
                    if f'for="{input_id}"' not in content and f"for='{input_id}'" not in content:
                        line_num = content[:match.start()].count('\n') + 1
                        self.issues.append(AccessibilityIssue(
                            issue_type=AccessibilityIssueType.MISSING_LABEL,
                            severity=AccessibilitySeverity.SERIOUS,
                            wcag_level=WCAGLevel.A,
                            wcag_criterion="3.3.2",
                            description="Form input missing associated label",
                            element=input_tag[:50],
                            line_number=line_num,
                            suggested_fix=f'Add <label for="{input_id}">Label text</label>',
                            auto_fixable=False
                        ))

        # Check for missing ARIA landmarks
        landmarks = ['main', 'nav', 'header', 'footer', 'aside']
        has_landmark = any(f'<{tag}' in content.lower() or f'role="{tag}"' in content.lower()
                           for tag in landmarks)
        if not has_landmark and '<body' in content.lower():
            self.issues.append(
                AccessibilityIssue(
                    issue_type=AccessibilityIssueType.ARIA_MISSING,
                    severity=AccessibilitySeverity.MODERATE,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="4.1.2",
                    description="Page missing landmark regions",
                    element="document",
                    suggested_fix=(
                        "Add semantic HTML5 elements (main, nav, header, "
                        "footer) or ARIA landmarks"
                    ),
                    auto_fixable=False))

        # Check heading hierarchy
        heading_levels = []
        for match in re.finditer(r'<h([1-6])', content, re.IGNORECASE):
            heading_levels.append(int(match.group(1)))

        if heading_levels:
            if heading_levels[0] != 1:
                self.issues.append(AccessibilityIssue(
                    issue_type=AccessibilityIssueType.HEADING_HIERARCHY,
                    severity=AccessibilitySeverity.MODERATE,
                    wcag_level=WCAGLevel.AA,
                    wcag_criterion="2.4.6",
                    description="Page should start with an h1 heading",
                    element="headings",
                    suggested_fix="Start page with <h1> element",
                    auto_fixable=False
                ))

            # Check for skipped levels
            for i in range(1, len(heading_levels)):
                if heading_levels[i] > heading_levels[i - 1] + 1:
                    self.issues.append(AccessibilityIssue(
                        issue_type=AccessibilityIssueType.HEADING_HIERARCHY,
                        severity=AccessibilitySeverity.MODERATE,
                        wcag_level=WCAGLevel.AA,
                        wcag_criterion="2.4.6",
                        description=(
                            f"Heading level skipped: "
                            f"h{heading_levels[i - 1]} to h{heading_levels[i]}"
                        ),
                        element=f"h{heading_levels[i]}",
                        suggested_fix="Use sequential heading levels without skipping",
                        auto_fixable=False
                    ))

    def _analyze_python_ui(self, content: str) -> None:
        """Analyze Python UI code (tkinter, PyQt, etc.) for accessibility issues.

        Args:
            content: Python source code.
        """
        # Check for tkinter widgets without accessibility properties
        widget_patterns = [
            (r'Button\s*\([^)]*\)', "Button"),
            (r'Label\s*\([^)]*\)', "Label"),
            (r'Entry\s*\([^)]*\)', "Entry"),
            (r'Canvas\s*\([^)]*\)', "Canvas"),
        ]

        for pattern, widget_name in widget_patterns:
            for match in re.finditer(pattern, content):
                widget_call = match.group()
                line_num = content[:match.start()].count('\n') + 1

                # Check for keyboard bindings
                if 'bind' not in content[match.end():match.end() + 200]:
                    # Check if there's a bind call near this widget
                    pass  # More complex analysis would be needed

                # Check for tooltips / accessibility text
                if 'tooltip' not in widget_call.lower() and 'help' not in widget_call.lower():
                    self.issues.append(AccessibilityIssue(
                        issue_type=AccessibilityIssueType.ARIA_MISSING,
                        severity=AccessibilitySeverity.MINOR,
                        wcag_level=WCAGLevel.AA,
                        wcag_criterion="4.1.2",
                        description=f"{widget_name} widget may benefit from tooltip or help text",
                        element=widget_call[:50],
                        line_number=line_num,
                        suggested_fix="Consider adding tooltip or accessibility description",
                        auto_fixable=False
                    ))

    def _analyze_javascript_ui(self, content: str) -> None:
        """Analyze JavaScript / React UI code for accessibility issues.

        Args:
            content: JavaScript / React source code.
        """
        # Check for click handlers without keyboard support
        click_pattern = r'onClick\s*=\s*\{[^}]+\}'
        for match in re.finditer(click_pattern, content):
            line_num = content[:match.start()].count('\n') + 1
            # Check if there's also onKeyPress / onKeyDown nearby
            context = content[max(0, match.start() - 100):match.end() + 100]
            if 'onKeyPress' not in context and 'onKeyDown' not in context:
                self.issues.append(AccessibilityIssue(
                    issue_type=AccessibilityIssueType.KEYBOARD_NAVIGATION,
                    severity=AccessibilitySeverity.SERIOUS,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="2.1.1",
                    description="Click handler without keyboard equivalent",
                    element=match.group()[:50],
                    line_number=line_num,
                    suggested_fix="Add onKeyPress or onKeyDown handler for keyboard users",
                    auto_fixable=False
                ))

        # Check for div / span used as interactive elements
        interactive_div = r'<div\s+onClick'
        for match in re.finditer(interactive_div, content, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1
            context = match.group()
            if 'role=' not in context and 'tabIndex' not in context:
                self.issues.append(AccessibilityIssue(
                    issue_type=AccessibilityIssueType.SEMANTIC_HTML,
                    severity=AccessibilitySeverity.SERIOUS,
                    wcag_level=WCAGLevel.A,
                    wcag_criterion="1.3.1",
                    description="Interactive div should be a button or have role / tabIndex",
                    element=context[:50],
                    line_number=line_num,
                    suggested_fix='Use <button> or add role="button" tabIndex="0"',
                    auto_fixable=False
                ))

    def check_color_contrast(
        self,
        foreground: str,
        background: str,
        is_large_text: bool = False
    ) -> ColorContrastResult:
        """Check color contrast ratio.

        Args:
            foreground: Foreground color (hex).
            background: Background color (hex).
            is_large_text: Whether text is large (14pt bold or 18pt+).

        Returns:
            Color contrast analysis result.
        """
        fg_luminance = self._relative_luminance(foreground)
        bg_luminance = self._relative_luminance(background)

        lighter = max(fg_luminance, bg_luminance)
        darker = min(fg_luminance, bg_luminance)
        contrast_ratio = (lighter + 0.05) / (darker + 0.05)

        # WCAG AA: 4.5:1 for normal text, 3:1 for large text
        # WCAG AAA: 7:1 for normal text, 4.5:1 for large text
        min_aa = 3.0 if is_large_text else 4.5
        min_aaa = 4.5 if is_large_text else 7.0

        return ColorContrastResult(
            foreground=foreground,
            background=background,
            contrast_ratio=round(contrast_ratio, 2),
            passes_aa=contrast_ratio >= min_aa,
            passes_aaa=contrast_ratio >= min_aaa,
            min_ratio_aa=min_aa,
            min_ratio_aaa=min_aaa
        )

    def _relative_luminance(self, hex_color: str) -> float:
        """Calculate relative luminance of a color.

        Args:
            hex_color: Hex color string (e.g., "#FFFFFF").

        Returns:
            Relative luminance value.
        """
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3:
            hex_color = ''.join([c * 2 for c in hex_color])

        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255

        def adjust(c: float) -> float:
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)

    def _generate_report(self, file_path: str) -> AccessibilityReport:
        """Generate accessibility report.

        Args:
            file_path: Path to analyzed file.

        Returns:
            Comprehensive accessibility report.
        """
        critical_count = sum(1 for i in self.issues if i.severity == AccessibilitySeverity.CRITICAL)
        serious_count = sum(1 for i in self.issues if i.severity == AccessibilitySeverity.SERIOUS)

        # Calculate compliance score (100 - weighted issues)
        score = 100.0
        for issue in self.issues:
            if issue.severity == AccessibilitySeverity.CRITICAL:
                score -= 15
            elif issue.severity == AccessibilitySeverity.SERIOUS:
                score -= 10
            elif issue.severity == AccessibilitySeverity.MODERATE:
                score -= 5
            else:
                score -= 2
        score = max(0, score)

        # Generate recommendations
        recommendations = []
        if critical_count > 0:
            recommendations.append("Address critical accessibility issues immediately")
        if serious_count > 0:
            recommendations.append("Fix serious issues to improve basic accessibility")
        if not self.issues:
            recommendations.append("Continue to test with screen readers and keyboard navigation")

        return AccessibilityReport(
            file_path=file_path,
            issues=list(self.issues),
            total_elements=len(self.issues),
            wcag_level=self.target_level,
            compliance_score=round(score, 1),
            critical_count=critical_count,
            serious_count=serious_count,
            recommendations=recommendations
        )

    def get_issues_by_severity(
        self,
        severity: AccessibilitySeverity
    ) -> List[AccessibilityIssue]:
        """Get issues filtered by severity.

        Args:
            severity: Severity level to filter by.

        Returns:
            List of issues with specified severity.
        """
        return [i for i in self.issues if i.severity == severity]

    def get_issues_by_wcag_level(
        self,
        level: WCAGLevel
    ) -> List[AccessibilityIssue]:
        """Get issues filtered by WCAG level.

        Args:
            level: WCAG level to filter by.

        Returns:
            List of issues affecting specified level.
        """
        return [i for i in self.issues if i.wcag_level == level]

    def enable_rule(self, wcag_criterion: str) -> None:
        """Enable a specific WCAG rule.

        Args:
            wcag_criterion: WCAG criterion identifier.
        """
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = True

    def disable_rule(self, wcag_criterion: str) -> None:
        """Disable a specific WCAG rule.

        Args:
            wcag_criterion: WCAG criterion identifier.
        """
        if wcag_criterion in self.rules:
            self.rules[wcag_criterion] = False


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
        self._style_rules: List[StyleRule] = list(DEFAULT_PYTHON_STYLE_RULES)
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

    @property
    def language(self) -> CodeLanguage:
        """Get the detected language."""
        return self._language

    def detect_language(self) -> CodeLanguage:
        """Detect the programming language from file extension."""
        return self._detect_language()

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
        violations = []
        lines = content.split('\n')
        for rule in self._style_rules:
            if not rule.enabled:
                continue
            if rule.language and rule.language != self._language:
                continue
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
                has_lineno = hasattr(node, 'end_lineno') and hasattr(node, 'lineno')
                lineno_not_none = node.end_lineno is not None and node.lineno is not None
                if has_lineno and lineno_not_none:
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
        # Test coverage placeholder (would need integration with coverage tools)
        score.test_coverage = 0  # Unknown without coverage data
        # Overall score (weighted average)
        score.score = (
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
                has_lineno = hasattr(node, 'end_lineno') and hasattr(node, 'lineno')
                lineno_not_none = node.end_lineno is not None and node.lineno is not None
                if has_lineno and lineno_not_none:
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
                            description=(
                                f"Class '{node.name}' has {method_count} "
                                f"methods (>{threshold})"
                            ),
                            severity="warning",
                            line_number=node.lineno,
                            suggestion="Consider splitting into smaller, focused classes",
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
        self._code_smells = smells
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
                        lines[line_numbers[0] - 1:
                              line_numbers[0] - 1 + min_lines]
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


# Create main function using the helper
main = create_main_function(
    CoderAgent,
    'Coder Agent: Updates code files',
    'Path to the code file'
)


if __name__ == '__main__':
    main()
