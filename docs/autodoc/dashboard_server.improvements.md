# Improvements: `dashboard_server.py`

## Suggested improvements

- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Function `__init__` is missing type annotations.
- Function `disconnect` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\interface\ui\gui\dashboard_server.py`