# Description: `agent-tests.py`

## Module purpose

`agent-tests.py` defines `TestsAgent`, an AI-assisted agent for improving an existing Python test module.

The agent focuses on editing a single test file in-place, optionally enriching the prompt with context from the corresponding source file and applying lightweight validation before writing changes.

## Location

- Path: `src/agent-tests.py`

## Public surface

- Primary CLI agent: `TestsAgent`
- CLI entrypoint: `main = create_main_function(TestsAgent, ...)` (invoked under `if __name__ == '__main__':`)

## Behavior summary

- Enhances the improvement prompt with source-code context when a matching source file is found.
- Calls `BaseAgent.improve_content()` to obtain updated test content (when AI tooling is unavailable, the base implementation may leave content unchanged).
- Validates generated tests via `ast.parse()`; on syntax failure, it reverts to the previous content.
- Performs a lightweight structural pass and logs warnings (e.g., test functions that appear to have no assertions).
- Writes updated content back to disk without applying markdown-specific formatting.

## Source-file lookup

To locate the source file being tested, `TestsAgent` attempts:

- A same-directory lookup using the test file stem (e.g., `test_foo.py` -> `foo.py`).
- A parent-directory lookup when tests live in a `tests/` folder.
- A legacy project-structure lookup under `scripts/agent/`.

## Key dependencies

- `base_agent.BaseAgent` and `base_agent.create_main_function`
- `ast` (syntax validation)
- `hashlib` (IDs for internal test records)

## File fingerprint

- SHA256(source): `60429DF051E5EEE8E9BE332C1F4FDC3E3651DC2C5D7F14431C1A147EC525A061`
