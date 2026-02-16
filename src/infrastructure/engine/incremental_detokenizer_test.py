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
from infrastructure.engine.incremental_detokenizer import StopMatch, IncrementalDetokenizer, NoOpDetokenizer, BaseIncrementalDetokenizer, FastIncrementalDetokenizer, SlowIncrementalDetokenizer, check_stop_strings, check_stop_strings_rust, validate_utf8, validate_utf8_rust


def test_stopmatch_basic():
    assert StopMatch is not None


def test_incrementaldetokenizer_basic():
    assert IncrementalDetokenizer is not None


def test_noopdetokenizer_basic():
    assert NoOpDetokenizer is not None


def test_baseincrementaldetokenizer_basic():
    assert BaseIncrementalDetokenizer is not None


def test_fastincrementaldetokenizer_basic():
    assert FastIncrementalDetokenizer is not None


def test_slowincrementaldetokenizer_basic():
    assert SlowIncrementalDetokenizer is not None


def test_check_stop_strings_basic():
    assert callable(check_stop_strings)


def test_check_stop_strings_rust_basic():
    assert callable(check_stop_strings_rust)


def test_validate_utf8_basic():
    assert callable(validate_utf8)


def test_validate_utf8_rust_basic():
    assert callable(validate_utf8_rust)
