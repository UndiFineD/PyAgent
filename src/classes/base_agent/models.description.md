# models

**File**: `src\classes\base_agent\models.py`  
**Type**: Python Module  
**Summary**: 53 classes, 16 functions, 15 imports  
**Lines**: 1051  
**Complexity**: 56 (very_complex)

## Overview

Data models and structures for BaseAgent.

## Classes (53)

### `AgentState`

**Inherits from**: Enum

Agent lifecycle states.

### `ResponseQuality`

**Inherits from**: Enum

AI response quality levels.

### `EventType`

**Inherits from**: Enum

Agent event types for hooks.

### `AuthMethod`

**Inherits from**: Enum

Authentication methods for backends.

### `SerializationFormat`

**Inherits from**: Enum

Custom serialization formats.

### `FilePriority`

**Inherits from**: Enum

File priority levels for request prioritization.

### `InputType`

**Inherits from**: Enum

Input types for multimodal support.

### `AgentType`

**Inherits from**: Enum

Agent type classifications.

### `MessageRole`

**Inherits from**: Enum

Roles for conversation messages.

### `AgentEvent`

**Inherits from**: Enum

Agent event types.

### `AgentExecutionState`

**Inherits from**: Enum

Execution state for an agent run.

### `AgentPriority`

**Inherits from**: Enum

Priority level for agent execution.

### `ConfigFormat`

**Inherits from**: Enum

Configuration file format.

### `DiffOutputFormat`

**Inherits from**: Enum

Output format for diff preview.

### `HealthStatus`

**Inherits from**: Enum

Health status for components.

### `LockType`

**Inherits from**: Enum

File locking type.

### `RateLimitStrategy`

**Inherits from**: Enum

Rate limiting strategy for API calls.

### `PromptTemplate`

Reusable prompt template.

Attributes:
    name: Human-readable template name.
    template: The prompt template with {variables}.
    variables: List of variable names in the template.
    id: Optional unique identifier for the template.
    description: Description of when to use this template.
    version: Version string for A/B testing.
    tags: Tags for categorization.

**Methods** (1):
- `render(self)`

### `ConversationMessage`

A message in conversation history.

Attributes:
    role: The role (user, assistant, system).
    content: Message content.
    timestamp: When the message was created.

### `ConversationHistory`

Manages a conversation history with message storage and retrieval.

**Methods** (4):
- `__init__(self, max_messages)`
- `add(self, role, content)`
- `get_context(self)`
- `clear(self)`

### `PromptTemplateManager`

Manages a collection of prompt templates.

**Methods** (3):
- `__init__(self)`
- `register(self, template)`
- `render(self, template_name)`

### `ResponsePostProcessor`

Manages post-processing hooks for agent responses.

**Methods** (3):
- `__init__(self)`
- `register(self, hook, priority)`
- `process(self, text)`

### `PromptVersion`

Versioned prompt for A/B testing.

Supports both simple and advanced versioning APIs.

Attributes:
    version: Version identifier.
    content: The prompt content.
    description: Prompt description.
    active: Whether this version is active.
    created_at: Creation timestamp.
    metrics: Performance metrics.
    version_id: Alias for version (compatibility).
    template_id: Template identifier (compatibility).
    variant: Variant name (compatibility).
    prompt_text: Alias for content (compatibility).
    weight: Selection weight (compatibility).

**Methods** (1):
- `__init__(self, version, content, description, active, version_id, template_id, variant, prompt_text, weight)`

### `BatchRequest`

Request in a batch processing queue.

Supports both generic batching (with items) and file-based batching.

Attributes:
    file_path: Path to the file to process (optional).
    prompt: Improvement prompt (optional).
    priority: Processing priority.
    callback: Optional callback on completion.
    max_size: Maximum batch size (for generic batching).
    items: Items in the batch (for generic batching).

**Methods** (4):
- `__init__(self, file_path, prompt, priority, callback, max_size)`
- `add(self, item)`
- `size(self)`
- `execute(self, processor)`

### `CacheEntry`

Cached response entry.

Attributes:
    key: Content-based cache key.
    response: Cached response content.
    timestamp: When the entry was cached.
    hit_count: Number of cache hits.
    quality_score: Quality score of response.

### `AgentConfig`

Agent configuration from environment or file.

Attributes:
    backend: AI backend to use.
    model: Model name/ID for the backend.
    max_tokens: Maximum tokens per request.
    temperature: Sampling temperature.
    retry_count: Number of retries on failure.
    timeout: Request timeout in seconds.
    cache_enabled: Whether to enable response caching.
    token_budget: Total token budget for session.

### `HealthCheckResult`

Result of agent health check.

Attributes:
    healthy: Overall health status.
    backend_available: Whether AI backend is available.
    memory_ok: Whether memory usage is acceptable.
    disk_ok: Whether disk space is sufficient.
    details: Additional health details.

### `AuthConfig`

Authentication configuration.

Attributes:
    method: Authentication method type.
    api_key: API key for API_KEY auth.
    token: Bearer token for token-based auth.
    username: Username for basic auth.
    password: Password for basic auth.
    oauth_client_id: OAuth2 client ID.
    oauth_client_secret: OAuth2 client secret.
    custom_headers: Custom headers to include.

### `BatchResult`

Result of a batch processing request.

Attributes:
    file_path: Path to the processed file.
    success: Whether processing succeeded.
    content: Processed content if successful.
    error: Error message if failed.
    processing_time: Time taken to process.

