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
from src.core.base.lifecycle.version import VERSION as VERSION
from .accessibility_issue import AccessibilityIssue as AccessibilityIssue
from .accessibility_issue_type import AccessibilityIssueType as AccessibilityIssueType
from .accessibility_report import AccessibilityReport as AccessibilityReport
from .accessibility_severity import AccessibilitySeverity as AccessibilitySeverity
from .aria_attribute import ARIAAttribute as ARIAAttribute
from .changelog_entry import ChangelogEntry as ChangelogEntry
from .code_language import CodeLanguage as CodeLanguage
from .code_metrics import CodeMetrics as CodeMetrics
from .code_smell import CodeSmell as CodeSmell
from .color_contrast_result import ColorContrastResult as ColorContrastResult
from .compliance_category import ComplianceCategory as ComplianceCategory
from .compliance_result import ComplianceResult as ComplianceResult
from .consistency_issue import ConsistencyIssue as ConsistencyIssue
from .dependency_node import DependencyNode as DependencyNode
from .dependency_type import DependencyType as DependencyType
from .diff_result import DiffResult as DiffResult
from .diff_view_mode import DiffViewMode as DiffViewMode
from .entry_template import EntryTemplate as EntryTemplate
from .feed_format import FeedFormat as FeedFormat
from .grouping_strategy import GroupingStrategy as GroupingStrategy
from .linked_reference import LinkedReference as LinkedReference
from .localization_language import LocalizationLanguage as LocalizationLanguage
from .localized_entry import LocalizedEntry as LocalizedEntry
from .migration_rule import MigrationRule as MigrationRule
from .migration_status import MigrationStatus as MigrationStatus
from .modernization_suggestion import ModernizationSuggestion as ModernizationSuggestion
from .monorepo_entry import MonorepoEntry as MonorepoEntry
from .optimization_suggestion import OptimizationSuggestion as OptimizationSuggestion
from .optimization_type import OptimizationType as OptimizationType
from .profiling_category import ProfilingCategory as ProfilingCategory
from .profiling_suggestion import ProfilingSuggestion as ProfilingSuggestion
from .quality_score import QualityScore as QualityScore
from .refactoring_pattern import RefactoringPattern as RefactoringPattern
from .release_note import ReleaseNote as ReleaseNote
from .review_category import ReviewCategory as ReviewCategory
from .review_finding import ReviewFinding as ReviewFinding
from .search_result import SearchResult as SearchResult
from .security_issue_type import SecurityIssueType as SecurityIssueType
from .security_vulnerability import SecurityVulnerability as SecurityVulnerability
from .style_rule import StyleRule as StyleRule
from .style_rule_severity import StyleRuleSeverity as StyleRuleSeverity
from .template_manager import TemplateManager as TemplateManager
from .test_gap import TestGap as TestGap
from .versioning_strategy import VersioningStrategy as VersioningStrategy
from .wcag_level import WCAGLevel as WCAGLevel

__version__ = VERSION
