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
Errors Agent: Improves and updates code file error reports.

Reads an errors file (Codefile.errors.md), uses Copilot to enhance the error analysis,
and updates the errors file with improvements.

# Description
This module provides an Errors Agent that reads existing code file error reports,
uses AI assistance to improve and complete them, and updates the errors files
with enhanced documentation.

# Changelog
- 1.0.0: Initial implementation
- 1.1.0: Added error correlation, clustering, severity scoring, pattern recognition
- 1.2.0: Added notification integrations, impact analysis, timeline visualization,
         regression detection, automated fix suggestions, external reporting,
         budget tracking, trend analysis, blame tracking, branch comparison

# Suggested Fixes
- Add validation for errors file format
- Improve prompt engineering for better error analysis

# Improvements
- Better integration with other agents
- Enhanced diff reporting
"""

from __future__ import annotations
import hashlib
import json
import logging
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple
from base_agent import BaseAgent, create_main_function


class ErrorSeverity(Enum):
    """Error severity levels."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


class ErrorCategory(Enum):
    """Error categories."""
    SYNTAX = "syntax"
    RUNTIME = "runtime"
    LOGIC = "logic"
    TYPE = "type"
    SECURITY = "security"
    PERFORMANCE = "performance"
    STYLE = "style"
    DEPRECATION = "deprecation"
    OTHER = "other"


class NotificationChannel(Enum):
    """Notification channel types."""
    SLACK = "slack"
    TEAMS = "teams"
    EMAIL = "email"
    WEBHOOK = "webhook"
    DISCORD = "discord"


class ExternalReporter(Enum):
    """External error reporting systems."""
    SENTRY = "sentry"
    ROLLBAR = "rollbar"
    BUGSNAG = "bugsnag"
    DATADOG = "datadog"
    NEWRELIC = "newrelic"


class TrendDirection(Enum):
    """Trend direction indicators."""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


@dataclass
class ErrorEntry:
    """A single error entry."""
    id: str
    message: str
    file_path: str
    line_number: int
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.OTHER
    timestamp: str = ""
    stack_trace: str = ""
    suggested_fix: str = ""
    resolved: bool = False
    resolution_timestamp: str = ""
    tags: List[str] = field(default_factory=list)


@dataclass
class ErrorCluster:
    """A cluster of similar errors."""
    id: str
    name: str
    pattern: str
    error_ids: List[str] = field(default_factory=list)
    description: str = ""


@dataclass
class ErrorPattern:
    """A recognized error pattern."""
    name: str
    regex: str
    severity: ErrorSeverity
    category: ErrorCategory
    suggested_fix: str = ""
    occurrences: int = 0


@dataclass
class SuppressionRule:
    """Rule for suppressing specific errors."""
    id: str
    pattern: str
    reason: str
    expires: Optional[str] = None
    created_by: str = ""
    created_at: str = ""


@dataclass
class NotificationConfig:
    """Configuration for error notifications.

    Attributes:
        channel: Notification channel type.
        endpoint: Webhook URL or email address.
        min_severity: Minimum severity to notify.
        enabled: Whether notifications are enabled.
        template: Message template.
    """
    channel: NotificationChannel
    endpoint: str
    min_severity: ErrorSeverity = ErrorSeverity.HIGH
    enabled: bool = True
    template: str = "Error: {message} in {file}:{line}"


@dataclass
class ErrorImpact:
    """Impact analysis for an error.

    Attributes:
        error_id: ID of the analyzed error.
        affected_files: List of files affected by the error.
        affected_functions: Functions impacted by the error.
        downstream_effects: Downstream components affected.
        impact_score: Overall impact score (0 - 100).
    """
    error_id: str
    affected_files: List[str] = field(default_factory=list)
    affected_functions: List[str] = field(default_factory=list)
    downstream_effects: List[str] = field(default_factory=list)
    impact_score: float = 0.0


@dataclass
class TimelineEvent:
    """Event in error timeline.

    Attributes:
        timestamp: When the event occurred.
        event_type: Type of event (created, resolved, recurred).
        error_id: Associated error ID.
        details: Additional event details.
    """
    timestamp: str
    event_type: str
    error_id: str
    details: str = ""


@dataclass
class RegressionInfo:
    """Information about error regression.

    Attributes:
        error_id: ID of the regressed error.
        original_fix_commit: Commit that originally fixed the error.
        regression_commit: Commit that reintroduced the error.
        occurrences: Number of times this error has regressed.
    """
    error_id: str
    original_fix_commit: str = ""
    regression_commit: str = ""
    occurrences: int = 1


