#!/usr/bin/env python3

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


"""Test agent functionality - extracted classes."""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

from .agents import TestsAgent  # noqa: F401
from .debugging import (ExecutionReplayer, TestProfiler, TestRecorder,  # noqa: F401
                        TestReplayer)
from .dependency_injection import DependencyInjector  # noqa: F401
from .enums import (BrowserType, CoverageType, ExecutionMode, MutationOperator,  # noqa: F401
                    TestPriority, TestSourceType, TestStatus)
from .environment import DataFactory, EnvironmentProvisioner  # noqa: F401
from .models import (AggregatedResult, ContractTest, CoverageGap,  # noqa: F401
                     CrossBrowserConfig, ExecutionTrace, GeneratedTest,
                     Mutation, ProvisionedEnvironment, Recording, ReplayResult,
                     ScheduleSlot, TestCase, TestDependency, TestEnvironment,
                     TestFactory, TestProfile, TestRun, ValidationResult,
                     VisualRegressionConfig, _empty_action_list,
                     _empty_dict_any, _empty_str_list)
from .mutation_testing import MutationRunner, MutationTester  # noqa: F401
from .optimization import CoverageGapAnalyzer, TestSuiteOptimizer  # noqa: F401
from .parallelization import ParallelizationStrategy  # noqa: F401
from .scheduling import CrossBrowserRunner, TestScheduler  # noqa: F401
from .test_generation import TestCaseMinimizer, TestDocGenerator, TestGenerator  # noqa: F401
from .test_management import (BaselineComparisonResult, BaselineManager,  # noqa: F401
                              ContractValidator, DIContainer,
                              FlakinessDetector, ImpactAnalyzer,
                              QuarantineManager, TestPrioritizer)
from .testing_utils import (ContractTestRunner, ResultAggregator,  # noqa: F401
                            TestMetricsCollector, VisualRegressionTester)

# Enums

# Models

# Testing utilities

# Optimization

# Mutation testing

# Test generation

# Debugging

# Environment and data

# Dependency injection

# Scheduling

# Parallelization

# Test management

# Agents
__version__ = VERSION

__all__ = [
    # Enums
    "TestPriority",
    "TestStatus",
    "CoverageType",
    "BrowserType",
    "TestSourceType",
    "MutationOperator",
    "ExecutionMode",
    # Models
    "TestCase",
    "TestRun",
    "CoverageGap",
    "TestFactory",
    "VisualRegressionConfig",
    "ContractTest",
    "TestEnvironment",
    "ExecutionTrace",
    "TestDependency",
    "CrossBrowserConfig",
    "AggregatedResult",
    "Mutation",
    "GeneratedTest",
    "TestProfile",
    "ScheduleSlot",
    "Recording",
    "ReplayResult",
    "ProvisionedEnvironment",
    "ValidationResult",
    "_empty_str_list",
    "_empty_dict_any",
    "_empty_action_list",
    # Testing utilities
    "VisualRegressionTester",
    "ContractTestRunner",
    "ResultAggregator",
    "TestMetricsCollector",
    # Optimization
    "TestSuiteOptimizer",
    "CoverageGapAnalyzer",
    # Mutation testing
    "MutationTester",
    "MutationRunner",
    # Test generation
    "TestGenerator",
    "TestCaseMinimizer",
    "TestDocGenerator",
    # Debugging
    "ExecutionReplayer",
    "TestProfiler",
    "TestRecorder",
    "TestReplayer",
    # Environment and data
    "EnvironmentProvisioner",
    "DataFactory",
    # Dependency injection
    "DependencyInjector",
    # Scheduling
    "CrossBrowserRunner",
    "TestScheduler",
    # Parallelization
    "ParallelizationStrategy",
    # Test management
    "BaselineComparisonResult",
    "BaselineManager",
    "DIContainer",
    "TestPrioritizer",
    "FlakinessDetector",
    "QuarantineManager",
    "ImpactAnalyzer",
    "ContractValidator",
    # Agents
    "TestsAgent",
]
