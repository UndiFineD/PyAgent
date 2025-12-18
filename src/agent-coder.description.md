# Description: `agent-coder.py`

## Module purpose

Improves and updates code files.

The agent delegates to `BaseAgent` for LLM-backed improvements (when available)
and then validates the generated output (for Python files) before writing.

## Location

- Path: `src/agent-coder.py`

## Public surface

- Class: `CoderAgent(BaseAgent)`
  - `improve_content(prompt: str) -> str`
- CLI entry point:
  - `main` is created via `create_main_function(CoderAgent, ...)` and executed
    under `if __name__ == "__main__":`.

## Validation behavior

- Python syntax validation (hard fail):
  - `_validate_syntax()` parses with `ast.parse()`.
  - On failure, the agent reverts to the prior content.
- Python style validation (soft fail):
  - `_validate_flake8()` runs `flake8` on a temporary file if `flake8` is available.
  - On failure, the agent logs a warning but proceeds.

## Notes

- Non-Python files skip the AST/flake8 checks.
- The module includes many analysis helpers (metrics, smells, refactoring patterns,
  dependency analysis, accessibility analysis). Only `CoderAgent` is the CLI-facing agent.

## File fingerprint

- SHA256(source): `50e12a910c74c36c3d1b6594891b02637a4597504cffc6b31a4b9359bb9d28fa`
