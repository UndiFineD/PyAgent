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
from interface.slash_commands.api import get_slash_commands, reset_slash_commands, process_prompt, execute_command, get_help


def test_get_slash_commands_basic():
    assert callable(get_slash_commands)


def test_reset_slash_commands_basic():
    assert callable(reset_slash_commands)


def test_process_prompt_basic():
    assert callable(process_prompt)


def test_execute_command_basic():
    assert callable(execute_command)


def test_get_help_basic():
    assert callable(get_help)
