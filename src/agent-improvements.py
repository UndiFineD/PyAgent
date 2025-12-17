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
Improvements Agent: Improves and updates code file improvement suggestions.

Reads an improvements file (Codefile.improvements.md), uses Copilot to enhance the suggestions,
and updates the improvements file with improvements.

# Description
This module provides an Improvements Agent that reads existing code file improvement suggestions,
uses AI assistance to improve and complete them, and updates the improvements files
with enhanced documentation.

# Changelog
- 1.0.0: Initial implementation
- 1.1.0: Added impact scoring, dependencies, effort estimation, templates
- 1.2.0: Added scheduling, progress dashboards, validation, rollback tracking,
         tool integration, SLA management, merge detection, archiving

# Suggested Fixes
- Add validation for improvements file format
- Improve prompt engineering for better suggestions

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
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from base_agent import BaseAgent, create_main_function


class ImprovementPriority(Enum):
    """Priority levels for improvements."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NICE_TO_HAVE = 1


class ImprovementCategory(Enum):
    """Categories for improvements."""
    PERFORMANCE = "performance"
    SECURITY = "security"
    MAINTAINABILITY = "maintainability"
    READABILITY = "readability"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    REFACTORING = "refactoring"
    BUG_FIX = "bug_fix"
    FEATURE = "feature"
    OTHER = "other"


class ImprovementStatus(Enum):
    """Status of an improvement."""
    PROPOSED = "proposed"
    SUGGESTED = "suggested"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    DEFERRED = "deferred"


class EffortEstimate(Enum):
    """Effort estimation levels."""
    TRIVIAL = 1  # < 1 hour
    SMALL = 2    # 1 - 4 hours
    MEDIUM = 3   # 1 - 2 days
    LARGE = 4    # 3 - 5 days
    EPIC = 5     # > 1 week


class ScheduleStatus(Enum):
    """Status of scheduled improvements."""
    UNSCHEDULED = "unscheduled"
    SCHEDULED = "scheduled"
    IN_SPRINT = "in_sprint"
    BLOCKED = "blocked"
    OVERDUE = "overdue"


class ValidationSeverity(Enum):
    """Severity of validation issues."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class AnalysisToolType(Enum):
    """Types of code analysis tools."""
    LINTER = "linter"
    TYPE_CHECKER = "type_checker"
    SECURITY_SCANNER = "security_scanner"
    COVERAGE = "coverage"
    COMPLEXITY = "complexity"


class SLALevel(Enum):
    """SLA priority levels."""
    P0 = 1   # 24 hours
    P1 = 2   # 3 days
    P2 = 3   # 1 week
    P3 = 4   # 2 weeks
    P4 = 5   # 1 month


@dataclass
class Improvement:
    """A single improvement suggestion."""
    id: str
    title: str
    description: str
    file_path: str
    priority: ImprovementPriority = ImprovementPriority.MEDIUM
    category: ImprovementCategory = ImprovementCategory.OTHER
    status: ImprovementStatus = ImprovementStatus.SUGGESTED
    effort: EffortEstimate = EffortEstimate.MEDIUM
    impact_score: float = 50.0
    created_at: str = ""
    updated_at: str = ""
    assignee: str = ""
    tags: List[str] = field(default_factory=list)  # type: ignore[assignment]
    dependencies: List[str] = field(default_factory=list)  # type: ignore[assignment]
    votes: int = 0


@dataclass
@dataclass
class ImprovementTemplate:
    """Template for creating improvements."""
    id: str
    name: str
    category: ImprovementCategory
    title_pattern: str = ""
    description_template: str = ""
    default_priority: ImprovementPriority = ImprovementPriority.MEDIUM
    default_effort: EffortEstimate = EffortEstimate.MEDIUM


@dataclass
class ScheduledImprovement:
    """A scheduled improvement with resource allocation.

    Attributes:
        improvement_id: ID of the scheduled improvement.
        scheduled_start: Planned start date.
        scheduled_end: Planned end date.
        assigned_resources: List of assigned team members.
        status: Current schedule status.
        sprint_id: Optional sprint identifier.
    """
    improvement_id: str
    scheduled_start: str = ""
    scheduled_end: str = ""
    assigned_resources: List[str] = field(default_factory=list)  # type: ignore[assignment]
    status: ScheduleStatus = ScheduleStatus.UNSCHEDULED
    sprint_id: str = ""


@dataclass
class ProgressReport:
    """Progress report for improvements dashboard.

    Attributes:
        report_date: Date of the report.
        completed_count: Number of completed improvements.
        in_progress_count: Number of in - progress improvements.
        blocked_count: Number of blocked improvements.
        velocity: Average improvements completed per week.
        burndown_data: Data for burndown chart.
    """
    report_date: str
    completed_count: int = 0
    in_progress_count: int = 0
    blocked_count: int = 0
    velocity: float = 0.0
    burndown_data: List[Tuple[str, int]] = field(default_factory=list)  # type: ignore[assignment]


@dataclass
class ValidationResult:
    """Result from improvement validation.

    Attributes:
        improvement_id: ID of the validated improvement.
        is_valid: Whether the improvement passed validation.
        issues: List of validation issues.
        test_results: Results from automated tests.
    """
    improvement_id: str
    is_valid: bool = True
    issues: List[Tuple[ValidationSeverity, str]] = field(
        default_factory=list
    )  # type: ignore[assignment]
    test_results: Dict[str, bool] = field(
        default_factory=dict
    )  # type: ignore[assignment]


@dataclass
class RollbackRecord:
    """Record of an improvement rollback.

    Attributes:
        improvement_id: ID of the rolled back improvement.
        rollback_date: When the rollback occurred.
        reason: Reason for the rollback.
        previous_state: State before the improvement.
        rollback_commit: Git commit of the rollback.
    """
    improvement_id: str
    rollback_date: str = ""
    reason: str = ""
    previous_state: str = ""
    rollback_commit: str = ""


@dataclass
class ToolSuggestion:
    """Suggestion from a code analysis tool.

    Attributes:
        tool_type: Type of analysis tool.
        tool_name: Name of the specific tool.
        file_path: File with the issue.
        line_number: Line number of the issue.
        message: Suggestion message.
        suggested_fix: Optional code fix.
    """
    tool_type: AnalysisToolType
    tool_name: str
    file_path: str
    line_number: int
    message: str
    suggested_fix: str = ""


@dataclass
class SLAConfiguration:
    """SLA configuration for improvements.

    Attributes:
        level: SLA priority level.
        max_hours: Maximum hours to resolution.
        escalation_hours: Hours before escalation.
        notification_emails: Emails to notify.
    """
    level: SLALevel
    max_hours: int
    escalation_hours: int
    notification_emails: List[str] = field(default_factory=list)  # type: ignore[assignment]


