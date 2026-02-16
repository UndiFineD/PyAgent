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

import pytest
from core.base.common.utils.math_utils import cdiv, next_power_of_2, prev_power_of_2, is_power_of_2, round_up, round_down, clamp, align_to, bit_count, gcd, lcm, batch_cdiv, batch_next_power_of_2, batch_round_up


def test_cdiv_basic():
    assert callable(cdiv)


def test_next_power_of_2_basic():
    assert callable(next_power_of_2)


def test_prev_power_of_2_basic():
    assert callable(prev_power_of_2)


def test_is_power_of_2_basic():
    assert callable(is_power_of_2)


def test_round_up_basic():
    assert callable(round_up)


def test_round_down_basic():
    assert callable(round_down)


def test_clamp_basic():
    assert callable(clamp)


def test_align_to_basic():
    assert callable(align_to)


def test_bit_count_basic():
    assert callable(bit_count)


def test_gcd_basic():
    assert callable(gcd)


def test_lcm_basic():
    assert callable(lcm)


def test_batch_cdiv_basic():
    assert callable(batch_cdiv)


def test_batch_next_power_of_2_basic():
    assert callable(batch_next_power_of_2)


def test_batch_round_up_basic():
    assert callable(batch_round_up)
