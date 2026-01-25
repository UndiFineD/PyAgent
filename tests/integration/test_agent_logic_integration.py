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

# -*- coding: utf-8 -*-
"""Test classes from test_agent.py - integration module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self) -> bool: 

            return self
        def __exit__(self, *args) -> bool: 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed

class TestPhase5Integration:
    """Integration tests for Phase 5 features."""

    def test_circuit_breaker_with_agent_execution(self, tmp_path: Path, agent_module) -> None:
        """Test circuit breaker integration with agent."""
        agent = agent_module.Agent(repo_root=str(tmp_path))

        cb = agent_module.CircuitBreaker("test_backend")

        def run_agent() -> bool:
            return agent.generate_improvement_report()

        report = cb.call(run_agent)

        assert 'summary' in report
        assert cb.state == "CLOSED"

    def test_full_phase5_workflow(self, tmp_path: Path, agent_module) -> None:
        """Test complete Phase 5 workflow."""
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=False)

        # Simulate execution metrics
        agent.metrics = {
            'files_processed': 10,
            'files_modified': 7,
            'agents_applied': {'coder': 8, 'tests': 6},
            'start_time': time.time() - 15,
            'end_time': time.time(),
        }

        # Generate report
        report = agent.generate_improvement_report()
        assert 'summary' in report

        # Benchmark
        files: List[Path] = [tmp_path / f'test{i}.py' for i in range(10)]
        for f in files:
            f.write_text('# test')
        benchmark = agent.benchmark_execution(files)
        assert 'average_per_file' in benchmark

        # Cost analysis
        cost = agent.cost_analysis(cost_per_request=0.0001)
        assert 'total_estimated_cost' in cost

# ============================================================================
# EDGE CASES & ERROR HANDLING
# ============================================================================



class TestPhase6Integration:
    """Integration tests for Phase 6 features."""

    def test_full_phase6_workflow(self, tmp_path: Path, agent_module) -> None:
        """Test complete Phase 6 workflow."""
        (tmp_path / ".git").mkdir()

        # Create agent with all Phase 6 features
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        agent.enable_rate_limiting()
        agent.enable_file_locking()
        agent.enable_diff_preview()
        agent.enable_incremental_processing()
        agent.enable_graceful_shutdown()

        # Verify all features are enabled
        assert hasattr(agent, 'rate_limiter')
        assert hasattr(agent, 'lock_manager')
        assert hasattr(agent, 'diff_generator')
        assert hasattr(agent, 'incremental_processor')
        assert hasattr(agent, 'shutdown_handler')

    def test_config_with_rate_limiting(self, tmp_path: Path, agent_module) -> None:
        """Test config file with rate limiting."""
        config_path: Path = tmp_path / "agent.json"
        config_content = '''
        {
            "repo_root": ".",
            "rate_limit": {
                "requests_per_second": 2.0,
                "burst_size": 5
            }
        }
        '''
        config_path.write_text(config_content)
        (tmp_path / ".git").mkdir()

        agent = agent_module.Agent.from_config_file(config_path)

        # Rate limiting should be enabled from config
        assert hasattr(agent, 'rate_limiter')
        assert agent.rate_limiter.config.requests_per_second == 2.0

    def test_plugin_execution_with_rate_limiting(self, tmp_path: Path, agent_module) -> None:
        """Test plugins execute with rate limiting."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.enable_rate_limiting()

        # Create and register a mock plugin
        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context) -> bool:
                return True

        plugin = MockPlugin("test")
        agent.register_plugin(plugin)

        # Run plugins on a test file
        test_file: Path = tmp_path / "test.py"
        test_file.write_text("# test")

        results = agent.run_plugins(test_file)

        assert 'test' in results
        assert results['test'] is True

    def test_health_check_before_run(self, tmp_path: Path, agent_module) -> None:
        """Test health check before agent run."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        # Run health checks
        results = agent.run_health_checks()

        # Check Python is healthy
        assert results['python'].status == agent_module.HealthStatus.HEALTHY

# ============================================================================
# SESSION 9: AGENT CHAINING TESTS
# ============================================================================



