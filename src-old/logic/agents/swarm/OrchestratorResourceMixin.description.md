# OrchestratorResourceMixin

**File**: `src\logic\agents\swarm\OrchestratorResourceMixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 52  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for OrchestratorResourceMixin.

## Classes (1)

### `OrchestratorResourceMixin`

Resource management methods (rate limiting, locking, incremental processing) for OrchestratorAgent.

**Methods** (6):
- `enable_rate_limiting(self, config)`
- `get_rate_limit_stats(self)`
- `enable_file_locking(self, lock_timeout)`
- `enable_incremental_processing(self)`
- `get_changed_files(self, files)`
- `reset_incremental_state(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `pathlib.Path`
- `src.core.base.IncrementalProcessor.IncrementalProcessor`
- `src.core.base.models.RateLimitConfig`
- `src.core.base.utils.FileLockManager.FileLockManager`
- `src.core.base.utils.RateLimiter.RateLimiter`
- `typing.Any`

---
*Auto-generated documentation*
