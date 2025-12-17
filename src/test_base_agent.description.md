# Description: `test_base_agent.py`

## Module purpose
Legacy tests for base_agent.py.

These live next to the agent scripts so they can be run directly via:

    pytest scripts/agent/test_base_agent.py

## Location
- Path: `scripts/agent/test_base_agent.py`

## Public surface
- Classes: (none)
- Functions: base_agent_module, test_read_previous_content_existing_file, test_read_previous_content_missing_file_uses_default, test_improve_content_uses_run_subagent, test_update_file_writes_content, test_get_diff_contains_unified_markers, test_run_subagent_prefers_local_copilot_cli, test_run_subagent_falls_back_to_gh_copilot_explain, test_llm_chat_via_github_models_builds_request_and_parses_response, test_llm_chat_via_github_models_requires_token_and_base_url, test_run_subagent_uses_github_models_backend

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `__future__`, `pathlib`, `typing`, `pytest`, `agent_test_utils`, `base_agent`

## File fingerprint
- SHA256(source): `b98e61f9b798d70d…`
