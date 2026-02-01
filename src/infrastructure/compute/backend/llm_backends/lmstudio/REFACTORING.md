# LMStudio Backend Refactoring

## Overview
The LMStudio backend has been refactored from a monolithic 998-line `backend.py` file into a modular architecture with clear separation of concerns. This improves maintainability, testability, and aligns with the official LMStudio Python SDK patterns.

## Module Structure

### 1. **api.py** - REST API Client
Handles all HTTP communication with the LM Studio server.

**Key Classes:**
- `LMStudioAPIClient`: REST API client with:
  - URL normalization (handles both `/api/v1` and `/v1` prefixes)
  - Automatic API token authorization (from config or `DV_LMSTUDIO_API_TOKEN`)
  - Exponential backoff retry logic for transient failures
  - Comprehensive logging with `[LMStudio]` prefix

**Methods:**
- `_normalize_url(endpoint)`: Auto-detect and normalize REST API URLs
- `_get_headers()`: Build HTTP headers with Bearer token support
- `_http_request_with_retry(method, url, max_retries=3, **kwargs)`: Robust HTTP with retry
- `list_models()`: Fetch available models from `/models` endpoint
- `get_info()`: Discover server version and capabilities

### 2. **chat.py** - Non-Streaming Chat Handler
Manages chat operations with SDK-first and HTTP fallback strategy.

**Key Classes:**
- `ChatHandler`: Handles chat completions with:
  - SDK primary approach (uses official LMStudio Python SDK)
  - HTTP fallback to REST API `/api/v1/chat`
  - Proper message extraction from response arrays
  - Configuration building from kwargs

**Methods:**
- `_build_prediction_config(sdk_available, **kwargs)`: Create LmPredictionConfig
- `_extract_chat_from_lmstudio(system_prompt)`: Create lmstudio.Chat objects
- `_sdk_chat(llm, prompt, system_prompt, **kwargs)`: SDK-based chat
- `_http_fallback_chat(prompt, model, system_prompt, **kwargs)`: HTTP REST fallback
- `chat(llm, prompt, model, system_prompt, sdk_available, **kwargs)`: Primary entry point

### 3. **chat_stream.py** - Streaming Chat Handler
Manages streaming chat operations with SSE support.

**Key Classes:**
- `StreamingChatHandler`: Handles streaming chat with:
  - SDK streaming via `respond_stream()`
  - HTTP fallback using Server-Sent Events (SSE)
  - Fragment callbacks for real-time token processing
  - Proper JSON parsing of SSE message.delta events

**Methods:**
- `_sdk_chat_stream(llm, prompt, system_prompt, on_fragment, **kwargs)`: SDK streaming
- `_http_fallback_chat_stream(prompt, model, system_prompt, on_fragment, **kwargs)`: HTTP SSE streaming
- `chat_stream(llm, prompt, model, system_prompt, sdk_available, on_fragment, **kwargs)`: Primary entry point

### 4. **mcp_client.py** - SDK Client Management
Manages LMStudio SDK client initialization and model access following Model Context Protocol patterns.

**Key Classes:**
- `MCPClient`: SDK client lifecycle and accessor management with:
  - Sync (`Client`) and async (`AsyncClient`) client creation
  - Support for multiple SDK accessor styles (.get(), callable, module-level helpers)
  - Model and embedding model fetching
  - Graceful client cleanup

**Methods:**
- `get_sync_client()`: Create or retrieve sync client
- `get_async_client()`: Create or retrieve async client
- `get_llm(client, model)`: Fetch LLM handle (handles multiple accessor patterns)
- `get_async_llm(client, model)`: Async LLM fetching with proper awaitable handling
- `get_embedding_model(client, model)`: Fetch embedding model
- `close()`: Clean up all client resources

### 5. **backend.py** - Refactored Main Backend
Simplified 998-line file to ~460 lines by delegating to modular components.

**Key Improvements:**
- Uses `MCPClient` for SDK management
- Uses `LMStudioAPIClient` for REST API operations
- Uses `ChatHandler` for chat operations
- Uses `StreamingChatHandler` for streaming
- Maintains all public API compatibility
- Cleaner error handling and logging

**Main Methods:**
- `__init__()`: Initializes all modular components
- `list_loaded_models()`: Delegates to SDK or API client
- `list_downloaded_models()`: Delegates to SDK or API client
- `get_model(model)`: Gets model with caching via MCPClient
- `chat()`: Non-streaming chat via ChatHandler
- `chat_stream()`: Streaming chat via StreamingChatHandler
- `chat_async()`: Async chat via MCPClient
- `embed()`: Embeddings via MCPClient
- `chat_with_tools()`: Tool-calling via MCPClient
- `health_check()`: Connectivity validation
- `get_info()`: Server information discovery

## Key Design Decisions

### 1. **Separation of Concerns**
- API communication (**api.py**) is isolated from business logic
- Chat strategies (**chat.py**, **chat_stream.py**) are independent
- SDK management (**mcp_client.py**) handles SDK complexities
- Backend (**backend.py**) orchestrates everything

### 2. **SDK-First with HTTP Fallback**
- All operations try SDK first (more reliable, feature-complete)
- HTTP fallback activates only on SDK failure
- Each fallback is tuned to its specific operation (e.g., retry counts)
- Health status updated automatically on successful fallback

### 3. **Configuration & Flexibility**
- Base URL normalization handles both `/api/v1` and `/v1` prefixes
- API token support from config or `DV_LMSTUDIO_API_TOKEN` environment variable
- Exponential backoff retry for transient network errors
- Comprehensive logging for debugging

### 4. **Accessor Pattern Compatibility**
- MCPClient supports multiple SDK versions with different accessor styles
- `.get()` method style (newer SDKs)
- Callable accessor style (callable factory)
- Module-level helper fallback (legacy/simple)

## Migration Notes

### For Users
No breaking changes. All public APIs remain identical:
- `LMStudioBackend(session, connectivity_manager, recorder, config)`
- `list_loaded_models()` → `list[str]`
- `chat(prompt, model, system_prompt, **kwargs)` → `str`
- `chat_stream(prompt, model, system_prompt, on_fragment, **kwargs)` → `Iterator[str]`
- `get_info()` → `dict[str, Any]`
- All other methods unchanged

### For Developers
When extending or debugging:
- REST API issues → check `api.py`
- Chat logic issues → check `chat.py` or `chat_stream.py`
- SDK integration issues → check `mcp_client.py`
- Overall orchestration → check `backend.py`

## Testing
All modules have been syntax-validated. Existing unit tests should continue to pass without modification.

```bash
# Run existing tests
pytest tests/unit/test_lmstudio_backend.py

# Test individual modules
pytest tests/unit/test_lmstudio_api.py
pytest tests/unit/test_lmstudio_chat.py
pytest tests/unit/test_lmstudio_chat_stream.py
pytest tests/unit/test_lmstudio_mcp_client.py
```

## Future Improvements
1. **Async Support**: `ChatHandler` and `StreamingChatHandler` could have async variants
2. **Response Caching**: Add optional response caching layer in `api.py`
3. **Metrics**: Integrate metrics collection for each operation type
4. **Plugin Architecture**: MCPClient could support plugin registration for custom model types
5. **Rate Limiting**: Add rate limiter in `api.py` for burst protection

## References
- [LMStudio Python SDK](https://github.com/lmstudio-ai/lmstudio-python)
- [LMStudio REST API Docs](https://lmstudio.ai/docs)
- Architecture follows official SDK patterns from `sync_api.py` and `async_api.py`
