# Splice: src/core/base/common/models/agent_models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- AgentConfig
- ComposedAgent
- AgentHealthCheck
- AgentPluginConfig
- ExecutionProfile
- AgentPipeline
- AgentParallel
- AgentRouter

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
