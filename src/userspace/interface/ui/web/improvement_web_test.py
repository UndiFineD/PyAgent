#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from .improvement_web import load_reasoning_chains, load_audit_log, save_steering_directive, load_self_improvement_log_tail, format_timestamp, main


def test_load_reasoning_chains_basic():
    assert callable(load_reasoning_chains)


def test_load_audit_log_basic():
    assert callable(load_audit_log)


def test_save_steering_directive_basic():
    assert callable(save_steering_directive)


def test_load_self_improvement_log_tail_basic():
    assert callable(load_self_improvement_log_tail)


def test_format_timestamp_basic():
    assert callable(format_timestamp)


def test_main_basic():
    assert callable(main)
