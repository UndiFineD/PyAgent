# Improvements: `RunnerBackends.py`

## Suggested improvements

- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting).
- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Consider documenting class construction / expected invariants.
- Function `try_codex_cli` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `infrastructure\backend\RunnerBackends.py`