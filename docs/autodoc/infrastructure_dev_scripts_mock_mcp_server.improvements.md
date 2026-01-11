# Improvements: `mock_mcp_server.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.
- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Contains bare `except:` clause (catches SystemExit / KeyboardInterrupt).
- Function `main` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `infrastructure\dev\scripts\mock_mcp_server.py`