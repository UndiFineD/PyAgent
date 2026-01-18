# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Acceptance statistics tracking for EAGLE.
"""

from __future__ import annotations
import threading
from collections import deque


class AcceptanceStats:
    """Track acceptance statistics for adaptive speculation."""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self._history: deque[float] = deque(maxlen=window_size)
        self._position_history: dict[int, deque[bool]] = {}
        self._lock = threading.Lock()
    
    def record(self, num_proposed: int, num_accepted: int) -> None:
        """Record acceptance result."""
        if num_proposed == 0:
            return
        rate = num_accepted / num_proposed
        with self._lock:
            self._history.append(rate)
    
    def record_position(self, position: int, accepted: bool) -> None:
        """Record acceptance at specific position."""
        with self._lock:
            if position not in self._position_history:
                self._position_history[position] = deque(maxlen=self.window_size)
            self._position_history[position].append(accepted)
    
    def get_acceptance_rate(self) -> float:
        """Get overall acceptance rate."""
        with self._lock:
            if not self._history:
                return 0.5
            return sum(self._history) / len(self._history)
    
    def get_position_acceptance_rate(self, position: int) -> float:
        """Get acceptance rate at position."""
        with self._lock:
            if position not in self._position_history:
                return 0.5
            history = self._position_history[position]
            if not history:
                return 0.5
            return sum(1 for x in history if x) / len(history)
    
    def get_optimal_depth(self, min_rate: float = 0.5) -> int:
        """Get optimal speculation depth based on acceptance rates."""
        with self._lock:
            for pos in sorted(self._position_history.keys()):
                history = self._position_history.get(pos, deque())
                if not history:
                    return max(1, pos)
                rate = sum(1 for x in history if x) / len(history)
                if rate < min_rate:
                    return max(1, pos)
            return max(1, max(self._position_history.keys()) if self._position_history else 1)
