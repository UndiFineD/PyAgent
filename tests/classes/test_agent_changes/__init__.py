# -*- coding: utf-8 -*-
"""Extracted test classes from test_agent_changes.py."""

__all__ = [
    "TestAssociatedFileDetection",
    "TestChangelogAccessControl",
    "TestChangelogApprovalWorkflows",
    "TestChangelogArchivalRetention",
    "TestChangelogBackupRestore",
    "TestChangelogBulkOperations",
    "TestChangelogCategorization",
    "TestChangelogCategoryFiltering",
    "TestChangelogDiffVisualization",
    "TestChangelogDiffing",
    "TestChangelogEntryComments",
    "TestChangelogEntrySigning",
    "TestChangelogExportFormats",
    "TestChangelogHistoryTracking",
    "TestChangelogInternationalization",
    "TestChangelogKeywordSearch",
    "TestChangelogMergingUnittest",
    "TestChangelogNotifications",
    "TestChangelogPriorityOrdering",
    "TestChangelogStatistics",
    "TestChangelogTimestamps",
    "TestChangelogValidationAdvanced",
    "TestChangelogValidationBasic",
    "TestChangelogValidationRules",
    "TestConfiguration",
    "TestCustomTemplatesUnittest",
    "TestDateValidationUnittest",
    "TestDuplicateDetectionUnittest",
    "TestEdgeCasesAndRegression",
    "TestErrorHandlingAdvanced",
    "TestErrorHandlingUnittest",
    "TestFileDetectionUnittest",
    "TestGitIntegrationAdvanced",
    "TestGitIntegrationBasic",
    "TestIntegrationAndAutomation",
    "TestIntegrationBasicUnittest",
    "TestIntegrationWorkflow",
    "TestIssueTrackerLinking",
    "TestMarkdownPreservation",
    "TestPerformanceOptimization",
    "TestQualityAssurance",
    "TestUserExperience",
    "TestVersionManagement",
    "TestVersionParsing",
    "TestVersionRangeQueries",
]

from .core import *  # noqa: F401, F403
from .integration import *  # noqa: F401, F403
from .advanced import *  # noqa: F401, F403
from .edge_cases import *  # noqa: F401, F403
from .performance import *  # noqa: F401, F403