@dataclass
class FixSuggestion:
    """Automated fix suggestion for an error.

    Attributes:
        error_id: ID of the error to fix.
        suggestion: The suggested fix.
        confidence: Confidence score (0 - 1).
        code_snippet: Example code for the fix.
        source: Source of the suggestion.
    """
    error_id: str
    suggestion: str
    confidence: float = 0.0
    code_snippet: str = ""
    source: str = "pattern_match"


@dataclass
class ErrorBudget:
    """Error budget tracking for SLO management.

    Attributes:
        budget_name: Name of the error budget.
        total_budget: Total allowed error budget.
        consumed: Amount of budget consumed.
        period_start: Start of the budget period.
        period_end: End of the budget period.
    """
    budget_name: str
    total_budget: float
    consumed: float = 0.0
    period_start: str = ""
    period_end: str = ""


@dataclass
class TrendData:
    """Error trend analysis data.

    Attributes:
        metric_name: Name of the metric being tracked.
        values: Historical values.
        timestamps: Timestamps for each value.
        direction: Current trend direction.
        prediction: Predicted next value.
    """
    metric_name: str
    values: List[float] = field(default_factory=list)
    timestamps: List[str] = field(default_factory=list)
    direction: TrendDirection = TrendDirection.STABLE
    prediction: Optional[float] = None


@dataclass
class BlameInfo:
    """Git blame information for an error.

    Attributes:
        error_id: ID of the error.
        commit_hash: Commit that introduced the error.
        author: Author of the commit.
        commit_date: Date of the commit.
        commit_message: Commit message.
    """
    error_id: str
    commit_hash: str = ""
    author: str = ""
    commit_date: str = ""
    commit_message: str = ""


@dataclass
class BranchComparison:
    """Comparison of errors across branches.

    Attributes:
        branch_a: First branch name.
        branch_b: Second branch name.
        errors_only_in_a: Error IDs only in branch A.
        errors_only_in_b: Error IDs only in branch B.
        common_errors: Error IDs in both branches.
    """
    branch_a: str
    branch_b: str
    errors_only_in_a: List[str] = field(default_factory=list)
    errors_only_in_b: List[str] = field(default_factory=list)
    common_errors: List[str] = field(default_factory=list)


# Default error patterns
DEFAULT_ERROR_PATTERNS: List[ErrorPattern] = [
    ErrorPattern(
        name="undefined_variable",
        regex=r"NameError: name '(\w+)' is not defined",
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
        suggested_fix="Define the variable before use or check for typos"
    ),
    ErrorPattern(
        name="syntax_error",
        regex=r"SyntaxError: (.*)",
        severity=ErrorSeverity.CRITICAL,
        category=ErrorCategory.SYNTAX,
        suggested_fix="Fix the syntax according to the error message"
    ),
    ErrorPattern(
        name="type_error",
        regex=r"TypeError: (.*)",
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.TYPE,
        suggested_fix="Check type compatibility of operands"
    ),
    ErrorPattern(
        name="import_error",
        regex=r"ImportError: (.*)",
        severity=ErrorSeverity.HIGH,
        category=ErrorCategory.RUNTIME,
        suggested_fix="Ensure the module is installed and accessible"
    ),
    ErrorPattern(
        name="attribute_error",
        regex=r"AttributeError: (.*)",
        severity=ErrorSeverity.MEDIUM,
        category=ErrorCategory.RUNTIME,
        suggested_fix="Check if the attribute exists on the object"
    ),
]


# ========== Session 7 Helper Classes ==========


