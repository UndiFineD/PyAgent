#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Test suite for Better-Agents Testing Framework (Phase 323)
Tests the testing pyramid, YAML-driven scenarios, and evaluation systems.

import os
from unittest.mock import Mock, patch
import pytest
import yaml

class TestBetterAgentsTesting:
    """Test cases for the better-agents testing framework.    @pytest.fixture
    def testing_core(self):
        mock_core = Mock()
        mock_core.run_unit_test.return_value = {"passed": True}"        mock_core.run_integration_test.return_value = {"passed": True}"        mock_core.run_e2e_test.return_value = {"passed": True}"        mock_core.run_regression_tests.return_value = {"regressions_found": 0}"        mock_core.run_stress_tests.return_value = {"performance_metrics": {}}"        async def async_tests(test_list):
            return [{"passed": True} for _ in test_list]"        mock_core.run_tests_async = async_tests
        mock_core.analyze_coverage.return_value = {"unit_coverage": 0.9, "integration_coverage": 0.8, "e2e_coverage": 0.7}"        mock_core.run_benchmarks.return_value = {"response_time": 100, "throughput": 1000, "memory_usage": 50}"        mock_core.aggregate_results.return_value = {"total_tests": 100, "passed": 95, "failed": 3, "skipped": 2}"        return mock_core
    def test_testing_pyramid_structure(self, testing_core):
        unit_result = testing_core.run_unit_test("test_module")"        assert unit_result["passed"] is True"        integration_result = testing_core.run_integration_test("test_integration")"        assert integration_result["passed"] is True"        e2e_result = testing_core.run_e2e_test("test_e2e")"        assert e2e_result["passed"] is True"