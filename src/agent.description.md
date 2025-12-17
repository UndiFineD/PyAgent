# Description: `agent.py`

## Module purpose
Agent: Orchestrates work among sub-agents for code improvement.

Assigns tasks to various agents to improve code files, their documentation,
tests, and related artifacts.

## Description
This module provides the main Agent that coordinates the improvement process
across code files by calling specialized sub-agents for different aspects
of code quality and documentation.

## Changelog
- 1.0.0: Initial implementation

## Suggested Fixes
- Add better error handling
- Implement async execution for agents

## Improvements
- Enhanced coordination between agents
- Better progress tracking

## Location
- Path: `scripts/agent/agent.py`

## Public surface
- Classes: Agent
- Functions: setup_logging, load_codeignore, main

## Behavior summary
- Has a CLI entrypoint (`__main__`).
- Uses `argparse` for CLI parsing.
- Invokes external commands via `subprocess`.
- Mutates `sys.path` to import sibling modules.

## Key dependencies
- Top imports: `subprocess`, `sys`, `os`, `logging`, `pathlib`, `typing`, `argparse`, `fnmatch`, `fix_markdown_lint`, `re`

## File fingerprint
- SHA256(source): `643e371284bca0e0…`
