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



# ErrorsAgent - Manage and analyze file-level error reports

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # # [Brief Summary]
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
# USAGE:
# Instantiate ErrorsAgent with the path to an .errors.md file and use its methods to add errors, match patterns, cluster similar errors, and apply suppression rules.

# WHAT IT DOES:
# Provides an agent for maintaining error-report files: parsing and validating error file paths, adding error entries, matching against default and custom patterns, clustering similar errors, tracking annotations and statistics, and optionally using Rust-accelerated pattern matching and suppression checks.

# WHAT IT SHOULD DO BETTER:
# Expose clearer public APIs for clustering and suppression decision reasons, add comprehensive unit tests for Rust vs Python code paths, and improve associated-file discovery robustness and configurability.

# FILE CONTENT SUMMARY:
Auto-extracted class from agent_errors.py


from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

from .error_category import ErrorCategory
from .error_cluster import ErrorCluster
from .error_entry import ErrorEntry
from .error_pattern import ErrorPattern
from .error_severity import ErrorSeverity
from .suppression_rule import SuppressionRule

# Rust acceleration imports
try:
    from rust_core import check_suppression_rust, match_patterns_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

# Default error patterns

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # DEFAULT_ERROR_PATTERNS: list[ErrorPattern] = [
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="undefined_variable",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rNameError: name '(\w+)' is not defined","  # [BATCHFIX] closed string
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
#         suggested_fix="Define the variable before use or check for typos",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="syntax_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rSyntaxError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.CRITICAL,
        category=ErrorCategory.SYNTAX,
#         suggested_fix="Fix the syntax according to the error message",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="type_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rTypeError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.TYPE,
#         suggested_fix="Check type compatibility of operands",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="import_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rImportError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
#         suggested_fix="Ensure the module is installed and accessible",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="attribute_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rAttributeError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.RUNTIME,
#         suggested_fix="Check if the attribute exists on the object",
    ),
]

__version__ = VERSION


class ErrorsAgent(BaseAgent):
    Updates code file error reports using AI assistance.

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_error_file_path()
        self._check_associated_file()
        # New features
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._errors: list[ErrorEntry] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._clusters: dict[str, ErrorCluster] = {}
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._patterns: list[ErrorPattern] = list(DEFAULT_ERROR_PATTERNS)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._suppression_rules: list[SuppressionRule] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._annotations: dict[str, list[str]] = {}  # error_id -> annotations
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._statistics: dict[str, Any] = {}

    def _validate_error_file_path(self) -> None:
        Validate that the file has the correct extension.
#         if not self.file_path.name.endswith(".errors.md"):
# [BATCHFIX] Commented metadata/non-Python
# #             logging.warning(fFile {self.file_path.name} does not end with .errors.md")"  # [BATCHFIX] closed string

    def _check_associated_file(self) -> None:
        Check if the associated code file exists.
        name = self.file_path.name
#         if name.endswith(".errors.md"):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             base_name = name[:-10]  # len('.errors.md')
            # Try to find the file with common extensions or exact match
            candidate = self.file_path.parent / base_name
            if candidate.exists():
                return
            # Try adding extensions
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #             for ext in [".py", ".sh", ".js", ".ts", ".md"]:
                candidate = self.file_path.parent / (base_name + ext)
                if candidate.exists() and candidate != self.file_path:
                    return
