# -*- coding: utf-8 -*-
"""Test classes from test_agent.py - core module."""

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
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args) -> str: 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))


# Core Logic and Utility Tests

class TestAgentExecutionStateEnum:
    """Test AgentExecutionState enum."""

    def test_enum_values_exist(self, agent_module) -> None:
        """Verify all execution state values exist."""
        states = agent_module.AgentExecutionState
        assert states.PENDING is not None
        assert states.RUNNING is not None
        assert states.COMPLETED is not None
        assert states.FAILED is not None
        assert states.CANCELLED is not None
        assert states.PAUSED is not None

    def test_enum_values_are_unique(self, agent_module) -> None:
        """Verify enum values are unique."""
        states = agent_module.AgentExecutionState
        values = [s.value for s in states]
        assert len(values) == len(set(values))



class TestRateLimitStrategyEnum:
    """Test RateLimitStrategy enum."""

    def test_all_strategies_exist(self, agent_module) -> None:
        """Verify all rate limit strategies exist."""
        strategies = agent_module.RateLimitStrategy
        assert strategies.FIXED_WINDOW is not None
        assert strategies.SLIDING_WINDOW is not None
        assert strategies.TOKEN_BUCKET is not None
        assert strategies.LEAKY_BUCKET is not None



class TestConfigFormatEnum:
    """Test ConfigFormat enum."""

    def test_all_formats_exist(self, agent_module) -> None:
        """Verify all config formats exist."""
        formats = agent_module.ConfigFormat
        assert formats.YAML is not None
        assert formats.TOML is not None
        assert formats.JSON is not None
        assert formats.INI is not None



class TestLockTypeEnum:
    """Test LockType enum."""

    def test_all_lock_types_exist(self, agent_module) -> None:
        """Verify all lock types exist."""
        locks = agent_module.LockType
        assert locks.SHARED is not None
        assert locks.EXCLUSIVE is not None
        assert locks.ADVISORY is not None



class TestDiffOutputFormatEnum:
    """Test DiffOutputFormat enum."""

    def test_all_formats_exist(self, agent_module) -> None:
        """Verify all diff output formats exist."""
        formats = agent_module.DiffOutputFormat
        assert formats.UNIFIED is not None
        assert formats.CONTEXT is not None
        assert formats.SIDE_BY_SIDE is not None
        assert formats.HTML is not None



class TestAgentPriorityEnum:
    """Test AgentPriority enum."""

    def test_all_priorities_exist(self, agent_module) -> None:
        """Verify all priority levels exist."""
        priorities = agent_module.AgentPriority
        assert priorities.CRITICAL is not None
        assert priorities.HIGH is not None
        assert priorities.NORMAL is not None
        assert priorities.LOW is not None
        assert priorities.BACKGROUND is not None

    def test_priority_ordering(self, agent_module) -> None:
        """Verify priority ordering is correct."""
        priorities = agent_module.AgentPriority
        assert priorities.CRITICAL.value < priorities.HIGH.value
        assert priorities.HIGH.value < priorities.NORMAL.value
        assert priorities.NORMAL.value < priorities.LOW.value
        assert priorities.LOW.value < priorities.BACKGROUND.value



class TestHealthStatusEnum:
    """Test HealthStatus enum."""

    def test_all_statuses_exist(self, agent_module) -> None:
        """Verify all health statuses exist."""
        statuses = agent_module.HealthStatus
        assert statuses.HEALTHY is not None
        assert statuses.DEGRADED is not None
        assert statuses.UNHEALTHY is not None
        assert statuses.UNKNOWN is not None



class TestRateLimitConfigDataclass:
    """Test RateLimitConfig dataclass."""

    def test_default_values(self, agent_module) -> None:
        """Verify default values are set correctly."""
        config = agent_module.RateLimitConfig()
        assert config.requests_per_second == 10.0
        assert config.requests_per_minute == 60
        assert config.burst_size == 10
        assert config.cooldown_seconds == 1.0

    def test_custom_values(self, agent_module) -> None:
        """Verify custom values can be set."""
        config = agent_module.RateLimitConfig(
            requests_per_second=5.0,
            requests_per_minute=30,
            burst_size=5,
            cooldown_seconds=0.5
        )
        assert config.requests_per_second == 5.0
        assert config.requests_per_minute == 30
        assert config.burst_size == 5
        assert config.cooldown_seconds == 0.5



