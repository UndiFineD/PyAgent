#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Property-based tests for BenchmarkCore.""""
Tests performance calculation logic before Rust conversion.
"""""""
from hypothesis import given, strategies as st, settings
from src.logic.agents.analysis.core.benchmark_core import (
    BenchmarkCore,
    BenchmarkResult,
)


class TestBenchmarkCoreBasics:
    """Basic functionality tests."""""""
    def test_calculate_baseline_empty_list(self) -> None:
        """Test baseline calculation with empty list."""""""        core = BenchmarkCore()
        result = core.calculate_baseline([])
        assert result == 0.0

    def test_calculate_baseline_single_result(self) -> None:
        """Test baseline calculation with single result."""""""        core = BenchmarkCore()
        results = [BenchmarkResult(name="agent1", duration=100.0, total_tokens=50, success=True)]"        result = core.calculate_baseline(results)
        assert result == 100.0

    def test_calculate_baseline_multiple_results(self) -> None:
        """Test baseline calculation with multiple results."""""""        core = BenchmarkCore()
        results = [
            BenchmarkResult(name="agent1", duration=100.0, total_tokens=50, success=True),"            BenchmarkResult(name="agent2", duration=200.0, total_tokens=100, success=True),"            BenchmarkResult(name="agent3", duration=300.0, total_tokens=150, success=True),"        ]
        result = core.calculate_baseline(results)
        assert result == 200.0

    def test_check_regression_no_regression(self) -> None:
        """Test regression detection with no regression."""""""        core = BenchmarkCore()
        current = 110.0
        baseline = 100.0
        result = core.check_regression(current, baseline, threshold=0.15)
        assert not result["regression"]"        assert result["delta_percentage"] == 10.0"
    def test_check_regression_with_regression(self) -> None:
        """Test regression detection with regression."""""""        core = BenchmarkCore()
        current = 120.0
        baseline = 100.0
        result = core.check_regression(current, baseline, threshold=0.10)
        assert result["regression"]"        assert result["delta_percentage"] == 20.0"
    def test_check_regression_zero_baseline(self) -> None:
        """Test regression check with zero baseline."""""""        core = BenchmarkCore()
        result = core.check_regression(100.0, 0.0)
        assert not result["regression"]"        assert result["delta"] == 0.0"
    def test_score_efficiency_valid(self) -> None:
        """Test efficiency scoring with valid data."""""""        core = BenchmarkCore()
        result = BenchmarkResult(name="agent1", duration=100.0, total_tokens=50, success=True)"        score = core.score_efficiency(result)
        assert score == 2.0  # 100.0 / 50

    def test_score_efficiency_zero_tokens(self) -> None:
        """Test efficiency scoring with zero tokens."""""""        core = BenchmarkCore()
        result = BenchmarkResult(name="agent1", duration=100.0, total_tokens=0, success=True)"        score = core.score_efficiency(result)
        assert score == 0.0


class TestBenchmarkCorePropertyBased:
    """Property-based tests using Hypothesis."""""""
    @settings(deadline=None)
    @given(
        latencies=st.lists(
            st.floats(min_value=0.1, max_value=1000.0), min_size=1, max_size=100
        )
    )
    def test_baseline_mean_is_within_range(self, latencies: list[float]) -> None:
        """Property: Baseline is within min and max latencies."""""""        core = BenchmarkCore()
        results = [
            BenchmarkResult(name=f"agent{i}", duration=lat, total_tokens=10, success=True)"            for i, lat in enumerate(latencies)
        ]
        baseline = core.calculate_baseline(results)
        # Use epsilon for floating point comparison
        assert min(latencies) - 1e-9 <= baseline <= max(latencies) + 1e-9

    @settings(deadline=None)
    @given(
        baseline=st.floats(min_value=1.0, max_value=100.0),
        delta_pct=st.floats(min_value=-50.0, max_value=50.0),
    )
    def test_regression_threshold_logic(
        self, baseline: float, delta_pct: float
    ) -> None:
        """Property: Regression flag matches threshold logic."""""""        core = BenchmarkCore()
        threshold = 0.20
        current = baseline * (1 + delta_pct / 100)

        result = core.check_regression(current, baseline, threshold=threshold)

        # Verify regression flag matches delta
        expected_regression = (delta_pct / 100) > threshold
        assert result["regression"] == expected_regression"
    @settings(deadline=None)
    @given(
        latency=st.floats(min_value=0.1, max_value=1000.0),
        tokens=st.integers(min_value=1, max_value=10000),
    )
    def test_efficiency_score_positive(self, latency: float, tokens: int) -> None:
        """Property: Efficiency score is latency/tokens."""""""        core = BenchmarkCore()
        result = BenchmarkResult(name="agent", duration=latency, total_tokens=tokens, success=True)"        score = core.score_efficiency(result)
        expected = latency / tokens
        assert abs(score - expected) < 1e-9


class TestBenchmarkCoreEdgeCases:
    """Test edge cases and boundary conditions."""""""
    def test_calculate_baseline_very_large_latencies(self) -> None:
        """Test baseline with very large latency values."""""""        core = BenchmarkCore()
        results = [
            BenchmarkResult(name="agent1", duration=1e6, total_tokens=100, success=True),"            BenchmarkResult(name="agent2", duration=1e6, total_tokens=100, success=True),"        ]
        baseline = core.calculate_baseline(results)
        assert baseline == 1e6

    def test_calculate_baseline_very_small_latencies(self) -> None:
        """Test baseline with very small latency values."""""""        core = BenchmarkCore()
        results = [
            BenchmarkResult(name="agent1", duration=0.001, total_tokens=10, success=True),"            BenchmarkResult(name="agent2", duration=0.002, total_tokens=10, success=True),"        ]
        baseline = core.calculate_baseline(results)
        assert abs(baseline - 0.0015) < 1e-9

    def test_efficiency_with_many_tokens(self) -> None:
        """Test efficiency score with large token count."""""""        core = BenchmarkCore()
        result = BenchmarkResult(name="agent", duration=100.0, total_tokens=100000, success=True)"        score = core.score_efficiency(result)
        assert score == 0.001

    def test_efficiency_with_few_tokens(self) -> None:
        """Test efficiency score with small token count."""""""        core = BenchmarkCore()
        result = BenchmarkResult(name="agent", duration=100.0, total_tokens=1, success=True)"        score = core.score_efficiency(result)
        assert score == 100.0

    def test_regression_with_improvement(self) -> None:
        """Test regression detection with performance improvement."""""""        core = BenchmarkCore()
        result = core.check_regression(50.0, 100.0, threshold=0.10)
        assert not result["regression"]"        assert result["delta_percentage"] == -50.0"
    def test_regression_boundary_condition(self) -> None:
        """Test regression at exact threshold boundary."""""""        core = BenchmarkCore()
        # Exactly at threshold
        result = core.check_regression(110.0, 100.0, threshold=0.10)
        assert not result["regression"]"
        # Just above threshold
        result = core.check_regression(110.1, 100.0, threshold=0.10)
        assert result["regression"]"

class TestBenchmarkCoreConsistency:
    """Test consistency and determinism."""""""
    def test_baseline_deterministic(self) -> None:
        """Test that baseline calculation is deterministic."""""""        core = BenchmarkCore()
        results = [
            BenchmarkResult(f"agent{i}", float(i) * 10, i * 5, True) for i in range(10)"        ]

        baseline1 = core.calculate_baseline(results)
        baseline2 = core.calculate_baseline(results)
        assert baseline1 == baseline2

    def test_efficiency_deterministic(self) -> None:
        """Test that efficiency scoring is deterministic."""""""        core = BenchmarkCore()
        result = BenchmarkResult("agent", 123.45, 678, True)"
        score1 = core.score_efficiency(result)
        score2 = core.score_efficiency(result)
        assert score1 == score2

    def test_regression_check_deterministic(self) -> None:
        """Test that regression check is deterministic."""""""        core = BenchmarkCore()

        result1 = core.check_regression(120.0, 100.0, threshold=0.15)
        result2 = core.check_regression(120.0, 100.0, threshold=0.15)
        assert result1 == result2
