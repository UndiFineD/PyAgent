# SystemManagers

**File**: `src\classes\base_agent\managers\SystemManagers.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 22 imports  
**Lines**: 155  
**Complexity**: 26 (complex)

## Overview

Python module containing implementation for SystemManagers.

## Classes (7)

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

### `PluginManager`

Manages agent plugins.

**Methods** (3):
- `register(self, plugin)`
- `activate_all(self)`
- `deactivate(self, name)`

### `HealthChecker`

Checks agent health status.

**Methods** (4):
- `add_check(self, name, check_func)`
- `check(self)`
- `record_request(self, success, latency_ms)`
- `get_metrics(self)`

### `ProfileManager`

Manages configuration profiles.

**Methods** (4):
- `active(self)`
- `add_profile(self, profile)`
- `set_active(self, name)`
- `get_setting(self, key, default)`

## Dependencies

**Imports** (22):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `fnmatch`
- `hashlib`
- `json`
- `logging`
- `models.AgentEvent`
- `models.ConfigProfile`
- `models.FilePriority`
- `models.FilePriorityConfig`
- `models._empty_agent_event_handlers`
- `models._empty_dict_str_any`
- `models._empty_dict_str_configprofile`
- `models._empty_dict_str_health_checks`
- ... and 7 more

---
*Auto-generated documentation*
