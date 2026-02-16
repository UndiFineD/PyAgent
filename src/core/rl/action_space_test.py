#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from core.rl.action_space import ActionMetadata, ActionSpace, DiscreteActionSpace, BoxActionSpace, MultiDiscreteActionSpace, DictActionSpace


def test_actionmetadata_basic():
    assert ActionMetadata is not None


def test_actionspace_basic():
    assert ActionSpace is not None


def test_discreteactionspace_basic():
    assert DiscreteActionSpace is not None


def test_boxactionspace_basic():
    assert BoxActionSpace is not None


def test_multidiscreteactionspace_basic():
    assert MultiDiscreteActionSpace is not None


def test_dictactionspace_basic():
    assert DictActionSpace is not None