@dataclass
class MergeCandidate:
    """Candidate for merging with another improvement.

    Attributes:
        source_id: ID of the source improvement.
        target_id: ID of the target improvement.
        similarity_score: How similar the improvements are.
        merge_reason: Why these should be merged.
    """
    source_id: str
    target_id: str
    similarity_score: float = 0.0
    merge_reason: str = ""


@dataclass
class ImprovementDiff:
    """Difference in a single improvement between branches.

    Attributes:
        improvement_id: Unique improvement identifier.
        diff_type: Type of difference.
        source_version: Improvement in source branch (if exists).
        target_version: Improvement in target branch (if exists).
        change_summary: Summary of changes.
    """
    improvement_id: str
    diff_type: ImprovementDiffType
    source_version: Optional[Improvement] = None
    target_version: Optional[Improvement] = None
    change_summary: str = ""


@dataclass
class ArchivedImprovement:
    """An archived improvement.

    Attributes:
        improvement: The archived improvement data.
        archived_date: When it was archived.
        archived_by: Who archived it.
        archive_reason: Why it was archived.
    """
    improvement: Improvement
    archived_date: str = ""
    archived_by: str = ""
    archive_reason: str = ""


# Default templates
DEFAULT_TEMPLATES: List[ImprovementTemplate] = [
    ImprovementTemplate(
        id="add_tests",
        name="add_tests",
        category=ImprovementCategory.TESTING,
        title_pattern="Add tests for {function_name}",
        description_template=(
            "Add unit tests to cover {function_name} including "
            "edge cases and error handling."
        ),
        default_effort=EffortEstimate.SMALL
    ),
    ImprovementTemplate(
        id="add_type_hints",
        name="add_type_hints",
        category=ImprovementCategory.MAINTAINABILITY,
        title_pattern="Add type hints to {function_name}",
        description_template=(
            "Add proper type annotations to {function_name} for "
            "better IDE support and documentation."
        ),
        default_effort=EffortEstimate.TRIVIAL
    ),
    ImprovementTemplate(
        id="improve_performance",
        name="improve_performance",
        category=ImprovementCategory.PERFORMANCE,
        title_pattern="Optimize {target}",
        description_template="Improve performance of {target} by {optimization_method}.",
        default_priority=ImprovementPriority.HIGH,
        default_effort=EffortEstimate.MEDIUM
    ),
    ImprovementTemplate(
        id="security_fix",
        name="security_fix",
        category=ImprovementCategory.SECURITY,
        title_pattern="Fix security issue in {component}",
        description_template="Address security vulnerability: {vulnerability_description}",
        default_priority=ImprovementPriority.CRITICAL,
        default_effort=EffortEstimate.MEDIUM
    ),
]


# ========== Session 7 Helper Classes ==========


class ImprovementScheduler:
    """Manages improvement scheduling with resource allocation.

    Schedules improvements into sprints and tracks resource availability.

    Attributes:
        schedule: Map of improvement IDs to scheduled items.
        resources: Map of resource names to availability.
    """

    def __init__(self) -> None:
        """Initialize the scheduler."""
        self.schedule: Dict[str, ScheduledImprovement] = {}
        self.resources: Dict[str, List[str]] = {}  # resource -> busy dates
        self.sprints: Dict[str, List[str]] = {}  # sprint_id -> improvement_ids

    def schedule_improvement(
        self,
        improvement: Improvement,
        start_date: str,
        resources: Optional[List[str]] = None,
        sprint_id: str = ""
    ) -> ScheduledImprovement:
        """Schedule an improvement.

        Args:
            improvement: The improvement to schedule.
            start_date: Start date (ISO format).
            resources: List of assigned resources.
            sprint_id: Optional sprint identifier.

        Returns:
            The scheduled improvement.
        """
        # Calculate end date based on effort
        effort_days = {
            EffortEstimate.TRIVIAL: 1,
            EffortEstimate.SMALL: 2,
            EffortEstimate.MEDIUM: 5,
            EffortEstimate.LARGE: 10,
            EffortEstimate.EPIC: 20,
        }
        days = effort_days.get(improvement.effort, 5)
        start_dt = datetime.fromisoformat(start_date)
        end_dt = start_dt + timedelta(days=days)

        scheduled = ScheduledImprovement(
            improvement_id=improvement.id,
            scheduled_start=start_date,
            scheduled_end=end_dt.isoformat()[:10],
            assigned_resources=resources or [],
            status=ScheduleStatus.SCHEDULED,
            sprint_id=sprint_id
        )

        self.schedule[improvement.id] = scheduled

        if sprint_id:
            if sprint_id not in self.sprints:
                self.sprints[sprint_id] = []
            self.sprints[sprint_id].append(improvement.id)

        return scheduled

    def get_schedule(self, improvement_id: str) -> Optional[ScheduledImprovement]:
        """Get schedule for an improvement."""
        return self.schedule.get(improvement_id)

    def update_status(
        self, improvement_id: str, status: ScheduleStatus
    ) -> bool:
        """Update schedule status."""
        if improvement_id in self.schedule:
            self.schedule[improvement_id].status = status
            return True
        return False

    def get_sprint_items(self, sprint_id: str) -> List[str]:
        """Get all items in a sprint."""
        return self.sprints.get(sprint_id, [])

    def get_overdue(self, current_date: str) -> List[ScheduledImprovement]:
        """Get overdue scheduled items."""
        overdue = []
        for item in self.schedule.values():
            if (item.status not in [ScheduleStatus.UNSCHEDULED] and
                    item.scheduled_end < current_date):
                item.status = ScheduleStatus.OVERDUE
                overdue.append(item)
        return overdue

    def check_resource_availability(
        self, resource: str, date: str
    ) -> bool:
        """Check if a resource is available on a date."""
        busy_dates = self.resources.get(resource, [])
        return date not in busy_dates


