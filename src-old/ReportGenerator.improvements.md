# Improvements: `ReportGenerator.py`

## Suggested improvements

- Add `--help` examples and validate CLI args (paths, required files).
- Add robust subprocess error handling (`check=True`, timeouts, clearer stderr reporting).
- Avoid `sys.path.insert(...)` imports; prefer a proper package layout or relative imports.
- Avoid broad `except:` or `except Exception:`; catch specific errors.
- Contains TODO or FIXME comments.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\classes\reports\ReportGenerator.py`