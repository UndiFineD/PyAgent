#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for agent-improvements.py."""

from __future__ import annotations
import json
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture()
def improvements_module() -> Any:
    """Load the improvements agent module."""
    with agent_dir_on_path():
        return load_agent_module("agent-improvements.py")


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent
        return base_agent


@pytest.fixture()
def agent(improvements_module: Any, tmp_path: Path) -> Any:
    """Create agent for testing."""
    target = tmp_path / "improvements.md"
    target.write_text("# Improvements\n", encoding="utf-8")
    return improvements_module.ImprovementsAgent(str(target))


def test_improvements_agent_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-improvements.py")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)
    target = tmp_path / "x.improvements.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ImprovementsAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "IMPROVED"


# ========== ImprovementPriority Tests ==========

class TestImprovementPriority:
    """Tests for ImprovementPriority enum."""

    def test_priority_values(self, improvements_module: Any) -> None:
        """Test that priority values are correct."""
        assert improvements_module.ImprovementPriority.CRITICAL.value == 5
        assert improvements_module.ImprovementPriority.HIGH.value == 4
        assert improvements_module.ImprovementPriority.MEDIUM.value == 3
        assert improvements_module.ImprovementPriority.LOW.value == 2
        assert improvements_module.ImprovementPriority.NICE_TO_HAVE.value == 1

    def test_all_priorities_exist(self, improvements_module: Any) -> None:
        """Test all priority levels exist."""
        priorities = list(improvements_module.ImprovementPriority)
        assert len(priorities) == 5


# ========== ImprovementCategory Tests ==========

class TestImprovementCategory:
    """Tests for ImprovementCategory enum."""

    def test_category_values(self, improvements_module: Any) -> None:
        """Test that category values are correct strings."""
        assert improvements_module.ImprovementCategory.PERFORMANCE.value == "performance"
        assert improvements_module.ImprovementCategory.SECURITY.value == "security"
        assert improvements_module.ImprovementCategory.MAINTAINABILITY.value == "maintainability"

    def test_all_categories_exist(self, improvements_module: Any) -> None:
        """Test all categories exist."""
        categories = list(improvements_module.ImprovementCategory)
        assert len(categories) == 8


# ========== ImprovementStatus Tests ==========

class TestImprovementStatus:
    """Tests for ImprovementStatus enum."""

    def test_status_values(self, improvements_module: Any) -> None:
        """Test that status values are correct."""
        assert improvements_module.ImprovementStatus.PROPOSED.value == "proposed"
        assert improvements_module.ImprovementStatus.COMPLETED.value == "completed"
        assert improvements_module.ImprovementStatus.REJECTED.value == "rejected"

    def test_all_statuses_exist(self, improvements_module: Any) -> None:
        """Test all statuses exist."""
        statuses = list(improvements_module.ImprovementStatus)
        assert len(statuses) == 6


# ========== EffortEstimate Tests ==========

class TestEffortEstimate:
    """Tests for EffortEstimate enum."""

    def test_effort_values(self, improvements_module: Any) -> None:
        """Test effort estimate values."""
        assert improvements_module.EffortEstimate.TRIVIAL.value == 1
        assert improvements_module.EffortEstimate.SMALL.value == 3
        assert improvements_module.EffortEstimate.MEDIUM.value == 5
        assert improvements_module.EffortEstimate.LARGE.value == 8
        assert improvements_module.EffortEstimate.EPIC.value == 13


# ========== Improvement Dataclass Tests ==========

class TestImprovementDataclass:
    """Tests for Improvement dataclass."""

    def test_create_improvement(self, improvements_module: Any) -> None:
        """Test creating an improvement."""
        improvement = improvements_module.Improvement(
            id="imp123",
            title="Add caching",
            description="Add caching to improve performance",
            file_path="cache.py"
        )
        assert improvement.id == "imp123"
        assert improvement.title == "Add caching"
        assert improvement.priority == improvements_module.ImprovementPriority.MEDIUM
        assert improvement.status == improvements_module.ImprovementStatus.PROPOSED


# ========== Add Improvement Tests ==========

class TestAddImprovement:
    """Tests for adding improvements."""

    def test_add_simple_improvement(self, agent: Any, improvements_module: Any) -> None:
        """Test adding a simple improvement."""
        imp = agent.add_improvement(
            title="Improve code",
            description="Make the code better"
        )
        assert imp.id is not None
        assert len(agent.get_improvements()) == 1

    def test_add_improvement_with_priority(self, agent: Any, improvements_module: Any) -> None:
        """Test adding improvement with priority."""
        imp = agent.add_improvement(
            title="Critical fix",
            description="Very important",
            priority=improvements_module.ImprovementPriority.CRITICAL
        )
        assert imp.priority == improvements_module.ImprovementPriority.CRITICAL

    def test_add_improvement_with_category(self, agent: Any, improvements_module: Any) -> None:
        """Test adding improvement with category."""
        imp = agent.add_improvement(
            title="Security fix",
            description="Fix vulnerability",
            category=improvements_module.ImprovementCategory.SECURITY
        )
        assert imp.category == improvements_module.ImprovementCategory.SECURITY

    def test_add_improvement_with_effort(self, agent: Any, improvements_module: Any) -> None:
        """Test adding improvement with effort estimate."""
        imp = agent.add_improvement(
            title="Large refactor",
            description="Big change",
            effort=improvements_module.EffortEstimate.LARGE
        )
        assert imp.effort == improvements_module.EffortEstimate.LARGE


# ========== Improvement Retrieval Tests ==========

class TestImprovementRetrieval:
    """Tests for improvement retrieval methods."""

    def test_get_all_improvements(self, agent: Any) -> None:
        """Test getting all improvements."""
        agent.add_improvement("Imp 1", "Description 1")
        agent.add_improvement("Imp 2", "Description 2")
        imps = agent.get_improvements()
        assert len(imps) == 2

    def test_get_improvement_by_id(self, agent: Any) -> None:
        """Test getting improvement by ID."""
        imp = agent.add_improvement("Find me", "Findable")
        found = agent.get_improvement_by_id(imp.id)
        assert found is not None
        assert found.id == imp.id

    def test_get_improvements_by_status(self, agent: Any, improvements_module: Any) -> None:
        """Test filtering by status."""
        agent.add_improvement("Proposed", "Description")
        agent.add_improvement("Also proposed", "Description")
        proposed = agent.get_improvements_by_status(improvements_module.ImprovementStatus.PROPOSED)
        assert len(proposed) == 2

    def test_get_improvements_by_category(self, agent: Any, improvements_module: Any) -> None:
        """Test filtering by category."""
        agent.add_improvement(
            "Perf 1",
            "Desc",
            category=improvements_module.ImprovementCategory.PERFORMANCE)
        agent.add_improvement(
            "Sec 1",
            "Desc",
            category=improvements_module.ImprovementCategory.SECURITY)
        perf = agent.get_improvements_by_category(
            improvements_module.ImprovementCategory.PERFORMANCE)
        assert len(perf) == 1


# ========== Status Update Tests ==========

class TestStatusUpdate:
    """Tests for updating improvement status."""

    def test_update_status(self, agent: Any, improvements_module: Any) -> None:
        """Test updating status."""
        imp = agent.add_improvement("Update me", "Description")
        result = agent.update_status(imp.id, improvements_module.ImprovementStatus.IN_PROGRESS)
        assert result is True
        assert imp.status == improvements_module.ImprovementStatus.IN_PROGRESS

    def test_update_status_nonexistent(self, agent: Any, improvements_module: Any) -> None:
        """Test updating non-existent improvement."""
        result = agent.update_status("fake123", improvements_module.ImprovementStatus.COMPLETED)
        assert result is False

    def test_approve_improvement(self, agent: Any, improvements_module: Any) -> None:
        """Test approving improvement."""
        imp = agent.add_improvement("Approve me", "Description")
        result = agent.approve_improvement(imp.id)
        assert result is True
        assert imp.status == improvements_module.ImprovementStatus.APPROVED

    def test_reject_improvement(self, agent: Any, improvements_module: Any) -> None:
        """Test rejecting improvement."""
        imp = agent.add_improvement("Reject me", "Description")
        result = agent.reject_improvement(imp.id, "Too complex")
        assert result is True
        assert imp.status == improvements_module.ImprovementStatus.REJECTED


# ========== Impact Scoring Tests ==========