# [BATCHFIX] Commented metadata/non-Python
# #             logging.warning(fCould not find associated code file for {self.file_path.name}")"  # [BATCHFIX] closed string

    # ========== Error Management ==========
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     def add_error(
        self,
        message: str,
        file_path: str,
        line_number: int,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.OTHER,
# [BATCHFIX] Commented metadata/non-Python
# #         stack_trace: str = ","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         suggested_fix: str = ","  # [BATCHFIX] closed string
    ) -> ErrorEntry:
        Add a new error entry.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #         error_id = hashlib.md5(f"{message}:{file_path}:{line_number}".encode()).hexdigest()[:8]
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         error = ErrorEntry(
            id=error_id,
            message=message,
            file_path=file_path,
            line_number=line_number,
            severity


from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

from .error_category import ErrorCategory
from .error_cluster import ErrorCluster
from .error_entry import ErrorEntry
from .error_pattern import ErrorPattern
from .error_severity import ErrorSeverity
from .suppression_rule import SuppressionRule

# Rust acceleration imports
try:
    from rust_core import check_suppression_rust, match_patterns_rust

    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

# Default error patterns

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # DEFAULT_ERROR_PATTERNS: list[ErrorPattern] = [
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="undefined_variable",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rNameError: name '(\w+)' is not defined","  # [BATCHFIX] closed string
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
#         suggested_fix="Define the variable before use or check for typos",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="syntax_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rSyntaxError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.CRITICAL,
        category=ErrorCategory.SYNTAX,
#         suggested_fix="Fix the syntax according to the error message",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="type_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rTypeError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.TYPE,
#         suggested_fix="Check type compatibility of operands",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="import_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rImportError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
#         suggested_fix="Ensure the module is installed and accessible",
    ),
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     ErrorPattern(
#         name="attribute_error",
# [BATCHFIX] Commented metadata/non-Python
# #         regex=rAttributeError: (.*)","  # [BATCHFIX] closed string
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.RUNTIME,
#         suggested_fix="Check if the attribute exists on the object",
    ),
]

__version__ = VERSION


class ErrorsAgent(BaseAgent):
    Updates code file error reports using AI assistance.

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_error_file_path()
        self._check_associated_file()
        # New features
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._errors: list[ErrorEntry] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._clusters: dict[str, ErrorCluster] = {}
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._patterns: list[ErrorPattern] = list(DEFAULT_ERROR_PATTERNS)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._suppression_rules: list[SuppressionRule] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._annotations: dict[str, list[str]] = {}  # error_id -> annotations
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         self._statistics: dict[str, Any] = {}

    def _validate_error_file_path(self) -> None:
        Validate that the file has the correct extension.
#         if not self.file_path.name.endswith(".errors.md"):
# [BATCHFIX] Commented metadata/non-Python
# #             logging.warning(fFile {self.file_path.name} does not end with .errors.md")"  # [BATCHFIX] closed string

    def _check_associated_file(self) -> None:
        Check if the associated code file exists.
        name = self.file_path.name
#         if name.endswith(".errors.md"):
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             base_name = name[:-10]  # len('.errors.md')
            # Try to find the file with common extensions or exact match
            candidate = self.file_path.parent / base_name
            if candidate.exists():
                return
            # Try adding extensions
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #             for ext in [".py", ".sh", ".js", ".ts", ".md"]:
                candidate = self.file_path.parent / (base_name + ext)
                if candidate.exists() and candidate != self.file_path:
                    return
# [BATCHFIX] Commented metadata/non-Python
# #             logging.warning(fCould not find associated code file for {self.file_path.name}")"  # [BATCHFIX] closed string

    # ========== Error Management ==========
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     def add_error(
        self,
        message: str,
        file_path: str,
        line_number: int,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.OTHER,
# [BATCHFIX] Commented metadata/non-Python
# #         stack_trace: str = ","  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #         suggested_fix: str = ","  # [BATCHFIX] closed string
    ) -> ErrorEntry:
        Add a new error entry.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #         error_id = hashlib.md5(f"{message}:{file_path}:{line_number}".encode()).hexdigest()[:8]
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         error = ErrorEntry(
            id=error_id,
            message=message,
            file_path=file_path,
            line_number=line_number,
            severity=severity,
            category=category,
            timestamp=datetime.now().isoformat(),
            stack_trace=stack_trace,
            suggested_fix=suggested_fix,
        )
        # Check if suppressed
        if not self._is_suppressed(error):
            self._errors.append(error)
            self._auto_categorize_error(error)
        return error

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_errors(self) -> list[ErrorEntry]:
        Get all errors.
        return self._errors

    def get_error_by_id(self, error_id: str) -> ErrorEntry | None:
        Get an error by ID.
        return next((e for e in self._errors if e.id == error_id), None)

