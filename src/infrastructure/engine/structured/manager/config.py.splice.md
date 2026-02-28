# Splice: src/infrastructure/engine/structured/manager/config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- GrammarType
- CompilationStatus
- GrammarSpec
- CompilationResult
- ValidationResult
- BackendStats

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
