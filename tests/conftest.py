"""Pytest configuration for PyAgent tests."""

import pytest
import tempfile
import types
from pathlib import Path
from src.infrastructure.fleet.agent_registry import AgentRegistry
from src.core.base.base_agent import BaseAgent
from src.core.base.circuit_breaker import CircuitBreaker
from src.core.base.agent_plugin_base import AgentPluginBase
from src.core.base.models.core_enums import HealthStatus


@pytest.fixture
def agent_module():
    """Provides a mock module with Agent and CircuitBreaker classes."""
    mod = types.SimpleNamespace()
    mod.Agent = BaseAgent

    mod.CircuitBreaker = CircuitBreaker
    mod.AgentPluginBase = AgentPluginBase
    mod.HealthStatus = HealthStatus
    return mod


@pytest.fixture
def agent_backend_module():
    """Provides backend infrastructure classes."""
    mod = types.SimpleNamespace()
    # Lazy imports to avoid circular dependencies or import errors if modules are broken

    try:
        from src.infrastructure.backend.request_queue import RequestQueue
        from src.infrastructure.backend.request_batcher import RequestBatcher
        from src.infrastructure.backend.request_priority import RequestPriority
        from src.infrastructure.backend.system_health_monitor import SystemHealthMonitor

        from src.infrastructure.backend.load_balancer import LoadBalancer
        from src.infrastructure.backend.request_tracer import RequestTracer

        from src.infrastructure.backend.audit_logger import AuditLogger

        mod.RequestQueue = RequestQueue

        mod.RequestBatcher = RequestBatcher
        mod.RequestPriority = RequestPriority
        mod.SystemHealthMonitor = SystemHealthMonitor
        mod.LoadBalancer = LoadBalancer
        mod.RequestTracer = RequestTracer
        mod.AuditLogger = AuditLogger
    except ImportError:
        pass
    return mod


@pytest.fixture
def base_agent_module():
    """Provides core base agent classes including BatchManagers."""
    mod = types.SimpleNamespace()
    try:
        from src.core.base.managers.batch_managers import BatchRequest, RequestBatcher

        mod.BatchRequest = BatchRequest
        mod.RequestBatcher = RequestBatcher
    except ImportError:
        pass
    return mod


@pytest.fixture
def agent_sandbox():
    """Provides a clean, temporary src/ and data/ environment for agent tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        src_dir = temp_path / "src"
        data_dir = temp_path / "data"
        src_dir.mkdir()
        data_dir.mkdir()

        # Initialize basic structure
        (src_dir / "__init__.py").touch()

        yield temp_path


@pytest.fixture
def agent_registry():
    """Provides a central AgentRegistry for test use."""
    workspace_root = Path(__file__).parent.parent
    return AgentRegistry.get_agent_map(workspace_root)
