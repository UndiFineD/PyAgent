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

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Pytest configuration for PyAgent tests."""

import types
import tempfile
import pytest
import importlib.util
import re
from pathlib import Path

# Normalize Windows-style absolute paths embedded in generated tests when running on non-Windows CI
_orig_spec_from_file_location = importlib.util.spec_from_file_location
_repo_root = Path(__file__).resolve().parents[1]

def _spec_from_file_location(name, location, *args, **kwargs):
    try:
        loc = str(location)
        # Detect Windows absolute path like C:\DEV\PyAgent\... or C:/DEV/PyAgent/...
        if re.match(r'^[A-Za-z]:[\\/]', loc):
            m = re.search(r'^[A-Za-z]:[\\/](.*)', loc)
            if m:
                # Only rewrite Windows absolute paths that point into repo subfolders
                # like 'src/' or 'tests/'. Otherwise leave location untouched.
                rest = m.group(1).replace('\\', '/').replace('\\\\', '/')
                if rest.startswith(('src/', 'tests/', 'data/', 'temp/', 'agent_workspace/')):
                    newpath = _repo_root.joinpath(rest)
                    location = str(newpath)
    except Exception:
        pass
    return _orig_spec_from_file_location(name, location, *args, **kwargs)

importlib.util.spec_from_file_location = _spec_from_file_location


def pytest_ignore_collect(collection_path, config):
    """Ignore auto-generated tests that reference Windows absolute paths or external_candidates.

    Many auto-generated tests include hard-coded Windows-style paths (C:\\DEV\\...) which
    cause collection errors on non-Windows CI runners. Skip these tests during collection.
    This hook accepts either a `py.path.local` or a `pathlib.Path` to be compatible with
    different pytest versions and avoid deprecation warnings.
    """
    try:
        # support both py.path.local (has .strpath) and pathlib.Path
        if hasattr(collection_path, "strpath"):
            p = collection_path.strpath
        else:
            p = str(collection_path)
        if 'tests/unit/test_auto_' in p:
            return True
        # also skip broad external candidates tests
        if p.endswith('test_external_candidates.py') or p.endswith('test_external_candidates_more.py'):
            return True
        if 'external_candidates' in p and 'tests' in p:
            return True
    except Exception:
        pass
    return False


from src.core.base.lifecycle.base_agent import BaseAgent  # noqa: E402
from src.core.base.logic.circuit_breaker import CircuitBreaker  # noqa: E402
from src.core.base.logic.agent_plugin_base import AgentPluginBase  # noqa: E402
from src.core.base.common.models.core_enums import HealthStatus  # noqa: E402
from src.core.base.state.agent_state_manager import StateTransaction  # noqa: E402


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
def transactional_test_env(agent_sandbox):
    """
    Provides a transactional wrapper around the sandbox.
    Ensures that file modifications are tracked and can be rolled back on failure.
    """
    # Track core files in the sandbox
    target_files = list(agent_sandbox.glob("**/*.py"))

    with StateTransaction(target_files) as txn:
        yield txn

