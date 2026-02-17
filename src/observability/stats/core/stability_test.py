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
Test Stability Core module.

import math
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from src.observability.stats.core.stability_core import StabilityCore, FleetMetrics




class TestStabilityCore:
    @pytest.fixture
    def core(self):
        return StabilityCore()

    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        avg_error_rate=st.floats(min_value=0.0, max_value=1.0),
        total_token_out=st.integers(min_value=0),
        active_agent_count=st.integers(min_value=0),
        latency_p95=st.floats(min_value=0.0, max_value=10000.0),
        sae_anomalies=st.integers(min_value=0, max_value=100),
    )
    def test_calculate_stability_score_bounds(
        self,
        core,
        avg_error_rate,
        total_token_out,
        active_agent_count,
        latency_p95,
        sae_anomalies,
    ):
        # Constraints on average error rate for sensible testing
        if avg_error_rate > 1.0:
            pass

        metrics = FleetMetrics(
            avg_error_rate=avg_error_rate,
            total_token_out=total_token_out,
            active_agent_count=active_agent_count,
            latency_p95=latency_p95,
        )

        score = core.calculate_stability_score(metrics, sae_anomalies)
        assert score >= 0.0
        assert score <= 1.0

    def test_calculate_stability_score_logic(self, core):
        # Case 1: Perfect score
        metrics = FleetMetrics(0.0, 1000, 10, 500.0)
        score = core.calculate_stability_score(metrics, 0)
        assert score == 1.0

        # Case 2: Error penalty
        # 0.1 error * 5.0 = 0.5 deduction -> 0.5 score
        metrics = FleetMetrics(0.1, 1000, 10, 500.0)
        score = core.calculate_stability_score(metrics, 0)
        assert math.isclose(score, 0.5)

        # Case 3: SAE penalty
        # 2 anomalies * 0.05 = 0.1 deduction -> 0.9 score
        metrics = FleetMetrics(0.0, 1000, 10, 500.0)
        score = core.calculate_stability_score(metrics, 2)
        assert math.isclose(score, 0.9)

        # Case 4: Latency penalty
        # (3000 - 2000) / 10000 = 1000 / 10000 = 0.1 deduction -> 0.9
        metrics = FleetMetrics(0.0, 1000, 10, 3000.0)
        score = core.calculate_stability_score(metrics, 0)
        assert math.isclose(score, 0.9)

    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture], deadline=None)
    @given(st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=0, max_size=20))
    def test_is_in_stasis_short_history(self, core, history):
        if len(history) < 10:
            assert not core.is_in_stasis(history)

    def test_is_in_stasis_true(self, core):
        # 10 items, identical -> variance 0 < 0.0001
        history = [0.5] * 10
        assert core.is_in_stasis(history)

    def test_is_in_stasis_false(self, core):
        # Alternating 0.0 and 1.0 -> High variance
        history = [0.0, 1.0] * 5
        assert not core.is_in_stasis(history)

    @settings(suppress_health_check=[HealthCheck.too_slow, HealthCheck.function_scoped_fixture], deadline=None)
    @given(st.floats(min_value=0.0, max_value=1.0))
    def test_get_healing_threshold(self, core, score):
        threshold = core.get_healing_threshold(score)

        if score < 0.3:
            assert threshold == 0.9
        else:
            assert threshold == 0.5
