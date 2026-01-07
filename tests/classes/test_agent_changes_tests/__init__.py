# -*- coding: utf-8 -*-
"""Extracted test classes from test_agent_changes_tests.py."""

__all__ = [
    "TestBatchProcessing",
    "TestChangelogApprovalWorkflow",
    "TestChangelogArchival",
    "TestChangelogAuthentication",
    "TestChangelogBackupRecovery",
    "TestChangelogConflictResolution",
    "TestChangelogCrossReference",
    "TestChangelogDeduplication",
    "TestChangelogEntryGrouping",
    "TestChangelogEntryPriority",
    "TestChangelogFormatMigration",
    "TestChangelogFromCommits",
    "TestChangelogMetadataExtraction",
    "TestChangelogNotificationTriggers",
    "TestChangelogPerformance",
    "TestChangelogSearchFiltering",
    "TestChangelogTagging",
    "TestChangelogTemplateCustomization",
    "TestChangelogVersioning",
    "TestChangesAggregation",
    "TestChangesCategorization",
    "TestChangesComparison",
    "TestChangesDetection",
    "TestChangesExport",
    "TestChangesFiltering",
    "TestChangesPersistence",
    "TestChangesSummary",
    "TestChangesValidation",
    "TestConcurrency",
    "TestImpactAnalysis",
    "TestIntegrationComprehensive",
    "TestIssuePRLinking",
    "TestNotifications",
    "TestReleaseNotesIntegration",
    "TestVisualizationAndDiff",
]

from .core import *  # noqa: F401, F403
from .integration import *  # noqa: F401, F403
from .performance import *  # noqa: F401, F403
