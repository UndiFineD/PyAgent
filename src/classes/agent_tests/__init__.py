#!/usr/bin/env python3
from __future__ import annotations
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

"""Test agent functionality - extracted classes."""

 from src.core.base.Version import VERSION as VERSION

# Attempt to import rich agent_tests implementations from infra; fall back silently
try:
    from .enums import (
        TestPriority,
        TestStatus,
        CoverageType,
        BrowserType,
        TestSourceType,
        MutationOperator,
        ExecutionMode,
    )

    from .models import (
        TestCase,
        TestRun,
        CoverageGap,
        TestFactory,
        VisualRegressionConfig,
        ContractTest,
        TestEnvironment,
        ExecutionTrace,
        TestDependency,
        CrossBrowserConfig,
        AggregatedResult,
        Mutation,
        GeneratedTest,
        TestProfile,
        ScheduleSlot,
        Recording,
        ReplayResult,
        ProvisionedEnvironment,
        ValidationResult,
        _empty_str_list,
        _empty_dict_any,
        _empty_action_list,
    )

    from .testing_utils import (
        VisualRegressionTester,
        ContractTestRunner,
        ResultAggregator,
        TestMetricsCollector,
    )

    from .optimization import TestSuiteOptimizer, CoverageGapAnalyzer
    from .mutation_testing import MutationTester, MutationRunner
    from .test_generation import TestGenerator, TestCaseMinimizer, TestDocGenerator

    from .debugging import (
        ExecutionReplayer,
        TestProfiler,
        TestRecorder,
        TestReplayer,
    )

    from .environment import EnvironmentProvisioner, DataFactory
    from .dependency_injection import DependencyInjector
    from .scheduling import CrossBrowserRunner, TestScheduler
    from .parallelization import ParallelizationStrategy

    from .test_management import (
        BaselineComparisonResult,
        BaselineManager,
        DIContainer,
        TestPrioritizer,
        FlakinessDetector,
        QuarantineManager,
        ImpactAnalyzer,
        ContractValidator,
    )

    from .agents import TestsAgent
except Exception:
    # If infra-backed modules are missing, keep going with available placeholders
    pass

# Ensure TestsAgent exists (placeholder may live in .agents); import if available
if "TestsAgent" not in globals():
    try:
        from .agents import TestsAgent  # type: ignore
    except Exception:
        class TestsAgent:  # minimal placeholder
            pass

__version__ = VERSION

_all_candidates = [
    # Enums
    "TestPriority", "TestStatus", "CoverageType", "BrowserType", "TestSourceType",
    "MutationOperator", "ExecutionMode",
    # Models
    "TestCase", "TestRun", "CoverageGap", "TestFactory", "VisualRegressionConfig",
    "ContractTest", "TestEnvironment", "ExecutionTrace", "TestDependency",
    "CrossBrowserConfig", "AggregatedResult", "Mutation", "GeneratedTest",
    "TestProfile", "ScheduleSlot", "Recording", "ReplayResult", "ProvisionedEnvironment",
    "ValidationResult",
    # Testing utilities
    "VisualRegressionTester", "ContractTestRunner", "ResultAggregator",
    "TestMetricsCollector",
    # Optimization
    "TestSuiteOptimizer", "CoverageGapAnalyzer",
    # Mutation testing
    "MutationTester", "MutationRunner",
    # Test generation
    "TestGenerator", "TestCaseMinimizer", "TestDocGenerator",
    # Debugging
    "ExecutionReplayer", "TestProfiler", "TestRecorder", "TestReplayer",
    # Environment and data
    "EnvironmentProvisioner", "DataFactory",
    # Dependency injection
    "DependencyInjector",
    # Scheduling
    "CrossBrowserRunner", "TestScheduler",
    # Parallelization
    "ParallelizationStrategy",
    # Test management
    "BaselineComparisonResult", "BaselineManager", "DIContainer", "TestPrioritizer",
    "FlakinessDetector", "QuarantineManager", "ImpactAnalyzer", "ContractValidator",
    # Agents
    "TestsAgent",
]

# Export only names that were actually defined to allow `from module import *` during collection
__all__ = [name for name in _all_candidates if name in globals()]
