# EnhancedLogger

**File**: `src\observability\logging\EnhancedLogger.py`  
**Type**: Python Module  
**Summary**: 3 classes, 14 functions, 10 imports  
**Lines**: 381  
**Complexity**: 25 (complex)

## Overview

EnhancedLogger - Extended logging with deduplication and scope control.

Inspired by vLLM's logger pattern with debug_once, info_once, warning_once
methods and scope-aware logging for distributed systems.

Phase 24: Advanced Observability & Parsing

## Classes (3)

### `LogScopeEnum`

**Inherits from**: Enum

Enum for log scope types.

### `EnhancedLoggerAdapter`

**Inherits from**: LoggerAdapter

Logger adapter providing enhanced logging methods.

Provides a clean API without patching the underlying logger.

**Methods** (7):
- `__init__(self, logger, extra)`
- `debug_once(self, msg)`
- `info_once(self, msg)`
- `warning_once(self, msg)`
- `error_once(self, msg)`
- `reset_once_cache(self)`
- `get_logged_count(self)`

### `EnhancedLogger`

**Inherits from**: Logger

Type hint class for enhanced logger.

Not for direct instantiation - use init_logger() or patch_logger().

**Methods** (4):
- `debug_once(self, msg)`
- `info_once(self, msg)`
- `warning_once(self, msg)`
- `error_once(self, msg)`

## Functions (14)

### `_dedupe_debug(logger, msg)`

Log debug message only once.

### `_dedupe_info(logger, msg)`

Log info message only once.

### `_dedupe_warning(logger, msg)`

Log warning message only once.

### `_dedupe_error(logger, msg)`

Log error message only once.

### `_should_log_with_scope(scope)`

Determine whether to log based on scope.

Args:
    scope: Logging scope
        - "process": Always log (default)
        - "global": Only log on global first rank
        - "local": Only log on local first rank
        
Returns:
    True if logging should proceed

### `debug_once(self, msg)`

Log debug message only once per unique (msg, args) combination.

Args:
    msg: Log message (can include % formatting)
    *args: Arguments for % formatting (must be hashable)
    scope: Logging scope for distributed systems

### `info_once(self, msg)`

Log info message only once per unique (msg, args) combination.

Args:
    msg: Log message (can include % formatting)
    *args: Arguments for % formatting (must be hashable)
    scope: Logging scope for distributed systems

### `warning_once(self, msg)`

Log warning message only once per unique (msg, args) combination.

Args:
    msg: Log message (can include % formatting)
    *args: Arguments for % formatting (must be hashable)
    scope: Logging scope for distributed systems

### `error_once(self, msg)`

Log error message only once per unique (msg, args) combination.

Args:
    msg: Log message (can include % formatting)
    *args: Arguments for % formatting (must be hashable)
    scope: Logging scope for distributed systems

### `patch_logger(logger)`

Patch a logger instance with _once methods.

Adds debug_once, info_once, warning_once, error_once methods
to the logger instance.

Args:
    logger: Logger to patch
    
Returns:
    The patched logger (same instance)

## Dependencies

**Imports** (10):
- `__future__.annotations`
- `collections.abc.Hashable`
- `enum.Enum`
- `functools.lru_cache`
- `logging`
- `src.infrastructure.distributed.is_global_first_rank`
- `src.infrastructure.distributed.is_local_first_rank`
- `types.MethodType`
- `typing.Any`
- `typing.Literal`

---
*Auto-generated documentation*