class TestAgentPluginConfigDataclass:
    """Test AgentPluginConfig dataclass."""

    def test_required_fields(self, agent_module) -> None:
        """Verify required fields are enforced."""
        config = agent_module.AgentPluginConfig(
            name="test_plugin",
            module_path="/path / to / plugin.py"
        )
        assert config.name == "test_plugin"
        assert config.module_path == "/path / to / plugin.py"
        assert config.entry_point == "run"
        assert config.enabled is True

    def test_custom_priority(self, agent_module) -> None:
        """Verify custom priority can be set."""
        config = agent_module.AgentPluginConfig(
            name="critical_plugin",
            module_path="/path / to / plugin.py",
            priority=agent_module.AgentPriority.CRITICAL
        )
        assert config.priority == agent_module.AgentPriority.CRITICAL



class TestFileLockDataclass:
    """Test FileLock dataclass."""

    def test_file_lock_creation(self, tmp_path: Path, agent_module) -> None:
        """Verify FileLock can be created."""
        lock = agent_module.FileLock(
            file_path=tmp_path / "test.py",
            lock_type=agent_module.LockType.EXCLUSIVE,
            owner="test_owner",
            acquired_at=time.time()
        )
        assert lock.file_path == tmp_path / "test.py"
        assert lock.lock_type == agent_module.LockType.EXCLUSIVE
        assert lock.owner == "test_owner"
        assert lock.expires_at is None



class TestDiffResultDataclass:
    """Test DiffResult dataclass."""

    def test_diff_result_creation(self, tmp_path: Path, agent_module) -> None:
        """Verify DiffResult can be created."""
        result = agent_module.DiffResult(
            file_path=tmp_path / "test.py",
            original_content="old content",
            modified_content="new content"
        )
        assert result.file_path == tmp_path / "test.py"
        assert result.original_content == "old content"
        assert result.modified_content == "new content"
        assert result.additions == 0
        assert result.deletions == 0



class TestIncrementalStateDataclass:
    """Test IncrementalState dataclass."""

    def test_default_values(self, agent_module) -> None:
        """Verify default values are set correctly."""
        state = agent_module.IncrementalState()
        assert state.last_run_timestamp == 0.0
        assert state.processed_files == {}
        assert state.file_hashes == {}
        assert state.pending_files == []



class TestAgentHealthCheckDataclass:
    """Test AgentHealthCheck dataclass."""

    def test_health_check_creation(self, agent_module) -> None:
        """Verify AgentHealthCheck can be created."""
        check = agent_module.AgentHealthCheck(
            agent_name="coder",
            status=agent_module.HealthStatus.HEALTHY,
            response_time_ms=50.0
        )
        assert check.agent_name == "coder"
        assert check.status == agent_module.HealthStatus.HEALTHY
        assert check.response_time_ms == 50.0
        assert check.error_message is None



class TestShutdownStateDataclass:
    """Test ShutdownState dataclass."""

    def test_default_values(self, agent_module) -> None:
        """Verify default values are set correctly."""
        state = agent_module.ShutdownState()
        assert state.shutdown_requested is False
        assert state.current_file is None
        assert state.completed_files == []
        assert state.pending_files == []



class TestRateLimiter:
    """Test RateLimiter class."""

    def test_rate_limiter_creation(self, agent_module) -> None:
        """Verify RateLimiter can be created."""
        limiter = agent_module.RateLimiter()
        assert limiter.config is not None
        assert limiter.tokens > 0

    def test_acquire_token(self, agent_module) -> None:
        """Verify token can be acquired."""
        limiter = agent_module.RateLimiter()
        result = limiter.acquire(timeout=1.0)
        assert result is True

    def test_get_stats(self, agent_module) -> None:
        """Verify stats can be retrieved."""
        limiter = agent_module.RateLimiter()
        stats = limiter.get_stats()
        assert 'tokens_available' in stats
        assert 'requests_last_minute' in stats
        assert 'requests_per_second' in stats
        assert 'burst_size' in stats

    def test_custom_config(self, agent_module) -> None:
        """Verify custom config is applied."""
        config = agent_module.RateLimitConfig(
            requests_per_second=1.0,
            burst_size=2
        )
        limiter = agent_module.RateLimiter(config)
        assert limiter.config.requests_per_second == 1.0
        assert limiter.config.burst_size == 2



