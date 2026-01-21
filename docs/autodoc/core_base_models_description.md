# Description: `models.py`

## Module purpose

Data models and structures for BaseAgent.

## Location
- Path: `core\base\models.py`

## Public surface
- Classes: AgentState, ResponseQuality, EventType, AuthMethod, SerializationFormat, FilePriority, InputType, AgentType, MessageRole, AgentEvent, AgentExecutionState, AgentPriority, ConfigFormat, DiffOutputFormat, HealthStatus, LockType, RateLimitStrategy, PromptTemplate, ConversationMessage, ConversationHistory, PromptTemplateManager, ResponsePostProcessor, PromptVersion, BatchRequest, CacheEntry, AgentConfig, HealthCheckResult, AuthConfig, BatchResult, MultimodalInput, ComposedAgent, SerializationConfig, FilePriorityConfig, ContextWindow, MultimodalBuilder, AgentPipeline, AgentParallel, AgentRouter, TokenBudget, ExecutionCondition, IncrementalState, RateLimitConfig, ShutdownState, ValidationRule, ModelConfig, ConfigProfile, AgentHealthCheck, AgentPluginConfig, CachedResult, DiffResult, ExecutionProfile, TelemetrySpan, SpanContext
- Functions: _empty_list_str, _empty_list_int, _empty_list_float, _empty_list_dict_str_any, _empty_dict_str_float, _empty_dict_str_any, _empty_dict_str_int, _empty_dict_str_str, _empty_dict_str_callable_any_any, _empty_dict_str_quality_criteria, _empty_dict_str_health_checks, _empty_dict_str_configprofile, _empty_routes_list, _empty_dict_str_filepriority, _empty_dict_str_modelconfig, _empty_agent_event_handlers

## Behavior summary
- Pure module (no obvious CLI / side effects).

## Key dependencies
- Top imports: `__future__`, `time`, `uuid`, `dataclasses`, `datetime`, `enum`, `pathlib`, `typing`

## Metadata

- SHA256(source): `c56324c29934fe2b`
- Last updated: `2026-01-11 12:52:58`
- File: `core\base\models.py`