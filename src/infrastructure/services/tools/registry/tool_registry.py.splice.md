# Splice: src/infrastructure/services/tools/registry/tool_registry.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- ToolParserRegistry
- StreamingToolParser

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
