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
from interface.slash_commands.loader import get_commands_dir, discover_command_modules, load_module, unload_module, load_commands, reload_commands, is_loaded, get_loaded_modules


def test_get_commands_dir_basic():
    assert callable(get_commands_dir)


def test_discover_command_modules_basic():
    assert callable(discover_command_modules)


def test_load_module_basic():
    assert callable(load_module)


def test_unload_module_basic():
    assert callable(unload_module)


def test_load_commands_basic():
    assert callable(load_commands)


def test_reload_commands_basic():
    assert callable(reload_commands)


def test_is_loaded_basic():
    assert callable(is_loaded)


def test_get_loaded_modules_basic():
    assert callable(get_loaded_modules)