class ProgressDashboard:
    """Generates progress reports and dashboards for improvements.

    Tracks completion rates, velocity, and generates burndown data.

    Attributes:
        reports: List of generated reports.
    """

    def __init__(self) -> None:
        """Initialize the dashboard."""
        self.reports: List[ProgressReport] = []
        self.velocity_history: List[float] = []

    def generate_report(
        self, improvements: List[Improvement]
    ) -> ProgressReport:
        """Generate a progress report.

        Args:
            improvements: List of all improvements.

        Returns:
            ProgressReport with current metrics.
        """
        completed = len([i for i in improvements
                        if i.status == ImprovementStatus.COMPLETED])
        in_progress = len([i for i in improvements
                           if i.status == ImprovementStatus.IN_PROGRESS])
        blocked = len([i for i in improvements
                      if i.status == ImprovementStatus.DEFERRED])

        # Calculate velocity (avg completions per week)
        velocity = self._calculate_velocity()

        report = ProgressReport(
            report_date=datetime.now().isoformat()[:10],
            completed_count=completed,
            in_progress_count=in_progress,
            blocked_count=blocked,
            velocity=velocity
        )

        self.reports.append(report)
        return report

    def _calculate_velocity(self) -> float:
        """Calculate velocity from recent reports."""
        if len(self.reports) < 2:
            return 0.0
        recent = self.reports[-4:]  # Last 4 reports
        if len(recent) < 2:
            return 0.0
        completions = [
            recent[i].completed_count - recent[i - 1].completed_count
            for i in range(1, len(recent))
        ]
        return sum(completions) / len(completions) if completions else 0.0

    def generate_burndown(
        self, improvements: List[Improvement]
    ) -> List[Tuple[str, int]]:
        """Generate burndown chart data."""
        remaining = len([i for i in improvements
                        if i.status not in [ImprovementStatus.COMPLETED,
                                            ImprovementStatus.REJECTED]])
        return [(datetime.now().isoformat()[:10], remaining)]

    def get_completion_rate(
        self, improvements: List[Improvement]
    ) -> float:
        """Calculate completion rate."""
        total = len(improvements)
        if total == 0:
            return 0.0
        completed = len([i for i in improvements
                        if i.status == ImprovementStatus.COMPLETED])
        return (completed / total) * 100

    def export_dashboard(self, improvements: List[Improvement]) -> str:
        """Export dashboard as markdown."""
        report = self.generate_report(improvements)
        lines = [
            "# Improvements Dashboard",
            f"\nGenerated: {report.report_date}",
            "\n## Summary",
            f"- Completed: {report.completed_count}",
            f"- In Progress: {report.in_progress_count}",
            f"- Blocked: {report.blocked_count}",
            f"- Velocity: {report.velocity:.1f} per week",
            f"- Completion Rate: {self.get_completion_rate(improvements):.1f}%"
        ]
        return '\n'.join(lines)


class ImprovementValidator:
    """Validates improvements with automated testing.

    Runs validation rules and automated tests on improvements.

    Attributes:
        rules: List of validation rules.
    """

    def __init__(self) -> None:
        """Initialize the validator."""
        self.rules: List[Callable[[Improvement], Tuple[bool, str]]] = []
        self._setup_default_rules()

    def _setup_default_rules(self) -> None:
        """Set up default validation rules."""
        self.rules.append(self._rule_has_description)
        self.rules.append(self._rule_has_category)
        self.rules.append(self._rule_valid_effort)

    def _rule_has_description(
        self, imp: Improvement
    ) -> Tuple[bool, str]:
        """Check that improvement has a description."""
        if not imp.description or len(imp.description) < 10:
            return False, "Description too short or missing"
        return True, ""

    def _rule_has_category(
        self, imp: Improvement
    ) -> Tuple[bool, str]:
        """Check that improvement has a valid category."""
        if imp.category == ImprovementCategory.OTHER:
            return False, "Category should be more specific"
        return True, ""

    def _rule_valid_effort(
        self, imp: Improvement
    ) -> Tuple[bool, str]:
        """Check that effort estimate is reasonable."""
        return True, ""

    def add_rule(
        self, rule: Callable[[Improvement], Tuple[bool, str]]
    ) -> None:
        """Add a custom validation rule."""
        self.rules.append(rule)

    def validate(self, improvement: Improvement) -> ValidationResult:
        """Validate an improvement.

        Args:
            improvement: The improvement to validate.

        Returns:
            ValidationResult with issues found.
        """
        result = ValidationResult(improvement_id=improvement.id)

        for rule in self.rules:
            passed, message = rule(improvement)
            if not passed:
                result.is_valid = False
                result.issues.append((ValidationSeverity.ERROR, message))

        return result

    def validate_all(
        self, improvements: List[Improvement]
    ) -> List[ValidationResult]:
        """Validate multiple improvements."""
        return [self.validate(imp) for imp in improvements]


class RollbackTracker:
    """Tracks improvement rollbacks.

    Records when and why improvements are rolled back.

    Attributes:
        rollbacks: List of rollback records.
    """

    def __init__(self) -> None:
        """Initialize the rollback tracker."""
        self.rollbacks: List[RollbackRecord] = []
        self.states: Dict[str, str] = {}  # improvement_id -> previous state

    def save_state(self, improvement: Improvement) -> None:
        """Save the current state before an improvement.

        Args:
            improvement: The improvement being applied.
        """
        self.states[improvement.id] = json.dumps({
            "status": improvement.status.value,
            "updated_at": improvement.updated_at,
            "votes": improvement.votes
        })

    def record_rollback(
        self,
        improvement: Improvement,
        reason: str,
        commit_hash: str = ""
    ) -> RollbackRecord:
        """Record a rollback.

        Args:
            improvement: The rolled back improvement.
            reason: Why the rollback occurred.
            commit_hash: Git commit of the rollback.

        Returns:
            The rollback record.
        """
        record = RollbackRecord(
            improvement_id=improvement.id,
            rollback_date=datetime.now().isoformat(),
            reason=reason,
            previous_state=self.states.get(improvement.id, ""),
            rollback_commit=commit_hash
        )
        self.rollbacks.append(record)
        return record

    def get_rollbacks(
        self, improvement_id: Optional[str] = None
    ) -> List[RollbackRecord]:
        """Get rollback records."""
        if improvement_id:
            return [r for r in self.rollbacks
                    if r.improvement_id == improvement_id]
        return self.rollbacks

    def get_rollback_rate(self, total_completed: int) -> float:
        """Calculate rollback rate."""
        if total_completed == 0:
            return 0.0
        return (len(self.rollbacks) / total_completed) * 100


class ToolIntegration:
    """Integrates with code analysis tools for suggestions.

    Parses output from linters, type checkers, and other tools.

    Attributes:
        tool_configs: Configuration for each tool.
    """

    def __init__(self) -> None:
        """Initialize tool integration."""
        self.tool_configs: Dict[str, Dict[str, Any]] = {}
        self.suggestions: List[ToolSuggestion] = []

    def configure_tool(
        self,
        tool_name: str,
        tool_type: AnalysisToolType,
        command: str = ""
    ) -> None:
        """Configure a tool.

        Args:
            tool_name: Name of the tool (e.g., "pylint").
            tool_type: Type of the tool.
            command: Command to run the tool.
        """
        self.tool_configs[tool_name] = {
            "type": tool_type,
            "command": command
        }

    def parse_pylint_output(self, output: str) -> List[ToolSuggestion]:
        """Parse pylint output into suggestions."""
        suggestions = []
        for line in output.split('\n'):
            match = re.match(
                r'(.+):(\d+):\d+: (\w+): (.+)',
                line
            )
            if match:
                suggestions.append(ToolSuggestion(
                    tool_type=AnalysisToolType.LINTER,
                    tool_name="pylint",
                    file_path=match.group(1),
                    line_number=int(match.group(2)),
                    message=match.group(4)
                ))
        self.suggestions.extend(suggestions)
        return suggestions

    def parse_mypy_output(self, output: str) -> List[ToolSuggestion]:
        """Parse mypy output into suggestions."""
        suggestions = []
        for line in output.split('\n'):
            match = re.match(r'(.+):(\d+): error: (.+)', line)
            if match:
                suggestions.append(ToolSuggestion(
                    tool_type=AnalysisToolType.TYPE_CHECKER,
                    tool_name="mypy",
                    file_path=match.group(1),
                    line_number=int(match.group(2)),
                    message=match.group(3)
                ))
        self.suggestions.extend(suggestions)
        return suggestions

    def get_suggestions(
        self, tool_type: Optional[AnalysisToolType] = None
    ) -> List[ToolSuggestion]:
        """Get all tool suggestions."""
        if tool_type:
            return [s for s in self.suggestions
                    if s.tool_type == tool_type]
        return self.suggestions

    def convert_to_improvements(
        self, suggestions: List[ToolSuggestion]
    ) -> List[Dict[str, Any]]:
        """Convert tool suggestions to improvement data."""
        return [{
            "title": f"Fix {s.tool_name} issue in {s.file_path}",
            "description": s.message,
            "file_path": s.file_path,
            "line_number": s.line_number,
            "category": ImprovementCategory.MAINTAINABILITY.value
        } for s in suggestions]


