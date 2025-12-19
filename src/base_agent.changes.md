# Changelog

## [2025-12-18] - Documentation refresh

- Updated docs to match current `src/base_agent.py` behavior and CLI helper surface.
- Corrected module path references from `scripts/agent/...` to `src/...`.
- Refreshed SHA256 fingerprint in the description doc.

## [2025-12-16] - Session 8 Implementation

### Added Enums

- `AuthMethod` enum: NONE, API_KEY, BEARER_TOKEN, BASIC_AUTH, OAUTH2, CUSTOM
- `SerializationFormat` enum: JSON, YAML, MSGPACK, PICKLE, PROTOBUF
- `FilePriority` enum: CRITICAL, HIGH, NORMAL, LOW, BACKGROUND
- `InputType` enum: TEXT, IMAGE, DIAGRAM, CODE, AUDIO, VIDEO

### Added Dataclasses

- `AuthConfig`: Authentication configuration with method, api_key, token, username, password, oauth credentials, custom_headers
- `BatchRequest`: Request for batch processing with file_path, prompt, priority, callback
- `BatchResult`: Result of batch processing with success, content, error, processing_time
- `PromptVersion`: Versioned prompt for A/B testing with version_id, template_id, variant, weight, metrics
- `MultimodalInput`: Multimodal input with input_type, content, mime_type, metadata
- `ComposedAgent`: Agent composition config with agent_type, config, order, depends_on
- `SerializationConfig`: Serialization config with format, options, compression, encryption
- `FilePriorityConfig`: File priority config with path_patterns, extension_priorities, default_priority

### Added Helper Classes

- `RequestBatcher`: Batch processor for multiple files with priority ordering and parallel execution
- `AuthenticationManager`: Manager for authentication methods (API keys, bearer tokens, OAuth2, custom)
- `PromptVersionManager`: Manager for prompt versioning and A/B testing with metrics tracking
- `MultimodalProcessor`: Processor for multimodal inputs (text, images, diagrams, code)
- `AgentComposer`: Orchestrator for multi-agent workflows with dependency handling
- `SerializationManager`: Manager for custom serialization formats with compression support
- `FilePriorityManager`: Manager for file priority and request ordering

## [2025-12-16] - Session 6 Implementation

### Added Enums (Session 6)

- `AgentState` enum: INITIALIZED, READING, PROCESSING, WRITING, COMPLETED, ERROR
- `ResponseQuality` enum: EXCELLENT, GOOD, ACCEPTABLE, POOR, INVALID
- `EventType` enum: PRE_READ, POST_READ, PRE_IMPROVE, POST_IMPROVE, PRE_WRITE, POST_WRITE, ERROR

### Added Dataclasses (Session 6)

- `PromptTemplate`: Reusable prompt template with id, name, template, description, version, tags
- `ConversationMessage`: Message in conversation history with role, content, timestamp
- `CacheEntry`: Cached response entry with key, response, timestamp, hit_count, quality_score
- `AgentConfig`: Agent configuration from environment (backend, model, max_tokens, temperature, retry_count, timeout, cache_enabled, token_budget)
- `HealthCheckResult`: Health check result with healthy, backend_available, memory_ok, disk_ok, details

### Added Constants

- `DEFAULT_PROMPT_TEMPLATES`: Pre-defined templates for improve_code, add_docstrings, fix_bugs, add_tests

### Added Methods

- `_load_config()`: Load configuration from environment variables
- `set_model()`, `get_model()`: Model selection per agent
- `register_template()`, `get_template()`, `improve_with_template()`: Prompt template system
- `add_to_history()`, `clear_history()`, `get_history()`, `_build_prompt_with_history()`: Conversation history
- `add_post_processor()`, `clear_post_processors()`: Response post-processing hooks
- `_score_response_quality()`: Response quality scoring with automatic retry
- `_generate_cache_key()`, `clear_cache()`, `get_cache_stats()`: Response caching
- `get_token_usage()`, `check_token_budget()`: Token budget management
- `register_hook()`, `unregister_hook()`, `_trigger_event()`: Event hook system
- `register_plugin()`, `get_plugin()`: Plugin system
- `health_check()`: Agent health checks and diagnostics
- `save_state()`, `load_state()`: State persistence across runs
- `estimate_tokens()`, `truncate_for_context()`: Context window management

## [Previous]

- Initial version of base_agent.py
- 2025-12-15: Force UTF-8 decoding for `subprocess` output to avoid Windows `cp1252` decode failures.
- 2025-12-15: Add multi-backend AI routing (`DV_AGENT_BACKEND`) supporting local `copilot` CLI, `gh copilot`, and GitHub Models.
- 2025-12-15: Add backend diagnostics (`--describe-backends`, `describe_backends`, `get_backend_status`) without leaking secrets.
- 2025-12-15: Move token access out of import-time code paths; treat missing/invalid configuration as a recoverable condition in `auto` mode.

## [2025-12-16]

- Improved `agent_backend` import logic. (Fixed)
- Added type hints for all methods. (Fixed)
- Add logging for all major actions. (Fixed)
- Add comprehensive docstrings for all methods following Google style format. (Fixed)
- Add unit tests for edge cases (missing files, permission errors, encoding issues). (Fixed)
- Add unit tests for context manager functionality (__enter__, __exit__). (Fixed)
- Test retry logic with various failure scenarios and network conditions. (Fixed)
- Review and remove all `type: ignore` comments, fix underlying type issues. (Fixed)
- Use `pathlib` consistently throughout (replace `str(path)` with `Path` objects). (Fixed)
- Add configuration class to manage backend selection, logging, timeouts, retries. (Fixed)
- Add request/response caching to avoid redundant AI calls for identical prompts. (Fixed)
- Support streaming response from AI backends for real-time output. (Fixed)
- Add timeout parameter to all subprocess calls. (Fixed)
- Implement response validation: ensure AI output contains expected content types. (Fixed)
- Add cost estimation for API-based backends (track tokens, calculate cost). (Fixed)
- Create `BackendFactory` pattern for cleaner backend instantiation. (Fixed)
- Add detailed logging of all backend requests/responses (without leaking API keys). (Fixed)
- Implement graceful degradation: fall back to local models if API unavailable. (Fixed)
- Add integration tests with real AI backends for end-to-end validation. (Fixed)

## [2025-12-15]

- Added robust file reading with error handling in `read_previous_content`.
- Added explicit type hints to `__init__`.
- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting). (Fixed)
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports. (Fixed)
- Function `__init__` is missing type annotations. (Fixed)
- Function `create_main_function` is missing type annotations. (Fixed)
- Function `main` is missing type annotations. (Fixed)
- Function `update_file` is missing type annotations. (Fixed)
