# Description: `test_agent.py`

## Module purpose

Tests for `src/agent.py`.

Run directly via:

    pytest src/test_agent.py

## Location

- Path: `src/test_agent.py`

## Public surface

- Classes: (none)
- Functions: agent_module, repo_root, test_agent_initialization_defaults, test_load_codeignore_ignores_comments, test_find_code_files_filters_extensions, test_agents_only_filters_to_scripts_agent, test_max_files_limits_results, test_is_ignored_matches_globs, test_run_stats_update_invokes_subprocess, test_run_tests_no_test_file_does_not_invoke_subprocess, test_run_tests_with_test_file_invokes_pytest

## Behavior summary

- Invokes external commands via `subprocess`.

## Key dependencies

- Top imports: `__future__`, `importlib`, `pathlib`, `pytest`, `agent_test_utils`, `agent`

## File fingerprint

- SHA256(source): `FFA6BF5CD0EFABA20EBDBD2A728EF98C8ABB31BF183543730D87DC1F49ADAD1B`
