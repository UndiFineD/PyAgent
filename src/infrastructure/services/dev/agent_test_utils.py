    # No changes needed; docstrings and code are already on separate lines.
#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Import test utilities from src."""


from __future__ import annotations

try:
    from pathlib import Path
except ImportError:
    from pathlib import Path

try:
    from typing import Union
except ImportError:
    from typing import Union

try:
    from .test_utils import FileSystemIsolator, MockAIBackend, ModuleLoader, SnapshotManager
except ImportError:
    from src.infrastructure.services.dev.test_utils import FileSystemIsolator, MockAIBackend, ModuleLoader, SnapshotManager
    MockResponse,
    TestDataFactory,
    TestEnvironment,
    TestSnapshot,
    PerformanceTracker,
    TestStatus,
    TestResult,
)

# Shared loader for constants
_loader = ModuleLoader()
AGENT_DIR = _loader.agent_dir

# Re-expose methods as expected by legacy tests
load_module_from_path = _loader.load_module_from_path


def agent_dir_on_path():
    """Context manager to ensure agent directory is on sys.path."""
    return _loader.agent_dir_on_path()


def agent_sys_path():
    """Context manager for adding agent directory to sys.path temporarily."""
    return _loader.agent_sys_path()


# Add the load_agent_module helper which is often used in conftest.py


def load_agent_module(module_path: Union[str, Path]):
    """Dynamically load an agent module (which may have hyphens in name)."""
    if isinstance(module_path, str):
        module_path = Path(module_path)

    # If path is relative, try to find it in AGENT_DIR
    if not module_path.is_absolute():
        potential_path = AGENT_DIR / module_path
        if potential_path.exists():
            module_path = potential_path

    name = module_path.stem.replace("-", "_")
    return _loader.load_module_from_path(name, module_path)


__all__ = [
    "AGENT_DIR",
    "agent_sys_path",
    "load_module_from_path",
    "agent_dir_on_path",
    "load_agent_module",
    "TestStatus",
    "TestResult",
    "MockResponse",
    "TestDataFactory",
    "TestEnvironment",
    "TestSnapshot",
    "MockAIBackend",
    "FileSystemIsolator",
    "PerformanceTracker",
    "SnapshotManager",
]
