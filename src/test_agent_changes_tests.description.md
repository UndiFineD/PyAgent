# Description: `test_agent_changes_tests.py`

## Module purpose
Additional legacy tests for agent-changes.py.

This replaces the previous filename `test_agent-changes.tests.py`, which pytest
cannot import reliably because of the extra dot in the basename.

Run directly via:

    pytest scripts/agent/test_agent_changes_tests.py

## Location
- Path: `scripts/agent/test_agent_changes_tests.py`

## Public surface
- Classes: (none)
- Functions: base_agent_module, test_changes_agent_default_content_for_missing_file, test_changes_agent_non_keyword_sets_current_content

## Behavior summary
- Pure module (no obvious CLI/side effects).

## Key dependencies
- Top imports: `__future__`, `pathlib`, `typing`, `pytest`, `agent_test_utils`, `base_agent`

## File fingerprint
- SHA256(source): `38546284a589ab36…`
