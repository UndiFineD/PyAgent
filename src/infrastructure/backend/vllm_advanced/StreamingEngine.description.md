# StreamingEngine

**File**: `src\infrastructure\backend\vllm_advanced\StreamingEngine.py`  
**Type**: Python Module  
**Summary**: 5 classes, 0 functions, 20 imports  
**Lines**: 510  
**Complexity**: 13 (moderate)

## Overview

Streaming vLLM Engine Integration.

Provides real-time token streaming for vLLM inference.
Supports both callback-based and iterator-based streaming.

## Classes (5)

### `StreamCallback`

**Inherits from**: Protocol

Protocol for stream callbacks.

**Methods** (1):
- `__call__(self, token, token_id, is_finished, finish_reason)`

### `StreamingConfig`

Configuration for streaming engine.

### `StreamToken`

A streamed token.

### `TokenStreamIterator`

Iterator for streaming tokens.

Can be used in both sync and async contexts.

Example (sync):
    for token in stream_iterator:
        print(token.text, end="", flush=True)

Example (async):
    async for token in stream_iterator:
        print(token.text, end="", flush=True)

**Methods** (4):
- `__init__(self, buffer_size)`
- `__iter__(self)`
- `tokens_per_second(self)`
- `get_full_text(self)`

### `StreamingVllmEngine`

Streaming vLLM engine for real-time token output.

Provides multiple streaming modes:
1. Callback-based: Register a callback for each token
2. Iterator-based: Use async for loop
3. Buffer-based: Collect tokens in batches

Example:
    engine = StreamingVllmEngine(StreamingConfig())
    
    # Callback mode
    def on_token(token, token_id, is_finished, finish_reason):
        print(token, end="", flush=True)
    
    engine.generate_with_callback("Tell me a story", on_token)
    
    # Iterator mode
    async for token in engine.generate_stream("Hello"):
        print(token.text, end="")

**Methods** (8):
- `__init__(self, config)`
- `get_instance(cls, config)`
- `is_available(self)`
- `_ensure_initialized(self)`
- `generate_with_callback(self, prompt, callback, temperature, max_tokens, system_prompt)`
- `generate_buffered(self, prompt, buffer_tokens, temperature, max_tokens, system_prompt)`
- `get_stats(self)`
- `shutdown(self)`

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `gc`
- `logging`
- `os`
- `time`
- `torch`
- `typing.Any`
- `typing.AsyncIterator`
- `typing.Callable`
- `typing.Iterator`
- `typing.List`
- `typing.Optional`
- ... and 5 more

---
*Auto-generated documentation*
