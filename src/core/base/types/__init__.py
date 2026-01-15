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

"""Domain types for the PyAgent core architecture."""

from __future__ import annotations
from src.core.base.version import VERSION as VERSION
from .AccessibilityIssue import AccessibilityIssue as AccessibilityIssue
from .AccessibilityIssueType import AccessibilityIssueType as AccessibilityIssueType
from .AccessibilityReport import AccessibilityReport as AccessibilityReport
from .AccessibilitySeverity import AccessibilitySeverity as AccessibilitySeverity
from .ARIAAttribute import ARIAAttribute as ARIAAttribute
from .ChangelogEntry import ChangelogEntry as ChangelogEntry
from .CodeLanguage import CodeLanguage as CodeLanguage
from .CodeMetrics import CodeMetrics as CodeMetrics
from .CodeSmell import CodeSmell as CodeSmell
from .ColorContrastResult import ColorContrastResult as ColorContrastResult
from .ComplianceCategory import ComplianceCategory as ComplianceCategory
from .ComplianceResult import ComplianceResult as ComplianceResult
from .ConsistencyIssue import ConsistencyIssue as ConsistencyIssue
from .DependencyNode import DependencyNode as DependencyNode
from .DependencyType import DependencyType as DependencyType
from .DiffResult import DiffResult as DiffResult
from .DiffViewMode import DiffViewMode as DiffViewMode
from .EntryTemplate import EntryTemplate as EntryTemplate
from .FeedFormat import FeedFormat as FeedFormat
from .GroupingStrategy import GroupingStrategy as GroupingStrategy
from .LinkedReference import LinkedReference as LinkedReference
from .LocalizationLanguage import LocalizationLanguage as LocalizationLanguage
from .LocalizedEntry import LocalizedEntry as LocalizedEntry
from .MigrationRule import MigrationRule as MigrationRule
from .MigrationStatus import MigrationStatus as MigrationStatus
from .ModernizationSuggestion import ModernizationSuggestion as ModernizationSuggestion
from .MonorepoEntry import MonorepoEntry as MonorepoEntry
from .OptimizationSuggestion import OptimizationSuggestion as OptimizationSuggestion
from .OptimizationType import OptimizationType as OptimizationType
from .ProfilingCategory import ProfilingCategory as ProfilingCategory
from .ProfilingSuggestion import ProfilingSuggestion as ProfilingSuggestion
from .QualityScore import QualityScore as QualityScore
from .RefactoringPattern import RefactoringPattern as RefactoringPattern
from .ReleaseNote import ReleaseNote as ReleaseNote
from .ReviewCategory import ReviewCategory as ReviewCategory
from .ReviewFinding import ReviewFinding as ReviewFinding
from .SearchResult import SearchResult as SearchResult
from .SecurityIssueType import SecurityIssueType as SecurityIssueType
from .SecurityVulnerability import SecurityVulnerability as SecurityVulnerability
from .StyleRule import StyleRule as StyleRule
from .StyleRuleSeverity import StyleRuleSeverity as StyleRuleSeverity
from .TemplateManager import TemplateManager as TemplateManager
from .TestGap import TestGap as TestGap
from .VersioningStrategy import VersioningStrategy as VersioningStrategy
from .WCAGLevel import WCAGLevel as WCAGLevel

__version__ = VERSION
