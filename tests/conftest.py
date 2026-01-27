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
<<<<<<< HEAD
=======

"""Pytest configuration for PyAgent tests."""
>>>>>>> 7691cd526 (chore: repository-wide stability and Pylint 10/10 compliance refactor)

<<<<<<< HEAD
<<<<<<< HEAD
"""Pytest configuration for PyAgent tests."""
import pytest
import tempfile
from pathlib import Path
from src.infrastructure.fleet.AgentRegistry import AgentRegistry
=======
import types
import tempfile
from pathlib import Path
=======
import types
import tempfile
from pathlib import Path
>>>>>>> 797ca81d4 (Fix Pylint errors: imports, whitespace, docstrings)
import pytest
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.logic.circuit_breaker import CircuitBreaker
from src.core.base.logic.agent_plugin_base import AgentPluginBase
from src.core.base.common.models.core_enums import HealthStatus


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
    # Lazy imports to avoid circular dependencies
    try:
        from src.infrastructure.compute.backend.request_queue import RequestQueue
        from src.infrastructure.compute.backend.request_batcher import RequestBatcher
        from src.infrastructure.compute.backend.request_priority import RequestPriority
        from src.infrastructure.compute.backend.system_health_monitor import SystemHealthMonitor
        from src.infrastructure.compute.backend.load_balancer import LoadBalancer
        from src.infrastructure.compute.backend.request_tracer import RequestTracer
        from src.infrastructure.compute.backend.audit_logger import AuditLogger

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
        from src.core.base.logic.managers.batch_managers import BatchRequest, RequestBatcher

        mod.BatchRequest = BatchRequest
        mod.RequestBatcher = RequestBatcher
    except ImportError:
        pass
    return mod

>>>>>>> d5f1917bc (Fix Pylint errors: imports, whitespace, docstrings)

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

<<<<<<< HEAD
<<<<<<< HEAD
@pytest.fixture
def agent_registry():
    """Provides a central AgentRegistry for test use."""
    workspace_root = Path(__file__).parent.parent
    return AgentRegistry.get_agent_map(workspace_root)


@pytest.fixture(autouse=True)
def isolation_cleanup():
    """
    Enforce isolation between tests (Phase 280).
    Resets global caches and static states to prevent cross-test contamination.
    """
    # Reset SubagentRunner command cache
    try:
        from src.infrastructure.compute.backend.subagent_runner import SubagentRunner

        # pylint: disable=protected-access
        SubagentRunner._command_cache.clear()
    except ImportError:
        pass

    yield

=======
>>>>>>> 6b596bef0 (Refactor: Massive test suite migration and reorganization. Legacy tests verified and moved to tests/unit/phases and tests/unit/features. Deleted tests-old.)
=======
>>>>>>> 558c5bd8f (Refactor: Massive test suite migration and reorganization. Legacy tests verified and moved to tests/unit/phases and tests/unit/features. Deleted tests-old.)
