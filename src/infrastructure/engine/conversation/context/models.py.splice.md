# Splice: src/infrastructure/engine/conversation/context/models.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ContextState
- TurnType
- ToolExecutionPolicy
- TokenMetrics
- ConversationTurn
- ToolExecution
- ContextConfig
- ContextSnapshot

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
