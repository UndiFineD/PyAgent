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
from .refactor_external_batch import parse_allowlist, sanitize_filename, is_ast_safe, file_hash, process, main


def test_parse_allowlist_basic():
    assert callable(parse_allowlist)


def test_sanitize_filename_basic():
    assert callable(sanitize_filename)


def test_is_ast_safe_basic():
    assert callable(is_ast_safe)


def test_file_hash_basic():
    assert callable(file_hash)


def test_process_basic():
    assert callable(process)


def test_main_basic():
    assert callable(main)