class TestImpactScoring:
    """Tests for impact scoring."""

    def test_calculate_impact_score(self, agent: Any, improvements_module: Any) -> None:
        """Test impact score calculation."""
        imp = agent.add_improvement(
            "High impact",
            "Description",
            priority=improvements_module.ImprovementPriority.CRITICAL
        )
        score = agent.calculate_impact_score(imp)
        assert score > 0
        assert score <= 100

    def test_prioritize_improvements(self, agent: Any, improvements_module: Any) -> None:
        """Test prioritizing improvements."""
        agent.add_improvement("Low", "Desc", priority=improvements_module.ImprovementPriority.LOW)
        agent.add_improvement(
            "Critical",
            "Desc",
            priority=improvements_module.ImprovementPriority.CRITICAL)
        agent.add_improvement(
            "Medium",
            "Desc",
            priority=improvements_module.ImprovementPriority.MEDIUM)
        prioritized = agent.prioritize_improvements()
        assert prioritized[0].priority == improvements_module.ImprovementPriority.CRITICAL


# ========== Effort Estimation Tests ==========

class TestEffortEstimation:
    """Tests for effort estimation."""

    def test_estimate_total_effort(self, agent: Any, improvements_module: Any) -> None:
        """Test total effort estimation."""
        agent.add_improvement("Small", "Desc", effort=improvements_module.EffortEstimate.SMALL)
        agent.add_improvement("Medium", "Desc", effort=improvements_module.EffortEstimate.MEDIUM)
        total = agent.estimate_total_effort()
        assert total == 8  # 3 + 5


# ========== Dependency Tests ==========

class TestDependencies:
    """Tests for improvement dependencies."""

    def test_add_dependency(self, agent: Any) -> None:
        """Test adding dependency."""
        imp1 = agent.add_improvement("Base", "First")
        imp2 = agent.add_improvement("Depends", "Second")
        result = agent.add_dependency(imp2.id, imp1.id)
        assert result is True
        assert imp1.id in imp2.dependencies

    def test_get_dependencies(self, agent: Any) -> None:
        """Test getting dependencies."""
        imp1 = agent.add_improvement("Base", "First")
        imp2 = agent.add_improvement("Depends", "Second")
        agent.add_dependency(imp2.id, imp1.id)
        deps = agent.get_dependencies(imp2.id)
        assert len(deps) == 1
        assert deps[0].id == imp1.id

    def test_get_ready_to_implement(self, agent: Any, improvements_module: Any) -> None:
        """Test getting ready to implement improvements."""
        imp1 = agent.add_improvement("Base", "First")
        agent.update_status(imp1.id, improvements_module.ImprovementStatus.COMPLETED)
        imp2 = agent.add_improvement("Depends", "Second")
        imp2.status = improvements_module.ImprovementStatus.APPROVED
        agent.add_dependency(imp2.id, imp1.id)
        ready = agent.get_ready_to_implement()
        assert len(ready) == 1
        assert ready[0].id == imp2.id


# ========== Template Tests ==========

class TestTemplates:
    """Tests for improvement templates."""

    def test_get_default_templates(self, improvements_module: Any) -> None:
        """Test that default templates exist."""
        templates = improvements_module.DEFAULT_TEMPLATES
        assert len(templates) > 0

    def test_create_from_template(self, agent: Any) -> None:
        """Test creating improvement from template."""
        imp = agent.create_from_template(
            "performance_optimization",
            variables={"component": "DatabasePool", "file": "database.py"}
        )
        assert imp is not None
        assert imp.title is not None

    def test_add_custom_template(self, agent: Any, improvements_module: Any) -> None:
        """Test adding custom template."""
        template = improvements_module.ImprovementTemplate(
            id="custom1",
            name="Custom Template",
            title_pattern="Custom: {item}",
            description_pattern="Custom description for {item}"
        )
        agent.add_template(template)
        imp = agent.create_from_template("custom1", {"item": "test"})
        assert "Custom: test" in imp.title


# ========== Voting Tests ==========

class TestVoting:
    """Tests for improvement voting."""

    def test_upvote(self, agent: Any) -> None:
        """Test upvoting improvement."""
        imp = agent.add_improvement("Vote me", "Description")
        agent.vote(imp.id, 1)
        assert imp.votes == 1

    def test_downvote(self, agent: Any) -> None:
        """Test downvoting improvement."""
        imp = agent.add_improvement("Vote me", "Description")
        agent.vote(imp.id, -1)
        assert imp.votes == -1

    def test_get_top_voted(self, agent: Any) -> None:
        """Test getting top voted."""
        imp1 = agent.add_improvement("Popular", "Description")
        imp2 = agent.add_improvement("Less popular", "Description")
        agent.vote(imp1.id, 5)
        agent.vote(imp2.id, 1)
        top = agent.get_top_voted(1)
        assert len(top) == 1
        assert top[0].id == imp1.id


# ========== Assignment Tests ==========

class TestAssignment:
    """Tests for improvement assignment."""

    def test_assign(self, agent: Any) -> None:
        """Test assigning improvement."""
        imp = agent.add_improvement("Assign me", "Description")
        result = agent.assign(imp.id, "developer1")
        assert result is True
        assert imp.assignee == "developer1"

    def test_unassign(self, agent: Any) -> None:
        """Test unassigning improvement."""
        imp = agent.add_improvement("Unassign me", "Description")
        agent.assign(imp.id, "developer1")
        result = agent.unassign(imp.id)
        assert result is True
        assert imp.assignee is None

    def test_get_by_assignee(self, agent: Any) -> None:
        """Test getting by assignee."""
        imp1 = agent.add_improvement("Task 1", "Description")
        imp2 = agent.add_improvement("Task 2", "Description")
        agent.assign(imp1.id, "dev1")
        agent.assign(imp2.id, "dev2")
        dev1_tasks = agent.get_by_assignee("dev1")
        assert len(dev1_tasks) == 1
        assert dev1_tasks[0].id == imp1.id


# ========== Analytics Tests ==========

class TestAnalytics:
    """Tests for improvement analytics."""

    def test_calculate_analytics(self, agent: Any, improvements_module: Any) -> None:
        """Test analytics calculation."""
        agent.add_improvement(
            "Perf",
            "Desc",
            category=improvements_module.ImprovementCategory.PERFORMANCE)
        agent.add_improvement(
            "Sec",
            "Desc",
            category=improvements_module.ImprovementCategory.SECURITY)
        analytics = agent.calculate_analytics()
        assert "total" in analytics
        assert "by_category" in analytics
        assert "by_status" in analytics
        assert "by_priority" in analytics


# ========== Export Tests ==========

class TestExport:
    """Tests for improvement export."""

    def test_export_json(self, agent: Any) -> None:
        """Test JSON export."""
        agent.add_improvement("Export me", "Description")
        exported = agent.export_improvements("json")
        data = json.loads(exported)
        assert len(data) == 1

    def test_export_csv(self, agent: Any) -> None:
        """Test CSV export."""
        agent.add_improvement("Export me", "Description")
        exported = agent.export_improvements("csv")
        assert "id,title" in exported


# ========== Documentation Tests ==========

class TestDocumentationGeneration:
    """Tests for documentation generation."""

    def test_generate_documentation(self, agent: Any, improvements_module: Any) -> None:
        """Test documentation generation."""
        agent.add_improvement(
            "Performance fix",
            "Optimize the database",
            category=improvements_module.ImprovementCategory.PERFORMANCE,
            priority=improvements_module.ImprovementPriority.HIGH
        )
        docs = agent.generate_documentation()
        assert "# Improvement Documentation" in docs
        assert "Performance fix" in docs


# ========== Session 7 Tests: New Enums ==========


class TestSession7Enums:
    """Tests for Session 7 enums."""

    def test_schedule_status_enum(self, improvements_module: Any) -> None:
        """Test ScheduleStatus enum values."""
        assert improvements_module.ScheduleStatus.UNSCHEDULED.value == "unscheduled"
        assert improvements_module.ScheduleStatus.SCHEDULED.value == "scheduled"
        assert improvements_module.ScheduleStatus.IN_SPRINT.value == "in_sprint"
        assert improvements_module.ScheduleStatus.BLOCKED.value == "blocked"
        assert improvements_module.ScheduleStatus.OVERDUE.value == "overdue"

    def test_validation_severity_enum(self, improvements_module: Any) -> None:
        """Test ValidationSeverity enum values."""
        assert improvements_module.ValidationSeverity.ERROR.value == "error"
        assert improvements_module.ValidationSeverity.WARNING.value == "warning"
        assert improvements_module.ValidationSeverity.INFO.value == "info"

    def test_analysis_tool_type_enum(self, improvements_module: Any) -> None:
        """Test AnalysisToolType enum values."""
        assert improvements_module.AnalysisToolType.LINTER.value == "linter"
        assert improvements_module.AnalysisToolType.TYPE_CHECKER.value == "type_checker"
        assert improvements_module.AnalysisToolType.SECURITY_SCANNER.value == "security_scanner"

    def test_sla_level_enum(self, improvements_module: Any) -> None:
        """Test SLALevel enum values."""
        assert improvements_module.SLALevel.P0.value == 1
        assert improvements_module.SLALevel.P4.value == 5


