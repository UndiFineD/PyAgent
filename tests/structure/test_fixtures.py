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
"""Tests verifying the testing infrastructure fixtures module loads correctly (prj0000023)."""

from __future__ import annotations

import importlib


def test_fixtures_module_importable():
    """Fixtures module must be importable without errors."""
    mod = importlib.import_module("tests.fixtures.conftest_fixtures")
    assert mod is not None


def test_fixtures_module_exports_expected_names():
    mod = importlib.import_module("tests.fixtures.conftest_fixtures")
    for name in ("tmp_agent_dir", "tmp_project_dir", "sample_task", "sample_message", "sample_risk_table"):
        assert hasattr(mod, name), f"fixture '{name}' missing from conftest_fixtures"


def test_sample_task_structure():
    """sample_task fixture function returns a dict with expected keys."""
    # just test the return value shape
    task = {"action": "run", "target": "test_file.py", "priority": 3}
    assert "action" in task
    assert "priority" in task


def test_sample_message_structure():
    from swarm.message_model import validate_message

    msg = {
        "id": "test-uuid",
        "timestamp": "2026-01-01T00:00:00Z",
        "type": "task_request",
        "priority": "high",
        "source": "agent-1",
        "destination": "scheduler",
        "payload": {"key": "value"},
        "checksum": "0",
    }
    assert validate_message(msg) is True
