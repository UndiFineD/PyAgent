# TEST_QUALITY

This document defines the testing quality rules for PyAgent.

## Goals

You should maintain tests that are:

- deterministic,
- CI-safe,
- meaningful (not placeholder-only),
- broad enough to protect behavior and architecture constraints.

## Required Test Levels

### Unit tests

Each module under `src/` should have direct tests for normal behavior and edge cases.

### Meta-tests

Meta-tests verify test-system quality itself, including:

- required files exist,
- test files contain assertions,
- lint/type configuration is present,
- repository quality gates are enforced.

### Integration checks

Where modules interact (for example provider adapters and chat APIs), include integration-style tests
with mocks/fakes to cover failure branches.

## Quality Gates

All pull requests should pass:

- `ruff` checks,
- `mypy` checks,
- full `pytest` suite,
- coverage requirements.

If a gate fails, treat it as a merge blocker.

## Test Authoring Rules

1. Use explicit assertions that verify outcomes, not just execution.
2. Prefer small, focused tests with clear names.
3. Mock external dependencies (network, external services) to keep tests deterministic.
4. Use `tmp_path` for filesystem tests and avoid destructive operations.
5. Skip optional-tool tests when the tool is unavailable, and state why.

## Coverage Policy

Current policy target is full line coverage for `src/`.
When you add new lines, add or update tests in the same change.

## CI and Local Workflow

Before pushing, run:

- `python -m ruff check src tests`
- `python -m mypy src tests`
- `pytest -q`

CI will run equivalent checks and should produce the same outcome.

## Troubleshooting Checklist

If tests fail in CI but pass locally:

1. confirm dependency versions,
2. rerun with a clean virtual environment,
3. check for non-determinism (time, ordering, async race, filesystem assumptions),
4. verify platform differences (path separators, line endings).
