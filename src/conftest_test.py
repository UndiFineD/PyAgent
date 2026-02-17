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

import pytest
from .conftest import pytest_ignore_collect, agent_module, agent_backend_module, base_agent_module, agent_sandbox, transactional_test_env


def test_pytest_ignore_collect_basic():
    assert callable(pytest_ignore_collect)


def test_agent_module_basic():
    assert callable(agent_module)


def test_agent_backend_module_basic():
    assert callable(agent_backend_module)


def test_base_agent_module_basic():
    assert callable(base_agent_module)


def test_agent_sandbox_basic():
    assert callable(agent_sandbox)


def test_transactional_test_env_basic():
    assert callable(transactional_test_env)