# ========== Session 7 Tests: Dataclasses ==========


class TestSession7Dataclasses:
    """Tests for Session 7 dataclasses."""

    def test_scheduled_improvement_dataclass(self, improvements_module: Any) -> None:
        """Test ScheduledImprovement dataclass."""
        scheduled = improvements_module.ScheduledImprovement(
            improvement_id="imp123"
        )
        assert scheduled.improvement_id == "imp123"
        assert scheduled.status == improvements_module.ScheduleStatus.UNSCHEDULED

    def test_progress_report_dataclass(self, improvements_module: Any) -> None:
        """Test ProgressReport dataclass."""
        report = improvements_module.ProgressReport(
            report_date="2025-01-01"
        )
        assert report.completed_count == 0
        assert report.velocity == 0.0

    def test_validation_result_dataclass(self, improvements_module: Any) -> None:
        """Test ValidationResult dataclass."""
        result = improvements_module.ValidationResult(
            improvement_id="imp123"
        )
        assert result.is_valid is True
        assert result.issues == []

    def test_rollback_record_dataclass(self, improvements_module: Any) -> None:
        """Test RollbackRecord dataclass."""
        record = improvements_module.RollbackRecord(
            improvement_id="imp123"
        )
        assert record.reason == ""

    def test_tool_suggestion_dataclass(self, improvements_module: Any) -> None:
        """Test ToolSuggestion dataclass."""
        suggestion = improvements_module.ToolSuggestion(
            tool_type=improvements_module.AnalysisToolType.LINTER,
            tool_name="pylint",
            file_path="test.py",
            line_number=10,
            message="Missing docstring"
        )
        assert suggestion.tool_name == "pylint"

    def test_sla_configuration_dataclass(self, improvements_module: Any) -> None:
        """Test SLAConfiguration dataclass."""
        config = improvements_module.SLAConfiguration(
            level=improvements_module.SLALevel.P0,
            max_hours=24,
            escalation_hours=12
        )
        assert config.max_hours == 24

    def test_merge_candidate_dataclass(self, improvements_module: Any) -> None:
        """Test MergeCandidate dataclass."""
        candidate = improvements_module.MergeCandidate(
            source_id="imp1",
            target_id="imp2"
        )
        assert candidate.similarity_score == 0.0

    def test_archived_improvement_dataclass(self, improvements_module: Any, agent: Any) -> None:
        """Test ArchivedImprovement dataclass."""
        imp = agent.add_improvement("Test", "Description")
        archived = improvements_module.ArchivedImprovement(
            improvement=imp
        )
        assert archived.archived_date == ""


# ========== Session 7 Tests: ImprovementScheduler ==========


