# Description: `agent.py`

## Module purpose

Repository-level agent orchestrator.

`agent.py` coordinates multiple sub-agents over a repo: reading files,
invoking backend-driven improvements, and emitting markdown reports.

## Location

- Path: `src/agent.py`

## Public surface

- Class: `Agent`
- Functions: `setup_logging`, `load_codeignore`, `main`

## Behavior summary

- CLI entrypoint via `main()` (uses `argparse`).
- Executes external commands via `subprocess`.
- Loads a markdown post-processor dynamically (`fix/fix_markdown_lint.py`) and
 applies it when writing `*.md` reports.

## Optional dependencies

- `requests` (webhook delivery)
  - Availability flag: `HAS_REQUESTS`
  - When unavailable, webhook sending is skipped safely.
- `tqdm` (progress display)
  - Availability flag: `HAS_TQDM`
  - When unavailable, a typed fallback `tqdm()` returns the input iterable.

## Notes on typing

- Uses typed empty-container factories for dataclass defaults to avoid
 `list[Unknown]` / `dict[Unknown, Unknown]` propagation in static analysis.

## File fingerprint

- SHA256(source): `b3057336af81ed1c175eeb6c3e85a750628593a77361ae43ff4f0f09f258aee0`
