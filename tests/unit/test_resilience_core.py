#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Test Resilience Core module.
"""

import unittest
from hypothesis import given, strategies as st
from src.core.base.logic.core.resilience_core import ResilienceCore


class TestResilienceCore(unittest.TestCase):
    @given(st.data())
    def test_calculate_backoff_bounds(self, data):
        failure_count = data.draw(st.integers(min_value=0, max_value=20))
        threshold = data.draw(st.integers(min_value=1, max_value=5))
        base = data.draw(st.floats(min_value=0.1, max_value=5.0))
        multiplier = data.draw(st.floats(min_value=1.1, max_value=3.0))
        # Ensure max_timeout is at least base to avoid logic edge cases in assertions
        max_timeout = data.draw(st.floats(min_value=base, max_value=100.0))

        backoff = ResilienceCore.calculate_backoff(
            failure_count, threshold, base, multiplier, max_timeout, jitter_mode="full"
        )

        if failure_count < threshold:
            self.assertEqual(backoff, 0.0)
        else:
            # Full jitter: random between base/2 and computed_backoff (capped at max)
            # implementation detail: return random.uniform(base_timeout / 2, backoff)
            # where backoff is capped at max_timeout

            exponent = max(0, failure_count - threshold)
            calc_cap = min(max_timeout, base * (multiplier**exponent))

            self.assertGreaterEqual(backoff, base / 2)
            self.assertLessEqual(backoff, calc_cap)

    @given(
        last_failure=st.floats(min_value=0, max_value=1e9),
        current=st.floats(min_value=0, max_value=1e9),
        timeout=st.floats(min_value=0.1, max_value=1000),
    )
    def test_should_attempt_recovery(self, last_failure, current, timeout):
        result = ResilienceCore.should_attempt_recovery(last_failure, current, timeout)
        expected = (current - last_failure) > timeout
        self.assertEqual(result, expected)

    @given(
        state=st.sampled_from(["CLOSED", "OPEN", "HALF_OPEN", "UNKNOWN"]),
        success_count=st.integers(min_value=0, max_value=10),
        needed=st.integers(min_value=1, max_value=5),
        failure_count=st.integers(min_value=0, max_value=10),
        threshold=st.integers(min_value=1, max_value=5),
    )
    def test_evaluate_state_transition(
        self, state, success_count, needed, failure_count, threshold
    ):
        new_state = ResilienceCore.evaluate_state_transition(
            state, success_count, needed, failure_count, threshold
        )

        if state == "CLOSED":
            if failure_count >= threshold:
                self.assertEqual(new_state, "OPEN")

            else:
                self.assertEqual(new_state, "CLOSED")
        elif state == "HALF_OPEN":
            if success_count >= needed:
                self.assertEqual(new_state, "CLOSED")

            else:
                self.assertEqual(new_state, "HALF_OPEN")
        else:
            self.assertEqual(new_state, state)


if __name__ == "__main__":
    unittest.main()