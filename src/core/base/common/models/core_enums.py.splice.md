# Splice: src/core/base/common/models/core_enums.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AgentState
- ResponseQuality
- FailureClassification
- EventType
- AuthMethod
- SerializationFormat
- FilePriority
- InputType
- AgentType
- MessageRole
- AgentEvent
- AgentExecutionState
- AgentPriority
- ConfigFormat
- DiffOutputFormat
- HealthStatus
- LockType
- RateLimitStrategy

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
