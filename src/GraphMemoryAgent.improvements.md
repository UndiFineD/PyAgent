# Improvements: `GraphMemoryAgent.py`

## Suggested improvements

- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Contains bare `except:` clause (catches SystemExit / KeyboardInterrupt).
- Function `_save_bead` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\classes\specialized\GraphMemoryAgent.py`