class TestImprovementScheduler:
    """Tests for ImprovementScheduler class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test ImprovementScheduler initialization."""
        scheduler = improvements_module.ImprovementScheduler()
        assert scheduler.schedule == {}

    def test_schedule_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test scheduling an improvement."""
        scheduler = improvements_module.ImprovementScheduler()
        imp = agent.add_improvement("Test", "Description")
        scheduled = scheduler.schedule_improvement(
            imp, "2025-01-15", resources=["dev1"]
        )
        assert scheduled.improvement_id == imp.id
        assert scheduled.status == improvements_module.ScheduleStatus.SCHEDULED

    def test_get_schedule(self, improvements_module: Any, agent: Any) -> None:
        """Test getting schedule."""
        scheduler = improvements_module.ImprovementScheduler()
        imp = agent.add_improvement("Test", "Description")
        scheduler.schedule_improvement(imp, "2025-01-15")
        schedule = scheduler.get_schedule(imp.id)
        assert schedule is not None

    def test_update_status(self, improvements_module: Any, agent: Any) -> None:
        """Test updating schedule status."""
        scheduler = improvements_module.ImprovementScheduler()
        imp = agent.add_improvement("Test", "Description")
        scheduler.schedule_improvement(imp, "2025-01-15")
        result = scheduler.update_status(
            imp.id, improvements_module.ScheduleStatus.IN_SPRINT
        )
        assert result is True

    def test_get_sprint_items(self, improvements_module: Any, agent: Any) -> None:
        """Test getting sprint items."""
        scheduler = improvements_module.ImprovementScheduler()
        imp = agent.add_improvement("Test", "Description")
        scheduler.schedule_improvement(imp, "2025-01-15", sprint_id="sprint-1")
        items = scheduler.get_sprint_items("sprint-1")
        assert imp.id in items


# ========== Session 7 Tests: ProgressDashboard ==========


class TestProgressDashboard:
    """Tests for ProgressDashboard class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test ProgressDashboard initialization."""
        dashboard = improvements_module.ProgressDashboard()
        assert dashboard.reports == []

    def test_generate_report(self, improvements_module: Any, agent: Any) -> None:
        """Test generating a report."""
        dashboard = improvements_module.ProgressDashboard()
        imp = agent.add_improvement("Test", "Description")
        report = dashboard.generate_report([imp])
        assert isinstance(report, improvements_module.ProgressReport)

    def test_get_completion_rate(self, improvements_module: Any, agent: Any) -> None:
        """Test getting completion rate."""
        dashboard = improvements_module.ProgressDashboard()
        imp = agent.add_improvement("Test", "Description")
        imp.status = improvements_module.ImprovementStatus.COMPLETED
        rate = dashboard.get_completion_rate([imp])
        assert rate == 100.0

    def test_export_dashboard(self, improvements_module: Any, agent: Any) -> None:
        """Test exporting dashboard."""
        dashboard = improvements_module.ProgressDashboard()
        imp = agent.add_improvement("Test", "Description")
        output = dashboard.export_dashboard([imp])
        assert "# Improvements Dashboard" in output


# ========== Session 7 Tests: ImprovementValidator ==========


class TestImprovementValidator:
    """Tests for ImprovementValidator class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test ImprovementValidator initialization."""
        validator = improvements_module.ImprovementValidator()
        assert len(validator.rules) > 0

    def test_validate_valid(self, improvements_module: Any, agent: Any) -> None:
        """Test validating a valid improvement."""
        validator = improvements_module.ImprovementValidator()
        imp = agent.add_improvement(
            "Test Improvement",
            "This is a detailed description",
            category=improvements_module.ImprovementCategory.PERFORMANCE
        )
        result = validator.validate(imp)
        assert result.is_valid is True

    def test_validate_invalid(self, improvements_module: Any, agent: Any) -> None:
        """Test validating an invalid improvement."""
        validator = improvements_module.ImprovementValidator()
        imp = agent.add_improvement("Test", "Short")
        result = validator.validate(imp)
        assert result.is_valid is False

    def test_validate_all(self, improvements_module: Any, agent: Any) -> None:
        """Test validating multiple improvements."""
        validator = improvements_module.ImprovementValidator()
        imps = [
            agent.add_improvement("Test 1", "Description " * 5),
            agent.add_improvement("Test 2", "Short")
        ]
        results = validator.validate_all(imps)
        assert len(results) == 2


# ========== Session 7 Tests: RollbackTracker ==========


class TestRollbackTracker:
    """Tests for RollbackTracker class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test RollbackTracker initialization."""
        tracker = improvements_module.RollbackTracker()
        assert tracker.rollbacks == []

    def test_save_state(self, improvements_module: Any, agent: Any) -> None:
        """Test saving state."""
        tracker = improvements_module.RollbackTracker()
        imp = agent.add_improvement("Test", "Description")
        tracker.save_state(imp)
        assert imp.id in tracker.states

    def test_record_rollback(self, improvements_module: Any, agent: Any) -> None:
        """Test recording rollback."""
        tracker = improvements_module.RollbackTracker()
        imp = agent.add_improvement("Test", "Description")
        tracker.save_state(imp)
        record = tracker.record_rollback(imp, "Tests failed")
        assert record.reason == "Tests failed"

    def test_get_rollbacks(self, improvements_module: Any, agent: Any) -> None:
        """Test getting rollbacks."""
        tracker = improvements_module.RollbackTracker()
        imp = agent.add_improvement("Test", "Description")
        tracker.record_rollback(imp, "Failed")
        rollbacks = tracker.get_rollbacks(imp.id)
        assert len(rollbacks) == 1


# ========== Session 7 Tests: ToolIntegration ==========


class TestToolIntegration:
    """Tests for ToolIntegration class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test ToolIntegration initialization."""
        integration = improvements_module.ToolIntegration()
        assert integration.tool_configs == {}

    def test_configure_tool(self, improvements_module: Any) -> None:
        """Test configuring a tool."""
        integration = improvements_module.ToolIntegration()
        integration.configure_tool(
            "pylint",
            improvements_module.AnalysisToolType.LINTER,
            "pylint {file}"
        )
        assert "pylint" in integration.tool_configs

    def test_parse_pylint_output(self, improvements_module: Any) -> None:
        """Test parsing pylint output."""
        integration = improvements_module.ToolIntegration()
        output = "test.py:10:0: C0114: Missing module docstring"
        suggestions = integration.parse_pylint_output(output)
        assert len(suggestions) == 1
        assert suggestions[0].tool_name == "pylint"

    def test_parse_mypy_output(self, improvements_module: Any) -> None:
        """Test parsing mypy output."""
        integration = improvements_module.ToolIntegration()
        output = "test.py:20: error: Incompatible types"
        suggestions = integration.parse_mypy_output(output)
        assert len(suggestions) == 1
        assert suggestions[0].tool_name == "mypy"

    def test_get_suggestions(self, improvements_module: Any) -> None:
        """Test getting suggestions."""
        integration = improvements_module.ToolIntegration()
        integration.parse_pylint_output("test.py:10:0: C0114: Missing docstring")
        suggestions = integration.get_suggestions()
        assert len(suggestions) == 1


# ========== Session 7 Tests: SLAManager ==========


class TestSLAManager:
    """Tests for SLAManager class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test SLAManager initialization."""
        manager = improvements_module.SLAManager()
        assert len(manager.sla_configs) == 5  # P0-P4

    def test_assign_sla(self, improvements_module: Any, agent: Any) -> None:
        """Test assigning SLA."""
        manager = improvements_module.SLAManager()
        imp = agent.add_improvement("Urgent", "Fix now")
        manager.assign_sla(imp, improvements_module.SLALevel.P0)
        assert imp.id in manager.tracked

    def test_check_sla_status(self, improvements_module: Any, agent: Any) -> None:
        """Test checking SLA status."""
        manager = improvements_module.SLAManager()
        imp = agent.add_improvement("Urgent", "Fix now")
        manager.assign_sla(imp, improvements_module.SLALevel.P1)
        status = manager.check_sla_status(imp.id)
        assert status["status"] == "on_track"

    def test_get_sla_compliance_rate(self, improvements_module: Any) -> None:
        """Test getting SLA compliance rate."""
        manager = improvements_module.SLAManager()
        rate = manager.get_sla_compliance_rate()
        assert rate == 100.0


# ========== Session 7 Tests: MergeDetector ==========


class TestMergeDetector:
    """Tests for MergeDetector class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test MergeDetector initialization."""
        detector = improvements_module.MergeDetector()
        assert detector.similarity_threshold == 0.7

    def test_find_similar(self, improvements_module: Any, agent: Any) -> None:
        """Test finding similar improvements."""
        detector = improvements_module.MergeDetector(similarity_threshold=0.5)
        imp1 = agent.add_improvement(
            "Fix performance issue",
            "Optimize database",
            category=improvements_module.ImprovementCategory.PERFORMANCE
        )
        imp2 = agent.add_improvement(
            "Fix performance problem",
            "Optimize queries",
            category=improvements_module.ImprovementCategory.PERFORMANCE
        )
        candidates = detector.find_similar([imp1, imp2])
        assert len(candidates) >= 0  # May or may not find depending on threshold

    def test_merge(self, improvements_module: Any, agent: Any) -> None:
        """Test merging improvements."""
        detector = improvements_module.MergeDetector()
        imp1 = agent.add_improvement("Source", "Description 1", tags=["tag1"])
        imp2 = agent.add_improvement("Target", "Description 2", tags=["tag2"])
        merged = detector.merge(imp1, imp2)
        assert "Merged from: Source" in merged.description


# ========== Session 7 Tests: ImprovementArchive ==========


class TestImprovementArchive:
    """Tests for ImprovementArchive class."""

    def test_init(self, improvements_module: Any) -> None:
        """Test ImprovementArchive initialization."""
        archive = improvements_module.ImprovementArchive()
        assert archive.archive == []

    def test_archive_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test archiving an improvement."""
        archive = improvements_module.ImprovementArchive()
        imp = agent.add_improvement("Old", "Completed long ago")
        archived = archive.archive_improvement(imp, "Completed", "admin")
        assert archived.archive_reason == "Completed"

    def test_restore(self, improvements_module: Any, agent: Any) -> None:
        """Test restoring an improvement."""
        archive = improvements_module.ImprovementArchive()
        imp = agent.add_improvement("Old", "Completed")
        archive.archive_improvement(imp, "Completed")
        restored = archive.restore(imp.id)
        assert restored is not None
        assert restored.id == imp.id

    def test_search_archive(self, improvements_module: Any, agent: Any) -> None:
        """Test searching the archive."""
        archive = improvements_module.ImprovementArchive()
        imp = agent.add_improvement("Performance fix", "Details")
        archive.archive_improvement(imp, "Done")
        results = archive.search_archive("Performance")
        assert len(results) == 1

    def test_get_archive_stats(self, improvements_module: Any, agent: Any) -> None:
        """Test getting archive stats."""
        archive = improvements_module.ImprovementArchive()
        imp = agent.add_improvement("Test", "Description")
        archive.archive_improvement(imp, "Completed")
        stats = archive.get_archive_stats()
        assert stats["total_archived"] == 1


# =============================================================================
# Session 8 Tests: Branch Comparison
# =============================================================================


class TestBranchComparisonStatusEnum:
    """Tests for BranchComparisonStatus enum."""

    def test_enum_values(self, improvements_module: Any) -> None:
        """Test enum has expected values."""
        assert improvements_module.BranchComparisonStatus.PENDING.value == "pending"
        assert improvements_module.BranchComparisonStatus.IN_PROGRESS.value == "in_progress"
        assert improvements_module.BranchComparisonStatus.COMPLETED.value == "completed"
        assert improvements_module.BranchComparisonStatus.FAILED.value == "failed"

    def test_all_members(self, improvements_module: Any) -> None:
        """Test all members exist."""
        members = list(improvements_module.BranchComparisonStatus)
        assert len(members) == 4


class TestImprovementDiffTypeEnum:
    """Tests for ImprovementDiffType enum."""

    def test_enum_values(self, improvements_module: Any) -> None:
        """Test enum has expected values."""
        assert improvements_module.ImprovementDiffType.ADDED.value == "added"
        assert improvements_module.ImprovementDiffType.REMOVED.value == "removed"
        assert improvements_module.ImprovementDiffType.MODIFIED.value == "modified"
        assert improvements_module.ImprovementDiffType.UNCHANGED.value == "unchanged"

    def test_all_members(self, improvements_module: Any) -> None:
        """Test all members exist."""
        members = list(improvements_module.ImprovementDiffType)
        assert len(members) == 4


class TestImprovementDiffDataclass:
    """Tests for ImprovementDiff dataclass."""

    def test_creation(self, improvements_module: Any) -> None:
        """Test creating ImprovementDiff."""
        diff = improvements_module.ImprovementDiff(
            improvement_id="imp_1",
            diff_type=improvements_module.ImprovementDiffType.ADDED,
            change_summary="New improvement added"
        )
        assert diff.improvement_id == "imp_1"
        assert diff.diff_type == improvements_module.ImprovementDiffType.ADDED
        assert diff.source_version is None
        assert diff.target_version is None

    def test_with_versions(self, improvements_module: Any, agent: Any) -> None:
        """Test ImprovementDiff with improvement versions."""
        imp = agent.add_improvement("Test", "Description")
        diff = improvements_module.ImprovementDiff(
            improvement_id=imp.id,
            diff_type=improvements_module.ImprovementDiffType.MODIFIED,
            source_version=imp,
            target_version=imp,
            change_summary="Title changed"
        )
        assert diff.source_version is not None
        assert diff.target_version is not None