class TestFileLockManager:
    """Test FileLockManager class."""

    def test_lock_manager_creation(self, agent_module) -> None:
        """Verify FileLockManager can be created."""
        manager = agent_module.FileLockManager()
        assert manager.lock_timeout == 300.0
        assert manager.locks == {}

    def test_acquire_and_release_lock(self, tmp_path: Path, agent_module) -> None:
        """Verify lock can be acquired and released."""
        manager = agent_module.FileLockManager()
        test_file: Path = tmp_path / "test.py"
        test_file.write_text("test")

        lock = manager.acquire_lock(test_file)
        assert lock is not None
        assert lock.lock_type == agent_module.LockType.EXCLUSIVE

        result = manager.release_lock(test_file)
        assert result is True

    def test_shared_lock_allows_multiple(self, tmp_path: Path, agent_module) -> None:
        """Verify shared locks can coexist."""
        manager = agent_module.FileLockManager()
        test_file: Path = tmp_path / "test.py"
        test_file.write_text("test")

        lock1 = manager.acquire_lock(test_file, lock_type=agent_module.LockType.SHARED)
        assert lock1 is not None

        lock2 = manager.acquire_lock(test_file, lock_type=agent_module.LockType.SHARED)
        assert lock2 is not None



class TestDiffGenerator:
    """Test DiffGenerator class."""

    def test_diff_generator_creation(self, agent_module) -> None:
        """Verify DiffGenerator can be created."""
        generator = agent_module.DiffGenerator()
        assert generator.output_format == agent_module.DiffOutputFormat.UNIFIED
        assert generator.context_lines == 3

    def test_generate_diff(self, tmp_path: Path, agent_module) -> None:
        """Verify diff can be generated."""
        generator = agent_module.DiffGenerator()
        test_file: Path = tmp_path / "test.py"

        result = generator.generate_diff(
            test_file,
            "line1\nline2\nline3",
            "line1\nmodified\nline3"
        )

        assert result.file_path == test_file
        assert result.additions > 0 or result.deletions > 0
        assert len(result.diff_lines) > 0

    def test_format_diff_unified(self, tmp_path: Path, agent_module) -> None:
        """Verify unified diff format works."""
        generator = agent_module.DiffGenerator()
        test_file: Path = tmp_path / "test.py"

        diff_result = generator.generate_diff(
            test_file,
            "old",
            "new"
        )

        formatted = generator.format_diff(diff_result)
        assert isinstance(formatted, str)

    def test_format_diff_html(self, tmp_path: Path, agent_module) -> None:
        """Verify HTML diff format works."""
        generator = agent_module.DiffGenerator()
        test_file: Path = tmp_path / "test.py"

        diff_result = generator.generate_diff(
            test_file,
            "old",
            "new"
        )

        formatted = generator.format_diff(
            diff_result,
            agent_module.DiffOutputFormat.HTML
        )
        assert '<html>' in formatted.lower() or '<table' in formatted.lower()



class TestIncrementalProcessor:
    """Test IncrementalProcessor class."""

    def test_processor_creation(self, tmp_path: Path, agent_module) -> None:
        """Verify IncrementalProcessor can be created."""
        processor = agent_module.IncrementalProcessor(tmp_path)
        assert processor.repo_root == tmp_path
        assert processor.state is not None

    def test_get_changed_files_all_new(self, tmp_path: Path, agent_module) -> None:
        """Verify all files are returned when none processed."""
        processor = agent_module.IncrementalProcessor(tmp_path)

        file1: Path = tmp_path / "test1.py"
        file2: Path = tmp_path / "test2.py"
        file1.write_text("test1")
        file2.write_text("test2")

        changed = processor.get_changed_files([file1, file2])
        assert len(changed) == 2

    def test_mark_processed(self, tmp_path: Path, agent_module) -> None:
        """Verify file can be marked as processed."""
        processor = agent_module.IncrementalProcessor(tmp_path)
        test_file: Path = tmp_path / "test.py"
        test_file.write_text("test")

        processor.mark_processed(test_file)

        assert str(test_file) in processor.state.processed_files
        assert str(test_file) in processor.state.file_hashes

    def test_reset_state(self, tmp_path: Path, agent_module) -> None:
        """Verify state can be reset."""
        processor = agent_module.IncrementalProcessor(tmp_path)
        test_file: Path = tmp_path / "test.py"
        test_file.write_text("test")

        processor.mark_processed(test_file)
        processor.reset_state()

        assert processor.state.processed_files == {}
        assert processor.state.file_hashes == {}



