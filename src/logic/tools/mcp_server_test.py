#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import pytest
except ImportError:
    import pytest

try:
    from logic.tools.mcp_server import init_openspec, create_sdd_spec, confirm_proceed, create_task, store_memory
except ImportError:
    from logic.tools.mcp_server import init_openspec, create_sdd_spec, confirm_proceed, create_task, store_memory



def test_init_openspec_basic():
    assert callable(init_openspec)


def test_create_sdd_spec_basic():
    assert callable(create_sdd_spec)


def test_confirm_proceed_basic():
    assert callable(confirm_proceed)


def test_create_task_basic():
    assert callable(create_task)


def test_store_memory_basic():
    assert callable(store_memory)
