# Description: `agent_backend.py`

## Module purpose

Handles communication with AI backends (GitHub Models, gh copilot, Copilot CLI, Codex CLI).

This module is the backend execution layer used by the main orchestrator. It
selects an available backend, builds prompts with bounded context, invokes the
backend, and returns the resulting text.

## Location

- Path: `src/agent_backend.py`

## Public surface

- Functions:
  - `run_subagent(description, prompt, original_content="") -> Optional[str]`
  - `llm_chat_via_github_models(...) -> str`
  - `get_backend_status() -> Dict[str, Any]`
  - `describe_backends() -> str`

## Key environment variables

- `DV_AGENT_BACKEND`: Force backend (`auto`, `codex`, `copilot`, `gh`, `github-models`).
- `DV_AGENT_REPO_ROOT`: Override repository root detection.
- `DV_AGENT_MAX_CONTEXT_CHARS`: Bound context size (default is handled in code).
- `DV_AGENT_MODEL`: Model name (used by GitHub Models backend).
- `DV_AGENT_SYSTEM_PROMPT`: System prompt override.
- `DV_AGENT_TIMEOUT_<BACKEND>`: Per-backend timeout override (e.g., `DV_AGENT_TIMEOUT_GH`).
- `GITHUB_TOKEN`: Token for GitHub Models API.
- `GITHUB_MODELS_BASE_URL`: Base URL for GitHub Models API.

## Optional dependencies

- `requests` is used for HTTP calls for API-based backends. When unavailable,
  API backends cannot be used.

## File fingerprint

- SHA256(source): `a77767a5d87a9e38472c078f6f242725dede9f19a2105d9f2f255206496b4d64`
