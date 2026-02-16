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
from infrastructure.engine.sampling.penalty_engine import PenaltyType, PenaltySchedule, PenaltyConfig, PenaltyState, PenaltyEngine, BatchPenaltyEngine, apply_repetition_penalty, apply_frequency_penalty, apply_presence_penalty


def test_penaltytype_basic():
    assert PenaltyType is not None


def test_penaltyschedule_basic():
    assert PenaltySchedule is not None


def test_penaltyconfig_basic():
    assert PenaltyConfig is not None


def test_penaltystate_basic():
    assert PenaltyState is not None


def test_penaltyengine_basic():
    assert PenaltyEngine is not None


def test_batchpenaltyengine_basic():
    assert BatchPenaltyEngine is not None


def test_apply_repetition_penalty_basic():
    assert callable(apply_repetition_penalty)


def test_apply_frequency_penalty_basic():
    assert callable(apply_frequency_penalty)


def test_apply_presence_penalty_basic():
    assert callable(apply_presence_penalty)