# [BATCHFIX] Commented metadata/non-Python
# #     def resolve_error(self, error_id: str, resolution_note: str = ") -> bool:"  # [BATCHFIX] closed string
        Mark an error as resolved.
        error = self.get_error_by_id(error_id)
        if error:
            error.resolved = True
            error.resolution_timestamp = datetime.now().isoformat()
            if resolution_note:
# [BATCHFIX] Commented metadata/non-Python
# #                 self.add_annotation(error_id, fResolution: {resolution_note}")"  # [BATCHFIX] closed string
            return True
        return False

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_unresolved_errors(self) -> list[ErrorEntry]:
        Get all unresolved errors.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         return [e for e in self._errors if not e.resolved]

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_errors_by_severity(self, severity: ErrorSeverity) -> list[ErrorEntry]:
        Get errors filtered by severity.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         return [e for e in self._errors if e.severity == severity]

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_errors_by_category(self, category: ErrorCategory) -> list[ErrorEntry]:
        Get errors filtered by category.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         return [e for e in self._errors if e.category == category]

    # ========== Severity Scoring ==========
    def calculate_severity_score(self, error: ErrorEntry) -> float:
        Calculate a severity score for an error.
        base_score = error.severity.value * 20
        # Adjust based on factors
        if error.category == ErrorCategory.SECURITY:
            base_score += 15
        # Note: CRITICAL category not defined in ErrorCategory enum
        if error.stack_trace:
            base_score += 5  # More context available
        if error.resolved:
            base_score -= 50  # Already resolved
        return max(0, min(100, base_score))

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def prioritize_errors(self) -> list[ErrorEntry]:
        Return errors sorted by priority (highest first).
        return sorted(self._errors, key=lambda e: self.calculate_severity_score(e), reverse=True)

    # ========== Error Clustering ==========
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def cluster_similar_errors(self) -> dict[str, ErrorCluster]:
        Cluster similar errors together.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         clusters: dict[str, list[ErrorEntry]] = {}
        for error in self._errors:
            # Create cluster key from error pattern
            cluster_key = self._get_cluster_key(error)
            if cluster_key not in clusters:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 clusters[cluster_key] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             clusters[cluster_key].append(error)
        # Convert to ErrorCluster objects
        self._clusters = {}
        for key, errors in clusters.items():
            if len(errors) > 1:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 cluster_id = hashlib.md5(key.encode()).hexdigest()[:8]
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 self._clusters[cluster_id] = ErrorCluster(
                    id=cluster_id,
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     name=key[:50],
                    pattern=key,
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     error_ids=[e.id for e in errors],
# [BATCHFIX] Commented metadata/non-Python
# #                     description=fCluster of {len(errors)} similar errors","  # [BATCHFIX] closed string
                )
        return self._clusters

    def _get_cluster_key(self, error: ErrorEntry) -> str:
        Generate a clustering key for an error.
        # Normalize the message by removing variable parts
#         normalized = re.sub(r"'[^']*'", "'<var>'", error.message)"  # [BATCHFIX] closed string"  # [BATCHFIX] closed string
#         normalized = re.sub(r"\\\\d+", "<num>", normalized)
# [BATCHFIX] Commented metadata/non-Python
# # #         return f"{error.category.value}:{normalized}"  # [BATCHFIX] closed string

    def get_cluster(self, cluster_id: str) -> ErrorCluster | None:
        Get a cluster by ID.
        return self._clusters.get(cluster_id)

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_errors_in_cluster(self, cluster_id: str) -> list[ErrorEntry]:
        Get all errors in a cluster.
        cluster = self._clusters.get(cluster_id)
        if not cluster:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             return []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         return [e for e in self._errors if e.id in cluster.error_ids]

    # ========== Pattern Recognition ==========
    def add_pattern(self, pattern: ErrorPattern) -> None:
        Add a custom error pattern.
        self._patterns.append(pattern)

    def recognize_pattern(self, error: ErrorEntry) -> ErrorPattern | None:
        Recognize if an error matches a known pattern.
        # Rust-accelerated pattern matching
        if _RUST_AVAILABLE and self._patterns:
            try:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 patterns = [p.regex for p in self._patterns]
                idx = match_patterns_rust(error.message, patterns)
                if idx >= 0:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     self._patterns[idx].occurrences += 1
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                     return self._patterns[idx]
                return None
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                pass  # Fall back to Python

        # Python fallback
        for pattern in self._patterns:
            if re.search(pattern.regex, error.message):
                pattern.occurrences += 1
                return pattern
        return None

    def _auto_categorize_error(self, error: ErrorEntry) -> None:
        Auto-categorize an error based on patterns.
        pattern = self.recognize_pattern(error)
        if pattern:
            if error.category == ErrorCategory.OTHER:
                error.category = pattern.category
            if error.severity == ErrorSeverity.MEDIUM:
                # Update if default
                error.severity = pattern.severity
            if not error.suggested_fix:
                error.suggested_fix = pattern.suggested_fix

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_pattern_statistics(self) -> dict[str, int]:
        Get statistics on pattern occurrences.
        return {p.name: p.occurrences for p in self._patterns}

    # ========== Suppression Rules ==========
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#     def add_suppression_rule(
        self,
        pattern: str,
        reason: str,
        expires: str | None = None,
