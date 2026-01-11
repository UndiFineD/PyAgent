# Improvements: `ConnectivityManager.py`

## Suggested improvements

- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Function `__new__` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\core\base\ConnectivityManager.py`