class TestGracefulShutdown:
    """Test GracefulShutdown class."""

    def test_shutdown_creation(self, tmp_path: Path, agent_module) -> None:
        """Verify GracefulShutdown can be created."""
        handler = agent_module.GracefulShutdown(tmp_path)
        assert handler.repo_root == tmp_path
        assert handler.state.shutdown_requested is False

    def test_should_continue_initially(self, tmp_path: Path, agent_module) -> None:
        """Verify should_continue returns True initially."""
        handler = agent_module.GracefulShutdown(tmp_path)
        assert handler.should_continue() is True

    def test_set_current_file(self, tmp_path: Path, agent_module) -> None:
        """Verify current file can be set."""
        handler = agent_module.GracefulShutdown(tmp_path)
        test_file: Path = tmp_path / "test.py"

        handler.set_current_file(test_file)
        assert handler.state.current_file == str(test_file)

        handler.set_current_file(None)
        assert handler.state.current_file is None

    def test_mark_completed(self, tmp_path: Path, agent_module) -> None:
        """Verify file can be marked as completed."""
        handler = agent_module.GracefulShutdown(tmp_path)
        test_file: Path = tmp_path / "test.py"

        handler.mark_completed(test_file)
        assert str(test_file) in handler.state.completed_files

    def test_set_pending_files(self, tmp_path: Path, agent_module) -> None:
        """Verify pending files can be set."""
        handler = agent_module.GracefulShutdown(tmp_path)
        files: List[Path] = [tmp_path / "test1.py", tmp_path / "test2.py"]

        handler.set_pending_files(files)
        assert len(handler.state.pending_files) == 2



class TestConfigLoader:
    """Test ConfigLoader class."""

    def test_loader_creation_without_path(self, agent_module) -> None:
        """Verify ConfigLoader can be created without path."""
        loader = agent_module.ConfigLoader()
        assert loader.config_path is None

    def test_loader_creation_with_json_path(self, tmp_path: Path, agent_module) -> None:
        """Verify ConfigLoader detects JSON format."""
        config_path: Path = tmp_path / "config.json"
        loader = agent_module.ConfigLoader(config_path)
        assert loader.format == agent_module.ConfigFormat.JSON

    def test_loader_creation_with_yaml_path(self, tmp_path: Path, agent_module) -> None:
        """Verify ConfigLoader detects YAML format."""
        config_path: Path = tmp_path / "config.yaml"
        loader = agent_module.ConfigLoader(config_path)
        assert loader.format == agent_module.ConfigFormat.YAML

    def test_load_json_config(self, tmp_path: Path, agent_module) -> None:
        """Verify JSON config can be loaded."""
        config_path: Path = tmp_path / "config.json"
        config_path.write_text('{"repo_root": ".", "dry_run": true, "loop": 3}')

        loader = agent_module.ConfigLoader(config_path)
        config = loader.load()

        assert config.dry_run is True
        assert config.loop == 3

    def test_find_config_file(self, tmp_path: Path, agent_module) -> None:
        """Verify config file can be found."""
        config_path: Path = tmp_path / "agent.json"
        config_path.write_text('{}')

        found = agent_module.ConfigLoader.find_config_file(tmp_path)
        assert found == config_path

    def test_find_config_file_not_found(self, tmp_path: Path, agent_module) -> None:
        """Verify None returned when no config found."""
        found = agent_module.ConfigLoader.find_config_file(tmp_path)
        assert found is None



