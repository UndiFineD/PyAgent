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
    from .pyagent_cli import check_server, list_agents, run_task, main
except ImportError:
    from .pyagent_cli import check_server, list_agents, run_task, main



def test_check_server_basic():
    assert callable(check_server)


def test_list_agents_basic():
    assert callable(list_agents)


def test_run_task_basic():
    assert callable(run_task)


def test_main_basic():
    assert callable(main)
