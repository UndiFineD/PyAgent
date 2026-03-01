# AsyncMicrobatcher

**File**: `src\infrastructure\backend\AsyncMicrobatcher.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 14 imports  
**Lines**: 375  
**Complexity**: 14 (moderate)

## Overview

AsyncMicrobatcher - Async micro-batching for LLM operations.

Inspired by vLLM's AsyncMicrobatchTokenizer patterns for efficient batching
with configurable batch size and timeout.

Phase 17: vLLM Pattern Integration

## Classes (4)

### `BatchItem`

**Inherits from**: Unknown

A single item in a batch with its associated future.

### `BatchStats`

Statistics for batching performance.

**Methods** (3):
- `avg_batch_size(self)`
- `avg_wait_time_ms(self)`
- `to_dict(self)`

### `AsyncMicrobatcher`

**Inherits from**: Unknown

Async micro-batcher that collects items and processes them in batches.

This is useful for batching LLM requests, tokenization, or any operation
that benefits from batch processing.

Example:
    >>> async def process_batch(items: list[str]) -> list[int]:
    ...     return [len(s) for s in items]
    >>> 
    >>> batcher = AsyncMicrobatcher(
    ...     batch_fn=process_batch,
    ...     max_batch_size=32,
    ...     batch_wait_timeout_s=0.002,
    ... )
    >>> 
    >>> # Submit items (they'll be batched automatically)
    >>> result = await batcher.submit("hello")

**Methods** (3):
- `__init__(self, batch_fn, max_batch_size, batch_wait_timeout_s, name)`
- `stats(self)`
- `is_running(self)`

### `SyncMicrobatcher`

**Inherits from**: Unknown

Synchronous micro-batcher using a background thread.

For use in synchronous code that needs batching.

**Methods** (8):
- `__init__(self, batch_fn, max_batch_size, batch_wait_timeout_s, name)`
- `stats(self)`
- `start(self)`
- `stop(self)`
- `submit(self, item)`
- `_process_loop(self)`
- `_collect_batch(self)`
- `_process_batch(self, batch)`

## Dependencies

**Imports** (14):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Awaitable`
- `collections.abc.Callable`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `dataclasses.field`
- `queue`
- `threading`
- `time`
- `typing.Any`
- `typing.Generic`
- `typing.Optional`
- `typing.TypeVar`

---
*Auto-generated documentation*
