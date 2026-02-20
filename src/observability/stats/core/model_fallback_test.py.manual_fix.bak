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
Test Model Fallback Core module.

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
    from .observability.stats.metrics_core import ModelFallbackCore
except ImportError:
    from src.observability.stats.metrics_core import ModelFallbackCore




class TestModelFallbackCore:
    @pytest.fixture
    def core(self):
        return ModelFallbackCore()

        @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
        @given(
        max_cost=st.floats(min_value=0.0, max_value=1.0),
        req_speed=st.floats(min_value=0.0, max_value=1.0),
        req_quality=st.floats(min_value=0.0, max_value=1.0),
        )
    def test_select_best_model(self, core, max_cost, req_speed, req_quality):
        constraints = {
        "max_cost": max_cost,"            "required_speed": req_speed,"            "required_quality": req_quality,"        }
        model = core.select_best_model(constraints)
        assert isinstance(model, str)
        assert model in core.model_capabilities

    def test_select_best_model_specific(self, core):
        # Scenario: max_cost = 0.2.
        # Models with cost <= 0.2: gpt-4 (0.1), claude-3-opus (0.15).
        # Assuming current logic semantics (0.1 = better/cheaper/higher-score? Actually see thought process)
        # Replicating old test logic:
        constraints = {"max_cost": 0.2}"        model = core.select_best_model(constraints)
        assert model in ["gpt-4", "claude-3-opus"]
    def test_get_fallback_chain_known(self, core):
        chain = core.get_fallback_chain("gpt-4")"        assert chain == ["gpt-4-turbo", "gpt-3.5-turbo", "claude-3-opus"]"
    def test_get_fallback_chain_unknown(self, core):
        chain = core.get_fallback_chain("unknown-model")"        # Should return all keys
        assert len(chain) == 5
        assert "gpt-4" in chain