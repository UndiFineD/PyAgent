# AsyncVllmEngine

**File**: `src\infrastructure\backend\vllm_advanced\AsyncVllmEngine.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 20 imports  
**Lines**: 503  
**Complexity**: 11 (moderate)

## Overview

Async vLLM Engine Integration.

Provides high-throughput async inference using vLLM's AsyncLLMEngine.
Inspired by vLLM's v1/engine/async_llm_engine.py patterns.

## Classes (4)

### `RequestState`

**Inherits from**: Enum

State of an async request.

### `AsyncEngineConfig`

Configuration for the async vLLM engine.

**Methods** (1):
- `to_engine_args(self)`

### `AsyncRequestHandle`

Handle for tracking an async request.

**Methods** (3):
- `is_finished(self)`
- `latency_ms(self)`
- `tokens_per_second(self)`

### `AsyncVllmEngine`

High-throughput async vLLM engine for PyAgent.

Provides:
- Concurrent request handling
- Request tracking and cancellation
- Automatic batching via vLLM scheduler
- Streaming support via async iterators

Example:
    engine = AsyncVllmEngine(AsyncEngineConfig(model="meta-llama/Llama-3-8B"))
    await engine.start()
    
    # Single request
    result = await engine.generate("What is AI?")
    
    # Concurrent requests
    handles = await engine.generate_batch(["Q1", "Q2", "Q3"])
    
    # Streaming
    async for token in engine.generate_stream("Tell me a story"):
        print(token, end="", flush=True)

**Methods** (7):
- `__init__(self, config)`
- `get_instance(cls, config)`
- `is_available(self)`
- `is_running(self)`
- `_generate_request_id(self)`
- `get_request(self, request_id)`
- `get_stats(self)`

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `logging`
- `time`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- ... and 5 more

---
*Auto-generated documentation*
