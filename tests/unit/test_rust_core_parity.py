
"""
Verification suite for Rust Core parity.
This test file checks if the Rust implementations match the Python expected logic.
Requires 'rust_core' to be compiled and installed.
"""

import pytest
import math
try:
    import rust_core
except ImportError:
    rust_core = None  # type: ignore[assignment]




@pytest.mark.skipif(
    rust_core is None or not hasattr(rust_core, "calculate_new_utility"),
    reason="rust_core module not compiled or incomplete"
)
class TestRustCoreParity:

    def test_memory_logic(self):
        # Python Logic
        base = 0.5
        success = 0.5 + 0.2
        failure = 0.5 - 0.3

        # Rust Logic
        r_success = rust_core.calculate_new_utility(0.5, 0.2)
        r_failure = rust_core.calculate_new_utility(0.5, -0.3)

        assert math.isclose(r_success, success)
        assert math.isclose(r_failure, failure)

        episode = rust_core.create_episode_struct(
            "AgentX", "Task1", "Done", True, 0.5
        )
        assert episode["utility_score"] == 0.7
        assert episode["success"] is True

    def test_statistical_significance(self):
        control = [10.0, 11.0, 9.0, 10.0, 10.0]
        treatment = [15.0, 16.0, 14.0, 15.0, 15.0]

        result = rust_core.calculate_statistical_significance(control, treatment)

        assert result["t_statistic"] != 0.0
        assert result["p_value"] <= 0.05
        assert result["effect_size"] > 0

    def test_task_decomposer_heuristic(self):
        plan = rust_core.generate_heuristic_plan("Please research quantum computing")
        assert len(plan) >= 1
        assert plan[0]["agent"] == "ResearchAgent"

        plan_code = rust_core.generate_heuristic_plan("fix the bug in main.py")
        assert any(s["agent"] == "CoderAgent" for s in plan_code)











    def test_context_compression(self):
        py_code = "class MyClass:\n    def method(self):\n        pass"
        compressed = rust_core.compress_python_regex(py_code)



        assert "class MyClass" in compressed
        assert "def method" in compressed
        assert "pass" not in compressed

    def test_deduplication(self):


        # Jaccard
        s1 = "This is a test"
        s2 = "This is a test"
        score = rust_core.calculate_jaccard_similarity(s1, s2)
        assert score == 1.0




        s3 = "Different content completely"
        score_diff = rust_core.calculate_jaccard_similarity(s1, s3)
        assert score_diff == 0.0





if __name__ == "__main__":
    pytest.main([__file__])
