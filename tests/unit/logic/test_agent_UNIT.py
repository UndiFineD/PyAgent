# -*- coding: utf-8 -*-
"""Test classes from test_agent.py - core module."""

from __future__ import annotations
from typing import List, Dict
import time
import pytest
import logging
from pathlib import Path
import sys
import os

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / 'src'

    class agent_sys_path:
        def __enter__(self) -> bool:

            return self







        def __exit__(self, *args) -> str:
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed


class TestDryRunMode:
    """Test dry-run mode functionality."""

    def test_dry_run_flag_set_on_init(self, tmp_path: Path, agent_module) -> None:
        """Verify dry_run flag is set correctly on Agent initialization."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True)
        assert agent.dry_run is True

    def test_dry_run_false_by_default(self, tmp_path: Path, agent_module) -> None:
        """Verify dry_run is False by default."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert agent.dry_run is False

    def test_dry_run_mode_logged(self, tmp_path: Path, agent_module, caplog) -> None:
        """Verify dry-run mode is logged when enabled."""
        (tmp_path / ".git").mkdir()
        with caplog.at_level(logging.INFO):
            agent_module.Agent(repo_root=str(tmp_path),
                               dry_run=True)
        assert "DRY RUN MODE" in caplog.text


class TestSelectiveAgentExecution:
    """Test selective agent execution (--only-agents)."""

    def test_selective_agents_stored_as_set(self, tmp_path: Path, agent_module) -> None:
        """Verify selective agents are stored as a set."""
        (tmp_path / ".git").mkdir()
        agents: List[str] = ['coder', 'tests']
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            selective_agents=agents
        )
        assert isinstance(agent.selective_agents, set)
        assert agent.selective_agents == {'coder', 'tests'}

    def test_selective_agents_none_by_default(self, tmp_path: Path, agent_module) -> None:
        """Verify selective_agents is empty set by default."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert agent.selective_agents == set()

    def test_should_execute_agent_returns_true_when_no_filter(self, tmp_path: Path, agent_module) -> None:
        """Verify all agents execute when no selective filter applied."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        assert agent.should_execute_agent('coder') is True
        assert agent.should_execute_agent('tests') is True
        assert agent.should_execute_agent('documentation') is True

    def test_should_execute_agent_respects_filter(self, tmp_path: Path, agent_module) -> None:
        """Verify selective filter is respected."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            selective_agents=['coder', 'tests']
        )

        assert agent.should_execute_agent('coder') is True
        assert agent.should_execute_agent('tests') is True
        assert agent.should_execute_agent('documentation') is False

    def test_should_execute_agent_case_insensitive(self, tmp_path: Path, agent_module) -> None:
        """Verify agent name matching is case-insensitive."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            selective_agents=['coder']
        )

        assert agent.should_execute_agent('CODER') is True
        assert agent.should_execute_agent('Coder') is True
        assert agent.should_execute_agent('coder') is True


class TestConfigurableTimeouts:
    """Test per-agent timeout configuration."""

    def test_timeout_per_agent_stored(self, tmp_path: Path, agent_module) -> None:
        """Verify timeout_per_agent dict is stored correctly."""
        (tmp_path / ".git").mkdir()
        timeouts: Dict[str, int] = {'coder': 60, 'tests': 300}
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            timeout_per_agent=timeouts
        )
        assert agent.timeout_per_agent == timeouts

    def test_timeout_per_agent_defaults_to_empty_dict(self, tmp_path: Path, agent_module) -> None:
        """Verify timeout_per_agent defaults to empty dict."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert agent.timeout_per_agent == {}

    def test_get_timeout_for_agent_returns_configured_value(self, tmp_path: Path, agent_module) -> None:
        """Verify configured timeout is returned."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            timeout_per_agent={'coder': 60}
        )
        assert agent.get_timeout_for_agent('coder') == 60

    def test_get_timeout_for_agent_returns_default(self, tmp_path: Path, agent_module) -> None:
        """Verify default timeout returned for unconfigured agent."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(
            repo_root=str(tmp_path),
            timeout_per_agent={'coder': 60}
        )
        assert agent.get_timeout_for_agent('tests', default=120) == 120


class TestMetricsTracking:
    """Test metrics collection and reporting."""

    def test_metrics_initialized(self, tmp_path: Path, agent_module) -> None:
        """Verify metrics dict is initialized."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        assert 'files_processed' in agent.metrics
        assert 'files_modified' in agent.metrics
        assert 'agents_applied' in agent.metrics
        assert 'start_time' in agent.metrics

    def test_metrics_counters_start_at_zero(self, tmp_path: Path, agent_module) -> None:
        """Verify metrics counters initialized to zero."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        assert agent.metrics['files_processed'] == 0
        assert agent.metrics['files_modified'] == 0
        assert agent.metrics['agents_applied'] == {}

    def test_print_metrics_summary_sets_end_time(self, tmp_path: Path, agent_module, capsys) -> None:
        """Verify print_metrics_summary sets end_time."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.print_metrics_summary()
        assert agent.metrics['end_time'] is not None

