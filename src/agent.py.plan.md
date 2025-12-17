# agent.py plan

## Purpose

Coordinate per-file improvement by invoking the specialized agents in this folder.

## CLI flags

- `--dir`: directory to scan (default `.`)
- `--loop`: number of passes (default `1`)
- `--agents-only`: limit processing to `scripts/agent/`
- `--max-files`: cap number of discovered files

## File filtering

- Candidate files are selected by `Agent.SUPPORTED_EXTENSIONS`.
- Ignore patterns come from `.codeignore`.

## Workflow

1. Discover code files (apply ignore patterns, then apply `--max-files`).
2. Update stats (`agent-stats.py`).
3. If a matching legacy test file exists (`scripts/agent/test_<stem>.py`), it can be run by path.
4. Refresh documentation artifacts (`*.description.md`, `*.errors.md`, `*.improvements.md`, `*.changes.md`) via the corresponding sub-agents.
5. Apply code changes via `agent-coder.py`.

## Notes

- Sub-agents may call external CLIs (`copilot`, `gh`, `git`); code and tests should use safe fallbacks.
- The repo now includes stable agent unit tests under `tests/` plus legacy script tests under `scripts/agent/test_*.py`.
