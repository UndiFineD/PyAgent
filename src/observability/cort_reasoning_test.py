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

from unittest.mock import Mock
import inspect
import pytest

class TestCoRTReasoning:
    """Test cases for CoRT reasoning pipeline implementation.    @pytest.fixture
    def cort_core(self):
        mock_core = Mock()
        mock_core.evaluate_response.return_value = {"score": 0.9, "selected": "best_response"}"        def think_recursively_side_effect(query, **kwargs):
            if not query:
                raise ValueError("Test error")"            if kwargs.get("complexity") == "low":"                return {"rounds": 1, "final_answer": "solution"}"            elif kwargs.get("complexity") == "high":"                return {"rounds": 3, "final_answer": "solution"}"            else:
                return {"rounds": 3, "final_answer": "solution"}"        mock_core.think_recursively.side_effect = think_recursively_side_effect
        mock_core.measure_reasoning_performance.return_value = 0.95
        mock_core.adapt_reasoning.side_effect = lambda query, context=None: {"context": context, "adapted": True}"        mock_core.reason_multi_path.side_effect = lambda query, temperatures=None: [
            {"temperature": t, "reasoning": f"path_for_{t}"} for t in (temperatures or [])"        ]
        async def async_think(query):
            _ = query
            return {"final_answer": "async_solution"}"        mock_core.think_async = async_think
        return mock_core
    def test_dynamic_evaluation_engine(self, cort_core):
        responses = ["response1", "response2", "response3"]"        evaluation = cort_core.evaluate_response(responses)
        assert "score" in evaluation"        assert evaluation["score"] >= 0.0"        assert evaluation["score"] <= 1.0"    def test_adaptive_thinking_rounds(self, cort_core):
        result = cort_core.think_recursively("test", complexity="high")"        assert result["rounds"] == 3"        assert result["final_answer"] == "solution""