"""Import test utilities from src."""
from __future__ import annotations
import sys
from pathlib import Path
from typing import Union
from src.infrastructure.dev.test_utils import (
    FileSystemIsolator,
    LogCapturer,
    MockAIBackend,
    ModuleLoader,
    SnapshotManager,
    MockResponse,
    TestDataFactory,
    TestEnvironment,
    TestSnapshot,
    PerformanceTracker,
    TestStatus,
    TestResult
)

# Shared loader for constants
_loader = ModuleLoader()
AGENT_DIR = _loader.agent_dir

# Re-expose methods as expected by legacy tests
load_module_from_path = _loader.load_module_from_path

def agent_dir_on_path():
    return _loader.agent_dir_on_path()

def agent_sys_path():
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
