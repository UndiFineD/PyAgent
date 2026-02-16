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
from interface.slash_commands.commands.environment.suggested import cmd_version, cmd_env, cmd_python, cmd_cwd, cmd_hostname, cmd_user, cmd_venv


def test_cmd_version_basic():
    assert callable(cmd_version)


def test_cmd_env_basic():
    assert callable(cmd_env)


def test_cmd_python_basic():
    assert callable(cmd_python)


def test_cmd_cwd_basic():
    assert callable(cmd_cwd)


def test_cmd_hostname_basic():
    assert callable(cmd_hostname)


def test_cmd_user_basic():
    assert callable(cmd_user)


def test_cmd_venv_basic():
    assert callable(cmd_venv)
