# Improvements: `run_fleet_self_improvement.py`

## Suggested improvements

- Add `--help` examples and validate CLI args (paths, required files).
- Add a concise module docstring describing purpose / usage.
- Consider using `logging` instead of `print` for controllable verbosity.
- Function `consult_external_models` is missing type annotations.
- Function `main` is missing type annotations.
- Function `run_cycle` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `infrastructure\dev\scripts\run_fleet_self_improvement.py`