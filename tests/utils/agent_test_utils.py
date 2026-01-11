"""Import test utilities from src."""
import sys
from pathlib import Path
from typing import Union

# Add src to path so tests can import from there
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Use importlib to avoid shadowing if possible, or just rely on sys.path order
# Actually, the simplest fix is to NOT name this file agent_test_utils.py if it's in tests/
# But it's already there. Let's try to import directly from the src file.
import importlib.util

def _load_src_utils():
    util_path = src_path / "core" / "utils" / "benchmarking.py"
    spec = importlib.util.spec_from_file_location("agent_test_utils_src", str(util_path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    raise ImportError("Could not load src/agent_test_utils.py")

_src_utils = _load_src_utils()
AGENT_DIR = _src_utils.AGENT_DIR
agent_sys_path = _src_utils.agent_sys_path
load_module_from_path = _src_utils.load_module_from_path
agent_dir_on_path = getattr(_src_utils, 'agent_dir_on_path', None)

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
    spec = importlib.util.spec_from_file_location(name, str(module_path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"Could not load module from {module_path}")

TestStatus = getattr(_src_utils, 'TestStatus', None)
TestResult = getattr(_src_utils, 'TestResult', None)
MockResponse = getattr(_src_utils, 'MockResponse', None)
TestDataFactory = getattr(_src_utils, 'TestDataFactory', None)
TestEnvironment = getattr(_src_utils, 'TestEnvironment', None)
TestSnapshot = getattr(_src_utils, 'TestSnapshot', None)
MockAIBackend = getattr(_src_utils, 'MockAIBackend', None)
FileSystemIsolator = getattr(_src_utils, 'FileSystemIsolator', None)
PerformanceTracker = getattr(_src_utils, 'PerformanceTracker', None)
SnapshotManager = getattr(_src_utils, 'SnapshotManager', None)

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
