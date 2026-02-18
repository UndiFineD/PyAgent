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
    from interface.slash_commands.commands.system.suggested import cmd_stats, cmd_memory, cmd_health, cmd_cpu, cmd_disk, cmd_gpu, cmd_processes
except ImportError:
    from interface.slash_commands.commands.system.suggested import cmd_stats, cmd_memory, cmd_health, cmd_cpu, cmd_disk, cmd_gpu, cmd_processes



def test_cmd_stats_basic():
    assert callable(cmd_stats)


def test_cmd_memory_basic():
    assert callable(cmd_memory)


def test_cmd_health_basic():
    assert callable(cmd_health)


def test_cmd_cpu_basic():
    assert callable(cmd_cpu)


def test_cmd_disk_basic():
    assert callable(cmd_disk)


def test_cmd_gpu_basic():
    assert callable(cmd_gpu)


def test_cmd_processes_basic():
    assert callable(cmd_processes)
