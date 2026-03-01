# SystemManagers

**File**: `src\core\base\managers\SystemManagers.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 28 imports  
**Lines**: 348  
**Complexity**: 33 (complex)

## Overview

Python module containing implementation for SystemManagers.

## Classes (6)

### `FilePriorityManager`

Manager for file priority and request ordering.

**Methods** (6):
- `__init__(self, config)`
- `set_pattern_priority(self, pattern, priority)`
- `set_extension_priority(self, extension, priority)`
- `get_priority(self, path)`
- `sort_by_priority(self, paths)`
- `filter_by_priority(self, paths, min_priority)`

### `ResponseCache`

Caches responses based on prompts. 
Supports Prompt Caching (Phase 128) by identifying prefix reusable contexts.

**Methods** (5):
- `__post_init__(self)`
- `_get_cache_key(self, prompt)`
- `set(self, prompt, response)`
- `get(self, prompt)`
- `invalidate(self, prompt)`

### `StatePersistence`

Persists agent state to disk.

**Methods** (2):
- `save(self, state)`
- `load(self, default)`

### `EventManager`

Manages agent events.

**Methods** (2):
- `on(self, event, handler)`
- `emit(self, event, data)`

### `HealthChecker`

Performs health checks on agent components.

**Methods** (10):
- `__init__(self, repo_root, recorder)`
- `add_check(self, name, check_func)`
- `record_request(self, success, latency_ms)`
- `get_metrics(self)`
- `check(self)`
- `check_agent_script(self, agent_name)`
- `check_git(self)`
- `check_python(self)`
- `run_all_checks(self)`
- `is_healthy(self)`

### `ProfileManager`

Manages configuration profiles and execution profiles.

**Methods** (8):
- `__init__(self)`
- `_register_defaults(self)`
- `add_profile(self, profile)`
- `activate(self, name)`
- `set_active(self, name)`
- `get_active_config(self)`
- `active(self)`
- `get_setting(self, key, default)`

## Dependencies

**Imports** (28):
- `__future__.annotations`
- `ast`
- `collections.abc.Callable`
- `dataclasses.dataclass`
- `dataclasses.field`
- `fnmatch`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `src.core.base.models.AgentEvent`
- `src.core.base.models.AgentHealthCheck`
- `src.core.base.models.ConfigProfile`
- `src.core.base.models.ExecutionProfile`
- `src.core.base.models.FilePriority`
- ... and 13 more

---
*Auto-generated documentation*