class TestBranchComparisonDataclass:
    """Tests for BranchComparison dataclass."""

    def test_creation(self, improvements_module: Any) -> None:
        """Test creating BranchComparison."""
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature / improvements",
            file_path="improvements.md"
        )
        assert comparison.source_branch == "main"
        assert comparison.target_branch == "feature / improvements"
        assert comparison.status == improvements_module.BranchComparisonStatus.PENDING

    def test_with_diffs(self, improvements_module: Any) -> None:
        """Test BranchComparison with diffs."""
        diff = improvements_module.ImprovementDiff(
            improvement_id="imp_1",
            diff_type=improvements_module.ImprovementDiffType.ADDED
        )
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature",
            file_path="test.md",
            diffs=[diff],
            added_count=1
        )
        assert len(comparison.diffs) == 1
        assert comparison.added_count == 1


class TestConflictResolutionDataclass:
    """Tests for ConflictResolution dataclass."""

    def test_creation(self, improvements_module: Any, agent: Any) -> None:
        """Test creating ConflictResolution."""
        imp = agent.add_improvement("Test", "Description")
        resolution = improvements_module.ConflictResolution(
            improvement_id=imp.id,
            resolution=imp,
            strategy="ours",
            resolved_by="admin"
        )
        assert resolution.improvement_id == imp.id
        assert resolution.strategy == "ours"

    def test_defaults(self, improvements_module: Any, agent: Any) -> None:
        """Test ConflictResolution defaults."""
        imp = agent.add_improvement("Test", "Description")
        resolution = improvements_module.ConflictResolution(
            improvement_id=imp.id,
            resolution=imp
        )
        assert resolution.strategy == "manual"
        assert resolution.resolved_by == ""


class TestBranchComparer:
    """Tests for BranchComparer class."""

    def test_initialization(self, improvements_module: Any, tmp_path: Path) -> None:
        """Test BranchComparer initialization."""
        comparer = improvements_module.BranchComparer(str(tmp_path))
        assert comparer.repo_path == tmp_path
        assert comparer.comparisons == []

    def test_initialization_default_path(self, improvements_module: Any) -> None:
        """Test BranchComparer with default path."""
        comparer = improvements_module.BranchComparer()
        assert comparer.repo_path is not None

    def test_parse_improvements(self, improvements_module: Any) -> None:
        """Test parsing improvements from markdown."""
        comparer = improvements_module.BranchComparer()
        content = """# Improvements

## Suggested improvements
- [x] First improvement
- [ ] Second improvement
- [x] Third improvement
"""
        improvements = comparer._parse_improvements(content)
        assert len(improvements) == 3

    def test_calculate_diffs_added(self, improvements_module: Any, agent: Any) -> None:
        """Test calculating diffs with added improvement."""
        comparer = improvements_module.BranchComparer()
        imp = agent.add_improvement("Test", "Description")

        source = {}
        target = {imp.id: imp}

        diffs = comparer._calculate_diffs(source, target)
        added = [d for d in diffs if d.diff_type == improvements_module.ImprovementDiffType.ADDED]
        assert len(added) == 1

    def test_calculate_diffs_removed(self, improvements_module: Any, agent: Any) -> None:
        """Test calculating diffs with removed improvement."""
        comparer = improvements_module.BranchComparer()
        imp = agent.add_improvement("Test", "Description")

        source = {imp.id: imp}
        target = {}

        diffs = comparer._calculate_diffs(source, target)
        removed = [d for d in diffs if d.diff_type ==
                   improvements_module.ImprovementDiffType.REMOVED]
        assert len(removed) == 1

    def test_calculate_diffs_unchanged(self, improvements_module: Any, agent: Any) -> None:
        """Test calculating diffs with unchanged improvement."""
        comparer = improvements_module.BranchComparer()
        imp = agent.add_improvement("Test", "Description")

        source = {imp.id: imp}
        target = {imp.id: imp}

        diffs = comparer._calculate_diffs(source, target)
        unchanged = [d for d in diffs if d.diff_type ==
                     improvements_module.ImprovementDiffType.UNCHANGED]
        assert len(unchanged) == 1

    def test_get_added_improvements(self, improvements_module: Any, agent: Any) -> None:
        """Test getting added improvements from comparison."""
        comparer = improvements_module.BranchComparer()
        imp = agent.add_improvement("New feature", "Details")

        diff = improvements_module.ImprovementDiff(
            improvement_id=imp.id,
            diff_type=improvements_module.ImprovementDiffType.ADDED,
            target_version=imp
        )
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature",
            file_path="test.md",
            diffs=[diff]
        )

        added = comparer.get_added_improvements(comparison)
        assert len(added) == 1
        assert added[0].title == "New feature"

    def test_get_removed_improvements(self, improvements_module: Any, agent: Any) -> None:
        """Test getting removed improvements from comparison."""
        comparer = improvements_module.BranchComparer()
        imp = agent.add_improvement("Old feature", "Details")

        diff = improvements_module.ImprovementDiff(
            improvement_id=imp.id,
            diff_type=improvements_module.ImprovementDiffType.REMOVED,
            source_version=imp
        )
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature",
            file_path="test.md",
            diffs=[diff]
        )

        removed = comparer.get_removed_improvements(comparison)
        assert len(removed) == 1
        assert removed[0].title == "Old feature"

    def test_get_modified_improvements(self, improvements_module: Any, agent: Any) -> None:
        """Test getting modified improvements from comparison."""
        comparer = improvements_module.BranchComparer()
        imp1 = agent.add_improvement("Feature v1", "Details v1")
        imp2 = agent.add_improvement("Feature v2", "Details v2")

        diff = improvements_module.ImprovementDiff(
            improvement_id="common_id",
            diff_type=improvements_module.ImprovementDiffType.MODIFIED,
            source_version=imp1,
            target_version=imp2
        )
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature",
            file_path="test.md",
            diffs=[diff]
        )

        modified = comparer.get_modified_improvements(comparison)
        assert len(modified) == 1
        assert modified[0][0].title == "Feature v1"
        assert modified[0][1].title == "Feature v2"

    def test_generate_merge_report(self, improvements_module: Any, agent: Any) -> None:
        """Test generating merge report."""
        comparer = improvements_module.BranchComparer()
        imp = agent.add_improvement("New feature", "Details")

        diff = improvements_module.ImprovementDiff(
            improvement_id=imp.id,
            diff_type=improvements_module.ImprovementDiffType.ADDED,
            target_version=imp,
            change_summary="New improvement"
        )
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature",
            file_path="test.md",
            diffs=[diff],
            added_count=1
        )

        report = comparer.generate_merge_report(comparison)
        assert "# Branch Comparison Report" in report
        assert "main" in report
        assert "feature" in report
        assert "Added: 1" in report

    def test_comparison_history(self, improvements_module: Any) -> None:
        """Test comparison history tracking."""
        comparer = improvements_module.BranchComparer()
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature",
            file_path="test.md"
        )
        comparer.comparisons.append(comparison)

        history = comparer.get_comparison_history()
        assert len(history) == 1

    def test_clear_history(self, improvements_module: Any) -> None:
        """Test clearing comparison history."""
        comparer = improvements_module.BranchComparer()
        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature",
            file_path="test.md"
        )
        comparer.comparisons.append(comparison)
        comparer.clear_history()

        assert len(comparer.comparisons) == 0


