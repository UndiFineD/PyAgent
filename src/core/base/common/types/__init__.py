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


"""Domain types for the PyAgent core architecture."""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .accessibility_issue import AccessibilityIssue  # noqa: F401
from .accessibility_issue_type import AccessibilityIssueType  # noqa: F401
from .accessibility_report import AccessibilityReport  # noqa: F401
from .accessibility_severity import AccessibilitySeverity  # noqa: F401
from .aria_attribute import ARIAAttribute  # noqa: F401
from .changelog_entry import ChangelogEntry  # noqa: F401
from .code_language import CodeLanguage  # noqa: F401
from .code_metrics import CodeMetrics  # noqa: F401
from .code_smell import CodeSmell  # noqa: F401
from .color_contrast_result import ColorContrastResult  # noqa: F401
from .compliance_category import ComplianceCategory  # noqa: F401
from .compliance_result import ComplianceResult  # noqa: F401
from .consistency_issue import ConsistencyIssue  # noqa: F401
from .dependency_node import DependencyNode  # noqa: F401
from .dependency_type import DependencyType  # noqa: F401
from .diff_result import DiffResult  # noqa: F401
from .diff_view_mode import DiffViewMode  # noqa: F401
from .entry_template import EntryTemplate  # noqa: F401
from .feed_format import FeedFormat  # noqa: F401
from .grouping_strategy import GroupingStrategy  # noqa: F401
from .linked_reference import LinkedReference  # noqa: F401
from .localization_language import LocalizationLanguage  # noqa: F401
from .localized_entry import LocalizedEntry  # noqa: F401
from .migration_rule import MigrationRule  # noqa: F401
from .migration_status import MigrationStatus  # noqa: F401
from .modernization_suggestion import ModernizationSuggestion  # noqa: F401
from .monorepo_entry import MonorepoEntry  # noqa: F401
from .optimization_suggestion import OptimizationSuggestion  # noqa: F401
from .optimization_type import OptimizationType  # noqa: F401
from .profiling_category import ProfilingCategory  # noqa: F401
from .profiling_suggestion import ProfilingSuggestion  # noqa: F401
from .quality_score import QualityScore  # noqa: F401
from .refactoring_pattern import RefactoringPattern  # noqa: F401
from .release_note import ReleaseNote  # noqa: F401
from .review_category import ReviewCategory  # noqa: F401
from .review_finding import ReviewFinding  # noqa: F401
from .search_result import SearchResult  # noqa: F401
from .security_issue_type import SecurityIssueType  # noqa: F401
from .security_vulnerability import SecurityVulnerability  # noqa: F401
from .style_rule import StyleRule  # noqa: F401
from .style_rule_severity import StyleRuleSeverity  # noqa: F401
from .template_manager import TemplateManager  # noqa: F401
from .test_gap import TestGap  # noqa: F401
from .versioning_strategy import VersioningStrategy  # noqa: F401
from .wcag_level import WCAGLevel  # noqa: F401

__version__ = VERSION
__all__ = [
    "AccessibilityIssue",
    "AccessibilityIssueType",
    "AccessibilityReport",
    "AccessibilitySeverity",
    "ARIAAttribute",
    "ChangelogEntry",
    "CodeLanguage",
    "CodeMetrics",
    "CodeSmell",
    "ColorContrastResult",
    "ComplianceCategory",
    "ComplianceResult",
    "ConsistencyIssue",
    "DependencyNode",
    "DependencyType",
    "DiffResult",
    "DiffViewMode",
    "EntryTemplate",
    "FeedFormat",
    "GroupingStrategy",
    "LinkedReference",
    "LocalizationLanguage",
    "LocalizedEntry",
    "MigrationRule",
    "MigrationStatus",
    "ModernizationSuggestion",
    "MonorepoEntry",
    "OptimizationSuggestion",
    "OptimizationType",
    "ProfilingCategory",
    "ProfilingSuggestion",
    "QualityScore",
    "RefactoringPattern",
    "ReleaseNote",
    "ReviewCategory",
    "ReviewFinding",
    "SearchResult",
    "SecurityIssueType",
    "SecurityVulnerability",
    "StyleRule",
    "StyleRuleSeverity",
    "TemplateManager",
    "TestGap",
    "VersioningStrategy",
    "WCAGLevel",
]
