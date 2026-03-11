# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Tools Framework Design

`src/tools` contains utility functions and helper classes used throughout the
project. The legacy `ToolParserFramework.py` has been successfully refactored
into a modular, maintainable structure with clear separation of concerns.

## Goals

- **Central registry** of available tools so agents and CLI scripts can
  discover and invoke them dynamically.
- **Parsing helpers** for standardizing command syntax, argument parsing, and
  configuration loading.
- **Error handling** wrappers to ensure uniform logging and exit codes.
- **Testability** – ability to stub or mock tools during automated testing.

## Implementation Status

All core design elements have been successfully implemented:
- `dev_tools_autonomy_design.md` - Implemented
- `dev_tools_capabilities_design.md` - Implemented
- `dev_tools_implementation_design.md` - Implemented
- `dev_tools_structure_design.md` - Implemented
- `dev_tools_utilities_design.md` - Implemented

## Legacy Insights

The original monolithic `ToolParserFramework.py` has been successfully refactored
into a modular, maintainable structure with clear separation of concerns.

## Brainstorm Topics

- Design of a `Tool` base class with metadata (name, description, version).
- Automatic documentation generation from tool definitions.
- Permission model for tools in multi-tenant or fleet environments.
- Integration with `tools.pm` (recently added) to enable Python-based tools as
  first-class citizens.

*Consider reusing any comments from `src-old` modules in the `tools/` folder
if present.*