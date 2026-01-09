# Improvements: `ModuleLoader.py`

## Suggested improvements

- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports.
- Avoid broad `except:` or `except Exception:`; catch specific errors.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\classes\test_utils\ModuleLoader.py`