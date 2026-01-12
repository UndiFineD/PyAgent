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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Domain types for the PyAgent core architecture."""



from .AccessibilityIssue import AccessibilityIssue
from .AccessibilityIssueType import AccessibilityIssueType
from .AccessibilityReport import AccessibilityReport
from .AccessibilitySeverity import AccessibilitySeverity
from .ARIAAttribute import ARIAAttribute
from .ChangelogEntry import ChangelogEntry
from .CodeLanguage import CodeLanguage
from .CodeMetrics import CodeMetrics
from .CodeSmell import CodeSmell
from .ColorContrastResult import ColorContrastResult
from .ComplianceCategory import ComplianceCategory
from .ComplianceResult import ComplianceResult
from .ConsistencyIssue import ConsistencyIssue
from .DependencyNode import DependencyNode
from .DependencyType import DependencyType
from .DiffResult import DiffResult
from .DiffViewMode import DiffViewMode
from .EntryTemplate import EntryTemplate
from .FeedFormat import FeedFormat
from .GroupingStrategy import GroupingStrategy
from .LinkedReference import LinkedReference
from .LocalizationLanguage import LocalizationLanguage
from .LocalizedEntry import LocalizedEntry
from .MigrationRule import MigrationRule
from .MigrationStatus import MigrationStatus
from .ModernizationSuggestion import ModernizationSuggestion
from .MonorepoEntry import MonorepoEntry
from .OptimizationSuggestion import OptimizationSuggestion
from .OptimizationType import OptimizationType
from .ProfilingCategory import ProfilingCategory
from .ProfilingSuggestion import ProfilingSuggestion
from .QualityScore import QualityScore
from .RefactoringPattern import RefactoringPattern
from .ReleaseNote import ReleaseNote
from .ReviewCategory import ReviewCategory
from .ReviewFinding import ReviewFinding
from .SearchResult import SearchResult
from .SecurityIssueType import SecurityIssueType
from .SecurityVulnerability import SecurityVulnerability
from .StyleRule import StyleRule
from .StyleRuleSeverity import StyleRuleSeverity
from .TemplateManager import TemplateManager
from .TestGap import TestGap
from .VersioningStrategy import VersioningStrategy
from .WCAGLevel import WCAGLevel
