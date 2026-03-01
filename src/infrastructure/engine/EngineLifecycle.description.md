# EngineLifecycle

**File**: `src\infrastructure\engine\EngineLifecycle.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 20 imports  
**Lines**: 547  
**Complexity**: 28 (complex)

## Overview

Engine lifecycle management for inference engines.

This module implements engine state management and lifecycle control,
inspired by vLLM's v1/engine/core.py architecture.

Key Components:
    - EngineState: Enum for engine states (INITIALIZING, READY, RUNNING, etc.)
    - EngineConfig: Configuration for engine lifecycle
    - EngineLifecycleManager: Manages engine state transitions

Example:
    >>> from src.infrastructure.engine import EngineLifecycleManager, EngineConfig
    >>> 
    >>> config = EngineConfig(max_requests=100)
    >>> manager = EngineLifecycleManager(config)
    >>> 
    >>> manager.start()  # INITIALIZING -> READY
    >>> manager.step()   # READY -> RUNNING -> READY
    >>> manager.shutdown()  # -> SHUTTING_DOWN -> DEAD

## Classes (3)

### `EngineState`

**Inherits from**: Enum

State of the inference engine.

State machine:
    INITIALIZING -> READY -> RUNNING <-> SLEEPING
                                |
                          SHUTTING_DOWN -> DEAD

**Methods** (4):
- `__str__(self)`
- `is_active(self)`
- `can_accept_requests(self)`
- `is_terminal(self)`

### `EngineConfig`

Configuration for the engine lifecycle manager.

Attributes:
    max_requests: Maximum concurrent requests
    max_tokens_per_step: Maximum tokens to process per step
    step_timeout: Timeout for each step in seconds
    shutdown_timeout: Timeout for graceful shutdown
    drain_requests_on_shutdown: Whether to complete pending requests
    enable_sleep_mode: Whether sleep mode is enabled
    sleep_level: Default sleep level (1-3)
    health_check_interval: Interval for health checks

### `EngineLifecycleManager`

Manages the lifecycle of an inference engine.

This class handles state transitions, request management, and
graceful shutdown following vLLM's EngineCore patterns.

Attributes:
    config: Engine configuration
    state: Current engine state
    request_queue: Queue for managing requests
    tracker: Request lifecycle tracker

**Methods** (24):
- `__init__(self, config, request_queue)`
- `state(self)`
- `is_sleeping(self)`
- `is_ready(self)`
- `is_running(self)`
- `is_shutting_down(self)`
- `is_dead(self)`
- `can_accept_requests(self)`
- `_transition_to(self, new_state)`
- `start(self)`
- ... and 14 more methods

## Dependencies

**Imports** (20):
- `RequestLifecycle.FinishReason`
- `RequestLifecycle.Request`
- `RequestLifecycle.RequestQueue`
- `RequestLifecycle.RequestStatus`
- `RequestLifecycle.RequestTracker`
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum`
- `logging`
- `signal`
- `threading`
- `time`
- `typing.Any`
- ... and 5 more

---
*Auto-generated documentation*
