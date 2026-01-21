import unittest
from hypothesis import given, strategies as st
from src.observability.stats.core.stability_core import StabilityCore, FleetMetrics


class TestStabilityCore(unittest.TestCase):
    def setUp(self):
        self.core = StabilityCore()

    @given(
        avg_error_rate=st.floats(min_value=0.0, max_value=1.0),
        total_token_out=st.integers(min_value=0),
        active_agent_count=st.integers(min_value=0),
        latency_p95=st.floats(min_value=0.0, max_value=10000.0),
        sae_anomalies=st.integers(min_value=0, max_value=100),
    )
    def test_calculate_stability_score_bounds(
        self,
        avg_error_rate,
        total_token_out,
        active_agent_count,
        latency_p95,
        sae_anomalies,
    ):
        # Constraints on average error rate for sensible testing
        if avg_error_rate > 1.0:
            # Though the strategy caps at 1.0, float precision might jitter.
            # logic handles floats generally, but error rate implies 0-1.
            pass

        metrics = FleetMetrics(
            avg_error_rate=avg_error_rate,
            total_token_out=total_token_out,
            active_agent_count=active_agent_count,
            latency_p95=latency_p95,
        )

        score = self.core.calculate_stability_score(metrics, sae_anomalies)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_calculate_stability_score_logic(self):
        # Case 1: Perfect score
        metrics = FleetMetrics(0.0, 1000, 10, 500.0)
        score = self.core.calculate_stability_score(metrics, 0)
        self.assertEqual(score, 1.0)

        # Case 2: Error penalty
        # 0.1 error * 5.0 = 0.5 deduction -> 0.5 score
        metrics = FleetMetrics(0.1, 1000, 10, 500.0)
        score = self.core.calculate_stability_score(metrics, 0)
        self.assertAlmostEqual(score, 0.5)

        # Case 3: SAE penalty
        # 2 anomalies * 0.05 = 0.1 deduction -> 0.9 score
        metrics = FleetMetrics(0.0, 1000, 10, 500.0)
        score = self.core.calculate_stability_score(metrics, 2)
        self.assertAlmostEqual(score, 0.9)

        # Case 4: Latency penalty
        # (3000 - 2000) / 10000 = 1000 / 10000 = 0.1 deduction -> 0.9
        metrics = FleetMetrics(0.0, 1000, 10, 3000.0)
        score = self.core.calculate_stability_score(metrics, 0)
        self.assertAlmostEqual(score, 0.9)

    @given(st.lists(st.floats(min_value=0.0, max_value=1.0), min_size=0, max_size=20))
    def test_is_in_stasis_short_history(self, history):
        if len(history) < 10:
            self.assertFalse(self.core.is_in_stasis(history))

    def test_is_in_stasis_true(self):
        # 10 items, identical -> variance 0 < 0.0001
        history = [0.5] * 10

        self.assertTrue(self.core.is_in_stasis(history))

    def test_is_in_stasis_false(self):
        # Alternating 0.0 and 1.0 -> High variance
        history = [0.0, 1.0] * 5

        self.assertFalse(self.core.is_in_stasis(history))

    @given(st.floats(min_value=0.0, max_value=1.0))
    def test_get_healing_threshold(self, score):
        threshold = self.core.get_healing_threshold(score)

        if score < 0.3:
            self.assertEqual(threshold, 0.9)
        else:
            self.assertEqual(threshold, 0.5)


if __name__ == "__main__":
    unittest.main()
