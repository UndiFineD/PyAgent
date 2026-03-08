# Description: `agent_backend.py`

## Module purpose

Multi-backend execution engine with fallback and caching capabilities.

## Location
- Path: `src\agent_backend.py`

## Public surface
- Classes: (none)
- Functions: _resolve_repo_root, _command_available, _get_cache_key, clear_response_cache, get_metrics, reset_metrics, validate_response_content, estimate_tokens, estimate_cost, configure_timeout_per_backend, llm_chat_via_github_models, run_subagent, get_backend_status, describe_backends

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `sys`, `pathlib`, `typing`, `requests`, `subprocess`, `src.classes.backend`

## Metadata

- SHA256(source): `05ed2ac666eb7c3c`
- Last updated: `2026-01-08 22:51:32`
- File: `src\agent_backend.py`