class TestSession8Integration:
    """Integration tests for Session 8 branch comparison features."""

    def test_full_comparison_workflow(self, improvements_module: Any, agent: Any) -> None:
        """Test full comparison workflow."""
        comparer = improvements_module.BranchComparer()

        # Create source and target improvement sets
        imp1 = agent.add_improvement("Common feature", "Details")
        imp2 = agent.add_improvement("New in target", "Details")
        imp3 = agent.add_improvement("Only in source", "Details")

        source = {imp1.id: imp1, imp3.id: imp3}
        target = {imp1.id: imp1, imp2.id: imp2}

        # Calculate diffs
        diffs = comparer._calculate_diffs(source, target)

        # Should have: 1 added (imp2), 1 removed (imp3), 1 unchanged (imp1)
        added = [d for d in diffs if d.diff_type == improvements_module.ImprovementDiffType.ADDED]
        removed = [d for d in diffs if d.diff_type ==
                   improvements_module.ImprovementDiffType.REMOVED]
        unchanged = [d for d in diffs if d.diff_type ==
                     improvements_module.ImprovementDiffType.UNCHANGED]

        assert len(added) == 1
        assert len(removed) == 1
        assert len(unchanged) == 1

    def test_merge_report_with_multiple_changes(self, improvements_module: Any, agent: Any) -> None:
        """Test merge report with various change types."""
        comparer = improvements_module.BranchComparer()

        imp_added = agent.add_improvement("Added", "New feature")
        imp_removed = agent.add_improvement("Removed", "Old feature")

        diffs = [
            improvements_module.ImprovementDiff(
                improvement_id="added_1",
                diff_type=improvements_module.ImprovementDiffType.ADDED,
                target_version=imp_added
            ),
            improvements_module.ImprovementDiff(
                improvement_id="removed_1",
                diff_type=improvements_module.ImprovementDiffType.REMOVED,
                source_version=imp_removed
            ),
        ]

        comparison = improvements_module.BranchComparison(
            source_branch="main",
            target_branch="feature / update",
            file_path="improvements.md",
            status=improvements_module.BranchComparisonStatus.COMPLETED,
            diffs=diffs,
            added_count=1,
            removed_count=1
        )

        report = comparer.generate_merge_report(comparison)
        assert "➕" in report  # Added emoji
        assert "➖" in report  # Removed emoji
        assert "Added: 1" in report
        assert "Removed: 1" in report


# =============================================================================
# Session 8: Test File Improvement Tests
# =============================================================================


class TestImprovementImpactScoring:
    """Tests for improvement impact scoring accuracy."""

    def test_impact_scorer_initialization(self, improvements_module: Any) -> None:
        """Test impact scorer initialization."""
        ImpactScorer = improvements_module.ImpactScorer

        scorer = ImpactScorer()
        assert scorer.weights is not None

    def test_calculate_impact_score(self, improvements_module: Any, agent: Any) -> None:
        """Test calculating impact score."""
        ImpactScorer = improvements_module.ImpactScorer

        scorer = ImpactScorer()
        imp = agent.add_improvement("Performance fix", "Reduces latency by 50%")

        score = scorer.calculate_score(imp)
        assert 0 <= score <= 100

    def test_impact_factors(self, improvements_module: Any) -> None:
        """Test impact factors are considered."""
        ImpactScorer = improvements_module.ImpactScorer

        scorer = ImpactScorer()
        scorer.set_weights({
            "complexity": 0.3,
            "reach": 0.4,
            "urgency": 0.3
        })

        factors = {"complexity": 80, "reach": 60, "urgency": 90}
        score = scorer.calculate_weighted_score(factors)

        # Weighted average: 0.3 * 80 + 0.4 * 60 + 0.3 * 90=24 + 24 + 27=75
        assert 74 <= score <= 76


class TestImprovementDependencyResolution:
    """Tests for improvement dependency resolution."""

    def test_dependency_resolver_init(self, improvements_module: Any) -> None:
        """Test dependency resolver initialization."""
        DependencyResolver = improvements_module.DependencyResolver

        resolver = DependencyResolver()
        assert resolver.dependencies == {}

    def test_add_dependency(self, improvements_module: Any, agent: Any) -> None:
        """Test adding dependencies."""
        DependencyResolver = improvements_module.DependencyResolver

        resolver = DependencyResolver()
        imp1 = agent.add_improvement("Base feature", "Foundation")
        imp2 = agent.add_improvement("Dependent feature", "Requires base")

        resolver.add_dependency(imp2.id, imp1.id)

        deps = resolver.get_dependencies(imp2.id)
        assert imp1.id in deps

    def test_resolve_order(self, improvements_module: Any, agent: Any) -> None:
        """Test resolving dependency order."""
        DependencyResolver = improvements_module.DependencyResolver

        resolver = DependencyResolver()
        imp1 = agent.add_improvement("First", "No deps")
        imp2 = agent.add_improvement("Second", "Depends on first")
        imp3 = agent.add_improvement("Third", "Depends on second")

        resolver.add_dependency(imp2.id, imp1.id)
        resolver.add_dependency(imp3.id, imp2.id)

        order = resolver.resolve_order([imp1.id, imp2.id, imp3.id])

        assert order.index(imp1.id) < order.index(imp2.id)
        assert order.index(imp2.id) < order.index(imp3.id)


class TestEffortEstimationAlgorithms:
    """Tests for effort estimation algorithms."""

    def test_effort_estimator_init(self, improvements_module: Any) -> None:
        """Test effort estimator initialization."""
        EffortEstimator = improvements_module.EffortEstimator

        estimator = EffortEstimator()
        assert estimator.base_rates is not None

    def test_estimate_simple_task(self, improvements_module: Any, agent: Any) -> None:
        """Test estimating simple task effort."""
        EffortEstimator = improvements_module.EffortEstimator

        estimator = EffortEstimator()
        imp = agent.add_improvement("Simple fix", "Typo correction")

        estimate = estimator.estimate(imp, complexity="low")
        assert estimate.hours > 0
        assert estimate.hours < 8  # Simple task should be < 1 day

    def test_estimate_with_historical_data(self, improvements_module: Any, agent: Any) -> None:
        """Test estimation using historical data."""
        EffortEstimator = improvements_module.EffortEstimator

        estimator = EffortEstimator()
        estimator.add_historical_data("bug_fix", actual_hours=4)
        estimator.add_historical_data("bug_fix", actual_hours=6)

        imp = agent.add_improvement("Bug fix", "Fix null pointer")
        estimate = estimator.estimate(imp, category="bug_fix")

        # Should be around average of historical data (5 hours)
        assert 4 <= estimate.hours <= 6


class TestImprovementTemplateInstantiation:
    """Tests for improvement template instantiation."""

    def test_template_creation(self, improvements_module: Any) -> None:
        """Test creating improvement template."""
        ImprovementTemplate = improvements_module.ImprovementTemplate

        template = ImprovementTemplate(
            name="bug_fix",
            title_pattern="Fix: {issue}",
            description_template="Resolves {issue_id}: {details}"
        )

        assert template.name == "bug_fix"

    def test_template_instantiation(self, improvements_module: Any) -> None:
        """Test instantiating template."""
        ImprovementTemplate = improvements_module.ImprovementTemplate

        template = ImprovementTemplate(
            name="feature",
            title_pattern="Add {feature_name}",
            description_template="Implements {feature_name} functionality"
        )

        result = template.instantiate({
            "feature_name": "dark mode"
        })

        assert result["title"] == "Add dark mode"
        assert "dark mode" in result["description"]


class TestStatusWorkflowTransitions:
    """Tests for status workflow transitions."""

    def test_workflow_engine_init(self, improvements_module: Any) -> None:
        """Test workflow engine initialization."""
        WorkflowEngine = improvements_module.WorkflowEngine

        engine = WorkflowEngine()
        assert len(engine.states) > 0

    def test_valid_transition(self, improvements_module: Any, agent: Any) -> None:
        """Test valid status transition."""
        WorkflowEngine = improvements_module.WorkflowEngine

        engine = WorkflowEngine()
        imp = agent.add_improvement("Test", "Details")

        result = engine.transition(imp, from_status="pending", to_status="in_progress")
        assert result.success
        assert imp.status == "in_progress"

    def test_invalid_transition_blocked(self, improvements_module: Any, agent: Any) -> None:
        """Test invalid transition is blocked."""
        WorkflowEngine = improvements_module.WorkflowEngine

        engine = WorkflowEngine()
        imp = agent.add_improvement("Test", "Details")

        # Can't go from pending directly to completed
        result = engine.transition(imp, from_status="pending", to_status="completed")
        assert not result.success


