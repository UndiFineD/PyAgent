#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# ruff: noqa: F401

"""Lazy-loading entry point for observability.improvements."""

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from src.core.base.lifecycle.version import VERSION
from src.core.lazy_loader import ModuleLazyLoader

if TYPE_CHECKING:
    from .access_controller import AccessController
    from .analysis_tool_type import AnalysisToolType
    from .analytics_engine import AnalyticsEngine
    from .archive_manager import ArchiveManager
    from .archived_improvement import ArchivedImprovement
    from .assignment_manager import AssignmentManager
    from .branch_comparer import BranchComparer
    from .branch_comparison import BranchComparison
    from .branch_comparison_status import BranchComparisonStatus
    from .bulk_manager import BulkManager
    from .bulk_operation_result import BulkOperationResult
    from .code_analyzer import CodeAnalyzer
    from .completion_trend import CompletionTrend
    from .conflict_resolution import ConflictResolution
    from .dependency_resolver import DependencyResolver
    from .doc_generator import DocGenerator
    from .effort_estimate import EffortEstimate
    from .effort_estimate_result import EffortEstimateResult
    from .effort_estimator import EffortEstimator
    from .impact_scorer import ImpactScorer
    from .improvement import Improvement
    from .improvement_archive import ImprovementArchive
    from .improvement_category import ImprovementCategory
    from .improvement_dashboard import ImprovementDashboard
    from .improvement_diff import ImprovementDiff
    from .improvement_diff_type import ImprovementDiffType
    from .improvement_exporter import ImprovementExporter
    from .improvement_manager import ImprovementManager, DEFAULT_TEMPLATES
    from .improvement_priority import ImprovementPriority
    from .improvement_scheduler import ImprovementScheduler
    from .improvement_status import ImprovementStatus
    from .improvement_template import ImprovementTemplate
    from .improvement_validator import ImprovementValidator
    from .improvements_agent import ImprovementsAgent
    from .merge_candidate import MergeCandidate
    from .merge_detector import MergeDetector
    from .notification_manager import NotificationManager
    from .progress_dashboard import ProgressDashboard
    from .progress_report import ProgressReport
    from .resource_allocation import ResourceAllocation
    from .rollback_manager import RollbackManager
    from .rollback_point import RollbackPoint
    from .rollback_record import RollbackRecord
    from .rollback_tracker import RollbackTracker
    from .sla_configuration import SLAConfiguration
    from .sla_level import SLALevel
    from .sla_manager import SLAManager
    from .sla_policy import SLAPolicy
    from .schedule_status import ScheduleStatus
    from .scheduled_entry import ScheduledEntry
    from .scheduled_improvement import ScheduledImprovement
    from .tool_integration import ToolIntegration
    from .tool_suggestion import ToolSuggestion
    from .transition_result import TransitionResult
    from .validation_result import ValidationResult
    from .validation_severity import ValidationSeverity
    from .voting_system import VotingSystem
    from .workflow_engine import WorkflowEngine
    from .schedule_store import _ScheduleStore