# [BATCHFIX] Commented metadata/non-Python
# #         created_by: str = ","  # [BATCHFIX] closed string
    ) -> SuppressionRule:
        Add a suppression rule.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         rule = SuppressionRule(
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             id=hashlib.md5(pattern.encode()).hexdigest()[:8],
            pattern=pattern,
            reason=reason,
            expires=expires,
            created_by=created_by,
            created_at=datetime.now().isoformat(),
        )
        self._suppression_rules.append(rule)
        return rule

    def remove_suppression_rule(self, rule_id: str) -> bool:
        Remove a suppression rule.
        for i, rule in enumerate(self._suppression_rules):
            if rule.id == rule_id:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 del self._suppression_rules[i]
                return True
        return False

    def _is_suppressed(self, error: ErrorEntry) -> bool:
        Check if an error is suppressed.
        # Filter out expired rules first
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         active_rules = []
        for rule in self._suppression_rules:
            if rule.expires:
                try:
                    expires_dt = datetime.fromisoformat(rule.expires)
                    if datetime.now() > expires_dt:
                        continue
                except ValueError:
                    pass
            active_rules.append(rule)

        if not active_rules:
            return False

        # Rust-accelerated suppression check
        if _RUST_AVAILABLE:
            try:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #                 patterns = [r.pattern for r in active_rules]
                is_match, _ = check_suppression_rust(error.message, patterns)
                return is_match
            except Exception:  # pylint: disable=broad-exception-caught, unused-variable
                pass  # Fall back to Python

        # Python fallback
        for rule in active_rules:
            if re.search(rule.pattern, error.message):
                return True
        return False

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_suppression_rules(self) -> list[SuppressionRule]:
        Get all suppression rules.
        return self._suppression_rules

    # ========== Annotations ==========

    def add_annotation(self, error_id: str, annotation: str) -> bool:
        Add an annotation to an error.
        if error_id not in self._annotations:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             self._annotations[error_id] = []
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #         self._annotations[error_id].append(f"[{datetime.now().isoformat()}] {annotation}")
        return True

# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def get_annotations(self, error_id: str) -> list[str]:
        Get annotations for an error.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         return self._annotations.get(error_id, [])

    # ========== Deduplication ==========
    def deduplicate_errors(self) -> int:
        Remove duplicate errors, returns count removed.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         seen: set[str] = set()
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         unique: list[ErrorEntry] = []
        removed = 0
        for error in self._errors:
