# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

The runtime change has direct consequences for the tools subsystem. **Every
component of the tools framework (ToolManager, ToolExecutor, parsers, and
helper utilities) must expose `async` APIs and avoid any blocking or
synchronous loops.**  Tool implementations themselves are expected to be
`async fn`s, and callers in agents or CLI scripts will `await` their results.
Lifecycle hooks such as startup/shutdown, health checks, and logging are now
designed to return `Future`s.  This migration is already enforced by the
`tools/tests/async_usage.rs` suite, which exercises the ToolManager in a
non‑blocking event loop.

If additional runtime notes are needed they belong in a separate
CHANGELOG/operational-notes document; the remainder of this file focuses on
aspects of the tools framework that are influenced by—but not limited to—the
async runtime.

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