class TestHealthChecker:
    """Test HealthChecker class."""

    def test_checker_creation(self, tmp_path: Path, agent_module) -> None:
        """Verify HealthChecker can be created."""
        checker = agent_module.HealthChecker(tmp_path)
        assert checker.repo_root == tmp_path
        assert checker.results == {}

    def test_check_python(self, tmp_path: Path, agent_module) -> None:
        """Verify Python check returns healthy."""
        checker = agent_module.HealthChecker(tmp_path)
        result = checker.check_python()

        assert result.agent_name == 'python'
        assert result.status == agent_module.HealthStatus.HEALTHY
        assert 'version' in result.details

    def test_check_git(self, tmp_path: Path, agent_module) -> None:
        """Verify git check runs."""
        checker = agent_module.HealthChecker(tmp_path)
        result = checker.check_git()

        assert result.agent_name == 'git'
        # May be healthy or unhealthy depending on git availability
        assert result.status in [
            agent_module.HealthStatus.HEALTHY,
            agent_module.HealthStatus.UNHEALTHY
        ]

    def test_run_all_checks(self, tmp_path: Path, agent_module) -> None:
        """Verify all checks can be run."""
        checker = agent_module.HealthChecker(tmp_path)
        results = checker.run_all_checks()

        assert 'python' in results
        assert 'git' in results
        # Agent scripts will be unhealthy in test environment
        assert 'coder' in results



class TestAgentPluginSystem:
    """Test Agent plugin system methods."""

    def test_register_plugin(self, tmp_path: Path, agent_module) -> None:
        """Verify plugin can be registered."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        # Create a mock plugin
        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context) -> bool:
                return True

        plugin = MockPlugin("test_plugin")
        agent.register_plugin(plugin)

        assert "test_plugin" in agent.plugins

    def test_unregister_plugin(self, tmp_path: Path, agent_module) -> None:
        """Verify plugin can be unregistered."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context) -> bool:
                return True

        plugin = MockPlugin("test_plugin")
        agent.register_plugin(plugin)

        result = agent.unregister_plugin("test_plugin")
        assert result is True
        assert "test_plugin" not in agent.plugins

    def test_get_plugin(self, tmp_path: Path, agent_module) -> None:
        """Verify plugin can be retrieved."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        class MockPlugin(agent_module.AgentPluginBase):
            def run(self, file_path, context) -> bool:
                return True

        plugin = MockPlugin("test_plugin")
        agent.register_plugin(plugin)

        retrieved = agent.get_plugin("test_plugin")
        assert retrieved is plugin



class TestAgentRateLimiting:
    """Test Agent rate limiting methods."""

    def test_enable_rate_limiting(self, tmp_path: Path, agent_module) -> None:
        """Verify rate limiting can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.enable_rate_limiting()

        assert hasattr(agent, 'rate_limiter')
        assert agent.rate_limiter is not None

    def test_enable_rate_limiting_with_config(self, tmp_path: Path, agent_module) -> None:
        """Verify rate limiting can be enabled with custom config."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        config = agent_module.RateLimitConfig(requests_per_second=5.0)
        agent.enable_rate_limiting(config)

        assert agent.rate_limiter.config.requests_per_second == 5.0

    def test_get_rate_limit_stats(self, tmp_path: Path, agent_module) -> None:
        """Verify rate limit stats can be retrieved."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.enable_rate_limiting()
        stats = agent.get_rate_limit_stats()

        assert 'tokens_available' in stats



class TestAgentFileLocking:
    """Test Agent file locking methods."""

    def test_enable_file_locking(self, tmp_path: Path, agent_module) -> None:
        """Verify file locking can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.enable_file_locking()

        assert hasattr(agent, 'lock_manager')
        assert agent.lock_manager is not None

    def test_enable_file_locking_with_timeout(self, tmp_path: Path, agent_module) -> None:
        """Verify file locking can be enabled with custom timeout."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.enable_file_locking(lock_timeout=600.0)

        assert agent.lock_manager.lock_timeout == 600.0



class TestAgentDiffPreview:
    """Test Agent diff preview methods."""

    def test_enable_diff_preview(self, tmp_path: Path, agent_module) -> None:
        """Verify diff preview can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.enable_diff_preview()

        assert hasattr(agent, 'diff_generator')
        assert agent.diff_generator is not None

    def test_preview_changes(self, tmp_path: Path, agent_module) -> None:
        """Verify changes can be previewed."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        test_file: Path = tmp_path / "test.py"
        test_file.write_text("old content")

        diff = agent.preview_changes(test_file, "new content")

        assert diff.original_content == "old content"
        assert diff.modified_content == "new content"



