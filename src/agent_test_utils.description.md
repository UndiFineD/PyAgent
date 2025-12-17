# Description: `agent_test_utils.py`

## Module purpose
Test utilities for agent scripts.

Provides helpers to load agent modules dynamically and manage sys.path for testing.

## Location
- Path: `scripts/agent/agent_test_utils.py`

## Public surface
- Classes: (none)
- Functions: agent_dir_on_path, load_agent_module

## Behavior summary
- Mutates `sys.path` to import sibling modules.

## Key dependencies
- Top imports: `__future__`, `importlib.util`, `re`, `sys`, `contextlib`, `pathlib`, `types`, `typing`

## File fingerprint
- SHA256(source): `e19868e4c8b5a47f…`
