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

"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from .ErrorCategory import ErrorCategory
from .ErrorCluster import ErrorCluster
from .ErrorEntry import ErrorEntry
from .ErrorPattern import ErrorPattern
from .ErrorSeverity import ErrorSeverity
from .SuppressionRule import SuppressionRule
from src.core.base.BaseAgent import BaseAgent
from datetime import datetime
from typing import Any
import hashlib
import json
import logging
import re

# Rust acceleration imports
try:
    from rust_core import match_patterns_rust, check_suppression_rust
    _RUST_AVAILABLE = True
except ImportError:
    _RUST_AVAILABLE = False

# Default error patterns

DEFAULT_ERROR_PATTERNS: list[ErrorPattern] = [
    ErrorPattern(
        name="undefined_variable",
        regex=r"NameError: name '(\w+)' is not defined",
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
        suggested_fix="Define the variable before use or check for typos",
    ),
    ErrorPattern(
        name="syntax_error",
        regex=r"SyntaxError: (.*)",
        severity=ErrorSeverity.CRITICAL,
        category=ErrorCategory.SYNTAX,
        suggested_fix="Fix the syntax according to the error message",
    ),
    ErrorPattern(
        name="type_error",
        regex=r"TypeError: (.*)",
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.TYPE,
        suggested_fix="Check type compatibility of operands",
    ),
    ErrorPattern(
        name="import_error",
        regex=r"ImportError: (.*)",
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
        suggested_fix="Ensure the module is installed and accessible",
    ),
    ErrorPattern(
        name="attribute_error",
        regex=r"AttributeError: (.*)",
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.RUNTIME,
        suggested_fix="Check if the attribute exists on the object",
    ),
]

__version__ = VERSION


