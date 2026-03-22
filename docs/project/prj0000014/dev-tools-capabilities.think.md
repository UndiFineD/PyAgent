# dev-tools-capabilities — Think

_Status: COMPLETE_
_Thinker: @2think | Updated: 2026-03-22_

## Problem Statement
PyAgent needed a comprehensive toolkit of development utilities — things every
real-world agent workflow touches: git operations, remote file transfer, TLS
certificate inspection, IP calculations, connectivity tests, NGINX config
verification, proxy testing, port forwarding, port knocking, and project
bootstrapping.

## Key Constraints
- Each utility is a standalone module with a `main()` CLI entry point.
- **No `shell=True`** with user-supplied input (injection risk).
- Minimal external dependencies — prefer Python stdlib.
- All modules must pass import and API tests in CI without network access.

## Options Explored

### Option A — Monolithic `capabilities.py`
All utilities in one file.
**Risk:** File grows unbounded; difficult to test in isolation; import cost.

### Option B — One module per capability (SELECTED)
Each capability (`git_utils`, `remote`, `ssl_utils`, etc.) is its own module
with a focused API and a `main()` CLI entrypoint.
**Benefit:** Testable in isolation; clear ownership; easy to extend.

### Option C — External CLI tools (click, typer)
Use `click` or `typer` for CLI.
**Risk:** Adds external deps; complicates the venv in CI.

## Security Decisions
- `remote.py`: uses explicit argument lists in `subprocess.run()` — no `shell=True`.
- `ssl_utils.py`: uses stdlib `ssl` + `socket` for cert inspection — no eval/exec.
- `plugin_loader.py` (prj0000013): allowlist-only import.

## Decision
Option B: one focused module per capability. Stdlib-first, no shell=True anywhere.
