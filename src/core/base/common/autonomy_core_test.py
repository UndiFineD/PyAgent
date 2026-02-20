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
"""
"""
Test Autonomy Core module.
"""
try:

"""
import pytest
except ImportError:
    import pytest

try:
    from hypothesis import given, strategies as st, settings, HealthCheck
except ImportError:
    from hypothesis import given, strategies as st, settings, HealthCheck

try:
    from .core.base.common.autonomy_core import AutonomyCore
except ImportError:
    from src.core.base.common.autonomy_core import AutonomyCore




class TestAutonomyCore:
    @pytest.fixture
    def core(self):
        return AutonomyCore("test_agent_01")
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        success_rate=st.floats(min_value=0.0, max_value=1.0),
        task_diversity=st.floats(min_value=0.0, max_value=1.0),
    )
    def test_identify_blind_spots(self, core, success_rate, task_diversity):
        blind_spots = core.identify_blind_spots(success_rate, task_diversity)
        if success_rate < 0.7:
            assert "GENERAL_REASONING_RELIABILITY" in blind_spots
        else:
            assert "GENERAL_REASONING_RELIABILITY" not in blind_spots

        if task_diversity < 0.3:
            assert "DOMAIN_SPECIFIC_RIGIDITY" in blind_spots
        else:
            assert "DOMAIN_SPECIFIC_RIGIDITY" not in blind_spots
    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(st.floats(min_value=0.0, max_value=2.0))
    def test_calculate_daemon_sleep_interval(self, core, optimization_score):
        interval = core.calculate_daemon_sleep_interval(optimization_score)

        if optimization_score >= 1.0:
            assert interval == 3600
        elif optimization_score > 0.8:
            assert interval == 600
        else:
            assert interval == 60

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(st.lists(st.text(min_size=1, max_size=50), min_size=0, max_size=5))
    def test_generate_self_improvement_plan(self, core, blind_spots):
        plan = core.generate_self_improvement_plan(blind_spots)
        # plan may be a string or dict-like; do basic checks
        assert core.agent_id in str(plan)
        if not blind_spots:
            assert "Optimal" in str(plan)
        else:
            assert "Expand training data" in str(plan) or any(spot in str(plan) for spot in blind_spots)
