#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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

# ruff: noqa: F401

"""Lazy-loading entry point for observability.errors."""

from __future__ import annotations
from typing import Any, TYPE_CHECKING
from src.core.base.lifecycle.version import VERSION as VERSION  # noqa: F401
from src.core.lazy_loader import ModuleLazyLoader


if TYPE_CHECKING:
    from .auto_fix_suggester import AutoFixSuggester as AutoFixSuggester  # noqa: F401
    from .blame_info import BlameInfo as BlameInfo  # noqa: F401
    from .code_context import CodeContext as CodeContext  # noqa: F401
    from .context_aggregator import ContextAggregator as ContextAggregator  # noqa: F401
    from .custom_err import CustomError as CustomError  # noqa: F401
    from .error_agent import ErrorAgent as ErrorAgent  # noqa: F401
    from .error_category import ErrorCategory as ErrorCategory  # noqa: F401
    from .error_classifier import ErrorClassifier as ErrorClassifier  # noqa: F401
    from .error_database import ErrorDatabase as ErrorDatabase  # noqa: F401
    from .error_descriptor import ErrorDescriptor as ErrorDescriptor  # noqa: F401
    from .error_handler import ErrorHandler as ErrorHandler  # noqa: F401
    from .error_manager import ErrorManager as ErrorManager  # noqa: F401
    from .error_priority import ErrorPriority as ErrorPriority  # noqa: F401
    from .error_report import ErrorReport as ErrorReport  # noqa: F401
    from .error_severity import ErrorSeverity as ErrorSeverity  # noqa: F401
    from .error_stats import ErrorStats as ErrorStats  # noqa: F401
    from .error_status import ErrorStatus as ErrorStatus  # noqa: F401
    from .notification_manager import NotificationManager as NotificationManager  # noqa: F401
    from .resolution_recommendation import ResolutionRecommendation as ResolutionRecommendation  # noqa: F401
    from .root_cause_analysis import RootCauseAnalysis as RootCauseAnalysis  # noqa: F401
    from .solution_verifier import SolutionVerifier as SolutionVerifier  # noqa: F401
    from .source_location import SourceLocation as SourceLocation  # noqa: F401
    from .suggested_fix import SuggestedFix as SuggestedFix  # noqa: F401

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
