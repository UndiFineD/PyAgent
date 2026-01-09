#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");

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
