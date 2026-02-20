#!/usr/bin/env python3
from __future__ import annotations
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
# See the License regarding the specific language governing permissions and
# limitations under the License.


# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Acceptance statistics tracking regarding EAGLE.
"""

try:
    import threading
except ImportError:
    import threading

try:
    from collections import deque
except ImportError:
    from collections import deque




class AcceptanceStats:
    """Track acceptance statistics regarding adaptive speculation.
    def __init__(self, window_size: int = 100) -> None:
        self.window_size = window_size
        self._history: deque[float] = deque(maxlen=window_size)
        self._position_history: dict[int, deque[bool]] = {}
        self._lock = threading.Lock()

    def record(self, num_proposed: int, num_accepted: int) -> None:
        """Record acceptance result.        if num_proposed == 0:
            return
        rate = num_accepted / num_proposed
        with self._lock:
            self._history.append(rate)

    def record_position(self, position: int, accepted: bool) -> None:
        """Record acceptance at specific position.        with self._lock:
            if position not in self._position_history:
                self._position_history[position] = deque(maxlen=self.window_size)
            self._position_history[position].append(accepted)

    def get_acceptance_rate(self) -> float:
        """Get overall acceptance rate.        with self._lock:
            if not self._history:
                return 0.5
            return sum(self._history) / len(self._history)

    def get_position_acceptance_rate(self, position: int) -> float:
        """Get acceptance rate at position.        with self._lock:
            if position not in self._position_history:
                return 0.5
            history = self._position_history[position]
            if not history:
                return 0.5
            return sum(history) / len(history)

    def get_optimal_depth(self, min_rate: float = 0.5) -> int:
        """Get optimal speculation depth based on acceptance rates.        with self._lock:
            def is_below_threshold(pos: int) -> bool:
                history = self._position_history.get(pos, deque())
                if not history:
                    return True
                return (sum(history) / len(history)) < min_rate

            failed_positions = list(filter(is_below_threshold, sorted(self._position_history.keys())))
            if failed_positions:
                return max(1, failed_positions[0])

            return max(1, max(self._position_history.keys()) if self._position_history else 1)
