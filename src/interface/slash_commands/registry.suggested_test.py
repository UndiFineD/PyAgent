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
    from interface.slash_commands.registry.suggested import get_global_registry, reset_global_registry, register, register_command, command, unregister, enable_command, disable_command, list_commands
except ImportError:
    from interface.slash_commands.registry.suggested import get_global_registry, reset_global_registry, register, register_command, command, unregister, enable_command, disable_command, list_commands



def test_get_global_registry_basic():
    assert callable(get_global_registry)


def test_reset_global_registry_basic():
    assert callable(reset_global_registry)


def test_register_basic():
    assert callable(register)


def test_register_command_basic():
    assert callable(register_command)


def test_command_basic():
    assert callable(command)


def test_unregister_basic():
    assert callable(unregister)


def test_enable_command_basic():
    assert callable(enable_command)


def test_disable_command_basic():
    assert callable(disable_command)


def test_list_commands_basic():
    assert callable(list_commands)
