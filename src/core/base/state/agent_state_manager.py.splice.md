# Splice: src/core/base/state/agent_state_manager.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EmergencyEventLog
- AgentCircuitBreaker
- AgentCheckpointManager
- StateDriftDetector
- StructuredErrorValidator
- StateTransaction
- AgentStateManager

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
