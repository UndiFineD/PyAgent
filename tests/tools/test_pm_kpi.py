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
"""Tests for tools.pm.kpi module (prj0000021)."""

import pytest

from tools.pm import kpi


def test_compute_throughput_basic():
    assert kpi.compute_throughput(["a", "b", "c"], []) == 3


def test_compute_throughput_empty():
    assert kpi.compute_throughput([], []) == 0


def test_velocity_single_sprint():
    assert kpi.velocity([5.0, 3.0, 2.0], sprints=1) == pytest.approx(10.0)


def test_velocity_multiple_sprints():
    assert kpi.velocity([10.0, 10.0], sprints=2) == pytest.approx(10.0)


def test_velocity_invalid_sprints():
    with pytest.raises(ValueError):
        kpi.velocity([1.0], sprints=0)


def test_cycle_time_basic():
    assert kpi.cycle_time(0.0, 100.0) == pytest.approx(100.0)


def test_cycle_time_invalid():
    with pytest.raises(ValueError):
        kpi.cycle_time(100.0, 50.0)


def test_defect_rate_basic():
    assert kpi.defect_rate(2, 10) == pytest.approx(0.2)


def test_defect_rate_zero_bugs():
    assert kpi.defect_rate(0, 10) == pytest.approx(0.0)


def test_defect_rate_invalid():
    with pytest.raises(ValueError):
        kpi.defect_rate(1, 0)


def test_sprint_health_green():
    assert kpi.sprint_health(9, 10) == "green"


def test_sprint_health_amber():
    assert kpi.sprint_health(7, 10) == "amber"


def test_sprint_health_red():
    assert kpi.sprint_health(5, 10) == "red"


def test_sprint_health_invalid():
    with pytest.raises(ValueError):
        kpi.sprint_health(5, 0)