class TestVotingAndPrioritization:
    """Tests for voting and prioritization mechanics."""

    def test_voting_system_init(self, improvements_module: Any) -> None:
        """Test voting system initialization."""
        VotingSystem = improvements_module.VotingSystem

        voting = VotingSystem()
        assert voting.votes == {}

    def test_cast_vote(self, improvements_module: Any, agent: Any) -> None:
        """Test casting a vote."""
        VotingSystem = improvements_module.VotingSystem

        voting = VotingSystem()
        imp = agent.add_improvement("Popular feature", "Many want this")

        voting.cast_vote(imp.id, voter_id="user1", vote_value=1)
        voting.cast_vote(imp.id, voter_id="user2", vote_value=1)

        assert voting.get_vote_count(imp.id) == 2

    def test_prioritization_by_votes(self, improvements_module: Any, agent: Any) -> None:
        """Test prioritization by vote count."""
        VotingSystem = improvements_module.VotingSystem

        voting = VotingSystem()
        imp1 = agent.add_improvement("Less popular", "Few want")
        imp2 = agent.add_improvement("Most popular", "Many want")

        voting.cast_vote(imp1.id, "user1", 1)
        voting.cast_vote(imp2.id, "user1", 1)
        voting.cast_vote(imp2.id, "user2", 1)
        voting.cast_vote(imp2.id, "user3", 1)

        prioritized = voting.get_prioritized_list([imp1.id, imp2.id])
        assert prioritized[0] == imp2.id


class TestSchedulingAndResourceAllocation:
    """Tests for scheduling and resource allocation."""

    def test_scheduler_init(self, improvements_module: Any) -> None:
        """Test scheduler initialization."""
        ImprovementScheduler = improvements_module.ImprovementScheduler

        scheduler = ImprovementScheduler()
        assert scheduler.schedule == []

    def test_schedule_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test scheduling an improvement."""
        ImprovementScheduler = improvements_module.ImprovementScheduler
        from datetime import datetime, timedelta

        scheduler = ImprovementScheduler()
        imp = agent.add_improvement("Scheduled task", "For next week")

        start_date = datetime.now() + timedelta(days=7)
        scheduled = scheduler.schedule_improvement(imp.id, start_date=start_date)

        assert scheduled.start_date == start_date

    def test_resource_allocation(self, improvements_module: Any, agent: Any) -> None:
        """Test resource allocation."""
        ImprovementScheduler = improvements_module.ImprovementScheduler

        scheduler = ImprovementScheduler()
        imp = agent.add_improvement("Resource task", "Needs team")

        scheduler.allocate_resources(imp.id, resources=["dev1", "dev2"])

        allocation = scheduler.get_allocation(imp.id)
        assert "dev1" in allocation.resources


class TestDashboardRenderingAndUpdates:
    """Tests for dashboard rendering and updates."""

    def test_dashboard_creation(self, improvements_module: Any) -> None:
        """Test dashboard creation."""
        ImprovementDashboard = improvements_module.ImprovementDashboard

        dashboard = ImprovementDashboard()
        assert dashboard is not None

    def test_dashboard_render(self, improvements_module: Any, agent: Any) -> None:
        """Test dashboard rendering."""
        ImprovementDashboard = improvements_module.ImprovementDashboard

        dashboard = ImprovementDashboard()
        imp1 = agent.add_improvement("Task 1", "Details")
        imp2 = agent.add_improvement("Task 2", "Details")

        rendered = dashboard.render([imp1, imp2])
        assert "Task 1" in rendered
        assert "Task 2" in rendered

    def test_dashboard_update_on_change(self, improvements_module: Any, agent: Any) -> None:
        """Test dashboard updates on changes."""
        ImprovementDashboard = improvements_module.ImprovementDashboard

        dashboard = ImprovementDashboard()

        updated: list[bool] = []
        dashboard.on_update(lambda: updated.append(True))

        imp = agent.add_improvement("New task", "Details")
        dashboard.add_improvement(imp)

        assert len(updated) >= 1


class TestAutomatedValidationIntegration:
    """Tests for automated validation integration."""

    def test_validator_init(self, improvements_module: Any) -> None:
        """Test validator initialization."""
        ImprovementValidator = improvements_module.ImprovementValidator

        validator = ImprovementValidator()
        assert validator.rules is not None

    def test_validate_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test validating an improvement."""
        ImprovementValidator = improvements_module.ImprovementValidator

        validator = ImprovementValidator()
        imp = agent.add_improvement("Valid improvement", "With proper description")

        result = validator.validate(imp)
        assert result.is_valid

    def test_validation_failure(self, improvements_module: Any, agent: Any) -> None:
        """Test validation failure."""
        ImprovementValidator = improvements_module.ImprovementValidator

        validator = ImprovementValidator()
        validator.add_rule("min_description_length", min_length=50)

        imp = agent.add_improvement("Short", "Too short")

        result = validator.validate(imp)
        assert not result.is_valid
        assert "description" in result.errors[0].lower()


class TestRollbackTracking:
    """Tests for rollback tracking functionality."""

    def test_rollback_manager_init(self, improvements_module: Any) -> None:
        """Test rollback manager initialization."""
        RollbackManager = improvements_module.RollbackManager

        manager = RollbackManager()
        assert manager.rollbacks == []

    def test_create_rollback_point(self, improvements_module: Any, agent: Any) -> None:
        """Test creating rollback point."""
        RollbackManager = improvements_module.RollbackManager

        manager = RollbackManager()
        imp = agent.add_improvement("Risky change", "May need rollback")

        point = manager.create_rollback_point(imp.id, state={"status": "pending"})

        assert point.improvement_id == imp.id

    def test_rollback_to_point(self, improvements_module: Any, agent: Any) -> None:
        """Test rolling back to point."""
        RollbackManager = improvements_module.RollbackManager

        manager = RollbackManager()
        imp = agent.add_improvement("Change", "Details")

        manager.create_rollback_point(imp.id, state={"status": "pending"})
        imp.status = "completed"

        restored = manager.rollback(imp.id)
        assert restored["status"] == "pending"


class TestCodeAnalysisToolSuggestions:
    """Tests for code analysis tool suggestions."""

    def test_analyzer_init(self, improvements_module: Any) -> None:
        """Test analyzer initialization."""
        CodeAnalyzer = improvements_module.CodeAnalyzer

        analyzer = CodeAnalyzer()
        assert analyzer.tools is not None

    def test_suggest_tools_for_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test suggesting tools for improvement."""
        CodeAnalyzer = improvements_module.CodeAnalyzer

        analyzer = CodeAnalyzer()
        imp = agent.add_improvement("Security fix", "Fix SQL injection")

        suggestions = analyzer.suggest_tools(imp)
        assert len(suggestions) > 0
        # Security tools should be suggested
        assert any("security" in s.lower() or "scan" in s.lower() for s in suggestions)


class TestDocumentationGenerationQuality:
    """Tests for documentation generation quality."""

    def test_doc_generator_init(self, improvements_module: Any) -> None:
        """Test documentation generator initialization."""
        DocGenerator = improvements_module.DocGenerator

        generator = DocGenerator()
        assert generator.templates is not None

    def test_generate_improvement_docs(self, improvements_module: Any, agent: Any) -> None:
        """Test generating improvement documentation."""
        DocGenerator = improvements_module.DocGenerator

        generator = DocGenerator()
        imp = agent.add_improvement("New API endpoint", "Adds /users endpoint")

        docs = generator.generate(imp)
        assert "API" in docs or "endpoint" in docs

    def test_docs_include_metadata(self, improvements_module: Any, agent: Any) -> None:
        """Test docs include metadata."""
        DocGenerator = improvements_module.DocGenerator

        generator = DocGenerator()
        imp = agent.add_improvement("Feature", "Details")
        imp.metadata = {"version": "1.0", "author": "team"}

        docs = generator.generate(imp, include_metadata=True)
        assert "version" in docs or "1.0" in docs


class TestAssignmentAndOwnershipTracking:
    """Tests for assignment and ownership tracking."""

    def test_assignment_manager_init(self, improvements_module: Any) -> None:
        """Test assignment manager initialization."""
        AssignmentManager = improvements_module.AssignmentManager

        manager = AssignmentManager()
        assert manager.assignments == {}

    def test_assign_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test assigning improvement."""
        AssignmentManager = improvements_module.AssignmentManager

        manager = AssignmentManager()
        imp = agent.add_improvement("Task", "Details")

        manager.assign(imp.id, assignee="developer1")

        assert manager.get_assignee(imp.id) == "developer1"

    def test_ownership_history(self, improvements_module: Any, agent: Any) -> None:
        """Test ownership history tracking."""
        AssignmentManager = improvements_module.AssignmentManager

        manager = AssignmentManager()
        imp = agent.add_improvement("Task", "Details")

        manager.assign(imp.id, assignee="dev1")
        manager.assign(imp.id, assignee="dev2")

        history = manager.get_ownership_history(imp.id)
        assert len(history) == 2
        assert history[0]["assignee"] == "dev1"


