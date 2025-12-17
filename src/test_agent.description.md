# Description: `test_agent.py`

## Module purpose
Legacy tests for scripts/agent/agent.py.

These tests live next to the agent scripts so they can be run directly via:

    pytest scripts/agent/test_agent.py

## Location
- Path: `scripts/agent/test_agent.py`

## Public surface
- Classes: (none)
- Functions: agent_module, repo_root, test_agent_initialization_defaults, test_load_codeignore_ignores_comments, test_find_code_files_filters_extensions, test_agents_only_filters_to_scripts_agent, test_max_files_limits_results, test_is_ignored_matches_globs, test_run_stats_update_invokes_subprocess, test_run_tests_no_test_file_does_not_invoke_subprocess, test_run_tests_with_test_file_invokes_pytest

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `__future__`, `importlib`, `pathlib`, `pytest`, `agent_test_utils`, `agent`

## File fingerprint
- SHA256(source): `1a01518c077111e6…`
