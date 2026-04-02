# dev-tools-structure — Think Notes

_Status: COMPLETE_

## Problem
`src/tools/__init__.py` silently swallowed import errors with a bare `except Exception: pass`. This made debugging tool registration failures invisible. Additionally, `common` was auto-imported (it is a helper, not a tool provider) and `pm` subpackage modules were not enumerated by `pkgutil.iter_modules` (subpackages skipped with `if ispkg: continue`).

## Analysis
The `__init__.py` auto-import loop serves as a registration trampoline. By adding `logging.getLogger` and emitting a `DEBUG` log on failure, operators running with `--log-level DEBUG` can discover broken tools without crashing the package import.

## Decision
- Add copyright + `logging` support.
- Add `"common"` to the skip set (it's a shared util, not a tool).
- Keep `pm` as-is (it handles its own imports via `from . import ...`).
- Add 3 new structure tests to lock in the presence of required files.
