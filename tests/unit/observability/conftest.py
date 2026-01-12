"""Pytest fixtures for test_agent_stats tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from tests.utils.agent_test_utils import agent_dir_on_path, load_agent_module


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
        AGENT_DIR = Path(__file__).parent.parent.parent.parent / 'src'
        sys.path.insert(0, str(AGENT_DIR))
        import observability.reports as reports
        return reports
