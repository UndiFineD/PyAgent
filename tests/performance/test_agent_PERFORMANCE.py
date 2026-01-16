# -*- coding: utf-8 -*-
"""Test classes from test_agent.py - performance module."""

from __future__ import annotations
import time
from pathlib import Path
import sys
from src.logic.agents.swarm.OrchestratorAgent import OrchestratorAgent

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import (
        AGENT_DIR,
        agent_sys_path,
        load_module_from_path,
        agent_dir_on_path,
    )
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent.parent / "src"

    class agent_sys_path:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed


class TestBenchmarking:
    """Tests for execution benchmarking."""

    def test_benchmark_execution(self, tmp_path: Path, agent_module) -> None:
        """Test execution benchmarking."""
        agent = OrchestratorAgent(repo_root=str(tmp_path))
        agent.metrics_manager.metrics = {
            "start_time": time.time() - 10,
            "end_time": time.time(),
            "files_processed": 5,
            "agents_applied": {"coder": 3, "tests": 2},
        }

        files = [tmp_path / f"test{i}.py" for i in range(5)]
        for f in files:
            f.write_text("# test")

        benchmark = agent.benchmark_execution(files)

        assert benchmark["file_count"] == 5
        assert "average_per_file" in benchmark
