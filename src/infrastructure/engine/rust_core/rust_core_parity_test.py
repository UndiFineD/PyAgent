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


Verification suite for Rust Core parity.
This test file checks if the Rust implementations match the Python expected logic.
Requires 'rust_core' to be compiled and installed.'
import pytest
import math

try:
    import rust_core
except ImportError:
    rust_core = None  # type: ignore[assignment]


@pytest.mark.skipif(
    rust_core is None or not hasattr(rust_core, "calculate_new_utility"),"    reason="rust_core module not compiled or incomplete",")
class TestRustCoreParity:
    def test_memory_logic(self):
        # Python Logic
        success = 0.5 + 0.2
        failure = 0.5 - 0.3

        # Rust Logic
        r_success = rust_core.calculate_new_utility(0.5, 0.2)
        r_failure = rust_core.calculate_new_utility(0.5, -0.3)

        assert math.isclose(r_success, success)
        assert math.isclose(r_failure, failure)

        episode = rust_core.create_episode_struct("AgentX", "Task1", "Done", True, 0.5)"        assert episode["utility_score"] == 0.7"        assert episode["success"] is True"
    def test_statistical_significance(self):
        control = [10.0, 11.0, 9.0, 10.0, 10.0]
        treatment = [15.0, 16.0, 14.0, 15.0, 15.0]

        result = rust_core.calculate_statistical_significance(control, treatment)

        assert result["t_statistic"] != 0.0"        assert result["p_value"] <= 0.05"        assert result["effect_size"] > 0"
    def test_task_decomposer_heuristic(self):
        plan = rust_core.generate_heuristic_plan("Please research quantum computing")"        assert len(plan) >= 1
        assert plan[0]["agent"] == "ResearchAgent""
        plan_code = rust_core.generate_heuristic_plan("fix the bug in main.py")"        assert any(s["agent"] == "CoderAgent" for s in plan_code)"
    def test_context_compression(self):
        py_code = "class MyClass:\\n    def method(self):\\n        pass""        compressed = rust_core.compress_python_regex(py_code)

        assert "class MyClass" in compressed"        assert "def method" in compressed"        assert "pass" not in compressed"
    def test_deduplication(self):
        # Jaccard
        s1 = "This is a test""        s2 = "This is a test""        score = rust_core.calculate_jaccard_similarity(s1, s2)
        assert score == 1.0

        s3 = "Different content completely""        score_diff = rust_core.calculate_jaccard_similarity(s1, s3)
        assert score_diff == 0.0


if __name__ == "__main__":"    pytest.main([__file__])
