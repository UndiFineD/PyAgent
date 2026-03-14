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

r"""LLM_CONTEXT_START

## Source: src-old/core/testing/framework.description.md

# framework

**File**: `src\\core\testing\framework.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 0 imports  
**Lines**: 635  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for framework.

---
*Auto-generated documentation*
## Source: src-old/core/testing/framework.improvements.md

# Improvements for framework

**File**: `src\\core\testing\framework.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 635 lines (large)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `framework_test.py` with pytest tests

### File Complexity
- [!] **Large file** (635 lines) - Consider refactoring

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""


import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest
import yaml

logger = logging.getLogger("pyagent.testing.framework")


class TestType(Enum):
    """Types of tests in the testing pyramid."""

    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"


class TestStatus(Enum):
    """Test execution status."""

    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    TIMEOUT = "timeout"


@dataclass
class TestResult:
    """Result of a test execution."""

    test_id: str
    test_type: TestType
    status: TestStatus
    duration: float
    output: str
    error_message: Optional[str] = None
    coverage: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class TestScenario:
    """Test scenario configuration."""

    name: str
    description: str
    test_type: TestType
    agent_class: str
    input_data: Dict[str, Any]
    expected_output: Dict[str, Any]
    timeout: int = 30
    tags: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)


@dataclass
class TestSuite:
    """Collection of test scenarios."""

    name: str
    description: str
    scenarios: List[TestScenario]
    setup_steps: List[Dict[str, Any]] = field(default_factory=list)
    teardown_steps: List[Dict[str, Any]] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


class AgentTestingPyramidCore:
    """Testing Pyramid Core.

    Implements unit, integration, and E2E testing infrastructure.
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.test_results: List[TestResult] = []
        self.logger = logging.getLogger("pyagent.testing.pyramid")

        # Test directories
        self.unit_tests = project_root / "tests" / "unit"
        self.integration_tests = project_root / "tests" / "integration"
        self.e2e_tests = project_root / "tests" / "e2e"
        self.scenarios_dir = project_root / "tests" / "scenarios"

        # Create directories if they don't exist
        for dir_path in [self.unit_tests, self.integration_tests, self.e2e_tests, self.scenarios_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

    async def run_test_pyramid(self, test_filter: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the complete testing pyramid.

        Args:
            test_filter: Optional filter for test selection
        Returns:
            Test execution summary

        """
        self.logger.info("Starting Agent Testing Pyramid execution")
        start_time = time.time()

        # Run tests in order: unit -> integration -> e2e
        results = {
            'unit': await self._run_unit_tests(test_filter),
            'integration': await self._run_integration_tests(test_filter),
            'e2e': await self._run_e2e_tests(test_filter),
            'performance': await self._run_performance_tests(test_filter),
            'security': await self._run_security_tests(test_filter)
        }

        total_time = time.time() - start_time
        # Generate summary
        summary = self._generate_test_summary(results, total_time)
        self.logger.info(f"Testing Pyramid complete in {total_time:.2f}s")
        return summary

    async def _run_unit_tests(self, test_filter: Optional[Dict[str, Any]] = None) -> List[TestResult]:
        """Run unit tests."""
        self.logger.info("Running unit tests")
        results = []
        # Discover and run unit tests
        test_files = list(self.unit_tests.glob("test_*.py"))
        for test_file in test_files:
            if self._matches_filter(test_file, test_filter):
                result = await self._run_pytest_file(test_file, TestType.UNIT)
                results.append(result)

        return results

    async def _run_integration_tests(self, test_filter: Optional[Dict[str, Any]] = None) -> List[TestResult]:
        """Run integration tests."""
        self.logger.info("Running integration tests")
        results = []
        # Discover and run integration tests
        test_files = list(self.integration_tests.glob("test_*.py"))
        for test_file in test_files:
            if self._matches_filter(test_file, test_filter):
                result = await self._run_pytest_file(test_file, TestType.INTEGRATION)
                results.append(result)

        return results

    async def _run_e2e_tests(self, test_filter: Optional[Dict[str, Any]] = None) -> List[TestResult]:
        """Run end-to-end tests."""
        self.logger.info("Running E2E tests")
        results = []
        # Load and run scenario-based E2E tests
        scenario_files = list(self.scenarios_dir.glob("*.yaml"))
        for scenario_file in scenario_files:
            if self._matches_filter(scenario_file, test_filter):
                scenario_results = await self.run_scenario_tests(scenario_file)
                results.extend(scenario_results)

        return results

    async def _run_performance_tests(self, test_filter: Optional[Dict[str, Any]] = None) -> List[TestResult]:
        """Run performance tests."""
        self.logger.info("Running performance tests")
        results = []
        # test_filter parameter available for future filtering implementation
        _ = test_filter  # Acknowledge parameter for linting
        # Discover and run performance tests
        # Implement performance test discovery and execution
        return results

    async def _run_security_tests(self, test_filter: Optional[Dict[str, Any]] = None) -> List[TestResult]:
        """Run security tests."""
        self.logger.info("Running security tests")
        results = []
        # test_filter parameter available for future filtering implementation
        _ = test_filter  # Acknowledge parameter for linting
        # Discover and run security tests
        # Implement security test discovery and execution
        return results

    def _matches_filter(self, test_path: Path, test_filter: Optional[Dict[str, Any]]) -> bool:
        """Check if test matches the filter criteria."""
        if not test_filter:
            return True

        # Check tags
        if 'tags' in test_filter:
            # This would require parsing test files for tags
            # Placeholder implementation
            pass

        # Check test type
        if 'type' in test_filter:
            if test_filter['type'] == 'unit' and 'unit' not in str(test_path):
                return False
            if test_filter['type'] == 'integration' and 'integration' not in str(test_path):
                return False
            if test_filter['type'] == 'e2e' and 'scenarios' not in str(test_path):
                return False

        return True

    async def _run_pytest_file(self, test_file: Path, test_type: TestType) -> TestResult:
        """Run a pytest file and return results."""
        start_time = time.time()
        try:
            # Run pytest programmatically
            result = pytest.main([
                str(test_file),
                "--tb=short",
                "--capture=no",
                "-v"
            ])
            duration = time.time() - start_time
            status = TestStatus.PASSED if result == 0 else TestStatus.FAILED
            return TestResult(
                test_id=str(test_file),
                test_type=test_type,
                status=status,
                duration=duration,
                output="",  # Would capture output in real implementation
                metadata={"exit_code": result}
            )

        except (OSError, RuntimeError, ValueError) as e:
            duration = time.time() - start_time
            return TestResult(
                test_id=str(test_file),
                test_type=test_type,
                status=TestStatus.ERROR,
                duration=duration,
                output="",
                error_message=str(e)
            )

    async def run_scenario_tests(self, scenario_file: Path) -> List[TestResult]:
        """Run scenario-based E2E tests."""
        results = []
        try:
            # Load scenario configuration
            with open(scenario_file, 'r', encoding='utf-8') as f:
                scenario_data = yaml.safe_load(f)

            suite = TestSuite(**scenario_data)

            for scenario in suite.scenarios:
                result = await self._run_single_scenario(scenario)
                results.append(result)

        except (OSError, IOError, yaml.YAMLError, TypeError, ValueError) as e:
            self.logger.error(f"Failed to run scenario {scenario_file}: {e}")

        return results

    async def _run_single_scenario(self, scenario: TestScenario) -> TestResult:
        """Run a single test scenario."""
        start_time = time.time()

        try:
            # Import the agent class dynamically
            module_name, class_name = scenario.agent_class.rsplit('.', 1)
            module = __import__(module_name, fromlist=[class_name])
            agent_class = getattr(module, class_name)

            # Create agent instance
            agent = agent_class()

            # Run the scenario
            result = await agent.process_input(scenario.input_data)

            # Validate result
            success = self._validate_scenario_result(result, scenario.expected_output)

            duration = time.time() - start_time

            return TestResult(
                test_id=scenario.name,
                test_type=TestType.E2E,
                status=TestStatus.PASSED if success else TestStatus.FAILED,
                duration=duration,
                output=json.dumps(result, indent=2),
                metadata={
                    "scenario": scenario.name,
                    "agent_class": scenario.agent_class,
                    "input": scenario.input_data,
                    "expected": scenario.expected_output,
                    "actual": result
                }
            )

        except (ImportError, AttributeError, TypeError, ValueError, RuntimeError) as e:
            duration = time.time() - start_time
            return TestResult(
                test_id=scenario.name,
                test_type=TestType.E2E,
                status=TestStatus.ERROR,
                duration=duration,
                output="",
                error_message=str(e)
            )

    def _validate_scenario_result(self, actual: Any, expected: Dict[str, Any]) -> bool:
        """Validate scenario result against expected output."""
        try:
            # Simple validation - check if expected keys are present
            if isinstance(expected, dict) and isinstance(actual, dict):
                for key, value in expected.items():
                    if key not in actual:
                        return False
                    if isinstance(value, dict):
                        if not self._validate_scenario_result(actual[key], value):
                            return False
                    elif actual[key] != value:
                        return False
                return True
            else:
                return actual == expected
        except (TypeError, KeyError, AttributeError):
            return False

    def _generate_test_summary(self, results: Dict[str, List[TestResult]], total_time: float) -> Dict[str, Any]:
        """Generate comprehensive test summary."""
        summary = {
            'total_time': total_time,
            'timestamp': time.time(),
            'results': {}
        }

        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_errors = 0

        for test_type, test_results in results.items():
            type_summary = {
                'count': len(test_results),
                'passed': len([r for r in test_results if r.status == TestStatus.PASSED]),
                'failed': len([r for r in test_results if r.status == TestStatus.FAILED]),
                'errors': len([r for r in test_results if r.status == TestStatus.ERROR]),
                'skipped': len([r for r in test_results if r.status == TestStatus.SKIPPED]),
                'average_duration': sum(r.duration for r in test_results) / len(test_results) if test_results else 0
            }

            summary['results'][test_type] = type_summary

            total_tests += type_summary['count']
            total_passed += type_summary['passed']
            total_failed += type_summary['failed']
            total_errors += type_summary['errors']

        summary.update({
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'total_errors': total_errors,
            'success_rate': total_passed / total_tests if total_tests > 0 else 0
        })

        return summary


class ScenarioTestingEngine:
    """YAML-driven scenario testing engine.

    Enables complex agent behavior testing through declarative scenarios.
    """

    def __init__(self, testing_core: AgentTestingPyramidCore):
        self.testing_core = testing_core
        self.logger = logging.getLogger("pyagent.testing.scenarios")

    def create_scenario_template(self, name: str, description: str) -> str:
        """Create a YAML template for a test scenario."""
        template = f"""
name: {name}
description: {description}
scenarios:
  - name: example_scenario
    description: Example test scenario
    test_type: e2e
    agent_class: src.logic.agents.example.ExampleAgent
    input_data:
      message: "Hello, agent!"
      context: {{}}
    expected_output:
      response: "Hello, human!"
      confidence: 0.9
    timeout: 30
    tags:
      - example
      - basic
    prerequisites: []
    environment:
      DEBUG: "true"
setup_steps: []
teardown_steps: []
tags:
  - {name}
"""
        return template

    async def run_scenario_file(self, scenario_path: Path) -> List[TestResult]:
        """
        """
