# Errors: `agent_test_utils.py`

This file documents realistic failure modes and limitations for
`src/agent_test_utils.py`.

## Import and module-loading risks

- Legacy helpers mutate interpreter state:
  - `agent_dir_on_path()` and `agent_sys_path()` temporarily modify `sys.path`.
    Tests that run in parallel or rely on import ordering may be affected if
    these context managers are misused.
- Dynamic imports execute module code:
  - `load_module_from_path()` and `load_agent_module()` execute the target file.
    Any side effects in that module will run at import time.

## Optional dependencies

- `numpy`:
  - Imported best-effort; parts of the module may behave differently when `numpy`
    is not installed.

## Filesystem operations

- Utilities that create temp directories or copy files may raise on:
  - permission errors
  - locked files on Windows
  - long path / invalid character issues
  - cleanup failures (best-effort cleanup swallows exceptions in a few places)

## Threading and timing

- Some helpers use `threading` and time-based behavior; flaky timing and
  concurrency hazards are possible in heavily parallel test runs.
