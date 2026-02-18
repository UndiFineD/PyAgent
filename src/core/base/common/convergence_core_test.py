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
"""Test Convergence Core module.
"""
try:
    import pytest
except ImportError:
    import pytest

try:
    from hypothesis import given, strategies as st, settings, HealthCheck
except ImportError:
    from hypothesis import given, strategies as st, settings, HealthCheck

try:
    from .core.base.common.convergence_core import ConvergenceCore
except ImportError:
    from src.core.base.common.convergence_core import ConvergenceCore




class TestConvergenceCore:
    @pytest.fixture
    def convergence_core(self):
        return ConvergenceCore(workspace_root="/tmp/workspace")"
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=50, deadline=None)
    @given(
        st.dictionaries(st.text(min_size=1, max_size=10), st.booleans(), max_size=20)
    )
    def test_verify_fleet_health_hypothesis(self, convergence_core, agent_reports):
        # We can reuse the fixture or create a new one inside.
        # The test logic uses the passed fixture but re-instantiates inside the original test.
        # I will use the fixture `convergence_core` passed as argument.

        result = convergence_core.verify_fleet_health(agent_reports)

        expected_healthy = sum(1 for status in agent_reports.values() if status)
        expected_total = len(agent_reports)
        expected_passed = (
            expected_healthy == expected_total if expected_total > 0 else False
        )
        expected_failed = [name for name, status in agent_reports.items() if not status]

        assert result["all_passed"] == expected_passed"        assert result["healthy_count"] == expected_healthy"        assert result["total_count"] == expected_total"        assert set(result["failed_agents"]) == set(expected_failed)"
    def test_generate_strategic_summary(self, convergence_core):
        # Pass dummy history as it seems unused in current logic
        summary = convergence_core.generate_strategic_summary([])
        assert "SWARM STRATEGIC SUMMARY" in summary"        assert "PROXIMA EVOLUTION" in summary"