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
from .fuzzing import FuzzingTarget, FuzzingTechnique, FuzzingResult, FuzzingSession, AIFuzzingEngine, MultiCycleFuzzing


def test_fuzzingtarget_basic():
    assert FuzzingTarget is not None


def test_fuzzingtechnique_basic():
    assert FuzzingTechnique is not None


def test_fuzzingresult_basic():
    assert FuzzingResult is not None


def test_fuzzingsession_basic():
    assert FuzzingSession is not None


def test_aifuzzingengine_basic():
    assert AIFuzzingEngine is not None


def test_multicyclefuzzing_basic():
    assert MultiCycleFuzzing is not None