class NotificationManager:
    """Manages error notifications to various channels.

    Supports Slack, Teams, Email, Webhooks, and Discord notifications
    with configurable severity thresholds.

    Attributes:
        configs: List of notification configurations.
    """

    def __init__(self) -> None:
        """Initialize the notification manager."""
        self.configs: List[NotificationConfig] = []

    def add_config(self, config: NotificationConfig) -> None:
        """Add a notification configuration.

        Args:
            config: The notification configuration to add.
        """
        self.configs.append(config)

    def remove_config(self, channel: NotificationChannel) -> bool:
        """Remove a notification configuration by channel.

        Args:
            channel: The channel type to remove.

        Returns:
            True if removed, False if not found.
        """
        for i, cfg in enumerate(self.configs):
            if cfg.channel == channel:
                del self.configs[i]
                return True
        return False

    def notify(self, error: ErrorEntry) -> List[str]:
        """Send notifications for an error.

        Args:
            error: The error to notify about.

        Returns:
            List of channels that were notified.
        """
        notified: List[str] = []
        for config in self.configs:
            if not config.enabled:
                continue
            if error.severity.value >= config.min_severity.value:
                message = self._format_message(error, config.template)
                if self._send(config, message):
                    notified.append(config.channel.value)
        return notified

    def _format_message(self, error: ErrorEntry, template: str) -> str:
        """Format notification message from template."""
        return template.format(
            message=error.message,
            file=error.file_path,
            line=error.line_number,
            severity=error.severity.name,
            category=error.category.value
        )

    def _send(self, config: NotificationConfig, message: str) -> bool:
        """Send a notification (stub for actual implementation)."""
        logging.info(f"Notification to {config.channel.value}: {message}")
        return True

    def get_configs(self) -> List[NotificationConfig]:
        """Get all notification configurations."""
        return self.configs


class ImpactAnalyzer:
    """Analyzes the impact of errors on the codebase.

    Determines which files and functions are affected by errors
    and calculates impact scores.

    Attributes:
        file_dependencies: Map of file dependencies.
    """

    def __init__(self) -> None:
        """Initialize the impact analyzer."""
        self.file_dependencies: Dict[str, List[str]] = {}
        self.function_map: Dict[str, List[str]] = {}

    def add_dependency(self, file: str, depends_on: List[str]) -> None:
        """Add file dependencies.

        Args:
            file: The file path.
            depends_on: List of files this file depends on.
        """
        self.file_dependencies[file] = depends_on

    def add_functions(self, file: str, functions: List[str]) -> None:
        """Add functions in a file.

        Args:
            file: The file path.
            functions: List of function names in the file.
        """
        self.function_map[file] = functions

    def analyze(self, error: ErrorEntry) -> ErrorImpact:
        """Analyze the impact of an error.

        Args:
            error: The error to analyze.

        Returns:
            ErrorImpact with affected files and functions.
        """
        affected_files = self._find_affected_files(error.file_path)
        affected_functions = self.function_map.get(error.file_path, [])
        downstream = self._find_downstream_effects(error.file_path)

        impact_score = self._calculate_impact_score(
            len(affected_files),
            len(affected_functions),
            error.severity
        )

        return ErrorImpact(
            error_id=error.id,
            affected_files=affected_files,
            affected_functions=affected_functions,
            downstream_effects=downstream,
            impact_score=impact_score
        )

    def _find_affected_files(self, file_path: str) -> List[str]:
        """Find files that depend on the given file."""
        affected = []
        for file, deps in self.file_dependencies.items():
            if file_path in deps:
                affected.append(file)
        return affected

    def _find_downstream_effects(self, file_path: str) -> List[str]:
        """Find downstream effects recursively."""
        effects: List[str] = []
        visited: Set[str] = set()
        self._find_downstream_recursive(file_path, effects, visited)
        return effects

    def _find_downstream_recursive(
        self, file_path: str, effects: List[str], visited: Set[str]
    ) -> None:
        """Recursively find downstream effects."""
        if file_path in visited:
            return
        visited.add(file_path)
        for file, deps in self.file_dependencies.items():
            if file_path in deps and file not in effects:
                effects.append(file)
                self._find_downstream_recursive(file, effects, visited)

    def _calculate_impact_score(
        self, file_count: int, func_count: int, severity: ErrorSeverity
    ) -> float:
        """Calculate an impact score."""
        base = severity.value * 10
        file_impact = min(file_count * 5, 30)
        func_impact = min(func_count * 2, 20)
        return min(100, base + file_impact + func_impact)


