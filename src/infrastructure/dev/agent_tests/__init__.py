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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Test agent functionality - extracted classes."""

from __future__ import annotations
from src.core.base.version import VERSION as VERSION
from .enums import (
    TestPriority, TestStatus, CoverageType, BrowserType, TestSourceType,
    MutationOperator, ExecutionMode
)
from .models import (
    TestCase, TestRun, CoverageGap, TestFactory, VisualRegressionConfig,
    ContractTest, TestEnvironment, ExecutionTrace, TestDependency,
    CrossBrowserConfig, AggregatedResult, Mutation, GeneratedTest,
    TestProfile, ScheduleSlot, Recording, ReplayResult, ProvisionedEnvironment,
    ValidationResult, _empty_str_list, _empty_dict_any, _empty_action_list
)
from .testing_utils import (
    VisualRegressionTester, ContractTestRunner, ResultAggregator,
    TestMetricsCollector
)
from .optimization import TestSuiteOptimizer, CoverageGapAnalyzer
from .mutation_testing import MutationTester, MutationRunner
from .test_generation import TestGenerator, TestCaseMinimizer, TestDocGenerator
from .debugging import (
    ExecutionReplayer, TestProfiler, TestRecorder, TestReplayer
)
from .environment import EnvironmentProvisioner, DataFactory
from .dependency_injection import DependencyInjector as DependencyInjector
from .scheduling import CrossBrowserRunner, TestScheduler
from .parallelization import ParallelizationStrategy as ParallelizationStrategy
from .test_management import (
    BaselineComparisonResult, BaselineManager, DIContainer, TestPrioritizer,
    FlakinessDetector, QuarantineManager, ImpactAnalyzer, ContractValidator
)
from .agents import TestsAgent as TestsAgent

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