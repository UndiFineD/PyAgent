# Description: `test_base_agent.py`

## Module purpose

Tests for `src/base_agent.py`.

Run directly via:

    pytest src/test_base_agent.py

## Location

- Path: `src/test_base_agent.py`

## Public surface

- Classes: (none)
- Functions: base_agent_module, test_read_previous_content_existing_file, test_read_previous_content_missing_file_uses_default, test_improve_content_uses_run_subagent, test_update_file_writes_content, test_get_diff_contains_unified_markers, test_run_subagent_prefers_local_copilot_cli, test_run_subagent_falls_back_to_gh_copilot_explain, test_llm_chat_via_github_models_builds_request_and_parses_response, test_llm_chat_via_github_models_requires_token_and_base_url, test_run_subagent_uses_github_models_backend

## Behavior summary

- Invokes external commands via `subprocess`.

## Key dependencies

- Top imports: `__future__`, `pathlib`, `typing`, `pytest`, `agent_test_utils`, `base_agent`

## File fingerprint

- SHA256(source): `1EADF6C4D33D2CA3A743EFE17504CAB6D354E9379DCE26F0BD4532115DE961A2`
