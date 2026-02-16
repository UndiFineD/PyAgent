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
from .extract_candidates import safe_module, sanitize_filename, write_extracted, make_test, extract_candidates, main


def test_safe_module_basic():
    assert callable(safe_module)


def test_sanitize_filename_basic():
    assert callable(sanitize_filename)


def test_write_extracted_basic():
    assert callable(write_extracted)


def test_make_test_basic():
    assert callable(make_test)


def test_extract_candidates_basic():
    assert callable(extract_candidates)


def test_main_basic():
    assert callable(main)
