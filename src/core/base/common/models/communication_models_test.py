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


"""Unit tests for communication models (CascadeContext)."""


try:
    import pytest
except ImportError:
    import pytest

try:
    from .core.base.common.models.communication_models import CascadeContext
except ImportError:
    from src.core.base.common.models.communication_models import CascadeContext

try:
    from .core.base.common.models import FailureClassification
except ImportError:
    from src.core.base.common.models import FailureClassification


class TestCascadeContext:
    """Tests for the CascadeContext model."""

    def test_initialization_defaults(self):
        """Test that default values are set correctly on initialization.
        """
        ctx = CascadeContext(task_id="test-task")
        assert ctx.cascade_depth == 0
        assert ctx.depth_limit == 10
        assert ctx.failure_history == []


    def test_depth_limit_validation(self):
        """Test that exceeding the depth limit raises an error.
        """
        with pytest.raises(RecursionError):
            CascadeContext(task_id="test", cascade_depth=11, depth_limit=10)


    def test_failure_history_validation_schema(self):
        """Test that invalid entries in failure history are filtered out.
        """
        # Pass invalid types in failure history
        bad_history = ["not-a-dict", 123, {"valid": "mostly"}]
        ctx = CascadeContext(
            task_id="test",
            failure_history=bad_history
        )
        # Should be filtered to just the dict, and keys added
        assert len(ctx.failure_history) == 1
        entry = ctx.failure_history[0]
        assert entry["error"] == "Unknown Error (Schema Violation)"
        assert "timestamp" in entry


    def test_recursive_improvement_blocking(self):
        """Test that recursive improvement loops are blocked.
        """
        ctx = CascadeContext(task_id="root")
        # Simulate failure history with recursive improvement loops
        ctx.failure_history = [
            {"error": "e1", "failure_type": FailureClassification.RECURSIVE_IMPROVEMENT.value},
            {"error": "e2", "failure_type": FailureClassification.RECURSIVE_IMPROVEMENT.value}
        ]
        # Should raise RecursionError on next_level
        with pytest.raises(RecursionError) as exc:
            ctx.next_level("agent-child")
        assert "Recursive Improvement Loop" in str(exc.value)


    def test_repeating_error_circuit_breaker(self):
        """Test that the circuit breaker triggers on repeating errors.
        """
        ctx = CascadeContext(task_id="root")
        ctx.log_failure(stage="test", error="Same Error")
        ctx.log_failure(stage="test", error="Same Error")
        # Third time should trigger breaker
        ctx.log_failure(stage="test", error="Same Error")
        assert len(ctx.failure_history) == 3  # 2 errors + 1 breaker (replacing 3rd)
        last = ctx.failure_history[-1]
        assert last["stage"] == "circuit_breaker_repeating"
        assert "Exact Repeating Error" in last["error"]
        