# Splice: src/infrastructure/engine/structured/structured_output_orchestrator.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- StructuredOutputBackendType
- ConstraintType
- GrammarProtocol
- BackendProtocol
- ConstraintSpec
- OrchestratorConfig
- BackendWrapper
- CompiledGrammarHandle
- StructuredOutputOrchestrator
- AsyncStructuredOutputOrchestrator
- BatchProcessor

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