class SLAManager:
    """Manages SLAs for improvements.

    Tracks SLA compliance and triggers escalations.

    Attributes:
        sla_configs: SLA configurations by level.
        tracked: Map of improvement IDs to SLA tracking data.
    """

    def __init__(self) -> None:
        """Initialize SLA manager."""
        self.sla_configs: Dict[SLALevel, SLAConfiguration] = {}
        self.tracked: Dict[str, Dict[str, Any]] = {}
        self._setup_default_slas()

    def _setup_default_slas(self) -> None:
        """Set up default SLA configurations."""
        defaults = [
            (SLALevel.P0, 24, 12),
            (SLALevel.P1, 72, 48),
            (SLALevel.P2, 168, 120),
            (SLALevel.P3, 336, 240),
            (SLALevel.P4, 720, 480),
        ]
        for level, max_h, esc_h in defaults:
            self.sla_configs[level] = SLAConfiguration(
                level=level,
                max_hours=max_h,
                escalation_hours=esc_h
            )

    def assign_sla(
        self, improvement: Improvement, level: SLALevel
    ) -> None:
        """Assign an SLA to an improvement.

        Args:
            improvement: The improvement to track.
            level: SLA priority level.
        """
        config = self.sla_configs.get(level)
        if not config:
            return

        self.tracked[improvement.id] = {
            "level": level,
            "start_time": datetime.now().isoformat(),
            "deadline": (datetime.now() +
                         timedelta(hours=config.max_hours)).isoformat(),
            "escalation_time": (datetime.now() +
                                timedelta(hours=config.escalation_hours)).isoformat()
        }

    def check_sla_status(
        self, improvement_id: str
    ) -> Dict[str, Any]:
        """Check SLA status for an improvement."""
        if improvement_id not in self.tracked:
            return {"status": "not_tracked"}

        tracking = self.tracked[improvement_id]
        now = datetime.now().isoformat()

        if now > tracking["deadline"]:
            return {"status": "breached", **tracking}
        elif now > tracking["escalation_time"]:
            return {"status": "escalation_needed", **tracking}
        else:
            return {"status": "on_track", **tracking}

    def get_breached(self) -> List[str]:
        """Get all breached improvement IDs."""
        now = datetime.now().isoformat()
        return [
            imp_id for imp_id, tracking in self.tracked.items()
            if now > tracking["deadline"]
        ]

    def get_sla_compliance_rate(self) -> float:
        """Calculate SLA compliance rate."""
        if not self.tracked:
            return 100.0
        breached = len(self.get_breached())
        return ((len(self.tracked) - breached) / len(self.tracked)) * 100


class MergeDetector:
    """Detects improvements that can be merged.

    Finds duplicate or similar improvements across files.

    Attributes:
        similarity_threshold: Threshold for considering items similar.
    """

    def __init__(self, similarity_threshold: float = 0.7) -> None:
        """Initialize merge detector."""
        self.similarity_threshold = similarity_threshold

    def find_similar(
        self, improvements: List[Improvement]
    ) -> List[MergeCandidate]:
        """Find similar improvements that could be merged.

        Args:
            improvements: List of improvements to analyze.

        Returns:
            List of merge candidates.
        """
        candidates = []
        for i, imp1 in enumerate(improvements):
            for imp2 in improvements[i + 1:]:
                similarity = self._calculate_similarity(imp1, imp2)
                if similarity >= self.similarity_threshold:
                    candidates.append(MergeCandidate(
                        source_id=imp1.id,
                        target_id=imp2.id,
                        similarity_score=similarity,
                        merge_reason=self._get_merge_reason(imp1, imp2)
                    ))
        return candidates

    def _calculate_similarity(
        self, imp1: Improvement, imp2: Improvement
    ) -> float:
        """Calculate similarity between two improvements."""
        score = 0.0

        # Title similarity
        title_words1 = set(imp1.title.lower().split())
        title_words2 = set(imp2.title.lower().split())
        if title_words1 and title_words2:
            title_overlap = len(title_words1 & title_words2)
            title_union = len(title_words1 | title_words2)
            score += (title_overlap / title_union) * 0.4

        # Category match
        if imp1.category == imp2.category:
            score += 0.3

        # File path similarity
        if imp1.file_path == imp2.file_path:
            score += 0.3

        return score

    def _get_merge_reason(
        self, imp1: Improvement, imp2: Improvement
    ) -> str:
        """Generate merge reason."""
        reasons = []
        if imp1.category == imp2.category:
            reasons.append(f"same category ({imp1.category.value})")
        if imp1.file_path == imp2.file_path:
            reasons.append("same file")
        return ", ".join(reasons) or "similar content"

    def merge(
        self, source: Improvement, target: Improvement
    ) -> Improvement:
        """Merge two improvements into one.

        Args:
            source: Source improvement.
            target: Target improvement (will be modified).

        Returns:
            The merged improvement.
        """
        # Combine descriptions
        target.description = f"{target.description}\n\nMerged from: {source.title}"

        # Take higher priority
        if source.priority.value > target.priority.value:
            target.priority = source.priority

        # Combine tags
        target.tags = list(set(target.tags + source.tags))

        # Add votes
        target.votes += source.votes

        return target