class TestAgentIncrementalProcessing:
    """Test Agent incremental processing methods."""

    def test_enable_incremental_processing(self, tmp_path: Path, agent_module) -> None:
        """Verify incremental processing can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.enable_incremental_processing()

        assert hasattr(agent, 'incremental_processor')
        assert agent.incremental_processor is not None

    def test_get_changed_files(self, tmp_path: Path, agent_module) -> None:
        """Verify changed files can be retrieved."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.enable_incremental_processing()

        file1: Path = tmp_path / "test1.py"
        file1.write_text("test")

        changed = agent.get_changed_files([file1])
        assert len(changed) == 1

    def test_reset_incremental_state(self, tmp_path: Path, agent_module) -> None:
        """Verify incremental state can be reset."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.enable_incremental_processing()

        # Process a file
        file1: Path = tmp_path / "test1.py"
        file1.write_text("test")
        agent.incremental_processor.mark_processed(file1)

        # Reset
        agent.reset_incremental_state()

        assert agent.incremental_processor.state.processed_files == {}



class TestAgentGracefulShutdown:
    """Test Agent graceful shutdown methods."""

    def test_enable_graceful_shutdown(self, tmp_path: Path, agent_module) -> None:
        """Verify graceful shutdown can be enabled."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.enable_graceful_shutdown()

        assert hasattr(agent, 'shutdown_handler')
        assert agent.shutdown_handler is not None

    def test_resume_from_shutdown_no_state(self, tmp_path: Path, agent_module) -> None:
        """Verify None returned when no resume state."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        result = agent.resume_from_shutdown()
        assert result is None



class TestAgentHealthChecks:
    """Test Agent health check methods."""

    def test_run_health_checks(self, tmp_path: Path, agent_module) -> None:
        """Verify health checks can be run."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        results = agent.run_health_checks()

        assert 'python' in results
        assert 'git' in results

    def test_is_healthy(self, tmp_path: Path, agent_module) -> None:
        """Verify is_healthy returns boolean."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        result = agent.is_healthy()

        assert isinstance(result, bool)



class TestAgentConfigFile:
    """Test Agent configuration file methods."""

    def test_from_config_file(self, tmp_path: Path, agent_module) -> None:
        """Verify Agent can be created from config file."""
        config_path: Path = tmp_path / "agent.json"
        config_path.write_text(
            '{"repo_root": "' +
            str(tmp_path).replace(
                '\\',
                '\\\\') +
            '", "dry_run": true}')
        (tmp_path / ".git").mkdir()

        agent = agent_module.Agent.from_config_file(config_path)

        assert agent.dry_run is True

    def test_auto_configure_no_config(self, tmp_path: Path, agent_module) -> None:
        """Verify auto_configure works without config file."""
        (tmp_path / ".git").mkdir()

        agent = agent_module.Agent.auto_configure(str(tmp_path))

        assert agent is not None
        assert agent.repo_root == tmp_path

    def test_auto_configure_with_config(self, tmp_path: Path, agent_module) -> None:
        """Verify auto_configure uses config file if found."""
        config_path: Path = tmp_path / "agent.json"
        config_path.write_text('{"loop": 5}')
        (tmp_path / ".git").mkdir()

        agent = agent_module.Agent.auto_configure(str(tmp_path))

        assert agent.loop == 5

# ============================================================================
# PHASE 6 INTEGRATION TESTS
# ============================================================================



class TestAgentChain:
    """Tests for AgentChain class."""

    def test_chain_init(self, agent_module) -> None:
        """Test AgentChain initialization."""
        AgentChain = agent_module.AgentChain

        chain = AgentChain(name="test_chain")
        assert chain.name == "test_chain"

    def test_add_step(self, agent_module) -> None:
        """Test adding steps to chain."""
        AgentChain = agent_module.AgentChain

        chain = AgentChain()
        result = chain.add_step("coder")

        assert result is chain  # Returns self for chaining
        assert len(chain._steps) == 1

    def test_execute_chain(self, agent_module) -> None:
        """Test executing agent chain."""
        AgentChain = agent_module.AgentChain

        chain = AgentChain()
        chain.add_step("step1")
        chain.add_step("step2")

        def mock_executor(agent_name, input_data) -> str:
            return f"{input_data}->{agent_name}"

        results = chain.execute("start", mock_executor)

        assert len(results) == 2
        assert results[0]["success"]
        assert results[1]["output"] == "start->step1->step2"

# ============================================================================
# SESSION 9: GIT BRANCH PROCESSOR TESTS
# ============================================================================



