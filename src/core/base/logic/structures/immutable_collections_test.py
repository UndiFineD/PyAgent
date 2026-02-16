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
from core.base.logic.structures.immutable_collections import ConstantList, ConstantDict, FrozenDict, as_constant


def test_constantlist_basic():
    assert ConstantList is not None


def test_constantdict_basic():
    assert ConstantDict is not None


def test_frozendict_basic():
    assert FrozenDict is not None


def test_as_constant_basic():
    assert callable(as_constant)
