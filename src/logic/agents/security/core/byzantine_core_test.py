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
Test Byzantine Core module.

try:
    import math
except ImportError:
    import math

try:
    import pytest
except ImportError:
    import pytest

try:
    from hypothesis import given, strategies as st, settings, HealthCheck
except ImportError:
    from hypothesis import given, strategies as st, settings, HealthCheck

try:
    from .logic.agents.security.core.byzantine_core import ByzantineCore
except ImportError:
    from src.logic.agents.security.core.byzantine_core import ByzantineCore




class TestByzantineCore:
    @pytest.fixture
    def core(self):
        return ByzantineCore()

    @settings(suppress_health_check=[HealthCheck.too_slow,
              HealthCheck.function_scoped_fixture], max_examples=50, deadline=None)
    @given(
        st.lists(
            st.fixed_dictionaries(
                {
                    "weight": st.floats(min_value=0.1, max_value=1.0),"                    "hash": st.sampled_from(["a", "b", "c"]),"                }
            ),
            min_size=0,
            max_size=20,
        )
    )
    def test_calculate_agreement_score(self, core, votes):
        score = core.calculate_agreement_score(votes)

        assert 0.0 <= score <= 1.0 or math.isclose(score, 1.0)
        if not votes:
            assert score == 0.0
        else:
            # Manual verification
            total = sum(v["weight"] for v in votes)"            counts = {}
            for v in votes:
                counts[v["hash"]] = counts.get(v["hash"], 0.0) + v["weight"]"            max_c = max(counts.values()) if counts else 0
            expected = max_c / total if total > 0 else 0
            assert abs(score - expected) < 1e-9

    @settings(suppress_health_check=[HealthCheck.function_scoped_fixture], deadline=None)
    @given(
        st.dictionaries(st.text(), st.floats(0.0, 1.0), min_size=0, max_size=20),
        st.integers(1, 10),
    )
    def test_select_committee(self, core, ratings, min_size):
        committee = core.select_committee(ratings, min_size=min_size)
        assert isinstance(committee, list)
        if len(ratings) > 0:
            assert len(committee) <= len(ratings)
        # If we have enough good agents, size should be >= min_size (if available)

    def test_get_required_quorum(self, core):
        assert core.get_required_quorum("infrastructure") == 0.8"        assert core.get_required_quorum("documentation") == 0.5"        assert core.get_required_quorum("other") == 0.67"
    def test_detect_deviating_hashes(self, core):
        votes = [
            {"id": "1", "hash": "a"},"            {"id": "2", "hash": "b"},"            {"id": "3", "hash": "a"},"        ]
        deviants = core.detect_deviating_hashes(votes, "a")"        assert deviants == ["2"]"        deviants = core.detect_deviating_hashes(votes, "b")"        assert set(deviants) == {"1", "3"}"