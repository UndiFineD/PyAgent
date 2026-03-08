# Improvements: `ConfigurationManager.py`

## Suggested improvements

- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Function `__init__` is missing type annotations.
- Function `get` is missing type annotations.
- Function `load` is missing type annotations.
- Function `save` is missing type annotations.
- Function `set` is missing type annotations.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\classes\gui\ConfigurationManager.py`