class TimelineTracker:
    """Tracks error events over time.

    Maintains a timeline of error creation, resolution, and recurrence
    events for visualization and analysis.

    Attributes:
        events: List of timeline events.
    """

    def __init__(self) -> None:
        """Initialize the timeline tracker."""
        self.events: List[TimelineEvent] = []

    def record_event(
        self, error_id: str, event_type: str, details: str = ""
    ) -> TimelineEvent:
        """Record a timeline event.

        Args:
            error_id: ID of the associated error.
            event_type: Type of event (created, resolved, recurred).
            details: Additional event details.

        Returns:
            The recorded TimelineEvent.
        """
        event = TimelineEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_type,
            error_id=error_id,
            details=details
        )
        self.events.append(event)
        return event

    def get_events_for_error(self, error_id: str) -> List[TimelineEvent]:
        """Get all events for a specific error."""
        return [e for e in self.events if e.error_id == error_id]

    def get_events_in_range(
        self, start: str, end: str
    ) -> List[TimelineEvent]:
        """Get events within a time range."""
        return [
            e for e in self.events
            if start <= e.timestamp <= end
        ]

    def generate_timeline_data(self) -> Dict[str, Any]:
        """Generate timeline data for visualization."""
        by_date: Dict[str, int] = {}
        for event in self.events:
            date = event.timestamp[:10]  # YYYY - MM - DD
            by_date[date] = by_date.get(date, 0) + 1

        return {
            "total_events": len(self.events),
            "events_by_date": by_date,
            "event_types": list(set(e.event_type for e in self.events))
        }

    def clear(self) -> None:
        """Clear all timeline events."""
        self.events = []


class RegressionDetector:
    """Detects error regressions.

    Identifies errors that were previously fixed but have reappeared
    in the codebase.

    Attributes:
        fixed_errors: Map of fixed error signatures to commit info.
    """

    def __init__(self) -> None:
        """Initialize the regression detector."""
        self.fixed_errors: Dict[str, str] = {}  # signature -> fix_commit
        self.regressions: List[RegressionInfo] = []

    def record_fix(self, error: ErrorEntry, commit_hash: str) -> None:
        """Record that an error was fixed.

        Args:
            error: The fixed error.
            commit_hash: The commit that fixed the error.
        """
        signature = self._get_error_signature(error)
        self.fixed_errors[signature] = commit_hash

    def check_regression(
        self, error: ErrorEntry, current_commit: str = ""
    ) -> Optional[RegressionInfo]:
        """Check if an error is a regression.

        Args:
            error: The error to check.
            current_commit: Current commit hash.

        Returns:
            RegressionInfo if this is a regression, None otherwise.
        """
        signature = self._get_error_signature(error)
        if signature in self.fixed_errors:
            regression = RegressionInfo(
                error_id=error.id,
                original_fix_commit=self.fixed_errors[signature],
                regression_commit=current_commit
            )
            # Check if already tracked
            for r in self.regressions:
                if r.error_id == error.id:
                    r.occurrences += 1
                    return r
            self.regressions.append(regression)
            return regression
        return None

    def _get_error_signature(self, error: ErrorEntry) -> str:
        """Generate a signature for an error."""
        normalized = re.sub(r"\d+", "N", error.message)
        return f"{error.file_path}:{normalized}"

    def get_regressions(self) -> List[RegressionInfo]:
        """Get all detected regressions."""
        return self.regressions

    def get_regression_rate(self) -> float:
        """Calculate the regression rate."""
        if not self.fixed_errors:
            return 0.0
        return len(self.regressions) / len(self.fixed_errors) * 100


class AutoFixSuggester:
    """Generates automated fix suggestions for errors.

    Uses pattern matching and common fixes to suggest
    resolutions for errors.

    Attributes:
        fix_patterns: Map of error patterns to fix templates.
    """

    def __init__(self) -> None:
        """Initialize the auto-fix suggester."""
        self.fix_patterns: Dict[str, str] = {
            r"NameError: name '(\w+)' is not defined":
                "Define variable '{0}' before use or import it",
            r"ImportError: No module named '(\w+)'":
                "Install module with: pip install {0}",
            r"TypeError: unsupported operand type":
                "Check operand types and convert if necessary",
            r"AttributeError: '(\w+)' object has no attribute '(\w+)'":
                "Check if '{1}' exists on {0} object or use hasattr()",
            r"IndexError: list index out of range":
                "Check list bounds before accessing index",
            r"KeyError: '(\w+)'":
                "Use .get('{0}', default) or check key existence",
        }

    def add_pattern(self, pattern: str, fix_template: str) -> None:
        """Add a fix pattern.

        Args:
            pattern: Regex pattern to match errors.
            fix_template: Template for the fix suggestion.
        """
        self.fix_patterns[pattern] = fix_template

    def suggest(self, error: ErrorEntry) -> Optional[FixSuggestion]:
        """Generate a fix suggestion for an error.

        Args:
            error: The error to fix.

        Returns:
            FixSuggestion if a fix is available, None otherwise.
        """
        for pattern, template in self.fix_patterns.items():
            match = re.search(pattern, error.message)
            if match:
                groups = match.groups()
                suggestion = template.format(*groups) if groups else template
                return FixSuggestion(
                    error_id=error.id,
                    suggestion=suggestion,
                    confidence=0.8,
                    source="pattern_match"
                )
        return None

    def suggest_all(
        self, errors: List[ErrorEntry]
    ) -> List[FixSuggestion]:
        """Generate suggestions for multiple errors."""
        suggestions = []
        for error in errors:
            sugg = self.suggest(error)
            if sugg:
                suggestions.append(sugg)
        return suggestions


