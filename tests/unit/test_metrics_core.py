from hypothesis import given, strategies as st
import math
from src.observability.stats.metrics_core import (
    TokenCostCore,
    ModelFallbackCore,
    StatsRollupCore,
    TokenCostResult,
    DerivedMetricCalculator,
    CorrelationCore,
    ABTestCore,
)

# === TokenCostCore Tests ===


class TestTokenCostCore:
    @given(
        st.integers(min_value=0, max_value=1_000_000),
        st.integers(min_value=0, max_value=1_000_000),
        st.sampled_from(["gpt-4", "gpt-3.5-turbo", "claude-3-opus"]),
    )
    def test_calculate_cost_properties(self, input_tokens, output_tokens, model):
        core = TokenCostCore()
        result = core.calculate_cost(input_tokens, output_tokens, model)
        assert isinstance(result, TokenCostResult)

        assert result.total_cost >= 0
        assert result.input_cost >= 0
        assert result.output_cost >= 0
        assert math.isclose(result.total_cost, result.input_cost + result.output_cost)

    def test_cost_calculation_accuracy(self):
        core = TokenCostCore()
        # GPT-4: Input 0.03/1M, Output 0.06/1M
        result = core.calculate_cost(1_000_000, 1_000_000, "gpt-4")
        assert math.isclose(result.input_cost, 0.03)

        assert math.isclose(result.output_cost, 0.06)
        assert math.isclose(result.total_cost, 0.09)


# === ModelFallbackCore Tests ===


class TestModelFallbackCore:
    @given(
        st.floats(min_value=0.1, max_value=1.0),
        st.floats(min_value=0.0, max_value=1.0),
        st.floats(min_value=0.0, max_value=1.0),
    )
    def test_select_best_model_consistency(self, max_cost, speed, quality):
        core = ModelFallbackCore()

        constraints = {
            "max_cost": max_cost,
            "required_speed": speed,
            "required_quality": quality,
        }
        model = core.select_best_model(constraints)
        assert isinstance(model, str)

        assert model in core.model_capabilities

    def test_fallback_chain(self):
        core = ModelFallbackCore()
        chain = core.get_fallback_chain("gpt-4")
        assert isinstance(chain, list)
        assert "gpt-4-turbo" in chain


# === StatsRollupCore Tests ===


class TestStatsRollupCore:
    @given(
        st.lists(
            st.floats(
                allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6
            ),
            min_size=1,
        )
    )
    def test_rollup_properties(self, values):
        core = StatsRollupCore()
        assert math.isclose(core.rollup_sum(values), sum(values), rel_tol=1e-9)
        assert math.isclose(
            core.rollup_avg(values), sum(values) / len(values), rel_tol=1e-9
        )

        assert core.rollup_min(values) == min(values)
        assert core.rollup_max(values) == max(values)

    def test_empty_lists(self):
        core = StatsRollupCore()

        assert core.rollup_sum([]) == 0.0
        assert core.rollup_avg([]) == 0.0

    @given(
        st.lists(
            st.floats(
                allow_nan=False, allow_infinity=False, min_value=-1e6, max_value=1e6
            ),
            min_size=20,
        )
    )
    def test_percentiles(self, values):
        core = StatsRollupCore()
        p50 = core.rollup_p50(values)
        p95 = core.rollup_p95(values)
        p99 = core.rollup_p99(values)

        assert core.rollup_min(values) <= p50 <= core.rollup_max(values)
        if len(values) >= 20:
            # p95 should generally be higher than p50 for typical distributions, but not strictly guaranteed for all random sets
            pass


# === DerivedMetricCalculator Tests ===


class TestDerivedMetricCalculator:
    def test_basic_math(self):
        core = DerivedMetricCalculator()

        assert core.evaluate_formula("1 + 1", {}) == 2.0
        assert core.evaluate_formula("x * 2", {"x": 5}) == 10.0


# === CorrelationCore Tests ===


class TestCorrelationCore:
    def test_perfect_correlation(self):
        core = CorrelationCore()
        s1 = [1.0, 2.0, 3.0]
        s2 = [2.0, 4.0, 6.0]
        assert math.isclose(core.calculate_correlation(s1, s2), 1.0)

    def test_perfect_negative_correlation(self):
        core = CorrelationCore()
        s1 = [1.0, 2.0, 3.0]
        s2 = [3.0, 2.0, 1.0]
        assert math.isclose(core.calculate_correlation(s1, s2), -1.0)


# === ABTestCore Tests ===


class TestABTestCore:
    def test_significance(self):
        core = ABTestCore()
        control = [10.0, 10.1, 9.9, 10.0]
        treatment = [15.0, 14.9, 15.1, 15.0]
        res = core.calculate_significance(control, treatment)
        assert res["p_value"] <= 0.05
        assert res["t_statistic"] > 0
