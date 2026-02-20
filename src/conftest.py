#!/usr/bin/env python3
"""Pytest configuration for PyAgent tests.

Lightweight fixtures and import hook helpers used by the test suite.
"""
from __future__ import annotations

import importlib.util
import re
import tempfile
import types
from pathlib import Path

import pytest

# Repository root (two levels up from src/)
_repo_root = Path(__file__).resolve().parents[1]
_orig_spec_from_file_location = importlib.util.spec_from_file_location


def _spec_from_file_location(name, location, *args, **kwargs):
    """Import hook that rewrites Windows absolute paths pointing into the repo."""
    try:
        loc = str(location)
        if re.match(r'^[A-Za-z]:[\\/]', loc):
            m = re.search(r'^[A-Za-z]:[\\/](.*)', loc)
            if m:
                rest = m.group(1).replace('\\', '/').replace('\\\\', '/')
                if rest.startswith(('src/', 'tests/', 'data/', 'temp/', 'agent_workspace/')):
                    newpath = _repo_root.joinpath(rest)
                    location = str(newpath)
    except Exception:
        pass
    return _orig_spec_from_file_location(name, location, *args, **kwargs)


importlib.util.spec_from_file_location = _spec_from_file_location


def pytest_ignore_collect(collection_path, config):
    """Skip auto-generated or external candidate tests that shouldn't run here."""
    try:
        if hasattr(collection_path, "strpath"):
            p = collection_path.strpath
        else:
            p = str(collection_path)
        if 'tests/unit/test_auto_' in p:
            return True
        if p.endswith('test_external_candidates.py') or p.endswith('test_external_candidates_more.py'):
            return True
        if 'external_candidates' in p and 'tests' in p:
            return True
    except Exception:
        pass
    return False


@pytest.fixture
def agent_module():
    """Provide lightweight Agent-related classes for tests."""
    try:
        from .core.base.lifecycle.base_agent import BaseAgent
    except Exception:
        from src.core.base.lifecycle.base_agent import BaseAgent
    try:
        from .core.base.logic.circuit_breaker import CircuitBreaker
    except Exception:
        from src.core.base.logic.circuit_breaker import CircuitBreaker
    try:
        from .core.base.logic.agent_plugin_base import AgentPluginBase
    except Exception:
        from src.core.base.logic.agent_plugin_base import AgentPluginBase
    try:
        from .core.base.common.models.core_enums import HealthStatus
    except Exception:
        from src.core.base.common.models.core_enums import HealthStatus

    mod = types.SimpleNamespace()
    mod.Agent = BaseAgent
    mod.CircuitBreaker = CircuitBreaker
    mod.AgentPluginBase = AgentPluginBase
    mod.HealthStatus = HealthStatus
    return mod


@pytest.fixture
def agent_backend_module():
    """Provide backend infrastructure classes for tests."""
    mod = types.SimpleNamespace()
    try:
        from .infrastructure.compute.backend.request_queue import RequestQueue
    except Exception:
        from src.infrastructure.compute.backend.request_queue import RequestQueue
    try:
        from .infrastructure.compute.backend.request_batcher import RequestBatcher
    except Exception:
        from src.infrastructure.compute.backend.request_batcher import RequestBatcher
    try:
        from .infrastructure.compute.backend.request_priority import RequestPriority
    except Exception:
        from src.infrastructure.compute.backend.request_priority import RequestPriority
    try:
        from .infrastructure.compute.backend.system_health_monitor import SystemHealthMonitor
    except Exception:
        from src.infrastructure.compute.backend.system_health_monitor import SystemHealthMonitor
    try:
        from .infrastructure.compute.backend.load_balancer import LoadBalancer
    except Exception:
        from src.infrastructure.compute.backend.load_balancer import LoadBalancer
    try:
        from .infrastructure.compute.backend.request_tracer import RequestTracer
    except Exception:
        from src.infrastructure.compute.backend.request_tracer import RequestTracer
    try:
        from .infrastructure.compute.backend.audit_logger import AuditLogger
    except Exception:
        from src.infrastructure.compute.backend.audit_logger import AuditLogger

    mod.RequestQueue = RequestQueue
    mod.RequestBatcher = RequestBatcher
    mod.RequestPriority = RequestPriority
    mod.SystemHealthMonitor = SystemHealthMonitor
    mod.LoadBalancer = LoadBalancer
    mod.RequestTracer = RequestTracer
    mod.AuditLogger = AuditLogger
    return mod


@pytest.fixture
def base_agent_module():
    """Provide batch managers used by some tests."""
    mod = types.SimpleNamespace()
    try:
        from .core.base.logic.managers.batch_managers import BatchRequest, RequestBatcher
    except Exception:
        from src.core.base.logic.managers.batch_managers import BatchRequest, RequestBatcher
    mod.BatchRequest = BatchRequest
    mod.RequestBatcher = RequestBatcher
    return mod


@pytest.fixture
def agent_sandbox():
    """Create a temporary repo-like sandbox for tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        src_dir = temp_path / "src"
        data_dir = temp_path / "data"
        src_dir.mkdir()
        data_dir.mkdir()
        (src_dir / "__init__.py").touch()
        yield temp_path


@pytest.fixture
def transactional_test_env(agent_sandbox):
    """Provide a transactional wrapper over the sandbox using StateTransaction."""
    try:
        from .core.base.state.agent_state_manager import StateTransaction
    except Exception:
        from src.core.base.state.agent_state_manager import StateTransaction

    target_files = list(agent_sandbox.glob("**/*.py"))
    with StateTransaction(target_files) as txn:
        yield txn
