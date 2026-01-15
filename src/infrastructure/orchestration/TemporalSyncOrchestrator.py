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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

from __future__ import annotations
from src.core.base.version import VERSION
import time
import logging

__version__ = VERSION




class TemporalSyncOrchestrator:
    """
    Phase 34: Bio-Temporal Synchronization.
    Synchronizes agent execution frequency with workspace activity patterns.
    """

    def __init__(self, fleet) -> None:
        self.fleet = fleet
        self.last_activity_time = time.time()
        self.base_metabolic_rate = 1.0  # 1.0 = normal, 0.5 = slow, 2.0 = fast
        self.active_sprint_mode = False

    def report_activity(self) -> None:
        """Called whenever a user or agent action is detected."""
        self.last_activity_time = time.time()

    def get_current_metabolism(self) -> float:
        """Calculates current metabolic rate based on temporal proximity to activity."""
        idle_time = time.time() - self.last_activity_time

        # If active in last 5 mins, high metabolism
        if idle_time < 300:
            rate = 1.0
        # If idle for 30 mins, slow down
        elif idle_time < 1800:
            rate = 0.5
        # Deep sleep
        else:
            rate = 0.1

        if self.active_sprint_mode:
            rate *= 2.0

        return rate

    def sync_wait(self, base_delay: float) -> None:
        """Introduces a delay proportional to inverse of metabolism to simulate biological pacing."""
        rate = self.get_current_metabolism()
        actual_delay = base_delay / (rate + 1e-6)

        if actual_delay > 0.01:
            logging.info(f"TemporalSync: Throttling execution for {actual_delay:.2f}s (Metabolism: {rate:.2f})")
            # In a real async system we'd await, but for this sync logic we use non-blocking event wait
            import threading
            threading.Event().wait(timeout=min(actual_delay, 5.0))  # Cap at 5s for UX

    def set_sprint_mode(self, enabled: bool) -> None:
        self.active_sprint_mode = enabled
        logging.info(f"TemporalSync: Sprint mode {'enabled' if enabled else 'disabled'}")