class ImprovementArchive:
    """Archives old or completed improvements.

    Maintains history of archived improvements.

    Attributes:
        archive: List of archived improvements.
    """

    def __init__(self) -> None:
        """Initialize the archive."""
        self.archive: List[ArchivedImprovement] = []

    def archive_improvement(
        self,
        improvement: Improvement,
        reason: str,
        archived_by: str = ""
    ) -> ArchivedImprovement:
        """Archive an improvement.

        Args:
            improvement: The improvement to archive.
            reason: Why it's being archived.
            archived_by: Who archived it.

        Returns:
            The archived improvement record.
        """
        archived = ArchivedImprovement(
            improvement=improvement,
            archived_date=datetime.now().isoformat(),
            archived_by=archived_by,
            archive_reason=reason
        )
        self.archive.append(archived)
        return archived

    def restore(self, improvement_id: str) -> Optional[Improvement]:
        """Restore an archived improvement.

        Args:
            improvement_id: ID of the improvement to restore.

        Returns:
            The restored improvement or None.
        """
        for i, archived in enumerate(self.archive):
            if archived.improvement.id == improvement_id:
                imp = archived.improvement
                del self.archive[i]
                return imp
        return None

    def search_archive(
        self,
        query: str = "",
        category: Optional[ImprovementCategory] = None
    ) -> List[ArchivedImprovement]:
        """Search the archive.

        Args:
            query: Text to search for.
            category: Filter by category.

        Returns:
            Matching archived improvements.
        """
        results = []
        for archived in self.archive:
            imp = archived.improvement
            if category and imp.category != category:
                continue
            if query and query.lower() not in imp.title.lower():
                continue
            results.append(archived)
        return results

    def get_archive_stats(self) -> Dict[str, Any]:
        """Get archive statistics."""
        by_category: Dict[str, int] = {}
        for archived in self.archive:
            cat = archived.improvement.category.value
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_archived": len(self.archive),
            "by_category": by_category
        }


# =============================================================================
# Session 8 Enums
# =============================================================================


