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

from __future__ import annotations
import random

class ResilienceCore:
    """
    Pure logic for Circuit Breaker and Retry mechanisms.
    Audited for Rust conversion.
    """

    @staticmethod
    def calculate_backoff(
        failure_count: int,
        threshold: int,
        base_timeout: float,
        multiplier: float,
        max_timeout: float,
        apply_jitter: bool = True
    ) -> float:
        """Calculates backoff with exponential multiplier and optional jitter."""
        if failure_count < threshold:
            return 0.0
        
        exponent = max(0, failure_count - threshold)
        backoff = min(max_timeout, base_timeout * (multiplier ** exponent))
        
        if apply_jitter:
            # 10% Jitter
            jitter = backoff * 0.1 * random.uniform(-1, 1)
            backoff = max(base_timeout / 2, backoff + jitter)
            
        return backoff

    @staticmethod
    def should_attempt_recovery(
        last_failure_time: float,
        current_time: float,
        timeout: float
    ) -> bool:
        """Determines if the cooldown period has passed."""
        return (current_time - last_failure_time) > timeout

    @staticmethod
    def evaluate_state_transition(
        current_state: str,
        success_count: int,
        consecutive_successes_needed: int,
        failure_count: int,
        failure_threshold: int
    ) -> str:
        """
        Pure state machine logic for transition.
        Transitions:
            CLOSED -> OPEN (if failure_count >= threshold)
            OPEN -> HALF_OPEN (externally timed)
            HALF_OPEN -> CLOSED (if success_count >= needed)
            HALF_OPEN -> OPEN (if any failure during half-open)
        """
        if current_state == "CLOSED":
            if failure_count >= failure_threshold:
                return "OPEN"
        elif current_state == "HALF_OPEN":
            if success_count >= consecutive_successes_needed:
                return "CLOSED"
        
        return current_state