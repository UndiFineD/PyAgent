# Class Breakdown: models

**File**: `src\classes\base_agent\models.py`  
**Classes**: 53

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentState`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

Agent lifecycle states.

[TIP] **Suggested split**: Move to `agentstate.py`

---

### 2. `ResponseQuality`

**Line**: 52  
**Inherits**: Enum  
**Methods**: 0

AI response quality levels.

[TIP] **Suggested split**: Move to `responsequality.py`

---

### 3. `EventType`

**Line**: 60  
**Inherits**: Enum  
**Methods**: 0

Agent event types for hooks.

[TIP] **Suggested split**: Move to `eventtype.py`

---

### 4. `AuthMethod`

**Line**: 70  
**Inherits**: Enum  
**Methods**: 0

Authentication methods for backends.

[TIP] **Suggested split**: Move to `authmethod.py`

---

### 5. `SerializationFormat`

**Line**: 80  
**Inherits**: Enum  
**Methods**: 0

Custom serialization formats.

[TIP] **Suggested split**: Move to `serializationformat.py`

---

### 6. `FilePriority`

**Line**: 89  
**Inherits**: Enum  
**Methods**: 0

File priority levels for request prioritization.

[TIP] **Suggested split**: Move to `filepriority.py`

---

### 7. `InputType`

**Line**: 97  
**Inherits**: Enum  
**Methods**: 0

Input types for multimodal support.

[TIP] **Suggested split**: Move to `inputtype.py`

---

### 8. `AgentType`

**Line**: 106  
**Inherits**: Enum  
**Methods**: 0

Agent type classifications.

[TIP] **Suggested split**: Move to `agenttype.py`

---

### 9. `MessageRole`

**Line**: 114  
**Inherits**: Enum  
**Methods**: 0

Roles for conversation messages.

[TIP] **Suggested split**: Move to `messagerole.py`

---

### 10. `AgentEvent`

**Line**: 120  
**Inherits**: Enum  
**Methods**: 0

Agent event types.

[TIP] **Suggested split**: Move to `agentevent.py`

---

### 11. `AgentExecutionState`

**Line**: 126  
**Inherits**: Enum  
**Methods**: 0

Execution state for an agent run.

[TIP] **Suggested split**: Move to `agentexecutionstate.py`

---

### 12. `AgentPriority`

**Line**: 135  
**Inherits**: Enum  
**Methods**: 0

Priority level for agent execution.

[TIP] **Suggested split**: Move to `agentpriority.py`

---

### 13. `ConfigFormat`

**Line**: 143  
**Inherits**: Enum  
**Methods**: 0

Configuration file format.

[TIP] **Suggested split**: Move to `configformat.py`

---

### 14. `DiffOutputFormat`

**Line**: 150  
**Inherits**: Enum  
**Methods**: 0

Output format for diff preview.

[TIP] **Suggested split**: Move to `diffoutputformat.py`

---

### 15. `HealthStatus`

**Line**: 157  
**Inherits**: Enum  
**Methods**: 0

Health status for components.

[TIP] **Suggested split**: Move to `healthstatus.py`

---

### 16. `LockType`

**Line**: 164  
**Inherits**: Enum  
**Methods**: 0

File locking type.

[TIP] **Suggested split**: Move to `locktype.py`

---

### 17. `RateLimitStrategy`

**Line**: 170  
**Inherits**: Enum  
**Methods**: 0

Rate limiting strategy for API calls.

[TIP] **Suggested split**: Move to `ratelimitstrategy.py`

---

### 18. `PromptTemplate`

**Line**: 229  
**Methods**: 1

Reusable prompt template.

Attributes:
    name: Human-readable template name.
    template: The prompt template with {variables}.
    variables: List of variable names in the template.
    id: Option...

[TIP] **Suggested split**: Move to `prompttemplate.py`

---

### 19. `ConversationMessage`

**Line**: 261  
**Methods**: 0

A message in conversation history.

Attributes:
    role: The role (user, assistant, system).
    content: Message content.
    timestamp: When the message was created.

[TIP] **Suggested split**: Move to `conversationmessage.py`

---

### 20. `ConversationHistory`

**Line**: 273  
**Methods**: 4

Manages a conversation history with message storage and retrieval.

[TIP] **Suggested split**: Move to `conversationhistory.py`

---

### 21. `PromptTemplateManager`

**Line**: 311  
**Methods**: 3

Manages a collection of prompt templates.

[TIP] **Suggested split**: Move to `prompttemplatemanager.py`

---

### 22. `ResponsePostProcessor`

**Line**: 342  
**Methods**: 3

Manages post-processing hooks for agent responses.

[TIP] **Suggested split**: Move to `responsepostprocessor.py`

---

### 23. `PromptVersion`

**Line**: 374  
**Methods**: 1

Versioned prompt for A/B testing.

Supports both simple and advanced versioning APIs.

Attributes:
    version: Version identifier.
    content: The prompt content.
    description: Prompt description...

[TIP] **Suggested split**: Move to `promptversion.py`

---

### 24. `BatchRequest`

**Line**: 435  
**Methods**: 4

Request in a batch processing queue.

Supports both generic batching (with items) and file-based batching.

Attributes:
    file_path: Path to the file to process (optional).
    prompt: Improvement p...

[TIP] **Suggested split**: Move to `batchrequest.py`

---

### 25. `CacheEntry`

**Line**: 506  
**Methods**: 0

Cached response entry.

Attributes:
    key: Content-based cache key.
    response: Cached response content.
    timestamp: When the entry was cached.
    hit_count: Number of cache hits.
    quality_...

[TIP] **Suggested split**: Move to `cacheentry.py`

---

### 26. `AgentConfig`

**Line**: 523  
**Methods**: 0

Agent configuration from environment or file.

Attributes:
    backend: AI backend to use.
    model: Model name/ID for the backend.
    max_tokens: Maximum tokens per request.
    temperature: Sampli...

[TIP] **Suggested split**: Move to `agentconfig.py`

---

### 27. `HealthCheckResult`

**Line**: 546  
**Methods**: 0

Result of agent health check.

Attributes:
    healthy: Overall health status.
    backend_available: Whether AI backend is available.
    memory_ok: Whether memory usage is acceptable.
    disk_ok: W...

[TIP] **Suggested split**: Move to `healthcheckresult.py`

---

### 28. `AuthConfig`

**Line**: 563  
**Methods**: 0

Authentication configuration.

Attributes:
    method: Authentication method type.
    api_key: API key for API_KEY auth.
    token: Bearer token for token-based auth.
    username: Username for basic...

[TIP] **Suggested split**: Move to `authconfig.py`

---

### 29. `BatchResult`

**Line**: 586  
**Methods**: 0

Result of a batch processing request.

Attributes:
    file_path: Path to the processed file.
    success: Whether processing succeeded.
    content: Processed content if successful.
    error: Error ...

[TIP] **Suggested split**: Move to `batchresult.py`

---

### 30. `MultimodalInput`

**Line**: 603  
**Methods**: 0

Multimodal input for agents.

Attributes:
    input_type: Type of input (text, image, etc.).
    content: Content data (text, base64, path).
    mime_type: MIME type for binary content.
    metadata: ...

[TIP] **Suggested split**: Move to `multimodalinput.py`

---

### 31. `ComposedAgent`

**Line**: 618  
**Methods**: 0

Configuration for agent composition.

Attributes:
    agent_type: Type of agent to use.
    config: Agent-specific configuration.
    order: Execution order in composition.
    depends_on: Other agent...

[TIP] **Suggested split**: Move to `composedagent.py`

---

### 32. `SerializationConfig`

**Line**: 633  
**Methods**: 0

Configuration for custom serialization.

Attributes:
    format: Serialization format.
    options: Format-specific options.
    compression: Whether to compress output.
    encryption: Whether to enc...

[TIP] **Suggested split**: Move to `serializationconfig.py`

---

### 33. `FilePriorityConfig`

**Line**: 648  
**Methods**: 0

Configuration for file priority.

Attributes:
    path_patterns: Patterns mapped to priorities.
    extension_priorities: Extensions mapped to priorities.
    default_priority: Default priority level.

[TIP] **Suggested split**: Move to `filepriorityconfig.py`

---

### 34. `ContextWindow`

**Line**: 661  
**Methods**: 4

Manages token-based context window.

[TIP] **Suggested split**: Move to `contextwindow.py`

---

### 35. `MultimodalBuilder`

**Line**: 693  
**Methods**: 4

Builds multimodal input sets.

[TIP] **Suggested split**: Move to `multimodalbuilder.py`

---

### 36. `AgentPipeline`

**Line**: 714  
**Methods**: 2

Chains agent steps sequentially.

[TIP] **Suggested split**: Move to `agentpipeline.py`

---

### 37. `AgentParallel`

**Line**: 732  
**Methods**: 2

Executes agent branches in parallel conceptually.

[TIP] **Suggested split**: Move to `agentparallel.py`

---

### 38. `AgentRouter`

**Line**: 745  
**Methods**: 3

Routes input based on conditions.

[TIP] **Suggested split**: Move to `agentrouter.py`

---

### 39. `TokenBudget`

**Line**: 770  
**Methods**: 4

Manages token allocation.

[TIP] **Suggested split**: Move to `tokenbudget.py`

---

### 40. `ExecutionCondition`

**Line**: 796  
**Methods**: 0

A condition for agent execution.

Attributes:
    name: Condition name.
    check: Function to check condition.
    description: Human - readable description.

[TIP] **Suggested split**: Move to `executioncondition.py`

---

### 41. `IncrementalState`

**Line**: 810  
**Methods**: 0

State for incremental processing.

Attributes:
    last_run_timestamp: Timestamp of last successful run.
    processed_files: Dict of file paths to their last processed timestamp.
    file_hashes: Dic...

[TIP] **Suggested split**: Move to `incrementalstate.py`

---

### 42. `RateLimitConfig`

**Line**: 825  
**Methods**: 0

Configuration for rate limiting.

Attributes:
    requests_per_second: Maximum requests per second.
    requests_per_minute: Maximum requests per minute.
    burst_size: Maximum burst size for token b...

[TIP] **Suggested split**: Move to `ratelimitconfig.py`

---

### 43. `ShutdownState`

**Line**: 842  
**Methods**: 0

State for graceful shutdown.

Attributes:
    shutdown_requested: Whether shutdown has been requested.
    current_file: Currently processing file.
    completed_files: List of completed files.
    pe...

[TIP] **Suggested split**: Move to `shutdownstate.py`

---

### 44. `ValidationRule`

**Line**: 859  
**Methods**: 1

Consolidated validation rule for Phase 126.

[TIP] **Suggested split**: Move to `validationrule.py`

---

### 45. `ModelConfig`

**Line**: 876  
**Methods**: 0

Model configuration.

[TIP] **Suggested split**: Move to `modelconfig.py`

---

### 46. `ConfigProfile`

**Line**: 885  
**Methods**: 1

Configuration profile.

[TIP] **Suggested split**: Move to `configprofile.py`

---

### 47. `AgentHealthCheck`

**Line**: 898  
**Methods**: 0

Health check result for an agent.

Attributes:
    agent_name: Name of the agent.
    status: Health status.
    response_time_ms: Response time in milliseconds.
    last_check: Timestamp of last heal...

[TIP] **Suggested split**: Move to `agenthealthcheck.py`

---

### 48. `AgentPluginConfig`

**Line**: 917  
**Methods**: 0

Configuration for an agent plugin.

Attributes:
    name: Unique plugin name.
    module_path: Path to the plugin module.
    entry_point: Entry point function name.
    priority: Execution priority.
...

[TIP] **Suggested split**: Move to `agentpluginconfig.py`

---

### 49. `CachedResult`

**Line**: 936  
**Methods**: 0

A cached agent result.

Attributes:
    file_path: File that was processed.
    agent_name: Agent that produced result.
    content_hash: Hash of input content.
    result: The cached result.
    time...

[TIP] **Suggested split**: Move to `cachedresult.py`

---

### 50. `DiffResult`

**Line**: 956  
**Methods**: 0

Result of a diff operation.

Attributes:
    file_path: Path to the file.
    original_content: Original file content.
    modified_content: Modified content after changes.
    diff_lines: List of dif...

[TIP] **Suggested split**: Move to `diffresult.py`

---

### 51. `ExecutionProfile`

**Line**: 977  
**Methods**: 0

A profile for agent execution settings.

Attributes:
    name: Profile name.
    max_files: Maximum files to process.
    timeout: Timeout per operation.
    parallel: Enable parallel execution.
    w...

[TIP] **Suggested split**: Move to `executionprofile.py`

---

### 52. `TelemetrySpan`

**Line**: 997  
**Methods**: 0

A telemetry span for tracing.

Attributes:
    name: Span name.
    trace_id: Trace identifier.
    span_id: Span identifier.
    parent_id: Parent span ID.
    start_time: Start timestamp.
    end_ti...

[TIP] **Suggested split**: Move to `telemetryspan.py`

---

### 53. `SpanContext`

**Line**: 1020  
**Methods**: 3

Context for a telemetry span.

[TIP] **Suggested split**: Move to `spancontext.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
