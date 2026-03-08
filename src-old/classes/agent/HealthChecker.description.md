# HealthChecker

**File**: `src\classes\agent\HealthChecker.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 40 imports  
**Lines**: 210  
**Complexity**: 8 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `HealthChecker`

Performs health checks on agent components.

Verifies that all required components are available and functional
before starting agent execution.

Attributes:
    repo_root: Repository root directory.
    results: Dict of health check results.

**Methods** (8):
- `__init__(self, repo_root, recorder)`
- `_record(self, action, result)`
- `check_agent_script(self, agent_name)`
- `check_git(self)`
- `check_python(self)`
- `run_all_checks(self)`
- `is_healthy(self)`
- `print_report(self)`

## Dependencies

**Imports** (40):
- `AgentHealthCheck.AgentHealthCheck`
- `HealthStatus.HealthStatus`
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `argparse`
- `ast`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `contextlib.contextmanager`
- `dataclasses.dataclass`
- `dataclasses.field`
- `difflib`
- `enum.Enum`
- `enum.auto`
- ... and 25 more

---
*Auto-generated documentation*
