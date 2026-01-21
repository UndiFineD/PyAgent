# -*- coding: utf-8 -*-
"""Extracted test classes from test_agent_coder.py."""

__all__ = [
    "TestAIRetryAndErrorRecovery",
    "TestAPICompatibility",
    "TestARIAAttributeDataclass",
    "TestAccessibilityAnalyzer",
    "TestAccessibilityIssueDataclass",
    "TestAccessibilityIssueTypeEnum",
    "TestAccessibilityReportDataclass",
    "TestAccessibilitySeverityEnum",
    "TestAdvancedCodeFormatting",
    "TestAdvancedSecurityValidation",
    "TestBackupCreation",
    "TestCodeComplexity",
    "TestCodeConsistency",
    "TestCodeDocumentationGeneration",
    "TestCodeFormatting",
    "TestCodeMetrics",
    "TestCodeOptimizationPatterns",
    "TestCodeQualityValidation",
    "TestCodeRefactoring",
    "TestCodeSplitting",
    "TestCodeTemplates",
    "TestColorContrastResultDataclass",
    "TestComplexityAnalysis",
    "TestConcurrency",
    "TestCoverageGapDetection",
    "TestDeadCodeDetection",
    "TestDependencyInjectionPatterns",
    "TestDiffApplication",
    "TestDocstringGeneration",
    "TestErrorRecovery",
    "TestFlake8Integration",
    "TestImportOrganization",
    "TestIncrementalImprovement",
    "TestIntegration",
    "TestLargeFileHandling",
    "TestMergeConflictResolution",
    "TestMigrationAutomation",
    "TestMultiLanguageCodeGeneration",
    "TestPerformanceProfiling",
    "TestQualityGates",
    "TestRollback",
    "TestSecurityScanning",
    "TestSecurityScanningIntegration",
    "TestStyleUnification",
    "TestSyntaxValidation",
    "TestTypeAnnotationInference",
    "TestWCAGLevelEnum",
]

from .test_coder_unit import *  # noqa: F401, F403
from .test_coder_core_unit import *  # noqa: F401, F403
from .test_agent_unit import *  # noqa: F401, F403
from .test_agent_core_unit import *  # noqa: F401, F403
from .test_agent_advanced_unit import *  # noqa: F401, F403
from .advanced import *  # noqa: F401, F403
from .edge_cases import *  # noqa: F401, F403