class ExternalReportingClient:
    """Reports errors to external systems.

    Supports Sentry, Rollbar, Bugsnag, Datadog, and NewRelic
    integrations.

    Attributes:
        system: The external system to report to.
        dsn: Data source name or API key.
    """

    def __init__(
        self, system: ExternalReporter, dsn: str = ""
    ) -> None:
        """Initialize the external reporting client.

        Args:
            system: The external system type.
            dsn: Data source name or API key.
        """
        self.system = system
        self.dsn = dsn
        self.enabled = bool(dsn)

    def report(self, error: ErrorEntry) -> bool:
        """Report an error to the external system.

        Args:
            error: The error to report.

        Returns:
            True if reported successfully.
        """
        if not self.enabled:
            return False
        self._build_payload(error)
        logging.info(
            f"Reporting to {self.system.value}: {error.id}"
        )
        # Actual implementation would send to the service
        return True

    def report_batch(self, errors: List[ErrorEntry]) -> int:
        """Report multiple errors.

        Args:
            errors: List of errors to report.

        Returns:
            Number of errors successfully reported.
        """
        count = 0
        for error in errors:
            if self.report(error):
                count += 1
        return count

    def _build_payload(self, error: ErrorEntry) -> Dict[str, Any]:
        """Build the payload for the external system."""
        return {
            "message": error.message,
            "level": error.severity.name.lower(),
            "tags": {
                "category": error.category.value,
                "file": error.file_path,
                "line": error.line_number
            },
            "extra": {
                "stack_trace": error.stack_trace,
                "suggested_fix": error.suggested_fix
            }
        }


class ErrorBudgetManager:
    """Manages error budgets for SLO tracking.

    Tracks error budget consumption over time periods
    to support SLO management.

    Attributes:
        budgets: Map of budget names to ErrorBudget objects.
    """

    def __init__(self) -> None:
        """Initialize the error budget manager."""
        self.budgets: Dict[str, ErrorBudget] = {}

    def create_budget(
        self,
        name: str,
        total: float,
        period_days: int = 30
    ) -> ErrorBudget:
        """Create an error budget.

        Args:
            name: Budget name.
            total: Total budget amount.
            period_days: Budget period in days.

        Returns:
            The created ErrorBudget.
        """
        now = datetime.now()
        end = now + timedelta(days=period_days)
        budget = ErrorBudget(
            budget_name=name,
            total_budget=total,
            period_start=now.isoformat(),
            period_end=end.isoformat()
        )
        self.budgets[name] = budget
        return budget

    def consume(self, name: str, amount: float) -> bool:
        """Consume error budget.

        Args:
            name: Budget name.
            amount: Amount to consume.

        Returns:
            True if budget was consumed, False if exceeded.
        """
        if name not in self.budgets:
            return False
        budget = self.budgets[name]
        if budget.consumed + amount > budget.total_budget:
            return False
        budget.consumed += amount
        return True

    def get_remaining(self, name: str) -> float:
        """Get remaining budget.

        Args:
            name: Budget name.

        Returns:
            Remaining budget amount.
        """
        if name not in self.budgets:
            return 0.0
        budget = self.budgets[name]
        return budget.total_budget - budget.consumed

    def get_consumption_rate(self, name: str) -> float:
        """Get budget consumption rate as percentage."""
        if name not in self.budgets:
            return 0.0
        budget = self.budgets[name]
        if budget.total_budget == 0:
            return 100.0
        return (budget.consumed / budget.total_budget) * 100

    def is_exceeded(self, name: str) -> bool:
        """Check if budget is exceeded."""
        if name not in self.budgets:
            return True
        budget = self.budgets[name]
        return budget.consumed >= budget.total_budget