class BranchComparisonStatus(Enum):
    """Status of branch comparison."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ImprovementDiffType(Enum):
    """Types of improvement differences between branches."""
    ADDED = "added"      # Improvement exists only in target branch
    REMOVED = "removed"  # Improvement exists only in source branch
    MODIFIED = "modified"  # Improvement exists in both but changed
    UNCHANGED = "unchanged"  # Improvement is identical in both


# =============================================================================
# Session 8 Dataclasses
# =============================================================================


@dataclass
class BranchComparison:
    """Result of comparing improvements across branches.

    Attributes:
        source_branch: Source branch name.
        target_branch: Target branch name.
        file_path: Path to improvements file.
        status: Comparison status.
        diffs: List of improvement differences.
        added_count: Number of improvements added.
        removed_count: Number of improvements removed.
        modified_count: Number of improvements modified.
        compared_at: Comparison timestamp.
    """
    source_branch: str
    target_branch: str
    file_path: str
    status: BranchComparisonStatus = BranchComparisonStatus.PENDING
    diffs: List[ImprovementDiff] = field(default_factory=list)  # type: ignore[assignment]
    added_count: int = 0
    removed_count: int = 0
    modified_count: int = 0
    compared_at: float = field(default_factory=time.time)


@dataclass
class ConflictResolution:
    """Resolution for a conflicting improvement.

    Attributes:
        improvement_id: ID of conflicting improvement.
        resolution: Resolved improvement version.
        strategy: Resolution strategy used.
        resolved_by: Who resolved the conflict.
    """
    improvement_id: str
    resolution: Improvement
    strategy: str = "manual"
    resolved_by: str = ""


# =============================================================================
# Session 8 Helper Classes
# =============================================================================


class BranchComparer:
    """Comparer for improvements across git branches.

    Enables comparison of improvement files between branches
    to identify additions, removals, and modifications.

    Attributes:
        repo_path: Path to git repository.
        comparisons: History of comparisons.

    Example:
        comparer=BranchComparer("/path / to / repo")
        result=comparer.compare("main", "feature / improvements")
        for diff in result.diffs:
            print(f"{diff.diff_type.value}: {diff.improvement_id}")
    """

    def __init__(self, repo_path: Optional[str] = None) -> None:
        """Initialize branch comparer.

        Args:
            repo_path: Path to git repository. Defaults to current directory.
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()
        self.comparisons: List[BranchComparison] = []
        logging.debug(f"BranchComparer initialized for {self.repo_path}")

    def compare(
        self,
        source_branch: str,
        target_branch: str,
        file_path: str
    ) -> BranchComparison:
        """Compare improvements between branches.

        Args:
            source_branch: Source branch name.
            target_branch: Target branch name.
            file_path: Path to improvements file.

        Returns:
            Comparison result with diffs.
        """
        comparison = BranchComparison(
            source_branch=source_branch,
            target_branch=target_branch,
            file_path=file_path,
            status=BranchComparisonStatus.IN_PROGRESS
        )

        try:
            # Get file content from each branch
            source_content = self._get_file_from_branch(source_branch, file_path)
            target_content = self._get_file_from_branch(target_branch, file_path)

            # Parse improvements from each branch
            source_improvements = self._parse_improvements(source_content)
            target_improvements = self._parse_improvements(target_content)

            # Calculate differences
            comparison.diffs = self._calculate_diffs(
                source_improvements, target_improvements
            )

            # Count by type
            comparison.added_count = sum(
                1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.ADDED
            )
            comparison.removed_count = sum(
                1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.REMOVED
            )
            comparison.modified_count = sum(
                1 for d in comparison.diffs if d.diff_type == ImprovementDiffType.MODIFIED
            )

            comparison.status = BranchComparisonStatus.COMPLETED

        except Exception as e:
            logging.error(f"Branch comparison failed: {e}")
            comparison.status = BranchComparisonStatus.FAILED

        self.comparisons.append(comparison)
        return comparison

    def _get_file_from_branch(self, branch: str, file_path: str) -> str:
        """Get file content from a specific branch.

        Args:
            branch: Branch name.
            file_path: Path to file.

        Returns:
            File content string.
        """
        try:
            result = subprocess.run(
                ["git", "show", f"{branch}:{file_path}"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    def _parse_improvements(self, content: str) -> Dict[str, Improvement]:
        """Parse improvements from markdown content.

        Args:
            content: Markdown content with improvements.

        Returns:
            Dictionary mapping improvement IDs to Improvement objects.
        """
        improvements: Dict[str, Improvement] = {}

        # Parse improvement items from markdown
        pattern = r'- \[[ x]\] (.+?)(?=\n- \[|\n##|\Z)'
        matches = re.findall(pattern, content, re.DOTALL)

        for i, match in enumerate(matches):
            title = match.strip().split('\n')[0]
            improvement_id = f"imp_{i}_{hashlib.md5(title.encode()).hexdigest()[:8]}"

            improvements[improvement_id] = Improvement(
                id=improvement_id,
                title=title,
                description=match.strip(),
                file_path=""
            )

        return improvements

    def _calculate_diffs(
        self,
        source: Dict[str, Improvement],
        target: Dict[str, Improvement]
    ) -> List[ImprovementDiff]:
        """Calculate differences between two improvement sets.

        Args:
            source: Source branch improvements.
            target: Target branch improvements.

        Returns:
            List of improvement differences.
        """
        diffs: List[ImprovementDiff] = []
        all_ids = set(source.keys()) | set(target.keys())

        for imp_id in all_ids:
            in_source = imp_id in source
            in_target = imp_id in target

            if in_source and not in_target:
                diffs.append(ImprovementDiff(
                    improvement_id=imp_id,
                    diff_type=ImprovementDiffType.REMOVED,
                    source_version=source[imp_id],
                    change_summary="Improvement removed in target branch"
                ))
            elif in_target and not in_source:
                diffs.append(ImprovementDiff(
                    improvement_id=imp_id,
                    diff_type=ImprovementDiffType.ADDED,
                    target_version=target[imp_id],
                    change_summary="New improvement in target branch"
                ))
            elif source[imp_id].title != target[imp_id].title:
                diffs.append(ImprovementDiff(
                    improvement_id=imp_id,
                    diff_type=ImprovementDiffType.MODIFIED,
                    source_version=source[imp_id],
                    target_version=target[imp_id],
                    change_summary="Improvement title or content changed"
                ))
            else:
                diffs.append(ImprovementDiff(
                    improvement_id=imp_id,
                    diff_type=ImprovementDiffType.UNCHANGED,
                    source_version=source[imp_id],
                    target_version=target[imp_id],
                    change_summary="No changes"
                ))

        return diffs

    def get_added_improvements(
        self,
        comparison: BranchComparison
    ) -> List[Improvement]:
        """Get improvements added in target branch.

        Args:
            comparison: Comparison result.

        Returns:
            List of added improvements.
        """
        return [
            d.target_version for d in comparison.diffs
            if d.diff_type == ImprovementDiffType.ADDED and d.target_version
        ]

    def get_removed_improvements(
        self,
        comparison: BranchComparison
    ) -> List[Improvement]:
        """Get improvements removed in target branch.

        Args:
            comparison: Comparison result.

        Returns:
            List of removed improvements.
        """
        return [
            d.source_version for d in comparison.diffs
            if d.diff_type == ImprovementDiffType.REMOVED and d.source_version
        ]

    def get_modified_improvements(
        self,
        comparison: BranchComparison
    ) -> List[Tuple[Improvement, Improvement]]:
        """Get improvements modified between branches.

        Args:
            comparison: Comparison result.

        Returns:
            List of (source, target) improvement tuples.
        """
        return [
            (d.source_version, d.target_version)
            for d in comparison.diffs
            if d.diff_type == ImprovementDiffType.MODIFIED
            and d.source_version and d.target_version
        ]

    def detect_conflicts(
        self,
        base_branch: str,
        branch1: str,
        branch2: str,
        file_path: str
    ) -> List[ImprovementDiff]:
        """Detect conflicting changes in a three-way comparison.

        Args:
            base_branch: Common ancestor branch.
            branch1: First branch.
            branch2: Second branch.
            file_path: Path to improvements file.

        Returns:
            List of conflicting improvement diffs.
        """
        comp1 = self.compare(base_branch, branch1, file_path)
        comp2 = self.compare(base_branch, branch2, file_path)

        # Find improvements modified in both branches
        modified1 = {
            d.improvement_id for d in comp1.diffs
            if d.diff_type == ImprovementDiffType.MODIFIED
        }
        modified2 = {
            d.improvement_id for d in comp2.diffs
            if d.diff_type == ImprovementDiffType.MODIFIED
        }

        conflicts = modified1 & modified2
        return [
            d for d in comp1.diffs
            if d.improvement_id in conflicts
        ]

    def generate_merge_report(
        self,
        comparison: BranchComparison
    ) -> str:
        """Generate a markdown merge report.

        Args:
            comparison: Comparison result.

        Returns:
            Markdown formatted report.
        """
        lines = [
            "# Branch Comparison Report",
            "",
            f"**Source Branch:** {comparison.source_branch}",
            f"**Target Branch:** {comparison.target_branch}",
            f"**File:** {comparison.file_path}",
            "",
            "## Summary",
            f"- Added: {comparison.added_count}",
            f"- Removed: {comparison.removed_count}",
            f"- Modified: {comparison.modified_count}",
            "",
            "## Changes",
        ]

        for diff in comparison.diffs:
            if diff.diff_type == ImprovementDiffType.UNCHANGED:
                continue

            emoji = {
                ImprovementDiffType.ADDED: "➕",
                ImprovementDiffType.REMOVED: "➖",
                ImprovementDiffType.MODIFIED: "📝"
            }.get(diff.diff_type, "•")

            title = (
                diff.target_version.title if diff.target_version
                else diff.source_version.title if diff.source_version
                else diff.improvement_id
            )
            lines.append(f"- {emoji} {title}")

        return "\n".join(lines)

    def get_comparison_history(self) -> List[BranchComparison]:
        """Get history of comparisons.

        Returns:
            List of past comparisons.
        """
        return list(self.comparisons)

    def clear_history(self) -> None:
        """Clear comparison history."""
        self.comparisons.clear()


class ImprovementsAgent(BaseAgent):
    """Updates code file improvement suggestions using AI assistance.

    This agent reads .improvements.md files and uses AI to suggest better,
    more actionable improvements for the associated code file.
    """

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._validate_file_extension()
        self._check_associated_file()

        # Improvement management
        self._improvements: List[Improvement] = []
        self._templates: Dict[str, ImprovementTemplate] = {
            t.name: t for t in DEFAULT_TEMPLATES
        }
        self._analytics: Dict[str, Any] = {}

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.improvements.md'):
            logging.warning(f"File {self.file_path.name} does not end with .improvements.md")

    def _check_associated_file(self) -> None:
        """Check if the associated code file exists."""
        name = self.file_path.name
        if name.endswith('.improvements.md'):
            base_name = name[:-16]  # len('.improvements.md')
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

    # ========== Improvement Management ==========

    def add_improvement(
        self,
        title: str,
        description: str,
        file_path: str = "",
        priority: ImprovementPriority = ImprovementPriority.MEDIUM,
        category: ImprovementCategory = ImprovementCategory.OTHER,
        effort: EffortEstimate = EffortEstimate.MEDIUM,
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None
    ) -> Improvement:
        """Add a new improvement."""
        improvement_id = hashlib.md5(
            f"{title}:{file_path}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:8]

        improvement = Improvement(
            id=improvement_id,
            title=title,
            description=description,
            file_path=file_path or str(self.file_path),
            priority=priority,
            category=category,
            effort=effort,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            tags=tags or [],
            dependencies=dependencies or []
        )

        self._improvements.append(improvement)
        return improvement

    def get_improvements(self) -> List[Improvement]:
        """Get all improvements."""
        return self._improvements

    def get_improvement_by_id(self, improvement_id: str) -> Optional[Improvement]:
        """Get an improvement by ID."""
        return next((i for i in self._improvements if i.id == improvement_id), None)

    def update_status(
        self,
        improvement_id: str,
        status: ImprovementStatus
    ) -> bool:
        """Update the status of an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.status = status
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_improvements_by_status(
        self,
        status: ImprovementStatus
    ) -> List[Improvement]:
        """Get improvements filtered by status."""
        return [i for i in self._improvements if i.status == status]

    def get_improvements_by_category(
        self,
        category: ImprovementCategory
    ) -> List[Improvement]:
        """Get improvements filtered by category."""
        return [i for i in self._improvements if i.category == category]

    def get_improvements_by_priority(
        self,
        priority: ImprovementPriority
    ) -> List[Improvement]:
        """Get improvements filtered by priority."""
        return [i for i in self._improvements if i.priority == priority]

    # ========== Impact Scoring ==========

    def calculate_impact_score(self, improvement: Improvement) -> float:
        """Calculate impact score for an improvement."""
        score = improvement.priority.value * 20

        # Adjust based on category
        category_weights = {
            ImprovementCategory.SECURITY: 20,
            ImprovementCategory.PERFORMANCE: 15,
            ImprovementCategory.BUG_FIX: 15,
            ImprovementCategory.TESTING: 10,
            ImprovementCategory.MAINTAINABILITY: 10,
            ImprovementCategory.DOCUMENTATION: 5,
        }
        score += category_weights.get(improvement.category, 0)

        # Consider votes
        score += min(improvement.votes * 2, 20)

        # Reduce score for items with many dependencies
        score -= len(improvement.dependencies) * 5

        return max(0, min(100, score))

    def prioritize_improvements(self) -> List[Improvement]:
        """Return improvements sorted by impact score."""
        for imp in self._improvements:
            imp.impact_score = self.calculate_impact_score(imp)

        return sorted(
            self._improvements,
            key=lambda i: (i.impact_score, i.priority.value),
            reverse=True
        )

    # ========== Effort Estimation ==========

    def estimate_total_effort(self) -> Dict[str, Any]:
        """Estimate total effort for all improvements."""
        # Effort in hours
        effort_hours = {
            EffortEstimate.TRIVIAL: 1,
            EffortEstimate.SMALL: 3,
            EffortEstimate.MEDIUM: 12,
            EffortEstimate.LARGE: 32,
            EffortEstimate.EPIC: 80,
        }

        total = 0
        by_category: Dict[str, int] = {}

        for imp in self._improvements:
            if imp.status not in [ImprovementStatus.COMPLETED, ImprovementStatus.REJECTED]:
                hours = effort_hours.get(imp.effort, 12)
                total += hours
                cat_name = imp.category.name
                by_category[cat_name] = by_category.get(cat_name, 0) + hours

        return {
            "total_hours": total,
            "by_category": by_category,
            "estimated_days": total / 8,
            "estimated_weeks": total / 40
        }

    # ========== Dependencies ==========

    def add_dependency(
        self,
        improvement_id: str,
        depends_on_id: str
    ) -> bool:
        """Add a dependency between improvements."""
        improvement = self.get_improvement_by_id(improvement_id)
        depends_on = self.get_improvement_by_id(depends_on_id)

        if improvement and depends_on and depends_on_id not in improvement.dependencies:
            improvement.dependencies.append(depends_on_id)
            return True
        return False

    def get_dependencies(self, improvement_id: str) -> List[Improvement]:
        """Get all dependencies for an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if not improvement:
            return []

        dependencies: List[Improvement] = []
        for dep_id in improvement.dependencies:
            dep = self.get_improvement_by_id(dep_id)
            if dep is not None:
                dependencies.append(dep)
        return dependencies

    def get_dependents(self, improvement_id: str) -> List[Improvement]:
        """Get all improvements that depend on this one."""
        return [
            i for i in self._improvements
            if improvement_id in i.dependencies
        ]

    def get_ready_to_implement(self) -> List[Improvement]:
        """Get improvements that have all dependencies satisfied."""
        ready: List[Improvement] = []
        for imp in self._improvements:
            if imp.status == ImprovementStatus.SUGGESTED:
                deps_satisfied = all(
                    (dep := self.get_improvement_by_id(dep_id)) is not None and
                    dep.status == ImprovementStatus.COMPLETED
                    for dep_id in imp.dependencies
                )
                if deps_satisfied or not imp.dependencies:
                    ready.append(imp)
        return ready

    # ========== Templates ==========

    def add_template(self, template: ImprovementTemplate) -> None:
        """Add a custom template."""
        self._templates[template.name] = template

    def get_templates(self) -> Dict[str, ImprovementTemplate]:
        """Get all templates."""
        return self._templates

    def create_from_template(
        self,
        template_name: str,
        variables: Dict[str, str],
        file_path: str = ""
    ) -> Optional[Improvement]:
        """Create an improvement from a template."""
        template = self._templates.get(template_name)
        if not template:
            return None

        title = template.title_pattern.format(**variables)
        description = template.description_template.format(**variables)

        return self.add_improvement(
            title=title,
            description=description,
            file_path=file_path,
            priority=template.default_priority,
            category=template.category,
            effort=template.default_effort
        )

    # ========== Voting ==========

    def vote(self, improvement_id: str, vote: int = 1) -> bool:
        """Vote for an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.votes += vote
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_top_voted(self, limit: int = 10) -> List[Improvement]:
        """Get top voted improvements."""
        return sorted(
            self._improvements,
            key=lambda i: i.votes,
            reverse=True
        )[:limit]

    # ========== Assignment ==========

    def assign(self, improvement_id: str, assignee: str) -> bool:
        """Assign an improvement to someone."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.assignee = assignee
            improvement.updated_at = datetime.now().isoformat()
            if improvement.status == ImprovementStatus.SUGGESTED:
                improvement.status = ImprovementStatus.IN_PROGRESS
            return True
        return False

    def unassign(self, improvement_id: str) -> bool:
        """Unassign an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.assignee = ""
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_by_assignee(self, assignee: str) -> List[Improvement]:
        """Get improvements assigned to a specific person."""
        return [i for i in self._improvements if i.assignee == assignee]

    def approve_improvement(self, improvement_id: str) -> bool:
        """Approve an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.status = ImprovementStatus.APPROVED
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def reject_improvement(self, improvement_id: str, reason: str = "") -> bool:
        """Reject an improvement."""
        improvement = self.get_improvement_by_id(improvement_id)
        if improvement:
            improvement.status = ImprovementStatus.REJECTED
            improvement.updated_at = datetime.now().isoformat()
            return True
        return False

    def get_assigned_to(self, assignee: str) -> List[Improvement]:
        """Get improvements assigned to a specific person."""
        return [i for i in self._improvements if i.assignee == assignee]

    # ========== Analytics ==========

    def calculate_analytics(self) -> Dict[str, Any]:
        """Calculate analytics for improvements."""
        total = len(self._improvements)
        if total == 0:
            return {"total": 0}

        by_status: Dict[str, int] = {}
        for status in ImprovementStatus:
            by_status[status.name] = len(self.get_improvements_by_status(status))

        by_category: Dict[str, int] = {}
        for category in ImprovementCategory:
            by_category[category.name] = len(self.get_improvements_by_category(category))

        by_priority: Dict[str, int] = {}
        for priority in ImprovementPriority:
            by_priority[priority.name] = len(self.get_improvements_by_priority(priority))

        completed = by_status.get("COMPLETED", 0)
        completion_rate = (completed / total * 100) if total > 0 else 0

        effort = self.estimate_total_effort()

        self._analytics = {
            "total": total,
            "by_status": by_status,
            "by_category": by_category,
            "by_priority": by_priority,
            "completion_rate": completion_rate,
            "effort_estimation": effort,
            "avg_votes": sum(i.votes for i in self._improvements) / total,
        }

        return self._analytics

    # ========== Export ==========

    def export_improvements(self, format: str = "json") -> str:
        """Export improvements to various formats."""
        if format == "json":
            data = [{
                "id": i.id,
                "title": i.title,
                "description": i.description,
                "priority": i.priority.name,
                "category": i.category.name,
                "status": i.status.name,
                "effort": i.effort.name,
                "impact_score": i.impact_score,
                "votes": i.votes,
                "assignee": i.assignee,
                "dependencies": i.dependencies,
                "tags": i.tags
            } for i in self._improvements]
            return json.dumps(data, indent=2)
        elif format == "markdown":
            lines = ["# Improvements\n"]
            for priority in ImprovementPriority:
                imps = self.get_improvements_by_priority(priority)
                if imps:
                    lines.append(f"\n## {priority.name}\n")
                    for i in imps:
                        status_icon = "✓" if i.status == ImprovementStatus.COMPLETED else "○"
                        lines.append(f"- [{status_icon}] **{i.title}** ({i.category.value})")
                        lines.append(f"  - {i.description}")
            return '\n'.join(lines)
        return ""

    # ========== Documentation Generation ==========

    def generate_documentation(self) -> str:
        """Generate documentation for all improvements."""
        analytics = self.calculate_analytics()

        docs = ["# Improvement Documentation\n"]
        docs.append("## Summary\n")
        docs.append(f"- Total Improvements: {analytics['total']}")
        docs.append(f"- Completion Rate: {analytics['completion_rate']:.1f}%")
        docs.append(
            f"- Total Effort: {analytics['effort_estimation']['estimated_days']:.1f} days\n")

        docs.append("## By Status\n")
        for status, count in analytics['by_status'].items():
            if count > 0:
                docs.append(f"- {status}: {count}")

        docs.append("\n## Prioritized List\n")
        for imp in self.prioritize_improvements()[:10]:
            docs.append(f"- [{imp.priority.name}] {imp.title} (Score: {imp.impact_score:.1f})")

        return '\n'.join(docs)

    # ========== Core Methods ==========

    def _get_default_content(self) -> str:
        """Return default content for new improvement files."""
        return "# Improvements\n\nNo improvements suggested.\n"

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original suggestions preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the improvement suggestions.

        When Copilot CLI is unavailable, BaseAgent keeps the existing content
        unchanged (avoids duplicated wrapper sections).
        """
        logging.info(f"Improving suggestions for {self.file_path}")
        # Add guidance for structured output
        enhanced_prompt = (
            f"{prompt}\n\n"
            "Please format the improvements as a markdown list with "
            "checkboxes for actionable items:\n"
            "- [ ] Actionable item 1\n"
            "- [ ] Actionable item 2\n\n"
            "Group improvements by priority (High, Medium, Low) if applicable."
        )
        return super().improve_content(enhanced_prompt)


# ========== Missing Classes (Session continuation) ==========

class ImpactScorer:
    """Scores improvements based on impact metrics."""
    def __init__(self) -> None:
        self.scores: Dict[str, float] = {}
    
    def score(self, improvement: Improvement) -> float:
        """Score an improvement."""
        score = improvement.priority.value * 20
        if improvement.category == ImprovementCategory.SECURITY:
            score += 30
        elif improvement.category == ImprovementCategory.PERFORMANCE:
            score += 25
        else:
            score += 10
        return min(100, max(0, score))


class DependencyResolver:
    """Resolves improvement dependencies."""
    def __init__(self) -> None:
        self.graph: Dict[str, List[str]] = {}
    
    def add_dependency(self, source: str, target: str) -> None:
        """Add a dependency edge."""
        if source not in self.graph:
            self.graph[source] = []
        self.graph[source].append(target)
    
    def resolve_order(self) -> List[str]:
        """Resolve dependency order using topological sort."""
        visited = set()
        stack = []
        
        def visit(node: str) -> None:
            if node not in visited:
                visited.add(node)
                for dep in self.graph.get(node, []):
                    visit(dep)
                stack.append(node)
        
        for node in self.graph:
            visit(node)
        
        return stack


class EffortEstimator:
    """Estimates effort for improvements."""
    def __init__(self) -> None:
        self.historical_data: Dict[str, List[float]] = {}
    
    def estimate(self, improvement: Improvement) -> int:
        """Estimate effort in hours."""
        effort_map = {
            EffortEstimate.TRIVIAL: 1,
            EffortEstimate.SMALL: 3,
            EffortEstimate.MEDIUM: 12,
            EffortEstimate.LARGE: 32,
            EffortEstimate.EPIC: 80
        }
        return effort_map.get(improvement.effort, 12)


class WorkflowEngine:
    """Manages improvement workflow transitions."""
    def __init__(self) -> None:
        self.transitions: Dict[str, List[str]] = {}
        self._setup_default_transitions()
    
    def _setup_default_transitions(self) -> None:
        """Setup default state transitions."""
        self.transitions = {
            "PROPOSED": ["SUGGESTED", "REJECTED"],
            "SUGGESTED": ["APPROVED", "REJECTED"],
            "APPROVED": ["IN_PROGRESS"],
            "IN_PROGRESS": ["COMPLETED", "DEFERRED"],
            "COMPLETED": [],
            "REJECTED": [],
            "DEFERRED": ["IN_PROGRESS"]
        }
    
    def can_transition(self, from_status: str, to_status: str) -> bool:
        """Check if transition is allowed."""
        return to_status in self.transitions.get(from_status, [])


class VotingSystem:
    """Manages voting on improvements."""
    def __init__(self) -> None:
        self.votes: Dict[str, List[str]] = {}
    
    def cast_vote(self, improvement_id: str, voter: str) -> bool:
        """Cast a vote for an improvement."""
        if improvement_id not in self.votes:
            self.votes[improvement_id] = []
        if voter not in self.votes[improvement_id]:
            self.votes[improvement_id].append(voter)
            return True
        return False
    
    def get_vote_count(self, improvement_id: str) -> int:
        """Get vote count for improvement."""
        return len(self.votes.get(improvement_id, []))


# Create main function using the helper
main = create_main_function(
    ImprovementsAgent,
    'Improvements Agent: Updates code file improvement suggestions',
    'Path to the improvements file (e.g., file.improvements.md)'
)

if __name__ == '__main__':
    main()
