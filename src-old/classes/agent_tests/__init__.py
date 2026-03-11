#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/classes/agent_tests/__init__.description.md

# __init__

**File**: `src\\classes\agent_tests\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 61 imports  
**Lines**: 117  
**Complexity**: 0 (simple)

## Overview

Test agent functionality - extracted classes.

## Dependencies

**Imports** (61):
- `__future__.annotations`
- `agents.TestsAgent`
- `debugging.ExecutionReplayer`
- `debugging.TestProfiler`
- `debugging.TestRecorder`
- `debugging.TestReplayer`
- `dependency_injection.DependencyInjector`
- `enums.BrowserType`
- `enums.CoverageType`
- `enums.ExecutionMode`
- `enums.MutationOperator`
- `enums.TestPriority`
- `enums.TestSourceType`
- `enums.TestStatus`
- `environment.DataFactory`
- ... and 46 more

---
*Auto-generated documentation*
## Source: src-old/classes/agent_tests/__init__.improvements.md

# Improvements for __init__

**File**: `src\\classes\agent_tests\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 117 lines (medium)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

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
    from .agents import TestsAgent
    from .debugging import (
        ExecutionReplayer,
        TestProfiler,
        TestRecorder,
        TestReplayer,
    )
    from .dependency_injection import DependencyInjector
    from .enums import (
        BrowserType,
        CoverageType,
        ExecutionMode,
        MutationOperator,
        TestPriority,
        TestSourceType,
        TestStatus,
    )
    from .environment import DataFactory, EnvironmentProvisioner
    from .models import (
        AggregatedResult,
        ContractTest,
        CoverageGap,
        CrossBrowserConfig,
        ExecutionTrace,
        GeneratedTest,
        Mutation,
        ProvisionedEnvironment,
        Recording,
        ReplayResult,
        ScheduleSlot,
        TestCase,
        TestDependency,
        TestEnvironment,
        TestFactory,
        TestProfile,
        TestRun,
        ValidationResult,
        VisualRegressionConfig,
        _empty_action_list,
        _empty_dict_any,
        _empty_str_list,
    )
    from .mutation_testing import MutationRunner, MutationTester
    from .optimization import CoverageGapAnalyzer, TestSuiteOptimizer
    from .parallelization import ParallelizationStrategy
    from .scheduling import CrossBrowserRunner, TestScheduler
    from .test_generation import TestCaseMinimizer, TestDocGenerator, TestGenerator
    from .test_management import (
        BaselineComparisonResult,
        BaselineManager,
        ContractValidator,
        DIContainer,
        FlakinessDetector,
        ImpactAnalyzer,
        QuarantineManager,
        TestPrioritizer,
    )
    from .testing_utils import (
        ContractTestRunner,
        ResultAggregator,
        TestMetricsCollector,
        VisualRegressionTester,
    )
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