class TrendAnalyzer:
    """Analyzes error trends over time.

    Provides trend analysis with predictions based on
    historical error data.

    Attributes:
        data_points: Map of metric names to TrendData.
    """

    def __init__(self) -> None:
        """Initialize the trend analyzer."""
        self.data_points: Dict[str, TrendData] = {}

    def record(self, metric: str, value: float) -> None:
        """Record a data point.

        Args:
            metric: Metric name.
            value: Value to record.
        """
        if metric not in self.data_points:
            self.data_points[metric] = TrendData(metric_name=metric)
        data = self.data_points[metric]
        data.values.append(value)
        data.timestamps.append(datetime.now().isoformat())

    def analyze(self, metric: str) -> TrendData:
        """Analyze trend for a metric.

        Args:
            metric: Metric name.

        Returns:
            TrendData with direction and prediction.
        """
        if metric not in self.data_points:
            return TrendData(metric_name=metric)

        data = self.data_points[metric]
        if len(data.values) < 2:
            data.direction = TrendDirection.STABLE
            return data

        # Calculate direction
        recent = data.values[-5:] if len(data.values) >= 5 else data.values
        avg_change = sum(
            recent[i] - recent[i - 1]
            for i in range(1, len(recent))
        ) / (len(recent) - 1)

        if avg_change > 0.1:
            data.direction = TrendDirection.INCREASING
        elif avg_change < -0.1:
            data.direction = TrendDirection.DECREASING
        else:
            data.direction = TrendDirection.STABLE

        # Simple prediction
        data.prediction = data.values[-1] + avg_change

        return data

    def predict(self, metric: str, periods: int = 1) -> List[float]:
        """Predict future values.

        Args:
            metric: Metric name.
            periods: Number of periods to predict.

        Returns:
            List of predicted values.
        """
        data = self.analyze(metric)
        if not data.values:
            return []

        predictions = []
        last_value = data.values[-1]
        avg_change = 0.0
        if len(data.values) >= 2:
            changes = [
                data.values[i] - data.values[i - 1]
                for i in range(1, len(data.values))
            ]
            avg_change = sum(changes) / len(changes)

        for i in range(periods):
            predictions.append(last_value + avg_change * (i + 1))

        return predictions


