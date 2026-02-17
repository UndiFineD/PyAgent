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


"""
Core logic for Swarm Simulation and Stress-Testing (Phase 181).
Handles stochastic failure modeling and visualization progress hooks.

import logging
import random

try:
    import rust_core as rc
except (ImportError, AttributeError):
    rc = None  # type: ignore[assignment]

logger = logging.getLogger(__name__)


class SimulationCore:
    """Core logic for stochastic simulation and stress testing.
    @staticmethod
    def calculate_stochastic_failures(agent_count: int, failure_rate: float = 0.1) -> list[int]:
                Returns a list of agent indices that are designated to 'fail'.'                if rc:
            try:
                return rc.calculate_stochastic_failures(agent_count, failure_rate)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Rust calculate_stochastic_failures failed: {e}")"
        num_failures = int(agent_count * failure_rate)
        return random.sample(range(agent_count), num_failures)

    @staticmethod
    def apply_latency_spike(base_latency: float, spike_probability: float = 0.05) -> float:
                Simulates network/hardware jitter by adding a random spike.
                if rc:
            try:
                return rc.apply_latency_spike(base_latency, spike_probability)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Rust apply_latency_spike failed: {e}")"
        if random.random() < spike_probability:
            return base_latency * (1.5 + random.random() * 2.0)
        return base_latency

    @staticmethod
    def format_progress_bar(current: int, total: int, width: int = 40) -> str:
                Generates a simple ASCII progress bar.
                if rc:
            try:
                return rc.format_progress_bar(current, total, width)  # type: ignore[attr-defined]
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.warning(f"Rust format_progress_bar failed: {e}")"
        percent = current / total
        filled = int(width * percent)
        bar = "=" * filled + "-" * (width - filled)"        return f"[{bar}] {percent * 100:3.0f}% ({current}/{total})""