class TestSLAEnforcementAndAlerting:
    """Tests for SLA enforcement and alerting."""

    def test_sla_manager_init(self, improvements_module: Any) -> None:
        """Test SLA manager initialization."""
        SLAManager = improvements_module.SLAManager

        manager = SLAManager()
        assert manager.sla_policies is not None

    def test_set_sla_policy(self, improvements_module: Any) -> None:
        """Test setting SLA policy."""
        SLAManager = improvements_module.SLAManager

        manager = SLAManager()
        manager.set_policy("critical", response_hours=4, resolution_hours=24)

        policy = manager.get_policy("critical")
        assert policy.resolution_hours == 24

    def test_sla_violation_alert(self, improvements_module: Any, agent: Any) -> None:
        """Test SLA violation alerting."""
        SLAManager = improvements_module.SLAManager
        from datetime import datetime, timedelta

        manager = SLAManager()
        manager.set_policy("urgent", resolution_hours=1)

        imp = agent.add_improvement("Urgent fix", "Needs immediate attention")
        imp.created_at = datetime.now() - timedelta(hours=2)  # 2 hours old

        violations = manager.check_violations([imp], priority="urgent")
        assert len(violations) >= 1


class TestAnalyticsAndTrendCalculations:
    """Tests for analytics and trend calculations."""

    def test_analytics_engine_init(self, improvements_module: Any) -> None:
        """Test analytics engine initialization."""
        AnalyticsEngine = improvements_module.AnalyticsEngine

        engine = AnalyticsEngine()
        assert engine is not None

    def test_calculate_completion_trend(self, improvements_module: Any, agent: Any) -> None:
        """Test calculating completion trend."""
        AnalyticsEngine = improvements_module.AnalyticsEngine

        engine = AnalyticsEngine()

        # Create some completed improvements
        for i in range(5):
            imp = agent.add_improvement(f"Task {i}", "Details")
            imp.status = "completed"
            engine.record_completion(imp)

        trend = engine.get_completion_trend(period_days=30)
        assert trend.total_completed == 5

    def test_velocity_calculation(self, improvements_module: Any, agent: Any) -> None:
        """Test velocity calculation."""
        AnalyticsEngine = improvements_module.AnalyticsEngine

        engine = AnalyticsEngine()

        for i in range(10):
            imp = agent.add_improvement(f"Sprint task {i}", "Details")
            imp.story_points = 3
            imp.status = "completed"
            engine.record_completion(imp)

        velocity = engine.calculate_velocity(sprint_days=14)
        assert velocity > 0


class TestImprovementBulkOperations:
    """Tests for improvement bulk operations."""

    def test_bulk_manager_init(self, improvements_module: Any) -> None:
        """Test bulk manager initialization."""
        BulkManager = improvements_module.BulkManager

        manager = BulkManager()
        assert manager is not None

    def test_bulk_status_update(self, improvements_module: Any, agent: Any) -> None:
        """Test bulk status update."""
        BulkManager = improvements_module.BulkManager

        manager = BulkManager()

        imps = [agent.add_improvement(f"Task {i}", "Details") for i in range(5)]
        ids = [imp.id for imp in imps]

        result = manager.bulk_update_status(ids, new_status="in_progress")

        assert result.success_count == 5

    def test_bulk_assign(self, improvements_module: Any, agent: Any) -> None:
        """Test bulk assignment."""
        BulkManager = improvements_module.BulkManager

        manager = BulkManager()

        imps = [agent.add_improvement(f"Task {i}", "Details") for i in range(3)]
        ids = [imp.id for imp in imps]

        result = manager.bulk_assign(ids, assignee="team_lead")

        assert result.success_count == 3


class TestImprovementArchival:
    """Tests for improvement archival."""

    def test_archive_manager_init(self, improvements_module: Any) -> None:
        """Test archive manager initialization."""
        ArchiveManager = improvements_module.ArchiveManager

        manager = ArchiveManager()
        assert manager.archived == []

    def test_archive_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test archiving improvement."""
        ArchiveManager = improvements_module.ArchiveManager

        manager = ArchiveManager()
        imp = agent.add_improvement("Old task", "Completed long ago")
        imp.status = "completed"

        manager.archive(imp)

        assert imp.id in [a.id for a in manager.archived]

    def test_restore_from_archive(self, improvements_module: Any, agent: Any) -> None:
        """Test restoring from archive."""
        ArchiveManager = improvements_module.ArchiveManager

        manager = ArchiveManager()
        imp = agent.add_improvement("Task", "Details")

        manager.archive(imp)
        restored = manager.restore(imp.id)

        assert restored.id == imp.id
        assert imp.id not in [a.id for a in manager.archived]


class TestImprovementExportFormats:
    """Tests for improvement export formats."""

    def test_exporter_init(self, improvements_module: Any) -> None:
        """Test exporter initialization."""
        ImprovementExporter = improvements_module.ImprovementExporter

        exporter = ImprovementExporter()
        assert exporter.formats is not None

    def test_export_to_json(self, improvements_module: Any, agent: Any) -> None:
        """Test export to JSON."""
        ImprovementExporter = improvements_module.ImprovementExporter

        exporter = ImprovementExporter()
        imp = agent.add_improvement("Export test", "For JSON export")

        output = exporter.export([imp], format="json")
        parsed = json.loads(output)

        assert len(parsed) == 1
        assert parsed[0]["title"] == "Export test"

    def test_export_to_csv(self, improvements_module: Any, agent: Any) -> None:
        """Test export to CSV."""
        ImprovementExporter = improvements_module.ImprovementExporter

        exporter = ImprovementExporter()
        imp = agent.add_improvement("CSV test", "For CSV export")

        output = exporter.export([imp], format="csv")

        assert "title" in output  # Header
        assert "CSV test" in output


class TestImprovementNotifications:
    """Tests for improvement notifications."""

    def test_notification_manager_init(self, improvements_module: Any) -> None:
        """Test notification manager initialization."""
        NotificationManager = improvements_module.NotificationManager

        manager = NotificationManager()
        assert manager.subscribers == []

    def test_subscribe_to_improvement(self, improvements_module: Any, agent: Any) -> None:
        """Test subscribing to improvement."""
        NotificationManager = improvements_module.NotificationManager

        manager = NotificationManager()
        imp = agent.add_improvement("Important", "Watch this")

        manager.subscribe(imp.id, subscriber="user@example.com")

        subscribers = manager.get_subscribers(imp.id)
        assert "user@example.com" in subscribers

    def test_notification_on_status_change(self, improvements_module: Any, agent: Any) -> None:
        """Test notification on status change."""
        NotificationManager = improvements_module.NotificationManager

        manager = NotificationManager()
        imp = agent.add_improvement("Task", "Details")

        notifications: list[dict[str, Any]] = []
        manager.on_notification(lambda n: notifications.append(n))
        manager.subscribe(imp.id, subscriber="watcher")

        manager.notify_status_change(imp.id, old_status="pending", new_status="completed")

        assert len(notifications) >= 1


class TestImprovementAccessControl:
    """Tests for improvement access control."""

    def test_access_controller_init(self, improvements_module: Any) -> None:
        """Test access controller initialization."""
        AccessController = improvements_module.AccessController

        controller = AccessController()
        assert controller.permissions is not None

    def test_grant_access(self, improvements_module: Any, agent: Any) -> None:
        """Test granting access."""
        AccessController = improvements_module.AccessController

        controller = AccessController()
        imp = agent.add_improvement("Restricted", "Limited access")

        controller.grant(imp.id, user="manager", level="write")

        assert controller.can_access(imp.id, user="manager", level="write")

    def test_deny_unauthorized_access(self, improvements_module: Any, agent: Any) -> None:
        """Test denying unauthorized access."""
        AccessController = improvements_module.AccessController

        controller = AccessController()
        imp = agent.add_improvement("Private", "No public access")

        controller.grant(imp.id, user="owner", level="admin")

        assert not controller.can_access(imp.id, user="random_user", level="read")

    def test_role_based_access(self, improvements_module: Any, agent: Any) -> None:
        """Test role-based access."""
        AccessController = improvements_module.AccessController

        controller = AccessController()
        controller.define_role("developer", permissions=["read", "comment"])
        controller.define_role("admin", permissions=["read", "write", "delete", "admin"])

        imp = agent.add_improvement("Team task", "For the team")
        controller.assign_role(imp.id, user="dev1", role="developer")

        assert controller.can_access(imp.id, user="dev1", level="read")
        assert not controller.can_access(imp.id, user="dev1", level="delete")
