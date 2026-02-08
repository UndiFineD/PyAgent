#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# ruff: noqa: F401

"""Lazy-loading entry point for observability.errors."""

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from src.core.base.lifecycle.version import VERSION
from src.core.lazy_loader import ModuleLazyLoader

if TYPE_CHECKING:
    from .auto_fix_suggester import AutoFixSuggester
    from .blame_info import BlameInfo
    from .code_context import CodeContext
    from .context_aggregator import ContextAggregator
    from .custom_err import CustomError
    from .error_agent import ErrorAgent
    from .error_category import ErrorCategory
    from .error_classifier import ErrorClassifier
    from .error_database import ErrorDatabase
    from .error_descriptor import ErrorDescriptor
    from .error_handler import ErrorHandler
    from .error_manager import ErrorManager
    from .error_priority import ErrorPriority
    from .error_report import ErrorReport
    from .error_severity import ErrorSeverity
    from .error_stats import ErrorStats
    from .error_status import ErrorStatus
    from .notification_manager import NotificationManager
    from .resolution_recommendation import ResolutionRecommendation
    from .root_cause_analysis import RootCauseAnalysis
    from .solution_verifier import SolutionVerifier
    from .source_location import SourceLocation
    from .suggested_fix import SuggestedFix

_LAZY_REGISTRY = {
    "AutoFixSuggester": ("src.observability.errors.auto_fix_suggester", "AutoFixSuggester"),
    "BlameInfo": ("src.observability.errors.blame_info", "BlameInfo"),
    "CodeContext": ("src.observability.errors.code_context", "CodeContext"),
    "ContextAggregator": ("src.observability.errors.context_aggregator", "ContextAggregator"),
    "CustomError": ("src.observability.errors.custom_err", "CustomError"),
    "ErrorAgent": ("src.observability.errors.error_agent", "ErrorAgent"),
    "ErrorCategory": ("src.observability.errors.error_category", "ErrorCategory"),
    "ErrorClassifier": ("src.observability.errors.error_classifier", "ErrorClassifier"),
    "ErrorDatabase": ("src.observability.errors.error_database", "ErrorDatabase"),
    "ErrorDescriptor": ("src.observability.errors.error_descriptor", "ErrorDescriptor"),
    "ErrorHandler": ("src.observability.errors.error_handler", "ErrorHandler"),
    "ErrorManager": ("src.observability.errors.error_manager", "ErrorManager"),
    "ErrorPriority": ("src.observability.errors.error_priority", "ErrorPriority"),
    "ErrorReport": ("src.observability.errors.error_report", "ErrorReport"),
    "ErrorSeverity": ("src.observability.errors.error_severity", "ErrorSeverity"),
    "ErrorStats": ("src.observability.errors.error_stats", "ErrorStats"),
    "ErrorStatus": ("src.observability.errors.error_status", "ErrorStatus"),
    "NotificationManager": ("src.observability.errors.notification_manager", "NotificationManager"),
    "ResolutionRecommendation": ("src.observability.errors.resolution_recommendation", "ResolutionRecommendation"),
    "RootCauseAnalysis": ("src.observability.errors.root_cause_analysis", "RootCauseAnalysis"),
    "SolutionVerifier": ("src.observability.errors.solution_verifier", "SolutionVerifier"),
    "SourceLocation": ("src.observability.errors.source_location", "SourceLocation"),
    "SuggestedFix": ("src.observability.errors.suggested_fix", "SuggestedFix"),
}

_loader = ModuleLazyLoader(_LAZY_REGISTRY)

def __getattr__(name: str) -> Any:
    return _loader.load(name)

__all__ = ["VERSION"] + list(_LAZY_REGISTRY.keys())
