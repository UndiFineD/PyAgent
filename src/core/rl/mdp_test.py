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
from core.rl.mdp import Transition, ExperienceReplayBuffer, MDP


def test_transition_basic():
    assert Transition is not None


def test_experiencereplaybuffer_basic():
    assert ExperienceReplayBuffer is not None


def test_mdp_basic():
    assert MDP is not None
