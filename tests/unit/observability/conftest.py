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

"""Pytest fixtures for test_agent_stats tests."""

import pytest
from pathlib import Path
from typing import Any

# Add src to path


@pytest.fixture
def stats_module() -> Any:
    """Load and return the stats module."""
    import src.observability.stats as stats

    return stats


@pytest.fixture
def agent(stats_module: Any, tmp_path: Path) -> Any:
    """Create a StatsAgent instance for testing."""
    StatsAgent = stats_module.StatsAgent
    test_file = tmp_path / "test_stats.md"
    test_file.write_text("# Test Stats\n")
    return StatsAgent(str(test_file))


@pytest.fixture
def report_module() -> Any:
    """Fixture to provide the report generation module."""
    try:
        import src.observability.reports as reports

        return reports
    except ImportError:
        # Fallback to loading it manually if path setup is tricky
        AGENT_DIR = Path(__file__).parent.parent.parent.parent / "src"

        import observability.reports as reports

        return reports