class ErrorsAgent(BaseAgent):
    """Updates code file error reports using AI assistance."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_error_file_path()
        self._check_associated_file()
        # New features
        self._errors: list[ErrorEntry] = []
        self._clusters: dict[str, ErrorCluster] = {}
        self._patterns: list[ErrorPattern] = list(DEFAULT_ERROR_PATTERNS)
        self._suppression_rules: list[SuppressionRule] = []
        self._annotations: dict[str, list[str]] = {}  # error_id -> annotations
        self._statistics: dict[str, Any] = {}

    def _validate_error_file_path(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith(".errors.md"):
            logging.warning(f"File {self.file_path.name} does not end with .errors.md")

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists."""
        name = self.file_path.name
        if name.endswith(".errors.md"):
            base_name = name[:-10]  # len('.errors.md')
            # Try to find the file with common extensions or exact match
            candidate = self.file_path.parent / base_name
            if candidate.exists():
                return
            # Try adding extensions
            for ext in [".py", ".sh", ".js", ".ts", ".md"]:
                candidate = self.file_path.parent / (base_name + ext)
                if candidate.exists() and candidate != self.file_path:
                    return
            logging.warning(
                f"Could not find associated code file for {self.file_path.name}"
            )

    # ========== Error Management ==========
    def add_error(
        self,
        message: str,
        file_path: str,
        line_number: int,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.OTHER,
        stack_trace: str = "",
        suggested_fix: str = "",
    ) -> ErrorEntry:
        """Add a new error entry."""
        error_id = hashlib.md5(
            f"{message}:{file_path}:{line_number}".encode()
        ).hexdigest()[:8]
        error = ErrorEntry(
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

    def get_errors(self) -> list[ErrorEntry]:
        """Get all errors."""
        return self._errors

    def get_error_by_id(self, error_id: str) -> ErrorEntry | None:
        """Get an error by ID."""
        return next((e for e in self._errors if e.id == error_id), None)

    def resolve_error(self, error_id: str, resolution_note: str = "") -> bool:
        """Mark an error as resolved."""
        error = self.get_error_by_id(error_id)
        if error:
            error.resolved = True
            error.resolution_timestamp = datetime.now().isoformat()
            if resolution_note:
                self.add_annotation(error_id, f"Resolution: {resolution_note}")
            return True
        return False

    def get_unresolved_errors(self) -> list[ErrorEntry]:
        """Get all unresolved errors."""
        return [e for e in self._errors if not e.resolved]

    def get_errors_by_severity(self, severity: ErrorSeverity) -> list[ErrorEntry]:
        """Get errors filtered by severity."""
        return [e for e in self._errors if e.severity == severity]

    def get_errors_by_category(self, category: ErrorCategory) -> list[ErrorEntry]:
        """Get errors filtered by category."""
        return [e for e in self._errors if e.category == category]

    # ========== Severity Scoring ==========
    def calculate_severity_score(self, error: ErrorEntry) -> float:
        """Calculate a severity score for an error."""
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

    def prioritize_errors(self) -> list[ErrorEntry]:
        """Return errors sorted by priority (highest first)."""
        return sorted(
            self._errors, key=lambda e: self.calculate_severity_score(e), reverse=True
        )

    # ========== Error Clustering ==========
    def cluster_similar_errors(self) -> dict[str, ErrorCluster]:
        """Cluster similar errors together."""
        clusters: dict[str, list[ErrorEntry]] = {}
        for error in self._errors:
            # Create cluster key from error pattern
            cluster_key = self._get_cluster_key(error)
            if cluster_key not in clusters:
                clusters[cluster_key] = []
            clusters[cluster_key].append(error)
        # Convert to ErrorCluster objects
        self._clusters = {}
        for key, errors in clusters.items():
            if len(errors) > 1:
                cluster_id = hashlib.md5(key.encode()).hexdigest()[:8]
                self._clusters[cluster_id] = ErrorCluster(
                    id=cluster_id,
                    name=key[:50],
                    pattern=key,
                    error_ids=[e.id for e in errors],
                    description=f"Cluster of {len(errors)} similar errors",
                )
        return self._clusters

    def _get_cluster_key(self, error: ErrorEntry) -> str:
        """Generate a clustering key for an error."""
        # Normalize the message by removing variable parts
        normalized = re.sub(r"'[^']*'", "'<var>'", error.message)
        normalized = re.sub(r"\d+", "<num>", normalized)
        return f"{error.category.value}:{normalized}"

    def get_cluster(self, cluster_id: str) -> ErrorCluster | None:
        """Get a cluster by ID."""
        return self._clusters.get(cluster_id)

    def get_errors_in_cluster(self, cluster_id: str) -> list[ErrorEntry]:
        """Get all errors in a cluster."""
        cluster = self._clusters.get(cluster_id)
        if not cluster:
            return []
        return [e for e in self._errors if e.id in cluster.error_ids]

    # ========== Pattern Recognition ==========
    def add_pattern(self, pattern: ErrorPattern) -> None:
        """Add a custom error pattern."""
        self._patterns.append(pattern)

    def recognize_pattern(self, error: ErrorEntry) -> ErrorPattern | None:
        """Recognize if an error matches a known pattern."""
        # Rust-accelerated pattern matching
        if _RUST_AVAILABLE and self._patterns:
            try:
                patterns = [p.regex for p in self._patterns]
                idx = match_patterns_rust(error.message, patterns)
                if idx >= 0:
                    self._patterns[idx].occurrences += 1
                    return self._patterns[idx]
                return None
            except Exception:
                pass  # Fall back to Python
        
        # Python fallback
        for pattern in self._patterns:
            if re.search(pattern.regex, error.message):
                pattern.occurrences += 1
                return pattern
        return None

    def _auto_categorize_error(self, error: ErrorEntry) -> None:
        """Auto-categorize an error based on patterns."""
        pattern = self.recognize_pattern(error)
        if pattern:
            if error.category == ErrorCategory.OTHER:
                error.category = pattern.category
            if error.severity == ErrorSeverity.MEDIUM:
                # Update if default
                error.severity = pattern.severity
            if not error.suggested_fix:
                error.suggested_fix = pattern.suggested_fix

    def get_pattern_statistics(self) -> dict[str, int]:
        """Get statistics on pattern occurrences."""
        return {p.name: p.occurrences for p in self._patterns}

    # ========== Suppression Rules ==========
    def add_suppression_rule(
        self,
        pattern: str,
        reason: str,
        expires: str | None = None,
        created_by: str = "",
    ) -> SuppressionRule:
        """Add a suppression rule."""
        rule = SuppressionRule(
            id=hashlib.md5(pattern.encode()).hexdigest()[:8],
            pattern=pattern,
            reason=reason,
            expires=expires,
            created_by=created_by,
            created_at=datetime.now().isoformat(),
        )
        self._suppression_rules.append(rule)
        return rule

    def remove_suppression_rule(self, rule_id: str) -> bool:
        """Remove a suppression rule."""
        for i, rule in enumerate(self._suppression_rules):
            if rule.id == rule_id:
                del self._suppression_rules[i]
                return True
        return False

    def _is_suppressed(self, error: ErrorEntry) -> bool:
        """Check if an error is suppressed."""
        # Filter out expired rules first
        active_rules = []
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
                patterns = [r.pattern for r in active_rules]
                is_match, _ = check_suppression_rust(error.message, patterns)
                return is_match
            except Exception:
                pass  # Fall back to Python
        
        # Python fallback
        for rule in active_rules:
            if re.search(rule.pattern, error.message):
                return True
        return False

    def get_suppression_rules(self) -> list[SuppressionRule]:
        """Get all suppression rules."""
        return self._suppression_rules

    # ========== Annotations ==========

    def add_annotation(self, error_id: str, annotation: str) -> bool:
        """Add an annotation to an error."""
        if error_id not in self._annotations:
            self._annotations[error_id] = []
        self._annotations[error_id].append(
            f"[{datetime.now().isoformat()}] {annotation}"
        )
        return True

    def get_annotations(self, error_id: str) -> list[str]:
        """Get annotations for an error."""
        return self._annotations.get(error_id, [])

    # ========== Deduplication ==========
    def deduplicate_errors(self) -> int:
        """Remove duplicate errors, returns count removed."""
        seen: set[str] = set()
        unique: list[ErrorEntry] = []
        removed = 0
        for error in self._errors:
            key = f"{error.message}:{error.file_path}:{error.line_number}"
            if key not in seen:
                seen.add(key)
                unique.append(error)
            else:
                removed += 1
        self._errors = unique
        return removed

    # ========== Statistics ==========
    def calculate_statistics(self) -> dict[str, Any]:
        """Calculate error statistics."""
        total = len(self._errors)
        resolved = len([e for e in self._errors if e.resolved])
        by_severity = {}
        for severity in ErrorSeverity:
            count = len([e for e in self._errors if e.severity == severity])
            by_severity[severity.name] = count
        by_category = {}
        for category in ErrorCategory:
            count = len([e for e in self._errors if e.category == category])
            by_category[category.name] = count
        self._statistics = {
            "total_errors": total,
            "resolved_errors": resolved,
            "unresolved_errors": total - resolved,
            "resolution_rate": (resolved / total * 100) if total > 0 else 0,
            "by_severity": by_severity,
            "by_category": by_category,
            "cluster_count": len(self._clusters),
            "suppression_rules_count": len(self._suppression_rules),
        }
        return self._statistics

    # ========== Documentation Generation ==========
    def generate_documentation(self) -> str:
        """Generate documentation for all errors."""
        docs = ["# Error Documentation\n"]
        stats = self.calculate_statistics()
        docs.append("## Summary\n")
        docs.append(f"- Total Errors: {stats['total_errors']}")
        docs.append(f"- Resolved: {stats['resolved_errors']}")
        docs.append(f"- Unresolved: {stats['unresolved_errors']}")
        docs.append(f"- Resolution Rate: {stats['resolution_rate']:.1f}%\n")
        # Group by category
        docs.append("## Errors by Category\n")
        for category in ErrorCategory:
            errors = self.get_errors_by_category(category)
            if errors:
                docs.append(f"### {category.value.title()}\n")
                for error in errors:
                    status = "✓" if error.resolved else "✗"
                    docs.append(
                        f"- [{status}] {error.message} (line {error.line_number})"
                    )
                docs.append("")
        return "\n".join(docs)

    def export_errors(self, format: str = "json") -> str:
        """Export errors to various formats."""
        if format == "json":
            data: list[dict[str, Any]] = [
                {
                    "id": e.id,
                    "message": e.message,
                    "file": e.file_path,
                    "line": e.line_number,
                    "severity": e.severity.name,
                    "category": e.category.name,
                    "resolved": e.resolved,
                }
                for e in self._errors
            ]
            return json.dumps(data, indent=2)
        elif format == "csv":
            lines = ["id,message,file,line,severity,category,resolved"]
            for e in self._errors:
                lines.append(
                    f"{e.id},{e.message},{e.file_path},"
                    f"{e.line_number},{e.severity.name},"
                    f"{e.category.name},{e.resolved}"
                )
            return "\n".join(lines)
        return ""

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return structured error report template."""
        return (
            "# Error Report\n\n"
            "## Summary\n\n"
            "No errors detected.\n\n"
            "## Details\n\n"
            "- **File**: (not specified)\n"
            "- **Last Analyzed**: (not specified)\n"
            "- **Status**: ✓ Clean\n\n"
            "## Static Analysis\n\n"
            "No issues found.\n\n"
            "## Linting Results\n\n"
            "No violations detected.\n\n"
            "## Type Checking\n\n"
            "No type errors.\n\n"
            "## Security Scan\n\n"
            "No vulnerabilities identified.\n"
        )

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return (
            "# AI Improvement Unavailable\n"
            "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
            "# Original error report preserved below:\n\n"
        )

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the error report.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids duplicated wrapper sections).
        """
        logging.info(f"Improving error report for {self.file_path}")
        return super().improve_content(prompt)