class BlameTracker:
    """Tracks git blame information for errors.

    Uses git integration to identify who introduced errors
    and when.

    Attributes:
        blame_cache: Cache of blame information.
    """

    def __init__(self) -> None:
        """Initialize the blame tracker."""
        self.blame_cache: Dict[str, BlameInfo] = {}

    def get_blame(self, error: ErrorEntry) -> BlameInfo:
        """Get blame information for an error.

        Args:
            error: The error to get blame for.

        Returns:
            BlameInfo with commit and author details.
        """
        cache_key = f"{error.file_path}:{error.line_number}"
        if cache_key in self.blame_cache:
            return self.blame_cache[cache_key]

        blame_info = BlameInfo(error_id=error.id)

        try:
            result = subprocess.run(
                ["git", "blame", "-L",
                 f"{error.line_number},{error.line_number}",
                 "--porcelain", error.file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                blame_info = self._parse_blame_output(
                    error.id, result.stdout
                )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        self.blame_cache[cache_key] = blame_info
        return blame_info

    def _parse_blame_output(
        self, error_id: str, output: str
    ) -> BlameInfo:
        """Parse git blame output."""
        lines = output.strip().split('\n')
        info = BlameInfo(error_id=error_id)

        if lines:
            parts = lines[0].split()
            if parts:
                info.commit_hash = parts[0]

        for line in lines:
            if line.startswith("author "):
                info.author = line[7:]
            elif line.startswith("author-time "):
                timestamp = int(line[12:])
                info.commit_date = datetime.fromtimestamp(
                    timestamp
                ).isoformat()
            elif line.startswith("summary "):
                info.commit_message = line[8:]

        return info

    def get_top_contributors(
        self, errors: List[ErrorEntry], limit: int = 5
    ) -> List[Tuple[str, int]]:
        """Get top contributors to errors.

        Args:
            errors: List of errors to analyze.
            limit: Maximum number of contributors to return.

        Returns:
            List of (author, count) tuples.
        """
        author_counts: Dict[str, int] = {}
        for error in errors:
            blame = self.get_blame(error)
            if blame.author:
                author_counts[blame.author] = (
                    author_counts.get(blame.author, 0) + 1
                )

        sorted_authors = sorted(
            author_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_authors[:limit]


class BranchComparer:
    """Compares errors across git branches.

    Identifies errors that exist only in specific branches
    or are common across branches.

    Attributes:
        branch_errors: Map of branch names to error sets.
    """

    def __init__(self) -> None:
        """Initialize the branch comparer."""
        self.branch_errors: Dict[str, Set[str]] = {}

    def set_branch_errors(
        self, branch: str, error_ids: List[str]
    ) -> None:
        """Set errors for a branch.

        Args:
            branch: Branch name.
            error_ids: List of error IDs in the branch.
        """
        self.branch_errors[branch] = set(error_ids)

    def compare(self, branch_a: str, branch_b: str) -> BranchComparison:
        """Compare errors between two branches.

        Args:
            branch_a: First branch name.
            branch_b: Second branch name.

        Returns:
            BranchComparison with differences.
        """
        errors_a = self.branch_errors.get(branch_a, set())
        errors_b = self.branch_errors.get(branch_b, set())

        return BranchComparison(
            branch_a=branch_a,
            branch_b=branch_b,
            errors_only_in_a=list(errors_a - errors_b),
            errors_only_in_b=list(errors_b - errors_a),
            common_errors=list(errors_a & errors_b)
        )

    def get_new_errors(
        self, base_branch: str, feature_branch: str
    ) -> List[str]:
        """Get errors introduced in feature branch.

        Args:
            base_branch: Base branch name (e.g., main).
            feature_branch: Feature branch name.

        Returns:
            List of error IDs only in feature branch.
        """
        comparison = self.compare(base_branch, feature_branch)
        return comparison.errors_only_in_b

    def get_fixed_errors(
        self, base_branch: str, feature_branch: str
    ) -> List[str]:
        """Get errors fixed in feature branch.

        Args:
            base_branch: Base branch name.
            feature_branch: Feature branch name.

        Returns:
            List of error IDs fixed in feature branch.
        """
        comparison = self.compare(base_branch, feature_branch)
        return comparison.errors_only_in_a


class ErrorsAgent(BaseAgent):
    """Updates code file error reports using AI assistance."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_error_file_path()
        self._check_associated_file()
        # New features
        self._errors: List[ErrorEntry] = []
        self._clusters: Dict[str, ErrorCluster] = {}
        self._patterns: List[ErrorPattern] = list(DEFAULT_ERROR_PATTERNS)
        self._suppression_rules: List[SuppressionRule] = []
        self._annotations: Dict[str, List[str]] = {}  # error_id -> annotations
        self._statistics: Dict[str, Any] = {}

    def _validate_error_file_path(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.errors.md'):
            logging.warning(f"File {self.file_path.name} does not end with .errors.md")

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists."""
        name = self.file_path.name
        if name.endswith('.errors.md'):
            base_name = name[:-10]  # len('.errors.md')
            # Try to find the file with common extensions or exact match
            candidate = self.file_path.parent / base_name
            if candidate.exists():
                return
            # Try adding extensions
            for ext in ['.py', '.sh', '.js', '.ts', '.md']:
                candidate = self.file_path.parent / (base_name + ext)
                if candidate.exists() and candidate != self.file_path:
                    return
            logging.warning(f"Could not find associated code file for {self.file_path.name}")

    # ========== Error Management ==========
    def add_error(
        self,
        message: str,
        file_path: str,
        line_number: int,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        category: ErrorCategory = ErrorCategory.OTHER,
        stack_trace: str = "",
        suggested_fix: str = ""
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
            suggested_fix=suggested_fix
        )
        # Check if suppressed
        if not self._is_suppressed(error):
            self._errors.append(error)
            self._auto_categorize_error(error)
        return error

    def get_errors(self) -> List[ErrorEntry]:
        """Get all errors."""
        return self._errors

    def get_error_by_id(self, error_id: str) -> Optional[ErrorEntry]:
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

    def get_unresolved_errors(self) -> List[ErrorEntry]:
        """Get all unresolved errors."""
        return [e for e in self._errors if not e.resolved]

    def get_errors_by_severity(self, severity: ErrorSeverity) -> List[ErrorEntry]:
        """Get errors filtered by severity."""
        return [e for e in self._errors if e.severity == severity]

    def get_errors_by_category(self, category: ErrorCategory) -> List[ErrorEntry]:
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

    def prioritize_errors(self) -> List[ErrorEntry]:
        """Return errors sorted by priority (highest first)."""
        return sorted(
            self._errors,
            key=lambda e: self.calculate_severity_score(e),
            reverse=True
        )

    # ========== Error Clustering ==========
    def cluster_similar_errors(self) -> Dict[str, ErrorCluster]:
        """Cluster similar errors together."""
        clusters: Dict[str, List[ErrorEntry]] = {}
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
                    description=f"Cluster of {len(errors)} similar errors"
                )
        return self._clusters

    def _get_cluster_key(self, error: ErrorEntry) -> str:
        """Generate a clustering key for an error."""
        # Normalize the message by removing variable parts
        normalized = re.sub(r"'[^']*'", "'<var>'", error.message)
        normalized = re.sub(r"\d+", "<num>", normalized)
        return f"{error.category.value}:{normalized}"

    def get_cluster(self, cluster_id: str) -> Optional[ErrorCluster]:
        """Get a cluster by ID."""
        return self._clusters.get(cluster_id)

    def get_errors_in_cluster(self, cluster_id: str) -> List[ErrorEntry]:
        """Get all errors in a cluster."""
        cluster = self._clusters.get(cluster_id)
        if not cluster:
            return []
        return [e for e in self._errors if e.id in cluster.error_ids]

    # ========== Pattern Recognition ==========
    def add_pattern(self, pattern: ErrorPattern) -> None:
        """Add a custom error pattern."""
        self._patterns.append(pattern)

    def recognize_pattern(self, error: ErrorEntry) -> Optional[ErrorPattern]:
        """Recognize if an error matches a known pattern."""
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
            if not error.suggested_fix:
                error.suggested_fix = pattern.suggested_fix

    def get_pattern_statistics(self) -> Dict[str, int]:
        """Get statistics on pattern occurrences."""
        return {p.name: p.occurrences for p in self._patterns}

    # ========== Suppression Rules ==========
    def add_suppression_rule(
        self,
        pattern: str,
        reason: str,
        expires: Optional[str] = None,
        created_by: str = ""
    ) -> SuppressionRule:
        """Add a suppression rule."""
        rule = SuppressionRule(
            id=hashlib.md5(pattern.encode()).hexdigest()[:8],
            pattern=pattern,
            reason=reason,
            expires=expires,
            created_by=created_by,
            created_at=datetime.now().isoformat()
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
        for rule in self._suppression_rules:
            # Check expiration
            if rule.expires:
                try:
                    expires_dt = datetime.fromisoformat(rule.expires)
                    if datetime.now() > expires_dt:
                        continue
                except ValueError:
                    pass
            if re.search(rule.pattern, error.message):
                return True
        return False

    def get_suppression_rules(self) -> List[SuppressionRule]:
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

    def get_annotations(self, error_id: str) -> List[str]:
        """Get annotations for an error."""
        return self._annotations.get(error_id, [])

    # ========== Deduplication ==========
    def deduplicate_errors(self) -> int:
        """Remove duplicate errors, returns count removed."""
        seen: Set[str] = set()
        unique: List[ErrorEntry] = []
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
    def calculate_statistics(self) -> Dict[str, Any]:
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
            "suppression_rules_count": len(self._suppression_rules)
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
                    docs.append(f"- [{status}] {error.message} (line {error.line_number})")
                docs.append("")
        return '\n'.join(docs)

    def export_errors(self, format: str = "json") -> str:
        """Export errors to various formats."""
        if format == "json":
            data = [{
                "id": e.id,
                "message": e.message,
                "file": e.file_path,
                "line": e.line_number,
                "severity": e.severity.name,
                "category": e.category.name,
                "resolved": e.resolved
            } for e in self._errors]
            return json.dumps(data, indent=2)
        elif format == "csv":
            lines = ["id,message,file,line,severity,category,resolved"]
            for e in self._errors:
                lines.append(
                    f"{e.id},{e.message},{e.file_path},"
                    f"{e.line_number},{e.severity.name},"
                    f"{e.category.name},{e.resolved}"
                )
            return '\n'.join(lines)
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
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original error report preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the error report.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids duplicated wrapper sections).
        """
        logging.info(f"Improving error report for {self.file_path}")
        return super().improve_content(prompt)


# Create main function using the helper
main = create_main_function(
    ErrorsAgent,
    'Errors Agent: Updates code file error reports',
    'Path to the errors file (e.g., file.errors.md)'
)


if __name__ == '__main__':
    main()