# ============================================================================
# PHASE 4B: ADVANCED FEATURES (SNAPSHOTS, CASCADING IGNORES, ROLLBACK)
# ============================================================================


class TestFileSnapshots:
    """Test file snapshot creation and restoration."""

    def test_create_file_snapshot_returns_snapshot_id(self, tmp_path: Path, agent_module) -> None:
        """Verify snapshot creation returns a snapshot ID."""
        (tmp_path / ".git").mkdir()
        file_path: Path = tmp_path / "test.py"
        file_path.write_text("original content", encoding="utf-8")

        agent = agent_module.Agent(repo_root=str(tmp_path))
        snapshot_id = agent.create_file_snapshot(file_path)

        assert snapshot_id is not None
        assert isinstance(snapshot_id, str)

    def test_create_file_snapshot_creates_snapshot_directory(self, tmp_path: Path, agent_module) -> None:
        """Verify .agent_snapshots directory is created."""
        (tmp_path / ".git").mkdir()
        file_path: Path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")

        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path  # Override to use temp path
        snapshot_dir: Path = tmp_path / ".agent_snapshots"

        agent.create_file_snapshot(file_path)
        assert snapshot_dir.exists()

    def test_restore_from_snapshot_returns_false_for_invalid_snapshot(
            self, tmp_path: Path, agent_module) -> str:
        """Verify False returned for invalid snapshot IDs."""
        (tmp_path / ".git").mkdir()
        file_path: Path = tmp_path / "test.py"
        file_path.write_text("content", encoding="utf-8")

        agent = agent_module.Agent(repo_root=str(tmp_path))
        result = agent.restore_from_snapshot(file_path, "invalid_snapshot_id")

        assert result is False


class TestCascadingCodeignore:
    """Test cascading .codeignore pattern loading."""

    def test_load_cascading_codeignore_loads_root_patterns(self, tmp_path: Path, agent_module) -> None:
        """Verify root .codeignore patterns are loaded."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n__pycache__/\n", encoding="utf-8")

        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore()

        assert "*.log" in patterns
        assert "__pycache__/" in patterns

    def test_load_cascading_codeignore_loads_subdirectory_patterns(
            self, tmp_path: Path, agent_module) -> str:
        """Verify patterns from subdirectory .codeignore are loaded."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".codeignore").write_text("*.log\n", encoding="utf-8")
        src_dir: Path = tmp_path / "src"
        src_dir.mkdir()
        (src_dir / ".codeignore").write_text("*.tmp\n", encoding="utf-8")

        agent = agent_module.Agent(repo_root=str(tmp_path))
        patterns = agent.load_cascading_codeignore(src_dir)

        # Should include patterns from both root and subdirectory
        assert "*.log" in patterns
        assert "*.tmp" in patterns

# ============================================================================
# PHASE 4C: PARALLEL EXECUTION (ASYNC, MULTIPROCESSING, WEBHOOKS, CALLBACKS)
# ============================================================================

