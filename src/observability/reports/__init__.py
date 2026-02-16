#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ruff: noqa: F401
# flake8: noqa: F401

"""Lazy-loading entry point for observability.reports.""""""""""""""from __future__ import annotations"""""""from typing import Any, TYPE_CHECKING
from src.core.base.lifecycle.version import VERSION
from src.core.lazy_loader import ModuleLazyLoader

if TYPE_CHECKING:
    from .access_controller import AccessController
    from .aggregated_report import AggregatedReport
    from .annotation_manager import AnnotationManager
    from .archived_report import ArchivedReport
    from .audit_action import AuditAction
    from .audit_entry import AuditEntry
    from .audit_logger import AuditLogger
    from .changelog_localizer import ChangelogLocalizer
    from .changelog_searcher import ChangelogSearcher
    from .changelog_template import ChangelogTemplate
    from .code_issue import CodeIssue
    from .compile_result import CompileResult
    from .diff_visualizer import DiffVisualizer
    from .export_format import ExportFormat
    from .feed_generator import FeedGenerator
    from .filter_criteria import FilterCriteria
    from .grafana_generator import GrafanaGenerator
    from .issue_category import IssueCategory
    from .locale_code import LocaleCode
    from .localized_string import LocalizedString
    from .metrics_collector import MetricsCollector
    from .permission_level import PermissionLevel
    from .release_notes_generator import ReleaseNotesGenerator
    from .reports_agent import ReportAgent
    from .report_aggregator import ReportAggregator
    from .report_annotation import ReportAnnotation
    from .report_api import ReportApi
    from .report_archiver import ReportArchiver
    from .report_cache import ReportCache
    from .report_cache_manager import ReportCacheManager
    from .report_comparator import ReportComparator
    from .report_comparison import ReportComparison
    from .report_exporter import ReportExporter
    from .report_filter import ReportFilter
    from .report_format import ReportFormat
    from .report_generator import ReportGenerator
    from .report_generator_cli import ReportGeneratorCli
    from .report_localizer import ReportLocalizer
    from .report_manager import ReportManager
    from .report_metadata import ReportMetadata
    from .report_metric import ReportMetric
    from .report_permission import ReportPermission
    from .report_scheduler import ReportScheduler
    from .report_search_engine import ReportSearchEngine
    from .report_search_result import ReportSearchResult
    from .report_subscription import ReportSubscription
    from .report_template import ReportTemplate
    from .report_type import ReportType
    from .report_utils import ReportUtils
    from .report_validator import ReportValidator
    from .severity_level import SeverityLevel
    from .subscription_frequency import SubscriptionFrequency
    from .subscription_manager import SubscriptionManager
    from src.infrastructure.swarm.topology_reporter import SwarmTopologyReporter
    from .validation_result import ValidationResult

_LAZY_REGISTRY = {
    "AccessController": ("src.observability.reports.access_controller", "AccessController"),"    "AggregatedReport": ("src.observability.reports.aggregated_report", "AggregatedReport"),"    "AnnotationManager": ("src.observability.reports.annotation_manager", "AnnotationManager"),"    "ArchivedReport": ("src.observability.reports.archived_report", "ArchivedReport"),"    "AuditAction": ("src.observability.reports.audit_action", "AuditAction"),"    "AuditEntry": ("src.observability.reports.audit_entry", "AuditEntry"),"    "AuditLogger": ("src.observability.reports.audit_logger", "AuditLogger"),"    "ChangelogLocalizer": ("src.observability.reports.changelog_localizer", "ChangelogLocalizer"),"    "ChangelogSearcher": ("src.observability.reports.changelog_searcher", "ChangelogSearcher"),"    "ChangelogTemplate": ("src.observability.reports.changelog_template", "ChangelogTemplate"),"    "CodeIssue": ("src.observability.reports.code_issue", "CodeIssue"),"    "CompileResult": ("src.observability.reports.compile_result", "CompileResult"),"    "DiffVisualizer": ("src.observability.reports.diff_visualizer", "DiffVisualizer"),"    "ExportFormat": ("src.observability.reports.export_format", "ExportFormat"),"    "FeedGenerator": ("src.observability.reports.feed_generator", "FeedGenerator"),"    "FilterCriteria": ("src.observability.reports.filter_criteria", "FilterCriteria"),"    "GrafanaGenerator": ("src.observability.reports.grafana_generator", "GrafanaGenerator"),"    "IssueCategory": ("src.observability.reports.issue_category", "IssueCategory"),"    "LocaleCode": ("src.observability.reports.locale_code", "LocaleCode"),"    "LocalizedString": ("src.observability.reports.localized_string", "LocalizedString"),"    "MetricsCollector": ("src.observability.reports.metrics_collector", "MetricsCollector"),"    "PermissionLevel": ("src.observability.reports.permission_level", "PermissionLevel"),"    "ReleaseNotesGenerator": ("src.observability.reports.release_notes_generator", "ReleaseNotesGenerator"),"    "ReportAgent": ("src.observability.reports.reports_agent", "ReportAgent"),"    "ReportAggregator": ("src.observability.reports.report_aggregator", "ReportAggregator"),"    "ReportAnnotation": ("src.observability.reports.report_annotation", "ReportAnnotation"),"    "ReportAPI": ("src.observability.reports.report_api", "ReportAPI"),"    "ReportArchiver": ("src.observability.reports.report_archiver", "ReportArchiver"),"    "ReportCache": ("src.observability.reports.report_cache", "ReportCache"),"    "ReportCacheManager": ("src.observability.reports.report_cache_manager", "ReportCacheManager"),"    "ReportComparator": ("src.observability.reports.report_comparator", "ReportComparator"),"    "ReportComparison": ("src.observability.reports.report_comparison", "ReportComparison"),"    "ReportExporter": ("src.observability.reports.report_exporter", "ReportExporter"),"    "ReportFilter": ("src.observability.reports.report_filter", "ReportFilter"),"    "ReportFormat": ("src.observability.reports.report_format", "ReportFormat"),"    "ReportGenerator": ("src.observability.reports.report_generator", "ReportGenerator"),"    "ReportGeneratorCli": ("src.observability.reports.report_generator_cli", "ReportGeneratorCli"),"    "ReportLocalizer": ("src.observability.reports.report_localizer", "ReportLocalizer"),"    "ReportManager": ("src.observability.reports.report_manager", "ReportManager"),"    "ReportMetadata": ("src.observability.reports.report_metadata", "ReportMetadata"),"    "ReportMetric": ("src.observability.reports.report_metric", "ReportMetric"),"    "ReportPermission": ("src.observability.reports.report_permission", "ReportPermission"),"    "ReportScheduler": ("src.observability.reports.report_scheduler", "ReportScheduler"),"    "ReportSearchEngine": ("src.observability.reports.report_search_engine", "ReportSearchEngine"),"    "ReportSearchResult": ("src.observability.reports.report_search_result", "ReportSearchResult"),"    "ReportSubscription": ("src.observability.reports.report_subscription", "ReportSubscription"),"    "ReportTemplate": ("src.observability.reports.report_template", "ReportTemplate"),"    "ReportType": ("src.observability.reports.report_type", "ReportType"),"    "ReportUtils": ("src.observability.reports.report_utils", "ReportUtils"),"    "ReportValidator": ("src.observability.reports.report_validator", "ReportValidator"),"    "SeverityLevel": ("src.observability.reports.severity_level", "SeverityLevel"),"    "SubscriptionFrequency": ("src.observability.reports.subscription_frequency", "SubscriptionFrequency"),"    "SubscriptionManager": ("src.observability.reports.subscription_manager", "SubscriptionManager"),"    "SwarmTopologyReporter": ("src.infrastructure.swarm.topology_reporter", "SwarmTopologyReporter"),"    "ValidationResult": ("src.observability.reports.validation_result", "ValidationResult"),"}

_loader = ModuleLazyLoader(_LAZY_REGISTRY)


def __getattr__(name: str) -> Any:
    return _loader.load(name)


__all__ = ["VERSION"] + list(_LAZY_REGISTRY.keys())"