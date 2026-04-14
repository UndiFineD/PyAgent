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
"""Shared pytest fixtures for the PyAgent test suite (prj0000023).

These fixtures provide:
- tmp_agent_dir: isolated temporary directory per-test
- sample_task: a minimal task dict
- sample_message: a minimal swarm Message dict
- async_client: a simple async HTTP test client scaffold
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

# ---------------------------------------------------------------------------
# Directory fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def tmp_agent_dir(tmp_path: Path) -> Path:
    """Return a temporary directory for agent sandbox tests."""
    agent_dir = tmp_path / "agent_sandbox"
    agent_dir.mkdir()
    return agent_dir


@pytest.fixture()
def tmp_project_dir(tmp_path: Path) -> Path:
    """Return a temporary directory mimicking the project/ layout."""
    d = tmp_path / "project"
    for sub in ("templates", "config"):
        (d / sub).mkdir(parents=True)
    return d


# ---------------------------------------------------------------------------
# Data fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def sample_task() -> dict[str, Any]:
    """Return a minimal valid task payload dict."""
    return {"action": "run", "target": "test_file.py", "priority": 3}


@pytest.fixture()
def sample_message() -> dict[str, Any]:
    """Return a minimal valid swarm Message dict."""
    return {
        "id": "test-uuid",
        "timestamp": "2026-01-01T00:00:00Z",
        "type": "task_request",
        "priority": "high",
        "source": "agent-1",
        "destination": "scheduler",
        "payload": {"key": "value"},
        "checksum": "0",
    }


@pytest.fixture()
def sample_risk_table(tmp_path: Path) -> Path:
    """Write a sample pipe-delimited risk matrix and return the path."""
    content = (
        "| Title | Probability | Impact | Mitigation |\n"
        "|---|---|---|---|\n"
        "| Auth bypass | high | high | Use MFA |\n"
        "| Data leak | medium | low | Encrypt at rest |\n"
    )
    f = tmp_path / "risk.md"
    f.write_text(content, encoding="utf-8")
    return f
