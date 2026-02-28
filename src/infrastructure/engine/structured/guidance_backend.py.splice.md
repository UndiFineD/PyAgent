# Splice: src/infrastructure/engine/structured/guidance_backend.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- GuidanceTemplateType
- GuidanceVariable
- GuidanceTemplate
- GuidanceState
- CompiledGuidanceProgram
- GuidanceGrammar
- GuidanceBackend
- AsyncGuidanceBackend

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
