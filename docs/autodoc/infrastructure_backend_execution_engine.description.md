# Description: `execution_engine.py`

## Module purpose

Multi-backend execution engine with fallback and caching capabilities.

## Location
- Path: `infrastructure\backend\execution_engine.py`

## Public surface
- Classes: (none)
- Functions: _resolve_repo_root, _command_available, _get_cache_key, clear_response_cache, get_metrics, reset_metrics, validate_response_content, estimate_tokens, estimate_cost, configure_timeout_per_backend, llm_chat_via_github_models, run_subagent, get_backend_status, describe_backends

## Behavior summary
- Invokes external commands via `subprocess`.

## Key dependencies
- Top imports: `src.core.base.version`, `sys`, `pathlib`, `typing`, `requests`, `subprocess`, `src.infrastructure.backend`

## Metadata

- SHA256(source): `90c989183b63b047`
- Last updated: `2026-01-11 12:53:10`
- File: `infrastructure\backend\execution_engine.py`