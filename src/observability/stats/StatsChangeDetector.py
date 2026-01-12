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

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent_stats.py"""



from typing import Any, Callable, Dict, List, Optional



































class StatsChangeDetector:
    """Detects changes in metric values."""
    def __init__(self, threshold: float = 0.1, threshold_percent: Optional[float] = None) -> None:
        if threshold_percent is not None:
            threshold = float(threshold_percent) / 100.0
        self.threshold = float(threshold)
        self.previous_values: Dict[str, float] = {}
        self._changes: List[Dict[str, Any]] = []
        self._listeners: List[Callable[[Dict[str, Any]], None]] = []

    def detect_change(self, metric: str, value: float) -> bool:
        """Detect if metric has significantly changed."""
        if metric not in self.previous_values:
            self.previous_values[metric] = value
            return False

        prev = self.previous_values[metric]
        if prev == 0:
            change = abs(value - prev) > 0
        else:
            change = abs((value - prev) / prev) > self.threshold

        self.previous_values[metric] = value
        return change

    def record(self, metric: str, value: float) -> bool:
        """Record a metric value and emit change notifications."""
        prev = self.previous_values.get(metric)
        changed = self.detect_change(metric, float(value))
        if changed:
            old_val = 0.0 if prev is None else float(prev)
            new_val = float(value)
            if old_val == 0.0:
                change_percent = 100.0 if new_val != 0.0 else 0.0
            else:
                change_percent = abs((new_val - old_val) / old_val) * 100.0
            change_info: Dict[str, Any] = {
                "metric": metric,
                "old": old_val,
                "new": new_val,
                "change_percent": change_percent,
            }
            self._changes.append(change_info)
            for listener in list(self._listeners):
                try:
                    listener(change_info)
                except Exception:
                    logging.debug("Change listener failed.")
        return changed

    def on_change(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Register a callback for change events."""
        self._listeners.append(callback)

    def get_changes(self) -> List[Dict[str, Any]]:
        """Return recorded changes."""
        return list(self._changes)
