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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Test agent functionality - extracted classes."""



# Enums
from .enums import (
    TestPriority, TestStatus, CoverageType, BrowserType, TestSourceType,
    MutationOperator, ExecutionMode
)

# Models
from .models import (
    TestCase, TestRun, CoverageGap, TestFactory, VisualRegressionConfig,
    ContractTest, TestEnvironment, ExecutionTrace, TestDependency,
    CrossBrowserConfig, AggregatedResult, Mutation, GeneratedTest,
    TestProfile, ScheduleSlot, Recording, ReplayResult, ProvisionedEnvironment,
    ValidationResult, _empty_str_list, _empty_dict_any, _empty_action_list
)

# Testing utilities
from .testing_utils import (
    VisualRegressionTester, ContractTestRunner, ResultAggregator,
    TestMetricsCollector
)

# Optimization
from .optimization import TestSuiteOptimizer, CoverageGapAnalyzer

# Mutation testing
from .mutation_testing import MutationTester, MutationRunner

# Test generation
from .test_generation import TestGenerator, TestCaseMinimizer, TestDocGenerator

# Debugging
from .debugging import (
    ExecutionReplayer, TestProfiler, TestRecorder, TestReplayer
)

# Environment and data
from .environment import EnvironmentProvisioner, DataFactory

# Dependency injection
from .dependency_injection import DependencyInjector

# Scheduling
from .scheduling import CrossBrowserRunner, TestScheduler

# Parallelization
from .parallelization import ParallelizationStrategy

# Test management
from .test_management import (
    BaselineComparisonResult, BaselineManager, DIContainer, TestPrioritizer,
    FlakinessDetector, QuarantineManager, ImpactAnalyzer, ContractValidator
)

# Agents
from .agents import TestsAgent

__all__ = [
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
