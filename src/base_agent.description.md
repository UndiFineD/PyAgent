# Description: `base_agent.py`

## Module purpose
`base_agent.py` provides the shared foundation for agent modules in this repo.

The primary class is `BaseAgent`, which reads a target file, sends an improvement request through `agent_backend`, stores the improved content, and writes changes back to disk (optionally normalizing markdown-like files).

## Location
- Path: `src/base_agent.py`

## Public surface
- Classes: `BaseAgent`
- Functions: `setup_logging`, `create_main_function`

## Behavior summary
- Uses `argparse` in `create_main_function()` to provide a uniform CLI wrapper for agent classes.
- Integrates with `agent_backend` for backend selection (e.g., `DV_AGENT_BACKEND`) and diagnostics (`describe_backends`).
- Applies markdown normalization only for markdown-like files (`.md`, `.markdown`, `.plan.md`).
- Uses a small in-memory response cache keyed by a SHA256-derived cache key.
- Performs lightweight health checks and can persist minimal state to `{file_path}.state.json`.

Note: This module contains many supporting enums/dataclasses/utilities (templates, caching, batching, auth config, serialization config, etc.) used by the agent ecosystem.

## Key dependencies
- Top imports: `argparse`, `difflib`, `hashlib`, `json`, `logging`, `os`, `pathlib`, `sys`, `time`, `typing`
- Internal dependency: `agent_backend`
- Optional dependency: markdown fixer (`scripts.fix.fix_markdown_lint` or `fix/fix_markdown_lint.py`)

## File fingerprint
- SHA256(source): `49f35f6c430130c8f7c79fb93bbdfbac2214b026d57276362d33a4aaf1413978`