_LAZY_REGISTRY = {
    "AccessController": ("src.observability.improvements.access_controller", "AccessController"),
    "AnalysisToolType": ("src.observability.improvements.analysis_tool_type", "AnalysisToolType"),
    "AnalyticsEngine": ("src.observability.improvements.analytics_engine", "AnalyticsEngine"),
    "ArchiveManager": ("src.observability.improvements.archive_manager", "ArchiveManager"),
    "ArchivedImprovement": ("src.observability.improvements.archived_improvement", "ArchivedImprovement"),
    "AssignmentManager": ("src.observability.improvements.assignment_manager", "AssignmentManager"),
    "BranchComparer": ("src.observability.improvements.branch_comparer", "BranchComparer"),
    "BranchComparison": ("src.observability.improvements.branch_comparison", "BranchComparison"),
    "BranchComparisonStatus": ("src.observability.improvements.branch_comparison_status", "BranchComparisonStatus"),
    "BulkManager": ("src.observability.improvements.bulk_manager", "BulkManager"),
    "BulkOperationResult": ("src.observability.improvements.bulk_operation_result", "BulkOperationResult"),
    "CodeAnalyzer": ("src.observability.improvements.code_analyzer", "CodeAnalyzer"),
    "CompletionTrend": ("src.observability.improvements.completion_trend", "CompletionTrend"),
    "ConflictResolution": ("src.observability.improvements.conflict_resolution", "ConflictResolution"),
    "DEFAULT_TEMPLATES": ("src.observability.improvements.improvement_manager", "DEFAULT_TEMPLATES"),
    "DependencyResolver": ("src.observability.improvements.dependency_resolver", "DependencyResolver"),
    "DocGenerator": ("src.observability.improvements.doc_generator", "DocGenerator"),
    "EffortEstimate": ("src.observability.improvements.effort_estimate", "EffortEstimate"),
    "EffortEstimateResult": ("src.observability.improvements.effort_estimate_result", "EffortEstimateResult"),
    "EffortEstimator": ("src.observability.improvements.effort_estimator", "EffortEstimator"),
    "ImpactScorer": ("src.observability.improvements.impact_scorer", "ImpactScorer"),
    "Improvement": ("src.observability.improvements.improvement", "Improvement"),
    "ImprovementArchive": ("src.observability.improvements.improvement_archive", "ImprovementArchive"),
    "ImprovementCategory": ("src.observability.improvements.improvement_category", "ImprovementCategory"),
    "ImprovementDashboard": ("src.observability.improvements.improvement_dashboard", "ImprovementDashboard"),
    "ImprovementDiff": ("src.observability.improvements.improvement_diff", "ImprovementDiff"),
    "ImprovementDiffType": ("src.observability.improvements.improvement_diff_type", "ImprovementDiffType"),
    "ImprovementExporter": ("src.observability.improvements.improvement_exporter", "ImprovementExporter"),
    "ImprovementManager": ("src.observability.improvements.improvement_manager", "ImprovementManager"),
    "ImprovementPriority": ("src.observability.improvements.improvement_priority", "ImprovementPriority"),
    "ImprovementScheduler": ("src.observability.improvements.improvement_scheduler", "ImprovementScheduler"),
    "ImprovementStatus": ("src.observability.improvements.improvement_status", "ImprovementStatus"),
    "ImprovementTemplate": ("src.observability.improvements.improvement_template", "ImprovementTemplate"),
    "ImprovementValidator": ("src.observability.improvements.improvement_validator", "ImprovementValidator"),
    "ImprovementsAgent": ("src.observability.improvements.improvements_agent", "ImprovementsAgent"),
    "MergeCandidate": ("src.observability.improvements.merge_candidate", "MergeCandidate"),
    "MergeDetector": ("src.observability.improvements.merge_detector", "MergeDetector"),
    "NotificationManager": ("src.observability.improvements.notification_manager", "NotificationManager"),
    "ProgressDashboard": ("src.observability.improvements.progress_dashboard", "ProgressDashboard"),
    "ProgressReport": ("src.observability.improvements.progress_report", "ProgressReport"),
    "ResourceAllocation": ("src.observability.improvements.resource_allocation", "ResourceAllocation"),
    "RollbackManager": ("src.observability.improvements.rollback_manager", "RollbackManager"),
    "RollbackPoint": ("src.observability.improvements.rollback_point", "RollbackPoint"),
    "RollbackRecord": ("src.observability.improvements.rollback_record", "RollbackRecord"),
    "RollbackTracker": ("src.observability.improvements.rollback_tracker", "RollbackTracker"),
    "SLAConfiguration": ("src.observability.improvements.sla_configuration", "SLAConfiguration"),
    "SLALevel": ("src.observability.improvements.sla_level", "SLALevel"),
    "SLAManager": ("src.observability.improvements.sla_manager", "SLAManager"),
    "SLAPolicy": ("src.observability.improvements.sla_policy", "SLAPolicy"),
    "ScheduleStatus": ("src.observability.improvements.schedule_status", "ScheduleStatus"),
    "ScheduledEntry": ("src.observability.improvements.scheduled_entry", "ScheduledEntry"),
    "ScheduledImprovement": ("src.observability.improvements.scheduled_improvement", "ScheduledImprovement"),
    "ToolIntegration": ("src.observability.improvements.tool_integration", "ToolIntegration"),
    "ToolSuggestion": ("src.observability.improvements.tool_suggestion", "ToolSuggestion"),
    "TransitionResult": ("src.observability.improvements.transition_result", "TransitionResult"),
    "ValidationResult": ("src.observability.improvements.validation_result", "ValidationResult"),
    "ValidationSeverity": ("src.observability.improvements.validation_severity", "ValidationSeverity"),
    "VotingSystem": ("src.observability.improvements.voting_system", "VotingSystem"),
    "WorkflowEngine": ("src.observability.improvements.workflow_engine", "WorkflowEngine"),
    "_ScheduleStore": ("src.observability.improvements.schedule_store", "_ScheduleStore"),
}

_loader = ModuleLazyLoader(_LAZY_REGISTRY)

def __getattr__(name: str) -> Any:
    return _loader.load(name)

__all__ = ["VERSION"] + list(_LAZY_REGISTRY.keys())