### `MultimodalInput`

Multimodal input for agents.

Attributes:
    input_type: Type of input (text, image, etc.).
    content: Content data (text, base64, path).
    mime_type: MIME type for binary content.
    metadata: Additional input metadata.

### `ComposedAgent`

Configuration for agent composition.

Attributes:
    agent_type: Type of agent to use.
    config: Agent-specific configuration.
    order: Execution order in composition.
    depends_on: Other agents this depends on.

### `SerializationConfig`

Configuration for custom serialization.

Attributes:
    format: Serialization format.
    options: Format-specific options.
    compression: Whether to compress output.
    encryption: Whether to encrypt output.

### `FilePriorityConfig`

Configuration for file priority.

Attributes:
    path_patterns: Patterns mapped to priorities.
    extension_priorities: Extensions mapped to priorities.
    default_priority: Default priority level.

### `ContextWindow`

Manages token-based context window.

**Methods** (4):
- `used_tokens(self)`
- `available_tokens(self)`
- `add(self, message, token_count)`
- `clear(self)`

### `MultimodalBuilder`

Builds multimodal input sets.

**Methods** (4):
- `add(self, content, input_type)`
- `add_text(self, content)`
- `add_image(self, content)`
- `build(self)`

### `AgentPipeline`

Chains agent steps sequentially.

**Methods** (2):
- `add_step(self, name, func)`
- `execute(self, data)`

### `AgentParallel`

Executes agent branches in parallel conceptually.

**Methods** (2):
- `add_branch(self, name, func)`
- `execute(self, data)`

### `AgentRouter`

Routes input based on conditions.

**Methods** (3):
- `add_route(self, condition, handler)`
- `set_default(self, handler)`
- `route(self, data)`

### `TokenBudget`

Manages token allocation.

**Methods** (4):
- `used(self)`
- `remaining(self)`
- `allocate(self, name, tokens)`
- `release(self, name)`

### `ExecutionCondition`

A condition for agent execution.

Attributes:
    name: Condition name.
    check: Function to check condition.
    description: Human - readable description.

### `IncrementalState`

State for incremental processing.

Attributes:
    last_run_timestamp: Timestamp of last successful run.
    processed_files: Dict of file paths to their last processed timestamp.
    file_hashes: Dict of file paths to their content hashes.
    pending_files: List of files pending processing.

### `RateLimitConfig`

Configuration for rate limiting.

Attributes:
    requests_per_second: Maximum requests per second.
    requests_per_minute: Maximum requests per minute.
    burst_size: Maximum burst size for token bucket.
    strategy: Rate limiting strategy to use.
    cooldown_seconds: Cooldown period after hitting limit.

### `ShutdownState`

State for graceful shutdown.

Attributes:
    shutdown_requested: Whether shutdown has been requested.
    current_file: Currently processing file.
    completed_files: List of completed files.
    pending_files: List of pending files.
    start_time: Processing start time.

### `ValidationRule`

Consolidated validation rule for Phase 126.

**Methods** (1):
- `__post_init__(self)`

### `ModelConfig`

Model configuration.

### `ConfigProfile`

Configuration profile.

**Methods** (1):
- `get(self, key, default)`

### `AgentHealthCheck`

Health check result for an agent.

Attributes:
    agent_name: Name of the agent.
    status: Health status.
    response_time_ms: Response time in milliseconds.
    last_check: Timestamp of last health check.
    error_message: Error message if unhealthy.
    details: Additional health details.

### `AgentPluginConfig`

Configuration for an agent plugin.

Attributes:
    name: Unique plugin name.
    module_path: Path to the plugin module.
    entry_point: Entry point function name.
    priority: Execution priority.
    enabled: Whether the plugin is enabled.
    config: Plugin - specific configuration.

### `CachedResult`

A cached agent result.

Attributes:
    file_path: File that was processed.
    agent_name: Agent that produced result.
    content_hash: Hash of input content.
    result: The cached result.
    timestamp: When cached.
    ttl_seconds: Time to live.

### `DiffResult`

Result of a diff operation.

Attributes:
    file_path: Path to the file.
    original_content: Original file content.
    modified_content: Modified content after changes.
    diff_lines: List of diff lines.
    additions: Number of lines added.
    deletions: Number of lines deleted.
    changes: Number of lines changed.

### `ExecutionProfile`

A profile for agent execution settings.

Attributes:
    name: Profile name.
    max_files: Maximum files to process.
    timeout: Timeout per operation.
    parallel: Enable parallel execution.
    workers: Number of workers.
    dry_run: Dry run mode.

### `TelemetrySpan`

A telemetry span for tracing.

Attributes:
    name: Span name.
    trace_id: Trace identifier.
    span_id: Span identifier.
    parent_id: Parent span ID.
    start_time: Start timestamp.
    end_time: End timestamp.
    attributes: Span attributes.
    events: Span events.

### `SpanContext`

Context for a telemetry span.

**Methods** (3):
- `__init__(self, span)`
- `set_attribute(self, key, value)`
- `add_event(self, name, attributes)`

## Functions (16)

### `_empty_list_str()`

### `_empty_list_int()`

### `_empty_list_float()`

### `_empty_list_dict_str_any()`

### `_empty_dict_str_float()`

### `_empty_dict_str_any()`

### `_empty_dict_str_int()`

### `_empty_dict_str_str()`

### `_empty_dict_str_callable_any_any()`

### `_empty_dict_str_quality_criteria()`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `enum.auto`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
