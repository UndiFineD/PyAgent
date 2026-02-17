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
from interface.slash_commands.commands.datetime_cmds import cmd_datetime, cmd_date, cmd_time, cmd_uptime, cmd_timestamp


def test_cmd_datetime_basic():
    assert callable(cmd_datetime)


def test_cmd_date_basic():
    assert callable(cmd_date)


def test_cmd_time_basic():
    assert callable(cmd_time)


def test_cmd_uptime_basic():
    assert callable(cmd_uptime)


def test_cmd_timestamp_basic():
    assert callable(cmd_timestamp)