class TestAsyncFileProcessing:
    """Test async file processing."""

    def test_enable_async_flag(self, tmp_path: Path, agent_module) -> None:
        """Verify enable_async flag can be set."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path), enable_async=True)
        assert agent.enable_async is True


class TestMultiprocessingExecution:
    """Test multiprocessing file processing."""

    def test_process_files_multiprocessing_exists(self, tmp_path: Path, agent_module) -> None:
        """Verify process_files_multiprocessing method exists."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert hasattr(agent, 'process_files_multiprocessing')
        assert callable(agent.process_files_multiprocessing)

    def test_multiprocessing_flag(self, tmp_path: Path, agent_module) -> None:
        """Verify multiprocessing flag can be set."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path), enable_multiprocessing=True)
        assert agent.enable_multiprocessing is True


class TestWebhookSupport:
    """Test webhook functionality."""

    def test_register_webhook(self, tmp_path: Path, agent_module) -> None:
        """Verify webhook registration works."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        agent.register_webhook("https://example.com / webhook")
        assert "https://example.com / webhook" in agent.webhooks

    def test_send_webhook_notification_exists(self, tmp_path: Path, agent_module) -> None:
        """Verify send_webhook_notification method exists."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert hasattr(agent, 'send_webhook_notification')


class TestCallbackSupport:
    """Test callback functionality."""

    def test_register_callback(self, tmp_path: Path, agent_module) -> None:
        """Verify callback registration works."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))

        def my_callback(event) -> bool:
            pass

        agent.register_callback(my_callback)
        assert len(agent.callbacks) > 0

    def test_execute_callbacks_exists(self, tmp_path: Path, agent_module) -> None:
        """Verify execute_callbacks method exists."""
        (tmp_path / ".git").mkdir()
        agent = agent_module.Agent(repo_root=str(tmp_path))
        assert hasattr(agent, 'execute_callbacks')

# ============================================================================
# PHASE 5: REPORTING & MONITORING
# ============================================================================


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_circuit_breaker_initialization(self, agent_module) -> None:
        """Test circuit breaker initialization with defaults."""
        cb = agent_module.CircuitBreaker("test_backend")

        assert cb.name == "test_backend"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_circuit_breaker_custom_parameters(self, agent_module) -> None:
        """Test circuit breaker with custom parameters."""
        cb = agent_module.CircuitBreaker(
            "service",
            failure_threshold=3,
            recovery_timeout=30,
            backoff_multiplier=1.5
        )

        assert cb.failure_threshold == 3
        assert cb.recovery_timeout == 30
        assert cb.backoff_multiplier == 1.5

    def test_circuit_breaker_success_call(self, agent_module) -> None:
        """Test successful call through circuit breaker."""
        cb = agent_module.CircuitBreaker("test")

        def successful_func() -> str:
            return "success"

        result = cb.call(successful_func)

        assert result == "success"
        assert cb.state == "CLOSED"
        assert cb.failure_count == 0

    def test_circuit_breaker_failure_call(self, agent_module) -> None:
        """Test failed call through circuit breaker."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=3)

        def failing_func() -> str:
            raise Exception("Service down")

        with pytest.raises(Exception):
            cb.call(failing_func)

        assert cb.failure_count == 1
        assert cb.state == "CLOSED"

    def test_circuit_breaker_opens_after_threshold(self, agent_module) -> None:
        """Test circuit opens after failure threshold exceeded."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=2)

        def failing_func() -> str:
            raise Exception("Service down")

        # First failure
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "CLOSED"

        # Second failure opens circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"

    def test_circuit_breaker_fast_fail_when_open(self, agent_module) -> None:
        """Test circuit fails immediately when open."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=1)

        def failing_func() -> str:
            raise Exception("Service down")

        # Open the circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"

        # Next call should fail immediately without calling function
        call_count = 0

        def count_calls() -> bool:
            nonlocal call_count
            call_count += 1
            raise Exception("Should not be called")

        with pytest.raises(Exception, match="Circuit breaker.*OPEN"):
            cb.call(count_calls)

        assert call_count == 0  # Function never called

    def test_circuit_breaker_recovery(self, agent_module) -> None:
        """Test circuit breaker recovery from OPEN to CLOSED."""
        cb = agent_module.CircuitBreaker("test", failure_threshold=1, recovery_timeout=1)

        def failing_func() -> str:
            raise Exception("Service down")

        def succeeding_func() -> bool:
            return "ok"

        # Open the circuit
        with pytest.raises(Exception):
            cb.call(failing_func)
        assert cb.state == "OPEN"

        # Wait for recovery timeout
        time.sleep(1.5)

        # Should enter HALF_OPEN state
        result = cb.call(succeeding_func)
        assert result == "ok"
        assert cb.state == "HALF_OPEN"

        # successes needed = 3, so keep calling
        result = cb.call(succeeding_func)
        assert cb.state == "HALF_OPEN"


class TestReportGeneration:
    """Tests for improvement report generation."""

    def test_generate_improvement_report(self, tmp_path: Path, agent_module) -> None:
        """Test basic improvement report generation."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 10,
            'files_modified': 5,
            'agents_applied': {'coder': 4, 'tests': 3},
            'start_time': 0.0,
            'end_time': 10.0,
        }

        report = agent.generate_improvement_report()

        assert report['summary']['files_processed'] == 10
        assert report['summary']['files_modified'] == 5
        assert 'coder' in report['agents']
        assert report['summary']['modification_rate'] == 50.0

    def test_generate_improvement_report_includes_mode_info(self, tmp_path: Path, agent_module) -> None:
        """Test report includes execution mode information."""
        agent = agent_module.Agent(repo_root=str(tmp_path), dry_run=True, enable_async=True)
        agent.metrics = {
            'files_processed': 5,
            'files_modified': 2,
            'agents_applied': {},
            'start_time': 0.0,
            'end_time': 5.0,
        }

        report = agent.generate_improvement_report()

        assert report['mode']['dry_run'] is True
        assert report['mode']['async_enabled'] is True