# [BATCHFIX] Commented metadata/non-Python
# # #             key = f"{error.message}:{error.file_path}:{error.line_number}"  # [BATCHFIX] closed string
            if key not in seen:
                seen.add(key)
                unique.append(error)
            else:
                removed += 1
        self._errors = unique
        return removed

    # ========== Statistics ==========
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #     def calculate_statistics(self) -> dict[str, Any]:
        Calculate error statistics.
        total = len(self._errors)
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         resolved = len([e for e in self._errors if e.resolved])
        by_severity = {}
        for severity in ErrorSeverity:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             count = len([e for e in self._errors if e.severity == severity])
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             by_severity[severity.name] = count
        by_category = {}
        for category in ErrorCategory:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             count = len([e for e in self._errors if e.category == category])
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             by_category[category.name] = count
        self._statistics = {
#             "total_errors": total,
#             "resolved_errors": resolved,
#             "unresolved_errors": total - resolved,
#             "resolution_rate": (resolved / total * 100) if total > 0 else 0,
#             "by_severity": by_severity,
#             "by_category": by_category,
#             "cluster_count": len(self._clusters),
#             "suppression_rules_count": len(self._suppression_rules),
        }
        return self._statistics

    # ========== Documentation Generation ==========
    def generate_documentation(self) -> str:
        Generate documentation for all errors.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #         docs = ["# Error Documentation\n"]
        stats = self.calculate_statistics()
        docs.append("## Summary\n")
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #         docs.append(f"- Total Errors: {stats['total_errors']}")
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #         docs.append(f"- Resolved: {stats['resolved_errors']}")
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #         docs.append(f"- Unresolved: {stats['unresolved_errors']}")
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #         docs.append(f"- Resolution Rate: {stats['resolution_rate']:.1f}%\n")
        # Group by category
        docs.append("## Errors by Category\n")
        for category in ErrorCategory:
            errors = self.get_errors_by_category(category)
            if errors:
                docs.append(f"### {category.value.title()}\n")
                for error in errors:
# [BATCHFIX] Commented metadata/non-Python
# # #                     status = "✓" if error.resolved else "✗"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #                     docs.append(f"- [{status}] {error.message} (line {error.line_number})")
# [BATCHFIX] Commented metadata/non-Python
# #                 docs.append(")"  # [BATCHFIX] closed string
#         return "\n".join(docs)

#     def export_errors(self, output_format: str = "json") -> str:
        Export errors to various formats.
#         if output_format == "json":
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# #             data: list[dict[str, Any]] = [
                {
#                     "id": e.id,
#                     "message": e.message,
#                     "file": e.file_path,
#                     "line": e.line_number,
#                     "severity": e.severity.name,
#                     "category": e.category.name,
#                     "resolved": e.resolved,
                }
                for e in self._errors
            ]
            return json.dumps(data, indent=2)
#         elif output_format == "csv":
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented metadata/non-Python
# [BATCHFIX] Commented metadata/non-Python
# # #             lines = ["id,message,file,line,severity,category,resolved"]
            for e in self._errors:
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#                 lines.append(
# [BATCHFIX] Commented metadata/non-Python
# # #                     f"{e.id},{e.message},{e.file_path},{e.line_number},"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #                     f"{e.severity.name},{e.category.name},{e.resolved}"  # [BATCHFIX] closed string
                )
#             return "\n".join(lines)
# #         return

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        Return structured error report template.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         return (
# [BATCHFIX] Commented metadata/non-Python
# #             "# Error Report\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "## Summary\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "No errors detected.\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "## Details\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "- **File**: (not specified)\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "- **Last Analyzed**: (not specified)\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "- **Status**: ✓ Clean\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "## Static Analysis\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "No issues found.\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "## Linting Results\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "No violations detected.\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "## Type Checking\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "No type errors.\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "## Security Scan\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# # #             "No vulnerabilities identified.\n"  # [BATCHFIX] closed string
        )

    def _get_fallback_response(self) -> str:
        Return fallback response when Copilot is unavailable.
# [BATCHFIX] Commented metadata/non-Python
# # [BATCHFIX] Commented unmatched parenthesis
#         return (
# [BATCHFIX] Commented metadata/non-Python
# #             "# AI Improvement Unavailable\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "# GitHub CLI not found. Install from https://cli.github.com/\n\n"  # [BATCHFIX] closed string
# [BATCHFIX] Commented metadata/non-Python
# #             "# Original error report preserved below:\n\n"  # [BATCHFIX] closed string
        )

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        Use AI to improve the error report.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids duplicated wrapper sections).
        
        actual_path = Path(target_file) if target_file else self.file_path
# [BATCHFIX] Commented metadata/non-Python
# #         logging.info(fImproving error report for {actual_path}")"  # [BATCHFIX] closed string
        return await super().improve_content(prompt, target_file=target_file)
