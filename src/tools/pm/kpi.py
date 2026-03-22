#!/usr/bin/env python3
"""KPI computation functions for PyAgent."""
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

from typing import Any, Sequence


def compute_throughput(completed: Sequence[Any], period: Sequence[Any]) -> int:
    """Return a simple throughput metric (items completed).

    ``period`` is reserved for future time-based weighting.
    """
    return len(completed)


def velocity(completed_points: Sequence[float], sprints: int = 1) -> float:
    """Return average story-points per sprint."""
    if sprints <= 0:
        raise ValueError("sprints must be >= 1")
    return sum(completed_points) / sprints


def cycle_time(start_ts: float, end_ts: float) -> float:
    """Return elapsed seconds between start and end timestamps."""
    if end_ts < start_ts:
        raise ValueError("end_ts must be >= start_ts")
    return end_ts - start_ts


def defect_rate(bugs_found: int, total_items: int) -> float:
    """Return defect rate as a fraction in [0, 1]."""
    if total_items <= 0:
        raise ValueError("total_items must be > 0")
    return bugs_found / total_items


def sprint_health(completed: int, planned: int) -> str:
    """Return a human-readable health label for a sprint."""
    if planned <= 0:
        raise ValueError("planned must be > 0")
    ratio = completed / planned
    if ratio >= 0.9:
        return "green"
    if ratio >= 0.7:
        return "amber"
    return "red"