class TestCostAnalysis:
    """Tests for cost analysis."""

    def test_cost_analysis_basic(self, tmp_path: Path, agent_module) -> None:
        """Test basic cost analysis."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 10,
            'agents_applied': {'coder': 8, 'tests': 7},
            'start_time': 0.0,
            'end_time': 10.0,
        }

        analysis = agent.cost_analysis(backend='github-models', cost_per_request=0.0001)

        assert analysis['backend'] == 'github-models'
        assert analysis['files_processed'] == 10
        assert analysis['total_agent_runs'] == 15

    def test_cost_analysis_different_backend(self, tmp_path: Path, agent_module) -> None:
        """Test cost analysis with different backend pricing."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.metrics = {
            'files_processed': 5,
            'agents_applied': {'coder': 3},
            'start_time': 0.0,
            'end_time': 5.0,
        }

        analysis = agent.cost_analysis(backend='openai', cost_per_request=0.001)

        assert analysis['backend'] == 'openai'
        assert analysis['cost_per_request'] == 0.001


class TestSnapshotCleanup:
    """Tests for snapshot cleanup functionality."""

    def test_cleanup_old_snapshots_no_directory(self, tmp_path: Path, agent_module) -> None:
        """Test cleanup handles missing snapshot directory gracefully."""
        agent = agent_module.Agent(repo_root=str(tmp_path))

        # No snapshot directory exists
        cleaned = agent.cleanup_old_snapshots()

        assert cleaned == 0

    def test_cleanup_old_snapshots_empty_directory(self, tmp_path: Path, agent_module) -> None:
        """Test cleanup with empty snapshot directory."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path

        snapshot_dir: Path = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()

        cleaned = agent.cleanup_old_snapshots()

        assert cleaned == 0

    def test_cleanup_old_snapshots_removes_old_files(self, tmp_path: Path, agent_module) -> None:
        """Test cleanup removes snapshots older than threshold."""
        agent = agent_module.Agent(repo_root=str(tmp_path))
        agent.repo_root = tmp_path

        snapshot_dir: Path = tmp_path / '.agent_snapshots'
        snapshot_dir.mkdir()

        # Create old snapshot (11 days old)
        old_snapshot: Path = snapshot_dir / '1000000_abc123_main.py'
        old_snapshot.write_text('old content')
        old_mtime: float = time.time() - (11 * 24 * 60 * 60)
        os.utime(old_snapshot, (old_mtime, old_mtime))

        # Create recent snapshot (2 days old)
        recent_snapshot: Path = snapshot_dir / '2000000_def456_main.py'
        recent_snapshot.write_text('recent content')

        cleaned = agent.cleanup_old_snapshots(max_age_days=7)

        assert cleaned == 1
        assert not old_snapshot.exists()
        assert recent_snapshot.exists()

# ============================================================================
# INTEGRATION TESTS
# ============================================================================
