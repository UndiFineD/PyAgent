# Description: `base_agent.py`

## Module purpose
Base Agent: Common functionality for all AI-powered agents.

Provides shared functionality for agents that improve code files using AI assistance.

## Location
- Path: `scripts/agent/base_agent.py`

## Public surface
- Classes: BaseAgent
- Functions: setup_logging, _resolve_repo_root, _command_available, create_main_function

## Behavior summary
- Uses `argparse` for CLI parsing.
- Invokes external commands via `subprocess`.
- Mutates `sys.path` to import sibling modules.

## Key dependencies
- Top imports: `argparse`, `difflib`, `json`, `logging`, `os`, `pathlib`, `subprocess`, `sys`, `typing`, `requests`, `scripts.fix.fix_markdown_lint`, `fix_markdown_lint`

## File fingerprint
- SHA256(source): `89f539359072285a…`
